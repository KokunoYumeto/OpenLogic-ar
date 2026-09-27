#!/usr/bin/env python3
"""Independently read back the 20 localized sense cards and every locator."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from verify_arabic_review_existing_20260927 import digest, source_url


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "expert-review/2026-09-26-final-page-review/arabic-senses-39-58"
OVERLAY = ROOT / "evidence/classical/terminology/ARABIC_SENSES_BATCH_39_58_20260927.json"
LOCATORS = ROOT / "evidence/classical/terminology/ENGLISH_LOCATOR_8_20260927.json"
INDEX = ROOT / "tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json"
PINNED_INDEX_SHA = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"


def main() -> None:
    receipt_path = BASE / "BUILD_RECEIPT.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    overlay = json.loads(OVERLAY.read_text(encoding="utf-8"))
    locators = json.loads(LOCATORS.read_text(encoding="utf-8"))
    if digest(INDEX) != PINNED_INDEX_SHA or receipt["source_index_sha256"] != PINNED_INDEX_SHA:
        raise AssertionError("Pinned index drift")
    if digest(OVERLAY) != receipt["overlay_sha256"]:
        raise AssertionError("Overlay drift")
    if digest(LOCATORS) != receipt["english_locator_sha256"]:
        raise AssertionError("English locator supplement drift")
    locator_by_id = {item["decision_id"]: item for item in locators["records"]}
    if len(locator_by_id) != receipt["english_locator_decisions"] or sum(
        len(item["lines"]) for item in locator_by_id.values()
    ) != receipt["english_locator_lines"]:
        raise AssertionError("English locator supplement census drift")
    records = overlay["records"]
    ids = [record["decision_id"] for record in records]
    if len(ids) != 20 or len(set(ids)) != 20 or ids != receipt["decision_ids"]:
        raise AssertionError("Choice inventory drift")
    for filename, key in (("README.md", "readme"), ("CARDS.md", "cards")):
        path = BASE / filename
        if path.stat().st_size != receipt[key]["bytes"] or digest(path) != receipt[key]["sha256"]:
            raise AssertionError(f"Rendered bytes drift: {filename}")
    start = (BASE / "README.md").read_text(encoding="utf-8")
    if "OpenAI Codex — GPT-6 Sol" not in start or "بمستوى جهد Ultra" not in start:
        raise AssertionError("New AI localization lacks exact reader-facing model/effort disclosure")
    body = (BASE / "CARDS.md").read_text(encoding="utf-8")
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    by_id = {decision["decision_id"]: decision for decision in index["decisions"]}
    markers = list(re.finditer(r"^الأصل الإنجليزي: .*? معرّف القرار: `([^`]+)`\.$", body, re.M))
    if [match.group(1) for match in markers] != ids:
        raise AssertionError("Rendered choice order or count drift")
    counts = Counter()
    source_hash_cache = {}
    for position, marker in enumerate(markers):
        decision_id = marker.group(1)
        decision = by_id[decision_id]
        localized_sense = records[position]["sense_ar"]
        card_begin = body.rfind("\n## ", 0, marker.start())
        card_end = body.find("\n## ", marker.end())
        if card_begin < 0:
            raise AssertionError(f"Missing card heading: {decision_id}")
        card = body[card_begin:card_end if card_end >= 0 else len(body)]
        if localized_sense not in card or any(
            decision[field] not in card for field in ("rationale", "expert_question")
        ):
            raise AssertionError(f"Missing localized or inherited explanation: {decision_id}")
        links = Counter()
        pages = Counter()
        unavailable_locations = 0
        for group in decision["index_metadata"]["occurrences"]:
            if not group.get("human_review_included"):
                continue
            for location in group["locations"]:
                if not location.get("human_review_included"):
                    continue
                counts["locations"] += 1
                link, resolved = source_url(location)
                links[link] += 1
                counts["resolved" if resolved else "unresolved"] += 1
                if location["source_kind"] != "english":
                    source = ROOT / location["logical_path"]
                    if source not in source_hash_cache:
                        source_hash_cache[source] = digest(source)
                    if source_hash_cache[source] != location["current_sha256"].upper():
                        raise AssertionError(f"Source file drift: {source}")
                if not resolved:
                    counts["unresolved_warnings_expected"] += 1
                location_has_page = False
                location_unavailable = False
                for page in location["page_evidence"]:
                    method = page["method"]
                    if method == "unavailable":
                        if page.get("pdf_pages"):
                            raise AssertionError(f"Unavailable page has number: {decision_id}")
                        location_unavailable = True
                        counts["unavailable_page_records"] += 1
                        continue
                    if method not in ("synctex-exact", "visual-text-exact", "unit-start-fallback"):
                        raise AssertionError(f"Unexpected page method: {method}")
                    location_has_page = True
                    counts["fallback_pages" if method == "unit-start-fallback" else "exact_pages"] += 1
                    filename = {
                        "الطبعة التراثية": "00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf",
                        "الطبعة الدولية": "00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf",
                        "طبعة المشرق": "03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf",
                    }.get(page["reader"].split(" — ", 1)[0])
                    if filename is None:
                        raise AssertionError(f"Unknown reader: {page['reader']}")
                    for number in page["pdf_pages"][:3]:
                        pages[f"{filename}#page={number})"] += 1
                if location_unavailable and not location_has_page:
                    unavailable_locations += 1
        for link, expected in links.items():
            if card.count(link) != expected:
                raise AssertionError(f"Missing or duplicate source locator: {decision_id}: {link}")
        for page, expected in pages.items():
            if card.count(page) != expected:
                raise AssertionError(f"Missing or duplicate PDF locator: {decision_id}: {page}")
        if card.count("⚠ لم يثبت السطر الحالي") != sum(
            not location["line_reconciliation"]["resolved"]
            for group in decision["index_metadata"]["occurrences"]
            for location in group["locations"] if location.get("human_review_included")
        ):
            raise AssertionError(f"Unresolved source warning count drift: {decision_id}")
        if card.count("⚠ لم تثبت صفحة PDF") != unavailable_locations:
            raise AssertionError(f"Unavailable PDF warning count drift: {decision_id}")
        if decision_id in locator_by_id:
            supplement = locator_by_id[decision_id]
            if supplement["alignment_ar"] not in card:
                raise AssertionError(f"English alignment qualification missing: {decision_id}")
            for candidate in supplement["lines"]:
                url = (
                    "https://github.com/OpenLogicProject/OpenLogic/blob/"
                    + locators["source_commit"] + "/" + supplement["source_path"]
                    + f"#L{candidate['line']}"
                )
                if card.count(url) != 1:
                    raise AssertionError(f"English candidate link missing or repeated: {decision_id}: {url}")
    expected_totals = {key: counts[key] for key in receipt["totals"]}
    if expected_totals != receipt["totals"]:
        raise AssertionError(f"Occurrence totals drift: {expected_totals} != {receipt['totals']}")
    result = {
        "status": "PASS_INDEPENDENT_ARABIC_SENSE_BATCH_READBACK",
        "source_index_sha256": PINNED_INDEX_SHA,
        "overlay_sha256": digest(OVERLAY),
        "english_locator_sha256": digest(LOCATORS),
        "english_locator_decisions": len(locator_by_id),
        "english_locator_lines": receipt["english_locator_lines"],
        "choice_count": len(ids),
        "counts": dict(counts),
        "source_files_checked": len(source_hash_cache),
        "cards_sha256": digest(BASE / "CARDS.md"),
        "build_receipt_sha256": digest(receipt_path),
        "scope_ar": "فحص البطاقات والمواضع والملفات والصفحات؛ لا يزعم اعتماد المصطلحات أو فحصها معجميًا من جديد.",
    }
    (BASE / "INDEPENDENT_READBACK.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
