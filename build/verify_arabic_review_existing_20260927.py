#!/usr/bin/env python3
"""Read back all 267 existing Arabic cards against the immutable page index."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "expert-review/2026-09-26-final-page-review/arabic-existing"
INDEX = ROOT / "tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json"
RECEIPT = BASE / "BUILD_RECEIPT.json"
CHECK = BASE / "INDEPENDENT_READBACK.json"
SOURCE_COMMIT = "86a4a7c11c0a0289ade28cb8f96acbacf9c01844"
EXPECTED_INDEX_SHA = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def east(number: int) -> str:
    return str(number).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))


def is_arabic(value: str) -> bool:
    return bool(value) and sum(0x600 <= ord(char) <= 0x6FF for char in value) > sum(char.isascii() and char.isalpha() for char in value)


def source_url(location: dict) -> tuple[str, bool]:
    recon = location["line_reconciliation"]
    if recon["resolved"]:
        line = recon.get("current_line_start") or location.get("line_start")
        if not isinstance(line, int) or line < 1:
            raise AssertionError(f"Bad current line: {location['location_id']}")
        url = location["source_url"].split("#L", 1)[0]
        if location["source_kind"] != "english":
            url = url.replace("/blob/main/", f"/blob/{SOURCE_COMMIT}/")
        return f"[السطر {east(line)}]({url}#L{line})", True
    file_url = location.get("file_url")
    if not file_url:
        raise AssertionError(f"Missing unresolved file URL: {location['location_id']}")
    return f"[الملف]({file_url.replace('/blob/main/', f'/blob/{SOURCE_COMMIT}/')})", False


def main() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if digest(INDEX) != EXPECTED_INDEX_SHA or receipt["source_index_sha256"] != EXPECTED_INDEX_SHA:
        raise AssertionError("Index source changed")
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    decisions = {d["decision_id"]: d for d in index["decisions"]}
    expected = {
        d["decision_id"] for d in index["decisions"]
        if d["index_metadata"]["human_index_included"]
        and all(is_arabic(d.get(key) or "") for key in ("sense", "rationale", "expert_question"))
        and is_arabic(d["review_display"].get("chosen_arabic") or "")
    }
    if len(expected) != 267:
        raise AssertionError(f"Arabic record census drift: {len(expected)}")
    seen = set()
    counts = Counter()
    source_hash_cache = {}
    shard_hashes = {}
    for shard in receipt["shards"]:
        path = ROOT / shard["path"]
        if path.stat().st_size != shard["bytes"] or digest(path) != shard["sha256"]:
            raise AssertionError(f"Shard bytes changed: {path}")
        shard_hashes[path.name] = shard["sha256"]
        body = path.read_text(encoding="utf-8")
        markers = list(re.finditer(r"^الأصل الإنجليزي: .*? معرّف القرار: `([^`]+)`\.$", body, re.M))
        if len(markers) != shard["choices"]:
            raise AssertionError(f"Card count mismatch: {path}")
        if [match.group(1) for match in markers] != shard["decision_ids"]:
            raise AssertionError(f"Decision order mismatch: {path}")
        for position, marker in enumerate(markers):
            decision_id = marker.group(1)
            if decision_id in seen or decision_id not in expected:
                raise AssertionError(f"Repeated or extraneous decision: {decision_id}")
            seen.add(decision_id)
            card_start = body.rfind("\n## ", 0, marker.start())
            if card_start < 0:
                raise AssertionError(f"Card heading missing: {decision_id}")
            next_start = body.find("\n## ", marker.end())
            card = body[card_start:next_start if next_start >= 0 else len(body)]
            decision = decisions[decision_id]
            for key in ("sense", "rationale", "expert_question"):
                if decision[key] not in card:
                    raise AssertionError(f"Missing exact Arabic field {key}: {decision_id}")
            expected_sources = Counter()
            expected_pages = Counter()
            unresolved = 0
            for group in decision["index_metadata"]["occurrences"]:
                for location in group["locations"]:
                    if not location.get("human_review_included"):
                        continue
                    counts["locations"] += 1
                    link, resolved = source_url(location)
                    expected_sources[link] += 1
                    if resolved:
                        counts["resolved"] += 1
                        if location["source_kind"] != "english":
                            path_source = ROOT / location["logical_path"]
                            if path_source not in source_hash_cache:
                                source_hash_cache[path_source] = digest(path_source)
                            if source_hash_cache[path_source] != location["current_sha256"].upper():
                                raise AssertionError(f"Drifted Arabic source: {path_source}")
                    else:
                        counts["unresolved"] += 1
                        unresolved += 1
                    for page in location["page_evidence"]:
                        filename = {
                            "الطبعة التراثية": "00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf",
                            "الطبعة الدولية": "00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf",
                            "طبعة المشرق": "03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf",
                        }.get(page["reader"].split(" — ", 1)[0])
                        if filename is None:
                            raise AssertionError(f"Unknown reader label: {page['reader']}")
                        for number in page["pdf_pages"][:3]:
                            expected_pages[f"{filename}#page={number})"] += 1
                        if page["method"] == "synctex-exact":
                            counts["exact_pages"] += 1
                        elif page["method"] == "unit-start-fallback":
                            counts["fallback_pages"] += 1
                        elif page["method"] == "visual-text-exact":
                            counts["exact_pages"] += 1
                        else:
                            raise AssertionError(f"Unexpected page method: {page['method']}")
            for link, count in expected_sources.items():
                if card.count(link) != count:
                    raise AssertionError(f"Missing or duplicate source link: {decision_id}: {link}")
            for link, count in expected_pages.items():
                if card.count(link) != count:
                    raise AssertionError(f"Missing or duplicate page link: {decision_id}: {link}")
            if unresolved and card.count("⚠ لم يثبت السطر الحالي") != unresolved:
                raise AssertionError(f"Unresolved locators lack honest warnings: {decision_id}")
    if seen != expected:
        raise AssertionError(f"Missing decisions: {sorted(expected - seen)[:5]}")
    if dict(counts) != receipt["totals"]:
        raise AssertionError(f"Occurrence counts differ: {dict(counts)} != {receipt['totals']}")
    readme = BASE / "README.md"
    if digest(readme) != receipt["readme"]["sha256"]:
        raise AssertionError("Start-page bytes changed")
    result = {
        "status": "PASS_INDEPENDENT_EXISTING_ARABIC_VIEW",
        "index_sha256": EXPECTED_INDEX_SHA,
        "choice_count": len(seen),
        "shard_count": len(shard_hashes),
        "counts": dict(counts),
        "readme_sha256": digest(readme),
        "build_receipt_sha256": digest(RECEIPT),
        "source_files_checked": len(source_hash_cache),
        "note_ar": "إثبات شامل للبطاقات والروابط والأعداد؛ لا يثبت صحة كل حكم لغوي أو معجمي من جديد.",
    }
    CHECK.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
