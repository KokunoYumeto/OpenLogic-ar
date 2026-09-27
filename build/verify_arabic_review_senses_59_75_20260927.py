#!/usr/bin/env python3
"""Independently read back 17 localized cards, all locations, and source bytes."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from verify_arabic_review_existing_20260927 import digest, east, source_url


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "expert-review/2026-09-26-final-page-review/arabic-senses-59-75"
OVERLAY = ROOT / "evidence/classical/terminology/ARABIC_SENSES_BATCH_59_75_20260927.json"
LOCATORS = ROOT / "evidence/classical/terminology/ENGLISH_LOCATOR_12_20260927.json"
INDEX = ROOT / "tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json"
EXPECTED_INDEX_SHA = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"


def main() -> None:
    receipt_path = BASE / "BUILD_RECEIPT.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    overlay = json.loads(OVERLAY.read_text(encoding="utf-8"))
    locator_overlay = json.loads(LOCATORS.read_text(encoding="utf-8"))
    locator_readback = json.loads((BASE / "ENGLISH_LOCATOR_READBACK.json").read_text(encoding="utf-8"))
    if digest(INDEX) != EXPECTED_INDEX_SHA or receipt["source_index_sha256"] != EXPECTED_INDEX_SHA:
        raise AssertionError("Review index drift")
    if digest(OVERLAY) != receipt["overlay_sha256"]:
        raise AssertionError("Localization overlay drift")
    locator_sha = digest(LOCATORS)
    if (
        locator_sha != receipt["english_locator_sha256"]
        or locator_sha != locator_readback["supplement_sha256"]
        or locator_overlay["source_index_sha256"] != EXPECTED_INDEX_SHA
        or locator_readback["status"] != "PASS_PINNED_ENGLISH_LOCATOR_12_WITH_NARY_GAP"
        or locator_readback["source_commit"] != locator_overlay["source_commit"]
        or locator_readback["source_files_http_200_and_hash_checked"] != len(locator_overlay["sources"])
    ):
        raise AssertionError("Pinned English locator supplement lacks matching source readback")
    ids = [record["decision_id"] for record in overlay["records"]]
    if len(ids) != 17 or len(set(ids)) != 17 or ids != receipt["decision_ids"]:
        raise AssertionError("Choice inventory drift")
    for name, key in (("README.md", "readme"), ("CARDS.md", "cards")):
        path = BASE / name
        if path.stat().st_size != receipt[key]["bytes"] or digest(path) != receipt[key]["sha256"]:
            raise AssertionError(f"Rendered artifact drift: {name}")
    readme = (BASE / "README.md").read_text(encoding="utf-8")
    if "OpenAI Codex — GPT-6 Sol" not in readme or "بمستوى جهد Ultra" not in readme:
        raise AssertionError("Reader-facing AI model/effort disclosure missing")
    body = (BASE / "CARDS.md").read_text(encoding="utf-8")
    markers = list(re.finditer(r"^الأصل الإنجليزي: .*? معرّف القرار: `([^`]+)`\.$", body, re.M))
    if [match.group(1) for match in markers] != ids:
        raise AssertionError("Rendered choices missing, repeated, or misordered")
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    by_id = {decision["decision_id"]: decision for decision in index["decisions"]}
    english_locations = {
        location["location_id"]: (decision["decision_id"], group["unit"]["unit_id"], location)
        for decision in index["decisions"]
        for group in decision["index_metadata"]["occurrences"]
        for location in group["locations"]
        if location["source_kind"] == "english"
    }
    locators_by_decision = {}
    locator_ids = set()
    for locator in locator_overlay["records"]:
        location_id = locator["english_location_id"]
        if location_id in locator_ids or location_id not in english_locations:
            raise AssertionError(f"Duplicate or unknown English location: {location_id}")
        locator_ids.add(location_id)
        decision_id, unit_id, source_location = english_locations[location_id]
        if (
            decision_id not in ids
            or unit_id != locator["unit_id"]
            or source_location["logical_path"] != locator["source_path"]
            or source_location["recorded_sha256"].upper() != locator_overlay["sources"][locator["source_path"]]
            or source_location["line_reconciliation"]["resolved"]
        ):
            raise AssertionError(f"English locator source binding drift: {location_id}")
        locators_by_decision.setdefault(decision_id, []).append(locator)
    if len(locator_ids) != receipt["english_locator_locations"] or len(locator_ids) != 12:
        raise AssertionError("English locator group census drift")
    counts = Counter()
    locator_line_counts = Counter()
    source_hashes = {}
    for position, marker in enumerate(markers):
        decision_id = marker.group(1)
        decision = by_id[decision_id]
        record = overlay["records"][position]
        card_begin = body.rfind("\n## ", 0, marker.start())
        card_end = body.find("\n## ", marker.end())
        if card_begin < 0:
            raise AssertionError(f"Card heading missing: {decision_id}")
        card = body[card_begin:card_end if card_end >= 0 else len(body)]
        if decision_id == "ar-classical-0701-0722-multi-conclusion" and "OLP-0710 — قواعد mG3i" not in card:
            raise AssertionError("OLP-0710 unit title was not localized")
        if decision_id == "ar-classical-0701-0722-side-formula" and "OLP-0711 — في القواعد والاشتقاقات" not in card:
            raise AssertionError("OLP-0711 unit title was not localized")
        for field in (record["sense_ar"], record.get("rationale_ar", decision["rationale"]), decision["expert_question"]):
            if field not in card:
                raise AssertionError(f"Missing Arabic explanation: {decision_id}")
        expected_context_markers = 0
        for locator in locators_by_decision.get(decision_id, []):
            if f"**أسطر الأصل الإنجليزي في {locator['unit_id']}:**" not in card or locator["relation_ar"] not in card:
                raise AssertionError(f"English locator explanation missing: {locator['english_location_id']}")
            source = (
                "https://github.com/OpenLogicProject/OpenLogic/blob/"
                + locator_overlay["source_commit"] + "/" + locator["source_path"]
            )
            for line in locator["lines"]:
                link = f"[{line['role_ar']}، السطر {east(line['line'])}]({source}#L{line['line']})"
                if card.count(link) != 1:
                    raise AssertionError(f"English source line missing or repeated: {locator['english_location_id']}: {line['line']}")
                locator_line_counts[line["kind"]] += 1
                if line["kind"] == "context_only":
                    if link + " (سياق للمقارنة، لا لفظ مطابق)" not in card:
                        raise AssertionError(f"Context-only qualifier missing: {locator['english_location_id']}")
                    expected_context_markers += 1
                elif line["kind"] != "direct":
                    raise AssertionError(f"Unknown English locator kind: {line['kind']}")
            question = locator.get("expert_question_ar")
            if question and f"**سؤال إضافي عن محاذاة الأصل:** {question}" not in card:
                raise AssertionError(f"Source-alignment expert question missing: {locator['english_location_id']}")
        if card.count(" (سياق للمقارنة، لا لفظ مطابق)") != expected_context_markers:
            raise AssertionError(f"Context-only qualifier census drift: {decision_id}")
        if card.count("**سؤال إضافي عن محاذاة الأصل:**") != (decision_id == "ar-classical-0701-0722-n-ary"):
            raise AssertionError(f"Unexpected source-alignment question count: {decision_id}")
        source_links = Counter()
        page_links = Counter()
        unresolved_count = 0
        unavailable_locations = 0
        for group in decision["index_metadata"]["occurrences"]:
            if not group.get("human_review_included"):
                continue
            for location in group["locations"]:
                if not location.get("human_review_included"):
                    continue
                counts["locations"] += 1
                link, resolved = source_url(location)
                source_links[link] += 1
                counts["resolved" if resolved else "unresolved"] += 1
                if not resolved:
                    unresolved_count += 1
                if location["source_kind"] != "english":
                    source = ROOT / location["logical_path"]
                    if source not in source_hashes:
                        source_hashes[source] = digest(source)
                    if source_hashes[source] != location["current_sha256"].upper():
                        raise AssertionError(f"Arabic source drift: {source}")
                has_page = False
                has_unavailable = False
                for page in location["page_evidence"]:
                    method = page["method"]
                    if method == "unavailable":
                        if page.get("pdf_pages"):
                            raise AssertionError(f"Unavailable record has a PDF page: {decision_id}")
                        has_unavailable = True
                        counts["unavailable_page_records"] += 1
                        continue
                    if method not in ("synctex-exact", "visual-text-exact", "unit-start-fallback"):
                        raise AssertionError(f"Unexpected PDF evidence method: {method}")
                    has_page = True
                    counts["fallback_pages" if method == "unit-start-fallback" else "exact_pages"] += 1
                    filename = {
                        "الطبعة التراثية": "00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf",
                        "الطبعة الدولية": "00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf",
                        "طبعة المشرق": "03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf",
                    }.get(page["reader"].split(" — ", 1)[0])
                    if filename is None:
                        raise AssertionError(f"Unknown reader label: {page['reader']}")
                    for number in page["pdf_pages"][:3]:
                        page_links[f"{filename}#page={number})"] += 1
                if has_unavailable and not has_page:
                    unavailable_locations += 1
        for link, expected in source_links.items():
            if card.count(link) != expected:
                raise AssertionError(f"Source link count mismatch: {decision_id}: {link}")
        for link, expected in page_links.items():
            if card.count(link) != expected:
                raise AssertionError(f"PDF link count mismatch: {decision_id}: {link}")
        if card.count("⚠ لم يثبت السطر الحالي") != unresolved_count:
            raise AssertionError(f"Unresolved-line warning count mismatch: {decision_id}")
        if card.count("⚠ لم تثبت صفحة PDF") != unavailable_locations:
            raise AssertionError(f"Unavailable-PDF warning count mismatch: {decision_id}")
    if {key: counts[key] for key in receipt["totals"]} != receipt["totals"]:
        raise AssertionError("Location or page totals differ from build receipt")
    if counts["unavailable_page_records"] != receipt["unavailable_page_records"]:
        raise AssertionError("Unavailable page count differs from build receipt")
    if (
        locator_line_counts["direct"] != receipt["english_locator_direct_lines"]
        or locator_line_counts["direct"] != locator_readback["direct_lines_checked"]
        or locator_line_counts["context_only"] != receipt["english_locator_context_lines"]
        or locator_line_counts["context_only"] != locator_readback["context_only_lines_checked"]
        or len(locator_ids) != locator_readback["grouped_english_locations"]
    ):
        raise AssertionError("Pinned English line census differs from rendered cards")
    result = {
        "status": "PASS_INDEPENDENT_ARABIC_SENSE_BATCH_59_75_READBACK",
        "source_index_sha256": EXPECTED_INDEX_SHA,
        "overlay_sha256": digest(OVERLAY),
        "english_locator_sha256": locator_sha,
        "english_locator_readback_sha256": digest(BASE / "ENGLISH_LOCATOR_READBACK.json"),
        "english_locator_locations": len(locator_ids),
        "english_locator_line_counts": dict(locator_line_counts),
        "choice_count": len(ids),
        "counts": dict(counts),
        "source_files_checked": len(source_hashes),
        "cards_sha256": digest(BASE / "CARDS.md"),
        "build_receipt_sha256": digest(receipt_path),
        "scope_ar": "تحقق مستقل من الشروح والوقوعات وروابط الأسطر والصفحات وبصمات المصادر العربية؛ لا يثبت المصطلحات الموروثة معجميًا من جديد.",
    }
    (BASE / "INDEPENDENT_READBACK.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
