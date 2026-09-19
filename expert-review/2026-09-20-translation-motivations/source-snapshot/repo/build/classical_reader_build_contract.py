#!/usr/bin/env python3
"""Bind one complete Classical reader build and its guarded deterministic replay.

No TeX is launched here. Preparation happens inside the captured tree, before
TeX; production is recorded as pending; only the outer caller, after the mutex
wrapper has returned, may finalize a PASS against its drained-tree receipt.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import sys

SCHEMA = "openlogic-classical-arabic-reader-build-v2"
INPUT_SCHEMA = "openlogic-classical-reader-build-inputs-v1"
UNIT_COUNT = 722
PDF_ROLES = {
    "canonical-reader-component", "closure-component", "standalone-722-unit-reader"
}
JOBS = (
    "open-logic-complete-ar-classical-eastern-rtl",
    "open-logic-closure-supplement-ar-classical-eastern-rtl",
)
ARTIFACT_ROLES = PDF_ROLES | {
    "reader-source-map", "closure-source-map", "routing-receipt", "assembly-receipt",
    "reader-link-repair-receipt", "closure-link-repair-receipt",
    *(f"{job}-{suffix}" for job in JOBS for suffix in ("log", "fls")),
}
TOOLS = (
    "build/BUILD_CLASSICAL_ARABIC_EASTERN_RTL.ps1",
    "build/BUILD_CLASSICAL_ARABIC_EASTERN_RTL_INNER.ps1",
    "build/classical_reader_build_contract.py",
    "build/Invoke-WithInterlanguageTeXMutex.ps1",
    "build/InterlanguageTeXCapturedTree.cs",
    "build/repair_rtl_link_rects_letter_ar.py",
    "build/repair_rtl_link_rects_ar.py",
    "build/verify_classical_reader_routing.py",
    "build/assemble_classical_722_reader.py",
    "build/assemble_complete_722_reader.py",
    "build/materialize_classical_notation.py",
    "build/validate_classical_rtl_closure_receipt.py",
)
SUPPORT_TREES = ("source/sty", "source/bib", "source/assets",
                 "00_control/fonts/scheherazade-2.100")
SUPPORT_TOPS = ("source", "source/locale/ar", "source/locale/ar-classical",
                "source/locale/ar-classical-presentation")
SUPPORT_SUFFIXES = {".tex", ".sty", ".cls", ".bib", ".bst", ".cfg", ".def",
                    ".lua", ".ltx", ".png", ".jpg", ".jpeg", ".pdf", ".ttf",
                    ".otf", ".eps", ".gin"}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path: Path) -> dict:
    result = json.loads(path.read_text(encoding="utf-8-sig"),
                        object_pairs_hook=strict_object)
    require(type(result) is dict, f"JSON root is not an object: {path}")
    return result


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def utc(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(result.tzinfo is not None, "timestamp has no timezone")
    return result.astimezone(timezone.utc)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def record(path: Path, label: str | None = None) -> dict:
    require(path.is_file(), f"missing bound input/artifact: {path}")
    return {"Path": label or str(path.resolve()), "Bytes": path.stat().st_size,
            "SHA256": sha256(path)}


def verify_record(item: dict, path: Path | None = None) -> None:
    require(set(item) == {"Path", "Bytes", "SHA256"}, "invalid file identity")
    require(type(item["Bytes"]) is int and item["Bytes"] >= 0, "invalid byte count")
    require(re.fullmatch(r"[0-9A-F]{64}", item["SHA256"]) is not None,
            "invalid SHA256")
    path = path or Path(item["Path"])
    require(record(path, item["Path"]) == item, f"identity drift: {item['Path']}")


def repo_path(repo: Path, relative: str) -> Path:
    path = (repo / relative).resolve()
    require(not Path(relative).is_absolute() and path.is_relative_to(repo),
            f"repository input escaped: {relative}")
    return path


def write_new(path: Path, value: dict) -> None:
    # Exclusive creation: no historical receipt or completed product is replaced.
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")


def support_paths(repo: Path) -> list[str]:
    paths = set(TOOLS)
    for relative in SUPPORT_TREES:
        directory = repo_path(repo, relative)
        require(directory.is_dir(), f"missing source support directory: {relative}")
        for path in directory.rglob("*"):
            if path.is_file() and path.suffix.lower() in SUPPORT_SUFFIXES:
                require(path.resolve().is_relative_to(repo), "support symlink escaped")
                paths.add(path.relative_to(repo).as_posix())
    for relative in SUPPORT_TOPS:
        for path in repo_path(repo, relative).iterdir():
            if path.is_file() and path.suffix.lower() in SUPPORT_SUFFIXES:
                paths.add(path.relative_to(repo).as_posix())
    require(len(paths) <= 4096, "source support inventory exceeds bounded contract")
    return sorted(paths)


def python_package_inputs() -> list[dict]:
    """Bind installed PDF-production distributions and active dependencies.

    Files are streamed, never loaded together. Generated bytecode is excluded;
    source/native code, package data and distribution metadata are included.
    """
    from packaging.requirements import Requirement
    pending = ["pypdf", "pdfplumber", "packaging"]
    seen, result, count = set(), [], 0
    while pending:
        name = re.sub(r"[-_.]+", "-", pending.pop()).lower()
        if name in seen:
            continue
        seen.add(name)
        require(len(seen) <= 128, "Python dependency inventory exceeds bounded contract")
        distribution = importlib.metadata.distribution(name)
        require(distribution.files is not None, f"Python distribution has no file inventory: {name}")
        files = []
        for relative in sorted(distribution.files, key=str):
            if relative.suffix == ".pyc" or "__pycache__" in relative.parts:
                continue
            count += 1
            require(count <= 16384, "Python dependency file inventory exceeds bounded contract")
            files.append(record(Path(distribution.locate_file(relative)).resolve()))
        result.append({"Name": name, "Version": distribution.version, "Files": files})
        for raw in distribution.requires or []:
            requirement = Requirement(raw)
            if requirement.marker is None or requirement.marker.evaluate({"extra": ""}):
                pending.append(requirement.name)
    return sorted(result, key=lambda item: item["Name"])


def materialized_inputs(repo: Path, materialization: Path,
                        source_closure: Path) -> tuple[dict, list[dict]]:
    data = read_json(materialization)
    require(data.get("schema") == "openlogic-classical-notation-materialization-receipt-v1"
            and data.get("status") == "PASS" and data.get("mode") == "final"
            and data.get("release_eligible") is True, "materialization is not final PASS")
    summary = data["summary"]
    require(summary["units"] == UNIT_COUNT and summary["untreated_candidates"] == 0
            and summary["source_files_with_failed_inverse"] == 0,
            "materialization coverage/inverse failure")
    identities: dict[str, dict] = {}

    def bind(item: dict) -> None:
        path = repo_path(repo, item["path"])
        identity = record(path, item["path"])
        require(identity["Bytes"] == item["bytes"] and
                identity["SHA256"] == item["sha256"].upper(),
                f"materialization authority drift: {item['path']}")
        identities[item["path"]] = identity

    def authority(value) -> None:
        if isinstance(value, dict):
            if {"path", "bytes", "sha256"} <= set(value):
                bind(value)
            for child in value.values():
                authority(child)
        elif isinstance(value, list):
            for child in value:
                authority(child)

    authority(data["authority"])
    closure_id = data["authority"]["source_closure"]
    require(repo_path(repo, closure_id["path"]) == source_closure,
            "source-closure argument differs from materialization authority")
    for key in ("presentation_contract", "decision_ledger", "summary_document"):
        bind(data[key])
    units = data["units"]
    require(len(units) == UNIT_COUNT and {u["id"] for u in units} ==
            {f"OLP-{i:04d}" for i in range(1, UNIT_COUNT + 1)},
            "materialization unit identities are incomplete or duplicated")
    for unit in units:
        for key, prefix in (("source", "source/locale/ar-classical/content/"),
                            ("presentation", "source/locale/ar-classical-presentation/content/")):
            require(unit[key]["path"].startswith(prefix), "unit escaped its content tree")
            bind(unit[key])
        require(unit["inverse_reconstruction"]["equals_source_bytes"] is True
                and unit["untreated_candidates"] == 0, "unit inverse/coverage failure")
    for key in ("source", "presentation"):
        require(len({unit[key]["path"] for unit in units}) == UNIT_COUNT,
                "multiple units alias the same source/presentation path")
    # Bind the contemporary MSA and every explicitly listed semantic authority
    # as well as the frozen closure receipt, without traversing another project.
    closure = read_json(source_closure)
    require(closure.get("schema") == "openlogic-classical-source-closure-manifest-v1"
            and closure.get("status") == "PASS" and closure.get("total_units") == UNIT_COUNT,
            "source closure is not complete PASS")
    for item in closure.get("authority_files", []):
        bind(item)
    for unit in closure["units"]:
        bind(unit["msa"])
        bind(unit["classical"])
    return data, [identities[key] for key in sorted(identities)]


def validate_context(context: dict) -> None:
    require(context["BuildRole"] in {"primary", "replay"}, "invalid build role")
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{7,79}", context["BuildRunId"])
            is not None, "invalid build run ID")
    require(type(context["InnerProcessId"]) is int and context["InnerProcessId"] > 0,
            "invalid captured root PID")
    work, final = Path(context["WorkingDirectory"]), Path(context["OutputDirectory"])
    require(work.is_absolute() and final.is_absolute() and work != final
            and not work.is_relative_to(final) and not final.is_relative_to(work),
            "build directories are not isolated")


def validate_inputs(payload: dict) -> None:
    require(payload["Schema"] == INPUT_SCHEMA, "unknown input-capture schema")
    validate_context(payload["Context"])
    repo = Path(payload["Repository"])
    inputs = payload["Inputs"]
    for item in inputs["RepositoryFiles"]:
        verify_record(item, repo_path(repo, item["Path"]))
    for section in ("Receipts", "Executables"):
        for item in inputs[section].values():
            verify_record(item)
    for package in inputs["PythonPackages"]:
        for item in package["Files"]:
            verify_record(item)
    require(inputs["SupportInventory"] == support_paths(repo),
            "source support inventory changed")
    for item in payload["ReferenceRuntimeInputs"]:
        verify_record(item, repo_path(repo, item["Path"]) if
                      not Path(item["Path"]).is_absolute() else None)


def validate_artifacts(receipt: dict) -> None:
    directory = Path(receipt["OutputDirectory"]).resolve()
    seen = set()
    for item in receipt["Artifacts"]:
        require(item["Role"] not in seen, "duplicate artifact role")
        seen.add(item["Role"])
        require(Path(item["File"]).name == item["File"], "artifact filename escaped")
        verify_record({"Path": item["File"], "Bytes": item["Bytes"],
                       "SHA256": item["SHA256"]}, directory / item["File"])
    require(ARTIFACT_ROLES == seen, "required PDF/source-map/QA artifact inventory differs")


def validate_primary(path: Path) -> dict:
    receipt = read_json(path)
    require(receipt.get("Schema") == SCHEMA and receipt.get("Status") == "PASS"
            and receipt.get("BuildRole") == "primary", "reference is not a finalized primary")
    require(path.resolve() == Path(receipt["OutputDirectory"]).resolve() /
            "CLASSICAL_BUILD_ARTIFACTS.json", "reference path differs from primary output")
    validate_artifacts(receipt)
    verify_record(receipt["InputCapture"])
    captured = read_json(Path(receipt["InputCapture"]["Path"]))
    validate_inputs(captured)
    require(receipt["Inputs"] == captured["Inputs"] and
            all(receipt[key] == captured["Context"][key] for key in
                ("BuildRole", "BuildRunId", "OutputDirectory", "WorkingDirectory")),
            "primary input/context binding differs")
    verify_record(receipt["GuardReceipt"])
    require(Path(receipt["GuardReceipt"]["Path"]).resolve() ==
            Path(captured["Context"]["WorkingDirectory"]) / "TEX_MUTEX_RECEIPT.json",
            "primary guard receipt path differs")
    validate_guard(read_json(Path(receipt["GuardReceipt"]["Path"])), captured,
                   receipt["ProductionFinishedAtUtc"])
    require(receipt.get("GuardDrainVerified") is True and
            utc(receipt["FinalizedAtUtc"]) >= utc(read_json(Path(
                receipt["GuardReceipt"]["Path"]))["FinishedAtUtc"]),
            "primary was finalized before guard completion")
    verify_record(receipt["PendingProduction"])
    pending = read_json(Path(receipt["PendingProduction"]["Path"]))
    require(pending.get("Status") == "PENDING_GUARD_DRAIN" and all(
        pending[key] == receipt[key] for key in
        ("BuildRole", "BuildRunId", "Inputs", "InputCapture", "RuntimeInputs", "Artifacts",
         "ProductionFinishedAtUtc")), "primary differs from guarded production")
    for item in receipt["RuntimeInputs"]:
        verify_record(item, repo_path(Path(captured["Repository"]), item["Path"])
                      if not Path(item["Path"]).is_absolute() else None)
    return receipt


def prepare(repo: Path, context: dict, receipts: dict[str, Path],
            executables: dict[str, Path], reference: Path | None) -> dict:
    repo = repo.resolve()
    validate_context(context)
    require((context["BuildRole"] == "replay") == (reference is not None),
            "primary/replay reference argument mismatch")
    data, records = materialized_inputs(repo, receipts["Materialization"],
                                       receipts["SourceClosure"])
    by_path = {item["Path"]: item for item in records}
    support = support_paths(repo)
    for relative in support:
        by_path[relative] = record(repo_path(repo, relative), relative)
    inputs = {
        "Receipts": {key: record(path) for key, path in receipts.items()},
        "Executables": {key: record(path) for key, path in executables.items()},
        "RepositoryFiles": [by_path[key] for key in sorted(by_path)],
        "SupportInventory": support,
        "PythonPackages": python_package_inputs(),
        "SourceTreeSHA256": data["source_tree_sha256"],
        "PresentationTreeSHA256": data["presentation_tree_sha256"],
        "Environment": {"SOURCE_DATE_EPOCH": "1783874174", "FORCE_SOURCE_DATE": "1",
                        "TZ": "UTC", "TEXINPUTS_SUFFIX": os.environ.get("TEXINPUTS", "")},
    }
    primary = validate_primary(reference) if reference else None
    if primary:
        require(primary["Inputs"] == inputs, "replay input identity differs from primary")
        require(primary["BuildRunId"] != context["BuildRunId"], "replay reused primary run ID")
        for key in ("OutputDirectory", "WorkingDirectory"):
            original = Path(primary[key]).resolve()
            for destination in (Path(context["OutputDirectory"]), Path(context["WorkingDirectory"])):
                require(original != destination and not original.is_relative_to(destination)
                        and not destination.is_relative_to(original), "replay reused a primary directory")
    return {"Schema": INPUT_SCHEMA, "PreparedAtUtc": now(), "Repository": str(repo),
            "Context": context, "Inputs": inputs,
            "ReferencePrimary": record(reference) if reference else None,
            "ReferenceRuntimeInputs": primary["RuntimeInputs"] if primary else []}


def runtime_inputs(captured: dict) -> list[dict]:
    repo = Path(captured["Repository"])
    work = Path(captured["Context"]["WorkingDirectory"])
    compile_root = repo / "source/locale/ar-classical"
    known = {item["Path"] for item in captured["Inputs"]["RepositoryFiles"]}
    records = {}
    for job in JOBS:
        fls = work / f"{job}.fls"
        for line in fls.read_text(encoding="utf-8", errors="strict").splitlines():
            if not line.startswith("INPUT "):
                continue
            name = line[6:].strip().strip('"')
            path = Path(name)
            path = (compile_root / path).resolve() if not path.is_absolute() else path.resolve()
            if path.is_relative_to(work):
                continue  # generated AUX/PDF products are bound as artifacts below
            if path.name == "m_t_x_t_e_s_t.tmp" and not path.is_file():
                continue  # MiKTeX's explicitly known ephemeral writability probe
            label = path.relative_to(repo).as_posix() if path.is_relative_to(repo) else str(path)
            require(not path.is_relative_to(repo) or label in known,
                    f"uncaptured repository recorder input: {label}")
            records[label] = record(path, label)
    require(records, "empty runtime recorder inventory")
    return [records[key] for key in sorted(records)]


def complete_inner(capture_path: Path, details: dict) -> dict:
    captured = read_json(capture_path)
    validate_inputs(captured)
    context = captured["Context"]
    require(details["Status"] == "PENDING_GUARD_DRAIN", "inner claimed premature PASS")
    require(details["OutputDirectory"] == context["OutputDirectory"]
            and details["WorkingDirectory"] == context["WorkingDirectory"],
            "production directories differ from captured context")
    validate_artifacts(details)
    runtime = runtime_inputs(captured)
    comparisons = []
    if captured["ReferencePrimary"]:
        verify_record(captured["ReferencePrimary"])
        primary = validate_primary(Path(captured["ReferencePrimary"]["Path"]))
        require(primary["Inputs"] == captured["Inputs"], "replay inputs changed")
        require(runtime == primary["RuntimeInputs"], "replay runtime input inventory differs")
        previous = {item["Role"]: item for item in primary["Artifacts"]}
        for item in details["Artifacts"]:
            if item["Role"] in PDF_ROLES:
                old = previous[item["Role"]]
                require((item["File"], item["Bytes"], item["SHA256"]) ==
                        (old["File"], old["Bytes"], old["SHA256"]),
                        f"replay PDF bytes differ: {item['Role']}")
                comparisons.append({"Role": item["Role"], "Bytes": item["Bytes"],
                                    "SHA256": item["SHA256"], "Equal": True})
    result = dict(details)
    result.update({"Schema": SCHEMA, "BuildRole": context["BuildRole"],
                   "BuildRunId": context["BuildRunId"], "InputCapture": record(capture_path),
                   "Inputs": captured["Inputs"], "RuntimeInputs": runtime,
                   "ReferencePrimary": captured["ReferencePrimary"],
                   "ReplayPDFComparisons": comparisons, "ProductionFinishedAtUtc": now()})
    return result


def validate_guard(guard: dict, captured: dict, production_finished: str) -> None:
    context = captured["Context"]
    require(guard.get("Schema") == "interlanguage-tex-mutex/v2" and
            guard.get("Mutex") == r"Global\InterlanguageTeXSlotV1" and
            guard.get("Status") == "PASS" and guard.get("Acquired") is True and
            type(guard.get("ExitCode")) is int and guard["ExitCode"] == 0,
            "mutex receipt is not a successful acquired guard")
    require(guard.get("Containment") ==
            "Windows Job Object; atomic job assignment; suspended start; kill-on-close; no breakaway",
            "guard lacks required process-tree containment")
    require(type(guard.get("AbandonedMutexRecovered")) is bool,
            "missing abandoned-mutex recovery observation")
    tree = guard["Tree"]
    require(tree.get("RootProcessId") == context["InnerProcessId"] and
            tree.get("AssignedBeforeResume") is True and tree.get("DrainVerified") is True
            and type(tree.get("FinalActiveProcesses")) is int and tree["FinalActiveProcesses"] == 0
            and type(tree.get("RootExitCode")) is int and tree["RootExitCode"] == 0
            and tree.get("TerminationRequested") is False
            and tree.get("TerminationRequestedAtUtc") is None, "guard tree not bound and drained")
    require(Path(guard["Command"]).resolve() ==
            Path(captured["Inputs"]["Executables"]["Shell"]["Path"]).resolve()
            and Path(guard["WorkingDirectory"]).resolve() ==
            Path(context["GuardWorkingDirectory"]).resolve(), "guard invocation differs")
    times = [guard["StartedAtUtc"], guard["AcquiredAtUtc"], tree["CreatedSuspendedAtUtc"],
             tree["ResumedAtUtc"], captured["PreparedAtUtc"], production_finished,
             tree["RootExitedAtUtc"], tree["TreeEmptyAtUtc"], tree["JobClosedAtUtc"],
             guard["FinishedAtUtc"]]
    parsed = [utc(value) for value in times]
    require(parsed == sorted(parsed), "guard/capture/production lifecycle is inconsistent")


def finalize(capture_path: Path, pending_path: Path, guard_path: Path) -> dict:
    captured, pending = read_json(capture_path), read_json(pending_path)
    validate_inputs(captured)
    require(pending.get("Schema") == SCHEMA and pending.get("Status") == "PENDING_GUARD_DRAIN",
            "build is not an unfinalized pending production")
    require(pending["InputCapture"] == record(capture_path) and
            pending["Inputs"] == captured["Inputs"] and
            all(pending[key] == captured["Context"][key] for key in
                ("BuildRole", "BuildRunId", "OutputDirectory", "WorkingDirectory")),
            "pending build is not bound to its input capture")
    require(guard_path.resolve() == Path(captured["Context"]["WorkingDirectory"]) /
            "TEX_MUTEX_RECEIPT.json", "guard receipt path differs from current build")
    validate_guard(read_json(guard_path), captured, pending["ProductionFinishedAtUtc"])
    validate_artifacts(pending)
    require(runtime_inputs(captured) == pending["RuntimeInputs"], "postproduction runtime input drift")
    # Recompute replay comparisons rather than trusting mutable pending flags.
    recomputed = complete_inner(capture_path, pending)
    require(recomputed["ReplayPDFComparisons"] == pending["ReplayPDFComparisons"],
            "pending replay comparisons were modified")
    result = dict(pending)
    result.update({"Status": "PASS", "GuardReceipt": record(guard_path),
                   "GuardDrainVerified": True,
                   "AbandonedMutexRecovered": read_json(guard_path)["AbandonedMutexRecovered"],
                   "PendingProduction": record(pending_path), "FinalizedAtUtc": now()})
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    prep = sub.add_parser("prepare")
    for name in ("repo", "source-closure", "rtl-closure", "materialization", "work", "final",
                 "shell", "python", "lualatex", "bibtex", "guard-working-directory", "output"):
        prep.add_argument("--" + name, type=Path, required=True)
    prep.add_argument("--role", choices=("primary", "replay"), required=True)
    prep.add_argument("--run-id", required=True)
    prep.add_argument("--inner-pid", type=int, required=True)
    prep.add_argument("--reference", type=Path)
    production = sub.add_parser("complete-inner")
    production.add_argument("--details", type=Path, required=True)
    finish = sub.add_parser("finalize")
    finish.add_argument("--pending", type=Path, required=True)
    finish.add_argument("--guard", type=Path, required=True)
    for command in (production, finish):
        command.add_argument("--capture", type=Path, required=True)
        command.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            context = {"BuildRole": args.role, "BuildRunId": args.run_id,
                       "InnerProcessId": args.inner_pid, "WorkingDirectory": str(args.work.resolve()),
                       "OutputDirectory": str(args.final.resolve()),
                       "GuardWorkingDirectory": str(args.guard_working_directory.resolve())}
            payload = prepare(args.repo, context, {
                "SourceClosure": args.source_closure.resolve(), "RTLClosure": args.rtl_closure.resolve(),
                "Materialization": args.materialization.resolve()}, {
                    key: getattr(args, key.lower()).resolve() for key in ("Shell", "Python", "LuaLaTeX", "BibTeX")},
                args.reference.resolve() if args.reference else None)
        elif args.command == "complete-inner":
            payload = complete_inner(args.capture.resolve(), read_json(args.details))
        else:
            payload = finalize(args.capture.resolve(), args.pending.resolve(), args.guard.resolve())
        write_new(args.output, payload)
    except (OSError, ValueError, KeyError, TypeError, ImportError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"command": args.command, "status": payload.get("Status", "CAPTURED"),
                      "output": str(args.output.resolve())}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
