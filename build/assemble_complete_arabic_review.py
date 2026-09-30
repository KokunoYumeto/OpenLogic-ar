#!/usr/bin/env python3
"""Assemble one searchable Arabic review directory and corrected JSONL ledger."""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import re
from pathlib import Path

from stream_expert_review_decisions import iter_decisions


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "expert-review/2026-09-26-final-page-review"
TERM = ROOT / "evidence/classical/terminology"
INDEX = ROOT / "tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json"
EXPECTED = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"
EAST = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(part)
    return h.hexdigest().upper()


def arabic(value: object) -> bool:
    if not isinstance(value, str):
        return False
    a = sum("\u0600" <= c <= "\u06ff" for c in value)
    e = sum("a" <= c.lower() <= "z" for c in value)
    return a >= 12 and a > e


def clean(value: object, limit: int | None = None) -> str:
    result = " ".join(str(value or "").split()).replace("|", "\\|")
    return (result[:limit - 1] + "…" if limit and len(result) > limit else result)


def card_map(include_revisions: bool = True) -> dict[str, str]:
    mapping = {}

    def add(ids: list[str], link: str) -> None:
        path = BASE / link
        if not path.is_file():
            raise AssertionError(f"Missing review card: {path}")
        for decision_id in ids:
            if decision_id in mapping:
                raise AssertionError(f"Decision has two cards: {decision_id}")
            mapping[decision_id] = link.replace("\\", "/")

    existing = json.loads((BASE / "arabic-existing/BUILD_RECEIPT.json").read_text(encoding="utf-8"))
    for shard in existing["shards"]:
        path = ROOT / shard["path"]
        assert sha(path) == shard["sha256"]
        add(shard["decision_ids"], "arabic-existing/" + Path(shard["path"]).name)
    first = json.loads((BASE / "BATCH_31_38_READBACK.json").read_text(encoding="utf-8"))
    assert first["status"].startswith("PASS")
    status = json.loads((BASE / "PUBLICATION_STATUS_READBACK.json").read_text(encoding="utf-8"))
    assert status["status"] == "PASS_STATUS_ONLY_FINALIZATION"
    first_change = next(c for c in status["changed_files"]
                        if c["path"].endswith("/BATCH_31_38_AR.md"))
    assert first_change["original_sha256"] == first["markdown_sha256"]
    assert sha(BASE / "BATCH_31_38_AR.md") == first_change["final_sha256"]
    add(first["decision_ids"], "BATCH_31_38_AR.md")
    priority_receipt = json.loads((BASE / "READBACK.json").read_text(encoding="utf-8"))
    assert priority_receipt["status"].startswith("PASS")
    assert sha(BASE / "START_HERE_AR.md") == priority_receipt["guide_sha256"]
    priority = json.loads((TERM / "ARABIC_PRIORITY_30_20260926.json").read_text(encoding="utf-8"))
    assert len(priority["records"]) == priority_receipt["priority_decisions"] == 30
    add([item["decision_id"] for item in priority["records"]], "START_HERE_AR.md")
    directories = sorted(path for path in BASE.iterdir() if path.is_dir()
                         and (path.name.startswith("arabic-senses-")
                              or path.name.startswith("arabic-decisions-")))
    for directory in directories:
        receipt = json.loads((directory / "BUILD_RECEIPT.json").read_text(encoding="utf-8"))
        readback = json.loads((directory / "INDEPENDENT_READBACK.json").read_text(encoding="utf-8"))
        assert readback["status"].startswith("PASS")
        assert receipt["source_index_sha256"] == EXPECTED
        cards = receipt["cards"]
        if isinstance(cards, dict):
            card_file = directory / "CARDS.md"
            assert sha(card_file) == cards["sha256"]
            add(receipt["decision_ids"], f"{directory.name}/CARDS.md")
        else:
            for card in cards:
                card_file = directory / card["path"]
                assert sha(card_file) == card["sha256"]
                add(card["decision_ids"], f"{directory.name}/{card['path']}")
            assert set(receipt["decision_ids"]) == {
                decision_id for card in cards for decision_id in card["decision_ids"]}
    global_readback = json.loads((BASE / "global-caption-decisions/INDEPENDENT_READBACK.json")
                                 .read_text(encoding="utf-8"))
    assert global_readback["status"].startswith("PASS")
    global_doc = json.loads((BASE / "global-caption-decisions/DECISIONS.json").read_text(encoding="utf-8"))
    add([item["decision_id"] for item in global_doc["records"]],
        "global-caption-decisions/CARDS.md")
    if not include_revisions:
        return mapping
    witnesses = source_witness_corrections()
    for item in witnesses.get("records", []):
        identifier = item["decision_id"]
        assert identifier in mapping
        path = BASE / witnesses["review_card"]
        assert path.is_file() and identifier in path.read_text(encoding="utf-8")
        mapping[identifier] = witnesses["review_card"]
    revision = review_corrections()
    for item in revision.get("records", []):
        identifier = item["decision_id"]
        assert identifier in mapping, "Correction cannot introduce an unrecorded decision"
        path = BASE / revision["review_card"]
        assert path.is_file() and identifier in path.read_text(encoding="utf-8")
        mapping[identifier] = revision["review_card"]
    for rechecks in recheck_layers():
        for item in rechecks.get("records", []):
            identifier = item["decision_id"]
            assert identifier in mapping
            path = BASE / rechecks["review_card"]
            assert path.is_file() and identifier in path.read_text(encoding="utf-8")
            mapping[identifier] = rechecks["review_card"]
    return mapping


