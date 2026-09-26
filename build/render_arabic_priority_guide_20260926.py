#!/usr/bin/env python3
"""Render the checked Arabic priority review guide from pinned decision data."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json"
LEDGER = ROOT / "evidence/classical/terminology/ARABIC_PRIORITY_30_20260926.json"
MANUAL_POTENT = ROOT / "evidence/classical/terminology/PRIORITY_MANUAL_POTENT_LOCATOR_20260926.json"
OUTPUT = ROOT / "expert-review/2026-09-26-final-page-review/START_HERE_AR.md"
INDEX_SHA256 = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"
SOURCE_COMMIT = "86a4a7c11c0a0289ade28cb8f96acbacf9c01844"
PDFS = {
    "classical": "https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf",
    "international": "https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf",
    "machrek": "https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf",
}
RAW_INDEX_URL = (
    "https://raw.githubusercontent.com/KokunoYumeto/OpenLogic-ar/main/"
    "expert-review/2026-09-26-final-page-review/EXPERT_REVIEW_INDEX.json.gz"
)
LABELS = {
    "classical": "الطبعة التراثية",
    "international": "الطبعة الدولية",
    "machrek": "طبعة المشرق",
}
LOCAL_PDFS = {
    "classical": ROOT / "output/pdf/classical-arabic-eastern-rtl/primary-olp0658-bibltr-mathdir-20260926a/OPENLOGIC_ar_CLASSICAL_COMPLETE_722_UNIT_READER_EASTERN_ARABIC_RTL_OLP-0722.pdf",
    "international": ROOT / "output/pdf/msa-20260922-26eda8e915cb-primary/00_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_INTERNATIONAL_NOTATION_OLP-0722.pdf",
    "machrek": ROOT / "output/pdf/msa-20260922-26eda8e915cb-primary/01_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_MACHREK_NOTATION_OLP-0722.pdf",
}
CONFIDENCE = {"high": "عالية", "medium": "متوسطة", "low": "منخفضة"}
PREFERRED_EXCERPTS = {
    "RETRO0051-0100-sequent": ("تتابعية",),
    "repair-0401-0500:TERM-MODAL": ("المنطق الموجهي", "المنطق الجهوي", "المنطق الجهي"),
    "repair-0401-0500:TERM-ACCESS": ("علاقة الوصول", "علاقة النفاذ", "علاقة الإتاحة"),
    "RETRO0051-0100-indirect-proof": ("البرهان غير المباشر", "برهان بالخلف", "خلاف الفرض"),
    "ar-classical-0451-0500-branch": ("فرع مفتوح", "شعبة", "في الفرع"),
    "ar-classical-0451-0500-equivalence-class": ("فئة التكافؤ", "فئات التكافؤ"),
    "TERM-REFLECTION-RELATIVIZATION-ABSOLUTENESS": ("الانعكاس", "نسبنة", "إطلاق"),
    "TERM-TRUTH-FUNCTIONAL": ("داليّا الصدق", "دوال الصدق"),
    "ar-classical-0701-0722-sequent": ("المتتالية", "التتابعية"),
    "ar-classical-0701-0722-quantifier": ("المكم", "المكمّ"),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def east(value: object) -> str:
    return str(value).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))


def pinned_url(url: str) -> str:
    return url.replace(
        "https://github.com/KokunoYumeto/OpenLogic-ar/blob/main/",
        f"https://github.com/KokunoYumeto/OpenLogic-ar/blob/{SOURCE_COMMIT}/",
    )


def reader_kind(name: str) -> str | None:
    if name.startswith("الطبعة التراثية"):
        return "classical"
    if name.startswith("الطبعة الدولية"):
        return "international"
    if name.startswith("طبعة المشرق"):
        return "machrek"
    return None


def source_line(location: dict) -> int:
    current = location.get("line_reconciliation", {}).get("current_line_start")
    if isinstance(current, int) and current > 0:
        return current
    recorded = location.get("line_start")
    if isinstance(recorded, int) and recorded > 0:
        return recorded
    match = re.search(r"#L([0-9]+)$", location.get("source_url") or "")
    if match:
        return int(match.group(1))
    raise ValueError(f"Resolved location has no usable source line: {location.get('location_id')}")


def representative_locations(decision: dict) -> tuple[dict, dict]:
    candidates: dict[str, list[tuple[tuple[int, int, int, int, int], dict, dict]]] = {
        key: [] for key in LABELS
    }
    counts = {"english": 0, "msa": 0, "classical": 0}
    original = None
    for occurrence in decision["index_metadata"]["occurrences"]:
        for location in occurrence["locations"]:
            if not location.get("human_review_included"):
                continue
            source_kind = location["source_kind"]
            if source_kind in counts:
                counts[source_kind] += 1
            if not location.get("source_url") or not location.get("line_reconciliation", {}).get("resolved"):
                continue
            if source_kind == "english" and original is None:
                original = location
            for page in location.get("page_evidence", []):
                kind = reader_kind(page.get("reader", ""))
                if kind is None or not page.get("pdf_pages"):
                    continue
                rank = {"synctex-exact": 0, "unit-start-fallback": 1}.get(
                    page.get("method"), 2
                )
                snippet = location.get("current_excerpt") or location.get("excerpt") or ""
                preferred = PREFERRED_EXCERPTS.get(decision["decision_id"])
                preference_penalty = (
                    min((i for i, term in enumerate(preferred) if term in snippet), default=len(preferred))
                    if preferred else 0
                )
                comment_penalty = int(snippet.lstrip().startswith("%"))
                score = (
                    comment_penalty,
                    preference_penalty,
                    rank,
                    source_line(location),
                    int(page["pdf_pages"][0]),
                )
                candidates[kind].append((score, location, page))
    chosen = {}
    for kind, entries in candidates.items():
        if entries:
            entries.sort(key=lambda item: item[0])
            _, location, page = entries[0]
            chosen[kind] = (location, page)
    return {"chosen": chosen, "original": original}, counts


def display_choice(decision: dict) -> str:
    if decision["decision_id"] == "RETRO0051-0100-indirect-proof":
        return (
            "البرهان غير المباشر؛ وفي العربية المعيارية «البرهان بالخلف» أيضًا، "
            "وقد تُعاد صياغة مواضع التراثية من غير تسمية الطريقة"
        )
    return decision["review_display"]["chosen_arabic"]


def excerpt(location: dict, decision_id: str | None = None) -> str:
    raw = " ".join((location.get("current_excerpt") or location.get("excerpt") or "").split())
    if len(raw) <= 260:
        return raw
    terms = PREFERRED_EXCERPTS.get(decision_id or "", ())
    found = [(i, raw.find(term), term) for i, term in enumerate(terms) if term in raw]
    if found:
        _, start, term = min(found)
        lo = max(0, start - 70)
        hi = min(len(raw), max(start + len(term) + 110, lo + 220))
        return ("…" if lo else "") + raw[lo:hi].strip() + ("…" if hi < len(raw) else "")
    return raw[:257].rstrip() + "…"


def page_links(kind: str, page: dict) -> str:
    printed = {
        int(item["pdf_page"]): item.get("printed_page")
        for item in page.get("printed_pages", [])
    }
    parts = []
    for number in page["pdf_pages"][:3]:
        link = f"[ص {east(number)}]({PDFS[kind]}#page={number})"
        if printed.get(int(number)):
            link += f" (ترقيم المتن: {east(printed[int(number)])})"
        parts.append(link)
    if len(page["pdf_pages"]) > 3:
        parts.append(f"و{east(len(page['pdf_pages']) - 3)} صفحات أخرى")
    return "، ".join(parts)


def manually_verified_potent_examples() -> dict:
    manual = json.loads(MANUAL_POTENT.read_text(encoding="utf-8"))
    if manual["decision_id"] != "TERM-POTENT-SET" or manual["source_commit"] != SOURCE_COMMIT:
        raise ValueError("Manual potent-set locator points to another decision or source commit")
    line_number = manual["source_line"]
    if line_number != 13:
        raise ValueError("Unexpected manually checked source line")
    source_by_kind = {
        "classical": manual["classical_source"],
        "international": manual["msa_source"],
        "machrek": manual["msa_source"],
    }
    pdf_by_kind = {
        "classical": manual["classical_source"],
        "international": manual["international_pdf"],
        "machrek": manual["machrek_pdf"],
    }
    out = {}
    for kind in LABELS:
        source = source_by_kind[kind]
        path = ROOT / source["path"]
        if digest(path) != source["sha256"]:
            raise ValueError(f"Changed manual source: {path}")
        line = path.read_text(encoding="utf-8").splitlines()[line_number - 1]
        if hashlib.sha256(line.encode("utf-8")).hexdigest().upper() != source["line_sha256"]:
            raise ValueError(f"Changed manual source line: {path}:{line_number}")
        if manual["target_term"] not in line:
            raise ValueError(f"Manual term absent from source line: {path}:{line_number}")
        pdf = pdf_by_kind[kind]
        if digest(LOCAL_PDFS[kind]) != pdf["pdf_sha256"]:
            raise ValueError(f"Changed manually inspected PDF: {LOCAL_PDFS[kind]}")
        number = pdf["pdf_page"]
        location = {
            "source_url": f"https://github.com/KokunoYumeto/OpenLogic-ar/blob/{SOURCE_COMMIT}/{source['path']}#L{line_number}",
            "line_start": line_number,
            "current_excerpt": line.strip(),
        }
        page = {
            "method": "visual-text-exact",
            "pdf_pages": [number],
            "printed_pages": [{"pdf_page": number, "printed_page": pdf["printed_page"]}],
        }
        out[kind] = (location, page)
    return out


def render() -> tuple[str, int]:
    if digest(INDEX) != INDEX_SHA256:
        raise ValueError("Final-page index hash changed; do not render against an unverified index")
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if ledger["source_index_sha256"].upper() != INDEX_SHA256:
        raise ValueError("Priority ledger refers to a different review index")
    records = ledger["records"]
    if len(records) != 30 or len({r["decision_id"] for r in records}) != 30:
        raise ValueError("Expected exactly 30 distinct priority records")
    decisions = {d["decision_id"]: d for d in index["decisions"]}
    lines = [
        "# ابدأ من هنا: ثلاثون اختيارًا عربيًا تُستحسن مراجعته",
        "",
        "هذه قائمة أولى لأهل الاختصاص، لا حصر لجميع اختيارات الكتاب. تشمل الطبعات "
        "العربية الثلاث: الدولية، والمشرقية، والتراثية ذات الترقيم المشرقي. "
        "أُنجزت نصوص القراء كاملة؛ والأسئلة أدناه دعوة إلى تصحيح الاختيارات "
        "المصطلحية أو البيانية، وليست شرطًا لنشر النص أو إتاحته.",
        "",
        "يصل رابط «السطر» إلى ملف مصدر ثابت عند النسخة المحفوظة في GitHub؛ "
        "ويصل رابط «ص» إلى صفحة من ملف PDF المنشور. إذا ظهر للموضع أكثر من "
        "رقم صفحة، فذلك لأن النص قد يظهر في القارئ أكثر من مرة. الشاهد المقتبس "
        "مثال يسهل البدء به، لا جميع مواضع اللفظ؛ أعداد المواضع في آخر كل بند "
        "تتعلق بسجلات الإحالة، لا بعدد الألفاظ المختلفة. علامات `!!{…}` مفاتيح "
        "اصطلاحية في مصدر LaTeX؛ تظهر بألفاظها العربية في القارئ PDF.",
        "",
        "الترجمة والصياغة والتصحيحات الموروثة: OpenAI Codex — GPT-5.6 Sol، "
        "بمستوى جهد Ultra. تجميع الطبعة الأخيرة والتحقق من صفحاتها وصياغة "
        "هذه التعليلات العربية: OpenAI Codex — GPT-6 Sol، بمستوى جهد Ultra. "
        "التعليل تحرير لاحق للقرار المسجل، لا ادعاء بأنه كان سبب قرار المترجم "
        "الأول. لم تُجر مراجعة بشرية عربية شاملة؛ وكل حكم هنا قابل للتصحيح.",
        "",
    ]
    exact_examples = 0
    for position, record in enumerate(records, 1):
        decision = decisions.get(record["decision_id"])
        if decision is None or not decision["index_metadata"]["human_index_included"]:
            raise ValueError(f"Missing human review decision: {record['decision_id']}")
        for key in ("sense_ar", "rationale_ar", "question_ar"):
            if not record.get(key, "").strip():
                raise ValueError(f"Empty Arabic field {key}: {record['decision_id']}")
        locations, counts = representative_locations(decision)
        manual_example = decision["decision_id"] == "TERM-POTENT-SET"
        if manual_example:
            if locations["chosen"]:
                raise ValueError("Manual potent override is no longer needed; reconcile the index")
            locations["chosen"] = manually_verified_potent_examples()
        if "classical" not in locations["chosen"]:
            raise ValueError(f"No Classical reader page for {record['decision_id']}")
        lines.extend(
            [
                f"## {east(position)}. {display_choice(decision)}",
                "",
                f"الأصل الإنجليزي: `{decision['english_term']}`. "
                f"معرّف القرار: `{decision['decision_id']}`.",
                "",
                f"**المعنى المقصود:** {record['sense_ar']}",
                "",
                f"**لماذا اختير هذا اللفظ مؤقتًا؟** {record['rationale_ar']}",
                "",
                f"**سؤال للمراجع:** {record['question_ar']}",
                "",
                "**مواضع للبدء:**",
                "",
            ]
        )
        for kind in ("classical", "international", "machrek"):
            selected = locations["chosen"].get(kind)
            if not selected:
                continue
            location, page = selected
            if page.get("method") in {"synctex-exact", "visual-text-exact"}:
                exact_examples += 1
                qualification = (
                    " — إحالة تعريف فُحصت بصريًا ولم تُدمج بعد في فهرس جميع المواضع"
                    if page.get("method") == "visual-text-exact"
                    else ""
                )
            else:
                qualification = " — إحالة إلى بداية الوحدة، لا إلى السطر بعينه"
            line_number = source_line(location)
            source = pinned_url(location["source_url"])
            lines.append(
                f"- **{LABELS[kind]}:** [المصدر، السطر {east(line_number)}]({source})؛ "
                f"PDF: {page_links(kind, page)}{qualification}. "
                f"الشاهد: «{excerpt(location, decision['decision_id'])}»"
            )
        original = locations["original"]
        if original is not None:
            lines.append(
                f"- **الأصل الإنجليزي:** [السطر {east(source_line(original))}]"
                f"({original['source_url']})؛ «{excerpt(original)}»"
            )
        lines.extend(
            [
                "",
                f"المواضع المسجلة: الأصل {east(counts['english'])}، "
                f"العربية المعيارية {east(counts['msa'])}، "
                f"العربية التراثية {east(counts['classical'])}. "
                "هذه أمثلة بدء؛ انظر السجل الكامل عند نشره لجميع الإحالات.",
                "",
            ]
        )
    lines.extend(
        [
            "---",
            "",
            "هذه الطبقة العربية تغطي ثلاثين قرارًا ذا أولوية من سجل يحوي "
            "١٠٩٥ اختيارًا موجهًا إلى القارئ. القائمة الكاملة ذات التعليلات "
            "العربية وإحالات جميع المواضع لم تكتمل بعد؛ فلا تُعامل هذه الصفحة "
            "على أنها فهرسها النهائي.",
            "",
            f"[نزّل سجل البيانات الكامل الحالي المضغوط]({RAW_INDEX_URL}) إذا أردت "
            "فحص جميع القرارات والإحالات آليًا. يحوي هذا السجل تعليلات إنجليزية "
            "لم تُعرَّب كلها بعد، وليس بديلًا من فهرس عربي كامل يسهل قراءته.",
            "",
        ]
    )
    return "\n".join(lines), exact_examples


def main() -> None:
    body, exact_examples = render()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(body, encoding="utf-8", newline="\n")
    print(f"output={OUTPUT}")
    print(f"bytes={OUTPUT.stat().st_size}")
    print(f"sha256={digest(OUTPUT)}")
    print(f"exact_reader_page_examples={exact_examples}")


if __name__ == "__main__":
    main()
