#!/usr/bin/env python3
"""Build or verify the reversible Classical-Arabic notation presentation tree.

The accepted Classical translation remains the source authority.  This tool
creates a separate presentation tree in which source-addressed mathematical
letters, selected Greek variables, and numeral literals are wrapped by the
typed Classical notation APIs.  Every potentially visible ASCII math
letter/digit and every Greek-letter command is assigned exactly one disposition:

* a typed Arabic presentation wrapper;
* the existing ``!A``/``\formula{A}`` formula-key hook; or
* an explicit, reasoned international/invariant exemption.

No source token is guessed from rendered output.  Each occurrence is bound to
the authoritative source path, SHA-256, character and UTF-8 byte span.  The
inverse transformation must reproduce every source byte (including BOM and
newline convention) before any output is written.  This script never invokes
TeX.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any, Iterable

sys.dont_write_bytecode = True

from validate_classical_overlay import Token, analyze, group, skip_space


SCHEMA = "openlogic-classical-notation-materialization-v2"
RECEIPT_SCHEMA = "openlogic-classical-notation-materialization-receipt-v1"
POLICY_SCHEMA = "openlogic-classical-notation-materialization-policy-v2"
BASELINE_SCHEMA = "openlogic-classical-baseline-v1"
LETTER_SCHEMA = "openlogic-classical-letter-presentation-v1"
CLOSURE_SCHEMA = "openlogic-classical-source-closure-manifest-v1"
RECONCILIATION_AUDIT_SCHEMA = "openlogic-classical-source-reconciliation-audit-v1"
RECONCILIATION_METADATA_SCHEMA = "openlogic-classical-source-reconciliation-metadata-v1"
ACCEPTANCE_SCHEMA = "openlogic-full-translation-acceptance-audit-v2"
PRESENTATION_LOCALE = "ar-classical-presentation"
SOURCE_PREFIX = Path("source/locale/ar-classical/content")
MSA_SOURCE_PREFIX = Path("source/locale/ar/content")
PRESENTATION_PREFIX = Path(f"source/locale/{PRESENTATION_LOCALE}/content")
DEFAULT_POLICY = Path("evidence/classical/NOTATION_MATERIALIZATION_POLICY.json")
DEFAULT_DECISIONS = Path("evidence/classical/NOTATION_MATERIALIZATION_DECISIONS.json")
DEFAULT_RECEIPT = Path("evidence/classical/NOTATION_MATERIALIZATION_RECEIPT.json")
DEFAULT_SUMMARY = Path("evidence/classical/NOTATION_MATERIALIZATION_SUMMARY.md")
DEFAULT_BASELINE = Path("evidence/classical/BASELINE.json")
DEFAULT_LETTERS = Path("evidence/classical/LETTER_PRESENTATION_REGISTRY.json")
DEFAULT_SETS = Path("evidence/classical/SET_SYMBOL_MAPPING.json")
DEFAULT_PRESENTATION_ROOT = Path(f"source/locale/{PRESENTATION_LOCALE}/content")
DEFAULT_CONTRACT = Path(
    f"source/locale/{PRESENTATION_LOCALE}/open-logic-materialization-contract.tex"
)
DEFAULT_SOURCE_CLOSURE = Path(
    "evidence/classical/SOURCE_RECONCILIATION_CLOSURE_MANIFEST_20260905.json"
)
DEFAULT_SOURCE_RECONCILIATION_AUDIT = Path(
    "evidence/classical/SOURCE_RECONCILIATION_AUDIT_20260905.json"
)
DEFAULT_SOURCE_RECONCILIATION_METADATA = Path(
    "evidence/classical/SOURCE_RECONCILIATION_METADATA_20260905.json"
)
SOURCE_RECONCILIATION_TRANSACTION = Path(
    "evidence/classical/.SOURCE_RECONCILIATION_WRITE_IN_PROGRESS"
)
RECONCILIATION_ARTIFACTS = {
    "baseline_correction_overlay":
        "evidence/classical/BASELINE_CORRECTION_OVERLAY_FULL_20260905.json",
    "math_text_declarations":
        "evidence/classical/MATH_TEXT_DECLARATIONS_FULL_20260905.json",
    "structural_reviews":
        "evidence/classical/STRUCTURAL_REVIEW_DECLARATIONS_FULL_20260905.json",
    "formal_repairs":
        "evidence/classical/FORMAL_REPAIR_DECLARATIONS_FULL_20260905.json",
    "general_reviews":
        "evidence/classical/GENERAL_REVIEW_DECLARATIONS_FULL_20260905.json",
}
STATIC_VALIDATION_PATH = (
    "evidence/classical/SOURCE_RECONCILIATION_STATIC_VALIDATION_20260905.json"
)
FILE_ID_FIELDS = frozenset(("path", "sha256", "bytes"))
CLOSURE_FIELDS = frozenset((
    "schema", "status", "release_id", "total_units",
    "source_snapshot_sha256", "frozen_baseline",
    *RECONCILIATION_ARTIFACTS.keys(), "authority_files",
    "source_acceptance", "counts", "checks", "units",
))
CLOSURE_UNIT_FIELDS = frozenset((
    "id", "source_path", "english_sha256", "msa", "classical",
    "correction", "math_text_declaration", "formal_repair",
    "structural_review", "unchanged_prose_review", "semantic_authority",
    "final_static_status", "raw_comparison_sha256",
))
CLOSURE_CHECKS = frozenset((
    "immutable_baseline_exact", "all_live_msa_deltas_declared",
    "all_formula_local_arabic_differences_declared",
    "all_formal_failures_exactly_declared",
    "all_unchanged_prose_exactly_reviewed",
    "semantic_review_unit_coverage_722", "full_static_validator_exit_zero",
    "source_ranges_semantically_ready",
))
CLOSURE_COUNTS = frozenset((
    "baseline_units", "corrected_msa_units", "math_text_units",
    "math_text_items", "formal_repair_units", "structural_review_units",
    "unchanged_prose_review_units", "static_statuses",
))
FINAL_STATIC_STATUSES = frozenset((
    "changed-prose-awaiting-semantic-review", "formal-repair-reviewed",
    "structural-reviewed", "unchanged-prose-reviewed",
))
ASCII_ALNUM = re.compile(r"[A-Za-z0-9]")
ASCII_LETTER = re.compile(r"[A-Za-z]")
ASCII_DIGIT = re.compile(r"[0-9]")
UPPER = re.compile(r"[A-Z]")
GREEK_COMMANDS = frozenset(
    ("alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta "
     "iota kappa varkappa lambda mu nu xi omicron pi varpi rho varrho "
     "sigma varsigma tau upsilon phi varphi chi psi omega digamma "
     "Gamma Delta Theta Lambda Xi Pi Sigma Upsilon Phi Psi Omega").split()
)
IMPLICIT_CARRIER_CONFIG = Path("source/open-logic-config.sty")
IMPLICIT_CARRIER_CONFIG_SHA = "ab19be71b50b415738603290317b504d9fa6b82850fe640d585c62db1540ced3"
# A finite extension, not macro expansion. The actual source definitions below
# establish math mode for these arguments, including TikZ label text.
IMPLICIT_CARRIERS = {
    "mTrue": (1, 859, r"\DeclareDocumentCommand \mTrue { m }{\ensuremath{#1}}"),
    "mFalse": (1, 860, r"\DeclareDocumentCommand \mFalse { m }{\ensuremath{\lnot #1}}"),
    "TMtrans": (3, 1041, r"\DeclareDocumentCommand \TMtrans { m m m } {\ensuremath{#1, #2, #3}}"),
}


class MaterializationError(ValueError):
    """A fail-closed source, policy, classification, or inverse error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise MaterializationError(message)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest().upper()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def json_load(path: Path) -> dict[str, Any]:
    def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON field {key!r} in {path}")
            result[key] = value
        return result

    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_pairs)
    require(isinstance(value, dict), f"JSON root must be an object: {path}")
    return value


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(raw).lower()


def strict_repo_path(repo: Path, value: Any, *, suffix: str | None = None) -> Path:
    require(isinstance(value, str) and value and "\\" not in value and ":" not in value,
            f"invalid repository-relative path: {value!r}")
    relative = PurePosixPath(value)
    require(not relative.is_absolute() and ".." not in relative.parts and
            relative.as_posix() == value,
            f"invalid repository-relative path: {value!r}")
    path = (repo / Path(*relative.parts)).resolve()
    require(path.is_relative_to(repo.resolve()), f"repository path escapes root: {value!r}")
    require(suffix is None or path.suffix == suffix,
            f"unexpected suffix for repository path: {value!r}")
    return path


def lower_sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def exact_file_identity(
    repo: Path, item: Any, label: str, *, expected_path: str | None = None,
) -> dict[str, Any]:
    require(isinstance(item, dict) and set(item) == FILE_ID_FIELDS,
            f"{label} must be an exact path/bytes/sha256 identity")
    value = item.get("path")
    if expected_path is not None:
        require(value == expected_path,
                f"{label} path differs: expected {expected_path!r}, got {value!r}")
    path = strict_repo_path(repo, value)
    require(path.is_file(), f"missing {label}: {value}")
    raw = path.read_bytes()
    digest = item.get("sha256")
    byte_count = item.get("bytes")
    require(type(byte_count) is int and byte_count >= 0 and
            isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
            f"malformed {label} identity: {value}")
    require(byte_count == len(raw) and digest == lower_sha256(raw),
            f"stale {label} identity: {value}")
    return {"path": value, "bytes": byte_count, "sha256": digest}


def strict_nonempty_strings(value: Any, label: str) -> list[str]:
    require(isinstance(value, list) and value and
            all(isinstance(item, str) and item.strip() for item in value) and
            len(value) == len(set(value)),
            f"{label} must be a nonempty unique string list")
    return value


