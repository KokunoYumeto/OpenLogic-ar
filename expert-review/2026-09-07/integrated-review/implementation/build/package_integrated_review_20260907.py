"""Finite local preservation of the accepted integrated reviewer export.

No network, credential access, Git, source mutation, TeX or review generation.
The old public snapshot remains intact; only its two entry pages and inventory
are updated after the new subtree passes its source, privacy and link checks.
"""
from __future__ import annotations

import argparse
import collections
import csv as csv_module
import gzip
import hashlib
import html
import itertools
import json
import os
from pathlib import Path
import re
import shutil
import zipfile
from urllib.parse import unquote

from build import package_expert_review_publication_20260907 as projection
from build.validate_expert_review_snapshot import decisions

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO.parent.parent / "openlogic-arabic-review-publication-20260907"
PUBLIC = ROOT / "expert-review/2026-09-07"
EXPORT = REPO / "tmp/expert-index-consolidated-review-16-stream-20260907"
CLOSURE = REPO / "evidence/classical/SOURCE_RECONCILIATION_CLOSURE_MANIFEST_20260905.json"
CLOSURE_SHA = "8cf84ddffa2d862b0ff8181dd34e79559ceedabdf119d30c614253001b19a973"
ARCHIVE = "OPENLOGIC_ARABIC_EXPERT_REVIEW_INTEGRATED_20260907.zip"
GUIDE = "START_HERE_AND_FULL_INTEGRATED_LIST_20260907.md"
SUMS = "EXPERT_REVIEW_INTEGRATED_SHA256_20260907.txt"
ENTRIES = ("EXPERT_REVIEW_START_HERE.md", "ALL_RECORDED_CHOICES.md")
LINK = projection.LINK
REFERENCE = projection.REFERENCE
TEXT_LIMIT = 16 * 1024 * 1024
PROPOSAL_NOTE = "**Proposed wording — not applied to the current source / صياغة مقترحة لم تُطبّق على النص الحالي.**"
PROPOSAL_SHORT = "**Proposed, not applied / مقترح غير مطبّق**"
PROPOSAL_HEADER = "Publication status / حالة التطبيق"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return projection.hash_file(path)


def identity(path, name=None):
    return {"path": name or path.name, "bytes": path.stat().st_size, "sha256": digest(path)}


def small_json(path):
    require(path.stat().st_size <= TEXT_LIMIT, "Oversized metadata: " + str(path))
    return json.loads(path.read_bytes())


def text(path):
    require(path.stat().st_size <= TEXT_LIMIT, "Oversized text: " + str(path))
    return path.read_text(encoding="utf-8-sig")


