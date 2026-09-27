#!/usr/bin/env python3
"""Render the next 17 Arabic sense glosses with every inherited occurrence."""

from __future__ import annotations

import json
from pathlib import Path

from render_arabic_review_existing_20260927 import (
    INDEX,
    PINNED_INDEX_SHA,
    arabic_dominant,
    decision_card,
    sha256,
)


ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "evidence/classical/terminology/ARABIC_SENSES_BATCH_59_75_20260927.json"
LOCATORS = ROOT / "evidence/classical/terminology/ENGLISH_LOCATOR_12_20260927.json"
BASE = ROOT / "expert-review/2026-09-26-final-page-review/arabic-senses-59-75"
PRIOR = [
    ROOT / "evidence/classical/terminology/ARABIC_PRIORITY_30_20260926.json",
    ROOT / "evidence/classical/terminology/ARABIC_REVIEW_BATCH_31_38_20260927.json",
    ROOT / "evidence/classical/terminology/ARABIC_SENSES_BATCH_39_58_20260927.json",
]
TITLE_OVERRIDES = {
    "OLP-0710": "قواعد mG3i",
    "OLP-0711": "في القواعد والاشتقاقات",
}


def main() -> None:
    overlay = json.loads(OVERLAY.read_text(encoding="utf-8"))
    locator_overlay = json.loads(LOCATORS.read_text(encoding="utf-8"))
    if sha256(INDEX) != PINNED_INDEX_SHA or overlay["source_index_sha256"] != PINNED_INDEX_SHA:
        raise ValueError("Pinned source index changed")
    if locator_overlay["source_index_sha256"] != PINNED_INDEX_SHA:
        raise ValueError("English locator supplement points to another index")
    locators_by_decision = {}
    for item in locator_overlay["records"]:
        decision_id = item["english_location_id"].rsplit(":occ", 1)[0]
        locators_by_decision.setdefault(decision_id, []).append(item)
    if len(locator_overlay["records"]) != 12:
        raise ValueError("Unexpected English locator supplement census")
    records = overlay["records"]
    ids = [record["decision_id"] for record in records]
    prior_ids = {
        record["decision_id"]
        for path in PRIOR
        for record in json.loads(path.read_text(encoding="utf-8"))["records"]
    }
    if len(ids) != 17 or len(set(ids)) != 17 or set(ids) & prior_ids:
        raise ValueError("Unexpected count, duplicate or previously localized choice")
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    by_id = {decision["decision_id"]: decision for decision in index["decisions"]}
    totals = {"locations": 0, "resolved": 0, "unresolved": 0, "exact_pages": 0, "fallback_pages": 0}
    unavailable = 0
    cards = []
    for record in records:
        decision = by_id[record["decision_id"]]
        if not decision["index_metadata"]["human_index_included"] or arabic_dominant(decision.get("sense")):
            raise ValueError(f"Unexpected inherited choice status: {record['decision_id']}")
        rationale = record.get("rationale_ar", decision.get("rationale"))
        if not arabic_dominant(rationale) or not arabic_dominant(decision.get("expert_question")):
            raise ValueError(f"Inherited explanation is not Arabic: {record['decision_id']}")
        if not arabic_dominant(record["sense_ar"]):
            raise ValueError(f"Localized sense is not Arabic: {record['decision_id']}")
        localized = dict(decision)
        localized["sense"] = record["sense_ar"]
        localized["rationale"] = rationale
        card, counts = decision_card(localized, title_overrides=TITLE_OVERRIDES)
        for locator in locators_by_decision.get(record["decision_id"], []):
            source = (
                "https://github.com/OpenLogicProject/OpenLogic/blob/"
                + locator_overlay["source_commit"] + "/" + locator["source_path"]
            )
            card += f"\n**أسطر الأصل الإنجليزي في {locator['unit_id']}:** "
            card += "؛ ".join(
                f"[{line['role_ar']}، السطر {str(line['line']).translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'))}]"
                f"({source}#L{line['line']})"
                + (" (سياق للمقارنة، لا لفظ مطابق)" if line["kind"] == "context_only" else "")
                for line in locator["lines"]
            )
            card += ". " + locator["relation_ar"] + "\n"
            if locator.get("expert_question_ar"):
                card += "\n**سؤال إضافي عن محاذاة الأصل:** " + locator["expert_question_ar"] + "\n"
        cards.append(card)
        for key in totals:
            totals[key] += counts[key]
        unavailable += sum(
            page["method"] == "unavailable"
            for group in decision["index_metadata"]["occurrences"]
            for location in group["locations"] if location.get("human_review_included")
            for page in location["page_evidence"]
        )
    BASE.mkdir(parents=True, exist_ok=True)
    readme = BASE / "README.md"
    readme.write_text(
        "# سبعة عشر شرحًا عربيًا آخر للمعاني ومواضعها\n\n"
        "[قراءة بطاقات القرارات والوقوعات](CARDS.md)\n\n"
        "عُرِّبت هنا شروح المعاني الإنجليزية لسبعة عشر اختيارًا آخر من السجل المثبَّت. "
        "بقيت ألفاظ الكتاب وأسئلة المراجعة العربية الموروثة على حالها؛ وعُرِّب أيضًا "
        "تعليل «لمّة الصدق» الذي كان يخلط العربية بالإنجليزية. "
        "هذا تعريب لاحق لواجهة المراجعة، لا توثيق لدافع المترجم الأول ولا اعتماد معجمي "
        "جديد للمصطلحات التي لم يفحصها السجل في المعاجم الرسمية. في كل بطاقة "
        "جميع الوقوعات المسجلة وروابط الأسطر والصفحات المتاحة، مع وسم ما لم يثبت. "
        "الاختيارات كلها مفتوحة للتصحيح.\n\n"
        "ألحقت باثنتي عشرة إحالة إلى الأصل الإنجليزي أسطرٌ محققة من تسعة ملفات "
        "مثبتة؛ ٢١ رابطًا لموضع لفظ أو معنى مباشر، وأربعة روابط لسياق المقارنة وحده. "
        "فالتعريفان العربيان للدالة n-موضعية يعممان تعريفين أحاديين في الأصل، "
        "لكن الأصل يستعمل بعدهما دالة بناء صيغ ثنائية. لهذا أُبقي التعميم "
        "مؤقتًا بوصفه توسعة تحريرية معلنة، ولا يُنسب لفظ n-ary إلى الأصل الإنجليزي. "
        "سُجل لذلك سؤال مراجعة رياضية "
        "صريح، من غير تعديل المتن أو تخمين موضع واحد للوقوعات العديدة.\n\n"
        "صاغ تعريب شروح المعاني وتعليل «لمّة الصدق» وإخراج هذه البطاقات "
        "OpenAI Codex — GPT-6 Sol، "
        "بمستوى جهد Ultra. وما عدا تعليل «لمّة الصدق» الجديد هنا، فالتعليلات "
        "والأسئلة العربية المعروضة موروثة من السجل السابق؛ يُراجع أصلها ونسبها فيه.\n\n"
        "هذه الدفعة محلية لم تُنشر بعد. الفهرس العربي المنشور ما زال يضم ٣٠٥ "
        "من ١٠٩٥ اختيارًا، وتبلغ التغطية العربية المحلية بعد هذه الدفعة ٣٤٢ اختيارًا.\n",
        encoding="utf-8", newline="\n",
    )
    cards_file = BASE / "CARDS.md"
    cards_file.write_text(
        "# بطاقات شرح المعاني العربية — القرارات ٥٩–٧٥\n\n"
        "[الرجوع إلى مقدمة الدفعة](README.md)\n\n" + "\n".join(cards),
        encoding="utf-8", newline="\n",
    )
    if cards_file.stat().st_size > 230_000:
        raise ValueError("Review card file exceeds easy-browsing cap")
    receipt = {
        "status": "LOCAL_ARABIC_SENSE_BATCH_RENDERED_PENDING_INDEPENDENT_READBACK",
        "source_index_sha256": PINNED_INDEX_SHA,
        "overlay_sha256": sha256(OVERLAY),
        "english_locator_sha256": sha256(LOCATORS),
        "english_locator_locations": len(locator_overlay["records"]),
        "english_locator_direct_lines": sum(line["kind"] == "direct" for item in locator_overlay["records"] for line in item["lines"]),
        "english_locator_context_lines": sum(line["kind"] == "context_only" for item in locator_overlay["records"] for line in item["lines"]),
        "choice_count": len(ids),
        "decision_ids": ids,
        "totals": totals,
        "unavailable_page_records": unavailable,
        "readme": {"bytes": readme.stat().st_size, "sha256": sha256(readme)},
        "cards": {"bytes": cards_file.stat().st_size, "sha256": sha256(cards_file)},
    }
    (BASE / "BUILD_RECEIPT.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"status": receipt["status"], "choices": len(ids), **totals, "unavailable_page_records": unavailable}, ensure_ascii=False))


if __name__ == "__main__":
    main()
