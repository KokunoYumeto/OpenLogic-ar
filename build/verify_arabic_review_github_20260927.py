#!/usr/bin/env python3
"""Anonymously byte-verify the narrowly published Arabic review files."""

from __future__ import annotations

import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMIT = "32298b975874cafd7bb5dba135ef687ed8886ff5"
PARENT = "085d1b8a93bd91377a8994d7e23bb480b29bd969"
OUT = ROOT / "evidence/publication/review-working-20260927/GITHUB_READBACK.json"
PREFIX = f"https://raw.githubusercontent.com/KokunoYumeto/OpenLogic-ar/{COMMIT}/"


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest().upper()


def get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "OpenLogic-Ar-public-byte-readback/1.0"})
    with urllib.request.urlopen(request, timeout=75) as response:
        if response.status != 200:
            raise ValueError(f"Anonymous fetch returned {response.status}: {url}")
        return response.read()


def main() -> None:
    names = subprocess.check_output(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", COMMIT],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    ).splitlines()
    if len(names) != 27 or len(set(names)) != 27:
        raise ValueError(f"Unexpected public commit file list: {len(names)}")
    parent = subprocess.check_output(["git", "rev-parse", f"{COMMIT}^"], cwd=ROOT, text=True).strip()
    if parent != PARENT:
        raise ValueError("Public review commit has another parent")
    files = []
    for name in names:
        local = ROOT / name
        if not local.is_file():
            raise FileNotFoundError(name)
        expected = local.read_bytes()
        got = get(PREFIX + name)
        if len(got) != len(expected) or digest(got) != digest(expected):
            raise ValueError(f"Public file bytes differ: {name}")
        files.append({"path": name, "bytes": len(got), "sha256": digest(got)})
    html = get(
        f"https://github.com/KokunoYumeto/OpenLogic-ar/blob/{COMMIT}/"
        "expert-review/2026-09-26-final-page-review/WORKING_INDEX_AR.md"
    )
    if not html or b"WORKING_INDEX_AR.md" not in html:
        raise ValueError("Human-readable GitHub entry page is not anonymously browsable")
    result = {
        "status": "PASS_ANONYMOUS_GITHUB_27_EXACT_FILES",
        "commit": COMMIT,
        "parent": PARENT,
        "file_count": len(files),
        "files": files,
        "human_entry_url": (
            f"https://github.com/KokunoYumeto/OpenLogic-ar/blob/{COMMIT}/"
            "expert-review/2026-09-26-final-page-review/WORKING_INDEX_AR.md"
        ),
        "html_response_bytes": len(html),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": result["status"], "commit": COMMIT, "files": len(files), "html_bytes": len(html)}))


if __name__ == "__main__":
    main()