def review_corrections() -> dict:
    path = TERM / "SOL6_REEXAMINATION_CORRECTIONS_20260930.json"
    if not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    assert value["schema"] == "openlogic-arabic-review-evidenced-corrections-v1"
    assert value["source_index_sha256"] == EXPECTED
    assert value["model"] == "GPT-6.1 Sol" and value["effort"] == "Ultra"
    assert len({r["decision_id"] for r in value["records"]}) == len(value["records"])
    return value


def source_witness_corrections() -> dict:
    path = TERM / "SOL6_SOURCE_WITNESS_CORRECTIONS_20260930.json"
    if not path.exists():
        return {}
    value = json.loads(path.read_bytes())
    assert value["schema"] == "openlogic-arabic-source-witness-corrections-v1"
    assert value["source_index_sha256"] == EXPECTED
    assert value["model"] == "GPT-6.1 Sol" and value["effort"] == "Ultra"
    assert len(value["records"]) == len({r["decision_id"] for r in value["records"]}) == 32
    assert sum(len(r["removed_non_supporting_pointers"]) for r in value["records"]) == 59
    return value


def function_definition_rechecks() -> dict:
    path = TERM / "SOL6_FUNCTION_DEFINITIONS_RECHECK_20260930.json"
    if not path.exists():
        return {}
    value = json.loads(path.read_bytes())
    assert value["schema"] == "openlogic-arabic-function-definitions-recheck-v1"
    assert value["source_index_sha256"] == EXPECTED
    assert value["model"] == "GPT-6.1 Sol" and value["effort"] == "Ultra"
    assert len(value["records"]) == len({r["decision_id"] for r in value["records"]}) == 3
    assert value["source_edit_applied"] is False
    return value


def contextual_rechecks() -> dict:
    path = TERM / "SOL6_CONTEXTUAL_RECHECK_20260930.json"
    if not path.exists():
        return {}
    value = json.loads(path.read_bytes())
    assert value["schema"] == "openlogic-arabic-contextual-recheck-v1"
    assert value["source_index_sha256"] == EXPECTED
    assert value["model"] == "GPT-6.1 Sol" and value["effort"] == "Ultra"
    assert len(value["records"]) == len({r["decision_id"] for r in value["records"]}) == 5
    assert value["source_edit_applied"] is False
    assert sum(len(r["checked_occurrences"]) for r in value["records"]) == 21
    return value


def proof_quantification_rechecks() -> dict:
    path = TERM / "SOL6_PROOF_QUANTIFICATION_RECHECK_20260930.json"
    if not path.exists():
        return {}
    value = json.loads(path.read_bytes())
    assert value["schema"] == "openlogic-arabic-contextual-recheck-v1"
    assert value["source_index_sha256"] == EXPECTED
    assert value["model"] == "GPT-6.1 Sol" and value["effort"] == "Ultra"
    assert len(value["records"]) == len({r["decision_id"] for r in value["records"]}) == 3
    assert value["source_edit_applied"] is True
    assert sum(len(r["checked_occurrences"]) for r in value["records"]) == 69
    assert len(value["source_transitions"]) == 1
    return value


