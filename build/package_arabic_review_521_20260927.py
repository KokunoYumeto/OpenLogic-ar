#!/usr/bin/env python3
"""Seal the 521-choice Arabic review surface with exact editable inputs."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "expert-review/2026-09-26-final-page-review"
TERM = ROOT / "evidence/classical/terminology"
PRIOR = REVIEW / "REVIEW_359_SOURCE_RECEIPT.json"
ARCHIVE = REVIEW / "REVIEW_521_EDITABLE_SOURCES.zip"
RECEIPT = REVIEW / "REVIEW_521_SOURCE_RECEIPT.json"
INDEX_SHA = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"
RANGES = (
    (93, 112), (113, 132), (133, 145), (146, 162), (163, 188),
    (189, 210), (211, 220), (221, 230), (231, 237), (238, 254),
)
SUPPORT = (
    "build/render_arabic_review_batch.py",
    "build/verify_arabic_review_batch.py",
    "build/stream_expert_review_decisions.py",
    "build/index_damascus_canon.py",
    "build/package_arabic_review_521_20260927.py",
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> None:
    prior = json.loads(PRIOR.read_text(encoding="utf-8"))
    if prior["status"] != "PASS_LOCAL_ARABIC_REVIEW_359_EDITABLE_SOURCE_ARCHIVE" or prior["coverage"] != {
        "arabic_choices": 359, "all_choices": 1095, "remaining": 736,
    }:
        raise ValueError("Prior 359-choice source package is not pinned")
    changed_prior = {
        "expert-review/2026-09-26-final-page-review/WORKING_INDEX_AR.md",
        "expert-review/2026-09-26-final-page-review/README_BUILD_AR.md",
    }
    members = [item["path"] for item in prior["members"]]
    for item in prior["members"]:
        path = ROOT / item["path"]
        if not path.is_file():
            raise FileNotFoundError(path)
        if item["path"] not in changed_prior and (path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]):
            raise ValueError("Inherited source differs: " + item["path"])
    if digest(ROOT / "tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json") != INDEX_SHA:
        raise ValueError("Frozen 1,095-choice index changed")

    batch_receipts = []
    new_ids = []
    additions = []
    for first, last in RANGES:
        name = f"ARABIC_REVIEW_BATCH_{first}_{last}_20260927.json"
        overlay_path = TERM / name
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        ids = [row["decision_id"] for row in overlay["records"]]
        if len(ids) != last - first + 1 or len(ids) != len(set(ids)):
            raise ValueError("Batch decision inventory differs: " + name)
        new_ids.extend(ids)
        directory = REVIEW / f"arabic-decisions-{first}-{last}"
        readback_path = directory / "INDEPENDENT_READBACK.json"
        readback = json.loads(readback_path.read_text(encoding="utf-8"))
        valid_status = (
            "PASS_INDEPENDENT_ARABIC_REVIEW_BATCH_READBACK",
            f"PASS_INDEPENDENT_ARABIC_CHOICE_BATCH_{first}_{last}_READBACK",
        )
        if readback["status"] not in valid_status or readback["choice_count"] != len(ids) or readback["overlay_sha256"] != digest(overlay_path):
            raise ValueError("Independent batch readback missing or stale: " + name)
        if readback["source_index_sha256"] != INDEX_SHA or readback["counts"]["resolved"] != readback["counts"]["locations"]:
            raise ValueError("Unbound source location or index drift: " + name)
        additions.append(relative(overlay_path))
        for file in sorted(directory.iterdir()):
            if file.is_file() and file.suffix in (".md", ".json"):
                additions.append(relative(file))
        canon = overlay["canon"]
        for key, value in canon.items():
            if key.endswith("_path") and isinstance(value, str) and value.endswith(".json"):
                additions.append(value)
        batch_receipts.append({
            "range": [first, last], "choices": len(ids),
            "overlay_sha256": digest(overlay_path),
            "readback_sha256": digest(readback_path),
            "locations": readback["counts"]["locations"],
        })
    if len(new_ids) != 162 or len(set(new_ids)) != 162:
        raise ValueError("The 162 new choices overlap")
    for value in SUPPORT:
        additions.append(value)
    for name in additions:
        if name not in members:
            members.append(name)
    if len(members) != len(set(members)) or any(not (ROOT / name).is_file() for name in members):
        raise ValueError("Missing or repeated package member")
    index = (REVIEW / "WORKING_INDEX_AR.md").read_text(encoding="utf-8")
    if "٥٢١ قرارًا من أصل ١٠٩٥" not in index or "٥٧٤ قرارًا" not in index:
        raise ValueError("Arabic navigation coverage does not match package")
    for first, last in RANGES:
        if f"arabic-decisions-{first}-{last}/README.md" not in index:
            raise ValueError("Arabic navigation misses a new batch")

    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, allowZip64=True) as archive:
        for name in members:
            path = ROOT / name
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 27, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with path.open("rb") as source, archive.open(info, "w", force_zip64=True) as target:
                shutil.copyfileobj(source, target, 1024 * 1024)
    with zipfile.ZipFile(ARCHIVE) as archive:
        if archive.namelist() != members:
            raise ValueError("Archive member order changed")
        for name in members:
            if hashlib.sha256(archive.read(name)).hexdigest().upper() != digest(ROOT / name):
                raise ValueError("Archive member differs from exact source: " + name)
    receipt = {
        "status": "PASS_LOCAL_ARABIC_REVIEW_521_EDITABLE_SOURCE_ARCHIVE",
        "source_index_sha256": INDEX_SHA,
        "coverage": {"arabic_choices": 521, "all_choices": 1095, "remaining": 574},
        "batch_readbacks": batch_receipts,
        "archive_path": relative(ARCHIVE),
        "archive_bytes": ARCHIVE.stat().st_size,
        "archive_sha256": digest(ARCHIVE),
        "member_count": len(members),
        "members": [
            {"path": name, "bytes": (ROOT / name).stat().st_size, "sha256": digest(ROOT / name)}
            for name in members
        ],
        "canon_pdf_note_ar": "صورة معجم مجمع دمشق شاهد خارجي موثق بالرابط والتجزئة في البطاقات؛ لا تضمها حزمة المصدر القابلة للتحرير.",
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": receipt["status"], "choices": 521,
                      "members": len(members), "archive_bytes": receipt["archive_bytes"],
                      "archive_sha256": receipt["archive_sha256"]}, ensure_ascii=True))


if __name__ == "__main__":
    main()
