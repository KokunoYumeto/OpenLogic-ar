#!/usr/bin/env python3
"""Independently read back the seven Arabic cards and pinned primary sources."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.request import Request, urlopen

from verify_arabic_review_existing_20260927 import digest, source_url
from verify_arabic_review_senses_76_85_20260927 import spans


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "expert-review/2026-09-26-final-page-review/arabic-senses-86-92"
OVERLAY = ROOT / "evidence/classical/terminology/ARABIC_SENSES_BATCH_86_92_20260927.json"
INDEX = ROOT / "tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json"
INDEX_SHA = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"
DICTIONARY = Path("C:/interlanguage-production/openlogic-arabic-dual-notation/sources/DAM2018ENAR/معجم مصطلحات الرياضيات.pdf")
EASTERN = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
PRIOR = (
    "ARABIC_PRIORITY_30_20260926.json",
    "ARABIC_REVIEW_BATCH_31_38_20260927.json",
    "ARABIC_SENSES_BATCH_39_58_20260927.json",
    "ARABIC_SENSES_BATCH_59_75_20260927.json",
    "ARABIC_SENSES_BATCH_76_85_20260927.json",
)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def main() -> None:
    overlay = json.loads(OVERLAY.read_text(encoding="utf-8"))
    receipt_path = BASE / "BUILD_RECEIPT.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if digest(INDEX) != INDEX_SHA or overlay["source_index_sha256"] != INDEX_SHA:
        raise AssertionError("Pinned review index drift")
    if receipt["source_index_sha256"] != INDEX_SHA or receipt["overlay_sha256"] != digest(OVERLAY):
        raise AssertionError("Build input binding drift")
    canon = overlay["canon_checks"]
    canon_ocr = ROOT / canon["dictionary_ocr_path"]
    if digest(canon_ocr) != canon["dictionary_ocr_sha256"] or digest(DICTIONARY) != canon["dictionary_pdf_sha256"]:
        raise AssertionError("Consulted dictionary identity drift")
    ocr = json.loads(canon_ocr.read_text(encoding="utf-8"))
    if not any(hit["pdf_page"] == 71 for hit in ocr["hits"]["binary relation"]):
        raise AssertionError("Dictionary relation attestation not located")
    if not any(hit["pdf_page"] == 139 for hit in ocr["hits"]["consistency condition"]):
        raise AssertionError("Dictionary consistency attestation not located")
    if any(ocr["hits"][term] for term in ("principal formula", "proof height", "regular proof")):
        raise AssertionError("Dictionary OCR gap caveat no longer matches search")

    records = overlay["records"]
    ids = [record["decision_id"] for record in records]
    prior_ids = {
        record["decision_id"]
        for name in PRIOR
        for record in json.loads((ROOT / "evidence/classical/terminology" / name).read_text(encoding="utf-8"))["records"]
    }
    if len(ids) != 7 or len(set(ids)) != 7 or ids != receipt["decision_ids"] or set(ids) & prior_ids:
        raise AssertionError("Seven-choice inventory is missing, duplicated or not new")
    readme_path = BASE / "README.md"
    if readme_path.stat().st_size != receipt["readme"]["bytes"] or digest(readme_path) != receipt["readme"]["sha256"]:
        raise AssertionError("Arabic README drift")
    readme = readme_path.read_text(encoding="utf-8")
    if "OpenAI Codex — GPT-6 Sol" not in readme or "بمستوى جهد Ultra" not in readme:
        raise AssertionError("Actual AI model/effort disclosure missing")
    if "٣٥٩ من ١٠٩٥" not in readme or "٣٠٥ اختيارات" not in readme:
        raise AssertionError("Local-versus-public coverage distinction missing")

    card_texts = []
    found_ids = []
    expected_partition = (ids[:4], ids[4:])
    for number, item in enumerate(receipt["cards"]):
        if item["path"] != f"CARDS-{number + 1}.md" or item["decision_ids"] != expected_partition[number]:
            raise AssertionError("Card partition/order drift")
        path = BASE / item["path"]
        if path.stat().st_size != item["bytes"] or digest(path) != item["sha256"] or path.stat().st_size > 230_000:
            raise AssertionError(f"Card byte identity or readable-size cap drift: {path.name}")
        body = path.read_text(encoding="utf-8")
        card_texts.append(body)
        found_ids.extend(re.findall(r"^الأصل الإنجليزي: .*? معرّف القرار: `([^`]+)`\.$", body, re.M))
    if found_ids != ids:
        raise AssertionError("Rendered cards are missing, duplicated or misordered")
    if not all(f"[البطاقات {str(number).translate(EASTERN)}–{str(end).translate(EASTERN)}]({item['path']})" in readme for number, end, item in ((1, 4, receipt["cards"][0]), (5, 7, receipt["cards"][1]))):
        raise AssertionError("README does not link both reader files")

    index = json.loads(INDEX.read_text(encoding="utf-8"))
    by_id = {decision["decision_id"]: decision for decision in index["decisions"]}
    frozen_english_hashes: dict[str, str] = {}
    arabic_source_hashes: dict[Path, str] = {}
    counts = Counter()
    for position, record in enumerate(records):
        decision_id = record["decision_id"]
        decision = by_id[decision_id]
        body = card_texts[0 if position < 4 else 1]
        marker_text = f"معرّف القرار: `{decision_id}`."
        marker = body.index(marker_text)
        begin = body.rfind("\n## ", 0, marker)
        end = body.find("\n## ", marker)
        if begin < 0:
            raise AssertionError(f"Card heading missing: {decision_id}")
        card = body[begin:end if end >= 0 else len(body)]
        for field in (record["sense_ar"], record["canon_note_ar"], decision["rationale"], decision["expert_question"]):
            if field not in card:
                raise AssertionError(f"Gloss or inherited review field missing: {decision_id}")
        if card.count("**كل وقوع مسجل لهذا القرار:**") != 1:
            raise AssertionError(f"Occurrence heading missing or repeated: {decision_id}")
        expected_paths = {
            location["logical_path"]: location["recorded_sha256"].upper()
            for group in decision["index_metadata"]["occurrences"]
            for location in group["locations"]
            if location["source_kind"] == "english"
        }
        for passage in record["source_passages"]:
            path = passage["path"]
            if path not in expected_paths:
                raise AssertionError(f"Passage is not bound to decision source: {decision_id}: {path}")
            existing = frozen_english_hashes.setdefault(path, expected_paths[path])
            if existing != expected_paths[path]:
                raise AssertionError(f"Inconsistent pinned English file hash: {path}")
            source = "https://github.com/OpenLogicProject/OpenLogic/blob/" + overlay["english_source_commit"] + "/" + path
            for first, last in spans(passage["lines"]):
                fragment = f"#L{first}" + (f"-L{last}" if last != first else "")
                label = f"{first}" + (f"-{last}" if last != first else "")
                link = f"[الأسطر {label.translate(EASTERN)}]({source}{fragment})"
                if card.count(link) != 1:
                    raise AssertionError(f"Pinned English passage link missing or repeated: {decision_id}: {link}")
                counts["source_spans"] += 1
            if passage["relevance_ar"].rstrip(".") not in card:
                raise AssertionError(f"Passage relevance note missing: {decision_id}")

        source_links = Counter()
        page_links = Counter()
        unresolved = unavailable = 0
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
                unresolved += not resolved
                if location["source_kind"] != "english":
                    source = ROOT / location["logical_path"]
                    if source not in arabic_source_hashes:
                        arabic_source_hashes[source] = digest(source)
                    if arabic_source_hashes[source] != location["current_sha256"].upper():
                        raise AssertionError(f"Current Arabic source hash drift: {source}")
                any_page = any_unavailable = False
                for page in location["page_evidence"]:
                    method = page["method"]
                    if method == "unavailable":
                        if page.get("pdf_pages"):
                            raise AssertionError("Unavailable page record has a PDF number")
                        any_unavailable = True
                        counts["unavailable_page_records"] += 1
                        continue
                    if method not in ("synctex-exact", "visual-text-exact", "unit-start-fallback"):
                        raise AssertionError(f"Unknown page evidence method: {method}")
                    any_page = True
                    counts["fallback_pages" if method == "unit-start-fallback" else "exact_pages"] += 1
                    filename = {
                        "الطبعة التراثية": "00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf",
                        "الطبعة الدولية": "00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf",
                        "طبعة المشرق": "03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf",
                    }.get(page["reader"].split(" — ", 1)[0])
                    if filename is None:
                        raise AssertionError(f"Unknown reader: {page['reader']}")
                    for number in page["pdf_pages"][:3]:
                        page_links[f"{filename}#page={number})"] += 1
                unavailable += any_unavailable and not any_page
        for link, expected in source_links.items():
            if card.count(link) != expected:
                raise AssertionError(f"Occurrence source-link census drift: {decision_id}: {link}")
        for link, expected in page_links.items():
            if card.count(link) != expected:
                raise AssertionError(f"PDF page-link census drift: {decision_id}: {link}")
        if card.count("⚠ لم يثبت السطر الحالي") != unresolved:
            raise AssertionError(f"Unresolved source-line warning drift: {decision_id}")
        if card.count("⚠ لم تثبت صفحة PDF") != unavailable:
            raise AssertionError(f"Unavailable PDF warning drift: {decision_id}")

    for path, expected_hash in frozen_english_hashes.items():
        url = "https://raw.githubusercontent.com/OpenLogicProject/OpenLogic/" + overlay["english_source_commit"] + "/" + path
        with urlopen(Request(url, headers={"User-Agent": "OpenLogic-Arabic-review-verifier/1"}), timeout=20) as response:
            if response.status != 200:
                raise AssertionError(f"Pinned English source HTTP error: {path}")
            raw = response.read(200_001)
        if len(raw) > 200_000 or b"\r" in raw or sha_bytes(raw.replace(b"\n", b"\r\n")) != expected_hash:
            raise AssertionError(f"Pinned English source hash/size/line endings drift: {path}")
        lines = raw.decode("utf-8").splitlines()
        for record in records:
            for passage in record["source_passages"]:
                if passage["path"] != path:
                    continue
                ranges = spans(passage["lines"])
                if any(last > len(lines) for _first, last in ranges):
                    raise AssertionError(f"Pinned English source span out of range: {path}")
                excerpt = "\n".join("\n".join(lines[first - 1:last]) for first, last in ranges)
                if passage["needle"].casefold() not in excerpt.casefold():
                    raise AssertionError(f"Source span does not support stated keyword: {path}: {passage['needle']}")
    if {key: counts[key] for key in receipt["totals"]} != receipt["totals"]:
        raise AssertionError("Occurrence/page census differs from render receipt")
    result = {
        "status": "PASS_INDEPENDENT_ARABIC_SENSE_BATCH_86_92_READBACK",
        "source_index_sha256": INDEX_SHA,
        "overlay_sha256": digest(OVERLAY),
        "choice_count": len(ids),
        "counts": dict(counts),
        "arabic_source_files_checked": len(arabic_source_hashes),
        "english_files_http_200_hash_checked": len(frozen_english_hashes),
        "dictionary_ocr_sha256": digest(canon_ocr),
        "dictionary_pdf_sha256": digest(DICTIONARY),
        "card_sha256": [digest(BASE / item["path"]) for item in receipt["cards"]],
        "build_receipt_sha256": digest(receipt_path),
        "scope_ar": "تحقق مستقل من الشروح والمواضع وروابط الأسطر والصفحات وبصمات الملفات؛ المصطلحات الموروثة تظل مفتوحة للتصحيح.",
    }
    (BASE / "INDEPENDENT_READBACK.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    main()
