#!/usr/bin/env python3
"""Render a bounded Arabic expert-review overlay using the frozen review index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import quote

from render_arabic_review_existing_20260927 import arabic_dominant, decision_card, sha256
from render_arabic_review_senses_76_85_20260927 import source_links
from stream_expert_review_decisions import iter_decisions


ROOT = Path(__file__).resolve().parents[1]
TERM_DIR = ROOT / "evidence/classical/terminology"
REVIEW_DIR = ROOT / "expert-review/2026-09-26-final-page-review"
EASTERN = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def east(value: object) -> str:
    return str(value).translate(EASTERN)


def printed_page(canon: dict, page: int) -> int:
    labels = canon.get("printed_page_labels")
    if labels is not None:
        if set(labels) != {str(number) for number in canon["visually_checked_pdf_pages"]}:
            raise ValueError("Printed-page labels do not cover exactly the visually checked pages")
        value = labels.get(str(page))
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"Invalid printed-page label: {page}")
        return value
    return page + canon["printed_page_offset"]


def canon_link(canon: dict, page: int) -> str:
    name = quote(Path(canon["pdf_path"]).name)
    url = f"https://archive.org/download/DAM2018ENAR/{name}#page={page}"
    return f"[ص {east(page)} من PDF (المطبوعة {east(printed_page(canon, page))})]({url})"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("overlay", type=Path, help="Overlay JSON path, absolute or relative to repository")
    args = parser.parse_args()
    overlay_path = args.overlay if args.overlay.is_absolute() else ROOT / args.overlay
    overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    batch = overlay["batch"]
    records = overlay["records"]
    ids = [item["decision_id"] for item in records]
    first, last = batch["first_number"], batch["last_number"]
    if len(records) != last - first + 1 or len(ids) != len(set(ids)):
        raise ValueError("Nonconsecutive or repeated choice inventory")
    index = ROOT / overlay["source_index_path"]
    if sha256(index) != overlay["source_index_sha256"]:
        raise ValueError("Frozen source index drift")
    canon = overlay["canon"]
    if sha256(Path(canon["pdf_path"])) != canon["pdf_sha256"]:
        raise ValueError("Dictionary PDF identity drift")
    for key in ("ocr_query", "ocr_evidence"):
        if sha256(ROOT / canon[key + "_path"]) != canon[key + "_sha256"]:
            raise ValueError(f"Dictionary intake identity drift: {key}")
    prior_ids = {
        item["decision_id"]
        for name in overlay["prior_overlays"]
        for item in json.loads((TERM_DIR / name).read_text(encoding="utf-8"))["records"]
    }
    wanted = set(ids)
    decisions = {}
    existing_arabic = set()
    for decision in iter_decisions(index):
        if decision["index_metadata"]["human_index_included"] and all(
            arabic_dominant(decision.get(key)) for key in ("sense", "rationale", "expert_question")
        ):
            existing_arabic.add(decision["decision_id"])
        if decision["decision_id"] in wanted:
            decisions[decision["decision_id"]] = decision
    if len(existing_arabic) != 267 or set(decisions) != wanted or wanted & (prior_ids | existing_arabic):
        raise ValueError("Choice missing, already localized, or base Arabic inventory drift")
    if batch["local_after"] != len(existing_arabic) + len(prior_ids) + len(records):
        raise ValueError("Claimed post-batch local total does not match disjoint inventory")

    cards = []
    totals = {key: 0 for key in ("locations", "resolved", "unresolved", "exact_pages", "fallback_pages")}
    observed_pages = set()
    for record in records:
        decision = decisions[record["decision_id"]]
        if not decision["index_metadata"]["human_index_included"]:
            raise ValueError("Excluded choice cannot be rendered")
        for key in ("sense_ar", "rationale_ar", "expert_question_ar", "source_relevance_ar",
                    "canon_note_ar", "confidence_ar"):
            if not arabic_dominant(record.get(key)):
                raise ValueError(f"Missing Arabic {key}: {record['decision_id']}")
        english_paths = {
            loc["logical_path"]
            for group in decision["index_metadata"]["occurrences"]
            for loc in group["locations"]
            if loc["source_kind"] == "english" and loc.get("human_review_included")
        }
        if "source_passages" in record:
            sources = record["source_passages"]
        else:
            if len(english_paths) != 1:
                raise ValueError(f"Multiple original paths require source_passages: {record['decision_id']}")
            sources = [{
                "path": next(iter(english_paths)), "lines": record["source_lines"],
                "needle": record["source_needle"], "relevance_ar": record["source_relevance_ar"],
            }]
        if (not sources or {item["path"] for item in sources} != english_paths
                or len({(item["path"], item["lines"], item["needle"]) for item in sources}) != len(sources)
                or not all(item["path"].startswith("content/")
                           and arabic_dominant(item.get("relevance_ar"))
                           for item in sources)):
            raise ValueError(f"Original passage inventory incomplete: {record['decision_id']}")
        localized = dict(decision)
        localized.update(sense=record["sense_ar"], rationale=record["rationale_ar"],
                         expert_question=record["expert_question_ar"])
        display = dict(decision["review_display"])
        display["chosen_arabic"] = display["chosen_arabic"].replace("\\-", "")
        localized["review_display"] = display
        card, counts = decision_card(localized, title_overrides=batch["unit_title_ar"])
        pages = record["canon_pdf_pages"]
        if not pages or not set(pages) <= set(canon["visually_checked_pdf_pages"]):
            raise ValueError(f"Uninspected dictionary page: {record['decision_id']}")
        observed_pages.update(pages)
        alternatives = ("؛ ".join(record["alternatives_ar"]) if record["alternatives_ar"]
                        else "لا بديل محدد تقتضيه الشواهد في هذا الموضع")
        evidence = (
            "**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** "
            + source_links({"source_passages": sources}, overlay["english_source_commit"])
            + ("\n\n**وجه جمع المواضع:** " + record["source_relevance_ar"]
               if "source_passages" in record else "")
            + "\n\n**مواضع المعجم المعاينة:** "
            + "، ".join(canon_link(canon, page) for page in pages)
            + "\n\n**حدود الشاهد المعجمي:** " + record["canon_note_ar"]
            + "\n\n**بديل جدير بالمقارنة:** " + alternatives
            + "\n\n**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** " + record["confidence_ar"]
        )
        marker = "**كل وقوع مسجل لهذا القرار:**"
        if card.count(marker) != 1:
            raise ValueError(f"Missing location block: {record['decision_id']}")
        cards.append(card.replace(marker, evidence + "\n\n" + marker, 1))
        for key in totals:
            totals[key] += counts[key]
    if observed_pages != set(canon["visually_checked_pdf_pages"]):
        raise ValueError("Inspected dictionary-page inventory is not all cited")

    sections = batch["sections"]
    if [n for begin, end, _name, _title in sections for n in range(begin, end)] != list(range(len(ids))):
        raise ValueError("Card section partition is incomplete or overlapping")
    base = REVIEW_DIR / batch["directory"]
    base.mkdir(parents=True, exist_ok=True)
    inventory = []
    for begin, end, name, title in sections:
        path = base / name
        path.write_text(
            f"# بطاقات {title} — القرارات {east(first + begin)}–{east(first + end - 1)}\n\n"
            "[الرجوع إلى مقدمة الدفعة](README.md)\n\n" + "\n".join(cards[begin:end]),
            encoding="utf-8", newline="\n",
        )
        if path.stat().st_size > 230_000:
            raise ValueError(f"Card page exceeds browseable size: {name}")
        inventory.append({"path": name, "bytes": path.stat().st_size,
                          "sha256": sha256(path), "decision_ids": ids[begin:end]})
    links = " · ".join(f"[{title}]({name})" for _begin, _end, name, title in sections)
    pages = "، ".join(east(page) for page in canon["visually_checked_pdf_pages"])
    page_label_note = (
        "رُبط كل موضع برقم صفحته المطبوع الذي عوين مباشرة."
        if "printed_page_labels" in canon
        else "ترقيم الكتاب المطبوع أقل باثنتي عشرة صفحة."
    )
    readme = base / "README.md"
    readme.write_text(
        f"# {batch['title_ar']}\n\n{links}\n\n"
        + batch["summary_ar"] + "\n\n" + batch["review_flags_ar"] + "\n\n"
        + overlay["editorial_basis_ar"] + "\n\n"
        + f"المصدر الاصطلاحي: {canon['identity']}؛ [صفحة النسخة]({canon['url']}). "
        + f"عُوينت صفحات PDF {pages}. {page_label_note} "
        + "لا تثبت هذه الصفحات وحدها جميع أساليب العربية التراثية.\n\n"
        + "صاغ هذه المراجعة اللاحقة وبطاقاتها OpenAI Codex — GPT-6 Sol، بمستوى جهد Ultra. "
        + "النصوص الإنجليزية والعربية المقتبسة موروثة من المصادر الموصولة. "
        + "لم تقع مراجعة بشرية شاملة؛ كل اختيار قابل للتصحيح.\n\n"
        + f"هذه دفعة محلية لم تُنشر بعد. مع هذه الدفعة تبلغ التغطية "
        + f"العربية المحلية {east(batch['local_after'])} من ١٠٩٥ اختيارًا؛ "
        + f"التغطية المنشورة حاليًا {east(batch['public_before'])} من ١٠٩٥.\n",
        encoding="utf-8", newline="\n",
    )
    receipt = {
        "status": "LOCAL_ARABIC_REVIEW_BATCH_PENDING_INDEPENDENT_READBACK",
        "source_index_sha256": overlay["source_index_sha256"],
        "overlay_sha256": sha256(overlay_path), "choice_count": len(ids),
        "decision_ids": ids, "totals": totals,
        "readme": {"bytes": readme.stat().st_size, "sha256": sha256(readme)},
        "cards": inventory,
    }
    (base / "BUILD_RECEIPT.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"status": receipt["status"], "choices": len(ids), **totals}, ensure_ascii=True))


if __name__ == "__main__":
    main()
