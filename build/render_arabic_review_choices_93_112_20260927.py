#!/usr/bin/env python3
"""Render twenty retrospectively reasoned Arabic review cards without a full-index load."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

from render_arabic_review_existing_20260927 import (
    INDEX, PINNED_INDEX_SHA, arabic_dominant, decision_card, sha256,
)
from render_arabic_review_senses_76_85_20260927 import source_links
from stream_expert_review_decisions import iter_decisions


ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "evidence/classical/terminology/ARABIC_REVIEW_BATCH_93_112_20260927.json"
BASE = ROOT / "expert-review/2026-09-26-final-page-review/arabic-decisions-93-112"
PRIOR = (
    "ARABIC_PRIORITY_30_20260926.json",
    "ARABIC_REVIEW_BATCH_31_38_20260927.json",
    "ARABIC_SENSES_BATCH_39_58_20260927.json",
    "ARABIC_SENSES_BATCH_59_75_20260927.json",
    "ARABIC_SENSES_BATCH_76_85_20260927.json",
    "ARABIC_SENSES_BATCH_86_92_20260927.json",
)
TITLES = {
    "OLP-0006": "المجموعات الجزئية ومجموعات القوى",
    "OLP-0008": "الاتحادات والتقاطعات",
    "OLP-0009": "الأزواج والصفوف المرتبة والضروب الديكارتية",
}
EASTERN = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def east(value: object) -> str:
    return str(value).translate(EASTERN)


def canon_link(canon: dict, page: int) -> str:
    filename = quote(Path(canon["pdf_path"]).name)
    url = f"https://archive.org/download/DAM2018ENAR/{filename}#page={page}"
    printed = page + canon["printed_page_offset"]
    return f"[ص {east(page)} من PDF (المطبوعة {east(printed)})]({url})"


def main() -> None:
    overlay = json.loads(OVERLAY.read_text(encoding="utf-8"))
    if sha256(INDEX) != PINNED_INDEX_SHA or overlay["source_index_sha256"] != PINNED_INDEX_SHA:
        raise ValueError("Pinned review index drift")
    if len(overlay["records"]) != 20:
        raise ValueError("Unexpected review batch size")
    ids = [record["decision_id"] for record in overlay["records"]]
    if len(set(ids)) != 20:
        raise ValueError("Repeated review choice")
    prior_ids = {
        record["decision_id"]
        for name in PRIOR
        for record in json.loads((ROOT / "evidence/classical/terminology" / name).read_text(encoding="utf-8"))["records"]
    }
    wanted = set(ids)
    decisions = {}
    existing_arabic = set()
    for decision in iter_decisions(INDEX):
        if decision["index_metadata"]["human_index_included"] and all(
            arabic_dominant(decision.get(key)) for key in ("sense", "rationale", "expert_question")
        ):
            existing_arabic.add(decision["decision_id"])
        if decision["decision_id"] in wanted:
            decisions[decision["decision_id"]] = decision
    if len(existing_arabic) != 267 or len(decisions) != 20:
        raise ValueError("Frozen human review inventory drift")
    if wanted & (prior_ids | existing_arabic):
        raise ValueError("A choice was already localized")
    canon = overlay["canon"]
    if sha256(Path(canon["pdf_path"])) != canon["pdf_sha256"]:
        raise ValueError("Consulted dictionary PDF identity drift")
    if sha256(ROOT / canon["ocr_evidence_path"]) != canon["ocr_evidence_sha256"]:
        raise ValueError("Bounded dictionary OCR evidence drift")
    observed_pages = set()
    cards = []
    totals = {key: 0 for key in ("locations", "resolved", "unresolved", "exact_pages", "fallback_pages")}
    for record in overlay["records"]:
        decision = decisions[record["decision_id"]]
        if not decision["index_metadata"]["human_index_included"]:
            raise ValueError("Choice excluded from human review index")
        for key in ("sense_ar", "rationale_ar", "expert_question_ar", "canon_note_ar", "confidence_ar"):
            if not arabic_dominant(record.get(key)):
                raise ValueError(f"Missing Arabic {key}: {record['decision_id']}")
        english_paths = {
            location["logical_path"]
            for group in decision["index_metadata"]["occurrences"]
            for location in group["locations"]
            if location["source_kind"] == "english" and location.get("human_review_included")
        }
        if len(english_paths) != 1:
            raise ValueError(f"Expected one bound English file: {record['decision_id']}")
        source_path = english_paths.pop()
        if not source_path.startswith("content/"):
            raise ValueError("Unexpected original-source path")
        source_passage = {
            "path": source_path,
            "lines": record["source_lines"],
            "needle": record["source_needle"],
            "relevance_ar": record["source_relevance_ar"],
        }
        localized = dict(decision)
        localized.update({
            "sense": record["sense_ar"],
            "rationale": record["rationale_ar"],
            "expert_question": record["expert_question_ar"],
        })
        card, counts = decision_card(localized, title_overrides=TITLES)
        pages = record["canon_pdf_pages"]
        if not pages or not set(pages) <= set(canon["visually_checked_pdf_pages"]):
            raise ValueError(f"Uninspected canon page: {record['decision_id']}")
        observed_pages.update(pages)
        alternatives = "؛ ".join(record["alternatives_ar"]) if record["alternatives_ar"] else "لا بديل محدد تقتضيه الشواهد في هذا الموضع"
        evidence = (
            "**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** "
            + source_links({"source_passages": [source_passage]}, overlay["english_source_commit"])
            + "\n\n**مواضع المعجم المعاينة:** " + "، ".join(canon_link(canon, page) for page in pages)
            + "\n\n**حدود الشاهد المعجمي:** " + record["canon_note_ar"]
            + "\n\n**بديل جدير بالمقارنة:** " + alternatives
            + "\n\n**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** " + record["confidence_ar"]
        )
        marker = "**كل وقوع مسجل لهذا القرار:**"
        if card.count(marker) != 1:
            raise ValueError(f"Occurrence heading missing: {record['decision_id']}")
        cards.append(card.replace(marker, evidence + "\n\n" + marker, 1))
        for key in totals:
            totals[key] += counts[key]
    if observed_pages != set(canon["visually_checked_pdf_pages"]):
        raise ValueError("The canon-page inventory includes an unused or missing page")
    BASE.mkdir(parents=True, exist_ok=True)
    sections = ((0, 7, "CARDS-1.md", "المجموعات الجزئية ومجموعات القوى"),
                (7, 15, "CARDS-2.md", "الاتحادات والتقاطعات"),
                (15, 20, "CARDS-3.md", "الأزواج والصفوف والضرب الديكارتي"))
    inventory = []
    for first, last, filename, title in sections:
        path = BASE / filename
        path.write_text(
            f"# بطاقات {title} — القرارات {east(93 + first)}–{east(92 + last)}\n\n"
            "[الرجوع إلى مقدمة الدفعة](README.md)\n\n" + "\n".join(cards[first:last]),
            encoding="utf-8", newline="\n",
        )
        if path.stat().st_size > 230_000:
            raise ValueError(f"Reader card file is too large: {filename}")
        inventory.append({
            "path": filename, "bytes": path.stat().st_size, "sha256": sha256(path),
            "decision_ids": ids[first:last],
        })
    readme = BASE / "README.md"
    readme.write_text(
        "# عشرون قرارًا اصطلاحيًا من أوائل نظرية المجموعات\n\n"
        "[المجموعات الجزئية والقوى](CARDS-1.md) · "
        "[الاتحادات والتقاطعات](CARDS-2.md) · "
        "[الأزواج والضرب الديكارتي](CARDS-3.md)\n\n"
        "هذه بطاقات عربية لاحقة لعشرين اختيارًا في الوحدات OLP-0006 وOLP-0008 وOLP-0009. "
        "يرى المراجع في كل بطاقة اللفظ المنشور، ومعناه، وسبب الإبقاء عليه أو موضع الشك، "
        "وسؤالًا محددًا، وموضع الأصل الإنجليزي، والمدخل المعجمي المعاين، وجميع وقوعات "
        "القرار المسجلة في الأصل والطبعتين العربيتين مع روابط الأسطر وصفحات القراء حيث ثبتت. "
        "صفحة بدء الوحدة الموسومة ليست إثباتًا لصفحة اللفظ. لم يتغير نص أي طبعة في هذه الدفعة؛ "
        "والتعليل اللاحق لا يُنسب إلى قرار الترجمة الأول.\n\n"
        "الموضعان الأشد حاجة إلى مراجعة اصطلاحية هما «متباينتين» بإزاء مدخل المعجم "
        "«مجموعات منفصلة»، و«الضرب الديكارتي» بإزاء «جداء ديكارتي لمجموعتين». "
        "المعنى الرياضي مضبوط بالمعادلات في المتن، لكن شاهد المعجم لا يثبت هذين "
        "اللفظين المنشورين. البدائل قابلة للتصحيح من غير انتظار رأي خبير.\n\n"
        "مصدر المصطلحات: معجم مصطلحات الرياضيات، مجمع اللغة العربية بدمشق، الطبعة الأولى "
        "٢٠١٨؛ [صفحة النسخة](https://archive.org/details/DAM2018ENAR). "
        "طابقت المعاينة المصورة صفحات PDF ٩١، ١٩٦، ٣٧٠، ٥٠٦، ٥٥٧، ٥٧١، ٦٤٤، "
        "٦٩٦، ٧٥٤ (الترقيم المطبوع أقل باثنتي عشرة صفحة). لا يثبت هذا المعجم وحده "
        "جميع أساليب العربية التراثية في الكتاب.\n\n"
        "صاغ هذه المراجعة اللاحقة وبطاقاتها OpenAI Codex — GPT-6 Sol، بمستوى جهد Ultra. "
        "النصوص الإنجليزية والعربية المقتبسة موروثة من المصادر الموصولة. لم تقع مراجعة "
        "بشرية شاملة؛ كل اختيار قابل للتصحيح.\n\n"
        "هذه دفعة محلية لم تُنشر بعد. إذا اجتازت التحقق المستقل تصبح التغطية العربية "
        "المحلية ٣٧٩ من ١٠٩٥ اختيارًا؛ التغطية المنشورة في الوقت الحالي ٣٥٩ من ١٠٩٥.\n",
        encoding="utf-8", newline="\n",
    )
    receipt = {
        "status": "LOCAL_ARABIC_CHOICE_BATCH_93_112_PENDING_INDEPENDENT_READBACK",
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
