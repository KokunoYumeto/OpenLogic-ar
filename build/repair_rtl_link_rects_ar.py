#!/usr/bin/env python3
"""Repair LuaTeX/hyperref RTL link rectangles that add a line width to x1.

The repair is intentionally fail-closed.  It accepts only the measured width
inflation signatures from the two Arabic screen PDFs, maps each malformed link
to the link-coloured glyph run on the same baseline, and changes only /Rect.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import pdfplumber
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, FloatObject, NameObject


PAGE_WIDTH = 960.0
PAGE_HEIGHT = 540.0
EXPECTED_INFLATIONS = (659.128, 659.129, 702.166, 702.167,
                       727.990, 745.205, 745.206, 751.024)
COLOUR_TOLERANCE = 0.01

# Independent visual/text extraction established these nine discontiguous
# bidi spans in the closure supplement.  They are keyed to the exact page,
# zero-based page-annotation ordinal, destination, and raw rectangle, so a
# changed build fails instead of receiving a stale correction.
SUPPLEMENT_AUDITED_SPANS: dict[tuple[int, int, str], dict[str, Any]] = {
    (11, 1, "prop*.2290"): {"old_x0": 637.143, "old_x1": 1339.310,
                             "glyph_x0": 638.169, "glyph_x1": 792.195,
                             "text": "قضايا 19.18"},
    (11, 3, "prop*.2299"): {"old_x0": 388.587, "old_x1": 1090.753,
                             "glyph_x0": 389.602, "glyph_x1": 543.337,
                             "text": "قضايا 19.21"},
    (12, 1, "Item*.2304"): {"old_x0": 326.973, "old_x1": 1029.140,
                             "glyph_x0": 327.969, "glyph_x1": 371.587,
                             "text": "Items 1"},
    (12, 4, "Item*.2305"): {"old_x0": 299.486, "old_x1": 1001.653,
                             "glyph_x0": 300.483, "glyph_x1": 343.692,
                             "text": "Items 2"},
    (12, 7, "prop*.2310"): {"old_x0": 535.365, "old_x1": 1237.532,
                             "glyph_x0": 536.391, "glyph_x1": 690.431,
                             "text": "قضايا 19.23"},
    (12, 12, "Item*.2318"): {"old_x0": 632.877, "old_x1": 1335.044,
                              "glyph_x0": 633.874, "glyph_x1": 676.693,
                              "text": "Items 1"},
    (12, 19, "Item*.2319"): {"old_x0": 471.445, "old_x1": 1173.612,
                              "glyph_x0": 472.441, "glyph_x1": 515.279,
                              "text": "Items 2"},
    (32, 1, "lem*.523"): {"old_x0": 532.149, "old_x1": 1277.354,
                           "glyph_x0": 533.167, "glyph_x1": 710.380,
                           "text": "قضايا مساعدة 6.14"},
    (166, 1, "table.506"): {"old_x0": 504.854, "old_x1": 1250.060,
                             "glyph_x0": 505.854, "glyph_x1": 634.107,
                             "text": "جداول 6.3"},
}


def die(message: str) -> None:
    raise RuntimeError(message)


def f(value: Any) -> float:
    return float(value)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def rect_values(annot: Any) -> list[float]:
    return [f(value) for value in annot["/Rect"]]


def target_key(annot: Any) -> str:
    action = annot.get("/A")
    if action is not None:
        action = action.get_object()
        kind = str(action.get("/S"))
        dest = str(action.get("/D"))
        file_spec = action.get("/F")
        if file_spec is not None:
            file_spec = file_spec.get_object()
        return f"A:{kind}:{file_spec!s}:{dest}"
    return f"D:{annot.get('/Dest')!s}"


def action_summary(annot: Any) -> dict[str, Any]:
    action = annot.get("/A")
    if action is not None:
        action = action.get_object()
        return {
            "S": str(action.get("/S")),
            "D": str(action.get("/D")),
            "F": str(action.get("/F")) if action.get("/F") is not None else None,
        }
    return {"Dest": str(annot.get("/Dest"))}


def colour_tuple(value: Any) -> tuple[float, ...]:
    if value is None:
        return ()
    try:
        return tuple(float(part) for part in value)
    except TypeError:
        return ()


def colours_match(observed: Any, expected: Any) -> bool:
    observed_tuple = colour_tuple(observed)
    expected_tuple = colour_tuple(expected)
    if len(observed_tuple) != len(expected_tuple):
        return False
    return all(abs(left - right) <= COLOUR_TOLERANCE
               for left, right in zip(observed_tuple, expected_tuple))


def vertical_overlap(char: dict[str, Any], top: float, bottom: float) -> bool:
    return min(f(char["bottom"]), bottom) - max(f(char["top"]), top) > 0.5


def char_centre_in_rect(char: dict[str, Any], rect: list[float], height: float) -> bool:
    cx = (f(char["x0"]) + f(char["x1"])) / 2.0
    cy = height - (f(char["top"]) + f(char["bottom"])) / 2.0
    return (rect[0] - 0.1 <= cx <= rect[2] + 0.1 and
            rect[1] - 0.1 <= cy <= rect[3] + 0.1)


def text_ascii(text: str) -> str:
    return text.encode("ascii", "backslashreplace").decode("ascii")


def group_runs(target_chars: list[dict[str, Any]],
               all_band_chars: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group link-coloured glyphs, splitting at intervening visible glyphs."""
    chars = sorted(target_chars, key=lambda item: (f(item["x0"]), f(item["x1"])))
    runs: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    current_right = -math.inf
    for char in chars:
        x0 = f(char["x0"])
        if current:
            gap = x0 - current_right
            intervening = False
            if gap > 0.25:
                for other in all_band_chars:
                    if other in target_chars:
                        continue
                    centre = (f(other["x0"]) + f(other["x1"])) / 2.0
                    if current_right + 0.1 < centre < x0 - 0.1 and str(other.get("text", "")).strip():
                        intervening = True
                        break
            if gap > 12.0 or intervening:
                runs.append(current)
                current = []
                current_right = -math.inf
        current.append(char)
        current_right = max(current_right, f(char["x1"]))
    if current:
        runs.append(current)

    result = []
    for run in runs:
        x0 = min(f(char["x0"]) for char in run)
        x1 = max(f(char["x1"]) for char in run)
        top = min(f(char["top"]) for char in run)
        bottom = max(f(char["bottom"]) for char in run)
        text = "".join(str(char.get("text", "")) for char in run)
        if x1 - x0 > 0.25 and text.strip():
            result.append({"x0": x0, "x1": x1, "top": top,
                           "bottom": bottom, "text": text, "chars": run})
    return result


