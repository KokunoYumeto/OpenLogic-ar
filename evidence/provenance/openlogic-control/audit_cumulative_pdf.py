#!/usr/bin/env python3
"""Emit a deterministic structural audit for one cumulative Open Logic PDF."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import unicodedata
from pathlib import Path

from pypdf import PdfReader
from pypdf.generic import ArrayObject, Destination, DictionaryObject, IndirectObject


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def resolve(value):
    return value.get_object() if isinstance(value, IndirectObject) else value


def plain(value):
    value = resolve(value)
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, ArrayObject):
        return [plain(item) for item in value]
    if isinstance(value, DictionaryObject):
        return {str(key): plain(item) for key, item in value.items()}
    return str(value)


def flatten_outline(items, reader: PdfReader):
    rows = []
    for item in items:
        if isinstance(item, list):
            rows.extend(flatten_outline(item, reader))
            continue
        title = getattr(item, "title", str(item))
        try:
            page = reader.get_destination_page_number(item) + 1
        except Exception:
            page = None
        rows.append({"title": title, "page": page})
    return rows


def destination_page(reader: PdfReader, value):
    value = resolve(value)
    if isinstance(value, Destination):
        return reader.get_destination_page_number(value) + 1
    if isinstance(value, str):
        names = reader.named_destinations
        if value in names:
            return reader.get_destination_page_number(names[value]) + 1
        return None
    if isinstance(value, ArrayObject) and value:
        page_ref = value[0]
        for index, page in enumerate(reader.pages):
            if page.indirect_reference == page_ref:
                return index + 1
    return None


def count_range(text: str, start: int, end: int) -> int:
    return sum(start <= ord(ch) <= end for ch in text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--poppler-text", type=Path)
    args = parser.parse_args()

    reader = PdfReader(str(args.pdf))
    root = resolve(reader.trailer["/Root"])
    metadata = reader.metadata or {}
    annotations = []
    invalid_goto = []
    counts = {}
    for page_index, page in enumerate(reader.pages, start=1):
        for annotation_ref in page.get("/Annots", []):
            annotation = resolve(annotation_ref)
            subtype = str(annotation.get("/Subtype", ""))
            action = resolve(annotation.get("/A")) if annotation.get("/A") else None
            destination = annotation.get("/Dest")
            action_type = str(action.get("/S", "")) if action else ""
            row = {"page": page_index, "subtype": subtype, "action": action_type}
            if action_type == "/URI":
                row["uri"] = str(action.get("/URI", ""))
            elif action_type == "/GoTo":
                target = destination_page(reader, action.get("/D"))
                row["target_page"] = target
                if target is None:
                    invalid_goto.append(row.copy())
            elif destination is not None:
                target = destination_page(reader, destination)
                row["action"] = "/Dest"
                row["target_page"] = target
                if target is None:
                    invalid_goto.append(row.copy())
            annotations.append(row)
            counts[row["action"] or subtype] = counts.get(row["action"] or subtype, 0) + 1

    pypdf_text = "\n\f\n".join(page.extract_text() or "" for page in reader.pages)
    extraction = {
        "pypdf_characters": len(pypdf_text),
        "pypdf_replacement_characters": pypdf_text.count("\ufffd"),
        "pypdf_presentation_forms": count_range(pypdf_text, 0xFB50, 0xFDFF)
        + count_range(pypdf_text, 0xFE70, 0xFEFF),
        "pypdf_zwnj": pypdf_text.count("\u200c"),
        "pypdf_bidi_controls": {
            f"U+{code:04X}": pypdf_text.count(chr(code))
            for code in list(range(0x202A, 0x202F)) + list(range(0x2066, 0x206A))
            if pypdf_text.count(chr(code))
        },
        "pypdf_nfc": unicodedata.normalize("NFC", pypdf_text) == pypdf_text,
    }
    if args.poppler_text and args.poppler_text.exists():
        poppler_text = args.poppler_text.read_text(encoding="utf-8-sig")
        extraction.update(
            {
                "poppler_characters": len(poppler_text),
                "poppler_replacement_characters": poppler_text.count("\ufffd"),
                "poppler_presentation_forms": count_range(poppler_text, 0xFB50, 0xFDFF)
                + count_range(poppler_text, 0xFE70, 0xFEFF),
                "poppler_zwnj": poppler_text.count("\u200c"),
                "poppler_nfc": unicodedata.normalize("NFC", poppler_text) == poppler_text,
                "poppler_sha256": sha256(args.poppler_text),
            }
        )

    output = {
        "schema": "openlogic-cumulative-pdf-audit-v1",
        "pdf": str(args.pdf.resolve()),
        "bytes": args.pdf.stat().st_size,
        "sha256": sha256(args.pdf),
        "pages": len(reader.pages),
        "encrypted": reader.is_encrypted,
        "metadata": {str(key): str(value) for key, value in metadata.items()},
        "catalog": {
            "Lang": plain(root.get("/Lang")),
            "PageMode": plain(root.get("/PageMode")),
            "ViewerPreferences": plain(root.get("/ViewerPreferences")),
            "MarkInfo": plain(root.get("/MarkInfo")),
            "has_StructTreeRoot": "/StructTreeRoot" in root,
            "has_AcroForm": "/AcroForm" in root,
            "has_OpenAction": "/OpenAction" in root,
            "has_Names": "/Names" in root,
        },
        "outlines": flatten_outline(reader.outline, reader),
        "annotation_counts": counts,
        "annotations": annotations,
        "invalid_internal_destinations": invalid_goto,
        "extraction": extraction,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
