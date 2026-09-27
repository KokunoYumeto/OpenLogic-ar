#!/usr/bin/env python3
"""Independently read back the three no-unit caption decisions and pinned bytes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

from stream_expert_review_decisions import iter_decisions


ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "expert-review/2026-09-26-final-page-review/global-caption-decisions"
INDEX = ROOT / "tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def main() -> None:
    record_bytes = (DIR / "DECISIONS.json").read_bytes()
    card_bytes = (DIR / "CARDS.md").read_bytes()
    record = json.loads(record_bytes)
    cards = card_bytes.decode("utf-8")
    assert sha(INDEX.read_bytes()) == record["source_index_sha256"]
    ids = {row["decision_id"] for row in record["records"]}
    assert len(ids) == len(record["records"]) == 3
    frozen = {row["decision_id"]: row for row in iter_decisions(INDEX)
              if row["decision_id"] in ids}
    assert ids == set(frozen)
    fetched: dict[str, bytes] = {}
    binding_count = 0
    relocated = 0
    for item in record["records"]:
        old = frozen[item["decision_id"]]
        assert old["chosen_arabic"] == item["chosen_arabic"]
        assert old["english_term"] == item["english_term"]
        assert old["index_metadata"]["occurrence_group_count"] == 0
        assert not old["index_metadata"]["occurrences"]
        assert len(item["bindings"]) == len(old["global_source_bindings"])
        assert item["chosen_arabic"] in cards and item["expert_question_ar"] in cards
        assert item["reader_page_status"] == "not-applicable-global-caption"
        assert sum("\u0600" <= c <= "\u06ff" for c in item["rationale_ar"]) >= 25
        for binding, original in zip(item["bindings"], old["global_source_bindings"]):
            assert binding["path"] == original["logical_path"]
            assert binding["recorded_sha256"] == original["current_sha256"]
            assert binding["recorded_line_start"] == original["line_start"]
            assert binding["recorded_line_end"] == original["line_end"]
            assert binding["excerpt"] == original["current_excerpt"].replace("\r\n", "\n")
            url = ("https://raw.githubusercontent.com/KokunoYumeto/OpenLogic-ar/"
                   + record["pinned_arabic_commit"] + "/" + quote(binding["path"], safe="/"))
            if url not in fetched:
                with urlopen(Request(url, headers={"User-Agent": "OpenLogic-Arabic-review-verify/1"}),
                             timeout=20) as response:
                    fetched[url] = response.read()
            raw = fetched[url]
            assert sha(raw) == binding["pinned_sha256"]
            lines = raw.decode("utf-8").splitlines()
            start, end = binding["pinned_line_start"], binding["pinned_line_end"]
            assert "\n".join(lines[start - 1:end]) == binding["excerpt"]
            assert "\n".join(lines).count(binding["excerpt"]) == 1
            assert binding["source_url"] in cards
            binding_count += 1
            if binding["reconciliation"] != "unchanged":
                assert (binding["pinned_sha256"] != binding["recorded_sha256"]
                        or start != binding["recorded_line_start"]
                        or end != binding["recorded_line_end"])
                relocated += 1
    assert "لا يُختلق رقم صفحة" in cards
    assert "GPT-6 Sol" in cards and "Ultra" in cards
    receipt = {
        "status": "PASS_INDEPENDENT_GLOBAL_CAPTION_READBACK",
        "source_index_sha256": record["source_index_sha256"],
        "pinned_arabic_commit": record["pinned_arabic_commit"],
        "decisions": 3, "bindings_http_verified": binding_count,
        "distinct_files_http_verified": len(fetched),
        "recorded_bindings_relocated": relocated,
        "decisions_json_sha256": sha(record_bytes),
        "cards_md_sha256": sha(card_bytes),
    }
    (DIR / "INDEPENDENT_READBACK.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, ensure_ascii=True))


if __name__ == "__main__":
    main()
