#!/usr/bin/env python3
"""Bind the MSA build manifest to historical closure and an exact new successor.

Only the ``ar_sha256`` CSV cells may change.  Every other cell, including all
Farsi paths, statuses, hashes, and QA fields, is protected by exact row/field
comparison.  The write path preserves each original physical CSV line and its
line ending; it replaces only the quoted stale hash token.
Without --successor-ledger the original closure route is unchanged. With the
explicit option, one fixed published OLP-0087 correction is inverse-verified;
historical Classical acceptance, closure and rebind receipts are preserved.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import os
import re
import sys
from pathlib import Path


SCHEMA = "openlogic-msa-closure-manifest-rebind-v1"
DEFAULT_MANIFEST = "evidence/provenance/openlogic-control/CLOSURE_MANIFEST.csv"
DEFAULT_AUTHORITY = "evidence/classical/SOURCE_RECONCILIATION_CLOSURE_MANIFEST_20260905.json"
DEFAULT_RECEIPT = "evidence/provenance/openlogic-control/MSA_CLOSURE_MANIFEST_REBIND_20260905.json"
HASH = re.compile(r"^[0-9a-fA-F]{64}$")
PROOF_LEDGER = "evidence/classical/terminology/SOL6_PROOF_QUANTIFICATION_RECHECK_20260930.json"
PROOF_LEDGER_SHA256 = "db3449f279e4d2a5edf9cec4e94f771ae9845da7622e270bda9160b4f1f63446"
PROOF_SOURCE = "source/locale/ar/content/first-order-logic/natural-deduction/quantifier-rules.tex"
PROOF_BEFORE = (4709, "4a35f7a7a408828a889a9df3233addcc625b4ff2551af04ad4d8f0b248983b23")
PROOF_AFTER = (5135, "703474b299636221bb5da83487d565cc39619c79e9156274fe91ea60e45b666f")
PROOF_CLASSICAL = "source/locale/ar-classical/content/first-order-logic/natural-deduction/quantifier-rules.tex"
PROOF_CLASSICAL_ID = (4876, "594bad6dd0327dcbe88ad702bc95adbbdb6fb56c4aa56e9d7ed3213362546fbe")


class RebindError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise RebindError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RebindError(f"cannot read strict JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RebindError(f"JSON root is not an object: {path}")
    return value


def field_digest(fieldnames: list[str], rows: list[dict], excluded: set[str]) -> str:
    digest = hashlib.sha256()
    for row in rows:
        for field in fieldnames:
            if field in excluded:
                continue
            encoded = (field + "\0" + str(row.get(field, "")) + "\0").encode("utf-8")
            digest.update(len(encoded).to_bytes(8, "big"))
            digest.update(encoded)
    return digest.hexdigest().upper()


def read_csv(raw: bytes) -> tuple[list[str], list[dict]]:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise RebindError(f"manifest is not UTF-8: {exc}") from exc
    reader = csv.DictReader(text.splitlines())
    fieldnames = list(reader.fieldnames or [])
    rows = list(reader)
    if len(rows) != 722:
        raise RebindError(f"manifest has {len(rows)} rows, expected 722")
    required = {
        "closure_id", "stable_order", "source_path", "source_sha256",
        "ar_target_path", "ar_status", "ar_sha256",
        "fa_IR_target_path", "fa_IR_status", "fa_IR_sha256", "fa_IR_qa",
    }
    missing = sorted(required - set(fieldnames))
    if missing:
        raise RebindError(f"manifest lacks required fields: {missing}")
    return fieldnames, rows


def proof_successor(repo: Path, ledger_path: Path, unit: dict) -> tuple[dict, dict]:
    """Admit one published, inverse-proved MSA change; never rewrite old audits.

    This is a current MSA build overlay, not retrospective Classical acceptance
    or a claim that the historical closure originally contained the correction.
    Both endpoint hashes and the complete published decision ledger are pinned.
    """
    if ledger_path.resolve() != (repo / PROOF_LEDGER).resolve():
        raise RebindError("MSA successor is not the single supported review ledger")
    if sha256_path(ledger_path).lower() != PROOF_LEDGER_SHA256:
        raise RebindError("published MSA successor ledger identity changed")
    ledger = load_json(ledger_path)
    transitions = ledger.get("source_transitions")
    if (ledger.get("schema") != "openlogic-arabic-contextual-recheck-v1" or
            not isinstance(transitions, list) or len(transitions) != 1):
        raise RebindError("MSA successor is not exactly one declared transition")
    t = transitions[0]
    if (unit.get("id") != "OLP-0087" or unit["msa"].get("path") != PROOF_SOURCE or
            (unit["msa"].get("bytes"), unit["msa"].get("sha256", "").lower()) != PROOF_BEFORE or
            t.get("logical_path") != PROOF_SOURCE or
            (t.get("before_bytes"), t.get("before_sha256")) != PROOF_BEFORE or
            (t.get("after_bytes"), t.get("after_sha256")) != PROOF_AFTER or
            len(t.get("edits", [])) != 2):
        raise RebindError("MSA successor endpoints differ from the exact OLP-0087 correction")
    raw = (repo / PROOF_SOURCE).read_bytes()
    if (len(raw), sha256_bytes(raw).lower()) != PROOF_AFTER:
        raise RebindError("MSA successor current source drifted")
    text = raw.decode("utf-8")
    inverse = text
    for edit in t["edits"]:
        before, after = edit["before_text"], edit["after_text"]
        if not before or not after or before == after or inverse.count(after) != 1:
            raise RebindError("MSA successor edit is not uniquely invertible")
        inverse = inverse.replace(after, before, 1)
    prior = inverse.encode("utf-8")
    if (len(prior), sha256_bytes(prior).lower()) != PROOF_BEFORE:
        raise RebindError("MSA successor inverse does not restore the historical whole-file bytes")
    pattern = r"\\begin\{(defish|prooftree)\}.*?\\end\{\1\}"
    old_blocks = [m.group() for m in re.finditer(pattern, inverse, flags=re.S)]
    new_blocks = [m.group() for m in re.finditer(pattern, text, flags=re.S)]
    if (len(inverse.splitlines()) != len(text.splitlines()) or
            len(old_blocks) != 4 or old_blocks != new_blocks):
        raise RebindError("MSA successor moved source lines or changed a rule/derivation block")
    classical = (repo / PROOF_CLASSICAL).read_bytes()
    if (len(classical), sha256_bytes(classical).lower()) != PROOF_CLASSICAL_ID:
        raise RebindError("already-correct Classical counterpart changed")
    from validate_classical_overlay import analyze, compare, formal_comparison_sha256, math_signature
    old_analysis, new_analysis = analyze(inverse), analyze(text)
    old_formulas = [(kind, math_signature(ts, {})) for kind, ts in old_analysis.formulas]
    new_formulas = [(kind, math_signature(ts, {})) for kind, ts in new_analysis.formulas]
    extra = [(kind, math_signature(ts, {})) for kind, ts in analyze("$!A(a)$").formulas]
    if (len(old_formulas) != 57 or len(new_formulas) != 58 or len(extra) != 1 or
            new_formulas != old_formulas[:26] + extra + old_formulas[26:]):
        raise RebindError("MSA successor formula inventory differs beyond one explanatory A(a) reference")
    previous_comparison = compare(inverse, classical.decode("utf-8"))
    current_comparison = compare(text, classical.decode("utf-8"))
    if (formal_comparison_sha256(previous_comparison) !=
            "912fd0ba38d41963bd10ae18d352327842f77066eb2cc65d2118c4c02e2a58f8" or
            formal_comparison_sha256(current_comparison) !=
            "805e78b03964cc0f5217908147ef5444daf10b5e7ca94b4ee9353861ab73eeab" or
            [key for key, value in current_comparison["checks"].items() if not value] !=
            ["ordered_formula_segments_and_tokens"]):
        raise RebindError("MSA successor raw cross-edition comparison changed")
    current = copy.deepcopy(unit)
    current["msa"].update(bytes=PROOF_AFTER[0], sha256=PROOF_AFTER[1],
                          identity_mode="exact-published-msa-successor")
    return current, {
        "schema": "openlogic-exact-msa-source-successor-v1", "status": "PASS",
        "unit_id": "OLP-0087",
        "ledger": {"path": PROOF_LEDGER, "bytes": ledger_path.stat().st_size,
                   "sha256": PROOF_LEDGER_SHA256},
        "source": {"path": PROOF_SOURCE, "before_bytes": PROOF_BEFORE[0],
                   "before_sha256": PROOF_BEFORE[1], "after_bytes": PROOF_AFTER[0],
                   "after_sha256": PROOF_AFTER[1]},
        "classical": {"path": PROOF_CLASSICAL, "bytes": PROOF_CLASSICAL_ID[0],
                      "sha256": PROOF_CLASSICAL_ID[1]},
        "checks": {"unique_two_edit_inverse": True, "whole_predecessor_restored": True,
                   "four_rule_blocks_unchanged": True, "source_line_count_unchanged": True,
                   "classical_counterpart_unchanged": True,
                   "all_57_preexisting_formula_segments_unchanged": True,
                   "only_one_explanatory_Aa_formula_reference_added": True},
        "cross_edition_comparison": {
            "previous_sha256": formal_comparison_sha256(previous_comparison),
            "current_sha256": formal_comparison_sha256(current_comparison),
            "raw_status": current_comparison["status"],
            "raw_failed_checks": ["ordered_formula_segments_and_tokens"],
            "previous_formula_segments": 57, "current_formula_segments": 58,
            "scope_ar": "المقارنة الحرفية مع التراثية تشير إلى زيادة إحالة تفسيرية واحدة A(a) في المعيارية. جميع المقاطع الرمزية السبعة والخمسين السابقة محفوظة بترتيبها؛ ليس هذا تغييرًا في قاعدة أو اشتقاق ولا إقرارًا رجعيًا بفحص كامل للتراثية.",
        },
        "scope_ar": "تصحيح عبارتين في المعيارية المشتركة: استثناء الافتراضات المؤقتة المسقطة، وبقاء الحد t مغلقًا. لا يعاد تأريخ الإقرار السابق ولا يدعى بناء PDF أو EPUB بهذا الإيصال.",
        "ai_work": "OpenAI Codex — GPT-6.1 Sol, Ultra effort",
    }


def authority_units(repo: Path, path: Path, successor_ledger: Path | None = None) -> tuple[dict, list[dict], dict | None]:
    authority = load_json(path)
    if authority.get("schema") != "openlogic-classical-source-closure-manifest-v1":
        raise RebindError("source authority schema is not the canonical closure manifest v1")
    if authority.get("status") != "PASS" or authority.get("total_units") != 722:
        raise RebindError("source authority is not a 722-unit PASS")
    units = authority.get("units")
    if not isinstance(units, list) or len(units) != 722:
        raise RebindError("source authority units are not exactly 722")
    expected_ids = [f"OLP-{number:04d}" for number in range(1, 723)]
    actual_ids = [str(unit.get("id", "")) for unit in units if isinstance(unit, dict)]
    if actual_ids != expected_ids:
        raise RebindError("source authority unit IDs are not exact ordered OLP-0001--0722")
    units = copy.deepcopy(units)
    successor = None
    if successor_ledger is not None:
        units[86], successor = proof_successor(repo, successor_ledger, units[86])
    for unit in units:
        msa = unit.get("msa")
        if not isinstance(msa, dict):
            raise RebindError(f"{unit['id']}: missing MSA identity")
        rel = str(msa.get("path", "")).replace("\\", "/")
        digest = str(msa.get("sha256", ""))
        if not rel.startswith("source/locale/ar/content/") or not HASH.fullmatch(digest):
            raise RebindError(f"{unit['id']}: malformed MSA path/hash authority")
        live = repo / rel
        if not live.is_file():
            raise RebindError(f"{unit['id']}: MSA source is missing: {rel}")
        raw = live.read_bytes()
        if sha256_bytes(raw).casefold() != digest.casefold() or len(raw) != msa.get("bytes"):
            raise RebindError(f"{unit['id']}: canonical MSA authority does not match live bytes")
    return authority, units, successor


def derive(repo: Path, manifest_path: Path, authority_path: Path,
           successor_ledger: Path | None = None) -> dict:
    before = manifest_path.read_bytes()
    fieldnames, rows = read_csv(before)
    authority, units, successor = authority_units(repo, authority_path, successor_ledger)
    expected_ids = [f"OLP-{number:04d}" for number in range(1, 723)]
    if [row["closure_id"] for row in rows] != expected_ids:
        raise RebindError("CSV unit IDs are not exact ordered OLP-0001--0722")
    if [row["stable_order"] for row in rows] != [str(number) for number in range(1, 723)]:
        raise RebindError("CSV stable_order is not exact 1--722")

    lines = before.decode("utf-8").splitlines(keepends=True)
    if len(lines) != 723:
        raise RebindError("CSV must contain one physical header and one physical line per unit")
    changed = []
    updated_lines = [lines[0]]
    after_rows = []
    for index, (row, unit) in enumerate(zip(rows, units), 1):
        msa = unit["msa"]
        expected_target = str(msa["path"]).removeprefix("source/")
        if row["ar_target_path"].replace("\\", "/") != expected_target:
            raise RebindError(f"{unit['id']}: CSV and closure MSA paths differ")
        if row["source_path"].replace("\\", "/") != str(unit["source_path"]).replace("\\", "/"):
            raise RebindError(f"{unit['id']}: CSV and closure English paths differ")
        if row["source_sha256"].casefold() != str(unit["english_sha256"]).casefold():
            raise RebindError(f"{unit['id']}: CSV and closure English hashes differ")
        if row["ar_status"] != "ACCEPTED":
            raise RebindError(f"{unit['id']}: CSV Arabic status is not ACCEPTED")
        old = row["ar_sha256"]
        new = str(msa["sha256"]).upper()
        if not HASH.fullmatch(old):
            raise RebindError(f"{unit['id']}: malformed current CSV Arabic hash")
        physical = lines[index]
        stale = old.casefold() != new.casefold()
        if stale:
            token = f'"{old}"'
            if physical.count(token) != 1:
                raise RebindError(f"{unit['id']}: stale hash is not one exact quoted line token")
            physical = physical.replace(token, f'"{new}"', 1)
            changed.append({"id": unit["id"], "old_ar_sha256": old.upper(), "new_ar_sha256": new})
        updated_lines.append(physical)
        updated = dict(row)
        # A digest that already binds the canonical bytes is not a changed
        # cell merely because its hexadecimal letter case differs.  Preserve
        # that exact physical/token spelling so the byte-level scope remains
        # strictly limited to genuinely stale hashes.
        updated["ar_sha256"] = new if stale else old
        after_rows.append(updated)
    after = "".join(updated_lines).encode("utf-8")
    parsed_fields, parsed_after_rows = read_csv(after)
    if parsed_fields != fieldnames or parsed_after_rows != after_rows:
        raise RebindError("post-rebind CSV parse differs from the intended rows")
    protected_before = field_digest(fieldnames, rows, {"ar_sha256"})
    protected_after = field_digest(fieldnames, after_rows, {"ar_sha256"})
    fa_fields = {name for name in fieldnames if name.startswith("fa_IR_")}
    fa_before = field_digest(fieldnames, rows, set(fieldnames) - fa_fields)
    fa_after = field_digest(fieldnames, after_rows, set(fieldnames) - fa_fields)
    if protected_before != protected_after or fa_before != fa_after:
        raise RebindError("a protected non-Arabic or Farsi field changed")
    return {
        "before": before,
        "after": after,
        "fieldnames": fieldnames,
        "rows": after_rows,
        "changed": changed,
        "protected_digest": protected_after,
        "fa_digest": fa_after,
        "authority": authority,
        "msa_source_successor": successor,
    }


def receipt_payload(repo: Path, manifest_path: Path, authority_path: Path, result: dict) -> dict:
    payload = {
        "schema": SCHEMA,
        "status": "PASS",
        "scope": "MSA ar_sha256 cells only; all Farsi and non-hash fields preserved",
        "authority": {
            "path": authority_path.relative_to(repo).as_posix(),
            "bytes": authority_path.stat().st_size,
            "sha256": sha256_path(authority_path),
            "schema": result["authority"]["schema"],
            "status": result["authority"]["status"],
            "source_snapshot_sha256": result["authority"]["source_snapshot_sha256"],
        },
        "manifest": {
            "path": manifest_path.relative_to(repo).as_posix(),
            "before_sha256": sha256_bytes(result["before"]),
            "after_sha256": sha256_bytes(result["after"]),
            "after_bytes": len(result["after"]),
            "row_count": len(result["rows"]),
            "changed_ar_sha256_cells": len(result["changed"]),
            "already_current_ar_sha256_cells": len(result["rows"]) - len(result["changed"]),
            "protected_non_ar_sha256_field_digest": result["protected_digest"],
            "farsi_field_digest": result["fa_digest"],
        },
        "changed_rows": result["changed"],
        "invariants": {
            "ordered_unique_olp_0001_0722": True,
            "all_live_msa_hashes_equal_canonical_closure": True,
            "all_live_msa_byte_counts_equal_canonical_closure": True,
            "all_non_ar_sha256_cells_unchanged": True,
            "all_farsi_cells_unchanged": True,
            "physical_csv_lines_preserved_except_exact_hash_tokens": True,
        },
    }
    if result["msa_source_successor"] is not None:
        payload["msa_source_successor"] = result["msa_source_successor"]
        payload["scope"] = "Current MSA ar_sha256 cells; historical closure plus one exact published successor; all Farsi and other cells preserved"
        for kind in ("hashes", "byte_counts"):
            old = f"all_live_msa_{kind}_equal_canonical_closure"
            del payload["invariants"][old]
            payload["invariants"][f"all_live_msa_{kind}_equal_effective_build_authority"] = True
        payload["invariants"]["historical_closure_bytes_not_rewritten"] = True
    return payload


def verify_receipt(repo: Path, manifest_path: Path, authority_path: Path, receipt_path: Path,
                   successor_ledger: Path | None = None) -> dict:
    receipt = load_json(receipt_path)
    result = derive(repo, manifest_path, authority_path, successor_ledger)
    if result["changed"]:
        raise RebindError(f"manifest still has {len(result['changed'])} stale Arabic hashes")
    if receipt.get("schema") != SCHEMA or receipt.get("status") != "PASS":
        raise RebindError("rebind receipt schema/status is not PASS")
    authority = receipt.get("authority") or {}
    manifest = receipt.get("manifest") or {}
    expected = {
        "authority_sha256": sha256_path(authority_path),
        "manifest_after_sha256": sha256_path(manifest_path),
        "manifest_after_bytes": manifest_path.stat().st_size,
        "protected_digest": result["protected_digest"],
        "fa_digest": result["fa_digest"],
    }
    actual = {
        "authority_sha256": str(authority.get("sha256", "")).upper(),
        "manifest_after_sha256": str(manifest.get("after_sha256", "")).upper(),
        "manifest_after_bytes": manifest.get("after_bytes"),
        "protected_digest": str(manifest.get("protected_non_ar_sha256_field_digest", "")).upper(),
        "fa_digest": str(manifest.get("farsi_field_digest", "")).upper(),
    }
    if actual != expected:
        raise RebindError(f"rebind receipt identity mismatch: {actual} != {expected}")
    if receipt.get("msa_source_successor") != result["msa_source_successor"]:
        raise RebindError("rebind receipt does not bind the exact current MSA successor")
    expected_invariants = receipt_payload(repo, manifest_path, authority_path, result)["invariants"]
    if receipt.get("invariants") != expected_invariants:
        raise RebindError("rebind receipt invariant inventory differs from the effective authority")
    if manifest.get("row_count") != 722:
        raise RebindError("rebind receipt row count is not 722")
    if any(value is not True for value in (receipt.get("invariants") or {}).values()):
        raise RebindError("rebind receipt has a non-PASS invariant")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--action", choices=("plan", "write", "verify"), default="verify")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--authority", default=DEFAULT_AUTHORITY)
    parser.add_argument("--receipt", default=DEFAULT_RECEIPT)
    parser.add_argument("--successor-ledger", help="one exact published OLP-0087 MSA correction; historical closure is preserved")
    args = parser.parse_args()
    repo = args.repo.resolve()
    manifest_path = (repo / args.manifest).resolve()
    authority_path = (repo / args.authority).resolve()
    receipt_path = (repo / args.receipt).resolve()
    successor_ledger = (repo / args.successor_ledger).resolve() if args.successor_ledger else None
    try:
        if args.action == "verify":
            receipt = verify_receipt(repo, manifest_path, authority_path, receipt_path, successor_ledger)
            print(json.dumps({"status": "PASS", "action": "verify", "receipt": receipt_path.relative_to(repo).as_posix(), "manifest_sha256": sha256_path(manifest_path)}, sort_keys=True))
            return 0
        result = derive(repo, manifest_path, authority_path, successor_ledger)
        payload = receipt_payload(repo, manifest_path, authority_path, result)
        if args.action == "write":
            if successor_ledger is not None and receipt_path == (repo / DEFAULT_RECEIPT).resolve():
                raise RebindError("new MSA successor needs a new receipt; historical receipt must be preserved")
            manifest_tmp = manifest_path.with_name(manifest_path.name + f".tmp-{os.getpid()}")
            receipt_tmp = receipt_path.with_name(receipt_path.name + f".tmp-{os.getpid()}")
            manifest_tmp.write_bytes(result["after"])
            receipt_tmp.parent.mkdir(parents=True, exist_ok=True)
            receipt_tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            os.replace(manifest_tmp, manifest_path)
            os.replace(receipt_tmp, receipt_path)
            verify_receipt(repo, manifest_path, authority_path, receipt_path, successor_ledger)
        print(json.dumps({"status": "PASS", "action": args.action, "changed": len(result["changed"]), "before_sha256": sha256_bytes(result["before"]), "after_sha256": sha256_bytes(result["after"])}, sort_keys=True))
        return 0
    except RebindError as exc:
        print(json.dumps({"status": "FAIL", "action": args.action, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
