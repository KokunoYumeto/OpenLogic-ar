#!/usr/bin/env python3
"""Recheck the released editable EPUBs; correct only their AI disclosures.

No translation body, MathML, stylesheet, graph or historical receipt is edited.
The old source archive is read directly, not trusted because of its filename.
Each old EPUB must be reproducible byte for byte before a successor is written.
Fresh checkers and exact-source packaging are required before publication.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import zipfile
from xml.etree import ElementTree as ET

REPO = Path(__file__).resolve().parents[1]
BASELINE = REPO / "tmp/epub/full-book-20260925-direct-complete/source-qa-r6b/OPENLOGIC_ar_R3_COMPLETE_EPUB_SOURCE_AND_QA.zip"
BASELINE_ID = (297333390, "9b247f33daf75b849df4711ff3b14f30d5f446e251dc66952e9930c38c404351")
EXPECTED = {
    "international": ("OpenLogic-Arabic-Complete-722-international.epub", "a4c5333d974a0d8ecdb0e70304756dadca9b596c3aad7374e02ae63c8b567568"),
    "machrek": ("OpenLogic-Arabic-Complete-722-machrek.epub", "e3684461384b423aaa069343abeb66e491ab0162fefc893da33a431afdd63d02"),
    "classical": ("OpenLogic-Arabic-Complete-722-classical.epub", "23504936c1ef737c28c4dcbf0ad2ce6ad21e8a6075914bfe04cb87dfea1a61d6"),
}
TIME = (2026, 9, 6, 0, 0, 0)
MODIFIED = "2026-09-30T00:00:00Z"
DISCLOSURE_AR = (
    "تُنسب الترجمة والتصحيحات الموروثة في مصادر هذه النسخة إلى OpenAI Codex — "
    "GPT-5.6 Sol، بمستوى جهد Ultra. أُنجز استكمال تحويل الطبعات الثلاث إلى EPUB، "
    "وتجميعها والتحقق الآلي منها وإعداد حزم مصادرها، بواسطة OpenAI Codex — "
    "GPT-6 Sol، بمستوى جهد Ultra. وأُعيد فحص إعادة البناء وصُحِّح هذا البيان "
    "بواسطة OpenAI Codex — GPT-6.1 Sol، بمستوى جهد Ultra. لا يُقدَّم هذا "
    "التصحيح بوصفه إعادة ترجمة للمتن، ولم تقع مراجعة بشرية شاملة. "
    "هذه نسخة EPUB من النص المنشور في ٢٥ سبتمبر؛ لا تضم تلقائيًا "
    "تصحيحات تنضيد PDF اللاحقة."
)
META = "{http://www.idpf.org/2007/opf}meta"
CHANGED = frozenset({"OEBPS/package.opf", "OEBPS/provenance.xhtml"})


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def identity(path: Path) -> dict:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as source:
        for data in iter(lambda: source.read(1024 * 1024), b""):
            size += len(data)
            h.update(data)
    return {"file": path.name, "bytes": size, "sha256": h.hexdigest()}


def pack(members: dict[str, bytes], target: Path) -> None:
    require(not target.exists(), "Refusing to overwrite " + str(target))
    require(members.get("mimetype") == b"application/epub+zip", "Invalid mimetype")
    with zipfile.ZipFile(target, "w", allowZip64=True) as z:
        for name in ["mimetype"] + sorted(set(members) - {"mimetype"}):
            info = zipfile.ZipInfo(name, TIME)
            info.compress_type = zipfile.ZIP_STORED if name == "mimetype" else zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.flag_bits |= 0x800
            z.writestr(info, members[name], compresslevel=9)


def correct(members: dict[str, bytes]) -> dict[str, bytes]:
    result = dict(members)
    opf = ET.fromstring(members["OEBPS/package.opf"])
    provenance = [e.text for e in opf.iter(META) if e.get("property") == "dcterms:provenance"]
    modified = [e.text for e in opf.iter(META) if e.get("property") == "dcterms:modified"]
    require(len(provenance) == len(modified) == 1 and isinstance(provenance[0], str), "Ambiguous OPF metadata")
    old = html.escape(provenance[0], quote=False).encode("utf-8")
    new = html.escape(DISCLOSURE_AR, quote=False).encode("utf-8")
    for name in CHANGED:
        raw = members[name]
        require(raw.count(old) == 1, "Disclosure not uniquely bound: " + name)
        result[name] = raw.replace(old, new)
        if name.endswith(".opf"):
            marker = (">" + str(modified[0]) + "</meta>").encode("utf-8")
            require(result[name].count(marker) == 1, "Modified timestamp is ambiguous")
            result[name] = result[name].replace(marker, (">" + MODIFIED + "</meta>").encode("utf-8"))
        ET.fromstring(result[name])
    require({name for name in members if members[name] != result[name]} == CHANGED, "Change scope differs")
    return result


def validate_xhtml(members: dict[str, bytes]) -> dict:
    """Independent XML, unique-ID and relative-link/fragment closure check."""
    import posixpath
    from urllib.parse import unquote, urlsplit
    roots = {name: ET.fromstring(raw) for name, raw in members.items() if name.endswith(".xhtml")}
    require(len(roots) == 812, "XHTML census differs")
    ids = {}
    links = []
    native_math = 0
    for name, root in roots.items():
        values = [node.get("id") for node in root.iter() if node.get("id") is not None]
        require(len(values) == len(set(values)), "Duplicate document ID: " + name)
        ids[name] = set(values)
        for node in root.iter():
            if node.tag == "{http://www.w3.org/1998/Math/MathML}math":
                native_math += 1
            for attr in ("href", "src"):
                if node.get(attr):
                    links.append((name, node.get(attr)))
    checked = 0
    for document, target in links:
        link = urlsplit(target)
        if link.scheme or link.netloc:
            continue
        path = posixpath.normpath(posixpath.join(posixpath.dirname(document), unquote(link.path))) if link.path else document
        require(path in members, "Missing relative link: " + document + " -> " + target)
        if link.fragment:
            require(path in ids and unquote(link.fragment) in ids[path], "Missing fragment: " + document + " -> " + target)
        checked += 1
    return {"xhtml_documents": len(roots), "native_math_elements": native_math,
            "relative_links_checked": checked, "unique_document_ids": True}


def run(output: Path) -> dict:
    require(not output.exists(), "Output directory already exists")
    old_id = identity(BASELINE)
    require((old_id["bytes"], old_id["sha256"]) == BASELINE_ID, "Released source archive differs")
    output.mkdir(parents=True)
    rows = []
    with zipfile.ZipFile(BASELINE) as source:
        require(len(source.namelist()) == len(set(source.namelist())) == 2478, "Source archive inventory differs")
        for profile, (filename, expected) in EXPECTED.items():
            prefix = "epub-source/" + profile + "/"
            members = {name[len(prefix):]: source.read(name) for name in source.namelist() if name.startswith(prefix)}
            require(len(members) == 819, "Expanded source census differs: " + profile)
            replay = output / ("BASELINE-" + filename)
            pack(members, replay)
            require(identity(replay)["sha256"] == expected, "Independent baseline rebuild differs: " + profile)
            before = validate_xhtml(members)
            revised = correct(members)
            after = validate_xhtml(revised)
            require(before == after, "Document/link/math census changed")
            target = output / filename
            pack(revised, target)
            with zipfile.ZipFile(target) as built:
                require(set(built.namelist()) == set(members), "Successor member inventory differs")
                for name, raw in revised.items():
                    require(built.read(name) == raw, "Successor member bytes differ: " + name)
            rows.append({"profile": profile, "baseline": identity(replay), "successor": identity(target),
                         "changed_members": sorted(CHANGED), "content_checks": after,
                         "all_other_817_members_byte_identical": True})
    receipt = {"schema": "openlogic-sol6-epub-independent-review-v1",
               "status": "CORRECTED_EPUBS_PENDING_FRESH_CHECKERS_AND_SOURCE_PACKAGING",
               "review_model": "GPT-6.1 Sol", "effort": "Ultra", "baseline_source": old_id,
               "disclosure_ar": DISCLOSURE_AR, "profiles": rows,
               "translation_body_changes": 0, "mathml_changes": 0,
               "scope_limit_ar": "فحص إعادة البناء والروابط والبيان؛ ليس تدقيقًا دلاليًا لجميع الترجمة أو قبولًا بصريًا جديدًا."}
    (output / "REVIEW_RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    print(json.dumps(run(parser.parse_args().output), ensure_ascii=True))
