#!/usr/bin/env python3
"""Finite additive admission: three NFC transitions and two marked notes.

No translation, old decision, source baseline, or historical receipt is edited.
The original MP assertions are evaluated on reconstructed historical bytes;
the current bytes are separately pinned.  The two editorial notes are admitted
as new content with their own source-derived proof, not as old reviewed prose.
"""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
from pathlib import Path
import re
import unicodedata

HELPER = "build/five_source_successors_20260909.py"
ROOT = "evidence/classical/repairs/five-source-closure-20260909"
HISTORY = ROOT + "/predecessor"
INVENTORY = HISTORY + "/INVENTORY.json"
INVENTORY_SHA256 = "9e0fca39cde6544604361738071a4c33a21c7e58900ffe49771458ae1b03c49e"
CLOSURE = "evidence/classical/SOURCE_RECONCILIATION_CLOSURE_MANIFEST_20260905.json"
OLD_CLOSURE_SHA256 = "274bdb05f2bbe34ad447cebccb998dc5c3637b714384b45009c69257c4f288e2"
NFC = "evidence/classical/repairs/msa-mp-nfc-20260909/NORMALIZATION_TRANSITIONS.json"
NOTE = "evidence/classical/repairs/olp0014-domain-size-20260909/REPAIR_RECORD.json"
BEFORE = "evidence/classical/repairs/olp0014-domain-size-20260909/BEFORE_SOURCES.json"
RECEIPT = "evidence/classical/repairs/olp0014-domain-size-20260909/RECEIPT.json"
PINS = {
    NFC: "bab1bc85dd51ce07232f0012c822620b9bdd53186b33f0accd45a5c4428beb65",
    NOTE: "48c352e665b1dcf7f7ebfe1900e0ea625b794408d2e18aad81e563d3e4602ea1",
    BEFORE: "e31555b2577a75b86d52022736f655f2c59569325db296c98a50582cf1514f40",
    RECEIPT: "bd5cae1e271b931938cd07ca18c766a95edb77a0df0c76263790e2db85bad82f",
}
NFC_UNITS = ("OLP-0079", "OLP-0093", "OLP-0497")
CHANGED_UNITS = frozenset((*NFC_UNITS, "OLP-0014"))
MARKER = b"% OLP0014-DOMAIN-SIZE-20260909 "
METADATA_SOURCE = "five-exact-source-successors-20260909"
NOTE_FINDING_ID = "OLP0014-DOMAIN-SIZE-20260909-P1"