def free_bound_variable_recheck() -> dict:
    path = TERM / "SOL6_FREE_BOUND_VARIABLE_RECHECK_20260930.json"
    if not path.exists():
        return {}
    value = json.loads(path.read_bytes())
    assert value["schema"] == "openlogic-arabic-contextual-recheck-v1"
    assert value["source_index_sha256"] == EXPECTED
    assert value["model"] == "GPT-6.1 Sol" and value["effort"] == "Ultra"
    assert len(value["records"]) == 1
    assert value["records"][0]["decision_id"] == "RETRO0051-0100-free-bound-variable"
    assert value["source_edit_applied"] is False
    assert len(value["records"][0]["checked_occurrences"]) == 3
    return value


def recheck_layers() -> tuple[dict, ...]:
    return (function_definition_rechecks(), contextual_rechecks(),
            proof_quantification_rechecks(), free_bound_variable_recheck())


def note_map() -> dict[str, dict]:
    notes = {}
    files = ([TERM / "ARABIC_PRIORITY_30_20260926.json",
              TERM / "ARABIC_REVIEW_BATCH_31_38_20260927.json"]
             + sorted(TERM.glob("ARABIC_SENSES_BATCH_*_20260927.json"))
             + sorted(TERM.glob("ARABIC_REVIEW_BATCH_*_20260927.json")))
    for path in files:
        obj = json.loads(path.read_text(encoding="utf-8"))
        for record in obj.get("records", []):
            decision_id = record["decision_id"]
            if decision_id in notes and path.name != "ARABIC_REVIEW_BATCH_31_38_20260927.json":
                raise AssertionError(f"Repeated note: {decision_id}")
            notes[decision_id] = record
    global_doc = json.loads((BASE / "global-caption-decisions/DECISIONS.json").read_text(encoding="utf-8"))
    for item in global_doc["records"]:
        assert item["decision_id"] not in notes
        notes[item["decision_id"]] = item
    for item in review_corrections().get("records", []):
        assert item["decision_id"] in notes, "Correction must replace an existing note"
        notes[item["decision_id"]] = item
    for rechecks in recheck_layers():
        for item in rechecks.get("records", []):
            assert item["decision_id"] in notes
            notes[item["decision_id"]] = item
    return notes


def representative(decision: dict) -> str:
    groups = decision["index_metadata"]["occurrences"]
    if not groups:
        bindings = decision.get("global_source_bindings") or []
        if bindings:
            first = bindings[0]
            return f"ملف عام: {Path(first['logical_path']).name}، سطر {str(first['line_start']).translate(EAST)}"
        return "لا موضع مسجل"
    units = []
    pages = {}
    for group in groups:
        unit = (group.get("unit") or {}).get("unit_id")
        if unit and unit not in units:
            units.append(unit)
        for location in group["locations"]:
            if location["source_kind"] not in {"msa", "classical"}:
                continue
            for evidence in location.get("page_evidence") or []:
                if not evidence.get("pdf_pages"):
                    continue
                key = "الدولية/المشرق" if location["source_kind"] == "msa" else "التراثية"
                if key not in pages or (evidence.get("exact_occurrence_page")
                                        and not pages[key][1]):
                    pages[key] = (evidence["pdf_pages"][0], bool(evidence.get("exact_occurrence_page")))
    parts = [", ".join(units[:2]) + (f" +{len(units)-2}" if len(units) > 2 else "")]
    for key in ("الدولية/المشرق", "التراثية"):
        if key in pages:
            page, exact = pages[key]
            parts.append(f"{key} PDF ص {str(page).translate(EAST)}" + (" تقريبًا" if not exact else ""))
    if not pages:
        parts.append("الموضع التفصيلي في البطاقة؛ لا صفحة دقيقة مثبتة")
    return "؛ ".join(part for part in parts if part)


