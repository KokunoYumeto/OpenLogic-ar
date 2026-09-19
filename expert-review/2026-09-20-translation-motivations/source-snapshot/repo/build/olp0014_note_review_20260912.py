"""Finite admission of six source-clarification choices; no source mutation."""
from __future__ import annotations

import base64
import copy
import hashlib
import json
from pathlib import Path


LEDGER_PATH = "evidence/classical/repairs/olp0014-domain-size-20260909/REPAIR_RECORD.json"
LEDGER_SHA256 = "48c352e665b1dcf7f7ebfe1900e0ea625b794408d2e18aad81e563d3e4602ea1"
BEFORE_PATH = "evidence/classical/repairs/olp0014-domain-size-20260909/BEFORE_SOURCES.json"
BEFORE_SHA256 = "e31555b2577a75b86d52022736f655f2c59569325db296c98a50582cf1514f40"
PREFIX = "olp0014-domain-size-20260909:"
FAMILIES = ("fixed-domain-scope", "two-elements-iff", "separate-antisymmetry-condition")
LOCATOR_STATUS = "source-clarification-exact-note-verified"


def require(condition, message):
    if not condition:
        raise ValueError("OLP0014 note admission: " + message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def normalize(repo, english_root, payload, identity):
    """Admit the pinned complete record, with exact history and active witnesses."""
    require(english_root is not None, "English source root missing")
    hashes = {}

    def checked(root, declaration):
        path = (root / declaration["path"]).resolve()
        require(path.stat().st_size == declaration["bytes"], "input byte count changed: " + declaration["path"])
        if path in hashes:
            actual = hashes[path].lower()
        else:
            with path.open("rb") as stream:
                actual = hashlib.file_digest(stream, "sha256").hexdigest()
        require(actual == declaration["sha256"].lower(), "input hash changed: " + declaration["path"])
        hashes[path] = actual.upper()
        return path

    require(identity["path"] == LEDGER_PATH and identity["sha256"].lower() == LEDGER_SHA256,
            "uncommissioned ledger identity")
    ledger_raw = checked(repo, identity).read_bytes()
    require(json.loads(ledger_raw) == payload, "supplied payload differs from pinned ledger")
    before_path = repo / BEFORE_PATH
    before_raw = before_path.read_bytes()
    require(digest(before_raw) == BEFORE_SHA256, "preserved predecessor receipt changed")
    before = json.loads(before_raw)
    hashes[before_path.resolve()] = BEFORE_SHA256.upper()
    originals = {entry["path"]: base64.b64decode(entry["base64"], validate=True) for entry in before["files"]}
    require(payload["schema"] == "openlogic-ar-source-clarification-record-v1"
            and payload["repair_id"] == "olp0014-domain-size-20260909"
            and payload["human_review_gate"] is False, "clarification provenance changed")
    sources = {}
    for change in payload["source_changes"]:
        raw = checked(repo, change).read_bytes()
        block = base64.b64decode(change["inserted_block_base64"], validate=True)
        require(raw.count(block) == 1, "additive note missing or repeated")
        restored = raw.replace(block, b"", 1)
        require(restored == originals[change["path"]]
                and digest(restored) == change["before_sha256"]
                and len(restored) == change["before_bytes"], "exact note inverse failed")
        lines = raw.decode("utf-8").splitlines()
        note = "\n".join(lines[change["line_start"] - 1:change["line_end"]])
        require(note == change["note_text"] and digest(note.encode()) == change["note_sha256"],
                "marked note excerpt changed")
        sources[change["edition"]] = (change, lines)
    require(set(sources) == {"msa", "classical"} and len(originals) == 2, "source inventory differs")
    english = payload["authority"]["english"]
    english_path = checked(english_root, {**english, "path": english["source_relative"]})
    english_lines = english_path.read_text(encoding="utf-8").splitlines()
    for passage in english["passages"]:
        excerpt = "\n".join(english_lines[passage["line_start"] - 1:passage["line_end"]])
        require(excerpt == passage["excerpt"] and digest(excerpt.encode()) == passage["excerpt_sha256"],
                "English definition context changed")
    for evidence in payload["authority"]["canon_checks"]:
        checked(repo, evidence["source"])
        checked(repo, evidence["page_image"])
    rows = payload["terminology_decisions"]
    expected = {PREFIX + edition + ":" + family for edition in sources for family in FAMILIES}
    require(len(rows) == 6 and {row["decision_id"] for row in rows} == expected, "six-decision inventory differs")
    normalized = []
    for row in rows:
        require(row["official_attestation_claimed"] is False and row["open_to_correction"] is True
                and row["expert_review_useful"] is True and bool(row["expert_question"]),
                "provisional choice provenance changed")
        require(row["authority_checks"] == payload["authority"]["canon_checks"], "consulted canon differs")
        require(len(row["occurrences"]) == 1, "unexpected note occurrence count")
        occurrence = row["occurrences"][0]
        change, lines = sources[row["edition"]]
        excerpt = "\n".join(lines[occurrence["line_start"] - 1:occurrence["line_end"]])
        require(occurrence["source_kind"] == row["edition"] and occurrence["unit_id"] == "OLP-0014"
                and occurrence["path"] == change["path"] and occurrence["sha256"] == change["sha256"]
                and occurrence["excerpt"] == excerpt and row["chosen_arabic"] in excerpt,
                "current note occurrence changed")
        record = copy.deepcopy(row)
        record["occurrences"] = [{"unit_id": "OLP-0014", row["edition"]: {
            "path": occurrence["path"], "sha256": occurrence["sha256"].upper(),
            "locator_status": LOCATOR_STATUS, "locators": [{
                "line_start": occurrence["line_start"], "line_end": occurrence["line_end"],
                "excerpt": excerpt, "ledger_locator_status": LOCATOR_STATUS}]}}]
        record["source_clarification"] = {
            "ledger_path": LEDGER_PATH, "ledger_sha256": LEDGER_SHA256.upper(),
            "source_ledger": copy.deepcopy(payload), "choice_record": copy.deepcopy(row),
            "historical_before_sources": copy.deepcopy(before)}
        normalized.append(record)
    identity["adapter"] = {"kind": "source-clarification-olp0014-domain-size-v1", "terminology_rows_contributed": 6}
    return normalized, hashes