def distance_between(run: dict[str, Any], rect: list[float]) -> float:
    if run["x1"] < rect[0]:
        return rect[0] - run["x1"]
    if run["x0"] > rect[2]:
        return run["x0"] - rect[2]
    return 0.0


def infer_mapping(page_number: int, annotation_index: int, annot: Any,
                  page_annots: list[Any], chars: list[dict[str, Any]],
                  width: float, height: float) -> dict[str, Any]:
    old_rect = rect_values(annot)
    band_top = height - old_rect[3]
    band_bottom = height - old_rect[1]
    # Use the glyph centre, not mere bbox overlap: adjacent compact lines can
    # overlap the annotation band by a fraction of a point.
    all_band = [char for char in chars
                if band_top - 0.5 <= (f(char["top"]) + f(char["bottom"])) / 2.0
                <= band_bottom + 0.5]
    target_colour = colour_tuple(annot.get("/C"))
    coloured = [char for char in all_band
                if colours_match(char.get("non_stroking_color"), target_colour)]
    if not coloured:
        die(f"p{page_number} a{annotation_index}: no glyphs match colour {target_colour}")

    key = target_key(annot)
    companions: list[list[float]] = []
    for other_index, other in enumerate(page_annots):
        if other_index == annotation_index or str(other.get("/Subtype")) != "/Link":
            continue
        other_rect = rect_values(other)
        if other_rect[2] > width + 0.01 or target_key(other) != key:
            continue
        if min(old_rect[3], other_rect[3]) - max(old_rect[1], other_rect[1]) > 0.5:
            companions.append(other_rect)

    uncovered = [char for char in coloured
                 if not any(char_centre_in_rect(char, rect, height) for rect in companions)]
    runs = group_runs(uncovered, all_band)
    if not runs:
        die(f"p{page_number} a{annotation_index}: no uncovered coloured glyph run")

    if companions:
        ranked = [(min(distance_between(run, rect) for rect in companions), run)
                  for run in runs]
        ranked.sort(key=lambda item: item[0])
        best_distance, chosen = ranked[0]
        if best_distance > 20.0:
            die(f"p{page_number} a{annotation_index}: paired run is {best_distance:.3f} pt away")
        if len(ranked) > 1 and abs(ranked[1][0] - best_distance) < 0.25:
            die(f"p{page_number} a{annotation_index}: ambiguous paired runs")
        method = "same-target-companion-complement"
    else:
        if len(runs) == 1:
            chosen = runs[0]
            method = "sole-colour-run"
        else:
            expected_left = old_rect[0] + 1.0
            ranked = [(abs(run["x0"] - expected_left), run) for run in runs]
            ranked.sort(key=lambda item: item[0])
            best_distance, chosen = ranked[0]
            if best_distance > 8.0:
                die(f"p{page_number} a{annotation_index}: nearest run starts {best_distance:.3f} pt away")
            if len(ranked) > 1 and abs(ranked[1][0] - best_distance) < 0.25:
                die(f"p{page_number} a{annotation_index}: ambiguous unpaired runs")
            method = "left-edge-colour-run"

        # A small class of multilingual references keeps the translated
        # conjunction black while the numeric anchor is link-coloured.  If
        # the raw x0 lands on such a prefix, include the contiguous baseline
        # glyphs beginning exactly there (but never punctuation to its left).
        expected_left = old_rect[0] + 1.0
        if chosen["x0"] - expected_left > 8.0:
            baseline = [char for char in all_band
                        if min(f(char["bottom"]), chosen["bottom"]) -
                           max(f(char["top"]), chosen["top"]) > 0.5]
            prefix = [char for char in baseline
                      if f(char["x0"]) >= expected_left - 1.5 and
                         f(char["x1"]) <= chosen["x0"] + 0.5]
            combined = sorted(prefix + chosen["chars"],
                              key=lambda item: (f(item["x0"]), f(item["x1"])))
            if not combined or abs(f(combined[0]["x0"]) - expected_left) > 1.5:
                die(f"p{page_number} a{annotation_index}: displaced sole run has no raw-edge prefix")
            right = f(combined[0]["x1"])
            for char in combined[1:]:
                if f(char["x0"]) - right > 12.0:
                    die(f"p{page_number} a{annotation_index}: raw-edge prefix is not contiguous")
                right = max(right, f(char["x1"]))
            chosen = {
                "x0": min(f(char["x0"]) for char in combined),
                "x1": max(f(char["x1"]) for char in combined),
                "top": min(f(char["top"]) for char in combined),
                "bottom": max(f(char["bottom"]) for char in combined),
                "text": "".join(str(char.get("text", "")) for char in combined),
                "chars": combined,
            }
            method += "+raw-edge-mixed-colour-prefix"

    if abs(chosen["x0"] - (old_rect[0] + 1.0)) <= 1.5:
        new_x0 = old_rect[0]
    else:
        new_x0 = max(0.0, chosen["x0"] - 1.0)
    new_x1 = min(width, chosen["x1"] + 1.0)
    if not (new_x0 < new_x1 <= width + 0.001):
        die(f"p{page_number} a{annotation_index}: invalid inferred x bounds")
    if new_x1 - new_x0 > 450.0:
        die(f"p{page_number} a{annotation_index}: inferred run is implausibly wide")

    return {
        "page": page_number,
        "annotation_index": annotation_index,
        "target": action_summary(annot),
        "old_rect": [round(value, 6) for value in old_rect],
        "new_rect": [round(new_x0, 6), round(old_rect[1], 6),
                     round(new_x1, 6), round(old_rect[3], 6)],
        "inflation_signature": round(old_rect[2] - old_rect[0], 6),
        "glyph_bbox_top_coordinates": [round(chosen["x0"], 6), round(chosen["top"], 6),
                                        round(chosen["x1"], 6), round(chosen["bottom"], 6)],
        "glyph_text_ascii": text_ascii(chosen["text"]),
        "annotation_colour": list(target_colour),
        "method": method,
        "companion_rects": [[round(value, 6) for value in rect]
                            for rect in companions],
        "candidate_runs": [{"x0": round(run["x0"], 6),
                            "x1": round(run["x1"], 6),
                            "text_ascii": text_ascii(run["text"])} for run in runs],
    }


