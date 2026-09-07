"""Bounded, independent readback of a generated reviewer snapshot.

Streams one JSON decision at a time. Missing review work is counted honestly;
stale applied assessments, dropped records and broken local links are errors.
This does not certify every translation choice or any unsupplied PDF page.
"""
from __future__ import annotations

import argparse
import bisect
from collections import Counter
import csv
import hashlib
import html
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote


# This is a separate readback contract, not an import of the producer. Terms,
# reasons, alternatives, questions and source phrases are read from these ledgers.
REPAIR_LEDGERS = {
    "OLP0497_MP_PROPAGATION_20260906.json": ("0497",),
    "OLP0079_0093_MP_PROPAGATION_20260906.json": ("0079", "0093"),
    "OLP0005_0008_0016_0018_QUALIFICATION_PROPAGATION_20260906.json":
        ("0005", "0008", "0016", "0018"),
    "OLP0033_0039_0072_0081_QUALIFICATION_PROPAGATION_20260906.json":
        ("0033", "0039", "0072", "0081"),
}
BATCH2_SHA256 = "c7caca6897613149f74de25b08ebbe324699de79ec7531a7f4e6e5842d9683bd"
PRIOR_MANIFEST = "evidence/classical/SOURCE_PROPAGATION_PRE_QUALIFICATIONS_20260906.json"
PRIOR_SHA256 = "865eb48a37f5a50876dc5f406adf432a0360bf1e7c9a5fb5667caf41d27aa9ec"
REPAIR_PREFIX = "semantic-propagation-20260906:"
INDEPENDENT_PREFIX = ("New independent assessment dated 2026-09-06; not a reconstruction of "
                      "the original translator's deliberation. ")
INHERITED_SCOPE = ("Inherited-source qualification: this makes the mathematical qualification or logical "
                   "scope explicit, rather than claiming only a lexical mistranslation. ")
TRANSLATION_SCOPE = ("Translation-scope clarification: the English condition is retained; this removes "
                     "ambiguity in the Arabic any-versus-none wording without claiming an error in the "
                     "English source. ")
HISTORICAL_STATUS = "historical-before-bytes-proved-by-exact-inverse-not-current-source"
HISTORY_FIELDS = ("english_term", "chosen_arabic", "before_arabic", "sense", "rationale",
                  "alternatives", "expert_question", "recording_mode")
SCOPE_LEDGER = "evidence/classical/repairs/OLP0051_0060_0068_SCOPE_PROPAGATION_20260906.json"
SCOPE_SHA256 = "0c66dd4c3449c9aa8d92a0d904a813d9365942b0ef92d8327420a26b864d5c43"
DUAL_LEDGER = "evidence/classical/repairs/OLP0067_DUAL_GRAMMAR_20260906.json"
DUAL_SHA256 = "b6af652713edbecb4457d6725790cdc9de4f0ee4c446f3e3844d2760dde81ef1"
PROSE_LEDGER = "evidence/classical/repairs/OLP0008_CLASSICAL_PROSE_20260906.json"
PROSE_SHA256 = "99eda5ab0d7714c9fe274ce5a1fce4f058090cfff0474c8da749b80956f1f033"
PROSE_REFRESH = "evidence/classical/repairs/OLP0008_CLASSICAL_WITNESS_REFRESH_20260906.json"
PROSE_REFRESH_SHA256 = "32446183261b9fbe62b916ee8f2262f4624b1831930fe6ca0121b13b61d57a2d"
SCOPE_IDS = {"OLP-0051": "scope-0051-generated-carrier",
             "OLP-0060": "scope-0060-hypothesis-final-index",
             "OLP-0068": "scope-0068-used-premise-membership"}
