#!/usr/bin/env python3
"""Independently read back an Arabic review batch, sources, canon and locators."""

from __future__ import annotations

import argparse
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
EASTERN = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def arabic_dominant(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    arabic = sum("\u0600" <= character <= "\u06ff" for character in value)
    latin = sum("A" <= character <= "Z" or "a" <= character <= "z" for character in value)
    return arabic >= 15 and arabic > latin


def check() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("overlay", type=Path, help="Overlay JSON path, absolute or relative to repository")
    args = parser.parse_args()
    overlay_path = args.overlay if args.overlay.is_absolute() else ROOT / args.overlay
    overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    batch = overlay["batch"]
    base = ROOT / "expert-review/2026-09-26-final-page-review" / batch["directory"]
    receipt = json.loads((base / "BUILD_RECEIPT.json").read_text(encoding="utf-8"))
    index = ROOT / overlay["source_index_path"]
    index_sha = overlay["source_index_sha256"]
    if digest(index) != index_sha or receipt["source_index_sha256"] != index_sha:
        raise AssertionError("Frozen review-index identity drift")
    if receipt["overlay_sha256"] != digest(overlay_path):
        raise AssertionError("Review overlay changed after rendering")
    canon = overlay["canon"]
    pdf = Path(canon["pdf_path"])
    if digest(pdf) != canon["pdf_sha256"]:
        raise AssertionError("Dictionary identity drift")
    printed_labels = canon.get("printed_page_labels")
    if printed_labels is not None:
        if (set(printed_labels) != {str(p) for p in canon["visually_checked_pdf_pages"]}
                or any(not isinstance(n, int) or isinstance(n, bool) or n < 1
                       for n in printed_labels.values())):
            raise AssertionError("Dictionary printed-page labels incomplete or invalid")
    elif canon.get("printed_page_offset") != -12:
        raise AssertionError("Legacy dictionary printed-page offset drift")
    if any(digest(ROOT / canon[key + "_path"]) != canon[key + "_sha256"]
           for key in ("ocr_query", "ocr_evidence")):
        raise AssertionError("Dictionary intake evidence drift")
    records = overlay["records"]
    ids = [item["decision_id"] for item in records]
    if (len(records) != batch["last_number"] - batch["first_number"] + 1
            or len(ids) != len(set(ids)) or receipt["decision_ids"] != ids):
        raise AssertionError("Decision inventory/order mismatch")
    wanted = set(ids)
    decisions = {}
    already_arabic = set()
    for decision in iter_decisions(index):
        if decision["index_metadata"]["human_index_included"] and all(
            arabic_dominant(decision.get(key)) for key in ("sense", "rationale", "expert_question")
        ):
            already_arabic.add(decision["decision_id"])
        if decision["decision_id"] in wanted:
            decisions[decision["decision_id"]] = decision
    prior_ids = {
        item["decision_id"]
        for name in overlay["prior_overlays"]
        for item in json.loads((ROOT / "evidence/classical/terminology" / name).read_text(encoding="utf-8"))["records"]
    }
    if (set(decisions) != wanted or len(already_arabic) != 267
            or wanted & (already_arabic | prior_ids)
            or batch["local_after"] != len(already_arabic | prior_ids | wanted)):
        raise AssertionError("Decision missing, repeated, or Arabic coverage total wrong")

    readme = base / "README.md"
    if readme.stat().st_size != receipt["readme"]["bytes"] or digest(readme) != receipt["readme"]["sha256"]:
        raise AssertionError("Reader entry byte identity drift")
    intro = readme.read_text(encoding="utf-8")
    if not all(token in intro for token in (
        "GPT-6 Sol", "Ultra", "لم تُنشر بعد", batch["summary_ar"],
        str(batch["local_after"]).translate(EASTERN) + " من ١٠٩٥",
        str(batch["public_before"]).translate(EASTERN) + " من ١٠٩٥",
    )):
        raise AssertionError("Arabic release status, counts, or AI disclosure omitted")

    card_by_id = {}
    sections = batch["sections"]
    if len(receipt["cards"]) != len(sections):
        raise AssertionError("Rendered card-section count mismatch")
    for item, (first, last, name, _title) in zip(receipt["cards"], sections):
        if item["path"] != name or item["decision_ids"] != ids[first:last]:
            raise AssertionError("Card partition/order mismatch")
        path = base / name
        if (path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]
                or path.stat().st_size > 230_000 or f"]({name})" not in intro):
            raise AssertionError("Card bytes or reader navigation mismatch")
        body = path.read_text(encoding="utf-8")
        matches = list(re.finditer(r"^الأصل الإنجليزي: .*? معرّف القرار: `([^`]+)`\.$", body, re.M))
        if [match.group(1) for match in matches] != item["decision_ids"]:
            raise AssertionError("Card omitted or repeated in reader")
        for match in matches:
            begin = body.rfind("\n## ", 0, match.start())
            end = body.find("\n## ", match.end())
            if begin < 0:
                raise AssertionError("Reader card heading missing")
            card_by_id[match.group(1)] = body[begin:end if end >= 0 else len(body)]
    if set(card_by_id) != wanted:
        raise AssertionError("Rendered choice inventory incomplete")

    english_hashes = {}
    arabic_hashes = {}
    counters = Counter()
    dictionary_filename = quote(pdf.name)
    cited_pages = set()
    for record in records:
        decision_id = record["decision_id"]
        decision = decisions[decision_id]
        if not decision["index_metadata"]["human_index_included"]:
            raise AssertionError("Nonhuman decision in Arabic batch")
        card = card_by_id[decision_id]
        displayed = decision["review_display"]["chosen_arabic"].replace("\\-", "")
        if not card.startswith(f"\n## {displayed}\n"):
            raise AssertionError(f"Chosen Arabic term not displayed correctly: {decision_id}")
        for field in ("sense_ar", "rationale_ar", "expert_question_ar", "source_relevance_ar",
                      "canon_note_ar", "confidence_ar"):
            if not arabic_dominant(record[field]) or record[field] not in card:
                raise AssertionError(f"Unrendered Arabic choice evidence: {decision_id}: {field}")
        if card.count("**كل وقوع مسجل لهذا القرار:**") != 1:
            raise AssertionError("Occurrence list missing or repeated")
        for alternative in record["alternatives_ar"]:
            if alternative not in card:
                raise AssertionError("Decision alternative omitted")

        locations = [
            loc for group in decision["index_metadata"]["occurrences"]
            for loc in group["locations"] if loc.get("human_review_included")
        ]
        english = [loc for loc in locations if loc["source_kind"] == "english"]
        english_paths = {loc["logical_path"] for loc in english}
        if not english_paths:
            raise AssertionError(f"Pinned original path missing: {decision_id}")
        if "source_passages" in record:
            passages = record["source_passages"]
        else:
            if len(english_paths) != 1:
                raise AssertionError(f"Multiple originals require source_passages: {decision_id}")
            passages = [{"path": next(iter(english_paths)), "lines": record["source_lines"],
                         "needle": record["source_needle"],
                         "relevance_ar": record["source_relevance_ar"]}]
        if (not passages or {item["path"] for item in passages} != english_paths
                or len({(item["path"], item["lines"], item["needle"]) for item in passages}) != len(passages)):
            raise AssertionError(f"Consulted original passage inventory incomplete: {decision_id}")
        for passage in passages:
            source_path = passage["path"]
            path_locs = [loc for loc in english if loc["logical_path"] == source_path]
            source_hashes = {loc["recorded_sha256"].upper() for loc in path_locs}
            if len(source_hashes) != 1:
                raise AssertionError("Inconsistent original occurrence hashes")
            source_hash = source_hashes.pop()
            if source_path in english_hashes and english_hashes[source_path] != source_hash:
                raise AssertionError("Inconsistent original file hashes")
            english_hashes[source_path] = source_hash
            original_url = ("https://github.com/OpenLogicProject/OpenLogic/blob/"
                            + overlay["english_source_commit"] + "/" + source_path)
            original_lines = [loc["line_reconciliation"]["current_line_start"]
                              for loc in path_locs]
            if not any(first <= line <= last for line in original_lines
                       for first, last in spans(passage["lines"])):
                raise AssertionError(f"Consulted original span misses choice: {decision_id}")
            for first, last in spans(passage["lines"]):
                label = (str(first) + (f"-{last}" if first != last else "")).translate(EASTERN)
                fragment = f"#L{first}" + (f"-L{last}" if first != last else "")
                if f"[الأسطر {label}]({original_url}{fragment})" not in card:
                    raise AssertionError(f"Consulted original span URL missing: {decision_id} {source_path} {first}-{last}")
                counters["original_spans"] += 1
        for page in record["canon_pdf_pages"]:
            if page not in canon["visually_checked_pdf_pages"]:
                raise AssertionError("Uninspected dictionary page cited")
            cited_pages.add(page)
            url = f"https://archive.org/download/DAM2018ENAR/{dictionary_filename}#page={page}"
            printed = printed_labels[str(page)] if printed_labels is not None else page - 12
            label = (f"[ص {str(page).translate(EASTERN)} من PDF "
                     f"(المطبوعة {str(printed).translate(EASTERN)})]({url})")
            if label not in card:
                raise AssertionError("Dictionary page or printed-label link omitted")
            counters["canon_page_links"] += 1

        expected_lines = Counter()
        expected_pages = Counter()
        unresolved = unavailable = 0
        for loc in locations:
            counters["locations"] += 1
            link, resolved = source_url(loc)
            expected_lines[link] += 1
            counters["resolved" if resolved else "unresolved"] += 1
            unresolved += not resolved
            if loc["source_kind"] != "english":
                path = ROOT / loc["logical_path"]
                arabic_hashes.setdefault(path, digest(path))
                if arabic_hashes[path] != loc["current_sha256"].upper():
                    raise AssertionError(f"Target source drift: {path}")
            any_page = any_unavailable = False
            for evidence in loc["page_evidence"]:
                method = evidence["method"]
                if method == "unavailable":
                    if evidence.get("pdf_pages"):
                        raise AssertionError("Unavailable page has spurious number")
                    any_unavailable = True
                    continue
                if method not in ("synctex-exact", "visual-text-exact", "unit-start-fallback"):
                    raise AssertionError("Unknown PDF locator method")
                any_page = True
                counters["fallback_pages" if method == "unit-start-fallback" else "exact_pages"] += 1
                filename = {
                    "الطبعة التراثية": "00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf",
                    "الطبعة الدولية": "00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf",
                    "طبعة المشرق": "03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf",
                }.get(evidence["reader"].split(" — ", 1)[0])
                if filename is None:
                    raise AssertionError("Unknown Arabic reader")
                for number in evidence["pdf_pages"][:3]:
                    expected_pages[f"{filename}#page={number})"] += 1
            unavailable += any_unavailable and not any_page
        for link, count in expected_lines.items():
            if card.count(link) != count:
                raise AssertionError(f"Source-line URL census mismatch: {decision_id}")
        for link, count in expected_pages.items():
            if card.count(link) != count:
                raise AssertionError(f"PDF-page URL census mismatch: {decision_id}")
        if card.count("⚠ لم يثبت السطر الحالي") != unresolved:
            raise AssertionError("Unresolved-line warning missing")
        if card.count("⚠ لم تثبت صفحة PDF") != unavailable:
            raise AssertionError("Unavailable-PDF warning missing")
    if cited_pages != set(canon["visually_checked_pdf_pages"]):
        raise AssertionError("Visually checked dictionary page was not cited")

    verified_passages = set()
    for source_path, expected_hash in english_hashes.items():
        url = ("https://raw.githubusercontent.com/OpenLogicProject/OpenLogic/"
               + overlay["english_source_commit"] + "/" + source_path)
        with urlopen(Request(url, headers={"User-Agent": "OpenLogic-Arabic-review-verifier/1"}), timeout=20) as response:
            if response.status != 200:
                raise AssertionError("Pinned English source HTTP unavailable")
            raw = response.read(200_001)
        if (len(raw) > 200_000 or b"\r" in raw
                or hashlib.sha256(raw.replace(b"\n", b"\r\n")).hexdigest().upper() != expected_hash):
            raise AssertionError(f"Pinned English file identity drift: {source_path}")
        lines = raw.decode("utf-8").splitlines()
        for record in records:
            if "source_passages" in record:
                passages = [item for item in record["source_passages"]
                            if item["path"] == source_path]
            else:
                decision = decisions[record["decision_id"]]
                relevant = source_path in {
                    loc["logical_path"] for group in decision["index_metadata"]["occurrences"]
                    for loc in group["locations"] if loc["source_kind"] == "english"
                }
                passages = ([{"lines": record["source_lines"], "needle": record["source_needle"]}]
                            if relevant else [])
            for passage in passages:
                ranges = spans(passage["lines"])
                if any(last > len(lines) for _first, last in ranges):
                    raise AssertionError("Consulted English lines outside pinned file")
                excerpt = "\n".join("\n".join(lines[first - 1:last]) for first, last in ranges)
                if (" ".join(passage["needle"].casefold().split())
                        not in " ".join(excerpt.casefold().split())):
                    raise AssertionError(f"Consulted English term missing: {record['decision_id']}")
                verified_passages.add((record["decision_id"], source_path,
                                       passage["lines"], passage["needle"]))
    expected_passages = {
        (record["decision_id"], item["path"], item["lines"], item["needle"])
        for record in records
        for item in (record["source_passages"] if "source_passages" in record else [{
            "path": next(iter({loc["logical_path"]
                               for group in decisions[record["decision_id"]]["index_metadata"]["occurrences"]
                               for loc in group["locations"] if loc["source_kind"] == "english"})),
            "lines": record["source_lines"], "needle": record["source_needle"]
        }])
    }
    if verified_passages != expected_passages:
        raise AssertionError("Not every pinned original passage was HTTP-verified")
    counters["original_choices_http_verified"] = len({item[0] for item in verified_passages})
    counters["original_source_passages_http_verified"] = len(verified_passages)
    if {key: counters[key] for key in receipt["totals"]} != receipt["totals"]:
        raise AssertionError("Rendered and independently counted locations disagree")
    result = {
        "status": "PASS_INDEPENDENT_ARABIC_REVIEW_BATCH_READBACK",
        "source_index_sha256": index_sha,
        "overlay_sha256": digest(overlay_path), "choice_count": len(ids),
        "counts": dict(counters), "arabic_source_files_sha256_checked": len(arabic_hashes),
        "english_source_files_http_sha256_checked": len(english_hashes),
        "dictionary_pdf_sha256": digest(pdf), "cards": receipt["cards"],
    }
    (base / "INDEPENDENT_READBACK.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"status": result["status"], "choices": len(ids),
                      "counts": dict(counters)}, ensure_ascii=True))


if __name__ == "__main__":
    check()
