#!/usr/bin/env python3
"""Package the Arabic reviewer-facing Markdown with exact editable inputs."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "expert-review/2026-09-26-final-page-review"
SHARDS = REVIEW / "arabic-existing"
ARCHIVE = REVIEW / "REVIEW_WORKING_EDITABLE_SOURCES.zip"
RECEIPT = REVIEW / "WORKING_SOURCE_ARCHIVE_RECEIPT.json"
INDEX_GZ = REVIEW / "EXPERT_REVIEW_INDEX.json.gz"
SOURCE_BASE = [
    "expert-review/2026-09-26-final-page-review/START_HERE_AR.md",
    "expert-review/2026-09-26-final-page-review/WORKING_INDEX_AR.md",
    "expert-review/2026-09-26-final-page-review/BATCH_31_38_AR.md",
    "expert-review/2026-09-26-final-page-review/BATCH_31_38_READBACK.json",
    "expert-review/2026-09-26-final-page-review/README_BUILD_AR.md",
    "expert-review/2026-09-26-final-page-review/EXPERT_REVIEW_INDEX.json.gz",
    "expert-review/2026-09-26-final-page-review/arabic-existing/README.md",
    "expert-review/2026-09-26-final-page-review/arabic-existing/BUILD_RECEIPT.json",
    "expert-review/2026-09-26-final-page-review/arabic-existing/INDEPENDENT_READBACK.json",
    "evidence/classical/terminology/ARABIC_PRIORITY_30_20260926.json",
    "evidence/classical/terminology/PRIORITY_MANUAL_POTENT_LOCATOR_20260926.json",
    "evidence/classical/terminology/ARABIC_REVIEW_BATCH_31_38_20260927.json",
    "evidence/classical/terminology/CANON_TRANSCRIPTION_ERRATUM_20260927.json",
    "evidence/publication/source-line-mirror-20260926/READBACK.json",
    "tmp/expert-index-final-pages-20260926-r1/INDEPENDENT_READBACK.json",
    "build/render_arabic_priority_guide_20260926.py",
    "build/verify_arabic_priority_guide_20260926.py",
    "build/render_arabic_review_batch_20260927.py",
    "build/verify_arabic_review_batch_20260927.py",
    "build/render_arabic_review_existing_20260927.py",
    "build/verify_arabic_review_existing_20260927.py",
    "build/package_arabic_review_working_20260927.py",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main() -> None:
    priority = json.loads((REVIEW / "READBACK.json").read_text(encoding="utf-8"))
    batch = json.loads((REVIEW / "BATCH_31_38_READBACK.json").read_text(encoding="utf-8"))
    existing = json.loads((SHARDS / "INDEPENDENT_READBACK.json").read_text(encoding="utf-8"))
    build = json.loads((SHARDS / "BUILD_RECEIPT.json").read_text(encoding="utf-8"))
    if priority["status"] != "PASS_30_ARABIC_DECISIONS_AND_PUBLIC_LINKS":
        raise ValueError("Priority guide verification is not accepted")
    if batch["status"] != "PASS_LOCAL_ARABIC_BATCH_31_38" or sha256(REVIEW / "BATCH_31_38_AR.md") != batch["markdown_sha256"]:
        raise ValueError("Eight-choice review batch is not accepted")
    if existing["status"] != "PASS_INDEPENDENT_EXISTING_ARABIC_VIEW" or existing["readme_sha256"] != build["readme"]["sha256"]:
        raise ValueError("Existing-Arabic reviewer shards are not accepted")
    if sha256(INDEX_GZ) != "801B538584BE34ECD21856C05AB264127BA10159049C69B643E45FD4342CDD74":
        raise ValueError("The compressed raw index changed")
    shard_paths = [item["path"] for item in build["shards"]]
    if len(shard_paths) != 11:
        raise ValueError("Expected eleven checked, reader-sized shards")
    members = SOURCE_BASE + shard_paths
    if len(members) != len(set(members)):
        raise ValueError("Repeated archive member")
    for relative in members:
        if not (ROOT / relative).is_file():
            raise FileNotFoundError(relative)
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, allowZip64=True) as archive:
        for relative in members:
            path = ROOT / relative
            info = zipfile.ZipInfo(relative, date_time=(2026, 9, 27, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with path.open("rb") as source, archive.open(info, "w", force_zip64=True) as target:
                shutil.copyfileobj(source, target, 1024 * 1024)
    with zipfile.ZipFile(ARCHIVE) as archive:
        if archive.namelist() != members:
            raise ValueError("Archive member order differs")
        for relative in members:
            content = archive.read(relative)
            if hashlib.sha256(content).hexdigest().upper() != sha256(ROOT / relative):
                raise ValueError(f"Archive member bytes differ: {relative}")
    manifest = {
        "status": "PASS_REPRODUCIBLE_ARABIC_REVIEW_SOURCE_ARCHIVE",
        "archive_path": str(ARCHIVE.relative_to(ROOT)).replace("\\", "/"),
        "archive_bytes": ARCHIVE.stat().st_size,
        "archive_sha256": sha256(ARCHIVE),
        "member_count": len(members),
        "members": [{"path": relative, "bytes": (ROOT / relative).stat().st_size, "sha256": sha256(ROOT / relative)} for relative in members],
        "reader_note_ar": "تضم الحزمة المصادر القابلة للتحرير والبيانات المضغوطة وبرامج إعادة إنتاج دليل الأولوية والبطاقات العربية المرحلية؛ لا تحل محل ملفات LaTeX المباشرة للطبعات.",
    }
    RECEIPT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": manifest["status"], "archive_bytes": manifest["archive_bytes"], "archive_sha256": manifest["archive_sha256"], "member_count": len(members)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
