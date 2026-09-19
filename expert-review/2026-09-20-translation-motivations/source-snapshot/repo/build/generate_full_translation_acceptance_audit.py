#!/usr/bin/env python3
"""Deterministically regenerate the full 722-unit translation acceptance audit.

The existing v1 FAIL audit is immutable historical evidence.  A v2 PASS audit
embeds its exact UTF-8 bytes and resolves its eight findings only through
explicit continuation records, a fresh source-reconciliation preflight, and a
fresh 722-unit English/MSA/Classical byte snapshot.  Default operation is
read-only.  ``--write`` replaces the JSON and Markdown only after two identical
in-memory derivations, stable source snapshots, and immediate post-write replay.

This script does not run TeX or edit translation, notation, or RTL sources.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path, PurePosixPath
import sys
from typing import Any


DEFAULT_ENGLISH_ROOT = Path(r"source-snapshot/english")
DEFAULT_METADATA = "evidence/classical/SOURCE_RECONCILIATION_METADATA_20260905.json"
AUDIT_PATH = "evidence/classical/FULL_TRANSLATION_ACCEPTANCE_AUDIT.json"
MARKDOWN_PATH = "evidence/classical/FULL_TRANSLATION_ACCEPTANCE_AUDIT.md"
OWNER_PATH = "evidence/classical/repairs/OWNER_FOLLOWUP_REPAIRS_20260905.json"
WRITE_MARKER = "evidence/classical/.FULL_TRANSLATION_ACCEPTANCE_WRITE_IN_PROGRESS"

RANGE_SPECS = (
    ("0001-0100", 1, 100,
     ("evidence/classical/reviews/0001-0050.json",
      "evidence/classical/reviews/0051-0100.json"),
     ("evidence/classical/repairs/0001-0100.json",
      "evidence/classical/repairs/0001-0100.md",
      "evidence/classical/repairs/OLP0021_TWO_ROOTS_NOTE_20260907.json",
      "evidence/classical/repairs/OLP0021_TWO_ROOTS_NOTE_20260907.md",
      "evidence/classical/repairs/OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907.json",
      "evidence/classical/repairs/OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907.md",
      "evidence/classical/repairs/OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907.json",
      "evidence/classical/repairs/OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907.md",
      "evidence/classical/repairs/OLP0031_0032_PAIRING_CONSTRUCTIONS_20260907.json",
      "evidence/classical/repairs/OLP0031_0032_PAIRING_CONSTRUCTIONS_20260907.md",
      "evidence/classical/repairs/OLP0033_NONENUMERABILITY_CONSTRUCTIONS_20260907.json",
      "evidence/classical/repairs/OLP0033_NONENUMERABILITY_CONSTRUCTIONS_20260907.md",
      "evidence/classical/repairs/OLP0034_REDUCTION_CONSTRUCTIONS_20260907.json",
      "evidence/classical/repairs/OLP0034_REDUCTION_CONSTRUCTIONS_20260907.md",
      "evidence/classical/repairs/OLP0035_EQUINUMEROSITY_CONSTRUCTIONS_20260907.json",
      "evidence/classical/repairs/OLP0035_EQUINUMEROSITY_CONSTRUCTIONS_20260907.md"),
     ("FTA-COVERAGE-0044-0050", "FTA-078-I1")),
    ("0101-0200", 101, 200,
     ("evidence/classical/reviews/0101-0200.json",),
     ("evidence/classical/repairs/0101-0200.json",
      "evidence/classical/repairs/0101-0200.md", OWNER_PATH,
      "evidence/classical/repairs/OWNER_FOLLOWUP_REPAIRS_20260905.md"),
     ("FTA-0118-I1", "C184-01", "C185-01")),
    ("0201-0300", 201, 300,
     ("evidence/classical/reviews/0201-0300.json",),
     ("evidence/classical/repairs/0201-0300.json",
      "evidence/classical/repairs/0201-0300.md"), ()),
    ("0301-0400", 301, 400,
     ("evidence/classical/reviews/0301-0400.json",),
     ("evidence/classical/repairs/0301-0400.json",
      "evidence/classical/repairs/0301-0400.md",
      "evidence/classical/repairs/OLP0321_0326_0368_SEMANTIC_SCOPE_20260907.json",
      "evidence/classical/repairs/OLP0321_0326_0368_SEMANTIC_SCOPE_20260907.md",
      "evidence/classical/repairs/OLP0375_0376_ARITHMETIC_SCOPE_20260907.json",
      "evidence/classical/repairs/OLP0375_0376_ARITHMETIC_SCOPE_20260907.md",
      "evidence/classical/repairs/OLP0394_0399_0400_0404_0409_MODAL_SCOPE_20260907.json",
      "evidence/classical/repairs/OLP0394_0399_0400_0404_0409_MODAL_SCOPE_20260907.md"), ()),
    ("0401-0500", 401, 500,
     ("evidence/classical/reviews/0401-0500.json",),
     ("evidence/classical/repairs/0401-0500.json",
      "evidence/classical/repairs/0401-0500.md", OWNER_PATH,
      "evidence/classical/repairs/OWNER_FOLLOWUP_REPAIRS_20260905.md",
      "evidence/classical/repairs/OLP0394_0399_0400_0404_0409_MODAL_SCOPE_20260907.json",
      "evidence/classical/repairs/OLP0394_0399_0400_0404_0409_MODAL_SCOPE_20260907.md"),
     ("FTA-0488-0490-M1", "0452-I1", "0452-I2", "0452-I3")),
    ("0501-0600", 501, 600,
     ("evidence/classical/reviews/0501-0600.json",),
     ("evidence/classical/repairs/0501-0600.json",
      "evidence/classical/repairs/0501-0600.md"), ("FTA-0588-N1",)),
    ("0601-0700", 601, 700,
     ("evidence/classical/reviews/0601-0700.json",),
     ("evidence/classical/repairs/0601-0700.json",
      "evidence/classical/repairs/0601-0700.md"), ("FTA-0643-WEAKGEN",)),
    ("0701-0722", 701, 722,
     ("evidence/classical/reviews/0701-0722.json",),
     ("evidence/classical/reviews/0701-0722.json",
      "evidence/classical/reviews/0701-0722.md"), ("FTA-0713-M1",)),
)

RESOLUTIONS = (
    ("FTA-COVERAGE-0044-0050", [f"OLP-{n:04d}" for n in range(44, 51)],
     ["evidence/classical/reviews/0001-0050.json#/units/43-49",
      "evidence/classical/repairs/0001-0100.json"],
     "The formerly unreviewed seven-unit gap now has explicit non-pending unit verdicts, substantive review notes, and empty issue lists."),
    ("FTA-078-I1", ["OLP-0078"],
     ["evidence/classical/repairs/0001-0100.json#/repairs/24"],
     "The finite-support and monotonicity repair is recorded as continuation 078-I1 and is included in the current source preflight."),
    ("FTA-0118-I1", ["OLP-0118"],
     ["evidence/classical/repairs/0101-0200.json#/finding_dispositions/7"],
     "The self-contained support-reserve and freshening proof is recorded as repaired in both Arabic layers."),
    ("FTA-0488-0490-M1", ["OLP-0490"],
     ["evidence/classical/repairs/0401-0500.json#/finding_dispositions/7"],
     "The neighborhood/propositional-letter repair is recorded in both Arabic layers and rebound by the fresh preflight."),
    ("FTA-0588-N1", ["OLP-0588"],
     ["evidence/classical/repairs/0501-0600.json#/finding_dispositions/11"],
     "The formerly Classical-only omission is repaired in both Arabic layers and accepted in the continuation ledger."),
    ("FTA-0643-WEAKGEN", ["OLP-0643"],
     ["evidence/classical/repairs/0601-0700.json#/finding_dispositions/14",
      "evidence/classical/repairs/0601-0700.json#/validation/independent_formal_reviews/1"],
     "The proof now uses freshened eigenconstants and a bijective constant swap covering Q1/Q2, identity, MP, and both QR forms."),
    ("FTA-0713-M1", ["OLP-0713"],
     ["evidence/classical/reviews/0701-0722.json#/findings/0"],
     "The modal-systems scope qualifier is explicitly resolved in both Arabic layers."),
    ("FTA-OWNER-INTEGRATION-0101-0700", ["OLP-0101-0700"],
     ["evidence/classical/SOURCE_RECONCILIATION_METADATA_20260905.json",
      "build/finalize_classical_source_reconciliation.py#source_reconciliation_preflight"],
     "A fresh independent preflight validates all 722 units and exact correction, formal, structural, semantic-review, and static-validation closure."),
)


def load_finalizer(repo: Path):
    path = repo / "build/finalize_classical_source_reconciliation.py"
    spec = importlib.util.spec_from_file_location("acceptance_finalizer", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load source reconciliation finalizer")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_json(finalizer, path: Path, label: str) -> tuple[dict, bytes]:
    return finalizer.load_unique_json(path, label)


def find_dict(items: Any, key: str, value: str, label: str) -> dict:
    if not isinstance(items, list):
        raise ValueError(f"{label} is not a list")
    matches = [item for item in items if isinstance(item, dict) and item.get(key) == value]
    if len(matches) != 1:
        raise ValueError(f"{label} does not contain exactly one {value}")
    return matches[0]


def validate_continuations(repo: Path, finalizer, preflight: dict,
                           baseline: dict) -> tuple[dict, dict]:
    review_0001, _ = load_json(finalizer, repo / "evidence/classical/reviews/0001-0050.json",
                               "0001-0050 review")
    reviewed = {item.get("id"): item for item in review_0001.get("units", [])
                if isinstance(item, dict)}
    for number in range(44, 51):
        uid = f"OLP-{number:04d}"
        item = reviewed.get(uid)
        if (not isinstance(item, dict) or not isinstance(item.get("verdict"), str) or
                item["verdict"].startswith("PENDING") or not item.get("review_notes") or
                item.get("issues") != []):
            raise ValueError(f"historical coverage blocker is not closed for {uid}")

    repair_0001, _ = load_json(finalizer, repo / "evidence/classical/repairs/0001-0100.json",
                               "0001-0100 repair continuation")
    repair_0078 = find_dict(repair_0001.get("repairs"), "unit_id", "OLP-0078", "0001 repairs")
    if "078-I1" not in repair_0078.get("finding_refs", []):
        raise ValueError("078-I1 continuation is absent")

    repair_0101, _ = load_json(finalizer, repo / "evidence/classical/repairs/0101-0200.json",
                               "0101-0200 repair continuation")
    item_0118 = find_dict(repair_0101.get("finding_dispositions"), "finding_id", "0118-I1",
                          "0101 finding dispositions")
    if item_0118.get("status") != "REPAIRED_WITH_SELF_CONTAINED_SUPPORT_RESERVE_AND_FRESHENING_PROOF_BOTH_LAYERS":
        raise ValueError("0118-I1 continuation is not the accepted both-layer repair")
    if repair_0101.get("unresolved_deterministic_issues_in_scope") != []:
        raise ValueError("0101-0200 repair continuation retains deterministic issues")

    repair_0401, _ = load_json(finalizer, repo / "evidence/classical/repairs/0401-0500.json",
                               "0401-0500 repair continuation")
    item_0490 = find_dict(repair_0401.get("finding_dispositions"), "finding_id", "0488-0490-M1",
                          "0401 finding dispositions")
    if not str(item_0490.get("status", "")).startswith("REPAIRED_BOTH_ARABIC_LAYERS"):
        raise ValueError("0488-0490-M1 continuation is not repaired in both layers")
    if repair_0401.get("unresolved_deterministic_issues_in_scope") != []:
        raise ValueError("0401-0500 repair continuation retains deterministic issues")

    repair_0501, _ = load_json(finalizer, repo / "evidence/classical/repairs/0501-0600.json",
                               "0501-0600 repair continuation")
    item_0588 = find_dict(repair_0501.get("finding_dispositions"), "finding_id", "0588-N1",
                          "0501 finding dispositions")
    if not str(item_0588.get("status", "")).startswith("REPAIRED_BOTH_ARABIC_LAYERS"):
        raise ValueError("0588-N1 continuation is not repaired in both layers")
    residual_0501 = repair_0501.get("residuals", {})
    if residual_0501.get("unresolved_deterministic_issues_in_scope") != []:
        raise ValueError("0501-0600 repair continuation retains deterministic issues")

    repair_0601, _ = load_json(finalizer, repo / "evidence/classical/repairs/0601-0700.json",
                               "0601-0700 repair continuation")
    item_0643 = find_dict(repair_0601.get("finding_dispositions"), "finding_id", "0643-I2",
                          "0601 finding dispositions")
    if (item_0643.get("formal_alias") != "FTA-0643-WEAKGEN" or
            item_0643.get("status") != "REPAIRED_BOTH_ARABIC_LAYERS_WITH_BIJECTIVE_CONSTANT_SWAP" or
            repair_0601.get("unresolved_deterministic_issues_in_scope") != [] or
            repair_0601.get("residual_blockers") != []):
        raise ValueError("FTA-0643-WEAKGEN continuation is not exactly closed")

    review_0701, _ = load_json(finalizer, repo / "evidence/classical/reviews/0701-0722.json",
                               "0701-0722 review continuation")
    item_0713 = find_dict(review_0701.get("findings"), "id", "0713-M1", "0701 findings")
    if (item_0713.get("status") != "RESOLVED_IN_BOTH_ARABIC_LAYERS" or
            item_0713.get("msa_defect_still_present") is not False):
        raise ValueError("FTA-0713-M1 continuation is not exactly closed")

    owner, _ = load_json(finalizer, repo / OWNER_PATH, "owner follow-up repairs")
    findings = owner.get("findings")
    if (owner.get("schema") != "openlogic-classical-owner-followup-repairs-v1" or
            owner.get("status") != "PASS_FOUR_CONFIRMED_REPAIRS_BOUND_TO_CURRENT_BYTES" or
            not isinstance(findings, list) or len(findings) != 4 or
            {item.get("finding_id") for item in findings if isinstance(item, dict)} !=
            finalizer.ACCEPTANCE_OWNER_FOLLOWUP_IDS):
        raise ValueError("owner follow-up continuation is not four-finding exact")
    baseline_by_id = {item["id"]: item for item in baseline["units"]}
    for finding in findings:
        if not isinstance(finding, dict):
            raise ValueError("owner follow-up finding is not an object")
        uid = finding.get("unit_id")
        if uid not in baseline_by_id:
            raise ValueError(f"owner follow-up has unknown unit: {uid}")
        if finding.get("english", {}).get("sha256") != baseline_by_id[uid]["english_sha256"]:
            raise ValueError(f"owner follow-up English identity differs for {uid}")
        review = finding.get("expert_review", {})
        if (review.get("open_to_correction") is not True or
                review.get("non_blocking") is not True or not review.get("question")):
            raise ValueError(f"owner follow-up expert-review contract differs for {uid}")
        for layer in ("msa", "classical"):
            current = finding.get("current", {}).get(layer, {})
            path_value = current.get("path")
            if not isinstance(path_value, str):
                raise ValueError(f"owner follow-up current path is absent for {uid}/{layer}")
            raw = finalizer.safe_repo_path(repo, path_value, suffix=".tex").read_bytes()
            if current.get("bytes") != len(raw) or current.get("sha256") != finalizer.sha256(raw):
                raise ValueError(f"owner follow-up current identity drifted for {uid}/{layer}")
    if preflight.get("status") != "PASS" or preflight.get("counts", {}).get("baseline_units") != 722:
        raise ValueError("fresh owner-integration preflight is not 722-unit PASS")
    return owner, review_0001


def historical_snapshot(finalizer, audit_path: Path) -> dict:
    raw = audit_path.read_bytes()
    data = finalizer.json_loads_unique(raw.decode("utf-8-sig"), "current acceptance audit")
    if data.get("schema") == finalizer.ACCEPTANCE_SCHEMA:
        historical = data.get("historical_audit")
        if not isinstance(historical, dict):
            raise ValueError("v2 audit lacks its frozen historical continuation")
        result = historical
    elif data.get("schema") == "openlogic-full-translation-acceptance-audit-v1":
        text = raw.decode("utf-8")
        result = {"path": AUDIT_PATH, "bytes": len(raw),
                  "sha256": finalizer.sha256(raw), "raw_utf8": text}
    else:
        raise ValueError("unsupported current acceptance audit schema")
    raw_text = result.get("raw_utf8")
    if not isinstance(raw_text, str):
        raise ValueError("historical audit does not preserve exact UTF-8 text")
    historical = finalizer.json_loads_unique(raw_text, "historical acceptance audit")
    blockers = historical.get("blocking_findings")
    if (historical.get("schema") != "openlogic-full-translation-acceptance-audit-v1" or
            historical.get("overall_status") != "FAIL" or not isinstance(blockers, list) or
            len(blockers) != 8 or {item.get("id") for item in blockers if isinstance(item, dict)} !=
            finalizer.ACCEPTANCE_RESOLVED_IDS or
            result.get("path") != AUDIT_PATH or
            result.get("bytes") != len(raw_text.encode("utf-8")) or
            result.get("sha256") != finalizer.sha256(raw_text.encode("utf-8"))):
        raise ValueError("historical audit is not the exact eight-blocker v1 continuation")
    return result


def external_path(root: Path, value: str) -> Path:
    rel = PurePosixPath(value)
    if rel.is_absolute() or ".." in rel.parts or rel.as_posix() != value:
        raise ValueError(f"unsafe frozen-English path: {value!r}")
    path = (root / Path(*rel.parts)).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"frozen-English path escapes root: {value!r}")
    return path


def build_source_snapshot(repo: Path, english_root: Path, finalizer,
                          baseline: dict, expected_live_hash: str) -> dict:
    english_root = english_root.resolve()
    if not english_root.is_dir():
        raise ValueError(f"frozen-English root does not exist: {english_root}")
    units = []
    live_rows = []
    for expected in baseline["units"]:
        english_raw = external_path(english_root, expected["source_path"]).read_bytes()
        if finalizer.sha256(english_raw) != expected["english_sha256"]:
            raise ValueError(f"frozen-English identity drifted for {expected['id']}")
        layers = {}
        for key, value in (("msa", expected["arabic_path"]),
                           ("classical", expected["target_path"])):
            raw = finalizer.safe_repo_path(repo, value, suffix=".tex").read_bytes()
            layers[key] = {"path": value, "bytes": len(raw),
                           "sha256": finalizer.sha256(raw)}
        units.append({
            "id": expected["id"],
            "english": {"path": expected["source_path"], "bytes": len(english_raw),
                        "sha256": finalizer.sha256(english_raw)},
            "msa": layers["msa"], "classical": layers["classical"],
        })
        live_rows.append({
            "id": expected["id"],
            "msa_sha256": layers["msa"]["sha256"],
            "msa_bytes": layers["msa"]["bytes"],
            "classical_sha256": layers["classical"]["sha256"],
            "classical_bytes": layers["classical"]["bytes"],
        })
    if len(units) != 722:
        raise ValueError("source snapshot is not 722-unit exact")
    if finalizer.canonical_sha256(live_rows) != expected_live_hash:
        raise ValueError("live MSA/Classical snapshot differs from fresh preflight")
    return {
        "schema": "openlogic-full-translation-source-snapshot-v1", "status": "PASS",
        "english_root": str(english_root), "unit_count": 722,
        "live_source_bindings": 2166,
        "snapshot_sha256": finalizer.canonical_sha256(units), "units": units,
    }


def render_markdown(audit: dict) -> bytes:
    summary = audit["summary"]
    lines = [
        "# Full translation acceptance audit", "",
        f"Status: **{audit['overall_status']}**", "",
        (f"This deterministic continuation accepts {summary['unit_count']} units and "
         f"{summary['live_source_bindings']} live English/MSA/Classical bindings. It "
         "preserves the original v1 FAIL audit byte-for-byte and resolves each of its "
         "eight blockers through named continuation evidence; it does not rewrite the "
         "historical reviews as contemporaneous records."), "",
        "## Acceptance counts", "",
        "| Measure | Count |", "|---|---:|",
    ]
    for key, value in summary.items():
        lines.append(f"| `{key}` | {value} |")
    lines += ["", "## Range acceptance", "",
              "| Range | Units | Result | Continuations |", "|---|---:|---|---|"]
    for item in audit["range_results"]:
        continuations = ", ".join(f"`{value}`" for value in item["continuation_finding_ids"]) or "—"
        lines.append(f"| {item['range']} | {item['unit_count']} | {item['source_acceptance']} | {continuations} |")
    lines += ["", "## Historical blocker continuation chain", "",
              "| Historical finding | Units | Resolution evidence |", "|---|---|---|"]
    for item in audit["resolved_historical_findings"]:
        refs = "<br>".join(f"`{value}`" for value in item["evidence_refs"])
        lines.append(f"| `{item['id']}` | {', '.join(item['units'])} | {refs}<br>{item['resolution']} |")
    lines += ["", "## Owner follow-up decisions open to expert correction", "",
              "These questions are review aids, not release blockers.", "",
              "| Finding | Unit | Provisional choice | Why | Expert question |",
              "|---|---|---|---|---|"]
    for item in audit["owner_followup_findings"]:
        lines.append("| `{}` | {} | {} | {} | {} |".format(
            item["finding_id"], item["unit_id"], item["chosen_arabic"].replace("|", "\\|"),
            item["rationale"].replace("|", "\\|"),
            item["expert_review"]["question"].replace("|", "\\|")))
    lines += ["", "## Deterministic identities", "",
              f"- Fresh preflight fingerprint: `{audit['preflight']['fingerprint_sha256']}`",
              f"- Full source snapshot: `{audit['source_snapshot']['snapshot_sha256']}`",
              f"- Frozen historical audit: `{audit['historical_audit']['sha256']}`", "",
              "| Input artifact | Bytes | SHA-256 |", "|---|---:|---|"]
    for item in audit["input_artifacts"]:
        lines.append(f"| `{item['path']}` | {item['bytes']} | `{item['sha256']}` |")
    lines += ["", "## Blocking findings", "",
              "None. All four expert-review questions remain explicitly non-blocking and open to correction.", ""]
    return "\n".join(lines).encode("utf-8")


def build(repo: Path, metadata_path: Path, english_root: Path,
          finalizer=None) -> tuple[bytes, bytes, dict]:
    finalizer = load_finalizer(repo) if finalizer is None else finalizer
    context = finalizer.source_reconciliation_preflight(repo, metadata_path)
    metadata = context["metadata"]
    baseline = context["baseline"]
    preflight = context["preflight"]
    owner, _ = validate_continuations(repo, finalizer, preflight, baseline)
    historical = historical_snapshot(finalizer, repo / AUDIT_PATH)
    source_snapshot = build_source_snapshot(
        repo, english_root, finalizer, baseline, preflight["source_snapshot_sha256"])
    input_artifacts = []
    for value in sorted(finalizer.acceptance_input_paths(metadata, preflight)):
        path = finalizer.safe_repo_path(repo, value)
        input_artifacts.append(finalizer.file_identity(repo, path))
    ranges = [{
        "range": name, "unit_start": start, "unit_end": end,
        "unit_count": end - start + 1, "source_acceptance": "PASS",
        "semantic_review_paths": list(reviews),
        "repair_evidence_paths": list(repairs),
        "continuation_finding_ids": list(continuations),
    } for name, start, end, reviews, repairs, continuations in RANGE_SPECS]
    resolved = [{"id": finding_id, "status": "PASS", "units": units,
                 "evidence_refs": refs, "resolution": resolution}
                for finding_id, units, refs, resolution in RESOLUTIONS]
    questions = [{
        "finding_id": item["finding_id"], "unit_id": item["unit_id"],
        "question": item["expert_review"]["question"],
        "open_to_correction": True, "non_blocking": True,
    } for item in owner["findings"]]
    audit = {
        "schema": finalizer.ACCEPTANCE_SCHEMA,
        "release_id": metadata["release_id"], "created_utc": owner["created_utc"],
        "overall_status": "PASS",
        "acceptance_rule": (
            "PASS requires an exact 722-unit and 2,166-binding source snapshot, a fresh "
            "source-reconciliation preflight, explicit continuations for all eight frozen "
            "v1 blockers, exactly four hash-bound owner follow-ups, zero blocking findings, "
            "and byte-identical deterministic replay."),
        "summary": {
            "unit_count": 722, "live_source_bindings": 2166, "range_count": 8,
            "historical_blocker_count": 8, "resolved_historical_blocker_count": 8,
            "owner_followup_finding_count": 4, "blocking_finding_count": 0,
        },
        "historical_audit": historical, "input_artifacts": input_artifacts,
        "preflight": preflight, "source_snapshot": source_snapshot,
        "range_results": ranges, "resolved_historical_findings": resolved,
        "owner_followup_findings": owner["findings"], "blocking_findings": [],
        "nonblocking_expert_review_questions": questions,
    }
    markdown_raw = render_markdown(audit)
    audit["markdown"] = {"path": MARKDOWN_PATH, "bytes": len(markdown_raw),
                         "sha256": finalizer.sha256(markdown_raw)}
    json_raw = finalizer.json_bytes(audit)
    return json_raw, markdown_raw, {
        "status": "PASS", "schema": audit["schema"], "unit_count": 722,
        "live_source_bindings": 2166,
        "source_snapshot_sha256": source_snapshot["snapshot_sha256"],
        "preflight_fingerprint_sha256": preflight["fingerprint_sha256"],
        "historical_audit_sha256": historical["sha256"],
        "owner_followup_finding_ids": [item["finding_id"] for item in owner["findings"]],
        "blocking_findings": [],
        "outputs": [
            {"path": AUDIT_PATH, "bytes": len(json_raw), "sha256": finalizer.sha256(json_raw)},
            {"path": MARKDOWN_PATH, "bytes": len(markdown_raw), "sha256": finalizer.sha256(markdown_raw)},
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--english-root", type=Path, default=DEFAULT_ENGLISH_ROOT)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        repo = args.repo.resolve()
        metadata_path = (args.metadata.resolve() if args.metadata else repo / DEFAULT_METADATA)
        english_root = args.english_root.resolve()
        finalizer = load_finalizer(repo)
        first_json, first_md, summary = build(repo, metadata_path, english_root, finalizer)
        second_json, second_md, second_summary = build(repo, metadata_path, english_root, finalizer)
        if (first_json != second_json or first_md != second_md or summary != second_summary):
            raise ValueError("deterministic replay differed before write; outputs were not written")
        summary["deterministic_replay"] = True
        if args.write:
            marker = finalizer.safe_repo_path(repo, WRITE_MARKER)
            finalizer.atomic_replace(marker, finalizer.json_bytes({
                "schema": "openlogic-full-translation-acceptance-transaction-v1",
                "status": "WRITE_IN_PROGRESS",
                "source_snapshot_sha256": summary["source_snapshot_sha256"],
            }))
            try:
                finalizer.atomic_replace(finalizer.safe_repo_path(repo, MARKDOWN_PATH), first_md)
                finalizer.atomic_replace(finalizer.safe_repo_path(repo, AUDIT_PATH), first_json)
                if (finalizer.safe_repo_path(repo, MARKDOWN_PATH).read_bytes() != first_md or
                        finalizer.safe_repo_path(repo, AUDIT_PATH).read_bytes() != first_json):
                    raise ValueError("post-write output readback differed")
                replay_json, replay_md, replay_summary = build(
                    repo, metadata_path, english_root, finalizer)
                if replay_json != first_json or replay_md != first_md:
                    raise ValueError("post-write deterministic replay differed")
                context = finalizer.source_reconciliation_preflight(repo, metadata_path)
                finalizer.source_acceptance_state(
                    repo, context["metadata"], context["baseline"], context["preflight"])
                if replay_summary["source_snapshot_sha256"] != summary["source_snapshot_sha256"]:
                    raise ValueError("source snapshot changed through write")
            except BaseException:
                raise
            else:
                marker.unlink(missing_ok=True)
            summary["written"] = True
            summary["post_write_replay"] = True
            summary["strict_consumer_verification"] = True
        else:
            summary["written"] = False
        print(json.dumps(summary, ensure_ascii=args.json, indent=2 if args.json else None))
        return 0
    except (OSError, UnicodeError, ValueError, KeyError, TypeError,
            AttributeError, IndexError) as exc:
        failure = {"status": "FAIL", "written": False, "error": str(exc)}
        print(json.dumps(failure, ensure_ascii=True, indent=2 if args.json else None), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
