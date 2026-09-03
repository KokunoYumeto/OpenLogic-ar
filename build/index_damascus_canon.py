#!/usr/bin/env python3
"""Extract page-addressable terminology evidence from Internet Archive DjVu XML."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET


DEFAULT_QUERIES = {
    "decimal point": r"\bdecimal\s+point\b",
    "digit": r"\bdigit\s+رقم\b",
    "function": r"\bfunction\b",
    "limit": r"\blimit\s+نهاية\b",
    "product": r"\bproduct\s+جداء\b",
    "summation sign": r"\bsummation\s+sign\b",
    "variable": r"\bvariable\s+متغير\b",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def object_lines(element: ET.Element) -> list[str]:
    lines: list[str] = []
    for line in element.iter("LINE"):
        words = ["".join(word.itertext()).strip() for word in line.findall("WORD")]
        text = " ".join(word for word in words if word)
        if text:
            lines.append(text)
    return lines


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xml", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--context-lines", type=int, default=3)
    args = parser.parse_args()

    compiled = {
        label: re.compile(pattern, re.IGNORECASE) for label, pattern in DEFAULT_QUERIES.items()
    }
    hits: dict[str, list[dict[str, object]]] = {label: [] for label in compiled}
    object_index = -1

    for _event, element in ET.iterparse(args.xml, events=("end",)):
        if element.tag != "OBJECT":
            continue
        object_index += 1
        lines = object_lines(element)
        joined = "\n".join(lines)
        for label, pattern in compiled.items():
            if not pattern.search(joined):
                continue
            matching_lines = [index for index, line in enumerate(lines) if pattern.search(line)]
            for line_index in matching_lines:
                start = max(0, line_index - args.context_lines)
                end = min(len(lines), line_index + args.context_lines + 1)
                hits[label].append(
                    {
                        "pdf_page": object_index + 1,
                        "object_index_zero_based": object_index,
                        "scan_leaf": element.get("usemap", ""),
                        "matched_line": lines[line_index],
                        "context": lines[start:end],
                    }
                )
        element.clear()

    payload = {
        "schema": "dam2018enar-selected-terminology-v1",
        "source": {
            "path": str(args.xml.resolve()),
            "bytes": args.xml.stat().st_size,
            "sha256": sha256(args.xml),
        },
        "queries": DEFAULT_QUERIES,
        "hits": hits,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