def validate_source_closure(
    repo: Path, closure_path: Path, baseline_path: Path,
) -> dict[str, Any]:
    """Validate the finalizer's complete, committed 722-unit source closure.

    This is intentionally a schema adapter, not a presence check.  It binds the
    canonical manifest and audit receipt to the current metadata release,
    baseline, derived reconciliation artifacts, authority files, and every live
    MSA/Classical source byte.  The source snapshot is independently recomputed
    using the finalizer's canonical serialization.
    """
    repo = repo.resolve()
    expected_closure = (repo / DEFAULT_SOURCE_CLOSURE).resolve()
    require(closure_path.resolve() == expected_closure,
            "final materialization requires the canonical source-closure manifest")
    require(not (repo / SOURCE_RECONCILIATION_TRANSACTION).exists(),
            "source reconciliation transaction is still in progress")
    require(closure_path.is_file(), "final source-closure manifest is missing")

    baseline = json_load(baseline_path)
    require(baseline.get("schema") == BASELINE_SCHEMA and
            baseline.get("total_units") == 722,
            "source closure requires the exact 722-unit baseline")
    baseline_units = baseline.get("units")
    require(isinstance(baseline_units, list) and len(baseline_units) == 722,
            "source closure baseline unit inventory is not 722-exact")
    expected_ids = [f"OLP-{number:04d}" for number in range(1, 723)]
    require([item.get("id") if isinstance(item, dict) else None
             for item in baseline_units] == expected_ids,
            "source closure baseline ids are not contiguous OLP-0001..OLP-0722")

    metadata_path = repo / DEFAULT_SOURCE_RECONCILIATION_METADATA
    require(metadata_path.is_file(), "source-reconciliation metadata is missing")
    metadata = json_load(metadata_path)
    require(metadata.get("schema") == RECONCILIATION_METADATA_SCHEMA,
            "unsupported source-reconciliation metadata schema")
    release_id = metadata.get("release_id")
    require(isinstance(release_id, str) and release_id.strip(),
            "source-reconciliation metadata lacks a release identity")
    require(metadata.get("baseline_sha256") == lower_sha256(baseline_path.read_bytes()),
            "source-reconciliation metadata binds a different baseline")

    closure = json_load(closure_path)
    require(set(closure) == CLOSURE_FIELDS and closure.get("schema") == CLOSURE_SCHEMA,
            "unsupported or malformed final source-closure schema")
    require(closure.get("status") == "PASS",
            "final source closure is pending or non-passing")
    require(closure.get("release_id") == release_id,
            "source closure binds a different release identity")
    require(closure.get("total_units") == 722,
            "source closure does not declare exactly 722 units")
    exact_file_identity(
        repo, closure.get("frozen_baseline"), "frozen baseline",
        expected_path=baseline_path.resolve().relative_to(repo).as_posix(),
    )

    for key, expected_path in RECONCILIATION_ARTIFACTS.items():
        exact_file_identity(repo, closure.get(key), key.replace("_", " "),
                            expected_path=expected_path)

    acceptance = closure.get("source_acceptance")
    acceptance_fields = frozenset((
        "source_ranges_ready", "nonpassing_source_ranges",
        "nonintegration_blocker_ids", "failed_required_verifications",
        "overall_status", "audit_schema", "source_snapshot_sha256",
        "preflight_fingerprint_sha256",
    ))
    require(isinstance(acceptance, dict) and set(acceptance) == acceptance_fields,
            "source-acceptance record is malformed")
    require(acceptance.get("source_ranges_ready") is True and
            acceptance.get("nonpassing_source_ranges") == [] and
            acceptance.get("nonintegration_blocker_ids") == [] and
            acceptance.get("failed_required_verifications") == [] and
            acceptance.get("overall_status") == "PASS" and
            acceptance.get("audit_schema") == ACCEPTANCE_SCHEMA,
            "source-acceptance record is pending or non-passing")
    for key in ("source_snapshot_sha256", "preflight_fingerprint_sha256"):
        require(isinstance(acceptance.get(key), str) and
                re.fullmatch(r"[0-9a-f]{64}", acceptance[key]) is not None,
                f"source-acceptance {key} is malformed")

    checks = closure.get("checks")
    require(isinstance(checks, dict) and set(checks) == CLOSURE_CHECKS and
            all(value is True for value in checks.values()),
            "source-closure checks are incomplete, pending, or non-passing")
    counts = closure.get("counts")
    require(isinstance(counts, dict) and set(counts) == CLOSURE_COUNTS,
            "source-closure counts are malformed")
    for key in CLOSURE_COUNTS - {"static_statuses"}:
        require(type(counts.get(key)) is int and counts[key] >= 0,
                f"source-closure count is malformed: {key}")
    require(counts.get("baseline_units") == 722,
            "source-closure baseline count is not 722")

    units = closure.get("units")
    require(isinstance(units, list) and len(units) == 722,
            "source closure lacks 722 exact unit records")
    observed_ids = [item.get("id") if isinstance(item, dict) else None for item in units]
    require(observed_ids == expected_ids and len(observed_ids) == len(set(observed_ids)),
            "source-closure unit ids are duplicate, missing, or non-contiguous")

    snapshot_rows: list[dict[str, Any]] = []
    observed_msa_paths: set[str] = set()
    observed_classical_paths: set[str] = set()
    status_counts: Counter[str] = Counter()
    correction_count = math_count = math_items = formal_count = 0
    structural_count = unchanged_count = 0
    hash_pattern = re.compile(r"[0-9a-f]{64}")

    def authority_refs(record: dict[str, Any], label: str) -> None:
        strict_nonempty_strings(record.get("authority_refs"), f"{label} authority refs")

    for baseline_unit, item in zip(baseline_units, units, strict=True):
        uid = baseline_unit["id"]
        require(isinstance(item, dict) and set(item) == CLOSURE_UNIT_FIELDS,
                f"malformed source-closure unit record: {uid}")
        require(item.get("source_path") == baseline_unit.get("source_path") and
                item.get("english_sha256") == baseline_unit.get("english_sha256") and
                isinstance(item.get("english_sha256"), str) and
                hash_pattern.fullmatch(item["english_sha256"]) is not None,
                f"frozen-English identity differs for {uid}")

        msa = item.get("msa")
        classical = item.get("classical")
        require(isinstance(msa, dict) and
                set(msa) == {"path", "sha256", "bytes", "identity_mode"},
                f"malformed MSA identity for {uid}")
        require(isinstance(classical, dict) and
                set(classical) == {"path", "sha256", "bytes"},
                f"malformed Classical identity for {uid}")
        require(msa.get("path") == baseline_unit.get("arabic_path") and
                classical.get("path") == baseline_unit.get("target_path"),
                f"source path binding differs for {uid}")
        msa_path = safe_repo_path(repo, Path(msa["path"]), MSA_SOURCE_PREFIX)
        classical_path = safe_repo_path(repo, Path(classical["path"]), SOURCE_PREFIX)
        require(msa_path.is_file() and classical_path.is_file(),
                f"live MSA/Classical source is missing for {uid}")
        msa_raw, classical_raw = msa_path.read_bytes(), classical_path.read_bytes()
        for layer, raw, label in ((msa, msa_raw, "MSA"),
                                  (classical, classical_raw, "Classical")):
            require(type(layer.get("bytes")) is int and
                    isinstance(layer.get("sha256"), str) and
                    hash_pattern.fullmatch(layer["sha256"]) is not None,
                    f"malformed {label} source identity for {uid}")
            require(layer["bytes"] == len(raw) and
                    layer["sha256"] == lower_sha256(raw),
                    f"stale {label} source identity for {uid}")
        require(msa["path"] not in observed_msa_paths and
                classical["path"] not in observed_classical_paths,
                f"duplicate MSA/Classical source path in closure: {uid}")
        observed_msa_paths.add(msa["path"])
        observed_classical_paths.add(classical["path"])

        correction = item.get("correction")
        frozen_msa = (msa["sha256"] == baseline_unit.get("arabic_sha256") and
                      msa["bytes"] == baseline_unit.get("arabic_bytes"))
        if msa.get("identity_mode") == "frozen-baseline":
            require(frozen_msa and correction is None,
                    f"frozen-baseline MSA binding is inconsistent for {uid}")
        elif msa.get("identity_mode") == "baseline-correction":
            require(not frozen_msa and isinstance(correction, dict) and
                    set(correction) == {"finding_ids", "rationale", "authority_refs",
                                        "metadata_source"},
                    f"baseline-correction MSA binding is incomplete for {uid}")
            strict_nonempty_strings(correction.get("finding_ids"),
                                    f"{uid} correction finding ids")
            authority_refs(correction, f"{uid} correction")
            require(isinstance(correction.get("rationale"), str) and
                    correction["rationale"].strip() and
                    isinstance(correction.get("metadata_source"), str) and
                    correction["metadata_source"].strip(),
                    f"{uid} correction rationale/metadata source is malformed")
            correction_count += 1
        else:
            raise MaterializationError(f"invalid MSA identity mode for {uid}")

        math_record = item.get("math_text_declaration")
        if math_record is not None:
            require(isinstance(math_record, dict) and
                    set(math_record) == {"indices", "authority_refs"},
                    f"malformed math-text declaration for {uid}")
            indices = math_record.get("indices")
            require(isinstance(indices, list) and indices and
                    all(type(index) is int and index >= 0 for index in indices) and
                    indices == sorted(set(indices)),
                    f"pending/duplicate math-text indices for {uid}")
            authority_refs(math_record, f"{uid} math-text declaration")
            math_count += 1
            math_items += len(indices)

        formal = item.get("formal_repair")
        if formal is not None:
            require(isinstance(formal, dict) and
                    set(formal) == {"accepted_failed_checks", "comparison_sha256",
                                    "authority_refs", "rationale", "metadata_source"},
                    f"malformed formal repair for {uid}")
            strict_nonempty_strings(formal.get("accepted_failed_checks"),
                                    f"{uid} accepted formal checks")
            authority_refs(formal, f"{uid} formal repair")
            require(isinstance(formal.get("comparison_sha256"), str) and
                    hash_pattern.fullmatch(formal["comparison_sha256"]) is not None and
                    isinstance(formal.get("rationale"), str) and formal["rationale"].strip() and
                    isinstance(formal.get("metadata_source"), str) and
                    formal["metadata_source"].strip(),
                    f"malformed formal-repair binding for {uid}")
            formal_count += 1

        structural = item.get("structural_review")
        if structural is not None:
            require(isinstance(structural, dict) and
                    set(structural) == {"kind", "authority_refs"} and
                    isinstance(structural.get("kind"), str) and structural["kind"].strip(),
                    f"malformed structural review for {uid}")
            authority_refs(structural, f"{uid} structural review")
            structural_count += 1

        unchanged = item.get("unchanged_prose_review")
        if unchanged is not None:
            require(isinstance(unchanged, dict) and
                    set(unchanged) == {"comparison_sha256", "authority_refs", "rationale"},
                    f"malformed unchanged-prose review for {uid}")
            authority_refs(unchanged, f"{uid} unchanged-prose review")
            require(isinstance(unchanged.get("comparison_sha256"), str) and
                    hash_pattern.fullmatch(unchanged["comparison_sha256"]) is not None and
                    isinstance(unchanged.get("rationale"), str) and
                    unchanged["rationale"].strip(),
                    f"malformed unchanged-prose binding for {uid}")
            unchanged_count += 1

        semantic = item.get("semantic_authority")
        require(isinstance(semantic, dict) and
                set(semantic) == {"authority_ref", "note"} and
                isinstance(semantic.get("authority_ref"), str) and
                semantic["authority_ref"].strip() and
                isinstance(semantic.get("note"), str) and semantic["note"].strip(),
                f"semantic authority is missing or pending for {uid}")
        status = item.get("final_static_status")
        require(status in FINAL_STATIC_STATUSES,
                f"pending or invalid final static status for {uid}: {status!r}")
        review_records = sum(record is not None for record in (formal, structural, unchanged))
        require(review_records <= 1,
                f"duplicate final review dispositions for {uid}")
        expected_status = (
            "formal-repair-reviewed" if formal is not None else
            "structural-reviewed" if structural is not None else
            "unchanged-prose-reviewed" if unchanged is not None else
            "changed-prose-awaiting-semantic-review"
        )
        require(status == expected_status,
                f"final static status/review binding differs for {uid}")
        require(isinstance(item.get("raw_comparison_sha256"), str) and
                hash_pattern.fullmatch(item["raw_comparison_sha256"]) is not None,
                f"raw comparison fingerprint is malformed for {uid}")
        status_counts[status] += 1
        snapshot_rows.append({
            "id": uid,
            "msa_sha256": lower_sha256(msa_raw), "msa_bytes": len(msa_raw),
            "classical_sha256": lower_sha256(classical_raw),
            "classical_bytes": len(classical_raw),
        })

    expected_counts = {
        "baseline_units": 722,
        "corrected_msa_units": correction_count,
        "math_text_units": math_count,
        "math_text_items": math_items,
        "formal_repair_units": formal_count,
        "structural_review_units": structural_count,
        "unchanged_prose_review_units": unchanged_count,
        "static_statuses": dict(sorted(status_counts.items())),
    }
    require(counts == expected_counts,
            "source-closure counts do not match the exact unit records")
    snapshot_hash = canonical_sha256(snapshot_rows)
    require(closure.get("source_snapshot_sha256") == snapshot_hash,
            "source-closure live MSA/Classical snapshot is stale")

    authority_files = closure.get("authority_files")
    require(isinstance(authority_files, list) and authority_files,
            "source-closure authority-file inventory is missing")
    authority_by_path: dict[str, dict[str, Any]] = {}
    for index, authority in enumerate(authority_files):
        identity = exact_file_identity(repo, authority, f"authority file {index}")
        previous = authority_by_path.get(identity["path"])
        require(previous is None or previous == identity,
                f"conflicting duplicate authority identity: {identity['path']}")
        authority_by_path[identity["path"]] = identity
    metadata_relative = DEFAULT_SOURCE_RECONCILIATION_METADATA.as_posix()
    require(metadata_relative in authority_by_path,
            "source-closure authorities omit the release metadata")
    acceptance_path_value = metadata.get("acceptance_audit")
    require(isinstance(acceptance_path_value, str) and
            acceptance_path_value in authority_by_path,
            "source-closure authorities omit the acceptance audit")
    acceptance_artifact = json_load(strict_repo_path(repo, acceptance_path_value, suffix=".json"))
    require(acceptance_artifact.get("schema") == ACCEPTANCE_SCHEMA and
            acceptance_artifact.get("release_id") == release_id and
            acceptance_artifact.get("overall_status") == "PASS" and
            isinstance(acceptance_artifact.get("source_snapshot"), dict) and
            acceptance_artifact["source_snapshot"].get("snapshot_sha256") ==
                acceptance["source_snapshot_sha256"] and
            isinstance(acceptance_artifact.get("preflight"), dict) and
            acceptance_artifact["preflight"].get("fingerprint_sha256") ==
                acceptance["preflight_fingerprint_sha256"],
            "source-closure acceptance artifact is stale, malformed, or non-passing")

    audit_path = repo / DEFAULT_SOURCE_RECONCILIATION_AUDIT
    require(audit_path.is_file(), "committed source-reconciliation audit receipt is missing")
    audit = json_load(audit_path)
    audit_fields = frozenset((
        "schema", "status", "release_id", "source_snapshot_sha256", "inputs",
        "outputs", "validation", "source_acceptance", "write_policy",
    ))
    require(set(audit) == audit_fields and
            audit.get("schema") == RECONCILIATION_AUDIT_SCHEMA and
            audit.get("status") == "PASS" and audit.get("release_id") == release_id and
            audit.get("source_snapshot_sha256") == snapshot_hash and
            audit.get("source_acceptance") == acceptance,
            "source-reconciliation audit receipt is malformed, stale, or non-passing")
    audit_inputs = audit.get("inputs")
    require(isinstance(audit_inputs, dict) and
            set(audit_inputs) == {"metadata", "validator", "frozen_baseline",
                                  "semantic_and_acceptance_authorities"},
            "source-reconciliation audit inputs are malformed")
    exact_file_identity(repo, audit_inputs.get("metadata"), "audit metadata",
                        expected_path=metadata_relative)
    exact_file_identity(repo, audit_inputs.get("validator"), "audit validator",
                        expected_path="build/validate_classical_overlay.py")
    exact_file_identity(
        repo, audit_inputs.get("frozen_baseline"), "audit frozen baseline",
        expected_path=baseline_path.resolve().relative_to(repo).as_posix(),
    )
    require(audit_inputs.get("semantic_and_acceptance_authorities") == authority_files,
            "audit authority inventory differs from the closure manifest")

    audit_outputs = audit.get("outputs")
    expected_output_paths = set(RECONCILIATION_ARTIFACTS.values()) | {
        STATIC_VALIDATION_PATH, DEFAULT_SOURCE_CLOSURE.as_posix(),
    }
    require(isinstance(audit_outputs, list) and len(audit_outputs) == len(expected_output_paths),
            "source-reconciliation audit output inventory is not exact")
    output_paths = [item.get("path") if isinstance(item, dict) else None
                    for item in audit_outputs]
    require(set(output_paths) == expected_output_paths and
            len(output_paths) == len(set(output_paths)),
            "source-reconciliation audit outputs are duplicate, missing, or unexpected")
    for index, identity in enumerate(audit_outputs):
        exact_file_identity(repo, identity, f"audit output {index}")

    validation = audit.get("validation")
    validation_fields = frozenset((
        "schema", "status", "exit_code", "selected_units",
        "effective_source_verified_units", "counts", "corrections_applied",
        "formal_repairs_applied", "general_reviews_applied",
    ))
    require(isinstance(validation, dict) and set(validation) == validation_fields and
            validation.get("schema") == "openlogic-classical-static-validation-v1" and
            validation.get("status") == "STATIC_CHECKS_SATISFIED" and
            validation.get("exit_code") == 0 and
            validation.get("selected_units") == 722 and
            validation.get("effective_source_verified_units") == 722 and
            validation.get("counts") == counts["static_statuses"] and
            validation.get("corrections_applied") == correction_count and
            validation.get("formal_repairs_applied") == formal_count and
            validation.get("general_reviews_applied") == unchanged_count,
            "source-reconciliation validator receipt is incomplete or inconsistent")
    require(isinstance(audit.get("write_policy"), str) and audit["write_policy"].strip(),
            "source-reconciliation audit lacks its write policy")

    closure_raw = closure_path.read_bytes()
    return {
        "path": DEFAULT_SOURCE_CLOSURE.as_posix(),
        "bytes": len(closure_raw),
        "sha256": lower_sha256(closure_raw),
        "schema": CLOSURE_SCHEMA,
        "release_id": release_id,
        "source_snapshot_sha256": snapshot_hash,
        "audit": {
            "path": DEFAULT_SOURCE_RECONCILIATION_AUDIT.as_posix(),
            "bytes": audit_path.stat().st_size,
            "sha256": lower_sha256(audit_path.read_bytes()),
        },
    }