def save(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def safe_child(root, relative):
    target = (root / relative).resolve()
    require(target.is_relative_to(root.resolve()), "Path escapes admitted root")
    return target


def exact_zip(archive, public):
    """Stream both writing and verification; reject duplicates and extra names."""
    paths = sorted(p for p in public.rglob("*") if p.is_file())
    expected = {"expert-review/2026-09-07/" + p.relative_to(public).as_posix(): identity(p) for p in paths}
    with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for path in paths:
            name = "expert-review/2026-09-07/" + path.relative_to(public).as_posix()
            entry = zipfile.ZipInfo(name, date_time=(2026, 9, 7, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            with path.open("rb") as source, output.open(entry, "w") as destination:
                shutil.copyfileobj(source, destination, 1024 * 1024)
    verify_zip(archive, expected)
    return len(expected)


def verify_zip(archive, expected):
    with zipfile.ZipFile(archive) as package:
        names = package.namelist()
        require(len(names) == len(set(names)), "Duplicate archive entry")
        require(set(names) == set(expected), "Archive inventory differs")
        for name, wanted in expected.items():
            hashed, length = hashlib.sha256(), 0
            with package.open(name) as member:
                for chunk in iter(lambda: member.read(1024 * 1024), b""):
                    hashed.update(chunk)
                    length += len(chunk)
            require((length, hashed.hexdigest()) == (wanted["bytes"], wanted["sha256"]), "Archive bytes differ: " + name)


def markdown_anchors(body):
    anchors = set(re.findall(r'\bid=["\']([^"\']+)["\']', body))
    seen = collections.Counter()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", body, re.M):
        heading = html.unescape(re.sub(r"<[^>]+>", "", heading)).lower()
        slug = re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")
        number = seen[slug]
        seen[slug] += 1
        anchors.add(slug + ("-" + str(number) if number else ""))
    return anchors


def check_links(body, target, public, cache):
    declared = set(re.findall(r"^\[([^\]]+)\]:", body, re.M))
    require(set(re.findall(r"\[[^\]\n]*\]\[([^\]]+)\]", body)) <= declared, "Undeclared reference link: " + str(target))
    count = 0
    for link in projection.all_links(body):
        if re.match(r"^(https?:|mailto:)", link, re.I):
            continue
        part, _, fragment = link.partition("#")
        destination = safe_child(public, os.path.relpath(target.parent / unquote(part), public)) if part else target
        require(destination.is_file() or destination == target, "Missing local link: " + str(destination))
        if fragment:
            fragment = unquote(fragment)
            if re.fullmatch(r"L\d+(?:-L?\d+)?", fragment):
                key = (destination, "lines")
                if key not in cache:
                    with destination.open("rb") as source:
                        cache[key] = sum(1 for _ in source)
                numbers = list(map(int, re.findall(r"\d+", fragment)))
                require(min(numbers) >= 1 and max(numbers) <= cache[key], "Source line anchor exceeds file")
            elif destination.suffix == ".md":
                key = (destination, "anchors")
                if key not in cache:
                    cache[key] = markdown_anchors(body if destination == target else text(destination))
                require(fragment in cache[key], "Unproved Markdown anchor: " + str(destination) + "#" + fragment)
            else:
                raise ValueError("Unproved local fragment: " + link)
        count += 1
    return count


def stream_gzip(source, destination):
    with source.open(encoding="utf-8") as incoming, destination.open("xb") as outgoing:
        with gzip.GzipFile(filename="", fileobj=outgoing, mode="wb", mtime=0) as compressed:
            for line in incoming:
                compressed.write(projection.private_projection(line).encode("utf-8"))


def proposal_ids(index):
    result = []
    for row in decisions(index):
        if row.get("status") == "proposed-unapplied":
            result.append(row["decision_id"])
    require(len(result) == len(set(result)) == 7, "Expected exactly seven distinct unapplied proposals")
    return set(result)


def annotate_proposals(body, proposals):
    """Add an explicit status, never rewrite wording or its recorded reasons."""
    original = body
    require(PROPOSAL_NOTE not in original and PROPOSAL_SHORT not in original, "Original already contains publication status annotations")
    sections, summaries = {}, {}
    for decision_id in sorted(proposals):
        pattern = r"(^- \*\*ID / الرقم:\*\* `" + re.escape(decision_id) + r"`[ \t]*$)"
        body, count = re.subn(pattern, lambda m: m.group(1) + "\n- " + PROPOSAL_NOTE, body, flags=re.M)
        if count:
            sections[decision_id] = count
        slug = re.sub(r"[^a-z0-9]+", "-", decision_id.lower()).strip("-")
        pattern = r"(\]\([^\)\n]*#(?:decision|priority|complete)-" + re.escape(slug) + r"(?:-[0-9a-f]{10})?\))"
        body, count = re.subn(pattern, lambda m: m.group(1) + " " + PROPOSAL_SHORT, body)
        if count:
            summaries[decision_id] = count
    require(body.count(PROPOSAL_NOTE) == sum(sections.values()), "Proposal section annotation count differs")
    require(body.count(PROPOSAL_SHORT) == sum(summaries.values()), "Proposal summary annotation count differs")
    require(body.replace("\n- " + PROPOSAL_NOTE, "").replace(" " + PROPOSAL_SHORT, "") == original,
            "Status annotation changed pre-existing Markdown")
    return body, {"sections": sections, "summaries": summaries}


def project_csv(source, destination, proposals):
    observed = collections.Counter()
    with source.open(encoding="utf-8-sig", newline="") as incoming, destination.open("x", encoding="utf-8-sig", newline="") as outgoing:
        reader, writer = csv_module.reader(incoming), csv_module.writer(outgoing, lineterminator="\n")
        header = next(reader)
        require(len(header) > 1 and header[1] == "Decision ID / رقم القرار", "Unexpected occurrence-table columns")
        writer.writerow(header + [PROPOSAL_HEADER])
        for row in reader:
            require(len(row) == len(header), "Malformed occurrence row")
            label = ""
            if row[1] in proposals:
                observed[row[1]] += 1
                label = "proposed-unapplied — Proposed wording, not applied to current source / صياغة مقترحة لم تُطبّق على النص الحالي"
            writer.writerow([projection.private_projection(field) for field in row] + [label])
    require(set(observed) == proposals, "An unapplied proposal lacks a labelled CSV row")
    # Independently read the public column, including every repeated occurrence.
    with destination.open(encoding="utf-8-sig", newline="") as checked, source.open(encoding="utf-8-sig", newline="") as original:
        reader, predecessor = csv_module.reader(checked), csv_module.reader(original)
        require(next(reader) == next(predecessor) + [PROPOSAL_HEADER], "Proposal status column/header differs")
        reread = collections.Counter()
        for row, prior in itertools.zip_longest(reader, predecessor):
            require(row is not None and prior is not None, "CSV row inventory differs")
            require(row[:-1] == [projection.private_projection(field) for field in prior], "An existing CSV cell changed")
            require(bool(row[-1]) == (row[1] in proposals), "CSV proposal status misassigned")
            if row[1] in proposals:
                require(row[-1].startswith("proposed-unapplied —"), "CSV proposal status corrupted")
                reread[row[1]] += 1
        require(reread == observed, "CSV proposal occurrence count differs")
    return dict(observed)


def package(expected_json, readback_receipt):
    require(re.fullmatch(r"[0-9a-f]{64}", expected_json) is not None, "Explicit SHA-256 required")
    readback_receipt = readback_receipt.resolve()
    require(readback_receipt.is_relative_to(REPO / "tmp/redo-20260906-reviewer"), "Readback receipt outside admitted run directory")
    validation_path = EXPORT / "READBACK_VALIDATION.json"
    validation = small_json(validation_path)
    runner = small_json(readback_receipt)
    require(validation.get("status") == "PASS" and validation.get("errors") == [], "Independent validation did not pass")
    require(runner.get("status") == "PASS_INDEPENDENT_READBACK" and not runner.get("owned_pids_not_drained"), "Bounded independent readback did not pass/drain")
    require(runner.get("snapshot") == EXPORT.relative_to(REPO).as_posix(), "Receipt names a different export")
    require(runner.get("validation_sha256") == digest(validation_path), "Validation receipt bytes changed")
    require(runner.get("counts") == validation["counts"], "Validation count inventory differs")
    require(validation.get("snapshot_json_sha256") == expected_json == digest(EXPORT / "EXPERT_REVIEW_INDEX.json"), "Accepted index hash differs")
    require(digest(CLOSURE) == CLOSURE_SHA, "Current source closure changed")
    terminal = runner["terminal_generation"]
    require(terminal["snapshot_json_sha256"] == expected_json, "Generation does not identify accepted JSON")
    generation_path = safe_child(REPO, terminal["path"])
    require(digest(generation_path) == terminal["sha256"], "Generation receipt changed")
    generation = small_json(generation_path)
    require(generation.get("resumed_source_checkpoint", {}).get("closure_sha256") == CLOSURE_SHA, "Generation used a different source closure")
    proposals = proposal_ids(EXPORT / "EXPERT_REVIEW_INDEX.json")
    integrated = PUBLIC / "integrated-review"
    for path in (integrated, ROOT / ARCHIVE, ROOT / GUIDE, ROOT / SUMS, ROOT / "INTEGRATED_PACKAGE_RECEIPT.json"):
        require(not path.exists(), "Output already exists; inspect instead of overwriting: " + str(path))
    old_manifest_path = PUBLIC / "PUBLICATION_MANIFEST.json"
    old_manifest = small_json(old_manifest_path)
    old_rows = old_manifest["files"] + [identity(old_manifest_path)]
    require(len(old_rows) == len({row["path"] for row in old_rows}), "Duplicate predecessor inventory")
    for row in old_rows:
        require(identity(safe_child(PUBLIC, row["path"]), row["path"]) == row, "Predecessor publication changed: " + row["path"])
    require({p.relative_to(PUBLIC).as_posix() for p in PUBLIC.rglob("*") if p.is_file()} == {r["path"] for r in old_rows}, "Unrecorded predecessor files")
    projection.EXPORT, projection.PUBLIC = EXPORT, integrated
    integrated.mkdir()
    history = integrated / "history"
    history.mkdir()
    for name in (*ENTRIES, "PUBLICATION_MANIFEST.json"):
        shutil.copyfile(PUBLIC / name, history / name)
    (history / "README.md").write_text(
        "# Historical preservation copies\n\n"
        "The two entry pages and manifest here preserve exact predecessor bytes. Their relative links describe the old directory location, not this archive directory. "
        "For a working historical view use [the immutable published snapshot](https://github.com/KokunoYumeto/OpenLogic-ar/tree/f051d7378ea1bcb617c0feec24a9f78e3fdcf659/expert-review/2026-09-07). "
        "These files do not replace the current integrated review or describe its status.\n", encoding="utf-8", newline="\n")
    inputs = {}

    def remember(path):
        inputs[path] = identity(path)

    sources = []
    for unit in small_json(CLOSURE)["units"]:
        rows = [("english", safe_child(projection.ENGLISH, unit["source_path"]), unit["english_sha256"], None)]
        rows += [(kind, safe_child(REPO, unit[kind]["path"]), unit[kind]["sha256"], unit[kind]["bytes"]) for kind in ("msa", "classical")]
        for edition, source, expected, size in rows:
            require(digest(source) == expected.lower() and (size is None or source.stat().st_size == size), "Source no longer matches accepted closure: " + str(source))
            destination = projection.public_target(source)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            remember(source)
            require(digest(destination) == expected.lower(), "Source copy differs")
            sources.append({"unit": unit["id"], "edition": edition, **identity(destination, destination.relative_to(integrated).as_posix())})
    require(len(sources) == 2166 and len({r["path"] for r in sources}) == 2166, "Expected exactly 2166 distinct source files")
    require(collections.Counter(r["edition"] for r in sources) == {"english": 722, "msa": 722, "classical": 722}, "Source edition inventory differs")
    save(integrated / "SOURCE_SNAPSHOT.json", {"source_closure_sha256": CLOSURE_SHA, "sources": sources, "live_sources_modified": False})

    # Admit every generated Markdown link and recursively project cited Markdown.
    pending = list(EXPORT.glob("*.md")) + list((EXPORT / "reviewer-index").glob("*.md"))
    seen, generated, annotations = set(), [], {}
    while pending:
        source = pending.pop()
        if source in seen:
            continue
        seen.add(source)
        remember(source)
        body, destination = text(source), projection.public_target(source)
        for link in projection.all_links(body):
            if re.match(r"^(https?:|mailto:|#)", link, re.I):
                continue
            origin = (source.parent / unquote(link.partition("#")[0])).resolve()
            target = projection.public_target(origin)
            require(origin.is_file(), "Missing cited evidence: " + str(origin))
            if origin.is_relative_to(EXPORT):
                continue
            if origin.suffix == ".md":
                pending.append(origin)
            elif not target.exists():
                require(origin.suffix.lower() in (".json", ".tex", ".txt", ".sty", ".py", ".ps1", ".cs"), "Unadmitted evidence type")
                remember(origin)
                target.parent.mkdir(parents=True, exist_ok=True)
                if origin.suffix.lower() in (".tex", ".sty"):
                    shutil.copyfile(origin, target)
                else:
                    target.write_text(projection.private_projection(text(origin)), encoding="utf-8", newline="\n")
        destination.parent.mkdir(parents=True, exist_ok=True)
        body = projection.rewrite_markdown(body, source, destination)
        if source.is_relative_to(EXPORT):
            body, annotations[source.relative_to(EXPORT).as_posix()] = annotate_proposals(body, proposals)
            if source.name == "EXPERT_REVIEW_START_HERE.md":
                body = ("Working-register notice: the complete list includes **7 unapplied proposals**, explicitly labelled as proposed wording rather than current source text. "
                        "[Full recorded list](ALL_RECORDED_CHOICES.md).\n\n" + body)
        destination.write_text(body, encoding="utf-8", newline="\n")
        generated.append(destination)
    stream_gzip(EXPORT / "EXPERT_REVIEW_INDEX.json", integrated / "EXPERT_REVIEW_INDEX.json.gz")
    csv = EXPORT / "EXPERT_REVIEW_OCCURRENCES.csv"
    remember(csv)
    csv_annotations = project_csv(csv, integrated / csv.name, proposals)
    require(set(annotations["EXPERT_REVIEW_INDEX.md"]["sections"]) == proposals, "Full register omitted a proposal section")
    require({key for name, row in annotations.items() if name.startswith("reviewer-index/complete-") for key in row["sections"]} == proposals, "Readable shards omitted an unapplied proposal")
    save(integrated / "PROPOSAL_STATUS_PROJECTION.json", {
        "scope": "Status copied from accepted raw records; wording, reasons and raw status fields are unchanged. These seven proposals are not applied source repairs.",
        "proposal_ids": sorted(proposals), "count": len(proposals), "markdown": annotations, "csv_occurrences": csv_annotations})
    for path in (validation_path, readback_receipt, generation_path, CLOSURE):
        remember(path)
    implementation = [REPO / name for name in (
        "build/generate_expert_review_index.py", "build/validate_expert_review_snapshot.py",
        "build/run_expert_review_readback_20260906.py", "build/run_current_arabic_source_checkpoint_20260907.py",
        "build/run_arabic_review_integration_20260906.py", "build/package_integrated_review_20260907.py",
        "build/package_expert_review_publication_20260907.py", "build/tests/test_expert_review_streamed_output.py",
        "build/tests/test_expert_review_next_source_batch.py", "build/tests/test_expert_review_consolidated_repairs.py",
        "build/tests/test_expert_review_applied_repairs.py", "build/tests/test_expert_review_snapshot_repairs.py",
        "build/tests/test_package_integrated_review_20260907.py",
        "tmp/redo-20260906-reviewer/consolidated-source-16-20260907/RUN_RECEIPT.json",
        "tmp/redo-20260906-reviewer/consolidated-source-16-20260907-guard/RUN_RECEIPT.json",
    )] + [readback_receipt, generation_path, generation_path.parent / "reviewer-generation.log"]
    implementation_rows = []
    for source in implementation:
        remember(source)
        target = integrated / "implementation" / source.relative_to(REPO)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(projection.private_projection(text(source)), encoding="utf-8", newline="\n")
        implementation_rows.append({"original": projection.private_projection(str(source)), "original_sha256": digest(source), **identity(target, target.relative_to(integrated).as_posix())})
    save(integrated / "IMPLEMENTATION_MANIFEST.json", {"scope": "Privacy-normalized preservation copies, not a standalone runnable repository. Historical failed wrappers retain their recorded status; acceptance is the exact independent readback, not those failures.", "files": implementation_rows})
    save(integrated / "READBACK_VALIDATION.json", json.loads(projection.private_projection(json.dumps(validation, ensure_ascii=False))))
    counts = validation["counts"]
    overview = (
        "# Integrated Arabic translation-review register\n\n"
        f"Working register: {counts['human_decisions']:,} readable entries; counts are recorded entries, not unique terms or a completed full-work audit.\n\n"
        f"**This total includes {len(proposals)} unapplied proposals, labelled explicitly in the readable sections and occurrence table. These proposals are not current source wording.**\n\n"
        "- [Start with priority choices](EXPERT_REVIEW_START_HERE.md).\n"
        "- [Browse all recorded entries](reviewer-index/README.md).\n"
        "- [Sortable occurrence table](EXPERT_REVIEW_OCCURRENCES.csv).\n"
        "- [Machine-readable register](EXPERT_REVIEW_INDEX.json.gz).\n\n"
        f"{counts['flagged_decisions']:,} flagged choices; {counts['unresolved_lexical_locations']:,} unresolved lexical locations; "
        f"{counts['flagged_missing_explicit_question']:,} flags still need explicit questions. "
        "Entries distinguish recorded evidence, retrospective reasons and provisional choices open to correction. "
        "Exact source locations are supplied where proved; final PDF page numbers are not certified. "
        "This integrated source/reviewer update does not rebuild the books or certify a finished Classical reader. "
        "Earlier source snapshots and the separate 16-choice supplement remain preserved beside this subtree.\n"
    )
    (integrated / "ALL_RECORDED_CHOICES.md").write_text(overview, encoding="utf-8", newline="\n")
    generated.append(integrated / "ALL_RECORDED_CHOICES.md")
    cache, links = {}, 0
    for path in generated:
        links += check_links(text(path), path, PUBLIC, cache)
    username = os.environ.get("USERNAME", "").casefold()
    for path in integrated.rglob("*"):
        if path.is_file() and path.suffix != ".gz":
            with path.open(encoding="utf-8-sig") as source:
                for line in source:
                    require(not username or username not in line.casefold(), "Privacy check failed")
                    require(not re.search(r"C:[/\\]Users[/\\]", line, re.I), "Private user path remains")
    with gzip.open(integrated / "EXPERT_REVIEW_INDEX.json.gz", "rt", encoding="utf-8") as source:
        for line in source:
            require(not username or username not in line.casefold(), "Compressed register privacy check failed")
    # The live originals must still have the identities used during projection.
    for path, row in inputs.items():
        require(identity(path) == row, "Input changed during packaging: " + str(path))
    require(digest(CLOSURE) == CLOSURE_SHA and digest(EXPORT / "EXPERT_REVIEW_INDEX.json") == expected_json, "Accepted source/index changed")
    for row in old_rows:
        require(identity(PUBLIC / row["path"], row["path"]) == row, "Historical public bytes changed")
    start_body = "# Arabic translation review — start here\n\n[Open the current priority choices](integrated-review/EXPERT_REVIEW_START_HERE.md).\n\n[Full recorded list](ALL_RECORDED_CHOICES.md). The current integrated register supplies wording, exact source locations where proved, reasons and provisional questions. It includes **7 unapplied proposals**, explicitly labelled as proposals rather than current source wording. It is an unfinished working register, not a finished Classical book or a certification of final PDF page numbers.\n\n[Previous start page](https://github.com/KokunoYumeto/OpenLogic-ar/blob/f051d7378ea1bcb617c0feec24a9f78e3fdcf659/expert-review/2026-09-07/EXPERT_REVIEW_START_HERE.md). [Earlier 16-choice supplement](supplement-16-choices/README.md).\n"
    full_body = overview.replace("](", "](integrated-review/")
    for name, body in zip(ENTRIES, (start_body, full_body)):
        links += check_links(body, PUBLIC / name, PUBLIC, cache)
        (PUBLIC / name).write_text(body, encoding="utf-8", newline="\n")
    manifest = {"schema": "arabic-expert-review-integrated-public-projection-v1", "status": "CHECKED_INTEGRATED_WORKING_REGISTER",
        "review_index_original_sha256": expected_json, "source_closure_sha256": CLOSURE_SHA,
        "counts": counts, "local_links_verified": links, "source_files": len(sources), "new_reader_built": False,
        "unapplied_proposals": len(proposals), "proposal_status_projection": "integrated-review/PROPOSAL_STATUS_PROJECTION.json",
        "previous_manifest": "integrated-review/history/PUBLICATION_MANIFEST.json",
        "files": [identity(p, p.relative_to(PUBLIC).as_posix()) for p in sorted(PUBLIC.rglob("*")) if p.is_file() and p != old_manifest_path]}
    save(old_manifest_path, manifest)
    package_files = exact_zip(ROOT / ARCHIVE, PUBLIC)
    (ROOT / GUIDE).write_text(
        "# Arabic translation-review register\n\n"
        "[Start here](https://github.com/KokunoYumeto/OpenLogic-ar/blob/main/expert-review/2026-09-07/EXPERT_REVIEW_START_HERE.md)\n\n"
        "[Full recorded list](https://github.com/KokunoYumeto/OpenLogic-ar/blob/main/expert-review/2026-09-07/ALL_RECORDED_CHOICES.md)\n\n"
        f"{counts['human_decisions']:,} readable entries in the accepted integrated working register. Reasons, exact source locations where established and questions open to correction accompany the wording. "
        "The count includes 7 explicitly labelled unapplied proposals, not seven additional implemented corrections. "
        "Earlier snapshots and existing books are preserved. This release is not a new Classical PDF, an exhaustive completed expert audit or a certification of final PDF page references. The ZIP is an offline mirror; the links above are readable online.\n",
        encoding="utf-8", newline="\n")
    files = [identity(ROOT / name) for name in (ARCHIVE, GUIDE)]
    (ROOT / SUMS).write_text("".join(f"{row['sha256']}  {row['path']}\n" for row in files), encoding="utf-8", newline="\n")
    files.append(identity(ROOT / SUMS))
    receipt = {"status": "PASS_LOCAL_EXACT_PACKAGE", "files": files, "counts": counts,
        "public_package_files": package_files, "source_files": len(sources), "local_links_verified": links,
        "review_index_original_sha256": expected_json, "source_closure_sha256": CLOSURE_SHA,
        "readback_validation_sha256": digest(validation_path), "readback_runner_sha256": digest(readback_receipt),
        "manifest_sha256": digest(old_manifest_path), "new_reader_built": False,
        "unapplied_proposals": len(proposals),
        "preserved_predecessor_files": len(old_rows) - 3}
    save(ROOT / "INTEGRATED_PACKAGE_RECEIPT.json", receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-json", required=True)
    parser.add_argument("--readback-receipt", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(package(args.expected_json.lower(), args.readback_receipt), ensure_ascii=False))


if __name__ == "__main__":
    main()
