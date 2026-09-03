#!/usr/bin/env python3
"""Fail-closed RTL link-rectangle repair for the Arabic US-Letter readers.

LuaTeX/hyperref occasionally adds the active line width to the right edge of
an RTL link annotation.  The page contents and link target remain correct,
but the clickable rectangle extends beyond the page.  This tool changes only
those malformed ``/Rect`` arrays.  It reuses the audited glyph-run inference
and semantic-preservation checks from the repository's released 16:9 repair.

Six cross-document references and two bibliography fragments have disjoint
BiDi colour runs that cannot be inferred from colour alone.  Their exact
glyph spans are independently witnessed by the prior public R2 PDFs (reader
SHA-256 FB1EAB6294FC62E0C7B2C1B793EA8CDB5F8EBE8A85683DA6DD5BFEE599CFB4E6;
supplement SHA-256 40ED33C1043EDD17603BDCC2E996A3E6CA51BBCE9D433399699F155D8BC4455A).
Every coordinate and target is checked so changed input fails closed.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import pdfplumber
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, FloatObject, NameObject


PAGE_WIDTH = 612.0
PAGE_HEIGHT = 792.0
EXPECTED_COUNTS = {"reader": 128, "supplement": 8}
EXPECTED_INFLATIONS = (
    396.513,
    432.378,
    432.379,
    453.898,
    468.244,
    468.245,
    473.093,
    473.094,
)


def load_core() -> Any:
    path = Path(__file__).with_name("repair_rtl_link_rects_ar.py")
    spec = importlib.util.spec_from_file_location("openlogic_rtl_link_core", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load shared repair implementation: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load_core()


# Coordinates are for the raw dual-profile Letter build.  The international
# and Machrek PDFs have the same affected text geometry; only their page index
# may diverge after profile-specific formula reflow.
AUDITED_SPANS: tuple[dict[str, Any], ...] = (
    {
        "role": "reader",
        "target": "cite.ButtonLT1",
        "old_rect": [517.716, 73.297, 985.960, 87.443],
        "glyph_x0": 518.712,
        "glyph_x1": 539.625985,
        "text_ascii": ")2021",
    },
    {
        "role": "reader",
        "target": "cite.Peter1935a",
        "old_rect": [505.938, 427.820, 974.182, 446.902],
        "glyph_x0": 506.934,
        "glyph_x1": 539.627295,
        "text_ascii": ")1935a",
    },
    {
        "role": "supplement",
        "target": "prop*.2290",
        "old_rect": [210.531, 302.906, 642.910, 321.098],
        "glyph_x0": 211.536,
        "glyph_x1": 239.750307,
        "text_ascii": "19.18",
    },
    {
        "role": "supplement",
        "target": "prop*.2299",
        "old_rect": [453.581, 196.050, 885.960, 214.119],
        "glyph_x0": 454.578,
        "glyph_x1": 503.761428,
        "text_ascii": "and20.21",
    },
    {
        "role": "supplement",
        "target": "prop*.2310",
        "old_rect": [453.807, 597.703, 886.185, 614.042],
        "glyph_x0": 454.803,
        "glyph_x1": 503.761428,
        "text_ascii": "and20.23",
    },
    {
        "role": "supplement",
        "target": "Item*.2318",
        "old_rect": [208.066, 522.825, 640.445, 540.893],
        "glyph_x0": 209.062,
        "glyph_x1": 244.741399,
        "text_ascii": "Items1",
    },
    {
        "role": "supplement",
        "target": "Item*.2319",
        "old_rect": [436.610, 464.621, 868.989, 480.960],
        "glyph_x0": 437.607,
        "glyph_x1": 473.286399,
        "text_ascii": "Items2",
    },
    {
        "role": "supplement",
        "target": "Item*.2319",
        "old_rect": [228.027, 440.096, 660.406, 457.053],
        "glyph_x0": 229.024,
        "glyph_x1": 264.021666,
        "text_ascii": "Items2",
    },
)


def document_role(path: Path) -> str:
    normalized = path.name.lower().replace("_", "-")
    return "supplement" if "closure-supplement" in normalized else "reader"


def target_destination(annot: Any) -> str:
    action = annot.get("/A")
    if action is not None:
        return str(action.get_object().get("/D"))
    return str(annot.get("/Dest"))


def close(left: float, right: float, tolerance: float = 0.01) -> bool:
    return abs(left - right) <= tolerance


def scan_bad_annotations(
    reader: PdfReader, *, expected_count: int | None
) -> tuple[list[dict[str, Any]], Counter]:
    bad: list[dict[str, Any]] = []
    signatures: Counter = Counter()
    for page_index, page in enumerate(reader.pages):
        box = [CORE.f(value) for value in page.mediabox]
        observed = (box[0], box[1], box[2] - box[0], box[3] - box[1])
        expected = (0.0, 0.0, PAGE_WIDTH, PAGE_HEIGHT)
        if any(not close(left, right, 0.001) for left, right in zip(observed, expected)):
            CORE.die(f"p{page_index + 1}: MediaBox is not [0,0,612,792]: {box}")
        for annotation_index, ref in enumerate(page.get("/Annots") or []):
            annot = ref.get_object()
            if str(annot.get("/Subtype")) != "/Link":
                continue
            rect = CORE.rect_values(annot)
            outside = (
                rect[0] < -0.01
                or rect[1] < -0.01
                or rect[2] > PAGE_WIDTH + 0.01
                or rect[3] > PAGE_HEIGHT + 0.01
            )
            if not outside:
                continue
            if not (
                rect[2] > PAGE_WIDTH + 0.01
                and rect[0] >= -0.01
                and rect[1] >= -0.01
                and rect[3] <= PAGE_HEIGHT + 0.01
            ):
                CORE.die(
                    f"p{page_index + 1} a{annotation_index}: "
                    f"unknown outside-page direction {rect}"
                )
            action = annot.get("/A")
            if action is None or str(action.get_object().get("/S")) not in ("/GoTo", "/GoToR"):
                CORE.die(
                    f"p{page_index + 1} a{annotation_index}: "
                    "outside rectangle is not a GoTo/GoToR link"
                )
            signature = rect[2] - rect[0]
            nearest = min(EXPECTED_INFLATIONS, key=lambda value: abs(value - signature))
            if not close(nearest, signature):
                CORE.die(
                    f"p{page_index + 1} a{annotation_index}: "
                    f"unknown width signature {signature:.6f}"
                )
            signatures[round(signature, 3)] += 1
            bad.append(
                {
                    "page_index": page_index,
                    "annotation_index": annotation_index,
                    "annot": annot,
                }
            )
    if expected_count is not None and len(bad) != expected_count:
        CORE.die(
            f"malformed link count changed: expected {expected_count}, got {len(bad)}"
        )
    return bad, signatures


def match_audited_span(role: str, annot: Any) -> dict[str, Any] | None:
    destination = target_destination(annot)
    old_rect = CORE.rect_values(annot)
    matches = [
        span
        for span in AUDITED_SPANS
        if span["role"] == role
        and span["target"] == destination
        and all(close(left, right) for left, right in zip(old_rect, span["old_rect"]))
    ]
    if len(matches) > 1:
        CORE.die(f"ambiguous audited span for {destination}: {old_rect}")
    return matches[0] if matches else None


def audited_mapping(
    page_number: int,
    annotation_index: int,
    annot: Any,
    chars: list[dict[str, Any]],
    span: dict[str, Any],
) -> dict[str, Any]:
    old_rect = CORE.rect_values(annot)
    band_top = PAGE_HEIGHT - old_rect[3]
    band_bottom = PAGE_HEIGHT - old_rect[1]
    witnesses = []
    for char in chars:
        centre_y = (CORE.f(char["top"]) + CORE.f(char["bottom"])) / 2.0
        centre_x = (CORE.f(char["x0"]) + CORE.f(char["x1"])) / 2.0
        if (
            band_top - 0.5 <= centre_y <= band_bottom + 0.5
            and span["glyph_x0"] - 0.25 <= centre_x <= span["glyph_x1"] + 0.25
        ):
            witnesses.append(char)
    if not witnesses:
        CORE.die(f"p{page_number} a{annotation_index}: audited span has no glyph witnesses")
    witnesses.sort(key=lambda char: (CORE.f(char["x0"]), CORE.f(char["x1"])))
    text = "".join(str(char.get("text", "")) for char in witnesses)
    observed_ascii = CORE.text_ascii(text).replace(" ", "")
    if observed_ascii != span["text_ascii"]:
        CORE.die(
            f"p{page_number} a{annotation_index}: audited glyph text changed: "
            f"expected {span['text_ascii']!r}, got {observed_ascii!r}"
        )
    glyph_x0 = min(CORE.f(char["x0"]) for char in witnesses)
    glyph_x1 = max(CORE.f(char["x1"]) for char in witnesses)
    if not close(glyph_x0, span["glyph_x0"], 0.02) or not close(
        glyph_x1, span["glyph_x1"], 0.02
    ):
        CORE.die(
            f"p{page_number} a{annotation_index}: audited glyph bounds changed: "
            f"{glyph_x0:.6f}..{glyph_x1:.6f}"
        )
    new_rect = [old_rect[0], old_rect[1], span["glyph_x1"] + 1.0, old_rect[3]]
    return {
        "page": page_number,
        "annotation_index": annotation_index,
        "target": CORE.action_summary(annot),
        "old_rect": [round(value, 6) for value in old_rect],
        "new_rect": [round(value, 6) for value in new_rect],
        "inflation_signature": round(old_rect[2] - old_rect[0], 6),
        "glyph_bbox_top_coordinates": [
            round(glyph_x0, 6),
            round(min(CORE.f(char["top"]) for char in witnesses), 6),
            round(glyph_x1, 6),
            round(max(CORE.f(char["bottom"]) for char in witnesses), 6),
        ],
        "glyph_text_ascii": observed_ascii,
        "annotation_colour": list(CORE.colour_tuple(annot.get("/C"))),
        "method": "prior-r2-witnessed-bidi-glyph-span",
        "companion_rects": [],
        "candidate_runs": [
            {
                "x0": round(glyph_x0, 6),
                "x1": round(glyph_x1, 6),
                "text_ascii": observed_ascii,
            }
        ],
    }


def run(input_path: Path, output_path: Path, receipt_path: Path, dry_run: bool) -> None:
    role = document_role(input_path)
    reader = PdfReader(str(input_path), strict=True)
    bad, signatures = scan_bad_annotations(
        reader, expected_count=EXPECTED_COUNTS[role]
    )
    by_page: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for entry in bad:
        by_page[entry["page_index"]].append(entry)

    mappings: list[dict[str, Any]] = []
    used_audited: list[dict[str, Any]] = []
    with pdfplumber.open(str(input_path)) as plumber:
        for page_index in sorted(by_page):
            page = reader.pages[page_index]
            annots = [ref.get_object() for ref in (page.get("/Annots") or [])]
            chars = plumber.pages[page_index].chars
            for entry in by_page[page_index]:
                span = match_audited_span(role, entry["annot"])
                if span is not None:
                    mappings.append(
                        audited_mapping(
                            page_index + 1,
                            entry["annotation_index"],
                            entry["annot"],
                            chars,
                            span,
                        )
                    )
                    used_audited.append(span)
                else:
                    mappings.append(
                        CORE.infer_mapping(
                            page_index + 1,
                            entry["annotation_index"],
                            entry["annot"],
                            annots,
                            chars,
                            PAGE_WIDTH,
                            PAGE_HEIGHT,
                        )
                    )
            plumber.pages[page_index].close()

    expected_audited = [span for span in AUDITED_SPANS if span["role"] == role]
    if len(used_audited) != len(expected_audited):
        CORE.die(
            f"audited-span count changed: expected {len(expected_audited)}, "
            f"got {len(used_audited)}"
        )
    if len(mappings) != len(bad):
        CORE.die("mapping count does not equal malformed annotation count")

    receipt: dict[str, Any] = {
        "schema": "arabic-letter-rtl-link-rect-repair-v1",
        "document_role": role,
        "input": str(input_path.resolve()),
        "output": str(output_path.resolve()),
        "input_sha256": CORE.sha256_file(input_path),
        "pages": len(reader.pages),
        "malformed_link_rectangles": len(bad),
        "width_signatures": dict(sorted(signatures.items())),
        "audited_span_count": len(used_audited),
        "mappings": mappings,
        "dry_run": dry_run,
    }
    if dry_run:
        print(json.dumps(receipt, ensure_ascii=True, indent=2, sort_keys=True))
        return
    if output_path.exists():
        CORE.die(f"refusing to overwrite output: {output_path}")

    before_content = CORE.content_hashes(reader)
    before_annots = CORE.annotation_snapshot(reader)
    before_text = CORE.text_extraction_fingerprint(reader)
    before_metadata = CORE.metadata_fingerprint(reader)
    before_destinations = CORE.named_destination_fingerprint(reader)
    before_outline = CORE.outline_fingerprint(reader)
    before_fonts = CORE.font_fingerprint(reader)
    before_boxes = CORE.page_box_fingerprint(reader)
    before_catalog = CORE.catalog_view(reader)

    for mapping in mappings:
        page = reader.pages[mapping["page"] - 1]
        annot = (page.get("/Annots") or [])[mapping["annotation_index"]].get_object()
        current = [round(value, 6) for value in CORE.rect_values(annot)]
        if current != mapping["old_rect"]:
            CORE.die(
                f"p{mapping['page']} a{mapping['annotation_index']}: "
                "/Rect changed before write"
            )
        annot[NameObject("/Rect")] = ArrayObject(
            [FloatObject(value) for value in mapping["new_rect"]]
        )

    writer = PdfWriter(clone_from=reader)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        writer.write(handle)

    final_reader = PdfReader(str(output_path), strict=True)
    remaining, _ = scan_bad_annotations(final_reader, expected_count=0)
    if remaining:
        CORE.die(f"final PDF still contains {len(remaining)} outside-page links")
    if before_content != CORE.content_hashes(final_reader):
        CORE.die("page content streams changed during annotation-only rewrite")

    after_annots = CORE.annotation_snapshot(final_reader)
    expected_changes = {
        (mapping["page"], mapping["annotation_index"]): mapping for mapping in mappings
    }
    observed_changes: list[tuple[int, int]] = []
    if len(before_annots) != len(after_annots):
        CORE.die("page count changed in annotation snapshot")
    for page_index, (before_page, after_page) in enumerate(
        zip(before_annots, after_annots), 1
    ):
        if len(before_page) != len(after_page):
            CORE.die(f"p{page_index}: annotation count changed")
        for annotation_index, (before_annot, after_annot) in enumerate(
            zip(before_page, after_page)
        ):
            if before_annot["semantic"] != after_annot["semantic"]:
                CORE.die(
                    f"p{page_index} a{annotation_index}: "
                    "non-/Rect annotation semantics changed"
                )
            if before_annot["rect"] != after_annot["rect"]:
                observed_changes.append((page_index, annotation_index))
                mapping = expected_changes.get((page_index, annotation_index))
                if mapping is None or after_annot["rect"] != mapping["new_rect"]:
                    CORE.die(
                        f"p{page_index} a{annotation_index}: unexpected /Rect delta"
                    )
    if set(observed_changes) != set(expected_changes):
        CORE.die("observed /Rect changes do not equal the fail-closed mapping")

    comparisons = {
        "text_extraction_fingerprint_equal": (
            before_text == CORE.text_extraction_fingerprint(final_reader)
        ),
        "metadata_fingerprint_equal": (
            before_metadata == CORE.metadata_fingerprint(final_reader)
        ),
        "named_destinations_fingerprint_equal": (
            before_destinations == CORE.named_destination_fingerprint(final_reader)
        ),
        "outline_fingerprint_equal": (
            before_outline == CORE.outline_fingerprint(final_reader)
        ),
        "font_resource_fingerprint_equal": (
            before_fonts == CORE.font_fingerprint(final_reader)
        ),
        "page_box_fingerprint_equal": (
            before_boxes == CORE.page_box_fingerprint(final_reader)
        ),
        "catalog_view_equal": before_catalog == CORE.catalog_view(final_reader),
    }
    failed = [name for name, value in comparisons.items() if not value]
    if failed:
        CORE.die(f"semantic post-write comparisons failed: {failed}")
    target_counts = CORE.validate_link_targets(final_reader, output_path)

    receipt.update(
        {
            "dry_run": False,
            "output_sha256": CORE.sha256_file(output_path),
            "output_bytes": output_path.stat().st_size,
            "semantic_invariants": {
                "strict_reopen": True,
                "page_count_equal": len(reader.pages) == len(final_reader.pages),
                "all_page_content_stream_hashes_equal": True,
                **comparisons,
                "text_extraction_sha256": CORE.text_extraction_fingerprint(final_reader),
                "metadata_sha256": CORE.metadata_fingerprint(final_reader),
                "named_destinations_sha256": CORE.named_destination_fingerprint(final_reader)[0],
                "named_destinations_count": CORE.named_destination_fingerprint(final_reader)[1],
                "outline_sha256": CORE.outline_fingerprint(final_reader)[0],
                "outline_count": CORE.outline_fingerprint(final_reader)[1],
                "font_resources_sha256": CORE.font_fingerprint(final_reader)[0],
                "font_resource_occurrences": CORE.font_fingerprint(final_reader)[1],
                "page_boxes_sha256": CORE.page_box_fingerprint(final_reader),
                "catalog_view": CORE.catalog_view(final_reader),
                "link_target_counts": target_counts,
                "all_link_targets_valid": True,
                "outside_page_link_rectangles_final": 0,
                "annotation_counts_equal": True,
                "non_rect_annotation_semantics_equal": True,
                "rectangles_changed_exactly": len(observed_changes),
                "changed_pdf_keys": ["page /Annots[n] /Rect"],
            },
        }
    )
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output_path),
                "receipt": str(receipt_path),
                "changed": len(mappings),
                "sha256": receipt["output_sha256"],
            },
            sort_keys=True,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        run(args.input, args.output, args.receipt, args.dry_run)
    except Exception as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
