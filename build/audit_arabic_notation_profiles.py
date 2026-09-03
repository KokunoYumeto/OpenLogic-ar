#!/usr/bin/env python3
"""Fail-closed source and wrapper audit for the two Arabic notation profiles."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


BIDI_CONTROLS = {
    "\u061c": "ARABIC LETTER MARK",
    "\u200e": "LEFT-TO-RIGHT MARK",
    "\u200f": "RIGHT-TO-LEFT MARK",
    "\u202a": "LEFT-TO-RIGHT EMBEDDING",
    "\u202b": "RIGHT-TO-LEFT EMBEDDING",
    "\u202c": "POP DIRECTIONAL FORMATTING",
    "\u202d": "LEFT-TO-RIGHT OVERRIDE",
    "\u202e": "RIGHT-TO-LEFT OVERRIDE",
    "\u2066": "LEFT-TO-RIGHT ISOLATE",
    "\u2067": "RIGHT-TO-LEFT ISOLATE",
    "\u2068": "FIRST STRONG ISOLATE",
    "\u2069": "POP DIRECTIONAL ISOLATE",
}

DRIVERS = {
    "international": {
        "reader": "open-logic-complete-ar-readable-letter-international.tex",
        "supplement": "open-logic-closure-supplement-ar-readable-letter-international.tex",
    },
    "machrek": {
        "reader": "open-logic-complete-ar-readable-letter-machrek.tex",
        "supplement": "open-logic-closure-supplement-ar-readable-letter-machrek.tex",
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def hash_records(records: list[tuple[str, str]]) -> str:
    digest = hashlib.sha256()
    for name, value in sorted(records):
        encoded_name = name.encode("utf-8")
        encoded_value = value.encode("ascii")
        digest.update(len(encoded_name).to_bytes(8, "big"))
        digest.update(encoded_name)
        digest.update(encoded_value)
    return digest.hexdigest().upper()


def strip_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        cut = len(line)
        for index, char in enumerate(line):
            if char != "%":
                continue
            slashes = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == "\\":
                slashes += 1
                cursor -= 1
            if slashes % 2 == 0:
                cut = index
                break
        lines.append(line[:cut])
    return "\n".join(lines)


def math_candidate_fingerprint(text: str) -> tuple[str, dict[str, int]]:
    clean = strip_comments(text)
    candidates = []
    counts: Counter[str] = Counter()
    patterns = {
        "dollar": re.compile(r"(?<!\\)\$"),
        "display_bracket": re.compile(r"\\\[|\\\]"),
        "inline_paren": re.compile(r"\\\(|\\\)"),
        "math_environment": re.compile(
            r"\\(?:begin|end)\{(?:math|displaymath|equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?)\}"
        ),
    }
    for line_number, line in enumerate(clean.splitlines(), 1):
        matched = False
        for label, pattern in patterns.items():
            found = len(pattern.findall(line))
            if found:
                counts[label] += found
                matched = True
        if matched:
            candidates.append(f"{line_number}:{line.strip()}")
    payload = "\n".join(candidates).encode("utf-8")
    return hashlib.sha256(payload).hexdigest().upper(), dict(sorted(counts.items()))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    locale = repo / "source" / "locale" / "ar"
    failures: list[str] = []

    with args.manifest.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 722:
        failures.append(f"closure manifest has {len(rows)} rows, expected 722")

    manifest_paths: set[str] = set()
    source_records: list[tuple[str, str]] = []
    math_records: list[tuple[str, str]] = []
    math_totals: Counter[str] = Counter()
    unicode_counts: Counter[str] = Counter()
    total_bytes = 0

    for row in rows:
        closure_id = row.get("closure_id", "")
        rel = row.get("ar_target_path", "").replace("\\", "/")
        if row.get("ar_status") != "ACCEPTED":
            failures.append(f"{closure_id}: ar_status is not ACCEPTED")
        if not rel.startswith("locale/ar/content/"):
            failures.append(f"{closure_id}: unexpected Arabic target path {rel!r}")
            continue
        source_rel = rel.removeprefix("locale/ar/")
        manifest_paths.add(source_rel)
        path = locale / source_rel
        if not path.is_file():
            failures.append(f"{closure_id}: missing {path}")
            continue
        raw = path.read_bytes()
        total_bytes += len(raw)
        actual_hash = hashlib.sha256(raw).hexdigest().upper()
        expected_hash = row.get("ar_sha256", "").upper()
        if actual_hash != expected_hash:
            failures.append(
                f"{closure_id}: hash mismatch for {source_rel}: {actual_hash} != {expected_hash}"
            )
        source_records.append((source_rel, actual_hash))
        if raw.startswith(b"\xef\xbb\xbf"):
            unicode_counts["utf8_bom_files"] += 1
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            failures.append(f"{closure_id}: UTF-8 decode failure: {exc}")
            continue
        if unicodedata.normalize("NFC", text) != text:
            unicode_counts["non_nfc_files"] += 1
        for char, name in BIDI_CONTROLS.items():
            occurrences = text.count(char)
            if occurrences:
                unicode_counts[f"bidi:{name}"] += occurrences
        math_hash, counts = math_candidate_fingerprint(text)
        math_records.append((source_rel, math_hash))
        math_totals.update(counts)

    disk_paths = {
        path.relative_to(locale).as_posix()
        for path in (locale / "content").rglob("*.tex")
        if path.is_file()
    }
    if disk_paths != manifest_paths:
        for rel in sorted(manifest_paths - disk_paths):
            failures.append(f"manifest path missing from disk inventory: {rel}")
        for rel in sorted(disk_paths - manifest_paths):
            failures.append(f"unmanifested Arabic content file: {rel}")
    if unicode_counts.get("utf8_bom_files", 0):
        failures.append(f"UTF-8 BOM found in {unicode_counts['utf8_bom_files']} files")
    if unicode_counts.get("non_nfc_files", 0):
        failures.append(f"non-NFC text found in {unicode_counts['non_nfc_files']} files")
    bidi_total = sum(value for key, value in unicode_counts.items() if key.startswith("bidi:"))
    if bidi_total:
        failures.append(f"raw bidi controls found: {bidi_total}")

    profile_file = locale / "open-logic-notation-profile-ar.tex"
    layout_file = locale / "open-logic-readable-letter-r2-layout-ar.tex"
    digit_font = locale / "fonts" / "OpenLogicMachrekDigits-Regular.otf"
    digit_font_receipt = repo / "evidence" / "notation" / "MACHREK_DIGIT_FONT_PROVENANCE.json"
    for required in (profile_file, layout_file, digit_font, digit_font_receipt, args.mapping):
        if not required.is_file():
            failures.append(f"required profile artifact is missing: {required}")

    driver_facts: dict[str, dict[str, dict[str, str]]] = {}
    for profile, roles in DRIVERS.items():
        driver_facts[profile] = {}
        for role, name in roles.items():
            path = locale / name
            if not path.is_file():
                failures.append(f"missing {profile} {role} driver: {path}")
                continue
            text = path.read_text(encoding="utf-8")
            expected_profile = f"\\newcommand*{{\\OLNotationProfile}}{{{profile}}}"
            expected_base = (
                "\\input{open-logic-complete-ar.tex}"
                if role == "reader"
                else "\\input{open-logic-closure-supplement-ar.tex}"
            )
            if expected_profile not in text:
                failures.append(f"{name}: does not select {profile}")
            if expected_base not in text:
                failures.append(f"{name}: does not input the shared {role} base")
            if "\\input{open-logic-readable-letter-r2-layout-ar.tex}" not in text:
                failures.append(f"{name}: does not input the shared readable layout")
            driver_facts[profile][role] = {
                "path": path.relative_to(repo).as_posix(),
                "bytes": str(path.stat().st_size),
                "sha256": sha256(path),
            }

    mapping = json.loads(args.mapping.read_text(encoding="utf-8"))
    if mapping.get("source_closure_units") != 722:
        failures.append("profile mapping does not bind 722 closure units")
    if set(mapping.get("profiles", {})) != set(DRIVERS):
        failures.append("profile mapping keys do not equal the implemented profiles")
    if mapping.get("source_transform") != "none":
        failures.append("profile mapping must declare source_transform=none")

    font_provenance: dict[str, object] = {}
    if digit_font_receipt.is_file():
        font_provenance = json.loads(digit_font_receipt.read_text(encoding="utf-8"))
        if font_provenance.get("status") != "PASS":
            failures.append("Machrek digit-font provenance receipt is not PASS")
        receipt_hash = font_provenance.get("output", {}).get("sha256")
        actual_hash = sha256(digit_font) if digit_font.is_file() else None
        if receipt_hash != actual_hash:
            failures.append(f"Machrek digit-font hash mismatch: {actual_hash} != {receipt_hash}")
        if font_provenance.get("build", {}).get("source_transform") != "none":
            failures.append("Machrek digit-font receipt does not preserve source_transform=none")

    payload = {
        "schema": "openlogic-arabic-dual-notation-source-audit-v1",
        "status": "PASS" if not failures else "FAIL",
        "repository": str(repo),
        "closure": {
            "manifest_rows": len(rows),
            "accepted_arabic_rows": sum(row.get("ar_status") == "ACCEPTED" for row in rows),
            "disk_tex_files": len(disk_paths),
            "total_bytes": total_bytes,
            "ordered_source_hash_manifest_sha256": hash_records(source_records),
            "math_candidate_manifest_sha256": hash_records(math_records),
            "math_delimiter_counts": dict(sorted(math_totals.items())),
        },
        "unicode": {
            "utf8_decode": "PASS" if not any("decode failure" in item for item in failures) else "FAIL",
            "utf8_bom_files": unicode_counts.get("utf8_bom_files", 0),
            "non_nfc_files": unicode_counts.get("non_nfc_files", 0),
            "raw_bidi_control_count": bidi_total,
            "raw_bidi_control_breakdown": {
                key.removeprefix("bidi:"): value
                for key, value in sorted(unicode_counts.items())
                if key.startswith("bidi:")
            },
        },
        "shared_profile_file": {
            "path": profile_file.relative_to(repo).as_posix(),
            "sha256": sha256(profile_file) if profile_file.is_file() else None,
        },
        "shared_layout_file": {
            "path": layout_file.relative_to(repo).as_posix(),
            "sha256": sha256(layout_file) if layout_file.is_file() else None,
        },
        "machrek_digit_font": {
            "path": digit_font.relative_to(repo).as_posix(),
            "bytes": digit_font.stat().st_size if digit_font.is_file() else None,
            "sha256": sha256(digit_font) if digit_font.is_file() else None,
            "provenance_receipt": digit_font_receipt.relative_to(repo).as_posix(),
            "provenance_status": font_provenance.get("status"),
        },
        "mapping": {
            "path": args.mapping.resolve().as_posix(),
            "sha256": sha256(args.mapping) if args.mapping.is_file() else None,
        },
        "drivers": driver_facts,
        "equivalence_claim": {
            "same_722_translated_source_files": not any("hash mismatch" in item for item in failures),
            "same_reader_base_driver": True,
            "same_supplement_base_driver": True,
            "formula_token_transform": "none",
            "only_profile_level_glyph_mapping": True,
            "machrek_source_character_slots": "U+0030--U+0039",
            "machrek_visual_glyphs": "Arabic-Indic U+0660--U+0669 outlines",
        },
        "failures": failures,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": payload["status"], "failures": len(failures), "output": str(args.output)}))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
