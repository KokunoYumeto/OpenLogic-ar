#!/usr/bin/env python3
"""Deterministically stage the Arabic reviewer guide and complete raw register."""

from __future__ import annotations

import gzip
import hashlib
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "expert-review/2026-09-26-final-page-review"
STAGE = ROOT / "output/expert-review/priority-20260927"
INDEX = ROOT / "tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json"
INDEX_SHA256 = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"
GZ = REVIEW / "EXPERT_REVIEW_INDEX.json.gz"
SOURCE_ZIP = REVIEW / "REVIEW_GUIDE_EDITABLE_SOURCES.zip"
ASSET_NAMES = (
    "00-REVIEW-01_START_HERE_AR.md",
    "00-REVIEW-02_EXPERT_REVIEW_INDEX.json.gz",
    "00-REVIEW-03_EDITABLE_SOURCES.zip",
    "00-REVIEW-04_SHA256SUMS.txt",
)
SOURCE_MEMBERS = (
    "expert-review/2026-09-26-final-page-review/START_HERE_AR.md",
    "expert-review/2026-09-26-final-page-review/README_BUILD_AR.md",
    "expert-review/2026-09-26-final-page-review/READBACK.json",
    "expert-review/2026-09-26-final-page-review/EXPERT_REVIEW_INDEX.json.gz",
    "evidence/classical/terminology/ARABIC_PRIORITY_30_20260926.json",
    "evidence/classical/terminology/PRIORITY_MANUAL_POTENT_LOCATOR_20260926.json",
    "evidence/publication/source-line-mirror-20260926/READBACK.json",
    "tmp/expert-index-final-pages-20260926-r1/INDEPENDENT_READBACK.json",
    "build/render_arabic_priority_guide_20260926.py",
    "build/verify_arabic_priority_guide_20260926.py",
    "build/package_arabic_priority_review_20260927.py",
)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def gzip_index() -> None:
    if sha(INDEX) != INDEX_SHA256:
        raise ValueError("Final-page index no longer matches independent readback")
    if not GZ.exists():
        with INDEX.open("rb") as source, GZ.open("wb") as destination:
            with gzip.GzipFile(fileobj=destination, mode="wb", filename="", mtime=0, compresslevel=9) as zipped:
                shutil.copyfileobj(source, zipped, 1024 * 1024)
    h = hashlib.sha256()
    count = 0
    with gzip.open(GZ, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
            count += len(block)
    if h.hexdigest().upper() != INDEX_SHA256 or count != INDEX.stat().st_size:
        raise ValueError("Compressed full review index does not round-trip exactly")


def source_archive() -> None:
    with zipfile.ZipFile(SOURCE_ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, allowZip64=True) as archive:
        for relative in SOURCE_MEMBERS:
            path = ROOT / relative
            if not path.is_file():
                raise FileNotFoundError(relative)
            info = zipfile.ZipInfo(relative, date_time=(2026, 9, 27, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with path.open("rb") as source, archive.open(info, "w", force_zip64=True) as target:
                shutil.copyfileobj(source, target, 1024 * 1024)
    with zipfile.ZipFile(SOURCE_ZIP) as archive:
        if archive.namelist() != list(SOURCE_MEMBERS):
            raise ValueError("Source archive inventory/order differs")
        for relative in SOURCE_MEMBERS:
            if hashlib.sha256(archive.read(relative)).digest() != bytes.fromhex(sha(ROOT / relative)):
                raise ValueError(f"Source archive byte mismatch: {relative}")


def stage() -> None:
    receipt = json.loads((REVIEW / "READBACK.json").read_text(encoding="utf-8"))
    if receipt.get("status") != "PASS_30_ARABIC_DECISIONS_AND_PUBLIC_LINKS":
        raise ValueError("Priority guide independent check has not passed")
    if receipt["guide_sha256"] != sha(REVIEW / "START_HERE_AR.md"):
        raise ValueError("Priority guide changed after readback")
    gzip_index()
    source_archive()
    STAGE.mkdir(parents=True, exist_ok=True)
    sources = (REVIEW / "START_HERE_AR.md", GZ, SOURCE_ZIP)
    for name, source in zip(ASSET_NAMES[:3], sources, strict=True):
        target = STAGE / name
        shutil.copyfile(source, target)
        if sha(target) != sha(source):
            raise ValueError(f"Staged public asset changed: {name}")
    checksums = "".join(f"{sha(STAGE / name).lower()}  {name}\n" for name in ASSET_NAMES[:3])
    (STAGE / ASSET_NAMES[3]).write_text(checksums, encoding="ascii", newline="\n")
    manifest = {
        "schema": "openlogic-arabic-priority-review-stage-v1",
        "status": "PASS_LOCAL_STAGE",
        "scope": "ثلاثون قرارًا عربيًا ذا أولوية، والسجل الكامل للبيانات فقط؛ تعريب جميع التعليلات لم يكتمل بعد",
        "full_review_index_sha256": INDEX_SHA256,
        "source_members": list(SOURCE_MEMBERS),
        "files": [
            {"name": name, "bytes": (STAGE / name).stat().st_size, "sha256": sha(STAGE / name)}
            for name in ASSET_NAMES
        ],
    }
    (STAGE / "LOCAL_STAGE.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": manifest["status"], "files": manifest["files"]}, ensure_ascii=False))


if __name__ == "__main__":
    stage()
