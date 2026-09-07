#!/usr/bin/env python3
"""Generate and verify the frozen-baseline reconciliation for all 722 units.

The default mode is read-only.  ``--write`` is reserved for the announced
source-freeze window: all MSA/Classical inputs are hashed before and after the
complete in-memory derivation, and no output is replaced unless those snapshots
are identical and the full static validator closes exactly.

This tool never rewrites ``evidence/classical/BASELINE.json``.  It derives:

* the exact live-MSA correction overlay;
* formula-local Arabic prose declarations;
* structural-driver declarations;
* exact formal-repair declarations;
* exact reviews for otherwise unchanged Classical prose;
* a full static-validation report;
* a 722-row source-closure manifest; and
* a hash-bound audit receipt.

Metadata supplies human audit rationales and authority references only.  Hashes,
byte counts, failed-check sets and comparison fingerprints are always recomputed
from current repository bytes.  Missing metadata, unused formula-local waivers,
syntax failures, undeclared formal differences, or any concurrent source change
fail closed.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
from typing import Any


EXPECTED_BASELINE_SHA256 = "c10a6321b79a210febba49b3fc216a7fb22b729a738af71d57dc1aea9e105beb"
METADATA_SCHEMA = "openlogic-classical-source-reconciliation-metadata-v1"
METADATA_FIELDS = frozenset((
    "schema", "release_id", "baseline_sha256", "correction_metadata_seed",
    "formal_repair_metadata_seed", "correction_metadata",
    "formal_repair_metadata", "math_text_metadata",
    "structural_review_metadata", "semantic_review_sources",
    "acceptance_audit",
))
CORRECTION_META_FIELDS = frozenset((
    "id", "finding_ids", "rationale", "authority_refs",
))
FORMAL_META_FIELDS = frozenset(("id", "authority_refs", "rationale"))
MATH_META_FIELDS = frozenset(("id", "items", "authority_refs"))
MATH_ITEM_FIELDS = frozenset(("index", "command", "note"))
STRUCTURAL_META_FIELDS = frozenset((
    "id", "kind", "note", "authority_refs",
))
FILE_ID_FIELDS = frozenset(("path", "sha256", "bytes"))
ACCEPTANCE_SCHEMA = "openlogic-full-translation-acceptance-audit-v2"
ACCEPTANCE_FIELDS = frozenset((
    "schema", "release_id", "created_utc", "overall_status",
    "acceptance_rule", "summary", "historical_audit", "input_artifacts",
    "preflight", "source_snapshot", "range_results",
    "resolved_historical_findings", "owner_followup_findings",
    "blocking_findings", "nonblocking_expert_review_questions", "markdown",
))
ACCEPTANCE_SUMMARY_FIELDS = frozenset((
    "unit_count", "live_source_bindings", "range_count",
    "historical_blocker_count", "resolved_historical_blocker_count",
    "owner_followup_finding_count", "blocking_finding_count",
))
ACCEPTANCE_RANGE_FIELDS = frozenset((
    "range", "unit_start", "unit_end", "unit_count", "source_acceptance",
    "semantic_review_paths", "repair_evidence_paths", "continuation_finding_ids",
))
ACCEPTANCE_EXPECTED_RANGES = (
    ("0001-0100", 1, 100), ("0101-0200", 101, 200),
    ("0201-0300", 201, 300), ("0301-0400", 301, 400),
    ("0401-0500", 401, 500), ("0501-0600", 501, 600),
    ("0601-0700", 601, 700), ("0701-0722", 701, 722),
)
ACCEPTANCE_RESOLVED_IDS = frozenset((
    "FTA-COVERAGE-0044-0050", "FTA-078-I1", "FTA-0118-I1",
    "FTA-0488-0490-M1", "FTA-0588-N1", "FTA-0643-WEAKGEN",
    "FTA-0713-M1", "FTA-OWNER-INTEGRATION-0101-0700",
))
ACCEPTANCE_OWNER_FOLLOWUP_IDS = frozenset((
    "C184-01", "C185-01", "0452-I2", "0452-I3",
))
ACCEPTANCE_RANGE_ARTIFACTS = (
    "evidence/classical/repairs/OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907.json",
    "evidence/classical/repairs/OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907.md",
    "evidence/classical/repairs/OLP0394_0399_0400_0404_0409_MODAL_SCOPE_20260907.json",
    "evidence/classical/repairs/OLP0394_0399_0400_0404_0409_MODAL_SCOPE_20260907.md",
    "evidence/classical/repairs/OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907.json",
    "evidence/classical/repairs/OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907.md",
    "evidence/classical/repairs/OLP0021_TWO_ROOTS_NOTE_20260907.json",
    "evidence/classical/repairs/OLP0021_TWO_ROOTS_NOTE_20260907.md",
    "evidence/classical/repairs/OLP0321_0326_0368_SEMANTIC_SCOPE_20260907.json",
    "evidence/classical/repairs/OLP0321_0326_0368_SEMANTIC_SCOPE_20260907.md",
    "evidence/classical/repairs/OLP0375_0376_ARITHMETIC_SCOPE_20260907.json",
    "evidence/classical/repairs/OLP0375_0376_ARITHMETIC_SCOPE_20260907.md",
    "evidence/classical/repairs/OLP0051_0060_0068_SCOPE_PROPAGATION_20260906.json",
    "evidence/classical/repairs/OLP0051_0060_0068_SCOPE_PROPAGATION_20260906.md",
    "evidence/classical/repairs/OLP0067_DUAL_GRAMMAR_20260906.json",
    "evidence/classical/repairs/OLP0067_DUAL_GRAMMAR_20260906.md",
    "evidence/classical/batches/0051-0100.corrections-OLP0067-20260906.json",
    "evidence/classical/repairs/OLP0008_CLASSICAL_PROSE_20260906.json",
    "evidence/classical/repairs/OLP0008_CLASSICAL_PROSE_20260906.md",
    "evidence/classical/repairs/OLP0033_0039_0072_0081_QUALIFICATION_PROPAGATION_20260906.json",
    "evidence/classical/repairs/OLP0033_0039_0072_0081_QUALIFICATION_PROPAGATION_20260906.md",
    "evidence/classical/SOURCE_PROPAGATION_PRE_QUALIFICATIONS_20260906.json",
    "evidence/classical/repairs/OLP0005_0008_0016_0018_QUALIFICATION_PROPAGATION_20260906.json",
    "evidence/classical/repairs/OLP0005_0008_0016_0018_QUALIFICATION_PROPAGATION_20260906.md",
    "evidence/classical/repairs/OLP0497_MP_PROPAGATION_20260906.json",
    "evidence/classical/repairs/OLP0497_MP_PROPAGATION_20260906.md",
    "evidence/classical/repairs/OLP0079_0093_MP_PROPAGATION_20260906.json",
    "evidence/classical/repairs/OLP0079_0093_MP_PROPAGATION_20260906.md",
    "evidence/classical/repairs/0001-0100.json",
    "evidence/classical/repairs/0001-0100.md",
    "evidence/classical/repairs/0101-0200.json",
    "evidence/classical/repairs/0101-0200.md",
    "evidence/classical/repairs/0201-0300.json",
    "evidence/classical/repairs/0201-0300.md",
    "evidence/classical/repairs/0301-0400.json",
    "evidence/classical/repairs/0301-0400.md",
    "evidence/classical/repairs/0401-0500.json",
    "evidence/classical/repairs/0401-0500.md",
    "evidence/classical/repairs/0501-0600.json",
    "evidence/classical/repairs/0501-0600.md",
    "evidence/classical/repairs/0601-0700.json",
    "evidence/classical/repairs/0601-0700.md",
    "evidence/classical/reviews/0701-0722.json",
    "evidence/classical/reviews/0701-0722.md",
)
ACCEPTANCE_OWNER_ARTIFACTS = (
    "evidence/classical/repairs/OWNER_FOLLOWUP_REPAIRS_20260905.json",
    "evidence/classical/repairs/OWNER_FOLLOWUP_REPAIRS_20260905.md",
)

OUTPUTS = {
    "baseline_corrections": "evidence/classical/BASELINE_CORRECTION_OVERLAY_FULL_20260905.json",
    "math_text_declarations": "evidence/classical/MATH_TEXT_DECLARATIONS_FULL_20260905.json",
    "structural_reviews": "evidence/classical/STRUCTURAL_REVIEW_DECLARATIONS_FULL_20260905.json",
    "formal_repairs": "evidence/classical/FORMAL_REPAIR_DECLARATIONS_FULL_20260905.json",
    "general_reviews": "evidence/classical/GENERAL_REVIEW_DECLARATIONS_FULL_20260905.json",
    "static_validation": "evidence/classical/SOURCE_RECONCILIATION_STATIC_VALIDATION_20260905.json",
    "closure_manifest": "evidence/classical/SOURCE_RECONCILIATION_CLOSURE_MANIFEST_20260905.json",
    "audit_receipt": "evidence/classical/SOURCE_RECONCILIATION_AUDIT_20260905.json",
}
TRANSACTION_MARKER = "evidence/classical/.SOURCE_RECONCILIATION_WRITE_IN_PROGRESS"

# Chronological order matters: the adjective opening succeeds, rather than
# replaces, the six-function phase. These are finite, independently checked
# ledger identities, not a generic permission to admit new source differences.
SOURCE_REPAIR_BATCH_20260907 = (
    ("OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907",
     "eb0e436d546c867a56d66767a24f66a2d687ea254ed83c9123aa0c2106a8e0c7",
     137782, 3, 7, 6, 12),
    ("OLP0394_0399_0400_0404_0409_MODAL_SCOPE_20260907",
     "6d29d66c0db082e2c348cf8a30219e9d6ae11b80e14d0ecfdd2cbc2c79a6f4cd",
     98459, 10, 15, 6, 15),
    ("OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907",
     "90364663431ea9dad27fef1a427acf033498f1cd95f8cbea29cc665f41186c79",
     64402, 3, 4, 4, 10),
)
FROZEN_ENGLISH_ROOT = Path(
    "C:/interlanguage-production/openlogic-interfarsi/repo/source/upstream")


class ReconciliationError(ValueError):
    """An input or closure condition failed."""


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return sha256(raw)


def json_loads_unique(raw: str, label: str) -> Any:
    def unique_fields(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ReconciliationError(f"duplicate JSON field in {label}: {key}")
            value[key] = item
        return value

    return json.loads(raw, object_pairs_hook=unique_fields)


def load_unique_json(path: Path, label: str) -> tuple[dict, bytes]:

    raw = path.read_bytes()
    data = json_loads_unique(raw.decode("utf-8-sig"), label)
    if not isinstance(data, dict):
        raise ReconciliationError(f"{label} must be a JSON object")
    return data, raw


def safe_repo_path(repo: Path, value: str, *, suffix: str | None = None) -> Path:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ReconciliationError(f"invalid repository-relative path: {value!r}")
    rel = PurePosixPath(value)
    if rel.is_absolute() or ".." in rel.parts or rel.as_posix() != value:
        raise ReconciliationError(f"invalid repository-relative path: {value!r}")
    path = (repo / Path(*rel.parts)).resolve()
    if not path.is_relative_to(repo.resolve()):
        raise ReconciliationError(f"out-of-scope repository path: {value!r}")
    if suffix is not None and path.suffix != suffix:
        raise ReconciliationError(f"unexpected suffix for {value!r}")
    return path


def repo_relative(repo: Path, path: Path) -> str:
    resolved = path.resolve()
    if not resolved.is_relative_to(repo.resolve()):
        raise ReconciliationError(f"path outside repository: {path}")
    return resolved.relative_to(repo.resolve()).as_posix()


def file_identity(repo: Path, path: Path, raw: bytes | None = None) -> dict:
    raw = path.read_bytes() if raw is None else raw
    return {"path": repo_relative(repo, path), "sha256": sha256(raw), "bytes": len(raw)}


def load_checker(repo: Path):
    path = repo / "build/validate_classical_overlay.py"
    spec = importlib.util.spec_from_file_location("classical_reconciliation_checker", path)
    if spec is None or spec.loader is None:
        raise ReconciliationError("cannot load classical overlay validator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def strict_meta_list(value: Any, fields: frozenset[str], label: str) -> list[dict]:
    if not isinstance(value, list):
        raise ReconciliationError(f"{label} must be a list")
    seen: set[str] = set()
    result = []
    for item in value:
        if not isinstance(item, dict) or set(item) != fields:
            raise ReconciliationError(f"{label} entry requires exactly {sorted(fields)}")
        uid = item.get("id")
        if not isinstance(uid, str) or not re.fullmatch(r"OLP-\d{4}", uid) or uid in seen:
            raise ReconciliationError(f"duplicate/invalid {label} identity")
        seen.add(uid)
        refs = item.get("authority_refs")
        if (not isinstance(refs, list) or not refs or len(refs) != len(set(refs)) or
                any(not isinstance(ref, str) or not ref.strip() for ref in refs)):
            raise ReconciliationError(f"{label} {uid} requires unique authority references")
        result.append(item)
    return result


def load_metadata(repo: Path, path: Path) -> tuple[dict, bytes]:
    data, raw = load_unique_json(path, "source-reconciliation metadata")
    if set(data) != METADATA_FIELDS or data.get("schema") != METADATA_SCHEMA:
        raise ReconciliationError("unsupported source-reconciliation metadata schema/fields")
    if data.get("baseline_sha256") != EXPECTED_BASELINE_SHA256:
        raise ReconciliationError("metadata binds a different frozen baseline")
    if not isinstance(data.get("release_id"), str) or not data["release_id"].strip():
        raise ReconciliationError("metadata requires a release identity")
    for key in ("correction_metadata_seed", "formal_repair_metadata_seed",
                "acceptance_audit"):
        safe_repo_path(repo, data[key], suffix=".json")
    sources = data.get("semantic_review_sources")
    if (not isinstance(sources, list) or not sources or len(sources) != len(set(sources)) or
            any(not isinstance(value, str) for value in sources)):
        raise ReconciliationError("semantic review sources must be unique paths")
    for value in sources:
        safe_repo_path(repo, value, suffix=".json")
    data["correction_metadata"] = strict_meta_list(
        data["correction_metadata"], CORRECTION_META_FIELDS, "correction metadata")
    data["formal_repair_metadata"] = strict_meta_list(
        data["formal_repair_metadata"], FORMAL_META_FIELDS, "formal metadata")
    data["math_text_metadata"] = strict_meta_list(
        data["math_text_metadata"], MATH_META_FIELDS, "math-text metadata")
    data["structural_review_metadata"] = strict_meta_list(
        data["structural_review_metadata"], STRUCTURAL_META_FIELDS, "structural metadata")
    for record in data["correction_metadata"]:
        findings = record["finding_ids"]
        if (not isinstance(findings, list) or not findings or len(findings) != len(set(findings)) or
                any(not isinstance(value, str) for value in findings)):
            raise ReconciliationError(f"invalid finding IDs for {record['id']}")
        if not isinstance(record["rationale"], str) or not record["rationale"].strip():
            raise ReconciliationError(f"empty correction rationale for {record['id']}")
    for key in ("formal_repair_metadata",):
        for record in data[key]:
            if not isinstance(record["rationale"], str) or not record["rationale"].strip():
                raise ReconciliationError(f"empty formal rationale for {record['id']}")
    for record in data["math_text_metadata"]:
        items = record["items"]
        if not isinstance(items, list) or not items:
            raise ReconciliationError(f"math-text metadata {record['id']} has no items")
        indices = set()
        for item in items:
            if not isinstance(item, dict) or set(item) != MATH_ITEM_FIELDS:
                raise ReconciliationError("invalid math-text metadata item fields")
            if (type(item["index"]) is not int or item["index"] < 0 or
                    item["index"] in indices or not isinstance(item["command"], str) or
                    not item["command"].startswith("\\") or
                    not isinstance(item["note"], str) or not item["note"].strip()):
                raise ReconciliationError(f"invalid math-text item for {record['id']}")
            indices.add(item["index"])
    for record in data["structural_review_metadata"]:
        if (record["kind"] != "heading-import-driver" or
                not isinstance(record["note"], str) or not record["note"].strip()):
            raise ReconciliationError(f"invalid structural metadata for {record['id']}")
    return data, raw


def source_snapshot(repo: Path, baseline: dict) -> tuple[list[dict], str]:
    rows = []
    for unit in baseline["units"]:
        source_path = safe_repo_path(repo, unit["arabic_path"], suffix=".tex")
        target_path = safe_repo_path(repo, unit["target_path"], suffix=".tex")
        if not source_path.is_file() or not target_path.is_file():
            raise ReconciliationError(f"missing source/target for {unit['id']}")
        source, target = source_path.read_bytes(), target_path.read_bytes()
        rows.append({
            "id": unit["id"],
            "msa_sha256": sha256(source), "msa_bytes": len(source),
            "classical_sha256": sha256(target), "classical_bytes": len(target),
        })
    return rows, canonical_sha256(rows)


def validate_source_repair_batch_20260907(repo: Path, checker, baseline: dict) -> dict:
    """Admit only the exact 16-decision batch, replaying all historical stages.

    This reads just the ledgers and their named source inputs. It writes nothing,
    runs no builds, and makes no full-edition semantic-acceptance claim. Earlier
    OLFUN/OLSIZ passages survive because every complete predecessor byte stream
    is recovered, not because a changed hash is treated as an acceptable alias.
    """
    by_id = {unit["id"]: unit for unit in baseline["units"]}
    ledgers, live, phases = [], {}, {}
    identities = []

    def check_identity(raw, row, phase):
        if (len(raw), sha256(raw)) != (row[phase + "_bytes"], row[phase + "_sha256"]):
            raise ReconciliationError(f"source repair {phase} identity drifted: {row['path']}")

    def source_path(row):
        edition, value = row["edition"], row["path"]
        if edition == "shared":
            if value != "source/locale/ar/open-logic-config.sty":
                raise ReconciliationError("unrecognized shared source-repair input")
            return safe_repo_path(repo, value)
        # The first ledger inventories paths without repeating unit_id. Resolve
        # those through the immutable baseline; do not rewrite its history.
        unit = by_id.get(row.get("unit_id"))
        if unit is None and "unit_id" not in row:
            candidates = [u for u in by_id.values() if value in (
                u["arabic_path"], u["target_path"],
                (FROZEN_ENGLISH_ROOT / u["source_path"]).as_posix())]
            unit = candidates[0] if len(candidates) == 1 else None
        if unit is None:
            raise ReconciliationError("source repair unit is not in frozen baseline")
        if edition == "english":
            expected = (FROZEN_ENGLISH_ROOT / unit["source_path"]).resolve()
            if Path(value).resolve() != expected:
                raise ReconciliationError("source repair English path is not frozen input")
            if row["after_sha256"] != unit["english_sha256"]:
                raise ReconciliationError("source repair English identity differs from baseline")
            return expected
        key = {"msa": "arabic_path", "classical": "target_path"}.get(edition)
        if key is None or value != unit[key]:
            raise ReconciliationError("source repair edition/path ownership differs")
        return safe_repo_path(repo, value, suffix=".tex")

    for name, digest, size, tx_count, patch_count, decision_count, inventory_count in SOURCE_REPAIR_BATCH_20260907:
        path = repo / "evidence/classical/repairs" / (name + ".json")
        ledger, raw = load_unique_json(path, "consolidated source repair ledger")
        if (sha256(raw), len(raw)) != (digest, size):
            raise ReconciliationError(f"consolidated source repair ledger identity drifted: {name}")
        transactions, inventory = ledger["transactions"], ledger["primary_source_inventory"]
        if (len(transactions), sum(len(t["patches"]) for t in transactions),
                len(ledger["decisions"]), len(inventory)) != (
                    tx_count, patch_count, decision_count, inventory_count):
            raise ReconciliationError("source repair batch scope differs")
        if len({t["path"] for t in transactions}) != tx_count:
            raise ReconciliationError("duplicate source repair transaction")
        for row in inventory:
            path_value = row["path"]
            resolved = source_path(row)
            if path_value not in live:
                live[path_value] = resolved.read_bytes()
                phases[path_value] = live[path_value]
        for tx in transactions:
            source_path(tx)
            if (tx["edition"] not in {"msa", "classical"} or
                    not any(all(row.get(k) == tx.get(k) for k in (
                        "path", "edition", "before_sha256", "before_bytes",
                        "after_sha256", "after_bytes")) for row in inventory)):
                raise ReconciliationError("source repair transaction lacks exact inventory binding")
        ledgers.append(ledger)
        identities.append(file_identity(repo, path, raw))

    transitions = []
    # Undo successor ledgers first. Thus 0022's recorded 8a73... phase must be
    # recovered from current 3a74... before the earlier seven-patch replay.
    for ledger in reversed(ledgers):
        for row in ledger["primary_source_inventory"]:
            check_identity(phases[row["path"]], row, "after")
        for tx in ledger["transactions"]:
            after = phases[tx["path"]]
            before = after
            for patch in reversed(tx["patches"]):
                a, b = patch["after"].encode("utf-8"), patch["before"].encode("utf-8")
                if patch["occurrences"] != 1 or before.count(a) != 1:
                    raise ReconciliationError("source repair inverse is not one exact occurrence")
                before = before.replace(a, b, 1)
            check_identity(before, tx, "before")
            replay = before
            for patch in tx["patches"]:
                a, b = patch["before"].encode("utf-8"), patch["after"].encode("utf-8")
                if replay.count(a) != 1:
                    raise ReconciliationError("source repair forward is not one exact occurrence")
                replay = replay.replace(a, b, 1)
            if replay != after:
                raise ReconciliationError("source repair forward replay differs")
            normalized = after.decode("utf-8")
            if tx["unit_id"] in {"OLP-0394", "OLP-0399"}:
                # Only these two mathematically proved changes alter formulas.
                # Ledger SHA pins the exact RHS or grid clause, not a whole-unit
                # formal-difference waiver. All surrounding formulas are checked.
                patch = tx["patches"][0]
                if len(tx["patches"]) != 1:
                    raise ReconciliationError("formal source repair is not one exact patch")
                if tx["unit_id"] == "OLP-0394":
                    if patch["after"].splitlines()[-1] != patch["before"].replace(
                            r"= \Undef$", r"= \False$"):
                        raise ReconciliationError("modal final RHS correction differs")
                elif patch["after"] != r"النظر أيضًا، لكل عدد طبيعي~$m\ge2$، في المجموعات الجزئية}":
                    raise ReconciliationError("finite-grid domain correction differs")
                normalized = normalized.replace(patch["after"], patch["before"], 1)
            result = checker.compare(before.decode("utf-8"), normalized)
            if result["failures"] or not all(result["checks"].values()):
                raise ReconciliationError(f"source repair has undeclared formal drift: {tx['path']}")
            phases[tx["path"]] = before
            transitions.append({k: tx[k] for k in (
                "unit_id", "edition", "path", "before_sha256", "before_bytes",
                "after_sha256", "after_bytes")})
        for row in ledger["primary_source_inventory"]:
            check_identity(phases[row["path"]], row, "before")

    return {
        "schema": "openlogic-consolidated-source-repair-admission-v1", "status": "PASS",
        "ledger_identities": identities,
        "decision_count": 16, "transaction_count": len(transitions),
        "patch_count": 26, "changed_file_count": len({t["path"] for t in transitions}),
        "historical_transitions_in_inverse_order": transitions,
        "live_input_identities": [{"path": value, "bytes": len(raw), "sha256": sha256(raw)}
                                  for value, raw in sorted(live.items())],
        "formula_changes": [
            {"unit_id": "OLP-0394", "editions": ["msa", "classical"],
             "change": "one final RHS Undef to False, derived from the unchanged truth tables"},
            {"unit_id": "OLP-0399", "editions": ["msa", "classical"],
             "change": "one natural m>=2 grid-domain clause; earlier m>0 and n<m preserved"},
        ],
        "scope": "Exact source-batch admission only; not full-edition semantic, PDF, or publication acceptance.",
    }


def metadata_maps(repo: Path, metadata: dict) -> tuple[dict, dict, dict, dict]:
    seed_corrections, _ = load_unique_json(
        safe_repo_path(repo, metadata["correction_metadata_seed"]), "correction metadata seed")
    if seed_corrections.get("schema") not in (
            "openlogic-classical-baseline-corrections-v1",
            "openlogic-classical-baseline-corrections-v2"):
        raise ReconciliationError("unsupported correction metadata seed")
    if seed_corrections.get("baseline_sha256", "").lower() != EXPECTED_BASELINE_SHA256:
        raise ReconciliationError("correction metadata seed binds a different frozen baseline")
    corrections = {}
    seed_units = seed_corrections.get("units")
    if not isinstance(seed_units, list):
        raise ReconciliationError("correction metadata seed lacks a unit list")
    for index, item in enumerate(seed_units):
        if not isinstance(item, dict) or item.get("id") in corrections:
            raise ReconciliationError("duplicate/invalid correction metadata seed identity")
        corrections[item["id"]] = {
            "finding_ids": item["finding_ids"], "rationale": item["rationale"],
            "authority_refs": [
                f"{metadata['correction_metadata_seed']}#/units/{index}"
            ],
            "metadata_source": metadata["correction_metadata_seed"],
            "seed_current_msa_sha256": item["current_msa_sha256"].lower(),
            "seed_current_msa_bytes": item["current_msa_bytes"],
        }
    for item in metadata["correction_metadata"]:
        corrections[item["id"]] = {
            "finding_ids": item["finding_ids"], "rationale": item["rationale"],
            "authority_refs": item["authority_refs"], "metadata_source": "explicit",
            "seed_current_msa_sha256": None, "seed_current_msa_bytes": None,
        }

    seed_formal, _ = load_unique_json(
        safe_repo_path(repo, metadata["formal_repair_metadata_seed"]), "formal metadata seed")
    if seed_formal.get("schema") != "openlogic-classical-formal-repairs-v1":
        raise ReconciliationError("unsupported formal metadata seed")
    if seed_formal.get("baseline_sha256", "").lower() != EXPECTED_BASELINE_SHA256:
        raise ReconciliationError("formal metadata seed binds a different frozen baseline")
    formal = {}
    for item in seed_formal.get("units", []):
        if not isinstance(item, dict) or item.get("id") in formal:
            raise ReconciliationError("duplicate/invalid formal metadata seed identity")
        formal[item["id"]] = {
            "authority_refs": item["authority_refs"], "rationale": item["rationale"],
            "metadata_source": metadata["formal_repair_metadata_seed"],
            "seed_accepted_failed_checks": sorted(item["accepted_failed_checks"]),
            "seed_comparison_sha256": item["comparison_sha256"].lower(),
        }
    for item in metadata["formal_repair_metadata"]:
        formal[item["id"]] = {
            "authority_refs": item["authority_refs"], "rationale": item["rationale"],
            "metadata_source": "explicit",
            "seed_accepted_failed_checks": None,
            "seed_comparison_sha256": None,
        }
    math = {item["id"]: item for item in metadata["math_text_metadata"]}
    structural = {item["id"]: item for item in metadata["structural_review_metadata"]}
    return corrections, formal, math, structural


def build_corrections(repo: Path, checker, baseline: dict, baseline_hash: str,
                      metadata: dict, correction_meta: dict) -> tuple[dict, dict]:
    records, authority = [], {}
    missing = []
    for unit in baseline["units"]:
        source = safe_repo_path(repo, unit["arabic_path"]).read_bytes()
        target = safe_repo_path(repo, unit["target_path"]).read_bytes()
        source_hash = sha256(source)
        if source_hash == unit["arabic_sha256"].lower() and len(source) == unit["arabic_bytes"]:
            continue
        meta = correction_meta.get(unit["id"])
        if (meta is None or
                (meta["metadata_source"] != "explicit" and
                 (meta["seed_current_msa_sha256"] != source_hash or
                  meta["seed_current_msa_bytes"] != len(source)))):
            missing.append(unit["id"])
            continue
        record = {
            "id": unit["id"], "arabic_path": unit["arabic_path"],
            "target_path": unit["target_path"],
            "old_msa_sha256": unit["arabic_sha256"].lower(),
            "old_msa_bytes": unit["arabic_bytes"],
            "current_msa_sha256": source_hash, "current_msa_bytes": len(source),
            "current_classical_target_sha256": sha256(target),
            "current_classical_target_bytes": len(target),
            "finding_ids": meta["finding_ids"], "rationale": meta["rationale"],
        }
        records.append(record)
        authority[unit["id"]] = {
            "authority_refs": meta["authority_refs"],
            "metadata_source": meta["metadata_source"],
        }
    if missing:
        raise ReconciliationError("live MSA deltas lack exact correction metadata: " + ", ".join(missing))
    output = {
        "schema": "openlogic-classical-baseline-corrections-v2",
        "baseline_sha256": baseline_hash,
        "units": records,
    }
    checker.baseline_correction_records(output, baseline, baseline_hash, repo)
    return output, authority


def build_math_declarations(repo: Path, checker, baseline: dict,
                            math_meta: dict) -> tuple[dict, dict]:
    by_id = {unit["id"]: unit for unit in baseline["units"]}
    discovered: dict[str, list[int]] = {}
    analyses = {}
    for unit in baseline["units"]:
        source_text = safe_repo_path(repo, unit["arabic_path"]).read_text(encoding="utf-8")
        target_text = safe_repo_path(repo, unit["target_path"]).read_text(encoding="utf-8")
        left, right = checker.analyze(source_text), checker.analyze(target_text)
        analyses[unit["id"]] = (left, right)
        if len(left.math_text) != len(right.math_text):
            continue
        indices = []
        for index, ((left_command, left_tokens),
                    (right_command, right_tokens)) in enumerate(zip(left.math_text, right.math_text)):
            if (left_command == right_command and
                    checker.canonical(left_tokens, True) != checker.canonical(right_tokens, True) and
                    checker.formal_text_projection(left_tokens) ==
                    checker.formal_text_projection(right_tokens)):
                indices.append(index)
        if indices:
            discovered[unit["id"]] = indices
    declared = {uid: sorted(item["index"] for item in meta["items"])
                for uid, meta in math_meta.items()}
    if discovered != declared:
        raise ReconciliationError(
            "formula-local Arabic prose declarations are not exact; discovered=" +
            json.dumps(discovered, sort_keys=True) + "; declared=" +
            json.dumps(declared, sort_keys=True))

    units, authority = [], {}
    for uid in sorted(math_meta):
        meta, unit = math_meta[uid], by_id.get(uid)
        if unit is None:
            raise ReconciliationError(f"unknown math-text metadata identity: {uid}")
        left, right = analyses[uid]
        items = []
        for spec in sorted(meta["items"], key=lambda item: item["index"]):
            index = spec["index"]
            left_command, left_tokens = left.math_text[index]
            right_command, right_tokens = right.math_text[index]
            if left_command != right_command or left_command != spec["command"]:
                raise ReconciliationError(f"math-text command drift at {uid} index {index}")
            if checker.formal_text_projection(left_tokens) != checker.formal_text_projection(right_tokens):
                raise ReconciliationError(f"math-text formal projection drift at {uid} index {index}")
            items.append({
                "index": index, "command": left_command,
                "source": checker.raw_body(left, left_tokens),
                "target": checker.raw_body(right, right_tokens),
                "note": spec["note"],
            })
        source = safe_repo_path(repo, unit["arabic_path"]).read_bytes()
        target = safe_repo_path(repo, unit["target_path"]).read_bytes()
        units.append({
            "id": uid, "arabic_sha256": sha256(source),
            "target_sha256": sha256(target), "math_text": items,
        })
        authority[uid] = meta["authority_refs"]
    return {"schema": "openlogic-classical-exceptions-v1", "units": units}, authority


def build_structural_reviews(repo: Path, checker, baseline: dict,
                             structural_meta: dict) -> tuple[dict, dict]:
    by_id = {unit["id"]: unit for unit in baseline["units"]}
    units, authority = [], {}
    for uid in sorted(structural_meta):
        meta, unit = structural_meta[uid], by_id.get(uid)
        if unit is None:
            raise ReconciliationError(f"unknown structural metadata identity: {uid}")
        source = safe_repo_path(repo, unit["arabic_path"]).read_bytes()
        target = safe_repo_path(repo, unit["target_path"]).read_bytes()
        left = checker.structural_driver(source.decode("utf-8"))
        right = checker.structural_driver(target.decode("utf-8"))
        if not left["eligible"] or not right["eligible"] or left["signature"] != right["signature"]:
            raise ReconciliationError(f"structural-driver mismatch for {uid}")
        units.append({
            "id": uid, "arabic_sha256": sha256(source),
            "target_sha256": sha256(target), "kind": meta["kind"],
            "note": meta["note"],
        })
        authority[uid] = meta["authority_refs"]
    return {"schema": checker.STRUCTURAL_SCHEMA, "units": units}, authority


def failed_checks(result: dict) -> list[str]:
    return sorted(name for name, passed in result.get("checks", {}).items()
                  if not passed and name in {
                      "environment_sequence",
                      "protected_reference_citation_and_macro_keys",
                      "protected_program_and_literal_blocks",
                      "ordered_proof_and_induction_commands",
                      "ordered_formula_segments_and_tokens",
                  })


def build_formal_repairs(repo: Path, checker, baseline: dict, baseline_hash: str,
                         corrections: dict, corrections_hash: str,
                         declarations: dict, structural: dict,
                         formal_meta: dict) -> tuple[dict, dict, dict]:
    raw_report = checker.validate(
        repo, baseline, baseline["units"], declarations, structural,
        baseline_corrections=corrections, baseline_sha256=baseline_hash)
    flagged = [unit for unit in raw_report["units"] if unit["status"] == "flagged"]
    missing = [unit["id"] for unit in flagged if unit["id"] not in formal_meta]
    if missing:
        raise ReconciliationError("formal differences lack exact audit metadata: " + ", ".join(missing))
    records, authority = [], {}
    for result in flagged:
        uid = result["id"]
        meta = formal_meta[uid]
        accepted = failed_checks(result)
        if (not accepted or set(accepted) - checker.FORMAL_REPAIR_ALLOWED_CHECKS or
                any(failure.startswith(("source syntax:", "target syntax:",
                                        "invalid math-text declaration:",
                                        "invalid terminology declaration:",
                                        "formula signature error:"))
                    for failure in result.get("failures", []))):
            raise ReconciliationError(f"{uid} has a non-declarable formal failure")
        expected_failures = [name + " differs" for name in accepted]
        observed_failures = result.get("failures")
        if (not isinstance(observed_failures, list) or
                len(observed_failures) != len(expected_failures) or
                len(set(observed_failures)) != len(observed_failures) or
                set(observed_failures) != set(expected_failures)):
            raise ReconciliationError(f"{uid} failure list is not the exact formal-check set")
        comparison_hash = checker.formal_comparison_sha256(result)
        if (meta["metadata_source"] != "explicit" and
                (meta["seed_accepted_failed_checks"] != accepted or
                 meta["seed_comparison_sha256"] != comparison_hash)):
            raise ReconciliationError(
                f"{uid} current formal difference drifted from its metadata seed; "
                "an explicit exact audit rationale is required")
        records.append({
            "id": uid,
            "effective_msa_sha256": result["arabic_sha256"],
            "effective_msa_bytes": result["arabic_bytes"],
            "target_sha256": result["target_sha256"],
            "target_bytes": result["target_bytes"],
            "accepted_failed_checks": accepted,
            "comparison_sha256": comparison_hash,
            "authority_refs": meta["authority_refs"],
            "rationale": meta["rationale"],
        })
        authority[uid] = {"metadata_source": meta["metadata_source"]}
    output = {
        "schema": checker.FORMAL_REPAIRS_SCHEMA,
        "baseline_sha256": baseline_hash,
        "baseline_corrections_sha256": corrections_hash,
        "units": records,
    }
    return output, authority, raw_report


def review_unit_id(record: Any) -> str | None:
    if isinstance(record, dict):
        value = record.get("id")
        return value if isinstance(value, str) else None
    if isinstance(record, list) and record and isinstance(record[0], str):
        return record[0]
    return None


def compact_review_note(record: Any) -> str:
    if isinstance(record, dict):
        for key in ("semantic_review", "coverage_note", "review_notes",
                    "verdict", "review_status", "confidence"):
            value = record.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
            if isinstance(value, (list, dict)) and value:
                return json.dumps(value, ensure_ascii=False, separators=(",", ":"))[:1600]
    if isinstance(record, list):
        scalar = [str(value) for value in record[1:] if isinstance(value, (str, int, float, bool))]
        if scalar:
            return "Unit-level review record: " + "; ".join(scalar[-3:])[:1500]
    return "The cited unit-level review records the bounded semantic comparison."


def semantic_authority(repo: Path, metadata: dict, baseline: dict) -> tuple[dict, list[dict]]:
    rows: dict[str, dict] = {}
    files = []
    for value in metadata["semantic_review_sources"]:
        path = safe_repo_path(repo, value, suffix=".json")
        data, raw = load_unique_json(path, "semantic review source")
        units = data.get("units")
        if not isinstance(units, list):
            raise ReconciliationError(f"semantic review source lacks units: {value}")
        files.append(file_identity(repo, path, raw))
        for index, record in enumerate(units):
            uid = review_unit_id(record)
            if uid is None or not re.fullmatch(r"OLP-\d{4}", uid) or uid in rows:
                raise ReconciliationError(f"duplicate/invalid semantic unit in {value}")
            rows[uid] = {
                "authority_ref": f"{value}#/units/{index}",
                "note": compact_review_note(record),
            }
    expected = {unit["id"] for unit in baseline["units"]}
    if set(rows) != expected:
        missing = sorted(expected - set(rows))
        extra = sorted(set(rows) - expected)
        raise ReconciliationError(
            f"semantic review coverage is not 722-exact; missing={missing}, extra={extra}")
    return rows, files


def acceptance_input_paths(metadata: dict, preflight: dict) -> set[str]:
    """Return the complete, non-self-referential acceptance authority set."""
    return set(ACCEPTANCE_RANGE_ARTIFACTS) | set(ACCEPTANCE_OWNER_ARTIFACTS) | {
        "evidence/classical/BASELINE.json",
        "evidence/classical/terminology/README.md",
        "build/finalize_classical_source_reconciliation.py",
        "build/generate_full_translation_acceptance_audit.py",
        metadata["correction_metadata_seed"],
        metadata["formal_repair_metadata_seed"],
        preflight["metadata"]["path"],
        preflight["validator"]["path"],
        *(item["path"] for item in preflight["semantic_authorities"]),
    }


def _verify_acceptance_file_identity(repo: Path, item: Any, label: str) -> dict:
    if not isinstance(item, dict) or set(item) != FILE_ID_FIELDS:
        raise ReconciliationError(f"invalid {label} file identity")
    value = item.get("path")
    if not isinstance(value, str):
        raise ReconciliationError(f"invalid {label} file path")
    path = safe_repo_path(repo, value)
    raw = path.read_bytes()
    if (type(item.get("bytes")) is not int or item["bytes"] < 0 or
            not isinstance(item.get("sha256"), str) or
            not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) or
            item["bytes"] != len(raw) or item["sha256"] != sha256(raw)):
        raise ReconciliationError(f"{label} identity drifted: {value}")
    return file_identity(repo, path, raw)


def _verify_acceptance_source_snapshot(repo: Path, baseline: dict,
                                       snapshot: Any) -> None:
    fields = frozenset((
        "schema", "status", "english_root", "unit_count",
        "live_source_bindings", "snapshot_sha256", "units",
    ))
    if not isinstance(snapshot, dict) or set(snapshot) != fields:
        raise ReconciliationError("invalid full acceptance source-snapshot fields")
    if (snapshot.get("schema") != "openlogic-full-translation-source-snapshot-v1" or
            snapshot.get("status") != "PASS" or snapshot.get("unit_count") != 722 or
            snapshot.get("live_source_bindings") != 2166):
        raise ReconciliationError("full acceptance source-snapshot summary is not exact")
    english_root_value = snapshot.get("english_root")
    if not isinstance(english_root_value, str) or not english_root_value.strip():
        raise ReconciliationError("full acceptance English root is invalid")
    english_root = Path(english_root_value).resolve()
    units = snapshot.get("units")
    if not isinstance(units, list) or len(units) != 722:
        raise ReconciliationError("full acceptance source snapshot is not 722-exact")
    unit_fields = frozenset(("id", "english", "msa", "classical"))
    layer_fields = frozenset(("path", "bytes", "sha256"))
    for expected, item in zip(baseline["units"], units, strict=True):
        if not isinstance(item, dict) or set(item) != unit_fields or item.get("id") != expected["id"]:
            raise ReconciliationError("full acceptance source-snapshot order/identity differs")
        for key, expected_path in (("msa", expected["arabic_path"]),
                                   ("classical", expected["target_path"])):
            layer = item.get(key)
            if not isinstance(layer, dict) or set(layer) != layer_fields or layer.get("path") != expected_path:
                raise ReconciliationError(f"invalid {key} snapshot identity for {expected['id']}")
            raw = safe_repo_path(repo, expected_path, suffix=".tex").read_bytes()
            if layer.get("bytes") != len(raw) or layer.get("sha256") != sha256(raw):
                raise ReconciliationError(f"live {key} snapshot drifted for {expected['id']}")
        english = item.get("english")
        if (not isinstance(english, dict) or set(english) != layer_fields or
                english.get("path") != expected["source_path"] or
                english.get("sha256") != expected["english_sha256"]):
            raise ReconciliationError(f"invalid frozen-English snapshot identity for {expected['id']}")
        relative = PurePosixPath(expected["source_path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ReconciliationError(f"unsafe frozen-English path for {expected['id']}")
        english_path = (english_root / Path(*relative.parts)).resolve()
        try:
            english_path.relative_to(english_root)
        except ValueError as exc:
            raise ReconciliationError(f"frozen-English path escapes root for {expected['id']}") from exc
        english_raw = english_path.read_bytes()
        if english.get("bytes") != len(english_raw) or english.get("sha256") != sha256(english_raw):
            raise ReconciliationError(f"live frozen-English snapshot drifted for {expected['id']}")
    if (not isinstance(snapshot.get("snapshot_sha256"), str) or
            snapshot["snapshot_sha256"] != canonical_sha256(units)):
        raise ReconciliationError("full acceptance source-snapshot fingerprint differs")


def source_acceptance_state(repo: Path, metadata: dict, baseline: dict,
                            preflight: dict) -> tuple[dict, list[dict]]:
    path = safe_repo_path(repo, metadata["acceptance_audit"], suffix=".json")
    data, raw = load_unique_json(path, "full translation acceptance audit")
    if set(data) != ACCEPTANCE_FIELDS or data.get("schema") != ACCEPTANCE_SCHEMA:
        raise ReconciliationError("unsupported full acceptance audit schema/fields")
    if data.get("release_id") != metadata.get("release_id"):
        raise ReconciliationError("full acceptance audit binds a different release")
    if data.get("overall_status") != "PASS" or not isinstance(data.get("acceptance_rule"), str):
        raise ReconciliationError("full acceptance audit is not an exact PASS")
    if not isinstance(data.get("created_utc"), str) or not data["created_utc"].strip():
        raise ReconciliationError("full acceptance audit lacks a deterministic creation identity")

    summary = data.get("summary")
    expected_summary = {
        "unit_count": 722, "live_source_bindings": 2166, "range_count": 8,
        "historical_blocker_count": 8,
        "resolved_historical_blocker_count": 8,
        "owner_followup_finding_count": 4, "blocking_finding_count": 0,
    }
    if not isinstance(summary, dict) or set(summary) != ACCEPTANCE_SUMMARY_FIELDS or summary != expected_summary:
        raise ReconciliationError("full acceptance summary counts are not exact")
    if data.get("preflight") != preflight:
        raise ReconciliationError("full acceptance preflight fingerprint/state drifted")

    historical = data.get("historical_audit")
    historical_fields = frozenset(("path", "bytes", "sha256", "raw_utf8"))
    if not isinstance(historical, dict) or set(historical) != historical_fields:
        raise ReconciliationError("full acceptance historical snapshot is invalid")
    historical_raw = historical.get("raw_utf8")
    if not isinstance(historical_raw, str):
        raise ReconciliationError("full acceptance historical bytes are unavailable")
    historical_bytes = historical_raw.encode("utf-8")
    if (historical.get("path") != metadata["acceptance_audit"] or
            historical.get("bytes") != len(historical_bytes) or
            historical.get("sha256") != sha256(historical_bytes)):
        raise ReconciliationError("full acceptance historical snapshot identity differs")
    historical_data = json_loads_unique(historical_raw, "historical full acceptance audit")
    if (historical_data.get("schema") != "openlogic-full-translation-acceptance-audit-v1" or
            historical_data.get("overall_status") != "FAIL" or
            not isinstance(historical_data.get("blocking_findings"), list) or
            len(historical_data["blocking_findings"]) != 8 or
            {item.get("id") for item in historical_data["blocking_findings"]
             if isinstance(item, dict)} != ACCEPTANCE_RESOLVED_IDS):
        raise ReconciliationError("full acceptance historical audit is not the eight-blocker v1 snapshot")

    authority_files = [file_identity(repo, path, raw)]
    artifacts = data.get("input_artifacts")
    if not isinstance(artifacts, list):
        raise ReconciliationError("full acceptance input artifacts are invalid")
    observed_paths = [item.get("path") for item in artifacts if isinstance(item, dict)]
    expected_paths = acceptance_input_paths(metadata, preflight)
    if (len(observed_paths) != len(set(observed_paths)) or
            set(observed_paths) != expected_paths):
        raise ReconciliationError("full acceptance input-artifact inventory is not exact")
    for item in artifacts:
        authority_files.append(_verify_acceptance_file_identity(repo, item, "full acceptance input"))

    ranges = data.get("range_results")
    if not isinstance(ranges, list) or len(ranges) != 8:
        raise ReconciliationError("full acceptance audit lacks eight exact range results")
    for expected, item in zip(ACCEPTANCE_EXPECTED_RANGES, ranges, strict=True):
        name, start, end = expected
        if (not isinstance(item, dict) or set(item) != ACCEPTANCE_RANGE_FIELDS or
                item.get("range") != name or item.get("unit_start") != start or
                item.get("unit_end") != end or item.get("unit_count") != end - start + 1 or
                item.get("source_acceptance") != "PASS" or
                not isinstance(item.get("semantic_review_paths"), list) or
                not item["semantic_review_paths"] or
                not isinstance(item.get("repair_evidence_paths"), list) or
                not item["repair_evidence_paths"] or
                not isinstance(item.get("continuation_finding_ids"), list)):
            raise ReconciliationError(f"full acceptance range result is invalid: {name}")

    resolved = data.get("resolved_historical_findings")
    if (not isinstance(resolved, list) or len(resolved) != 8 or
            any(not isinstance(item, dict) for item in resolved) or
            {item.get("id") for item in resolved if isinstance(item, dict)} != ACCEPTANCE_RESOLVED_IDS or
            any(set(item) != {"id", "status", "units", "evidence_refs", "resolution"} or
                item.get("status") != "PASS" or not item.get("units") or
                not item.get("evidence_refs") or not item.get("resolution")
                for item in resolved if isinstance(item, dict))):
        raise ReconciliationError("historical blocker resolution inventory is not exact")
    if data.get("blocking_findings") != []:
        raise ReconciliationError("full acceptance audit retains blocking findings")

    owner_path = safe_repo_path(repo, ACCEPTANCE_OWNER_ARTIFACTS[0], suffix=".json")
    owner, _ = load_unique_json(owner_path, "owner follow-up repairs")
    owner_findings = owner.get("findings")
    if (owner.get("schema") != "openlogic-classical-owner-followup-repairs-v1" or
            owner.get("status") != "PASS_FOUR_CONFIRMED_REPAIRS_BOUND_TO_CURRENT_BYTES" or
            not isinstance(owner_findings, list) or len(owner_findings) != 4 or
            {item.get("finding_id") for item in owner_findings if isinstance(item, dict)} !=
            ACCEPTANCE_OWNER_FOLLOWUP_IDS or data.get("owner_followup_findings") != owner_findings):
        raise ReconciliationError("owner follow-up continuation is not four-finding exact")
    expected_questions = [{
        "finding_id": item["finding_id"], "unit_id": item["unit_id"],
        "question": item["expert_review"]["question"],
        "open_to_correction": True, "non_blocking": True,
    } for item in owner_findings]
    if (any(item.get("expert_review", {}).get("open_to_correction") is not True or
            item.get("expert_review", {}).get("non_blocking") is not True
            for item in owner_findings) or
            data.get("nonblocking_expert_review_questions") != expected_questions):
        raise ReconciliationError("owner follow-up expert-review questions are not exact")

    _verify_acceptance_source_snapshot(repo, baseline, data.get("source_snapshot"))
    markdown = _verify_acceptance_file_identity(repo, data.get("markdown"), "full acceptance Markdown")
    authority_files.append(markdown)
    return {
        "source_ranges_ready": True,
        "nonpassing_source_ranges": [],
        "nonintegration_blocker_ids": [],
        "failed_required_verifications": [],
        "overall_status": "PASS",
        "audit_schema": ACCEPTANCE_SCHEMA,
        "source_snapshot_sha256": data["source_snapshot"]["snapshot_sha256"],
        "preflight_fingerprint_sha256": preflight["fingerprint_sha256"],
    }, authority_files


def build_general_reviews(checker, baseline: dict, baseline_hash: str,
                          corrections_hash: str, declarations_hash: str,
                          formal_hash: str, structural_hash: str,
                          report: dict, semantic: dict) -> dict:
    records = []
    for result in report["units"]:
        if result["status"] != "unchanged-prose":
            continue
        authority = semantic[result["id"]]
        records.append({
            "id": result["id"],
            "effective_msa_sha256": result["arabic_sha256"],
            "effective_msa_bytes": result["arabic_bytes"],
            "target_sha256": result["target_sha256"],
            "target_bytes": result["target_bytes"],
            "accepted_status": "unchanged-prose",
            "comparison_sha256": checker.formal_comparison_sha256(result),
            "authority_refs": [authority["authority_ref"]],
            "rationale": (
                "The exact current MSA and Classical Arabic-word projections are identical; "
                "the cited unit-level independent review found that this wording already "
                "fits the requested Classical register. " + authority["note"]),
        })
    return {
        "schema": checker.GENERAL_REVIEWS_SCHEMA,
        "baseline_sha256": baseline_hash,
        "baseline_corrections_sha256": corrections_hash,
        "declarations_sha256": declarations_hash,
        "formal_repairs_sha256": formal_hash,
        "structural_reviews_sha256": structural_hash,
        "units": records,
    }


def source_reconciliation_preflight(repo: Path, metadata_path: Path) -> dict:
    """Derive and validate every source-level artifact without reading acceptance.

    The acceptance audit calls this phase, and the finalizer repeats it before
    consuming that audit.  Keeping the phase independent removes the previous
    circularity in which acceptance asserted owner integration that could not be
    validated until after acceptance had already passed.
    """
    checker = load_checker(repo)
    baseline_path = repo / "evidence/classical/BASELINE.json"
    baseline, baseline_hash = checker.load_baseline(baseline_path)
    if baseline_hash != EXPECTED_BASELINE_SHA256 or len(baseline["units"]) != 722:
        raise ReconciliationError("immutable 722-unit baseline identity differs")
    metadata, metadata_raw = load_metadata(repo, metadata_path)
    source_repair_admission = validate_source_repair_batch_20260907(repo, checker, baseline)
    correction_meta, formal_meta, math_meta, structural_meta = metadata_maps(repo, metadata)

    corrections, correction_authority = build_corrections(
        repo, checker, baseline, baseline_hash, metadata, correction_meta)
    corrections_raw = json_bytes(corrections)
    corrections_hash = sha256(corrections_raw)

    declarations, math_authority = build_math_declarations(
        repo, checker, baseline, math_meta)
    declarations_raw = json_bytes(declarations)
    declarations_hash = sha256(declarations_raw)

    structural, structural_authority = build_structural_reviews(
        repo, checker, baseline, structural_meta)
    structural_raw = json_bytes(structural)
    structural_hash = sha256(structural_raw)

    formal, formal_authority, raw_report = build_formal_repairs(
        repo, checker, baseline, baseline_hash, corrections, corrections_hash,
        declarations, structural, formal_meta)
    formal_raw = json_bytes(formal)
    formal_hash = sha256(formal_raw)

    with_formal = checker.validate(
        repo, baseline, baseline["units"], declarations, structural,
        baseline_corrections=corrections, baseline_sha256=baseline_hash,
        formal_repairs=formal, baseline_corrections_sha256=corrections_hash)
    if any(unit["status"] in ("flagged", "baseline-mismatch") for unit in with_formal["units"]):
        raise ReconciliationError("formal declarations do not close every exact formal difference")

    semantic, semantic_files = semantic_authority(repo, metadata, baseline)
    general = build_general_reviews(
        checker, baseline, baseline_hash, corrections_hash, declarations_hash,
        formal_hash, structural_hash, with_formal, semantic)
    general_raw = json_bytes(general)
    general_hash = sha256(general_raw)

    final = checker.validate(
        repo, baseline, baseline["units"], declarations, structural,
        baseline_corrections=corrections, baseline_sha256=baseline_hash,
        formal_repairs=formal, baseline_corrections_sha256=corrections_hash,
        general_reviews=general, declarations_sha256=declarations_hash,
        formal_repairs_sha256=formal_hash,
        structural_reviews_sha256=structural_hash)
    if (final["exit_code"] != 0 or final["status"] != "STATIC_CHECKS_SATISFIED" or
            len(final["baseline_correction_entries_applied"]) != len(corrections["units"]) or
            len(final["formal_repair_entries_applied"]) != len(formal["units"]) or
            len(final["general_review_entries_applied"]) != len(general["units"]) or
            final["baseline_correction_entries_failed_binding"] or
            final["formal_repair_entries_failed_binding"] or
            final["general_review_entries_failed_binding"]):
        raise ReconciliationError("full 722-unit static reconciliation did not close")
    static_raw = json_bytes(final)
    snapshot_rows, snapshot_hash = source_snapshot(repo, baseline)
    derived = {
        OUTPUTS["baseline_corrections"]: corrections_raw,
        OUTPUTS["math_text_declarations"]: declarations_raw,
        OUTPUTS["structural_reviews"]: structural_raw,
        OUTPUTS["formal_repairs"]: formal_raw,
        OUTPUTS["general_reviews"]: general_raw,
        OUTPUTS["static_validation"]: static_raw,
    }
    preflight = {
        "schema": "openlogic-classical-source-reconciliation-preflight-v1",
        "status": "PASS",
        "release_id": metadata["release_id"],
        "source_snapshot_sha256": snapshot_hash,
        "frozen_baseline": file_identity(repo, baseline_path),
        "metadata": file_identity(repo, metadata_path, metadata_raw),
        "validator": file_identity(repo, repo / "build/validate_classical_overlay.py"),
        "semantic_authorities": semantic_files,
        "source_repair_admission": source_repair_admission,
        "derived_artifacts": [
            {"path": value, "bytes": len(raw), "sha256": sha256(raw)}
            for value, raw in derived.items()
        ],
        "counts": {
            "baseline_units": 722,
            "corrected_msa_units": len(corrections["units"]),
            "math_text_units": len(declarations["units"]),
            "math_text_items": sum(len(item["math_text"]) for item in declarations["units"]),
            "formal_repair_units": len(formal["units"]),
            "structural_review_units": len(structural["units"]),
            "unchanged_prose_review_units": len(general["units"]),
            "semantic_review_units": len(semantic),
            "static_statuses": dict(sorted(Counter(
                item["status"] for item in final["units"]).items())),
        },
        "checks": {
            "immutable_baseline_exact": True,
            "all_live_msa_deltas_declared": True,
            "all_formula_local_arabic_differences_declared": True,
            "all_formal_failures_exactly_declared": True,
            "all_unchanged_prose_exactly_reviewed": True,
            "semantic_review_unit_coverage_722": True,
            "full_static_validator_exit_zero": True,
            "consolidated_source_repair_batch_exact": True,
        },
    }
    preflight["fingerprint_sha256"] = canonical_sha256(preflight)
    return {
        "checker": checker, "baseline_path": baseline_path,
        "baseline": baseline, "baseline_hash": baseline_hash,
        "metadata": metadata, "metadata_raw": metadata_raw,
        "corrections": corrections, "correction_authority": correction_authority,
        "corrections_raw": corrections_raw, "corrections_hash": corrections_hash,
        "declarations": declarations, "math_authority": math_authority,
        "declarations_raw": declarations_raw, "declarations_hash": declarations_hash,
        "structural": structural, "structural_authority": structural_authority,
        "structural_raw": structural_raw, "structural_hash": structural_hash,
        "formal": formal, "formal_authority": formal_authority,
        "formal_raw": formal_raw, "formal_hash": formal_hash,
        "raw_report": raw_report, "semantic": semantic,
        "semantic_files": semantic_files, "general": general,
        "general_raw": general_raw, "general_hash": general_hash,
        "final": final, "static_raw": static_raw,
        "snapshot_rows": snapshot_rows, "snapshot_hash": snapshot_hash,
        "preflight": preflight,
    }


def derive(repo: Path, metadata_path: Path) -> tuple[dict[str, bytes], dict]:
    context = source_reconciliation_preflight(repo, metadata_path)
    checker = context["checker"]
    baseline_path = context["baseline_path"]
    baseline = context["baseline"]
    metadata = context["metadata"]
    metadata_raw = context["metadata_raw"]
    corrections = context["corrections"]
    correction_authority = context["correction_authority"]
    corrections_raw = context["corrections_raw"]
    corrections_hash = context["corrections_hash"]
    declarations = context["declarations"]
    math_authority = context["math_authority"]
    declarations_raw = context["declarations_raw"]
    declarations_hash = context["declarations_hash"]
    structural = context["structural"]
    structural_authority = context["structural_authority"]
    structural_raw = context["structural_raw"]
    structural_hash = context["structural_hash"]
    formal = context["formal"]
    formal_authority = context["formal_authority"]
    formal_raw = context["formal_raw"]
    formal_hash = context["formal_hash"]
    raw_report = context["raw_report"]
    semantic = context["semantic"]
    semantic_files = context["semantic_files"]
    general = context["general"]
    general_raw = context["general_raw"]
    general_hash = context["general_hash"]
    final = context["final"]
    static_raw = context["static_raw"]
    snapshot_rows = context["snapshot_rows"]
    snapshot_hash = context["snapshot_hash"]
    acceptance, acceptance_files = source_acceptance_state(
        repo, metadata, baseline, context["preflight"])

    correction_by_id = {item["id"]: item for item in corrections["units"]}
    formal_by_id = {item["id"]: item for item in formal["units"]}
    math_by_id = {item["id"]: item for item in declarations["units"]}
    structural_by_id = {item["id"]: item for item in structural["units"]}
    general_by_id = {item["id"]: item for item in general["units"]}
    final_by_id = {item["id"]: item for item in final["units"]}
    closure_units = []
    for unit in baseline["units"]:
        uid, result = unit["id"], final_by_id[unit["id"]]
        correction = correction_by_id.get(uid)
        formal_record = formal_by_id.get(uid)
        math_record = math_by_id.get(uid)
        structural_record = structural_by_id.get(uid)
        general_record = general_by_id.get(uid)
        closure_units.append({
            "id": uid, "source_path": unit["source_path"],
            "english_sha256": unit["english_sha256"],
            "msa": {
                "path": unit["arabic_path"], "sha256": result["arabic_sha256"],
                "bytes": result["arabic_bytes"],
                "identity_mode": "baseline-correction" if correction else "frozen-baseline",
            },
            "classical": {
                "path": unit["target_path"], "sha256": result["target_sha256"],
                "bytes": result["target_bytes"],
            },
            "correction": None if correction is None else {
                "finding_ids": correction["finding_ids"],
                "rationale": correction["rationale"],
                **correction_authority[uid],
            },
            "math_text_declaration": None if math_record is None else {
                "indices": [item["index"] for item in math_record["math_text"]],
                "authority_refs": math_authority[uid],
            },
            "formal_repair": None if formal_record is None else {
                "accepted_failed_checks": formal_record["accepted_failed_checks"],
                "comparison_sha256": formal_record["comparison_sha256"],
                "authority_refs": formal_record["authority_refs"],
                "rationale": formal_record["rationale"],
                **formal_authority[uid],
            },
            "structural_review": None if structural_record is None else {
                "kind": structural_record["kind"],
                "authority_refs": structural_authority[uid],
            },
            "unchanged_prose_review": None if general_record is None else {
                "comparison_sha256": general_record["comparison_sha256"],
                "authority_refs": general_record["authority_refs"],
                "rationale": general_record["rationale"],
            },
            "semantic_authority": semantic[uid],
            "final_static_status": result["status"],
            "raw_comparison_sha256": checker.formal_comparison_sha256(result),
        })
    closure = {
        "schema": "openlogic-classical-source-closure-manifest-v1",
        "status": ("PASS" if acceptance["source_ranges_ready"] else
                   "STATIC_PASS_SOURCE_ACCEPTANCE_PENDING"),
        "release_id": metadata["release_id"],
        "total_units": len(closure_units),
        "source_snapshot_sha256": snapshot_hash,
        "frozen_baseline": file_identity(repo, baseline_path),
        "baseline_correction_overlay": {
            "path": OUTPUTS["baseline_corrections"],
            "sha256": corrections_hash, "bytes": len(corrections_raw),
        },
        "math_text_declarations": {
            "path": OUTPUTS["math_text_declarations"],
            "sha256": declarations_hash, "bytes": len(declarations_raw),
        },
        "structural_reviews": {
            "path": OUTPUTS["structural_reviews"],
            "sha256": structural_hash, "bytes": len(structural_raw),
        },
        "formal_repairs": {
            "path": OUTPUTS["formal_repairs"],
            "sha256": formal_hash, "bytes": len(formal_raw),
        },
        "general_reviews": {
            "path": OUTPUTS["general_reviews"],
            "sha256": general_hash, "bytes": len(general_raw),
        },
        "authority_files": semantic_files + acceptance_files,
        "source_acceptance": acceptance,
        "counts": {
            "baseline_units": 722,
            "corrected_msa_units": len(corrections["units"]),
            "math_text_units": len(declarations["units"]),
            "math_text_items": sum(len(item["math_text"]) for item in declarations["units"]),
            "formal_repair_units": len(formal["units"]),
            "structural_review_units": len(structural["units"]),
            "unchanged_prose_review_units": len(general["units"]),
            "static_statuses": dict(sorted(Counter(
                item["final_static_status"] for item in closure_units).items())),
        },
        "checks": {
            "immutable_baseline_exact": True,
            "all_live_msa_deltas_declared": True,
            "all_formula_local_arabic_differences_declared": True,
            "all_formal_failures_exactly_declared": True,
            "all_unchanged_prose_exactly_reviewed": True,
            "semantic_review_unit_coverage_722": True,
            "full_static_validator_exit_zero": True,
            "source_ranges_semantically_ready": acceptance["source_ranges_ready"],
        },
        "units": closure_units,
    }
    closure_raw = json_bytes(closure)
    outputs = {
        OUTPUTS["baseline_corrections"]: corrections_raw,
        OUTPUTS["math_text_declarations"]: declarations_raw,
        OUTPUTS["structural_reviews"]: structural_raw,
        OUTPUTS["formal_repairs"]: formal_raw,
        OUTPUTS["general_reviews"]: general_raw,
        OUTPUTS["static_validation"]: static_raw,
        OUTPUTS["closure_manifest"]: closure_raw,
    }
    receipt_files = [
        {"path": path, "sha256": sha256(raw), "bytes": len(raw)}
        for path, raw in outputs.items()
    ]
    receipt = {
        "schema": "openlogic-classical-source-reconciliation-audit-v1",
        "status": "PASS" if acceptance["source_ranges_ready"] else "STATIC_PASS_SOURCE_ACCEPTANCE_PENDING",
        "release_id": metadata["release_id"],
        "source_snapshot_sha256": snapshot_hash,
        "inputs": {
            "metadata": file_identity(repo, metadata_path, metadata_raw),
            "validator": file_identity(repo, repo / "build/validate_classical_overlay.py"),
            "frozen_baseline": file_identity(repo, baseline_path),
            "semantic_and_acceptance_authorities": semantic_files + acceptance_files,
        },
        "outputs": receipt_files,
        "validation": {
            "schema": final["schema"], "status": final["status"],
            "exit_code": final["exit_code"], "selected_units": final["selected_units"],
            "effective_source_verified_units": final["effective_source_verified_units"],
            "counts": final["counts"],
            "corrections_applied": len(final["baseline_correction_entries_applied"]),
            "formal_repairs_applied": len(final["formal_repair_entries_applied"]),
            "general_reviews_applied": len(final["general_review_entries_applied"]),
        },
        "source_acceptance": acceptance,
        "write_policy": (
            "All outputs are derived in memory between three identical 1,444-file "
            "MSA/Classical snapshots and replaced atomically per file under a fail-closed "
            "transaction marker. The closure manifest and audit receipt are committed "
            "last and bind the complete set; a partial replacement cannot validate."),
    }
    receipt_raw = json_bytes(receipt)
    outputs[OUTPUTS["audit_receipt"]] = receipt_raw
    summary = {
        "status": receipt["status"], "release_id": metadata["release_id"],
        "source_snapshot_sha256": snapshot_hash,
        "counts": closure["counts"], "output_identities": [
            {"path": path, "bytes": len(raw), "sha256": sha256(raw)}
            for path, raw in outputs.items()
        ],
        "raw_status_counts": raw_report["counts"],
        "final_status_counts": final["counts"],
        "source_acceptance": acceptance,
        "snapshot_rows": snapshot_rows,
    }
    return outputs, summary


def atomic_replace(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    except BaseException:
        try:
            os.unlink(name)
        except FileNotFoundError:
            pass
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--metadata", type=Path,
                        help="default: REPO/evidence/classical/SOURCE_RECONCILIATION_METADATA_20260905.json")
    parser.add_argument("--write", action="store_true",
                        help="replace final artifacts only after an unchanged source snapshot")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        repo = args.repo.resolve()
        metadata_path = (args.metadata.resolve() if args.metadata else
                         repo / "evidence/classical/SOURCE_RECONCILIATION_METADATA_20260905.json")
        checker = load_checker(repo)
        baseline, _ = checker.load_baseline(repo / "evidence/classical/BASELINE.json")
        before_rows, before_hash = source_snapshot(repo, baseline)
        outputs, summary = derive(repo, metadata_path)
        after_rows, after_hash = source_snapshot(repo, baseline)
        derived_rows = summary.get("snapshot_rows")
        derived_hash = summary.get("source_snapshot_sha256")
        if (before_hash != derived_hash or before_rows != derived_rows or
                before_hash != after_hash or before_rows != after_rows):
            raise ReconciliationError(
                "MSA/Classical source changed during reconciliation; no outputs were written")
        summary["source_snapshot_stable_during_derivation"] = True
        summary.pop("snapshot_rows", None)
        if args.write:
            if (summary.get("status") != "PASS" or
                    not summary.get("source_acceptance", {}).get("source_ranges_ready")):
                raise ReconciliationError(
                    "source acceptance is not PASS; final reconciliation outputs were not written")
            marker_path = safe_repo_path(repo, TRANSACTION_MARKER)
            marker_raw = json_bytes({
                "schema": "openlogic-classical-source-reconciliation-transaction-v1",
                "status": "WRITE_IN_PROGRESS",
                "release_id": summary.get("release_id"),
                "source_snapshot_sha256": before_hash,
            })
            atomic_replace(marker_path, marker_raw)
            audit_path = OUTPUTS["audit_receipt"]
            closure_path = OUTPUTS["closure_manifest"]
            write_order = [
                value for value in outputs
                if value not in (closure_path, audit_path)
            ] + [closure_path, audit_path]
            for value in write_order:
                raw = outputs[value]
                atomic_replace(safe_repo_path(repo, value, suffix=Path(value).suffix), raw)
            # Immediate byte readback of every local output.
            for value, raw in outputs.items():
                observed = safe_repo_path(repo, value).read_bytes()
                if observed != raw:
                    raise ReconciliationError(f"post-write byte readback differs: {value}")
            committed_rows, committed_hash = source_snapshot(repo, baseline)
            if committed_hash != before_hash or committed_rows != before_rows:
                raise ReconciliationError(
                    "MSA/Classical source changed during reconciliation commit; "
                    "the transaction marker remains and the outputs must not be consumed")
            marker_path.unlink(missing_ok=True)
            summary["source_snapshot_stable_through_commit"] = True
            summary["written"] = True
        else:
            summary["written"] = False
        if args.json:
            print(json.dumps(summary, ensure_ascii=True, indent=2))
        else:
            print(json.dumps({key: value for key, value in summary.items()
                              if key != "output_identities"}, ensure_ascii=True))
            print("READ-ONLY" if not args.write else "WRITTEN_AND_READ_BACK")
        return 0
    except (OSError, UnicodeError, ValueError, KeyError, TypeError,
            AttributeError, IndexError) as exc:
        failure = {"status": "FAIL", "written": False, "error": str(exc)}
        print(json.dumps(failure, ensure_ascii=True, indent=2 if args.json else None),
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