def safe_repo_path(repo: Path, relative: Path, prefix: Path) -> Path:
    require(not relative.is_absolute() and ".." not in relative.parts,
            f"out-of-scope relative path: {relative}")
    path = (repo / relative).resolve()
    root = (repo / prefix).resolve()
    require(path.is_relative_to(root), f"path escapes {prefix}: {relative}")
    return path


def decode_exact(raw: bytes) -> tuple[str, bool]:
    bom = raw.startswith(b"\xef\xbb\xbf")
    body = raw[3:] if bom else raw
    return body.decode("utf-8", errors="strict"), bom


def encode_exact(text: str, bom: bool) -> bytes:
    raw = text.encode("utf-8", errors="strict")
    return (b"\xef\xbb\xbf" + raw) if bom else raw


def tree_hash(files: dict[str, bytes]) -> str:
    """Hash an ordered path/length/byte stream, not filesystem metadata."""
    digest = hashlib.sha256()
    for relative, raw in sorted(files.items()):
        path_bytes = relative.encode("utf-8")
        digest.update(len(path_bytes).to_bytes(8, "big"))
        digest.update(path_bytes)
        digest.update(len(raw).to_bytes(8, "big"))
        digest.update(raw)
    return digest.hexdigest().upper()


def token_body(tokens: list[Token], start: int, opener: str = "{") -> tuple[list[Token], int] | None:
    try:
        return group(tokens, start, opener)
    except ValueError as exc:
        raise MaterializationError(str(exc)) from exc


def one_argument(tokens: list[Token], start: int) -> tuple[list[Token], int] | None:
    parsed = token_body(tokens, start)
    if parsed:
        return parsed
    pos = skip_space(tokens, start)
    if pos >= len(tokens):
        return None
    return [tokens[pos]], pos + 1


def argument_sequence(
    tokens: list[Token], start: int, *, optional: int, required: int,
    allow_star: bool = False,
) -> tuple[list[list[Token]], list[list[Token]], int]:
    """Parse the bounded argument grammar declared in the policy."""
    pos = skip_space(tokens, start)
    if allow_star and pos < len(tokens) and tokens[pos].value == "*":
        pos = skip_space(tokens, pos + 1)
    optional_bodies: list[list[Token]] = []
    for _ in range(optional):
        parsed = token_body(tokens, pos, "[")
        if not parsed:
            break
        body, pos = parsed
        optional_bodies.append(body)
    required_bodies: list[list[Token]] = []
    for _ in range(required):
        parsed = one_argument(tokens, pos)
        if not parsed:
            break
        body, pos = parsed
        required_bodies.append(body)
    return optional_bodies, required_bodies, pos


def candidate_count(tokens: Iterable[Token]) -> int:
    return sum(
        1 for token in tokens
        if token.kind == "char" and ASCII_ALNUM.fullmatch(token.value)
    ) + sum(
        1 for token in tokens
        if token.kind == "command" and token.value[1:] in GREEK_COMMANDS
    )


@dataclass(frozen=True)
class Protection:
    start: int
    end: int
    reason: str
    priority: int


@dataclass(frozen=True)
class Replacement:
    source_start: int
    source_end: int
    source: str
    replacement: str
    occurrence_id: str


@dataclass
class Occurrence:
    occurrence_id: str
    formula_index: int
    formula_kind: str
    source_char_start: int
    source_char_end: int
    source_utf8_byte_start: int
    source_utf8_byte_end: int
    line: int
    column: int
    source: str
    candidate_scalars: int
    category: str
    disposition: str
    reason: str
    replacement: str | None = None
    family: str | None = None
    key: str | None = None
    carrier_evidence: list[dict[str, Any]] | None = None


def span_for_tokens(tokens: list[Token]) -> tuple[int, int] | None:
    if not tokens:
        return None
    return tokens[0].start, tokens[-1].end


def add_protection(
    protections: list[Protection], tokens: list[Token], reason: str, priority: int
) -> None:
    span = span_for_tokens(tokens)
    if span:
        protections.append(Protection(span[0], span[1], reason, priority))


def validate_implicit_carrier_authority(repo: Path) -> dict[str, Any]:
    """Fail closed if the consulted three definitions or their source changed."""
    path = repo / IMPLICIT_CARRIER_CONFIG
    raw = path.read_bytes()
    require(lower_sha256(raw) == IMPLICIT_CARRIER_CONFIG_SHA,
            "implicit math-carrier configuration identity changed")
    lines = raw.decode("utf-8-sig").splitlines()
    for name, (_, number, definition) in IMPLICIT_CARRIERS.items():
        require(len(lines) >= number and lines[number - 1] == definition,
                f"implicit math-carrier definition changed: {name}")
    return {"path": IMPLICIT_CARRIER_CONFIG.as_posix(), "bytes": len(raw),
            "sha256": IMPLICIT_CARRIER_CONFIG_SHA,
            "contracts": {name: {"required_math_arguments": arity, "line": line,
                                  "consulted_definition": definition}
                          for name, (arity, line, definition) in IMPLICIT_CARRIERS.items()},
            "TMtrans_direction_exception": {
                "argument": 3, "exact_literal_tokens": ["R", "L", "N"],
                "reason": "typed machine-direction names, not running variables; policy review remains open"}}