def audited_supplement_mapping(page_number: int, annotation_index: int,
                               annot: Any, chars: list[dict[str, Any]],
                               span: dict[str, Any]) -> dict[str, Any]:
    old_rect = rect_values(annot)
    action = action_summary(annot)
    if action.get("S") != "/GoTo" and action.get("S") != "/GoToR":
        die(f"p{page_number} a{annotation_index}: audited link action changed")
    if abs(old_rect[0] - span["old_x0"]) > 0.01 or abs(old_rect[2] - span["old_x1"]) > 0.01:
        die(f"p{page_number} a{annotation_index}: audited raw x bounds changed: {old_rect}")
    if abs(span["glyph_x0"] - old_rect[0] - 1.0) > 0.05:
        die(f"p{page_number} a{annotation_index}: audited glyph start no longer matches raw x0")
    band_top = PAGE_HEIGHT - old_rect[3]
    band_bottom = PAGE_HEIGHT - old_rect[1]
    witnesses = [char for char in chars
                 if band_top - 0.5 <= (f(char["top"]) + f(char["bottom"])) / 2.0 <= band_bottom + 0.5
                 and f(char["x1"]) >= span["glyph_x0"] - 0.25
                 and f(char["x0"]) <= span["glyph_x1"] + 0.25]
    if not witnesses:
        die(f"p{page_number} a{annotation_index}: audited span has no glyph witnesses")
    return {
        "page": page_number,
        "annotation_index": annotation_index,
        "target": action,
        "old_rect": [round(value, 6) for value in old_rect],
        "new_rect": [round(old_rect[0], 6), round(old_rect[1], 6),
                     round(span["glyph_x1"] + 1.0, 6), round(old_rect[3], 6)],
        "inflation_signature": round(old_rect[2] - old_rect[0], 6),
        "glyph_bbox_top_coordinates": [round(span["glyph_x0"], 6),
                                        round(min(f(char["top"]) for char in witnesses), 6),
                                        round(span["glyph_x1"], 6),
                                        round(max(f(char["bottom"]) for char in witnesses), 6)],
        "glyph_text_ascii": text_ascii(span["text"]),
        "annotation_colour": list(colour_tuple(annot.get("/C"))),
        "method": "independent-audited-bidi-glyph-span",
        "companion_rects": [],
        "candidate_runs": [{"x0": round(span["glyph_x0"], 6),
                            "x1": round(span["glyph_x1"], 6),
                            "text_ascii": text_ascii(span["text"])}],
    }


