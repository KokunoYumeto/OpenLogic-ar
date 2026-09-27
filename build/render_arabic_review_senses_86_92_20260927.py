#!/usr/bin/env python3
"""Render seven source-qualified Arabic meaning cards in two readable files."""

from __future__ import annotations

import json
from pathlib import Path

from render_arabic_review_existing_20260927 import (
    INDEX, PINNED_INDEX_SHA, arabic_dominant, decision_card, sha256,
)
from render_arabic_review_senses_76_85_20260927 import source_links


ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "evidence/classical/terminology/ARABIC_SENSES_BATCH_86_92_20260927.json"
BASE = ROOT / "expert-review/2026-09-26-final-page-review/arabic-senses-86-92"
PRIOR = (
    "ARABIC_PRIORITY_30_20260926.json",
    "ARABIC_REVIEW_BATCH_31_38_20260927.json",
    "ARABIC_SENSES_BATCH_39_58_20260927.json",
    "ARABIC_SENSES_BATCH_59_75_20260927.json",
    "ARABIC_SENSES_BATCH_76_85_20260927.json",
)
TITLE_OVERRIDES = {"OLP-0711": "في القواعد والاشتقاقات"}
CARD_FILES = ("CARDS-1.md", "CARDS-2.md")


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
    if len(ids) != 7 or len(set(ids)) != 7 or set(ids) & prior_ids:
        raise ValueError("Unexpected or previously localized choice inventory")
    decisions = {
        decision["decision_id"]: decision
        for decision in json.loads(INDEX.read_text(encoding="utf-8"))["decisions"]
    }
    totals = {key: 0 for key in ("locations", "resolved", "unresolved", "exact_pages", "fallback_pages")}
    cards = []
    for record in records:
        decision = decisions[record["decision_id"]]
        if not decision["index_metadata"]["human_index_included"]:
            raise ValueError("Choice excluded from human review index")
        if arabic_dominant(decision.get("sense")) or not all(
            arabic_dominant(decision.get(field)) for field in ("rationale", "expert_question")
        ):
            raise ValueError(f"Unexpected inherited explanation language: {record['decision_id']}")
        if not arabic_dominant(record["sense_ar"]) or not arabic_dominant(record["canon_note_ar"]):
            raise ValueError(f"New Arabic gloss or canon limit missing: {record['decision_id']}")
        localized = dict(decision)
        localized["sense"] = record["sense_ar"]
        card, counts = decision_card(localized, title_overrides=TITLE_OVERRIDES)
        evidence = (
            "**مواضع الأصل الإنجليزي المقابلة لهذا الشرح:** "
            + source_links(record, overlay["english_source_commit"]).replace(".؛", "؛")
            + "\n\n**حدود الشاهد الاصطلاحي:** " + record["canon_note_ar"]
        )
        marker = "**كل وقوع مسجل لهذا القرار:**"
        if card.count(marker) != 1:
            raise ValueError(f"Occurrence heading missing or repeated: {record['decision_id']}")
        cards.append(card.replace(marker, evidence + "\n\n" + marker, 1))
        for key in totals:
            totals[key] += counts[key]

    BASE.mkdir(parents=True, exist_ok=True)
    readme = BASE / "README.md"
    readme.write_text(
        "# سبعة شروح عربية إضافية للمعاني\n\n"
        "[البطاقات ١–٤](CARDS-1.md) · [البطاقات ٥–٧](CARDS-2.md)\n\n"
        "تضم هذه الدفعة سبعة اختيارات موروثة من الفهرس المثبّت. في كل بطاقة شرح عربي "
        "لاحق للمعنى، وسبب الاختيار وسؤال المراجع كما ورثهما السجل، وروابط لمواضع "
        "الأصل الإنجليزي، وحدود الشهادة المعجمية، وجميع الوقوعات المسجلة مع إحالات "
        "السطر أو الملف وصفحات القرّاء حيث ثبتت. لم تُغيَّر ألفاظ الكتاب، ولا يُدَّعى "
        "أن الشرح الجديد كان دافع المترجم الأول. ما بقي من مواضع غير محسومة معلَّم "
        "صراحة، وكل اختيار قابل للتصحيح دون تعليق العمل على مراجعة بشرية.\n\n"
        "عُوين معجم مصطلحات الرياضيات بصريًا في PDF ص ٧١ (المطبوعة ٥٩) "
        "لـ«علاقة ثنائية»، وفي PDF ص ١٣٩ (المطبوعة ١٢٧) لـ«شرط الاتساق». "
        "صفحة ٤٤٥ (المطبوعة ٤٣٣) تشهد لـ«استقراء رياضي» في الحالة العددية، "
        "لا لكل تطبيق على الصيغ والبراهين. البحث المحدود في OCR المعجم لم يُثبت "
        "العبارات الفنية الأخرى المذكورة في البطاقات؛ ولا يعني ذلك نفيها في سائر "
        "المصادر أو اعتماد ألفاظها الموروثة رسميًا. النص الإنجليزي الأصلي هو "
        "المرجع الحاسم في حدود كل تعريف.\n\n"
        "صاغ الشروح وملاحظات الشواهد وأخرج البطاقات OpenAI Codex — GPT-6 Sol، "
        "بمستوى جهد Ultra. التعليلات والأسئلة العربية الأخرى موروثة من السجل السابق.\n\n"
        "هذه دفعة محلية لم تُنشر بعد. إن اجتازت التحقق المستقل صارت التغطية "
        "العربية المحلية ٣٥٩ من ١٠٩٥ اختيارًا؛ ويظل الفهرس العربي المنشور عند "
        "٣٠٥ اختيارات إلى أن تُنشَر دفعة جوهرية موحّدة.\n",
        encoding="utf-8", newline="\n",
    )
    inventory = []
    for filename, subcards, subids in (
        (CARD_FILES[0], cards[:4], ids[:4]),
        (CARD_FILES[1], cards[4:], ids[4:]),
    ):
        path = BASE / filename
        path.write_text(
            "# بطاقات شرح المعاني العربية — القرارات ٨٦–٩٢\n\n"
            "[الرجوع إلى مقدمة الدفعة](README.md)\n\n" + "\n".join(subcards),
            encoding="utf-8", newline="\n",
        )
        if path.stat().st_size > 230_000:
            raise ValueError(f"Review card file exceeds easy-browsing cap: {filename}")
        inventory.append({"path": filename, "bytes": path.stat().st_size, "sha256": sha256(path), "decision_ids": subids})
    receipt = {
        "status": "LOCAL_ARABIC_SENSE_BATCH_86_92_PENDING_INDEPENDENT_READBACK",
        "source_index_sha256": PINNED_INDEX_SHA,
        "overlay_sha256": sha256(OVERLAY),
        "choice_count": len(ids),
        "decision_ids": ids,
        "totals": totals,
        "readme": {"bytes": readme.stat().st_size, "sha256": sha256(readme)},
        "cards": inventory,
    }
    (BASE / "BUILD_RECEIPT.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"status": receipt["status"], "choices": len(ids), **totals}, ensure_ascii=True))


if __name__ == "__main__":
    main()
