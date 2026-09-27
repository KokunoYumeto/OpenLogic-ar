#!/usr/bin/env python3
"""Expose already Arabic-language review entries with every recorded locator."""

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
BASE = ROOT / "expert-review/2026-09-26-final-page-review/arabic-existing"
PINNED_INDEX_SHA = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"
MAX_CARD_BYTES_PER_SHARD = 220_000


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def arabic_dominant(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    arabic = sum(0x600 <= ord(char) <= 0x6FF for char in value)
    latin = sum(char.isascii() and char.isalpha() for char in value)
    return arabic > latin


def current_source(location: dict) -> tuple[str, str]:
    recon = location.get("line_reconciliation", {})
    if recon.get("resolved"):
        number = source_line(location)
        url = pinned_url(location["source_url"]).split("#L", 1)[0] + f"#L{number}"
        return f"[السطر {east(number)}]({url})", ""
    file_url = location.get("file_url")
    if not file_url:
        raise ValueError(f"Unresolved location lacks even a file URL: {location['location_id']}")
    url = pinned_url(file_url).split("#L", 1)[0]
    return f"[الملف]({url})", "⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة"


def page_parts(location: dict) -> tuple[list[str], int, int]:
    pages = location.get("page_evidence", [])
    if location["source_kind"] == "english":
        if pages:
            raise ValueError(f"Unexpected English PDF page evidence: {location['location_id']}")
        return [], 0, 0
    out = []
    exact = 0
    fallback = 0
    unavailable = 0
    for page in pages:
        reader = reader_kind(page.get("reader", ""))
        if reader is None:
            raise ValueError(f"Unknown reader: {location['location_id']}")
        method = page.get("method")
        if method == "synctex-exact":
            note = "موضع السطر مطابق لصفحة القارئ"
            exact += 1
        elif method == "visual-text-exact":
            note = "موضع فُحص في الصفحة المصوَّرة"
            exact += 1
        elif method == "unit-start-fallback":
            note = "صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة"
            fallback += 1
        elif method == "unavailable":
            if page.get("pdf_pages"):
                raise ValueError(f"Unavailable page record unexpectedly has pages: {location['location_id']}")
            unavailable += 1
            continue
        else:
            raise ValueError(f"Unexpected page evidence method: {method}")
        out.append(f"{LABELS[reader]}: {page_links(reader, page)} ({note})")
    if unavailable and not out:
        out.append("⚠ لم تثبت صفحة PDF لهذا الموضع؛ إحالة السطر أعلاه هي الإحالة الدقيقة المتاحة")
    return out, exact, fallback


def decision_card(decision: dict, title_overrides: dict[str, str] | None = None) -> tuple[str, dict]:
    index_meta = decision["index_metadata"]
    surface = decision["review_display"]["chosen_arabic"]
    lines = [
        f"## {surface}",
        "",
        f"الأصل الإنجليزي: `{decision['english_term']}`. معرّف القرار: `{decision['decision_id']}`.",
        "",
        f"**المعنى المقصود:** {decision['sense']}",
        "",
        f"**سبب الاختيار:** {decision['rationale']}",
        "",
        f"**سؤال مفتوح:** {decision['expert_question']}",
        "",
        "**كل وقوع مسجل لهذا القرار:**",
        "",
    ]
    counts = {"locations": 0, "resolved": 0, "unresolved": 0, "exact_pages": 0, "fallback_pages": 0}
    for group in index_meta["occurrences"]:
        if not group.get("human_review_included"):
            continue
        unit = group["unit"]
        unit_title = (title_overrides or {}).get(unit["unit_id"], unit["title"])
        lines.append(f"- **{unit['unit_id']} — {unit_title}، وقوع {east(group['occurrence_index'])}:**")
        for location in group["locations"]:
            if not location.get("human_review_included"):
                continue
            counts["locations"] += 1
            link, unresolved = current_source(location)
            if unresolved:
                counts["unresolved"] += 1
            else:
                counts["resolved"] += 1
            kind = {"english": "الأصل", "msa": "العربية المعيارية", "classical": "العربية التراثية"}[location["source_kind"]]
            pages, exact, fallback = page_parts(location)
            counts["exact_pages"] += exact
            counts["fallback_pages"] += fallback
            sample = excerpt(location, decision["decision_id"])
            page_text = "؛ ".join(pages)
            suffix = f"؛ {page_text}" if page_text else ""
            if unresolved:
                suffix += f"؛ {unresolved}"
            lines.append(f"  - **{kind}:** {link}{suffix}. الشاهد المسجل: «{sample}».")
    lines.append("")
    return "\n".join(lines), counts


def main() -> None:
    if sha256(INDEX) != PINNED_INDEX_SHA:
        raise ValueError("Final-page index changed")
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    ready = [
        decision for decision in index["decisions"]
        if decision["index_metadata"]["human_index_included"]
        and all(arabic_dominant(decision.get(key)) for key in ("sense", "rationale", "expert_question"))
        and arabic_dominant(decision["review_display"].get("chosen_arabic"))
    ]
    ready.sort(key=lambda decision: (decision["english_term"].casefold(), decision["decision_id"]))
    if len(ready) != 267 or len({decision["decision_id"] for decision in ready}) != 267:
        raise ValueError(f"Unexpected already-Arabic choice count: {len(ready)}")
    BASE.mkdir(parents=True, exist_ok=True)
    totals = {"locations": 0, "resolved": 0, "unresolved": 0, "exact_pages": 0, "fallback_pages": 0}
    rendered_cards = []
    for decision in ready:
        card, counts = decision_card(decision)
        rendered_cards.append((decision, card))
        for key in totals:
            totals[key] += counts[key]
    chunks = []
    current_chunk = []
    current_bytes = 0
    for item in rendered_cards:
        card_bytes = len(item[1].encode("utf-8"))
        if card_bytes > MAX_CARD_BYTES_PER_SHARD:
            raise ValueError(f"Single choice exceeds the reader shard cap: {item[0]['decision_id']}")
        if current_chunk and current_bytes + card_bytes > MAX_CARD_BYTES_PER_SHARD:
            chunks.append(current_chunk)
            current_chunk = []
            current_bytes = 0
        current_chunk.append(item)
        current_bytes += card_bytes
    if current_chunk:
        chunks.append(current_chunk)
    inventory = []
    toc = [
        "# فهرس القرارات المعلَّلة بالعربية في السجل الحالي",
        "",
        "هذه واجهة لما وُجدت له في السجل المنشور صياغة عربية للمعنى والسبب "
        "وسؤال المراجعة، لا إعادة ترجمة جديدة ولا فحصًا مستقلًا لجميع تعليلاته. "
        "تضم ٢٦٧ قرارًا من أصل ١٠٩٥. رتبت البطاقات بحسب المصطلح الإنجليزي "
        "ليسهل العثور عليها، وفي كل بطاقة جميع الوقوعات المسجلة مع إحالات "
        "المصدر والصفحة وما بقي غير محسوم. تُعرض صفحات بدء الوحدات بوسم صريح، "
        "ولا تُنسب إليها دقة صفحة اللفظ. لا تشمل هذه الواجهة وحدها دليل "
        "الثلاثين قرارًا ذا الأولوية ولا الدفعة المحلية الجديدة ذات الثمانية؛ "
        "والقائمة العربية الكاملة ما زالت قيد التحرير.",
        "",
        "الترجمة والتعليلات الموروثة: OpenAI Codex — GPT-5.6 Sol، بمستوى جهد Ultra. "
        "إخراج هذا الفهرس وربط صفحاته: OpenAI Codex — GPT-6 Sol، بمستوى جهد Ultra. "
        "لم تقع مراجعة بشرية شاملة، وكل اختيار قابل للتصحيح.",
        "",
        "## الأجزاء",
        "",
    ]
    for number, chunk in enumerate(chunks, 1):
        filename = f"part-{number:03}.md"
        shard = [
            f"# القرارات العربية الحالية — الجزء {east(number)} من {east(len(chunks))}",
            "",
            "[الرجوع إلى فهرس الأجزاء](README.md)",
            "",
            "السياقات والتعليلات أدناه من السجل القائم؛ لم تُراجع جميعها مراجعة معجمية "
            "جديدة في هذا الإخراج. يعني تحذير الموضع غير المحسوم أن الملف معروف "
            "لكن السطر الحالي لم يثبت، ويعني رابط بدء الوحدة أن صفحة اللفظ ليست معلومة بالدقة.",
            "",
        ]
        for decision, card in chunk:
            shard.append(card)
        path = BASE / filename
        path.write_text("\n".join(shard), encoding="utf-8", newline="\n")
        if path.stat().st_size > 230_000:
            raise ValueError(f"Reader shard too large for easy browsing: {path}")
        title = f"{chunk[0][0]['english_term']} — {chunk[-1][0]['english_term']}"
        toc.append(f"- [الجزء {east(number)}: {title}]({filename}) — {east(len(chunk))} قرارًا.")
        inventory.append({"path": f"expert-review/2026-09-26-final-page-review/arabic-existing/{filename}", "bytes": path.stat().st_size, "sha256": sha256(path), "choices": len(chunk), "decision_ids": [d["decision_id"] for d, _ in chunk]})
    toc.extend(["", "انظر أيضًا [دليل البدء ذي الثلاثين قرارًا](../START_HERE_AR.md).", ""])
    start = BASE / "README.md"
    start.write_text("\n".join(toc), encoding="utf-8", newline="\n")
    if totals["locations"] != 2789 or totals["unresolved"] != 19:
        raise ValueError(f"Unexpected occurrence census: {totals}")
    receipt = {
        "status": "LOCAL_EXISTING_ARABIC_VIEW_BUILT_NOT_FULLY_AUDITED",
        "source_index_sha256": PINNED_INDEX_SHA,
        "choice_count": len(ready),
        "shard_count": len(inventory),
        "totals": totals,
        "readme": {"path": "expert-review/2026-09-26-final-page-review/arabic-existing/README.md", "bytes": start.stat().st_size, "sha256": sha256(start)},
        "shards": inventory,
    }
    receipt_path = BASE / "BUILD_RECEIPT.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": receipt["status"], "choices": len(ready), "shards": len(inventory), **totals, "readme_sha256": receipt["readme"]["sha256"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
