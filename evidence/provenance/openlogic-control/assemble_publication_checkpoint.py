#!/usr/bin/env python3
"""Assemble the exact OLP-0010 Arabic/Persian publication checkpoint.

This script never reads credentials, performs network operations, or deletes
files. It copies only declared live inputs and creates deterministic ZIPs.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "00_control"
LANE = ROOT.parents[1]
LANE_CONTROL = LANE / "00_lane_control"
SOURCE_CACHE = (
    ROOT.parents[4]
    / "outputs"
    / "019ff6c5-84a2-79d3-997e-424cc5e549c8"
    / "research_cache"
    / "OpenLogic"
)
PUBLICATION = ROOT / "publication"
ZIP_EPOCH = (2026, 8, 13, 0, 0, 0)

LOCALIZED_FILES = [
    "content/open-logic-about.tex",
    "content/content.tex",
    "content/sets-functions-relations/sets-functions-relations-complete.tex",
    "content/sets-functions-relations/sets/sets.tex",
    "content/sets-functions-relations/sets/basics.tex",
    "content/sets-functions-relations/sets/subsets.tex",
    "content/sets-functions-relations/sets/important-sets.tex",
    "content/sets-functions-relations/sets/unions-and-intersections.tex",
    "content/sets-functions-relations/sets/pairs-and-products.tex",
    "content/sets-functions-relations/sets/russells-paradox.tex",
]
LOCALIZED_SUPPORT_GLOBS = [
    "about-*.tex",
    "include/*.tex",
    "content/sets-functions-relations/sets/open-logic-*-config.sty",
]
SHARED_FILES = [
    "open-logic-config.sty",
    "open-logic-envs.sty",
    "open-logic-locale.sty",
    "sty/bussproofs-extra.sty",
    "sty/open-logic-formulas.sty",
    "sty/open-logic-referencing.sty",
    "sty/open-logic-selective.sty",
    "sty/open-logic-tokenize.sty",
    "sty/open-logic.sty",
    "sty/ptolemaicastronomy.sty",
    "assets/diagrams/difference.tikz",
    "assets/diagrams/intersection.tikz",
    "assets/diagrams/union.tikz",
]

LOCALES = {
    "ar": {
        "worktree": ROOT / "ar",
        "repo": PUBLICATION / "OpenLogic-ar",
        "driver": "open-logic-through-olp0010-ar.tex",
        "reader_name": "00_OPENLOGIC_ar_CUMULATIVE_LINKED_READER_OLP-0010.pdf",
        "source_zip": "01_OPENLOGIC_ar_EDITABLE_SOURCES_OLP-0010.zip",
        "evidence_zip": "02_OPENLOGIC_ar_EVIDENCE_AND_PROVENANCE_OLP-0010.zip",
        "manifest": "03_OPENLOGIC_ar_SHA256_MANIFEST_OLP-0010.txt",
        "pdf_sha": "AFFF3F21E71060462FD842C18E48B15F7C8284175FB2D39C23920B870DA57ABD",
        "reader_src": PUBLICATION / "OpenLogic-ar/build/output-ar/open-logic-through-olp0010-ar.pdf",
    },
    "fa-IR": {
        "worktree": ROOT / "fa-IR",
        "repo": PUBLICATION / "OpenLogic-fa-ir",
        "driver": "open-logic-through-olp0010-fa-IR.tex",
        "reader_src": PUBLICATION / "OpenLogic-fa-ir/build/output-fa-IR/open-logic-through-olp0010-fa-IR.pdf",
        "reader_name": "00_OPENLOGIC_fa-IR_CUMULATIVE_LINKED_READER_OLP-0010.pdf",
        "source_zip": "01_OPENLOGIC_fa-IR_EDITABLE_SOURCES_OLP-0010.zip",
        "evidence_zip": "02_OPENLOGIC_fa-IR_EVIDENCE_AND_PROVENANCE_OLP-0010.zip",
        "manifest": "03_OPENLOGIC_fa-IR_SHA256_MANIFEST_OLP-0010.txt",
        "pdf_sha": "6CF8F82A0C05775C9C4852C3C8D3D09D1B5E08DAEB6E6942E75C3487F0C2229D",
    },
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def copy_file(src: Path, dst: Path) -> None:
    if not src.is_file():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def clear_dir(path: Path) -> None:
    if path.exists():
        for child in sorted(path.iterdir(), reverse=True):
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    path.mkdir(parents=True, exist_ok=True)


def copy_tree_files(src: Path, dst: Path, *, exclude_dirs: set[str] | None = None) -> None:
    excluded = exclude_dirs or set()
    for path in sorted(src.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(src)
        if any(part in excluded for part in rel.parts):
            continue
        copy_file(path, dst / rel)


def write_git_blob(pathspec: str, dst: Path) -> None:
    data = subprocess.check_output(
        ["git", "-C", str(SOURCE_CACHE), "show", f"9620cc73f9c8e0ad003c514a5d3748f29611c4c0:{pathspec}"]
    )
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)


def deterministic_zip(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_suffix(output.suffix + ".tmp")
    if temp.exists():
        temp.unlink()
    with zipfile.ZipFile(temp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(source.rglob("*"), key=lambda p: p.relative_to(source).as_posix()):
            if not path.is_file():
                continue
            rel = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(rel, ZIP_EPOCH)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(temp, "r") as archive:
        bad = archive.testzip()
        if bad is not None:
            raise RuntimeError(f"ZIP CRC failure: {bad}")
    os.replace(temp, output)


def sanitize_public_provenance(root: Path) -> None:
    """Remove host-local identity and credential locators from public copies.

    The original durable evidence remains untouched. Replacement changes only
    local machine paths, never decisions, source text, hashes, or QA results.
    """
    text_suffixes = {
        ".aux", ".cff", ".csv", ".fls", ".json", ".jsonl", ".log",
        ".md", ".out", ".ps1", ".py", ".tex", ".thm", ".toc", ".tsv", ".txt",
    }
    replacements = {
        r"[REDACTED_LOCAL_CREDENTIAL_PATH]": "[REDACTED_LOCAL_CREDENTIAL_PATH]",
        r"[REDACTED_LOCAL_CREDENTIAL_PATH]": "[REDACTED_LOCAL_CREDENTIAL_PATH]",
        r"<LOCAL_USER_ROOT>": "<LOCAL_USER_ROOT>",
        "<LOCAL_USER_ROOT>": "<LOCAL_USER_ROOT>",
    }
    changed = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in text_suffixes:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        revised = text
        for old, new in replacements.items():
            revised = revised.replace(old, new)
        # TeX consoles hard-wrap long paths, including occasionally inside
        # the local account name (for example `Flori\n s`). Remove that
        # disclosure too while retaining the remainder of each diagnostic.
        revised = re.sub(
            r"C\s*:\s*[/\\]+\s*U\s*s\s*e\s*r\s*s\s*[/\\]+\s*F\s*l\s*o\s*r\s*i\s*s",
            "<LOCAL_USER_ROOT>",
            revised,
            flags=re.IGNORECASE,
        )
        if revised != text:
            path.write_text(revised, encoding="utf-8", newline="\n")
            changed.append(path.relative_to(root).as_posix())
    receipt = root / "PUBLIC_PATH_SANITIZATION.md"
    receipt.write_text(
        "# Public-path sanitization receipt\n\n"
        "This public evidence copy preserves all decisions, raw authority, hashes, "
        "translation ledgers, failures, corrections, build and QA results. Host-local "
        "user-root paths were replaced by `<LOCAL_USER_ROOT>`, and credential-file "
        "locators by `[REDACTED_LOCAL_CREDENTIAL_PATH]`. Credential contents were never "
        "read into or copied to the evidence. The original durable files were not edited.\n\n"
        f"Sanitized text artifacts: {len(changed)}.\n",
        encoding="utf-8",
        newline="\n",
    )


def assemble(locale: str) -> None:
    cfg = LOCALES[locale]
    repo: Path = cfg["repo"]
    worktree: Path = cfg["worktree"]
    locale_src = worktree / "locale" / locale
    source_root = repo / "source"
    evidence_root = repo / "evidence" / "provenance"

    if sha256(cfg["reader_src"]) != cfg["pdf_sha"]:
        raise RuntimeError(f"Frozen reader hash mismatch for {locale}")

    # Public reader and exact build source.
    clear_dir(repo / "reader")
    copy_file(cfg["reader_src"], repo / "reader" / cfg["reader_name"])

    clear_dir(source_root)
    for rel in SHARED_FILES:
        copy_file(worktree / rel, source_root / rel)
    for rel in LOCALIZED_FILES:
        copy_file(locale_src / rel, source_root / "locale" / locale / rel)
    for pattern in LOCALIZED_SUPPORT_GLOBS:
        for path in sorted(locale_src.glob(pattern)):
            copy_file(path, source_root / "locale" / locale / path.relative_to(locale_src))
    for name in [
        "open-logic-config.sty",
        "open-logic-locale.sty",
        cfg["driver"],
    ]:
        copy_file(locale_src / name, source_root / "locale" / locale / name)
    write_git_blob("LICENSE.md", repo / "LICENSE.md")
    if sha256(repo / "LICENSE.md") != "BB5E0179A1E9BDB55634A4303784CF73C297A1DCEE27B92CD546BF398075531C":
        raise RuntimeError("Canonical LF Git-blob license hash mismatch")
    copy_tree_files(CONTROL / "fonts", repo / "00_control" / "fonts")

    # Complete, locale-scoped durable evidence. Repository metadata files in
    # evidence/ are preserved; only evidence/provenance is rebuilt.
    clear_dir(evidence_root)
    copy_tree_files(CONTROL, evidence_root / "openlogic-control", exclude_dirs={"fonts"})
    copy_tree_files(LANE_CONTROL, evidence_root / "lane-control")
    # Preserve the translation-cursor state without presenting its earlier
    # package-building flag as the current release gate. The operative local
    # checkpoint gate is the repository-level evidence/QA_STATE.json.
    cursor_state = evidence_root / "openlogic-control" / "CURRENT_STATE.json"
    if cursor_state.is_file():
        cursor_snapshot = evidence_root / "openlogic-control" / "CURRENT_STATE_TRANSLATION_CURSOR_SNAPSHOT.json"
        cursor_state.replace(cursor_snapshot)
        (evidence_root / "openlogic-control" / "PUBLICATION_STATE_CONTEXT.json").write_text(
            "{\n"
            '  "schema_version": 1,\n'
            '  "snapshot_file": "CURRENT_STATE_TRANSLATION_CURSOR_SNAPSHOT.json",\n'
            '  "snapshot_is_historical_for_release_gate": true,\n'
            '  "snapshot_purpose": "Preserves the paired translation cursor and the pre-publication package-building state.",\n'
            '  "operative_local_release_gate": "../../QA_STATE.json",\n'
            '  "local_checkpoint_state": "CLOSED_WITH_DISCLOSED_CAVEATS",\n'
            '  "remote_publication_state_at_bundle_assembly": "UNPUBLISHED",\n'
            '  "scope": "OLP-0001 through OLP-0010; 10/722; OLP-0011 remains the production cursor"\n'
            "}\n",
            encoding="utf-8",
            newline="\n",
        )
    for name in [
        "ATTRIBUTION_AND_CHANGES.md",
        "TERMINOLOGY_AND_ADVERSE_LEDGER.csv",
    ]:
        copy_file(locale_src / name, evidence_root / "locale" / name)
    for path in sorted(locale_src.glob("BUILD_AND_QA_*.md")):
        copy_file(path, evidence_root / "locale" / path.name)
    build_dir = (
        locale_src / "output/build/cumulative-olp0010"
        if locale == "ar"
        else locale_src / "output/build/cumulative-olp0010-release"
    )
    for path in sorted(build_dir.iterdir()):
        if path.is_file() and path.suffix.lower() != ".pdf":
            copy_file(path, evidence_root / "final-build" / path.name)
    sanitize_public_provenance(repo / "evidence")

    provenance_inventory = evidence_root / "PROVENANCE_SHA256.tsv"
    provenance_rows = ["relative_path\tbytes\tsha256\n"]
    for path in sorted(evidence_root.rglob("*"), key=lambda p: p.relative_to(evidence_root).as_posix()):
        if path.is_file() and path != provenance_inventory:
            provenance_rows.append(
                f"{path.relative_to(evidence_root).as_posix()}\t{path.stat().st_size}\t{sha256(path)}\n"
            )
    provenance_inventory.write_text("".join(provenance_rows), encoding="utf-8", newline="\n")

    # Repository inventory covers the stable checkout surface. Numbered
    # Zenodo assets are excluded because they are hashed by file 03 and the
    # remote publication receipt; this file excludes itself by definition.
    # Local build/output-* directories are reproducible, host-path-bearing
    # scratch outputs and are ignored by Git, so they are not public artifacts.
    inventory = repo / "evidence" / "ARTIFACT_SHA256.tsv"
    rows = [
        "# Covers repository files except this inventory, .git, and root numbered Zenodo assets.\n",
        "relative_path\tbytes\tsha256\n",
    ]
    for path in sorted(repo.rglob("*"), key=lambda p: p.relative_to(repo).as_posix()):
        rel = path.relative_to(repo)
        if not path.is_file() or path == inventory or ".git" in rel.parts:
            continue
        if len(rel.parts) >= 2 and rel.parts[0] == "build" and rel.parts[1].startswith("output-"):
            continue
        if len(rel.parts) == 1 and rel.name[:3] in {"00_", "01_", "02_", "03_"}:
            continue
        rows.append(f"{rel.as_posix()}\t{path.stat().st_size}\t{sha256(path)}\n")
    inventory.write_text("".join(rows), encoding="utf-8", newline="\n")

    # Deterministic public archives. The source ZIP includes the exact source
    # tree, build recipe, canonical license, and pinned font files.
    with tempfile.TemporaryDirectory(prefix="openlogic-source-") as td:
        temp_root = Path(td) / f"OpenLogic-{locale}-OLP-0010-editable-sources"
        copy_tree_files(source_root, temp_root / "source")
        copy_tree_files(repo / "00_control" / "fonts", temp_root / "00_control" / "fonts")
        copy_file(repo / "build" / "BUILD.ps1", temp_root / "build" / "BUILD.ps1")
        copy_file(repo / "LICENSE.md", temp_root / "LICENSE.md")
        deterministic_zip(temp_root, repo / cfg["source_zip"])
    with tempfile.TemporaryDirectory(prefix="openlogic-evidence-") as td:
        temp_root = Path(td) / f"OpenLogic-{locale}-OLP-0010-evidence-and-provenance"
        copy_tree_files(repo / "evidence", temp_root / "evidence")
        deterministic_zip(temp_root, repo / cfg["evidence_zip"])

    # Zenodo's deliberately small four-file surface is mirrored at repo root.
    copy_file(repo / "reader" / cfg["reader_name"], repo / cfg["reader_name"])
    manifest = repo / cfg["manifest"]
    manifest_lines = []
    for name in [cfg["reader_name"], cfg["source_zip"], cfg["evidence_zip"]]:
        path = repo / name
        manifest_lines.append(f"{sha256(path)}  {name}\n")
    manifest.write_text("".join(manifest_lines), encoding="utf-8", newline="\n")

    print(
        f"ASSEMBLED {locale} reader={sha256(repo / cfg['reader_name'])} "
        f"source_zip={sha256(repo / cfg['source_zip'])} "
        f"evidence_zip={sha256(repo / cfg['evidence_zip'])} "
        f"manifest={sha256(manifest)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("locales", nargs="*", choices=sorted(LOCALES), default=sorted(LOCALES))
    args = parser.parse_args()
    for locale in args.locales:
        assemble(locale)


if __name__ == "__main__":
    main()
