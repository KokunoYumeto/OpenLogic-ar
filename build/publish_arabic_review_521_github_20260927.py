#!/usr/bin/env python3
"""Publish the exact 521-choice Arabic review package to the existing GitHub main."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import publish_arabic_review_359_github_20260927 as old


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "expert-review/2026-09-26-final-page-review"
PACKAGE = REVIEW / "REVIEW_521_SOURCE_RECEIPT.json"
STATE_DIR = ROOT / "evidence/publication/review-521-20260927"
old.PACKAGE = PACKAGE
old.STATE = STATE_DIR / "GITHUB_TRANSACTION.json"
old.READBACK = STATE_DIR / "GITHUB_READBACK.json"
old.EXPECTED_PARENT = "b4a870dd6320c34a7ba7eab350232657043797d5"
old.COMMIT_MESSAGE = "توسيع فهرس مراجعة الترجمة العربية إلى ٥٢١ قرارًا"
old.READBACK_STATUS = "PASS_ANONYMOUS_GITHUB_REVIEW_521_EXACT_FILES"
old.ALLOW_CHANGED = {
    "expert-review/2026-09-26-final-page-review/WORKING_INDEX_AR.md",
    "expert-review/2026-09-26-final-page-review/README_BUILD_AR.md",
    "build/publish_arabic_review_359_github_20260927.py",
    "build/index_damascus_canon.py",
}


def selected_files() -> list[str]:
    package = json.loads(PACKAGE.read_text(encoding="utf-8"))
    if package["status"] != "PASS_LOCAL_ARABIC_REVIEW_521_EDITABLE_SOURCE_ARCHIVE" or package["coverage"] != {
        "arabic_choices": 521, "all_choices": 1095, "remaining": 574,
    }:
        raise RuntimeError("521-choice editable-source package not accepted")
    archive = ROOT / package["archive_path"]
    if archive.stat().st_size != package["archive_bytes"] or old.digest(archive) != package["archive_sha256"]:
        raise RuntimeError("Exact editable-source archive changed")
    for item in package["members"]:
        path = ROOT / item["path"]
        if path.stat().st_size != item["bytes"] or old.digest(path) != item["sha256"]:
            raise RuntimeError("Packaged source changed: " + item["path"])
    paths = [item["path"] for item in package["members"]]
    paths.extend([package["archive_path"], PACKAGE.relative_to(ROOT).as_posix(),
                  "build/publish_arabic_review_521_github_20260927.py",
                  "build/publish_arabic_review_359_github_20260927.py"])
    if len(paths) != len(set(paths)):
        raise RuntimeError("Repeated selected GitHub path")
    return paths


old.selected_files = selected_files


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"prepare", "push", "verify"}:
        raise SystemExit("Usage: publish_arabic_review_521_github_20260927.py prepare|push|verify")
    {"prepare": old.prepare, "push": old.push, "verify": old.verify}[sys.argv[1]]()
