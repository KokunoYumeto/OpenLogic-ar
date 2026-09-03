#!/usr/bin/env python3
"""Build the deterministic OpenLogic Machrek digit presentation font.

The Arabic Open Logic source retains ASCII digits and conventional LTR formula
order.  This font maps the ASCII digit character slots to the Arabic-Indic
digit outlines already present in XITS Math 1.302.  LuaTeX therefore sees
ordinary ASCII math character nodes while the PDF presents Machrek digit
shapes.  No translated source or formula token stream is rewritten.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import fontTools
from fontTools.ttLib import TTFont


SOURCE_BYTES = 548_096
SOURCE_SHA256 = "3025792ADB0B7072ACE08BF5726D341DE32F2254612DDEC6DD98271A8DD29689"
LICENSE_BYTES = 4_998
LICENSE_SHA256 = "10C83ACB7BF240C6E263906E0905C8E419F3483C89141E83243465C221D322AD"
SOURCE_URL = "https://github.com/aliftype/xits/blob/v1.302/XITSMath-Regular.otf"
LICENSE_URL = "https://github.com/aliftype/xits/blob/v1.302/OFL.txt"
FAMILY_NAME = "OpenLogic Machrek Digits"
POSTSCRIPT_NAME = "OpenLogicMachrekDigits-Regular"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def require_exact(path: Path, expected_bytes: int, expected_hash: str, label: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"{label} is missing: {path}")
    actual_bytes = path.stat().st_size
    actual_hash = sha256(path)
    if actual_bytes != expected_bytes or actual_hash != expected_hash:
        raise ValueError(
            f"{label} identity mismatch: bytes={actual_bytes}, sha256={actual_hash}; "
            f"expected bytes={expected_bytes}, sha256={expected_hash}"
        )


def set_english_windows_name(font: TTFont, name_id: int, value: str) -> None:
    table = font["name"]
    table.names = [record for record in table.names if record.nameID != name_id]
    table.setName(value, name_id, 3, 1, 0x0409)


def build(source: Path, license_path: Path, output: Path, receipt: Path) -> dict[str, object]:
    require_exact(source, SOURCE_BYTES, SOURCE_SHA256, "XITS Math source font")
    require_exact(license_path, LICENSE_BYTES, LICENSE_SHA256, "XITS OFL license")

    font = TTFont(source, recalcTimestamp=False)
    if font["OS/2"].fsType != 0:
        raise ValueError(f"source font embedding flags are not installable/embeddable: {font['OS/2'].fsType}")

    source_cmap = font.getBestCmap()
    glyph_mapping: dict[str, str] = {}
    for digit in range(10):
        source_codepoint = 0x0660 + digit
        glyph = source_cmap.get(source_codepoint)
        if glyph is None:
            raise ValueError(f"source font lacks U+{source_codepoint:04X}")
        glyph_mapping[f"U+{0x0030 + digit:04X}"] = glyph

    changed_cmaps = 0
    for cmap_table in font["cmap"].tables:
        if not cmap_table.isUnicode():
            continue
        for digit in range(10):
            cmap_table.cmap[0x0030 + digit] = glyph_mapping[f"U+{0x0030 + digit:04X}"]
        changed_cmaps += 1
    if changed_cmaps == 0:
        raise ValueError("source font has no Unicode cmap table")

    original_copyright = next(
        (
            record.toUnicode()
            for record in font["name"].names
            if record.nameID == 0 and "Copyright" in record.toUnicode()
        ),
        "",
    )
    if not original_copyright:
        raise ValueError("source font copyright metadata is missing")

    set_english_windows_name(
        font,
        0,
        original_copyright
        + " Modified in 2026 for the Open Logic Arabic notation profiles; "
        + "the modification remaps only digit presentation slots.",
    )
    set_english_windows_name(font, 1, FAMILY_NAME)
    set_english_windows_name(font, 2, "Regular")
    set_english_windows_name(font, 3, "OpenLogicMachrekDigits-1.302-1")
    set_english_windows_name(font, 4, FAMILY_NAME)
    set_english_windows_name(font, 5, "Version 1.302; OpenLogic digit-map 1")
    set_english_windows_name(font, 6, POSTSCRIPT_NAME)
    set_english_windows_name(
        font,
        10,
        "A modified XITS Math 1.302 face. ASCII digit slots U+0030--U+0039 "
        "present the corresponding Arabic-Indic digit outlines U+0660--U+0669. "
        "Formula direction and source character data are not changed.",
    )
    set_english_windows_name(
        font,
        13,
        "Licensed under the SIL Open Font License, Version 1.1. "
        "See the bundled vendor/xits-1.302/OFL.txt file.",
    )
    set_english_windows_name(font, 14, "https://openfontlicense.org/open-font-license-official-text/")
    set_english_windows_name(font, 16, FAMILY_NAME)
    set_english_windows_name(font, 17, "Regular")

    # Preserve the fixed upstream timestamps and suppress save-time clock data.
    font.recalcTimestamp = False
    output.parent.mkdir(parents=True, exist_ok=True)
    font.save(output, reorderTables=True)

    result = TTFont(output, recalcTimestamp=False)
    result_cmap = result.getBestCmap()
    failures: list[str] = []
    for digit in range(10):
        ascii_cp = 0x0030 + digit
        arabic_cp = 0x0660 + digit
        expected_glyph = glyph_mapping[f"U+{ascii_cp:04X}"]
        if result_cmap.get(ascii_cp) != expected_glyph:
            failures.append(f"U+{ascii_cp:04X} does not map to {expected_glyph}")
        if result_cmap.get(arabic_cp) != expected_glyph:
            failures.append(f"original U+{arabic_cp:04X} mapping was not retained")
    if result["OS/2"].fsType != 0:
        failures.append(f"output fsType={result['OS/2'].fsType}, expected 0")

    names = {
        str(name_id): sorted(
            {
                record.toUnicode()
                for record in result["name"].names
                if record.nameID == name_id
            }
        )
        for name_id in (0, 1, 2, 3, 4, 5, 6, 10, 13, 14, 16, 17)
    }
    if names["1"] != [FAMILY_NAME] or names["6"] != [POSTSCRIPT_NAME]:
        failures.append("renamed family or PostScript identity is incorrect")
    if any("STIX Fonts" == value or "TM Math" == value for value in names["1"]):
        failures.append("a Reserved Font Name remains in the primary family name")

    payload: dict[str, object] = {
        "schema": "openlogic-machrek-digit-font-provenance-v1",
        "status": "PASS" if not failures else "FAIL",
        "purpose": (
            "Presentation-only Arabic-Indic math digits while retaining ASCII source "
            "characters and left-to-right formula order."
        ),
        "source": {
            "path": str(source.resolve()),
            "url": SOURCE_URL,
            "version": "XITS 1.302",
            "bytes": source.stat().st_size,
            "sha256": sha256(source),
            "embedding_fsType": font["OS/2"].fsType,
        },
        "license": {
            "path": str(license_path.resolve()),
            "url": LICENSE_URL,
            "identifier": "OFL-1.1",
            "bytes": license_path.stat().st_size,
            "sha256": sha256(license_path),
        },
        "build": {
            "fonttools_version": fontTools.__version__,
            "unicode_cmap_tables_modified": changed_cmaps,
            "source_slots": [f"U+{0x0030 + digit:04X}" for digit in range(10)],
            "visual_glyph_sources": [f"U+{0x0660 + digit:04X}" for digit in range(10)],
            "glyph_mapping": glyph_mapping,
            "source_transform": "none",
            "formula_direction": "LTR",
        },
        "output": {
            "path": str(output.resolve()),
            "family": FAMILY_NAME,
            "postscript_name": POSTSCRIPT_NAME,
            "bytes": output.stat().st_size,
            "sha256": sha256(output),
            "embedding_fsType": result["OS/2"].fsType,
            "names": names,
        },
        "failures": failures,
    }
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if failures:
        raise ValueError("font verification failed: " + "; ".join(failures))
    return payload


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    default_vendor = root / "source" / "locale" / "ar" / "fonts" / "vendor" / "xits-1.302"
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=default_vendor / "XITSMath-Regular.otf")
    parser.add_argument("--license", dest="license_path", type=Path, default=default_vendor / "OFL.txt")
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "source" / "locale" / "ar" / "fonts" / "OpenLogicMachrekDigits-Regular.otf",
    )
    parser.add_argument(
        "--receipt",
        type=Path,
        default=root / "evidence" / "notation" / "MACHREK_DIGIT_FONT_PROVENANCE.json",
    )
    args = parser.parse_args()
    payload = build(args.source, args.license_path, args.output, args.receipt)
    print(
        json.dumps(
            {
                "status": payload["status"],
                "output": payload["output"]["path"],
                "sha256": payload["output"]["sha256"],
                "receipt": str(args.receipt.resolve()),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
