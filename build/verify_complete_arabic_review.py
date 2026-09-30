#!/usr/bin/env python3
"""Independently verify the final Arabic human index against the frozen ledger."""

from __future__ import annotations

import gzip
import argparse
import hashlib
import json
from pathlib import Path

from stream_expert_review_decisions import iter_decisions


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "expert-review/2026-09-26-final-page-review"
FROZEN = ROOT / "tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json"
FROZEN_SHA = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main(output_path: Path | None = None) -> None:
    assert sha(FROZEN) == FROZEN_SHA
    frozen = {d["decision_id"]: d for d in iter_decisions(FROZEN)
              if d["index_metadata"]["human_index_included"]}
    excluded = sum(1 for d in iter_decisions(FROZEN)
                   if not d["index_metadata"]["human_index_included"])
    assert len(frozen) == 1095 and excluded == 84
    receipt = json.loads((BASE / "COMPLETE_DIRECTORY_RECEIPT.json").read_text(encoding="utf-8"))
    directory = BASE / receipt["directory"]["path"]
    machine = BASE / receipt["machine_record"]["path"]
    assert directory.stat().st_size == receipt["directory"]["bytes"]
    assert machine.stat().st_size == receipt["machine_record"]["bytes"]
    assert sha(directory) == receipt["directory"]["sha256"]
    assert sha(machine) == receipt["machine_record"]["sha256"]
    status = json.loads((BASE / "PUBLICATION_STATUS_READBACK.json").read_text(encoding="utf-8"))
    assert status["status"] == "PASS_STATUS_ONLY_FINALIZATION"
    assert status["count"] == len(status["changed_files"]) == 44
    for change in status["changed_files"]:
        path = ROOT / change["path"]
        assert sha(path) == change["final_sha256"]
        content = path.read_text(encoding="utf-8")
        assert "لم تُنشر بعد" not in content
        assert "ما زالت قيد التحرير" not in content
    lines = directory.read_text(encoding="utf-8").splitlines()
    assert "١٠٩٥ من ١٠٩٥" in lines[0]
    rows = [line for line in lines if line.startswith("| ") and line.endswith(" |")]
    assert len(rows) == 1096  # header and one row for every reviewable decision
    seen = set()
    with gzip.open(machine, "rt", encoding="utf-8") as source:
        records = [json.loads(line) for line in source]
    assert len(records) == 1095
    for record, row in zip(records, rows[1:], strict=True):
        identifier = record["decision_id"]
        assert identifier in frozen and identifier not in seen, identifier
        seen.add(identifier)
        prior = frozen[identifier]
        assert record["english_term"] == prior["english_term"]
        assert record["original_occurrences"] == prior["index_metadata"]["occurrences"]
        assert record["global_source_bindings"] == prior.get("global_source_bindings", [])
        assert record["open_to_correction"] is True
        for key in ("sense_ar", "rationale_ar", "expert_question_ar"):
            value = record[key]
            assert len(value.strip()) >= 20
            assert sum("\u0600" <= char <= "\u06ff" for char in value) >= 12
        card = BASE / record["review_card"]
        assert card.is_file(), card
        card_text = card.read_text(encoding="utf-8")
        if record["review_card"].startswith("global-caption-decisions/"):
            assert record["english_term"] in card_text, identifier
        else:
            assert identifier in card_text, identifier
        assert f"]({record['review_card']})" in row, identifier
        assert record["english_term"].replace("|", "\\|")[:30] in row, identifier
    assert seen == set(frozen)
    result = {
        "status": "PASS_COMPLETE_LOCAL_ARABIC_REVIEW",
        "frozen_index_sha256": FROZEN_SHA,
        "frozen_total": len(frozen) + excluded,
        "reviewable_decisions": len(frozen),
        "excluded_machine_only_records": excluded,
        "verified_directory_rows": len(rows) - 1,
        "verified_machine_records": len(records),
        "directory_sha256": sha(directory),
        "machine_record_sha256": sha(machine),
        "all_reviewable_ids_exactly_once": True,
        "all_frozen_occurrences_preserved": True,
        "all_card_files_and_id_bindings_exist": True,
        "scope": "Structural IDs, bytes, Arabic fields and inherited occurrence bindings only; not semantic or canon approval of every explanation.",
    }
    if output_path is not None:
        with output_path.open("x", encoding="utf-8", newline="\n") as destination:
            destination.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Fresh receipt path; historical receipts are never overwritten")
    main(parser.parse_args().output)
