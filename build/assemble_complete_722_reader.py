#!/usr/bin/env python3
"""Assemble one self-contained 722-source-unit Arabic Open Logic PDF.

The upstream book graph reaches 642 translated source files.  The separately
built closure document exposes the remaining 80 tracked translated files while
suppressing their import edges.  This assembler appends that closure inside the
reader, prefixes all closure-local named destinations, and converts the 25
cross-document reader links into ordinary internal links.
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
    DictionaryObject,
    Fit,
    NameObject,
    NullObject,
    TextStringObject,
)


CLOSURE_PREFIX = "closure-80."


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def page_stream_hash(page: Any) -> str:
    digest = hashlib.sha256()
    contents = page.get_contents()
    if contents is not None:
        data = contents.get_data()
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest().upper()


def text_fingerprint(readers: list[PdfReader]) -> str:
    digest = hashlib.sha256()
    absolute_page = 0
    for reader in readers:
        for page in reader.pages:
            text = (page.extract_text() or "").encode("utf-8", "surrogatepass")
            digest.update(absolute_page.to_bytes(8, "big"))
            digest.update(len(text).to_bytes(8, "big"))
            digest.update(text)
            absolute_page += 1
    return digest.hexdigest().upper()


def remapped_destination_array(
    source_reader: PdfReader,
    destination: Any,
    writer: PdfWriter,
    page_offset: int,
) -> ArrayObject:
    source_index = source_reader.get_destination_page_number(destination)
    if source_index < 0:
        raise ValueError(f"destination has no source page: {destination!r}")
    target_page = writer.pages[page_offset + source_index]
    values = ArrayObject([target_page.indirect_reference])
    for value in destination.dest_array[1:]:
        values.append(value)
    return values


def replace_named_destination_tree(
    writer: PdfWriter,
    reader: PdfReader,
    closure: PdfReader,
    page_offset: int,
) -> int:
    """Install a balanced NameTree containing reader and prefixed closure names.

    ``PdfWriter(clone_from=...)`` retains the source document's indirect
    ``/Names`` dictionary.  In pypdf 6.12.2, ``get_named_dest_root()`` does not
    find that indirect tree and creates an unused direct tree instead.  Rebuild
    ``/Dests`` explicitly so every appended closure destination is reachable
    from the catalog while preserving any other catalog name trees.
    """

    entries: list[tuple[str, ArrayObject]] = []
    names_seen: set[str] = set()
    for name, destination in reader.named_destinations.items():
        if name in names_seen:
            raise ValueError(f"duplicate reader destination name: {name}")
        names_seen.add(name)
        entries.append(
            (name, remapped_destination_array(reader, destination, writer, 0))
        )
    for name, destination in closure.named_destinations.items():
        prefixed_name = CLOSURE_PREFIX + name
        if prefixed_name in names_seen:
            raise ValueError(
                f"prefixed closure destination collides with reader: {prefixed_name}"
            )
        names_seen.add(prefixed_name)
        entries.append(
            (
                prefixed_name,
                remapped_destination_array(
                    closure, destination, writer, page_offset
                ),
            )
        )
    entries.sort(key=lambda item: item[0])
    if not entries:
        raise ValueError("refusing to install an empty destination NameTree")

    # Match the compact 32-pair leaf size emitted by the TeX source PDFs.
    # Internal fanout 32 keeps the resulting tree shallow and deterministic.
    nodes: list[tuple[Any, str, str]] = []
    for start in range(0, len(entries), 32):
        chunk = entries[start : start + 32]
        names_array = ArrayObject()
        for name, destination_array in chunk:
            names_array.append(TextStringObject(name))
            names_array.append(destination_array)
        leaf = DictionaryObject(
            {
                NameObject("/Names"): names_array,
                NameObject("/Limits"): ArrayObject(
                    [TextStringObject(chunk[0][0]), TextStringObject(chunk[-1][0])]
                ),
            }
        )
        nodes.append((writer._add_object(leaf), chunk[0][0], chunk[-1][0]))

    while len(nodes) > 1:
        parents: list[tuple[Any, str, str]] = []
        for start in range(0, len(nodes), 32):
            chunk = nodes[start : start + 32]
            branch = DictionaryObject(
                {
                    NameObject("/Kids"): ArrayObject(
                        [reference for reference, _, _ in chunk]
                    ),
                    NameObject("/Limits"): ArrayObject(
                        [TextStringObject(chunk[0][1]), TextStringObject(chunk[-1][2])]
                    ),
                }
            )
            parents.append(
                (writer._add_object(branch), chunk[0][1], chunk[-1][2])
            )
        nodes = parents

    root = writer._root_object
    names_reference = root.get("/Names")
    if names_reference is None:
        names_object = DictionaryObject()
        root[NameObject("/Names")] = writer._add_object(names_object)
    else:
        names_object = names_reference.get_object()
    names_object[NameObject("/Dests")] = nodes[0][0]
    return len(entries)


def fit_from_destination(destination: Any) -> Fit:
    values = list(destination.dest_array)
    kind = str(values[1])

    def number(index: int) -> float | None:
        if index >= len(values) or isinstance(values[index], NullObject):
            return None
        return float(values[index])

    if kind == "/XYZ":
        return Fit.xyz(number(2), number(3), number(4))
    if kind == "/Fit":
        return Fit.fit()
    if kind == "/FitH":
        return Fit.fit_horizontally(number(2))
    if kind == "/FitV":
        return Fit.fit_vertically(number(2))
    if kind == "/FitR":
        return Fit.fit_rectangle(number(2), number(3), number(4), number(5))
    if kind == "/FitB":
        return Fit.fit_box()
    if kind == "/FitBH":
        return Fit.fit_box_horizontally(number(2))
    if kind == "/FitBV":
        return Fit.fit_box_vertically(number(2))
    raise ValueError(f"unsupported outline destination fit: {kind}")


def import_outline(
    writer: PdfWriter,
    source_reader: PdfReader,
    sequence: list[Any],
    page_offset: int,
    parent: Any,
) -> int:
    imported = 0
    previous = None
    for item in sequence:
        if isinstance(item, list):
            if previous is None:
                raise ValueError("outline child list has no preceding parent")
            imported += import_outline(
                writer, source_reader, item, page_offset, previous
            )
            continue
        page_index = source_reader.get_destination_page_number(item)
        if page_index < 0:
            raise ValueError(f"outline item has no page: {item!r}")
        previous = writer.add_outline_item(
            str(item.title),
            page_offset + page_index,
            parent=parent,
            fit=fit_from_destination(item),
            is_open=bool(item.get("/%is_open%", True)),
        )
        imported += 1
    return imported


def link_inventory(reader: PdfReader) -> dict[str, Any]:
    names = set(reader.named_destinations)
    links = 0
    uri = 0
    goto = 0
    gotor = 0
    outside = 0
    broken: list[str] = []
    uri_values: list[str] = []
    rects: list[list[float]] = []
    for page_index, page in enumerate(reader.pages, 1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        for annotation_index, reference in enumerate(page.get("/Annots", [])):
            annotation = reference.get_object()
            if str(annotation.get("/Subtype")) != "/Link":
                continue
            links += 1
            rect = [float(value) for value in annotation["/Rect"]]
            rects.append([round(value, 6) for value in rect])
            if (
                rect[0] < -0.01
                or rect[1] < -0.01
                or rect[2] > width + 0.01
                or rect[3] > height + 0.01
                or rect[2] < rect[0]
                or rect[3] < rect[1]
            ):
                outside += 1
            action = annotation.get("/A")
            if hasattr(action, "get_object"):
                action = action.get_object()
            if not isinstance(action, dict):
                continue
            kind = str(action.get("/S", ""))
            if kind == "/URI":
                uri += 1
                uri_values.append(str(action.get("/URI", "")))
            elif kind == "/GoTo":
                goto += 1
                destination = action.get("/D")
                if destination is not None and not isinstance(destination, ArrayObject):
                    name = str(destination)
                    if name not in names:
                        broken.append(
                            f"p{page_index}:a{annotation_index}:missing:{name}"
                        )
            elif kind == "/GoToR":
                gotor += 1
    uri_digest = hashlib.sha256()
    for value in uri_values:
        encoded = value.encode("utf-8", "surrogatepass")
        uri_digest.update(len(encoded).to_bytes(8, "big"))
        uri_digest.update(encoded)
    rect_digest = hashlib.sha256(
        json.dumps(rects, separators=(",", ":")).encode("ascii")
    ).hexdigest().upper()
    return {
        "links": links,
        "uri": uri,
        "goto": goto,
        "gotor": gotor,
        "outside_page_rectangles": outside,
        "broken_internal_targets": broken,
        "uri_values_sha256": uri_digest.hexdigest().upper(),
        "rectangles_sha256": rect_digest,
    }


def assemble(
    reader_path: Path,
    closure_path: Path,
    output_path: Path,
    receipt_path: Path,
    profile: str,
) -> dict[str, Any]:
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
                    raise ValueError(f"closure link target is not closure-local: {name}")
                action[NameObject("/D")] = TextStringObject(CLOSURE_PREFIX + name)
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

    titles = {
        "international": (
            "نص المنطق المفتوح — النسخة العربية الكاملة 722 وحدة بالترميز الدولي",
            "Complete 722-source-unit Arabic edition — international mathematical notation",
        ),
        "machrek": (
            "نص المنطق المفتوح — النسخة العربية الكاملة 722 وحدة بترميز المشرق",
            "Complete 722-source-unit Arabic edition — Machrek Arabic-Indic formula digits",
        ),
    }
    if profile not in titles:
        raise ValueError(f"unknown profile: {profile}")
    title, subject = titles[profile]
    writer.add_metadata(
        {
            "/Title": title,
            "/Subject": subject,
            "/Author": "Open Logic Project",
            "/Producer": "LuaTeX; deterministic 722-unit assembly with pypdf 6.12.2",
        }
    )
    deterministic_id = hashlib.sha256(
        (sha256(reader_path) + sha256(closure_path) + profile).encode("ascii")
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
            f"named destinations={len(combined.named_destinations)}, expected {expected_names}"
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
        "schema": "openlogic-arabic-complete-722-reader-assembly-v1",
        "status": "PASS" if not failures else "FAIL",
        "profile": profile,
        "coverage": {
            "tracked_translated_source_units": 722,
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
            "page_content_streams_equal": output_stream_hashes
            == expected_stream_hashes,
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
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
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
    parser.add_argument(
        "--profile", choices=("international", "machrek"), required=True
    )
    args = parser.parse_args()
    try:
        payload = assemble(
            args.reader, args.closure, args.output, args.receipt, args.profile
        )
    except Exception as exc:
        print(f"FAIL-CLOSED: {exc}")
        return 2
    print(
        json.dumps(
            {
                "status": payload["status"],
                "file": payload["output"]["file"],
                "bytes": payload["output"]["bytes"],
                "sha256": payload["output"]["sha256"],
                "pages": payload["output"]["pages"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
