"""Adversarial non-TeX tests for the Classical RTL receipt build gate."""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_classical_rtl_closure_receipt as validator


ROOT = Path(__file__).resolve().parents[2]
INNER = ROOT / "build/BUILD_CLASSICAL_ARABIC_EASTERN_RTL_INNER.ps1"
CURRENT = ROOT / "evidence/classical/RTL_MATH_PROBE_V7_PRIVATE_CACHE_20260908.json"
HISTORICAL = ROOT / "evidence/classical/RTL_RUNTIME_CLOSURE_20260905.json"
HISTORICAL_SHA256 = "21F5DC54BCDF249F7C407063ABE78EA9BC601B3EEA37FEFFD20FA2163EDE9F2F"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def upper_identity(path: Path, recorded_path: str) -> dict:
    return {
        "Path": recorded_path,
        "Bytes": path.stat().st_size,
        "SHA256": digest(path),
    }


def lower_identity(path: Path, path_key: str) -> dict:
    return {
        path_key: str(path),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


class ReceiptFixture:
    """Synthetic guarded layout using the actual v7 PDFs/logs, never TeX.

    Its recorder is deliberately small and recomputable, so the ordinary
    current-input branch is tested without depending on mutable MiKTeX caches.
    The real current receipt is separately tested without mocking readback.
    """
    def __init__(self, temporary: str):
        self.root = Path(temporary).resolve()
        self.engine = Path(sys.executable).resolve()
        self.original = validator.read_json(CURRENT)
        self.sources = {}
        for relative in validator.DIRECT_INPUTS:
            path = ROOT / relative
            self.sources[relative] = {
                "bytes": path.stat().st_size,
                "sha256": digest(path),
            }
        self.manifests = {}
        self.guards = {}
        for run_name in ("primary", "replay"):
            self.make_run(run_name)
        self.receipt = self.root / "RTL_RUNTIME_QA.json"
        self.payload = {
            "schema": validator.RECEIPT_SCHEMA,
            "status": "PASS",
            "scope": validator.RECEIPT_SCOPE,
            "visual_acceptance": validator.VISUAL_ACCEPTANCE,
            "sources": self.sources,
            "build_manifests": {
                name: lower_identity(path, "path")
                for name, path in self.manifests.items()
            },
            "guards": {
                name: {
                    **lower_identity(path, "receipt"),
                    "abandoned_mutex_recovered": False,
                }
                for name, path in self.guards.items()
            },
            "direction_traces": copy.deepcopy(self.original["direction_traces"]),
            "recorder": {},
            "artifacts": copy.deepcopy(self.original["artifacts"]),
            "deterministic_replay": True,
            "extracted_alphanumeric_inventory_equal_by_probe": True,
            "visible_directional_faces_checked_without_per_symbol_actualtext": True,
            "all_p01_p20_geometry_checked": True,
            "links_and_named_destinations_checked": True,
            "font_embedding_and_tounicode_checked": True,
            "limitations": validator.EXPECTED_LIMITATIONS,
            "failures": [],
        }
        contract = validator.load_readback_contract(ROOT)
        for name, other in (("primary", "replay"), ("replay", "primary")):
            self.payload["recorder"][name] = {
                job: contract.validate_fls(
                    self.manifests[name].parent, ROOT,
                    validator.read_json(self.manifests[name]), job,
                    self.manifests[other].parent,
                ) for job in ("control", "rtl")
            }
        self.write_receipt()

    def make_run(self, run_name: str) -> None:
        directory = self.root / run_name
        directory.mkdir()
        inputs = [
            {
                "Path": relative,
                "Bytes": self.sources[relative]["bytes"],
                "SHA256": self.sources[relative]["sha256"],
            }
            for relative in validator.DIRECT_INPUTS
        ]
        jobs = {}
        fingerprint = f"aux={'A' * 64};out={'B' * 64}"
        for job_name in ("control", "rtl"):
            original_directory = Path(
                self.original["build_manifests"][run_name]["path"]
            ).parent
            passes = []
            for number in (1, 2):
                terminal = directory / f"{job_name}-pass-{number}.terminal.txt"
                log = directory / f"{job_name}-pass-{number}.log"
                terminal.write_text("terminal\n", encoding="utf-8")
                log.write_text("log\n", encoding="utf-8")
                passes.append({
                    "Pass": number,
                    "ExitCode": 0,
                    "Terminal": upper_identity(terminal, terminal.name),
                    "Log": upper_identity(log, log.name),
                    "Diagnostics": [],
                    "StateFingerprint": fingerprint,
                })
            outputs = []
            for suffix in validator.REQUIRED_PRODUCTS:
                output = directory / f"{job_name}.{suffix}"
                if suffix in {"pdf", "log"}:
                    output.write_bytes(
                        (original_directory / f"{job_name}.{suffix}").read_bytes()
                    )
                elif suffix == "fls":
                    recorder_inputs = (
                        f"tmp/pdfs/classical-rtl-math-probe/{job_name}.tex",
                        "tmp/pdfs/classical-rtl-math-probe/common.tex",
                        "source/locale/ar-classical/open-logic-rtl-math.tex",
                        "source/sty/open-logic.sty", "source/sty/open-logic-defer.sty",
                        "source/open-logic-envs.sty", "source/locale/ar/open-logic-config.sty",
                    )
                    lines = [f"INPUT {ROOT / name}" for name in recorder_inputs]
                    cache = directory / "texmf-cache/luatex-cache/generic/fonts/otl/fixture.luc"
                    cache.parent.mkdir(parents=True, exist_ok=True)
                    cache.write_bytes(b"synthetic cache input; never executed by these tests\n")
                    lines.append(f"INPUT {cache}")
                    lines += [f"OUTPUT {directory / (job_name + '.' + ending)}"
                              for ending in ("aux", "out", "log", "pdf")]
                    lines += [f"OUTPUT {directory / 'texmf-cache/m_t_x_t_e_s_t.tmp'}"]
                    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
                else:
                    output.write_bytes(f"{job_name}-{suffix}\n".encode("ascii"))
                outputs.append(upper_identity(output, output.name))
            source = ROOT / f"tmp/pdfs/classical-rtl-math-probe/{job_name}.tex"
            jobs[job_name] = {
                "Source": str(source),
                "Arguments": [
                    "-interaction=nonstopmode", "-halt-on-error",
                    "-file-line-error", "-recorder",
                    f"-output-directory={directory}", str(source),
                ],
                "Passes": passes,
                "Converged": True,
                "StablePass": 2,
                "Outputs": outputs,
            }
        manifest = {
            "Schema": validator.BUILD_SCHEMA,
            "Status": "PASS",
            "StartedAtUtc": "2026-09-05T00:00:04Z",
            "FinishedAtUtc": "2026-09-05T00:00:06Z",
            "OutputDirectory": str(directory),
            "WorkingDirectory": str(ROOT / "source/locale/ar"),
            "Engine": upper_identity(self.engine, str(self.engine)),
            "GuardInvocation": {
                "Command": str(self.engine),
                "Arguments": [
                    "-NoProfile", "-File",
                    str(ROOT / "tmp/pdfs/classical-rtl-math-probe/BUILD_PROBE.ps1"),
                    "-OutputDirectory", str(directory),
                ],
                "WorkingDirectory": str(self.root),
            },
            "Environment": {
                "SOURCE_DATE_EPOCH": "1783874174",
                "FORCE_SOURCE_DATE": "1",
                "TZ": "UTC",
                "TEXINPUTS": f"{directory};",
                "TEMP": str(directory),
                "TMP": str(directory),
                "TEXMFCACHE": str(directory / "texmf-cache"),
            },
            "MaximumPasses": 4,
            "RequiredProducts": validator.REQUIRED_PRODUCTS,
            "ConvergenceState": validator.CONVERGENCE_STATE,
            "InputsCapturedAtUtc": "2026-09-05T00:00:05Z",
            "Inputs": inputs,
            "Jobs": jobs,
        }
        manifest_path = directory / "BUILD_MANIFEST.json"
        write_json(manifest_path, manifest)
        guard_path = directory.parent / f"{directory.name}-TEX_MUTEX_RECEIPT.json"
        guard = {
            "Schema": validator.GUARD_SCHEMA,
            "Mutex": validator.MUTEX_NAME,
            "Acquired": True,
            "AbandonedMutexRecovered": False,
            "StartedAtUtc": "2026-09-05T00:00:00Z",
            "Status": "PASS",
            "Containment": validator.CONTAINMENT,
            "OutputTransport": validator.OUTPUT_TRANSPORT,
            "AcquiredAtUtc": "2026-09-05T00:00:01Z",
            "Command": str(self.engine),
            "WorkingDirectory": str(self.root),
            "Tree": {
                "RootProcessId": 123,
                "AssignedBeforeResume": True,
                "CreatedSuspendedAtUtc": "2026-09-05T00:00:02Z",
                "ResumedAtUtc": "2026-09-05T00:00:03Z",
                "RootExitedAtUtc": "2026-09-05T00:00:07Z",
                "RootExitCode": 0,
                "TreeEmptyAtUtc": "2026-09-05T00:00:08Z",
                "FinalActiveProcesses": 0,
                "TotalProcesses": 3,
                "PeakObservedActiveProcesses": 2,
                "TerminationRequested": False,
                "TerminationRequestedAtUtc": None,
                "JobClosedAtUtc": "2026-09-05T00:00:09Z",
                "DrainVerified": True,
            },
            "FinishedAtUtc": "2026-09-05T00:00:10Z",
            "ExitCode": 0,
        }
        write_json(guard_path, guard)
        guarded_time = validator.utc("2026-09-05T00:00:05Z", "fixture time").timestamp()
        for member in directory.iterdir():
            os.utime(member, (guarded_time, guarded_time))
        self.manifests[run_name] = manifest_path
        self.guards[run_name] = guard_path

    def write_receipt(self) -> None:
        write_json(self.receipt, self.payload)
        newest = max(
            [path.stat().st_mtime_ns for path in self.manifests.values()]
            + [path.stat().st_mtime_ns for path in self.guards.values()]
            + [(ROOT / relative).stat().st_mtime_ns
               for relative in validator.DIRECT_INPUTS]
        )
        os.utime(self.receipt, ns=(newest + 1, newest + 1))


class ClassicalRTLClosureReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.fixture = ReceiptFixture(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_ordinary_current_inventory_v7_receipt_passes_without_tex(self):
        result = validator.validate_receipt(ROOT, self.fixture.receipt)
        self.assertEqual(result["transitive_inventory_binding"], "current-input-bytes")
        self.assertEqual(result["historical_inventory_differences"], [])
        self.assertEqual(result["visible_semantic_checks_recomputed"],
                         {"control": 14, "rtl": 14})

    def test_actual_primary_and_replay_v7_receipt_passes_with_current_input_readback(self):
        result = validator.validate_receipt(ROOT, CURRENT)
        self.assertEqual(result["scope"], "isolated-probe-only")
        self.assertEqual(result["unique_pdfs_recomputed"], 2)
        self.assertEqual(result["replay_pdfs_independently_byte_checked"], 2)
        self.assertEqual(result["transitive_inventory_binding"], "current-input-bytes")
        self.assertEqual(result["historical_inventory_differences"], [])
        self.assertEqual(result["visible_semantic_checks_recomputed"],
                         {"control": 14, "rtl": 14})
        self.assertEqual(result["limitations"], validator.EXPECTED_LIMITATIONS)

    def test_exact_historical_v6_receipt_cannot_pass_current_reader_gate(self):
        self.assertEqual(digest(HISTORICAL), HISTORICAL_SHA256)
        with self.assertRaisesRegex(validator.ValidationError, "exact v7 schema"):
            validator.validate_receipt(ROOT, HISTORICAL)

    def test_duplicate_json_key_is_rejected(self):
        text = self.fixture.receipt.read_text(encoding="utf-8")
        text = text.replace('  "status": "PASS",',
                            '  "status": "PASS",\n  "status": "PASS",', 1)
        self.fixture.receipt.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(validator.ValidationError,
                                    "duplicate JSON key: status"):
            validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_false_runtime_predicate_is_rejected(self):
        self.fixture.payload["artifacts"]["replay"]["rtl"][
            "geometry"
        ]["all_probe_regions_covered"] = False
        self.fixture.write_receipt()
        with self.assertRaisesRegex(validator.ValidationError,
                                    "runtime boolean is not true"):
            validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_schema_scope_and_replay_claim_are_exact(self):
        cases = (
            ("schema", "openlogic-classical-rtl-math-runtime-probe-v5",
             "exact v7 schema"),
            ("schema", "openlogic-classical-rtl-math-runtime-probe-v6",
             "exact v7 schema"),
            ("scope", "complete-reader", "receipt scope"),
            ("deterministic_replay", False, "deterministic_replay"),
        )
        original = copy.deepcopy(self.fixture.payload)
        for field, value, message in cases:
            with self.subTest(field=field):
                self.fixture.payload = copy.deepcopy(original)
                self.fixture.payload[field] = value
                self.fixture.write_receipt()
                with self.assertRaisesRegex(validator.ValidationError, message):
                    validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_nonempty_failures_are_rejected(self):
        self.fixture.payload["failures"] = ["probe failed"]
        self.fixture.write_receipt()
        with self.assertRaisesRegex(validator.ValidationError,
                                    "failures are not empty"):
            validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_current_source_hash_drift_is_rejected(self):
        relative = "source/locale/ar-classical/open-logic-rtl-math.tex"
        self.fixture.payload["sources"][relative]["sha256"] = "0" * 64
        self.fixture.write_receipt()
        with self.assertRaisesRegex(validator.ValidationError,
                                    "open-logic-rtl-math.tex hash"):
            validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_manifest_hash_drift_is_rejected(self):
        path = self.fixture.manifests["replay"]
        path.write_text(path.read_text(encoding="utf-8") + " ", encoding="utf-8")
        with self.assertRaisesRegex(validator.ValidationError,
                                    "replay manifest identity (byte count|hash)"):
            validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_guard_hash_drift_is_rejected(self):
        path = self.fixture.guards["primary"]
        path.write_text(path.read_text(encoding="utf-8") + " ", encoding="utf-8")
        with self.assertRaisesRegex(validator.ValidationError,
                                    "primary guard identity (byte count|hash)"):
            validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_receipt_predating_guarded_builds_is_rejected(self):
        os.utime(self.fixture.receipt, ns=(1, 1))
        with self.assertRaisesRegex(validator.ValidationError,
                                    "isolated RTL receipt predates guarded builds"):
            validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_identical_byte_source_touch_is_allowed_without_changing_real_file(self):
        real_stat = Path.stat
        target = ROOT / "source/locale/ar/open-logic-config.sty"
        newer = self.fixture.receipt.stat().st_mtime + 3600

        def touched(path, *args, **kwargs):
            observed = real_stat(path, *args, **kwargs)
            if path == target:
                fields = list(observed)
                fields[8] = newer
                return os.stat_result(fields)
            return observed

        with mock.patch.object(Path, "stat", touched):
            result = validator.validate_receipt(ROOT, self.fixture.receipt)
        self.assertEqual(result["transitive_inventory_binding"], "current-input-bytes")

    def test_forged_nested_geometry_counts_are_rejected(self):
        for field in ("directional_faces_checked", "invariant_faces_checked",
                      "transformed_tableau_nodes_checked_by_face_topology_and_visual_audit"):
            with self.subTest(field=field):
                original = self.fixture.payload["artifacts"]["primary"]["control"]["geometry"][field]
                self.fixture.payload["artifacts"]["primary"]["control"]["geometry"][field] = original + 1
                self.fixture.write_receipt()
                with self.assertRaisesRegex(validator.ValidationError, "primary/control PDF facts"):
                    validator.validate_receipt(ROOT, self.fixture.receipt)
                self.fixture.payload["artifacts"]["primary"]["control"]["geometry"][field] = original

    def test_forged_direction_and_type_confusion_are_rejected(self):
        trace = self.fixture.payload["direction_traces"]["primary"]["rtl"]
        trace["begin-document"]["primitive"] = True
        self.fixture.write_receipt()
        with self.assertRaisesRegex(validator.ValidationError, "primary/rtl direction traces"):
            validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_forged_recorder_count_is_rejected(self):
        self.fixture.payload["recorder"]["primary"]["control"]["input_count"] += 1
        self.fixture.write_receipt()
        with self.assertRaisesRegex(validator.ValidationError, "primary/control recorder"):
            validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_current_receipt_cannot_use_historical_inventory_exception(self):
        self.fixture.payload["recorder"]["primary"]["control"]["input_inventory_sha256"] = "0" * 64
        self.fixture.write_receipt()
        with self.assertRaisesRegex(validator.ValidationError, "primary/control recorder"):
            validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_even_whitespace_changed_original_cannot_use_historical_exception(self):
        self.fixture.receipt.write_bytes(HISTORICAL.read_bytes() + b" ")
        self.assertNotEqual(digest(self.fixture.receipt), HISTORICAL_SHA256)
        with self.assertRaisesRegex(validator.ValidationError, "exact v7 schema"):
            validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_forged_pdf_facts_and_missing_regions_are_rejected(self):
        original = copy.deepcopy(self.fixture.payload)
        mutations = (
            lambda artifact: artifact.__setitem__("pages", 9),
            lambda artifact: artifact["geometry_anchors"].pop("P20-fallback-nvdash"),
            lambda artifact: artifact["geometry_anchors"]["P01-arrow"].__setitem__("logical_text", "→"),
            lambda artifact: artifact["geometry_anchors"]["P01-arrow"]["rect"].__setitem__(0, 0.0),
            lambda artifact: artifact["internal_destination_pages"].__setitem__("probe-eq-one", 2),
            lambda artifact: artifact["font_facts"][0].__setitem__("embedded", "no"),
            lambda artifact: artifact["font_facts"][0].__setitem__("unicode", "no"),
            lambda artifact: artifact["logical_regions"]["P20"]["required_token_counts"].__setitem__("A", 1),
            lambda artifact: artifact["geometry"]["display_tag_policy"]["align"].__setitem__("physical_side", "right"),
            lambda artifact: artifact["links"].pop(),
        )
        for index, mutate in enumerate(mutations):
            with self.subTest(mutation=index):
                self.fixture.payload = copy.deepcopy(original)
                mutate(self.fixture.payload["artifacts"]["primary"]["rtl"])
                self.fixture.write_receipt()
                with self.assertRaisesRegex(validator.ValidationError, "primary/rtl PDF facts"):
                    validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_stale_pdf_bytes_are_rejected_before_runtime_claims(self):
        path = self.fixture.manifests["replay"].parent / "rtl.pdf"
        path.write_bytes(path.read_bytes() + b" ")
        with self.assertRaisesRegex(validator.ValidationError, "rtl output rtl.pdf byte count"):
            validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_build_member_timestamp_outside_guard_is_rejected(self):
        path = self.fixture.manifests["replay"].parent / "rtl.pdf"
        os.utime(path, (1, 1))
        with self.assertRaisesRegex(validator.ValidationError, "build member outside guard lifecycle"):
            validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_guard_lifecycle_and_captured_process_bounds_remain_strict(self):
        original = validator.read_json(self.fixture.guards["primary"])
        manifest = validator.read_json(self.fixture.manifests["primary"])
        for mutation, message in (
            (lambda guard: guard["Tree"].__setitem__("ResumedAtUtc", "2026-09-05T00:00:09Z"), "guard lifecycle ordering"),
            (lambda guard: guard["Tree"].__setitem__("ResumedAtUtc", "2026-09-05T00:00:05Z"), "outside captured process"),
            (lambda guard: guard["Tree"].__setitem__("DrainVerified", False), "assignment/drain"),
        ):
            with self.subTest(message=message):
                guard = copy.deepcopy(original)
                mutation(guard)
                write_json(self.fixture.guards["primary"], guard)
                with self.assertRaisesRegex(validator.ValidationError, message):
                    validator.validate_guard(self.fixture.guards["primary"], manifest, False)

    def test_pdf_fonts_command_is_bounded_and_never_tex_or_render(self):
        contract = validator.load_readback_contract(ROOT)
        with mock.patch.object(validator.subprocess, "run") as run:
            run.return_value.stdout = "pdffonts version test\n"
            run.return_value.stderr = ""
            self.assertEqual(contract.pdffonts_version(), "pdffonts version test")
        self.assertEqual(run.call_args.args[0], ["pdffonts", "-v"])
        self.assertEqual(run.call_args.kwargs["timeout"], 30)

    def test_inner_build_consumes_gate_before_first_tex_process(self):
        source = INNER.read_text(encoding="utf-8")
        invocation = source.index("& python $rtlClosureValidator")
        first_tex = source.index("& lualatex")
        self.assertLess(invocation, first_tex)
        block = source[invocation:first_tex]
        self.assertIn("--receipt $resolvedRTLClosureReceipt", block)
        self.assertIn("Classical RTL closure receipt preflight failed", block)


if __name__ == "__main__":
    unittest.main()
