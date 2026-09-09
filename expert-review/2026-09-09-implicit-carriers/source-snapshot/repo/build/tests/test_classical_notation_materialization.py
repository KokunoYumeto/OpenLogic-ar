"""Bounded non-TeX tests for the reversible Classical notation overlay."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]

import sys
sys.path.insert(0, str(ROOT / "build"))

import materialize_classical_notation as materializer


POLICY_PATH = ROOT / "evidence/classical/NOTATION_MATERIALIZATION_POLICY.json"
LETTERS_PATH = ROOT / "evidence/classical/LETTER_PRESENTATION_REGISTRY.json"


class UnitMaterializationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        registry = json.loads(LETTERS_PATH.read_text(encoding="utf-8"))
        cls.greek = {
            entry["key"] for entry in registry["entries"]
            if entry["family"] == "greek-variable"
        }

    def classify(self, text, unit="OLP-0001", bom=False):
        occurrences, replacements, summary = materializer.classify_unit(
            unit, text, bom, self.policy, self.greek,
        )
        presented, spans = materializer.apply_replacements(text, replacements)
        inverse = materializer.inverse_reconstruct(presented, replacements, spans)
        self.assertEqual(inverse, text)
        self.assertEqual(summary["untreated_candidates"], 0)
        return occurrences, replacements, presented, summary

    def test_typed_letters_numerals_greek_and_formula_hook(self):
        text = r"$x+Y+12+\Gamma+\alpha+\beta+!A+\formula{B}$"
        occurrences, _, presented, summary = self.classify(text)
        self.assertIn(r"\OLId{latin-ordinary}{x}", presented)
        self.assertIn(r"\OLId{latin-looped}{Y}", presented)
        self.assertIn(r"\OLMathNumeral{12}", presented)
        self.assertIn(r"\OLId{greek-variable}{Gamma}", presented)
        self.assertIn(r"\OLId{greek-variable}{alpha}", presented)
        self.assertIn(r"\beta", presented)
        self.assertIn("!A", presented)
        self.assertIn(r"\formula{B}", presented)
        self.assertEqual(summary["ascii_candidate_scalars"], 6)
        self.assertEqual(summary["greek_candidate_commands"], 3)
        self.assertEqual(
            sum(item.candidate_scalars for item in occurrences), 9,
        )
        by_source = {item.source: item.disposition for item in occurrences}
        self.assertEqual(by_source[r"\beta"], "explicit-international-exemption")

    def test_protected_names_text_styles_keys_and_structural_arguments(self):
        text = (
            r"\[\fn{rank}(x)+\mathrm{ABC}+\text{A1}+"
            r"\begin{array}{cc}y&2\end{array}+ab\]"
        )
        occurrences, _, presented, _ = self.classify(text)
        self.assertIn(r"\fn{rank}", presented)
        self.assertIn(r"\mathrm{ABC}", presented)
        self.assertIn(r"\text{A1}", presented)
        self.assertIn(r"\begin{array}{cc}", presented)
        self.assertIn(r"\OLId{latin-ordinary}{x}", presented)
        self.assertIn(r"\OLId{latin-ordinary}{y}", presented)
        self.assertIn(r"\OLMathNumeral{2}", presented)
        self.assertIn("+ab", presented)
        reasons = [item.reason for item in occurrences
                   if item.disposition == "explicit-international-exemption"]
        self.assertTrue(any("whole-typed-identifier" in reason for reason in reasons))
        self.assertTrue(any("styled whole identifier" in reason for reason in reasons))
        self.assertTrue(any("text-inside-math" in reason for reason in reasons))
        self.assertTrue(any("array column specification" in reason for reason in reasons))
        self.assertTrue(any("multi-letter identifier" in reason for reason in reasons))

    def test_layout_dimensions_are_never_rewritten_as_notation(self):
        text = r"\[x+\hspace{1em}y+\mkern2mu z\]"
        occurrences, _, presented, _ = self.classify(text)
        self.assertIn(r"\hspace{1em}", presented)
        self.assertIn(r"\mkern2mu", presented)
        self.assertNotIn(r"\OLMathNumeral{1}", presented)
        self.assertNotIn(r"\OLMathNumeral{2}", presented)
        self.assertEqual(
            sum(item.candidate_scalars for item in occurrences
                if "dimension" in item.reason), 6,
        )

    def test_row_break_optional_spacing_is_layout_not_notation(self):
        text = r"\[\begin{array}{c}x\\[2ex]y\end{array}\]"
        occurrences, _, presented, _ = self.classify(text)
        self.assertIn(r"\\[2ex]", presented)
        self.assertNotIn(r"\\[\OLMathNumeral{2}ex]", presented)
        self.assertIn(r"\OLId{latin-ordinary}{x}", presented)
        self.assertIn(r"\OLId{latin-ordinary}{y}", presented)
        row_break = [
            item for item in occurrences
            if "row-break spacing" in item.reason
        ]
        self.assertEqual([item.source for item in row_break], ["2", "ex"])
        self.assertEqual(
            sum(item.candidate_scalars for item in row_break), 3,
        )

    def test_reference_specimen_unit_is_explicitly_exempt(self):
        text = r"$A+x+12+\Gamma$"
        occurrences, replacements, presented, _ = self.classify(
            text, unit="OLP-0641",
        )
        self.assertEqual(presented, text)
        self.assertEqual(replacements, [])
        self.assertTrue(all(item.disposition == "explicit-international-exemption"
                            for item in occurrences))

    def test_existing_wrappers_and_parser_anomalies_fail_closed(self):
        with self.assertRaisesRegex(materializer.MaterializationError,
                                    "forbidden wrapper"):
            self.classify(r"$\OLId{latin-ordinary}{x}$")
        with self.assertRaisesRegex(materializer.MaterializationError,
                                    "parser anomalies"):
            self.classify("$x")

    def test_exact_bom_and_crlf_inverse(self):
        text = "$x+12$\r\n"
        _, replacements, presented, _ = self.classify(text, bom=True)
        spans = materializer.apply_replacements(text, replacements)[1]
        inverse = materializer.inverse_reconstruct(presented, replacements, spans)
        raw = materializer.encode_exact(text, True)
        self.assertEqual(materializer.encode_exact(inverse, True), raw)
        self.assertTrue(raw.startswith(b"\xef\xbb\xbf"))
        self.assertIn(b"\r\n", raw)


class ProductionContractTests(unittest.TestCase):
    def test_policy_requires_separate_tree_inverse_and_zero_untreated(self):
        policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        self.assertEqual(policy["schema"], materializer.POLICY_SCHEMA)
        self.assertEqual(
            policy["presentation_tree"]["locale"],
            materializer.PRESENTATION_LOCALE,
        )
        self.assertFalse(policy["global_mathcode_or_catcode_mutation"])
        gate = policy["completion_gate"]
        for phrase in ("722-unit source-closure", "every potentially visible",
                       "inverse reconstruction", "runtime/PDF/visual"):
            self.assertIn(phrase, gate)

    def test_final_mode_cannot_accept_presence_as_source_authority(self):
        source = Path(__file__)
        with self.assertRaisesRegex(materializer.MaterializationError,
                                    "canonical source-closure manifest"):
            materializer.build_payload(
                ROOT,
                POLICY_PATH,
                ROOT / "evidence/classical/BASELINE.json",
                LETTERS_PATH,
                ROOT / "evidence/classical/SET_SYMBOL_MAPPING.json",
                mode="final",
                source_closure=source,
            )


class SourceClosureAdapterTests(unittest.TestCase):
    """Synthetic exact-schema tests; no presentation output is materialized."""

    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.repo = Path(cls.temporary.name)
        cls.baseline_path = cls.repo / materializer.DEFAULT_BASELINE
        cls.closure_path = cls.repo / materializer.DEFAULT_SOURCE_CLOSURE
        cls.audit_path = cls.repo / materializer.DEFAULT_SOURCE_RECONCILIATION_AUDIT
        cls.metadata_path = cls.repo / materializer.DEFAULT_SOURCE_RECONCILIATION_METADATA
        (cls.repo / "build").mkdir(parents=True)
        (cls.repo / "build/validate_classical_overlay.py").write_bytes(b"validator\n")
        units = []
        cls.snapshot_rows = []
        for number in range(1, 723):
            uid = f"OLP-{number:04d}"
            source_path = f"content/unit-{number:04d}.tex"
            msa_relative = f"source/locale/ar/content/unit-{number:04d}.tex"
            classical_relative = f"source/locale/ar-classical/content/unit-{number:04d}.tex"
            msa_raw = f"msa-{number:04d}\n".encode()
            classical_raw = f"classical-{number:04d}\n".encode()
            for relative, raw in ((msa_relative, msa_raw),
                                  (classical_relative, classical_raw)):
                path = cls.repo / Path(relative)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
            msa_sha = materializer.lower_sha256(msa_raw)
            classical_sha = materializer.lower_sha256(classical_raw)
            units.append({
                "id": uid,
                "source_path": source_path,
                "english_sha256": materializer.lower_sha256(source_path.encode()),
                "arabic_path": msa_relative,
                "arabic_sha256": msa_sha,
                "arabic_bytes": len(msa_raw),
                "target_path": classical_relative,
            })
            cls.snapshot_rows.append({
                "id": uid,
                "msa_sha256": msa_sha,
                "msa_bytes": len(msa_raw),
                "classical_sha256": classical_sha,
                "classical_bytes": len(classical_raw),
            })
        cls.write_json(cls.baseline_path, {
            "schema": materializer.BASELINE_SCHEMA,
            "total_units": 722,
            "units": units,
        })
        cls.acceptance_relative = "evidence/classical/FULL_TRANSLATION_ACCEPTANCE_AUDIT.json"
        cls.acceptance_path = cls.repo / cls.acceptance_relative
        cls.preflight_hash = "1" * 64
        cls.acceptance_snapshot_hash = "2" * 64
        cls.write_json(cls.acceptance_path, {
            "schema": materializer.ACCEPTANCE_SCHEMA,
            "release_id": "test-source-closure-release",
            "overall_status": "PASS",
            "source_snapshot": {"snapshot_sha256": cls.acceptance_snapshot_hash},
            "preflight": {"fingerprint_sha256": cls.preflight_hash},
        })
        cls.write_json(cls.metadata_path, {
            "schema": materializer.RECONCILIATION_METADATA_SCHEMA,
            "release_id": "test-source-closure-release",
            "baseline_sha256": materializer.lower_sha256(cls.baseline_path.read_bytes()),
            "acceptance_audit": cls.acceptance_relative,
        })
        for path in materializer.RECONCILIATION_ARTIFACTS.values():
            cls.write_json(cls.repo / path, {"fixture": path})
        cls.write_json(cls.repo / materializer.STATIC_VALIDATION_PATH,
                       {"fixture": "static-validation"})

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    @staticmethod
    def write_json(path: Path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8", newline="\n")

    @classmethod
    def identity(cls, relative: str):
        raw = (cls.repo / relative).read_bytes()
        return {
            "path": relative,
            "sha256": materializer.lower_sha256(raw),
            "bytes": len(raw),
        }

    @classmethod
    def valid_closure(cls):
        baseline = json.loads(cls.baseline_path.read_text(encoding="utf-8"))
        units = []
        for baseline_unit, snapshot in zip(baseline["units"], cls.snapshot_rows,
                                           strict=True):
            units.append({
                "id": baseline_unit["id"],
                "source_path": baseline_unit["source_path"],
                "english_sha256": baseline_unit["english_sha256"],
                "msa": {
                    "path": baseline_unit["arabic_path"],
                    "sha256": snapshot["msa_sha256"],
                    "bytes": snapshot["msa_bytes"],
                    "identity_mode": "frozen-baseline",
                },
                "classical": {
                    "path": baseline_unit["target_path"],
                    "sha256": snapshot["classical_sha256"],
                    "bytes": snapshot["classical_bytes"],
                },
                "correction": None,
                "math_text_declaration": None,
                "formal_repair": None,
                "structural_review": None,
                "unchanged_prose_review": None,
                "semantic_authority": {
                    "authority_ref": "evidence/classical/reviews/all.json#/units/0",
                    "note": "Fixture semantic comparison is closed.",
                },
                "final_static_status": "changed-prose-awaiting-semantic-review",
                "raw_comparison_sha256": "3" * 64,
            })
        authorities = [
            cls.identity(materializer.DEFAULT_SOURCE_RECONCILIATION_METADATA.as_posix()),
            cls.identity(cls.acceptance_relative),
        ]
        return {
            "schema": materializer.CLOSURE_SCHEMA,
            "status": "PASS",
            "release_id": "test-source-closure-release",
            "total_units": 722,
            "source_snapshot_sha256": materializer.canonical_sha256(cls.snapshot_rows),
            "frozen_baseline": cls.identity(materializer.DEFAULT_BASELINE.as_posix()),
            **{
                key: cls.identity(path)
                for key, path in materializer.RECONCILIATION_ARTIFACTS.items()
            },
            "authority_files": authorities,
            "source_acceptance": {
                "source_ranges_ready": True,
                "nonpassing_source_ranges": [],
                "nonintegration_blocker_ids": [],
                "failed_required_verifications": [],
                "overall_status": "PASS",
                "audit_schema": materializer.ACCEPTANCE_SCHEMA,
                "source_snapshot_sha256": cls.acceptance_snapshot_hash,
                "preflight_fingerprint_sha256": cls.preflight_hash,
            },
            "counts": {
                "baseline_units": 722,
                "corrected_msa_units": 0,
                "math_text_units": 0,
                "math_text_items": 0,
                "formal_repair_units": 0,
                "structural_review_units": 0,
                "unchanged_prose_review_units": 0,
                "static_statuses": {"changed-prose-awaiting-semantic-review": 722},
            },
            "checks": {key: True for key in materializer.CLOSURE_CHECKS},
            "units": units,
        }

    @classmethod
    def install(cls, mutate=None, raw_closure=None):
        closure = cls.valid_closure()
        if mutate is not None:
            mutate(closure)
        if raw_closure is None:
            cls.write_json(cls.closure_path, closure)
        else:
            cls.closure_path.write_text(raw_closure, encoding="utf-8", newline="\n")
        output_paths = list(materializer.RECONCILIATION_ARTIFACTS.values()) + [
            materializer.STATIC_VALIDATION_PATH,
            materializer.DEFAULT_SOURCE_CLOSURE.as_posix(),
        ]
        cls.write_json(cls.audit_path, {
            "schema": materializer.RECONCILIATION_AUDIT_SCHEMA,
            "status": "PASS",
            "release_id": "test-source-closure-release",
            "source_snapshot_sha256": materializer.canonical_sha256(cls.snapshot_rows),
            "inputs": {
                "metadata": cls.identity(
                    materializer.DEFAULT_SOURCE_RECONCILIATION_METADATA.as_posix()),
                "validator": cls.identity("build/validate_classical_overlay.py"),
                "frozen_baseline": cls.identity(materializer.DEFAULT_BASELINE.as_posix()),
                "semantic_and_acceptance_authorities": closure["authority_files"],
            },
            "outputs": [cls.identity(path) for path in output_paths],
            "validation": {
                "schema": "openlogic-classical-static-validation-v1",
                "status": "STATIC_CHECKS_SATISFIED",
                "exit_code": 0,
                "selected_units": 722,
                "effective_source_verified_units": 722,
                "counts": closure["counts"]["static_statuses"],
                "corrections_applied": closure["counts"]["corrected_msa_units"],
                "formal_repairs_applied": closure["counts"]["formal_repair_units"],
                "general_reviews_applied": closure["counts"]["unchanged_prose_review_units"],
            },
            "source_acceptance": closure["source_acceptance"],
            "write_policy": "Fixture commit is complete and hash-bound.",
        })
        return closure

    def setUp(self):
        self.install()

    def validate(self):
        return materializer.validate_source_closure(
            self.repo, self.closure_path, self.baseline_path,
        )

    def test_exact_committed_closure_is_accepted(self):
        identity = self.validate()
        self.assertEqual(identity["schema"], materializer.CLOSURE_SCHEMA)
        self.assertEqual(identity["release_id"], "test-source-closure-release")
        self.assertEqual(identity["source_snapshot_sha256"],
                         materializer.canonical_sha256(self.snapshot_rows))

    def test_presence_only_and_malformed_manifests_are_rejected(self):
        self.closure_path.write_text("{}\n", encoding="utf-8")
        with self.assertRaisesRegex(materializer.MaterializationError,
                                    "malformed final source-closure"):
            self.validate()

    def test_pending_manifest_is_rejected(self):
        self.install(lambda value: value.update(
            status="STATIC_PASS_SOURCE_ACCEPTANCE_PENDING"))
        with self.assertRaisesRegex(materializer.MaterializationError,
                                    "pending or non-passing"):
            self.validate()

    def test_pending_unit_record_is_rejected(self):
        def pending(value):
            value["units"][0]["final_static_status"] = "pending-missing"
            value["counts"]["static_statuses"] = {
                "changed-prose-awaiting-semantic-review": 721,
                "pending-missing": 1,
            }
        self.install(pending)
        with self.assertRaisesRegex(materializer.MaterializationError,
                                    "pending or invalid final static status"):
            self.validate()

    def test_duplicate_json_field_is_rejected(self):
        closure = self.valid_closure()
        raw = json.dumps(closure, ensure_ascii=False, indent=2) + "\n"
        raw = raw.replace('  "status": "PASS",',
                          '  "status": "PASS",\n  "status": "PASS",', 1)
        self.closure_path.write_text(raw, encoding="utf-8", newline="\n")
        with self.assertRaisesRegex(materializer.MaterializationError,
                                    "duplicate JSON field"):
            self.validate()

    def test_duplicate_unit_identity_is_rejected(self):
        def duplicate(value):
            value["units"][1]["id"] = value["units"][0]["id"]
        self.install(duplicate)
        with self.assertRaisesRegex(materializer.MaterializationError,
                                    "duplicate, missing, or non-contiguous"):
            self.validate()

    def test_stale_live_source_identity_is_rejected(self):
        def stale(value):
            value["units"][0]["msa"]["sha256"] = "f" * 64
        self.install(stale)
        with self.assertRaisesRegex(materializer.MaterializationError,
                                    "stale MSA source identity"):
            self.validate()

    def test_stale_linked_artifact_is_rejected(self):
        path = self.repo / next(iter(materializer.RECONCILIATION_ARTIFACTS.values()))
        path.write_bytes(path.read_bytes() + b"drift\n")
        with self.assertRaisesRegex(materializer.MaterializationError,
                                    "stale baseline correction overlay identity"):
            self.validate()


if __name__ == "__main__":
    unittest.main()