def implicit_definition_spans(tokens: list[Token]) -> list[tuple[int, int]]:
    """Keep carrier-looking tokens in definitions literal; reject shadowing.

    Only the common explicit TeX/LaTeX definition signatures are inspected.
    This does not evaluate definitions, aliases, conditionals or csname code.
    """
    spans: list[tuple[int, int]] = []
    primitives = {"def", "gdef", "edef", "xdef"}
    classic = {"newcommand", "renewcommand", "providecommand", "DeclareRobustCommand"}
    document = {"NewDocumentCommand", "RenewDocumentCommand", "ProvideDocumentCommand",
                "DeclareDocumentCommand", "NewExpandableDocumentCommand",
                "RenewExpandableDocumentCommand", "ProvideExpandableDocumentCommand",
                "DeclareExpandableDocumentCommand"}
    for index, token in enumerate(tokens):
        name = token.value[1:] if token.kind == "command" else ""
        if name not in primitives | classic | document | {"let", "futurelet"}:
            continue
        pos = skip_space(tokens, index + 1)
        if pos < len(tokens) and tokens[pos].value == "*":
            pos = skip_space(tokens, pos + 1)
        target = one_argument(tokens, pos)
        if not target:
            continue
        target_body, pos = target
        visible = [item for item in target_body if item.kind != "space"]
        require(not any(item.kind == "command" and item.value[1:] in IMPLICIT_CARRIERS
                        for item in visible),
                f"shadowed implicit math carrier at character {token.start}")
        if name in {"let", "futurelet"}:
            # Do not misread a carrier on the RHS as an invocation. An alias is
            # not an added contract and its later use is never expanded here.
            pos = skip_space(tokens, pos)
            if pos < len(tokens) and tokens[pos].value == "=":
                pos = skip_space(tokens, pos + 1)
            after = min(len(tokens), pos + (2 if name == "futurelet" else 1))
        else:
            if name in primitives:
                while pos < len(tokens) and tokens[pos].value != "{":
                    pos += 1
            elif name in classic:
                for _ in range(2):
                    option = token_body(tokens, pos, "[")
                    if option:
                        _, pos = option
            else:
                signature = token_body(tokens, pos)
                if not signature:
                    continue
                _, pos = signature
            body = token_body(tokens, pos)
            if not body:
                continue
            _, after = body
        if after > index:
            spans.append((token.start, tokens[after - 1].end))
    return spans


def implicit_carrier_arguments(tokens: list[Token]) -> list[dict[str, Any]]:
    """Recognize only source-bound mTrue/mFalse/TMtrans argument positions."""
    if not any(t.kind == "command" and t.value[1:] in IMPLICIT_CARRIERS for t in tokens):
        return []
    definitions = implicit_definition_spans(tokens)
    arguments: list[dict[str, Any]] = []
    for index, token in enumerate(tokens):
        name = token.value[1:] if token.kind == "command" else ""
        if name not in IMPLICIT_CARRIERS or in_any_span(token.start, definitions):
            continue
        pos = index + 1
        for number in range(1, IMPLICIT_CARRIERS[name][0] + 1):
            pos = skip_space(tokens, pos)
            require(pos < len(tokens) and tokens[pos].value not in ("}", "$", r"\)", r"\]", r"\end"),
                    f"{name} missing math argument {number} at character {token.start}")
            parsed = one_argument(tokens, pos)
            require(parsed is not None, f"{name} lacks argument {number}")
            body, pos = parsed
            if body:
                arguments.append({"name": name, "call_start": token.start,
                                  "argument": number, "tokens": body,
                                  "start": body[0].start, "end": body[-1].end})
    return arguments


def append_implicit_formulas(formulas: list[tuple[str, list[Token]]],
                             arguments: list[dict[str, Any]]) -> list[tuple[str, list[Token]]]:
    """Leave all original formula indices unchanged and append uncovered spans."""
    result = list(formulas)
    covered = {token.start for _, tokens in formulas for token in tokens}
    for arg in arguments:
        run: list[Token] = []
        for token in arg["tokens"] + [None]:
            if token is not None and token.start not in covered:
                run.append(token)
                covered.add(token.start)
            elif run:
                kind = (f"implicit-carrier:{arg['name']}:argument-{arg['argument']}:"
                        f"source-char-{arg['call_start']}:span-{run[0].start}")
                result.append((kind, run))
                run = []
    return result


def explicit_math_spans(tokens: list[Token]) -> list[tuple[int, int]]:
    """Find bounded, explicit math islands within a text/program context.

    The source graphs use $...$ node labels and intertext formulas; also
    recognize paired \\(...\\), \\[...\\], $$...$$ and braced ensuremath.
    Literal lexer tokens and escaped dollar commands cannot open an island.
    Brace depth keeps a nested text argument's dollars from closing its
    surrounding math.  This does not expand macros, evaluate diagram code,
    or infer math mode from arbitrary environments or implicit math labels.
    """
    spans: list[tuple[int, int]] = []
    pos = 0
    while pos < len(tokens):
        token = tokens[pos]
        if token.kind == "command" and token.value == r"\ensuremath":
            parsed = token_body(tokens, pos + 1)
            require(parsed is not None,
                    f"unbraced ensuremath in text/program context at character {token.start}")
            _, after = parsed
            spans.append((token.start, tokens[after - 1].end))
            pos = after
            continue
        if token.value not in ("$", r"\(", r"\["):
            pos += 1
            continue
        double = (token.value == "$" and pos + 1 < len(tokens) and
                  tokens[pos + 1].value == "$" and
                  tokens[pos + 1].start == token.end)
        closer = {"$": "$", r"\(": r"\)", r"\[": r"\]"}[token.value]
        first, depth = pos + (2 if double else 1), 0
        for end in range(first, len(tokens)):
            value = tokens[end].value
            if value == closer and depth == 0:
                if double:
                    require(end + 1 < len(tokens) and tokens[end + 1].value == "$" and
                            tokens[end + 1].start == tokens[end].end,
                            f"single dollar closes display math at character {tokens[end].start}")
                after = end + (2 if double else 1)
                spans.append((token.start, tokens[after - 1].end))
                pos = after
                break
            depth += (value == "{") - (value == "}")
        else:
            raise MaterializationError(
                f"unclosed explicit math in text/program context at character {token.start}"
            )
    return spans


def add_reentrant_protection(
    protections: list[Protection], tokens: list[Token], reason: str, priority: int,
) -> None:
    """Protect syntax while allowing explicit math and three pinned carriers.

    Only this enclosing context is split.  Independent policy protections
    for international escapes, keys, dimensions, definitions, styled names,
    and nested text remain effective inside every reopened math island.
    """
    span = span_for_tokens(tokens)
    if span is None:
        return
    cursor, limit = span
    islands = explicit_math_spans(tokens) + [
        (item["start"], item["end"]) for item in implicit_carrier_arguments(tokens)
    ]
    for start, end in sorted(islands):
        if cursor < start:
            protections.append(Protection(cursor, start, reason, priority))
        cursor = max(cursor, end)
    if cursor < limit:
        protections.append(Protection(cursor, limit, reason, priority))


def protection_at(protections: list[Protection], start: int, end: int) -> Protection | None:
    matches = [item for item in protections if start >= item.start and end <= item.end]
    if not matches:
        return None
    return min(matches, key=lambda item: (item.priority, item.end - item.start, item.reason))


def in_any_span(position: int, spans: list[tuple[int, int]]) -> bool:
    return any(start <= position < end for start, end in spans)


def surrounding_ascii_identifier(text: str, start: int, end: int) -> str | None:
    """Return a lexical ID containing this digit run, but not a plain number."""
    identifier_characters = frozenset(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_:.+-/"
    )
    left, right = start, end
    while left > 0 and text[left - 1] in identifier_characters:
        left -= 1
    while right < len(text) and text[right] in identifier_characters:
        right += 1
    candidate = text[left:right]
    return candidate if ASCII_LETTER.search(candidate) else None


def exact_single_upper(tokens: list[Token]) -> Token | None:
    visible = [token for token in tokens if token.kind != "space"]
    if len(visible) == 1 and visible[0].kind == "char" and UPPER.fullmatch(visible[0].value):
        return visible[0]
    return None


def collect_formula_keys(tokens: list[Token]) -> dict[int, str]:
    result: dict[int, str] = {}
    for index, token in enumerate(tokens):
        if token.kind == "command" and token.value == r"\formula":
            parsed = one_argument(tokens, index + 1)
            require(parsed is not None, f"formula command lacks an argument at character {token.start}")
            body, _ = parsed
            key_token = exact_single_upper(body)
            require(key_token is not None,
                    f"formula command has a non-registry key at character {token.start}")
            result[key_token.start] = key_token.value
        if token.kind != "char" or token.value != "!":
            continue
        pos = skip_space(tokens, index + 1)
        if pos >= len(tokens):
            continue
        if tokens[pos].kind == "char" and UPPER.fullmatch(tokens[pos].value):
            result[tokens[pos].start] = tokens[pos].value
            continue
        parsed = token_body(tokens, pos)
        if parsed:
            body, _ = parsed
            key_token = exact_single_upper(body)
            if key_token is not None:
                result[key_token.start] = key_token.value
    return result


def collect_protections(
    tokens: list[Token], policy: dict[str, Any], *, protected_unit: bool
) -> list[Protection]:
    protections: list[Protection] = []
    if protected_unit:
        add_protection(
            protections, tokens,
            "international reference specimen unit explicitly preserved by policy", 0,
        )
        return protections

    contracts: dict[str, dict[str, Any]] = {}
    for contract in policy["command_contracts"]:
        for name in contract["commands"]:
            require(name not in contracts, f"duplicate command contract: {name}")
            contracts[name] = contract

    review = set(policy["review_argument_commands"])
    arrays = set(policy["array_like_environment_structural_argument"])
    dimensions = set(policy.get("primitive_dimension_commands", []))
    definition_commands = set(policy.get("definition_commands", []))

    for index, token in enumerate(tokens):
        if token.kind != "command":
            continue
        name = token.value[1:]
        if name in contracts:
            contract = contracts[name]
            optional, required, _ = argument_sequence(
                tokens, index + 1,
                optional=int(contract.get("optional", 0)),
                required=int(contract.get("required", 0)),
                allow_star=bool(contract.get("allow_star", False)),
            )
            for position in contract.get("protect_optional", []):
                if position < len(optional):
                    add_protection(
                        protections, optional[position],
                        str(contract["reason"]), 10,
                    )
            for position in contract.get("protect_required", []):
                if position < len(required):
                    protect = (add_reentrant_protection
                               if contract["reason"] == "text-inside-math"
                               else add_protection)
                    protect(
                        protections, required[position],
                        str(contract["reason"]), 10,
                    )

        if name.startswith(policy["cite_command_prefix"]):
            optional, required, _ = argument_sequence(
                tokens, index + 1, optional=3, required=1,
            )
            for body in optional + required:
                add_protection(protections, body, "citation key or locator", 8)

        if name in review:
            _, required, _ = argument_sequence(
                tokens, index + 1, optional=0, required=1,
            )
            if required:
                add_protection(
                    protections, required[0],
                    "styled whole identifier retained because no equivalent Arabic mathematical style family is registered",
                    12,
                )

        if name == "begin":
            _, required, pos = argument_sequence(
                tokens, index + 1, optional=0, required=1,
            )
            if required:
                env = "".join(t.value for t in required[0] if t.kind != "space")
                if env in arrays:
                    pos = skip_space(tokens, pos)
                    optional = token_body(tokens, pos, "[")
                    if optional:
                        add_protection(
                            protections, optional[0],
                            "array alignment placement option", 7,
                        )
                        pos = optional[1]
                    columns = one_argument(tokens, pos)
                    if columns:
                        add_protection(
                            protections, columns[0],
                            "array column specification is structural TeX syntax", 7,
                        )

        if name in dimensions:
            pos = skip_space(tokens, index + 1)
            if pos < len(tokens) and tokens[pos].value == "*":
                pos = skip_space(tokens, pos + 1)
            parsed = token_body(tokens, pos)
            if parsed:
                add_protection(
                    protections, parsed[0],
                    "layout dimension is not a mathematical numeral or identifier", 6,
                )
            else:
                start = pos
                while pos < len(tokens):
                    value = tokens[pos].value
                    if tokens[pos].kind == "space" or value in ("&", "{", "}", "$", r"\)", r"\]"):
                        break
                    if tokens[pos].kind == "command":
                        break
                    pos += 1
                add_protection(
                    protections, tokens[start:pos],
                    "unbraced layout dimension is not mathematical notation", 6,
                )

        if token.value == r"\\":
            optional = token_body(tokens, index + 1, "[")
            if optional:
                add_protection(
                    protections, optional[0],
                    "row-break spacing is a layout dimension, not mathematical notation", 6,
                )

        if name in definition_commands:
            pos = skip_space(tokens, index + 1)
            if pos < len(tokens) and tokens[pos].kind == "command":
                pos = skip_space(tokens, pos + 1)
            body = token_body(tokens, pos)
            if body:
                add_protection(
                    protections, body[0],
                    "local TeX definition body is implementation syntax, not displayed mathematical notation", 5,
                )
    return protections