def main() -> None:
    assert sha(INDEX) == EXPECTED
    links = card_map()
    notes = note_map()
    witness_revision = {r["decision_id"]: r for r in source_witness_corrections().get("records", [])}
    recheck_documents = {}
    for rechecks in recheck_layers():
        for row in rechecks.get("records", []):
            assert row["decision_id"] not in recheck_documents
            recheck_documents[row["decision_id"]] = rechecks
    decisions = []
    seen = set()
    for decision in iter_decisions(INDEX):
        if not decision["index_metadata"]["human_index_included"]:
            continue
        decision_id = decision["decision_id"]
        if decision_id in seen:
            raise AssertionError(f"Duplicate frozen ID: {decision_id}")
        seen.add(decision_id)
        note = notes.get(decision_id, {})
        display = decision.get("review_display", {})
        chosen = (note.get("display_override_ar") or note.get("surface_ar")
                  or display.get("chosen_arabic") or decision["chosen_arabic"])
        sense = note.get("sense_ar") or display.get("sense") or decision.get("sense")
        rationale = (note.get("rationale_ar") or display.get("rationale")
                     or decision.get("rationale"))
        question = (note.get("expert_question_ar") or note.get("question_ar")
                    or display.get("expert_question") or decision.get("expert_question"))
        if not all(arabic(value) for value in (sense, rationale, question)):
            raise AssertionError(f"Incomplete Arabic justification: {decision_id}")
        if decision_id not in links:
            raise AssertionError(f"Missing card for {decision_id}")
        decisions.append({
            "decision_id": decision_id, "english_term": decision["english_term"],
            "chosen_arabic": chosen, "sense_ar": sense, "rationale_ar": rationale,
            "expert_question_ar": question, "review_card": links[decision_id],
            "representative_location_ar": representative(decision),
            "original_occurrences": decision["index_metadata"]["occurrences"],
            "global_source_bindings": decision.get("global_source_bindings", []),
            "open_to_correction": True,
        })
        if "source_bindings" in note:
            decisions[-1]["revision_source_bindings"] = note["source_bindings"]
            decisions[-1]["revision_target_bindings"] = note["target_bindings"]
            decisions[-1]["revision_canon_limit_ar"] = note["canon_limit_ar"]
            decisions[-1]["revision_confidence_ar"] = note["confidence_ar"]
            decisions[-1]["revision_source_identity_note_ar"] = (
                recheck_documents.get(decision_id) or review_corrections())["source_identity_note_ar"]
        if decision_id in recheck_documents:
            rechecks = recheck_documents[decision_id]
            decisions[-1]["revision_canon_evidence"] = note["canon_evidence"]
            decisions[-1]["revision_canon_sources"] = rechecks["canon_sources"]
            decisions[-1]["revision_register_comparison"] = rechecks["register_comparison"]
            decisions[-1]["revision_alternatives_ar"] = note["alternatives_ar"]
            decisions[-1]["revision_checked_occurrences"] = note["checked_occurrences"]
            decisions[-1]["revision_recording_mode"] = rechecks["recording_mode"]
            if "context_bindings" in note:
                decisions[-1]["revision_context_bindings"] = note["context_bindings"]
            if rechecks.get("source_transitions"):
                decisions[-1]["revision_source_transitions"] = rechecks["source_transitions"]
                decisions[-1]["revision_body_corrections_ar"] = rechecks["body_corrections_ar"]
                decisions[-1]["revision_source_edit_applied"] = rechecks["source_edit_applied"]
        if decision_id in witness_revision:
            decisions[-1]["source_witness_revision"] = witness_revision[decision_id]
    assert len(decisions) == len(seen) == len(links) == 1095
    decisions.sort(key=lambda row: (row["english_term"].casefold(), row["decision_id"]))
    directory = [
        "# الدليل الكامل لقرارات الترجمة العربية — ١٠٩٥ من ١٠٩٥\n",
        "[ابدأ من هنا](INDEX_AR.md) · [دليل الأولويات](START_HERE_AR.md) · "
        "[قرارات التعليقات العامة](global-caption-decisions/CARDS.md)\n",
        "ابحث هنا بالمصطلح الإنجليزي أو العربي. يعرض السطر اختيار الطبعة وموضعًا ممثلًا "
        "وسببًا موجزًا؛ افتح البطاقة لرؤية **جميع** الوقوعات المسجلة، وأسطر الأصل والترجمة "
        "وروابط صفحات القارئ الدقيقة أو المعلَّمة بأنها تقريبية، والشاهد المعجمي وحدوده "
        "والبدائل وسؤال المراجع. السبب المختصر لا يحل محل التعليل الكامل في البطاقة.\n",
        "السجلات الثلاثة للتعليقات العامة لا تقع في وحدة من متن الكتاب؛ يرد رابط ملف المصدر "
        "بدلًا من صفحة مختلقة. الرقم في عمود الموضع مثال للعثور، لا حصر لجميع الوقوعات.\n",
        "| الأصل الإنجليزي | اللفظ أو الصياغة العربية | موضع مثال | لماذا؟ (خلاصة) | البطاقة الكاملة |",
        "|---|---|---|---|---|",
    ]
    for item in decisions:
        directory.append("| " + " | ".join([
            clean(item["english_term"], 100), clean(item["chosen_arabic"], 100),
            clean(item["representative_location_ar"], 120),
            clean(item["rationale_ar"], 180),
            f"[كل المواضع والسؤال]({item['review_card']})",
        ]) + " |")
    directory.append("\nأُنجزت الترجمة والتعليلات الموروثة بواسطة OpenAI Codex — GPT-5.6 Sol، "
                     "بمستوى جهد Ultra؛ وصيغت المراجعات العربية اللاحقة والربط والتحقق "
                     "بواسطة OpenAI Codex — GPT-6 Sol، بمستوى جهد Ultra. "
                     "وصُحِّحت شروح قابلية المحورة والتجاوز والمختزلات وإحالاتها بواسطة OpenAI Codex — GPT-6.1 Sol، "
                     "بمستوى جهد Ultra؛ وقوبلت ثلاثة تعريفات للدوال وخمسة اختيارات أخرى في سياقاتها "
                     "بالمستوى نفسه، وثلاثة قرارات في المتغير المميّز والروابط والمكمّمات؛ "
                     "وصُحح نطاق شاهد المتغير الحر والمقيد، مع إبقاء فجوة الشاهد المستقل ظاهرة؛ "
                     "نُقل تصحيحان إلى المصدر المعياري المشترك؛ تحفظ البطاقة حالة المصدر عند المقابلة الأولى، "
                     "ويبين مدخل القراءة حالة القارئين الحالية. الصفحات الموروثة ليست قياسًا جديدًا. فجوات الشاهد ظاهرة. "
                     "لم تقع مراجعة بشرية شاملة؛ كل اختيار قابل للتصحيح.\n")
    historic = BASE / "COMPLETE_DIRECTORY_RECEIPT_20260927_HISTORICAL.json"
    previous_receipt = BASE / "COMPLETE_DIRECTORY_RECEIPT.json"
    if previous_receipt.exists() and not historic.exists():
        historic.write_bytes(previous_receipt.read_bytes())
    (BASE / "DIRECTORY_AR.md").write_text("\n".join(directory), encoding="utf-8", newline="\n")
    machine_path = BASE / "DECISION_RECORD_AR.jsonl.gz"
    with machine_path.open("wb") as sink:
        with gzip.GzipFile(fileobj=sink, mode="wb", filename="", mtime=0, compresslevel=9) as zipper:
            with io.TextIOWrapper(zipper, encoding="utf-8", newline="\n") as writer:
                for item in decisions:
                    writer.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n")
    receipt = {
        "status": "COMPLETE_LOCAL_ARABIC_REVIEW_DIRECTORY_PENDING_PUBLIC_READBACK",
        "source_index_sha256": EXPECTED, "decision_count": len(decisions),
        "all_frozen_decisions_mapped_exactly_once": True,
        "directory": {"path": "DIRECTORY_AR.md", "bytes": (BASE / "DIRECTORY_AR.md").stat().st_size,
                      "sha256": sha(BASE / "DIRECTORY_AR.md")},
        "machine_record": {"path": "DECISION_RECORD_AR.jsonl.gz",
                           "bytes": machine_path.stat().st_size, "sha256": sha(machine_path)},
    }
    (BASE / "COMPLETE_DIRECTORY_RECEIPT.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, ensure_ascii=True))


if __name__ == "__main__":
    main()
