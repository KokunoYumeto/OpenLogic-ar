#!/usr/bin/env python3
"""Create and verify the deterministic OLP-0722 source/evidence release bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath


ARCHIVE_ROOT = "OpenLogic-ar-OLP-0722-complete-dual-notation"
FIXED_ZIP_TIME = (2026, 9, 3, 0, 0, 0)

ROOT_FILES = (
    ".zenodo.json",
    "CITATION.cff",
    "LICENSE.md",
    "README.md",
    "RELEASE_NOTES_COMPLETE_DUAL_NOTATION.md",
)

TREE_ROOTS = (
    "00_control",
    "source",
    "evidence/canon",
    "evidence/notation",
    "evidence/provenance/openlogic-control",
)

EXACT_FILES = (
    "evidence/DEPENDENCY_CLOSURE_SUMMARY.json",
    "build/BUILD_COMPLETE_DUAL_NOTATION_REQUIREMENTS.md",
    "build/BUILD_DUAL_NOTATION.ps1",
    "build/BUILD_DUAL_NOTATION_INNER.ps1",
    "build/Invoke-WithInterlanguageTeXMutex.ps1",
    "build/assemble_complete_722_reader.py",
    "build/audit_arabic_notation_profiles.py",
    "build/index_damascus_canon.py",
    "build/make_machrek_digit_font.py",
    "build/package_complete_dual_notation_release.py",
    "build/qa_dual_notation_pdfs.py",
    "build/repair_rtl_link_rects_letter_ar.py",
    "output/pdf/complete-722-v1/00_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_INTERNATIONAL_NOTATION_OLP-0722.assembly.json",
    "output/pdf/complete-722-v1/01_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_MACHREK_NOTATION_OLP-0722.assembly.json",
    "output/pdf/complete-722-v1/OPENLOGIC_ar_COMPLETE_722_DUAL_NOTATION_QA.json",
    "output/pdf/dual-notation-v4/VISUAL_QA.json",
    "output/pdf/dual-notation-v5-replay/BUILD_ARTIFACTS.json",
    "output/pdf/dual-notation-v5-replay/BUILD_CONVERGENCE.json",
    "output/pdf/dual-notation-v5-replay/OPENLOGIC_ar_DUAL_NOTATION_PDF_QA.json",
)

TEXT_SUFFIXES = {
    ".bib",
    ".bst",
    ".cff",
    ".csv",
    ".html",
    ".json",
    ".jsonl",
    ".md",
    ".ps1",
    ".py",
    ".sty",
    ".tex",
    ".tsv",
    ".txt",
    ".xml",
}

FORBIDDEN_PUBLIC_PATTERNS = (
    re.compile(rb"[A-Za-z]:\\Users\\", re.IGNORECASE),
    re.compile(rb"github_pat_[A-Za-z0-9_]+"),
    re.compile(rb"ghp_[A-Za-z0-9]+"),
    re.compile(rb"(?:access_token|authorization)\s*[:=]", re.IGNORECASE),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def collect_files(repo: Path) -> list[Path]:
    relative_paths: set[Path] = set()
    for relative in ROOT_FILES + EXACT_FILES:
        path = repo / relative
        if not path.is_file():
            raise FileNotFoundError(f"required bundle file is missing: {relative}")
        relative_paths.add(Path(relative))
    for relative in TREE_ROOTS:
        root = repo / relative
        if not root.is_dir():
            raise FileNotFoundError(f"required bundle tree is missing: {relative}")
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(repo)
            if "__pycache__" in rel.parts or path.suffix.lower() == ".pyc":
                continue
            relative_paths.add(rel)
    return sorted(relative_paths, key=lambda path: path.as_posix())


def scan_public_bytes(repo: Path, files: list[Path]) -> None:
    failures: list[str] = []
    for relative in files:
        if relative.suffix.lower() not in TEXT_SUFFIXES:
            continue
        data = (repo / relative).read_bytes()
        for pattern in FORBIDDEN_PUBLIC_PATTERNS:
            if pattern.search(data):
                failures.append(relative.as_posix())
                break
    if failures:
        raise ValueError(
            "forbidden local-path or credential-like text in public bundle: "
            + ", ".join(failures)
        )


def zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    return info


def write_zip(repo: Path, files: list[Path], output: Path) -> None:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite release ZIP: {output}")
    temporary = output.with_suffix(output.suffix + ".tmp")
    if temporary.exists():
        raise FileExistsError(f"refusing to overwrite temporary ZIP: {temporary}")
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(
            temporary,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
            strict_timestamps=True,
        ) as archive:
            for relative in files:
                archive_name = f"{ARCHIVE_ROOT}/{relative.as_posix()}"
                archive.writestr(zip_info(archive_name), (repo / relative).read_bytes())
        temporary.replace(output)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def verify_zip(output: Path, expected_files: list[Path]) -> dict[str, int | bool]:
    with zipfile.ZipFile(output, "r") as archive:
        names = archive.namelist()
        bad_crc = archive.testzip()
        if bad_crc is not None:
            raise ValueError(f"ZIP CRC failure: {bad_crc}")
        if len(names) != len(set(names)):
            raise ValueError("ZIP contains duplicate member names")
        expected_names = [
            f"{ARCHIVE_ROOT}/{relative.as_posix()}" for relative in expected_files
        ]
        if names != expected_names:
            raise ValueError("ZIP member inventory/order differs from source selection")
        for name in names:
            pure = PurePosixPath(name)
            if pure.is_absolute() or ".." in pure.parts or "\\" in name:
                raise ValueError(f"unsafe ZIP member path: {name}")
        content_prefix = f"{ARCHIVE_ROOT}/source/locale/ar/content/"
        translated_tex = sum(
            1
            for name in names
            if name.startswith(content_prefix) and name.endswith(".tex")
        )
        if translated_tex != 722:
            raise ValueError(
                f"ZIP contains {translated_tex} translated content files, expected 722"
            )
    return {
        "members": len(expected_files),
        "translated_content_tex_files": translated_tex,
        "crc_test_passed": True,
        "safe_relative_paths": True,
        "member_order_deterministic": True,
    }


def write_manifest(paths: list[Path], manifest: Path) -> None:
    if manifest.exists():
        raise FileExistsError(f"refusing to overwrite release manifest: {manifest}")
    lines = ["# SHA-256  bytes  filename"]
    for path in paths:
        lines.append(f"{sha256(path)}  {path.stat().st_size}  {path.name}")
    manifest.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--international-pdf", type=Path, required=True)
    parser.add_argument("--machrek-pdf", type=Path, required=True)
    parser.add_argument("--zip", dest="zip_path", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    if args.receipt.exists():
        raise FileExistsError(f"refusing to overwrite packaging receipt: {args.receipt}")
    for pdf in (args.international_pdf, args.machrek_pdf):
        if not pdf.is_file() or pdf.stat().st_size <= 0:
            raise FileNotFoundError(f"required final PDF is missing or empty: {pdf}")

    files = collect_files(repo)
    scan_public_bytes(repo, files)
    write_zip(repo, files, args.zip_path)
    verification = verify_zip(args.zip_path, files)
    write_manifest(
        [args.international_pdf, args.machrek_pdf, args.zip_path], args.manifest
    )

    assets = []
    for path in (
        args.international_pdf,
        args.machrek_pdf,
        args.zip_path,
        args.manifest,
    ):
        assets.append(
            {
                "file": path.name,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    payload = {
        "schema": "openlogic-arabic-complete-dual-notation-packaging-v1",
        "status": "PASS",
        "version": "OLP-0722-COMPLETE-DUAL-NOTATION-20260903",
        "zip": verification,
        "public_text_scan": {
            "windows_user_paths": 0,
            "credential_like_patterns": 0,
        },
        "release_assets": assets,
        "failures": [],
    }
    args.receipt.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