def collect_math_field_boundaries(
    tokens: list[Token], protections: list[Protection],
) -> set[int]:
    """Keep source TeX argument/field boundaries ahead of lexical run merging.

    A naked script or undelimited macro argument consumes one token, not an
    adjacent digit/letter run.  Thus x_12, \\frac12 and \\sqrt12 must not acquire
    the meaning of x_{12}, \\frac{12} or \\sqrt{12} when wrappers are inserted.
    Existing groups still permit whole runs.  This is a finite source-token
    scanner, not expansion of arbitrary user macros.

    Signatures were consulted in the installed amsmath.sty (frac/binom,
    genfrac, root, cfrac, overset/underset/sideset, smash, boxed, substack),
    base latex.ltx/fontmath.ltx (sqrt, stackrel, ensuremath, phantoms and
    accents), units/nicefrac.sty, cancel/cancel.sty, and the Classical RTL
    accent wrappers.  The policy's transparent list is NOT an arity table:
    notably root is delimited, sqrt has a mathematical optional index,
    cfrac/smash have structural options, and not consumes no argument.
    """
    boundaries: set[int] = set()
    one = frozenset((
        "ensuremath overline underline overbrace underbrace widehat widetilde "
        "hat check breve acute grave dot ddot dddot ddddot vec bar tilde "
        "mathring mathord mathop mathbin mathrel mathopen mathclose mathpunct "
        "mathinner substack phantom vphantom hphantom boxed cancel bcancel "
        "xcancel sqrtsign overrightarrow overleftarrow underrightarrow "
        "underleftarrow"
    ).split())
    two = frozenset((
        "frac dfrac tfrac binom dbinom tbinom overset underset stackrel cancelto"
    ).split())
    three = frozenset(("sideset", "overunderset"))

    def argument(pos: int, *, structural: str | None = None) -> int:
        pos = skip_space(tokens, pos)
        parsed = token_body(tokens, pos)
        if parsed is not None:
            body, after = parsed
        elif pos < len(tokens):
            body, after = [tokens[pos]], pos + 1
            boundaries.update((tokens[pos].start, tokens[pos].end))
        else:
            return pos
        if structural is not None:
            add_protection(protections, body, structural, 7)
        return after

    def optional(pos: int, *, structural: str | None = None) -> int:
        pos = skip_space(tokens, pos)
        if pos >= len(tokens) or tokens[pos].value != "[":
            return pos
        # TeX's delimited [#1] parameter ends at the first unbraced ], not
        # at a balanced closing square bracket. Braced nested content is safe.
        first, depth = pos + 1, 0
        for end in range(first, len(tokens)):
            value = tokens[end].value
            if value == "]" and depth == 0:
                if structural is not None:
                    add_protection(protections, tokens[first:end], structural, 7)
                return end + 1
            depth += (value == "{") - (value == "}")
        raise MaterializationError(
            f"unclosed math-command option at character {tokens[pos].start}"
        )

    for index, token in enumerate(tokens):
        if protection_at(protections, token.start, token.end):
            continue
        if token.kind == "char" and token.value in ("^", "_"):
            argument(index + 1)
            continue
        if token.kind != "command":
            continue
        name, pos = token.value[1:], index + 1
        if name in one | two | three:
            arity = 1 if name in one else 2 if name in two else 3
            for _ in range(arity):
                pos = argument(pos)
        elif name in ("sqrt", "cfrac", "nicefrac", "smash"):
            structural = None if name == "sqrt" else (
                f"{name} option is TeX alignment, axis or style syntax, not mathematical notation"
            )
            pos = optional(pos, structural=structural)
            for _ in range(2 if name in ("cfrac", "nicefrac") else 1):
                pos = argument(pos)
        elif name == "genfrac":
            for _ in range(4):
                pos = argument(pos, structural=(
                    "genfrac delimiter, rule thickness or style argument is structural TeX syntax"
                ))
            for _ in range(2):
                pos = argument(pos)
        elif name == "root":
            # AMS root permits leading uproot/leftroot integer adjustments.
            # Its index is otherwise delimited by an unbraced \of, NOT one
            # token; only the following radicand is one token or one group.
            pos = skip_space(tokens, pos)
            for _ in range(2):
                if pos >= len(tokens) or tokens[pos].value not in (
                    r"\uproot", r"\leftroot",
                ):
                    break
                pos = skip_space(tokens, argument(pos + 1, structural=(
                    "root positioning adjustment is structural TeX syntax"
                )))
            depth = 0
            for end in range(pos, len(tokens)):
                value = tokens[end].value
                if value == r"\of" and depth == 0:
                    argument(end + 1)
                    break
                depth += (value == "{") - (value == "}")
            else:
                raise MaterializationError(
                    f"root lacks its unbraced of delimiter at character {token.start}"
                )
    return boundaries


def char_line_column(text: str, start: int) -> tuple[int, int]:
    line = text.count("\n", 0, start) + 1
    previous = text.rfind("\n", 0, start)
    return line, start - previous


def utf8_offset(text: str, position: int, bom: bool) -> int:
    return (3 if bom else 0) + len(text[:position].encode("utf-8"))


def new_occurrence(
    *, unit_id: str, sequence: int, formula_index: int, formula_kind: str,
    text: str, bom: bool, start: int, end: int, source: str,
    candidate_scalars: int, category: str, disposition: str, reason: str,
    replacement: str | None = None, family: str | None = None,
    key: str | None = None,
) -> Occurrence:
    line, column = char_line_column(text, start)
    return Occurrence(
        occurrence_id=f"{unit_id}-N{sequence:06d}",
        formula_index=formula_index,
        formula_kind=formula_kind,
        source_char_start=start,
        source_char_end=end,
        source_utf8_byte_start=utf8_offset(text, start, bom),
        source_utf8_byte_end=utf8_offset(text, end, bom),
        line=line,
        column=column,
        source=source,
        candidate_scalars=candidate_scalars,
        category=category,
        disposition=disposition,
        reason=reason,
        replacement=replacement,
        family=family,
        key=key,
    )


