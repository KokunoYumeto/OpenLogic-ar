#!/usr/bin/env python3
"""Validate the isolated Classical RTL-math receipt before a reader build.

This consumer deliberately does not rerun TeX.  It accepts only the exact v7
receipt contract and binds that receipt to the current repository inputs and
to the primary/replay manifests and machine-wide mutex receipts that produced
the isolated probe. It re-reads the bound logs, recorder files and existing
PDFs, including the eight delimiter faces and six tableau node orders; no
success flag or nested measurement is accepted on assertion alone. Historical
v6 receipts cannot establish this stronger current reader preflight.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys


RECEIPT_SCHEMA = "openlogic-classical-rtl-math-runtime-probe-v7"
# The executable readback contract is the actual audited v7 producer, not a
# caller-supplied module with a conveniently matching schema string. A future
# contract revision must deliberately update this pin and its adversarial tests.
PRODUCER_SHA256 = "BD3657A6D100EA3DC24FD79383DFA3F273AFC0C1255E6030A7C9E1BBCE3D9D6E"
# This current gate has no historical inventory exception. The exact v6
# consumer is preserved under evidence/classical/rtl-history/
# before-v7-reader-gate-20260908 for historical interpretation only.
FONT_COMMAND_TIMEOUT_SECONDS = 30
EXPECTED_LIMITATIONS = [
    "This receipt validates an isolated ten-page fixture, not the 722-unit reader.",
    "Visual inspection is outside this deterministic receipt; no visual-review claim is made.",
    "Canonical formula tokens are bound by source hashes; no structured formula-level ActualText is supplied.",
]
RECEIPT_SCOPE = "isolated-probe-only"
VISUAL_ACCEPTANCE = "NOT_CLAIMED_BY_THIS_DETERMINISTIC_RECEIPT"
BUILD_SCHEMA = "openlogic-classical-rtl-math-probe-build-v1"
GUARD_SCHEMA = "interlanguage-tex-mutex/v2"
MUTEX_NAME = r"Global\InterlanguageTeXSlotV1"
CONTAINMENT = (
    "Windows Job Object; atomic job assignment; suspended start; "
    "kill-on-close; no breakaway"
)
OUTPUT_TRANSPORT = (
    "inherited native standard handles (outer-process redirection supported)"
)
DIRECT_INPUTS = (
    "tmp/pdfs/classical-rtl-math-probe/common.tex",
    "tmp/pdfs/classical-rtl-math-probe/control.tex",
    "tmp/pdfs/classical-rtl-math-probe/rtl.tex",
    "tmp/pdfs/classical-rtl-math-probe/BUILD_PROBE.ps1",
    "tmp/pdfs/classical-rtl-math-probe/RUN_PROBE.ps1",
    "tmp/pdfs/classical-rtl-math-probe/cache-seed/SEED_MANIFEST.json",
    "source/locale/ar-classical/open-logic-rtl-math.tex",
    "source/sty/open-logic.sty",
    "source/sty/open-logic-defer.sty",
    "source/open-logic-envs.sty",
    "source/locale/ar/open-logic-config.sty",
    "build/qa_classical_rtl_math_probe.py",
    "build/Invoke-WithInterlanguageTeXMutex.ps1",
    "build/InterlanguageTeXCapturedTree.cs",
    "00_control/fonts/scheherazade-2.100/Scheherazade-Regular.ttf",
    "00_control/fonts/scheherazade-2.100/Scheherazade-Bold.ttf",
)
REQUIRED_PRODUCTS = ["aux", "out", "fls", "log", "pdf"]
CONVERGENCE_STATE = ["aux", "out", "toc", "lof", "lot", "loe"]
KNOWN_DIAGNOSTICS = {
    "MissingGlyph", "OverfullHBox", "OverfullVBox", "UndefinedReference",
    "UndefinedCitation", "MultiplyDefined", "Rerun", "Fatal",
}
RUNTIME_FLAGS = (
    "deterministic_replay",
    "extracted_alphanumeric_inventory_equal_by_probe",
    "visible_directional_faces_checked_without_per_symbol_actualtext",
    "all_p01_p20_geometry_checked",
    "links_and_named_destinations_checked",
    "font_embedding_and_tounicode_checked",
)
RECEIPT_KEYS = {
    "schema", "status", "scope", "visual_acceptance", "sources",
    "build_manifests", "guards", "direction_traces", "recorder",
    "artifacts", *RUNTIME_FLAGS, "limitations", "failures",
}
BUILD_KEYS = {
    "Schema", "Status", "StartedAtUtc", "FinishedAtUtc", "OutputDirectory",
    "WorkingDirectory", "Engine", "GuardInvocation", "Environment",
    "MaximumPasses", "RequiredProducts", "ConvergenceState",
    "InputsCapturedAtUtc", "Inputs", "Jobs",
}
GUARD_KEYS = {
    "Schema", "Mutex", "Acquired", "AbandonedMutexRecovered", "StartedAtUtc",
    "Status", "Containment", "OutputTransport", "AcquiredAtUtc", "Command",
    "WorkingDirectory", "Tree", "FinishedAtUtc", "ExitCode",
}
TREE_KEYS = {
    "RootProcessId", "AssignedBeforeResume", "CreatedSuspendedAtUtc",
    "ResumedAtUtc", "RootExitedAtUtc", "RootExitCode", "TreeEmptyAtUtc",
    "FinalActiveProcesses", "TotalProcesses", "PeakObservedActiveProcesses",
    "TerminationRequested", "TerminationRequestedAtUtc", "JobClosedAtUtc",
    "DrainVerified",
}


class ValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def strict_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path: Path) -> dict:
    require(path.is_file(), f"missing JSON file: {path}")
    try:
        value = json.loads(
            path.read_text(encoding="utf-8-sig"), object_pairs_hook=strict_object
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"invalid JSON file {path}: {error}") from error
    require(type(value) is dict, f"JSON root must be an object: {path}")
    return value


def exact_keys(value: object, expected: set[str], label: str) -> dict:
    require(type(value) is dict and set(value) == expected, f"{label} schema")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def valid_digest(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9A-F]{64}", value) is not None


def integer(value: object, minimum: int = 0) -> bool:
    return type(value) is int and value >= minimum


def same_path(one: object, two: object) -> bool:
    if not isinstance(one, (str, os.PathLike)) or not isinstance(two, (str, os.PathLike)):
        return False
    return os.path.normcase(str(Path(one).resolve())) == os.path.normcase(
        str(Path(two).resolve())
    )


def utc(value: object, label: str) -> datetime:
    require(isinstance(value, str), f"{label} timestamp")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValidationError(f"{label} timestamp") from error
    require(result.tzinfo is not None, f"{label} timezone")
    return result.astimezone(timezone.utc)


def validate_identity(record: object, path: Path, path_key: str, bytes_key: str,
                      hash_key: str, recorded_path: str, label: str) -> None:
    exact_keys(record, {path_key, bytes_key, hash_key}, label)
    assert isinstance(record, dict)
    require(record[path_key] == recorded_path, f"{label} path")
    require(path.is_file(), f"{label} missing")
    require(integer(record[bytes_key]) and record[bytes_key] == path.stat().st_size,
            f"{label} byte count")
    require(valid_digest(record[hash_key]) and record[hash_key] == sha256(path),
            f"{label} hash")


def validate_source_map(repo: Path, sources: object) -> list[Path]:
    exact_keys(sources, set(DIRECT_INPUTS), "receipt sources")
    assert isinstance(sources, dict)
    paths = []
    for relative in DIRECT_INPUTS:
        path = repo / Path(relative)
        record = exact_keys(sources[relative], {"bytes", "sha256"},
                            f"receipt source {relative}")
        require(path.is_file(), f"receipt source {relative} missing")
        require(integer(record["bytes"]) and record["bytes"] == path.stat().st_size,
                f"receipt source {relative} byte count")
        require(valid_digest(record["sha256"]) and record["sha256"] == sha256(path),
                f"receipt source {relative} hash")
        paths.append(path)
    return paths


def validate_upper_identity(record: object, path: Path, recorded_path: str,
                            label: str) -> None:
    validate_identity(record, path, "Path", "Bytes", "SHA256", recorded_path, label)


def validate_manifest(path: Path, repo: Path, receipt_sources: dict) -> dict:
    manifest = exact_keys(read_json(path), BUILD_KEYS, "build manifest")
    require(manifest["Schema"] == BUILD_SCHEMA and manifest["Status"] == "PASS",
            "build manifest did not pass")
    directory = path.parent.resolve()
    require(same_path(manifest["OutputDirectory"], directory),
            "build manifest output binding")
    require(same_path(manifest["WorkingDirectory"], repo / "source/locale/ar"),
            "build manifest working directory")
    times = [utc(manifest[key], f"build {key}") for key in
             ("StartedAtUtc", "InputsCapturedAtUtc", "FinishedAtUtc")]
    require(times == sorted(times), "build manifest lifecycle ordering")
    require(manifest["MaximumPasses"] == 4 and
            type(manifest["MaximumPasses"]) is int, "build pass limit")
    require(manifest["RequiredProducts"] == REQUIRED_PRODUCTS,
            "build required products")
    require(manifest["ConvergenceState"] == CONVERGENCE_STATE,
            "build convergence state")
    require(manifest["Environment"] == {
        "SOURCE_DATE_EPOCH": "1783874174", "FORCE_SOURCE_DATE": "1",
        "TZ": "UTC", "TEXINPUTS": f"{directory};",
        "TEMP": str(directory), "TMP": str(directory),
        "TEXMFCACHE": str(directory / "texmf-cache"),
    }, "build deterministic environment")

    engine = exact_keys(manifest["Engine"], {"Path", "Bytes", "SHA256"},
                        "build engine")
    engine_path = Path(engine["Path"])
    require(engine_path.is_absolute(), "build engine path")
    validate_upper_identity(engine, engine_path, str(engine["Path"]), "build engine")

    invocation = exact_keys(manifest["GuardInvocation"],
                            {"Command", "Arguments", "WorkingDirectory"},
                            "build guard invocation")
    build_script = repo / "tmp/pdfs/classical-rtl-math-probe/BUILD_PROBE.ps1"
    require(Path(invocation["Command"]).is_absolute(), "guard command path")
    require(invocation["Arguments"] == [
        "-NoProfile", "-File", str(build_script),
        "-OutputDirectory", str(directory),
    ], "guard command arguments")
    require(isinstance(invocation["WorkingDirectory"], str) and
            Path(invocation["WorkingDirectory"]).is_absolute(),
            "guard working directory")

    inputs = manifest["Inputs"]
    require(type(inputs) is list and len(inputs) == len(DIRECT_INPUTS),
            "build input inventory")
    require([item.get("Path") if isinstance(item, dict) else None for item in inputs]
            == list(DIRECT_INPUTS), "build input order")
    for item, relative in zip(inputs, DIRECT_INPUTS, strict=True):
        validate_upper_identity(item, repo / relative, relative,
                                f"build input {relative}")
        require(item["Bytes"] == receipt_sources[relative]["bytes"] and
                item["SHA256"] == receipt_sources[relative]["sha256"],
                f"receipt/manifest input binding {relative}")

    jobs = exact_keys(manifest["Jobs"], {"control", "rtl"}, "build jobs")
    for job_name in ("control", "rtl"):
        job = exact_keys(jobs[job_name], {
            "Source", "Arguments", "Passes", "Converged", "StablePass", "Outputs",
        }, f"{job_name} build job")
        source = repo / f"tmp/pdfs/classical-rtl-math-probe/{job_name}.tex"
        require(same_path(job["Source"], source), f"{job_name} source")
        require(job["Arguments"] == [
            "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
            "-recorder", f"-output-directory={directory}", str(source),
        ], f"{job_name} engine arguments")
        require(job["Converged"] is True and integer(job["StablePass"], 2) and
                job["StablePass"] <= 4, f"{job_name} convergence")
        passes = job["Passes"]
        require(type(passes) is list and len(passes) == job["StablePass"],
                f"{job_name} pass sequence")
        for index, pass_record in enumerate(passes, 1):
            exact_keys(pass_record, {
                "Pass", "ExitCode", "Terminal", "Log", "Diagnostics",
                "StateFingerprint",
            }, f"{job_name} pass {index}")
            require(pass_record["Pass"] == index and
                    type(pass_record["Pass"]) is int and
                    pass_record["ExitCode"] == 0 and
                    type(pass_record["ExitCode"]) is int,
                    f"{job_name} pass {index} result")
            validate_upper_identity(
                pass_record["Terminal"],
                directory / f"{job_name}-pass-{index}.terminal.txt",
                f"{job_name}-pass-{index}.terminal.txt",
                f"{job_name} pass {index} terminal",
            )
            validate_upper_identity(
                pass_record["Log"], directory / f"{job_name}-pass-{index}.log",
                f"{job_name}-pass-{index}.log", f"{job_name} pass {index} log",
            )
            diagnostics = pass_record["Diagnostics"]
            require(type(diagnostics) is list and
                    len(diagnostics) == len(set(diagnostics)) and
                    all(isinstance(item, str) and item in KNOWN_DIAGNOSTICS
                        for item in diagnostics),
                    f"{job_name} pass {index} diagnostics")
            require(isinstance(pass_record["StateFingerprint"], str) and
                    re.fullmatch(
                        r"(?:aux|out|toc|lof|lot|loe)=[0-9A-F]{64}"
                        r"(?:;(?:aux|out|toc|lof|lot|loe)=[0-9A-F]{64})+",
                        pass_record["StateFingerprint"],
                    ) is not None, f"{job_name} pass {index} fingerprint")
        require(passes[-1].get("Diagnostics") == [] and
                passes[-1].get("StateFingerprint") ==
                passes[-2].get("StateFingerprint"), f"{job_name} final convergence")
        expected_outputs = [f"{job_name}.{suffix}" for suffix in REQUIRED_PRODUCTS]
        expected_outputs += [
            f"{job_name}.{suffix}" for suffix in CONVERGENCE_STATE
            if suffix not in {"aux", "out"} and
            (directory / f"{job_name}.{suffix}").is_file()
        ]
        outputs = job["Outputs"]
        require(type(outputs) is list and
                [item.get("Path") if isinstance(item, dict) else None
                 for item in outputs] == expected_outputs,
                f"{job_name} output inventory")
        for item, name in zip(outputs, expected_outputs, strict=True):
            validate_upper_identity(item, directory / name, name,
                                    f"{job_name} output {name}")
    return manifest


def validate_guard(path: Path, manifest: dict, abandoned: object) -> dict:
    guard = exact_keys(read_json(path), GUARD_KEYS, "guard receipt")
    require(guard["Schema"] == GUARD_SCHEMA and guard["Mutex"] == MUTEX_NAME,
            "guard identity")
    require(guard["Status"] == "PASS" and guard["Acquired"] is True,
            "guard did not pass")
    require(type(abandoned) is bool and
            guard["AbandonedMutexRecovered"] is abandoned,
            "guard abandoned-mutex binding")
    require(guard["Containment"] == CONTAINMENT and
            guard["OutputTransport"] == OUTPUT_TRANSPORT,
            "guard containment/transport")
    require(type(guard["ExitCode"]) is int and guard["ExitCode"] == 0,
            "guard exit code")
    require(same_path(guard["Command"], manifest["GuardInvocation"]["Command"]) and
            same_path(guard["WorkingDirectory"],
                      manifest["GuardInvocation"]["WorkingDirectory"]),
            "guard invocation binding")
    tree = exact_keys(guard["Tree"], TREE_KEYS, "guard tree")
    require(tree["AssignedBeforeResume"] is True and tree["DrainVerified"] is True,
            "guard assignment/drain")
    require(type(tree["RootExitCode"]) is int and tree["RootExitCode"] == 0 and
            type(tree["FinalActiveProcesses"]) is int and
            tree["FinalActiveProcesses"] == 0, "guard process completion")
    require(tree["TerminationRequested"] is False and
            tree["TerminationRequestedAtUtc"] is None, "guard termination")
    require(integer(tree["RootProcessId"], 1) and
            integer(tree["TotalProcesses"], 1) and
            integer(tree["PeakObservedActiveProcesses"], 1) and
            tree["PeakObservedActiveProcesses"] <= tree["TotalProcesses"],
            "guard process accounting")
    lifecycle = [
        utc(guard["StartedAtUtc"], "guard start"),
        utc(guard["AcquiredAtUtc"], "guard acquire"),
        utc(tree["CreatedSuspendedAtUtc"], "guard create"),
        utc(tree["ResumedAtUtc"], "guard resume"),
        utc(tree["RootExitedAtUtc"], "guard root exit"),
        utc(tree["TreeEmptyAtUtc"], "guard tree empty"),
        utc(tree["JobClosedAtUtc"], "guard close"),
        utc(guard["FinishedAtUtc"], "guard finish"),
    ]
    require(lifecycle == sorted(lifecycle), "guard lifecycle ordering")
    require(lifecycle[0] <= utc(manifest["StartedAtUtc"], "build start") <=
            utc(manifest["FinishedAtUtc"], "build finish") <= lifecycle[-1],
            "build lifecycle outside guard")
    require(lifecycle[3] <= utc(manifest["StartedAtUtc"], "build start") <=
            utc(manifest["FinishedAtUtc"], "build finish") <= lifecycle[4],
            "build lifecycle outside captured process")
    return guard


def exact_fact(recorded: object, observed: object, label: str) -> None:
    """Compare the complete fact tree, including JSON number/boolean types."""
    try:
        def canonical(value: object) -> str:
            return json.dumps(value, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":"), allow_nan=False)
        matches = canonical(recorded) == canonical(observed)
    except (TypeError, ValueError) as error:
        raise ValidationError(f"{label} invalid JSON fact: {error}") from error
    require(matches, f"{label} differs from bound-artifact readback")


def load_readback_contract(repo: Path):
    """Load only the pinned producer; never execute its TeX-free main writer."""
    path = repo / "build/qa_classical_rtl_math_probe.py"
    require(sha256(path) == PRODUCER_SHA256, "unsupported v7 producer contract hash")
    spec = importlib.util.spec_from_file_location("_rtl_v7_readback_contract", path)
    require(spec is not None and spec.loader is not None, "v7 readback contract loader")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except ImportError as error:
        raise ValidationError(f"v7 readback dependency unavailable: {error}") from error
    require(module.SCHEMA == RECEIPT_SCHEMA and
            module.DIRECT_INPUTS == DIRECT_INPUTS,
            "v7 readback contract identity")
    # The producer's PDF checks only launch pdffonts. Give those read-only
    # commands a finite timeout here; never dispatch a TeX engine or a renderer.
    def font_command(arguments: list[str]) -> subprocess.CompletedProcess:
        try:
            return subprocess.run(["pdffonts", *arguments], check=True,
                                  capture_output=True, text=True,
                                  encoding="utf-8", errors="strict",
                                  timeout=FONT_COMMAND_TIMEOUT_SECONDS)
        except (OSError, subprocess.SubprocessError, UnicodeError) as error:
            raise ValidationError(f"bounded pdffonts readback failed: {error}") from error

    def fonts_version() -> str:
        completed = font_command(["-v"])
        lines = [line.strip() for line in
                 (completed.stdout + completed.stderr).splitlines() if line.strip()]
        require(bool(lines), "pdffonts version unavailable")
        return lines[0]

    module.pdffonts_version = fonts_version
    module.font_facts = lambda pdf: module.parse_pdffonts(
        font_command([str(pdf)]).stdout, pdf.name
    )
    return module


def validate_bound_runtime_facts(repo: Path, receipt: dict,
                                 manifests: dict, directories: dict,
                                 guards: dict) -> dict:
    """Recompute v7 facts from byte-bound artifacts without rebuilding them.

    Only two unique ten-page PDFs are parsed. The replay files are first
    independently hashed and required to have identical bytes, so their facts
    must then equal the same complete readback. Logs and recorder inventories
    are read separately for every run/job. This is not a new visual review.
    """
    contract = load_readback_contract(repo)
    try:
        for run_name in ("primary", "replay"):
            contract.bind_guard_file_times(directories[run_name],
                                          manifests[run_name], guards[run_name])
        for job in ("control", "rtl"):
            primary_pdf = directories["primary"] / f"{job}.pdf"
            replay_pdf = directories["replay"] / f"{job}.pdf"
            require(primary_pdf.stat().st_size == replay_pdf.stat().st_size and
                    sha256(primary_pdf) == sha256(replay_pdf),
                    f"{job} replay PDF bytes differ")

        fonts_version = contract.pdffonts_version()
        facts, raw_regions, observed_recorder = {}, {}, {}
        for job in ("control", "rtl"):
            # pdf_facts reopens the actual PDF, derives its anchor rectangles
            # from the PDF links, and runs visible_semantic_checks against
            # actual glyph positions. Recorded anchors/expected strings/pass
            # flags are never inputs to that readback.
            facts[job], raw_regions[job] = contract.pdf_facts(
                directories["primary"] / f"{job}.pdf", fonts_version
            )
        for run_name, other_name in (("primary", "replay"), ("replay", "primary")):
            directory = directories[run_name]
            observed_recorder[run_name] = {}
            for job in ("control", "rtl"):
                trace = contract.direction_trace(
                    (directory / f"{job}.log").read_text(encoding="utf-8"), job
                )
                exact_fact(receipt["direction_traces"][run_name][job], trace,
                           f"{run_name}/{job} direction traces")
                exact_fact(receipt["artifacts"][run_name][job], facts[job],
                           f"{run_name}/{job} PDF facts")
                recorder = contract.validate_fls(directory, repo, manifests[run_name],
                                                 job, directories[other_name])
                observed_recorder[run_name][job] = recorder
                exact_fact(receipt["recorder"][run_name][job], recorder,
                           f"{run_name}/{job} recorder")
        for job in ("control", "rtl"):
            one, two = (observed_recorder[name][job]
                        for name in ("primary", "replay"))
            require(one["input_inventory_sha256"] == two["input_inventory_sha256"] and
                    one["outputs"] == two["outputs"],
                    f"{job} replay recorder inventory differs")
        for probe in contract.PROBE_IDS:
            require(Counter(c for c in raw_regions["control"][probe] if c.isalnum()) ==
                    Counter(c for c in raw_regions["rtl"][probe] if c.isalnum()),
                    f"control/RTL extracted alphanumeric inventory differs for {probe}")
        for key in contract.GEOMETRY_KEYS:
            control = facts["control"]["geometry_anchors"][key]["logical_text"]
            rtl = facts["rtl"]["geometry_anchors"][key]["logical_text"]
            require(Counter(c for c in control if c.isalnum()) ==
                    Counter(c for c in rtl if c.isalnum()),
                    f"control/RTL linked alphanumeric content differs: {key}")
            if key in contract.PRESERVED_FACE_KEYS:
                require(control == rtl, f"control/RTL scoped-preservation face differs: {key}")
    except (OSError, ValueError, UnicodeError) as error:
        if isinstance(error, ValidationError):
            raise
        raise ValidationError(f"v7 bound-artifact readback failed: {error}") from error
    return {
        "scope": RECEIPT_SCOPE,
        "unique_pdfs_recomputed": 2,
        "replay_pdfs_independently_byte_checked": 2,
        "visible_semantic_checks_recomputed": {
            job: len(facts[job]["visible_semantic_checks"])
            for job in ("control", "rtl")
        },
        "transitive_inventory_binding": "current-input-bytes",
        "historical_inventory_differences": [],
        "limitations": list(EXPECTED_LIMITATIONS),
    }


def require_no_false_runtime_boolean(value: object, path: str = "receipt") -> None:
    if type(value) is bool:
        require(value, f"runtime boolean is not true: {path}")
    elif type(value) is dict:
        for key, child in value.items():
            if path == "receipt.guards" and key in {"primary", "replay"}:
                # AbandonedMutexRecovered is an observation, not a runtime
                # success predicate; it is cross-bound to the guard below.
                require(type(child) is dict, f"{path}.{key} schema")
                for child_key, grandchild in child.items():
                    if child_key != "abandoned_mutex_recovered":
                        require_no_false_runtime_boolean(
                            grandchild, f"{path}.{key}.{child_key}"
                        )
                continue
            require_no_false_runtime_boolean(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            require_no_false_runtime_boolean(child, f"{path}[{index}]")


def validate_receipt(repo: Path, receipt_path: Path) -> dict:
    repo = repo.resolve()
    receipt_path = receipt_path.resolve()
    require(repo.is_dir(), "repository path")
    require(receipt_path.is_file(), "missing RTL receipt")
    receipt_hash = sha256(receipt_path)
    receipt = exact_keys(read_json(receipt_path), RECEIPT_KEYS, "RTL receipt")
    require(receipt["schema"] == RECEIPT_SCHEMA and receipt["status"] == "PASS",
            "RTL receipt did not pass exact v7 schema")
    require(receipt["scope"] == RECEIPT_SCOPE, "RTL receipt scope")
    require(receipt["visual_acceptance"] == VISUAL_ACCEPTANCE,
            "RTL receipt visual-acceptance contract")
    require(receipt["limitations"] == EXPECTED_LIMITATIONS,
            "RTL receipt limitations")
    require(receipt["failures"] == [], "RTL receipt failures are not empty")
    for flag in RUNTIME_FLAGS:
        require(receipt[flag] is True, f"RTL receipt runtime flag: {flag}")
    for section in ("direction_traces", "recorder", "artifacts"):
        runs = exact_keys(receipt[section], {"primary", "replay"},
                          f"RTL receipt {section}")
        for run_name in ("primary", "replay"):
            exact_keys(runs[run_name], {"control", "rtl"},
                       f"RTL receipt {section} {run_name}")
    require_no_false_runtime_boolean(receipt)

    validate_source_map(repo, receipt["sources"])
    manifest_records = exact_keys(receipt["build_manifests"],
                                  {"primary", "replay"},
                                  "RTL receipt build manifests")
    guard_records = exact_keys(receipt["guards"], {"primary", "replay"},
                               "RTL receipt guards")
    manifests: dict[str, dict] = {}
    directories: dict[str, Path] = {}
    guards: dict[str, dict] = {}
    for run_name in ("primary", "replay"):
        record = exact_keys(manifest_records[run_name],
                            {"path", "bytes", "sha256"},
                            f"{run_name} manifest identity")
        path = Path(record["path"])
        require(path.is_absolute() and path.name == "BUILD_MANIFEST.json",
                f"{run_name} manifest path")
        validate_identity(record, path, "path", "bytes", "sha256", str(path),
                          f"{run_name} manifest identity")
        manifests[run_name] = validate_manifest(path, repo, receipt["sources"])
        directories[run_name] = path.parent.resolve()
    require(directories["primary"] != directories["replay"] and
            not directories["primary"].is_relative_to(directories["replay"]) and
            not directories["replay"].is_relative_to(directories["primary"]),
            "primary/replay build isolation")
    require(manifests["primary"]["Inputs"] == manifests["replay"]["Inputs"] and
            manifests["primary"]["Engine"] == manifests["replay"]["Engine"],
            "primary/replay producer identities differ")

    for run_name in ("primary", "replay"):
        record = exact_keys(guard_records[run_name],
                            {"receipt", "bytes", "sha256",
                             "abandoned_mutex_recovered"},
                            f"{run_name} guard identity")
        path = Path(record["receipt"])
        expected = directories[run_name].parent / (
            f"{directories[run_name].name}-TEX_MUTEX_RECEIPT.json"
        )
        require(path.is_absolute() and same_path(path, expected),
                f"{run_name} guard path")
        require(record["receipt"] == str(path) and path.is_file(),
                f"{run_name} guard identity path")
        require(integer(record["bytes"]) and
                record["bytes"] == path.stat().st_size,
                f"{run_name} guard identity byte count")
        require(valid_digest(record["sha256"]) and
                record["sha256"] == sha256(path),
                f"{run_name} guard identity hash")
        guards[run_name] = validate_guard(path, manifests[run_name],
                                          record["abandoned_mutex_recovered"])

    # Source mtimes are not semantic identities. An identical-byte source
    # touch is admissible only because every direct input was freshly checked
    # above against both manifests and this receipt. Guard/build lifecycle and
    # original build-member times remain independently enforced below.
    require(receipt_path.stat().st_mtime >= max(
        utc(guard["FinishedAtUtc"], "guard finish").timestamp()
        for guard in guards.values()
    ), "isolated RTL receipt predates guarded builds")
    readback = validate_bound_runtime_facts(
        repo, receipt, manifests, directories, guards,
    )
    # Detect input drift during readback too; this never refreshes the receipt.
    validate_source_map(repo, receipt["sources"])
    for run_name in ("primary", "replay"):
        record = manifest_records[run_name]
        path = Path(record["path"])
        validate_identity(record, path, "path", "bytes", "sha256", str(path),
                          f"{run_name} final manifest identity")
        validate_manifest(path, repo, receipt["sources"])
        guard_record = guard_records[run_name]
        guard_path = Path(guard_record["receipt"])
        require(guard_path.stat().st_size == guard_record["bytes"] and
                sha256(guard_path) == guard_record["sha256"],
                f"{run_name} final guard identity")
    require(sha256(receipt_path) == receipt_hash, "RTL receipt changed during readback")
    return readback


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    try:
        readback = validate_receipt(args.repo, args.receipt)
    except (OSError, ValidationError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(json.dumps({
        "schema": RECEIPT_SCHEMA,
        "status": "PASS",
        "receipt": str(args.receipt.resolve()),
        "readback": readback,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