def scan_bad_annotations(reader: PdfReader) -> tuple[list[dict[str, Any]], Counter]:
    bad: list[dict[str, Any]] = []
    signatures: Counter = Counter()
    for page_index, page in enumerate(reader.pages):
        box = [f(value) for value in page.mediabox]
        width = box[2] - box[0]
        height = box[3] - box[1]
        if any(abs(left - right) > 0.001 for left, right in
               zip((box[0], box[1], width, height), (0.0, 0.0, PAGE_WIDTH, PAGE_HEIGHT))):
            die(f"p{page_index + 1}: MediaBox is not [0,0,960,540]: {box}")
        for annotation_index, ref in enumerate(page.get("/Annots") or []):
            annot = ref.get_object()
            if str(annot.get("/Subtype")) != "/Link":
                continue
            rect = rect_values(annot)
            outside = rect[0] < -0.01 or rect[1] < -0.01 or rect[2] > width + 0.01 or rect[3] > height + 0.01
            if not outside:
                continue
            signature = rect[2] - rect[0]
            if not (rect[2] > width + 0.01 and rect[0] >= -0.01 and rect[1] >= -0.01 and rect[3] <= height + 0.01):
                die(f"p{page_index + 1} a{annotation_index}: unknown outside-page direction {rect}")
            nearest = min(EXPECTED_INFLATIONS, key=lambda value: abs(value - signature))
            if abs(nearest - signature) > 0.01:
                die(f"p{page_index + 1} a{annotation_index}: unknown width signature {signature:.6f}")
            signatures[round(signature, 3)] += 1
            bad.append({"page_index": page_index, "annotation_index": annotation_index,
                        "annot": annot, "page": page})
    return bad, signatures


