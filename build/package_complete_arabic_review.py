#!/usr/bin/env python3
"""Package the editable complete Arabic review, its data and verification code."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "expert-review/2026-09-26-final-page-review"
TERM = ROOT / "evidence/classical/terminology"
ZIP = BASE / "90-ARABIC-REVIEW-COMPLETE-SOURCE.zip"
RECEIPT = BASE / "COMPLETE_SOURCE_PACKAGE_RECEIPT.json"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def include_files() -> list[Path]:
    top = [
        "INDEX_AR.md", "DIRECTORY_AR.md", "DECISION_RECORD_AR.jsonl.gz",
        "COMPLETE_DIRECTORY_RECEIPT.json", "COMPLETE_INDEPENDENT_READBACK.json",
        "PUBLICATION_STATUS_READBACK.json", "README_BUILD_AR.md",
        "WORKING_INDEX_AR.md", "START_HERE_AR.md", "READBACK.json",
        "BATCH_31_38_AR.md", "BATCH_31_38_READBACK.json",
        "EXPERT_REVIEW_INDEX.json.gz",
        "SOL6_CORRECTIONS_AR.md", "COMPLETE_INDEPENDENT_READBACK_20260930.json",
        "SOL6_SOURCE_REFERENCES_AR.md", "SOURCE_WITNESS_PUBLIC_READBACK_20260930.json",
        "COMPLETE_INDEPENDENT_READBACK_20260930_R3.json",
        "COMPLETE_DIRECTORY_RECEIPT_20260927_HISTORICAL.json",
    ]
    files = [BASE / name for name in top]
    for directory in BASE.iterdir():
        if directory.is_dir() and (directory.name.startswith("arabic-")
                                   or directory.name in {"global-caption-decisions", "reexamination-source"}):
            files.extend(path for path in directory.rglob("*") if path.is_file())
    for path in TERM.iterdir():
        if path.is_file() and path.name.endswith("_20260927.json") and (
            path.name.startswith("ARABIC_") or path.name.startswith("DAM_")
            or path.name.startswith("REVIEW_NOTES_")
            or path.name.startswith("GLOBAL_CAPTION_")
            or path.name.startswith("CANON_TRANSCRIPTION_")
            or path.name.startswith("ENGLISH_LOCATOR_")
        ):
            files.append(path)
    files.append(TERM / "ARABIC_PRIORITY_30_20260926.json")
    files.append(TERM / "PRIORITY_MANUAL_POTENT_LOCATOR_20260926.json")
    files.append(TERM / "SOL6_REEXAMINATION_CORRECTIONS_20260930.json")
    files.append(TERM / "SOL6_SOURCE_WITNESS_CORRECTIONS_20260930.json")
    files.append(TERM / "SOL6_COMMENT_ONLY_WITNESS_CENSUS_20260930.json")
    files.append(ROOT / "LICENSE.md")
    build = ROOT / "build"
    for path in build.glob("*.py"):
        if (path.name.startswith(("render_arabic_", "verify_arabic_"))
                or path.name in {
                    "assemble_complete_arabic_review.py",
                    "verify_complete_arabic_review.py",
                    "finalize_arabic_review_status.py",
                    "render_global_caption_review.py",
                    "verify_global_caption_review.py",
                    "stream_expert_review_decisions.py",
                    "package_complete_arabic_review.py",
                    "render_sol6_review_corrections_20260930.py",
                    "correct_added_source_witnesses_20260930.py",
                    "replay_corrected_review_20260930.py",
                }):
            files.append(path)
    assert len(files) == len(set(files))
    assert all(path.is_file() for path in files)
    return sorted(files, key=lambda path: path.relative_to(ROOT).as_posix())


def info(name: str) -> zipfile.ZipInfo:
    item = zipfile.ZipInfo(name, (2026, 9, 27, 0, 0, 0))
    item.compress_type = zipfile.ZIP_DEFLATED
    item.external_attr = 0o644 << 16
    item.create_system = 3
    return item


def main() -> None:
    files = include_files()
    manifest = {
        "title_ar": "مصادر فهرس مراجعة الترجمة العربية الكامل",
        "reviewable_decisions": 1095,
        "instructions": "expert-review/2026-09-26-final-page-review/README_BUILD_AR.md",
        "files": [{"path": path.relative_to(ROOT).as_posix(),
                   "bytes": path.stat().st_size, "sha256": sha(path)} for path in files],
    }
    payload = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with zipfile.ZipFile(ZIP, "w", allowZip64=True) as archive:
        archive.writestr(info("SOURCE_MANIFEST_AR.json"), payload)
        for path in files:
            archive.writestr(info(path.relative_to(ROOT).as_posix()), path.read_bytes())
    with zipfile.ZipFile(ZIP, "r") as archive:
        assert archive.testzip() is None
        archived = json.loads(archive.read("SOURCE_MANIFEST_AR.json"))
        assert archived == manifest
        for file in manifest["files"]:
            data = archive.read(file["path"])
            assert len(data) == file["bytes"]
            assert hashlib.sha256(data).hexdigest().upper() == file["sha256"]
    receipt = {"status": "PASS_COMPLETE_EDITABLE_SOURCE_PACKAGE",
               "zip": ZIP.name, "bytes": ZIP.stat().st_size,
               "sha256": sha(ZIP), "file_count": len(files) + 1,
               "reviewable_decisions": 1095}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8", newline="\n")
    print(json.dumps(receipt, ensure_ascii=True))


if __name__ == "__main__":
    main()
