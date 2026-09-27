#!/usr/bin/env python3
"""Render the three no-unit Arabic locale decisions without inventing pages."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

from stream_expert_review_decisions import iter_decisions


ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "evidence/classical/terminology/GLOBAL_CAPTION_REVIEW_NOTES_20260927.json"
DEST = ROOT / "expert-review/2026-09-26-final-page-review/global-caption-decisions"
EAST = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def main() -> None:
    notes = json.loads(NOTES.read_text(encoding="utf-8"))
    source_path = ROOT / notes["source_index_path"]
    assert digest(source_path.read_bytes()) == notes["source_index_sha256"]
    wanted = {row["decision_id"]: row for row in notes["records"]}
    decisions = {row["decision_id"]: row for row in iter_decisions(source_path)
                 if row["decision_id"] in wanted}
    assert len(wanted) == len(decisions) == 3
    source_cache: dict[str, tuple[bytes, list[str]]] = {}
    records = []
    cards = [
        "# قرارات تعليقات الواجهة العامة — بلا موضع صفحة مختلق\n",
        "[الرجوع إلى الفهرس العربي الكامل](../WORKING_INDEX_AR.md)\n",
        "هذه القرارات الثلاثة تخص تعليقات عامة ومادة صدرية، لا وحدة من وحدات متن الكتاب. "
        "لذلك يرد موضع ملف المصدر وسطره المثبت، ولا يُختلق رقم صفحة قارئ أو سطر إنجليزي لم يُسجّل.\n",
    ]
    for index, item in enumerate(notes["records"], 1):
        decision = decisions[item["decision_id"]]
        assert not decision["index_metadata"]["occurrences"]
        assert decision["chosen_arabic"] == decision["review_display"]["chosen_arabic"]
        assert decision["expert_source_binding"]["disposition"] == "global-source-only"
        bound = []
        for location in decision["global_source_bindings"]:
            assert location["human_review_included"]
            path = location["logical_path"]
            if path not in source_cache:
                url = ("https://raw.githubusercontent.com/KokunoYumeto/OpenLogic-ar/"
                       + notes["arabic_source_commit"] + "/" + quote(path, safe="/"))
                with urlopen(Request(url, headers={"User-Agent": "OpenLogic-Arabic-review/1"}),
                             timeout=20) as response:
                    raw = response.read()
                source_cache[path] = raw, raw.decode("utf-8").splitlines()
            raw, lines = source_cache[path]
            needle = location["current_excerpt"].replace("\r\n", "\n")
            body = "\n".join(lines)
            if body.count(needle) != 1:
                raise ValueError(f"Global witness absent/ambiguous: {item['decision_id']} {path}")
            offset = body.index(needle)
            start = body[:offset].count("\n") + 1
            end = start + needle.count("\n")
            if "\n".join(lines[start - 1:end]) != needle:
                raise ValueError("Global witness is not an entire line range")
            blob = ("https://github.com/KokunoYumeto/OpenLogic-ar/blob/"
                    + notes["arabic_source_commit"] + "/" + quote(path, safe="/")
                    + f"#L{start}" + (f"-L{end}" if end != start else ""))
            bound.append({
                "path": path, "pinned_commit": notes["arabic_source_commit"],
                "pinned_sha256": digest(raw), "pinned_line_start": start,
                "pinned_line_end": end, "excerpt": needle, "source_url": blob,
                "recorded_sha256": location["current_sha256"],
                "recorded_line_start": location["line_start"],
                "recorded_line_end": location["line_end"],
                "reconciliation": ("unchanged" if digest(raw) == location["current_sha256"]
                                   and start == location["line_start"]
                                   and end == location["line_end"]
                                   else "exact-excerpt-relocated-in-pinned-source"),
            })
        record = {"decision_id": item["decision_id"],
                  "english_term": decision["english_term"],
                  "chosen_arabic": decision["chosen_arabic"],
                  "sense_ar": item["sense_ar"], "rationale_ar": item["rationale_ar"],
                  "expert_question_ar": item["expert_question_ar"],
                  "alternatives_ar": item["alternatives_ar"],
                  "original_location_count": 0, "reader_page_status": "not-applicable-global-caption",
                  "bindings": bound}
        if item.get("external_source_url"):
            record["external_source_url"] = item["external_source_url"]
            record["external_source_relevance_ar"] = item["external_source_relevance_ar"]
        records.append(record)
        cards.extend([
            f"## {str(index).translate(EAST)}. {decision['chosen_arabic']}\n",
            f"- الأصل الإنجليزي: `{decision['english_term']}`.",
            f"- المقصود: {item['sense_ar']}",
            f"- سبب الاختيار وحدّه: {item['rationale_ar']}",
            "- بدائل للمقارنة: " + "؛ ".join(item["alternatives_ar"]) + ".",
            f"- سؤال للمراجع: {item['expert_question_ar']}",
            "- المواضع: " + "؛ ".join(
                f"[{binding['path']}، السطر {str(binding['pinned_line_start']).translate(EAST)}]"
                f"({binding['source_url']})"
                + ("؛ نُقل الموضع بعد تغير الملف مع بقاء العبارة نفسها"
                   if binding["reconciliation"] != "unchanged" else "")
                for binding in bound) + ".",
            "- صفحة في متن الكتاب: لا تنطبق؛ هذا تعليق عام، ولم يسجل المؤشر وقوعًا في وحدة محتوى.",
        ])
        if item.get("external_source_url"):
            cards.append("- [شاهد الجهة الناشرة للرخصة]("
                         + item["external_source_url"] + "): "
                         + item["external_source_relevance_ar"])
        cards.append("")
    DEST.mkdir(parents=True, exist_ok=True)
    payload = {"schema": "openlogic-arabic-global-caption-review-v1",
               "source_index_sha256": notes["source_index_sha256"],
               "pinned_arabic_commit": notes["arabic_source_commit"],
               "records": records}
    (DEST / "DECISIONS.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    cards.append("صاغ هذه المراجعة اللاحقة OpenAI Codex — GPT-6 Sol، بمستوى جهد Ultra. "
                 "لم تقع مراجعة بشرية؛ كل اختيار قابل للتصحيح.\n")
    (DEST / "CARDS.md").write_text("\n".join(cards), encoding="utf-8", newline="\n")
    print(json.dumps({"decisions": len(records), "bindings": sum(len(r["bindings"]) for r in records)},
                     ensure_ascii=True))


if __name__ == "__main__":
    main()