def classify_unit(
    unit_id: str, text: str, bom: bool, policy: dict[str, Any],
    greek_registry: set[str], *, carrier_authority: dict[str, Any] | None = None,
) -> tuple[list[Occurrence], list[Replacement], dict[str, int]]:
    analysis = analyze(text)
    require(not analysis.errors,
            f"{unit_id} has parser anomalies: {'; '.join(analysis.errors)}")
    carriers = implicit_carrier_arguments(analysis.tokens)
    carrier_definition_spans = (implicit_definition_spans(analysis.tokens)
        if any(t.kind == "command" and t.value[1:] in IMPLICIT_CARRIERS for t in analysis.tokens) else [])
    if carriers:
        if carrier_authority is None:
            carrier_authority = validate_implicit_carrier_authority(Path(__file__).resolve().parents[1])
        require(carrier_authority.get("sha256") == IMPLICIT_CARRIER_CONFIG_SHA,
                "unbound implicit math-carrier authority")
    formulas = append_implicit_formulas(analysis.formulas, carriers)
    forbidden = set(policy["forbidden_preexisting_materialization_commands"])
    protected_ids = {item["id"] for item in policy["protected_unit_formulas"]}
    occurrences: list[Occurrence] = []
    replacements: list[Replacement] = []
    assigned: set[tuple[int, int, str]] = set()
    expected_ascii: set[int] = set()
    expected_greek: set[int] = set()
    expected_text_digits: set[int] = set()
    sequence = 0

    # The validator discovers these blocks even when an outer align/math
    # segment contains them.  TikZ node names, coordinates, options and
    # dimensions remain literal; explicit math and the three pinned carrier
    # arguments reopen classification. Installed tikz.code.tex puts text in an hbox
    # (tikz@do@fig); amsmath's intertext likewise restores text in a vbox.
    program_protections: list[Protection] = []
    for start, end in analysis.opaque_spans:
        add_reentrant_protection(
            program_protections,
            [token for token in analysis.tokens
             if start <= token.start and token.end <= end],
            "program, diagram, proof-tree, or rendering implementation block outside explicit math",
            2,
        )

    # Supplemental carrier slices may straddle an already recognized formula.
    # Collect their independent contracts from the complete source, not from a
    # truncated token slice. This preserves keys, styles and definitions around
    # the newly recognized math; only text/program containers are reentrant.
    carrier_protections = (collect_protections(
        analysis.tokens, policy, protected_unit=unit_id in protected_ids,
    ) if carriers or carrier_definition_spans else [])
    if carriers or carrier_definition_spans:
        carrier_protections.extend(Protection(start, end,
            "local TeX definition or alias is implementation syntax, not displayed mathematical notation", 5)
            for start, end in carrier_definition_spans)
        for arg in carriers:
            visible = [t for t in arg["tokens"] if t.kind != "space"]
            if (arg["name"] == "TMtrans" and arg["argument"] == 3 and len(visible) == 1 and
                    visible[0].kind == "char" and visible[0].value in ("R", "L", "N")):
                add_protection(carrier_protections, visible,
                    "typed machine-direction literal in TMtrans argument 3 (R/L/N); "
                    "not a running variable; retained explicitly pending notation-policy review", 4)
    carrier_boundaries = {edge for arg in carriers for edge in (arg["start"], arg["end"])}
    supplemental_field_protections = list(carrier_protections) + program_protections
    supplemental_boundaries: set[int] = set()
    supplemental_keys: dict[int, str] = {}
    for arg in carriers:
        supplemental_boundaries.update(collect_math_field_boundaries(arg["tokens"], supplemental_field_protections))
        supplemental_keys.update(collect_formula_keys(arg["tokens"]))

    for formula_index, (formula_kind, tokens) in enumerate(formulas):
        for token in tokens:
            if token.kind == "command":
                require(token.value[1:] not in forbidden,
                        f"{unit_id} already contains forbidden wrapper {token.value} at character {token.start}")
            if token.kind == "char" and ASCII_ALNUM.fullmatch(token.value):
                expected_ascii.add(token.start)
            elif token.kind == "command" and token.value[1:] in GREEK_COMMANDS:
                expected_greek.add(token.start)

        supplemental = formula_index >= len(analysis.formulas)
        protections = (list(supplemental_field_protections) if supplemental else collect_protections(
            tokens, policy, protected_unit=unit_id in protected_ids,
        ))
        # Global carrier protections also bind calls inside an existing formula.
        if carrier_protections:
            protections.extend(carrier_protections)
        protections.extend(program_protections)
        math_field_boundaries = ((supplemental_boundaries if supplemental else
                                 collect_math_field_boundaries(tokens, protections)) | carrier_boundaries)
        formula_keys = supplemental_keys if supplemental else collect_formula_keys(tokens)
        pos = 0
        while pos < len(tokens):
            token = tokens[pos]
            if token.kind == "command" and token.value[1:] in GREEK_COMMANDS:
                name = token.value[1:]
                protection = protection_at(protections, token.start, token.end)
                sequence += 1
                if protection:
                    occurrence = new_occurrence(
                        unit_id=unit_id, sequence=sequence,
                        formula_index=formula_index, formula_kind=formula_kind,
                        text=text, bom=bom, start=token.start, end=token.end,
                        source=token.value, candidate_scalars=1,
                        category="greek-command", disposition="explicit-international-exemption",
                        reason=protection.reason,
                    )
                elif name in greek_registry:
                    replacement = rf"{{\OLId{{greek-variable}}{{{name}}}}}"
                    occurrence = new_occurrence(
                        unit_id=unit_id, sequence=sequence,
                        formula_index=formula_index, formula_kind=formula_kind,
                        text=text, bom=bom, start=token.start, end=token.end,
                        source=token.value, candidate_scalars=1,
                        category="greek-command", disposition="typed-arabic-letter-wrapper",
                        reason="exact Greek variable has an authority-bound Arabic registry entry",
                        replacement=replacement, family="greek-variable", key=name,
                    )
                    replacements.append(Replacement(
                        token.start, token.end, token.value, replacement,
                        occurrence.occurrence_id,
                    ))
                else:
                    occurrence = new_occurrence(
                        unit_id=unit_id, sequence=sequence,
                        formula_index=formula_index, formula_kind=formula_kind,
                        text=text, bom=bom, start=token.start, end=token.end,
                        source=token.value, candidate_scalars=1,
                        category="greek-command", disposition="explicit-international-exemption",
                        reason=("no authority-bound Arabic mathematical presentation is registered for this Greek symbol; "
                                "preserving the semantic command is safer than inventing a substitution"),
                    )
                occurrences.append(occurrence)
                assigned.add((token.start, token.end, "greek"))
                pos += 1
                continue

            if token.kind != "char" or not ASCII_ALNUM.fullmatch(token.value):
                pos += 1
                continue

            is_digit = bool(ASCII_DIGIT.fullmatch(token.value))
            end_pos = pos + 1
            protection = protection_at(protections, token.start, token.end)
            formula_key = formula_keys.get(token.start)
            while end_pos < len(tokens):
                nxt = tokens[end_pos]
                if nxt.kind != "char" or nxt.start != tokens[end_pos - 1].end:
                    break
                if nxt.start in math_field_boundaries:
                    break
                if is_digit != bool(ASCII_DIGIT.fullmatch(nxt.value)):
                    break
                if not ASCII_ALNUM.fullmatch(nxt.value):
                    break
                if protection_at(protections, nxt.start, nxt.end) != protection:
                    break
                if formula_keys.get(nxt.start) != formula_key:
                    break
                end_pos += 1
            run = tokens[pos:end_pos]
            start, end = run[0].start, run[-1].end
            source = text[start:end]
            require(all(item.start not in {s for s, _, kind in assigned if kind == "ascii"}
                        for item in run), f"duplicate ASCII assignment in {unit_id}")
            sequence += 1
            if protection:
                occurrence = new_occurrence(
                    unit_id=unit_id, sequence=sequence,
                    formula_index=formula_index, formula_kind=formula_kind,
                    text=text, bom=bom, start=start, end=end, source=source,
                    candidate_scalars=len(run), category="ascii-digit-run" if is_digit else "ascii-letter-run",
                    disposition="explicit-international-exemption", reason=protection.reason,
                )
            elif formula_key:
                require(len(run) == 1 and source == formula_key,
                        f"invalid formula-key run in {unit_id} at {start}")
                occurrence = new_occurrence(
                    unit_id=unit_id, sequence=sequence,
                    formula_index=formula_index, formula_kind=formula_kind,
                    text=text, bom=bom, start=start, end=end, source=source,
                    candidate_scalars=1, category="formula-metavariable",
                    disposition="typed-arabic-formula-hook",
                    reason="the existing exact !X or formula{X} parser consumes this single registered key",
                    family="formula", key=formula_key,
                )
            elif is_digit:
                replacement = rf"{{\OLMathNumeral{{{source}}}}}"
                occurrence = new_occurrence(
                    unit_id=unit_id, sequence=sequence,
                    formula_index=formula_index, formula_kind=formula_kind,
                    text=text, bom=bom, start=start, end=end, source=source,
                    candidate_scalars=len(run), category="ascii-digit-run",
                    disposition="typed-eastern-arabic-numeral-wrapper",
                    reason=("visible mathematical numeral; exact ASCII source run, bounded by original TeX "
                            "fields and command arguments, remains the reversible wrapper argument; the outer "
                            "group makes the complete typed wrapper one math field"),
                    replacement=replacement,
                )
                replacements.append(Replacement(
                    start, end, source, replacement, occurrence.occurrence_id,
                ))
            elif len(run) == 1:
                family = "latin-ordinary" if source.islower() else "latin-looped"
                replacement = rf"{{\OLId{{{family}}}{{{source}}}}}"
                occurrence = new_occurrence(
                    unit_id=unit_id, sequence=sequence,
                    formula_index=formula_index, formula_kind=formula_kind,
                    text=text, bom=bom, start=start, end=end, source=source,
                    candidate_scalars=1, category="ascii-letter-run",
                    disposition="typed-arabic-letter-wrapper",
                    reason=("single mathematical identifier outside every protected whole-name, text, style, key, "
                            "layout, and international-specimen context"),
                    replacement=replacement, family=family, key=source,
                )
                replacements.append(Replacement(
                    start, end, source, replacement, occurrence.occurrence_id,
                ))
            else:
                occurrence = new_occurrence(
                    unit_id=unit_id, sequence=sequence,
                    formula_index=formula_index, formula_kind=formula_kind,
                    text=text, bom=bom, start=start, end=end, source=source,
                    candidate_scalars=len(run), category="ascii-letter-run",
                    disposition="explicit-international-exemption",
                    reason=("contiguous multi-letter identifier retained as one semantic name; letter-by-letter mapping "
                            "would falsely assert a product or independently typed variables"),
                )
            occurrences.append(occurrence)
            for item in run:
                assigned.add((item.start, item.end, "ascii"))
            pos = end_pos

    # Arabic prose numerals are a separate typed presentation concern.  Scan
    # every ASCII digit outside formula spans too: visibly numeric runs use the
    # expandable text wrapper; machine/layout arguments and alphanumeric
    # identifiers receive explicit source-addressed exemptions.  Formula
    # candidates have already been assigned above and can never overlap these.
    formula_spans = [
        (tokens[0].start, tokens[-1].end)
        for _, tokens in formulas if tokens
    ]
    text_protections = collect_protections(
        analysis.tokens, policy, protected_unit=False,
    )
    text_protections.extend(Protection(start, end,
        "local TeX definition or alias is implementation syntax, not displayed mathematical notation", 5)
        for start, end in carrier_definition_spans)
    for start, end in analysis.masks:
        if not any(start == left and end == right for left, right in formula_spans):
            text_protections.append(Protection(
                start, end,
                "non-rendered TeX key, file/import identity, terminology key, or literal block",
                40,
            ))
    for start, end in analysis.opaque_spans:
        text_protections.append(Protection(
            start, end,
            "program, diagram, proof-tree, or rendering implementation block",
            2,
        ))

    tokens = analysis.tokens
    for token in tokens:
        if (token.kind == "char" and ASCII_DIGIT.fullmatch(token.value) and
                not in_any_span(token.start, formula_spans)):
            expected_text_digits.add(token.start)
    pos = 0
    while pos < len(tokens):
        token = tokens[pos]
        if (token.kind != "char" or not ASCII_DIGIT.fullmatch(token.value) or
                in_any_span(token.start, formula_spans)):
            pos += 1
            continue
        protection = protection_at(text_protections, token.start, token.end)
        end_pos = pos + 1
        while end_pos < len(tokens):
            nxt = tokens[end_pos]
            if (nxt.kind != "char" or not ASCII_DIGIT.fullmatch(nxt.value) or
                    nxt.start != tokens[end_pos - 1].end or
                    in_any_span(nxt.start, formula_spans) or
                    protection_at(text_protections, nxt.start, nxt.end) != protection):
                break
            end_pos += 1
        run = tokens[pos:end_pos]
        start, end = run[0].start, run[-1].end
        source = text[start:end]
        identifier = surrounding_ascii_identifier(text, start, end)
        sequence += 1
        if protection:
            occurrence = new_occurrence(
                unit_id=unit_id, sequence=sequence,
                formula_index=-1, formula_kind="prose-or-structure",
                text=text, bom=bom, start=start, end=end, source=source,
                candidate_scalars=len(run), category="ascii-text-digit-run",
                disposition="explicit-international-exemption",
                reason=protection.reason,
            )
        elif identifier is not None:
            occurrence = new_occurrence(
                unit_id=unit_id, sequence=sequence,
                formula_index=-1, formula_kind="prose-or-structure",
                text=text, bom=bom, start=start, end=end, source=source,
                candidate_scalars=len(run), category="ascii-text-digit-run",
                disposition="explicit-international-exemption",
                reason=("digit run belongs to an ASCII alphanumeric identifier; "
                        f"preserve the exact international identity {identifier!r}"),
            )
        else:
            replacement = rf"\OLClassicalDigits{{{source}}}"
            occurrence = new_occurrence(
                unit_id=unit_id, sequence=sequence,
                formula_index=-1, formula_kind="prose-or-structure",
                text=text, bom=bom, start=start, end=end, source=source,
                candidate_scalars=len(run), category="ascii-text-digit-run",
                disposition="typed-eastern-arabic-text-numeral-wrapper",
                reason=("visible non-formula numeral in Arabic content; exact ASCII source run "
                        "remains the reversible expandable-wrapper argument"),
                replacement=replacement,
            )
            replacements.append(Replacement(
                start, end, source, replacement, occurrence.occurrence_id,
            ))
        occurrences.append(occurrence)
        for item in run:
            assigned.add((item.start, item.end, "text-digit"))
        pos = end_pos

    assigned_ascii = {start for start, _, kind in assigned if kind == "ascii"}
    assigned_greek = {start for start, _, kind in assigned if kind == "greek"}
    assigned_text_digits = {
        start for start, _, kind in assigned if kind == "text-digit"
    }
    missing_ascii = sorted(expected_ascii - assigned_ascii)
    missing_greek = sorted(expected_greek - assigned_greek)
    missing_text_digits = sorted(expected_text_digits - assigned_text_digits)
    require(not missing_ascii and not missing_greek and not missing_text_digits,
            f"{unit_id} has untreated candidates: ascii={missing_ascii[:8]}, "
            f"greek={missing_greek[:8]}, text-digits={missing_text_digits[:8]}")
    require(len(assigned_ascii) == len(expected_ascii), f"{unit_id} duplicate ASCII candidate assignment")
    require(len(assigned_greek) == len(expected_greek), f"{unit_id} duplicate Greek candidate assignment")
    require(len(assigned_text_digits) == len(expected_text_digits),
            f"{unit_id} duplicate text-digit candidate assignment")

    for left, right in zip(sorted(replacements, key=lambda item: item.source_start),
                           sorted(replacements, key=lambda item: item.source_start)[1:]):
        require(left.source_end <= right.source_start,
                f"overlapping replacements in {unit_id}: {left.occurrence_id}, {right.occurrence_id}")
    for occurrence in occurrences:
        evidence = []
        for arg in carriers:
            if arg["start"] <= occurrence.source_char_start and occurrence.source_char_end <= arg["end"]:
                evidence.append({"carrier": arg["name"], "argument": arg["argument"],
                    "call_source_char_start": arg["call_start"],
                    "authority_path": IMPLICIT_CARRIER_CONFIG.as_posix(),
                    "authority_sha256": IMPLICIT_CARRIER_CONFIG_SHA,
                    "authority_line": IMPLICIT_CARRIERS[arg["name"]][1],
                    "consulted_definition": IMPLICIT_CARRIERS[arg["name"]][2]})
        if evidence:
            occurrence.carrier_evidence = evidence
    summary = {
        "formula_segments": len(formulas),
        "implicit_carrier_segments": len(formulas) - len(analysis.formulas),
        "ascii_candidate_scalars": len(expected_ascii),
        "text_digit_candidate_scalars": len(expected_text_digits),
        "greek_candidate_commands": len(expected_greek),
        "occurrence_records": len(occurrences),
        "replacement_records": len(replacements),
        "untreated_candidates": 0,
    }
    return occurrences, replacements, summary


