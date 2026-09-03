#!/usr/bin/env python3
"""Deterministic structural QA for the four Arabic notation-profile PDFs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from pypdf import PdfReader


ARABIC_INDIC_RE = re.compile("[\u0660-\u0669]")
ASCII_DIGIT_RE = re.compile("[0-9]")
DIGIT_FONT_MARKER = "OpenLogicMachrekDigits-Regular"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def hash_strings(values: list[str]) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8", "surrogatepass")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest().upper()


def font_facts(page: object) -> list[dict[str, object]]:
    resources = page.get("/Resources") or {}
    if hasattr(resources, "get_object"):
        resources = resources.get_object()
    fonts = resources.get("/Font") or {}
    if hasattr(fonts, "get_object"):
        fonts = fonts.get_object()
    facts: list[dict[str, object]] = []
    for resource_name, reference in fonts.items():
        font = reference.get_object() if hasattr(reference, "get_object") else reference
        descendants = font.get("/DescendantFonts") or []
        descendants = [
            descendant.get_object() if hasattr(descendant, "get_object") else descendant
            for descendant in descendants
        ]
        candidates = [font, *descendants]
        embedded = False
        for candidate in candidates:
            descriptor = candidate.get("/FontDescriptor")
            if hasattr(descriptor, "get_object"):
                descriptor = descriptor.get_object()
            if descriptor and any(descriptor.get(key) is not None for key in ("/FontFile", "/FontFile2", "/FontFile3")):
                embedded = True
        facts.append(
            {
                "resource": str(resource_name),
                "base_font": str(font.get("/BaseFont", "")),
                "subtype": str(font.get("/Subtype", "")),
                "to_unicode": font.get("/ToUnicode") is not None,
                "embedded": embedded,
            }
        )
    return facts


def inspect(
    path: Path, expected_pages: int, expected_profile: str, expected_links: int
) -> dict[str, object]:
    reader = PdfReader(str(path), strict=True)
    failures: list[str] = []
    links = 0
    outside = 0
    arabic_indic_digits = 0
    ascii_digits = 0
    boxes_ok = True
    rotations_ok = True
    text_digest = hashlib.sha256()
    uri_targets: list[str] = []
    link_semantics: list[str] = []
    broken_link_targets: list[str] = []
    digit_font_pages: list[int] = []
    digit_font_facts: set[tuple[str, str, bool, bool]] = set()

    named_destinations = set(reader.named_destinations)
    generated_page_destinations = {
        name for name in named_destinations if re.fullmatch(r"page\.\d+", name)
    }
    structural_destinations = named_destinations - generated_page_destinations
    for page_index, page in enumerate(reader.pages):
        media = [float(value) for value in page.mediabox]
        crop = [float(value) for value in page.cropbox]
        boxes_ok = boxes_ok and all(
            abs(left - right) <= 0.01
            for left, right in zip(media, [0.0, 0.0, 612.0, 792.0])
        ) and crop == media
        rotations_ok = rotations_ok and int(page.get("/Rotate", 0)) == 0
        width = media[2] - media[0]
        height = media[3] - media[1]
        for ref in page.get("/Annots", []):
            annotation = ref.get_object()
            if str(annotation.get("/Subtype")) != "/Link":
                continue
            links += 1
            x0, y0, x1, y1 = [float(value) for value in annotation["/Rect"]]
            if x0 < -0.01 or y0 < -0.01 or x1 > width + 0.01 or y1 > height + 0.01 or x1 < x0 or y1 < y0:
                outside += 1
            action = annotation.get("/A")
            if hasattr(action, "get_object"):
                action = action.get_object()
            if isinstance(action, dict):
                action_kind = str(action.get("/S", ""))
                destination_value = action.get("/D")
                destination = str(destination_value) if destination_value is not None else ""
                if action_kind == "/URI":
                    uri = str(action.get("/URI", ""))
                    uri_targets.append(uri)
                    link_semantics.append(f"URI:{uri}")
                elif action_kind == "/GoTo":
                    link_semantics.append(f"GoTo:{destination}")
                    if destination and not isinstance(destination_value, (list, tuple)) and destination not in named_destinations:
                        broken_link_targets.append(f"p{page_index + 1}:missing-GoTo:{destination}")
                elif action_kind == "/GoToR":
                    file_spec = str(action.get("/F", ""))
                    # Profile filenames intentionally differ; target kind and
                    # destination must still be semantically identical.
                    link_semantics.append(f"GoToR:<complete-reader>:{destination}")
                    if not file_spec or not (path.parent / file_spec).is_file():
                        broken_link_targets.append(f"p{page_index + 1}:missing-GoToR-file:{file_spec}")
                else:
                    link_semantics.append(f"{action_kind}:{destination}")
            else:
                destination_value = annotation.get("/Dest")
                destination = str(destination_value) if destination_value is not None else ""
                link_semantics.append(f"Dest:{destination}")
                if destination and not isinstance(destination_value, (list, tuple)) and destination not in named_destinations:
                    broken_link_targets.append(f"p{page_index + 1}:missing-Dest:{destination}")
        text = page.extract_text() or ""
        arabic_indic_digits += len(ARABIC_INDIC_RE.findall(text))
        ascii_digits += len(ASCII_DIGIT_RE.findall(text))
        encoded = text.encode("utf-8", "surrogatepass")
        text_digest.update(page_index.to_bytes(8, "big"))
        text_digest.update(len(encoded).to_bytes(8, "big"))
        text_digest.update(encoded)
        for facts in font_facts(page):
            if DIGIT_FONT_MARKER in facts["base_font"]:
                if not digit_font_pages or digit_font_pages[-1] != page_index + 1:
                    digit_font_pages.append(page_index + 1)
                digit_font_facts.add(
                    (
                        str(facts["base_font"]),
                        str(facts["subtype"]),
                        bool(facts["to_unicode"]),
                        bool(facts["embedded"]),
                    )
                )

    root = reader.trailer["/Root"]
    action = root.get("/OpenAction")
    if hasattr(action, "get_object"):
        action = action.get_object()
    destination = action.get("/D") if isinstance(action, dict) else action
    fit = str(destination[1]) if isinstance(destination, (list, tuple)) and len(destination) > 1 else ""

    if len(reader.pages) != expected_pages:
        failures.append(f"pages={len(reader.pages)}, expected {expected_pages}")
    if links != expected_links:
        failures.append(f"links={links}, expected {expected_links}")
    if reader.is_encrypted:
        failures.append("PDF is encrypted")
    if not boxes_ok:
        failures.append("page geometry is not unrotated US Letter")
    if not rotations_ok:
        failures.append("one or more pages are rotated")
    if outside:
        failures.append(f"outside-page link rectangles={outside}")
    if broken_link_targets:
        failures.append(f"broken link targets={len(broken_link_targets)}")
    if len(generated_page_destinations) != len(reader.pages):
        failures.append(
            "generated page destinations="
            f"{len(generated_page_destinations)}, expected {len(reader.pages)}"
        )
    if str(root.get("/PageMode", "")) != "/UseOutlines":
        failures.append("PageMode is not /UseOutlines")
    if str(root.get("/PageLayout", "")) != "/OneColumn":
        failures.append("PageLayout is not /OneColumn")
    if fit != "/FitH":
        failures.append(f"OpenAction fit is {fit!r}, expected /FitH")

    metadata = {str(key): str(value) for key, value in (reader.metadata or {}).items()}
    title = metadata.get("/Title", "")
    if expected_profile == "machrek" and "المشرق" not in title:
        failures.append("Machrek title marker is absent")
    if expected_profile == "international" and "الدولي" not in title:
        failures.append("international title marker is absent")
    if expected_profile == "machrek":
        if not digit_font_pages:
            failures.append("Machrek digit presentation font is not used")
        if digit_font_facts and not all(facts[2] and facts[3] for facts in digit_font_facts):
            failures.append("Machrek digit font is not both embedded and ToUnicode-enabled")
        if ascii_digits == 0:
            failures.append("Machrek text extraction lost all semantic ASCII digits")
    elif digit_font_pages:
        failures.append("Machrek digit presentation font leaked into international profile")

    uri_arabic_indic_digits = sum(len(ARABIC_INDIC_RE.findall(uri)) for uri in uri_targets)
    uri_ascii_digits = sum(len(ASCII_DIGIT_RE.findall(uri)) for uri in uri_targets)
    if uri_arabic_indic_digits:
        failures.append(f"Arabic-Indic digits leaked into URI targets={uri_arabic_indic_digits}")

    return {
        "path": str(path.resolve()),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "pages": len(reader.pages),
        "encrypted": bool(reader.is_encrypted),
        "us_letter_boxes": boxes_ok,
        "rotation_zero": rotations_ok,
        "links": links,
        "expected_links": expected_links,
        "link_semantics_sha256": hash_strings(link_semantics),
        "broken_link_targets": broken_link_targets,
        "uri_targets": len(uri_targets),
        "uri_target_sha256": hash_strings(uri_targets),
        "uri_ascii_digits": uri_ascii_digits,
        "uri_arabic_indic_digits": uri_arabic_indic_digits,
        "outside_page_link_rectangles": outside,
        "page_mode": str(root.get("/PageMode", "")),
        "page_layout": str(root.get("/PageLayout", "")),
        "open_action_fit": fit,
        "metadata": metadata,
        "ascii_digits_in_extracted_text": ascii_digits,
        "arabic_indic_digits_in_extracted_text": arabic_indic_digits,
        "machrek_digit_font": {
            "marker": DIGIT_FONT_MARKER,
            "page_count": len(digit_font_pages),
            "first_pages": digit_font_pages[:10],
            "last_pages": digit_font_pages[-10:],
            "resource_facts": [
                {
                    "base_font": base_font,
                    "subtype": subtype,
                    "to_unicode": to_unicode,
                    "embedded": embedded,
                }
                for base_font, subtype, to_unicode, embedded in sorted(digit_font_facts)
            ],
        },
        "text_extraction_sha256": text_digest.hexdigest().upper(),
        "named_destination_names": len(named_destinations),
        "named_destination_names_sha256": hash_strings(sorted(named_destinations)),
        "generated_page_destination_names": len(generated_page_destinations),
        "structural_destination_names": len(structural_destinations),
        "structural_destination_names_sha256": hash_strings(sorted(structural_destinations)),
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--international-reader", type=Path, required=True)
    parser.add_argument("--international-supplement", type=Path, required=True)
    parser.add_argument("--machrek-reader", type=Path, required=True)
    parser.add_argument("--machrek-supplement", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    artifacts = {
        "international_reader": inspect(args.international_reader, 1008, "international", 3014),
        "international_supplement": inspect(args.international_supplement, 145, "international", 140),
        "machrek_reader": inspect(args.machrek_reader, 1009, "machrek", 3014),
        "machrek_supplement": inspect(args.machrek_supplement, 145, "machrek", 140),
    }
    failures = [f"{name}: {message}" for name, facts in artifacts.items() for message in facts["failures"]]
    if artifacts["machrek_reader"]["machrek_digit_font"]["page_count"] <= 0:
        failures.append("Machrek reader has no pages using the presentation font")
    if artifacts["machrek_supplement"]["machrek_digit_font"]["page_count"] <= 0:
        failures.append("Machrek supplement has no pages using the presentation font")
    reader_uri_equal = (
        artifacts["international_reader"]["uri_target_sha256"]
        == artifacts["machrek_reader"]["uri_target_sha256"]
    )
    supplement_uri_equal = (
        artifacts["international_supplement"]["uri_target_sha256"]
        == artifacts["machrek_supplement"]["uri_target_sha256"]
    )
    if not reader_uri_equal:
        failures.append("reader URI targets differ between notation profiles")
    if not supplement_uri_equal:
        failures.append("supplement URI targets differ between notation profiles")
    reader_link_semantics_equal = (
        artifacts["international_reader"]["link_semantics_sha256"]
        == artifacts["machrek_reader"]["link_semantics_sha256"]
    )
    supplement_link_semantics_equal = (
        artifacts["international_supplement"]["link_semantics_sha256"]
        == artifacts["machrek_supplement"]["link_semantics_sha256"]
    )
    reader_destination_names_equal = (
        artifacts["international_reader"]["structural_destination_names_sha256"]
        == artifacts["machrek_reader"]["structural_destination_names_sha256"]
    )
    supplement_destination_names_equal = (
        artifacts["international_supplement"]["structural_destination_names_sha256"]
        == artifacts["machrek_supplement"]["structural_destination_names_sha256"]
    )
    if not reader_link_semantics_equal:
        failures.append("reader link semantics differ between notation profiles")
    if not supplement_link_semantics_equal:
        failures.append("supplement link semantics differ between notation profiles")
    if not reader_destination_names_equal:
        failures.append("reader structural-destination inventories differ between notation profiles")
    if not supplement_destination_names_equal:
        failures.append("supplement structural-destination inventories differ between notation profiles")

    payload = {
        "schema": "openlogic-arabic-dual-notation-pdf-qa-v1",
        "status": "PASS" if not failures else "FAIL",
        "artifacts": artifacts,
        "cross_profile": {
            "reader_page_count_equal": artifacts["international_reader"]["pages"] == artifacts["machrek_reader"]["pages"],
            "supplement_page_count_equal": artifacts["international_supplement"]["pages"] == artifacts["machrek_supplement"]["pages"],
            "reader_uri_targets_equal": reader_uri_equal,
            "supplement_uri_targets_equal": supplement_uri_equal,
            "reader_link_semantics_equal": reader_link_semantics_equal,
            "supplement_link_semantics_equal": supplement_link_semantics_equal,
            "reader_destination_names_equal": reader_destination_names_equal,
            "supplement_destination_names_equal": supplement_destination_names_equal,
            "machrek_reader_digit_font_pages": artifacts["machrek_reader"]["machrek_digit_font"]["page_count"],
            "machrek_supplement_digit_font_pages": artifacts["machrek_supplement"]["machrek_digit_font"]["page_count"],
            "machrek_reader_semantic_ascii_digits": artifacts["machrek_reader"]["ascii_digits_in_extracted_text"],
            "machrek_supplement_semantic_ascii_digits": artifacts["machrek_supplement"]["ascii_digits_in_extracted_text"],
        },
        "failures": failures,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "failures": len(failures), "output": str(args.output)}))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
