#!/usr/bin/env python3
"""Independent source, page-link, and Arabic-field readback of batch 31–38."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json"
BATCH = ROOT / "evidence/classical/terminology/ARABIC_REVIEW_BATCH_31_38_20260927.json"
MARKDOWN = ROOT / "expert-review/2026-09-26-final-page-review/BATCH_31_38_AR.md"
RECEIPT = ROOT / "expert-review/2026-09-26-final-page-review/BATCH_31_38_READBACK.json"
ERRATUM = ROOT / "evidence/classical/terminology/CANON_TRANSCRIPTION_ERRATUM_20260927.json"
DICTIONARY = ROOT.parent / "sources/DAM2018ENAR/معجم مصطلحات الرياضيات.pdf"
SOURCE_COMMIT = "86a4a7c11c0a0289ade28cb8f96acbacf9c01844"
EXPECTED_INDEX_SHA = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"
PDF_RELEASES = {
    "classical": "00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf",
    "international": "00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf",
    "machrek": "03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def east(number: int) -> str:
    return str(number).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))


def checked_source_url(location: dict) -> tuple[str, int]:
    recon = location["line_reconciliation"]
    if not recon["resolved"]:
        raise AssertionError(f"Unresolved batch location: {location['location_id']}")
    number = recon.get("current_line_start") or location["line_start"]
    if not isinstance(number, int) or number < 1:
        raise AssertionError(f"No positive current source line: {location['location_id']}")
    url = location["source_url"]
    if location["source_kind"] != "english":
        url = url.replace("/blob/main/", f"/blob/{SOURCE_COMMIT}/")
        path = ROOT / location["logical_path"]
        if digest(path) != location["current_sha256"].upper():
            raise AssertionError(f"Changed source bytes: {path}")
        lines = path.read_text(encoding="utf-8").splitlines()
        if number > len(lines):
            raise AssertionError(f"Source line past EOF: {path}:{number}")
    url = url.split("#L", 1)[0] + f"#L{number}"
    return url, number


def reader(page: dict) -> str:
    label = page["reader"]
    if label.startswith("الطبعة التراثية"):
        return "classical"
    if label.startswith("الطبعة الدولية"):
        return "international"
    if label.startswith("طبعة المشرق"):
        return "machrek"
    raise AssertionError(f"Unexpected reader label: {label}")


def main() -> None:
    if digest(INDEX) != EXPECTED_INDEX_SHA:
        raise AssertionError("The index is no longer the pinned release index")
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    erratum = json.loads(ERRATUM.read_text(encoding="utf-8"))
    markdown = MARKDOWN.read_text(encoding="utf-8")
    if digest(DICTIONARY) != batch["dictionary_source"]["pdf_sha256"]:
        raise AssertionError("Dictionary source bytes changed")
    if batch["source_index_sha256"] != EXPECTED_INDEX_SHA:
        raise AssertionError("Batch has another source index")
    records = batch["records"]
    if len(records) != 8 or len({x["decision_id"] for x in records}) != 8:
        raise AssertionError("Expected eight distinct choices")
    decisions = {d["decision_id"]: d for d in index["decisions"]}
    human_locations = 0
    source_links = 0
    page_links = 0
    exact_pages = 0
    fallback_pages = 0
    matched_location_ids = []
    for position, record in enumerate(records, 31):
        decision_id = record["decision_id"]
        decision = decisions[decision_id]
        if not decision["index_metadata"]["human_index_included"]:
            raise AssertionError(f"Not a human choice: {decision_id}")
        start = markdown.index(f"## {east(position)}. {record['surface_ar']}\n")
        end = markdown.find("\n## ", start + 4)
        card = markdown[start:end if end >= 0 else len(markdown)]
        if card.count(f"معرّف القرار: `{decision_id}`") != 1:
            raise AssertionError(f"Missing or repeated decision ID: {decision_id}")
        for field in ("sense_ar", "rationale_ar", "alternatives_ar", "question_ar"):
            value = record[field]
            if len(re.findall(r"[\u0600-\u06ff]", value)) < 8 or value not in card:
                raise AssertionError(f"Unlocalized or missing {field}: {decision_id}")
        for group in decision["index_metadata"]["occurrences"]:
            for location in group["locations"]:
                if not location.get("human_review_included"):
                    continue
                human_locations += 1
                matched_location_ids.append(location["location_id"])
                url, line_number = checked_source_url(location)
                # MSA links appear once per modern reader, otherwise once.
                copies = 2 if location["source_kind"] == "msa" else 1
                if card.count(f"[السطر {east(line_number)}]({url})") != copies:
                    raise AssertionError(f"Missing/repeated source link: {location['location_id']}")
                source_links += copies
                for page in location["page_evidence"]:
                    kind = reader(page)
                    for number in page["pdf_pages"][:3]:
                        token = f"{PDF_RELEASES[kind]}#page={number}"
                        if token not in card:
                            raise AssertionError(f"Missing reader page: {location['location_id']} {number}")
                        page_links += 1
                    if page["method"] == "synctex-exact":
                        exact_pages += 1
                    elif page["method"] == "unit-start-fallback":
                        fallback_pages += 1
                        if "صفحة بدء الوحدة فقط" not in card:
                            raise AssertionError(f"Unqualified approximate page: {location['location_id']}")
                    else:
                        raise AssertionError(f"Unexpected page method: {page['method']}")
    if human_locations != 30 or len(set(matched_location_ids)) != 30:
        raise AssertionError(f"Incomplete occurrence census: {human_locations}")
    if erratum["decision_id"] != records[5]["decision_id"]:
        raise AssertionError("Wrong dictionary erratum linkage")
    if any(item["visually_verified_normalized_transcription"] != "مجموعة غير عدودة" for item in erratum["entries"]):
        raise AssertionError("Dictionary erratum transcription drift")
    if "لا «غير معدودة» كما سبق أن نقل السجل خطأ" not in records[5]["rationale_ar"]:
        raise AssertionError("The batch fails to label the earlier false attribution")
    receipt = {
        "status": "PASS_LOCAL_ARABIC_BATCH_31_38",
        "source_index_sha256": EXPECTED_INDEX_SHA,
        "batch_sha256": digest(BATCH),
        "markdown_sha256": digest(MARKDOWN),
        "erratum_sha256": digest(ERRATUM),
        "dictionary_pdf_sha256": digest(DICTIONARY),
        "choices": len(records),
        "human_locations": human_locations,
        "source_line_links": source_links,
        "reader_page_links": page_links,
        "exact_reader_page_records": exact_pages,
        "unit_start_fallback_records": fallback_pages,
        "decision_ids": [x["decision_id"] for x in records],
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == "__main__":
    main()