# Independently pinned reader registries, not the export's claimed expansions.
DISPLAY_REGISTRY_SOURCES = {
    "source/open-logic-config.sty": "ab19be71b50b415738603290317b504d9fa6b82850fe640d585c62db1540ced3",
    "source/locale/ar/open-logic-config.sty": "018ce747a3957ce35eb05820e919d46fe4af0f3452ecdbe4d1ddc7e95bf33280",
}
CONSOLIDATED_LEDGERS = {
    "evidence/classical/repairs/OLP0375_0376_ARITHMETIC_SCOPE_20260907.json":
        ("042822d86510960c3ae3fc9600ddf273f015bc00adc09e19c240a7071d265ff5", "openlogic-arithmetic-scope-repairs-v1"),
    "evidence/classical/repairs/OLP0021_TWO_ROOTS_NOTE_20260907.json":
        ("98b939cba500c9cbe8e591917709940ca0f685c61a0a4965535864e9aefd7120", "openlogic-square-root-note-repair-v1"),
    "evidence/classical/repairs/OLP0321_0326_0368_SEMANTIC_SCOPE_20260907.json":
        ("3cff7ba6901f09815be1ea4f42b2a29074639079fc21b09ae8cb4e6096e899da", "openlogic-semantic-scope-repairs-v1"),
}
CONSOLIDATED_PREFIX = "semantic-propagation-20260907:"
NEXT_REPAIR_LEDGERS = {
    "evidence/classical/repairs/OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907.json":
        ("eb0e436d546c867a56d66767a24f66a2d687ea254ed83c9123aa0c2106a8e0c7", "openlogic-classical-construction-repairs-v1", 3, 7,
         ("AR-OLP-0021-CLASSICAL-SUCCESSOR-CONSTRUCTION-20260907", "AR-OLP-0022-CLASSICAL-IDENTITY-PREDICATE-20260907",
          "AR-OLP-0022-CLASSICAL-PIECEWISE-PREDICATE-20260907", "AR-OLP-0022-CLASSICAL-BIJECTIVE-RELATIVE-20260907",
          "AR-OLP-0022-CLASSICAL-BIJECTION-IFF-20260907", "AR-OLP-0024-CLASSICAL-INVERSE-PREDICATE-20260907")),
    "evidence/classical/repairs/OLP0394_0399_0400_0404_0409_MODAL_SCOPE_20260907.json":
        ("6d29d66c0db082e2c348cf8a30219e9d6ae11b80e14d0ecfdd2cbc2c79a6f4cd", "openlogic-consolidated-modal-semantic-repairs-v1", 10, 15,
         ("AR-OLP-0394-MODAL-FINAL-VALUE-20260907", "AR-OLP-0399-FINITE-GRID-DOMAIN-20260907",
          "AR-OLP-0400-FINITE-PREMISE-CONVERSE-20260907", "AR-OLP-0404-THEOREM-EMPTY-SLOTS-20260907",
          "AR-OLP-0409-MODAL-SCOPE-20260907", "AR-OLP-0409-NECESSITY-WORLD-SCOPE-20260907")),
    "evidence/classical/repairs/OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907.json":
        ("90364663431ea9dad27fef1a427acf033498f1cd95f8cbea29cc665f41186c79", "openlogic-classical-adjective-construction-repairs-v1", 3, 4,
         ("AR-OLP-0022-CLASSICAL-SURJECTIVE-OPENING-20260907", "AR-OLP-0028-CLASSICAL-ENUMERABLE-OPENING-20260907",
          "AR-OLP-0029-CLASSICAL-DUAL-SURJECTIVE-20260907", "AR-OLP-0029-CLASSICAL-ZERO-INDEXED-ELEMENTS-20260907")),
}
HISTORICAL_TRANSITIONS = {
    ("source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex",
     "8183c83e20fc04ced33d83554ebb142f94b7c8bf323b992336a25b9153db2498"):
        "evidence/classical/repairs/OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907.json",
    ("source/locale/ar-classical/content/sets-functions-relations/functions/function-kinds.tex",
     "8a73d76a7d09e54a6956468280c054ded5243f4f4a43ed05aee76de126dd9ca9"):
        "evidence/classical/repairs/OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907.json",
}
NEXT_ENGLISH_PHRASES = {
    "AR-OLP-0024-CLASSICAL-INVERSE-PREDICATE-20260907":
        ("In\nother words, for $g$ to be defined, $f$~must be both !!{injective} and\n!!{surjective}.",),
    "AR-OLP-0394-MODAL-FINAL-VALUE-20260907":
        ("if $\\pAssign v(p) =\n\\Undef$, then $\\pValue v(\\lnot \\Diamond(p \\land \\lnot p)) =\n\\Undef$",),
    "AR-OLP-0399-FINITE-GRID-DOMAIN-20260907":
        ("When considering this infinite truth value set, it is often\nuseful to also consider the subsets",),
    "AR-OLP-0400-FINITE-PREMISE-CONVERSE-20260907": ("In fact, the converse holds as well.",),
    "AR-OLP-0404-THEOREM-EMPTY-SLOTS-20260907":
        ("of the $n$-sequent containing $!A$ in each position corresponding to a\ndesignated truth value of~$\\Log{L}$.",),
    "AR-OLP-0409-MODAL-SCOPE-20260907":
        ("It is necessarily possible that it will rain tomorrow.",
         "If it is necessarily possible that~$!A$ then it is possible\n  that~$!A$.",
         "Possibly necessarily\n\\ldots possibly $!A$"),
    "AR-OLP-0409-NECESSITY-WORLD-SCOPE-20260907":
        ("the truth of statement at\na world $w$ (or a state description $s$) does not depend on $w$ at\nall.",),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def byte_digest(data):
    return hashlib.sha256(data).hexdigest()


def same_hash(left, right):
    return isinstance(left, str) and isinstance(right, str) and left.lower() == right.lower()


def bounded_bytes(path):
    require(path.stat().st_size <= 2 * 1024 * 1024, "oversized repair input: " + str(path))
    return path.read_bytes()


def active_phrase(text, phrase, kind):
    """Literal Unicode phrase, ignoring TeX comments but not TeX syntax/diacritics.

    English boundaries stop `enumerable` matching `nonenumerable`. Arabic clitics
    are permitted; an ellipsis or a removed word never becomes a literal phrase.
    """
    lines = []
    for line in unicodedata.normalize("NFC", text).splitlines():
        for pos, char in enumerate(line):
            if char == "%":
                backslashes = len(line[:pos]) - len(line[:pos].rstrip("\\"))
                if backslashes % 2 == 0:
                    line = line[:pos]
                    break
        lines.append(line)
    pattern = r"\s+".join(re.escape(word) for word in unicodedata.normalize("NFC", phrase).split())
    if kind == "english":
        pattern = r"(?<![\w-])" + pattern + r"(?![\w-])"
    return bool(pattern and re.search(pattern, "\n".join(lines), re.IGNORECASE))


def exact_excerpt(data, start, end):
    lines = data.decode("utf-8-sig").splitlines()
    require(type(start) is int and type(end) is int and 1 <= start <= end <= len(lines),
            "invalid exact source line range")
    return "\n".join(lines[start - 1:end])


def declared_witness(data, declaration, term, kind, *, historical=False):
    prefix = "before_" if historical else ("after_" if kind == "msa" and "after_sha256" in declaration else "")
    require(same_hash(declaration.get(prefix + "sha256"), byte_digest(data)),
            kind + " source hash mismatch")
    if prefix + "bytes" in declaration:
        require(declaration[prefix + "bytes"] == len(data), kind + " source byte count mismatch")
    start_key = "before_line_start" if historical and "before_line_start" in declaration else "line_start"
    end_key = "before_line_end" if historical and "before_line_end" in declaration else "line_end"
    start, end = declaration[start_key], declaration[end_key]
    excerpt = exact_excerpt(data, start, end)
    excerpt_key = "before_excerpt" if historical else "excerpt"
    if excerpt_key in declaration:
        require(declaration[excerpt_key] == excerpt, kind + " exact excerpt mismatch")
        require(same_hash(declaration.get(excerpt_key + "_sha256"), byte_digest(excerpt.encode("utf-8"))),
                kind + " exact excerpt hash mismatch")
    require(active_phrase(excerpt, term, kind), kind + " active literal phrase missing from declared lines")
    return {"path": declaration["path"], "sha256": byte_digest(data), "bytes": len(data),
            "line_start": start, "line_end": end, "excerpt": excerpt, "data": data, "term": term}


def inverse_source(data, patches):
    require(isinstance(patches, list) and patches, "missing exact source patches")
    before = data
    for patch in reversed(patches):
        old, new = patch["before"].encode("utf-8"), patch["after"].encode("utf-8")
        require(old != new and before.count(new) == 1, "non-unique or unchanged inverse source patch")
        before = before.replace(new, old, 1)
    replay = before
    for patch in patches:
        old, new = patch["before"].encode("utf-8"), patch["after"].encode("utf-8")
        require(replay.count(old) == 1, "non-unique forward source patch")
        replay = replay.replace(old, new, 1)
    require(replay == data, "source patch forward replay mismatch")
    return before


def identity_bytes(data, declaration, label):
    require(same_hash(declaration.get("sha256"), byte_digest(data)) and
            declaration.get("bytes") == len(data), label + " identity mismatch")


def source_bytes(root, declaration, inventory):
    root = root.resolve()
    target = (root / declaration["path"]).resolve()
    require(target.is_relative_to(root), "source path escapes declared root")
    data = bounded_bytes(target)
    identity_bytes(data, declaration, declaration["path"])
    inventory[str(target)] = byte_digest(data)
    return data


def historical_version_bytes(root, declaration, inventory):
    """Only the two pinned named predecessor transitions permit old bytes."""
    ledger = HISTORICAL_TRANSITIONS.get((declaration["path"], declaration["sha256"].lower()))
    if ledger is None:
        return source_bytes(root, declaration, inventory)
    raw = bounded_bytes(root / ledger)
    require(byte_digest(raw) == NEXT_REPAIR_LEDGERS[ledger][0], "historical transition ledger identity mismatch")
    inventory[str((root / ledger).resolve())] = byte_digest(raw)
    candidates = [t for t in json.loads(raw)["transactions"] if t["path"] == declaration["path"]]
    require(len(candidates) == 1, "historical transition path mismatch")
    t = candidates[0]
    require(same_hash(t["before_sha256"], declaration["sha256"]) and t["before_bytes"] == declaration["bytes"],
            "historical transition predecessor mismatch")
    live = source_bytes(root, {"path": t["path"], "sha256": t["after_sha256"], "bytes": t["after_bytes"]}, inventory)
    return before_history(live, t["patches"], declaration)[0]


def next_literal(data, logical, kind, literal, first, last):
    # Blank comments independently of the producer; keep the selected tokens.
    clean = []
    for line in literal.splitlines():
        for index, char in enumerate(line):
            if char == "%" and (index - len(line[:index].rstrip("\\"))) % 2 == 0:
                line = line[:index]
                break
        clean.append(line)
    literal = "\n".join(clean).strip()
    witness = {"path": logical, "sha256": byte_digest(data), "bytes": len(data), "data": data,
               "line_start": first, "line_end": last, "excerpt": exact_excerpt(data, first, last), "term": literal}
    ranges = literal_ranges(witness, kind)
    require(len(ranges) == 1, "next repair exact active phrase missing or ambiguous")
    start, end = next(iter(ranges))
    witness.update(line_start=start, line_end=end, excerpt=exact_excerpt(data, start, end))
    public = {key: witness[key] for key in ("path", "bytes", "line_start", "line_end", "excerpt")}
    public.update(sha256=byte_digest(data).upper(), excerpt_sha256=byte_digest(witness["excerpt"].encode()).upper(), literal=literal)
    return witness, public


def current_literal(repo, kind, witness, inventory):
    if (witness["path"], witness["sha256"].lower()) not in HISTORICAL_TRANSITIONS:
        return witness, {key: witness[key] for key in ("path", "bytes", "line_start", "line_end", "excerpt")} | {
            "sha256": witness["sha256"].upper(), "excerpt_sha256": byte_digest(witness["excerpt"].encode()).upper(), "literal": witness["term"]}
    require(historical_version_bytes(repo, witness, inventory) == witness["data"], "historical projection revalidation differs")
    live = bounded_bytes(repo / witness["path"])
    require(inventory[str((repo / witness["path"]).resolve())] == byte_digest(live), "current projection source changed")
    return next_literal(live, witness["path"], kind, witness["term"], 1, len(live.decode().splitlines()))


def strict_passage(data, declaration):
    identity_bytes(data, declaration, declaration["path"])
    passage = exact_excerpt(data, declaration["line_start"], declaration["line_end"])
    require(declaration.get("excerpt") == passage and
            same_hash(declaration.get("excerpt_sha256"), byte_digest(passage.encode("utf-8"))),
            declaration["path"] + " exact passage mismatch")
    return passage


def ledger_witness(data, declaration, term, kind):
    """Bind a ledger's byte/line witness while accepting preserved CRLF text.

    The prose ledger records the English excerpt with its source CRLF line
    ending, whereas the independent line reader uses normalized LF lines.
    Byte ranges are therefore checked first and the returned witness is the
    normalized, line-addressable form used by the rest of this validator.
    """
    require(same_hash(declaration.get("sha256"), byte_digest(data)), kind + " ledger witness hash mismatch")
    if "bytes" in declaration:
        require(declaration["bytes"] == len(data), kind + " ledger witness byte count mismatch")
    if "byte_start" in declaration:
        start, end = declaration["byte_start"], declaration["byte_end"]
        require(type(start) is int and type(end) is int and 0 <= start < end <= len(data),
                kind + " invalid byte witness range")
        require(data[start:end].decode("utf-8") == declaration["excerpt"],
                kind + " byte witness excerpt mismatch")
    excerpt = exact_excerpt(data, declaration["line_start"], declaration["line_end"])
    recorded = declaration.get("excerpt", "").replace("\r\n", "\n").replace("\r", "\n")
    # A byte witness may intentionally select only the first clause of a
    # source line; line-addressable output nevertheless retains the complete
    # line range so raw/human locators can be checked independently.
    require(active_phrase(recorded, term, kind), kind + " active literal phrase missing from ledger witness")
    return {"path": declaration["path"], "sha256": byte_digest(data), "bytes": len(data),
            "line_start": declaration["line_start"], "line_end": declaration["line_end"],
            "excerpt": excerpt, "data": data, "term": term}


def literal_ranges(witness, kind):
    """Independently enumerate every active literal occurrence in its witness.

    Keep one newline per source line while blanking comment suffixes. Offsets
    belong to the normalized search text only; returned ranges index the
    original UTF-8 line inventory. No producer tokenizer or locator is used.
    """
    if "passages" in witness:
        return set().union(*(literal_ranges(passage, kind) for passage in witness["passages"]))
    rows = []
    for line in unicodedata.normalize("NFC", witness["excerpt"]).splitlines():
        for offset, char in enumerate(line):
            if char == "%" and (offset - len(line[:offset].rstrip("\\"))) % 2 == 0:
                line = line[:offset]
                break
        rows.append(line)
    body = "\n".join(rows)
    starts = [0] + [m.end() for m in re.finditer("\n", body)]
    phrase = unicodedata.normalize("NFC", witness["term"])
    expression = r"\s+".join(re.escape(word) for word in phrase.split())
    require(bool(expression), "empty exact literal phrase")
    if kind == "english":
        expression = r"(?<![\w-])" + expression + r"(?![\w-])"
    base = witness["line_start"]
    return {(base + bisect.bisect_right(starts, m.start()) - 1,
             base + bisect.bisect_right(starts, m.end() - 1) - 1)
            for m in re.finditer(expression, body, re.IGNORECASE)}


def before_history(after, patches, anchor):
    for patch in patches:
        for key in ("before", "after"):
            if key + "_sha256" in patch:
                require(same_hash(patch[key + "_sha256"], byte_digest(patch[key].encode("utf-8"))),
                        "inverse patch literal hash mismatch")
    before = inverse_source(after, patches)
    identity_bytes(before, anchor, "independently frozen historical source")
    return before, {"path": anchor["path"], "sha256": byte_digest(before), "bytes": len(before),
                    "text_utf8": before.decode("utf-8"), "patches": patches, "status": HISTORICAL_STATUS}


def prose_transition(repo, inventory):
    """Pinned five-patch transition; this also rebinds the older qualification."""
    raw = bounded_bytes(repo / PROSE_LEDGER)
    require(byte_digest(raw) == PROSE_SHA256, "commissioned Classical prose ledger identity mismatch")
    payload = json.loads(raw)
    identity = {"path": PROSE_LEDGER, "sha256": byte_digest(raw), "bytes": len(raw)}
    inventory[str(repo / PROSE_LEDGER)] = identity["sha256"]
    require(payload.get("schema") == "openlogic-classical-prose-repairs-v1" and
            payload.get("unit_id") == "OLP-0008" and payload.get("assessed_on") == "2026-09-06" and
            payload.get("status") == "implemented-in-classical-source", "Classical prose ledger provenance mismatch")
    require([d["decision_id"] for d in payload["decisions"]] ==
            ["AR-OLP-0008-CLASSICAL-" + suffix for suffix in ("C005", "C009", "C014", "C016")],
            "Classical prose decision inventory mismatch")
    source = payload["source"]
    after_id = {"path": source["path"], "sha256": source["after_sha256"], "bytes": source["after_bytes"]}
    before_id = {"path": source["path"], "sha256": source["before_sha256"], "bytes": source["before_bytes"]}
    after = source_bytes(repo, after_id, inventory)
    patches = [p for choice in payload["decisions"] for p in choice["patches"]]
    require(len(patches) == 5 and all(len(c["patches"]) == (2 if c["decision_id"].endswith("C009") else 1)
                                   for c in payload["decisions"]), "Classical prose patch inventory mismatch")
    before, history = before_history(after, patches, before_id)
    preserved = source_bytes(repo, source["prior_snapshot"], inventory)
    require(before == preserved, "Classical prose inverse differs from preserved historical bytes")
    prior_data = bounded_bytes(repo / PRIOR_MANIFEST)
    require(byte_digest(prior_data) == PRIOR_SHA256, "Classical prose prior manifest identity mismatch")
    inventory[str(repo / PRIOR_MANIFEST)] = byte_digest(prior_data)
    prior = next(u for u in json.loads(prior_data)["units"] if u["id"] == "OLP-0008")
    identity_bytes(before, prior["classical"], "independently frozen Classical prose predecessor")
    return payload, identity, before, after, history


def qualification_refresh(repo, old_payload, old_identity, declaration, inventory):
    payload, repair_identity, before, after, history = prose_transition(repo, inventory)
    raw = bounded_bytes(repo / PROSE_REFRESH)
    require(byte_digest(raw) == PROSE_REFRESH_SHA256, "Classical qualification refresh identity mismatch")
    companion = json.loads(raw)
    inventory[str(repo / PROSE_REFRESH)] = byte_digest(raw)
    require(companion.get("schema") == "openlogic-classical-witness-refresh-v1" and
            companion.get("date") == "2026-09-06" and companion.get("unit_id") == "OLP-0008" and
            companion.get("applied_repair") == PROSE_LEDGER and companion.get("source_transition") == payload["source"],
            "Classical qualification refresh provenance mismatch")
    witness = companion["qualification_witness"]
    old_row = next(u for u in old_payload["units"] if u["unit_id"] == "OLP-0008")
    old = witness["historical_ledger"]
    require(old["path"] == old_identity["path"] and old["bytes"] == old_identity["bytes"] and
            same_hash(old["sha256"], old_identity["sha256"]), "historical qualification ledger identity changed")
    require(witness["finding_id"] == "0008-P1" and witness["kind"] == "classical" and
            witness["historical_declaration"] == declaration and witness["historical_rationale"] == old_row["rationale"] and
            witness["historical_expert_review"] == old_row["expert_review"], "historical qualification decision overwritten")
    old_excerpt = strict_passage(before, declaration)
    current = witness["current_declaration"]
    require(current["path"] == declaration["path"] and strict_passage(after, current) == old_excerpt and
            current["line_start"] == declaration["line_start"] and current["line_end"] == declaration["line_end"],
            "qualification refresh changed its selected passage")
    return current, {"path": PROSE_REFRESH, "sha256": byte_digest(raw), "bytes": len(raw),
                     "source_companion": companion}


def dual_grammar_expectations(repo, english_root, baseline, prior, inventory):
    path = repo / DUAL_LEDGER
    raw = bounded_bytes(path)
    require(byte_digest(raw) == DUAL_SHA256,
            "dual grammar ledger identity mismatch")
    payload = json.loads(raw)
    identity = {"path": DUAL_LEDGER, "sha256": byte_digest(raw), "bytes": len(raw)}
    inventory[str(path)] = identity["sha256"]
    require(payload.get("schema") == "openlogic-olp0067-dual-grammar-repairs-v1" and
            payload.get("assessed_on") == "2026-09-06" and
            payload.get("status") == "implemented-in-both-arabic-wording-registers",
            "dual grammar schema/provenance mismatch")
    rows = payload.get("decisions", [])
    expected_ids = [f"ar-{kind}-OLP0067-signed-formula-{case}-20260906"
                    for kind in ("msa", "classical")
                    for case in ("added-nominative", "both-genitive", "closure-genitive")]
    require([r.get("decision_id") for r in rows] == expected_ids and len(rows) == 6,
            "dual grammar choice inventory mismatch")
    unit = baseline["OLP-0067"]
    old = prior["OLP-0067"]
    english_decl = payload["authorities"]["english"]
    english = source_bytes(english_root, english_decl, inventory)
    require(same_hash(byte_digest(english), unit["english_sha256"]) and
            same_hash(byte_digest(english), old["english_sha256"]), "dual grammar frozen English mismatch")
    sources, histories, patches_by_kind = {}, {}, {}
    for kind, field in (("msa", "arabic_path"), ("classical", "target_path")):
        edition = payload["editions"][kind]
        require(edition["after"]["path"] == unit[field] and
                edition["before"]["path"] == old[kind]["path"] and
                same_hash(edition["before"]["sha256"], old[kind]["sha256"]) and
                edition["before"]["bytes"] == old[kind]["bytes"],
                "dual grammar predecessor identity mismatch")
        sources[kind] = source_bytes(repo, edition["after"], inventory)
        patches = [r["patch"] for r in rows if r["edition"] == kind]
        patches_by_kind[kind] = patches
        histories[kind] = before_history(sources[kind], patches, edition["before"])[1]
        # before_history returns text and history; recompute text for witnesses.
        histories[kind]["data"] = inverse_source(sources[kind], patches)
    specs = {}
    for row in rows:
        kind = row["edition"]
        occurrence = row["occurrences"][0]
        before_data = histories[kind]["data"]
        before_decl, after_decl = occurrence["before"], occurrence["after"]
        english_w = ledger_witness(english, row["english_source_literal_witness"],
                                    row["english_source_literal"], "english")
        target_w = ledger_witness(sources[kind], after_decl, row["chosen_arabic"], kind)
        before_w = ledger_witness(before_data, before_decl, row["patch"]["before"], kind)
        terms = dict(row, before_arabic=row["patch"]["before"], chosen_arabic=row["chosen_arabic"],
                     source_term=row["english_term"],
                     alternatives=[{**a, "form": a.get("form", a.get("wording"))} for a in row["alternatives"]])
        expected_fields = dated_fields(terms, payload)
        key = REPAIR_PREFIX + row["decision_id"]
        specs[key] = {"payload": payload, "terms": terms, "identity": identity,
                      "unit_id": "OLP-0067", "finding_id": row["decision_id"],
                      "qualification": False, "classification": None,
                      "witnesses": {"english": english_w, kind: target_w},
                      "historical": {"path": before_decl["path"], "sha256": byte_digest(before_data),
                                     "bytes": len(before_data), "status": HISTORICAL_STATUS,
                                     "text_utf8": before_data.decode("utf-8"),
                                     "patches": patches_by_kind[kind]},
                      "dated_family": "dual", "changed_edition": kind,
                      "canonical_choice": row, "expected_fields": expected_fields}
    return specs, [identity], inventory


def classical_prose_expectations(repo, english_root, baseline, prior, inventory):
    path = repo / PROSE_LEDGER
    raw = bounded_bytes(path)
    require(byte_digest(raw) == PROSE_SHA256, "Classical prose ledger identity mismatch")
    payload = json.loads(raw)
    identity = {"path": PROSE_LEDGER, "sha256": byte_digest(raw), "bytes": len(raw)}
    inventory[str(path)] = identity["sha256"]
    require(payload.get("schema") == "openlogic-classical-prose-repairs-v1" and
            payload.get("assessed_on") == "2026-09-06" and payload.get("status") == "implemented-in-classical-source",
            "Classical prose schema/provenance mismatch")
    source = payload["source"]
    after = source_bytes(repo, {"path": source["path"], "sha256": source["after_sha256"], "bytes": source["after_bytes"]}, inventory)
    before = source_bytes(repo, source["prior_snapshot"], inventory)
    patches = [p for row in payload["decisions"] for p in row["patches"]]
    inverse = inverse_source(after, patches)
    require(inverse == before, "Classical prose inverse differs from preserved predecessor")
    english_expected = baseline["OLP-0008"]["english_sha256"]
    specs = {}
    for row in payload["decisions"]:
        occurrence_specs = []
        for idx, occ in enumerate(row["occurrences"]):
            patch = row["patches"][idx]
            english_path = (english_root / occ["english"]["path"]).resolve()
            english_data = bounded_bytes(english_path)
            inventory[str(english_path)] = byte_digest(english_data)
            ew = ledger_witness(english_data, occ["english"], occ["english"]["excerpt"], "english")
            cw = ledger_witness(after, occ["classical_after"], patch["after"], "classical")
            bw = ledger_witness(before, occ["classical_before"], patch["before"], "classical")
            occurrence_specs.append({"witnesses": {"english": ew, "classical": cw},
                                     "unit_id": "OLP-0008", "occurrence": occ,
                                     "dated_family": "classical-prose"})
        # The producer's occurrence normalization emits later source passages
        # first; bind by the same deterministic descending line order rather
        # than relying on ledger JSON array order.
        occurrence_specs.sort(key=lambda item: item["witnesses"]["classical"]["line_start"], reverse=True)
        terms = {"source_term": row["english_term"], "english_term": row["english_term"],
                 "chosen_arabic": row["chosen_arabic"],
                 "before_arabic": "\n\n".join(p["before"] for p in row["patches"]),
                 "sense": row["sense"],
                 "rationale": row["rationale"],
                 "alternatives": [a for o in row["occurrences"] for a in o["alternatives"]],
                 "expert_review": {"question": row["expert_review_question"]},
                 "recording_mode": row["recording_mode"], "basis": row["basis"],
                 "status": row["status"], "expert_review_useful": row["expert_review_useful"],
                 "open_to_correction": row["open_to_correction"],
                 "official_attestation_claimed": row["official_whole_sentence_attestation_claimed"],
                 "decision_id": row["decision_id"]}
        specs[REPAIR_PREFIX + row["decision_id"]] = {
                "payload": payload, "terms": terms, "identity": identity, "unit_id": "OLP-0008",
                "finding_id": row["decision_id"], "qualification": False, "classification": None,
                "witnesses": occurrence_specs[0]["witnesses"], "occurrence_specs": occurrence_specs,
                "dated_family": "classical-prose",
                "changed_edition": "classical", "canonical_choice": row,
                "historical": {"path": source["path"], "sha256": byte_digest(before), "bytes": len(before),
                               "status": HISTORICAL_STATUS, "text_utf8": before.decode("utf-8"),
                               "patches": patches},
                "expected_fields": dated_fields(terms, payload)}
    return specs, [identity], inventory


def dated_fields(choice, payload):
    """Expected public fields are literal canonical values, never regenerated reasons."""
    expert = choice.get("expert_review", {})
    question = choice.get("expert_question", expert.get("question"))
    require(isinstance(question, str) and question.strip(), "missing canonical expert question")
    for field in ("rationale", "sense", "chosen_arabic", "recording_mode", "basis", "status"):
        require(isinstance(choice.get(field), str) and choice[field].strip(), "missing canonical " + field)
    fields = {field: choice[field] for field in ("chosen_arabic", "sense", "rationale", "recording_mode", "basis", "status")}
    fields.update(recorded_decision_id=choice["decision_id"],
                  english_term=choice.get("english_term", choice.get("source_term")),
                  before_arabic=choice["before_arabic"], alternatives=choice.get("alternatives", []),
                  expert_question=question, expert_review_useful=True, expert_review_non_blocking=True,
                  open_to_correction=True, official_attestation_claimed=False,
                  assessed_on=payload["assessed_on"], printed_page=None, page_status="bind-after-final-reader-build")
    for field in ("classical_arabic", "english_source_literal", "classification", "edition",
                  "expert_review_reason", "uncertainty", "grammatical_realization", "authority_checks"):
        if field in choice:
            fields[field] = choice[field]
    return fields


def new_repair_expectations(repo, english_root):
    """Independent current-source/inverse witnesses for the additional families.

    The older twelve-repair contract remains separate. Absence of these newly
    commissioned ledgers is an error in a complete production readback.
    """
    baseline_path = repo / "evidence/classical/BASELINE.json"
    baseline_data = bounded_bytes(baseline_path)
    baseline = json.loads(baseline_data)
    prior_data = bounded_bytes(repo / PRIOR_MANIFEST)
    require(byte_digest(prior_data) == PRIOR_SHA256, "immutable prior manifest identity mismatch")
    prior = json.loads(prior_data)
    units = {u["id"]: u for u in baseline["units"]}
    predecessors = {u["id"]: u for u in prior["units"]}
    require(list(predecessors) == [f"OLP-{n:04d}" for n in range(1, 723)], "prior unit inventory mismatch")
    identity_bytes(baseline_data, prior["frozen_baseline"], "frozen baseline")
    inventory = {str(baseline_path): byte_digest(baseline_data), str(repo / PRIOR_MANIFEST): byte_digest(prior_data)}
    specs, ledgers = {}, []
    path = repo / SCOPE_LEDGER
    raw = bounded_bytes(path)
    require(byte_digest(raw) == SCOPE_SHA256, "commissioned scope ledger identity mismatch")
    payload = json.loads(raw)
    identity = {"path": SCOPE_LEDGER, "sha256": byte_digest(raw), "bytes": len(raw)}
    inventory[str(path)] = identity["sha256"]
    ledgers.append(identity)
    require(payload.get("schema") == "openlogic-semantic-qualification-repairs-v1" and
            payload.get("assessed_on") == "2026-09-06" and
            payload.get("recording_mode") == "retrospective-reconstruction" and
            payload.get("status") == "implemented-in-shared-msa-source" and
            payload.get("unit_count") == 3 and payload.get("decision_count") == 4,
            "scope ledger schema/provenance mismatch")
    require("printed_page" in payload and payload["printed_page"] is None and
            payload.get("page_status") == "bind-after-final-reader-build", "scope ledger page claim")
    require({r["unit_id"]: r["decision_id"] for r in payload["units"]} == SCOPE_IDS and
            len(payload["units"]) == 3, "scope choice inventory mismatch")
    for unit in payload["units"]:
        uid, base, predecessor = unit["unit_id"], units[unit["unit_id"]], predecessors[unit["unit_id"]]
        data_by_kind = {}
        for kind, field in (("english", "source_path"), ("msa", "arabic_path"), ("classical", "target_path")):
            declaration = unit["locations"][kind]
            require(declaration["path"] == base[field], "scope baseline path mismatch")
            data = source_bytes(english_root if kind == "english" else repo, declaration, inventory)
            strict_passage(data, declaration)
            data_by_kind[kind] = data
            if kind == "english":
                require(same_hash(base["english_sha256"], byte_digest(data)) and
                        same_hash(predecessor["english_sha256"], byte_digest(data)), "scope frozen English mismatch")
            elif kind == "classical":
                identity_bytes(data, predecessor[kind], "unchanged Classical counterpart")
        anchor = unit["historical_before_anchor"]
        require(anchor["path"] == PRIOR_MANIFEST and same_hash(anchor["sha256"], PRIOR_SHA256) and
                anchor["unit_id"] == uid and anchor["identity"] == predecessor["msa"] and
                anchor["prior_correction"] == predecessor.get("correction"), "scope frozen predecessor declaration mismatch")
        before, history = before_history(data_by_kind["msa"], unit["patches"], predecessor["msa"])
        before_witness = declared_witness(before, unit["locations"]["msa"], unit["before_arabic"], "msa", historical=True)
        for witness in unit["supporting_primary_witnesses"]:
            kind = witness["edition"]
            require(witness["path"] == unit["locations"][kind]["path"], "supporting scope witness path mismatch")
            strict_passage(data_by_kind[kind], witness)
        for kind, declaration in unit["reviewed_primary_files"].items():
            identity_bytes(data_by_kind[kind], declaration, "scope whole-file review")
            require(declaration["lines_read"] == [1, len(data_by_kind[kind].decode("utf-8-sig").splitlines())],
                    "whole-file review endpoints mismatch")
        choices = [unit] + unit.get("additional_phrase_choices", [])
        require(len(choices) == (2 if uid == "OLP-0060" else 1), "scope separate choice inventory mismatch")
        for choice in choices:
            if choice is not unit:
                require(choice["decision_id"] == "scope-0060-prefix-final-index" and choice["unit_patch_indices"] == [1]
                        and choice["patches"] == [unit["patches"][1]], "scope subchoice patch mismatch")
                declared_witness(before, choice["locations"]["msa_before"], choice["before_arabic"], "msa")
            expert = choice["expert_review"]
            require(all(expert.get(key) is True for key in ("useful", "non_blocking", "open_to_correction")) and
                    expert.get("official_attestation_claimed") is False and
                    expert.get("original_translator_motivation_claimed") is False, "scope expert provenance mismatch")
            witnesses = {kind: declared_witness(data_by_kind[kind], choice["locations"][kind], choice[field], kind)
                         for kind, field in (("english", "source_term"), ("msa", "chosen_arabic"), ("classical", "classical_arabic"))}
            key = REPAIR_PREFIX + choice["decision_id"]
            specs[key] = {"payload": payload, "terms": choice, "identity": identity, "unit_id": uid,
                          "finding_id": unit["finding_id"], "qualification": False,
                          "classification": choice["classification"], "witnesses": witnesses,
                          "historical": history, "dated_family": "scope", "changed_edition": "msa",
                          "canonical_choice": choice, "expected_fields": dated_fields(choice, payload)}
    require(len(specs) == 4, "incomplete additional scope choice inventory")
    dual, dual_ledgers, inventory = dual_grammar_expectations(repo, english_root, units, predecessors, inventory)
    prose, prose_ledgers, inventory = classical_prose_expectations(repo, english_root, units, predecessors, inventory)
    require(not (set(specs) & (set(dual) | set(prose))), "duplicate additional repair decision ID")
    specs.update(dual)
    specs.update(prose)
    ledgers.extend(dual_ledgers)
    ledgers.extend(prose_ledgers)
    # Six dual choices plus four Classical prose choices are now canonical
    # current-source assessments alongside the four scope choices.
    require(len(specs) == 14, "incomplete additional repair choice inventory")
    attach_display_contracts(repo, specs, inventory)
    return specs, ledgers, inventory


def repair_expectations(repo, english_root):
    """Independently bind twelve assessments to canonical ledgers and live bytes.

    Only small declared files are read. No generator code, old generated decision,
    claimed PASS flag, or mutable before-source overlay supplies an expected value.
    """
    baseline_path = repo / "evidence/classical/BASELINE.json"
    baseline = json.loads(bounded_bytes(baseline_path))
    units = {row["id"]: row for row in baseline["units"]}
    prior_data = bounded_bytes(repo / PRIOR_MANIFEST)
    require(byte_digest(prior_data) == PRIOR_SHA256, "immutable prior manifest identity mismatch")
    prior = json.loads(prior_data)
    require(prior.get("schema") == "openlogic-classical-source-closure-manifest-v1" and
            prior.get("total_units") == 722 and len(prior.get("units", [])) == 722,
            "immutable prior manifest schema/inventory mismatch")
    frozen_baseline = prior["frozen_baseline"]
    require(frozen_baseline["path"] == baseline_path.relative_to(repo).as_posix() and
            same_hash(frozen_baseline["sha256"], digest(baseline_path)) and
            frozen_baseline["bytes"] == baseline_path.stat().st_size,
            "frozen baseline identity differs from immutable prior manifest")
    prior_units = {row["id"]: row for row in prior["units"]}
    prior_identity = {"path": PRIOR_MANIFEST, "sha256": byte_digest(prior_data).upper(),
                      "bytes": len(prior_data), "source_snapshot_sha256": prior["source_snapshot_sha256"]}
    inventory = {str(baseline_path): digest(baseline_path), str(repo / PRIOR_MANIFEST): byte_digest(prior_data)}
    ledgers, specs = [], {}
    for name, commissioned in REPAIR_LEDGERS.items():
        path = repo / "evidence/classical/repairs" / name
        raw = bounded_bytes(path)
        payload = json.loads(raw)
        identity = {"path": path.relative_to(repo).as_posix(), "sha256": byte_digest(raw), "bytes": len(raw)}
        inventory[str(path)] = identity["sha256"]
        ledgers.append(identity)
        batch2 = commissioned == ("0033", "0039", "0072", "0081")
        if batch2:
            require(identity["sha256"] == BATCH2_SHA256, "commissioned batch2 ledger identity mismatch")
        qualification = "QUALIFICATION" in name
        schema = ("openlogic-semantic-qualification-repairs-v1" if qualification else
                  "openlogic-semantic-propagation-repair-v1" if len(commissioned) == 1 else
                  "openlogic-semantic-propagation-repairs-v1")
        require(payload.get("schema") == schema, name + " schema mismatch")
        require(payload.get("assessed_on") == "2026-09-06" and
                payload.get("recording_mode") == "new-independent-assessment-of-retained-translation" and
                payload.get("status") == "implemented-in-shared-msa-source", name + " provenance mismatch")
        rows = payload.get("units", [payload])
        require([row["unit_id"] for row in rows] == ["OLP-" + unit for unit in commissioned],
                name + " commissioned unit inventory mismatch")
        for row in rows:
            unit_id, finding = row["unit_id"], row["finding_id"]
            require(finding == unit_id[4:] + "-P1", "unexpected repair finding")
            terms = row if qualification else payload
            declarations = row["locations"] if qualification or len(commissioned) == 1 else row
            page_owner = declarations if not qualification and len(commissioned) == 1 else payload
            require("printed_page" in page_owner and page_owner["printed_page"] is None and
                    page_owner.get("page_status") == "bind-after-final-reader-build", finding + " ledger page claim")
            require(terms["before_arabic"] != terms["chosen_arabic"], finding + " unchanged phrase")
            expert = terms["expert_review"]
            require(expert.get("useful") is True and expert.get("open_to_correction") is True and
                    expert.get("non_blocking") is True and expert.get("official_attestation_claimed") is False and
                    bool(expert.get("question")), finding + " expert-review provenance mismatch")
            witnesses = {}
            witness_refreshes = []
            base = units[unit_id]
            for kind, field, term_field in (("english", "source_path", "source_term"),
                                          ("msa", "arabic_path", "chosen_arabic"),
                                          ("classical", "target_path", "classical_arabic")):
                declaration = declarations[kind]
                if unit_id == "OLP-0008" and kind == "classical":
                    declaration, refresh = qualification_refresh(repo, payload, identity, declaration, inventory)
                    witness_refreshes.append(refresh)
                require(declaration["path"] == base[field], finding + " baseline path mismatch: " + kind)
                root = english_root.resolve() if kind == "english" else repo.resolve()
                target = (root / declaration["path"]).resolve()
                require(target.is_relative_to(root), finding + " escaped source root")
                data = bounded_bytes(target)
                inventory[str(target)] = byte_digest(data)
                if kind == "english":
                    require(same_hash(base["english_sha256"], byte_digest(data)), finding + " frozen English mismatch")
                term = terms.get(term_field, terms["chosen_arabic"])
                witnesses[kind] = declared_witness(data, declaration, term, kind)
            patches = terms["patches"] if qualification else [
                {"before": terms["before_arabic"], "after": terms["chosen_arabic"]}]
            before = inverse_source(witnesses["msa"]["data"], patches)
            before_witness = declared_witness(before, declarations["msa"], terms["before_arabic"],
                                               "msa", historical=True)
            historical = {"path": before_witness["path"], "sha256": before_witness["sha256"],
                          "bytes": len(before), "status": HISTORICAL_STATUS}
            if qualification:
                historical.update(text_utf8=before.decode("utf-8"), patches=patches)
                previous = prior_units[unit_id] if batch2 else None
                old_identity = previous["msa"] if previous else {
                    "sha256": base["arabic_sha256"], "bytes": base["arabic_bytes"]}
                require(same_hash(old_identity["sha256"], byte_digest(before)) and
                        old_identity["bytes"] == len(before), finding + " independently frozen before identity mismatch")
                if previous:
                    require(previous["source_path"] == base["source_path"] and
                            same_hash(previous["english_sha256"], base["english_sha256"]) and
                            previous["msa"]["path"] == base["arabic_path"], finding + " prior unit mismatch")
                    historical["identity_basis"] = {"kind": "immutable-pre-qualification-source-manifest",
                                                     "manifest": prior_identity, "unit": previous}
            if not qualification or batch2:
                historical.update({key: before_witness[key] for key in ("line_start", "line_end", "excerpt")})
            classification = row.get("classification") if qualification else None
            if qualification:
                require(bool(classification) and
                        classification.startswith("translation-") == (unit_id == "OLP-0081"),
                        finding + " English fault / Arabic ambiguity classification mismatch")
            spec = {"payload": payload, "terms": terms, "identity": identity, "unit_id": unit_id,
                    "finding_id": finding, "classification": classification, "witnesses": witnesses,
                    "historical": historical, "qualification": qualification,
                    "witness_refreshes": witness_refreshes}
            specs[REPAIR_PREFIX + finding] = spec
            extras = row.get("additional_phrase_choices", [])
            require(bool(extras) == (unit_id == "OLP-0039") and len(extras) <= 1,
                    finding + " missing/unexpected separate connective")
            for extra in extras:
                require(extra.get("choice_id") == "0039-P1-no-surjection-connective" and
                        extra.get("unit_patch_indices") == [0], "separate connective identity mismatch")
                subwitnesses = {}
                for kind, term_field in (("english", "source_term"), ("msa", "chosen_arabic"),
                                         ("classical", "classical_arabic"), ("msa_before", "before_arabic")):
                    parent_kind = "msa" if kind == "msa_before" else kind
                    declaration = extra["locations"][kind]
                    outer = before_witness if kind == "msa_before" else witnesses[kind]
                    require(declaration["path"] == outer["path"] and
                            outer["line_start"] <= declaration["line_start"] <= declaration["line_end"] <= outer["line_end"],
                            "separate connective outside the parent source witness")
                    witness = declared_witness(before if kind == "msa_before" else witnesses[kind]["data"],
                                               declaration, extra[term_field], parent_kind)
                    if kind != "msa_before":
                        subwitnesses[kind] = witness
                for patch in extra["patches"]:
                    require(all(patches[0][key].count(patch[key]) == 1 for key in ("before", "after")) and
                            before.count(patch["before"].encode("utf-8")) == 1 and
                            witnesses["msa"]["data"].count(patch["after"].encode("utf-8")) == 1,
                            "separate connective is not the actual already-applied unit subpatch")
                specs[REPAIR_PREFIX + extra["choice_id"]] = {**spec, "terms": extra,
                    "witnesses": subwitnesses, "choice": extra}
    require(len(specs) == 12, "incomplete commissioned repair decision inventory")
    attach_display_contracts(repo, specs, inventory)
    return specs, ledgers, inventory


def expected_repair_fields(spec):
    if spec.get("dated_family"):
        return spec["expected_fields"]
    terms, payload = spec["terms"], spec["payload"]
    inherited = bool(spec["classification"] and not spec["classification"].startswith("translation-"))
    qualification = spec["qualification"]
    rationale = INDEPENDENT_PREFIX
    if qualification:
        rationale += (INHERITED_SCOPE if inherited else TRANSLATION_SCOPE) + "Previous MSA wording: " + terms["before_arabic"] + ". "
    rationale += terms["rationale"]
    fields = {"recorded_decision_id": terms.get("choice_id", spec["finding_id"]),
              "english_term": terms["source_term"], "chosen_arabic": terms["chosen_arabic"],
              "before_arabic": terms["before_arabic"], "sense": terms.get("sense", terms.get("human_topic")),
              "rationale": rationale, "expert_question": terms["expert_review"]["question"],
              "expert_review_useful": True, "expert_review_non_blocking": True, "open_to_correction": True,
              "official_attestation_claimed": False, "recording_mode": payload["recording_mode"],
              "assessed_on": payload["assessed_on"], "status": payload["status"],
              "printed_page": None, "page_status": "bind-after-final-reader-build",
              "alternatives": [{**alt, "status": alt["disposition"]} for alt in terms.get("alternatives", [])]}
    fields["expert_review_reason"] = fields["sense"]
    fields["basis"] = ("authoritative-dated-inherited-source-qualification-repair" if inherited else
                       "authoritative-dated-translation-scope-clarification-repair" if qualification else
                       "authoritative-dated-semantic-propagation-repair")
    if qualification:
        fields["classical_arabic"] = terms["classical_arabic"]
    return fields


def consolidated_repair_expectations(repo, english_root):
    """Independent exact-byte/source-phrase admission of eight September 7 choices.

    No generator import, ledger PASS flag, or descriptive heading supplies a
    literal witness. All nine transactions are reversed and forward-replayed.
    """
    baseline_data = bounded_bytes(repo / "evidence/classical/BASELINE.json")
    baseline = {u["id"]: u for u in json.loads(baseline_data)["units"]}
    inventory = {str(repo / "evidence/classical/BASELINE.json"): byte_digest(baseline_data)}
    specs, ledgers = {}, []
    for path, (expected_sha, schema) in CONSOLIDATED_LEDGERS.items():
        raw = bounded_bytes(repo / path)
        require(byte_digest(raw) == expected_sha, "unapproved consolidated ledger identity: " + path)
        payload = json.loads(raw)
        identity = {"path": path, "sha256": byte_digest(raw), "bytes": len(raw)}
        ledgers.append(identity)
        inventory[str(repo / path)] = byte_digest(raw)
        require(payload["schema"] == schema and payload["assessed_on"] == "2026-09-07" and
                payload["open_to_correction"] is True, "consolidated ledger date/schema/provisional mismatch")
        arithmetic = schema == "openlogic-arithmetic-scope-repairs-v1"
        semantic = schema == "openlogic-semantic-scope-repairs-v1"
        multiple = arithmetic or semantic
        choices = payload["decisions"] if multiple else [payload]
        ids = (["AR-OLP-0375-ZERO-EXPONENT-20260907", "AR-OLP-0375-PAIR-METHOD-20260907",
                "AR-OLP-0376-TRUNCATED-SUBTRACTION-20260907"] if arithmetic else
               ["AR-OLP-0321-FUNCTION-RELATION-20260907", "AR-OLP-0326-COMPLEMENT-FIRST-ORDER-20260907",
                "AR-OLP-0326-COMPLEMENT-SECOND-ORDER-20260907",
                "AR-OLP-0368-CONDITIONAL-NORMAL-FORM-UNIQUENESS-20260907"] if semantic else
               ["AR-OLP-0021-TWO-ROOTS-NOTE-20260907"])
        require([r["decision_id"] for r in choices] == ids, "consolidated choice inventory mismatch")
        transactions = payload["transactions"] if multiple else [dict(payload["source"],
            unit_id="OLP-0021", edition="msa", patches=[payload["patch"]])]
        require(len(transactions) == (4 if multiple else 1), "consolidated transaction inventory mismatch")
        sources, histories = {}, {}
        for transaction in transactions:
            uid, kind = transaction["unit_id"], transaction["edition"]
            require(kind in {"msa", "classical"}, "unexpected transaction register")
            require((uid, kind) not in sources, "duplicate transaction register")
            logical = baseline[uid]["arabic_path" if kind == "msa" else "target_path"]
            require(transaction["path"] == logical, "consolidated transaction baseline path mismatch")
            after_id = {"path": logical, "sha256": transaction["after_sha256"], "bytes": transaction["after_bytes"]}
            before_id = {"path": logical, "sha256": transaction["before_sha256"], "bytes": transaction["before_bytes"]}
            data = source_bytes(repo, after_id, inventory)
            before, history = before_history(data, transaction["patches"], before_id)
            history["sha256"] = history["sha256"].upper()
            require(all(p.get("occurrences") == 1 for p in transaction["patches"]), "consolidated inverse patch count mismatch")
            sources[(uid, kind)] = (data, after_id, transaction)
            histories[(uid, kind)] = (before, history)
        english = payload["english_sources"] if multiple else [dict(
            next(s for s in payload["unchanged_sources"] if s["kind"] == "english"), unit_id="OLP-0021")]
        for item in english:
            uid, logical = item["unit_id"], baseline[item["unit_id"]]["source_path"]
            require(item["path"] == logical or item["path"].endswith("/" + logical), "consolidated English path mismatch")
            declaration = dict(item, path=logical)
            data = source_bytes(english_root, declaration, inventory)
            require(same_hash(byte_digest(data), baseline[uid]["english_sha256"]), "consolidated frozen English hash mismatch")
            sources[(uid, "english")] = (data, declaration, None)
        if arithmetic:
            declaration = payload["supporting_definition"]
            data = source_bytes(repo, declaration, inventory)
            require(exact_excerpt(data, declaration["line_start"], declaration["line_end"]) == declaration["excerpt"],
                    "supporting exact-numeral definition excerpt mismatch")
        elif semantic:
            for declaration in payload["preserved_arabic_sources"]:
                uid = declaration["unit_id"]
                require(declaration["path"] == baseline[uid]["target_path"] and
                        (uid, "classical") not in sources, "preserved Classical path mismatch")
                sources[(uid, "classical")] = (source_bytes(repo, declaration, inventory), declaration, None)
            witnesses = [w for c in choices for w in c["source_witnesses"]]
            require(len(witnesses) == 20, "semantic primary witness inventory mismatch")
            for witness in witnesses:
                uid, kind = witness["unit_id"], witness["edition"]
                data, declared, _ = sources[(uid, kind)]
                if witness["phase"] == "before":
                    data = histories[(uid, kind)][0]
                else:
                    require(witness["phase"] == "after", "unknown semantic witness phase")
                identity_bytes(data, witness, "semantic primary witness")
                require(witness["path"] == declared["path"] and
                        exact_excerpt(data, witness["line_start"], witness["line_end"]) == witness["excerpt"],
                        "semantic primary witness path/excerpt mismatch")
        else:
            declaration = next(s for s in payload["unchanged_sources"] if s["kind"] == "classical")
            require(declaration["path"] == baseline["OLP-0021"]["target_path"], "unchanged Classical path mismatch")
            sources[("OLP-0021", "classical")] = (historical_version_bytes(repo, declaration, inventory), declaration, None)

        def selected(uid, kind, loc, historical=False):
            data, declaration, _ = sources[(uid, kind)]
            if historical:
                data, history = histories[(uid, kind)]
                declaration = {k: history[k] for k in ("path", "sha256", "bytes")}
            start, end = loc["line_start"], loc["line_end"]
            excerpt = exact_excerpt(data, start, end)
            require(active_phrase(excerpt, loc["literal"], kind), "selected consolidated literal absent from exact source lines")
            witness = {"path": declaration["path"], "sha256": byte_digest(data), "bytes": len(data),
                       "line_start": start, "line_end": end, "excerpt": excerpt, "term": loc["literal"], "data": data}
            require(literal_ranges(witness, kind) == {(start, end)}, "consolidated literal range is not exact")
            public = {k: witness[k] for k in ("path", "sha256", "bytes", "line_start", "line_end", "excerpt")}
            public.update(sha256=public["sha256"].upper(), excerpt_sha256=byte_digest(excerpt.encode("utf-8")).upper(), literal=loc["literal"])
            if not historical and (declaration["path"], byte_digest(data)) in HISTORICAL_TRANSITIONS:
                original = public
                witness, public = current_literal(repo, kind, witness, inventory)
                public["assessed_source_phase"] = "unchanged-at-earlier-assessment-now-historical"
                public["assessed_source_witness"] = original
            return witness, public

        for choice in choices:
            uid = choice["unit_id"]
            occurrence_specs, passages = [], []
            for item in choice["literal_review_occurrences"]:
                kind, index = item["edition"], item["patch_index"]
                transaction = sources[(uid, kind)][2]
                patch = transaction["patches"][index]
                if multiple:
                    binding = next(b for b in choice["occurrence_bindings"] if b["edition"] == kind)
                    require(binding["path"] == transaction["path"] and binding["sha256"] == transaction["after_sha256"]
                            and index in binding["patch_indices"], "consolidated occurrence binding mismatch")
                for phase in ("before", "after"):
                    require(active_phrase(patch[phase], item[phase]["literal"], kind), "selected literal outside canonical patch")
                ew, ep = selected(uid, "english", item["english"])
                aw, ap = selected(uid, kind, item["after"])
                _, bp = selected(uid, kind, item["before"], historical=True)
                witnesses = {"english": ew, kind: aw}
                passage = {"edition": kind, "patch_index": index, "english": ep, "after": ap, "before": bp}
                if "before_role" in item:
                    passage["before_role"] = item["before_role"]
                if "classical" in item:
                    witnesses["classical"], passage["classical"] = selected(uid, "classical", item["classical"])
                occurrence_specs.append({"witnesses": witnesses, "unit_id": uid, "dated_family": "20260907"})
                passages.append(passage)
            before = "\n\n".join(p["before"]["literal"] for p in passages)
            changed_kinds = {item["edition"] for item in choice["literal_review_occurrences"]}
            enriched = dict(choice, before_arabic=before, recording_mode=choice.get("recording_mode", payload["recording_mode"]),
                            basis=choice.get("basis", choice.get("classification")),
                            edition="msa-and-classical" if changed_kinds == {"msa", "classical"} else next(iter(changed_kinds)))
            fields = dated_fields(enriched, payload)
            fields["literal_source_passages"] = passages
            specs[CONSOLIDATED_PREFIX + choice["decision_id"]] = {
                "payload": payload, "terms": enriched, "identity": identity, "unit_id": uid,
                "finding_id": choice["finding_id"], "qualification": False, "classification": None,
                "witnesses": occurrence_specs[0]["witnesses"], "occurrence_specs": occurrence_specs,
                "dated_family": "20260907", "changed_edition": enriched["edition"], "canonical_choice": choice,
                "expected_fields": fields, "historical": {"sources": [histories[(uid, kind)][1]
                    for kind in ("msa", "classical") if (uid, kind) in histories], "status": HISTORICAL_STATUS}}
    require(len(specs) == 8 and sum(len(s["occurrence_specs"]) for s in specs.values()) == 16,
            "consolidated eight-choice/sixteen-occurrence inventory mismatch")
    attach_display_contracts(repo, specs, inventory)
    return specs, ledgers, inventory


def next_repair_expectations(repo, english_root):
    """Independent 16-choice admission, including historical source transitions.

    Read the raw ledgers and source bytes, never the producer or its output.
    Exact old contexts remain evidence; displayed locations are current phrases.
    """
    baseline_raw = bounded_bytes(repo / "evidence/classical/BASELINE.json")
    baseline = {u["id"]: u for u in json.loads(baseline_raw)["units"]}
    inventory = {str(repo / "evidence/classical/BASELINE.json"): byte_digest(baseline_raw)}
    specs, ledgers = {}, []
    for logical, contract in NEXT_REPAIR_LEDGERS.items():
        raw = bounded_bytes(repo / logical)
        require(byte_digest(raw) == contract[0], "next repair ledger identity mismatch")
        payload = json.loads(raw)
        require(payload["schema"] == contract[1] and payload["assessed_on"] == "2026-09-07"
                and payload["open_to_correction"] is True, "next repair schema/date/provisional mismatch")
        identity = {"path": logical, "sha256": byte_digest(raw), "bytes": len(raw)}
        inventory[str(repo / logical)] = byte_digest(raw)
        ledgers.append(identity)
        choices, trans = payload["decisions"], payload["transactions"]
        require(tuple(c["decision_id"] for c in choices) == contract[4], "next repair decision inventory mismatch")
        require(len(trans) == contract[2] and sum(len(t["patches"]) for t in trans) == contract[3], "next repair transaction inventory mismatch")
        sources, histories, tx = {}, {}, {}
        for item in payload["primary_source_inventory"]:
            kind = item["edition"]
            root = english_root if kind == "english" else repo
            field = {"english": "source_path", "msa": "arabic_path", "classical": "target_path"}.get(kind)
            candidates = ["shared"] if kind == "shared" else [uid for uid, b in baseline.items()
                if (root / b[field]).resolve() == (root / item["path"]).resolve()]
            require(len(candidates) == 1, "next repair source has no unique baseline unit")
            uid = item.get("unit_id", candidates[0])
            require(uid == candidates[0], "next repair unit/path mismatch")
            path = (baseline[uid][{"english": "source_path", "msa": "arabic_path", "classical": "target_path"}[kind]]
                    if kind != "shared" else "source/locale/ar/open-logic-config.sty")
            require((root / item["path"]).resolve() == (root / path).resolve(), "next repair source path mismatch")
            declaration = {"path": path, "sha256": item["after_sha256"], "bytes": item["after_bytes"]}
            data = historical_version_bytes(root, declaration, inventory)
            require((uid, kind) not in sources, "next repair duplicate source identity")
            if kind == "english":
                require(same_hash(byte_digest(data), baseline[uid]["english_sha256"]), "next repair frozen English mismatch")
            sources[(uid, kind)] = (data, declaration)
        for t in trans:
            uid, kind = t["unit_id"], t["edition"]
            data, declaration = sources[(uid, kind)]
            require(kind in {"msa", "classical"} and (uid, kind) not in tx, "next repair repeated/non-Arabic transaction")
            require(t["path"] == declaration["path"] and same_hash(t["after_sha256"], byte_digest(data))
                    and t["after_bytes"] == len(data), "next repair after identity mismatch")
            before, history = before_history(data, t["patches"], {"path": t["path"], "sha256": t["before_sha256"], "bytes": t["before_bytes"]})
            history["sha256"] = history["sha256"].upper()
            histories[(uid, kind)] = (before, history)
            tx[(uid, kind)] = t
            for p in t["patches"]:
                require(p["occurrences"] == 1 and bool(p["decision_ids"]) and set(p["decision_ids"]) <= set(contract[4]),
                        "next repair patch ownership mismatch")
                for phase, body in (("before", before), ("after", data)):
                    loc = p[phase + "_location"]
                    require(body[loc["byte_start"]:loc["byte_end"]] == p[phase].encode(), "next repair patch bytes mismatch")
                    require(exact_excerpt(body, loc["line_start"], loc["line_end"]) == loc["excerpt"], "next repair patch lines mismatch")
        for choice in choices:
            for w in choice.get("source_witnesses", []) + choice.get("primary_evidence_before", []):
                uid, kind = w["unit_id"], w["edition"]
                if (uid, kind) not in sources:
                    root = english_root if kind == "english" else repo
                    expected = baseline[uid][{"english": "source_path", "msa": "arabic_path", "classical": "target_path"}[kind]]
                    require((root / w["path"]).resolve() == (root / expected).resolve(), "support witness baseline mismatch")
                    declaration = {"path": expected, "sha256": w["sha256"], "bytes": w["bytes"]}
                    sources[(uid, kind)] = (source_bytes(root, declaration, inventory), declaration)
                data, declaration = sources[(uid, kind)]
                if w.get("phase", "before") == "before" and (uid, kind) in histories:
                    data = histories[(uid, kind)][0]
                root = english_root if kind == "english" else repo
                require((root / w["path"]).resolve() == (root / declaration["path"]).resolve(), "next repair witness path mismatch")
                identity_bytes(data, w, "next repair primary witness")
                require(exact_excerpt(data, w.get("line_start", w.get("start_line")), w.get("line_end", w.get("end_line")))
                    == w.get("excerpt", w.get("quote")), "next repair primary witness lines mismatch")
                if "byte_start" in w:
                    require(data[w["byte_start"]:w["byte_end"]] == w["literal"].encode(), "next repair witness exact bytes mismatch")
            matches = [(uid, kind, i, p) for (uid, kind), t in tx.items() for i, p in enumerate(t["patches"])
                       if choice["decision_id"] in p["decision_ids"]]
            require(matches and len({u for u, _, _, _ in matches}) == 1, "next repair invalid choice patch inventory")
            uid = matches[0][0]
            passages, occurrence_specs = [], []
            for _, kind, index, p in matches:
                data, declaration = sources[(uid, kind)]
                en, en_id = sources[(uid, "english")]
                supplied = next((o for o in choice.get("literal_review_occurrences", [])
                    if o["edition"] == kind and o["patch_index"] == index), None)
                if supplied:
                    anchor = supplied["english"]
                else:
                    w = next(w for w in choice.get("source_witnesses", []) + choice.get("primary_evidence_before", [])
                        if w["edition"] == "english" and w["unit_id"] == uid)
                    anchor = {"literal": w.get("literal", w.get("quote")), "line_start": w.get("line_start", w.get("start_line")),
                        "line_end": w.get("line_end", w.get("end_line"))}
                preferred = NEXT_ENGLISH_PHRASES.get(choice["decision_id"])
                if preferred:
                    literal = preferred[index] if len(preferred) > 1 else preferred[0]
                    contexts = [w.get("literal", w.get("quote", "")) for w in
                        choice.get("source_witnesses", []) + choice.get("primary_evidence_before", [])
                        if w["edition"] == "english" and w["unit_id"] == uid]
                    require(any(active_phrase(c, literal, "english") for c in contexts), "selected English phrase outside canonical witnesses")
                    anchor = {"literal": literal, "line_start": 1, "line_end": len(en.decode().splitlines())}
                ew, ep = next_literal(en, en_id["path"], "english", anchor["literal"], anchor["line_start"], anchor["line_end"])
                bp_loc, ap_loc = p["before_location"], p["after_location"]
                _, bp = next_literal(histories[(uid, kind)][0], declaration["path"], kind, p["before"], bp_loc["line_start"], bp_loc["line_end"])
                assessed, assessed_public = next_literal(data, declaration["path"], kind, p["after"], ap_loc["line_start"], ap_loc["line_end"])
                aw, ap = current_literal(repo, kind, assessed, inventory)
                passage = {"edition": kind, "patch_index": index, "english": ep, "before": bp, "after": ap}
                if ap != assessed_public:
                    passage["assessed_after"] = assessed_public
                    passage["before_role"] = "Before and assessed-after are historical stages; the linked after passage is verified current wording."
                passages.append(passage)
                occurrence_specs.append({"unit_id": uid, "witnesses": {"english": ew, kind: aw}, "dated_family": "20260907"})
            enriched = dict(choice, unit_id=uid, finding_id=choice.get("finding_id", choice["decision_id"]),
                chosen_arabic=choice.get("chosen_arabic") or "\n\n".join(dict.fromkeys(p["after"]["literal"] for p in passages)),
                sense=choice.get("sense") or choice["english_term"], basis=choice.get("basis") or "contextual-semantic-source-correction",
                recording_mode=choice.get("recording_mode", payload["recording_mode"]),
                edition="msa-and-classical" if {k for _, k, _, _ in matches} == {"msa", "classical"} else matches[0][1],
                before_arabic="\n\n".join(p["before"]["literal"] for p in passages))
            fields = dated_fields(enriched, payload)
            fields["literal_source_passages"] = passages
            specs[CONSOLIDATED_PREFIX + choice["decision_id"]] = {"payload": payload, "terms": enriched, "identity": identity,
                "unit_id": uid, "finding_id": enriched["finding_id"], "qualification": False, "classification": None,
                "witnesses": occurrence_specs[0]["witnesses"], "occurrence_specs": occurrence_specs, "dated_family": "20260907",
                "changed_edition": enriched["edition"], "canonical_choice": choice, "expected_fields": fields,
                "historical": {"sources": [histories[(uid, k)][1] for k in ("msa", "classical") if (uid, k) in histories], "status": HISTORICAL_STATUS}}
    require(len(specs) == 16 and sum(len(s["occurrence_specs"]) for s in specs.values()) == 26,
            "next repair sixteen-choice/twenty-six-occurrence inventory mismatch")
    attach_display_contracts(repo, specs, inventory)
    return specs, ledgers, inventory


def validate_repair_record(row, spec, errors):
    key = row["decision_id"]
    def problem(message):
        errors.append(key + ": " + message)
    if spec.get("dated_family") == "20260907" and key != CONSOLIDATED_PREFIX + spec["canonical_choice"]["decision_id"]:
        problem("canonical dated decision namespace mismatch")
    for field, value in expected_repair_fields(spec).items():
        if field not in row or row[field] != value:
            problem("canonical repair field mismatch: " + field)
    display = row.get("review_display", {})
    for field in ("english_term", "chosen_arabic", "before_arabic", "rationale", "expert_question"):
        registry = spec.get("display_registries", {}).get(
            "arabic" if field in {"chosen_arabic", "before_arabic"} else "english")
        if display and (field not in display or
                surface_literal(display[field], registry) != surface_literal(expected_repair_fields(spec)[field], registry)):
            problem("repair display changes a canonical literal/explanation: " + field)
    if not row.get("index_metadata", {}).get("human_index_included"):
        problem("repair excluded from human index")
    repair = row.get("semantic_propagation_repair", {})
    identity = spec["identity"]
    if (repair.get("ledger_path") != identity["path"] or
            not same_hash(repair.get("ledger_sha256"), identity["sha256"]) or
            repair.get("source_ledger") != spec["payload"] or
            repair.get("finding_id") != spec["finding_id"] or
            repair.get("assessed_on") != spec["payload"]["assessed_on"]):
        problem("complete canonical repair provenance mismatch")
    if spec.get("dated_family"):
        if (repair.get("choice_record") != spec["canonical_choice"] or
                repair.get("changed_edition") != spec["changed_edition"]):
            problem("complete separate choice/edition provenance mismatch")
    if spec.get("witness_refreshes"):
        expected_refreshes = [{"path": item["path"], "sha256": item["sha256"].upper(), "bytes": item["bytes"],
                               "source_ledger": item["source_companion"]} for item in spec["witness_refreshes"]]
        actual_refreshes = repair.get("current_witness_companions")
        if isinstance(actual_refreshes, list):
            actual_refreshes = [{**item, "sha256": str(item.get("sha256", "")).upper()} for item in actual_refreshes]
        if actual_refreshes != expected_refreshes:
            problem("complete dated current-witness refresh provenance mismatch")
    source = row.get("source_record", {})
    if (source.get("path") != identity["path"] or source.get("bytes") != identity["bytes"] or
            not same_hash(source.get("sha256"), identity["sha256"])):
        problem("source ledger identity mismatch")
    history = repair.get("historical_before_source", {})
    for field, value in spec["historical"].items():
        matches = same_hash(history.get(field), value) if field == "sha256" else history.get(field) == value
        if not matches:
            problem("inverse-proved historical before source mismatch: " + field)
    if spec["qualification"]:
        inherited = not spec["classification"].startswith("translation-")
        if (repair.get("classification") != spec["classification"] or
                repair.get("inherited_source_qualification") is not inherited or
                repair.get("translation_scope_clarification") is not (not inherited)):
            problem("English fault / Arabic ambiguity classification mismatch")
    if "choice" in spec:
        if (repair.get("choice_record") != spec["choice"] or
                repair.get("choice_id") != spec["choice"]["choice_id"] or
                repair.get("parent_finding_id") != spec["finding_id"] or
                repair.get("proof_scope") != "Exact subchoice within the complete unit repair; its patch is not applied twice."):
            problem("separate connective provenance mismatch")
    occurrences = row.get("occurrences", [])
    occurrence_specs = spec.get("occurrence_specs", [spec])
    if len(occurrences) != len(occurrence_specs) or any(o.get("unit_id") != spec["unit_id"] for o in occurrences):
        problem("repair raw occurrence inventory mismatch")
        return
    normalized = row.get("index_metadata", {}).get("occurrences", [])
    if len(normalized) != len(occurrence_specs) or any(o.get("unit", {}).get("unit_id") != spec["unit_id"] for o in normalized):
        problem("repair human occurrence inventory mismatch")
        return
    if spec.get("dated_family") == "20260907":
        # Producer normalization may reorder independent passages. Match the
        # raw and human groups separately by their canonical source signatures.
        def raw_key(occ):
            return tuple(sorted((kind, group.get("path"), loc.get("line_start"), loc.get("line_end"))
                for kind, group in occ.items() if kind in {"english", "msa", "classical"}
                for loc in group.get("locators", [])))
        def human_key(occ):
            return tuple(sorted((loc.get("source_kind"), loc.get("logical_path"),
                loc.get("line_reconciliation", {}).get("current_line_start"),
                loc.get("line_reconciliation", {}).get("current_line_end")) for loc in occ.get("locations", [])))
        raw_map, human_map = {raw_key(o): o for o in occurrences}, {human_key(o): o for o in normalized}
        wanted = {tuple(sorted((kind, w["path"], start, end) for kind, w in s["witnesses"].items()
                     for start, end in literal_ranges(w, kind))): s for s in occurrence_specs}
        if (len(raw_map) != len(occurrences) or len(human_map) != len(normalized) or
                raw_map.keys() != wanted.keys() or human_map.keys() != wanted.keys()):
            problem("consolidated raw/human canonical occurrence signatures differ or repeat")
            return
        for signature, location_spec in wanted.items():
            validate_repair_locations(raw_map[signature], human_map[signature], location_spec, problem)
        return
    for raw, human, location_spec in zip(occurrences, normalized, occurrence_specs):
        validate_repair_locations(raw, human, location_spec, problem)


def validate_repair_locations(raw, human, spec, problem):
    raw_ranges, human_ranges = {}, {}
    for kind, witness in spec["witnesses"].items():
        group = raw.get(kind, {})
        if group.get("path") != witness["path"] or not same_hash(group.get("sha256"), witness["sha256"]):
            problem(kind + " raw live identity mismatch")
        locators = group.get("locators", [])
        if not locators:
            problem(kind + " missing source-located phrase")
        raw_ranges[kind] = set()
        human_ranges[kind] = set()
        for locator in locators:
            try:
                start, end = locator["line_start"], locator["line_end"]
                excerpt = exact_excerpt(witness["data"], start, end)
                require(witness["line_start"] <= start <= end <= witness["line_end"], "outside canonical witness")
                require(excerpt == locator.get("excerpt"), "wrong exact raw excerpt")
                require(active_phrase(excerpt, witness["term"], kind), "active literal phrase absent")
                raw_ranges[kind].add((start, end))
            except (ValueError, KeyError, TypeError) as exc:
                problem(kind + " raw locator invalid: " + str(exc))
        if spec.get("dated_family"):
            if raw_ranges[kind] != literal_ranges(witness, kind):
                problem(kind + " raw locators do not enumerate every exact canonical literal occurrence")
            if len(locators) != len(raw_ranges[kind]):
                problem(kind + " duplicate raw locator")
    for loc in human.get("locations", []):
        kind = loc.get("source_kind")
        if kind not in spec["witnesses"]:
            problem("unexpected human source kind")
            continue
        witness = spec["witnesses"][kind]
        rec = loc.get("line_reconciliation", {})
        try:
            start, end = rec["current_line_start"], rec["current_line_end"]
            require(rec.get("resolved") is True and rec.get("recorded_hash_matches_current") is True,
                    "unresolved or stale human locator")
            require(loc.get("human_review_included") is not False, "excluded human locator")
            require(loc.get("logical_path") == witness["path"] and
                    same_hash(loc.get("current_sha256"), witness["sha256"]), "human live identity mismatch")
            require(witness["line_start"] <= start <= end <= witness["line_end"], "human locator outside canonical witness")
            excerpt = exact_excerpt(witness["data"], start, end)
            require(excerpt == loc.get("current_excerpt") and active_phrase(excerpt, witness["term"], kind),
                    "wrong exact human source-located phrase")
            require(not loc.get("page_evidence"), "unverified final PDF page evidence in source-only repair")
            human_ranges[kind].add((start, end))
        except (ValueError, KeyError, TypeError) as exc:
            problem(kind + " human locator invalid: " + str(exc))
    if raw_ranges != human_ranges:
        problem("raw versus human locator coverage differs")
    if spec.get("dated_family") and len(human.get("locations", [])) != sum(map(len, human_ranges.values())):
        problem("duplicate human locator")


def visible(value):
    return " ".join(html.unescape(re.sub(r"</?(?:span|a|br|em|strong)\b[^>]*>", "", str(value))).split())


def read_display_registry(data):
    """Read the small declarative token subset in the hash-pinned sources.

    This is intentionally not a TeX interpreter or an import of the producer.
    A declaration outside the supported grammar fails closed instead of being
    silently skipped. Values and article overrides come from the actual files.
    """
    text = re.sub(r"(?<!\\)%[^\n]*", "", data.decode("utf-8-sig"))
    group = r"\{([^{}]*)\}"
    declarations = re.compile(r"\\settexttoken\s*" + group + r"\s*(\*)?\s*" + group +
                              r"\s*" + group + r"(?:\s*\[([^\[\]]*)\])?(?:\s*\[([^\[\]]*)\])?")
    overrides = re.compile(r"\\definetoken\s*" + group + r"\s*" + group + r"\s*" + group)
    matches = list(declarations.finditer(text))
    switches = list(overrides.finditer(text))
    require(len(matches) == len(re.findall(r"\\settexttoken\b", text)) and
            len(switches) == len(re.findall(r"\\definetoken\b", text)), "unsupported display registry declaration")
    result = {}
    for match in matches:
        token, star, singular, plural, capital_s, capital_p = match.groups()
        token, singular, plural = (" ".join(s.split()) for s in (token, singular, plural))
        result.update({("s", token): singular, ("p", token): plural,
                       ("S", token): capital_s if capital_s is not None else singular[:1].upper() + singular[1:],
                       ("P", token): capital_p if capital_p is not None else plural[:1].upper() + plural[1:],
                       ("a", token): "an" if star else "a", ("A", token): "An" if star else "A"})
    for match in switches:
        switch, token, value = (" ".join(s.split()) for s in match.groups())
        result[(switch, token)] = value
    return result


def attach_display_contracts(repo, specs, inventory):
    registries = {}
    inherited = {}
    for language, (path, expected_hash) in zip(("english", "arabic"), DISPLAY_REGISTRY_SOURCES.items()):
        data = bounded_bytes(repo / path)
        require(same_hash(byte_digest(data), expected_hash), "pinned display registry source hash mismatch: " + path)
        inventory[str(repo / path)] = byte_digest(data)
        inherited = {**inherited, **read_display_registry(data)}
        registries[language] = inherited
    for spec in specs.values():
        spec["display_registries"] = registries


def surface_literal(value, registry=None):
    """Normalize presentation syntax without deleting mathematical operators.

    Only the four standard operators in the commissioned repair prose are
    aliased here. Unknown commands remain literal: removing or renaming one
    cannot make a corrupt display agree. Token expansion uses pinned sources.
    """
    text = visible(value)
    if registry is not None:
        def token(match):
            capital, article, name, plural = match.groups()
            switch = ("p" if plural else "s")
            if capital:
                switch = switch.upper()
            require((switch, name) in registry, "unregistered display token: " + name)
            replacement = registry[(switch, name)]
            if article:
                article_switch = "A" if capital else "a"
                require((article_switch, name) in registry, "unregistered display article: " + name)
                replacement = registry[(article_switch, name)] + " " + replacement
            return replacement.strip()
        text = re.sub(r"!!(\^)?(a)?\{([^{}]+)\}(s)?", token, text)
        def explicit_token(match):
            switch, name = match.groups()
            require((switch, name) in registry, "unregistered explicit display token: " + name)
            return registry[(switch, name)]
        text = re.sub(r"\\(?:use|print)token\{([^{}]+)\}\{([^{}]+)\}", explicit_token, text)
    for command, symbol in (("in", "∈"), ("subseteq", "⊆"), ("bigcup", "⋃"), ("setminus", "∖")):
        text = re.sub(r"\\" + command + r"\b", lambda _m: symbol, text)
    text = re.sub(r"\\(?:emph|texttt|textbf)\s*\{([^{}]*)\}", r"\1", text)
    return " ".join(text.replace("$", "").replace("~", " ").split())


def canonical_csv_locator_groups(spec):
    """One exact source-line multiset per independently proved occurrence."""
    groups = []
    for occurrence in spec.get("occurrence_specs", [spec]):
        locators = []
        for kind, witness in occurrence["witnesses"].items():
            ranges = (literal_ranges(witness, kind) if occurrence.get("dated_family") else
                      {(witness["line_start"], witness["line_end"])})
            locators.extend((witness["path"], start, end) for start, end in ranges)
        groups.append(tuple(sorted(locators)))
    return groups


def parsed_csv_locators(value):
    return tuple(sorted((m[0], int(m[1]), int(m[2] or m[1])) for m in re.findall(
        r"([^\s|]+):L(\d+)(?:–L(\d+))?(?=$|[\s|])", value)))


def decision_sections(body):
    """ID-scoped sections prevent one shared reason from certifying another ID."""
    matches = list(re.finditer(r"^- \*\*ID / الرقم:\*\* `([^`]+)`", body, re.M))
    references = dict(re.findall(r"^\[([^\]]+)\]:\s*(\S+)", body, re.M))
    result = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        # Stop at the following anchor as well, excluding the next heading.
        next_anchor = body.find('<a id="', match.end(), end)
        section = body[match.start():next_anchor if next_anchor >= 0 else end]
        section = re.sub(r"^\[[^\]]+\]:\s*\S+.*$", "", section, flags=re.M)
        used = re.findall(r"\[[^\]\n]*\]\[([^\]]+)\]", section)
        section += "\n" + "\n".join(references[key] for key in dict.fromkeys(used) if key in references)
        result.setdefault(match.group(1), []).append(section)
    return result


def validate_explanations(key, rationale, question, surfaces, csv_rows, errors, spec=None, flagged=True, locations=None):
    reason, question = visible(rationale), visible(question)
    for surface, sections in surfaces.items():
        relevant = sections.get(key, [])
        required = surface in {"complete", "priority"} or surface.startswith("complete-") or surface.startswith("priority-")
        if surface == "priority" and not flagged:
            required = False
        if surface in {"complete", "priority"} and required and not relevant:
            errors.append(key + ": missing decision section: " + surface)
        for section in relevant:
            why = next((line for line in section.splitlines() if "**Why this choice / سبب الاختيار:**" in line), "")
            questions = " ".join(line for line in section.splitlines() if
                                 "**Please double-check / يُرجى التحقق:**" in line or
                                 "PLEASE DOUBLE-CHECK THIS CHOICE" in line)
            if not reason or reason not in visible(why):
                errors.append(key + ": missing/truncated full reason: " + surface)
            if question and question not in visible(questions):
                errors.append(key + ": missing/truncated full expert question: " + surface)
            if spec:
                text = visible(section)
                registry = spec.get("display_registries", {}).get("arabic")
                provenance_match = re.search(
                    r"^- \*\*New repair assessment / تقييم تصحيحي جديد:\*\*.*?(?=^- |\Z)",
                    section, re.M | re.S)
                provenance = provenance_match.group(0) if provenance_match else ""
                if (surface_literal(spec["terms"]["before_arabic"], registry) not in surface_literal(provenance, registry) or
                        spec["payload"]["assessed_on"] + "; not the original translator's deliberation." not in visible(provenance) or
                        spec["identity"]["path"] not in unquote(section)):
                    errors.append(key + ": missing complete dated/previous-wording provenance: " + surface)
                if spec.get("dated_family") == "20260907":
                    actual_passages = [line for line in section.splitlines() if "**Literal source passage / اللفظ في موضعه:**" in line]
                    expected_passages = spec["expected_fields"]["literal_source_passages"]
                    if len(actual_passages) != len(expected_passages):
                        errors.append(key + ": missing literal before/after/source passage inventory: " + surface)
                    for line, passage in zip(actual_passages, expected_passages):
                        for phase, language in (("english", "english"), ("before", "arabic"), ("after", "arabic")):
                            registry = spec["display_registries"][language]
                            if surface_literal(passage[phase]["literal"], registry) not in surface_literal(line, registry):
                                errors.append(key + ": altered literal " + phase + " passage: " + surface)
                        if passage.get("before_role") and passage["before_role"] not in visible(line):
                            errors.append(key + ": missing insertion-context qualification: " + surface)
                if spec["qualification"]:
                    label = "Translation-scope clarification" if spec["unit_id"] == "OLP-0081" else "Inherited-source qualification"
                    other = "Inherited-source qualification" if spec["unit_id"] == "OLP-0081" else "Translation-scope clarification"
                    if label not in text or other in text:
                        errors.append(key + ": wrong rendered scope classification: " + surface)
                for location in locations or []:
                    rec = location.get("line_reconciliation", {})
                    start, end = rec.get("current_line_start"), rec.get("current_line_end")
                    suffix = "#L" + str(start) + ("-L" + str(end) if end != start else "")
                    wanted = location.get("logical_path", "") + suffix
                    if not re.search(re.escape(wanted) + r"(?=$|[\s)>])", unquote(section)):
                        errors.append(key + ": missing exact human source link: " + surface + ":" + str(location.get("source_kind")))
    for prefix in ("complete-", "priority-") if flagged else ("complete-",):
        if not any(key in sections for name, sections in surfaces.items() if name.startswith(prefix)):
            errors.append(key + ": missing detailed shard: " + prefix)
    rows = csv_rows.get(key, [])
    if not rows:
        errors.append(key + ": missing CSV occurrence")
    expected_groups = canonical_csv_locator_groups(spec) if spec else []
    if spec and not spec.get("dated_family") and locations is not None:
        # The older twelve-repair contract permits either a complete witness
        # passage or its narrower literal-containing lines. These locations
        # have already been checked against live bytes and the canonical
        # witness by validate_repair_record. Preserve that contract while
        # requiring CSV to reproduce its exact validated raw/human inventory.
        expected_groups = [tuple(sorted((loc["logical_path"],
            loc["line_reconciliation"]["current_line_start"],
            loc["line_reconciliation"]["current_line_end"]) for loc in locations))]
    actual_groups = []
    for values in rows:
        if len(values) != 13 or reason not in visible(values[5]):
            errors.append(key + ": missing/truncated full CSV reason")
        if spec and len(values) == 13:
            registries = spec.get("display_registries", {})
            if (surface_literal(spec["terms"]["chosen_arabic"], registries.get("arabic")) !=
                    surface_literal(values[3], registries.get("arabic")) or
                    surface_literal(expected_repair_fields(spec)["english_term"], registries.get("english")) not in
                    surface_literal(values[2], registries.get("english"))):
                errors.append(key + ": CSV literal source/chosen phrase mismatch")
            if values[9].strip() or values[10].strip():
                errors.append(key + ": invented final PDF page in source-only repair CSV")
            group = parsed_csv_locators(values[8])
            actual_groups.append(group)
            if group not in expected_groups:
                errors.append(key + ": missing exact CSV source locator: occurrence group mismatch")
            if not re.match(re.escape(spec["unit_id"]) + r"(?=$|\s)", values[7]):
                errors.append(key + ": wrong CSV occurrence unit")
    if spec and (len(rows) != len(expected_groups) or Counter(actual_groups) != Counter(expected_groups)):
        errors.append(key + ": repair CSV occurrence inventory mismatch")
    if question and rows and not any(len(values) == 13 and question in visible(values[12]) for values in rows):
        errors.append(key + ": missing/truncated full CSV expert question")


def history_fingerprint(row):
    """Keep the old raw lexical assessment, not its changing display metadata."""
    original = (row.get("expert_review_assessment") or {}).get("original_fields", {})
    values = {field: original[field] if field in original else row.get(field) for field in HISTORY_FIELDS}
    return byte_digest(json.dumps(values, ensure_ascii=False, sort_keys=True).encode("utf-8"))


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def decisions(path):
    active = False
    block = []
    with path.open(encoding="utf-8-sig") as stream:
        for line in stream:
            if line.rstrip() == '  "decisions": [':
                active = True
                continue
            if not active:
                continue
            if line.rstrip() == "  ],":
                if block:
                    raise ValueError("truncated decision block")
                return
            if line.startswith("    {"):
                block = [line]
            elif block:
                block.append(line)
            if line.rstrip() in ("    },", "    }") and block:
                yield json.loads("".join(block).rstrip().rstrip(","))
                block = []
    raise ValueError("missing/truncated decisions array")


def check(repo, snapshot, previous, english_root=None, *, include_new_repairs=True):
    errors = []
    counts = Counter()
    statuses = Counter()
    expected = {}
    ledger_identities = []
    if english_root is None:
        english_root = repo.parent.parent / "openlogic-interfarsi/repo/source/upstream"
    repairs, repair_ledgers, repair_inputs = {}, [], {}
    try:
        repairs, repair_ledgers, repair_inputs = repair_expectations(repo, english_root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append("independent canonical repair input verification failed: " + str(exc))
    if include_new_repairs:
        try:
            newer, ledgers, inputs = new_repair_expectations(repo, english_root)
            require(not (repairs.keys() & newer.keys()), "duplicate commissioned repair decision ID")
            repairs.update(newer)
            repair_ledgers.extend(ledgers)
            repair_inputs.update(inputs)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append("independent additional repair input verification failed: " + str(exc))
        try:
            newer, ledgers, inputs = consolidated_repair_expectations(repo, english_root)
            require(not (repairs.keys() & newer.keys()), "duplicate consolidated repair decision ID")
            repairs.update(newer)
            repair_ledgers.extend(ledgers)
            repair_inputs.update(inputs)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append("independent consolidated repair input verification failed: " + str(exc))
        try:
            newer, ledgers, inputs = next_repair_expectations(repo, english_root)
            require(not (repairs.keys() & newer.keys()), "duplicate next-batch repair decision ID")
            repairs.update(newer)
            repair_ledgers.extend(ledgers)
            repair_inputs.update(inputs)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append("independent next-batch repair input verification failed: " + str(exc))
    for path in sorted((repo / "evidence/provenance/locale-ar/expert-review-amendments").glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        ledger_identities.append({"path": path.relative_to(repo).as_posix(), "sha256": digest(path)})
        for row in payload["amendments"]:
            if row["decision_id"] in expected:
                errors.append("duplicate assessment " + row["decision_id"])
            expected[row["decision_id"]] = row
    full_md = (snapshot / "EXPERT_REVIEW_INDEX.md").read_text(encoding="utf-8-sig")
    priority_md = (snapshot / "EXPERT_REVIEW_PRIORITY_ONLY.md").read_text(encoding="utf-8-sig")
    shards = sorted((snapshot / "reviewer-index").glob("*.md"))
    surfaces = {"complete": decision_sections(full_md), "priority": decision_sections(priority_md)}
    for path in shards:
        if path.name.startswith(("complete-", "priority-")):
            surfaces[path.stem] = decision_sections(path.read_text(encoding="utf-8-sig"))
    csv_rows = {}
    required_csv_ids = set(expected) | set(repairs)
    try:
        with (snapshot / "EXPERT_REVIEW_OCCURRENCES.csv").open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream)
            header = next(reader)
            require(len(header) == 13 and header[1].startswith("Decision ID") and
                    header[5].startswith("Short rationale") and header[12].startswith("Please double-check"),
                    "unexpected reviewer CSV header")
            for values in reader:
                if len(values) > 1 and values[1] in required_csv_ids:
                    csv_rows.setdefault(values[1], []).append(values)
    except (OSError, ValueError, StopIteration) as exc:
        errors.append("reviewer CSV unavailable/invalid: " + str(exc))
    ids = set()
    applied = set()
    applied_repairs = set()
    verified_repairs = set()
    history = {}
    for row in decisions(snapshot / "EXPERT_REVIEW_INDEX.json"):
        key = row["decision_id"]
        if key in ids:
            errors.append("duplicate generated decision " + key)
        ids.add(key)
        history[key] = history_fingerprint(row)
        counts["raw_decisions"] += 1
        metadata = row.get("index_metadata", {})
        human = bool(metadata.get("human_index_included"))
        if human:
            counts["human_decisions"] += 1
            flagged = bool(row.get("expert_review_useful"))
            counts["flagged_decisions"] += flagged
            counts["flagged_missing_explicit_question"] += flagged and not bool(row.get("expert_question"))
            counts["missing_sense"] += not bool(row.get("sense"))
            counts["retrospective_template_rationales"] += (
                "This is a present-tense retrospective justification" in row.get("rationale", ""))
            for occurrence in metadata.get("occurrences", []):
                if occurrence.get("human_review_included") is False:
                    continue
                counts["human_occurrence_groups"] += 1
                locs = [loc for loc in occurrence.get("locations", [])
                        if loc.get("human_review_included") is not False]
                counts["occurrence_groups_without_supplied_locations"] += not bool(locs)
                for loc in locs:
                    status = loc.get("line_reconciliation", {}).get("status", "missing")
                    statuses[status] += 1
                    counts["unresolved_lexical_locations"] += status.startswith("unresolved-")
        assessment = row.get("expert_review_assessment")
        if key in repairs:
            applied_repairs.add(key)
            prior_errors = len(errors)
            validate_repair_record(row, repairs[key], errors)
            fields = expected_repair_fields(repairs[key])
            validate_explanations(key, fields["rationale"], fields["expert_question"],
                                  surfaces, csv_rows, errors, repairs[key], locations=[
                                      location for occurrence in row.get("index_metadata", {}).get("occurrences", [])
                                      for location in occurrence.get("locations", [])])
            if len(errors) == prior_errors:
                verified_repairs.add(key)
        elif key.startswith((REPAIR_PREFIX, CONSOLIDATED_PREFIX)) or row.get("semantic_propagation_repair"):
            errors.append("uncommissioned/unverified generated repair " + key)
        if key not in expected:
            if assessment:
                errors.append("unexpected applied assessment " + key)
            continue
        approved = expected[key]
        if not isinstance(assessment, dict):
            errors.append("missing applied assessment " + key)
            continue
        applied.add(key)
        if assessment.get("expected") != approved["expected"]:
            errors.append("lost original fields " + key)
        if assessment.get("witnesses") != approved["witnesses"]:
            errors.append("stale assessment witnesses " + key)
        for field, value in approved["changes"].items():
            if row.get(field) != value:
                errors.append("stale current assessment field " + key + ":" + field)
        if row.get("chosen_arabic") != approved["expected"]["chosen_arabic"]:
            errors.append("raw translation choice overwritten " + key)
        original = assessment.get("original_fields", {})
        if original.get("rationale") != approved["expected"]["rationale"]:
            errors.append("original rationale not preserved " + key)
        display = row.get("review_display", {})
        observed = approved.get("observed_arabic_forms") or []
        if observed:
            actual = "؛ ".join(dict.fromkeys(value["form"] for value in observed))
            if display.get("chosen_arabic") != actual:
                errors.append("wrong observed wording display " + key)
            counts["observed_arabic_forms"] += len(observed)
        full_reason = ("Current assessment (" + approved["assessed_on"] + "; open to correction): "
                       + display.get("rationale", ""))
        validate_explanations(key, full_reason, display.get("expert_question", row.get("expert_question", "")),
                              surfaces, csv_rows, errors, flagged=bool(row.get("expert_review_useful")))
        # A rejected locator may be replaced by a source-checked context row
        # for the same unit.  That replacement is active evidence, not the
        # retired occurrence being tested for removal; identify it by the
        # amendment's explicit replacement witness marker.
        active_units = {
            occurrence.get("unit_id") for occurrence in row.get("occurrences", [])
            if not (occurrence.get("expert_source_binding_witness") or
                    str(occurrence.get("context_note", "")).startswith("New source-checked context replacing"))
        }
        preserved_units = {occurrence.get("unit_id") for occurrence in
                           assessment.get("rejected_occurrence_records", [])}
        for rejection in approved.get("rejected_occurrences") or []:
            counts["rejected_wrong_sense_occurrence_groups"] += 1
            if rejection["unit_id"] in active_units or rejection["unit_id"] not in preserved_units:
                errors.append("wrong-sense rejection not applied/preserved " + key)
    if applied != set(expected):
        errors.append("not all approved assessments appear in the generated snapshot")
    missing_repairs = sorted(set(repairs) - applied_repairs)
    if missing_repairs:
        errors.append("commissioned repair assessments missing: " + repr(missing_repairs))
    if previous:
        old_ids = set()
        for old in decisions(previous / "EXPERT_REVIEW_INDEX.json"):
            key = old["decision_id"]
            old_ids.add(key)
            if key in history and history[key] != history_fingerprint(old):
                errors.append("previous raw decision history overwritten: " + key)
        if not old_ids.issubset(ids):
            errors.append("previous raw decisions dropped: " + repr(sorted(old_ids - ids)))
        counts["previous_raw_decisions_preserved"] = len(old_ids & ids)
    counts["applied_assessments"] = len(applied)
    counts["applied_repair_assessments"] = len(applied_repairs)
    counts["independently_verified_repair_assessments"] = len(verified_repairs)
    counts["canonical_repair_assessments_expected"] = len(repairs)
    counts["repair_input_files_verified"] = len(repair_inputs)
    counts["repair_source_locations_expected"] = sum(len(spec["witnesses"]) for spec in repairs.values())
    # Check every local navigation/reference target, not just the first screen.
    docs = sorted(snapshot.glob("*.md")) + shards
    contents = {path.resolve(): path.read_text(encoding="utf-8-sig") for path in docs}
    for doc, body in contents.items():
        refs = dict(re.findall(r"^\[([^\]]+)\]:\s*(\S+)", body, re.M))
        for key in re.findall(r"\[[^\]\n]*\]\[([^\]]+)\]", body):
            counts["reference_link_uses"] += 1
            if key not in refs:
                errors.append("undefined reference in " + doc.name + ":" + key)
        for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", body) + list(refs.values()):
            if target.startswith(("https://", "http://", "mailto:")):
                counts["remote_urls_not_fetched"] += 1
                continue
            name, _, fragment = unquote(target.strip("<>")).partition("#")
            dest = (doc.parent / name).resolve() if name else doc
            counts["local_links_checked"] += 1
            if not dest.is_file():
                errors.append("missing local link " + doc.name + ":" + target)
            elif dest.suffix == ".md" and fragment:
                linked = contents.get(dest)
                if linked is None:
                    linked = dest.read_text(encoding="utf-8-sig")
                if 'id="' + fragment + '"' not in linked:
                    headings = re.findall(r"^#{1,6}\s+(.+)$", linked, re.M)
                    slugs = {re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-") for h in headings}
                    if fragment not in slugs:
                        errors.append("missing local anchor " + doc.name + ":" + target)
    # A source edit while readback was running invalidates this receipt too.
    for name, expected_hash in repair_inputs.items():
        if not same_hash(digest(Path(name)), expected_hash):
            errors.append("repair input changed during independent readback: " + name)
    return {
        "schema": "openlogic-expert-review-snapshot-readback-v1",
        "status": "PASS" if not errors else "FAIL", "counts": dict(counts),
        "location_statuses": dict(statuses), "errors": errors,
        "assessment_ledgers": ledger_identities,
        "semantic_repair_ledgers": repair_ledgers,
        "semantic_repair_input_sha256": repair_inputs,
        "snapshot_json_sha256": digest(snapshot / "EXPERT_REVIEW_INDEX.json"),
        "limitations": ["No final PDF page claim is certified by this check; the dated source-only repairs must not invent one.",
                        "No claim that every actual translation choice has been catalogued.",
                        "Remote URLs were not fetched; local paths and Markdown anchors were checked."],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--english-root", type=Path,
                        help="Frozen English source root; default is the sibling Interfarsi source/upstream.")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = check(args.repo.resolve(), args.snapshot.resolve(),
                   args.previous.resolve() if args.previous else None,
                   args.english_root.resolve() if args.english_root else None)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items()
                      if key in {"status", "counts", "errors", "snapshot_json_sha256"}}))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