def require(condition, message):
    if not condition:
        raise ValueError("five-source admission: " + message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def identity(raw):
    return {"sha256": digest(raw), "bytes": len(raw)}


def exact(raw, record):
    return identity(raw) == {k: record[k] for k in ("sha256", "bytes")}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def read_json(repo, path, expected=None):
    p = Path(path)
    require(not p.is_absolute() and ".." not in p.parts, "unscoped path")
    raw = (repo / p).read_bytes()
    if expected:
        require(digest(raw) == expected, "pinned artifact changed: " + path)
    return json.loads(raw, object_pairs_hook=unique_object), {"path": path, **identity(raw)}


def pointer(value, path):
    for part in path.strip("/").split("/"):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def history(repo):
    inventory, inventory_id = read_json(repo, INVENTORY, INVENTORY_SHA256)
    identities = [inventory_id]
    for item in inventory["files"]:
        raw = (repo / item["preserved_path"]).read_bytes()
        require(exact(raw, item), "preserved predecessor bytes changed")
        identities.append({"path": item["preserved_path"], **identity(raw)})
    old, _ = read_json(repo, HISTORY + "/" + Path(CLOSURE).name, OLD_CLOSURE_SHA256)
    require(old["status"] == "PASS" and old["total_units"] == 722 and
            len({r["id"] for r in old["units"]}) == 722, "predecessor is not a full PASS closure")
    return old, identities


def check_nfc(current, row, ledger):
    """Recompute both encoding and older semantic inverse assertions."""
    require(exact(current, row["current"]), "current NFC witness drift")
    p = row["patch"]
    old, new = bytes.fromhex(p["old_utf8_hex"]), bytes.fromhex(p["new_utf8_hex"])
    require(old == bytes.fromhex("D8A7D984D985D982D8AFD991D98ED985") and
            new == bytes.fromhex("D8A7D984D985D982D8AFD98ED991D985"), "not the admitted combining-mark pair")
    start, end = p["byte_start"], p["byte_end_exclusive"]
    require(type(start) is int and type(end) is int and 0 <= start < end and
            end - start == len(new) and current[start:end] == new and
            current.count(new) == 1 and current.count(old) == 0,
            "NFC patch is not its one exact occurrence")
    require(current[:start].count(b"\n") + 1 == p["line"], "NFC line changed")
    require(old.decode() == p["old_text"] and new.decode() == p["new_text"], "NFC literal fields disagree")
    prior = current[:start] + old + current[end:]
    require(exact(prior, row["predecessor"]), "NFC inverse differs from predecessor")
    require(prior[:start] + new + prior[end:] == current, "NFC forward replay differs")
    require(unicodedata.normalize("NFC", prior.decode()) == current.decode() and
            unicodedata.is_normalized("NFC", current.decode()), "not whole-source canonical equivalence")
    loc = pointer(ledger, row["historical_ledger"]["msa_pointer"])
    require(loc["path"] == row["target_path"] and identity(prior) == {
        "sha256": loc["after_sha256"], "bytes": loc["after_bytes"]}, "old MP after identity not preserved")
    chosen, original = ledger["chosen_arabic"].encode(), ledger["before_arabic"].encode()
    require(prior.count(chosen) == 1, "historical MP inverse is ambiguous")
    before_mp = prior.replace(chosen, original, 1)
    require(identity(before_mp) == {"sha256": loc["before_sha256"], "bytes": loc["before_bytes"]},
            "original MP semantic inverse assertion fails")
    return prior


def check_note(current, row, preserved):
    require(exact(current, row), "current note witness drift")
    block = base64.b64decode(row["inserted_block_base64"], validate=True)
    require(block.startswith(MARKER + b"BEGIN\n") and block.endswith(MARKER + b"END\n\n") and
            current.count(MARKER) == 2 and current.count(block) == 1, "note marker/block not unique")
    prior = current.replace(block, b"", 1)
    require(prior == base64.b64decode(preserved["base64"], validate=True) and exact(prior, preserved) and
            identity(prior) == {"sha256": row["before_sha256"], "bytes": row["before_bytes"]},
            "note removal fails exact source restoration")
    lines = current.decode().splitlines()
    note = "\n".join(lines[row["line_start"] - 1:row["line_end"]])
    require(note == row["note_text"] and digest(note.encode()) == row["note_sha256"] and
            note.encode() + b"\n\n" == block, "note range differs")
    original = row["original_paragraph"]
    require("\n".join(lines[original["line_start"] - 1:original["line_end"]]) == original["excerpt"] and
            original["excerpt"].encode() + b"\n\n" + block in current,
            "note is not directly after its unchanged paragraph")
    require(re.findall(r"\$([^$]*)\$", note) == ["A", "A"] and
            "تنبيه توضيحي على الأصل" in note, "unadmitted new mathematics or missing editorial label")
    return prior


def proof_check():
    """Finite edge-case verification supplements, never replaces, the written general proof."""
    results = []
    for n in range(4):
        pairs = [(a, b) for a in range(n) for b in range(n)]
        neither = anti_not_asym = 0
        for mask in range(1 << len(pairs)):
            relation = {pair for i, pair in enumerate(pairs) if mask & (1 << i)}
            reflexive = all((a, a) in relation for a in range(n))
            irreflexive = all((a, a) not in relation for a in range(n))
            antisymmetric = all(a == b or (b, a) not in relation for a, b in relation)
            asymmetric = all((b, a) not in relation for a, b in relation)
            neither += not reflexive and not irreflexive
            anti_not_asym += antisymmetric and not asymmetric
        results.append([n, neither, anti_not_asym])
    require(results == [[0, 0, 0], [1, 0, 1], [2, 8, 9], [3, 384, 189]], "domain-size finite proof check failed")
    return results


def normalize(repo, english_root, checker, baseline):
    old, input_ids = history(repo)
    artifacts = {}
    for path, pin in PINS.items():
        artifacts[path], file_id = read_json(repo, path, pin)
        input_ids.append(file_id)
    nfc, note, before = artifacts[NFC], artifacts[NOTE], artifacts[BEFORE]
    require(nfc["schema"] == "openlogic-msa-nfc-normalization-transition-v1" and
            [r["unit_id"] for r in nfc["transitions"]] == list(NFC_UNITS), "NFC inventory differs")
    require(note["unit_id"] == "OLP-0014" and len(note["source_changes"]) == 2 and
            {r["edition"] for r in note["source_changes"]} == {"msa", "classical"} and
            len(before["files"]) == 2, "note inventory differs")
    ledgers = {}
    for item in nfc["historical_ledgers"]:
        ledgers[item["path"]], file_id = read_json(repo, item["path"], item["sha256"])
        require(file_id["bytes"] == item["bytes"], "old MP ledger size changed")
        input_ids.append(file_id)
    prior_rows = {r["id"]: r for r in old["units"]}
    baseline_rows = {r["id"]: r for r in baseline["units"]}
    preserved = {r["path"]: r for r in before["files"]}
    sources = []
    for index, row in enumerate(nfc["transitions"]):
        current = (repo / row["target_path"]).read_bytes()
        prior = check_nfc(current, row, ledgers[row["historical_ledger"]["path"]])
        sources.append({"unit_id": row["unit_id"], "edition": "msa", "path": row["target_path"],
                        "before": prior, "after": current, "authority_ref": NFC + f"#/transitions/{index}"})
    for index, row in enumerate(note["source_changes"]):
        current = (repo / row["path"]).read_bytes()
        prior = check_note(current, row, preserved[row["path"]])
        sources.append({"unit_id": "OLP-0014", "edition": row["edition"], "path": row["path"],
                        "before": prior, "after": current, "authority_ref": NOTE + f"#/source_changes/{index}"})
    require(len({s["path"] for s in sources}) == 5, "not five distinct source files")
    for source in sources:
        uid, edition = source["unit_id"], source["edition"]
        frozen = baseline_rows[uid]
        field = "arabic_path" if edition == "msa" else "target_path"
        require(source["path"] == frozen[field] == prior_rows[uid][edition]["path"] and
                exact(source["before"], prior_rows[uid][edition]), "predecessor closure binding failed")
        english = (english_root / frozen["source_path"]).read_bytes()
        require(digest(english) == frozen["english_sha256"] == prior_rows[uid]["english_sha256"], "frozen English changed")
        comparison = checker.compare(source["before"].decode(), source["after"].decode()
                                     if uid != "OLP-0014" else source["before"].decode())
        require(not comparison["failures"] and all(comparison["checks"].values()), "unadmitted formal source drift")
    english = note["authority"]["english"]
    raw_english = (english_root / english["source_relative"]).read_bytes()
    require(exact(raw_english, english), "note English authority changed")
    lines = raw_english.decode().splitlines()
    for passage in english["passages"]:
        text = "\n".join(lines[passage["line_start"] - 1:passage["line_end"]])
        require(text == passage["excerpt"] and digest(text.encode()) == passage["excerpt_sha256"], "English proof premise excerpt changed")
    pairs = {}
    for uid in sorted(CHANGED_UNITS):
        by_edition = {s["edition"]: s for s in sources if s["unit_id"] == uid}
        for edition in ("msa", "classical"):
            if edition not in by_edition:
                witness = (repo / prior_rows[uid][edition]["path"]).read_bytes()
                require(exact(witness, prior_rows[uid][edition]), "unchanged counterpart drift")
                by_edition[edition] = {"before": witness, "after": witness}
        before_cmp = checker.compare(by_edition["msa"]["before"].decode(), by_edition["classical"]["before"].decode())
        after_cmp = checker.compare(by_edition["msa"]["after"].decode(), by_edition["classical"]["after"].decode())
        require(checker.formal_comparison_sha256(before_cmp) == prior_rows[uid]["raw_comparison_sha256"] and
                not before_cmp["failures"] and not after_cmp["failures"] and
                all(after_cmp["checks"].values()), "cross-edition formal proof differs")
        if uid != "OLP-0014":
            require(checker.formal_comparison_sha256(before_cmp) == checker.formal_comparison_sha256(after_cmp), "NFC changed formal comparison")
        pairs[uid] = {"before_comparison_sha256": checker.formal_comparison_sha256(before_cmp),
                      "after_comparison_sha256": checker.formal_comparison_sha256(after_cmp)}
    report = {"schema": "openlogic-five-source-successor-admission-v1", "status": "PASS",
              "changed_file_count": 5, "changed_unit_count": 4, "new_formal_waivers": 0,
              "new_integration_finding": {"finding_id": NOTE_FINDING_ID,
                  "repair_id": note["repair_id"], "authority_ref": NOTE,
                  "identity_note": "New source-closure finding key assigned during this integration; not an older review finding."},
              "input_artifacts": input_ids,
              "transitions": [{k: v for k, v in s.items() if k not in ("before", "after")} |
                              {"before": identity(s["before"]), "after": identity(s["after"])} for s in sources],
              "cross_edition_checks": pairs, "finite_domain_checks": proof_check(),
              "general_proof": NOTE + "#/mathematical_analysis",
              "scope": "Exact encoding successors plus two marked source-derived editorial notes; no new claim of whole-work semantic or canon review."}
    return {"sources": sources, "predecessor": old, "report": report}


def rebind_metadata(batch, correction_meta):
    result = copy.deepcopy(correction_meta)
    old_rows = {r["id"]: r for r in batch["predecessor"]["units"]}
    for s in batch["sources"]:
        if s["edition"] != "msa":
            continue
        uid = s["unit_id"]
        old = result.get(uid)
        if uid in NFC_UNITS:
            prior = old_rows[uid]["correction"]
            require(old is not None and all(old[k] == prior[k] for k in ("finding_ids", "rationale", "authority_refs")),
                    "older MP correction reasons changed")
            if old["metadata_source"] != "explicit":
                require(old["seed_current_msa_sha256"] == digest(s["before"]) and
                        old["seed_current_msa_bytes"] == len(s["before"]), "correction seed differs from predecessor")
            rationale = old["rationale"] + " Exact encoding successor (2026-09-09): one NFC combining-mark reorder only. The original MP semantic inverse is checked against reconstructed historical bytes; its finding IDs, reason, and original ledger remain unchanged. No new translation choice or canon attestation is inferred."
        else:
            require(old is None and old_rows[uid]["correction"] is None, "OLP0014 unexpectedly has prior correction metadata")
            old = {"finding_ids": [NOTE_FINDING_ID], "authority_refs": []}
            rationale = "Append a visibly marked explanatory note while retaining every original byte. For a fixed A, a neither-reflexive-nor-irreflexive relation exists exactly when A has two distinct elements; an antisymmetric-but-not-asymmetric relation needs only nonempty A. General necessity/sufficiency proofs and exact consulted-source/choice records are in the new repair record. This is new editorial inference, not an original English sentence or retrospective claim that the old review covered the note."
        result[uid] = {**old, "finding_ids": list(old["finding_ids"]), "rationale": rationale,
                       "authority_refs": list(dict.fromkeys([*old["authority_refs"], s["authority_ref"]])),
                       "metadata_source": METADATA_SOURCE, "seed_current_msa_sha256": digest(s["after"]),
                       "seed_current_msa_bytes": len(s["after"])}
    return result


def validate_closure_rows(batch, rows):
    prior = {r["id"]: r for r in batch["predecessor"]["units"]}
    after_sources = {(s["unit_id"], s["edition"]): s for s in batch["sources"]}
    require(len(rows) == 722 and len({r["id"] for r in rows}) == 722 and
            {r["id"] for r in rows} == set(prior), "722-unit closure inventory differs")
    for row in rows:
        uid = row["id"]
        if uid not in CHANGED_UNITS:
            require(row == prior[uid], "unrelated closure row changed: " + uid)
        else:
            for edition in ("msa", "classical"):
                source = after_sources.get((uid, edition))
                expected = (identity(source["after"]) if source else
                            {k: prior[uid][edition][k] for k in ("sha256", "bytes")})
                require({k: row[edition][k] for k in expected} == expected and
                        row[edition]["path"] == prior[uid][edition]["path"],
                        "current closure successor identity differs: " + uid)
            require(row["source_path"] == prior[uid]["source_path"] and
                    row["english_sha256"] == prior[uid]["english_sha256"] and
                    row["raw_comparison_sha256"] == batch["report"]["cross_edition_checks"][uid]["after_comparison_sha256"],
                    "current closure comparison differs: " + uid)
            require(row["formal_repair"] == prior[uid]["formal_repair"] and
                    row["math_text_declaration"] == prior[uid]["math_text_declaration"] and
                    row["structural_review"] == prior[uid]["structural_review"], "new source change widened a waiver")
            if uid in NFC_UNITS:
                old_correction, current_correction = prior[uid]["correction"], row["correction"]
                require(current_correction["finding_ids"] == old_correction["finding_ids"] and
                        current_correction["rationale"].startswith(old_correction["rationale"]) and
                        all(ref in current_correction["authority_refs"] for ref in old_correction["authority_refs"]) and
                        row["semantic_authority"] == prior[uid]["semantic_authority"],
                        "current closure loses older MP rationale or authority")
            else:
                require(row["correction"]["finding_ids"] == [NOTE_FINDING_ID] and
                        row["semantic_authority"].get("additive_editorial_note_authority") == NOTE + "#/mathematical_analysis" and
                        all(row["semantic_authority"].get(k) == v for k, v in prior[uid]["semantic_authority"].items()),
                        "new note lacks separate authority or rewrites old review")
    return {"unchanged_unrelated_rows": 718, "total_rows": 722, "status": "PASS"}


def capture_predecessor(repo):
    """One-time immutable copy of exact finite central predecessors, never overwrite."""
    require(digest((repo / CLOSURE).read_bytes()) == OLD_CLOSURE_SHA256, "central predecessor already changed")
    names = [
        "BASELINE_CORRECTION_OVERLAY_FULL_20260905.json", "MATH_TEXT_DECLARATIONS_FULL_20260905.json",
        "STRUCTURAL_REVIEW_DECLARATIONS_FULL_20260905.json", "FORMAL_REPAIR_DECLARATIONS_FULL_20260905.json",
        "GENERAL_REVIEW_DECLARATIONS_FULL_20260905.json", "SOURCE_RECONCILIATION_STATIC_VALIDATION_20260905.json",
        Path(CLOSURE).name, "SOURCE_RECONCILIATION_AUDIT_20260905.json",
        "FULL_TRANSLATION_ACCEPTANCE_AUDIT.json", "FULL_TRANSLATION_ACCEPTANCE_AUDIT.md"]
    originals = ["evidence/classical/" + name for name in names] + ["build/finalize_classical_source_reconciliation.py"]
    records = []
    for original in originals:
        target = HISTORY + "/" + Path(original).name
        raw = (repo / original).read_bytes()
        destination = repo / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as stream:
            stream.write(raw)
        require(destination.read_bytes() == raw, "predecessor preservation readback differs")
        records.append({"original_path": original, "preserved_path": target, **identity(raw)})
    raw = (json.dumps({"schema": "openlogic-five-source-predecessor-inventory-v1", "files": records},
                      ensure_ascii=False, indent=2) + "\n").encode()
    with (repo / INVENTORY).open("xb") as stream:
        stream.write(raw)
    return {"path": INVENTORY, **identity(raw), "preserved_files": len(records)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--capture-predecessor", action="store_true")
    args = parser.parse_args()
    require(args.capture_predecessor, "this helper is consumed by the central finalizer; CLI only captures predecessors")
    print(json.dumps(capture_predecessor(args.repo.resolve()), indent=2))
