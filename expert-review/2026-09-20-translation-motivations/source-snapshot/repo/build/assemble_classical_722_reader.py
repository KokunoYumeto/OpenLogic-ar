#!/usr/bin/env python3
"""Assemble the Classical-Arabic reader and closure PDFs without page rewrites.

This Classical-only adapter deliberately leaves the existing MSA assembler and
its two profiles unchanged.  It reuses its audited low-level PDF helpers while
giving the third edition its own metadata, deterministic identifier and receipt
schema.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    ByteStringObject,
    Fit,
    NameObject,
    TextStringObject,
)

from assemble_complete_722_reader import (
    CLOSURE_PREFIX,
    import_outline,
    link_inventory,
    page_stream_hash,
    replace_named_destination_tree,
    sha256,
    text_fingerprint,
)


PROFILE = "classical-eastern-arabic-rtl"
SCHEMA = "openlogic-classical-arabic-complete-722-reader-assembly-v1"


def assemble(reader_path: Path, closure_path: Path, output_path: Path,
             receipt_path: Path) -> dict[str, Any]:
    if output_path.exists():
        raise FileExistsError(f"refusing to overwrite output: {output_path}")
    if receipt_path.exists():
        raise FileExistsError(f"refusing to overwrite receipt: {receipt_path}")

    reader = PdfReader(str(reader_path), strict=True)
    closure = PdfReader(str(closure_path), strict=True)
    reader_names = set(reader.named_destinations)
    closure_names = set(closure.named_destinations)
    page_offset = len(reader.pages)

    expected_stream_hashes = [page_stream_hash(page) for page in reader.pages]
    expected_stream_hashes.extend(page_stream_hash(page) for page in closure.pages)
    input_text_sha = text_fingerprint([reader, closure])
    reader_links = link_inventory(reader)
    closure_links = link_inventory(closure)

    writer = PdfWriter(clone_from=reader)
    for page in closure.pages:
        writer.add_page(page)
    installed_destination_count = replace_named_destination_tree(
        writer, reader, closure, page_offset
    )

    converted_external = 0
    prefixed_internal = 0
    expected_reader_filename = reader_path.name
    for page in writer.pages[page_offset:]:
        for reference in page.get("/Annots", []):
            annotation = reference.get_object()
            if str(annotation.get("/Subtype")) != "/Link":
                continue
            action = annotation.get("/A")
            if hasattr(action, "get_object"):
                action = action.get_object()
            if not isinstance(action, dict):
                continue
            kind = str(action.get("/S", ""))
            destination = action.get("/D")
            if kind == "/GoTo":
                if destination is None or isinstance(destination, ArrayObject):
                    continue
                name = str(destination)
                if name not in closure_names:
                    raise ValueError(
                        f"closure link target is not closure-local: {name}"
                    )
                action[NameObject("/D")] = TextStringObject(
                    CLOSURE_PREFIX + name
                )
                prefixed_internal += 1
            elif kind == "/GoToR":
                file_spec = str(action.get("/F", ""))
                name = str(destination)
                if file_spec != expected_reader_filename:
                    raise ValueError(
                        f"unexpected closure external file: {file_spec!r}, "
                        f"expected {expected_reader_filename!r}"
                    )
                if name not in reader_names:
                    raise ValueError(f"external target absent from reader: {name}")
                action[NameObject("/S")] = NameObject("/GoTo")
                action.pop(NameObject("/F"), None)
                action.pop(NameObject("/NewWindow"), None)
                converted_external += 1

    closure_parent = writer.add_outline_item(
        "ملحق إغلاق المصدر — الوحدات الثمانون",
        page_offset,
        bold=True,
        fit=Fit.fit_horizontally(None),
        is_open=False,
    )
    imported_outline_items = import_outline(
        writer, closure, closure.outline, page_offset, closure_parent
    )

    writer.add_metadata(
        {
            "/Title": (
                "نص المنطق المفتوح — الطبعة العربية ذات البيان التراثي "
                "الكاملة في 722 وحدة"
            ),
            "/Subject": (
                "Complete 722-source-unit Classical-Arabic edition — Eastern "
                "Arabic numerals, Arabic mathematical symbols, RTL formulas"
            ),
            "/Author": "Open Logic Project",
            "/Producer": (
                "LuaTeX; deterministic Classical 722-unit assembly with pypdf"
            ),
        }
    )
    deterministic_id = hashlib.sha256(
        (sha256(reader_path) + sha256(closure_path) + PROFILE).encode("ascii")
    ).digest()[:16]
    writer._ID = ArrayObject(
        [ByteStringObject(deterministic_id), ByteStringObject(deterministic_id)]
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as stream:
        writer.write(stream)

    combined = PdfReader(str(output_path), strict=True)
    output_stream_hashes = [page_stream_hash(page) for page in combined.pages]
    output_text_sha = text_fingerprint([combined])
    combined_links = link_inventory(combined)
    root = combined.trailer["/Root"]
    expected_names = len(reader_names) + len(closure_names)

    failures: list[str] = []
    if len(combined.pages) != len(reader.pages) + len(closure.pages):
        failures.append("page count is not reader plus closure")
    if output_stream_hashes != expected_stream_hashes:
        failures.append("one or more page content streams changed")
    if output_text_sha != input_text_sha:
        failures.append("concatenated text extraction changed")
    if len(combined.named_destinations) != expected_names:
        failures.append(
            f"named destinations={len(combined.named_destinations)}, "
            f"expected {expected_names}"
        )
    if converted_external != closure_links["gotor"]:
        failures.append("not every closure GoToR link was internalized")
    if prefixed_internal != closure_links["goto"]:
        failures.append("not every closure-local GoTo link was prefixed")
    if combined_links["links"] != reader_links["links"] + closure_links["links"]:
        failures.append("link count is not the sum of both components")
    if combined_links["gotor"] != 0:
        failures.append("combined PDF retains cross-document GoToR links")
    if combined_links["outside_page_rectangles"] != 0:
        failures.append("combined PDF has outside-page link rectangles")
    if combined_links["broken_internal_targets"]:
        failures.append("combined PDF has broken internal link targets")
    if str(root.get("/PageMode", "")) != "/UseOutlines":
        failures.append("PageMode is not /UseOutlines")
    if str(root.get("/PageLayout", "")) != "/OneColumn":
        failures.append("PageLayout is not /OneColumn")

    payload: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "PASS" if not failures else "FAIL",
        "profile": PROFILE,
        "coverage": {
            "tracked_classical_source_units": 722,
            "canonical_reader_graph_units": 642,
            "appended_closure_units": 80,
            "self_contained_pdf": True,
        },
        "inputs": {
            "reader": {
                "file": reader_path.name,
                "bytes": reader_path.stat().st_size,
                "sha256": sha256(reader_path),
                "pages": len(reader.pages),
            },
            "closure": {
                "file": closure_path.name,
                "bytes": closure_path.stat().st_size,
                "sha256": sha256(closure_path),
                "pages": len(closure.pages),
            },
        },
        "output": {
            "file": output_path.name,
            "bytes": output_path.stat().st_size,
            "sha256": sha256(output_path),
            "pages": len(combined.pages),
            "named_destinations": len(combined.named_destinations),
            "page_content_streams_equal":
                output_stream_hashes == expected_stream_hashes,
            "text_extraction_sha256": output_text_sha,
            "text_extraction_equal": output_text_sha == input_text_sha,
            "links": combined_links,
            "page_mode": str(root.get("/PageMode", "")),
            "page_layout": str(root.get("/PageLayout", "")),
        },
        "transform": {
            "closure_destination_prefix": CLOSURE_PREFIX,
            "closure_named_destinations_added": len(closure_names),
            "combined_named_destinations_installed": installed_destination_count,
            "closure_internal_links_prefixed": prefixed_internal,
            "closure_reader_links_internalized": converted_external,
            "closure_outline_items_imported": imported_outline_items,
            "page_content_changed": False,
        },
        "failures": failures,
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2,
                   sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if failures:
        raise ValueError("assembly QA failed: " + "; ".join(failures))
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reader", type=Path, required=True)
    parser.add_argument("--closure", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    try:
        payload = assemble(
            args.reader, args.closure, args.output, args.receipt
        )
    except Exception as exc:
        print(f"FAIL-CLOSED: {exc}")
        return 2
    print(json.dumps({
        "status": payload["status"],
        "file": payload["output"]["file"],
        "bytes": payload["output"]["bytes"],
        "sha256": payload["output"]["sha256"],
        "pages": payload["output"]["pages"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