def apply_replacements(text: str, replacements: list[Replacement]) -> tuple[str, list[dict[str, Any]]]:
    output = text
    transformed_spans: list[dict[str, Any]] = []
    delta = 0
    for replacement in sorted(replacements, key=lambda item: item.source_start):
        require(text[replacement.source_start:replacement.source_end] == replacement.source,
                f"source span drift: {replacement.occurrence_id}")
        transformed_start = replacement.source_start + delta
        transformed_end = transformed_start + len(replacement.replacement)
        output = output[:transformed_start] + replacement.replacement + output[transformed_start + len(replacement.source):]
        transformed_spans.append({
            "occurrence_id": replacement.occurrence_id,
            "presented_char_start": transformed_start,
            "presented_char_end": transformed_end,
        })
        delta += len(replacement.replacement) - len(replacement.source)
    return output, transformed_spans


def inverse_reconstruct(presented: str, replacements: list[Replacement],
                        transformed_spans: list[dict[str, Any]]) -> str:
    by_id = {item.occurrence_id: item for item in replacements}
    output = presented
    for span in reversed(transformed_spans):
        replacement = by_id[span["occurrence_id"]]
        start, end = span["presented_char_start"], span["presented_char_end"]
        require(output[start:end] == replacement.replacement,
                f"presented span drift: {replacement.occurrence_id}")
        output = output[:start] + replacement.source + output[end:]
    return output


def atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".tmp-{os.getpid()}")
    require(not temporary.exists(), f"temporary output already exists: {temporary}")
    try:
        temporary.write_bytes(raw)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def contract_text(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    release_eligible = "true" if payload["release_eligible"] else "false"
    return (
        "% Generated by build/materialize_classical_notation.py; do not hand-edit.\n"
        f"\\def\\OLClassicalMaterializationStatus{{{payload['status']}}}\n"
        f"\\def\\OLClassicalMaterializationMode{{{payload['mode']}}}\n"
        f"\\def\\OLClassicalMaterializationReleaseEligible{{{release_eligible}}}\n"
        f"\\def\\OLClassicalMaterializationSourceTreeSHA{{{payload['source_tree_sha256']}}}\n"
        f"\\def\\OLClassicalMaterializationPresentationTreeSHA{{{payload['presentation_tree_sha256']}}}\n"
        f"\\def\\OLClassicalMaterializationFormulaSegments{{{summary['formula_segments']}}}\n"
        f"\\def\\OLClassicalMaterializationASCIICandidates{{{summary['ascii_candidate_scalars']}}}\n"
        f"\\def\\OLClassicalMaterializationTextDigitCandidates{{{summary['text_digit_candidate_scalars']}}}\n"
        f"\\def\\OLClassicalMaterializationGreekCandidates{{{summary['greek_candidate_commands']}}}\n"
        f"\\def\\OLClassicalMaterializationReplacements{{{summary['replacement_records']}}}\n"
        "\\typeout{OL-CLASSICAL-MATERIALIZATION=source-addressed-wrappers-v2}\n"
        "\\typeout{OL-CLASSICAL-MATERIALIZATION-STATUS=\\OLClassicalMaterializationStatus}\n"
        "\\typeout{OL-CLASSICAL-MATERIALIZATION-MODE=\\OLClassicalMaterializationMode}\n"
        "\\typeout{OL-CLASSICAL-MATERIALIZATION-RELEASE-ELIGIBLE=\\OLClassicalMaterializationReleaseEligible}\n"
        "\\typeout{OL-CLASSICAL-MATERIALIZATION-SOURCE-TREE-SHA256=\\OLClassicalMaterializationSourceTreeSHA}\n"
        "\\typeout{OL-CLASSICAL-MATERIALIZATION-PRESENTATION-TREE-SHA256=\\OLClassicalMaterializationPresentationTreeSHA}\n"
        "\\typeout{OL-CLASSICAL-MATERIALIZATION-COVERAGE="
        "formulas-\\OLClassicalMaterializationFormulaSegments;"
        "ascii-\\OLClassicalMaterializationASCIICandidates;"
        "text-digits-\\OLClassicalMaterializationTextDigitCandidates;"
        "greek-\\OLClassicalMaterializationGreekCandidates;"
        "replacements-\\OLClassicalMaterializationReplacements;untreated-0}\n"
    )


def markdown_summary(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    dispositions = summary["dispositions"]
    lines = [
        "# Classical notation materialization summary",
        "",
        f"Status: **{payload['status']}**",
        "",
        "This is a machine-generated, reversible presentation overlay. The accepted",
        "Classical translation remains authoritative; each wrapper retains the exact",
        "source token in its argument, and every exemption is source-addressed.",
        "",
        f"- Units: {summary['units']}",
        f"- Formula segments: {summary['formula_segments']}",
        f"- ASCII letter/digit candidate scalars: {summary['ascii_candidate_scalars']}",
        f"- Non-formula ASCII digit candidate scalars: {summary['text_digit_candidate_scalars']}",
        f"- Greek command candidates: {summary['greek_candidate_commands']}",
        f"- Replacement records: {summary['replacement_records']}",
        f"- Untreated candidates: {summary['untreated_candidates']}",
        f"- Source tree SHA-256: `{payload['source_tree_sha256']}`",
        f"- Presentation tree SHA-256: `{payload['presentation_tree_sha256']}`",
        "",
        "## Dispositions",
        "",
        "| Disposition | Occurrence records | Candidate scalars/commands |",
        "| --- | ---: | ---: |",
    ]
    for name, values in sorted(dispositions.items()):
        lines.append(f"| `{name}` | {values['records']} | {values['candidates']} |")
    lines.extend([
        "",
        "The complete source paths, line/column locations, original spans,",
        "replacements, reasons, hashes, and inverse checks are in",
        "`NOTATION_MATERIALIZATION_DECISIONS.json`.",
        "",
    ])
    return "\n".join(lines)


def build_payload(
    repo: Path, policy_path: Path, baseline_path: Path, letters_path: Path,
    sets_path: Path, *, mode: str, source_closure: Path | None,
) -> tuple[dict[str, Any], dict[str, bytes], bytes, bytes]:
    policy = json_load(policy_path)
    baseline = json_load(baseline_path)
    letters = json_load(letters_path)
    sets = json_load(sets_path)
    carrier_authority = validate_implicit_carrier_authority(repo)
    require(policy.get("schema") == POLICY_SCHEMA, "unsupported materialization policy schema")
    require(baseline.get("schema") == BASELINE_SCHEMA and baseline.get("total_units") == 722,
            "baseline must be the exact 722-unit Classical authority")
    units = baseline.get("units")
    require(isinstance(units, list) and len(units) == 722, "baseline must contain 722 units")
    require(letters.get("schema") == LETTER_SCHEMA and
            letters.get("status") == "implemented-opt-in-nucleus-not-rendered-or-full-occurrence-coverage",
            "letter presentation registry implementation status drifted")
    require(sets.get("status") == "implemented-awaiting-guarded-render-test",
            "set-symbol registry implementation status drifted")
    greek_registry = {
        entry["key"] for entry in letters["entries"]
        if entry.get("family") == "greek-variable"
    }
    require(greek_registry == {"Gamma", "Delta", "alpha"},
            "Greek registry scope drifted")
    require(mode in ("working", "final"), "invalid materialization mode")
    source_closure_identity = None
    if mode == "final":
        require(source_closure is not None and source_closure.is_file(),
                "final materialization requires the post-freeze source-closure receipt")
        source_closure_identity = validate_source_closure(
            repo, source_closure, baseline_path,
        )

    ids = [item.get("id") for item in units]
    require(ids == [f"OLP-{number:04d}" for number in range(1, 723)],
            "baseline ids must be contiguous OLP-0001..OLP-0722")
    source_files: dict[str, bytes] = {}
    presented_files: dict[str, bytes] = {}
    unit_payloads: list[dict[str, Any]] = []
    totals: Counter[str] = Counter()
    disposition_records: Counter[str] = Counter()
    disposition_candidates: Counter[str] = Counter()

    for item in units:
        unit_id = item["id"]
        source_relative = Path(item["target_path"])
        require(source_relative.parts[:len(SOURCE_PREFIX.parts)] == SOURCE_PREFIX.parts,
                f"{unit_id} target is outside the Classical source tree")
        source_path = safe_repo_path(repo, source_relative, SOURCE_PREFIX)
        raw_before = source_path.read_bytes()
        text, bom = decode_exact(raw_before)
        suffix = Path(*source_relative.parts[len(SOURCE_PREFIX.parts):])
        presented_relative = PRESENTATION_PREFIX / suffix
        occurrences, replacements, unit_summary = classify_unit(
            unit_id, text, bom, policy, greek_registry, carrier_authority=carrier_authority,
        )
        presented_text, transformed_spans = apply_replacements(text, replacements)
        reconstructed = inverse_reconstruct(presented_text, replacements, transformed_spans)
        require(reconstructed == text, f"{unit_id} inverse character reconstruction failed")
        presented_raw = encode_exact(presented_text, bom)
        reconstructed_raw = encode_exact(reconstructed, bom)
        require(reconstructed_raw == raw_before,
                f"{unit_id} inverse byte reconstruction failed")
        require(source_path.read_bytes() == raw_before,
                f"{unit_id} source changed during materialization")

        span_by_id = {span["occurrence_id"]: span for span in transformed_spans}
        occurrence_dicts = []
        for occurrence in occurrences:
            record = asdict(occurrence)
            if occurrence.occurrence_id in span_by_id:
                record.update(span_by_id[occurrence.occurrence_id])
            occurrence_dicts.append({key: value for key, value in record.items() if value is not None})
            disposition_records[occurrence.disposition] += 1
            disposition_candidates[occurrence.disposition] += occurrence.candidate_scalars
        for key, value in unit_summary.items():
            totals[key] += value
        source_key = source_relative.as_posix()
        presented_key = presented_relative.as_posix()
        source_files[source_key] = raw_before
        presented_files[presented_key] = presented_raw
        unit_payloads.append({
            "id": unit_id,
            "source": {
                "path": source_key,
                "bytes": len(raw_before),
                "sha256": sha256_bytes(raw_before),
                "utf8_bom": bom,
            },
            "presentation": {
                "path": presented_key,
                "bytes": len(presented_raw),
                "sha256": sha256_bytes(presented_raw),
            },
            "formula_segments": unit_summary["formula_segments"],
            "ascii_candidate_scalars": unit_summary["ascii_candidate_scalars"],
            "text_digit_candidate_scalars": unit_summary["text_digit_candidate_scalars"],
            "greek_candidate_commands": unit_summary["greek_candidate_commands"],
            "occurrence_records": len(occurrence_dicts),
            "replacement_records": len(replacements),
            "untreated_candidates": 0,
            "inverse_reconstruction": {
                "status": "PASS",
                "bytes": len(reconstructed_raw),
                "sha256": sha256_bytes(reconstructed_raw),
                "equals_source_bytes": True,
            },
            "occurrences": occurrence_dicts,
        })

    require(len(source_files) == 722 and len(presented_files) == 722,
            "source/presentation path uniqueness failure")
    require(totals["untreated_candidates"] == 0, "untreated candidates remain")
    require(validate_implicit_carrier_authority(repo) == carrier_authority,
            "implicit math-carrier source changed during materialization")
    for relative, frozen_raw in source_files.items():
        require((repo / relative).read_bytes() == frozen_raw,
                f"source changed after its unit was classified: {relative}")
    if mode == "final":
        closing_identity = validate_source_closure(
            repo, source_closure, baseline_path,  # type: ignore[arg-type]
        )
        require(closing_identity == source_closure_identity,
                "source closure changed during final materialization")
    payload: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "WORKING_UNFROZEN_SOURCE_SNAPSHOT" if mode == "working" else "PASS",
        "release_eligible": mode == "final",
        "mode": mode,
        "presentation_locale": PRESENTATION_LOCALE,
        "authority": {
            "baseline": {
                "path": baseline_path.relative_to(repo).as_posix(),
                "bytes": baseline_path.stat().st_size,
                "sha256": sha256(baseline_path),
            },
            "source_closure": source_closure_identity,
            "implicit_math_carriers": carrier_authority,
            "policy": {
                "path": policy_path.relative_to(repo).as_posix(),
                "bytes": policy_path.stat().st_size,
                "sha256": sha256(policy_path),
            },
            "letter_registry": {
                "path": letters_path.relative_to(repo).as_posix(),
                "bytes": letters_path.stat().st_size,
                "sha256": sha256(letters_path),
            },
            "set_registry": {
                "path": sets_path.relative_to(repo).as_posix(),
                "bytes": sets_path.stat().st_size,
                "sha256": sha256(sets_path),
            },
            "generator": {
                "path": Path(__file__).resolve().relative_to(repo).as_posix(),
                "bytes": Path(__file__).stat().st_size,
                "sha256": sha256(Path(__file__)),
            },
        },
        "source_tree_hash_algorithm": "SHA-256(path-length||path-utf8||byte-length||bytes), paths sorted",
        "source_tree_sha256": tree_hash(source_files),
        "presentation_tree_sha256": tree_hash(presented_files),
        "summary": {
            "units": 722,
            "formula_segments": totals["formula_segments"],
            "implicit_carrier_segments": totals["implicit_carrier_segments"],
            "ascii_candidate_scalars": totals["ascii_candidate_scalars"],
            "text_digit_candidate_scalars": totals["text_digit_candidate_scalars"],
            "greek_candidate_commands": totals["greek_candidate_commands"],
            "occurrence_records": totals["occurrence_records"],
            "replacement_records": totals["replacement_records"],
            "untreated_candidates": 0,
            "source_files_with_failed_inverse": 0,
            "dispositions": {
                name: {
                    "records": disposition_records[name],
                    "candidates": disposition_candidates[name],
                }
                for name in sorted(disposition_records)
            },
        },
        "units": unit_payloads,
        "limitations": [
            "The conservative TeX lexer does not expand arbitrary macros or execute conditional branches.",
            "Multi-letter Latin identifiers and unregistered Greek commands remain explicit international exemptions rather than guessed products or substitutions.",
            "Static source coverage and inverse reconstruction do not replace the mutex-guarded runtime, PDF-font, extraction, link, and visual gates.",
        ],
    }
    contract_raw = contract_text(payload).encode("utf-8")
    payload["presentation_contract"] = {
        "path": DEFAULT_CONTRACT.as_posix(),
        "bytes": len(contract_raw),
        "sha256": sha256_bytes(contract_raw),
    }
    decisions_raw = (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    summary_raw = markdown_summary(payload).encode("utf-8")
    return payload, presented_files, contract_raw, decisions_raw + b"\0" + summary_raw


def split_decisions_and_summary(combined: bytes) -> tuple[bytes, bytes]:
    decisions, separator, summary = combined.partition(b"\0")
    require(separator == b"\0", "internal decisions/summary separator missing")
    return decisions, summary


def compact_receipt(
    payload: dict[str, Any], decisions_raw: bytes, summary_raw: bytes,
    contract_raw: bytes,
) -> dict[str, Any]:
    """Bind the complete audit ledger without duplicating its occurrences."""
    units = []
    for unit in payload["units"]:
        units.append({
            key: unit[key]
            for key in (
                "id", "source", "presentation", "formula_segments",
                "ascii_candidate_scalars", "greek_candidate_commands",
                "text_digit_candidate_scalars",
                "occurrence_records", "replacement_records",
                "untreated_candidates", "inverse_reconstruction",
            )
        })
    return {
        "schema": RECEIPT_SCHEMA,
        "status": payload["status"],
        "release_eligible": payload["release_eligible"],
        "mode": payload["mode"],
        "presentation_locale": payload["presentation_locale"],
        "authority": payload["authority"],
        "decision_ledger": {
            "path": DEFAULT_DECISIONS.as_posix(),
            "bytes": len(decisions_raw),
            "sha256": sha256_bytes(decisions_raw),
            "schema": SCHEMA,
        },
        "summary_document": {
            "path": DEFAULT_SUMMARY.as_posix(),
            "bytes": len(summary_raw),
            "sha256": sha256_bytes(summary_raw),
        },
        "presentation_contract": {
            "path": DEFAULT_CONTRACT.as_posix(),
            "bytes": len(contract_raw),
            "sha256": sha256_bytes(contract_raw),
        },
        "source_tree_hash_algorithm": payload["source_tree_hash_algorithm"],
        "source_tree_sha256": payload["source_tree_sha256"],
        "presentation_tree_sha256": payload["presentation_tree_sha256"],
        "summary": payload["summary"],
        "units": units,
    }


def expected_output_paths(repo: Path, presented_files: dict[str, bytes]) -> set[Path]:
    return {(repo / relative).resolve() for relative in presented_files}


def write_or_verify(
    *, action: str, repo: Path, presented_files: dict[str, bytes],
    contract_path: Path, contract_raw: bytes, decisions_path: Path,
    decisions_raw: bytes, summary_path: Path, summary_raw: bytes,
    receipt_path: Path, receipt_raw: bytes,
) -> None:
    expected = expected_output_paths(repo, presented_files)
    presentation_root = (repo / DEFAULT_PRESENTATION_ROOT).resolve()
    if presentation_root.exists():
        actual = {path.resolve() for path in presentation_root.rglob("*.tex")}
        extras = actual - expected
        require(not extras,
                "presentation tree contains untracked TeX files: " +
                ", ".join(str(path) for path in sorted(extras)[:8]))
    if action == "write":
        for relative, raw in sorted(presented_files.items()):
            atomic_write(repo / relative, raw)
        atomic_write(contract_path, contract_raw)
        atomic_write(decisions_path, decisions_raw)
        atomic_write(summary_path, summary_raw)
        atomic_write(receipt_path, receipt_raw)
        return
    require(action == "verify", "invalid action")
    for relative, raw in sorted(presented_files.items()):
        path = repo / relative
        require(path.is_file(), f"missing presentation file: {relative}")
        require(path.read_bytes() == raw, f"presentation file drift: {relative}")
    for path, raw, label in (
        (contract_path, contract_raw, "presentation contract"),
        (decisions_path, decisions_raw, "decisions"),
        (summary_path, summary_raw, "summary"),
        (receipt_path, receipt_raw, "receipt"),
    ):
        require(path.is_file(), f"missing {label}: {path}")
        require(path.read_bytes() == raw, f"{label} drift: {path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--mode", choices=("working", "final"), required=True)
    parser.add_argument("--action", choices=("write", "verify", "audit"), required=True)
    parser.add_argument("--source-closure", type=Path)
    args = parser.parse_args()
    try:
        repo = args.repo.resolve()
        require(repo.is_dir(), "repository path is not a directory")
        policy = repo / DEFAULT_POLICY
        baseline = repo / DEFAULT_BASELINE
        letters = repo / DEFAULT_LETTERS
        sets = repo / DEFAULT_SETS
        payload, presented, contract_raw, combined = build_payload(
            repo, policy, baseline, letters, sets,
            mode=args.mode,
            source_closure=args.source_closure.resolve() if args.source_closure else None,
        )
        decisions_raw, summary_raw = split_decisions_and_summary(combined)
        receipt_raw = (
            json.dumps(
                compact_receipt(payload, decisions_raw, summary_raw, contract_raw),
                ensure_ascii=False, indent=2, sort_keys=True,
            ) + "\n"
        ).encode("utf-8")
        if args.action != "audit":
            write_or_verify(
                action=args.action,
                repo=repo,
                presented_files=presented,
                contract_path=repo / DEFAULT_CONTRACT,
                contract_raw=contract_raw,
                decisions_path=repo / DEFAULT_DECISIONS,
                decisions_raw=decisions_raw,
                summary_path=repo / DEFAULT_SUMMARY,
                summary_raw=summary_raw,
                receipt_path=repo / DEFAULT_RECEIPT,
                receipt_raw=receipt_raw,
            )
        print(json.dumps({
            "status": payload["status"],
            "action": args.action,
            "units": payload["summary"]["units"],
            "formula_segments": payload["summary"]["formula_segments"],
            "ascii_candidate_scalars": payload["summary"]["ascii_candidate_scalars"],
            "text_digit_candidate_scalars": payload["summary"]["text_digit_candidate_scalars"],
            "greek_candidate_commands": payload["summary"]["greek_candidate_commands"],
            "replacement_records": payload["summary"]["replacement_records"],
            "untreated_candidates": payload["summary"]["untreated_candidates"],
            "dispositions": payload["summary"]["dispositions"],
            "source_tree_sha256": payload["source_tree_sha256"],
            "presentation_tree_sha256": payload["presentation_tree_sha256"],
        }, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
