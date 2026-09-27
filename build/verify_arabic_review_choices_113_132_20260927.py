#!/usr/bin/env python3
"""Independent source, canon, location and byte readback for twenty relation cards."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

from stream_expert_review_decisions import iter_decisions
from verify_arabic_review_existing_20260927 import digest, source_url
from verify_arabic_review_senses_76_85_20260927 import spans


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "expert-review/2026-09-26-final-page-review/arabic-decisions-113-132"
OVERLAY = ROOT / "evidence/classical/terminology/ARABIC_REVIEW_BATCH_113_132_20260927.json"
INDEX = ROOT / "tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json"
INDEX_SHA = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"
EASTERN = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
PRIOR = (
    "ARABIC_PRIORITY_30_20260926.json",
    "ARABIC_REVIEW_BATCH_31_38_20260927.json",
    "ARABIC_SENSES_BATCH_39_58_20260927.json",
    "ARABIC_SENSES_BATCH_59_75_20260927.json",
    "ARABIC_SENSES_BATCH_76_85_20260927.json",
    "ARABIC_SENSES_BATCH_86_92_20260927.json",
    "ARABIC_REVIEW_BATCH_93_112_20260927.json",
)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def arabic_dominant(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    arabic = sum("\u0600" <= character <= "\u06ff" for character in value)
    latin = sum("A" <= character <= "Z" or "a" <= character <= "z" for character in value)
    return arabic >= 15 and arabic > latin


def main() -> None:
    overlay = json.loads(OVERLAY.read_text(encoding="utf-8"))
    receipt = json.loads((BASE / "BUILD_RECEIPT.json").read_text(encoding="utf-8"))
    if digest(INDEX) != INDEX_SHA or receipt["source_index_sha256"] != INDEX_SHA:
        raise AssertionError("Frozen index identity drift")
    if overlay["source_index_sha256"] != INDEX_SHA or receipt["overlay_sha256"] != digest(OVERLAY):
        raise AssertionError("Overlay identity drift")
    canon = overlay["canon"]
    pdf = Path(canon["pdf_path"])
    if digest(pdf) != canon["pdf_sha256"] or canon["printed_page_offset"] != -12:
        raise AssertionError("Dictionary PDF identity or page offset drift")
    if set(canon["visually_checked_pdf_pages"]) != {42, 52, 71, 138, 228, 602, 706, 732}:
        raise AssertionError("Inspected dictionary-page inventory drift")

    records = overlay["records"]
    ids = [record["decision_id"] for record in records]
    if len(ids) != 20 or len(set(ids)) != 20 or receipt["decision_ids"] != ids:
        raise AssertionError("Twenty-choice inventory mismatch")
    wanted = set(ids)
    decisions: dict[str, dict] = {}
    already_arabic: set[str] = set()
    for decision in iter_decisions(INDEX):
        if decision["index_metadata"]["human_index_included"] and all(
            arabic_dominant(decision.get(key)) for key in ("sense", "rationale", "expert_question")
        ):
            already_arabic.add(decision["decision_id"])
        if decision["decision_id"] in wanted:
            decisions[decision["decision_id"]] = decision
    if set(decisions) != wanted:
        raise AssertionError("Choice absent from frozen index")
    prior_ids = {
        record["decision_id"]
        for name in PRIOR
        for record in json.loads((ROOT / "evidence/classical/terminology" / name).read_text(encoding="utf-8"))["records"]
    }
    if len(already_arabic) != 267 or wanted & (already_arabic | prior_ids):
        raise AssertionError("Choice already represented in Arabic")

    readme = BASE / "README.md"
    if readme.stat().st_size != receipt["readme"]["bytes"] or digest(readme) != receipt["readme"]["sha256"]:
        raise AssertionError("Arabic entry byte identity drift")
    intro = readme.read_text(encoding="utf-8")
    if not all(token in intro for token in ("GPT-6 Sol", "Ultra", "٣٩٩ من ١٠٩٥", "٣٥٩ من ١٠٩٥")):
        raise AssertionError("Model disclosure or honest local/public count missing")
    if "لم تُغيَّر نصوص الطبعات" not in intro or "لم تُنشر بعد" not in intro:
        raise AssertionError("Local-only and no-edition-change status omitted")

    partition = (ids[:2], ids[2:18], ids[18:])
    card_by_id: dict[str, str] = {}
    for n, item in enumerate(receipt["cards"], 1):
        if item["path"] != f"CARDS-{n}.md" or item["decision_ids"] != partition[n - 1]:
            raise AssertionError("Card partition or order mismatch")
        path = BASE / item["path"]
        if path.stat().st_size != item["bytes"] or digest(path) != item["sha256"] or path.stat().st_size > 230_000:
            raise AssertionError(f"Card byte identity or browseability failed: {path}")
        if f"]({item['path']})" not in intro:
            raise AssertionError(f"Entry page does not link {item['path']}")
        body = path.read_text(encoding="utf-8")
        matches = list(re.finditer(r"^الأصل الإنجليزي: .*? معرّف القرار: `([^`]+)`\.$", body, re.M))
        if [match.group(1) for match in matches] != item["decision_ids"]:
            raise AssertionError(f"Missing or repeated card: {path.name}")
        for match in matches:
            begin = body.rfind("\n## ", 0, match.start())
            end = body.find("\n## ", match.end())
            if begin < 0:
                raise AssertionError("Card heading absent")
            card_by_id[match.group(1)] = body[begin:end if end >= 0 else len(body)]
    if set(card_by_id) != wanted:
        raise AssertionError("Rendered choice inventory incomplete")

    english_hashes: dict[str, str] = {}
    arabic_hashes: dict[Path, str] = {}
    counters = Counter()
    dictionary_filename = quote(pdf.name)
    cited_pages: set[int] = set()
    for record in records:
        decision_id = record["decision_id"]
        decision = decisions[decision_id]
        if not decision["index_metadata"]["human_index_included"]:
            raise AssertionError(f"Non-human choice rendered: {decision_id}")
        card = card_by_id[decision_id]
        displayed = decision["review_display"]["chosen_arabic"].replace("\\-", "")
        if not card.startswith(f"\n## {displayed}\n") or "\\-" in displayed:
            raise AssertionError(f"Reader heading does not normalize discretionary TeX: {decision_id}")
        for field in ("sense_ar", "rationale_ar", "expert_question_ar", "source_relevance_ar",
                      "canon_note_ar", "confidence_ar"):
            if not arabic_dominant(record[field]) or record[field] not in card:
                raise AssertionError(f"Missing exact Arabic {field}: {decision_id}")
        if card.count("**كل وقوع مسجل لهذا القرار:**") != 1:
            raise AssertionError(f"Occurrence heading missing or repeated: {decision_id}")
        if "لا انعكاسية ولا لا انعكاسية" in card or "الانعكاسية السالبة" in card:
            raise AssertionError("Known ungrounded irreflexivity phrasing resurfaced")
        for alternative in record["alternatives_ar"]:
            if alternative not in card:
                raise AssertionError(f"Named alternative omitted: {decision_id}")

        locations = [
            location for group in decision["index_metadata"]["occurrences"]
            for location in group["locations"] if location.get("human_review_included")
        ]
        english = [location for location in locations if location["source_kind"] == "english"]
        if len(english) != 1:
            raise AssertionError(f"Expected one pinned English location: {decision_id}")
        source_path = english[0]["logical_path"]
        expected_hash = english[0]["recorded_sha256"].upper()
        if source_path in english_hashes and english_hashes[source_path] != expected_hash:
            raise AssertionError("Contradictory pinned English hashes")
        english_hashes[source_path] = expected_hash
        source_url_base = ("https://github.com/OpenLogicProject/OpenLogic/blob/"
                           + overlay["english_source_commit"] + "/" + source_path)
        first_source_line = english[0]["line_reconciliation"]["current_line_start"]
        cover = False
        for first, last in spans(record["source_lines"]):
            cover |= first <= first_source_line <= last
            label = (str(first) + (f"-{last}" if first != last else "")).translate(EASTERN)
            fragment = f"#L{first}" + (f"-L{last}" if first != last else "")
            if f"[الأسطر {label}]({source_url_base}{fragment})" not in card:
                raise AssertionError(f"Consulted original span link missing: {decision_id}")
            counters["original_spans"] += 1
        if not cover:
            raise AssertionError(f"Consulted source range misses choice: {decision_id}")
        for page in record["canon_pdf_pages"]:
            if page not in canon["visually_checked_pdf_pages"]:
                raise AssertionError(f"Uninspected dictionary page cited: {page}")
            cited_pages.add(page)
            url = f"https://archive.org/download/DAM2018ENAR/{dictionary_filename}#page={page}"
            if url not in card:
                raise AssertionError(f"Dictionary page link absent: {decision_id}: {page}")
            counters["canon_page_links"] += 1

        expected_links = Counter()
        expected_pdf_links = Counter()
        unresolved = unavailable = 0
        for location in locations:
            counters["locations"] += 1
            link, resolved = source_url(location)
            expected_links[link] += 1
            counters["resolved" if resolved else "unresolved"] += 1
            unresolved += not resolved
            if location["source_kind"] != "english":
                path = ROOT / location["logical_path"]
                arabic_hashes.setdefault(path, digest(path))
                if arabic_hashes[path] != location["current_sha256"].upper():
                    raise AssertionError(f"Target source changed: {path}")
            any_page = any_unavailable = False
            for page in location["page_evidence"]:
                if page["method"] == "unavailable":
                    if page.get("pdf_pages"):
                        raise AssertionError("Unavailable page falsely has numbers")
                    any_unavailable = True
                    continue
                if page["method"] not in ("synctex-exact", "visual-text-exact", "unit-start-fallback"):
                    raise AssertionError("Unknown PDF locator method")
                any_page = True
                counters["fallback_pages" if page["method"] == "unit-start-fallback" else "exact_pages"] += 1
                filename = {
                    "الطبعة التراثية": "00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf",
                    "الطبعة الدولية": "00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf",
                    "طبعة المشرق": "03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf",
                }.get(page["reader"].split(" — ", 1)[0])
                if filename is None:
                    raise AssertionError(f"Unknown PDF reader: {page['reader']}")
                for number in page["pdf_pages"][:3]:
                    expected_pdf_links[f"{filename}#page={number})"] += 1
            unavailable += any_unavailable and not any_page
        for link, count in expected_links.items():
            if card.count(link) != count:
                raise AssertionError(f"Occurrence link census mismatch: {decision_id}: {link}")
        for link, count in expected_pdf_links.items():
            if card.count(link) != count:
                raise AssertionError(f"PDF page census mismatch: {decision_id}: {link}")
        if card.count("⚠ لم يثبت السطر الحالي") != unresolved:
            raise AssertionError("Unresolved-line warning missing")
        if card.count("⚠ لم تثبت صفحة PDF") != unavailable:
            raise AssertionError("Unavailable-PDF warning missing")
    if cited_pages != set(canon["visually_checked_pdf_pages"]):
        raise AssertionError("An inspected dictionary page was never cited")

    for source_path, expected_hash in english_hashes.items():
        url = ("https://raw.githubusercontent.com/OpenLogicProject/OpenLogic/"
               + overlay["english_source_commit"] + "/" + source_path)
        with urlopen(Request(url, headers={"User-Agent": "OpenLogic-Arabic-review-verifier/1"}), timeout=20) as response:
            if response.status != 200:
                raise AssertionError(f"Pinned source unavailable: {source_path}")
            raw = response.read(200_001)
        if len(raw) > 200_000 or b"\r" in raw or sha_bytes(raw.replace(b"\n", b"\r\n")) != expected_hash:
            raise AssertionError(f"Pinned English file hash drift: {source_path}")
        lines = raw.decode("utf-8").splitlines()
        for record in records:
            decision = decisions[record["decision_id"]]
            if source_path not in {
                location["logical_path"] for group in decision["index_metadata"]["occurrences"]
                for location in group["locations"] if location["source_kind"] == "english"
            }:
                continue
            ranges = spans(record["source_lines"])
            if any(last > len(lines) for _first, last in ranges):
                raise AssertionError(f"Consulted original range out of file: {source_path}")
            excerpt = "\n".join("\n".join(lines[first - 1:last]) for first, last in ranges)
            if record["source_needle"].casefold() not in excerpt.casefold():
                raise AssertionError(f"Consulted source phrase missing: {record['decision_id']}")
            counters["original_choices_http_verified"] += 1
    if {key: counters[key] for key in receipt["totals"]} != receipt["totals"]:
        raise AssertionError("Render receipt and independent location census differ")
    result = {
        "status": "PASS_INDEPENDENT_ARABIC_CHOICE_BATCH_113_132_READBACK",
        "source_index_sha256": INDEX_SHA,
        "overlay_sha256": digest(OVERLAY),
        "choice_count": 20,
        "counts": dict(counters),
        "arabic_source_files_sha256_checked": len(arabic_hashes),
        "english_source_files_http_sha256_checked": len(english_hashes),
        "dictionary_pdf_sha256": digest(pdf),
        "cards": receipt["cards"],
    }
    (BASE / "INDEPENDENT_READBACK.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"status": result["status"], "choices": 20, "counts": dict(counters)}, ensure_ascii=True))


if __name__ == "__main__":
    main()
