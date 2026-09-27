#!/usr/bin/env python3
"""Render a bounded, Arabic-readable sense-localization batch with all locators."""

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
OVERLAY = ROOT / "evidence/classical/terminology/ARABIC_SENSES_BATCH_39_58_20260927.json"
LOCATORS = ROOT / "evidence/classical/terminology/ENGLISH_LOCATOR_8_20260927.json"
BASE = ROOT / "expert-review/2026-09-26-final-page-review/arabic-senses-39-58"


def main() -> None:
    overlay = json.loads(OVERLAY.read_text(encoding="utf-8"))
    locator_overlay = json.loads(LOCATORS.read_text(encoding="utf-8"))
    if sha256(INDEX) != PINNED_INDEX_SHA or overlay["source_index_sha256"] != PINNED_INDEX_SHA:
        raise ValueError("Pinned review index changed")
    if locator_overlay["source_index_sha256"] != PINNED_INDEX_SHA:
        raise ValueError("Locator supplement points to another index")
    locator_by_id = {item["decision_id"]: item for item in locator_overlay["records"]}
    if len(locator_by_id) != 8:
        raise ValueError("Unexpected English locator supplement inventory")
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    by_id = {decision["decision_id"]: decision for decision in index["decisions"]}
    records = overlay["records"]
    ids = [record["decision_id"] for record in records]
    if len(ids) != 20 or len(set(ids)) != 20:
        raise ValueError("Expected 20 distinct choices")
    totals = {"locations": 0, "resolved": 0, "unresolved": 0, "exact_pages": 0, "fallback_pages": 0}
    cards = []
    for record in records:
        decision = by_id[record["decision_id"]]
        if not decision["index_metadata"]["human_index_included"]:
            raise ValueError(f"Not a human-review choice: {record['decision_id']}")
        if arabic_dominant(decision.get("sense")) or not all(
            arabic_dominant(decision.get(field)) for field in ("rationale", "expert_question")
        ):
            raise ValueError(f"Unexpected inherited field language: {record['decision_id']}")
        if not arabic_dominant(record["sense_ar"]):
            raise ValueError(f"Non-Arabic sense gloss: {record['decision_id']}")
        localized = dict(decision)
        localized["sense"] = record["sense_ar"]
        card, counts = decision_card(localized)
        if record["decision_id"] in locator_by_id:
            locator = locator_by_id[record["decision_id"]]
            source = (
                "https://github.com/OpenLogicProject/OpenLogic/blob/"
                + locator_overlay["source_commit"] + "/" + locator["source_path"]
            )
            card += "\n**أسطر الأصل الإنجليزي المعثور عليها بعد الفهرسة:** "
            card += "؛ ".join(
                f"[{line['role_ar']}، السطر {str(line['line']).translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'))}]"
                f"({source}#L{line['line']})"
                for line in locator["lines"]
            )
            card += ". " + locator["alignment_ar"] + "\n"
        cards.append(card)
        for key in totals:
            totals[key] += counts[key]
    BASE.mkdir(parents=True, exist_ok=True)
    start = BASE / "README.md"
    start.write_text(
        "# عشرون شرحًا عربيًا للمعاني مع مواضعها\n\n"
        "[بطاقات القرارات والوقوعات](CARDS.md)\n\n"
        "عُرِّبت في هذه الدفعة شروح المعنى الإنجليزية لعشرين قرارًا إضافيًا من السجل المثبَّت. "
        "بقيت ألفاظ الكتاب والتعليلات وأسئلة المراجعة العربية الموروثة على حالها. "
        "هذه صياغة لاحقة لمواد المراجعة، لا ادعاء بأن المترجم الأول قد علَّل اختياره بها، "
        "ولا إثبات معجمي جديد للمصطلحات التي سجل الفهرس أنها لم تُفحَص في المعاجم الرسمية. "
        "ترد في البطاقات جميع الوقوعات المسجلة، مع تمييز السطر غير المثبت وصفحة بدء الوحدة "
        "من صفحة اللفظ المحددة. كل اختيار قابل للتصحيح.\n\n"
        "أُلحقت بثماني بطاقات إحالات مدقَّقة إلى أسطر الأصل الإنجليزي: ثلاثة مواضع "
        "ذات وقوع واحد وخمسة سجلات تجمع وقوعات متعددة. تظل خانة الفهرس الخام "
        "المجمَّعة غير محلولة حتى يُفصل كل وقوع فيها؛ فلا نعرض سطرًا واحدًا "
        "مخمنًا بدل الوقوعات العديدة.\n\n"
        "صاغ تعريب شروح المعاني الجديدة وتعيين أسطر الأصل وإخراج هذه البطاقات "
        "OpenAI Codex — GPT-6 Sol، "
        "بمستوى جهد Ultra. والتعليلات والأسئلة العربية الموروثة من السجل السابق "
        "ليست من تأليف هذه الدفعة؛ يُراجع أصلها ونسبها في السجل المثبَّت.\n\n"
        "هذه الدفعة محلية ولم تُنشر بعد. القائمة العامة المنشورة تضم ٣٠٥ من ١٠٩٥ قرارًا؛ "
        "وتبلغ التغطية العربية المحلية ٣٢٥ قرارًا بعد هذه الدفعة، ولا تزال القائمة الكاملة قيد العمل.\n",
        encoding="utf-8",
        newline="\n",
    )
    cards_file = BASE / "CARDS.md"
    cards_file.write_text(
        "# بطاقات شرح المعاني العربية — القرارات ٣٩–٥٨\n\n"
        "[الرجوع إلى مقدمة الدفعة](README.md)\n\n"
        + "\n".join(cards),
        encoding="utf-8",
        newline="\n",
    )
    if cards_file.stat().st_size > 230_000:
        raise ValueError("Review card file exceeds easy-browsing cap")
    receipt = {
        "status": "LOCAL_ARABIC_SENSE_BATCH_RENDERED_PENDING_INDEPENDENT_READBACK",
        "source_index_sha256": PINNED_INDEX_SHA,
        "overlay_sha256": sha256(OVERLAY),
        "english_locator_sha256": sha256(LOCATORS),
        "english_locator_decisions": len(locator_by_id),
        "english_locator_lines": sum(len(item["lines"]) for item in locator_by_id.values()),
        "choice_count": len(ids),
        "decision_ids": ids,
        "totals": totals,
        "readme": {"bytes": start.stat().st_size, "sha256": sha256(start)},
        "cards": {"bytes": cards_file.stat().st_size, "sha256": sha256(cards_file)},
    }
    (BASE / "BUILD_RECEIPT.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"status": receipt["status"], "choices": len(ids), **totals}, ensure_ascii=False))


if __name__ == "__main__":
    main()