def content_hashes(reader: PdfReader) -> list[str]:
    result = []
    for page in reader.pages:
        contents = page.get_contents()
        data = b"" if contents is None else contents.get_data()
        result.append(sha256_bytes(data))
    return result


def canonical_pdf_value(value: Any, *, drop_keys: frozenset[str] = frozenset(),
                        depth: int = 0) -> Any:
    if depth > 20:
        die("PDF object nesting exceeded verification limit")
    if hasattr(value, "get_object") and not isinstance(value, (dict, list, tuple, str, bytes)):
        value = value.get_object()
    if isinstance(value, dict):
        result = {}
        for key in sorted(value, key=str):
            if str(key) in drop_keys:
                continue
            result[str(key)] = canonical_pdf_value(value[key], drop_keys=drop_keys,
                                                   depth=depth + 1)
        if hasattr(value, "get_data"):
            result["__stream_sha256__"] = sha256_bytes(value.get_data())
            result.pop("/Length", None)
        return result
    if isinstance(value, (list, tuple)):
        return [canonical_pdf_value(item, drop_keys=drop_keys, depth=depth + 1)
                for item in value]
    if isinstance(value, bytes):
        return {"bytes_sha256": sha256_bytes(value), "bytes_length": len(value)}
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, float)):
        return round(float(value), 9)
    return str(value)


def annotation_snapshot(reader: PdfReader) -> list[list[dict[str, Any]]]:
    snapshot: list[list[dict[str, Any]]] = []
    for page in reader.pages:
        page_entries = []
        for ref in page.get("/Annots") or []:
            annot = ref.get_object()
            rect = ([round(f(value), 6) for value in annot.get("/Rect")]
                    if annot.get("/Rect") is not None else None)
            semantic = canonical_pdf_value(annot, drop_keys=frozenset(("/Rect", "/P")))
            page_entries.append({"rect": rect, "semantic": semantic})
        snapshot.append(page_entries)
    return snapshot


def text_extraction_fingerprint(reader: PdfReader) -> str:
    digest = hashlib.sha256()
    for page_index, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        payload = text.encode("utf-8", "surrogatepass")
        digest.update(page_index.to_bytes(8, "big"))
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest().upper()


def metadata_fingerprint(reader: PdfReader) -> str:
    data = {str(key): str(value) for key, value in (reader.metadata or {}).items()}
    return sha256_bytes(json.dumps(data, ensure_ascii=True, sort_keys=True,
                                   separators=(",", ":")).encode("ascii"))


def named_destination_fingerprint(reader: PdfReader) -> tuple[str, int]:
    records = []
    for name, destination in sorted(reader.named_destinations.items()):
        try:
            page_number = reader.get_destination_page_number(destination)
        except Exception:
            page_number = None
        records.append({
            "name": str(name),
            "page": page_number,
            "typ": str(getattr(destination, "typ", None)),
            "left": str(getattr(destination, "left", None)),
            "top": str(getattr(destination, "top", None)),
            "zoom": str(getattr(destination, "zoom", None)),
        })
    payload = json.dumps(records, ensure_ascii=True, sort_keys=True,
                         separators=(",", ":")).encode("ascii")
    return sha256_bytes(payload), len(records)


