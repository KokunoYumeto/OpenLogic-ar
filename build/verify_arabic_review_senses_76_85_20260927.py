#!/usr/bin/env python3
"""Independently verify ten Arabic cards and their pinned source/canon evidence."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.request import Request, urlopen

from verify_arabic_review_existing_20260927 import digest, source_url


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "expert-review/2026-09-26-final-page-review/arabic-senses-76-85"
OVERLAY = ROOT / "evidence/classical/terminology/ARABIC_SENSES_BATCH_76_85_20260927.json"
INDEX = ROOT / "tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json"
EXPECTED_INDEX_SHA = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"
DICTIONARY = Path("C:/interlanguage-production/openlogic-arabic-dual-notation/sources/DAM2018ENAR/معجم مصطلحات الرياضيات.pdf")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def spans(value: str) -> list[tuple[int, int]]:
    out = []
    for part in value.split(","):
        match = re.fullmatch(r"(\d+)(?:-(\d+))?", part.strip())
        if not match:
            raise AssertionError(f"Malformed source line span: {part}")
        first = int(match.group(1))
        last = int(match.group(2) or first)
        if not 1 <= first <= last:
            raise AssertionError(f"Backwards source line span: {part}")
        out.append((first, last))
    return out


def main() -> None:
    overlay = json.loads(OVERLAY.read_text(encoding="utf-8"))
    receipt_path = BASE / "BUILD_RECEIPT.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if digest(INDEX) != EXPECTED_INDEX_SHA or overlay["source_index_sha256"] != EXPECTED_INDEX_SHA:
        raise AssertionError("Pinned review index drift")
    if receipt["source_index_sha256"] != EXPECTED_INDEX_SHA or receipt["overlay_sha256"] != digest(OVERLAY):
        raise AssertionError("Build receipt input binding drift")
    canon = overlay["canon_checks"]
    canon_ocr = ROOT / canon["dictionary_ocr_path"]
    if digest(canon_ocr) != canon["dictionary_ocr_sha256"] or digest(DICTIONARY) != canon["dictionary_pdf_sha256"]:
        raise AssertionError("Consulted dictionary identity drift")
    ocr = json.loads(canon_ocr.read_text(encoding="utf-8"))
    if (
        not any(hit["pdf_page"] == 477 for hit in ocr["hits"]["natural number"])
        or not any(hit["pdf_page"] == 445 for hit in ocr["hits"]["mathematical induction"])
        or any(ocr["hits"][key] for key in (
            "successor function", "premise", "sequent", "structural rule",
            "invertible rule", "satisfiable", "second-order logic",
        ))
    ):
        raise AssertionError("Bounded dictionary evidence differs from stated caveat")
    records = overlay["records"]
    ids = [record["decision_id"] for record in records]
    if len(ids) != 10 or len(set(ids)) != 10 or ids != receipt["decision_ids"]:
        raise AssertionError("Ten-choice inventory drift")
    for name, key in (("README.md", "readme"), ("CARDS.md", "cards")):
        path = BASE / name
        if path.stat().st_size != receipt[key]["bytes"] or digest(path) != receipt[key]["sha256"]:
            raise AssertionError(f"Rendered artifact drift: {name}")
    readme = (BASE / "README.md").read_text(encoding="utf-8")
    if "OpenAI Codex — GPT-6 Sol" not in readme or "بمستوى جهد Ultra" not in readme:
        raise AssertionError("AI model and effort disclosure missing")
    body = (BASE / "CARDS.md").read_text(encoding="utf-8")
    markers = list(re.finditer(r"^الأصل الإنجليزي: .*? معرّف القرار: `([^`]+)`\.$", body, re.M))
    if [marker.group(1) for marker in markers] != ids:
        raise AssertionError("Card inventory missing, repeated or misordered")
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    by_id = {decision["decision_id"]: decision for decision in index["decisions"]}
    frozen_english_hashes = {}
    source_hashes = {}
    counts = Counter()
    for position, marker in enumerate(markers):
        record = records[position]
        decision_id = marker.group(1)
        decision = by_id[decision_id]
        begin = body.rfind("\n## ", 0, marker.start())
        end = body.find("\n## ", marker.end())
        if begin < 0:
            raise AssertionError(f"Card heading missing: {decision_id}")
        card = body[begin:end if end >= 0 else len(body)]
        for field in (record["sense_ar"], record["canon_note_ar"], decision["rationale"], decision["expert_question"]):
            if field not in card:
                raise AssertionError(f"Arabic gloss or inherited review field missing: {decision_id}")
        expected_paths = {
            location["logical_path"]: location["recorded_sha256"].upper()
            for group in decision["index_metadata"]["occurrences"]
            for location in group["locations"]
            if location["source_kind"] == "english"
        }
        for passage in record["source_passages"]:
            path = passage["path"]
            if path not in expected_paths:
                raise AssertionError(f"Passage not bound to decision source: {decision_id}: {path}")
            existing = frozen_english_hashes.setdefault(path, expected_paths[path])
            if existing != expected_paths[path]:
                raise AssertionError(f"Inconsistent frozen English hash: {path}")
            source = "https://github.com/OpenLogicProject/OpenLogic/blob/" + overlay["english_source_commit"] + "/" + path
            for part in passage["lines"].split(","):
                first, last = spans(part.strip())[0]
                fragment = f"#L{first}" + (f"-L{last}" if last != first else "")
                label = part.strip().translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))
                link = f"[الأسطر {label}]({source}{fragment})"
                if card.count(link) != 1:
                    raise AssertionError(f"Source passage link missing or repeated: {decision_id}: {part}")
                counts["source_spans"] += 1
            if passage["relevance_ar"] not in card:
                raise AssertionError(f"Source passage relevance missing: {decision_id}")
        source_links = Counter()
        page_links = Counter()
        unresolved = 0
        unavailable = 0
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
                    if source not in source_hashes:
                        source_hashes[source] = digest(source)
                    if source_hashes[source] != location["current_sha256"].upper():
                        raise AssertionError(f"Current Arabic source drift: {source}")
                any_page = False
                any_unavailable = False
                for page in location["page_evidence"]:
                    method = page["method"]
                    if method == "unavailable":
                        if page.get("pdf_pages"):
                            raise AssertionError("Unavailable page has assigned PDF number")
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
            raise AssertionError(f"Unresolved-line warnings drift: {decision_id}")
        if card.count("⚠ لم تثبت صفحة PDF") != unavailable:
            raise AssertionError(f"Unavailable-page warnings drift: {decision_id}")
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
                    raise AssertionError(f"Source span out of range: {path}")
                text = "\n".join("\n".join(lines[first - 1:last]) for first, last in ranges)
                if passage["needle"].casefold() not in text.casefold():
                    raise AssertionError(f"Source passage lacks stated concept: {path}: {passage['needle']}")
    if {key: counts[key] for key in receipt["totals"]} != receipt["totals"]:
        raise AssertionError("Occurrence/page census differs from build receipt")
    result = {
        "status": "PASS_INDEPENDENT_ARABIC_SENSE_BATCH_76_85_READBACK",
        "source_index_sha256": EXPECTED_INDEX_SHA,
        "overlay_sha256": digest(OVERLAY),
        "choice_count": len(ids),
        "counts": dict(counts),
        "arabic_source_files_checked": len(source_hashes),
        "english_files_http_200_hash_checked": len(frozen_english_hashes),
        "dictionary_ocr_sha256": digest(canon_ocr),
        "dictionary_pdf_sha256": digest(DICTIONARY),
        "cards_sha256": digest(BASE / "CARDS.md"),
        "build_receipt_sha256": digest(receipt_path),
        "scope_ar": "تحقق مستقل من الشروح والمواقع وروابط الأسطر والصفحات وبصمات المصدر؛ أما الصياغة الاصطلاحية الموروثة فتظل قابلة لمراجعة الخبير.",
    }
    (BASE / "INDEPENDENT_READBACK.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    main()
