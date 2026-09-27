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
from verify_arabic_review_existing_20260927 import SOURCE_COMMIT as ARABIC_SOURCE_COMMIT, digest, source_url
from verify_arabic_review_senses_76_85_20260927 import spans


ROOT = Path(__file__).resolve().parents[1]
EASTERN = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def load_overlay(path: Path, depth: int = 0) -> dict:
    """Independently expand compact review metadata before readback."""
    if depth > 100:
        raise AssertionError("Review overlay inheritance too deep")
    raw = json.loads(path.read_text(encoding="utf-8"))
    parent = raw.pop("inherit_from", None)
    if parent is None:
        return raw
    if (not isinstance(parent, str) or Path(parent).name != parent
            or not parent.endswith(".json") or "prior_overlays" in raw):
        raise AssertionError("Invalid review overlay inheritance")
    base = load_overlay(path.parent / parent, depth + 1)
    merged = {**base, **raw}
    merged["prior_overlays"] = [*base["prior_overlays"], parent]
    merged["canon"] = {**base["canon"], **raw.get("canon", {})}
    merged["record_defaults"] = {**base.get("record_defaults", {}), **raw.get("record_defaults", {})}
    return merged


def arabic_dominant(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    arabic = sum("\u0600" <= character <= "\u06ff" for character in value)
    latin = sum("A" <= character <= "Z" or "a" <= character <= "z" for character in value)
    return arabic >= 15 and arabic > latin


def arabic_display_label(value: object) -> bool:
    return (isinstance(value, str)
            and sum("\u0600" <= character <= "\u06ff" for character in value) >= 2
            and not any("A" <= character <= "Z" or "a" <= character <= "z"
                        for character in value))


def derived_passages(decision: dict, record: dict) -> list[dict]:
    selected = {}
    for group in decision["index_metadata"]["occurrences"]:
        for location in group["locations"]:
            if (location["source_kind"] != "english" or not location.get("human_review_included")
                    or location["logical_path"] in selected):
                continue
            reconciliation = location["line_reconciliation"]
            first = reconciliation.get("current_line_start")
            last = reconciliation.get("current_line_end")
            excerpt = location.get("current_excerpt") or location.get("excerpt") or ""
            if isinstance(first, int) and isinstance(last, int) and excerpt.strip():
                selected[location["logical_path"]] = {
                    "path": location["logical_path"],
                    "lines": str(first) + (f"-{last}" if last != first else ""),
                    "needle": " ".join(excerpt.split())[:120].strip(),
                    "relevance_ar": record["source_relevance_ar"],
                }
    return list(selected.values())


def check() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("overlay", type=Path, help="Overlay JSON path, absolute or relative to repository")
    args = parser.parse_args()
    overlay_path = args.overlay if args.overlay.is_absolute() else ROOT / args.overlay
    overlay = load_overlay(overlay_path)
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
    records = [{**overlay.get("record_defaults", {}), **row} for row in overlay["records"]]
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
        card_page_limit = batch.get("single_card_limit_bytes", 400_000) if last - first == 1 else 230_000
        if (path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]
                or path.stat().st_size > card_page_limit or f"]({name})" not in intro):
            raise AssertionError("Card bytes or reader navigation mismatch")
        body = path.read_text(encoding="utf-8")
        matches = list(re.finditer(r"معرّف القرار: `([^`]+)`\.$", body, re.M))
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
        english_label = " ".join(decision["english_term"].split())
        inference = record.get("inference_from_original") is True
        supplemental = record.get("supplemental_original") is True
        if inference and supplemental:
            raise AssertionError(f"Conflicting original-provenance modes: {decision_id}")
        label = ("القضية التحريرية المستنبطة من تعريفات الأصل (ليست عبارة حرفية منه): `"
                 if inference else ("مصطلح الأصل بشاهد إضافي مستعاد (لا يسجّل المؤشر وقوعه الإنجليزي): `"
                                    if supplemental else "الأصل الإنجليزي: `"))
        if label + english_label + "`. معرّف القرار: `" + decision_id + "`." not in card:
            raise AssertionError(f"Original English choice label omitted: {decision_id}")
        displayed = record.get("display_override_ar", decision["review_display"]["chosen_arabic"].replace("\\-", ""))
        if not card.startswith(f"\n## {displayed}\n"):
            raise AssertionError(f"Chosen Arabic term not displayed correctly: {decision_id}")
        if record.get("legacy_absent") is True:
            target_paths = {
                ROOT / loc["logical_path"]
                for group in decision["index_metadata"]["occurrences"]
                for loc in group["locations"] if loc["source_kind"] != "english"
            }
            if (not target_paths or not arabic_dominant(record.get("legacy_note_ar"))
                    or any(displayed in path.read_text(encoding="utf-8") for path in target_paths)
                    or "**حالة الاختيار في النص الجاري:** " + record["legacy_note_ar"] not in card):
                raise AssertionError(f"Legacy absent choice not proved: {decision_id}")
        if "display_override_ar" in record:
            target_excerpts = [
                loc.get("current_excerpt") or loc.get("excerpt") or ""
                for group in decision["index_metadata"]["occurrences"]
                for loc in group["locations"] if loc["source_kind"] != "english"
            ]
            macro = record.get("display_macro_witness")
            legacy_head = (record.get("display_from_legacy_head") is True
                           and decision["chosen_arabic"].startswith(displayed))
            macro_ok = False
            if isinstance(macro, dict):
                logical = macro["logical_path"]
                line = macro["line"]
                source = ROOT / logical
                if (not logical.startswith("source/locale/ar/")
                        or ".." in Path(logical).parts or not isinstance(line, int)
                        or line < 1 or digest(source) != macro["sha256"]
                        or not arabic_dominant(macro.get("relevance_ar"))):
                    raise AssertionError(f"Token registry witness invalid: {decision_id}")
                lines = source.read_text(encoding="utf-8").splitlines()
                macro_ok = (line <= len(lines) and macro["needle"] in lines[line - 1]
                            and displayed in lines[line - 1]
                            and any("!!{" in excerpt or "!!a{" in excerpt
                                    for excerpt in target_excerpts))
                url = (f"https://github.com/KokunoYumeto/OpenLogic-ar/blob/"
                       f"{ARABIC_SOURCE_COMMIT}/{logical}#L{line}")
                if (f"**شاهد حل الرمز في ملف الطبعة:** "
                        f"[السطر {str(line).translate(EASTERN)}]({url})"
                        f" — {macro['relevance_ar']}" not in card):
                    raise AssertionError(f"Token registry link omitted: {decision_id}")
            if (not arabic_display_label(displayed)
                    or not (macro_ok or legacy_head or any(" ".join(displayed.split()) in " ".join(excerpt.split())
                                             for excerpt in target_excerpts))
                    or not arabic_dominant(record.get("display_correction_note_ar"))
                    or (("**تنقية رأس البطاقة الموروث:** " if legacy_head else
                         "**تصحيح رأس البطاقة من النص الجاري:** ")
                        + record["display_correction_note_ar"] not in card)
                    or (legacy_head and "**صفة الرأس المختصر:** جزء عربي من رأس السجل الموروث، "
                        "لا اقتباس حرفي من السطر الجاري." not in card)):
                raise AssertionError(f"Unsupported localized display correction: {decision_id}")
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
        if inference or supplemental:
            if (english_paths or (inference and not decision.get("source_proposition_status", "").startswith(
                    "new editorial inference from cited original definitions"))
                    or not isinstance(record.get("original_sha256"), str)
                    or len(record["original_sha256"]) != 64
                    or (inference and "**مواضع تعريفات الأصل الإنجليزي التي استُعملت في هذا الاستنباط:** " not in card)
                    or (supplemental and (not arabic_dominant(record.get("source_witness_note_ar"))
                                          or "**شاهد الأصل الإنجليزي المستعاد استدراكًا:** " not in card
                                          or record["source_witness_note_ar"] not in card))):
                raise AssertionError(f"Invalid editorial-inference provenance: {decision_id}")
            target_locations = [loc for loc in locations if loc["source_kind"] != "english"]
            focus = record.get("target_focus")
            if len(target_locations) == 1 and isinstance(focus, dict):
                target = target_locations[0]
                first, last = focus["first_line"], focus["last_line"]
                if (not isinstance(first, int) or not isinstance(last, int)
                        or (not supplemental and
                            not target["line_start"] <= first <= last <= target["line_end"])
                        or not arabic_dominant(focus["relevance_ar"])):
                    raise AssertionError(f"Editorial-inference target focus invalid: {decision_id}")
                target_lines = (ROOT / target["logical_path"]).read_text(encoding="utf-8").splitlines()
                excerpt = "\n".join(target_lines[first - 1:last])
                if " ".join(focus["needle"].split()) not in " ".join(excerpt.split()):
                    raise AssertionError(f"Editorial-inference exact target text missing: {decision_id}")
                current_link, resolved = source_url(target)
                if not resolved and not supplemental:
                    raise AssertionError(f"Editorial-inference target line unresolved: {decision_id}")
                match = re.search(r"\]\((https://[^)]+)\)", current_link)
                if not match:
                    raise AssertionError("Target source URL missing")
                url = match.group(1).split("#L", 1)[0]
                url += f"#L{first}" + (f"-L{last}" if last != first else "")
                label = str(first).translate(EASTERN) + (
                    "–" + str(last).translate(EASTERN) if last != first else "")
                focus_heading = ("الموضع الدقيق في النص العربي" if supplemental
                                 else "الموضع الدقيق داخل التنبيه العربي")
                expected_focus = (f"**{focus_heading}:** [الأسطر {label}]({url})"
                                  f" — {focus['relevance_ar']}")
                if expected_focus not in card:
                    raise AssertionError(f"Editorial-inference exact target link omitted: {decision_id}")
            elif supplemental and record.get("target_witnesses"):
                expected_notes = []
                for witness in record["target_witnesses"]:
                    logical = witness["logical_path"]
                    first, last = witness["first_line"], witness["last_line"]
                    path = ROOT / logical
                    if (not logical.startswith("source/locale/ar") or ".." in Path(logical).parts
                            or not isinstance(first, int) or not isinstance(last, int)
                            or first < 1 or last < first
                            or digest(path) != witness["sha256"]
                            or not arabic_dominant(witness["relevance_ar"])):
                        raise AssertionError(f"Supplemental target identity invalid: {decision_id}")
                    excerpt = "\n".join(path.read_text(encoding="utf-8").splitlines()[first - 1:last])
                    if " ".join(witness["needle"].split()) not in " ".join(excerpt.split()):
                        raise AssertionError(f"Supplemental target text absent: {decision_id}")
                    fragment = f"#L{first}" + (f"-L{last}" if last != first else "")
                    url = (f"https://github.com/KokunoYumeto/OpenLogic-ar/blob/{ARABIC_SOURCE_COMMIT}/"
                           + logical + fragment)
                    label = str(first).translate(EASTERN) + (
                        "–" + str(last).translate(EASTERN) if last != first else "")
                    expected_notes.append(f"{witness['label_ar']}: [الأسطر {label}]({url}) — {witness['relevance_ar']}")
                expected_focus = "**شواهد عربية دقيقة مستعادة استدراكًا:** " + "؛ ".join(expected_notes)
                if expected_focus not in card:
                    raise AssertionError(f"Supplemental target links omitted: {decision_id}")
            else:
                raise AssertionError(f"Original-index gap has no verified Arabic witness: {decision_id}")
        elif not english_paths:
            raise AssertionError(f"Pinned original path missing: {decision_id}")
        if record.get("source_from_occurrences") is True:
            passages = derived_passages(decision, record)
        elif "source_passages" in record:
            passages = record["source_passages"]
        else:
            if len(english_paths) != 1:
                raise AssertionError(f"Multiple originals require source_passages: {decision_id}")
            passages = [{"path": next(iter(english_paths)), "lines": record["source_lines"],
                         "needle": record["source_needle"],
                         "relevance_ar": record["source_relevance_ar"]}]
        passage_paths = {item["path"] for item in passages}
        supplemental_hashes = record.get("original_sha256_by_path")
        if (not passages or (not inference and not supplemental
                             and passage_paths != english_paths)
                or (inference and len(passage_paths) != 1)
                or (supplemental and len(passage_paths) > 1
                    and (not isinstance(supplemental_hashes, dict)
                         or set(supplemental_hashes) != passage_paths
                         or not all(isinstance(value, str) and len(value) == 64
                                    for value in supplemental_hashes.values())))
                or len({(item["path"], item["lines"], item["needle"]) for item in passages}) != len(passages)):
            raise AssertionError(f"Consulted original passage inventory incomplete: {decision_id}")
        for passage in passages:
            source_path = passage["path"]
            path_locs = [loc for loc in english if loc["logical_path"] == source_path]
            source_hashes = {loc["recorded_sha256"].upper() for loc in path_locs}
            if inference or supplemental:
                source_hashes = {(record.get("original_sha256_by_path") or {}).get(
                    source_path, record["original_sha256"]).upper()}
            if len(source_hashes) != 1:
                raise AssertionError("Inconsistent original occurrence hashes")
            source_hash = source_hashes.pop()
            if source_path in english_hashes and english_hashes[source_path] != source_hash:
                raise AssertionError("Inconsistent original file hashes")
            english_hashes[source_path] = source_hash
            original_url = ("https://github.com/OpenLogicProject/OpenLogic/blob/"
                            + overlay["english_source_commit"] + "/" + source_path)
            original_lines = [line for loc in path_locs
                              if isinstance((line := loc["line_reconciliation"].get("current_line_start")), int)]
            # A frozen occurrence may identify the file while leaving its
            # current line unresolved. In that case the separately pinned,
            # exact passage is checked below; never invent an old line.
            if (not inference and not supplemental and original_lines
                    and not any(first <= line <= last for line in original_lines
                                for source_item in passages
                                if source_item["path"] == source_path
                                for first, last in spans(source_item["lines"]))):
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
        if not record["canon_pdf_pages"]:
            label = ({
                "not-applicable": "**انطباق المعجم الرياضي:** ",
                "not-found-in-checked-sources": "**نتيجة البحث المعجمي المحدود:** ",
            }).get(record.get("canon_status"))
            if not label or label + record["canon_note_ar"] not in card:
                raise AssertionError(f"Unjustified dictionary non-applicability: {decision_id}")

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
        normalized = raw.replace(b"\r\n", b"\n")
        if (len(raw) > 200_000 or b"\r" in normalized
                or hashlib.sha256(normalized.replace(b"\n", b"\r\n")).hexdigest().upper() != expected_hash):
            raise AssertionError(f"Pinned English file identity drift: {source_path}")
        lines = normalized.decode("utf-8").splitlines()
        for record in records:
            if record.get("source_from_occurrences") is True:
                passages = [item for item in derived_passages(decisions[record["decision_id"]], record)
                            if item["path"] == source_path]
            elif "source_passages" in record:
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
    supplemental_arabic = {}
    for record in records:
        for witness in [*record.get("target_witnesses", []),
                        *([{"logical_path": record["display_macro_witness"]["logical_path"],
                            "sha256": record["display_macro_witness"]["sha256"]}]
                          if record.get("display_macro_witness") else [])]:
            logical = witness["logical_path"]
            expected_hash = witness["sha256"]
            if logical in supplemental_arabic:
                if supplemental_arabic[logical] != expected_hash:
                    raise AssertionError("Inconsistent supplemental Arabic source identity")
                continue
            url = (f"https://raw.githubusercontent.com/KokunoYumeto/OpenLogic-ar/"
                   f"{ARABIC_SOURCE_COMMIT}/{logical}")
            with urlopen(Request(url, headers={"User-Agent": "OpenLogic-Arabic-review-verifier/1"}),
                         timeout=20) as response:
                if response.status != 200:
                    raise AssertionError("Pinned supplemental Arabic source unavailable")
                raw = response.read(200_001)
            if len(raw) > 200_000 or hashlib.sha256(raw).hexdigest().upper() != expected_hash:
                raise AssertionError(f"Pinned supplemental Arabic bytes differ: {logical}")
            supplemental_arabic[logical] = expected_hash
    expected_passages = {
        (record["decision_id"], item["path"], item["lines"], item["needle"])
        for record in records
        for item in (derived_passages(decisions[record["decision_id"]], record)
                     if record.get("source_from_occurrences") is True else
                     record["source_passages"] if "source_passages" in record else [{
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
    counters["supplemental_arabic_files_http_verified"] = len(supplemental_arabic)
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
