#!/usr/bin/env python3
"""Verify recorder-level routing for the two Classical-Arabic components.

The frozen baseline assigns 642 source units to the canonical reader graph and
80 to the closure component.  This verifier proves that the two LuaLaTeX .fls
inventories read the exact generated notation-presentation targets, never the
authoritative Classical prose or MSA prose, and together cover all 722 units
exactly once by component.  It performs no TeX invocation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Iterable


SCHEMA = "openlogic-classical-reader-routing-v2"
MATERIALIZATION_SCHEMA = "openlogic-classical-notation-materialization-receipt-v1"
BASELINE_RELATIVE = Path("evidence/classical/BASELINE.json")
CLASSICAL_PREFIX = Path("source/locale/ar-classical/content")
PRESENTATION_PREFIX = Path("source/locale/ar-classical-presentation/content")
MSA_PREFIX = Path("source/locale/ar/content")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def json_object(path: Path) -> dict:
    def unique(pairs: list[tuple[str, object]]) -> dict:
        result = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON field {key!r}: {path}")
            result[key] = value
        return result

    require(path.is_file(), f"missing JSON authority: {path}")
    value = json.loads(
        path.read_text(encoding="utf-8-sig", errors="strict"),
        object_pairs_hook=unique,
    )
    require(isinstance(value, dict), f"JSON authority is not an object: {path}")
    return value


def bound_path(repo: Path, binding: dict, label: str) -> Path:
    require(isinstance(binding, dict), f"{label} binding must be an object")
    relative = binding.get("path")
    require(isinstance(relative, str) and relative,
            f"{label} binding lacks a path")
    relative_path = Path(relative)
    require(not relative_path.is_absolute() and ".." not in relative_path.parts,
            f"{label} path is not repository-relative")
    path = (repo / relative_path).resolve()
    require(path.is_relative_to(repo), f"{label} path escapes repository")
    require(path.is_file(), f"missing {label}: {relative}")
    require(binding.get("bytes") == path.stat().st_size,
            f"{label} byte count drifted")
    require(binding.get("sha256") == sha256(path),
            f"{label} SHA-256 drifted")
    return path


def tree_hash(paths: dict[str, Path]) -> str:
    digest = hashlib.sha256()
    for relative, path in sorted(paths.items()):
        path_bytes = relative.encode("utf-8")
        raw = path.read_bytes()
        digest.update(len(path_bytes).to_bytes(8, "big"))
        digest.update(path_bytes)
        digest.update(len(raw).to_bytes(8, "big"))
        digest.update(raw)
    return digest.hexdigest().upper()


def read_baseline(repo: Path) -> tuple[dict[str, Path], set[Path], set[Path]]:
    baseline_path = repo / BASELINE_RELATIVE
    payload = json_object(baseline_path)
    require(payload.get("schema") == "openlogic-classical-baseline-v1",
            "unexpected Classical baseline schema")
    units = payload.get("units")
    require(isinstance(units, list) and len(units) == 722,
            "Classical baseline must contain exactly 722 units")
    require(payload.get("total_units") == 722,
            "Classical baseline total_units must be 722")

    by_id: dict[str, Path] = {}
    canonical: set[Path] = set()
    closure: set[Path] = set()
    classical_root = (repo / CLASSICAL_PREFIX).resolve()
    for unit in units:
        require(isinstance(unit, dict), "baseline unit must be an object")
        unit_id = unit.get("id")
        relative = unit.get("target_path")
        require(isinstance(unit_id, str) and
                re.fullmatch(r"OLP-[0-9]{4}", unit_id) is not None,
                "invalid baseline unit id")
        require(unit_id not in by_id, f"duplicate baseline id: {unit_id}")
        require(isinstance(relative, str), f"missing target_path: {unit_id}")
        relative_path = Path(relative)
        require(relative_path.parts[:len(CLASSICAL_PREFIX.parts)] ==
                CLASSICAL_PREFIX.parts,
                f"non-Classical baseline target: {unit_id}")
        absolute = (repo / relative_path).resolve()
        require(is_under(absolute, classical_root),
                f"Classical target escapes content root: {unit_id}")
        require(absolute.is_file(), f"missing Classical target: {relative}")
        canonical_reader = unit.get("canonical_reader")
        require(type(canonical_reader) is bool,
                f"canonical_reader must be boolean: {unit_id}")
        by_id[unit_id] = absolute
        (canonical if canonical_reader else closure).add(absolute)

    require(len(by_id) == 722 and len(set(by_id.values())) == 722,
            "baseline ids and target paths must be one-to-one")
    require(len(canonical) == 642 and len(closure) == 80,
            "baseline split must be 642 canonical plus 80 closure units")
    require(canonical.isdisjoint(closure), "baseline components overlap")
    return by_id, canonical, closure


def read_materialization(
    repo: Path, receipt_path: Path, by_id: dict[str, Path],
) -> tuple[dict[str, Path], dict, dict]:
    payload = json_object(receipt_path)
    require(payload.get("schema") == MATERIALIZATION_SCHEMA,
            "unexpected notation-materialization receipt schema")
    require(payload.get("status") == "PASS" and
            payload.get("release_eligible") is True and
            payload.get("mode") == "final",
            "notation materialization is not a final release-eligible PASS")
    require(payload.get("presentation_locale") == "ar-classical-presentation",
            "notation presentation locale drifted")

    authority = payload.get("authority")
    require(isinstance(authority, dict), "materialization authority is missing")
    baseline = authority.get("baseline")
    require(isinstance(baseline, dict) and
            baseline.get("path") == BASELINE_RELATIVE.as_posix(),
            "materialization is not bound to the Classical baseline")
    bound_path(repo, baseline, "materialization baseline")
    source_closure = authority.get("source_closure")
    require(isinstance(source_closure, dict),
            "materialization lacks a frozen source-closure binding")
    bound_path(repo, source_closure, "source-closure receipt")
    for key in ("policy", "letter_registry", "set_registry", "generator"):
        bound_path(repo, authority.get(key), f"materialization {key}")
    bound_path(repo, payload.get("decision_ledger"), "materialization decision ledger")
    bound_path(repo, payload.get("summary_document"), "materialization summary")
    bound_path(repo, payload.get("presentation_contract"), "materialization contract")

    summary = payload.get("summary")
    require(isinstance(summary, dict) and summary.get("units") == 722,
            "materialization summary must cover 722 units")
    require(summary.get("untreated_candidates") == 0 and
            summary.get("source_files_with_failed_inverse") == 0,
            "materialization summary has untreated or non-invertible units")
    units = payload.get("units")
    require(isinstance(units, list) and len(units) == 722,
            "materialization receipt must bind 722 units")
    require([unit.get("id") for unit in units] == list(by_id),
            "materialization unit ids/order drifted from baseline")

    source_paths: dict[str, Path] = {}
    presentation_paths: dict[str, Path] = {}
    presentation_by_id: dict[str, Path] = {}
    totals = {
        "formula_segments": 0,
        "ascii_candidate_scalars": 0,
        "text_digit_candidate_scalars": 0,
        "greek_candidate_commands": 0,
        "occurrence_records": 0,
        "replacement_records": 0,
    }
    source_root = (repo / CLASSICAL_PREFIX).resolve()
    presentation_root = (repo / PRESENTATION_PREFIX).resolve()
    for unit in units:
        unit_id = unit["id"]
        source = unit.get("source")
        source_path = bound_path(repo, source, f"{unit_id} source")
        require(source_path == by_id[unit_id],
                f"{unit_id} source does not match baseline")
        require(is_under(source_path, source_root),
                f"{unit_id} source escapes Classical authority")
        source_relative = Path(source["path"])
        suffix = Path(*source_relative.parts[len(CLASSICAL_PREFIX.parts):])
        expected_presentation = (repo / PRESENTATION_PREFIX / suffix).resolve()
        presentation = unit.get("presentation")
        presentation_path = bound_path(
            repo, presentation, f"{unit_id} presentation",
        )
        require(presentation_path == expected_presentation and
                is_under(presentation_path, presentation_root),
                f"{unit_id} presentation path is not the exact source counterpart")
        inverse = unit.get("inverse_reconstruction")
        require(isinstance(inverse, dict) and inverse.get("status") == "PASS" and
                inverse.get("equals_source_bytes") is True and
                inverse.get("bytes") == source["bytes"] and
                inverse.get("sha256") == source["sha256"],
                f"{unit_id} inverse reconstruction proof failed")
        require(unit.get("untreated_candidates") == 0,
                f"{unit_id} has untreated notation candidates")
        for key in totals:
            value = unit.get(key)
            require(type(value) is int and value >= 0,
                    f"{unit_id} invalid {key}")
            totals[key] += value
        source_paths[source["path"]] = source_path
        presentation_paths[presentation["path"]] = presentation_path
        presentation_by_id[unit_id] = presentation_path

    require(len(source_paths) == len(presentation_paths) ==
            len(presentation_by_id) == 722,
            "materialization unit paths are not one-to-one")
    for key, value in totals.items():
        require(summary.get(key) == value,
                f"materialization summary {key} does not equal unit total")
    require(payload.get("source_tree_sha256") == tree_hash(source_paths),
            "materialization source-tree hash drifted")
    require(payload.get("presentation_tree_sha256") == tree_hash(presentation_paths),
            "materialization presentation-tree hash drifted")
    receipt_binding = {
        "path": receipt_path.relative_to(repo).as_posix(),
        "bytes": receipt_path.stat().st_size,
        "sha256": sha256(receipt_path),
    }
    return presentation_by_id, payload, receipt_binding


def normalize_recorder_path(raw: str, compile_root: Path) -> Path:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        value = value[1:-1]
    require(bool(value) and "\x00" not in value, "invalid recorder path")
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = compile_root / candidate
    return candidate.resolve()


def recorder_inputs(path: Path, compile_root: Path) -> set[Path]:
    require(path.is_file(), f"missing recorder file: {path}")
    inputs = {
        normalize_recorder_path(line[6:], compile_root)
        for line in path.read_text(encoding="utf-8", errors="strict").splitlines()
        if line.startswith("INPUT ")
    }
    require(inputs, f"recorder has no inputs: {path}")
    return inputs


def relative_names(paths: Iterable[Path], repo: Path) -> list[str]:
    return sorted(path.relative_to(repo).as_posix() for path in paths)


def is_under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def verify(repo: Path, compile_root: Path, reader_fls: Path,
           closure_fls: Path, materialization_receipt: Path) -> dict:
    repo = repo.resolve()
    compile_root = compile_root.resolve()
    require(repo.is_dir(), "repository path is not a directory")
    require(compile_root ==
            (repo / "source/locale/ar-classical").resolve(),
            "compile root must be source/locale/ar-classical")

    by_id, source_reader, source_closure = read_baseline(repo)
    presentations, materialization, materialization_binding = read_materialization(
        repo, materialization_receipt.resolve(), by_id,
    )
    expected_reader = {
        presentations[unit_id] for unit_id, source in by_id.items()
        if source in source_reader
    }
    expected_closure = {
        presentations[unit_id] for unit_id, source in by_id.items()
        if source in source_closure
    }
    reader_inputs = recorder_inputs(reader_fls.resolve(), compile_root)
    closure_inputs = recorder_inputs(closure_fls.resolve(), compile_root)
    all_targets = set(presentations.values())
    observed_reader = reader_inputs & all_targets
    observed_closure = closure_inputs & all_targets

    require(observed_reader == expected_reader,
            "reader recorder does not contain the exact 642-unit canonical set")
    require(observed_closure == expected_closure,
            "closure recorder does not contain the exact 80-unit closure set")
    require(observed_reader.isdisjoint(observed_closure),
            "a Classical presentation unit was read by both components")
    require(observed_reader | observed_closure == all_targets,
            "component union does not cover all 722 Classical units")

    msa_root = (repo / MSA_PREFIX).resolve()
    forbidden = {
        path for path in reader_inputs | closure_inputs if is_under(path, msa_root)
    }
    require(not forbidden,
            "a Classical build read MSA prose: " +
            ", ".join(relative_names(forbidden, repo)))
    classical_root = (repo / CLASSICAL_PREFIX).resolve()
    authoritative = {
        path for path in reader_inputs | closure_inputs
        if is_under(path, classical_root)
    }
    require(not authoritative,
            "a Classical build bypassed the reversible presentation tree: " +
            ", ".join(relative_names(authoritative, repo)))

    return {
        "schema": SCHEMA,
        "status": "PASS",
        "baseline": {
            "path": BASELINE_RELATIVE.as_posix(),
            "bytes": (repo / BASELINE_RELATIVE).stat().st_size,
            "sha256": sha256(repo / BASELINE_RELATIVE),
        },
        "compile_root": "source/locale/ar-classical",
        "materialization": materialization_binding,
        "presentation_locale": materialization["presentation_locale"],
        "source_tree_sha256": materialization["source_tree_sha256"],
        "presentation_tree_sha256": materialization["presentation_tree_sha256"],
        "coverage": {
            "reader_units": len(observed_reader),
            "closure_units": len(observed_closure),
            "total_units": len(observed_reader | observed_closure),
            "component_overlap": 0,
            "all_722_classical_targets_read": True,
            "msa_content_inputs": 0,
            "authoritative_classical_content_inputs": 0,
            "untreated_notation_candidates": 0,
        },
        "recorders": {
            "reader": {
                "path": str(reader_fls.resolve()),
                "bytes": reader_fls.stat().st_size,
                "sha256": sha256(reader_fls),
            },
            "closure": {
                "path": str(closure_fls.resolve()),
                "bytes": closure_fls.stat().st_size,
                "sha256": sha256(closure_fls),
            },
        },
        "failures": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--compile-root", type=Path, required=True)
    parser.add_argument("--reader-fls", type=Path, required=True)
    parser.add_argument("--closure-fls", type=Path, required=True)
    parser.add_argument("--materialization-receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        require(not args.output.exists(),
                f"refusing to overwrite routing receipt: {args.output}")
        payload = verify(args.repo, args.compile_root,
                         args.reader_fls, args.closure_fls,
                         args.materialization_receipt)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2,
                       sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except Exception as exc:
        print(f"FAIL-CLOSED: {exc}")
        return 2
    print(json.dumps({"status": "PASS", "output": str(args.output),
                      "total_units": 722}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
