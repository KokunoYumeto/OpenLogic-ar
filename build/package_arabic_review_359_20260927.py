#!/usr/bin/env python3
"""Package the 359-choice Arabic review surface and its exact editable inputs."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from package_arabic_review_working_20260927 import SOURCE_BASE


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "expert-review/2026-09-26-final-page-review"
TERM = ROOT / "evidence/classical/terminology"
ARCHIVE = REVIEW / "REVIEW_359_EDITABLE_SOURCES.zip"
RECEIPT = REVIEW / "REVIEW_359_SOURCE_RECEIPT.json"
INDEX = ROOT / "tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json"
INDEX_SHA = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"
BATCHES = (
    ("arabic-senses-39-58", "ARABIC_SENSES_BATCH_39_58_20260927.json", 20),
    ("arabic-senses-59-75", "ARABIC_SENSES_BATCH_59_75_20260927.json", 17),
    ("arabic-senses-76-85", "ARABIC_SENSES_BATCH_76_85_20260927.json", 10),
    ("arabic-senses-86-92", "ARABIC_SENSES_BATCH_86_92_20260927.json", 7),
)
EXTRA_EVIDENCE = (
    "ENGLISH_LOCATOR_8_20260927.json",
    "ENGLISH_LOCATOR_12_20260927.json",
    "DAM_QUERY_REVIEW_76_85_20260927.json",
    "DAM_REVIEW_76_85_20260927.json",
    "DAM_QUERY_REVIEW_86_92_20260927.json",
    "DAM_REVIEW_86_92_20260927.json",
)
EXTRA_SCRIPTS = (
    "render_arabic_review_senses_20260927.py",
    "verify_arabic_review_senses_20260927.py",
    "render_arabic_review_senses_59_75_20260927.py",
    "verify_arabic_review_senses_59_75_20260927.py",
    "render_arabic_review_senses_76_85_20260927.py",
    "verify_arabic_review_senses_76_85_20260927.py",
    "render_arabic_review_senses_86_92_20260927.py",
    "verify_arabic_review_senses_86_92_20260927.py",
    "package_arabic_review_359_20260927.py",
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> None:
    if digest(INDEX) != INDEX_SHA:
        raise ValueError("Pinned 1,095-choice raw index drift")
    priority = json.loads((TERM / "ARABIC_PRIORITY_30_20260926.json").read_text(encoding="utf-8"))
    first = json.loads((TERM / "ARABIC_REVIEW_BATCH_31_38_20260927.json").read_text(encoding="utf-8"))
    existing = json.loads((REVIEW / "arabic-existing/BUILD_RECEIPT.json").read_text(encoding="utf-8"))
    existing_readback = json.loads((REVIEW / "arabic-existing/INDEPENDENT_READBACK.json").read_text(encoding="utf-8"))
    if existing["choice_count"] != 267 or existing_readback["status"] != "PASS_INDEPENDENT_EXISTING_ARABIC_VIEW":
        raise ValueError("Earlier 267-choice surface not verified")
    groups = [
        [item["decision_id"] for item in priority["records"]],
        [decision_id for shard in existing["shards"] for decision_id in shard["decision_ids"]],
        [item["decision_id"] for item in first["records"]],
    ]
    if tuple(map(len, groups)) != (30, 267, 8):
        raise ValueError("Earlier Arabic choice census drift")
    members = SOURCE_BASE + [item["path"] for item in existing["shards"]]
    per_batch = []
    for directory, overlay_name, expected_count in BATCHES:
        overlay_path = TERM / overlay_name
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        readback_path = REVIEW / directory / "INDEPENDENT_READBACK.json"
        readback = json.loads(readback_path.read_text(encoding="utf-8"))
        ids = [item["decision_id"] for item in overlay["records"]]
        if len(ids) != expected_count or len(set(ids)) != expected_count:
            raise ValueError(f"Choice count/uniqueness drift: {directory}")
        if readback["choice_count"] != expected_count or readback["overlay_sha256"] != digest(overlay_path):
            raise ValueError(f"Independent readback input drift: {directory}")
        if not readback["status"].startswith("PASS_INDEPENDENT_ARABIC_SENSE_BATCH"):
            raise ValueError(f"Independent readback not accepted: {directory}")
        groups.append(ids)
        members.append(rel(overlay_path))
        for path in sorted((REVIEW / directory).iterdir()):
            if path.suffix in (".md", ".json"):
                members.append(rel(path))
        per_batch.append({"directory": directory, "choices": expected_count,
                          "overlay_sha256": digest(overlay_path), "readback_sha256": digest(readback_path)})
    all_ids = [decision_id for group in groups for decision_id in group]
    if len(all_ids) != 359 or len(set(all_ids)) != 359:
        raise ValueError("Consolidated Arabic choice census overlaps or misses a batch")
    page = (REVIEW / "WORKING_INDEX_AR.md").read_text(encoding="utf-8")
    if "٣٥٩ قرارًا من أصل ١٠٩٥" not in page or "٧٣٦ قرارًا" not in page:
        raise ValueError("Arabic landing page coverage is not current")
    if any(f"({directory}/README.md)" not in page for directory, _overlay, _count in BATCHES):
        raise ValueError("Arabic landing page omits a new reader batch")
    for name in EXTRA_EVIDENCE:
        members.append(rel(TERM / name))
    for name in EXTRA_SCRIPTS:
        members.append(rel(ROOT / "build" / name))
    if len(members) != len(set(members)):
        raise ValueError("Repeated source archive member")
    for name in members:
        if not (ROOT / name).is_file():
            raise FileNotFoundError(name)
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
            raise ValueError("Archive source order drift")
        for name in members:
            if hashlib.sha256(archive.read(name)).hexdigest().upper() != digest(ROOT / name):
                raise ValueError(f"Archive member differs from local source: {name}")
    manifest = {
        "status": "PASS_LOCAL_ARABIC_REVIEW_359_EDITABLE_SOURCE_ARCHIVE",
        "source_index_sha256": INDEX_SHA,
        "coverage": {"arabic_choices": 359, "all_choices": 1095, "remaining": 736},
        "batch_readbacks": per_batch,
        "archive_path": rel(ARCHIVE),
        "archive_bytes": ARCHIVE.stat().st_size,
        "archive_sha256": digest(ARCHIVE),
        "member_count": len(members),
        "members": [{"path": name, "bytes": (ROOT / name).stat().st_size, "sha256": digest(ROOT / name)} for name in members],
        "canon_pdf_note_ar": "معجم دمشق البالغ ١٧٣ ميغابايت شاهد مصور خارجي موثق بالرابط والتجزئة في مدخلات الشروح؛ لا يدخل في حزمة مصدر البطاقات القابلة للتحرير.",
    }
    RECEIPT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": manifest["status"], "choices": len(all_ids),
                      "archive_bytes": manifest["archive_bytes"], "archive_sha256": manifest["archive_sha256"],
                      "members": len(members)}, ensure_ascii=True))


if __name__ == "__main__":
    main()