def outline_fingerprint(reader: PdfReader) -> tuple[str, int]:
    records: list[dict[str, Any]] = []

    def walk(items: Iterable[Any], depth: int) -> None:
        for item in items:
            if isinstance(item, list):
                walk(item, depth + 1)
                continue
            try:
                page_number = reader.get_destination_page_number(item)
            except Exception:
                page_number = None
            records.append({"depth": depth, "title": str(getattr(item, "title", item)),
                            "page": page_number})

    walk(reader.outline, 0)
    payload = json.dumps(records, ensure_ascii=True, sort_keys=True,
                         separators=(",", ":")).encode("ascii")
    return sha256_bytes(payload), len(records)


def font_fingerprint(reader: PdfReader) -> tuple[str, int]:
    """Fingerprint page font resources, including embedded font streams."""
    records = []
    for page_index, page in enumerate(reader.pages):
        resources = page.get("/Resources")
        if resources is None:
            continue
        resources = resources.get_object()
        fonts = resources.get("/Font")
        if fonts is None:
            continue
        fonts = fonts.get_object()
        for resource_name, font_ref in sorted(fonts.items(), key=lambda item: str(item[0])):
            font = font_ref.get_object()
            records.append({
                "page": page_index + 1,
                "resource": str(resource_name),
                "font": canonical_pdf_value(font, drop_keys=frozenset(("/Length",))),
            })
    payload = json.dumps(records, ensure_ascii=True, sort_keys=True,
                         separators=(",", ":")).encode("ascii")
    return sha256_bytes(payload), len(records)


def page_box_fingerprint(reader: PdfReader) -> str:
    records = []
    for page in reader.pages:
        records.append({
            "MediaBox": [round(f(value), 6) for value in page.mediabox],
            "CropBox": [round(f(value), 6) for value in page.cropbox],
            "Rotate": int(page.get("/Rotate", 0)),
        })
    return sha256_bytes(json.dumps(records, sort_keys=True,
                                   separators=(",", ":")).encode("ascii"))


def catalog_view(reader: PdfReader) -> dict[str, Any]:
    root = reader.trailer["/Root"]
    action = root.get("/OpenAction")
    if hasattr(action, "get_object"):
        action = action.get_object()
    if isinstance(action, dict):
        destination = action.get("/D")
    else:
        destination = action
    fit = None
    if isinstance(destination, (list, tuple)) and len(destination) >= 2:
        fit = str(destination[1])
    return {"PageLayout": str(root.get("/PageLayout")),
            "PageMode": str(root.get("/PageMode")), "OpenActionFit": fit}


def validate_link_targets(reader: PdfReader, pdf_path: Path) -> dict[str, int]:
    named = set(reader.named_destinations)
    counts: Counter = Counter()
    for page_index, page in enumerate(reader.pages):
        for annotation_index, ref in enumerate(page.get("/Annots") or []):
            annot = ref.get_object()
            if str(annot.get("/Subtype")) != "/Link":
                continue
            counts["links"] += 1
            action = annot.get("/A")
            if action is None:
                destination = annot.get("/Dest")
                if destination is not None and not isinstance(destination, (list, tuple)):
                    if str(destination) not in named:
                        die(f"p{page_index + 1} a{annotation_index}: missing /Dest {destination}")
                counts["direct_dest"] += 1
                continue
            action = action.get_object()
            kind = str(action.get("/S"))
            destination = action.get("/D")
            if kind == "/GoTo":
                if destination is not None and not isinstance(destination, (list, tuple)):
                    if str(destination) not in named:
                        die(f"p{page_index + 1} a{annotation_index}: missing GoTo {destination}")
                counts["goto"] += 1
            elif kind == "/GoToR":
                file_spec = action.get("/F")
                if not file_spec:
                    die(f"p{page_index + 1} a{annotation_index}: GoToR lacks /F")
                candidate = pdf_path.parent / str(file_spec)
                if not candidate.exists():
                    die(f"p{page_index + 1} a{annotation_index}: GoToR file missing: {candidate}")
                counts["gotor"] += 1
            elif kind == "/URI":
                if not action.get("/URI"):
                    die(f"p{page_index + 1} a{annotation_index}: URI link lacks /URI")
                counts["uri"] += 1
            else:
                counts[f"action:{kind}"] += 1
    return dict(sorted(counts.items()))


