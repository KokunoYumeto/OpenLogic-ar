#!/usr/bin/env python3
"""Render ten source- and canon-qualified Arabic sense cards."""

from __future__ import annotations

import json
import re
from pathlib import Path

from render_arabic_review_existing_20260927 import INDEX, PINNED_INDEX_SHA, arabic_dominant, decision_card, sha256


ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "evidence/classical/terminology/ARABIC_SENSES_BATCH_76_85_20260927.json"
BASE = ROOT / "expert-review/2026-09-26-final-page-review/arabic-senses-76-85"
PRIOR = [
    "ARABIC_PRIORITY_30_20260926.json",
    "ARABIC_REVIEW_BATCH_31_38_20260927.json",
    "ARABIC_SENSES_BATCH_39_58_20260927.json",
    "ARABIC_SENSES_BATCH_59_75_20260927.json",
]
TITLE_OVERRIDES = {
    "OLP-0704": "قواعد G1c",
    "OLP-0705": "قواعد G1i",
    "OLP-0706": "قواعد G2c",
    "OLP-0709": "قواعد LK",
    "OLP-0711": "في القواعد والاشتقاقات",
}
EASTERN_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def source_links(record: dict, commit: str) -> str:
    parts = []
    for passage in record["source_passages"]:
        path = passage["path"]
        if not path.startswith("content/") or ".." in Path(path).parts:
            raise ValueError("Unexpected English source path")
        ranges = []
        for span in passage["lines"].split(","):
            match = re.fullmatch(r"(\d+)(?:-(\d+))?", span.strip())
            if not match:
                raise ValueError(f"Invalid English line range: {span}")
            first = int(match.group(1))
            last = int(match.group(2) or first)
            if first < 1 or last < first:
                raise ValueError(f"Backwards English line range: {span}")
            fragment = f"#L{first}" + (f"-L{last}" if last != first else "")
            ranges.append(f"[الأسطر {span.strip().translate(EASTERN_DIGITS)}](https://github.com/OpenLogicProject/OpenLogic/blob/{commit}/{path}{fragment})")
        parts.append("، ".join(ranges) + " — " + passage["relevance_ar"])
    return "؛ ".join(parts)


