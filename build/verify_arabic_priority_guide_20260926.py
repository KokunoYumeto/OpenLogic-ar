#!/usr/bin/env python3
"""Independently verify the reviewer-facing 30-decision Arabic guide."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "expert-review/2026-09-26-final-page-review/START_HERE_AR.md"
LEDGER = ROOT / "evidence/classical/terminology/ARABIC_PRIORITY_30_20260926.json"
PUBLIC_COMMIT_ZIP = ROOT / "tmp/review-source-public-comparison-20260926/github-main-86a4a7c.zip"
OUTPUT = ROOT / "expert-review/2026-09-26-final-page-review/READBACK.json"
COMMIT = "86a4a7c11c0a0289ade28cb8f96acbacf9c01844"
INDEX_SHA256 = "FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12"
PDF_PAGES = {
    "00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf": 1145,
    "00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf": 1164,
    "03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf": 1165,
}
EAST = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    guide = GUIDE.read_text(encoding="utf-8")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if ledger["source_index_sha256"].upper() != INDEX_SHA256:
        raise ValueError("Wrong source index in Arabic priority ledger")
    ids = [record["decision_id"] for record in ledger["records"]]
    if len(ids) != 30 or len(set(ids)) != 30:
        raise ValueError("Arabic priority ledger must contain 30 unique IDs")
    headings = re.findall(r"^## ([٠-٩]+)\. (.+)$", guide, re.M)
    if len(headings) != 30 or [int(number.translate(EAST)) for number, _ in headings] != list(range(1, 31)):
        raise ValueError("Guide priority headings are incomplete or out of order")
    guide_ids = re.findall(r"معرّف القرار: `([^`]+)`", guide)
    if guide_ids != ids:
        raise ValueError("Guide IDs differ from the 30-record ledger or order")
    if guide.count("**المعنى المقصود:**") != 30 or guide.count("**لماذا اختير هذا اللفظ مؤقتًا؟**") != 30 or guide.count("**سؤال للمراجع:**") != 30:
        raise ValueError("Guide missing senses, rationales or expert questions")
    if "Floris" in guide or "السطر None" in guide or "TODO" in guide or "HOLD" in guide:
        raise ValueError("Guide contains prohibited attribution or placeholder")
    source_links = re.findall(r"\[(?:المصدر، )?السطر ([٠-٩]+)\]\((https://[^)]+#L[0-9]+(?:-L[0-9]+)?)\)", guide)
    if len(source_links) < 90:
        raise ValueError("Too few source links for three editions and English")
    checked_source = set()
    with zipfile.ZipFile(PUBLIC_COMMIT_ZIP) as archive:
        names = {name.split("/", 1)[1]: name for name in archive.namelist() if "/" in name}
        for shown, url in source_links:
            line = int(shown.translate(EAST))
            match = re.search(r"#L([0-9]+)(?:-L[0-9]+)?$", url)
            if match is None or line != int(match.group(1)):
                raise ValueError(f"Displayed source line and URL disagree: {url}")
            if "github.com/KokunoYumeto/OpenLogic-ar/blob/" in url:
                prefix = f"https://github.com/KokunoYumeto/OpenLogic-ar/blob/{COMMIT}/"
                if not url.startswith(prefix):
                    raise ValueError(f"Unpinned or foreign Arabic source link: {url}")
                relative = url[len(prefix):].split("#", 1)[0]
                if relative not in names:
                    raise ValueError(f"Arabic source absent from anonymous public archive: {relative}")
                remote = archive.read(names[relative])
                local = (ROOT / relative).read_bytes()
                if remote != local:
                    raise ValueError(f"Arabic source differs from anonymous public archive: {relative}")
                if line > len(remote.decode("utf-8").splitlines()):
                    raise ValueError(f"Arabic source line is beyond EOF: {relative}:{line}")
                checked_source.add(relative)
            elif not url.startswith("https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/"):
                raise ValueError(f"Unrecognized English source provenance: {url}")
    pdf_links = re.findall(r"\[ص ([٠-٩]+)\]\((https://[^)]+#page=([0-9]+))\)", guide)
    if len(pdf_links) < 90:
        raise ValueError("Too few PDF-page links for three editions")
    for shown, url, page in pdf_links:
        filename = url.rsplit("/", 1)[-1].split("#", 1)[0]
        if filename not in PDF_PAGES or int(shown.translate(EAST)) != int(page) or not (1 <= int(page) <= PDF_PAGES[filename]):
            raise ValueError(f"Invalid printed PDF link: {url}")
    receipt = {
        "schema": "openlogic-arabic-priority-guide-independent-readback-v1",
        "status": "PASS_30_ARABIC_DECISIONS_AND_PUBLIC_LINKS",
        "source_index_sha256": INDEX_SHA256,
        "source_commit": COMMIT,
        "guide_sha256": sha(GUIDE),
        "guide_bytes": GUIDE.stat().st_size,
        "priority_decisions": len(ids),
        "arabic_senses": guide.count("**المعنى المقصود:**"),
        "arabic_rationales": guide.count("**لماذا اختير هذا اللفظ مؤقتًا؟**"),
        "arabic_expert_questions": guide.count("**سؤال للمراجع:**"),
        "source_line_links_checked": len(source_links),
        "distinct_arabic_source_files_byte_checked_against_anonymous_archive": len(checked_source),
        "pdf_page_links_checked": len(pdf_links),
        "full_1095_choice_guide_complete": False,
        "published": False,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == "__main__":
    main()