def run(input_path: Path, output_path: Path, receipt_path: Path, dry_run: bool) -> None:
    raw_hash = sha256_file(input_path)
    reader = PdfReader(str(input_path), strict=True)
    bad, signatures = scan_bad_annotations(reader)
    if not bad:
        die("input contains no malformed link rectangles")

    by_page: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for entry in bad:
        by_page[entry["page_index"]].append(entry)

    mappings: list[dict[str, Any]] = []
    is_supplement = "closure-supplement" in input_path.name
    used_audited_spans: set[tuple[int, int, str]] = set()
    with pdfplumber.open(str(input_path)) as plumber:
        for page_index in sorted(by_page):
            plumber_page = plumber.pages[page_index]
            chars = plumber_page.chars
            page = reader.pages[page_index]
            annots = [ref.get_object() for ref in (page.get("/Annots") or [])]
            for entry in by_page[page_index]:
                action = action_summary(entry["annot"])
                audited_key = (page_index + 1, entry["annotation_index"], str(action.get("D")))
                if is_supplement:
                    if audited_key not in SUPPLEMENT_AUDITED_SPANS:
                        die(f"supplement malformed link lacks audited span: {audited_key}")
                    mappings.append(audited_supplement_mapping(
                        page_index + 1, entry["annotation_index"], entry["annot"],
                        chars, SUPPLEMENT_AUDITED_SPANS[audited_key]))
                    used_audited_spans.add(audited_key)
                else:
                    mappings.append(infer_mapping(
                        page_index + 1, entry["annotation_index"], entry["annot"],
                        annots, chars, PAGE_WIDTH, PAGE_HEIGHT))
            plumber_page.close()

    if is_supplement and used_audited_spans != set(SUPPLEMENT_AUDITED_SPANS):
        missing = sorted(set(SUPPLEMENT_AUDITED_SPANS) - used_audited_spans)
        die(f"supplement did not present every audited malformed link: {missing}")

    if len(mappings) != len(bad):
        die("mapping count does not equal malformed annotation count")

    receipt: dict[str, Any] = {
        "schema": "arabic-screen-rtl-link-rect-repair-v1",
        "input": str(input_path.resolve()),
        "output": str(output_path.resolve()),
        "input_sha256": raw_hash,
        "pages": len(reader.pages),
        "malformed_link_rectangles": len(bad),
        "width_signatures": dict(sorted(signatures.items())),
        "mappings": mappings,
        "dry_run": dry_run,
    }

    if dry_run:
        print(json.dumps(receipt, ensure_ascii=True, indent=2, sort_keys=True))
        return

    before_content = content_hashes(reader)
    before_annots = annotation_snapshot(reader)
    before_text = text_extraction_fingerprint(reader)
    before_metadata = metadata_fingerprint(reader)
    before_destinations = named_destination_fingerprint(reader)
    before_outline = outline_fingerprint(reader)
    before_fonts = font_fingerprint(reader)
    before_boxes = page_box_fingerprint(reader)
    before_catalog = catalog_view(reader)
    for mapping in mappings:
        page = reader.pages[mapping["page"] - 1]
        annot = (page.get("/Annots") or [])[mapping["annotation_index"]].get_object()
        current = [round(value, 6) for value in rect_values(annot)]
        if current != mapping["old_rect"]:
            die(f"p{mapping['page']} a{mapping['annotation_index']}: /Rect changed before write")
        annot[NameObject("/Rect")] = ArrayObject(
            [FloatObject(value) for value in mapping["new_rect"]])

    writer = PdfWriter(clone_from=reader)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        writer.write(handle)

    final_reader = PdfReader(str(output_path), strict=True)
    remaining, _ = scan_bad_annotations(final_reader)
    if remaining:
        die(f"final PDF still contains {len(remaining)} outside-page link rectangles")
    after_content = content_hashes(final_reader)
    if before_content != after_content:
        die("page content streams changed during annotation-only rewrite")
    after_annots = annotation_snapshot(final_reader)
    if len(before_annots) != len(after_annots):
        die("page count changed in annotation snapshot")
    expected_changes = {(mapping["page"], mapping["annotation_index"]): mapping
                        for mapping in mappings}
    observed_changes: list[tuple[int, int]] = []
    for page_index, (before_page, after_page) in enumerate(zip(before_annots, after_annots), 1):
        if len(before_page) != len(after_page):
            die(f"p{page_index}: annotation count changed")
        for annotation_index, (before_annot, after_annot) in enumerate(zip(before_page, after_page)):
            if before_annot["semantic"] != after_annot["semantic"]:
                die(f"p{page_index} a{annotation_index}: non-/Rect annotation semantics changed")
            if before_annot["rect"] != after_annot["rect"]:
                observed_changes.append((page_index, annotation_index))
                mapping = expected_changes.get((page_index, annotation_index))
                if mapping is None or after_annot["rect"] != mapping["new_rect"]:
                    die(f"p{page_index} a{annotation_index}: unexpected /Rect delta")
    if set(observed_changes) != set(expected_changes):
        die("observed /Rect changes do not equal the fail-closed mapping")

    after_text = text_extraction_fingerprint(final_reader)
    after_metadata = metadata_fingerprint(final_reader)
    after_destinations = named_destination_fingerprint(final_reader)
    after_outline = outline_fingerprint(final_reader)
    after_fonts = font_fingerprint(final_reader)
    after_boxes = page_box_fingerprint(final_reader)
    after_catalog = catalog_view(final_reader)
    comparisons = {
        "text_extraction_fingerprint_equal": before_text == after_text,
        "metadata_fingerprint_equal": before_metadata == after_metadata,
        "named_destinations_fingerprint_equal": before_destinations == after_destinations,
        "outline_fingerprint_equal": before_outline == after_outline,
        "font_resource_fingerprint_equal": before_fonts == after_fonts,
        "page_box_fingerprint_equal": before_boxes == after_boxes,
        "catalog_view_equal": before_catalog == after_catalog,
    }
    failed = [name for name, value in comparisons.items() if not value]
    if failed:
        die(f"semantic post-write comparisons failed: {failed}")
    target_counts = validate_link_targets(final_reader, output_path)

    receipt.update({
        "dry_run": False,
        "output_sha256": sha256_file(output_path),
        "output_bytes": output_path.stat().st_size,
        "semantic_invariants": {
            "strict_reopen": True,
            "page_count_equal": len(reader.pages) == len(final_reader.pages),
            "all_page_content_stream_hashes_equal": True,
            **comparisons,
            "text_extraction_sha256": after_text,
            "metadata_sha256": after_metadata,
            "named_destinations_sha256": after_destinations[0],
            "named_destinations_count": after_destinations[1],
            "outline_sha256": after_outline[0],
            "outline_count": after_outline[1],
            "font_resources_sha256": after_fonts[0],
            "font_resource_occurrences": after_fonts[1],
            "page_boxes_sha256": after_boxes,
            "catalog_view": after_catalog,
            "link_target_counts": target_counts,
            "all_link_targets_valid": True,
            "outside_page_link_rectangles_final": 0,
            "annotation_counts_equal": True,
            "non_rect_annotation_semantics_equal": True,
            "rectangles_changed_exactly": len(observed_changes),
            "changed_pdf_keys": ["page /Annots[n] /Rect"],
        },
    })
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8")
    print(json.dumps({"output": str(output_path), "receipt": str(receipt_path),
                      "changed": len(mappings), "sha256": receipt["output_sha256"]},
                     sort_keys=True))


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