def main() -> None:
    overlay = json.loads(OVERLAY.read_text(encoding="utf-8"))
    if sha256(INDEX) != PINNED_INDEX_SHA or overlay["source_index_sha256"] != PINNED_INDEX_SHA:
        raise ValueError("Pinned review index drift")
    prior_ids = {
        record["decision_id"]
        for name in PRIOR
        for record in json.loads((ROOT / "evidence/classical/terminology" / name).read_text(encoding="utf-8"))["records"]
    }
    records = overlay["records"]
    ids = [record["decision_id"] for record in records]
    if len(ids) != 10 or len(set(ids)) != 10 or set(ids) & prior_ids:
        raise ValueError("Unexpected or previously localized choice inventory")
    decisions = {decision["decision_id"]: decision for decision in json.loads(INDEX.read_text(encoding="utf-8"))["decisions"]}
    totals = {key: 0 for key in ("locations", "resolved", "unresolved", "exact_pages", "fallback_pages")}
    cards = []
    for record in records:
        decision = decisions[record["decision_id"]]
        if not decision["index_metadata"]["human_index_included"]:
            raise ValueError("Choice is excluded from the human index")
        if arabic_dominant(decision.get("sense")) or not all(
            arabic_dominant(decision.get(field)) for field in ("rationale", "expert_question")
        ):
            raise ValueError(f"Unexpected inherited explanation language: {record['decision_id']}")
        if not arabic_dominant(record["sense_ar"]) or not arabic_dominant(record["canon_note_ar"]):
            raise ValueError(f"New Arabic gloss or evidence note missing: {record['decision_id']}")
        localized = dict(decision)
        localized["sense"] = record["sense_ar"]
        card, counts = decision_card(localized, title_overrides=TITLE_OVERRIDES)
        evidence = (
            "**مواضع الأصل الإنجليزي المقابلة لهذا الشرح:** "
            + source_links(record, overlay["english_source_commit"])
            + "\n\n**حدود الشاهد الاصطلاحي:** " + record["canon_note_ar"]
        )
        if card.count("**كل وقوع مسجل لهذا القرار:**") != 1:
            raise ValueError(f"Occurrence heading missing or repeated: {record['decision_id']}")
        card = card.replace("**كل وقوع مسجل لهذا القرار:**", evidence + "\n\n**كل وقوع مسجل لهذا القرار:**", 1)
        cards.append(card)
        for key in totals:
            totals[key] += counts[key]
    BASE.mkdir(parents=True, exist_ok=True)
    readme = BASE / "README.md"
    readme.write_text(
        "# عشرة شروح عربية إضافية للمعاني\n\n"
        "[بطاقات القرارات ومواضعها](CARDS.md)\n\n"
        "عُرّبت شروح المعاني لعشرة اختيارات موروثة من الفهرس المثبّت، وقورنت "
        "بمواضع محددة من الأصل الإنجليزي وبالنص العربي الحالي. لم تُغيَّر ألفاظ "
        "الكتاب ولا التعليلات وأسئلة الخبير الموروثة. في كل بطاقة جميع الوقوعات "
        "المسجلة، وشرح لاحق للمعنى، وإحالات الأصل التي استُعملت، وحدود الشهادة "
        "المعجمية. لا يُدَّعى أن الشرح الجديد كان دافع المترجم الأول؛ وكل قرار "
        "قابل للتصحيح من غير أن يكون ردّ الخبير شرطًا للعمل.\n\n"
        "عُوين مدخل «عدد طبيعي» في معجم مصطلحات الرياضيات (PDF ص ٤٧٧، "
        "المطبوعة ص ٤٦٥)، ومدخل «استقراء رياضي» (PDF ص ٤٤٥، المطبوعة ص ٤٣٣). "
        "المعجم يذكر عدّ الصفر طبيعيًا عند بعضهم؛ أما هذا الكتاب فيعدّه طبيعيًا "
        "قطعًا. واستُعمل مثال الاستقراء في مذكرة رياضيات جامعية من جامعة الملك "
        "سعود (الباب ٢، تعريف ٢.١، PDF ص ٢٦) لشكل الانتقال فقط؛ يبدأ مثالها من ١. "
        "البحث المحدود في نص المعجم الممسوح لم يُثبت أسماء القواعد البرهانية "
        "الأخرى؛ لا يعني ذلك نفي ورودها في المعجم أو غيره.\n\n"
        "صاغ الشروح الجديدة وملاحظات الشواهد وأخرج هذه البطاقات OpenAI Codex — "
        "GPT-6 Sol، بمستوى جهد Ultra. التعليلات والأسئلة العربية الأخرى موروثة "
        "من الفهرس السابق، ولا تُنسب إلى هذه الدفعة.\n\n"
        "هذه الدفعة محلية لم تُنشر بعد. تبلغ التغطية العربية المحلية ٣٥٢ "
        "من ١٠٩٥ اختيارًا؛ ويظل الفهرس العربي المنشور عند ٣٠٥ اختيارات.\n",
        encoding="utf-8", newline="\n",
    )
    cards_file = BASE / "CARDS.md"
    cards_file.write_text(
        "# بطاقات شرح المعاني العربية — القرارات ٧٦–٨٥\n\n"
        "[الرجوع إلى مقدمة الدفعة](README.md)\n\n" + "\n".join(cards),
        encoding="utf-8", newline="\n",
    )
    if cards_file.stat().st_size > 230_000:
        raise ValueError("Review card file exceeds easy-browsing cap")
    receipt = {
        "status": "LOCAL_ARABIC_SENSE_BATCH_76_85_PENDING_INDEPENDENT_READBACK",
        "source_index_sha256": PINNED_INDEX_SHA,
        "overlay_sha256": sha256(OVERLAY),
        "choice_count": len(ids),
        "decision_ids": ids,
        "totals": totals,
        "readme": {"bytes": readme.stat().st_size, "sha256": sha256(readme)},
        "cards": {"bytes": cards_file.stat().st_size, "sha256": sha256(cards_file)},
    }
    (BASE / "BUILD_RECEIPT.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"status": receipt["status"], "choices": len(ids), **totals}, ensure_ascii=True))


if __name__ == "__main__":
    main()
