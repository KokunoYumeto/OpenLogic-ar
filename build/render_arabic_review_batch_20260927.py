#!/usr/bin/env python3
"""Render eight fully located Arabic review cards from a pinned index."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from render_arabic_priority_guide_20260926 import (
    INDEX,
    LABELS,
    east,
    excerpt,
    page_links,
    pinned_url,
    reader_kind,
    source_line,
)


ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "evidence/classical/terminology/ARABIC_REVIEW_BATCH_31_38_20260927.json"
PRIORITY = ROOT / "evidence/classical/terminology/ARABIC_PRIORITY_30_20260926.json"
OUTPUT = ROOT / "expert-review/2026-09-26-final-page-review/BATCH_31_38_AR.md"
INDEX_SHA = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"
SOURCE_NAMES = {"english": "الأصل الإنجليزي", "msa": "العربية المعيارية", "classical": "العربية التراثية"}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest().upper()


def source_link(location: dict) -> str:
    url = location.get("source_url")
    if not url or not location.get("line_reconciliation", {}).get("resolved"):
        raise ValueError(f"A batch location is not source-line resolved: {location.get('location_id')}")
    number = source_line(location)
    pinned = pinned_url(url)
    if not pinned.endswith(f"#L{number}"):
        prefix = pinned.split("#L", 1)[0]
        pinned = f"{prefix}#L{number}"
    return f"[السطر {east(number)}]({pinned})"


def render_location(location: dict) -> tuple[list[str], int]:
    kind = location["source_kind"]
    if kind not in SOURCE_NAMES:
        raise ValueError(f"Unexpected source kind: {kind}")
    source = source_link(location)
    sample = excerpt(location)
    if kind == "english":
        return [f"  - **{SOURCE_NAMES[kind]}:** {source}؛ الشاهد «{sample}»."], 0
    pages = {}
    for page in location.get("page_evidence", []):
        reader = reader_kind(page.get("reader", ""))
        if reader is not None:
            if reader in pages:
                raise ValueError(f"Repeated page record for {reader}: {location.get('location_id')}")
            pages[reader] = page
    required = {"classical"} if kind == "classical" else {"international", "machrek"}
    if set(pages) != required:
        raise ValueError(f"Missing or stray page evidence: {location.get('location_id')}, {sorted(pages)}")
    lines = []
    exact_pages = 0
    for reader in ("classical", "international", "machrek"):
        if reader not in pages:
            continue
        page = pages[reader]
        method = page.get("method")
        if method == "synctex-exact":
            qualifier = "موضع اللفظ مطابق لسجل الصفحة"
            exact_pages += 1
        elif method == "unit-start-fallback":
            qualifier = "صفحة بدء الوحدة فقط، وليست صفحة اللفظ مثبتةً بالدقة"
        elif method == "visual-text-exact":
            qualifier = "موضع فُحص في الصفحة المصوَّرة"
            exact_pages += 1
        else:
            raise ValueError(f"Unknown page method {method}: {location.get('location_id')}")
        lines.append(
            f"  - **{LABELS[reader]}:** {source}؛ {page_links(reader, page)}؛ "
            f"{qualifier}. الشاهد «{sample}»."
        )
    return lines, exact_pages


def render() -> tuple[str, dict]:
    if digest(INDEX) != INDEX_SHA:
        raise ValueError("Pinned final-page index changed")
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    priority = json.loads(PRIORITY.read_text(encoding="utf-8"))
    if batch["source_index_sha256"] != INDEX_SHA or priority["source_index_sha256"] != INDEX_SHA:
        raise ValueError("Localization layers refer to another index")
    records = batch["records"]
    ids = [record["decision_id"] for record in records]
    if len(ids) != 8 or len(set(ids)) != 8:
        raise ValueError("Expected eight distinct batch choices")
    if set(ids) & {record["decision_id"] for record in priority["records"]}:
        raise ValueError("Batch overlaps the earlier 30-choice guide")
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    decisions = {decision["decision_id"]: decision for decision in index["decisions"]}
    lines = [
        "# فهرس المراجعة العربية: القرارات ٣١–٣٨",
        "",
        "ثمانية قرارات مضافة إلى الثلاثين المنشورة في دليل البدء. في كل قرار أدناه "
        "المعنى المختار وسببه وسؤال مفتوح، ثم **جميع المواضع المسجلة** لهذا القرار "
        "في الأصل الإنجليزي والطبعات العربية. هذه دفعة عمل محلية لم تُنشر بعد؛ "
        "والفهرس الكامل ذو ١٠٩٥ قرارًا لم يكتمل تعريبه.",
        "",
        "الترجمة الموروثة: OpenAI Codex — GPT-5.6 Sol، بمستوى جهد Ultra. "
        "التعليلات والأسئلة الحالية والتحقق من الشواهد: OpenAI Codex — GPT-6 Sol، "
        "بمستوى جهد Ultra. هذه موازنة لاحقة لا تدّعي دوافع تاريخية أو مراجعة بشرية.",
        "",
        "علامات `!!{…}` مفاتيح في مصدر LaTeX تظهر بألفاظ عربية في ملفات PDF. "
        "وصف «صفحة بدء الوحدة فقط» لا يثبت أن اللفظ يقع في تلك الصفحة بعينها.",
        "",
    ]
    human_locations = 0
    rendered_location_ids = []
    exact_reader_pages = 0
    for number, record in enumerate(records, 31):
        decision_id = record["decision_id"]
        decision = decisions.get(decision_id)
        if decision is None or not decision["index_metadata"]["human_index_included"]:
            raise ValueError(f"Absent human-review decision: {decision_id}")
        for field in ("surface_ar", "sense_ar", "rationale_ar", "alternatives_ar", "question_ar"):
            if not record.get(field, "").strip():
                raise ValueError(f"Missing Arabic review field {field}: {decision_id}")
        lines.extend(
            [
                f"## {east(number)}. {record['surface_ar']}",
                "",
                f"الأصل: `{decision['english_term']}`. معرّف القرار: `{decision_id}`.",
                "",
                f"**المعنى:** {record['sense_ar']}",
                "",
                f"**سبب الاختيار المؤقت:** {record['rationale_ar']}",
                "",
                f"**البدائل:** {record['alternatives_ar']}",
                "",
                f"**سؤال للمراجع:** {record['question_ar']}",
                "",
            ]
        )
        if record["canon_evidence"]:
            lines.append("**الشاهد المعجمي وحدّه:**")
            lines.append("")
            for witness in record["canon_evidence"]:
                forms = "، ".join(f"«{form}»" for form in witness["short_forms_ar"])
                lines.append(
                    f"- *معجم مصطلحات الرياضيات*، صفحة PDF {east(witness['physical_pdf_page'])} "
                    f"(المطبوعة {east(witness['printed_page'])}): {forms}. "
                    f"{witness['relation_ar']}."
                )
            lines.append("")
        else:
            lines.extend([f"**حد الشاهد:** {record['canon_gap_ar']}", ""])
        lines.extend([f"**فحص السياق:** {record['source_check_ar']}", "", "**جميع مواضع القرار المسجلة:**", ""])
        groups = decision["index_metadata"]["occurrences"]
        for group in groups:
            if not group.get("human_review_included"):
                continue
            unit = group["unit"]
            lines.append(f"- **{unit['unit_id']} — {unit['title']}، وقوع {east(group['occurrence_index'])}:**")
            for location in group["locations"]:
                if not location.get("human_review_included"):
                    continue
                loc_lines, exact = render_location(location)
                lines.extend(loc_lines)
                exact_reader_pages += exact
                human_locations += 1
                rendered_location_ids.append(location["location_id"])
        lines.append("")
    if human_locations != 30 or len(set(rendered_location_ids)) != human_locations:
        raise ValueError(f"Unexpected human location census: {human_locations}")
    lines.extend(
        [
            "---",
            "",
            "هذه دفعة تعريب لسجل المراجعة؛ لا تصير قائمة الـ١٠٩٥ قرارًا كاملةً "
            "إلا بعد تحرير بقية القرارات ودمجها والتحقق منها ونشر نسخة مجمعة.",
            "",
        ]
    )
    return "\n".join(lines), {
        "decision_ids": ids,
        "human_locations": human_locations,
        "location_ids": rendered_location_ids,
        "exact_reader_page_links": exact_reader_pages,
    }


def main() -> None:
    body, census = render()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(body, encoding="utf-8", newline="\n")
    print(json.dumps({"output": str(OUTPUT), "sha256": digest(OUTPUT), **{k: v for k, v in census.items() if k != "location_ids"}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
