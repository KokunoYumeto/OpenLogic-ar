#!/usr/bin/env python3
"""Render a bounded Arabic expert-review overlay using the frozen review index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import quote

from render_arabic_review_existing_20260927 import arabic_dominant, decision_card, pinned_url, sha256
from render_arabic_review_senses_76_85_20260927 import source_links
from render_arabic_priority_guide_20260926 import SOURCE_COMMIT as ARABIC_SOURCE_COMMIT
from stream_expert_review_decisions import iter_decisions


ROOT = Path(__file__).resolve().parents[1]
TERM_DIR = ROOT / "evidence/classical/terminology"
REVIEW_DIR = ROOT / "expert-review/2026-09-26-final-page-review"
EASTERN = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def load_overlay(path: Path, depth: int = 0) -> dict:
    """Expand a compact batch by inheriting immutable shared batch metadata."""
    if depth > 100:
        raise ValueError("Review overlay inheritance too deep")
    raw = json.loads(path.read_text(encoding="utf-8"))
    parent = raw.pop("inherit_from", None)
    if parent is None:
        return raw
    if (not isinstance(parent, str) or Path(parent).name != parent
            or not parent.endswith(".json") or "prior_overlays" in raw):
        raise ValueError("Invalid review overlay inheritance")
    base = load_overlay(path.parent / parent, depth + 1)
    merged = {**base, **raw}
    merged["prior_overlays"] = [*base["prior_overlays"], parent]
    merged["canon"] = {**base["canon"], **raw.get("canon", {})}
    merged["record_defaults"] = {**base.get("record_defaults", {}), **raw.get("record_defaults", {})}
    return merged


def east(value: object) -> str:
    return str(value).translate(EASTERN)


def arabic_display_label(value: object) -> bool:
    """Allow genuine short Arabic headwords without relaxing prose checks."""
    return (isinstance(value, str)
            and sum("\u0600" <= character <= "\u06ff" for character in value) >= 2
            and not any("A" <= character <= "Z" or "a" <= character <= "z"
                        for character in value))


def printed_page(canon: dict, page: int) -> int:
    labels = canon.get("printed_page_labels")
    if labels is not None:
        if set(labels) != {str(number) for number in canon["visually_checked_pdf_pages"]}:
            raise ValueError("Printed-page labels do not cover exactly the visually checked pages")
        value = labels.get(str(page))
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"Invalid printed-page label: {page}")
        return value
    return page + canon["printed_page_offset"]


def canon_link(canon: dict, page: int) -> str:
    name = quote(Path(canon["pdf_path"]).name)
    url = f"https://archive.org/download/DAM2018ENAR/{name}#page={page}"
    return f"[ص {east(page)} من PDF (المطبوعة {east(printed_page(canon, page))})]({url})"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("overlay", type=Path, help="Overlay JSON path, absolute or relative to repository")
    args = parser.parse_args()
    overlay_path = args.overlay if args.overlay.is_absolute() else ROOT / args.overlay
    overlay = load_overlay(overlay_path)
    batch = overlay["batch"]
    records = [{**overlay.get("record_defaults", {}), **row} for row in overlay["records"]]
    ids = [item["decision_id"] for item in records]
    first, last = batch["first_number"], batch["last_number"]
    if len(records) != last - first + 1 or len(ids) != len(set(ids)):
        raise ValueError("Nonconsecutive or repeated choice inventory")
    index = ROOT / overlay["source_index_path"]
    if sha256(index) != overlay["source_index_sha256"]:
        raise ValueError("Frozen source index drift")
    canon = overlay["canon"]
    if sha256(Path(canon["pdf_path"])) != canon["pdf_sha256"]:
        raise ValueError("Dictionary PDF identity drift")
    for key in ("ocr_query", "ocr_evidence"):
        if sha256(ROOT / canon[key + "_path"]) != canon[key + "_sha256"]:
            raise ValueError(f"Dictionary intake identity drift: {key}")
    prior_ids = {
        item["decision_id"]
        for name in overlay["prior_overlays"]
        for item in json.loads((TERM_DIR / name).read_text(encoding="utf-8"))["records"]
    }
    wanted = set(ids)
    decisions = {}
    existing_arabic = set()
    for decision in iter_decisions(index):
        if decision["index_metadata"]["human_index_included"] and all(
            arabic_dominant(decision.get(key)) for key in ("sense", "rationale", "expert_question")
        ):
            existing_arabic.add(decision["decision_id"])
        if decision["decision_id"] in wanted:
            decisions[decision["decision_id"]] = decision
    if len(existing_arabic) != 267 or set(decisions) != wanted or wanted & (prior_ids | existing_arabic):
        raise ValueError("Choice missing, already localized, or base Arabic inventory drift")
    if batch["local_after"] != len(existing_arabic) + len(prior_ids) + len(records):
        raise ValueError("Claimed post-batch local total does not match disjoint inventory")

    cards = []
    totals = {key: 0 for key in ("locations", "resolved", "unresolved", "exact_pages", "fallback_pages")}
    observed_pages = set()
    for record in records:
        decision = decisions[record["decision_id"]]
        if not decision["index_metadata"]["human_index_included"]:
            raise ValueError("Excluded choice cannot be rendered")
        for key in ("sense_ar", "rationale_ar", "expert_question_ar", "source_relevance_ar",
                    "canon_note_ar", "confidence_ar"):
            if not arabic_dominant(record.get(key)):
                raise ValueError(f"Missing Arabic {key}: {record['decision_id']}")
        english_paths = {
            loc["logical_path"]
            for group in decision["index_metadata"]["occurrences"]
            for loc in group["locations"]
            if loc["source_kind"] == "english" and loc.get("human_review_included")
        }
        inference = record.get("inference_from_original") is True
        supplemental = record.get("supplemental_original") is True
        if inference and supplemental:
            raise ValueError(f"Conflicting source provenance modes: {record['decision_id']}")
        if inference:
            if (english_paths or not decision.get("source_proposition_status", "").startswith(
                    "new editorial inference from cited original definitions")
                    or not isinstance(record.get("original_sha256"), str)
                    or len(record["original_sha256"]) != 64):
                raise ValueError(f"Unbound editorial inference: {record['decision_id']}")
        elif supplemental:
            if (english_paths or not isinstance(record.get("original_sha256"), str)
                    or len(record["original_sha256"]) != 64
                    or not arabic_dominant(record.get("source_witness_note_ar"))):
                raise ValueError(f"Invalid supplemental source witness: {record['decision_id']}")
        elif not english_paths:
            raise ValueError(f"Original occurrence missing without inference status: {record['decision_id']}")
        if record.get("source_from_occurrences") is True:
            selected = {}
            for group in decision["index_metadata"]["occurrences"]:
                for loc in group["locations"]:
                    if (loc["source_kind"] != "english" or not loc.get("human_review_included")
                            or loc["logical_path"] in selected):
                        continue
                    first_line = loc["line_reconciliation"].get("current_line_start")
                    last_line = loc["line_reconciliation"].get("current_line_end")
                    excerpt = loc.get("current_excerpt") or loc.get("excerpt") or ""
                    if not isinstance(first_line, int) or not isinstance(last_line, int) or not excerpt.strip():
                        continue
                    selected[loc["logical_path"]] = {
                        "path": loc["logical_path"],
                        "lines": str(first_line) + (f"-{last_line}" if last_line != first_line else ""),
                        "needle": " ".join(excerpt.split())[:120].strip(),
                        "relevance_ar": record["source_relevance_ar"],
                    }
            sources = list(selected.values())
            if set(selected) != english_paths:
                raise ValueError(f"Cannot derive exact original passages: {record['decision_id']}")
        elif "source_passages" in record:
            sources = record["source_passages"]
        else:
            if len(english_paths) != 1:
                raise ValueError(f"Multiple original paths require source_passages: {record['decision_id']}")
            sources = [{
                "path": next(iter(english_paths)), "lines": record["source_lines"],
                "needle": record["source_needle"], "relevance_ar": record["source_relevance_ar"],
            }]
        source_path_set = {item["path"] for item in sources}
        supplemental_hashes = record.get("original_sha256_by_path")
        if (not sources or (not inference and not supplemental
                            and source_path_set != english_paths)
                or (inference and len(source_path_set) != 1)
                or (supplemental and len(source_path_set) > 1
                    and (not isinstance(supplemental_hashes, dict)
                         or set(supplemental_hashes) != source_path_set
                         or not all(isinstance(value, str) and len(value) == 64
                                    for value in supplemental_hashes.values())))
                or len({(item["path"], item["lines"], item["needle"]) for item in sources}) != len(sources)
                or not all(item["path"].startswith("content/")
                           and arabic_dominant(item.get("relevance_ar"))
                           for item in sources)):
            raise ValueError(f"Original passage inventory incomplete: {record['decision_id']}")
        localized = dict(decision)
        localized.update(sense=record["sense_ar"], rationale=record["rationale_ar"],
                         expert_question=record["expert_question_ar"],
                         english_term=" ".join(decision["english_term"].split()))
        display = dict(decision["review_display"])
        display["chosen_arabic"] = display["chosen_arabic"].replace("\\-", "")
        if "display_override_ar" in record:
            correction = record["display_override_ar"]
            target_excerpts = [
                loc.get("current_excerpt") or loc.get("excerpt") or ""
                for group in decision["index_metadata"]["occurrences"]
                for loc in group["locations"] if loc["source_kind"] != "english"
            ]
            macro = record.get("display_macro_witness")
            legacy_head = (record.get("display_from_legacy_head") is True
                           and decision["chosen_arabic"].startswith(correction))
            macro_ok = False
            if isinstance(macro, dict):
                logical = macro["logical_path"]
                line = macro["line"]
                if (not logical.startswith("source/locale/ar/")
                        or ".." in Path(logical).parts or not isinstance(line, int)
                        or line < 1 or sha256(ROOT / logical) != macro["sha256"]
                        or not arabic_dominant(macro.get("relevance_ar"))):
                    raise ValueError(f"Unverified token registry witness: {record['decision_id']}")
                content_lines = (ROOT / logical).read_text(encoding="utf-8").splitlines()
                macro_ok = (line <= len(content_lines)
                            and macro["needle"] in content_lines[line - 1]
                            and correction in content_lines[line - 1]
                            and any("!!{" in excerpt or "!!a{" in excerpt
                                    for excerpt in target_excerpts))
            if (not arabic_display_label(correction)
                    or not (macro_ok or legacy_head or any(" ".join(correction.split()) in " ".join(excerpt.split())
                                             for excerpt in target_excerpts))
                    or not arabic_dominant(record.get("display_correction_note_ar"))):
                raise ValueError(f"Unverified display correction: {record['decision_id']}")
            display["chosen_arabic"] = correction
        localized["review_display"] = display
        card, counts = decision_card(localized, title_overrides=batch["unit_title_ar"])
        if record.get("legacy_absent") is True:
            target_paths = {
                ROOT / loc["logical_path"]
                for group in decision["index_metadata"]["occurrences"]
                for loc in group["locations"] if loc["source_kind"] != "english"
            }
            chosen = display["chosen_arabic"]
            if (not target_paths or not arabic_dominant(record.get("legacy_note_ar"))
                    or any(chosen in path.read_text(encoding="utf-8") for path in target_paths)):
                raise ValueError(f"Unproven legacy-absent classification: {record['decision_id']}")
            card = card.replace("**المعنى المقصود:**",
                                "**حالة الاختيار في النص الجاري:** " + record["legacy_note_ar"]
                                + "\n\n**المعنى المقصود:**", 1)
        if record.get("display_macro_witness"):
            macro = record["display_macro_witness"]
            logical = macro["logical_path"]
            line = macro["line"]
            url = (f"https://github.com/KokunoYumeto/OpenLogic-ar/blob/{ARABIC_SOURCE_COMMIT}/"
                   f"{logical}#L{line}")
            card = card.replace("**المعنى المقصود:**",
                                f"**شاهد حل الرمز في ملف الطبعة:** [السطر {east(line)}]({url})"
                                f" — {macro['relevance_ar']}\n\n**المعنى المقصود:**", 1)
        if record.get("display_from_legacy_head") is True:
            card = card.replace("**المعنى المقصود:**",
                                "**صفة الرأس المختصر:** جزء عربي من رأس السجل الموروث، "
                                "لا اقتباس حرفي من السطر الجاري.\n\n**المعنى المقصود:**", 1)
        if inference or supplemental:
            original_label = f"الأصل الإنجليزي: `{localized['english_term']}`."
            derived_label = (("القضية التحريرية المستنبطة من تعريفات الأصل "
                              "(ليست عبارة حرفية منه): ") if inference else
                             ("مصطلح الأصل بشاهد إضافي مستعاد (لا يسجّل المؤشر "
                              "وقوعه الإنجليزي): "))
            derived_label += f"`{localized['english_term']}`."
            if card.count(original_label) != 1:
                raise ValueError(f"Editorial-inference label missing: {record['decision_id']}")
            card = card.replace(original_label, derived_label, 1)
            target_locations = [
                loc for group in decision["index_metadata"]["occurrences"]
                for loc in group["locations"]
                if loc.get("human_review_included") and loc["source_kind"] != "english"
            ]
            focus = record.get("target_focus")
            if len(target_locations) == 1 and isinstance(focus, dict):
                location = target_locations[0]
                focus_first, focus_last = focus["first_line"], focus["last_line"]
                if (not isinstance(focus_first, int) or not isinstance(focus_last, int)
                        or (not supplemental and
                            not location["line_start"] <= focus_first <= focus_last <= location["line_end"])):
                    raise ValueError(f"Editorial-inference target focus outside recorded note: {record['decision_id']}")
                path = ROOT / location["logical_path"]
                excerpt = "\n".join(path.read_text(encoding="utf-8").splitlines()[focus_first - 1:focus_last])
                if " ".join(focus["needle"].split()) not in " ".join(excerpt.split()):
                    raise ValueError(f"Editorial-inference focus text missing: {record['decision_id']}")
                url = (pinned_url(location["source_url"]).split("#L", 1)[0]
                       if location.get("source_url") else
                       f"https://github.com/KokunoYumeto/OpenLogic-ar/blob/{ARABIC_SOURCE_COMMIT}/"
                       + location["logical_path"])
                url += f"#L{focus_first}" + (f"-L{focus_last}" if focus_last != focus_first else "")
                label = east(focus_first) + (f"–{east(focus_last)}" if focus_last != focus_first else "")
                focus_heading = ("الموضع الدقيق في النص العربي" if supplemental
                                 else "الموضع الدقيق داخل التنبيه العربي")
                focus_note = f"**{focus_heading}:** [الأسطر {label}]({url}) — {focus['relevance_ar']}"
                if not arabic_dominant(focus["relevance_ar"]):
                    raise ValueError(f"Editorial-inference target focus lacks Arabic explanation: {record['decision_id']}")
            elif supplemental and record.get("target_witnesses"):
                witness_notes = []
                for witness in record["target_witnesses"]:
                    logical = witness["logical_path"]
                    first_line, last_line = witness["first_line"], witness["last_line"]
                    if (not logical.startswith("source/locale/ar") or ".." in Path(logical).parts
                            or not isinstance(first_line, int) or not isinstance(last_line, int)
                            or first_line < 1 or last_line < first_line
                            or not arabic_dominant(witness["relevance_ar"])
                            or sha256(ROOT / logical) != witness["sha256"]):
                        raise ValueError(f"Unverified supplemental Arabic witness: {record['decision_id']}")
                    excerpt = "\n".join((ROOT / logical).read_text(encoding="utf-8").splitlines()[first_line - 1:last_line])
                    if " ".join(witness["needle"].split()) not in " ".join(excerpt.split()):
                        raise ValueError(f"Supplemental Arabic witness text missing: {record['decision_id']}")
                    fragment = f"#L{first_line}" + (f"-L{last_line}" if last_line != first_line else "")
                    url = (f"https://github.com/KokunoYumeto/OpenLogic-ar/blob/{ARABIC_SOURCE_COMMIT}/"
                           + logical + fragment)
                    label = east(first_line) + (f"–{east(last_line)}" if last_line != first_line else "")
                    witness_notes.append(f"{witness['label_ar']}: [الأسطر {label}]({url}) — {witness['relevance_ar']}")
                focus_note = "**شواهد عربية دقيقة مستعادة استدراكًا:** " + "؛ ".join(witness_notes)
            else:
                raise ValueError(f"Original-index gap lacks exact Arabic supplemental witnesses: {record['decision_id']}")
            marker = "**كل وقوع مسجل لهذا القرار:**"
            card = card.replace(marker, focus_note + "\n\n" + marker, 1)
        pages = record["canon_pdf_pages"]
        if not set(pages) <= set(canon["visually_checked_pdf_pages"]):
            raise ValueError(f"Uninspected dictionary page: {record['decision_id']}")
        if not pages and record.get("canon_status") not in (
            "not-applicable", "not-found-in-checked-sources"
        ):
            raise ValueError(f"Dictionary applicability not explained: {record['decision_id']}")
        observed_pages.update(pages)
        alternatives = ("؛ ".join(record["alternatives_ar"]) if record["alternatives_ar"]
                        else "لا بديل محدد تقتضيه الشواهد في هذا الموضع")
        evidence = (
            ("**مواضع تعريفات الأصل الإنجليزي التي استُعملت في هذا الاستنباط:** "
             if inference else ("**شاهد الأصل الإنجليزي المستعاد استدراكًا:** "
                                if supplemental else
                                "**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** "))
            + source_links({"source_passages": sources}, overlay["english_source_commit"])
            + ("\n\n**وجه جمع المواضع:** " + record["source_relevance_ar"]
               if "source_passages" in record or record.get("source_from_occurrences") else "")
            + ("\n\n**حدود استدراك الشاهد:** " + record["source_witness_note_ar"]
               if supplemental else "")
            + ("\n\n**تصحيح رأس البطاقة من النص الجاري:** " + record["display_correction_note_ar"]
               if "display_override_ar" in record and not record.get("display_from_legacy_head") else
               "\n\n**تنقية رأس البطاقة الموروث:** " + record["display_correction_note_ar"]
               if "display_override_ar" in record else "")
            + ("\n\n**مواضع المعجم المعاينة:** "
               + "، ".join(canon_link(canon, page) for page in pages)
               + "\n\n**حدود الشاهد المعجمي:** " + record["canon_note_ar"]
               if pages else (
                   "\n\n**نتيجة البحث المعجمي المحدود:** "
                   if record["canon_status"] == "not-found-in-checked-sources"
                   else "\n\n**انطباق المعجم الرياضي:** "
               ) + record["canon_note_ar"])
            + "\n\n**بديل جدير بالمقارنة:** " + alternatives
            + "\n\n**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** " + record["confidence_ar"]
        )
        marker = "**كل وقوع مسجل لهذا القرار:**"
        if card.count(marker) != 1:
            raise ValueError(f"Missing location block: {record['decision_id']}")
        cards.append(card.replace(marker, evidence + "\n\n" + marker, 1))
        for key in totals:
            totals[key] += counts[key]
    if observed_pages != set(canon["visually_checked_pdf_pages"]):
        raise ValueError("Inspected dictionary-page inventory is not all cited")

    sections = batch["sections"]
    if [n for begin, end, _name, _title in sections for n in range(begin, end)] != list(range(len(ids))):
        raise ValueError("Card section partition is incomplete or overlapping")
    base = REVIEW_DIR / batch["directory"]
    base.mkdir(parents=True, exist_ok=True)
    inventory = []
    for begin, end, name, title in sections:
        path = base / name
        path.write_text(
            f"# بطاقات {title} — القرارات {east(first + begin)}–{east(first + end - 1)}\n\n"
            "[الرجوع إلى مقدمة الدفعة](README.md)\n\n" + "\n".join(cards[begin:end]),
            encoding="utf-8", newline="\n",
        )
        # A single high-frequency choice (notably proof) may need a larger
        # page to retain every recorded locator. Splitting its one card would
        # lose the one-decision reading unit; keep multi-card pages lean.
        card_page_limit = batch.get("single_card_limit_bytes", 400_000) if end - begin == 1 else 230_000
        if path.stat().st_size > card_page_limit:
            raise ValueError(f"Card page exceeds browseable size: {name}")
        inventory.append({"path": name, "bytes": path.stat().st_size,
                          "sha256": sha256(path), "decision_ids": ids[begin:end]})
    links = " · ".join(f"[{title}]({name})" for _begin, _end, name, title in sections)
    pages = "، ".join(east(page) for page in canon["visually_checked_pdf_pages"])
    page_label_note = (
        "رُبط كل موضع برقم صفحته المطبوع الذي عوين مباشرة."
        if "printed_page_labels" in canon
        else "ترقيم الكتاب المطبوع أقل باثنتي عشرة صفحة."
    )
    readme = base / "README.md"
    readme.write_text(
        f"# {batch['title_ar']}\n\n{links}\n\n"
        + batch["summary_ar"] + "\n\n" + batch["review_flags_ar"] + "\n\n"
        + overlay["editorial_basis_ar"] + "\n\n"
        + f"المصدر الاصطلاحي: {canon['identity']}؛ [صفحة النسخة]({canon['url']}). "
        + f"عُوينت صفحات PDF {pages}. {page_label_note} "
        + "لا تثبت هذه الصفحات وحدها جميع أساليب العربية التراثية.\n\n"
        + "صاغ هذه المراجعة اللاحقة وبطاقاتها OpenAI Codex — GPT-6 Sol، بمستوى جهد Ultra. "
        + "النصوص الإنجليزية والعربية المقتبسة موروثة من المصادر الموصولة. "
        + "لم تقع مراجعة بشرية شاملة؛ كل اختيار قابل للتصحيح.\n\n"
        + f"هذه دفعة محلية لم تُنشر بعد. مع هذه الدفعة تبلغ التغطية "
        + f"العربية المحلية {east(batch['local_after'])} من ١٠٩٥ اختيارًا؛ "
        + f"التغطية المنشورة حاليًا {east(batch['public_before'])} من ١٠٩٥.\n",
        encoding="utf-8", newline="\n",
    )
    receipt = {
        "status": "LOCAL_ARABIC_REVIEW_BATCH_PENDING_INDEPENDENT_READBACK",
        "source_index_sha256": overlay["source_index_sha256"],
        "overlay_sha256": sha256(overlay_path), "choice_count": len(ids),
        "decision_ids": ids, "totals": totals,
        "readme": {"bytes": readme.stat().st_size, "sha256": sha256(readme)},
        "cards": inventory,
    }
    (base / "BUILD_RECEIPT.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"status": receipt["status"], "choices": len(ids), **totals}, ensure_ascii=True))


if __name__ == "__main__":
    main()
