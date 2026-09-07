#!/usr/bin/env python3
"""Generate the bilingual, reviewer-facing Arabic terminology index.

The source ledgers are intentionally more detailed than the human index.  This
program preserves every record in JSON while omitting generic, whole-passage
placeholders from the word/term index.  It also re-resolves recorded excerpts
against the current source tree so moved lines are linked correctly and stale
or ambiguous locators are never presented as verified.

Page evidence is optional until final readers exist.  When supplied, SyncTeX
records provide exact occurrence PDF pages.  If no exact SyncTeX record exists,
an AUX label plus the corresponding PDF named destination may provide only the
unit-start page.  The two evidence grades are kept visibly distinct; this
program never estimates a page by applying an offset.
"""

from __future__ import annotations

import argparse
import csv
import copy
import gzip
import hashlib
import html
import io
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence
from urllib.parse import quote, unquote


GENERIC_PASSAGE_ID = re.compile(r"(?:^|-)passage-OLP-\d{4}$", re.IGNORECASE)
GENERIC_PASSAGE_TERM = "passage-level exposition and semantic qualification"
UNIT_ID = re.compile(r"OLP-(\d{4})$")
SYNC_RECORD = re.compile(r"^[^0-9]*?(\d+),(\d+)(?:,\d+)?:", re.ASCII)

SOURCE_LABELS = {
    "english": "EN",
    "msa": "MSA",
    "classical": "CA",
}

EXPERT_SOURCE_BINDINGS_RELATIVE = Path(
    "evidence/provenance/locale-ar/EXPERT_REVIEW_SOURCE_BINDINGS.json"
)
EXPERT_SOURCE_BINDING_SCHEMA = "openlogic-locale-ar-expert-source-bindings-v1"
EXPERT_SOURCE_BINDING_WITNESS = "expert-audited-hash-bound-semantic-source-v1"
EXPERT_AMENDMENTS_RELATIVE = Path(
    "evidence/provenance/locale-ar/expert-review-amendments"
)
EXPERT_AMENDMENT_SCHEMA = "openlogic-ar-expert-review-amendments-v1"
SEMANTIC_PROPAGATION_REPAIRS = {
    "evidence/classical/repairs/OLP0497_MP_PROPAGATION_20260906.json": (
        "openlogic-semantic-propagation-repair-v1",
        {"OLP-0497": "content/intuitionistic-logic/introduction/axiomatic-derivations.tex"},
    ),
    "evidence/classical/repairs/OLP0079_0093_MP_PROPAGATION_20260906.json": (
        "openlogic-semantic-propagation-repairs-v1",
        {
            "OLP-0079": "content/first-order-logic/sequent-calculus/provability-propositional.tex",
            "OLP-0093": "content/first-order-logic/natural-deduction/provability-propositional.tex",
        },
    ),
}
QUALIFICATION_PROPAGATION_REPAIRS = {
    "evidence/classical/repairs/OLP0005_0008_0016_0018_QUALIFICATION_PROPAGATION_20260906.json": (
        "openlogic-semantic-qualification-repairs-v1",
        {
            "OLP-0005": "content/sets-functions-relations/sets/basics.tex",
            "OLP-0008": "content/sets-functions-relations/sets/unions-and-intersections.tex",
            "OLP-0016": "content/sets-functions-relations/relations/orders.tex",
            "OLP-0018": "content/sets-functions-relations/relations/trees.tex",
        },
    ),
    "evidence/classical/repairs/OLP0033_0039_0072_0081_QUALIFICATION_PROPAGATION_20260906.json": (
        "openlogic-semantic-qualification-repairs-v1",
        {
            "OLP-0033": "content/sets-functions-relations/size-of-sets/non-enumerability.tex",
            "OLP-0039": "content/sets-functions-relations/size-of-sets/non-enumerability-alt.tex",
            "OLP-0072": "content/first-order-logic/sequent-calculus/quantifier-rules.tex",
            "OLP-0081": "content/first-order-logic/sequent-calculus/soundness.tex",
        },
    ),
}
QUALIFICATION_PRIOR_MANIFEST_RELATIVE = Path(
    "evidence/classical/SOURCE_PROPAGATION_PRE_QUALIFICATIONS_20260906.json"
)
QUALIFICATION_PRIOR_MANIFEST_SHA256 = "865EB48A37F5A50876DC5F406ADF432A0360BF1E7C9A5FB5667CAF41D27AA9EC"
QUALIFICATION_PRIOR_MANIFEST_UNITS = frozenset({"OLP-0033", "OLP-0039", "OLP-0072", "OLP-0081"})
QUALIFICATION_PROPAGATION_CLASSIFICATIONS = {
    **{unit: "inherited-source-qualification-already-correct-in-classical"
       for unit in ("OLP-0005", "OLP-0008", "OLP-0016", "OLP-0018", "OLP-0033")},
    "OLP-0039": "inherited-source-implication-scope-already-correct-in-classical",
    "OLP-0072": "inherited-source-scope-clarification-already-correct-in-classical",
    "OLP-0081": "translation-any-versus-none-scope-ambiguity-already-correct-in-classical",
}
QUALIFICATION_PROPAGATION_TERMS = {
    "OLP-0005": ("extensionality", "تضمن الامتدادية أن هناك دائمًا", "إذا وُجدت مجموعة", "قضت الامتدادية بوحدتها"),
    "OLP-0008": ("intersection", "مجموعة من المجموعات", "مجموعة غير خالية من المجموعات", "مجموعة غير خالية من المجموعات"),
    "OLP-0016": ("extension relation", "لكنها ليست ترتيبًا خطيًا", "لكنها ليست ترتيبًا خطيًا بوجه عام", "لا خطي عمومًا"),
    "OLP-0018": ("subtree", "كل مجموعة", "كل مجموعة غير خالية", "كل مجموعة غير خالية"),
    "OLP-0033": ("enumerable", "فلكل مجموعة", "فلكل مجموعة غير خالية", "المجموعة غير الخالية"),
    "OLP-0039": ("nonenumerable", "هو القول", "يقتضي", "يقتضي"),
    "OLP-0072": ("no restrictions", "لا ترد أي قيود على الحد", "لا ترد أي قيود من جهة المتغير المميَّز على الحد", "من جهة المتغير المميَّز"),
    "OLP-0081": ("do not hold", "فإذا لم تتحقق أي منها", "فإذا تخلّفت واحدة على الأقل منها", "فإذا تخلف شيء منها"),
}
APPLIED_SCOPE_LEDGER = "evidence/classical/repairs/OLP0051_0060_0068_SCOPE_PROPAGATION_20260906.json"
APPLIED_DUAL_LEDGER = "evidence/classical/repairs/OLP0067_DUAL_GRAMMAR_20260906.json"
APPLIED_CLASSICAL_LEDGER = "evidence/classical/repairs/OLP0008_CLASSICAL_PROSE_20260906.json"
APPLIED_REPAIR_LEDGERS = {APPLIED_SCOPE_LEDGER, APPLIED_DUAL_LEDGER, APPLIED_CLASSICAL_LEDGER}
CONSOLIDATED_REPAIR_LEDGERS = {
    "evidence/classical/repairs/OLP0375_0376_ARITHMETIC_SCOPE_20260907.json":
        ("042822D86510960C3AE3FC9600DDF273F015BC00ADC09E19C240A7071D265FF5", "openlogic-arithmetic-scope-repairs-v1"),
    "evidence/classical/repairs/OLP0021_TWO_ROOTS_NOTE_20260907.json":
        ("98B939CBA500C9CBE8E591917709940CA0F685C61A0A4965535864E9AEFD7120", "openlogic-square-root-note-repair-v1"),
    "evidence/classical/repairs/OLP0321_0326_0368_SEMANTIC_SCOPE_20260907.json":
        ("3CFF7BA6901F09815BE1EA4F42B2A29074639079FC21B09AE8CB4E6096E899DA", "openlogic-semantic-scope-repairs-v1"),
}
APPLIED_REPAIR_LEDGERS.update(CONSOLIDATED_REPAIR_LEDGERS)
NEXT_BATCH_LEDGERS = {
    "evidence/classical/repairs/OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907.json":
        ("EB0E436D546C867A56D66767A24F66A2D687EA254ED83C9123AA0C2106A8E0C7", "openlogic-classical-construction-repairs-v1", 3, 7,
         ("AR-OLP-0021-CLASSICAL-SUCCESSOR-CONSTRUCTION-20260907", "AR-OLP-0022-CLASSICAL-IDENTITY-PREDICATE-20260907",
          "AR-OLP-0022-CLASSICAL-PIECEWISE-PREDICATE-20260907", "AR-OLP-0022-CLASSICAL-BIJECTIVE-RELATIVE-20260907",
          "AR-OLP-0022-CLASSICAL-BIJECTION-IFF-20260907", "AR-OLP-0024-CLASSICAL-INVERSE-PREDICATE-20260907")),
    "evidence/classical/repairs/OLP0394_0399_0400_0404_0409_MODAL_SCOPE_20260907.json":
        ("6D29D66C0DB082E2C348CF8A30219E9D6AE11B80E14D0ECFDD2CBC2C79A6F4CD", "openlogic-consolidated-modal-semantic-repairs-v1", 10, 15,
         ("AR-OLP-0394-MODAL-FINAL-VALUE-20260907", "AR-OLP-0399-FINITE-GRID-DOMAIN-20260907",
          "AR-OLP-0400-FINITE-PREMISE-CONVERSE-20260907", "AR-OLP-0404-THEOREM-EMPTY-SLOTS-20260907",
          "AR-OLP-0409-MODAL-SCOPE-20260907", "AR-OLP-0409-NECESSITY-WORLD-SCOPE-20260907")),
    "evidence/classical/repairs/OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907.json":
        ("90364663431EA9DAD27FEF1A427ACF033498F1CD95F8CBEA29CC665F41186C79", "openlogic-classical-adjective-construction-repairs-v1", 3, 4,
         ("AR-OLP-0022-CLASSICAL-SURJECTIVE-OPENING-20260907", "AR-OLP-0028-CLASSICAL-ENUMERABLE-OPENING-20260907",
          "AR-OLP-0029-CLASSICAL-DUAL-SURJECTIVE-20260907", "AR-OLP-0029-CLASSICAL-ZERO-INDEXED-ELEMENTS-20260907")),
}
APPLIED_REPAIR_LEDGERS.update(NEXT_BATCH_LEDGERS)
# Only these exact predecessor identities may be reconstructed. Never accept an
# arbitrary stale hash or a matching phrase in a changed whole file.
NEXT_BATCH_HISTORY = {
    ("source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex",
     "8183C83E20FC04CED33D83554EBB142F94B7C8BF323B992336A25B9153DB2498"):
        "evidence/classical/repairs/OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907.json",
    ("source/locale/ar-classical/content/sets-functions-relations/functions/function-kinds.tex",
     "8A73D76A7D09E54A6956468280C054DED5243F4F4A43ED05AEE76DE126DD9CA9"):
        "evidence/classical/repairs/OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907.json",
}
NEXT_BATCH_ENGLISH_LITERALS = {
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
APPLIED_SCOPE_IDS = {
    "OLP-0051": "scope-0051-generated-carrier",
    "OLP-0060": "scope-0060-hypothesis-final-index",
    "OLP-0068": "scope-0068-used-premise-membership",
}
APPLIED_SCOPE_SHA256 = "0C66DD4C3449C9AA8D92A0D904A813D9365942B0EF92D8327420A26B864D5C43"
APPLIED_CLASSICAL_SHA256 = "99EDA5AB0D7714C9FE274CE5A1FCE4F058090CFFF0474C8DA749B80956F1F033"
APPLIED_CLASSICAL_REFRESH = "evidence/classical/repairs/OLP0008_CLASSICAL_WITNESS_REFRESH_20260906.json"
APPLIED_CLASSICAL_REFRESH_SHA256 = "32446183261B9FBE62B916EE8F2262F4624B1831930FE6CA0121B13B61D57A2D"
APPLIED_DUAL_SHA256 = "B6AF652713EDBECB4457D6725790CDC9DE4F0EE4C446F3E3844D2760DDE81EF1"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def read_json_bytes(path: Path) -> tuple[object, bytes]:
    raw = path.read_bytes()
    return json.loads(raw.decode("utf-8-sig")), raw


def apply_expert_review_amendments(
    repo: Path, decisions: list[dict], english_root: Path | None,
    baseline_units: Sequence[dict] = (),
) -> tuple[list[dict], dict[Path, str]]:
    """Apply new assessments only after every original field and witness checks.

    Original ledgers are never rewritten. The generated decision retains its
    former explanation and the exact independently dated assessment. A changed
    source, unexpected decision, or duplicate amendment fails the whole batch.
    These are current semantic assessments, not reconstructed private thoughts.
    """
    root = repo.resolve()
    directory = root / EXPERT_AMENDMENTS_RELATIVE
    by_id = {row["decision_id"]: row for row in decisions}
    if len(by_id) != len(decisions):
        raise ValueError("review amendments require unique decision IDs")
    plans: list[tuple[dict, dict, str]] = []
    identities: list[dict] = []
    hashes: dict[Path, str] = {}
    amended: set[str] = set()
    unit_paths: dict[tuple[str, str], list[str]] = defaultdict(list)
    for unit in baseline_units:
        for kind, field in (("english", "source_path"), ("msa", "arabic_path"),
                            ("classical", "target_path")):
            if unit.get(field):
                unit_paths[(kind, unit[field])].append(unit["id"])
    global_captions = {
        "locale-ar-chosen-8be3b0e9c878f801",  # photo credits
        "locale-ar-chosen-fa3fc341675951b1",  # remixed by
        "locale-ar-chosen-dbda654d0ab634b0",  # license title
    }
    for path in sorted(directory.glob("*.json")):
        payload, raw = read_json_bytes(path)
        logical = path.relative_to(root).as_posix()
        if not isinstance(payload, dict) or payload.get("schema") != EXPERT_AMENDMENT_SCHEMA:
            raise ValueError(f"{logical}: invalid review amendment schema")
        entries = payload.get("amendments")
        if not isinstance(entries, list) or not entries:
            raise ValueError(f"{logical}: empty/malformed review amendments")
        digest = sha256_bytes(raw)
        hashes[path.resolve()] = digest
        identities.append({"path": logical, "bytes": len(raw), "sha256": digest,
                           "amendment_count": len(entries)})
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError(f"{logical}: malformed review amendment")
            decision_id = entry.get("decision_id")
            if decision_id not in by_id or decision_id in amended:
                raise ValueError(f"{logical}: unknown/duplicate amendment {decision_id!r}")
            amended.add(decision_id)
            if (entry.get("recording_mode") != "new-independent-semantic-assessment"
                    or entry.get("open_to_correction") is not True
                    or entry.get("official_attestation_claimed") is not False
                    or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(entry.get("assessed_on", "")))):
                raise ValueError(f"{decision_id}: invalid assessment provenance")
            expected = entry.get("expected")
            decision = by_id[decision_id]
            if (not isinstance(expected, dict)
                    or set(expected) != {"english_term", "chosen_arabic", "rationale"}
                    or any(not isinstance(value, str) or decision.get(key) != value
                           for key, value in expected.items())):
                raise ValueError(f"{decision_id}: original decision fields changed")
            changes = entry.get("changes")
            if (not isinstance(changes, dict)
                    or set(changes) != {"sense", "rationale", "expert_question"}
                    or any(not isinstance(value, str) or not value.strip()
                           for value in changes.values())):
                raise ValueError(f"{decision_id}: assessment must supply sense, rationale and question")
            witnesses = entry.get("witnesses")
            if not isinstance(witnesses, list) or not witnesses:
                raise ValueError(f"{decision_id}: assessment lacks source witnesses")
            kinds: set[str] = set()
            witness_excerpts: list[str] = []
            for witness in witnesses:
                if not isinstance(witness, dict):
                    raise ValueError(f"{decision_id}: malformed source witness")
                kind, relative = witness.get("source_kind"), witness.get("path")
                if kind not in SOURCE_LABELS or not isinstance(relative, str):
                    raise ValueError(f"{decision_id}: invalid witness source/path")
                # Restrict reads to the language source trees, even for a ledger
                # which happens to have a valid-looking checksum and line range.
                base = english_root.resolve() if kind == "english" and english_root else root
                if kind == "english" and english_root is None:
                    raise ValueError(f"{decision_id}: English witness root unavailable")
                expected_prefix = {"english": "content/", "msa": "source/locale/ar/",
                                   "classical": "source/locale/ar-classical/"}[kind]
                if "\\" in relative or not relative.startswith(expected_prefix):
                    raise ValueError(f"{decision_id}: witness outside its language source tree")
                target = (base / relative).resolve()
                allowed = (base / expected_prefix).resolve()
                if not target.is_relative_to(allowed) or not target.is_file():
                    raise ValueError(f"{decision_id}: missing/out-of-scope witness {relative}")
                data = target.read_bytes()
                file_hash = sha256_bytes(data)
                if file_hash != str(witness.get("file_sha256", "")).upper():
                    raise ValueError(f"{decision_id}: witness file hash changed: {relative}")
                start, end = witness.get("line_start"), witness.get("line_end")
                lines = data.decode("utf-8-sig").splitlines()
                if (type(start) is not int or type(end) is not int
                        or not 1 <= start <= end <= len(lines)):
                    raise ValueError(f"{decision_id}: invalid witness line range")
                excerpt = "\n".join(lines[start - 1:end])
                if (not any(line.strip() and not line.lstrip().startswith("%")
                            for line in lines[start - 1:end])
                        or sha256_bytes(excerpt.encode("utf-8"))
                        != str(witness.get("excerpt_sha256", "")).upper()
                        or not isinstance(witness.get("semantic_basis"), str)
                        or not witness["semantic_basis"].strip()):
                    raise ValueError(f"{decision_id}: invalid witness excerpt/semantic basis")
                hashes[target] = file_hash
                kinds.add(kind)
                witness_excerpts.append(excerpt)
            if not kinds.intersection({"msa", "classical"}) or (
                "english" not in kinds and decision_id not in global_captions
            ):
                raise ValueError(f"{decision_id}: assessment needs English and Arabic witnesses")
            observed_forms = entry.get("observed_arabic_forms", [])
            if not isinstance(observed_forms, list):
                raise ValueError(f"{decision_id}: malformed observed Arabic forms")
            for observed in observed_forms:
                if not isinstance(observed, dict):
                    raise ValueError(f"{decision_id}: malformed observed Arabic form")
                form = observed.get("form")
                indices = observed.get("source_witness_indices")
                if (not isinstance(form, str) or not form.strip()
                        or not isinstance(observed.get("note"), str) or not observed["note"].strip()
                        or not isinstance(indices, list) or not indices
                        or any(type(i) is not int or not 0 <= i < len(witnesses)
                               or witnesses[i]["source_kind"] == "english" for i in indices)
                        or not any(form in witness_excerpts[i] for i in indices)):
                    raise ValueError(f"{decision_id}: observed Arabic form lacks a literal Arabic witness")
            prepared = copy.deepcopy(entry)
            rejections = entry.get("rejected_occurrences", [])
            if not isinstance(rejections, list):
                raise ValueError(f"{decision_id}: malformed rejected occurrences")
            rejected_units: set[str] = set()
            rejected_rows: list[dict] = []
            replacement_indices: set[int] = set()
            for rejection in rejections:
                if not isinstance(rejection, dict):
                    raise ValueError(f"{decision_id}: malformed occurrence rejection")
                unit_id = rejection.get("unit_id")
                old_rows = [row for row in decision.get("occurrences", [])
                            if row.get("unit_id") == unit_id]
                indices = rejection.get("replacement_witness_indices")
                if (not isinstance(unit_id, str) or unit_id in rejected_units
                        or len(old_rows) != 1 or not collapse(rejection.get("reason"))
                        or not isinstance(indices, list) or not indices
                        or any(type(i) is not int or not 0 <= i < len(witnesses) for i in indices)):
                    raise ValueError(f"{decision_id}: unproved or ambiguous occurrence rejection")
                replacement_kinds = {witnesses[i]["source_kind"] for i in indices}
                if ("english" not in replacement_kinds
                        or not replacement_kinds.intersection({"msa", "classical"})):
                    raise ValueError(f"{decision_id}: replacement context needs both languages")
                rejected_units.add(unit_id)
                rejected_rows.extend(copy.deepcopy(old_rows))
                replacement_indices.update(indices)
            replacements: dict[str, dict] = {}
            for index in sorted(replacement_indices):
                witness = witnesses[index]
                matches = unit_paths.get((witness["source_kind"], witness["path"]), [])
                if len(matches) != 1:
                    raise ValueError(f"{decision_id}: replacement witness has no unique baseline unit")
                unit_id = matches[0]
                row = replacements.setdefault(unit_id, {
                    "unit_id": unit_id,
                    "context_note": (
                        "New source-checked context replacing a rejected wrong-sense binding. "
                        "This is a witness for the specified component, not an exhaustive occurrence census."
                    ),
                    "expert_source_binding_witness": EXPERT_SOURCE_BINDING_WITNESS,
                })
                declaration = {
                    "source_kind": witness["source_kind"], "path": witness["path"],
                    "line_ranges": [[witness["line_start"], witness["line_end"]]],
                    "file_sha256": witness["file_sha256"],
                    "cited_text_sha256": witness["excerpt_sha256"],
                    "semantic_basis": witness["semantic_basis"],
                }
                kind, group, _ = _validated_expert_source_group(
                    declaration, repo, english_root, witness["path"], digest
                )
                if kind in row:
                    row[kind]["locators"].extend(group["locators"])
                else:
                    row[kind] = group
            prepared["rejected_occurrence_records"] = rejected_rows
            prepared["replacement_occurrence_records"] = list(replacements.values())
            plans.append((decision, prepared, logical))
    # No decision is changed until every file, expectation and witness passes.
    for decision, entry, logical in plans:
        before = {key: copy.deepcopy(decision.get(key)) for key in
                  ("sense", "rationale", "expert_question", "recording_mode")}
        decision.update(entry["changes"])
        decision["recording_mode"] = entry["recording_mode"]
        decision["open_to_correction"] = True
        if entry.get("rejected_occurrences"):
            rejected_ids = {row["unit_id"] for row in entry["rejected_occurrences"]}
            decision["occurrences"] = [row for row in decision.get("occurrences", [])
                                       if row.get("unit_id") not in rejected_ids]
            decision["occurrences"].extend(entry["replacement_occurrence_records"])
        decision["expert_review_assessment"] = {
            "ledger_path": logical,
            "original_fields": before,
            **entry,
        }
    return identities, hashes


def collapse(value: object) -> str:
    return " ".join(str(value or "").split())


def md_text(value: object) -> str:
    return html.escape(collapse(value), quote=False)


def humanize_arabic_display(value: object) -> str:
    """Make Arabic ledger prose safe for human-facing Markdown/CSV surfaces.

    Review ledgers retain Open Logic token shorthand in their source fields;
    expose the token name (and plural marker) rather than leaking implementation
    syntax into the reviewer index.  TeX commands are then rendered by the
    existing display adapter.
    """
    text = collapse(value)
    text = re.sub(
        r"!!(?:\^|a)?\{([^{}]+)\}(s)?",
        lambda match: match.group(1) + (match.group(2) or ""),
        text,
    )
    # A few retained ledgers use the unbraced shorthand form (for example
    # ``!!^atableau``); stop at the Arabic text that follows it.
    text = re.sub(
        r"!!(?:\^|a)?([A-Za-z][A-Za-z0-9_-]*)",
        lambda match: match.group(1),
        text,
    )
    return humanize_tex(text)


class ExactReviewLiteral(str):
    """A registry-expanded formula passage; a second lossy render is forbidden."""


def rtl(value: object) -> str:
    text = value if isinstance(value, ExactReviewLiteral) else humanize_arabic_display(value)
    return f'<span lang="ar" dir="rtl">{md_text(text)}</span>'


def human_english_term(decision: dict) -> str:
    display = decision.get("review_display")
    if isinstance(display, dict) and collapse(display.get("english_term")):
        return collapse(display["english_term"])
    return collapse(decision.get("english_term"))


def human_chosen_arabic(decision: dict) -> str:
    display = decision.get("review_display")
    if isinstance(display, dict) and collapse(display.get("chosen_arabic")):
        if (decision.get("semantic_propagation_repair") or {}).get("ledger_path") in NEXT_BATCH_LEDGERS:
            return ExactReviewLiteral(collapse(display["chosen_arabic"]))
        return humanize_arabic_display(display["chosen_arabic"])
    assessment = decision.get("expert_review_assessment") or {}
    forms = assessment.get("observed_arabic_forms") or []
    if forms:
        return "؛ ".join(dict.fromkeys(humanize_arabic_display(row["form"]) for row in forms))
    value = collapse(decision.get("chosen_arabic"))
    value = re.sub(r"\s*؛\s*مع إبقاء.*$", "", value)
    value = value.replace("usetoken", "").strip(" ؛،,")
    return humanize_arabic_display(value)


def human_decision_field(decision: dict, field: str) -> str:
    display = decision.get("review_display")
    if isinstance(display, dict) and (decision.get("semantic_propagation_repair") or {}).get("ledger_path") in NEXT_BATCH_LEDGERS:
        return ExactReviewLiteral(collapse(display.get(field)))
    if isinstance(display, dict) and collapse(display.get(field)):
        value = humanize_arabic_display(display[field]) if field in {"before_arabic", "chosen_arabic", "classical_arabic"} else collapse(display[field])
    else:
        value = humanize_tex(decision.get(field))
    assessment = decision.get("expert_review_assessment")
    if field == "rationale" and isinstance(assessment, dict):
        return (
            f"Current assessment ({assessment['assessed_on']}; open to correction): "
            + value
        )
    return value


def append_assessment_provenance(
    lines: list[str], decision: dict, arabic_prefix: str,
) -> None:
    propagation = decision.get("semantic_propagation_repair")
    if isinstance(propagation, dict):
        href = arabic_prefix + quote(propagation["ledger_path"], safe="/")
        lines.append(
            "- **New repair assessment / تقييم تصحيحي جديد:** "
            + md_text(decision["assessed_on"])
            + "; not the original translator's deliberation. Previous "
            + ("Classical" if propagation.get("changed_edition") == "classical" else "MSA")
            + " wording / اللفظ السابق: "
            + rtl(human_decision_field(decision, "before_arabic"))
            + f". [Dated rationale and source evidence / التعليل المؤرخ وشواهد المصدر]({href})."
        )
        if propagation.get("inherited_source_qualification"):
            lines.append(
                "- **Inherited-source qualification / تقييد عبارة الأصل:** "
                "This makes an omitted mathematical qualification explicit; it is not "
                "presented as merely repairing an Arabic lexical mistranslation. "
                "The retained English, Classical counterpart, exact changed MSA wording "
                "and reversible source patches are preserved in the linked ledger; the "
                "machine-readable index also retains the complete previous MSA source."
            )
        elif propagation.get("translation_scope_clarification"):
            lines.append(
                "- **Translation-scope clarification / توضيح نطاق الترجمة:** "
                "The English condition is retained. This removes an Arabic any-versus-none "
                "ambiguity; it does not claim that the English source is erroneous. "
                "The linked ledger preserves the wording and reversible source patches; "
                "the machine-readable index also retains the complete previous MSA source."
            )
        if propagation.get("ledger_path") == APPLIED_CLASSICAL_LEDGER:
            for occurrence in propagation["choice_record"]["occurrences"]:
                locator = occurrence["classical_after"]
                target = arabic_prefix + quote(locator["path"], safe="/") + f"#L{locator['line_start']}"
                lines.append(
                    "- **Passage / الموضع:** " + md_text(occurrence["subchoice"])
                    + f" — [CA L{locator['line_start']}–{locator['line_end']}]({target}). "
                    + "Why / التعليل: " + md_text(occurrence["rationale"])
                    + " Please double-check / يرجى التحقق: " + md_text(occurrence["expert_review_question"])
                )
                for alternative in occurrence["alternatives"]:
                    lines.append("  - " + rtl(alternative["form"]) + ": "
                                 + md_text(alternative["disposition"]) + "; " + md_text(alternative["reason"]))
        passage_displays = (decision.get("review_display") or {}).get("literal_source_passages", [])
        if len(passage_displays) != len(decision.get("literal_source_passages", [])):
            raise ValueError("literal source passages require registered display expansion")
        for passage_index, passage in enumerate(decision.get("literal_source_passages", [])):
            shown = passage_displays[passage_index]
            if propagation.get("ledger_path") in NEXT_BATCH_LEDGERS:
                shown = {key: ExactReviewLiteral(value) for key, value in shown.items()}
            current = passage["after"]
            href = arabic_prefix + quote(current["path"], safe="/") + f"#L{current['line_start']}"
            lines.append("- **Literal source passage / اللفظ في موضعه:** "
                         + md_text(passage["edition"]) + "; English: " + md_text(shown["english"])
                         + "; before / السابق: " + rtl(shown["before"])
                         + "; after / المختار: " + rtl(shown["after"])
                         + f". [Exact source / المصدر]({href}). " + md_text(passage.get("before_role", "")))
    assessment = decision.get("expert_review_assessment")
    if not isinstance(assessment, dict):
        return
    href = arabic_prefix + quote(assessment["ledger_path"], safe="/")
    lines.append(
        "- **Assessment provenance / توثيق التقييم:** New assessment, not a claim "
        "about the original translator's reasoning. "
        f"[Original explanation and checked source witnesses / التعليل السابق وشواهد المصدر]({href})."
    )
    for observed in assessment.get("observed_arabic_forms") or []:
        citations = []
        for index in observed["source_witness_indices"]:
            witness = assessment["witnesses"][index]
            witness_href = arabic_prefix + quote(witness["path"], safe="/")
            witness_href += f"#L{witness['line_start']}"
            citations.append(
                f"[{SOURCE_LABELS[witness['source_kind']]} L{witness['line_start']}]({witness_href})"
            )
        lines.append(
            f"- **Observed wording / اللفظ المشهود:** {rtl(observed['form'])} — "
            + md_text(observed["note"]) + " (" + "; ".join(citations) + ")."
        )
    for rejection in assessment.get("rejected_occurrences") or []:
        lines.append(
            f"- **Corrected locator / تصحيح الموضع:** {md_text(rejection['unit_id'])} "
            + "was a wrong-sense binding, not an occurrence of this choice: "
            + md_text(rejection["reason"])
            + " The rejected record remains in the assessment history."
        )


def human_prose(value: object) -> str:
    return (
        collapse(value)
        .replace("an frame", "a frame")
        .replace("a explicitly", "an explicitly")
    )


def code_text(value: object) -> str:
    return f'<code dir="auto">{html.escape(collapse(value), quote=False)}</code>'


def text_value(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        level = value.get("level") or value.get("value") or ""
        reason = value.get("reason") or value.get("justification") or ""
        if level and reason:
            return f"{level} — {reason}"
        return str(level or reason)
    return ""


def parse_braced(text: str, start: int) -> tuple[str, int] | None:
    """Return the contents and exclusive end of a balanced TeX group."""

    if start >= len(text) or text[start] != "{":
        return None
    depth = 0
    index = start
    while index < len(text):
        char = text[index]
        if char in "{}":
            backslashes = 0
            probe = index - 1
            while probe >= 0 and text[probe] == "\\":
                backslashes += 1
                probe -= 1
            escaped = bool(backslashes % 2)
            if not escaped:
                depth += 1 if char == "{" else -1
                if depth == 0:
                    return text[start + 1:index], index + 1
        index += 1
    return None


def parse_delimited(
    text: str, start: int, opening: str, closing: str
) -> tuple[str, int] | None:
    """Return a balanced delimited group and its exclusive end."""

    if start >= len(text) or text[start] != opening:
        return None
    depth = 0
    for index in range(start, len(text)):
        char = text[index]
        if char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return text[start + 1:index], index + 1
    return None


def strip_tex_comments(text: str) -> str:
    rows = []
    for line in text.splitlines():
        cut = len(line)
        for index, char in enumerate(line):
            if char != "%":
                continue
            preceding = 0
            probe = index - 1
            while probe >= 0 and line[probe] == "\\":
                preceding += 1
                probe -= 1
            if preceding % 2 == 0:
                cut = index
                break
        rows.append(line[:cut])
    return "\n".join(rows)


@dataclass(frozen=True)
class TokenRegistry:
    values: dict[tuple[str, str], str]
    identity: dict


def first_character_upper(value: str) -> str:
    if not value:
        return value
    return value[0].upper() + value[1:]


def parse_token_registry(paths: Sequence[Path], repo: Path) -> TokenRegistry:
    """Read the exact Open Logic token definitions used by a reader locale."""

    values: dict[tuple[str, str], str] = {}
    sources = []
    for path in paths:
        if not path.is_file():
            continue
        raw = path.read_bytes()
        text = strip_tex_comments(raw.decode("utf-8-sig"))
        sources.append(
            {
                "path": path.resolve().relative_to(repo.resolve()).as_posix(),
                "bytes": len(raw),
                "sha256": sha256_bytes(raw),
            }
        )
        marker = re.compile(r"\\settexttoken\s*")
        for match in marker.finditer(text):
            position = match.end()
            parsed_token = parse_braced(text, position)
            if parsed_token is None:
                continue
            token, position = parsed_token
            starred = False
            while position < len(text) and text[position].isspace():
                position += 1
            if position < len(text) and text[position] == "*":
                starred = True
                position += 1
            while position < len(text) and text[position].isspace():
                position += 1
            parsed_singular = parse_braced(text, position)
            if parsed_singular is None:
                continue
            singular, position = parsed_singular
            while position < len(text) and text[position].isspace():
                position += 1
            parsed_plural = parse_braced(text, position)
            if parsed_plural is None:
                continue
            plural, position = parsed_plural
            optional = []
            for _ in range(2):
                while position < len(text) and text[position].isspace():
                    position += 1
                parsed_optional = parse_delimited(text, position, "[", "]")
                if parsed_optional is None:
                    break
                value, position = parsed_optional
                optional.append(value)
            token = collapse(token)
            singular = collapse(singular)
            plural = collapse(plural)
            values[("s", token)] = singular
            values[("p", token)] = plural
            values[("a", token)] = "an" if starred else "a"
            values[("A", token)] = "An" if starred else "A"
            values[("S", token)] = collapse(optional[0]) if optional else first_character_upper(singular)
            values[("P", token)] = (
                collapse(optional[1]) if len(optional) >= 2 else first_character_upper(plural)
            )

        override = re.compile(r"\\definetoken\s*")
        for match in override.finditer(text):
            position = match.end()
            fields = []
            for _ in range(3):
                while position < len(text) and text[position].isspace():
                    position += 1
                parsed = parse_braced(text, position)
                if parsed is None:
                    fields = []
                    break
                value, position = parsed
                fields.append(value)
            if fields:
                switch, token, value = fields
                values[(collapse(switch), collapse(token))] = collapse(value)
    return TokenRegistry(
        values=values,
        identity={"sources": sources, "parsed_switch_values": len(values)},
    )


TOKEN_SHORTHAND = re.compile(
    r"!!(?P<capital>\^)?(?P<article>a)?\{(?P<token>[^{}]+)\}(?P<plural>s)?"
)
USETOKEN = re.compile(r"\\usetoken\{(?P<switch>[^{}]+)\}\{(?P<token>[^{}]+)\}")
PRINTTOKEN = re.compile(r"\\printtoken\{(?P<switch>[^{}]+)\}\{(?P<token>[^{}]+)\}")


def expand_registered_tokens(value: object, registry: TokenRegistry) -> tuple[str, list[dict]]:
    """Expand only token macros whose exact switch/token pair is registered."""

    text = collapse(value)
    expansions: list[dict] = []

    def replace_usetoken(match: re.Match[str]) -> str:
        switch = match.group("switch")
        token = collapse(match.group("token"))
        replacement = registry.values.get((switch, token))
        if replacement is None:
            return match.group(0)
        expansions.append(
            {"source_syntax": match.group(0), "switch": switch, "token": token, "display": replacement}
        )
        return replacement

    def replace_shorthand(match: re.Match[str]) -> str:
        token = collapse(match.group("token"))
        switch = "p" if match.group("plural") else "s"
        if match.group("capital"):
            switch = switch.upper()
        replacement = registry.values.get((switch, token))
        if replacement is None:
            return match.group(0)
        if match.group("article"):
            article_switch = "A" if match.group("capital") else "a"
            article = registry.values.get((article_switch, token))
            if article is None:
                return match.group(0)
            replacement = (article + " " + replacement).strip()
        expansions.append(
            {"source_syntax": match.group(0), "switch": switch, "token": token, "display": replacement}
        )
        return replacement

    text = USETOKEN.sub(replace_usetoken, text)
    text = PRINTTOKEN.sub(replace_usetoken, text)
    text = TOKEN_SHORTHAND.sub(replace_shorthand, text)
    return collapse(text), expansions


TEX_REVIEW_SYMBOLS = {
    "Nat": "ℕ", "Int": "ℤ", "Rat": "ℚ", "Real": "ℝ",
    "True": "True", "False": "False", "lfalse": "⊥", "ltrue": "⊤",
    "LogCL": "classical logic", "ZFC": "ZFC", "Cut": "Cut",
    "beta": "β", "gamma": "γ", "Gamma": "Γ", "delta": "δ",
    "Delta": "Δ", "lambda": "λ", "Lambda": "Λ", "Sigma": "Σ",
    "omega": "ω", "alpha": "α", "forall": "∀", "exists": "∃",
    "land": "∧", "lor": "∨", "lnot": "¬", "lif": "→",
    "liff": "↔", "in": "∈", "notin": "∉", "leq": "≤", "geq": "≥",
    "subseteq": "⊆", "bigcup": "⋃", "setminus": "∖",
    "equiv": "≡", "ident": "=", "times": "×", "cdot": "·",
    "dots": "…", "ldots": "…", "mapsto": "↦",
}


def humanize_tex(value: object, registry: TokenRegistry | None = None) -> str:
    """Render ledger TeX as readable Unicode while preserving the raw JSON field.

    This is deliberately a display adapter, not a TeX interpreter. Registered
    Open Logic tokens are expanded exactly; familiar mathematical commands are
    rendered as Unicode/name equivalents; any remaining command is exposed as
    its readable command name rather than leaking implementation syntax.
    """

    text = collapse(value)
    if registry is not None:
        text, _ = expand_registered_tokens(text, registry)
    # Common two-argument wrappers whose second argument is the visible text.
    for _ in range(4):
        updated = re.sub(
            r"\\foreignlanguage\s*\{[^{}]*\}\s*\{([^{}]*)\}", r"\1", text
        )
        updated = re.sub(
            r"\\(?:textbf|textit|emph|mbox|text|mathrm|mathbf|mathit)\s*\{([^{}]*)\}",
            r"\1",
            updated,
        )
        if updated == text:
            break
        text = updated
    # TeX accent spellings seen in titles, captions and decision prose.
    accents = {
        r'\\"{o}': "ö", r'\\"o': "ö", r'\\"{O}': "Ö", r'\\"O': "Ö",
        r"\\H{o}": "ő", r"\\H{O}": "Ő", r"\\L": "Ł",
    }
    for source, display in accents.items():
        text = text.replace(source, display)
    text = re.sub(r"\\Pow\s*\{([^{}]+)\}", r"℘(\1)", text)
    text = re.sub(r"\\Bin\b", "2", text)
    text = re.sub(
        r"\\([A-Za-z@]+)\*?",
        lambda match: TEX_REVIEW_SYMBOLS.get(match.group(1), match.group(1)),
        text,
    )
    text = re.sub(r"\\(?:[,;:!]|\s)", " ", text)
    text = text.replace(r"\\", " ").replace("~", " ")
    text = text.replace(r"\(", "").replace(r"\)", "")
    text = text.replace(r"\[", "").replace(r"\]", "").replace("$", "")
    text = text.replace("{", "").replace("}", "")
    return collapse(text)


def load_review_token_registries(repo: Path) -> dict[str, TokenRegistry]:
    base = repo / "source/open-logic-config.sty"
    arabic = repo / "source/locale/ar/open-logic-config.sty"
    return {
        "english": parse_token_registry([base], repo),
        # The Classical reader inherits the same semantic token registry; its
        # prose realization differs in the unit sources, not in these macros.
        "arabic": parse_token_registry([base, arabic], repo),
    }


def humanize_retrospective_template(
    value: str, field: str, decision: dict, registries: dict[str, TokenRegistry]
) -> str:
    """Render quote roles proved by the retained retrospective templates only.

    A shared semantic token can have identical raw bytes in both quotations but
    different English and Arabic realizations. Do not infer quotation language
    from the surrounding prose or rewrite the raw ledger's retrospective basis.
    Unrecognized prose keeps the existing English display behavior.
    """
    text = collapse(value)
    patterns = {
        "rationale": (
            r"The Classical target retains «(?P<arabic>[^«»]+)» "
            r"from the MSA target for English «(?P<english>[^«»]+)» "
            r"in an aligned [^«»]+\. The identical semantic markup and the local "
            r"mathematical context constrain the referent\. This is a present-tense "
            r"retrospective justification, not a claim about the original "
            r"translator’s deliberation\."
        ),
        "expert_question": (
            r"At OLP-\d{4}, English line \d+ and Classical line \d+, "
            r"does «(?P<arabic>[^«»]+)» best preserve the sense of "
            r"«(?P<english>[^«»]+)» as [^«»]+, or is another officially "
            r"attested realization preferable\?"
        ),
    }
    pattern = patterns.get(field)
    match = (
        re.fullmatch(pattern, text)
        if pattern and decision.get("recording_mode") == "retrospective-reconstruction"
        else None
    )
    if match and (
        match.group("arabic") == collapse(decision.get("chosen_arabic"))
        and match.group("english") == collapse(decision.get("english_term"))
    ):
        # Replace from right to left so the original match offsets stay valid.
        for language in ("english", "arabic"):
            start, end = match.span(language)
            rendered = humanize_tex(match.group(language), registries[language])
            text = text[:start] + rendered + text[end:]
    return humanize_tex(text, registries["english"])


def attach_review_display(
    decision: dict, registries: dict[str, TokenRegistry]
) -> None:
    repair = decision.get("semantic_propagation_repair", {})
    if repair.get("ledger_path") in NEXT_BATCH_LEDGERS:
        # This batch contains complete formulas, not just lexical headwords.
        # Preserve unknown TeX operators/braces instead of the legacy display's
        # command-name fallback. Only registered prose tokens are expanded.
        def literal_display(value, language):
            return expand_registered_tokens(value, registries[language])[0]
        fields = ("english_term", "chosen_arabic", "before_arabic", "sense", "rationale", "edition",
                  "expert_review_reason", "expert_question")
        decision["review_display"] = {field: literal_display(decision.get(field),
            "arabic" if field in {"chosen_arabic", "before_arabic"} else "english") for field in fields}
        decision["review_display"].update(alternatives=copy.deepcopy(decision.get("alternatives", [])),
            registry_expansions={}, raw_fields_preserved=True,
            literal_source_passages=[{phase: literal_display(p[phase]["literal"],
                "english" if phase == "english" else "arabic") for phase in ("english", "before", "after")}
                for p in decision.get("literal_source_passages", [])])
        return
    raw_english = collapse(decision.get("english_term"))
    raw_arabic = collapse(decision.get("chosen_arabic"))
    trimmed_arabic = re.sub(r"\s*؛\s*مع إبقاء.*$", "", raw_arabic)
    english, english_expansions = expand_registered_tokens(
        raw_english, registries["english"]
    )
    arabic, arabic_expansions = expand_registered_tokens(
        trimmed_arabic, registries["arabic"]
    )
    before_arabic, before_expansions = expand_registered_tokens(
        decision.get("before_arabic"), registries["arabic"]
    )
    # Repair only literal article errors proved by starred registry tokens;
    # the raw ledger wording remains unchanged in JSON.
    an_tokens = sorted(
        token for (switch, token), article in registries["english"].values.items()
        if switch == "a" and article == "an"
    )
    for token in an_tokens:
        english = re.sub(
            r"\ba\s+" + re.escape(token) + r"\b",
            "an " + token,
            english,
            flags=re.IGNORECASE,
        )
    english = humanize_tex(english, registries["english"])
    arabic = humanize_tex(arabic, registries["arabic"])
    before_arabic = humanize_tex(before_arabic, registries["arabic"])
    observed_forms = (decision.get("expert_review_assessment") or {}).get("observed_arabic_forms") or []
    if observed_forms:
        arabic = "؛ ".join(dict.fromkeys(row["form"] for row in observed_forms))
    display_alternatives = []
    for row in decision.get("alternatives") or []:
        if isinstance(row, dict):
            rendered = copy.deepcopy(row)
            for key in ("form", "alternative", "value", "status", "decision", "reason", "disposition", "note"):
                if key in rendered:
                    rendered[key] = humanize_tex(rendered[key], registries["arabic"])
            display_alternatives.append(rendered)
        else:
            display_alternatives.append(humanize_tex(row, registries["arabic"]))
    decision["review_display"] = {
        "english_term": english,
        "chosen_arabic": arabic.replace("usetoken", "").strip(" ؛،,"),
        "before_arabic": before_arabic,
        "sense": humanize_tex(decision.get("sense"), registries["english"]),
        "rationale": humanize_retrospective_template(
            decision.get("rationale"), "rationale", decision, registries
        ),
        "edition": humanize_tex(decision.get("edition"), registries["english"]),
        "expert_review_reason": humanize_tex(
            decision.get("expert_review_reason"), registries["english"]
        ),
        "expert_question": humanize_retrospective_template(
            decision.get("expert_question") or decision.get("expert_review_question"),
            "expert_question", decision, registries,
        ),
        "alternatives": display_alternatives,
        "registry_expansions": {
            "english": english_expansions,
            "arabic": arabic_expansions,
            "before_arabic": before_expansions,
        },
        "literal_source_passages": [
            {phase: humanize_tex(passage[phase]["literal"],
                                registries["english" if phase == "english" else "arabic"])
             for phase in ("english", "before", "after")}
            for passage in decision.get("literal_source_passages", [])
        ],
        "raw_fields_preserved": bool(
            english != raw_english or arabic != raw_arabic
            or before_arabic != collapse(decision.get("before_arabic"))
        ),
    }


def command_args(text: str, command: str, count: int) -> list[str] | None:
    pattern = re.compile(r"\\" + re.escape(command) + r"\s*(?:\[[^\]]*\]\s*)?")
    match = pattern.search(text)
    if not match:
        return None
    position = match.end()
    args: list[str] = []
    for _ in range(count):
        while position < len(text) and text[position].isspace():
            position += 1
        parsed = parse_braced(text, position)
        if parsed is None:
            return None
        value, position = parsed
        args.append(value)
    return args


def plain_tex_title(value: str, registry: TokenRegistry | None = None) -> str:
    value = re.sub(r"%.*", "", value)
    value = re.sub(r"\\(?:textbf|textit|emph|mbox)\s*\{([^{}]*)\}", r"\1", value)
    if registry is not None:
        value, _ = expand_registered_tokens(value, registry)
    value = re.sub(r"\\(?:use|print)token\s*\{[^{}]*\}\s*\{([^{}]*)\}", r"\1", value)
    value = re.sub(r"!!(?:\^?a?)?\{([^{}]*)\}s?", r"\1", value)
    value = re.sub(r"\\Log\s*\{([^{}]*)\}", r"\1", value)
    value = value.replace(r"\Nat", "ℕ").replace(r"\L ukasiewicz", "Łukasiewicz")
    value = value.replace("~", " ")
    return humanize_tex(value, registry) or "Untitled / بلا عنوان"


@dataclass(frozen=True)
class UnitMeta:
    unit_id: str
    title: str
    source_role: str
    target_path: str
    aux_label: str | None


def derive_unit_meta(
    repo: Path, row: dict, registry: TokenRegistry | None = None
) -> UnitMeta:
    target = repo / str(row["target_path"])
    text = target.read_text(encoding="utf-8-sig") if target.is_file() else ""
    file_id = command_args(text, "olfileid", 3)
    section = command_args(text, "olsection", 1)
    chapter = command_args(text, "olchapter", 3)
    part = command_args(text, "olpart", 2)
    starred_chapter = command_args(text, "chapter*", 1)
    label = None
    if file_id and section:
        label = f"{file_id[0]}:{file_id[1]}:{file_id[2]}:sec"
        title = section[0]
    elif chapter:
        label = f"{chapter[0]}:{chapter[1]}::chap"
        title = chapter[2]
    elif part:
        label = f"{part[0]}:::part"
        title = part[1]
    elif starred_chapter:
        title = starred_chapter[0]
    else:
        title = target.stem.replace("-", " ")
    return UnitMeta(
        unit_id=str(row["id"]),
        title=plain_tex_title(title, registry),
        source_role=str(row.get("source_role") or ""),
        target_path=str(row["target_path"]).replace("\\", "/"),
        aux_label=label,
    )


@dataclass
class SourceSnapshot:
    path: Path
    logical_path: str
    data: bytes
    text: str
    lines: list[str]
    sha256: str


class SourceCache:
    def __init__(self) -> None:
        self._cache: dict[Path, SourceSnapshot] = {}

    def get(self, path: Path, logical_path: str) -> SourceSnapshot:
        resolved = path.resolve()
        if resolved not in self._cache:
            data = resolved.read_bytes()
            text = data.decode("utf-8-sig")
            self._cache[resolved] = SourceSnapshot(
                path=resolved,
                logical_path=logical_path,
                data=data,
                text=text,
                lines=text.splitlines(),
                sha256=sha256_bytes(data),
            )
        return self._cache[resolved]

    def observed_hashes(self) -> dict[Path, str]:
        return {path: snapshot.sha256 for path, snapshot in self._cache.items()}


def normalized_excerpt(value: str) -> str:
    return " ".join(unicodedata.normalize("NFC", value).split())


def excerpt_pattern(excerpt: str) -> re.Pattern[str] | None:
    tokens = re.findall(r"\S+", unicodedata.normalize("NFC", excerpt))
    if not tokens:
        return None
    return re.compile(r"\s+".join(re.escape(token) for token in tokens))


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def reconcile_lines(
    snapshot: SourceSnapshot,
    line_start: int | None,
    line_end: int | None,
    excerpt: str,
    recorded_sha256: str,
) -> dict:
    """Verify or relocate a locator without fuzzy/nearest-line guessing."""

    line_count = len(snapshot.lines)
    result = {
        "status": "unresolved-no-line-locator",
        "resolved": False,
        "current_line_start": None,
        "current_line_end": None,
        "candidate_line_ranges": [],
        "recorded_hash_matches_current": bool(recorded_sha256)
        and recorded_sha256.upper() == snapshot.sha256,
    }
    if not isinstance(line_start, int) or not isinstance(line_end, int):
        return result
    if line_start < 1 or line_end < line_start:
        result["status"] = "unresolved-invalid-line-range"
        return result
    recorded_range_in_bounds = line_start <= line_count and line_end <= line_count
    effective_end = min(line_end, line_count)
    if not excerpt.strip():
        if not recorded_range_in_bounds:
            result["status"] = "unresolved-invalid-line-range"
        elif result["recorded_hash_matches_current"]:
            result.update(
                status="verified-recorded-lines-by-hash",
                resolved=True,
                current_line_start=line_start,
                current_line_end=effective_end,
                resolution_certificate={
                    "method": "recorded exact line range bound to matching file hash",
                    "accepted_line_range": [line_start, effective_end],
                },
            )
        else:
            result["status"] = "unresolved-no-excerpt-and-hash-changed"
        return result

    expected = "\n".join(snapshot.lines[line_start - 1:effective_end])
    wanted = normalized_excerpt(excerpt)
    if (
        recorded_range_in_bounds
        and line_count >= 25
        and line_start == 1
        and effective_end == line_count
        and wanted == normalized_excerpt(snapshot.text)
    ):
        result.update(
            status="unresolved-whole-file-span-not-exact-occurrence",
            candidate_line_ranges=[[1, line_count]],
        )
        return result
    pattern = excerpt_pattern(excerpt)
    if recorded_range_in_bounds and wanted and wanted in normalized_excerpt(expected):
        if pattern is None:
            result["status"] = "unresolved-empty-excerpt"
            return result
        normalized_text = unicodedata.normalize("NFC", snapshot.text)
        matches = list(pattern.finditer(normalized_text))
        ranges = [
            [
                line_for_offset(normalized_text, match.start()),
                line_for_offset(
                    normalized_text, max(match.start(), match.end() - 1)
                ),
            ]
            for match in matches
        ]
        inside = [
            found for found in ranges
            if found[0] >= line_start and found[1] <= effective_end
        ]
        accepted = [line_start, effective_end]
        status = "verified-recorded-lines"
        if wanted != normalized_excerpt(expected):
            if len(inside) == 1:
                accepted = inside[0]
                status = "verified-exact-excerpt-within-recorded-range"
            elif len(inside) > 1:
                result.update(
                    status="unresolved-excerpt-ambiguous-within-recorded-range",
                    candidate_line_ranges=inside,
                )
                return result
        result.update(
            status=status,
            resolved=True,
            current_line_start=accepted[0],
            current_line_end=accepted[1],
            resolution_certificate={
                "method": "recorded exact excerpt verified at recorded lines",
                "recorded_bounding_range": [line_start, effective_end],
                "accepted_line_range": accepted,
                "accepted_exact_excerpt": excerpt,
            },
        )
        return result

    if pattern is None:
        result["status"] = "unresolved-empty-excerpt"
        return result
    normalized_text = unicodedata.normalize("NFC", snapshot.text)
    matches = list(pattern.finditer(normalized_text))
    ranges = [
        [line_for_offset(normalized_text, match.start()),
         line_for_offset(normalized_text, max(match.start(), match.end() - 1))]
        for match in matches
    ]
    result["candidate_line_ranges"] = ranges
    if len(matches) == 1:
        result.update(
            status="relocated-by-exact-excerpt",
            resolved=True,
            current_line_start=ranges[0][0],
            current_line_end=ranges[0][1],
            resolution_certificate={
                "method": "unique exact recorded excerpt",
                "accepted_line_range": ranges[0],
                "accepted_exact_excerpt": excerpt,
            },
        )
    elif not matches:
        result["status"] = "unresolved-excerpt-not-found"
    else:
        result["status"] = "unresolved-excerpt-ambiguous"
    return result


def explicit_term_variants(value: object) -> list[str]:
    """Return only variants explicitly written in a ledger term field."""

    rendered = collapse(value).strip("`'\"“”«» ")
    if not rendered:
        return []
    candidates = [rendered]
    candidates.extend(
        piece for piece in re.split(r"\s*(?:/|;|؛)\s*", rendered) if piece
    )
    before_parenthesis = re.sub(r"\s*\([^()]*\)\s*$", "", rendered).strip()
    if before_parenthesis and before_parenthesis != rendered:
        candidates.append(before_parenthesis)
    for parenthetical in re.findall(r"\(([^()]*)\)", rendered):
        explicit = re.split(r"[:：]", parenthetical, maxsplit=1)[-1].strip()
        if explicit:
            candidates.extend(
                piece for piece in re.split(r"\s*(?:/|;|؛)\s*", explicit) if piece
            )
    result: list[str] = []
    for candidate in candidates:
        candidate = collapse(candidate).strip("`'\"“”«» ,،.;؛: ")
        if candidate and len(candidate) >= 3 and candidate not in result:
            result.append(candidate)
    return result


ENGLISH_TERM_STOPWORDS = {
    "a", "an", "and", "as", "at", "by", "for", "formula", "function",
    "in", "law", "of", "or", "property", "relation", "rule", "symbol",
    "the", "to", "value", "with",
}


def distinctive_english_term_components(value: object) -> list[str]:
    """Extract only explicit, non-generic lexical components from a term."""

    result: list[str] = []
    for variant in explicit_term_variants(value):
        words = re.findall(r"[A-Za-z][A-Za-z'-]{3,}", variant)
        for word in words:
            if word.casefold() not in ENGLISH_TERM_STOPWORDS and word not in result:
                result.append(word)
    return result


ARABIC_TERM_STOPWORDS = {
    "الاختيار", "التعبير", "المصطلح", "المعنى", "القاعدة", "قاعدة",
    "القيمة", "قيمة", "الصدق", "صدق", "الدالة", "دالة", "المجموعة",
    "مجموعة", "المنطق", "منطق", "قابل", "قابلة", "مختصرًا", "واللفظ",
    "المصنوع", "لفظ", "صيغة", "حالة", "نوع", "علاقة", "غير", "التي",
    "إثبات", "اثبات", "كلا", "كلتا",
}


def distinctive_arabic_term_components(value: object) -> list[str]:
    """Extract explicit Arabic lexical components for exact, file-bounded search."""

    result: list[str] = []
    for variant in explicit_term_variants(value):
        suffix = re.split(r"[:：]", variant, maxsplit=1)[-1]
        for candidate in (variant, suffix):
            for word in re.findall(r"[\u0600-\u06FF][\u0600-\u06FF\u064B-\u065Fـ]{2,}", candidate):
                normalized = word.strip("ـ")
                if normalized in ARABIC_TERM_STOPWORDS or normalized in result:
                    continue
                result.append(normalized)
                # Exact Arabic clitic realizations are useful when a ledger
                # records the citation form but the source uses لـ + الــ.
                if normalized.startswith("ال") and len(normalized) > 4:
                    with_lam = "لل" + normalized[2:]
                    if with_lam not in result:
                        result.append(with_lam)
    return result


def quoted_grammatical_forms(value: object) -> list[str]:
    rendered = human_prose(value)
    result: list[str] = []
    for quoted in re.findall(r"«([^»]+)»", rendered):
        for variant in explicit_term_variants(quoted):
            if variant not in result:
                result.append(variant)
    return result


def unit_wide_no_discrete_reason(decision: dict, occurrence: dict) -> str | None:
    combined = " ".join(
        collapse(value).casefold()
        for value in (
            decision.get("usage_scope"),
            occurrence.get("context_note"),
            decision.get("grammatical_realization"),
        )
        if collapse(value)
    )
    markers = (
        "recommendation only; source targets were not changed",
        "used in this review's recommendation only",
        "unit-wide policy",
        "whole-unit policy",
        "no discrete lexical occurrence",
    )
    if any(marker in combined for marker in markers):
        return (
            "The ledger describes a unit-wide policy or a proposed wording not applied "
            "as a discrete lexical occurrence in the current source."
        )
    return None


def exact_phrase_ranges(snapshot: SourceSnapshot, phrase: str) -> list[list[int]]:
    """Find case-insensitive, whitespace-flexible exact phrases by source line."""

    tokens = re.findall(r"\S+", unicodedata.normalize("NFC", phrase))
    if not tokens:
        return []
    body = r"\s+".join(re.escape(token) for token in tokens)
    if tokens[0][0].isalnum() or tokens[0][0] == "_":
        body = r"(?<!\w)" + body
    if tokens[-1][-1].isalnum() or tokens[-1][-1] == "_":
        body += r"(?!\w)"
    pattern = re.compile(body, re.IGNORECASE)
    normalized_text = unicodedata.normalize("NFC", snapshot.text)
    ranges: list[list[int]] = []
    for match in pattern.finditer(normalized_text):
        found = [
            line_for_offset(normalized_text, match.start()),
            line_for_offset(normalized_text, max(match.start(), match.end() - 1)),
        ]
        if found not in ranges:
            ranges.append(found)
    return ranges


def exact_query_tier(
    snapshot: SourceSnapshot,
    tier: str,
    queries: Sequence[str],
    allow_compound_span: bool = False,
) -> dict:
    unique_by_range: dict[tuple[int, int], list[str]] = {}
    matched_ranges: list[list[int]] = []
    searched: list[str] = []
    for query in queries:
        query = collapse(query)
        if not query or query in searched:
            continue
        searched.append(query)
        ranges = exact_phrase_ranges(snapshot, query)
        for found in ranges:
            if found not in matched_ranges:
                matched_ranges.append(found)
        if len(ranges) == 1:
            unique_by_range.setdefault(tuple(ranges[0]), []).append(query)
    candidates = sorted(unique_by_range)
    status = "no-unique-match"
    selected_range = None
    supporting_queries: list[str] = []
    if len(candidates) == 1:
        status = "unique"
        selected_range = list(candidates[0])
        supporting_queries = unique_by_range[candidates[0]]
    elif (
        allow_compound_span
        and len(candidates) > 1
        and max(item[1] for item in candidates) - min(item[0] for item in candidates) <= 8
    ):
        status = "unique-compound-span"
        selected_range = [
            min(item[0] for item in candidates),
            max(item[1] for item in candidates),
        ]
        supporting_queries = [
            query for candidate in candidates for query in unique_by_range[candidate]
        ]
    elif len(candidates) > 1:
        status = "conflicting-unique-matches"
    return {
        "tier": tier,
        "status": status,
        "queries": searched,
        "candidate_line_ranges": [list(item) for item in candidates],
        "all_matched_line_ranges": matched_ranges[:50],
        "selected_line_range": selected_range,
        "supporting_queries": supporting_queries,
    }


def exact_context_fragment_tier(snapshot: SourceSnapshot, excerpt: str) -> dict | None:
    """Use the longest uniquely occurring exact context fragment, never similarity."""

    tokens = re.findall(r"\S+", unicodedata.normalize("NFC", excerpt))
    if len(tokens) < 4:
        return None
    for width in range(min(12, len(tokens) - 1), 3, -1):
        queries: list[tuple[int, str]] = []
        for start in range(0, len(tokens) - width + 1):
            query = " ".join(tokens[start:start + width])
            if len(query) >= 20 and all(query != item[1] for item in queries):
                queries.append((start, query))
        unique_matches: list[tuple[int, str, list[int]]] = []
        all_matched: list[list[int]] = []
        for token_offset, query in queries:
            ranges = exact_phrase_ranges(snapshot, query)
            for found in ranges:
                if found not in all_matched:
                    all_matched.append(found)
            if len(ranges) == 1:
                unique_matches.append((token_offset, query, ranges[0]))
        if not unique_matches:
            continue
        unique_matches.sort(key=lambda item: item[0])
        monotone = all(
            previous[2][0] <= current[2][0]
            for previous, current in zip(unique_matches, unique_matches[1:])
        )
        if monotone:
            selected = [
                min(item[2][0] for item in unique_matches),
                max(item[2][1] for item in unique_matches),
            ]
            return {
                "tier": "recorded-excerpt exact context fragment",
                "status": "unique",
                "queries": [item[1] for item in queries],
                "candidate_line_ranges": [selected],
                "all_matched_line_ranges": all_matched[:50],
                "selected_line_range": selected,
                "supporting_queries": [
                    item[1] for item in unique_matches[:3]
                ] + ([unique_matches[-1][1]] if len(unique_matches) > 3 else []),
                "fragment_token_count": width,
                "unique_fragment_count": len(unique_matches),
            }
        return {
            "tier": "recorded-excerpt exact context fragment",
            "status": "conflicting-unique-matches",
            "queries": [item[1] for item in queries],
            "candidate_line_ranges": [item[2] for item in unique_matches[:50]],
            "all_matched_line_ranges": all_matched[:50],
            "selected_line_range": None,
            "supporting_queries": [],
            "fragment_token_count": width,
            "unique_fragment_count": len(unique_matches),
        }
    return None


def invalidate_broad_excerpt_without_recorded_term(
    location: dict, decision: dict
) -> None:
    """Treat a broad legacy region as context pending exact-term recovery.

    Some retrospective rows paired an entire file range with a heading; others
    asserted only a hash-bound region. Such ranges preserve useful provenance,
    but they must go through the stricter exact-term recovery path before a
    reviewer-facing source line is called exact.
    """

    reconciliation = location["line_reconciliation"]
    witness = location.get("witness")
    # The dedicated source-binding ledger is admitted only after its file hash,
    # complete declared line set, excerpt hash, OLP-unit path, and semantic
    # basis have all been validated against live bytes.  Some legitimate
    # semantic witnesses span more than eight lines without repeating the
    # ledger headword verbatim.  Preserve that narrow exception here; no other
    # legacy or caller-supplied witness can bypass the broad-span guard.
    if (
        isinstance(witness, dict)
        and witness.get("rule") == EXPERT_SOURCE_BINDING_WITNESS
        and witness.get("validated") is True
    ):
        return
    start = location.get("line_start")
    end = location.get("line_end")
    if (
        not reconciliation["resolved"]
        or not isinstance(start, int)
        or not isinstance(end, int)
        or end - start + 1 <= 8
    ):
        return
    terms = (
        explicit_term_variants(decision.get("english_term"))
        if location["source_kind"] == "english" else
        explicit_term_variants(decision.get("chosen_arabic"))
    )
    visible = unicodedata.normalize(
        "NFC", str(location.get("current_excerpt") or "")
    )
    current_start = reconciliation.get("current_line_start")
    current_end = reconciliation.get("current_line_end")
    current_width = (
        current_end - current_start + 1
        if isinstance(current_start, int) and isinstance(current_end, int)
        else end - start + 1
    )
    current_excerpt_contains_term = any(
        exact_phrase_ranges(
            SourceSnapshot(
                path=Path("<review-snippet>"),
                logical_path="<review-snippet>",
                data=visible.encode("utf-8"),
                text=visible,
                lines=visible.splitlines(),
                sha256="",
            ),
            term,
        )
        for term in terms
    )
    # A broad recorded bounding region may legitimately carry a short exact
    # excerpt. Keep it only when that already-narrowed excerpt itself contains
    # the full recorded term. A whole paragraph/file remains context evidence.
    if current_width <= 8 and current_excerpt_contains_term:
        return
    accepted = [
        reconciliation["current_line_start"],
        reconciliation["current_line_end"],
    ]
    reconciliation["broad_context_previous_resolution"] = {
        "status": reconciliation["status"],
        "accepted_line_range": accepted,
        "recorded_bounding_range": [start, end],
        "exact_excerpt": location.get("excerpt"),
    }
    reconciliation.update(
        status="unresolved-broad-span-excerpt-not-term-occurrence",
        resolved=False,
        current_line_start=None,
        current_line_end=None,
        candidate_line_ranges=[],
        broad_context_guard_reason=(
            "The recorded or accepted span exceeded eight lines and was therefore "
            "treated as context evidence until a full recorded term could be "
            "recovered by an exact, deterministic search."
        ),
    )
    reconciliation.pop("resolution_certificate", None)
    location["source_url"] = None
    location["_require_primary_term_recovery"] = True


def recover_location_by_exact_search(
    location: dict,
    decision: dict,
    occurrence: dict,
    cache: SourceCache,
    repo_web_root: str,
    english_web_root: str,
) -> dict:
    """Recover a missing/stale line only from a uniquely locating exact query."""

    reconciliation = location["line_reconciliation"]
    fs_path = location.get("_fs_path")
    if reconciliation["resolved"] or not isinstance(fs_path, Path):
        return location
    snapshot = cache.get(fs_path, location["logical_path"])
    attempts: list[dict] = []

    require_primary = bool(location.get("_require_primary_term_recovery"))
    context_result = None
    if (
        not require_primary
        and reconciliation["status"]
        != "unresolved-whole-file-span-not-exact-occurrence"
    ):
        context_result = exact_context_fragment_tier(
            snapshot, str(location.get("excerpt") or "")
        )
    if context_result is not None:
        attempts.append(context_result)

    context_note = collapse(occurrence.get("context_note"))
    if context_note and not require_primary:
        attempts.append(
            exact_query_tier(snapshot, "occurrence context", [context_note])
        )

    source_kind = location["source_kind"]
    primary_terms = (
        explicit_term_variants(decision.get("english_term"))
        if source_kind == "english" else
        explicit_term_variants(decision.get("chosen_arabic"))
    )
    if primary_terms:
        attempts.append(
            exact_query_tier(
                snapshot,
                "primary recorded term",
                primary_terms,
                allow_compound_span=bool(
                    re.search(r"[/;؛]", collapse(decision.get("chosen_arabic")))
                    or re.search(r"[/;؛]", collapse(decision.get("english_term")))
                ),
            )
        )
    if source_kind == "english":
        components = distinctive_english_term_components(decision.get("english_term"))
        if components:
            component_attempt = exact_query_tier(
                snapshot, "distinctive exact English term component", components
            )
            component_attempt["candidate_only"] = True
            attempts.append(component_attempt)
    else:
        grammatical_forms = quoted_grammatical_forms(
            decision.get("grammatical_realization")
        )
        if grammatical_forms:
            attempts.append(
                exact_query_tier(snapshot, "explicit quoted grammatical form", grammatical_forms)
            )
        arabic_components = distinctive_arabic_term_components(
            decision.get("chosen_arabic")
        )
        if arabic_components:
            component_attempt = exact_query_tier(
                    snapshot,
                    "distinctive exact Arabic term component",
                    arabic_components,
                    allow_compound_span=bool(
                        re.search(r"[/;؛]", collapse(decision.get("chosen_arabic")))
                        or re.search(r"[/;؛]", collapse(decision.get("english_term")))
                    ),
                )
            component_attempt["candidate_only"] = True
            attempts.append(component_attempt)
    if source_kind in {"msa", "classical"}:
        untranslated_markers = explicit_term_variants(decision.get("english_term"))
        if untranslated_markers:
            attempts.append(
                exact_query_tier(
                    snapshot, "exact English term retained in Arabic source", untranslated_markers
                )
            )
    elif collapse(decision.get("sense")):
        attempts.append(
            exact_query_tier(snapshot, "recorded mathematical sense", [decision["sense"]])
        )

    selected: dict | None = None
    for attempt in attempts:
        if attempt["status"] == "conflicting-unique-matches":
            # A stronger exact tier disagrees internally.  A weaker search may
            # not be used to guess which of those exact locations was intended.
            break
        if (
            attempt["status"] in {"unique", "unique-compound-span"}
            and not attempt.get("candidate_only")
        ):
            selected = attempt
            break
    reconciliation["exact_recovery_attempts"] = attempts
    if selected is None:
        review_candidates: list[list[int]] = []
        for attempt in attempts:
            for found in attempt.get("all_matched_line_ranges") or []:
                if found not in review_candidates:
                    review_candidates.append(found)
        reconciliation["exact_search_candidate_line_ranges"] = review_candidates[:50]
        nonlexical_reason = unit_wide_no_discrete_reason(decision, occurrence)
        if nonlexical_reason:
            reconciliation.update(
                status="unit-wide/no-discrete-lexical-occurrence",
                non_locator_record=True,
                non_locator_reason=nonlexical_reason,
            )
        return location

    start, end = selected["selected_line_range"]
    method_slug = {
        "recorded-excerpt exact context fragment": "unique-exact-context-fragment",
        "occurrence context": "unique-exact-occurrence-context",
        "primary recorded term": "unique-exact-term",
        "distinctive exact English term component": "unique-exact-term-component",
        "distinctive exact Arabic term component": "unique-exact-arabic-term-component",
        "explicit quoted grammatical form": "unique-exact-grammatical-form",
        "exact English term retained in Arabic source": "unique-exact-retained-english-term",
        "recorded mathematical sense": "unique-exact-sense",
    }[selected["tier"]]
    reconciliation.update(
        status="relocated-by-" + method_slug,
        resolved=True,
        current_line_start=start,
        current_line_end=end,
        candidate_line_ranges=[selected["selected_line_range"]],
        recovery_basis=selected["tier"],
        recovery_queries=selected["supporting_queries"],
        resolution_certificate={
            "method": selected["tier"],
            "accepted_line_range": [start, end],
            "accepted_exact_variants": selected["supporting_queries"],
        },
    )
    location["source_url"] = source_web_url(
        location["logical_path"],
        source_kind,
        repo_web_root,
        english_web_root,
        start,
        end,
    )
    location["current_excerpt"] = "\n".join(snapshot.lines[start - 1:end])
    return location


INLINE_MATH_ANCHOR = re.compile(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$", re.DOTALL)
REFERENCE_ANCHOR = re.compile(
    r"\\(?:olref|ollabel|label|ref|pageref)(?:\[[^\]\n]*\])?\{[^{}\n]+\}"
)


def structural_anchors(value: object) -> list[str]:
    """Extract ordered language-neutral TeX anchors from an aligned passage."""

    text = str(value or "")
    found: list[tuple[int, str]] = []
    for match in INLINE_MATH_ANCHOR.finditer(text):
        anchor = "$" + collapse(match.group(1)) + "$"
        if len(anchor) >= 8 and re.search(r"[\\^_=]", anchor):
            found.append((match.start(), anchor))
    for match in REFERENCE_ANCHOR.finditer(text):
        found.append((match.start(), collapse(match.group(0))))
    found.sort(key=lambda item: item[0])
    return [anchor for _, anchor in found]


def flexible_exact_body(value: str) -> str:
    return r"\s+".join(re.escape(token) for token in re.findall(r"\S+", value))


def unique_structural_windows(
    snapshot: SourceSnapshot, anchors: Sequence[str]
) -> list[dict]:
    """Find unique exact structural anchors/signatures in one target file."""

    evidence: list[dict] = []
    for anchor in anchors:
        ranges = exact_phrase_ranges(snapshot, anchor)
        if len(ranges) == 1:
            evidence.append(
                {
                    "kind": "unique exact cross-language TeX anchor",
                    "anchors": [anchor],
                    "line_range": ranges[0],
                    "candidate_window": [max(1, ranges[0][0] - 2), ranges[0][1] + 2],
                }
            )

    # A repeated short anchor can still become unique as part of an exact,
    # order-preserving signature.  The bounded gap prevents a signature from
    # spanning unrelated sections of a unit.
    normalized_text = unicodedata.normalize("NFC", snapshot.text)
    for width in range(min(4, len(anchors)), 1, -1):
        for start in range(0, len(anchors) - width + 1):
            group = list(anchors[start:start + width])
            if len(set(group)) < 2:
                continue
            body = r"[\s\S]{0,1200}?".join(flexible_exact_body(item) for item in group)
            matches = list(re.finditer(body, normalized_text, re.IGNORECASE))
            if len(matches) != 1:
                continue
            match = matches[0]
            line_range = [
                line_for_offset(normalized_text, match.start()),
                line_for_offset(normalized_text, max(match.start(), match.end() - 1)),
            ]
            evidence.append(
                {
                    "kind": "unique exact cross-language TeX signature",
                    "anchors": group,
                    "line_range": line_range,
                    "candidate_window": [max(1, line_range[0] - 1), line_range[1] + 1],
                }
            )
    unique = {}
    for row in evidence:
        key = (
            row["kind"],
            tuple(row["anchors"]),
            tuple(row["line_range"]),
        )
        unique[key] = row
    return [unique[key] for key in sorted(unique, key=str)]


def exact_term_candidate_ranges(location: dict) -> list[list[int]]:
    reconciliation = location["line_reconciliation"]
    rows: list[list[int]] = []
    for attempt in reconciliation.get("exact_recovery_attempts") or []:
        tier = str(attempt.get("tier") or "")
        if not any(
            marker in tier
            for marker in ("term", "grammatical form", "retained in Arabic")
        ):
            continue
        for found in attempt.get("all_matched_line_ranges") or []:
            if found not in rows:
                rows.append(found)
    return rows


def recover_by_cross_language_exact_structure(
    locations: Sequence[dict],
    cache: SourceCache,
    repo_web_root: str,
    english_web_root: str,
) -> None:
    """Resolve a term only inside a uniquely aligned exact TeX structure."""

    passage_anchors = []
    for location in locations:
        excerpt = location.get("current_excerpt") or location.get("excerpt") or ""
        passage_anchors.extend(structural_anchors(excerpt))
    # Preserve order while keeping the search bounded and deterministic.
    anchors = []
    for anchor in passage_anchors:
        if anchor not in anchors:
            anchors.append(anchor)
    if not anchors:
        return

    for location in locations:
        reconciliation = location["line_reconciliation"]
        fs_path = location.get("_fs_path")
        if reconciliation["resolved"] or not isinstance(fs_path, Path):
            continue
        candidates = exact_term_candidate_ranges(location)
        if not candidates:
            continue
        snapshot = cache.get(fs_path, location["logical_path"])
        evidence = unique_structural_windows(snapshot, anchors)
        supported: dict[tuple[int, int], list[dict]] = defaultdict(list)
        for item in evidence:
            first, last = item["candidate_window"]
            inside = [
                candidate for candidate in candidates
                if candidate[0] >= first and candidate[1] <= last
            ]
            if len(inside) == 1:
                supported[tuple(inside[0])].append(item)
        reconciliation["cross_language_exact_structure_attempts"] = evidence
        if len(supported) != 1:
            continue
        (start, end), support = next(iter(supported.items()))
        reconciliation.update(
            status="relocated-by-cross-language-exact-structure",
            resolved=True,
            current_line_start=start,
            current_line_end=end,
            candidate_line_ranges=[[start, end]],
            recovery_basis=(
                "exact term hit inside a uniquely matching language-neutral TeX "
                "anchor/signature from the aligned recorded occurrence"
            ),
            cross_language_structure_support=support,
            resolution_certificate={
                "method": "cross-language exact structural confirmation",
                "accepted_line_range": [start, end],
                "support": support,
            },
        )
        location["source_url"] = source_web_url(
            location["logical_path"],
            location["source_kind"],
            repo_web_root,
            english_web_root,
            start,
            end,
        )
        location["current_excerpt"] = "\n".join(snapshot.lines[start - 1:end])


def recover_unique_monotone_sequences(
    locations: Sequence[dict],
    cache: SourceCache,
    repo_web_root: str,
    english_web_root: str,
) -> None:
    """Resolve ambiguous exact excerpts only when file-wide order is unique."""

    groups: dict[tuple[str, str], list[tuple[int, dict]]] = defaultdict(list)
    for position, location in enumerate(locations):
        start = location.get("line_start")
        if not isinstance(start, int) or location.get("_fs_path") is None:
            continue
        reconciliation = location["line_reconciliation"]
        if reconciliation["resolved"] or (
            reconciliation["status"] in {
                "unresolved-excerpt-ambiguous",
                "unresolved-excerpt-ambiguous-within-recorded-range",
            }
            and reconciliation.get("candidate_line_ranges")
        ):
            groups[(location["source_kind"], location["logical_path"])].append(
                (position, location)
            )

    for rows in groups.values():
        rows.sort(key=lambda item: (item[1]["line_start"], item[0]))
        if not any(
            not location["line_reconciliation"]["resolved"]
            for _, location in rows
        ):
            continue
        options: list[list[tuple[int, int]]] = []
        for _, location in rows:
            reconciliation = location["line_reconciliation"]
            if reconciliation["resolved"]:
                choices = [
                    (
                        int(reconciliation["current_line_start"]),
                        int(reconciliation["current_line_end"]),
                    )
                ]
            else:
                choices = [
                    (int(found[0]), int(found[1]))
                    for found in reconciliation["candidate_line_ranges"]
                ]
            options.append(sorted(set(choices)))

        counts: list[list[int]] = [[1 for _ in options[0]]]
        parents: list[list[int | None]] = [[None for _ in options[0]]]
        for index in range(1, len(options)):
            current_counts: list[int] = []
            current_parents: list[int | None] = []
            previous_recorded = rows[index - 1][1]["line_start"]
            current_recorded = rows[index][1]["line_start"]
            same_recorded_line = current_recorded == previous_recorded
            for current in options[index]:
                valid: list[int] = []
                total = 0
                for previous_index, previous in enumerate(options[index - 1]):
                    ordered = (
                        previous == current if same_recorded_line
                        else previous[1] < current[0]
                    )
                    if not ordered or counts[index - 1][previous_index] == 0:
                        continue
                    total = min(2, total + counts[index - 1][previous_index])
                    valid.append(previous_index)
                current_counts.append(total)
                current_parents.append(valid[0] if total == 1 and len(valid) == 1 else None)
            counts.append(current_counts)
            parents.append(current_parents)

        endpoints = [
            index for index, count in enumerate(counts[-1]) if count > 0
        ]
        solution_count = min(2, sum(counts[-1][index] for index in endpoints))
        if solution_count != 1 or len(endpoints) != 1:
            continue
        selected_indices = [0] * len(rows)
        selected_indices[-1] = endpoints[0]
        valid_solution = True
        for index in range(len(rows) - 1, 0, -1):
            parent = parents[index][selected_indices[index]]
            if parent is None:
                valid_solution = False
                break
            selected_indices[index - 1] = parent
        if not valid_solution:
            continue

        for index, (_, location) in enumerate(rows):
            reconciliation = location["line_reconciliation"]
            if reconciliation["resolved"]:
                continue
            start, end = options[index][selected_indices[index]]
            snapshot = cache.get(location["_fs_path"], location["logical_path"])
            reconciliation.update(
                status="relocated-by-unique-exact-monotone-sequence",
                resolved=True,
                current_line_start=start,
                current_line_end=end,
                candidate_line_ranges=[[start, end]],
                recovery_basis=(
                    "unique order-preserving assignment among exact excerpt matches "
                    "within the same recorded source file"
                ),
                sequence_recovery={
                    "ordered_location_count": len(rows),
                    "solution_count": 1,
                    "selected_line_range": [start, end],
                },
                resolution_certificate={
                    "method": "unique order-preserving exact excerpt assignment",
                    "accepted_line_range": [start, end],
                },
            )
            location["source_url"] = source_web_url(
                location["logical_path"],
                location["source_kind"],
                repo_web_root,
                english_web_root,
                start,
                end,
            )
            location["current_excerpt"] = "\n".join(snapshot.lines[start - 1:end])


def semantic_mismatch_reason(decision: dict, unit: UnitMeta, location: dict) -> str | None:
    """Apply narrow, independently reviewed sense exclusions to recorded rows."""

    decision_id = str(decision.get("decision_id") or "")
    if unit.unit_id != "OLP-0451":
        return None
    excerpt = normalized_excerpt(str(location.get("current_excerpt") or "")).casefold()
    if decision_id == "ar-classical-0451-0500-tableau-token" and any(
        phrase in excerpt
        for phrase in ("truth table", "جدول صدق", "جدول الصدق", "بجدول الصدق")
    ):
        return (
            "Excluded after semantic audit: this is a truth table, not a proof-theoretic "
            "or semantic tableau occurrence."
        )
    if decision_id == "ar-classical-0451-0500-equivalence-class":
        generic_model_class = {
            "english": (
                "class of models",
                "frame in the class",
                "models of interest",
            ),
            "msa": (
                "فئة من النماذج",
                "الفئة التي تهمنا",
                "فئة النماذج موضع الاهتمام",
            ),
            "classical": (
                "فئة من النماذج",
                "الفئة المقصودة",
                "فئة النماذج التي نبحث فيها",
            ),
        }
        if any(
            phrase in excerpt
            for phrase in generic_model_class.get(location["source_kind"], ())
        ):
            return (
                "Excluded after semantic audit: this denotes a generic class of models "
                "or frames, not an equivalence class."
            )
    return None


def apply_location_quality_guards(
    location: dict, decision: dict, unit: UnitMeta
) -> None:
    """Prevent structural or wrong-sense spans from masquerading as term locations."""

    reconciliation = location["line_reconciliation"]
    excerpt = str(location.get("current_excerpt") or "").strip()
    if reconciliation["resolved"] and excerpt:
        substantive_lines = [
            line.strip() for line in excerpt.splitlines()
            if line.strip() and not line.lstrip().startswith("%")
        ]
        comment_only = not substantive_lines
        boilerplate = bool(substantive_lines) and all(
            re.match(
                r"^\\(?:documentclass(?:\[|\{)|begin\{document\}|end\{document\}|"
                r"olfileid(?:\s*\{|\b)|usepackage(?:\[|\{)|subfile(?:\[|\{))",
                line,
            )
            for line in substantive_lines
        )
        if comment_only or boilerplate:
            start = reconciliation["current_line_start"]
            end = reconciliation["current_line_end"]
            reconciliation["quality_guard_previous_status"] = reconciliation["status"]
            reconciliation.update(
                status=(
                    "unresolved-comment-only-not-term-occurrence"
                    if comment_only else "unresolved-boilerplate-not-term-occurrence"
                ),
                resolved=False,
                current_line_start=None,
                current_line_end=None,
                candidate_line_ranges=[[start, end]],
                quality_guard_reason=(
                    "The recorded line contains only a TeX comment, not a reader-visible "
                    "term occurrence."
                    if comment_only else
                    "The recorded line contains only TeX document structure, not the "
                    "recorded term in its stated sense."
                ),
            )
            reconciliation.pop("resolution_certificate", None)
            location["source_url"] = None

    exclusion = semantic_mismatch_reason(decision, unit, location)
    location["human_review_included"] = exclusion is None
    location["human_review_exclusion_reason"] = exclusion


def resolved_reconciliation_status(status: str) -> bool:
    return status.startswith("verified-") or status.startswith("relocated-by-")


def non_locator_reconciliation_status(status: str) -> bool:
    return status.startswith("unit-wide/")


def path_is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def resolve_source_path(
    repo: Path,
    english_root: Path | None,
    recorded_path: str,
    source_kind: str,
) -> tuple[Path | None, str]:
    raw = Path(recorded_path)
    candidates: list[tuple[Path, str]] = []
    if raw.is_absolute():
        candidates.append((raw, recorded_path.replace("\\", "/")))
    else:
        posix = recorded_path.replace("\\", "/").lstrip("./")
        candidates.append((repo / Path(posix), posix))
        if source_kind == "english" and english_root is not None:
            candidates.insert(0, (english_root / Path(posix), posix))
    for candidate, logical in candidates:
        if candidate.is_file():
            if path_is_within(candidate, repo):
                logical = candidate.resolve().relative_to(repo.resolve()).as_posix()
            elif english_root is not None and path_is_within(candidate, english_root):
                logical = candidate.resolve().relative_to(english_root.resolve()).as_posix()
            return candidate.resolve(), logical
    logical = recorded_path.replace("\\", "/")
    return None, logical


def source_web_url(
    logical_path: str,
    source_kind: str,
    repo_web_root: str,
    english_web_root: str,
    line_start: int | None = None,
    line_end: int | None = None,
) -> str:
    base = english_web_root if source_kind == "english" else repo_web_root
    url = base.rstrip("/") + "/" + quote(logical_path.lstrip("/"), safe="/")
    if line_start is not None:
        url += f"#L{line_start}"
        if line_end is not None and line_end != line_start:
            url += f"-L{line_end}"
    return url


def group_locators(group: dict) -> list[dict]:
    if isinstance(group.get("locators"), list):
        return [item for item in group["locators"] if isinstance(item, dict)]
    if isinstance(group.get("hits"), list):
        rows = []
        for hit in group["hits"]:
            if not isinstance(hit, dict):
                continue
            rows.append(
                {
                    "line_start": hit.get("line_start"),
                    "line_end": hit.get("line_end"),
                    "excerpt": hit.get("exact_excerpt") or hit.get("excerpt") or "",
                    "witness": copy.deepcopy(hit),
                }
            )
        return rows
    if "line_start" in group or "line_end" in group or "excerpt" in group:
        return [group]
    return []


def normalize_occurrence_sources(occurrence: dict) -> list[dict]:
    sources: list[dict] = []
    nested_kinds: set[str] = set()
    for source_kind in ("english", "msa", "classical"):
        group = occurrence.get(source_kind)
        if not isinstance(group, dict):
            continue
        nested_kinds.add(source_kind)
        locators = group_locators(group)
        if not locators:
            sources.append(
                {
                    "source_kind": source_kind,
                    "path": group.get("path"),
                    "recorded_sha256": group.get("sha256"),
                    "line_start": None,
                    "line_end": None,
                    "excerpt": "",
                    "ledger_locator_status": group.get("locator_status")
                    or group.get("availability_note")
                    or "identity-only; no exact line asserted",
                }
            )
        for locator in locators:
            sources.append(
                {
                    "source_kind": source_kind,
                    "path": group.get("path"),
                    "recorded_sha256": group.get("sha256"),
                    "line_start": locator.get("line_start"),
                    "line_end": locator.get("line_end"),
                    "excerpt": locator.get("excerpt") or "",
                    "witness": locator.get("witness"),
                    "ledger_locator_status": locator.get("ledger_locator_status"),
                }
            )

    # Older reviews predate the nested occurrence schema.  Preserve their
    # identity-only English/MSA records and their exact Classical locators.
    # The aliases cover both the 0051--0100 and 0301--0400 review layouts.
    aliases = {
        "english": {
            "paths": ("english_path", "source_path"),
            "hashes": ("english_sha256",),
            "lines": ("english_lines", "source_lines"),
            "excerpts": ("english_excerpt", "source_excerpt"),
        },
        "msa": {
            "paths": ("msa_path", "arabic_path"),
            "hashes": ("msa_sha256", "baseline_arabic_sha256"),
            "lines": ("msa_lines", "arabic_lines"),
            "excerpts": ("msa_excerpt", "arabic_excerpt"),
        },
        "classical": {
            "paths": ("classical_path", "target_path"),
            "hashes": ("classical_sha256", "target_sha256"),
            "lines": ("classical_lines", "target_lines"),
            "excerpts": ("classical_excerpt", "target_excerpt"),
        },
    }

    def first(names: Sequence[str]) -> object:
        for name in names:
            if occurrence.get(name) is not None:
                return occurrence[name]
        return None

    for source_kind, fields in aliases.items():
        if source_kind in nested_kinds:
            continue
        path = first(fields["paths"])
        if not path:
            continue
        recorded_lines = first(fields["lines"])
        if isinstance(recorded_lines, list) and recorded_lines:
            start = recorded_lines[0]
            end = recorded_lines[1] if len(recorded_lines) >= 2 else start
        else:
            start = end = None
        sources.append(
            {
                "source_kind": source_kind,
                "path": path,
                "recorded_sha256": first(fields["hashes"]),
                "line_start": start,
                "line_end": end,
                "excerpt": first(fields["excerpts"]) or "",
                "ledger_locator_status": (
                    None if start is not None
                    else "identity-only legacy record; no exact line asserted"
                ),
            }
        )
    return sources


def is_generic_passage(decision: dict) -> bool:
    decision_id = str(decision.get("decision_id") or "")
    term = collapse(decision.get("english_term")).casefold()
    return bool(GENERIC_PASSAGE_ID.search(decision_id)) or term == GENERIC_PASSAGE_TERM


def unit_number(unit_id: str) -> int:
    match = UNIT_ID.fullmatch(unit_id)
    if not match:
        raise ValueError(f"invalid unit id: {unit_id!r}")
    return int(match.group(1))


def discover_ledgers(repo: Path) -> list[Path]:
    evidence = repo / "evidence/classical"
    # A missing commissioned repair ledger is an error, not an empty glob.
    # Generic test/small repositories without reconciliation metadata retain
    # their ordinary discovery behavior.
    metadata_path = evidence / "SOURCE_RECONCILIATION_METADATA_20260905.json"
    if metadata_path.is_file():
        metadata, _ = read_json_bytes(metadata_path)
        for entry in metadata.get("correction_metadata", []):
            for reference in entry.get("authority_refs", []):
                logical = reference.split("#", 1)[0]
                if (logical in SEMANTIC_PROPAGATION_REPAIRS or logical in QUALIFICATION_PROPAGATION_REPAIRS or logical in APPLIED_REPAIR_LEDGERS) and not (repo / logical).is_file():
                    raise ValueError(f"missing commissioned propagation ledger: {logical}")
    paths = list(sorted((evidence / "terminology").glob("retro-*.json")))
    candidates = list((evidence / "reviews").glob("*.json"))
    candidates += list((evidence / "batches").glob("*.json"))
    candidates += list((evidence / "repairs").glob("*.json"))
    recognized_arrays = (
        "terminology_decisions",
        "decisions",
        "difficult_terminology_decisions",
        "difficult_terminology",
        "provisional_terminology_questions",
        "provisional_expert_questions",
        "terminology_and_expert_review_index",
        "difficult_decisions_and_double_checks",
    )
    for path in sorted(candidates):
        if (path.relative_to(repo).as_posix() in SEMANTIC_PROPAGATION_REPAIRS
                or path.relative_to(repo).as_posix() in QUALIFICATION_PROPAGATION_REPAIRS
                or path.relative_to(repo).as_posix() in APPLIED_REPAIR_LEDGERS):
            # Explicitly commissioned ledgers must reach their strict adapter,
            # even when malformed; discovery must not silently drop them.
            paths.append(path)
            continue
        data, _ = read_json_bytes(path)
        if isinstance(data, dict) and (
            any(
                isinstance(data.get(key), list) and data[key]
                for key in recognized_arrays
            )
            or any(
                isinstance(row, dict) and collapse(row.get("chosen_arabic"))
                for row in data.get("finding_dispositions") or []
            )
            or (
                data.get("schema")
                == "openlogic-classical-owner-followup-repairs-v1"
                and isinstance(data.get("findings"), list)
                and bool(data["findings"])
            )
        ):
            paths.append(path)
    locale_ledger = repo / "evidence/provenance/locale-ar/TERMINOLOGY_AND_ADVERSE_LEDGER.csv"
    if locale_ledger.is_file():
        paths.append(locale_ledger)
    # Stable repository-relative ordering also prevents a platform-specific
    # review/batch discovery order from changing the generated JSON.
    return sorted(set(paths), key=lambda path: path.relative_to(repo).as_posix())


def parse_repair_line_spec(value: object) -> list[tuple[int, int]]:
    ranges = []
    for part in re.split(r"\s*[,،;؛]\s*", collapse(value)):
        if not part:
            continue
        match = re.fullmatch(r"(\d+)\s*[-–]\s*(\d+)", part)
        if match:
            start, end = int(match.group(1)), int(match.group(2))
        elif part.isdigit():
            start = end = int(part)
        else:
            raise ValueError(f"invalid repair terminology line specification: {part!r}")
        if start < 1 or end < start:
            raise ValueError(f"invalid repair terminology line range: {part!r}")
        ranges.append((start, end))
    return ranges


def current_repo_hash(repo: Path, logical_path: str) -> str:
    path = repo / logical_path
    return sha256_file(path) if path.is_file() else ""


def join_text_values(value: object, separator: str = " / ") -> str:
    if isinstance(value, list):
        return separator.join(collapse(item) for item in value if collapse(item))
    return collapse(value)


def stable_row_id(prefix: str, row: dict) -> str:
    encoded = json.dumps(
        row, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return prefix + sha256_bytes(encoded)[:16].lower()


def baseline_lookup(units: Sequence[dict]) -> tuple[dict[str, dict], dict[str, list[tuple[str, str]]]]:
    by_id = {collapse(row.get("id")): row for row in units if isinstance(row, dict)}
    by_path: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for unit_id, row in by_id.items():
        for source_kind, field in (
            ("english", "source_path"),
            ("msa", "arabic_path"),
            ("classical", "target_path"),
        ):
            path = collapse(row.get(field)).replace("\\", "/").lstrip("./")
            if path:
                by_path[path.casefold()].append((unit_id, source_kind))
    return by_id, by_path


def unit_source_binding(
    repo: Path,
    unit_id: str,
    source_kind: str,
    baseline_by_id: dict[str, dict],
    payload_unit: dict | None = None,
) -> tuple[str, str]:
    """Return only a path/hash mechanically bound to this unit and language."""

    row = payload_unit or {}
    baseline = baseline_by_id.get(unit_id, {})
    fields = {
        "english": (
            ("current_english_path", "current_english_sha256"),
            ("pinned_english_path", "pinned_english_sha256"),
            ("source_path", "english_sha256"),
        ),
        "msa": (
            ("current_msa_path", "current_msa_sha256"),
            ("msa_path", "msa_sha256"),
            ("arabic_path", "arabic_sha256"),
        ),
        "classical": (
            ("current_classical_path", "current_classical_sha256"),
            ("target_path", "target_sha256"),
        ),
    }
    for source in (row, baseline):
        for path_field, hash_field in fields[source_kind]:
            path = collapse(source.get(path_field)).replace("\\", "/")
            if not path:
                continue
            digest = collapse(source.get(hash_field))
            if not digest and not re.match(r"^[A-Za-z]:/", path):
                digest = current_repo_hash(repo, path)
            return path, digest
    return "", ""


def payload_units_by_id(payload: dict) -> dict[str, dict]:
    result = {}
    for row in payload.get("units") or payload.get("unit_dispositions") or []:
        if not isinstance(row, dict):
            continue
        unit_id = collapse(row.get("id") or row.get("unit_id"))
        if unit_id:
            result[unit_id] = row
    return result


def structured_occurrence(
    unit_id: str,
    source_kind: str,
    path: str,
    digest: str,
    ranges: Sequence[tuple[int, int]],
    locator_status: str,
    excerpt: str = "",
) -> dict:
    group = {
        "path": path,
        "sha256": digest,
        "locator_status": locator_status,
    }
    if ranges:
        group["locators"] = [
            {
                "line_start": start,
                "line_end": end,
                "excerpt": excerpt if len(ranges) == 1 else "",
                "ledger_locator_status": locator_status,
            }
            for start, end in ranges
        ]
    return {"unit_id": unit_id, source_kind: group}


def current_term_bearing_excerpt(
    repo: Path,
    logical_path: str,
    start: int,
    end: int,
    source_kind: str,
    decision: dict,
) -> str:
    """Return a current span only when it visibly contains the recorded term.

    Compact historical ledgers often record line numbers without a source hash
    or excerpt.  Pairing those old numbers with a newly computed current hash
    would falsely certify drifted blank or unrelated lines.  A current excerpt
    is therefore promoted only by an exact term/component witness; otherwise
    the raw line claim remains preserved but unresolved.
    """

    candidate = Path(logical_path)
    path = candidate if candidate.is_absolute() else repo / candidate
    if not path.is_file() or start < 1 or end < start:
        return ""
    lines = path.read_text(encoding="utf-8-sig", errors="strict").splitlines()
    if end > len(lines):
        return ""
    excerpt = "\n".join(lines[start - 1:end])
    visible = strip_tex_comments(excerpt).strip()
    if not visible:
        return ""
    if source_kind == "english":
        terms = explicit_term_variants(decision.get("english_term"))
        terms += distinctive_english_term_components(decision.get("english_term"))
    else:
        terms = explicit_term_variants(decision.get("chosen_arabic"))
        terms += distinctive_arabic_term_components(decision.get("chosen_arabic"))
        terms += explicit_term_variants(decision.get("english_term"))
    normalized_visible = normalized_excerpt(visible).casefold()
    for term in terms:
        normalized_term = normalized_excerpt(term).casefold()
        if normalized_term and normalized_term in normalized_visible:
            return excerpt
    return ""


def merge_raw_occurrences(rows: Sequence[dict]) -> list[dict]:
    """Merge source groups for the same unit without discarding raw locators."""

    result: dict[str, dict] = {}
    for row in rows:
        unit_id = collapse(row.get("unit_id"))
        if not unit_id:
            continue
        target = result.setdefault(unit_id, {"unit_id": unit_id})
        for source_kind in ("english", "msa", "classical"):
            group = row.get(source_kind)
            if not isinstance(group, dict):
                continue
            existing = target.get(source_kind)
            if not isinstance(existing, dict):
                target[source_kind] = copy.deepcopy(group)
                continue
            existing_locators = list(existing.get("locators") or [])
            seen = {
                json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                for item in existing_locators
            }
            for locator in group.get("locators") or []:
                key = json.dumps(
                    locator, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                )
                if key not in seen:
                    seen.add(key)
                    existing_locators.append(copy.deepcopy(locator))
            if existing_locators:
                existing["locators"] = existing_locators
    return [result[key] for key in sorted(result)]


def compact_decision_base(
    decision_id: str,
    english_term: object,
    chosen_arabic: object,
    rationale: object,
    alternatives: Sequence[object],
    question: object,
    identity: dict,
    raw: dict,
    edition: str,
) -> dict:
    return {
        "decision_id": decision_id,
        "edition": edition,
        "english_term": join_text_values(english_term),
        "sense": collapse(raw.get("sense")),
        "chosen_arabic": join_text_values(chosen_arabic),
        "rationale": collapse(rationale),
        "alternatives": [
            {"form": collapse(item), "status": "recorded alternative"}
            for item in alternatives
            if collapse(item)
        ],
        "basis": collapse(raw.get("basis")) or "recorded-review-ledger",
        "confidence": {
            "level": collapse(raw.get("uncertainty")) or "not separately recorded",
            "reason": collapse(raw.get("authority_status") or raw.get("uncertainty")),
        },
        "expert_review_useful": raw.get("expert_review_useful") is not False,
        "expert_review_reason": collapse(
            raw.get("authority_status") or raw.get("uncertainty")
        ),
        "expert_question": collapse(question),
        "open_to_correction": True,
        "recording_mode": collapse(raw.get("recording_mode")) or "compact-ledger-adapter",
        "status": collapse(raw.get("status")) or "provisional-open-to-correction",
        "occurrences": [],
        "compact_source_record": copy.deepcopy(raw),
        "source_record": identity,
    }


def enrich_legacy_occurrence_paths(
    decision: dict,
    payload: dict,
    repo: Path,
    baseline_by_id: dict[str, dict],
) -> None:
    """Restore only unit-bound paths/hashes omitted by a legacy row schema."""

    units = payload_units_by_id(payload)
    for occurrence in decision.get("occurrences") or []:
        if not isinstance(occurrence, dict):
            continue
        unit_id = collapse(occurrence.get("unit_id"))
        for source_kind in ("english", "msa", "classical"):
            if not occurrence.get(f"{source_kind}_lines"):
                continue
            if occurrence.get(f"{source_kind}_path") or isinstance(
                occurrence.get(source_kind), dict
            ):
                continue
            path, digest = unit_source_binding(
                repo, unit_id, source_kind, baseline_by_id, units.get(unit_id)
            )
            if path:
                occurrence[f"{source_kind}_path"] = path
                occurrence[f"{source_kind}_sha256"] = digest
                occurrence[f"{source_kind}_path_binding"] = (
                    "Path and hash joined mechanically by unit ID from this ledger's "
                    "unit inventory; no line or sense was inferred."
                )


def normalize_compact_decisions(
    payload: dict,
    identity: dict,
    repo: Path,
    baseline_by_id: dict[str, dict],
) -> list[dict]:
    """Adapt the compact terminology indices used by later review/repair ledgers."""

    normalized: list[dict] = []
    units = payload_units_by_id(payload)

    for key in ("provisional_terminology_questions", "provisional_expert_questions"):
        for raw in payload.get(key) or []:
            if not isinstance(raw, dict):
                continue
            raw_id = collapse(raw.get("id"))
            english = raw.get("english_term") or raw.get("english")
            current = raw.get("chosen_arabic") or raw.get("current")
            # H-* rows are historical questions without a term or Arabic choice.
            if not raw_id or not collapse(english) or not join_text_values(current):
                continue
            alternatives = list(raw.get("alternatives") or [])
            preference = collapse(raw.get("provisional_preference"))
            if preference and preference != join_text_values(current):
                alternatives.append(preference)
            decision = compact_decision_base(
                "compact:" + raw_id,
                english,
                current,
                raw.get("rationale"),
                alternatives,
                raw.get("expert_question"),
                identity,
                raw,
                "Classical Arabic terminology review",
            )
            occurrences = []
            if key == "provisional_terminology_questions" and isinstance(
                raw.get("locations"), list
            ):
                for location in raw["locations"]:
                    if not isinstance(location, dict):
                        continue
                    unit_id = collapse(location.get("unit_id"))
                    path = collapse(location.get("path")).replace("\\", "/")
                    lines = [
                        int(value) for value in location.get("lines") or []
                        if isinstance(value, int) and value > 0
                    ]
                    if not unit_id or not path or not lines:
                        continue
                    source_kind = (
                        "classical" if "/ar-classical/" in path
                        else "msa" if "/ar/" in path
                        else "english"
                    )
                    for line in lines:
                        excerpt = current_term_bearing_excerpt(
                            repo, path, line, line, source_kind, decision
                        )
                        occurrences.append(
                            structured_occurrence(
                                unit_id,
                                source_kind,
                                path,
                                "",
                                [(line, line)],
                                "Historical compact-ledger line; promoted to an exact "
                                "current locator only when the current span contains an "
                                "exact recorded term witness.",
                                excerpt,
                            )
                        )
            if not occurrences:
                occurrences = [
                    {
                        "unit_id": unit_id,
                        "compact_locator_status": (
                            "Unit identity only; the compact ledger supplies no "
                            "unambiguous path/language/line binding."
                        ),
                        "unparsed_line_evidence": copy.deepcopy(raw.get("lines")),
                    }
                    for unit_id in raw.get("units") or []
                    if UNIT_ID.fullmatch(collapse(unit_id))
                ]
            decision["occurrences"] = merge_raw_occurrences(occurrences)
            normalized.append(decision)

    for raw in payload.get("terminology_and_expert_review_index") or []:
        if not isinstance(raw, dict):
            continue
        raw_id = collapse(raw.get("finding_id"))
        if "english_concept" not in raw and raw_id not in {"0650-N1", "0684-T1"}:
            # The 0601--0700 compact array also contains two formal proof
            # decisions. They remain in their source ledger but are not
            # misrepresented as word/sense terminology rows.
            continue
        english = raw.get("english_concept") or raw.get("term")
        chosen = raw.get("chosen_arabic") or raw.get("applied")
        if not raw_id or not collapse(english) or not collapse(chosen):
            continue
        alternatives = [
            raw.get("alternative_for_expert_check"), raw.get("rejected_here"),
            raw.get("reserved"), raw.get("allowed_synonym_retained"),
        ]
        decision = compact_decision_base(
            f"repair-compact-{Path(identity['path']).stem}:{raw_id}",
            english,
            chosen,
            raw.get("motivation"),
            alternatives,
            raw.get("double_check_prompt"),
            identity,
            raw,
            "authoritative Classical Arabic repair audit",
        )
        occurrences = []
        if "english_concept" in raw:
            unit_ids = re.findall(r"OLP-\d{4}", collapse(raw.get("unit_id")))
            for locator in raw.get("locations") or []:
                locator_text = collapse(locator)
                locator_units = re.findall(r"OLP-\d{4}", locator_text) or unit_ids[:1]
                if len(locator_units) != 1:
                    continue
                unit_id = locator_units[0]
                without_unit = re.sub(r"OLP-\d{4}", "", locator_text)
                matches = list(re.finditer(r"\b(MSA|Classical)\b", without_unit, re.I))
                for index, match in enumerate(matches):
                    tail = without_unit[match.end(): matches[index + 1].start() if index + 1 < len(matches) else None]
                    values = re.findall(r"\d+\s*(?:--|[-–])\s*\d+|\b\d+\b", tail)
                    ranges = []
                    for value in values:
                        normalized_value = re.sub(r"\s*(?:--|[–])\s*", "-", value)
                        ranges.extend(parse_repair_line_spec(normalized_value))
                    source_kind = "msa" if match.group(1).casefold() == "msa" else "classical"
                    path, _recorded_digest = unit_source_binding(
                        repo, unit_id, source_kind, baseline_by_id, units.get(unit_id)
                    )
                    if path and ranges:
                        for start, end in ranges:
                            excerpt = current_term_bearing_excerpt(
                                repo, path, start, end, source_kind, decision
                            )
                            occurrences.append(
                                structured_occurrence(
                                    unit_id, source_kind, path, "", [(start, end)],
                                    "Historical repair-index range; promoted to an exact "
                                    "current locator only with an exact term witness.",
                                    excerpt,
                                )
                            )
        else:
            finding = next(
                (
                    item for item in payload.get("finding_dispositions") or []
                    if isinstance(item, dict)
                    and collapse(item.get("finding_id")) == raw_id
                ),
                None,
            )
            if finding:
                for location in finding.get("locations") or []:
                    if not isinstance(location, dict):
                        continue
                    source_kind = collapse(location.get("layer")).casefold()
                    if source_kind not in {"english", "msa", "classical"}:
                        continue
                    unit_id = collapse(
                        location.get("unit_id") or finding.get("unit_id")
                    )
                    after = location.get("after") or {}
                    path = collapse(location.get("path") or after.get("path")).replace("\\", "/")
                    spans = after.get("line_spans") or []
                    ranges = [
                        (int(span[0]), int(span[1]))
                        for span in spans
                        if isinstance(span, list) and len(span) >= 2
                        and isinstance(span[0], int) and isinstance(span[1], int)
                    ]
                    excerpt = collapse(after.get("excerpt"))
                    if unit_id and path and ranges:
                        for start, end in ranges:
                            current_excerpt = current_term_bearing_excerpt(
                                repo, path, start, end, source_kind, decision
                            )
                            occurrences.append(
                                structured_occurrence(
                                    unit_id, source_kind, path, "", [(start, end)],
                                    "Historical post-repair span; promoted to an exact "
                                    "current locator only with an exact term witness.",
                                    current_excerpt,
                                )
                            )
            decision["rationale"] = collapse(
                (finding or {}).get("rationale") or raw.get("uncertainty")
            )
        decision["occurrences"] = merge_raw_occurrences(occurrences)
        if raw_id == "0650-N1":
            decision["authoritative_precedence_over_decision_ids"] = [
                "compact:T-ACCUMULATOR-RIGHT-FOLD"
            ]
        elif raw_id == "0684-T1":
            decision["authoritative_precedence_over_decision_ids"] = [
                "compact:T-SEMANTIC-TABLEAUX"
            ]
        normalized.append(decision)

    repair_term_names = {
        "0505-M1": "undischarged/open assumptions",
        "COND-M1": "modus ponens",
        "0524-N1": "innermost sphere",
        "0583-M1": "Axiom of Foundation / Regularity",
        "0590-N1": "transfinite induction / transfinite recursion",
    }
    repair_precedence = {
        "0505-M1": ["TERM-UNDISCHARGED-ASSUMPTION"],
        "COND-M1": ["TERM-MODUS-PONENS", "repair-0401-0500:TERM-MP"],
        "0583-M1": ["TERM-FOUNDATION-AXIOM"],
        "0590-N1": ["TERM-TRANSFINITE-INDUCTION-RECURSION"],
    }
    findings = {
        collapse(row.get("finding_id")): row
        for row in payload.get("finding_dispositions") or []
        if isinstance(row, dict)
    }
    for raw in payload.get("difficult_decisions_and_double_checks") or []:
        if not isinstance(raw, dict) or "terminology" not in collapse(raw.get("kind")).casefold():
            continue
        finding_ids = [collapse(value) for value in raw.get("finding_ids") or []]
        primary_id = finding_ids[0] if finding_ids else ""
        if primary_id not in repair_term_names:
            continue
        decision = compact_decision_base(
            f"repair-compact-{Path(identity['path']).stem}:{primary_id}",
            repair_term_names[primary_id],
            raw.get("chosen"),
            raw.get("rationale"),
            raw.get("alternatives") or [],
            raw.get("double_check_prompt"),
            identity,
            raw,
            "authoritative Classical Arabic repair audit",
        )
        decision["english_term_derivation"] = (
            "Exact concept wording transcribed from the linked finding and its "
            "double-check prompt; no new terminology decision inferred."
        )
        occurrences = []
        for finding_id in finding_ids:
            finding = findings.get(finding_id) or {}
            unit_ids = [
                collapse(value) for value in finding.get("units") or []
                if UNIT_ID.fullmatch(collapse(value))
            ]
            for location in finding.get("locations") or []:
                if not isinstance(location, dict):
                    continue
                source_kind = collapse(location.get("layer")).casefold()
                after = location.get("after") or {}
                path = collapse(after.get("path") or location.get("path")).replace("\\", "/")
                unit_id = collapse(location.get("unit_id")) or (unit_ids[0] if len(unit_ids) == 1 else "")
                if source_kind not in {"english", "msa", "classical"} or not unit_id or not path:
                    continue
                occurrence_lines = after.get("occurrence_lines") or []
                if occurrence_lines:
                    ranges = [(int(line), int(line)) for line in occurrence_lines]
                else:
                    ranges = [
                        (int(region["start"]), int(region["end"]))
                        for region in after.get("regions") or []
                        if isinstance(region, dict)
                        and isinstance(region.get("start"), int)
                        and isinstance(region.get("end"), int)
                    ]
                if ranges:
                    occurrences.append(
                        structured_occurrence(
                            unit_id, source_kind, path, collapse(after.get("sha256")),
                            ranges,
                            "Exact post-repair term locations asserted by the linked "
                            "finding disposition.",
                        )
                    )
        decision["occurrences"] = merge_raw_occurrences(occurrences)
        decision["authoritative_precedence_over_decision_ids"] = repair_precedence.get(
            primary_id, []
        )
        normalized.append(decision)

    explicit_finding_terms = {
        "QNT-01": "quantifier",
        "0177-A1": "arity / k-ary relation",
        "0186-A1": "arbitrarily large finite models",
    }
    explicit_finding_precedence = {
        "QNT-01": ["compact:T-QUANTIFIER"],
        "0177-A1": ["compact:T-ARITY"],
    }
    for raw in payload.get("finding_dispositions") or []:
        if not isinstance(raw, dict):
            continue
        raw_id = collapse(raw.get("finding_id"))
        if raw_id not in explicit_finding_terms or not collapse(raw.get("chosen_arabic")):
            continue
        alternatives = list(raw.get("rejected_or_deferred_alternatives") or [])
        if collapse(raw.get("alternative")):
            alternatives.append(raw["alternative"])
        expert_review = raw.get("expert_review") or {}
        decision = compact_decision_base(
            f"repair-compact-{Path(identity['path']).stem}:{raw_id}",
            explicit_finding_terms[raw_id],
            raw.get("chosen_arabic"),
            raw.get("rationale"),
            alternatives,
            expert_review.get("question"),
            identity,
            raw,
            "authoritative Arabic repair audit",
        )
        decision["expert_review_useful"] = expert_review.get("useful") is True
        decision["expert_review_reason"] = collapse(expert_review.get("reason"))
        decision["english_term_derivation"] = (
            "Concise English concept label taken directly from the linked finding's "
            "rationale, alternatives and review reason."
        )
        occurrences = []
        for location in raw.get("locations") or []:
            if not isinstance(location, dict):
                continue
            unit_id = collapse(location.get("unit"))
            if not unit_id and len(raw.get("units") or []) == 1:
                unit_id = collapse(raw["units"][0])
            if not UNIT_ID.fullmatch(unit_id):
                continue
            if collapse(location.get("layer")).casefold() in {"msa", "classical"}:
                source_kinds = [collapse(location["layer"]).casefold()]
            else:
                source_kinds = [
                    kind for kind in ("msa", "classical")
                    if location.get(f"{kind}_lines")
                    or location.get(f"{kind}_already_correct")
                ]
            for source_kind in source_kinds:
                path, digest = unit_source_binding(
                    repo, unit_id, source_kind, baseline_by_id, units.get(unit_id)
                )
                if not path:
                    continue
                ranges = []
                for group in location.get("line_groups") or []:
                    if isinstance(group, list) and len(group) >= 2:
                        ranges.append((int(group[0]), int(group[1])))
                direct_lines = location.get(f"{source_kind}_lines") or location.get("lines") or []
                if direct_lines:
                    if raw_id == "QNT-01":
                        ranges.extend((int(line), int(line)) for line in direct_lines)
                    elif len(direct_lines) == 2:
                        ranges.append((int(direct_lines[0]), int(direct_lines[1])))
                    else:
                        ranges.extend((int(line), int(line)) for line in direct_lines)
                occurrences.append(
                    structured_occurrence(
                        unit_id, source_kind, path, digest, ranges,
                        "Exact repair finding lines bound by unit/language to the current "
                        "source file; file-only where no line was asserted.",
                    )
                )
        decision["occurrences"] = merge_raw_occurrences(occurrences)
        decision["authoritative_precedence_over_decision_ids"] = (
            explicit_finding_precedence.get(raw_id, [])
        )
        normalized.append(decision)
    compact_keys = (
        "provisional_terminology_questions",
        "provisional_expert_questions",
        "terminology_and_expert_review_index",
        "difficult_decisions_and_double_checks",
    )
    candidate_count = sum(
        len(payload.get(key) or []) for key in compact_keys
        if isinstance(payload.get(key), list)
    )
    candidate_count += sum(
        1
        for row in payload.get("finding_dispositions") or []
        if isinstance(row, dict)
        and collapse(row.get("finding_id")) in explicit_finding_terms
        and collapse(row.get("chosen_arabic"))
    )
    if candidate_count:
        identity["adapter"] = {
            "kind": "compact-terminology-json-adapter-v1",
            "candidate_rows": candidate_count,
            "terminology_rows_contributed": len(normalized),
            "nonterminology_or_incomplete_rows_preserved_in_source_only": (
                candidate_count - len(normalized)
            ),
        }
    return normalized


LOCALE_PATH = re.compile(
    r"(?P<path>(?:[A-Za-z]:[/\\][^\s;؛,،]+|"
    r"(?:source/)?locale/ar(?:-classical)?/(?:content/)?[^\s;؛,،]+|"
    r"source/locale/ar/open-logic-config\.sty|content/[^\s;؛,،]+|"
    r"(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+\.(?:tex|sty)|"
    r"[A-Za-z0-9_.-]+\.(?:tex|sty)))",
    re.IGNORECASE,
)


def normalize_locale_path(value: str) -> str:
    path = value.replace("\\", "/").strip(" .:()[]")
    if path.startswith("locale/ar/"):
        path = "source/" + path
    return path


def locale_unit_ids(text: str) -> list[str]:
    result = []
    for match in re.finditer(r"OLP-(\d{4})((?:/\d{4})*)", text, re.I):
        candidates = [match.group(1)] + re.findall(r"\d{4}", match.group(2))
        for number in candidates:
            unit_id = "OLP-" + number
            if unit_id not in result:
                result.append(unit_id)
    return result


def line_ranges_from_locator_clause(clause: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for marker in re.finditer(r"\blines?\s+", clause, re.I):
        tail = clause[marker.end():]
        tail = re.split(
            r"\b(?:at\s+commit|in\s+commit|OLP-|theorem|proof|clause|paragraph)\b",
            tail,
            maxsplit=1,
            flags=re.I,
        )[0]
        for value in re.findall(r"\d+\s*(?:--|[-–])\s*\d+|\b\d+\b", tail):
            normalized = re.sub(r"\s*(?:--|[–])\s*", "-", value)
            for item in parse_repair_line_spec(normalized):
                if item not in ranges:
                    ranges.append(item)
    return ranges


def parse_locale_locator_evidence(
    text: str,
    repo: Path,
    baseline_by_id: dict[str, dict],
    baseline_by_path: dict[str, list[tuple[str, str]]],
) -> list[dict]:
    """Parse only explicit, mechanically unambiguous path/unit/line evidence."""

    all_units = locale_unit_ids(text)
    result: list[dict] = []
    clauses = [collapse(part) for part in re.split(r"[;؛]", text) if collapse(part)]
    for clause in clauses:
        clause_units = locale_unit_ids(clause) or all_units
        paths = list(LOCALE_PATH.finditer(clause))
        for path_match in paths:
            recorded_path = path_match.group("path")
            path = normalize_locale_path(recorded_path)
            source_kind = ""
            if "/locale/ar-classical/" in path:
                source_kind = "classical"
            elif "/locale/ar/" in path or path.startswith("source/locale/ar/"):
                source_kind = "msa"
            elif path.startswith("content/") or "pinned" in clause[:path_match.start()].casefold():
                source_kind = "english"

            candidates = baseline_by_path.get(path.casefold(), [])
            if not candidates and Path(path).name == path:
                for unit_id in clause_units:
                    unit = baseline_by_id.get(unit_id, {})
                    for kind, field in (
                        ("english", "source_path"),
                        ("msa", "arabic_path"),
                        ("classical", "target_path"),
                    ):
                        candidate_path = collapse(unit.get(field)).replace("\\", "/")
                        if Path(candidate_path).name.casefold() == path.casefold():
                            if source_kind and source_kind != kind:
                                continue
                            candidates.append((unit_id, kind))
                            path = candidate_path
            if clause_units:
                candidates = [item for item in candidates if item[0] in clause_units]
            if source_kind:
                candidates = [item for item in candidates if item[1] == source_kind]
            candidates = sorted(set(candidates))
            unit_id = candidates[0][0] if len(candidates) == 1 else ""
            if len(candidates) == 1:
                source_kind = candidates[0][1]
            ranges = line_ranges_from_locator_clause(clause)
            precision = (
                "exact-path-unit-lines" if unit_id and source_kind and ranges
                else "file-only" if unit_id and source_kind
                else "ambiguous-path-or-unit"
            )
            digest = ""
            if unit_id and source_kind:
                if source_kind == "english":
                    digest = collapse(baseline_by_id[unit_id].get("english_sha256"))
                elif not re.match(r"^[A-Za-z]:/", path):
                    digest = current_repo_hash(repo, path)
            result.append(
                {
                    "recorded_path": recorded_path,
                    "normalized_path": path,
                    "unit_id": unit_id or None,
                    "source_kind": source_kind or None,
                    "line_ranges": [list(item) for item in ranges] if precision == "exact-path-unit-lines" else [],
                    "precision": precision,
                    "current_or_pinned_sha256": digest or None,
                    "raw_clause": clause,
                    "candidate_unit_language_bindings": [list(item) for item in candidates],
                    "recorded_unit_ids": clause_units,
                }
            )
    if not result and (all_units or re.search(r"\blines?\s+\d", text, re.I)):
        result.append(
            {
                "recorded_path": None,
                "normalized_path": None,
                "unit_id": all_units[0] if len(all_units) == 1 else None,
                "source_kind": None,
                "line_ranges": [],
                "precision": "ambiguous-unit-or-line-without-path",
                "current_or_pinned_sha256": None,
                "raw_clause": text,
                "candidate_unit_language_bindings": [],
                "recorded_unit_ids": all_units,
            }
        )
    return result


def locale_semicolon_components(value: object) -> list[str]:
    """Return the explicitly recorded, top-level terminology components."""

    return [
        collapse(item).strip("`'\"“”«» ,،.;؛: ")
        for item in re.split(r"\s*[;؛]\s*", collapse(value))
        if collapse(item).strip("`'\"“”«» ,،.;؛: ")
    ]


def locale_english_search_component(value: str) -> str:
    """Remove only a terminal parenthesized sense label from an English term."""

    without_label = re.sub(r"\s*\([^()]*\)\s*$", "", collapse(value)).strip()
    return without_label or collapse(value)


def exact_locale_term_hits(
    path: Path,
    logical_path: str,
    term: str,
    source_kind: str,
    cache: dict[Path, dict],
) -> tuple[list[dict], str]:
    """Locate exact visible term strings while preserving source line numbers."""

    resolved = path.resolve()
    if resolved not in cache:
        data = resolved.read_bytes()
        text = data.decode("utf-8-sig")
        visible = strip_tex_comments(text)
        cache[resolved] = {
            "text": text,
            "visible": visible,
            "lines": text.splitlines(),
            "sha256": sha256_bytes(data),
            "logical_path": logical_path,
        }
    snapshot = cache[resolved]
    search_term = unicodedata.normalize("NFC", collapse(term))
    tokens = re.findall(r"\S+", search_term)
    if not tokens:
        return [], snapshot["sha256"]
    body = r"\s+".join(re.escape(token) for token in tokens)
    if search_term[0].isalnum():
        body = r"(?<!\w)" + body
    if search_term[-1].isalnum():
        body += r"(?!\w)"
    flags = re.IGNORECASE if source_kind == "english" else 0
    matches = list(re.finditer(body, snapshot["visible"], flags))
    hits = []
    for match in matches:
        start = line_for_offset(snapshot["visible"], match.start())
        end = line_for_offset(snapshot["visible"], match.end() - 1)
        hits.append(
            {
                "line_start": start,
                "line_end": end,
                "excerpt": "\n".join(snapshot["lines"][start - 1:end]),
            }
        )
    return hits, snapshot["sha256"]


def backtrack_locale_choice_occurrences(
    repo: Path,
    english_root: Path | None,
    baseline_units: Sequence[dict],
    english_term: object,
    chosen_arabic: object,
    source_cache: dict[Path, dict],
) -> tuple[list[dict], dict]:
    """Recover only unique, exact, three-way occurrences in baseline-paired files.

    This intentionally does not infer a unit from a corpus-wide lexical hit.  A
    component is promoted only inside one baseline unit when its recorded
    English form and recorded Arabic form each occur exactly once in that
    unit's English, MSA, and Classical files.  The pinned English hash must also
    match the file inspected.  Multiple or absent hits remain unresolved.
    """

    english_parts = locale_semicolon_components(english_term)
    arabic_parts = locale_semicolon_components(chosen_arabic)
    metadata = {
        "schema": "locale-ar-exact-three-way-backtracking-v1",
        "rule": (
            "A paired component is bound only when the BASELINE unit supplies all "
            "three files, the inspected English bytes equal BASELINE.english_sha256, "
            "and the explicit English and Arabic component strings each have exactly "
            "one visible non-comment occurrence in English, MSA, and Classical."
        ),
        "component_pair_count": 0,
        "resolved_component_pair_count": 0,
        "resolved_unit_count": 0,
        "resolved_three_way_location_count": 0,
        "unresolved_component_pairs": [],
        "rejection_counts": {},
    }
    if english_root is None:
        metadata["status"] = "unresolved-english-root-unavailable"
        return [], metadata
    if len(english_parts) != len(arabic_parts):
        metadata["status"] = "unresolved-component-cardinality-mismatch"
        metadata["english_component_count"] = len(english_parts)
        metadata["arabic_component_count"] = len(arabic_parts)
        return [], metadata

    pairs = [
        (locale_english_search_component(english), arabic)
        for english, arabic in zip(english_parts, arabic_parts)
    ]
    metadata["component_pair_count"] = len(pairs)
    english_frequency = Counter(item[0].casefold() for item in pairs)
    arabic_frequency = Counter(item[1] for item in pairs)
    eligible_pairs = []
    for english, arabic in pairs:
        if len(english) < 3 or len(arabic) < 3:
            metadata["unresolved_component_pairs"].append(
                {"english": english, "arabic": arabic, "reason": "component-too-short"}
            )
        elif english_frequency[english.casefold()] != 1 or arabic_frequency[arabic] != 1:
            metadata["unresolved_component_pairs"].append(
                {
                    "english": english,
                    "arabic": arabic,
                    "reason": "repeated-component-makes-pairing-ambiguous",
                }
            )
        else:
            eligible_pairs.append((english, arabic))

    rejection_counts: Counter[str] = Counter()
    resolved_pair_keys: set[tuple[str, str]] = set()
    occurrences: list[dict] = []
    for unit in baseline_units:
        unit_id = collapse(unit.get("id"))
        logical_paths = {
            "english": collapse(unit.get("source_path")).replace("\\", "/"),
            "msa": collapse(unit.get("arabic_path")).replace("\\", "/"),
            "classical": collapse(unit.get("target_path")).replace("\\", "/"),
        }
        paths = {
            "english": english_root / logical_paths["english"],
            "msa": repo / logical_paths["msa"],
            "classical": repo / logical_paths["classical"],
        }
        if not unit_id or not all(logical_paths.values()) or not all(
            path.is_file() for path in paths.values()
        ):
            rejection_counts["paired-source-file-unavailable"] += len(eligible_pairs)
            continue
        unit_groups: dict[str, dict] = {}
        for english, arabic in eligible_pairs:
            hits: dict[str, list[dict]] = {}
            hashes: dict[str, str] = {}
            for source_kind, term in (
                ("english", english), ("msa", arabic), ("classical", arabic)
            ):
                hits[source_kind], hashes[source_kind] = exact_locale_term_hits(
                    paths[source_kind], logical_paths[source_kind], term,
                    source_kind, source_cache,
                )
            pinned_english = collapse(unit.get("english_sha256")).upper()
            if not pinned_english or hashes["english"].upper() != pinned_english:
                rejection_counts["english-pinned-hash-mismatch"] += 1
                continue
            nonunique = [kind for kind in ("english", "msa", "classical") if len(hits[kind]) != 1]
            if nonunique:
                for kind in nonunique:
                    rejection_counts[f"{kind}-hit-count-{min(len(hits[kind]), 2)}"] += 1
                continue
            witness = {
                "schema": "locale-ar-exact-three-way-term-witness-v1",
                "english_component": english,
                "arabic_component": arabic,
                "rule": "unique-exact-visible-hit-in-each-baseline-paired-file",
            }
            for source_kind in ("english", "msa", "classical"):
                group = unit_groups.setdefault(
                    source_kind,
                    {
                        "path": logical_paths[source_kind],
                        "sha256": hashes[source_kind],
                        "locator_status": (
                            "Backtracked from an exact unique term pair across the "
                            "BASELINE-bound English, MSA, and Classical files."
                        ),
                        "locators": [],
                    },
                )
                locator = copy.deepcopy(hits[source_kind][0])
                locator["ledger_locator_status"] = group["locator_status"]
                locator["witness"] = copy.deepcopy(witness)
                group["locators"].append(locator)
            resolved_pair_keys.add((english, arabic))
        if unit_groups:
            occurrence = {"unit_id": unit_id}
            occurrence.update(unit_groups)
            occurrence["locale_occurrence_binding"] = (
                "Exact unique three-way terminology witness; no lexical sense, "
                "nearest line, or source unit was inferred."
            )
            occurrences.append(occurrence)

    metadata["resolved_component_pair_count"] = len(resolved_pair_keys)
    metadata["resolved_unit_count"] = len(occurrences)
    metadata["resolved_three_way_location_count"] = sum(
        len(group.get("locators") or [])
        for occurrence in occurrences
        for group in (occurrence.get(kind) for kind in ("english", "msa", "classical"))
        if isinstance(group, dict)
    )
    metadata["rejection_counts"] = dict(sorted(rejection_counts.items()))
    for english, arabic in eligible_pairs:
        if (english, arabic) not in resolved_pair_keys:
            metadata["unresolved_component_pairs"].append(
                {
                    "english": english,
                    "arabic": arabic,
                    "reason": "no-baseline-unit-with-one-exact-hit-in-all-three-files",
                }
            )
    metadata["status"] = (
        "resolved" if occurrences and not metadata["unresolved_component_pairs"]
        else "partially-resolved" if occurrences
        else "unresolved-no-unique-three-way-witness"
    )
    return occurrences, metadata


def normalize_locale_csv(
    repo: Path,
    raw_bytes: bytes,
    identity: dict,
    baseline_units: Sequence[dict],
    english_root: Path | None = None,
) -> list[dict]:
    """Adapt chosen CSV rows and preserve the complete mixed ledger losslessly."""

    baseline_by_id, baseline_by_path = baseline_lookup(baseline_units)
    reader = csv.DictReader(io.StringIO(raw_bytes.decode("utf-8-sig")))
    records = []
    decisions = []
    exact_source_cache: dict[Path, dict] = {}
    backtracking_counts: Counter[str] = Counter()
    for row_number, original in enumerate(reader, 2):
        raw = {str(key): str(value or "") for key, value in original.items()}
        record_id = stable_row_id("locale-ar-record-", raw)
        locator_text = " ; ".join(
            value for value in (
                raw.get("domain_or_context", ""), raw.get("evidence_or_rationale", "")
            ) if collapse(value)
        )
        locators = parse_locale_locator_evidence(
            locator_text, repo, baseline_by_id, baseline_by_path
        )
        record = {
            "record_id": record_id,
            "source_row": row_number,
            "raw": raw,
            "parsed_locator_evidence": locators,
            "terminology_decision_included": raw.get("status", "").casefold().startswith("chosen"),
        }
        records.append(record)
        if not record["terminology_decision_included"]:
            continue
        alternatives = []
        if collapse(raw.get("adverse_or_rejected")):
            alternatives.append(
                {
                    "form": collapse(raw["adverse_or_rejected"]),
                    "status": "adverse or rejected form recorded in source ledger",
                }
            )
        if collapse(raw.get("aliases_or_notes")):
            alternatives.append(
                {
                    "form": collapse(raw["aliases_or_notes"]),
                    "status": "alias or note recorded in source ledger",
                }
            )
        occurrences = []
        recorded_unit_ids: list[str] = []
        for locator in locators:
            for unit_id in locator.get("recorded_unit_ids") or []:
                if UNIT_ID.fullmatch(collapse(unit_id)) and unit_id not in recorded_unit_ids:
                    recorded_unit_ids.append(unit_id)
            unit_id = collapse(locator.get("unit_id"))
            source_kind = collapse(locator.get("source_kind"))
            path = collapse(locator.get("normalized_path"))
            if not unit_id or source_kind not in {"english", "msa", "classical"} or not path:
                continue
            ranges = [tuple(item) for item in locator.get("line_ranges") or []]
            status = (
                "Exact path, unit and line syntax parsed from the locale ledger."
                if ranges else
                "File identity only; the locale ledger does not assert an exact line."
            )
            occurrences.append(
                structured_occurrence(
                    unit_id,
                    source_kind,
                    path,
                    collapse(locator.get("current_or_pinned_sha256")),
                    ranges,
                    status,
                )
            )
        occurrences = merge_raw_occurrences(occurrences)
        backtracking = None
        if not recorded_unit_ids and not occurrences:
            occurrences, backtracking = backtrack_locale_choice_occurrences(
                repo,
                english_root,
                baseline_units,
                raw.get("source_term"),
                raw.get("chosen_arabic"),
                exact_source_cache,
            )
            backtracking_counts["candidate_decisions"] += 1
            if occurrences:
                backtracking_counts["decisions_bound"] += 1
                backtracking_counts["units_bound"] += len(occurrences)
                backtracking_counts["three_way_locations_bound"] += int(
                    backtracking.get("resolved_three_way_location_count") or 0
                )
            else:
                backtracking_counts["decisions_unresolved"] += 1
            if backtracking.get("status") == "partially-resolved":
                backtracking_counts["decisions_partially_bound"] += 1
        located_units = {collapse(row.get("unit_id")) for row in occurrences}
        for unit_id in recorded_unit_ids:
            if unit_id in located_units:
                continue
            evidence = [
                copy.deepcopy(locator)
                for locator in locators
                if unit_id in (locator.get("recorded_unit_ids") or [])
            ]
            occurrences.append(
                {
                    "unit_id": unit_id,
                    "locale_locator_status": (
                        "The locale ledger explicitly names this OLP unit, but does "
                        "not prove one source edition, path and line for the choice."
                    ),
                    "unresolved_locator_evidence": evidence,
                }
            )
        occurrences.sort(key=lambda row: collapse(row.get("unit_id")))
        decision = {
            "decision_id": stable_row_id("locale-ar-chosen-", raw),
            "edition": "shared Arabic locale terminology ledger",
            "english_term": collapse(raw.get("source_term")),
            "sense": collapse(raw.get("domain_or_context")),
            "chosen_arabic": collapse(raw.get("chosen_arabic")),
            "rationale": collapse(raw.get("evidence_or_rationale")),
            "alternatives": alternatives,
            "basis": "locale-ar terminology and adverse ledger",
            "confidence": {
                "level": collapse(raw.get("review_status")) or "not separately recorded",
                "reason": collapse(raw.get("review_status")),
            },
            "expert_review_useful": "pending" in raw.get("review_status", "").casefold(),
            "expert_review_reason": collapse(raw.get("review_status")),
            "expert_question": "",
            "open_to_correction": True,
            "recording_mode": "deterministic-locale-csv-adapter",
            "status": collapse(raw.get("status")),
            "occurrences": occurrences,
            "unresolved_locator_evidence": [
                copy.deepcopy(locator)
                for locator in locators
                if locator.get("precision") != "exact-path-unit-lines"
            ],
            "locale_ledger_record": record,
            "locale_occurrence_backtracking": backtracking,
            "source_record": identity,
        }
        decisions.append(decision)

    precision_counts = Counter(
        locator["precision"]
        for record in records
        for locator in record["parsed_locator_evidence"]
    )
    chosen_precision_counts = Counter(
        locator["precision"]
        for record in records
        if record["terminology_decision_included"]
        for locator in record["parsed_locator_evidence"]
    )
    identity["adapter"] = {
        "kind": "locale-ar-terminology-and-adverse-csv-v1",
        "raw_records": len(records),
        "chosen_terminology_records_contributed": len(decisions),
        "adverse_or_repair_records_preserved_machine_only": (
            len(records) - len(decisions)
        ),
        "parsed_locator_precision_counts": dict(sorted(precision_counts.items())),
        "chosen_locator_precision_counts": dict(
            sorted(chosen_precision_counts.items())
        ),
        "exact_three_way_backtracking": dict(sorted(backtracking_counts.items())),
    }
    identity["_locale_records"] = records
    public_identity = {
        key: copy.deepcopy(value)
        for key, value in identity.items()
        if not key.startswith("_")
    }
    for decision in decisions:
        decision["source_record"] = public_identity
    return decisions


def normalize_repair_decisions(payload: dict, identity: dict) -> list[dict]:
    """Adapt an authoritative repair audit's terminology rows losslessly."""

    repair_rows = payload.get("difficult_terminology_decisions")
    if not isinstance(repair_rows, list):
        return []
    unit_sources = {
        str(row.get("unit_id")): row
        for row in payload.get("unit_dispositions") or []
        if isinstance(row, dict)
    }
    scope_slug = Path(str(identity["path"])).stem
    normalized = []
    for raw in repair_rows:
        if not isinstance(raw, dict):
            continue
        raw_id = collapse(raw.get("id"))
        if not raw_id:
            raise ValueError(f"repair terminology decision without id in {identity['path']}")
        grouped: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
        for location in raw.get("representative_locations") or []:
            if not isinstance(location, dict):
                continue
            unit_id = collapse(location.get("unit_id"))
            edition = collapse(location.get("edition")).casefold()
            source_kind = "english" if edition in {"en", "english"} else edition
            if source_kind not in {"english", "msa", "classical"}:
                raise ValueError(
                    f"{raw_id}: invalid repair representative edition {edition!r}"
                )
            path = collapse(location.get("path"))
            source_info = unit_sources.get(unit_id, {}).get(source_kind, {})
            recorded_hash = collapse(source_info.get("after_live_sha256"))
            if collapse(source_info.get("path")) != path:
                recorded_hash = ""
            for start, end in parse_repair_line_spec(location.get("lines")):
                grouped[(unit_id, source_kind, path, recorded_hash)].append(
                    {
                        "line_start": start,
                        "line_end": end,
                        "excerpt": "",
                        "repair_locator_status": (
                            "Exact line asserted by authoritative repair ledger and bound "
                            "to its recorded post-repair file hash."
                        ),
                    }
                )
        occurrences_by_unit: dict[str, dict] = {}
        for (unit_id, source_kind, path, recorded_hash), locators in grouped.items():
            occurrence = occurrences_by_unit.setdefault(unit_id, {"unit_id": unit_id})
            occurrence[source_kind] = {
                "path": path,
                "sha256": recorded_hash,
                "locators": sorted(
                    locators, key=lambda item: (item["line_start"], item["line_end"])
                ),
            }
        authority_status = collapse(raw.get("authority_status"))
        selected = collapse(
            raw.get("post_repair_current_arabic")
            or raw.get("audit_snapshot_current_arabic")
        )
        normalized.append(
            {
                "decision_id": f"repair-{scope_slug}:{raw_id}",
                "edition": "classical repair audit",
                "english_term": collapse(raw.get("english_term")),
                "sense": (
                    "Project-wide consistency of the listed technical expression in the "
                    "authoritative post-repair source state."
                ),
                "chosen_arabic": selected,
                "grammatical_realization": (
                    "Current source realizations are listed verbatim; the review question "
                    "asks whether they should be unified."
                ),
                "rationale": collapse(raw.get("motivation")),
                "alternatives": [
                    {"form": collapse(value), "status": "expert alternative"}
                    for value in raw.get("alternatives") or []
                ],
                "authority_checks": [
                    {
                        "result": (
                            "not-found-in-checked-sources"
                            if "no official" in authority_status.casefold()
                            else "repair-audit-recorded"
                        ),
                        "note": authority_status,
                    }
                ],
                "basis": "authoritative-repair-audit",
                "confidence": {
                    "level": "medium",
                    "reason": authority_status
                    or "Current terminology is exactly located by the repair audit.",
                },
                "expert_review_useful": True,
                "expert_review_reason": authority_status,
                "expert_question": collapse(raw.get("expert_question")),
                "open_to_correction": True,
                "recording_mode": "authoritative-repair-audit",
                "status": "provisional-in-use",
                "occurrences": [
                    occurrences_by_unit[key] for key in sorted(occurrences_by_unit)
                ],
                "authoritative_precedence_over_decision_ids": sorted(
                    collapse(value)
                    for value in raw.get("existing_decision_ids") or []
                    if collapse(value)
                ),
                "repair_record": copy.deepcopy(raw),
                "source_record": identity,
            }
        )
    return normalized


def normalize_owner_followup_findings(payload: dict, identity: dict) -> list[dict]:
    """Adapt the hash-bound owner follow-up ledger without losing its evidence."""

    rows = payload.get("findings")
    if not isinstance(rows, list):
        return []
    if payload.get("schema") != "openlogic-classical-owner-followup-repairs-v1":
        return []

    scope_slug = Path(str(identity["path"])).stem
    normalized = []
    for raw in rows:
        if not isinstance(raw, dict):
            raise ValueError(f"non-object owner follow-up finding in {identity['path']}")
        finding_id = collapse(raw.get("finding_id"))
        unit_id = collapse(raw.get("unit_id"))
        if not finding_id or not UNIT_ID.fullmatch(unit_id):
            raise ValueError(
                f"owner follow-up finding lacks a valid id/unit in {identity['path']}"
            )

        occurrence_rows = []
        english = raw.get("english")
        if isinstance(english, dict):
            path = collapse(english.get("path"))
            digest = collapse(english.get("sha256"))
            ranges = parse_repair_line_spec(english.get("lines"))
            if path and digest:
                occurrence_rows.append(
                    structured_occurrence(
                        unit_id,
                        "english",
                        path,
                        digest,
                        ranges,
                        "Exact English lines and file identity asserted by the hash-bound "
                        "owner follow-up ledger.",
                    )
                )

        current = raw.get("current")
        if isinstance(current, dict):
            for source_kind in ("msa", "classical"):
                group = current.get(source_kind)
                if not isinstance(group, dict):
                    continue
                path = collapse(group.get("path"))
                digest = collapse(group.get("sha256"))
                ranges = parse_repair_line_spec(group.get("term_lines"))
                if path and digest:
                    occurrence_rows.append(
                        structured_occurrence(
                            unit_id,
                            source_kind,
                            path,
                            digest,
                            ranges,
                            "Exact current term lines and file identity asserted by the "
                            "hash-bound owner follow-up ledger.",
                        )
                    )

        expert = raw.get("expert_review")
        if not isinstance(expert, dict):
            expert = {}
        normalized.append(
            {
                "decision_id": f"owner-followup-{scope_slug}:{finding_id}",
                "recorded_decision_id": finding_id,
                "edition": "MSA and Classical owner follow-up",
                "english_term": collapse(raw.get("source_term")),
                "sense": collapse(raw.get("problem")),
                "chosen_arabic": collapse(raw.get("chosen_arabic")),
                "rationale": collapse(raw.get("rationale")),
                "alternatives": [
                    {"form": collapse(value), "status": "recorded alternative"}
                    for value in raw.get("alternatives") or []
                    if collapse(value)
                ],
                "basis": "hash-bound-owner-followup-repair",
                "confidence": {
                    "level": "medium",
                    "reason": (
                        "The applied wording and exact current source identities are "
                        "verified; the specialist wording remains open to correction."
                    ),
                },
                "expert_review_useful": bool(expert.get("sensitive", True)),
                "expert_review_reason": collapse(raw.get("problem")),
                "expert_question": collapse(expert.get("question")),
                "open_to_correction": bool(expert.get("open_to_correction", True)),
                "recording_mode": "authoritative-hash-bound-owner-followup",
                "status": "provisional-in-use",
                "occurrences": merge_raw_occurrences(occurrence_rows),
                "owner_followup_record": copy.deepcopy(raw),
                "source_record": identity,
            }
        )
    return normalized


def normalize_semantic_propagation_repairs(
    payload: dict, identity: dict, repo: Path,
    baseline_by_id: dict[str, dict], english_root: Path | None,
) -> tuple[list[dict], dict[Path, str]]:
    """Admit the three dated MP repairs as distinct, live-hash-bound decisions.

    These are newly assessed source repairs, not reconstructions of old private
    deliberation. Validate the complete ledger before returning any decisions;
    old labels and historical review qualifications remain verbatim evidence.
    """
    logical = identity["path"]
    contract = SEMANTIC_PROPAGATION_REPAIRS.get(logical)
    known_schemas = {row[0] for row in SEMANTIC_PROPAGATION_REPAIRS.values()}
    if contract is None:
        if payload.get("schema") in known_schemas:
            raise ValueError(f"unexpected semantic propagation ledger path: {logical}")
        return [], {}
    schema, expected_units = contract
    if payload.get("schema") != schema:
        raise ValueError(f"{logical}: unexpected semantic propagation schema")
    if (payload.get("assessed_on") != "2026-09-06"
            or payload.get("recording_mode") != "new-independent-assessment-of-retained-translation"
            or payload.get("status") != "implemented-in-shared-msa-source"):
        raise ValueError(f"{logical}: invalid new repair assessment provenance")
    for field in ("source_term", "sense", "before_arabic", "chosen_arabic", "rationale"):
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            raise ValueError(f"{logical}: empty/malformed propagation {field}")
    if payload["source_term"] != "modus ponens" or payload["before_arabic"] == payload["chosen_arabic"]:
        raise ValueError(f"{logical}: unexpected propagation term or unchanged choice")
    expert = payload.get("expert_review")
    if (not isinstance(expert, dict)
            or not isinstance(expert.get("question"), str) or not expert["question"].strip()
            or expert.get("useful") is not True or expert.get("open_to_correction") is not True
            or expert.get("official_attestation_claimed") is not False
            or expert.get("non_blocking") is not True):
        raise ValueError(f"{logical}: invalid propagation expert question/provenance")
    alternatives = payload.get("alternatives")
    if (not isinstance(alternatives, list) or not alternatives
            or any(not isinstance(row, dict) or any(
                not isinstance(row.get(key), str) or not row[key].strip()
                for key in ("form", "disposition", "reason")
            ) for row in alternatives)):
        raise ValueError(f"{logical}: malformed propagation alternatives")
    singular = schema == "openlogic-semantic-propagation-repair-v1"
    rows = [payload] if singular else payload.get("units")
    if (not isinstance(rows, list) or len(rows) != len(expected_units)
            or any(not isinstance(row, dict) for row in rows)
            or {row.get("unit_id") for row in rows} != set(expected_units)):
        raise ValueError(f"{logical}: unexpected/duplicate propagation units")
    if english_root is None:
        raise ValueError(f"{logical}: English propagation source root unavailable")
    normalized, hashes = [], {}
    for row in rows:
        unit_id = row["unit_id"]
        finding_id = unit_id[4:] + "-P1"
        if row.get("finding_id") != finding_id:
            raise ValueError(f"{logical}: unexpected propagation finding ID")
        locations = row.get("locations") if singular else row
        page = locations if singular else payload
        if (not isinstance(locations, dict) or "printed_page" not in page
                or page["printed_page"] is not None
                or page.get("page_status") != "bind-after-final-reader-build"):
            raise ValueError(f"{finding_id}: propagation must not assert a reader page")
        baseline = baseline_by_id.get(unit_id)
        if not isinstance(baseline, dict):
            raise ValueError(f"{finding_id}: missing propagation baseline unit")
        occurrence = {"unit_id": unit_id, "context_note": (
            "New 2026-09-06 semantic repair assessment; shared MSA correction also applies "
            "to International and Machrek. Classical wording was already correct. "
            "Reader pages await independent final-build evidence."
        )}
        before_witness = None
        for kind, field, prefix in (
            ("english", "source_path", ""),
            ("msa", "arabic_path", "source/locale/ar/"),
            ("classical", "target_path", "source/locale/ar-classical/"),
        ):
            declaration = locations.get(kind)
            expected_path = prefix + expected_units[unit_id]
            if (not isinstance(declaration, dict) or declaration.get("path") != expected_path
                    or baseline.get(field) != expected_path):
                raise ValueError(f"{finding_id}: unexpected {kind} propagation path")
            base = english_root.resolve() if kind == "english" else repo.resolve()
            target = (base / expected_path).resolve()
            allowed = (base / ("content" if kind == "english" else prefix)).resolve()
            if not path_is_within(target, allowed) or not target.is_file():
                raise ValueError(f"{finding_id}: missing/out-of-scope propagation source")
            data = target.read_bytes()
            digest = sha256_bytes(data)
            recorded = declaration.get("after_sha256" if kind == "msa" else "sha256")
            if not isinstance(recorded, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", recorded) or digest != recorded.upper():
                raise ValueError(f"{finding_id}: {kind} propagation source hash mismatch")
            if kind == "english" and digest != str(baseline.get("english_sha256", "")).upper():
                raise ValueError(f"{finding_id}: English propagation baseline hash mismatch")
            byte_field = "after_bytes" if kind == "msa" else "bytes"
            if byte_field in declaration and (type(declaration[byte_field]) is not int or declaration[byte_field] != len(data)):
                raise ValueError(f"{finding_id}: {kind} propagation byte count mismatch")
            text = data.decode("utf-8-sig")
            lines = text.splitlines()
            start, end = declaration.get("line_start"), declaration.get("line_end")
            if type(start) is not int or type(end) is not int or not 1 <= start <= end <= len(lines):
                raise ValueError(f"{finding_id}: invalid {kind} propagation line range")
            excerpt = "\n".join(lines[start - 1:end])
            term = payload["source_term"] if kind == "english" else payload["chosen_arabic"]
            visible = normalized_excerpt(strip_tex_comments(excerpt)).casefold()
            if normalized_excerpt(term).casefold() not in visible:
                raise ValueError(f"{finding_id}: {kind} propagation lines lack the recorded term")
            hashes[target] = digest
            occurrence[kind] = structured_occurrence(
                unit_id, kind, expected_path, digest, [(start, end)],
                "dated-propagation-repair-live-hash-and-term-verified", excerpt,
            )[kind]
            if kind == "msa":
                chosen, old = payload["chosen_arabic"], payload["before_arabic"]
                if text.count(chosen) != 1:
                    raise ValueError(f"{finding_id}: non-unique propagation inverse replacement")
                before = data.replace(chosen.encode("utf-8"), old.encode("utf-8"), 1)
                before_digest = sha256_bytes(before)
                if (before_digest != str(declaration.get("before_sha256", "")).upper()
                        or type(declaration.get("before_bytes")) is not int
                        or len(before) != declaration["before_bytes"]):
                    raise ValueError(f"{finding_id}: propagation inverse/before hash mismatch")
                before_witness = {
                    "path": expected_path, "sha256": before_digest, "bytes": len(before),
                    "line_start": start, "line_end": end,
                    "excerpt": "\n".join(before.decode("utf-8-sig").splitlines()[start - 1:end]),
                    "status": "historical-before-bytes-proved-by-exact-inverse-not-current-source",
                }
        normalized.append({
            "decision_id": f"semantic-propagation-20260906:{finding_id}",
            "recorded_decision_id": finding_id,
            "edition": "Shared MSA (International and Machrek); Classical already correct",
            "english_term": payload["source_term"], "sense": payload["sense"],
            "before_arabic": payload["before_arabic"], "chosen_arabic": payload["chosen_arabic"],
            "assessed_on": payload["assessed_on"],
            "rationale": (
                "New independent assessment dated 2026-09-06; not a reconstruction of "
                "the original translator's deliberation. " + payload["rationale"]
            ),
            "alternatives": [{**copy.deepcopy(alt), "status": alt["disposition"]} for alt in alternatives],
            "basis": "authoritative-dated-semantic-propagation-repair",
            "confidence": {"level": "medium", "reason": (
                "The inference, current wording and exact inverse source hashes are checked; "
                "no official dictionary attestation is claimed. Arabic terminology remains open to correction."
            )},
            "expert_review_useful": True, "expert_review_reason": payload["sense"],
            "expert_question": expert["question"], "open_to_correction": True,
            "official_attestation_claimed": False, "expert_review_non_blocking": True,
            "recording_mode": payload["recording_mode"], "status": payload["status"],
            "occurrences": [occurrence], "printed_page": None,
            "page_status": "bind-after-final-reader-build",
            "semantic_propagation_repair": {
                "ledger_path": logical, "ledger_sha256": identity["sha256"],
                "finding_id": finding_id, "assessed_on": payload["assessed_on"],
                "historical_before_source": before_witness,
                "source_ledger": copy.deepcopy(payload),
            },
            "source_record": identity,
        })
    identity["adapter"] = {
        "kind": "dated-semantic-propagation-repair-v1", "schema": schema,
        "terminology_rows_contributed": len(normalized),
        "decision_ids": sorted(row["decision_id"] for row in normalized),
        "historical_deliberation_claimed": False,
    }
    return normalized, hashes


def load_qualification_prior_manifest(
    repo: Path, expected_units: dict[str, str], baseline_by_id: dict[str, dict],
) -> tuple[dict[str, dict], dict, dict[Path, str]]:
    """Bind batch 2 to one immutable pre-qualification source snapshot.

    OLP-0039 and OLP-0081 already contained earlier corrections. The frozen
    original MSA baseline is therefore not their immediate predecessor. Never
    substitute the mutable current overlay or accept a self-declared before hash.
    """
    if set(expected_units) != QUALIFICATION_PRIOR_MANIFEST_UNITS:
        raise ValueError("unexpected qualification prior-manifest unit contract")
    target = (repo / QUALIFICATION_PRIOR_MANIFEST_RELATIVE).resolve()
    if not path_is_within(target, (repo / "evidence/classical").resolve()) or not target.is_file():
        raise ValueError("missing/out-of-scope immutable qualification prior manifest")
    if target.stat().st_size > 2 * 1024 * 1024:
        raise ValueError("oversized immutable qualification prior manifest")
    raw = target.read_bytes()
    digest = sha256_bytes(raw)
    if digest != QUALIFICATION_PRIOR_MANIFEST_SHA256:
        raise ValueError("immutable qualification prior manifest hash mismatch")
    manifest = json.loads(raw.decode("utf-8-sig"))
    if (not isinstance(manifest, dict)
            or manifest.get("schema") != "openlogic-classical-source-closure-manifest-v1"
            or manifest.get("total_units") != 722):
        raise ValueError("invalid immutable qualification prior manifest schema/inventory")
    units = manifest.get("units")
    if (not isinstance(units, list) or len(units) != 722
            or any(not isinstance(unit, dict) for unit in units)
            or [unit.get("id") for unit in units] != [f"OLP-{i:04d}" for i in range(1, 723)]):
        raise ValueError("invalid immutable qualification prior manifest unit inventory")
    selected = {unit["id"]: unit for unit in units if unit["id"] in expected_units}
    for unit_id, relative in expected_units.items():
        unit = selected[unit_id]
        baseline = baseline_by_id.get(unit_id)
        if (not isinstance(baseline, dict)
                or unit.get("source_path") != relative
                or baseline.get("source_path") != relative
                or not isinstance(unit.get("english_sha256"), str)
                or not re.fullmatch(r"[0-9a-fA-F]{64}", unit["english_sha256"])
                or unit["english_sha256"].upper() != str(baseline.get("english_sha256", "")).upper()):
            raise ValueError(f"{unit_id}: prior-manifest English baseline identity mismatch")
        for kind, prefix, field in (
            ("msa", "source/locale/ar/", "arabic_path"),
            ("classical", "source/locale/ar-classical/", "target_path"),
        ):
            source = unit.get(kind)
            if (not isinstance(source, dict) or source.get("path") != prefix + relative
                    or baseline.get(field) != prefix + relative
                    or not isinstance(source.get("sha256"), str)
                    or not re.fullmatch(r"[0-9a-fA-F]{64}", source["sha256"])
                    or type(source.get("bytes")) is not int or source["bytes"] < 1):
                raise ValueError(f"{unit_id}: prior-manifest {kind} identity malformed/out of scope")
    identity = {"path": QUALIFICATION_PRIOR_MANIFEST_RELATIVE.as_posix(),
                "sha256": digest, "bytes": len(raw),
                "source_snapshot_sha256": manifest["source_snapshot_sha256"]}
    return selected, identity, {target: digest}


def qualification_active_phrase_ranges(
    excerpt: str, term: str, source_kind: str, start_line: int,
) -> list[tuple[int, int]]:
    """Find active literal phrase lines, not English substrings of another term."""
    pattern = excerpt_pattern(term)
    if pattern is None:
        return []
    expression = pattern.pattern
    if source_kind == "english":
        # 'enumerable' must not be certified by 'nonenumerable'. Arabic prefixes
        # such as the conjunction in 'وكل' do not create an analogous boundary.
        expression = r"(?<!\w)" + expression + r"(?!\w)"
    active = unicodedata.normalize("NFC", strip_tex_comments(excerpt))
    result = []
    for match in re.finditer(expression, active, flags=re.IGNORECASE):
        interval = (start_line + line_for_offset(active, match.start()) - 1,
                    start_line + line_for_offset(active, match.end() - 1) - 1)
        if interval not in result:
            result.append(interval)
    return result


def normalize_qualification_additional_choice(
    row: dict, parent: dict, repo: Path, english_root: Path,
    source_hashes: dict[Path, str], scope_description: str,
) -> list[dict]:
    """Expose the second OLP-0039 connective choice without reapplying its patch."""
    extras = row.get("additional_phrase_choices")
    if row["unit_id"] != "OLP-0039":
        if extras not in (None, []):
            raise ValueError("unexpected additional qualification phrase choice")
        return []
    choice_id = "0039-P1-no-surjection-connective"
    if (not isinstance(extras, list) or len(extras) != 1 or not isinstance(extras[0], dict)
            or extras[0].get("choice_id") != choice_id):
        raise ValueError("missing/duplicate/unexpected commissioned 0039 connective choice")
    extra = extras[0]
    fields = ("source_term", "before_arabic", "chosen_arabic", "classical_arabic")
    if tuple(extra.get(key) for key in fields) != ("that is", "أي لا توجد دالة", "بل لا توجد دالة", "بل لا توجد دالة"):
        raise ValueError("0039 connective literal phrase contract mismatch")
    for key in ("human_topic", "rationale", "patch_application_note"):
        if not isinstance(extra.get(key), str) or not extra[key].strip():
            raise ValueError(f"0039 connective missing {key}")
    expert = extra.get("expert_review")
    if (not isinstance(expert, dict)
            or not isinstance(expert.get("question"), str) or not expert["question"].strip()
            or expert.get("useful") is not True or expert.get("open_to_correction") is not True
            or expert.get("official_attestation_claimed") is not False
            or expert.get("non_blocking") is not True):
        raise ValueError("0039 connective expert provenance mismatch")
    if extra.get("unit_patch_indices") != [0] or type(extra["unit_patch_indices"][0]) is not int:
        raise ValueError("0039 connective must identify its containing unit patch")
    patches = extra.get("patches")
    if (not isinstance(patches, list) or len(patches) != 1 or not isinstance(patches[0], dict)
            or set(patches[0]) != {"before", "after"}
            or any(not isinstance(patches[0].get(key), str) or not patches[0][key] for key in ("before", "after"))
            or patches[0]["before"] == patches[0]["after"]
            or any(row["patches"][0][key].count(patches[0][key]) != 1 for key in ("before", "after"))):
        raise ValueError("0039 connective patch is not the recorded unit-patch subchoice")
    locations = extra.get("locations")
    if not isinstance(locations, dict) or set(locations) != {"english", "msa_before", "msa", "classical"}:
        raise ValueError("0039 connective source locations malformed")
    occurrence = {"unit_id": row["unit_id"], "context_note": (
        "Separate exact connective choice within 0039-P1, not a second source mutation. "
        + scope_description
    )}
    historical = parent["semantic_propagation_repair"]["historical_before_source"]
    prior_bytes = historical["text_utf8"].encode("utf-8")
    current_msa = None
    for kind, term in (("english", extra["source_term"]), ("msa_before", extra["before_arabic"]),
                       ("msa", extra["chosen_arabic"]), ("classical", extra["classical_arabic"])):
        location = locations[kind]
        parent_kind = "msa" if kind == "msa_before" else kind
        parent_location = row["locations"][parent_kind]
        if not isinstance(location, dict) or location.get("path") != parent_location["path"]:
            raise ValueError(f"0039 connective {kind} source path mismatch")
        if kind == "msa_before":
            data = prior_bytes
            bound_start, bound_end = parent_location["before_line_start"], parent_location["before_line_end"]
            digest = historical["sha256"]
        else:
            target = ((english_root if kind == "english" else repo) / parent_location["path"]).resolve()
            data = target.read_bytes()
            digest = sha256_bytes(data)
            if digest != source_hashes.get(target):
                raise ValueError(f"0039 connective {kind} source changed during admission")
            bound_start, bound_end = parent_location["line_start"], parent_location["line_end"]
            if kind == "msa":
                current_msa = data
        if str(location.get("sha256", "")).upper() != digest:
            raise ValueError(f"0039 connective {kind} source hash mismatch")
        if "bytes" in location and (type(location["bytes"]) is not int or location["bytes"] != len(data)):
            raise ValueError(f"0039 connective {kind} source size mismatch")
        lines = data.decode("utf-8-sig").splitlines()
        start, end = location.get("line_start"), location.get("line_end")
        if (type(start) is not int or type(end) is not int
                or not bound_start <= start <= end <= bound_end or end > len(lines)):
            raise ValueError(f"0039 connective {kind} excerpt range mismatch")
        excerpt = "\n".join(lines[start - 1:end])
        if (location.get("excerpt") != excerpt
                or str(location.get("excerpt_sha256", "")).upper() != sha256_bytes(excerpt.encode("utf-8"))):
            raise ValueError(f"0039 connective {kind} excerpt/hash mismatch")
        ranges = qualification_active_phrase_ranges(excerpt, term, parent_kind, start)
        if not ranges:
            raise ValueError(f"0039 connective {kind} active phrase missing")
        if kind != "msa_before":
            occurrence[kind] = structured_occurrence(
                row["unit_id"], kind, location["path"], digest, ranges,
                "dated-qualification-subchoice-live-hash-excerpt-and-term-verified", excerpt,
            )[kind]
            for locator in occurrence[kind]["locators"]:
                locator["excerpt"] = "\n".join(lines[locator["line_start"] - 1:locator["line_end"]])
    if (prior_bytes.count(patches[0]["before"].encode("utf-8")) != 1
            or current_msa is None or current_msa.count(patches[0]["after"].encode("utf-8")) != 1):
        raise ValueError("0039 connective patch lacks unique prior/current source witnesses")
    decision = copy.deepcopy(parent)
    decision.update(
        decision_id="semantic-propagation-20260906:" + choice_id,
        recorded_decision_id=choice_id, english_term=extra["source_term"],
        before_arabic=extra["before_arabic"], chosen_arabic=extra["chosen_arabic"],
        classical_arabic=extra["classical_arabic"], sense=extra["human_topic"],
        rationale=("New independent assessment dated 2026-09-06; not a reconstruction of "
                   "the original translator's deliberation. " + scope_description
                   + "Previous MSA wording: " + extra["before_arabic"] + ". " + extra["rationale"]),
        alternatives=[], alternative_recording_status="No separate lexical alternative recorded for this connective.",
        expert_question=expert["question"], expert_review_reason=extra["human_topic"],
        occurrences=[occurrence],
    )
    decision["semantic_propagation_repair"].update(
        choice_id=choice_id, parent_finding_id=row["finding_id"],
        choice_record=copy.deepcopy(extra),
        proof_scope="Exact subchoice within the complete unit repair; its patch is not applied twice.",
    )
    return [decision]


def normalize_qualification_propagation_repairs(
    payload: dict, identity: dict, repo: Path,
    baseline_by_id: dict[str, dict], english_root: Path | None,
) -> tuple[list[dict], dict[Path, str]]:
    """Validate commissioned qualification repairs without rewriting history.

    The English wording can itself omit a mathematical hypothesis. These records
    disclose the exact origin: inherited-source qualification or Arabic-only
    scope ambiguity. Complete current witnesses and exact reverse patches bind each
    newly assessed choice to its independently recoverable prior source bytes.
    """
    logical = identity["path"]
    contract = QUALIFICATION_PROPAGATION_REPAIRS.get(logical)
    if logical in APPLIED_REPAIR_LEDGERS:
        return [], {}
    if contract is None:
        if payload.get("schema") in {r[0] for r in QUALIFICATION_PROPAGATION_REPAIRS.values()}:
            raise ValueError(f"unexpected qualification propagation ledger path: {logical}")
        return [], {}
    schema, expected_units = contract
    if payload.get("schema") != schema:
        raise ValueError(f"{logical}: unexpected qualification propagation schema")
    if (payload.get("assessed_on") != "2026-09-06"
            or payload.get("recording_mode") != "new-independent-assessment-of-retained-translation"
            or payload.get("status") != "implemented-in-shared-msa-source"):
        raise ValueError(f"{logical}: invalid qualification assessment provenance")
    if ("printed_page" not in payload or payload["printed_page"] is not None
            or payload.get("page_status") != "bind-after-final-reader-build"
            or payload.get("rebuilt_pdf_verified") is not False
            or payload.get("published_pdf_verified") is not False):
        raise ValueError(f"{logical}: qualification repair must not assert a reader page")

    def forbid_page_claims(value: object) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if ((key == "printed_page" and item is not None)
                        or (key == "page_status" and item != "bind-after-final-reader-build")
                        or (key in {"printed_pages", "pdf_pages", "assembled_pdf_pages", "page_evidence"} and item)):
                    raise ValueError(f"{logical}: qualification repair must not assert a reader page")
                forbid_page_claims(item)
        elif isinstance(value, list):
            for item in value:
                forbid_page_claims(item)

    forbid_page_claims(payload)
    rows = payload.get("units")
    if (not isinstance(rows, list) or len(rows) != len(expected_units)
            or any(not isinstance(row, dict) for row in rows)
            or {row.get("unit_id") for row in rows} != set(expected_units)):
        raise ValueError(f"{logical}: unexpected/duplicate qualification units")
    if english_root is None:
        raise ValueError(f"{logical}: English qualification source root unavailable")
    normalized, hashes = [], {}
    prior_units, prior_identity = {}, {}
    if set(expected_units) & QUALIFICATION_PRIOR_MANIFEST_UNITS:
        prior_units, prior_identity, prior_hashes = load_qualification_prior_manifest(
            repo, expected_units, baseline_by_id
        )
        hashes.update(prior_hashes)
    for row in rows:
        unit_id = row["unit_id"]
        finding_id = unit_id[4:] + "-P1"
        if row.get("finding_id") != finding_id:
            raise ValueError(f"{logical}: unexpected qualification finding ID")
        for field in ("source_term", "before_arabic", "chosen_arabic", "classical_arabic", "sense", "rationale"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError(f"{finding_id}: empty/malformed qualification {field}")
        if row["before_arabic"] == row["chosen_arabic"]:
            raise ValueError(f"{finding_id}: unchanged qualification choice")
        if tuple(row[k] for k in ("source_term", "before_arabic", "chosen_arabic", "classical_arabic")) != QUALIFICATION_PROPAGATION_TERMS[unit_id]:
            raise ValueError(f"{finding_id}: unexpected qualification term or wording")
        classification = QUALIFICATION_PROPAGATION_CLASSIFICATIONS[unit_id]
        if row.get("classification") != classification:
            raise ValueError(f"{finding_id}: qualification origin classification mismatch")
        inherited = classification.startswith("inherited-source-")
        scope_description = (
            "Inherited-source qualification: this makes the mathematical qualification "
            "or logical scope explicit, rather than claiming only a lexical mistranslation. "
            if inherited else
            "Translation-scope clarification: the English condition is retained; this "
            "removes ambiguity in the Arabic any-versus-none wording without claiming "
            "an error in the English source. "
        )
        expert = row.get("expert_review")
        if (not isinstance(expert, dict)
                or not isinstance(expert.get("question"), str) or not expert["question"].strip()
                or expert.get("useful") is not True or expert.get("open_to_correction") is not True
                or expert.get("official_attestation_claimed") is not False
                or expert.get("non_blocking") is not True):
            raise ValueError(f"{finding_id}: invalid qualification expert question/provenance")
        alternatives = row.get("alternatives")
        if (not isinstance(alternatives, list) or not alternatives
                or any(not isinstance(alt, dict) or any(
                    not isinstance(alt.get(key), str) or not alt[key].strip()
                    for key in ("form", "disposition", "reason")
                ) for alt in alternatives)):
            raise ValueError(f"{finding_id}: malformed qualification alternatives")
        patches = row.get("patches")
        if (not isinstance(patches, list) or not patches
                or any(not isinstance(patch, dict) or set(patch) != {"before", "after"}
                       or any(not isinstance(patch.get(key), str) or not patch[key]
                              for key in ("before", "after"))
                       or patch["before"] == patch["after"] for patch in patches)):
            raise ValueError(f"{finding_id}: malformed qualification patches")
        baseline = baseline_by_id.get(unit_id)
        if not isinstance(baseline, dict):
            raise ValueError(f"{finding_id}: missing qualification baseline unit")
        locations = row.get("locations")
        if not isinstance(locations, dict) or set(locations) != set(SOURCE_LABELS):
            raise ValueError(f"{finding_id}: malformed qualification locations")
        occurrence = {"unit_id": unit_id, "context_note": (
            "New 2026-09-06 assessment. " + scope_description + "The Classical "
            "counterpart already makes the relevant qualification explicit; shared MSA "
            "corrections feed both International and Machrek. Reader pages are not yet asserted."
        )}
        before_witness = None
        current_witness_companions = []
        for kind, field, prefix, term in (
            ("english", "source_path", "", row["source_term"]),
            ("msa", "arabic_path", "source/locale/ar/", row["chosen_arabic"]),
            ("classical", "target_path", "source/locale/ar-classical/", row["classical_arabic"]),
        ):
            declaration = locations[kind]
            expected_path = prefix + expected_units[unit_id]
            if (not isinstance(declaration, dict) or declaration.get("path") != expected_path
                    or baseline.get(field) != expected_path):
                raise ValueError(f"{finding_id}: unexpected {kind} qualification path")
            base = english_root.resolve() if kind == "english" else repo.resolve()
            target = (base / expected_path).resolve()
            allowed = (base / ("content" if kind == "english" else prefix)).resolve()
            if not path_is_within(target, allowed) or not target.is_file():
                raise ValueError(f"{finding_id}: missing/out-of-scope qualification source")
            data = target.read_bytes()
            digest = sha256_bytes(data)
            recorded = declaration.get("after_sha256" if kind == "msa" else "sha256")
            if (unit_id == "OLP-0008" and kind == "classical" and digest != str(recorded).upper()
                    and (repo / APPLIED_CLASSICAL_REFRESH).is_file()):
                declaration, companion = refreshed_classical_qualification(
                    repo, english_root, baseline_by_id, identity, row, hashes
                )
                current_witness_companions.append(companion)
                recorded = declaration["sha256"]
            if (not isinstance(recorded, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", recorded)
                    or digest != recorded.upper()):
                raise ValueError(f"{finding_id}: {kind} qualification source hash mismatch")
            if kind == "english" and digest != str(baseline.get("english_sha256", "")).upper():
                raise ValueError(f"{finding_id}: English qualification baseline hash mismatch")
            byte_field = "after_bytes" if kind == "msa" else "bytes"
            if type(declaration.get(byte_field)) is not int or declaration[byte_field] != len(data):
                raise ValueError(f"{finding_id}: {kind} qualification byte count mismatch")
            prior_unit = prior_units.get(unit_id)
            if prior_unit and kind == "english" and digest != prior_unit["english_sha256"].upper():
                raise ValueError(f"{finding_id}: English immutable prior-manifest identity mismatch")
            if prior_unit and kind == "classical" and (
                digest != prior_unit["classical"]["sha256"].upper()
                or len(data) != prior_unit["classical"]["bytes"]
            ):
                raise ValueError(f"{finding_id}: Classical immutable prior-manifest identity mismatch")
            text = data.decode("utf-8-sig")
            lines = text.splitlines()
            start, end = declaration.get("line_start"), declaration.get("line_end")
            if type(start) is not int or type(end) is not int or not 1 <= start <= end <= len(lines):
                raise ValueError(f"{finding_id}: invalid {kind} qualification line range")
            excerpt = "\n".join(lines[start - 1:end])
            if declaration.get("excerpt") != excerpt:
                raise ValueError(f"{finding_id}: {kind} qualification excerpt mismatch")
            if sha256_bytes(excerpt.encode("utf-8")) != str(declaration.get("excerpt_sha256", "")).upper():
                raise ValueError(f"{finding_id}: {kind} qualification excerpt hash mismatch")
            visible = normalized_excerpt(strip_tex_comments(excerpt)).casefold()
            if normalized_excerpt(term).casefold() not in visible:
                raise ValueError(f"{finding_id}: {kind} qualification lines lack the recorded term")
            # Every admitted qualification witness is context, not an occurrence
            # bounding box. Keep all active literal phrase locations inside that
            # exact hash-/excerpt-verified witness, including the first batch.
            # Its complete declared context remains losslessly in source_ledger;
            # narrowing must not depend on which predecessor proves the inverse.
            term_ranges = qualification_active_phrase_ranges(excerpt, term, kind, start)
            if not term_ranges:
                raise ValueError(f"{finding_id}: {kind} qualification lines lack the recorded term")
            hashes[target] = digest
            occurrence[kind] = structured_occurrence(
                unit_id, kind, expected_path, digest, term_ranges,
                "dated-qualification-repair-live-hash-excerpt-and-term-verified", excerpt,
            )[kind]
            for locator in occurrence[kind]["locators"]:
                locator["excerpt"] = "\n".join(lines[locator["line_start"] - 1:locator["line_end"]])
            if kind == "msa":
                changed_ranges = []
                for patch in patches:
                    if text.count(patch["after"]) != 1:
                        raise ValueError(f"{finding_id}: non-unique qualification current patch")
                    patch_start = line_for_offset(text, text.index(patch["after"]))
                    changed_ranges.append([patch_start, patch_start + patch["after"].count("\n")])
                recorded_ranges = declaration.get("changed_ranges")
                if (not isinstance(recorded_ranges, list)
                        or any(not isinstance(r, list) or len(r) != 2
                               or any(type(n) is not int for n in r) for r in recorded_ranges)
                        or recorded_ranges != changed_ranges
                        or (not prior_unit and [start, end] != [min(r[0] for r in changed_ranges), max(r[1] for r in changed_ranges)])
                        or (prior_unit and not all(start <= a <= b <= end for a, b in changed_ranges))):
                    raise ValueError(f"{finding_id}: qualification changed ranges mismatch")
                before = data
                for patch in reversed(patches):
                    after_bytes, before_bytes = patch["after"].encode("utf-8"), patch["before"].encode("utf-8")
                    if before.count(after_bytes) != 1:
                        raise ValueError(f"{finding_id}: non-unique qualification inverse replacement")
                    before = before.replace(after_bytes, before_bytes, 1)
                before_digest = sha256_bytes(before)
                if (before_digest != str(declaration.get("before_sha256", "")).upper()
                        or type(declaration.get("before_bytes")) is not int
                        or len(before) != declaration["before_bytes"]):
                    raise ValueError(f"{finding_id}: qualification inverse/before hash mismatch")
                if prior_unit:
                    if (before_digest != prior_unit["msa"]["sha256"].upper()
                            or len(before) != prior_unit["msa"]["bytes"]):
                        raise ValueError(f"{finding_id}: MSA qualification immutable prior-manifest before identity mismatch")
                elif (before_digest != str(baseline.get("arabic_sha256", "")).upper()
                      or type(baseline.get("arabic_bytes")) is not int
                      or len(before) != baseline["arabic_bytes"]):
                    raise ValueError(f"{finding_id}: MSA qualification baseline before hash/bytes mismatch")
                # Also prove that each forward patch was unambiguous when applied;
                # a forged inverse alone must not certify an ambiguous edit.
                replay = before
                for patch in patches:
                    old, new = patch["before"].encode("utf-8"), patch["after"].encode("utf-8")
                    if replay.count(old) != 1:
                        raise ValueError(f"{finding_id}: non-unique qualification forward replacement")
                    replay = replay.replace(old, new, 1)
                if replay != data:
                    raise ValueError(f"{finding_id}: qualification patch replay mismatch")
                old_visible = normalized_excerpt(strip_tex_comments(before.decode("utf-8-sig"))).casefold()
                if normalized_excerpt(row["before_arabic"]).casefold() not in old_visible:
                    raise ValueError(f"{finding_id}: before source lacks the recorded qualification wording")
                before_witness = {
                    "path": expected_path, "sha256": before_digest, "bytes": len(before),
                    "text_utf8": before.decode("utf-8"),
                    "patches": copy.deepcopy(patches),
                    "status": "historical-before-bytes-proved-by-exact-inverse-not-current-source",
                }
                if prior_unit:
                    before_witness["identity_basis"] = {
                        "kind": "immutable-pre-qualification-source-manifest",
                        "manifest": copy.deepcopy(prior_identity),
                        "unit": copy.deepcopy(prior_unit),
                    }
                    before_lines = before.decode("utf-8-sig").splitlines()
                    old_start, old_end = declaration.get("before_line_start"), declaration.get("before_line_end")
                    if (type(old_start) is not int or type(old_end) is not int
                            or not 1 <= old_start <= old_end <= len(before_lines)):
                        raise ValueError(f"{finding_id}: invalid qualification before excerpt range")
                    old_excerpt = "\n".join(before_lines[old_start - 1:old_end])
                    if (declaration.get("before_excerpt") != old_excerpt
                            or str(declaration.get("before_excerpt_sha256", "")).upper() != sha256_bytes(old_excerpt.encode("utf-8"))
                            or not qualification_active_phrase_ranges(old_excerpt, row["before_arabic"], "msa", old_start)):
                        raise ValueError(f"{finding_id}: qualification before excerpt/phrase mismatch")
                    before_witness.update(line_start=old_start, line_end=old_end, excerpt=old_excerpt)
        normalized.append({
            "decision_id": f"semantic-propagation-20260906:{finding_id}",
            "recorded_decision_id": finding_id,
            "edition": "Shared MSA (International and Machrek); Classical qualification already explicit",
            "english_term": row["source_term"], "sense": row["sense"],
            "before_arabic": row["before_arabic"], "chosen_arabic": row["chosen_arabic"],
            "classical_arabic": row["classical_arabic"], "assessed_on": payload["assessed_on"],
            "rationale": (
                "New independent assessment dated 2026-09-06; not a reconstruction of "
                "the original translator's deliberation. " + scope_description + "Previous MSA wording: "
                + row["before_arabic"] + ". " + row["rationale"]
            ),
            "alternatives": [{**copy.deepcopy(alt), "status": alt["disposition"]} for alt in alternatives],
            "basis": ("authoritative-dated-inherited-source-qualification-repair" if inherited
                      else "authoritative-dated-translation-scope-clarification-repair"),
            "confidence": {"level": "medium", "reason": (
                "Current English/MSA/Classical source identities, literal excerpts and exact "
                "reversible source patches are checked. The mathematical clarification and "
                "its Arabic expression remain open to expert correction; no official attestation is claimed."
            )},
            "expert_review_useful": True, "expert_review_reason": row["sense"],
            "expert_question": expert["question"], "open_to_correction": True,
            "official_attestation_claimed": False, "expert_review_non_blocking": True,
            "recording_mode": payload["recording_mode"], "status": payload["status"],
            "occurrences": [occurrence], "printed_page": None,
            "page_status": "bind-after-final-reader-build",
            "semantic_propagation_repair": {
                "ledger_path": logical, "ledger_sha256": identity["sha256"],
                "finding_id": finding_id, "assessed_on": payload["assessed_on"],
                "classification": classification,
                "inherited_source_qualification": inherited,
                "translation_scope_clarification": not inherited,
                "historical_before_source": before_witness,
                "source_ledger": copy.deepcopy(payload),
                "current_witness_companions": current_witness_companions,
            },
            "source_record": identity,
        })
        normalized.extend(normalize_qualification_additional_choice(
            row, normalized[-1], repo, english_root, hashes, scope_description
        ))
    identity["adapter"] = {
        "kind": ("dated-semantic-qualification-repair-v1" if prior_units
                 else "dated-inherited-source-qualification-repair-v1"), "schema": schema,
        "terminology_rows_contributed": len(normalized),
        "decision_ids": sorted(row["decision_id"] for row in normalized),
        "historical_deliberation_claimed": False,
    }
    if prior_identity:
        identity["adapter"]["prior_source_manifest"] = copy.deepcopy(prior_identity)
    return normalized, hashes


def apply_authoritative_repair_precedence(decisions: list[dict]) -> None:
    """Fold superseded decision occurrences into the current repair entry."""

    by_recorded_id: dict[str, list[dict]] = defaultdict(list)
    for decision in decisions:
        by_recorded_id[
            str(decision.get("recorded_decision_id") or decision["decision_id"])
        ].append(decision)
    for repair in [row for row in decisions if row.get("authoritative_precedence_over_decision_ids")]:
        merged_occurrences = list(repair.get("occurrences") or [])
        merged_keys = {
            json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            for row in merged_occurrences
        }
        folded_ids = []
        for old_id in repair["authoritative_precedence_over_decision_ids"]:
            for old in by_recorded_id.get(old_id, []):
                if old.get("semantic_propagation_repair"):
                    raise ValueError("A new dated propagation assessment cannot be silently superseded")
                for occurrence in old.get("occurrences") or []:
                    key = json.dumps(
                        occurrence,
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    )
                    if key not in merged_keys:
                        merged_keys.add(key)
                        merged_occurrences.append(copy.deepcopy(occurrence))
                old["human_superseded_by_authoritative_repair"] = repair["decision_id"]
                folded_ids.append(old["decision_id"])
        repair["occurrences"] = sorted(
            merged_occurrences,
            key=lambda row: (
                collapse(row.get("unit_id")),
                json.dumps(row, ensure_ascii=False, sort_keys=True),
            ),
        )
        repair["folded_source_decision_ids"] = sorted(set(folded_ids))


def raw_exact_occurrence_keys(decision: dict) -> set[tuple[str, str, str, int, int]]:
    keys = set()
    for occurrence in decision.get("occurrences") or []:
        if not isinstance(occurrence, dict):
            continue
        unit_id = collapse(occurrence.get("unit_id"))
        for location in normalize_occurrence_sources(occurrence):
            start = location.get("line_start")
            end = location.get("line_end")
            path = collapse(location.get("path")).replace("\\", "/").casefold()
            if unit_id and path and isinstance(start, int) and isinstance(end, int):
                keys.add((unit_id, location["source_kind"], path, start, end))
    return keys


def decision_evidence_richness(decision: dict) -> tuple[int, int, int, str]:
    authoritative = int(
        "authoritative" in collapse(decision.get("basis")).casefold()
        or collapse(decision.get("recording_mode")).casefold().startswith("authoritative")
        or decision.get("authoritative_precedence_over_decision_ids") is not None
    )
    exact_count = len(raw_exact_occurrence_keys(decision))
    evidence_chars = sum(
        len(collapse(decision.get(field)))
        for field in (
            "sense", "rationale", "expert_question", "expert_review_reason",
            "grammatical_realization",
        )
    ) + len(json.dumps(decision.get("authority_checks") or [], ensure_ascii=False))
    return authoritative, exact_count, evidence_chars, decision["decision_id"]


def merge_exact_semantic_duplicates(decisions: Sequence[dict]) -> tuple[list[dict], int]:
    """Merge only term+sense records sharing an identical exact occurrence."""

    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    untouched: list[dict] = []
    for decision in decisions:
        if decision.get("semantic_propagation_repair"):
            # New repair chronology is itself reviewable evidence, even if an
            # older record names the same term/sense at the same exact line.
            untouched.append(decision)
            continue
        keys = raw_exact_occurrence_keys(decision)
        if not keys:
            untouched.append(decision)
            continue
        semantic = (
            normalized_review_headword(decision.get("english_term")),
            normalized_review_headword(decision.get("sense")),
        )
        groups[semantic].append(decision)

    merged_rows = list(untouched)
    merged_count = 0
    for rows in groups.values():
        components: list[list[dict]] = []
        for decision in sorted(rows, key=lambda row: row["decision_id"]):
            decision_keys = raw_exact_occurrence_keys(decision)
            touching = [
                component for component in components
                if any(
                    decision_keys & raw_exact_occurrence_keys(other)
                    for other in component
                )
            ]
            if not touching:
                components.append([decision])
                continue
            primary = touching[0]
            primary.append(decision)
            for extra in touching[1:]:
                primary.extend(extra)
                components.remove(extra)
        for component in components:
            if len(component) == 1:
                merged_rows.append(component[0])
                continue
            winner = copy.deepcopy(max(component, key=decision_evidence_richness))
            losers = [row for row in component if row["decision_id"] != winner["decision_id"]]
            merged_count += len(losers)
            occurrence_map = {}
            for row in component:
                for occurrence in row.get("occurrences") or []:
                    key = json.dumps(
                        occurrence, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                    )
                    occurrence_map[key] = copy.deepcopy(occurrence)
            winner["occurrences"] = [occurrence_map[key] for key in sorted(occurrence_map)]
            source_records = []
            for row in component:
                for source in row.get("source_records") or [row.get("source_record")]:
                    if source and source not in source_records:
                        source_records.append(copy.deepcopy(source))
            winner["source_records"] = sorted(source_records, key=lambda row: row["path"])
            winner["source_record"] = winner["source_records"][0]
            alternatives = list(winner.get("alternatives") or [])
            for loser in losers:
                form = collapse(loser.get("chosen_arabic"))
                if form and form != collapse(winner.get("chosen_arabic")):
                    alternatives.append(
                        {
                            "form": form,
                            "status": "recorded form from exact-occurrence duplicate",
                            "source_decision_id": loser["decision_id"],
                        }
                    )
            winner["alternatives"] = alternatives
            winner["deduplicated_source_decisions"] = [
                copy.deepcopy(row) for row in sorted(losers, key=lambda row: row["decision_id"])
            ]
            winner["deduplicated_source_decision_ids"] = [
                row["decision_id"] for row in winner["deduplicated_source_decisions"]
            ]
            winner["deduplication_rule"] = (
                "Same normalized English term and sense plus at least one identical "
                "unit/language/path/exact-line occurrence; richest authoritative evidence "
                "selected, all provenance and other forms retained."
            )
            merged_rows.append(winner)
    return sorted(
        merged_rows,
        key=lambda row: (collapse(row.get("english_term")).casefold(), row["decision_id"]),
    ), merged_count


def dated_repair_require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError("dated applied repair: " + message)


def dated_repair_no_page_claims(value: object) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"printed_page", "printed_pages", "assembled_pdf_page", "assembled_pdf_pages", "pdf_pages", "page_evidence"}:
                dated_repair_require(not item, "unverified final page claim")
            if key in {"rebuilt_pdf_verified", "published_pdf_verified", "final_reader_verified", "publication_or_reader_completion_claimed"}:
                dated_repair_require(item is False, "unverified reader/publication claim")
            dated_repair_no_page_claims(item)
    elif isinstance(value, list):
        for item in value:
            dated_repair_no_page_claims(item)


def dated_repair_identity(data: bytes, declaration: dict, path: str) -> None:
    dated_repair_require(isinstance(declaration, dict) and declaration.get("path") == path,
                         "source identity path mismatch")
    dated_repair_require(str(declaration.get("sha256", "")).upper() == sha256_bytes(data)
                         and type(declaration.get("bytes")) is int
                         and declaration["bytes"] == len(data), "source identity hash/bytes mismatch")


def dated_repair_source(repo: Path, declaration: dict, hashes: dict[Path, str]) -> bytes:
    logical = declaration.get("path", "")
    path = (repo / logical).resolve()
    dated_repair_require(path_is_within(path, repo.resolve()) and path.is_file(),
                         "source missing or outside declared root")
    data = path.read_bytes()
    dated_repair_identity(data, declaration, logical)
    digest = sha256_bytes(data)
    dated_repair_require(path not in hashes or hashes[path] == digest, "source changed during admission")
    hashes[path] = digest
    return data


def next_batch_version_source(repo: Path, declaration: dict, hashes: dict[Path, str]) -> bytes:
    """Recover a named historical stage with a pinned, replayed transition."""
    transition = NEXT_BATCH_HISTORY.get((declaration["path"], str(declaration["sha256"]).upper()))
    if transition is None:
        return dated_repair_source(repo, declaration, hashes)
    ledger_path = repo / transition
    raw = ledger_path.read_bytes()
    dated_repair_require(sha256_bytes(raw) == NEXT_BATCH_LEDGERS[transition][0], "history transition identity mismatch")
    hashes[ledger_path.resolve()] = sha256_bytes(raw)
    ledger = json.loads(raw)
    matches = [t for t in ledger["transactions"] if t["path"] == declaration["path"]]
    dated_repair_require(len(matches) == 1, "history transition path inventory mismatch")
    transaction = matches[0]
    dated_repair_require(str(transaction["before_sha256"]).upper() == str(declaration["sha256"]).upper()
                         and transaction["before_bytes"] == declaration["bytes"], "history predecessor identity mismatch")
    after = dated_repair_source(repo, {"path": transaction["path"], "sha256": transaction["after_sha256"],
        "bytes": transaction["after_bytes"]}, hashes)
    history = dated_repair_inverse(after, transaction["patches"], declaration)
    return history["text_utf8"].encode("utf-8")


def next_batch_literal(uid, kind, data, logical, literal, start, end):
    """Check the supplied context, then narrow to its actual active phrase."""
    lines = data.decode("utf-8-sig").splitlines()
    dated_repair_require(type(start) is int and type(end) is int and 1 <= start <= end <= len(lines),
                         "next batch literal context range mismatch")
    context = "\n".join(lines[start - 1:end])
    literal = strip_tex_comments(literal).strip()
    ranges = qualification_active_phrase_ranges(context, literal, kind, start)
    dated_repair_require(len(ranges) == 1, "next batch selected phrase missing or ambiguous")
    first, last = ranges[0]
    excerpt = "\n".join(lines[first - 1:last])
    witness = {"path": logical, "sha256": sha256_bytes(data), "bytes": len(data),
        "line_start": first, "line_end": last, "excerpt": excerpt,
        "excerpt_sha256": sha256_bytes(excerpt.encode("utf-8")), "literal": literal}
    return dated_repair_occurrence(uid, kind, data, witness, literal), witness


def next_batch_live_literal(repo, uid, kind, data, witness, hashes):
    """Historical assessed-after passage stays stored; the clickable one is live."""
    logical = witness["path"]
    if (logical, sha256_bytes(data)) not in NEXT_BATCH_HISTORY:
        return next_batch_literal(uid, kind, data, logical, witness["literal"], witness["line_start"], witness["line_end"])
    # Prove the complete historical-to-current edge before relocating any text.
    dated_repair_require(next_batch_version_source(repo, witness, hashes) == data, "history revalidation differs")
    live = (repo / logical).read_bytes()
    dated_repair_require(hashes[(repo / logical).resolve()] == sha256_bytes(live), "live source changed during projection")
    return next_batch_literal(uid, kind, live, logical, witness["literal"], 1, len(live.decode("utf-8-sig").splitlines()))


def dated_repair_excerpt(data: bytes, declaration: dict, path: str) -> tuple[str, int, int]:
    dated_repair_identity(data, declaration, path)
    lines = data.decode("utf-8-sig").splitlines()
    start, end = declaration.get("line_start"), declaration.get("line_end")
    dated_repair_require(type(start) is int and type(end) is int and 1 <= start <= end <= len(lines),
                         "invalid exact excerpt line range")
    excerpt = "\n".join(lines[start - 1:end])
    dated_repair_require(excerpt == declaration.get("excerpt")
                         and sha256_bytes(excerpt.encode("utf-8")) == str(declaration.get("excerpt_sha256", "")).upper(),
                         "exact excerpt/hash mismatch")
    return excerpt, start, end


def dated_repair_occurrence(unit: str, kind: str, data: bytes, declaration: dict, term: str) -> dict:
    excerpt, start, _ = dated_repair_excerpt(data, declaration, declaration["path"])
    ranges = qualification_active_phrase_ranges(excerpt, term, kind, start)
    dated_repair_require(bool(ranges), "active literal phrase absent from canonical witness")
    group = structured_occurrence(unit, kind, declaration["path"], sha256_bytes(data), ranges,
                                  "dated-applied-repair-live-hash-excerpt-and-term-verified")[kind]
    lines = data.decode("utf-8-sig").splitlines()
    for loc in group["locators"]:
        loc["excerpt"] = "\n".join(lines[loc["line_start"] - 1:loc["line_end"]])
    return group


def dated_repair_inverse(after: bytes, patches: list[dict], before_identity: dict) -> dict:
    dated_repair_require(isinstance(patches, list) and bool(patches), "missing reversible patches")
    before = after
    for patch in reversed(patches):
        dated_repair_require(isinstance(patch, dict) and all(isinstance(patch.get(k), str) and patch[k]
                             for k in ("before", "after")) and patch["before"] != patch["after"],
                             "invalid reversible patch")
        old, new = patch["before"].encode("utf-8"), patch["after"].encode("utf-8")
        for key, value in (("before_sha256", old), ("after_sha256", new)):
            if key in patch:
                dated_repair_require(str(patch[key]).upper() == sha256_bytes(value), "patch hash mismatch")
        dated_repair_require(before.count(new) == 1, "non-unique inverse patch")
        before = before.replace(new, old, 1)
    dated_repair_identity(before, before_identity, before_identity["path"])
    replay = before
    for patch in patches:
        old, new = patch["before"].encode("utf-8"), patch["after"].encode("utf-8")
        dated_repair_require(replay.count(old) == 1, "non-unique forward patch")
        replay = replay.replace(old, new, 1)
    dated_repair_require(replay == after, "forward replay mismatch")
    return {"path": before_identity["path"], "sha256": sha256_bytes(before), "bytes": len(before),
            "text_utf8": before.decode("utf-8"), "patches": copy.deepcopy(patches),
            "status": "historical-before-bytes-proved-by-exact-inverse-not-current-source"}


def dated_repair_prior(repo: Path, hashes: dict[Path, str]) -> dict[str, dict]:
    path = (repo / QUALIFICATION_PRIOR_MANIFEST_RELATIVE).resolve()
    dated_repair_require(path.is_file() and path.stat().st_size <= 2 * 1024 * 1024,
                         "missing/oversized pinned predecessor manifest")
    data = path.read_bytes()
    dated_repair_require(sha256_bytes(data) == QUALIFICATION_PRIOR_MANIFEST_SHA256,
                         "pinned predecessor manifest hash mismatch")
    hashes[path] = sha256_bytes(data)
    manifest = json.loads(data.decode("utf-8-sig"))
    units = manifest.get("units", [])
    dated_repair_require(manifest.get("schema") == "openlogic-classical-source-closure-manifest-v1"
                         and [u.get("id") for u in units] == [f"OLP-{i:04d}" for i in range(1, 723)],
                         "pinned predecessor inventory mismatch")
    return {u["id"]: u for u in units}


def dated_repair_record(row: dict, payload: dict, identity: dict, occurrence: dict | list,
                        history: dict, changed_edition: str, finding_id: str,
                        before_arabic: str | None = None) -> dict:
    expert = row.get("expert_review", {})
    question = row.get("expert_question", row.get("expert_review_question", expert.get("question")))
    dated_repair_require(isinstance(question, str) and bool(question.strip()), "missing expert question")
    dated_repair_require(row.get("open_to_correction", expert.get("open_to_correction")) is True
                         and row.get("expert_review_useful", expert.get("useful")) is True,
                         "missing provisional/expert-review provenance")
    for key in ("rationale", "sense", "chosen_arabic"):
        dated_repair_require(isinstance(row.get(key), str) and bool(row[key].strip()), "missing " + key)
    record = copy.deepcopy(row)
    record.update(
        decision_id="semantic-propagation-20260906:" + row["decision_id"],
        recorded_decision_id=row["decision_id"],
        english_term=row.get("english_term", row.get("source_term")),
        occurrences=occurrence if isinstance(occurrence, list) else [occurrence], source_record=identity,
        before_arabic=before_arabic if before_arabic is not None else row["before_arabic"],
        assessed_on=payload["assessed_on"], expert_question=question,
        expert_review_useful=True, expert_review_non_blocking=True, open_to_correction=True,
        official_attestation_claimed=False, printed_page=None, page_status="bind-after-final-reader-build",
        semantic_propagation_repair={
            "ledger_path": identity["path"], "ledger_sha256": identity["sha256"],
            "assessed_on": payload["assessed_on"], "finding_id": finding_id,
            "changed_edition": changed_edition, "historical_before_source": history,
            "source_ledger": copy.deepcopy(payload), "choice_record": copy.deepcopy(row),
        },
    )
    return record


def dated_repair_byte_occurrence(unit: str, kind: str, data: bytes, loc: dict) -> dict:
    """Certify a byte-exact selected phrase; never treat its heading as literal."""
    dated_repair_require(str(loc.get("sha256", "")).upper() == sha256_bytes(data), "byte witness source hash mismatch")
    start, end = loc.get("byte_start"), loc.get("byte_end")
    dated_repair_require(type(start) is int and type(end) is int and 0 <= start < end <= len(data),
                         "byte witness range mismatch")
    excerpt = loc["excerpt"].encode("utf-8")
    dated_repair_require(data[start:end] == excerpt and data.count(excerpt) == 1
                         and sha256_bytes(excerpt) == str(loc["excerpt_sha256"]).upper(), "byte witness exact excerpt mismatch")
    first, last = data[:start].count(b"\n") + 1, data[:end - 1].count(b"\n") + 1
    dated_repair_require((first, last) == (loc["line_start"], loc["line_end"]), "byte witness line mapping mismatch")
    dated_repair_require(bool(strip_tex_comments(loc["excerpt"]).strip()), "comment-only byte witness")
    # Reviewer links use complete exact lines; byte selection and full original
    # phrase remain preserved in the immutable canonical choice_record.
    group = structured_occurrence(unit, kind, loc["path"], sha256_bytes(data), [(first, last)],
                                  "dated-applied-repair-exact-byte-phrase-verified")[kind]
    group["locators"][0]["excerpt"] = "\n".join(data.decode("utf-8-sig").splitlines()[first - 1:last])
    return group


def normalize_applied_classical_repairs(payload: dict, identity: dict, repo: Path,
                                       baseline: dict[str, dict], english_root: Path | None
                                       ) -> tuple[list[dict], dict[Path, str]]:
    if identity["path"] != APPLIED_CLASSICAL_LEDGER:
        return [], {}
    dated_repair_require(identity["sha256"] == APPLIED_CLASSICAL_SHA256, "unapproved Classical prose ledger identity")
    dated_repair_require(english_root is not None and payload.get("schema") == "openlogic-classical-prose-repairs-v1"
                         and payload.get("assessed_on") == "2026-09-06"
                         and payload.get("status") == "implemented-in-classical-source"
                         and payload.get("unit_id") == "OLP-0008", "Classical prose schema/provenance mismatch")
    rows = payload["decisions"]
    dated_repair_require([r["decision_id"] for r in rows] == ["AR-OLP-0008-CLASSICAL-" + c for c in ("C005", "C009", "C014", "C016")],
                         "Classical prose choice inventory mismatch")
    hashes, result = {}, []
    source = payload["source"]
    expected = baseline["OLP-0008"]
    dated_repair_require(source["path"] == expected["target_path"] and payload["english"]["path"] == expected["source_path"]
                         and payload["msa_unchanged"]["path"] == expected["arabic_path"], "Classical prose baseline path mismatch")
    after_identity = {"path": source["path"], "sha256": source["after_sha256"], "bytes": source["after_bytes"]}
    before_identity = {"path": source["path"], "sha256": source["before_sha256"], "bytes": source["before_bytes"]}
    after = dated_repair_source(repo, after_identity, hashes)
    english = dated_repair_source(english_root, payload["english"], hashes)
    dated_repair_require(sha256_bytes(english) == expected["english_sha256"].upper(), "Classical prose frozen English mismatch")
    dated_repair_source(repo, payload["msa_unchanged"], hashes)
    patches = [p for r in rows for p in r["patches"]]
    dated_repair_require(len(patches) == 5, "Classical prose patch inventory mismatch")
    history = dated_repair_inverse(after, patches, before_identity)
    prior = dated_repair_source(repo, source["prior_snapshot"], hashes)
    dated_repair_require(prior == history["text_utf8"].encode("utf-8"), "Classical prose preserved predecessor mismatch")
    for field in ("historical_proposal", "historical_proposal_markdown"):
        dated_repair_source(repo, payload[field], hashes)
    for row in rows:
        occurrences = []
        dated_repair_require(len(row["occurrences"]) == len(row["patches"]), "Classical prose patch/occurrence mismatch")
        for occ, patch in zip(row["occurrences"], row["patches"]):
            dated_repair_require(occ["english"]["path"] == expected["source_path"]
                                 and occ["classical_after"]["path"] == source["path"]
                                 and occ["classical_before"]["path"] == source["prior_snapshot"]["path"]
                                 and occ["classical_before"]["excerpt"] == patch["before"]
                                 and occ["classical_after"]["excerpt"] == patch["after"], "Classical prose occurrence/patch path mismatch")
            dated_repair_byte_occurrence("OLP-0008", "classical", prior, occ["classical_before"])
            occurrences.append({"unit_id": "OLP-0008", "context_note": occ["subchoice"],
                "rationale": occ["rationale"], "expert_question": occ["expert_review_question"],
                "alternatives": copy.deepcopy(occ["alternatives"]),
                "english": dated_repair_byte_occurrence("OLP-0008", "english", english, occ["english"]),
                "classical": dated_repair_byte_occurrence("OLP-0008", "classical", after, occ["classical_after"])})
        record = dated_repair_record(row, payload, identity, occurrences, copy.deepcopy(history), "classical", row["decision_id"],
                                    "\n\n".join(p["before"] for p in row["patches"]))
        record["alternatives"] = [copy.deepcopy(a) for o in row["occurrences"] for a in o["alternatives"]]
        result.append(record)
    identity["adapter"] = {"kind": "dated-applied-classical-prose-repair-v1", "terminology_rows_contributed": len(result)}
    return result, hashes


def refreshed_classical_qualification(repo: Path, english_root: Path, baseline: dict[str, dict],
                                     identity: dict, row: dict, hashes: dict[Path, str]) -> tuple[dict, dict]:
    """Apply only the proved unchanged 0008 passage after five unrelated edits."""
    path = repo / APPLIED_CLASSICAL_REFRESH
    raw = path.read_bytes()
    dated_repair_require(sha256_bytes(raw) == APPLIED_CLASSICAL_REFRESH_SHA256, "unapproved qualification refresh identity")
    companion = json.loads(raw.decode("utf-8-sig"))
    hashes[path.resolve()] = sha256_bytes(raw)
    applied_path = repo / APPLIED_CLASSICAL_LEDGER
    applied_raw = applied_path.read_bytes()
    applied_identity = {"path": APPLIED_CLASSICAL_LEDGER, "sha256": sha256_bytes(applied_raw), "bytes": len(applied_raw)}
    applied = json.loads(applied_raw.decode("utf-8-sig"))
    repairs, inputs = normalize_applied_classical_repairs(applied, applied_identity, repo, baseline, english_root)
    hashes[applied_path.resolve()] = applied_identity["sha256"]
    hashes.update(inputs)
    declaration = companion["qualification_witness"]
    dated_repair_require(companion["schema"] == "openlogic-classical-witness-refresh-v1"
                         and companion["source_transition"] == applied["source"]
                         and all(declaration["historical_ledger"][k] == identity[k] for k in ("path", "bytes"))
                         and declaration["historical_ledger"]["sha256"].upper() == identity["sha256"].upper()
                         and declaration["finding_id"] == row["finding_id"]
                         and declaration["historical_declaration"] == row["locations"]["classical"]
                         and declaration["historical_rationale"] == row["rationale"]
                         and declaration["historical_expert_review"] == row["expert_review"], "qualification refresh historical provenance mismatch")
    old = declaration["historical_declaration"]
    new = declaration["current_declaration"]
    before = repairs[0]["semantic_propagation_repair"]["historical_before_source"]["text_utf8"].encode("utf-8")
    after = dated_repair_source(repo, new, hashes)
    dated_repair_require(dated_repair_excerpt(before, old, old["path"])
                         == dated_repair_excerpt(after, new, old["path"]), "qualification refresh changed selected passage")
    return copy.deepcopy(new), {"path": APPLIED_CLASSICAL_REFRESH, "sha256": sha256_bytes(raw),
                                "bytes": len(raw), "source_ledger": companion}


def normalize_applied_repairs(payload: dict, identity: dict, repo: Path,
                              baseline: dict[str, dict], english_root: Path | None
                              ) -> tuple[list[dict], dict[Path, str]]:
    if identity["path"] not in APPLIED_REPAIR_LEDGERS and (
        payload.get("schema") in {"openlogic-classical-prose-repairs-v1", "openlogic-olp0067-dual-grammar-repairs-v1"}
        or payload.get("schema") in {contract[1] for contract in NEXT_BATCH_LEDGERS.values()}
        or any(isinstance(r, dict) and r.get("decision_id") in APPLIED_SCOPE_IDS.values() for r in payload.get("units", []))
    ):
        raise ValueError("unexpected applied repair ledger path: " + identity["path"])
    if identity["path"] in APPLIED_REPAIR_LEDGERS:
        dated_repair_no_page_claims(payload)
    if identity["path"] in NEXT_BATCH_LEDGERS:
        return normalize_next_batch_repairs(payload, identity, repo, baseline, english_root)
    if identity["path"] in CONSOLIDATED_REPAIR_LEDGERS:
        return normalize_consolidated_repairs(payload, identity, repo, baseline, english_root)
    if identity["path"] == APPLIED_CLASSICAL_LEDGER:
        return normalize_applied_classical_repairs(payload, identity, repo, baseline, english_root)
    if identity["path"] == APPLIED_DUAL_LEDGER:
        return normalize_applied_dual_repairs(payload, identity, repo, baseline, english_root)
    return normalize_applied_scope_repairs(payload, identity, repo, baseline, english_root)


def normalize_consolidated_repairs(payload: dict, identity: dict, repo: Path,
                                   baseline: dict[str, dict], english_root: Path | None
                                   ) -> tuple[list[dict], dict[Path, str]]:
    """Admit only the three pinned September 7 repair ledgers, without exporting."""
    contract = CONSOLIDATED_REPAIR_LEDGERS.get(identity["path"])
    if contract is None:
        return [], {}
    hashes, result = {}, []
    dated_repair_require(identity["sha256"].upper() == contract[0], "unapproved consolidated ledger identity")
    raw = dated_repair_source(repo, identity, hashes)
    dated_repair_require(json.loads(raw.decode("utf-8-sig")) == payload, "consolidated payload differs from pinned bytes")
    dated_repair_require(english_root is not None and payload["schema"] == contract[1]
                         and payload["assessed_on"] == "2026-09-07" and payload["open_to_correction"] is True,
                         "consolidated schema/date/provisional mismatch")
    dated_repair_no_page_claims(payload)
    arithmetic = payload["schema"] == "openlogic-arithmetic-scope-repairs-v1"
    semantic = payload["schema"] == "openlogic-semantic-scope-repairs-v1"
    multiple = arithmetic or semantic
    choices = payload["decisions"] if multiple else [payload]
    expected_ids = (["AR-OLP-0375-ZERO-EXPONENT-20260907", "AR-OLP-0375-PAIR-METHOD-20260907",
                     "AR-OLP-0376-TRUNCATED-SUBTRACTION-20260907"] if arithmetic else
                    ["AR-OLP-0321-FUNCTION-RELATION-20260907", "AR-OLP-0326-COMPLEMENT-FIRST-ORDER-20260907",
                     "AR-OLP-0326-COMPLEMENT-SECOND-ORDER-20260907",
                     "AR-OLP-0368-CONDITIONAL-NORMAL-FORM-UNIQUENESS-20260907"] if semantic else
                    ["AR-OLP-0021-TWO-ROOTS-NOTE-20260907"])
    dated_repair_require([r["decision_id"] for r in choices] == expected_ids, "consolidated choice inventory mismatch")
    transactions = payload["transactions"] if multiple else [dict(payload["source"],
        unit_id="OLP-0021", edition="msa", patches=[payload["patch"]])]
    dated_repair_require(len(transactions) == (4 if multiple else 1), "consolidated transaction inventory mismatch")
    sources, histories = {}, {}
    for transaction in transactions:
        uid, kind, path = transaction["unit_id"], transaction["edition"], transaction["path"]
        dated_repair_require(kind in {"msa", "classical"} and (uid, kind) not in sources,
                             "unexpected or duplicate transaction register")
        dated_repair_require(path == baseline[uid]["arabic_path" if kind == "msa" else "target_path"],
                             "consolidated source baseline path mismatch")
        after_id = {"path": path, "sha256": transaction["after_sha256"], "bytes": transaction["after_bytes"]}
        before_id = {"path": path, "sha256": transaction["before_sha256"], "bytes": transaction["before_bytes"]}
        data = dated_repair_source(repo, after_id, hashes)
        history = dated_repair_inverse(data, transaction["patches"], before_id)
        dated_repair_require(all(p.get("occurrences") == 1 for p in transaction["patches"]), "consolidated patch count mismatch")
        sources[(uid, kind)] = (data, after_id, transaction)
        histories[(uid, kind)] = history
    english_declarations = payload["english_sources"] if multiple else [
        dict(next(s for s in payload["unchanged_sources"] if s["kind"] == "english"), unit_id="OLP-0021")]
    for declared in english_declarations:
        uid = declared["unit_id"]
        logical = baseline[uid]["source_path"]
        dated_repair_require(declared["path"] == logical or declared["path"].endswith("/" + logical),
                             "consolidated English logical path mismatch")
        declaration = dict(declared, path=logical)
        data = dated_repair_source(english_root, declaration, hashes)
        dated_repair_require(sha256_bytes(data) == baseline[uid]["english_sha256"].upper(), "consolidated frozen English mismatch")
        sources[(uid, "english")] = (data, declaration, None)
    if arithmetic:
        supporting = payload["supporting_definition"]
        data = dated_repair_source(repo, supporting, hashes)
        actual = "\n".join(data.decode("utf-8-sig").splitlines()[supporting["line_start"]-1:supporting["line_end"]])
        dated_repair_require(actual == supporting["excerpt"], "consolidated supporting definition mismatch")
    elif semantic:
        for declaration in payload["preserved_arabic_sources"]:
            uid = declaration["unit_id"]
            dated_repair_require(declaration["path"] == baseline[uid]["target_path"] and
                                 (uid, "classical") not in sources, "preserved Classical baseline mismatch")
            sources[(uid, "classical")] = (dated_repair_source(repo, declaration, hashes), declaration, None)
        witnesses = [w for c in choices for w in c["source_witnesses"]]
        dated_repair_require(len(witnesses) == 20, "semantic primary witness inventory mismatch")
        for witness in witnesses:
            uid, kind = witness["unit_id"], witness["edition"]
            data = sources[(uid, kind)][0]
            if witness["phase"] == "before":
                data = histories[(uid, kind)]["text_utf8"].encode("utf-8")
            else:
                dated_repair_require(witness["phase"] == "after", "unknown semantic witness phase")
            declared = dict(witness, excerpt_sha256=sha256_bytes(witness["excerpt"].encode("utf-8")))
            dated_repair_excerpt(data, declared, sources[(uid, kind)][1]["path"])
    else:
        declaration = next(s for s in payload["unchanged_sources"] if s["kind"] == "classical")
        dated_repair_require(declaration["path"] == baseline["OLP-0021"]["target_path"], "unchanged Classical baseline mismatch")
        sources[("OLP-0021", "classical")] = (next_batch_version_source(repo, declaration, hashes), declaration, None)

    def selected(uid, kind, loc, *, before=False):
        data, declaration, transaction = sources[(uid, kind)]
        if before:
            history = histories[(uid, kind)]
            data = history["text_utf8"].encode("utf-8")
            declaration = {k: history[k] for k in ("path", "sha256", "bytes")}
        start, end = loc["line_start"], loc["line_end"]
        text = "\n".join(data.decode("utf-8-sig").splitlines()[start-1:end])
        witness = dict(declaration, sha256=sha256_bytes(data), line_start=start, line_end=end, excerpt=text,
                       excerpt_sha256=sha256_bytes(text.encode("utf-8")))
        group = dated_repair_occurrence(uid, kind, data, witness, loc["literal"])
        dated_repair_require([(l["line_start"], l["line_end"]) for l in group["locators"]] == [(start, end)],
                             "consolidated literal is not exact declared range")
        public = {k: witness[k] for k in ("path", "sha256", "bytes", "line_start", "line_end", "excerpt", "excerpt_sha256")} | {"literal": loc["literal"]}
        if not before and (declaration["path"], sha256_bytes(data)) in NEXT_BATCH_HISTORY:
            group, live = next_batch_live_literal(repo, uid, kind, data, public, hashes)
            live["assessed_source_phase"] = "unchanged-at-earlier-assessment-now-historical"
            live["assessed_source_witness"] = public
            public = live
        return group, public

    for choice in choices:
        uid = choice["unit_id"]
        occurrences, passages = [], []
        for number, item in enumerate(choice["literal_review_occurrences"], 1):
            kind, patch_index = item["edition"], item["patch_index"]
            transaction = sources[(uid, kind)][2]
            patch = transaction["patches"][patch_index]
            if multiple:
                binding = next(b for b in choice["occurrence_bindings"] if b["edition"] == kind)
                dated_repair_require(binding["path"] == transaction["path"] and
                    binding["sha256"] == transaction["after_sha256"] and patch_index in binding["patch_indices"],
                    "consolidated literal/transaction binding mismatch")
            for phase in ("before", "after"):
                dated_repair_require(collapse(item[phase]["literal"]) in collapse(patch[phase]),
                                     "selected literal not in its declared patch")
            occurrence = {"unit_id": uid, "context_note": "Literal passage " + str(number) + ": " + kind,
                          "preserve_literal_pair": True}
            passage = {"edition": kind, "patch_index": patch_index}
            occurrence["english"], passage["english"] = selected(uid, "english", item["english"])
            occurrence[kind], passage["after"] = selected(uid, kind, item["after"])
            _, passage["before"] = selected(uid, kind, item["before"], before=True)
            if "before_role" in item:
                passage["before_role"] = item["before_role"]
            if "classical" in item:
                occurrence["classical"], passage["classical"] = selected(uid, "classical", item["classical"])
            occurrences.append(occurrence)
            passages.append(passage)
        relevant_histories = [copy.deepcopy(histories[(uid, kind)]) for kind in ("msa", "classical") if (uid, kind) in histories]
        changed_kinds = {item["edition"] for item in choice["literal_review_occurrences"]}
        enriched = dict(choice, recording_mode=choice.get("recording_mode", payload["recording_mode"]),
                        basis=choice.get("basis", choice.get("classification")),
                        edition="msa-and-classical" if changed_kinds == {"msa", "classical"} else next(iter(changed_kinds)))
        record = dated_repair_record(enriched, payload, identity, occurrences,
            {"sources": relevant_histories, "status": "historical-before-bytes-proved-by-exact-inverse-not-current-source"},
            enriched["edition"], choice["finding_id"], "\n\n".join(p["before"]["literal"] for p in passages))
        record["decision_id"] = "semantic-propagation-20260907:" + choice["decision_id"]
        record["literal_source_passages"] = passages
        record["semantic_propagation_repair"]["choice_record"] = copy.deepcopy(choice)
        result.append(record)
    dated_repair_require(sum(len(r["occurrences"]) for r in result) == (10 if arithmetic else 5 if semantic else 1),
                         "consolidated occurrence inventory mismatch")
    identity["adapter"] = {"kind": "dated-consolidated-repair-20260907", "terminology_rows_contributed": len(result)}
    return result, hashes


def normalize_next_batch_repairs(payload, identity, repo, baseline, english_root):
    """Six functions, six modal choices and four adjective choices; source-only.

    No claim is derived from a PASS label. Every admitted ledger, complete source,
    inverse patch, quoted context and clickable literal is independently checked.
    Canonical rows and ledgers remain unchanged inside the normalized records.
    """
    logical = identity["path"]
    contract = NEXT_BATCH_LEDGERS[logical]
    hashes, sources, histories, transactions = {}, {}, {}, {}
    raw = dated_repair_source(repo, identity, hashes)
    dated_repair_require(identity["sha256"].upper() == contract[0] and json.loads(raw) == payload,
                         "next batch pinned payload mismatch")
    dated_repair_require(english_root is not None and payload["schema"] == contract[1]
        and payload["assessed_on"] == "2026-09-07" and payload["open_to_correction"] is True,
        "next batch schema/date/provisional mismatch")
    dated_repair_no_page_claims(payload)
    choices = payload["decisions"]
    dated_repair_require(tuple(c["decision_id"] for c in choices) == contract[4], "next batch exact decision inventory mismatch")
    dated_repair_require(len(payload["transactions"]) == contract[2]
        and sum(len(t["patches"]) for t in payload["transactions"]) == contract[3], "next batch transaction inventory mismatch")
    for item in payload["primary_source_inventory"]:
        kind = item["edition"]
        root = english_root if kind == "english" else repo
        field = {"english": "source_path", "msa": "arabic_path", "classical": "target_path"}.get(kind)
        candidates = (["shared"] if kind == "shared" else [u for u, b in baseline.items()
                      if (root / b[field]).resolve() == (root / item["path"]).resolve()])
        dated_repair_require(len(candidates) == 1, "next batch source unit not uniquely identified")
        uid = item.get("unit_id", candidates[0])
        dated_repair_require(uid == candidates[0], "next batch declared unit differs from source")
        expected_path = (baseline[uid][{"english": "source_path", "msa": "arabic_path", "classical": "target_path"}[kind]]
                         if kind != "shared" else "source/locale/ar/open-logic-config.sty")
        dated_repair_require((root / item["path"]).resolve() == (root / expected_path).resolve(), "next batch source path mismatch")
        declaration = {"path": expected_path, "sha256": item["after_sha256"], "bytes": item["after_bytes"]}
        data = next_batch_version_source(root, declaration, hashes)
        dated_repair_require((uid, kind) not in sources, "duplicate next batch source identity")
        if kind == "english":
            dated_repair_require(sha256_bytes(data) == baseline[uid]["english_sha256"].upper(), "next batch frozen English mismatch")
        sources[(uid, kind)] = (data, declaration)
    for transaction in payload["transactions"]:
        uid, kind = transaction["unit_id"], transaction["edition"]
        data, declaration = sources[(uid, kind)]
        dated_repair_require(kind in {"msa", "classical"} and (uid, kind) not in transactions,
                             "next batch duplicate or non-Arabic transaction")
        dated_repair_require(transaction["path"] == declaration["path"] and
            transaction["after_sha256"].upper() == sha256_bytes(data) and transaction["after_bytes"] == len(data),
            "next batch transaction after identity mismatch")
        histories[(uid, kind)] = dated_repair_inverse(data, transaction["patches"],
            {"path": declaration["path"], "sha256": transaction["before_sha256"], "bytes": transaction["before_bytes"]})
        transactions[(uid, kind)] = transaction
        for patch in transaction["patches"]:
            dated_repair_require(patch["occurrences"] == 1 and bool(patch["decision_ids"])
                and set(patch["decision_ids"]) <= set(contract[4]), "next batch patch ownership mismatch")
            for phase in ("before", "after"):
                phase_data = histories[(uid, kind)]["text_utf8"].encode() if phase == "before" else data
                location = patch[phase + "_location"]
                dated_repair_require(phase_data[location["byte_start"]:location["byte_end"]] == patch[phase].encode(),
                                     "next batch exact patch byte range mismatch")
                dated_repair_require("\n".join(phase_data.decode().splitlines()[location["line_start"]-1:location["line_end"]])
                    == location["excerpt"], "next batch patch line context mismatch")
    # Complete recorded witness contexts, not just the few displayed words.
    for choice in choices:
        for witness in choice.get("source_witnesses", []) + choice.get("primary_evidence_before", []):
            uid, kind = witness["unit_id"], witness["edition"]
            if (uid, kind) not in sources:
                root = english_root if kind == "english" else repo
                expected = baseline[uid][{"english": "source_path", "msa": "arabic_path", "classical": "target_path"}[kind]]
                dated_repair_require((root / witness["path"]).resolve() == (root / expected).resolve(), "support witness baseline mismatch")
                declaration = {"path": expected, "sha256": witness["sha256"], "bytes": witness["bytes"]}
                sources[(uid, kind)] = (dated_repair_source(root, declaration, hashes), declaration)
            data, declaration = sources[(uid, kind)]
            if witness.get("phase", "before") == "before" and (uid, kind) in histories:
                data = histories[(uid, kind)]["text_utf8"].encode()
            dated_repair_require(( (english_root if kind == "english" else repo) / witness["path"]).resolve()
                == ((english_root if kind == "english" else repo) / declaration["path"]).resolve(), "next batch witness path mismatch")
            dated_repair_identity(data, dict(witness, path=declaration["path"]), declaration["path"])
            start, end = witness.get("line_start", witness.get("start_line")), witness.get("line_end", witness.get("end_line"))
            dated_repair_require("\n".join(data.decode("utf-8-sig").splitlines()[start-1:end]) == witness.get("excerpt", witness.get("quote")),
                                 "next batch primary witness context mismatch")
            if "byte_start" in witness:
                dated_repair_require(data[witness["byte_start"]:witness["byte_end"]] == witness["literal"].encode(),
                                     "next batch primary witness literal mismatch")
    result = []
    for choice in choices:
        matches = [(uid, kind, i, patch) for (uid, kind), t in transactions.items()
                   for i, patch in enumerate(t["patches"]) if choice["decision_id"] in patch["decision_ids"]]
        dated_repair_require(bool(matches) and len({uid for uid, _, _, _ in matches}) == 1,
                             "next batch choice has no or mixed-unit patches")
        uid = matches[0][0]
        occurrences, passages = [], []
        for _, kind, index, patch in matches:
            english_data, english_id = sources[(uid, "english")]
            supplied = next((o for o in choice.get("literal_review_occurrences", [])
                             if o["edition"] == kind and o["patch_index"] == index), None)
            if supplied:
                anchor = supplied["english"]
            else:
                witnesses = choice.get("source_witnesses", []) + choice.get("primary_evidence_before", [])
                selected = next(w for w in witnesses if w["edition"] == "english" and w["unit_id"] == uid)
                anchor = {"literal": selected.get("literal", selected.get("quote")),
                    "line_start": selected.get("line_start", selected.get("start_line")),
                    "line_end": selected.get("line_end", selected.get("end_line"))}
            preferred = NEXT_BATCH_ENGLISH_LITERALS.get(choice["decision_id"])
            if preferred:
                literal = preferred[index] if len(preferred) > 1 else preferred[0]
                contexts = [w.get("literal", w.get("quote", "")) for w in
                    choice.get("source_witnesses", []) + choice.get("primary_evidence_before", [])
                    if w["edition"] == "english" and w["unit_id"] == uid]
                dated_repair_require(any(qualification_active_phrase_ranges(c, literal, "english", 1) for c in contexts),
                                     "selected English subphrase absent from canonical context")
                anchor = {"literal": literal, "line_start": 1, "line_end": len(english_data.decode().splitlines())}
            eg, ew = next_batch_literal(uid, "english", english_data, english_id["path"], anchor["literal"],
                                       anchor["line_start"], anchor["line_end"])
            data, declaration = sources[(uid, kind)]
            old = histories[(uid, kind)]["text_utf8"].encode()
            phase_witnesses = {}
            for phase, body in (("before", old), ("after", data)):
                loc = patch[phase + "_location"]
                _, phase_witnesses[phase] = next_batch_literal(uid, kind, body, declaration["path"], patch[phase], loc["line_start"], loc["line_end"])
            ag, aw = next_batch_live_literal(repo, uid, kind, data, phase_witnesses["after"], hashes)
            passage = {"edition": kind, "patch_index": index, "english": ew, "before": phase_witnesses["before"], "after": aw}
            if aw != phase_witnesses["after"]:
                passage["assessed_after"] = phase_witnesses["after"]
                passage["before_role"] = "Before and assessed-after are historical stages; the linked after passage is verified current wording."
            occurrences.append({"unit_id": uid, "context_note": "Exact correction passage: " + kind,
                "preserve_literal_pair": True, "english": eg, kind: ag})
            passages.append(passage)
        # Modal schema names actual choices on bindings, not on a top-level term.
        # These are explicit display projections; the original row remains intact.
        enriched = dict(choice, unit_id=uid, finding_id=choice.get("finding_id", choice["decision_id"]),
            chosen_arabic=choice.get("chosen_arabic") or "\n\n".join(dict.fromkeys(p["after"]["literal"] for p in passages)),
            sense=choice.get("sense") or choice["english_term"], basis=choice.get("basis") or "contextual-semantic-source-correction",
            recording_mode=choice.get("recording_mode", payload["recording_mode"]),
            edition="msa-and-classical" if {k for _, k, _, _ in matches} == {"msa", "classical"} else matches[0][1])
        record = dated_repair_record(enriched, payload, identity, occurrences,
            {"sources": [copy.deepcopy(histories[(uid, kind)]) for kind in ("msa", "classical") if (uid, kind) in histories],
             "status": "historical-before-bytes-proved-by-exact-inverse-not-current-source"}, enriched["edition"],
            enriched["finding_id"], "\n\n".join(p["before"]["literal"] for p in passages))
        record["decision_id"] = "semantic-propagation-20260907:" + choice["decision_id"]
        record["literal_source_passages"] = passages
        record["semantic_propagation_repair"]["choice_record"] = copy.deepcopy(choice)
        result.append(record)
    dated_repair_require(sum(len(r["occurrences"]) for r in result) == contract[3], "next batch occurrence inventory mismatch")
    identity["adapter"] = {"kind": "dated-next-source-batch-20260907", "terminology_rows_contributed": len(result),
        "historical_motives_or_new_attestation_claimed": False}
    return result, hashes


def normalize_applied_dual_repairs(payload: dict, identity: dict, repo: Path,
                                  baseline: dict[str, dict], english_root: Path | None
                                  ) -> tuple[list[dict], dict[Path, str]]:
    dated_repair_require(identity["sha256"] == APPLIED_DUAL_SHA256, "unapproved dual grammar ledger identity")
    dated_repair_require(english_root is not None and payload.get("schema") == "openlogic-olp0067-dual-grammar-repairs-v1"
                         and payload.get("assessed_on") == "2026-09-06"
                         and payload.get("status") == "implemented-in-both-arabic-wording-registers",
                         "dual grammar schema/provenance mismatch")
    rows = payload["decisions"]
    dated_repair_require([r["decision_id"] for r in rows] == [
        f"ar-{kind}-OLP0067-signed-formula-{case}-20260906" for kind in ("msa", "classical")
        for case in ("added-nominative", "both-genitive", "closure-genitive")], "dual grammar six-choice inventory mismatch")
    hashes, result = {}, []
    prior = dated_repair_prior(repo, hashes)["OLP-0067"]
    expected = baseline["OLP-0067"]
    english_id = payload["authorities"]["english"]
    dated_repair_require(english_id["path"] == expected["source_path"], "dual grammar English path mismatch")
    english = dated_repair_source(english_root, english_id, hashes)
    dated_repair_require(sha256_bytes(english) == expected["english_sha256"].upper() == prior["english_sha256"].upper(),
                         "dual grammar frozen English mismatch")
    sources, histories = {}, {}
    for kind, field in (("msa", "arabic_path"), ("classical", "target_path")):
        edition = payload["editions"][kind]
        dated_repair_require(edition["after"]["path"] == expected[field]
                             and all(edition["before"][k] == prior[kind][k] for k in ("path", "sha256", "bytes")),
                             "dual grammar pinned predecessor mismatch")
        sources[kind] = dated_repair_source(repo, edition["after"], hashes)
        patches = [r["patch"] for r in rows if r["edition"] == kind]
        for p in patches:
            dated_repair_require(p["inverse_before"] == p["after"] and p["inverse_after"] == p["before"],
                                 "dual grammar inverse declaration mismatch")
        histories[kind] = dated_repair_inverse(sources[kind], patches, edition["before"])
    for row in rows:
        kind = row["edition"]
        occurrences = row["occurrences"]
        dated_repair_require(row["unit_id"] == "OLP-0067" and len(occurrences) == 1
                             and occurrences[0]["edition"] == kind, "dual grammar occurrence inventory mismatch")
        occurrence = occurrences[0]
        before = histories[kind]["text_utf8"].encode("utf-8")
        dated_repair_excerpt(before, occurrence["before"], expected["arabic_path" if kind == "msa" else "target_path"])
        dated_repair_excerpt(english, row["source_evidence"], expected["source_path"])
        literal = row["english_source_literal"]
        dated_repair_require(sha256_bytes(literal.encode("utf-8")) == row["english_source_literal_sha256"].upper()
                             and sha256_bytes(row["english_source_literal_raw"].encode("utf-8")) == row["english_source_literal_raw_sha256"].upper()
                             and row["english_source_literal_raw"].replace("\r\n", "\n") == literal
                             and english.count(row["english_source_literal_raw"].encode("utf-8")) == 1,
                             "dual grammar literal source phrase mismatch")
        dated_repair_require(qualification_active_phrase_ranges(occurrence["before"]["excerpt"], row["patch"]["before"], kind,
                                                               occurrence["before"]["line_start"]),
                             "dual grammar historical patch missing from witness")
        for authority in row["authority_checks"]:
            witnesses = authority.get("witnesses", []) + ([authority["witness"]] if "witness" in authority else [])
            for witness in witnesses:
                data = dated_repair_source(repo, witness, hashes)
                dated_repair_excerpt(data, witness, witness["path"])
        normalized = {"unit_id": "OLP-0067",
            "english": dated_repair_occurrence("OLP-0067", "english", english, row["english_source_literal_witness"], literal),
            kind: dated_repair_occurrence("OLP-0067", kind, sources[kind], occurrence["after"], row["chosen_arabic"])}
        record = dated_repair_record(row, payload, identity, normalized, copy.deepcopy(histories[kind]), kind, row["decision_id"], row["patch"]["before"])
        record["alternatives"] = [{**copy.deepcopy(a), "form": a.get("form", a.get("wording"))} for a in row["alternatives"]]
        result.append(record)
    identity["adapter"] = {"kind": "dated-applied-dual-grammar-repair-v1", "terminology_rows_contributed": len(result)}
    return result, hashes


def normalize_applied_scope_repairs(payload: dict, identity: dict, repo: Path,
                                    baseline: dict[str, dict], english_root: Path | None
                                    ) -> tuple[list[dict], dict[Path, str]]:
    if identity["path"] != APPLIED_SCOPE_LEDGER:
        return [], {}
    # Pin the admitted assessment, not a self-asserted success flag. Independent
    # current-byte, passage and reversible predecessor checks still follow.
    dated_repair_require(identity["sha256"] == APPLIED_SCOPE_SHA256,
                         "unapproved scope ledger identity")
    dated_repair_require(english_root is not None and payload.get("schema") == "openlogic-semantic-qualification-repairs-v1"
                         and payload.get("assessed_on") == "2026-09-06"
                         and payload.get("recording_mode") == "retrospective-reconstruction"
                         and payload.get("status") == "implemented-in-shared-msa-source"
                         and payload.get("unit_count") == 3 and payload.get("decision_count") == 4,
                         "scope assessment schema/provenance mismatch")
    rows = payload.get("units", [])
    dated_repair_require(len(rows) == 3 and {r.get("unit_id"): r.get("decision_id") for r in rows} == APPLIED_SCOPE_IDS,
                         "scope choice inventory mismatch")
    hashes, result = {}, []
    prior = dated_repair_prior(repo, hashes)
    for row in rows:
        uid = row["unit_id"]
        expected = baseline[uid]
        previous = prior[uid]
        data_by_kind = {}
        for kind, field in (("english", "source_path"), ("msa", "arabic_path"), ("classical", "target_path")):
            loc = row["locations"][kind]
            dated_repair_require(loc.get("path") == expected[field], "scope baseline path mismatch")
            data = dated_repair_source(english_root if kind == "english" else repo, loc, hashes)
            data_by_kind[kind] = data
            dated_repair_excerpt(data, loc, expected[field])
            if kind == "english":
                dated_repair_require(sha256_bytes(data) == str(expected["english_sha256"]).upper()
                                     == str(previous["english_sha256"]).upper(), "frozen English identity mismatch")
            if kind == "classical":
                dated_repair_identity(data, previous[kind], expected[field])
        anchor = row["historical_before_anchor"]
        dated_repair_require(anchor["path"] == QUALIFICATION_PRIOR_MANIFEST_RELATIVE.as_posix()
                             and str(anchor["sha256"]).upper() == QUALIFICATION_PRIOR_MANIFEST_SHA256
                             and anchor["unit_id"] == uid and anchor["identity"] == previous["msa"]
                             and anchor["prior_correction"] == previous.get("correction"),
                             "scope pinned predecessor declaration mismatch")
        history = dated_repair_inverse(data_by_kind["msa"], row["patches"], previous["msa"])
        before = history["text_utf8"].encode("utf-8")
        current = row["locations"]["msa"]
        old_loc = {"path": current["path"], "sha256": current["before_sha256"], "bytes": current["before_bytes"],
                   **{k: current["before_" + k] for k in ("line_start", "line_end", "excerpt", "excerpt_sha256")}}
        dated_repair_excerpt(before, old_loc, current["path"])
        for witness in row["supporting_primary_witnesses"]:
            kind = witness["edition"]
            dated_repair_excerpt(data_by_kind[kind], witness, row["locations"][kind]["path"])
        for kind, declared in row["reviewed_primary_files"].items():
            dated_repair_identity(data_by_kind[kind], declared, row["locations"][kind]["path"])
            dated_repair_require(declared["lines_read"] == [1, len(data_by_kind[kind].decode("utf-8-sig").splitlines())],
                                 "whole-file review endpoints mismatch")
        choices = [row] + row.get("additional_phrase_choices", [])
        dated_repair_require(len(choices) == (2 if uid == "OLP-0060" else 1), "scope additional choice inventory mismatch")
        for choice in choices:
            if choice is not row:
                dated_repair_require(choice["decision_id"] == "scope-0060-prefix-final-index"
                                     and choice["unit_patch_indices"] == [1]
                                     and choice["patches"] == [row["patches"][1]], "scope subchoice patch mismatch")
                old_loc = choice["locations"]["msa_before"]
            dated_repair_occurrence(uid, "msa", before, old_loc, choice["before_arabic"])
            occurrence = {"unit_id": uid}
            for kind, term in (("english", choice["source_term"]), ("msa", choice["chosen_arabic"]),
                               ("classical", choice["classical_arabic"])):
                occurrence[kind] = dated_repair_occurrence(uid, kind, data_by_kind[kind], choice["locations"][kind], term)
            result.append(dated_repair_record(choice, payload, identity, occurrence, copy.deepcopy(history), "msa", row["finding_id"]))
    identity["adapter"] = {"kind": "dated-applied-scope-repair-v1", "terminology_rows_contributed": len(result)}
    return result, hashes


def load_decisions(
    repo: Path,
    paths: Sequence[Path],
    baseline_units: Sequence[dict] = (),
    english_root: Path | None = None,
) -> tuple[list[dict], list[dict], dict[Path, str]]:
    decision_variants: dict[str, list[dict]] = defaultdict(list)
    inventory: list[dict] = []
    hashes: dict[Path, str] = {}
    duplicate_review_sources: dict[str, list[dict]] = defaultdict(list)
    for path in paths:
        resolved = path.resolve()
        raw = resolved.read_bytes()
        digest = sha256_bytes(raw)
        hashes[resolved] = digest
        try:
            relative = resolved.relative_to(repo.resolve()).as_posix()
        except ValueError:
            relative = resolved.name
        identity = {"path": relative, "bytes": len(raw), "sha256": digest}
        inventory.append(identity)
        if resolved.suffix.casefold() == ".csv":
            rows = normalize_locale_csv(
                repo, raw, identity, baseline_units, english_root
            )
            for decision in rows:
                decision_variants[decision["decision_id"]].append(decision)
            continue
        payload = json.loads(raw.decode("utf-8-sig"))
        if not isinstance(payload, dict):
            raise ValueError(f"ledger is not an object: {relative}")
        difficult_review = payload.get("difficult_terminology")
        if isinstance(difficult_review, list) and difficult_review:
            identity["adapter"] = {
                "kind": "authoritative-repair-duplicate-provenance-v1",
                "candidate_rows": len(difficult_review),
                "terminology_rows_contributed": 0,
                "duplicate_rows_linked_to_authoritative_repair": len(difficult_review),
            }
            for raw_review in difficult_review:
                if isinstance(raw_review, dict) and collapse(raw_review.get("id")):
                    duplicate_review_sources[collapse(raw_review["id"])].append(identity)
        rows = payload.get("terminology_decisions")
        if not isinstance(rows, list):
            rows = payload.get("decisions")
        repair_rows = normalize_repair_decisions(payload, identity)
        owner_followup_rows = normalize_owner_followup_findings(payload, identity)
        baseline_by_id, _ = baseline_lookup(baseline_units)
        propagation_rows, propagation_hashes = normalize_semantic_propagation_repairs(
            payload, identity, repo, baseline_by_id, english_root
        )
        qualification_rows, qualification_hashes = normalize_qualification_propagation_repairs(
            payload, identity, repo, baseline_by_id, english_root
        )
        applied_rows, applied_hashes = normalize_applied_repairs(
            payload, identity, repo, baseline_by_id, english_root
        )
        if relative in APPLIED_REPAIR_LEDGERS:
            rows = []  # Only strictly admitted rows may enter, never a generic duplicate.
        propagation_rows += applied_rows
        for source_path, digest in applied_hashes.items():
            if source_path in propagation_hashes and propagation_hashes[source_path] != digest:
                raise ValueError(f"applied repair source changed during loading: {source_path}")
            propagation_hashes[source_path] = digest
        propagation_rows += qualification_rows
        for source_path, digest in qualification_hashes.items():
            if source_path in propagation_hashes and propagation_hashes[source_path] != digest:
                raise ValueError(f"qualification source changed during loading: {source_path}")
            propagation_hashes[source_path] = digest
        for source_path, digest in propagation_hashes.items():
            if source_path in hashes and hashes[source_path] != digest:
                raise ValueError(f"propagation source changed during loading: {source_path}")
            hashes[source_path] = digest
        compact_rows = normalize_compact_decisions(
            payload, identity, repo, baseline_by_id
        )
        if not isinstance(rows, list):
            rows = []
        rows = list(rows) + repair_rows + owner_followup_rows + compact_rows + propagation_rows
        repair_by_unit = {
            str(item.get("unit_id")): item
            for item in payload.get("repairs") or []
            if isinstance(item, dict)
        }
        for original in rows:
            if not isinstance(original, dict):
                raise ValueError(f"non-object decision in {relative}")
            decision = copy.deepcopy(original)
            enrich_legacy_occurrence_paths(
                decision, payload, repo, baseline_by_id
            )
            if not collapse(decision.get("rationale")) and collapse(
                decision.get("motivation")
            ):
                decision["rationale"] = collapse(decision["motivation"])
            if not isinstance(decision.get("occurrences"), list) and collapse(
                decision.get("unit_id")
            ):
                repair = repair_by_unit.get(collapse(decision.get("unit_id")))
                if repair and collapse(repair.get("target_path")):
                    decision["occurrences"] = [
                        {
                            "unit_id": collapse(decision["unit_id"]),
                            "classical": {
                                "path": collapse(repair["target_path"]),
                                "sha256": collapse(repair.get("after_sha256")),
                                "locator_status": (
                                    "Repair ledger supplies exact current file identity; "
                                    "the generator must recover a discrete term line by exact search."
                                ),
                            },
                        }
                    ]
            decision_id = decision.get("decision_id")
            if not isinstance(decision_id, str) or not decision_id.strip():
                raise ValueError(f"decision without decision_id in {relative}")
            is_propagation_row = any(original is row for row in propagation_rows)
            if decision.get("semantic_propagation_repair") and not is_propagation_row:
                raise ValueError(f"unvalidated dated propagation assessment in {relative}")
            if decision_id.startswith(("semantic-propagation-20260906:", "semantic-propagation-20260907:")) and (
                not is_propagation_row or decision_variants[decision_id]
            ):
                raise ValueError(f"unexpected/duplicate dated propagation decision ID: {decision_id}")
            for field in ("english_term", "chosen_arabic", "rationale"):
                if not collapse(decision.get(field)):
                    raise ValueError(f"{decision_id}: missing {field} in {relative}")
            if decision.get("open_to_correction") is not True:
                raise ValueError(f"{decision_id}: open_to_correction must be true")
            decision["source_record"] = identity
            decision_variants[decision_id].append(decision)

    decisions: list[dict] = []
    for recorded_id, variants in sorted(decision_variants.items()):
        by_core: dict[str, list[dict]] = defaultdict(list)
        for decision in variants:
            core = copy.deepcopy(decision)
            core.pop("source_record", None)
            core.pop("occurrences", None)
            signature = json.dumps(
                core, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            )
            by_core[signature].append(decision)
        merged_variants: list[dict] = []
        for signature, group in sorted(by_core.items()):
            merged = copy.deepcopy(group[0])
            source_records = []
            occurrence_by_identity: dict[str, dict] = {}
            for decision in group:
                source_record = decision["source_record"]
                if source_record not in source_records:
                    source_records.append(source_record)
                for occurrence in decision.get("occurrences") or []:
                    key = json.dumps(
                        occurrence,
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    )
                    occurrence_by_identity[key] = copy.deepcopy(occurrence)
            merged["occurrences"] = [
                occurrence_by_identity[key] for key in sorted(occurrence_by_identity)
            ]
            merged["source_records"] = sorted(
                source_records, key=lambda row: row["path"]
            )
            merged["source_record"] = merged["source_records"][0]
            merged_variants.append(merged)
        if len(merged_variants) == 1:
            decisions.append(merged_variants[0])
            continue
        for merged in merged_variants:
            core = copy.deepcopy(merged)
            core.pop("source_record", None)
            core.pop("source_records", None)
            core.pop("occurrences", None)
            core_hash = sha256_bytes(
                json.dumps(
                    core, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                ).encode("utf-8")
            )[:8].lower()
            merged["recorded_decision_id"] = recorded_id
            merged["decision_id"] = f"{recorded_id}--variant-{core_hash}"
            merged["decision_id_collision_resolution"] = (
                "The same recorded ID was used for materially different decisions. "
                "Variants remain separate under deterministic content-derived IDs; "
                "no occurrence or rationale was suppressed."
            )
            decisions.append(merged)
    ordered = sorted(
        decisions,
        key=lambda row: (collapse(row.get("english_term")).casefold(), row["decision_id"]),
    )
    for decision in ordered:
        recorded_id = collapse(
            decision.get("recorded_decision_id") or decision.get("decision_id")
        )
        repair_id = recorded_id.rsplit(":", 1)[-1]
        sources = duplicate_review_sources.get(repair_id) or []
        if not sources or not recorded_id.startswith("repair-0401-0500:"):
            continue
        source_records = list(decision.get("source_records") or [decision["source_record"]])
        for source in sources:
            if source not in source_records:
                source_records.append(copy.deepcopy(source))
        decision["source_records"] = sorted(source_records, key=lambda row: row["path"])
        decision["duplicate_review_source_records"] = sorted(
            (copy.deepcopy(source) for source in sources), key=lambda row: row["path"]
        )
        decision["duplicate_review_provenance_note"] = (
            "The independent-review snapshot duplicates this authoritative repair row; "
            "it is retained as provenance without a second human decision."
        )
    apply_authoritative_repair_precedence(ordered)
    ordered, exact_deduplicated = merge_exact_semantic_duplicates(ordered)
    locale_exact_deduplicated = sum(
        1
        for decision in ordered
        for duplicate in decision.get("deduplicated_source_decisions") or []
        if collapse(duplicate.get("source_record", {}).get("path")).endswith(
            "TERMINOLOGY_AND_ADVERSE_LEDGER.csv"
        )
    )
    for identity in inventory:
        if identity.get("adapter", {}).get("kind") == "locale-ar-terminology-and-adverse-csv-v1":
            identity["adapter"]["exact_semantic_duplicates_merged"] = (
                locale_exact_deduplicated
            )
            identity["adapter"]["global_exact_semantic_duplicates_merged"] = exact_deduplicated
    return ordered, inventory, hashes


@dataclass(frozen=True)
class AuxLabel:
    printed_page: str
    title: str
    destination: str


def parse_group_sequence(value: str) -> list[str]:
    fields: list[str] = []
    position = 0
    while position < len(value):
        while position < len(value) and value[position].isspace():
            position += 1
        if position >= len(value):
            break
        parsed = parse_braced(value, position)
        if parsed is None:
            break
        field, position = parsed
        fields.append(field)
    return fields


def parse_aux_labels(path: Path) -> dict[str, AuxLabel]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    labels: dict[str, AuxLabel] = {}
    for match in re.finditer(r"\\newlabel\s*", text):
        first = parse_braced(text, match.end())
        if first is None:
            continue
        name, position = first
        second = parse_braced(text, position)
        if second is None or name.endswith("@cref"):
            continue
        payload, _ = second
        fields = parse_group_sequence(payload)
        if len(fields) >= 4:
            labels[name] = AuxLabel(
                printed_page=collapse(fields[1]),
                title=collapse(fields[2]),
                destination=collapse(fields[3]),
            )
    return labels


def normalize_sync_path(value: str) -> str:
    value = value.strip().strip('"').replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return value.casefold()


@dataclass
class SyncIndex:
    path: Path
    inputs: dict[int, str]
    tag_line_pages: dict[tuple[int, int], set[int]]

    @classmethod
    def load(cls, path: Path) -> "SyncIndex":
        if path.suffix.casefold() == ".gz":
            with gzip.open(path, "rt", encoding="utf-8", errors="replace") as stream:
                text = stream.read()
        else:
            text = path.read_text(encoding="utf-8", errors="replace")
        inputs: dict[int, str] = {}
        page: int | None = None
        records: dict[tuple[int, int], set[int]] = defaultdict(set)
        for line in text.splitlines():
            if line.startswith("Input:"):
                parts = line.split(":", 2)
                if len(parts) == 3 and parts[1].isdigit():
                    inputs[int(parts[1])] = parts[2].strip()
                continue
            sheet = re.fullmatch(r"\{(\d+)", line.strip())
            if sheet:
                page = int(sheet.group(1))
                continue
            if re.fullmatch(r"\}\d+", line.strip()):
                page = None
                continue
            if page is None:
                continue
            record = SYNC_RECORD.match(line)
            if record:
                records[(int(record.group(1)), int(record.group(2)))].add(page)
        return cls(path=path, inputs=inputs, tag_line_pages=dict(records))

    def pages_for(
        self,
        logical_path: str,
        fs_path: Path | None,
        line_start: int,
        line_end: int,
    ) -> tuple[list[int], str | None]:
        logical = normalize_sync_path(logical_path)
        absolute = normalize_sync_path(str(fs_path.resolve())) if fs_path else ""
        exact = [tag for tag, name in self.inputs.items() if normalize_sync_path(name) == absolute]
        if exact:
            tags = exact
        else:
            suffix = "/" + logical.lstrip("/")
            tags = [
                tag for tag, name in self.inputs.items()
                if normalize_sync_path(name).endswith(suffix)
                or normalize_sync_path(name) == logical
            ]
            distinct = {normalize_sync_path(self.inputs[tag]) for tag in tags}
            if len(distinct) > 1:
                return [], "ambiguous SyncTeX source-path match"
        if not tags:
            return [], "source path absent from SyncTeX inputs"
        pages: set[int] = set()
        for tag in tags:
            for line in range(line_start, line_end + 1):
                pages.update(self.tag_line_pages.get((tag, line), set()))
        if not pages:
            return [], "no exact SyncTeX record for the resolved source line"
        return sorted(pages), None


class ReaderEvidence:
    def __init__(
        self,
        name: str,
        source_kind: str,
        pdf_path: Path,
        component_pdf_path: Path | None,
        aux_path: Path | None,
        synctex_path: Path | None,
        page_offset: int,
        repo: Path,
    ) -> None:
        if source_kind not in {"msa", "classical"}:
            raise ValueError(f"reader {name!r}: source kind must be msa or classical")
        try:
            import pypdf
        except ImportError as exc:  # pragma: no cover - depends on host runtime
            raise RuntimeError("pypdf is required when --reader-pdf is supplied") from exc
        self.name = name
        self.source_kind = source_kind
        self.pdf_path = pdf_path.resolve()
        self.component_pdf_path = component_pdf_path.resolve() if component_pdf_path else None
        self.aux_path = aux_path.resolve() if aux_path else None
        self.synctex_path = synctex_path.resolve() if synctex_path else None
        self.page_offset = page_offset
        if page_offset < 0:
            raise ValueError(f"reader {name!r}: page offset must be non-negative")
        if not self.pdf_path.is_file():
            raise FileNotFoundError(self.pdf_path)
        if self.aux_path and not self.aux_path.is_file():
            raise FileNotFoundError(self.aux_path)
        if self.synctex_path and not self.synctex_path.is_file():
            raise FileNotFoundError(self.synctex_path)
        if self.component_pdf_path and not self.component_pdf_path.is_file():
            raise FileNotFoundError(self.component_pdf_path)
        self.pdf = pypdf.PdfReader(str(self.pdf_path))
        self.page_count = len(self.pdf.pages)
        try:
            labels = list(self.pdf.page_labels)
        except Exception:
            labels = []
        self.page_labels = labels if len(labels) == self.page_count else []
        # A component PDF supplies its own page-label tree and named
        # destinations.  Its physical pages are translated into the assembled
        # reader with the explicit offset.  Without a component PDF, named
        # destinations are already in assembled-reader coordinates.
        self.component_pdf = (
            pypdf.PdfReader(str(self.component_pdf_path))
            if self.component_pdf_path else None
        )
        map_pdf = self.component_pdf or self.pdf
        self.map_page_count = len(map_pdf.pages)
        try:
            component_labels = list(map_pdf.page_labels)
        except Exception:
            component_labels = []
        self.component_page_labels = (
            component_labels if len(component_labels) == self.map_page_count else []
        )
        def named_pages(pdf) -> dict[str, int]:
            result: dict[str, int] = {}
            for key, destination in pdf.named_destinations.items():
                try:
                    result[str(key)] = pdf.get_destination_page_number(destination) + 1
                except Exception:
                    continue
            return result

        self.named_pages = named_pages(map_pdf)
        self.assembled_named_pages = (
            named_pages(self.pdf) if self.component_pdf else self.named_pages
        )
        self.aux_labels = parse_aux_labels(self.aux_path) if self.aux_path else {}
        self.sync = SyncIndex.load(self.synctex_path) if self.synctex_path else None
        self.identity = {
            "name": name,
            "source_kind": source_kind,
            "assembled_pdf": self._identity(self.pdf_path, repo),
            "component_pdf": (
                self._identity(self.component_pdf_path, repo)
                if self.component_pdf_path else None
            ),
            "aux": self._identity(self.aux_path, repo) if self.aux_path else None,
            "synctex": self._identity(self.synctex_path, repo) if self.synctex_path else None,
            "component_page_offset": self.page_offset,
            "assembled_pdf_page_count": self.page_count,
            "component_pdf_page_count": self.map_page_count if self.component_pdf else None,
        }

    @staticmethod
    def _identity(path: Path, repo: Path) -> dict:
        try:
            label = path.resolve().relative_to(repo.resolve()).as_posix()
        except ValueError:
            label = path.name
        return {"path": label, "bytes": path.stat().st_size, "sha256": sha256_file(path)}

    def printed_for_component_page(self, component_page: int, assembled_page: int) -> str | None:
        labels = self.component_page_labels if self.component_pdf else self.page_labels
        index = component_page if self.component_pdf else assembled_page
        if 1 <= index <= len(labels):
            value = collapse(labels[index - 1])
            return value or None
        return None

    def locate(self, location: dict, unit: UnitMeta) -> dict:
        sync_reason: str | None = None
        if (
            self.sync is not None
            and location["line_reconciliation"]["resolved"]
            and location.get("_fs_path") is not None
        ):
            start = int(location["line_reconciliation"]["current_line_start"])
            end = int(location["line_reconciliation"]["current_line_end"])
            component_pages, sync_reason = self.sync.pages_for(
                location["logical_path"], location["_fs_path"], start, end
            )
            mapped_pages = [
                page for page in component_pages
                if 1 <= page <= self.map_page_count
                and 1 <= page + self.page_offset <= self.page_count
            ]
            if component_pages and not mapped_pages:
                sync_reason = "SyncTeX page lies outside configured component/assembled PDF bounds"
            component_pages = mapped_pages
            if component_pages:
                assembled_pages = [page + self.page_offset for page in component_pages]
                return {
                    "reader": self.name,
                    "method": "synctex-exact",
                    "exact_occurrence_page": True,
                    "pdf_pages": assembled_pages,
                    "assembled_pdf_pages": assembled_pages,
                    "component_pdf_pages": component_pages,
                    "component_page_offset": self.page_offset,
                    "printed_pages": [
                        {
                            "pdf_page": assembled_page,
                            "assembled_pdf_page": assembled_page,
                            "component_pdf_page": component_page,
                            "printed_page": self.printed_for_component_page(
                                component_page, assembled_page
                            ),
                        }
                        for component_page, assembled_page
                        in zip(component_pages, assembled_pages)
                    ],
                    "note": (
                        "Exact resolved source line matched a component SyncTeX record; "
                        "the declared component offset maps it to the assembled reader."
                    ),
                }

        if unit.aux_label and unit.aux_label in self.aux_labels:
            label = self.aux_labels[unit.aux_label]
            component_page = self.named_pages.get(label.destination)
            if component_page is None:
                component_page = self.named_pages.get(unit.aux_label)
            if component_page is not None and self.component_pdf:
                pdf_page = component_page + self.page_offset
                destination_source = "component PDF"
            elif self.component_pdf:
                # Assembly may preserve a destination that a stripped
                # component PDF does not.  Such a destination is already in
                # assembled coordinates and therefore receives no offset.
                pdf_page = self.assembled_named_pages.get(label.destination)
                if pdf_page is None:
                    pdf_page = self.assembled_named_pages.get(unit.aux_label)
                destination_source = "assembled PDF"
            else:
                # Named destinations read from the assembled PDF are already
                # in assembled coordinates.  The offset still applies to
                # SyncTeX, but must not be added a second time here.
                pdf_page = component_page
                destination_source = "assembled PDF"
            if pdf_page is not None and not (1 <= pdf_page <= self.page_count):
                pdf_page = None
            note = "Unit/section start from AUX label"
            if pdf_page is not None:
                note += f" and {destination_source} named destination"
            else:
                note += "; matching PDF named destination unavailable"
            if sync_reason:
                note += f"; {sync_reason}"
            return {
                "reader": self.name,
                "method": "unit-start-fallback",
                "exact_occurrence_page": False,
                "pdf_pages": [pdf_page] if pdf_page is not None else [],
                "assembled_pdf_pages": [pdf_page] if pdf_page is not None else [],
                "component_pdf_pages": (
                    [component_page] if component_page is not None and self.component_pdf else []
                ),
                "component_page_offset": self.page_offset,
                "printed_pages": [
                    {
                        "pdf_page": pdf_page,
                        "assembled_pdf_page": pdf_page,
                        "component_pdf_page": (
                            component_page if self.component_pdf else None
                        ),
                        "printed_page": label.printed_page,
                    }
                ],
                "unit_aux_label": unit.aux_label,
                "pdf_destination": label.destination,
                "note": note + "; this is not asserted as the term's exact page.",
            }

        reasons = []
        if self.sync is None:
            reasons.append("SyncTeX not supplied")
        elif sync_reason:
            reasons.append(sync_reason)
        if not unit.aux_label:
            reasons.append("unit has no derivable AUX label")
        elif not self.aux_path:
            reasons.append("AUX not supplied")
        elif unit.aux_label not in self.aux_labels:
            reasons.append(f"AUX label {unit.aux_label!r} absent")
        return {
            "reader": self.name,
            "method": "unavailable",
            "exact_occurrence_page": False,
            "pdf_pages": [],
            "printed_pages": [],
            "note": "; ".join(reasons) or "No deterministic page evidence.",
        }


def parse_assignments(values: Iterable[str], option: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"{option} expects NAME=VALUE, got {value!r}")
        name, assigned = value.split("=", 1)
        name, assigned = name.strip(), assigned.strip()
        if not name or not assigned:
            raise ValueError(f"{option} expects non-empty NAME=VALUE")
        if name in result and result[name] != assigned:
            raise ValueError(f"{option}: duplicate conflicting reader {name!r}")
        result[name] = assigned
    return result


def infer_reader_source(name: str) -> str:
    lowered = name.casefold()
    if "classical" in lowered:
        return "classical"
    if any(token in lowered for token in ("msa", "international", "machrek")):
        return "msa"
    raise ValueError(
        f"cannot infer source kind for reader {name!r}; use --reader-source {name}=msa|classical"
    )


def build_readers(args: argparse.Namespace, repo: Path) -> list[ReaderEvidence]:
    pdfs = parse_assignments(args.reader_pdf, "--reader-pdf")
    component_pdfs = parse_assignments(args.reader_component_pdf, "--reader-component-pdf")
    auxes = parse_assignments(args.reader_aux, "--reader-aux")
    synctexes = parse_assignments(args.reader_synctex, "--reader-synctex")
    sources = parse_assignments(args.reader_source, "--reader-source")
    offsets = parse_assignments(args.reader_page_offset, "--reader-page-offset")
    unknown = (
        set(component_pdfs) | set(auxes) | set(synctexes) | set(sources) | set(offsets)
    ) - set(pdfs)
    if unknown:
        raise ValueError(f"reader metadata has no matching --reader-pdf: {sorted(unknown)}")
    readers = []
    for name in sorted(pdfs):
        source_kind = sources.get(name) or infer_reader_source(name)
        try:
            offset = int(offsets.get(name, "0"))
        except ValueError as exc:
            raise ValueError(f"reader {name!r}: offset must be an integer") from exc
        readers.append(
            ReaderEvidence(
                name=name,
                source_kind=source_kind,
                pdf_path=Path(pdfs[name]),
                component_pdf_path=(
                    Path(component_pdfs[name]) if name in component_pdfs else None
                ),
                aux_path=Path(auxes[name]) if name in auxes else None,
                synctex_path=Path(synctexes[name]) if name in synctexes else None,
                page_offset=offset,
                repo=repo,
            )
        )
    return readers


def reconcile_location(
    raw: dict,
    repo: Path,
    english_root: Path | None,
    cache: SourceCache,
    repo_web_root: str,
    english_web_root: str,
) -> dict:
    source_kind = raw["source_kind"]
    recorded_path = str(raw.get("path") or "")
    result = copy.deepcopy(raw)
    result["recorded_path"] = recorded_path
    result.pop("path", None)
    if not recorded_path:
        result.update(
            logical_path="",
            current_sha256=None,
            file_url=None,
            source_url=None,
            line_reconciliation={
                "status": "unresolved-missing-path",
                "resolved": False,
                "current_line_start": None,
                "current_line_end": None,
                "candidate_line_ranges": [],
                "recorded_hash_matches_current": False,
            },
            _fs_path=None,
        )
        return result

    fs_path, logical = resolve_source_path(repo, english_root, recorded_path, source_kind)
    result["logical_path"] = logical
    result["file_url"] = source_web_url(
        logical, source_kind, repo_web_root, english_web_root
    )
    result["_fs_path"] = fs_path
    if fs_path is None:
        result.update(
            current_sha256=None,
            source_url=None,
            line_reconciliation={
                "status": "unresolved-file-missing",
                "resolved": False,
                "current_line_start": None,
                "current_line_end": None,
                "candidate_line_ranges": [],
                "recorded_hash_matches_current": False,
            },
        )
        return result
    snapshot = cache.get(fs_path, logical)
    reconciliation = reconcile_lines(
        snapshot,
        raw.get("line_start"),
        raw.get("line_end"),
        str(raw.get("excerpt") or ""),
        str(raw.get("recorded_sha256") or ""),
    )
    result["current_sha256"] = snapshot.sha256
    result["line_reconciliation"] = reconciliation
    if reconciliation["resolved"]:
        result["source_url"] = source_web_url(
            logical,
            source_kind,
            repo_web_root,
            english_web_root,
            reconciliation["current_line_start"],
            reconciliation["current_line_end"],
        )
        start = int(reconciliation["current_line_start"])
        end = int(reconciliation["current_line_end"])
        result["current_excerpt"] = "\n".join(snapshot.lines[start - 1:end])
    else:
        result["source_url"] = None
        result["current_excerpt"] = None
    return result


def _validated_expert_source_group(
    declaration: dict,
    repo: Path,
    english_root: Path | None,
    expected_path: str | None,
    declaration_sha256: str,
) -> tuple[str, dict, list[dict]]:
    """Validate one canonical declaration and return occurrence/global raws."""

    required = {
        "source_kind", "path", "line_ranges", "file_sha256",
        "cited_text_sha256", "semantic_basis",
    }
    if set(declaration) != required:
        raise ValueError(
            "expert source binding location has unexpected keys: "
            + ", ".join(sorted(set(declaration) ^ required))
        )
    source_kind = collapse(declaration.get("source_kind"))
    if source_kind not in SOURCE_LABELS:
        raise ValueError(f"expert source binding has invalid source kind {source_kind!r}")
    recorded_path = collapse(declaration.get("path")).replace("\\", "/")
    if not recorded_path:
        raise ValueError("expert source binding has a blank path")
    if expected_path is not None and recorded_path != expected_path.replace("\\", "/"):
        raise ValueError(
            f"expert source binding path/unit mismatch: {recorded_path} != {expected_path}"
        )
    fs_path, _ = resolve_source_path(
        repo, english_root, recorded_path, source_kind
    )
    if fs_path is None or not fs_path.is_file():
        raise ValueError(f"expert source binding file is missing: {recorded_path}")
    raw_bytes = fs_path.read_bytes()
    current_sha256 = sha256_bytes(raw_bytes)
    if current_sha256 != collapse(declaration.get("file_sha256")).upper():
        raise ValueError(f"expert source binding file hash mismatch: {recorded_path}")
    source_lines = raw_bytes.decode("utf-8").splitlines()
    declared_ranges = declaration.get("line_ranges")
    if not isinstance(declared_ranges, list) or not declared_ranges:
        raise ValueError(f"expert source binding has no line ranges: {recorded_path}")
    cited_lines: list[str] = []
    locator_rows: list[dict] = []
    flat_ranges: list[list[int]] = []
    for line_range in declared_ranges:
        if not isinstance(line_range, list) or len(line_range) != 2:
            raise ValueError(f"expert source binding has malformed range: {recorded_path}")
        start, end = line_range
        if (
            not isinstance(start, int)
            or not isinstance(end, int)
            or start < 1
            or end < start
            or end > len(source_lines)
        ):
            raise ValueError(
                f"expert source binding has out-of-bounds range: {recorded_path}:{start}-{end}"
            )
        excerpt_lines = source_lines[start - 1:end]
        if not strip_tex_comments("\n".join(excerpt_lines)).strip():
            raise ValueError(
                f"expert source binding range is blank/comment-only: {recorded_path}:{start}-{end}"
            )
        cited_lines.extend(excerpt_lines)
        flat_ranges.append([start, end])
        locator_rows.append(
            {
                "line_start": start,
                "line_end": end,
                "excerpt": "\n".join(excerpt_lines),
                "ledger_locator_status": EXPERT_SOURCE_BINDING_WITNESS,
                "witness": {
                    "rule": EXPERT_SOURCE_BINDING_WITNESS,
                    "validated": True,
                    "declaration_sha256": declaration_sha256,
                    "declared_file_sha256": current_sha256,
                    "declared_line_ranges": copy.deepcopy(declared_ranges),
                    "range_cited_text_sha256": sha256_bytes(
                        "\n".join(excerpt_lines).encode("utf-8")
                    ),
                    "semantic_basis": collapse(declaration.get("semantic_basis")),
                },
            }
        )
    cited_sha256 = sha256_bytes("\n".join(cited_lines).encode("utf-8"))
    if cited_sha256 != collapse(declaration.get("cited_text_sha256")).upper():
        raise ValueError(f"expert source binding excerpt hash mismatch: {recorded_path}")
    if not collapse(declaration.get("semantic_basis")):
        raise ValueError(f"expert source binding has blank semantic basis: {recorded_path}")
    group = {
        "path": recorded_path,
        "sha256": current_sha256,
        "locator_status": EXPERT_SOURCE_BINDING_WITNESS,
        "locators": locator_rows,
    }
    global_rows = [
        {
            "source_kind": source_kind,
            "path": recorded_path,
            "recorded_sha256": current_sha256,
            "line_start": locator["line_start"],
            "line_end": locator["line_end"],
            "excerpt": locator["excerpt"],
            "ledger_locator_status": EXPERT_SOURCE_BINDING_WITNESS,
            "witness": copy.deepcopy(locator["witness"]),
        }
        for locator in locator_rows
    ]
    return source_kind, group, global_rows


def apply_expert_source_bindings(
    repo: Path,
    baseline_path: Path,
    baseline_units: Sequence[dict],
    decisions: list[dict],
    english_root: Path | None,
) -> tuple[dict, Path | None, str | None]:
    """Attach the canonical 70-decision source audit, if present.

    The public generator repeats every byte/range/path check.  A canonical
    declaration can therefore add semantic source evidence without weakening
    any of the historical locator guards.
    """

    path = (repo / EXPERT_SOURCE_BINDINGS_RELATIVE).resolve()
    if not path.is_file():
        return {}, None, None
    payload, raw = read_json_bytes(path)
    if not isinstance(payload, dict) or payload.get("schema") != EXPERT_SOURCE_BINDING_SCHEMA:
        raise ValueError("expert source bindings have the wrong schema")
    declaration_sha256 = sha256_bytes(raw)
    authority = payload.get("authority")
    if not isinstance(authority, dict) or authority.get("witness_rule") != EXPERT_SOURCE_BINDING_WITNESS:
        raise ValueError("expert source bindings have the wrong witness rule")
    baseline_identity = authority.get("baseline")
    if not isinstance(baseline_identity, dict):
        raise ValueError("expert source bindings omit the baseline identity")
    baseline_raw = baseline_path.read_bytes()
    if (
        baseline_identity.get("bytes") != len(baseline_raw)
        or collapse(baseline_identity.get("sha256")).upper() != sha256_bytes(baseline_raw)
    ):
        raise ValueError("expert source bindings were not made against this baseline")
    bindings = payload.get("bindings")
    if not isinstance(bindings, list) or len(bindings) != 70:
        raise ValueError("expert source bindings must contain exactly 70 decisions")
    indices = [item.get("selected_index") for item in bindings if isinstance(item, dict)]
    if indices != list(range(1, 71)):
        raise ValueError("expert source binding indices are not exactly 1..70")
    decisions_by_id = {collapse(item.get("decision_id")): item for item in decisions}
    declared_ids = [collapse(item.get("decision_id")) for item in bindings]
    if len(set(declared_ids)) != 70:
        raise ValueError("expert source bindings contain duplicate decision IDs")
    currently_unbound = {
        collapse(item.get("decision_id"))
        for item in decisions
        if collapse(item.get("decision_id")).startswith("locale-ar-chosen-")
        and not (item.get("occurrences") or [])
    }
    if set(declared_ids) != currently_unbound:
        missing = sorted(currently_unbound - set(declared_ids))
        extra = sorted(set(declared_ids) - currently_unbound)
        raise ValueError(
            "expert source bindings do not exactly cover current unbound Arabic decisions: "
            f"missing={missing[:5]}, extra={extra[:5]}"
        )
    units = {collapse(unit.get("id")): unit for unit in baseline_units}
    totals = Counter()
    for binding in bindings:
        decision_id = collapse(binding.get("decision_id"))
        decision = decisions_by_id[decision_id]
        disposition = collapse(binding.get("disposition"))
        occurrences = binding.get("occurrences")
        globals_ = binding.get("global_locations")
        unresolved = binding.get("unresolved_components")
        if not isinstance(occurrences, list) or not isinstance(globals_, list) or not isinstance(unresolved, list):
            raise ValueError(f"{decision_id}: malformed expert binding arrays")
        if disposition == "bound" and not occurrences:
            raise ValueError(f"{decision_id}: bound declaration lacks an occurrence")
        if disposition == "partially-bound" and (not occurrences or not unresolved):
            raise ValueError(f"{decision_id}: partial declaration lacks one side")
        if disposition == "global-source-only" and (occurrences or not globals_):
            raise ValueError(f"{decision_id}: global-only declaration has an invalid locator mix")
        if disposition not in {"bound", "partially-bound", "global-source-only"}:
            raise ValueError(f"{decision_id}: invalid expert binding disposition")
        occurrence_rows = []
        seen_units: set[str] = set()
        for occurrence in occurrences:
            unit_id = collapse(occurrence.get("unit_id"))
            if unit_id in seen_units or unit_id not in units:
                raise ValueError(f"{decision_id}: duplicate or unknown unit {unit_id!r}")
            seen_units.add(unit_id)
            unit = units[unit_id]
            expected_paths = {
                "english": collapse(unit.get("source_path")),
                "msa": collapse(unit.get("arabic_path")),
                "classical": collapse(unit.get("target_path")),
            }
            raw_occurrence = {
                "unit_id": unit_id,
                "context_note": collapse(binding.get("binding_note")),
                "expert_source_binding_witness": EXPERT_SOURCE_BINDING_WITNESS,
            }
            seen_kinds: set[str] = set()
            for declaration in occurrence.get("locations") or []:
                kind = collapse(declaration.get("source_kind"))
                source_kind, group, _ = _validated_expert_source_group(
                    declaration,
                    repo,
                    english_root,
                    expected_paths.get(kind),
                    declaration_sha256,
                )
                if source_kind in seen_kinds:
                    raise ValueError(f"{decision_id}: duplicate {source_kind} unit source")
                seen_kinds.add(source_kind)
                raw_occurrence[source_kind] = group
                # Canonical totals count one source declaration even when it
                # deliberately cites several discontiguous exact ranges.
                totals["unit_source_locations"] += 1
            if not seen_kinds:
                raise ValueError(f"{decision_id}: unit occurrence has no source locations")
            occurrence_rows.append(raw_occurrence)
        global_rows: list[dict] = []
        for declaration in globals_:
            _, _, expanded = _validated_expert_source_group(
                declaration, repo, english_root, None, declaration_sha256
            )
            global_rows.extend(expanded)
            totals["global_source_locations"] += 1
        decision["occurrences"] = merge_raw_occurrences(
            list(decision.get("occurrences") or []) + occurrence_rows
        )
        decision["_expert_global_source_raw"] = global_rows
        decision["expert_source_binding"] = {
            "disposition": disposition,
            "binding_note": collapse(binding.get("binding_note")),
            "unresolved_components": [collapse(item) for item in unresolved],
            "witness_rule": EXPERT_SOURCE_BINDING_WITNESS,
        }
        totals["bindings"] += 1
        totals[disposition] += 1
        totals["unit_occurrences"] += len(occurrence_rows)
        totals["unresolved_components"] += len(unresolved)
    declared_totals = payload.get("totals") or {}
    total_mapping = {
        "bindings": totals["bindings"],
        "bound": totals["bound"],
        "partially_bound": totals["partially-bound"],
        "global_source_only": totals["global-source-only"],
        "unit_occurrences": totals["unit_occurrences"],
        "unit_source_locations": totals["unit_source_locations"],
        "global_source_locations": totals["global_source_locations"],
        "unresolved_components": totals["unresolved_components"],
    }
    if declared_totals != total_mapping:
        raise ValueError(
            f"expert source binding totals mismatch: {declared_totals!r} != {total_mapping!r}"
        )
    identity = {
        "path": path.relative_to(repo.resolve()).as_posix(),
        "bytes": len(raw),
        "sha256": declaration_sha256,
        "schema": payload["schema"],
        "witness_rule": EXPERT_SOURCE_BINDING_WITNESS,
        "totals": total_mapping,
    }
    return identity, path, declaration_sha256


def alternatives_text(decision: dict) -> list[str]:
    display = decision.get("review_display")
    rows = (
        display.get("alternatives")
        if isinstance(display, dict) and isinstance(display.get("alternatives"), list)
        else decision.get("alternatives")
    )
    if not isinstance(rows, list) or not rows:
        return []
    rendered = []
    for row in rows:
        if isinstance(row, str):
            rendered.append(trim_alternative_workflow_tail(collapse(row)))
            continue
        if not isinstance(row, dict):
            rendered.append(trim_alternative_workflow_tail(collapse(row)))
            continue
        form = collapse(row.get("form") or row.get("alternative") or row.get("value"))
        status = collapse(row.get("status") or row.get("decision"))
        reason = collapse(row.get("reason") or row.get("disposition") or row.get("note"))
        pieces = [piece for piece in (form, status, reason) if piece]
        rendered.append(
            trim_alternative_workflow_tail(
                " — ".join(pieces) or json.dumps(row, ensure_ascii=False, sort_keys=True)
            )
        )
    return rendered


def trim_alternative_workflow_tail(value: str) -> str:
    tails = (
        " — Present retrospective alternative assessment, not a reconstructed claim "
        "about the earlier author's original deliberation.",
        " — Contemporaneous alternative assessment; provisional wording remains in "
        "use pending better evidence, without delaying construction.",
    )
    for tail in tails:
        if value.endswith(tail):
            return value[:-len(tail)].rstrip()
    return value


def default_review_question(decision: dict) -> str:
    default = (
        f"Is «{human_chosen_arabic(decision)}» the best Arabic rendering of "
        f"“{human_english_term(decision)}” in the stated mathematical sense? "
        "هل هذه الصياغة العربية هي الأدق في هذا المعنى الرياضي؟"
    )
    reason = human_decision_field(decision, "expert_review_reason")
    return default + (f" Review context / سياق المراجعة: {reason}" if reason else "")


def review_question(decision: dict) -> str:
    display = decision.get("review_display")
    explicit = (
        display.get("expert_question")
        if isinstance(display, dict) else None
    ) or decision.get("expert_question") or decision.get("expert_review_question")
    if collapse(explicit):
        question = collapse(explicit)
        raw_english = collapse(decision.get("english_term"))
        raw_arabic = collapse(decision.get("chosen_arabic"))
        # Replace quoted raw fields first so mixed bilingual questions retain
        # the correct locale-specific registry expansion.
        for left, right in (("“", "”"), ('"', '"')):
            question = question.replace(
                left + raw_english + right,
                left + human_english_term(decision) + right,
            )
        question = question.replace(
            "«" + raw_arabic + "»",
            "«" + human_chosen_arabic(decision) + "»",
        )
        if (
            TOKEN_SHORTHAND.search(question)
            or USETOKEN.search(question)
            or PRINTTOKEN.search(question)
            or re.search(r"\\[A-Za-z@]+", question)
        ):
            # A mixed-language unquoted macro is ambiguous.  Use the precise
            # generated question instead of leaking implementation syntax.
            explicit = None
        else:
            return human_prose(question)
    return default_review_question(decision)


def strip_private(value: object) -> object:
    if isinstance(value, dict):
        return {
            key: strip_private(item)
            for key, item in value.items()
            if not key.startswith("_")
        }
    if isinstance(value, list):
        return [strip_private(item) for item in value]
    return value


def page_summary(page: dict) -> str:
    reader = md_text(page["reader"])
    method = page["method"]
    if method == "synctex-exact":
        pairs = []
        printed_by_pdf = {
            item.get("pdf_page"): item.get("printed_page")
            for item in page.get("printed_pages", [])
        }
        for pdf_page in page.get("pdf_pages", []):
            printed = printed_by_pdf.get(pdf_page)
            if printed:
                pairs.append(f"assembled PDF {pdf_page}; printed {md_text(printed)}")
            else:
                pairs.append(f"assembled PDF {pdf_page}; printed page unavailable")
        return f"{reader}: " + ", ".join(pairs) + " — exact SyncTeX"
    if method == "unit-start-fallback":
        pdfs = page.get("pdf_pages") or []
        printed = [
            item.get("printed_page") for item in page.get("printed_pages", [])
            if item.get("printed_page")
        ]
        bits = []
        if pdfs:
            bits.append("assembled PDF " + ", ".join(str(number) for number in pdfs))
        if printed:
            bits.append("printed " + ", ".join(md_text(item) for item in printed))
        value = "; ".join(bits) or "page identifiers unavailable"
        return f"{reader}: {value} — **unit-start fallback, not exact term page**"
    return f"{reader}: unavailable — {md_text(page.get('note'))}"


def markdown_source_href(
    location: dict, exact_line: bool, arabic_prefix: str = "../../../"
) -> str:
    """Use compact repository-relative Arabic links and pinned English links."""

    if location["source_kind"] == "english":
        key = "source_url" if exact_line else "file_url"
        return str(location.get(key) or "")
    logical = str(location.get("logical_path") or "").lstrip("/")
    href = arabic_prefix + quote(logical, safe="/")
    if exact_line:
        reconciliation = location["line_reconciliation"]
        start = reconciliation["current_line_start"]
        end = reconciliation["current_line_end"]
        href += f"#L{start}"
        if end != start:
            href += f"-L{end}"
    return href


def markdown_relative_directory(from_directory: Path, target_directory: Path) -> str:
    """Return a URL-quoted relative directory link, failing on cross-drive output."""

    try:
        relative = os.path.relpath(
            target_directory.resolve(), start=from_directory.resolve()
        )
    except ValueError as exc:
        raise ValueError(
            "Markdown output and its linked directory must be on the same drive"
        ) from exc
    normalized = relative.replace("\\", "/")
    return "" if normalized == "." else quote(normalized, safe="/._-")


def markdown_relative_prefix(from_directory: Path, target_directory: Path) -> str:
    directory = markdown_relative_directory(from_directory, target_directory)
    return (directory + "/") if directory else ""


def markdown_relative_file(from_directory: Path, target_file: Path) -> str:
    directory = markdown_relative_directory(from_directory, target_file.parent)
    filename = quote(target_file.name, safe="._-")
    return f"{directory}/{filename}" if directory else filename


def markdown_candidate_href(
    location: dict,
    start: int,
    end: int,
    arabic_prefix: str = "../../../",
) -> str:
    if location["source_kind"] == "english":
        href = str(location.get("file_url") or "")
    else:
        logical = str(location.get("logical_path") or "").lstrip("/")
        href = arabic_prefix + quote(logical, safe="/")
    if not href:
        return ""
    href += f"#L{start}"
    if end != start:
        href += f"-L{end}"
    return href


class LinkRegistry:
    """Use reference links only when a URL actually repeats."""

    def __init__(self, counts: Counter[str]) -> None:
        self.counts = counts
        self.references: dict[str, str] = {}

    def link(self, label: str, href: str) -> str:
        if self.counts[href] <= 1:
            return f"[{label}]({href})"
        if href not in self.references:
            self.references[href] = "r" + self._base36(len(self.references) + 1)
        return f"[{label}][{self.references[href]}]"

    @staticmethod
    def _base36(value: int) -> str:
        digits = "0123456789abcdefghijklmnopqrstuvwxyz"
        result = ""
        while value:
            value, remainder = divmod(value, 36)
            result = digits[remainder] + result
        return result or "0"

    def definitions(self) -> list[str]:
        return [f"[{reference}]: {href}" for href, reference in self.references.items()]


def human_occurrence_rows(decision: dict) -> list[dict]:
    return [
        occurrence for occurrence in decision["index_metadata"]["occurrences"]
        if occurrence.get("human_review_included", True)
    ]


def human_location_rows(occurrence: dict) -> list[dict]:
    return [
        location for location in occurrence["locations"]
        if location.get("human_review_included", True)
    ]


def human_global_source_rows(decision: dict) -> list[dict]:
    """Return exact global/front-matter locations without inventing a unit."""

    return [
        location for location in decision.get("global_source_bindings") or []
        if location.get("human_review_included", True)
    ]


def expert_unresolved_components(decision: dict) -> list[str]:
    binding = decision.get("expert_source_binding") or {}
    return [
        collapse(item) for item in binding.get("unresolved_components") or []
        if collapse(item)
    ]


def append_global_source_markdown(
    lines: list[str],
    decision: dict,
    link_registry: "LinkRegistry",
    arabic_prefix: str,
    indent: str = "",
) -> None:
    locations = human_global_source_rows(decision)
    if not locations:
        return
    lines.append(
        indent
        + "- **Exact global/front-matter source location; no OLP unit or reader-page claim "
        "/ موضع دقيق في المصدر العام أو الصفحات التمهيدية؛ بلا وحدة OLP ولا ادعاء لصفحة القارئ:**"
    )
    for rendered in location_lines_markdown(
        locations, False, link_registry, arabic_prefix=arabic_prefix
    ):
        lines.append(indent + rendered)


def append_unresolved_component_markdown(
    lines: list[str], decision: dict, indent: str = ""
) -> None:
    for component in expert_unresolved_components(decision):
        lines.append(
            indent
            + "- ⚠ **Component still unresolved / جزء ما زال غير مربوط بموضع:** "
            + md_text(component)
        )


def grouped_human_occurrence_rows(decision: dict) -> list[dict]:
    """Group repeated unit headings while preserving every displayed locator.

    Several ledgers record one term more than once in the same Open Logic unit.
    Repeating the unit heading for every ledger row makes the review sheets hard
    to scan.  This view groups only that heading: every non-duplicate source
    locator remains in order, and every distinct locationless note remains
    visible.  The underlying occurrence records stay unchanged in JSON and CSV.
    """

    grouped: dict[tuple[str, str], dict] = {}
    for occurrence in human_occurrence_rows(decision):
        unit = occurrence["unit"]
        key = (collapse(unit.get("unit_id")), collapse(unit.get("title")))
        row = grouped.setdefault(
            key,
            {
                "unit": unit,
                "occurrence_record_count": 0,
                "locations": [],
                "missing_language_notes": [],
                "locationless_notes": [],
            },
        )
        row["occurrence_record_count"] += 1
        locations = human_location_rows(occurrence)
        row["locations"].extend(locations)
        missing = missing_language_note(occurrence)
        if missing and missing not in row["missing_language_notes"]:
            row["missing_language_notes"].append(missing)
        if not locations:
            note = locationless_occurrence_note(occurrence)
            rendered = note or "No source edition/path/line was supplied for this occurrence."
            if rendered not in row["locationless_notes"]:
                row["locationless_notes"].append(rendered)
    return list(grouped.values())


def distinct_human_occurrence_rows(decision: dict) -> list[dict]:
    """Return one sortable row per distinct human-visible occurrence.

    Raw ledgers sometimes repeat the same decision, unit and exact locators.
    Those provenance records remain separate in JSON, but repeating an
    indistinguishable CSV row gives a reviewer no additional place to check.
    """

    seen: set[tuple] = set()
    rows: list[dict] = []
    for occurrence in human_occurrence_rows(decision):
        location_keys = []
        for location in human_location_rows(occurrence):
            reconciliation = location["line_reconciliation"]
            non_locator = non_locator_reconciliation_status(
                reconciliation["status"]
            )
            location_keys.append(
                (
                    location["source_kind"],
                    collapse(
                        location.get("logical_path") or location.get("recorded_path")
                    ),
                    reconciliation["status"],
                    None if non_locator else reconciliation.get("current_line_start"),
                    None if non_locator else reconciliation.get("current_line_end"),
                    json.dumps(
                        location.get("page_evidence") or [],
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                )
            )
        key = (
            collapse(occurrence["unit"].get("unit_id")),
            tuple(sorted(location_keys)),
            locationless_occurrence_note(occurrence),
            missing_language_note(occurrence),
        )
        if key in seen:
            continue
        seen.add(key)
        rows.append(occurrence)
    return rows


def make_link_registry(
    decisions: Sequence[dict], arabic_prefix: str = "../../../"
) -> LinkRegistry:
    """Count the public links used by a selected human-facing decision set."""

    link_counts: Counter[str] = Counter()
    for decision in decisions:
        location_sets = [
            human_location_rows(occurrence)
            for occurrence in human_occurrence_rows(decision)
        ]
        if human_global_source_rows(decision):
            location_sets.append(human_global_source_rows(decision))
        for locations in location_sets:
            groups: dict[tuple[str, str], bool] = {}
            for location in locations:
                file_href = markdown_source_href(
                    location, exact_line=False, arabic_prefix=arabic_prefix
                )
                group = (location["source_kind"], file_href)
                groups[group] = groups.get(group, False) or not location[
                    "line_reconciliation"
                ]["resolved"]
                if location["line_reconciliation"]["resolved"]:
                    link_counts[
                        markdown_source_href(
                            location, exact_line=True, arabic_prefix=arabic_prefix
                        )
                    ] += 1
            for (_, file_href), has_unresolved in groups.items():
                if file_href and has_unresolved:
                    link_counts[file_href] += 1
    return LinkRegistry(link_counts)


def location_lines_markdown(
    locations: list[dict],
    readers_present: bool,
    link_registry: LinkRegistry,
    arabic_prefix: str = "../../../",
) -> list[str]:
    """Render all locations compactly, grouping only repeated file metadata.

    Each resolved occurrence remains its own clickable line/range link.  The
    exact excerpts and per-location hashes stay in JSON, while grouping avoids
    repeating a long repository URL and label in prose thousands of times.
    """

    file_groups: dict[tuple[str, str, str], list[dict]] = {}
    for location in locations:
        key = (
            location["source_kind"],
            location.get("logical_path") or location.get("recorded_path") or "",
            location.get("file_url") or "",
        )
        file_groups.setdefault(key, []).append(location)

    lines: list[str] = []
    for (source_kind, logical_path, file_url), rows in file_groups.items():
        source_label = SOURCE_LABELS.get(source_kind, source_kind)
        short_path = logical_path.replace("\\", "/").split("/")[-1]
        if file_url and any(
            not row["line_reconciliation"]["resolved"] for row in rows
        ):
            file_display = link_registry.link(
                md_text(short_path),
                markdown_source_href(
                    rows[0], exact_line=False, arabic_prefix=arabic_prefix
                ),
            )
        else:
            file_display = f"`{md_text(short_path or 'path missing')}`"
        lines.append(f"    - **{md_text(source_label)}:** {file_display}")

        resolved_buckets: dict[tuple[str, bool, str], list[dict]] = {}
        unresolved_rows = []
        for location in rows:
            reconciliation = location["line_reconciliation"]
            if not reconciliation["resolved"]:
                unresolved_rows.append(location)
                continue
            page_key = json.dumps(
                location.get("page_evidence") or [],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            key = (
                reconciliation["status"],
                bool(reconciliation["recorded_hash_matches_current"]),
                page_key,
            )
            resolved_buckets.setdefault(key, []).append(location)

        for (status, hash_matches, _), bucket in resolved_buckets.items():
            links = []
            for location in bucket:
                reconciliation = location["line_reconciliation"]
                start = reconciliation["current_line_start"]
                end = reconciliation["current_line_end"]
                label = f"L{start}" if start == end else f"L{start}–L{end}"
                links.append(
                    link_registry.link(
                        label,
                        markdown_source_href(
                            location, exact_line=True, arabic_prefix=arabic_prefix
                        ),
                    )
                )
            notes = []
            if status == "relocated-by-exact-excerpt":
                notes.append("moved lines, each re-found by one unique exact excerpt")
            elif status.startswith("relocated-by-unique-exact-"):
                basis = collapse(
                    bucket[0]["line_reconciliation"].get("recovery_basis")
                )
                notes.append(
                    "recovered by a unique exact search"
                    + (f" ({basis})" if basis else "")
                )
            if not hash_matches:
                notes.append("current file differs from recorded snapshot")
            suffix = " — " + "; ".join(notes) if notes else ""
            lines.append("      - " + ", ".join(links) + suffix)
            page_rows = bucket[0].get("page_evidence") or []
            if page_rows:
                lines.extend(
                    f"        - Pages / الصفحات — {page_summary(page)}"
                    for page in page_rows
                )
            elif readers_present and source_kind in {"msa", "classical"}:
                lines.append("        - Pages / الصفحات — no matching final-reader configuration.")

        for location in unresolved_rows:
            reconciliation = location["line_reconciliation"]
            if non_locator_reconciliation_status(reconciliation["status"]):
                lines.append(
                    "      - ℹ **unit-wide / no discrete lexical occurrence** — "
                    + md_text(reconciliation.get("non_locator_reason"))
                )
                continue
            start = location.get("line_start")
            end = location.get("line_end")
            recorded = "no line asserted"
            if start is not None:
                recorded = f"recorded L{start}" + (f"–L{end}" if end != start else "")
            candidates = (
                reconciliation.get("candidate_line_ranges")
                or reconciliation.get("exact_search_candidate_line_ranges")
                or []
            )
            candidate_note = ""
            if candidates:
                labels = []
                for first, last in candidates[:12]:
                    label = f"L{first}" if first == last else f"L{first}–L{last}"
                    href = markdown_candidate_href(
                        location, first, last, arabic_prefix=arabic_prefix
                    )
                    labels.append(f"[{label}]({href})" if href else label)
                candidate_note = "; exact-search candidates, **not yet sense-resolved**: " + ", ".join(labels)
                if len(candidates) > 12:
                    candidate_note += f", … (+{len(candidates) - 12})"
            lines.append(
                "      - ⚠ **unresolved** — "
                f"{recorded}; `{md_text(reconciliation['status'])}`{candidate_note}"
            )
    return lines


def missing_language_note(occurrence: dict) -> str:
    missing = occurrence.get("language_coverage", {}).get("not_recorded_source_kinds") or []
    labels = [SOURCE_LABELS.get(kind, kind) for kind in missing]
    if not labels:
        return ""
    return (
        "No occurrence supplied in the ledger for / لا موضع مسجل في السجل لـ: "
        + ", ".join(labels)
        + ". This is not counted as an unresolved locator / ولا يُعد ذلك موضعًا مسجلًا متعذر الحسم."
    )


def locationless_occurrence_note(occurrence: dict) -> str:
    """Explain a proved unit-only record without implying a lexical location."""

    raw = occurrence.get("raw_occurrence") or {}
    if not isinstance(raw, dict):
        return ""
    return humanize_tex(
        raw.get("locale_locator_status")
        or raw.get("compact_locator_status")
        or raw.get("locator_status")
        or ""
    )


def unresolved_decision_locator_lines(decision: dict) -> list[str]:
    """Summarize non-bindable path/unit evidence, never promoting it to a link."""

    lines = []
    for evidence in decision.get("unresolved_locator_evidence") or []:
        if not isinstance(evidence, dict):
            continue
        precision = humanize_tex(evidence.get("precision")) or "unresolved"
        path = humanize_tex(
            evidence.get("normalized_path") or evidence.get("recorded_path")
        )
        units = [
            collapse(value)
            for value in evidence.get("recorded_unit_ids") or []
            if collapse(value)
        ]
        pieces = [precision]
        if units:
            pieces.append("unit(s) " + ", ".join(units))
        if path:
            pieces.append("recorded path " + path)
        lines.append("; ".join(pieces) + "; no exact source line claimed")
    return lines


def suppress_duplicate_locator_stubs(occurrences: Sequence[dict]) -> None:
    """Hide empty identity stubs when the same unit has a located occurrence."""

    by_unit: dict[str, list[dict]] = defaultdict(list)
    for occurrence in occurrences:
        by_unit[occurrence["unit"]["unit_id"]].append(occurrence)
    for siblings in by_unit.values():
        has_located = any(
            any(
                location.get("human_review_included", True)
                and location["line_reconciliation"]["resolved"]
                for location in occurrence["locations"]
            )
            for occurrence in siblings
        )
        if not has_located:
            continue
        for occurrence in siblings:
            locations = human_location_rows(occurrence)
            stub = not locations or all(
                location["line_reconciliation"]["status"]
                in {
                    "unresolved-no-line-locator",
                    "unit-wide/no-discrete-lexical-occurrence",
                }
                and not location["line_reconciliation"].get(
                    "exact_search_candidate_line_ranges"
                )
                for location in locations
            )
            if stub:
                occurrence["human_review_included"] = False
                occurrence["human_review_exclusion_reason"] = (
                    "Unlocated identity stub superseded in the human index by a located "
                    "occurrence for the same decision and unit; raw record retained in JSON."
                )


def suppress_repeated_human_locations(occurrences: Sequence[dict]) -> None:
    """Show each indistinguishable locator or empty unit stub only once.

    Machine records remain untouched apart from explicit display-disposition
    metadata, so duplicate provenance is still auditable in JSON.
    """

    resolved_files: set[tuple[str, str, str]] = set()
    for occurrence in occurrences:
        unit_id = occurrence["unit"]["unit_id"]
        for location in human_location_rows(occurrence):
            if location["line_reconciliation"]["resolved"]:
                resolved_files.add(
                    (
                        unit_id,
                        location["source_kind"],
                        collapse(location.get("logical_path") or location.get("recorded_path")),
                    )
                )

    seen_locations: set[tuple] = set()
    seen_empty_units: set[str] = set()
    for occurrence in occurrences:
        unit_id = occurrence["unit"]["unit_id"]
        # An English witness may participate in several separately proved
        # translation pairs. Preserve it in each distinct canonical pair, while
        # still suppressing a wholly duplicated pair or duplicate local locator.
        pair_scope = None
        if occurrence.get("raw_occurrence", {}).get("preserve_literal_pair") is True:
            pair_scope = tuple(sorted(
                (loc["source_kind"], collapse(loc.get("logical_path") or loc.get("recorded_path")),
                 loc["line_reconciliation"].get("current_line_start"),
                 loc["line_reconciliation"].get("current_line_end"))
                for loc in occurrence["locations"]
            ))
        for location in human_location_rows(occurrence):
            reconciliation = location["line_reconciliation"]
            logical = collapse(
                location.get("logical_path") or location.get("recorded_path")
            )
            file_key = (unit_id, location["source_kind"], logical)
            no_line_stub = (
                not reconciliation["resolved"]
                and location.get("line_start") is None
                and not reconciliation.get("exact_search_candidate_line_ranges")
                and not reconciliation.get("candidate_line_ranges")
            )
            if no_line_stub and file_key in resolved_files:
                location["human_review_included"] = False
                location["human_review_exclusion_reason"] = (
                    "File-only locator stub superseded by an exact locator for the same "
                    "decision, unit, language and file; raw record retained in JSON."
                )
                continue
            locator_key = (
                pair_scope,
                unit_id,
                location["source_kind"],
                logical,
                reconciliation["status"],
                reconciliation.get("current_line_start"),
                reconciliation.get("current_line_end"),
                location.get("line_start"),
                location.get("line_end"),
                normalized_excerpt(str(location.get("current_excerpt") or location.get("excerpt") or "")),
            )
            if locator_key in seen_locations:
                location["human_review_included"] = False
                location["human_review_exclusion_reason"] = (
                    "Duplicate human locator suppressed; the separate raw ledger record "
                    "and provenance remain in JSON."
                )
            else:
                seen_locations.add(locator_key)

        included = human_location_rows(occurrence)
        if not occurrence["locations"]:
            if unit_id in seen_empty_units:
                occurrence["human_review_included"] = False
                occurrence["human_review_exclusion_reason"] = (
                    "Duplicate empty occurrence stub for this decision and unit; raw "
                    "record retained in JSON."
                )
            else:
                seen_empty_units.add(unit_id)
        elif not included and all(
            location.get("human_review_exclusion_reason")
            for location in occurrence["locations"]
        ):
            occurrence["human_review_included"] = False
            occurrence["human_review_exclusion_reason"] = (
                "All human locators in this occurrence duplicate richer or earlier "
                "display locators; raw record retained in JSON."
            )
        occurrence["human_review_location_count"] = len(included)


def normalized_review_headword(value: object) -> str:
    return unicodedata.normalize("NFKC", collapse(value)).casefold()


def refresh_decision_index_counts(decision: dict) -> None:
    metadata = decision["index_metadata"]
    occurrences = metadata["occurrences"]
    for item in occurrences:
        item["human_review_location_count"] = len(human_location_rows(item))
    metadata["occurrence_group_count"] = sum(
        1 for item in occurrences if item["human_review_included"]
    )
    metadata["machine_occurrence_group_count"] = len(occurrences)
    metadata["location_count"] = sum(
        item["human_review_location_count"]
        for item in occurrences
        if item["human_review_included"]
    )
    metadata["machine_location_count"] = sum(
        item["machine_location_count"] for item in occurrences
    )


def suppress_cross_decision_locator_stubs(decisions: Sequence[dict]) -> None:
    """Hide exact-headword identity stubs superseded by located records."""

    located: dict[tuple[str, str], set[str]] = defaultdict(set)
    for decision in decisions:
        headword = normalized_review_headword(decision.get("english_term"))
        for occurrence in decision["index_metadata"]["occurrences"]:
            if any(
                location["line_reconciliation"]["resolved"]
                for location in human_location_rows(occurrence)
            ):
                located[(headword, occurrence["unit"]["unit_id"])].add(
                    decision["decision_id"]
                )

    for decision in decisions:
        headword = normalized_review_headword(decision.get("english_term"))
        superseded_by = set()
        for occurrence in decision["index_metadata"]["occurrences"]:
            if occurrence["machine_location_count"] or occurrence[
                "language_coverage"
            ]["recorded_source_kinds"]:
                continue
            raw = occurrence.get("raw_occurrence") or {}
            if not isinstance(raw, dict):
                continue
            allowed = {
                "unit_id", "english_lines", "msa_lines", "classical_lines",
                "context_note", "note",
            }
            if set(raw) - allowed:
                continue
            counterparts = located.get((headword, occurrence["unit"]["unit_id"]), set())
            counterparts = {item for item in counterparts if item != decision["decision_id"]}
            if not counterparts:
                continue
            occurrence["human_review_included"] = False
            occurrence["human_review_exclusion_reason"] = (
                "Unlocated legacy identity stub superseded by an exact-headword located "
                "decision for the same unit; raw record retained in JSON."
            )
            occurrence["superseded_by_located_decision_ids"] = sorted(counterparts)
            superseded_by.update(counterparts)
        if superseded_by:
            decision["index_metadata"]["superseded_by_located_decision_ids"] = sorted(
                superseded_by
            )

    for decision in decisions:
        metadata = decision["index_metadata"]
        refresh_decision_index_counts(decision)
        if decision.get("human_superseded_by_authoritative_repair"):
            metadata["human_index_included"] = False
            metadata["human_index_exclusion_reason"] = (
                "Superseded on human-facing surfaces by authoritative current repair "
                f"evidence in {decision['human_superseded_by_authoritative_repair']}; "
                "raw decision and occurrences remain in JSON."
            )
            continue
        if (
            metadata["human_index_included"]
            and metadata["occurrences"]
            and not any(item["human_review_included"] for item in metadata["occurrences"])
            and all(
                item.get("human_review_exclusion_reason")
                for item in metadata["occurrences"]
            )
        ):
            metadata["human_index_included"] = False
            metadata["human_index_exclusion_reason"] = (
                "Every occurrence is a superseded unlocated stub; richer located "
                "decisions remain in the human index and this record remains in JSON."
            )


def render_markdown(
    payload: dict,
    arabic_prefix: str = "../../../",
    reviewer_index_href: str = "reviewer-index",
) -> str:
    summary = payload["summary"]
    reader_names = [row["name"] for row in payload["reader_evidence"]]
    lines = [
        "# Arabic terminology choices for expert review / فهرس المصطلحات العربية للمراجعة المتخصصة",
        "",
        "This is the practical review index: find an English term or sense, see the Arabic now in use and a one-sentence reason, then follow every provable occurrence to its exact current source line. File-only and ambiguous evidence is labelled instead of guessed. Each choice remains open to correction; review is welcome and never a release hold.",
        "",
        f"For normal browser review, use the small files in [`reviewer-index/`]({reviewer_index_href}/README.md). This canonical monolith is retained for preservation and bulk search.",
        "",
        '<p lang="ar" dir="rtl">هذا فهرس عملي للمراجعة: يُذكر المصطلح الإنجليزي، والصياغة العربية المستعملة، وسبب اختيارها، ثم تُسرد جميع المواضع المسجلة بروابط إلى أسطر المصدر الحالية. وكل اختيار قابل للتصحيح، ولا تتوقف مواصلة العمل أو نشره على ورود مراجعة بشرية.</p>',
        "",
        "## At a glance / خلاصة",
        "",
        f"- Recorded decisions in machine data: **{summary['recorded_decisions']}**.",
        f"- Locale terminology/adverse ledger: **{summary['locale_ledger_raw_records_preserved']}** raw records preserved; **{summary['locale_ledger_chosen_terminology_records_contributed']}** chosen terminology rows adapted; **{summary['locale_ledger_adverse_or_repair_records_machine_only']}** adverse/repair rows retained below the human term surface.",
        f"- Locale-ledger location result: **{summary['locale_ledger_resolved_source_locations']}** exact source locators, **{summary['locale_ledger_unresolved_source_locations']}** supplied file/source locators still unresolved, **{summary['locale_ledger_chosen_unit_only_occurrence_records']}** exact unit-only records, and **{summary['locale_ledger_chosen_decisions_without_named_unit']}** chosen rows with no named unit. No missing source edition, path, line or unit was inferred.",
        f"- Exact semantic duplicates merged across ledgers: **{summary['exact_semantic_duplicates_merged_across_ledgers']}** (all source provenance retained in JSON).",
        f"- Real word/term choices in this human index: **{summary['human_index_decisions']}**.",
        f"- Sortable CSV rows: **{summary['human_csv_rows']}**: one per distinct recorded occurrence plus **{summary['human_decisions_without_occurrence']}** explicit unplaced-choice rows. **{summary['duplicate_occurrence_rows_suppressed_from_csv']}** indistinguishable duplicate ledger rows remain in JSON rather than being repeated for reviewers.",
        f"- Generic passage placeholders omitted from this word index: **{summary['generic_passage_decisions_omitted']}**; their complete records remain in `EXPERT_REVIEW_INDEX.json`.",
        f"- Superseded repair snapshots or duplicate empty stubs omitted from the human index: **{summary['superseded_or_duplicate_decisions_omitted_from_human_index']}**; their raw records also remain in JSON.",
        f"- Recorded locator rows shown below: **{summary['human_location_records']}**.",
        f"- Exact current real-term source locators resolved: **{summary['real_term_resolved_source_locations']}**.",
        f"- Real-term source locators still needing repair: **{summary['real_term_unresolved_source_locations']}**.",
        f"- Unit-wide policies or proposed wording with no discrete lexical occurrence: **{summary['real_term_unit_wide_or_nonlexical_records']}**.",
        f"- Classification check: **{summary['human_location_records']} = {summary['real_term_resolved_source_locations']} exact + {summary['real_term_unresolved_source_locations']} unresolved + {summary['real_term_unit_wide_or_nonlexical_records']} unit-wide/non-lexical**.",
        f"- Generic-placeholder unresolved locators kept only in machine data: **{summary['generic_placeholder_unresolved_source_locations']}**.",
        f"- Choices explicitly marked as especially useful for expert review: **{summary['expert_review_requested']}**.",
        "",
        "## Reading page evidence / كيفية قراءة الصفحات",
        "",
        "- **Exact SyncTeX** means the final reader's SyncTeX map directly associates that exact current source line with the listed 1-based PDF page. The printed-page label comes from that PDF's own page-label tree when available.",
        "- **Unit-start fallback** means the page is only the beginning of the containing Open Logic unit, proved by its AUX label and PDF named destination. It is deliberately labelled *not* the exact term page.",
        "- No page number is estimated from offsets. Missing evidence stays visibly unavailable.",
        "- Source codes: **EN / الإنجليزية** = pinned English; **MSA / المعيارية** = shared international/Machrek Arabic source; **CA / التراثية** = Classical Arabic source.",
    ]
    if reader_names:
        lines.append("- Final-reader evidence loaded: " + ", ".join(md_text(name) for name in reader_names) + ".")
    else:
        lines.append("- No final-reader PDF/AUX/SyncTeX set was supplied for this snapshot; source links are usable now and page fields remain unclaimed until the final build is passed to the generator.")

    included = [row for row in payload["decisions"] if row["index_metadata"]["human_index_included"]]
    requested = [row for row in included if row.get("expert_review_useful") is True]
    optional = [row for row in included if row.get("expert_review_useful") is not True]

    link_registry = make_link_registry(included, arabic_prefix=arabic_prefix)
    lines += [
        "",
        "## Quick term index / فهرس سريع",
        "",
        "| English term / المصطلح | Arabic in use / العربية المستعملة | Review | Locations |",
        "| --- | --- | --- | ---: |",
    ]
    for decision in requested + optional:
        anchor = "decision-" + re.sub(r"[^a-z0-9-]+", "-", decision["decision_id"].casefold()).strip("-")
        priority = "Please check / يُرجى التحقق" if decision.get("expert_review_useful") is True else "Open / قابل للتصحيح"
        lines.append(
            f"| [{md_text(human_english_term(decision))}](#{anchor}) | {rtl(human_chosen_arabic(decision))} | {priority} | {decision['index_metadata']['location_count']} |"
        )

    def append_section(title: str, rows: list[dict]) -> None:
        lines.extend(["", f"## {title}", ""])
        for decision in rows:
            anchor = "decision-" + re.sub(r"[^a-z0-9-]+", "-", decision["decision_id"].casefold()).strip("-")
            lines.extend(
                [
                    f'<a id="{anchor}"></a>',
                    f"### {md_text(human_english_term(decision))} — {rtl(human_chosen_arabic(decision))}",
                    "",
                    f"- **ID / الرقم:** `{md_text(decision['decision_id'])}`",
                    f"- **Edition / النسخة:** {md_text(human_decision_field(decision, 'edition') or 'not recorded')}",
                    f"- **Sense / المعنى:** {md_text(human_decision_field(decision, 'sense') or 'No separate sense note recorded / لم يسجل بيان مستقل للمعنى')}",
                    f"- **Why this choice / سبب الاختيار:** {md_text(human_decision_field(decision, 'rationale'))}",
                ]
            )
            append_assessment_provenance(lines, decision, arabic_prefix)
            alternatives = alternatives_text(decision)
            if alternatives:
                lines.append("- **Alternatives / البدائل:**")
                lines.extend(f"  - {md_text(item)}" for item in alternatives)
            else:
                lines.append("- **Alternatives / البدائل:** none recorded / لم يُسجّل بديل.")
            lines.extend([
                f"- **Please double-check / يُرجى التحقق:** {md_text(review_question(decision))}",
            ])
            occurrences = human_occurrence_rows(decision)
            if not occurrences:
                if human_global_source_rows(decision):
                    append_global_source_markdown(
                        lines, decision, link_registry, arabic_prefix, indent="  "
                    )
                else:
                    lines.append("  - **No exact occurrence record is present in the source ledger; this gap needs repair. / لا يوجد موضع دقيق في السجل المصدر.**")
                    lines.extend(
                        "    - ⚠ " + md_text(item)
                        for item in unresolved_decision_locator_lines(decision)
                    )
            for occurrence in grouped_human_occurrence_rows(decision):
                unit = occurrence["unit"]
                locations = occurrence["locations"]
                lines.append(
                    f"  - **{md_text(unit['unit_id'])} — {md_text(unit['title'])}**"
                )
                if occurrence["occurrence_record_count"] > 1:
                    lines.append(
                        "    - Grouped here: "
                        f"{occurrence['occurrence_record_count']} recorded occurrence records; "
                        "every distinct source locator is listed below."
                    )
                for missing_note in occurrence["missing_language_notes"]:
                    if locations:
                        lines.append(f"    - {md_text(missing_note)}")
                if not locations:
                    for note in occurrence["locationless_notes"] or [""]:
                        lines.append(
                            "    - **No discrete source occurrence supplied / لم يُسجّل موضع نصي منفصل.**"
                            + (" " + md_text(note) if note else "")
                        )
                lines.extend(
                    location_lines_markdown(
                        locations,
                        bool(reader_names),
                        link_registry,
                        arabic_prefix=arabic_prefix,
                    )
                )
            if occurrences and human_global_source_rows(decision):
                append_global_source_markdown(
                    lines, decision, link_registry, arabic_prefix, indent="  "
                )
            append_unresolved_component_markdown(lines, decision, indent="  ")
            lines.append("")

    append_section("Please double-check these choices / اختيارات يُرجى تدقيقها", requested)
    append_section("Other recorded choices, also open to correction / اختيارات أخرى قابلة للتصحيح", optional)
    lines += [
        "## Machine-readable companion / السجل المقروء آليًا",
        "",
        "`EXPERT_REVIEW_INDEX.json` contains every decision, including the generic passage records omitted above, every original occurrence record, current file hashes, reconciliation outcomes, page-evidence methods and input-ledger identities.",
        "",
    ]
    if link_registry.references:
        lines += ["<!-- Compact repeated source-link definitions -->", ""]
        lines.extend(link_registry.definitions())
        lines.append("")
    return "\n".join(lines)


def render_priority_markdown(
    payload: dict,
    arabic_prefix: str = "../../../",
    reviewer_index_href: str = "reviewer-index",
) -> str:
    """Render the exhaustive worksheet containing all explicit review flags."""

    requested = [
        row for row in payload["decisions"]
        if row["index_metadata"]["human_index_included"]
        and row.get("expert_review_useful") is True
    ]
    reader_names = [row["name"] for row in payload["reader_evidence"]]
    link_registry = make_link_registry(requested, arabic_prefix=arabic_prefix)
    lines = [
        "# Priority terminology review sheet / ورقة أولوية لمراجعة المصطلحات",
        "",
        f"This exhaustive bulk sheet contains every recorded word choice explicitly marked as useful for expert attention. It is not a curated short list: ordinary lexical fragments can appear when an intake ledger flagged them. Start with `EXPERT_REVIEW_START_HERE.md`, then use the small browser-friendly files in [`reviewer-index/`]({reviewer_index_href}/README.md); this canonical monolith remains available for preservation and bulk search. Every choice remains provisional; feedback can improve a later revision and is not a publication hold.",
        "",
        '<p lang="ar" dir="rtl">لا تشتمل هذه الورقة الموجزة إلا على الاختيارات المصطلحية التي وُسِمت صراحةً بأنها أولى بالمراجعة المتخصصة. وكل اختيار فيها مؤقت وقابل للتصحيح، ولا تتوقف مواصلة العمل أو نشره على ورود المراجعة.</p>',
        "",
        f"**Priority choices / الاختيارات ذات الأولوية:** {len(requested)}",
        f"**Recorded priority occurrences / مواضع الأولوية المسجلة:** {payload['summary']['expert_review_occurrence_records']}",
        "",
        "Page evidence is never guessed: **Exact SyncTeX** is an exact occurrence page; **unit-start fallback** is only the proved beginning of the unit and is not the term's exact page.",
        "",
    ]
    if reader_names:
        lines.append(
            "Final-reader evidence loaded / أدلة القارئ النهائي: "
            + ", ".join(md_text(name) for name in reader_names)
            + "."
        )
    else:
        lines.append(
            "No final-reader evidence was supplied for this snapshot; PDF-page fields remain unclaimed / لم تُزوَّد هذه النسخة بأدلة القارئ النهائي، ولذلك لا يُدّعى فيها رقم صفحة PDF."
        )

    lines += [
        "",
        "## Quick review index / فهرس المراجعة السريع",
        "",
        "| ID | English term / المصطلح | Arabic in use / العربية المستعملة | Recorded occurrence groups |",
        "| --- | --- | --- | ---: |",
    ]
    for decision in requested:
        anchor = "priority-" + re.sub(
            r"[^a-z0-9-]+", "-", decision["decision_id"].casefold()
        ).strip("-")
        lines.append(
            f"| `{md_text(decision['decision_id'])}` | [{md_text(human_english_term(decision))}](#{anchor}) | "
            f"{rtl(human_chosen_arabic(decision))} | {decision['index_metadata']['occurrence_group_count']} |"
        )

    for decision in requested:
        anchor = "priority-" + re.sub(
            r"[^a-z0-9-]+", "-", decision["decision_id"].casefold()
        ).strip("-")
        lines.extend(
            [
                "",
                f'<a id="{anchor}"></a>',
                f"## {md_text(human_english_term(decision))} — {rtl(human_chosen_arabic(decision))}",
                "",
                f"- **ID / الرقم:** `{md_text(decision['decision_id'])}`",
                f"- **Sense / المعنى:** {md_text(human_decision_field(decision, 'sense') or 'No separate sense note recorded / لم يسجل بيان مستقل للمعنى')}",
                f"- **Edition / النسخة:** {md_text(human_decision_field(decision, 'edition') or 'not recorded')}",
                f"- **Why this choice / سبب الاختيار:** {md_text(human_decision_field(decision, 'rationale'))}",
            ]
        )
        append_assessment_provenance(lines, decision, arabic_prefix)
        alternatives = alternatives_text(decision)
        if alternatives:
            lines.append(
                "- **Alternatives / البدائل:** "
                + "; ".join(md_text(item) for item in alternatives)
            )
        else:
            lines.append("- **Alternatives / البدائل:** none recorded / لم يُسجّل بديل.")
        lines.append(
            f"- **Please double-check / يُرجى التحقق:** {md_text(review_question(decision))}"
        )
        occurrences = distinct_human_occurrence_rows(decision)
        if not occurrences:
            if human_global_source_rows(decision):
                append_global_source_markdown(
                    lines, decision, link_registry, arabic_prefix
                )
            else:
                lines.append(
                    "- ⚠ **No exact occurrence record is present / لا يوجد موضع دقيق في السجل.**"
                )
                lines.extend(
                    "  - ⚠ " + md_text(item)
                    for item in unresolved_decision_locator_lines(decision)
                )
        for occurrence in grouped_human_occurrence_rows(decision):
            unit = occurrence["unit"]
            locations = occurrence["locations"]
            lines.append(f"- **{md_text(unit['unit_id'])} — {md_text(unit['title'])}**")
            if occurrence["occurrence_record_count"] > 1:
                lines.append(
                    "  - Grouped here: "
                    f"{occurrence['occurrence_record_count']} recorded occurrence records; "
                    "every distinct source locator is listed below."
                )
            for missing_note in occurrence["missing_language_notes"]:
                if locations:
                    lines.append(f"  - {md_text(missing_note)}")
            if not locations:
                for note in occurrence["locationless_notes"] or [""]:
                    lines.append(
                        "  - ℹ **No discrete source occurrence supplied / لم يُسجّل موضع نصي منفصل.**"
                        + (" " + md_text(note) if note else "")
                    )
            lines.extend(
                location_lines_markdown(
                    locations,
                    bool(reader_names),
                    link_registry,
                    arabic_prefix=arabic_prefix,
                )
            )
        if occurrences and human_global_source_rows(decision):
            append_global_source_markdown(
                lines, decision, link_registry, arabic_prefix
            )
        append_unresolved_component_markdown(lines, decision)

    lines += [
        "",
        "Full context and non-priority choices are in `EXPERT_REVIEW_INDEX.md`; the sortable occurrence table is `EXPERT_REVIEW_OCCURRENCES.csv`.",
        "",
    ]
    if link_registry.references:
        lines += ["<!-- Compact repeated source-link definitions -->", ""]
        lines.extend(link_registry.definitions())
        lines.append("")
    return "\n".join(lines)


BULK_FRAGMENT_TERMS = {
    "all", "any", "are", "as", "be", "can", "does", "each", "every",
    "for", "from", "has", "if", "in", "is", "may", "not", "of", "on",
    "or", "some", "that", "the", "then", "to", "with",
}

# Ordinary prose fragments can be honestly retained in the exhaustive archive
# without occupying the default expert's first screen.  This is deliberately a
# small, explicit list; it never deletes a ledger record.
ROUTINE_START_HERE_TERMS = BULK_FRAGMENT_TERMS | {
    "basics", "both", "compiled", "construct", "constructed", "decode",
    "defined", "definitions", "deny", "difficult", "do", "doing",
    "driver file", "first, geometrically", "forget about", "help ourselves",
    "if it exists", "initial", "introduction", "invoke", "many times",
    "may not yet be complete", "meant", "more", "no", "odd", "ought",
    "perfectly general", "quite", "really", "require", "second, formally.",
    "specify", "treat", "turned out", "useful", "what", "wrong", "yet",
}

START_HERE_CHECK_FIRST_COUNT = 12
START_HERE_CHECK_FIRST_REPAIR_QUOTA = 4


def confidence_level(decision: dict) -> str:
    confidence = decision.get("confidence")
    if isinstance(confidence, dict):
        return collapse(confidence.get("level")).casefold()
    return collapse(confidence).casefold()


def human_unresolved_statuses(decision: dict) -> list[str]:
    statuses = []
    for occurrence in human_occurrence_rows(decision):
        for location in human_location_rows(occurrence):
            status = str(location["line_reconciliation"]["status"])
            if not resolved_reconciliation_status(status) and not non_locator_reconciliation_status(status):
                statuses.append(status)
    return statuses


def authority_gap_kind(decision: dict) -> str | None:
    evidence = json.dumps(
        {
            "basis": decision.get("basis"),
            "authority_checks": decision.get("authority_checks"),
            "authority_status": decision.get("authority_status"),
            "expert_review_reason": decision.get("expert_review_reason"),
        },
        ensure_ascii=False,
        sort_keys=True,
    ).casefold()
    if "not-found-in-checked-sources" in evidence or "no official-dictionary" in evidence or "no official dictionary" in evidence:
        return "not found in checked authority sources"
    if "not-checked" in evidence or "unperformed" in evidence:
        return "authority check not performed"
    return None


def explicit_hazard(decision: dict) -> bool:
    text = " ".join(
        collapse(decision.get(field)).casefold()
        for field in (
            "english_term", "sense", "rationale", "expert_review_reason",
            "expert_question", "expert_review_question",
        )
    )
    return any(
        marker in text
        for marker in (
            "ambig", "coinage", "coined", "conflict", "distinguish", "eponym",
            "false friend", "hazard", "inconsisten", "nonce", "polysem",
            "regional", "register", "terminological",
        )
    )


def source_repair_signal(decision: dict) -> bool:
    decision_id = collapse(decision.get("decision_id")).casefold()
    if decision_id.startswith(("repair-", "repair_", "repair:")):
        return True
    records = decision.get("source_records") or [decision.get("source_record")]
    return any(
        isinstance(record, dict)
        and "/repairs/" in ("/" + collapse(record.get("path")).replace("\\", "/")).casefold()
        for record in records
    )


def start_here_candidate(row: dict) -> bool:
    """Keep the default queue technical/actionable; archive everything else."""

    decision = row["decision"]
    headword = normalized_review_headword(human_english_term(decision)).strip(" .:;,")
    if headword in ROUTINE_START_HERE_TERMS:
        return False
    strong = (
        source_repair_signal(decision)
        or authority_gap_kind(decision) is not None
        or bool(human_unresolved_statuses(decision))
        or "same headword has conflicting Arabic choices" in row.get("reasons", [])
        or explicit_hazard(decision)
        or "ai-proposed" in collapse(decision.get("basis")).casefold()
        or "contextual-extension" in collapse(decision.get("basis")).casefold()
    )
    # Auto-mined emphasis/heading fragments whose only signal is a low
    # confidence flag remain searchable in the exhaustive archive.
    auto_surface = any(
        marker in collapse(decision.get("decision_id")).casefold()
        for marker in (":emphasis:", ":section:", ":chapter:")
    )
    return strong and not (auto_surface and row["issue"] == "Low-confidence terminology")


def review_risk_rows(payload: dict) -> list[dict]:
    requested = [
        row for row in payload["decisions"]
        if row["index_metadata"]["human_index_included"]
        and row.get("expert_review_useful") is True
    ]
    forms_by_headword: dict[str, set[str]] = defaultdict(set)
    for decision in requested:
        forms_by_headword[normalized_review_headword(human_english_term(decision))].add(
            normalized_review_headword(human_chosen_arabic(decision))
        )

    ranked = []
    for decision in requested:
        score = 0
        reasons = []
        confidence = confidence_level(decision)
        if confidence == "low":
            score += 50
            reasons.append("low confidence")
        elif confidence == "medium":
            score += 18
            reasons.append("medium confidence")
        elif not confidence:
            score += 12
            reasons.append("confidence not recorded")

        gap = authority_gap_kind(decision)
        if gap:
            score += 35 if gap.startswith("not found") else 30
            reasons.append(gap)

        headword = normalized_review_headword(human_english_term(decision))
        cross_choice = len(forms_by_headword[headword]) > 1
        if cross_choice:
            score += 32
            reasons.append("same headword has conflicting Arabic choices")

        unresolved = human_unresolved_statuses(decision)
        if unresolved:
            score += 25 + min(15, len(unresolved))
            reasons.append(f"{len(unresolved)} unresolved exact locator(s)")
            if any("ambiguous" in status for status in unresolved):
                score += 10
                reasons.append("ambiguous exact candidates")

        if explicit_hazard(decision):
            score += 20
            reasons.append("explicit terminology hazard")

        repair_choice = source_repair_signal(decision)
        if repair_choice:
            score += 30
            reasons.append("translation/source repair choice")

        basis = collapse(decision.get("basis")).casefold()
        if "ai-proposed" in basis:
            score += 22
            reasons.append("AI-proposed wording")
        elif "inherited-unverified" in basis:
            score += 12
            reasons.append("inherited but unverified")
        elif "contextual-extension" in basis:
            score += 7
            reasons.append("contextual extension")

        if headword in BULK_FRAGMENT_TERMS:
            score -= 80
            reasons.append("bulk lexical fragment; deprioritized")

        if repair_choice:
            issue = "Translation/source repair choice"
        elif unresolved:
            issue = "Exact locator repair"
        elif cross_choice:
            issue = "Conflicting Arabic choices"
        elif gap:
            issue = "Authority gap"
        elif confidence == "low":
            issue = "Low-confidence terminology"
        elif explicit_hazard(decision):
            issue = "Terminology or register hazard"
        else:
            issue = "Other recorded expert priority"
        ranked.append(
            {
                "decision": decision,
                "score": score,
                "issue": issue,
                "reasons": reasons,
            }
        )
    return sorted(
        ranked,
        key=lambda row: (
            -row["score"],
            human_english_term(row["decision"]).casefold(),
            row["decision"]["decision_id"],
        ),
    )


def shorten_words(value: object, limit: int) -> str:
    text = human_prose(value)
    if len(text) <= limit:
        return text
    cut = text.rfind(" ", 0, limit - 1)
    if cut < max(20, limit // 2):
        cut = limit - 1
    return text[:cut].rstrip(" ,.;:؛،") + "…"


def markdown_cell(value: object) -> str:
    return md_text(value).replace("|", "&#124;")


def start_here_where(
    decision: dict,
    detail_href: str,
    arabic_prefix: str = "../../../",
) -> str:
    """Give the queue one concrete locator without replacing full detail."""

    exact = []
    unresolved = []
    nonlocators = []
    global_exact = [
        location for location in human_global_source_rows(decision)
        if location["line_reconciliation"]["resolved"]
    ]
    source_location_count = 0
    locationless_occurrence_count = 0
    for occurrence in human_occurrence_rows(decision):
        unit = occurrence["unit"]
        locations = human_location_rows(occurrence)
        source_location_count += len(locations)
        if not locations:
            locationless_occurrence_count += 1
        for location in locations:
            reconciliation = location["line_reconciliation"]
            if reconciliation["resolved"]:
                exact.append((unit, location))
            elif non_locator_reconciliation_status(reconciliation["status"]):
                nonlocators.append((unit, location))
            else:
                unresolved.append((unit, location))
    edition = human_decision_field(decision, "edition") or "edition not recorded"

    edition_key = edition.casefold()
    classical_first = (
        edition_key.startswith("classical")
        or "classical arabic" in edition_key
        or "classical repair" in edition_key
    )
    source_order = (
        {"classical": 0, "msa": 1, "english": 2}
        if classical_first else
        {"msa": 0, "classical": 1, "english": 2}
    )

    def exact_sort_key(item: tuple[dict, dict]) -> tuple:
        unit, location = item
        has_exact_page = any(
            page.get("method") == "synctex-exact"
            and (page.get("assembled_pdf_pages") or page.get("pdf_pages"))
            for page in location.get("page_evidence") or []
        )
        reconciliation = location["line_reconciliation"]
        return (
            0 if has_exact_page else 1,
            source_order.get(location["source_kind"], 9),
            unit["unit_id"],
            reconciliation["current_line_start"],
            reconciliation["current_line_end"],
        )

    exact.sort(key=exact_sort_key)
    global_exact.sort(
        key=lambda location: (
            source_order.get(location["source_kind"], 9),
            collapse(location.get("logical_path") or location.get("recorded_path")),
            location["line_reconciliation"]["current_line_start"],
            location["line_reconciliation"]["current_line_end"],
        )
    )

    def unit_label(unit: dict) -> str:
        title = shorten_words(unit.get("title"), 58)
        return markdown_cell(
            unit["unit_id"] + (f" — {title}" if title else "")
        )

    if exact:
        unit, location = exact[0]
        reconciliation = location["line_reconciliation"]
        start = reconciliation["current_line_start"]
        end = reconciliation["current_line_end"]
        label = f"L{start}" if start == end else f"L{start}–L{end}"
        source = SOURCE_LABELS.get(location["source_kind"], location["source_kind"])
        rendered = (
            f"{unit_label(unit)} · {md_text(edition)} · {source} · "
            f"[{label}]({markdown_source_href(location, exact_line=True, arabic_prefix=arabic_prefix)})"
        )
        exact_page_facts = []
        for page in location.get("page_evidence") or []:
            if page.get("method") == "synctex-exact":
                pdf_pages = page.get("assembled_pdf_pages") or page.get("pdf_pages") or []
                if pdf_pages:
                    reader = collapse(page.get("reader")) or "final reader"
                    fact = (
                        f"{md_text(reader)} final PDF "
                        + ", ".join(map(str, pdf_pages))
                    )
                    if fact not in exact_page_facts:
                        exact_page_facts.append(fact)
        if exact_page_facts:
            rendered += " · " + " · ".join(exact_page_facts)
        more = source_location_count - 1
        if more > 0:
            rendered += f" · [+{more} more source locations]({detail_href})"
        if locationless_occurrence_count:
            rendered += (
                f" · [+{locationless_occurrence_count} unit-only/unplaced "
                f"record{'s' if locationless_occurrence_count != 1 else ''}]({detail_href})"
            )
        return rendered
    if global_exact:
        location = global_exact[0]
        reconciliation = location["line_reconciliation"]
        start = reconciliation["current_line_start"]
        end = reconciliation["current_line_end"]
        label = f"L{start}" if start == end else f"L{start}–L{end}"
        source = SOURCE_LABELS.get(location["source_kind"], location["source_kind"])
        rendered = (
            "Global/front matter; no OLP unit / مصدر عام أو صفحات تمهيدية؛ بلا وحدة OLP"
            f" · {md_text(edition)} · {source} · "
            f"[{label}]({markdown_source_href(location, exact_line=True, arabic_prefix=arabic_prefix)})"
        )
        if len(global_exact) > 1:
            rendered += f" · [+{len(global_exact) - 1} more global source locations]({detail_href})"
        return rendered
    if unresolved:
        unit, location = unresolved[0]
        source = SOURCE_LABELS.get(location["source_kind"], location["source_kind"])
        status = location["line_reconciliation"]["status"]
        more = source_location_count - 1
        suffix = f"; +{more} more source locations" if more else ""
        return (
            f"⚠ {unit_label(unit)} · {md_text(edition)} · {source} · "
            f"no proved exact line ({md_text(status)}{suffix}); "
            f"[details]({detail_href})"
        )
    if nonlocators:
        unit, location = nonlocators[0]
        source = SOURCE_LABELS.get(location["source_kind"], location["source_kind"])
        more = source_location_count - 1
        suffix = f"; +{more} more source locations" if more else ""
        return (
            f"ℹ {unit_label(unit)} · {md_text(edition)} · {source} · "
            f"unit-wide/no discrete lexical occurrence ({md_text(location['line_reconciliation']['status'])}{suffix}); "
            f"[details]({detail_href})"
        )
    occurrences = human_occurrence_rows(decision)
    if occurrences:
        first = occurrences[0]["unit"]
        more = max(0, locationless_occurrence_count - 1)
        suffix = f"; +{more} more unit-only/unplaced records" if more else ""
        note = locationless_occurrence_note(occurrences[0])
        missing = (
            shorten_words(note, 95)
            if note else
            "unit is known; source edition/path/line are not proved"
        )
        return (
            f"⚠ {unit_label(first)} · {md_text(edition)}{suffix} · "
            f"{md_text(missing)}; "
            f"[details]({detail_href})"
        )
    unresolved_evidence = unresolved_decision_locator_lines(decision)
    if unresolved_evidence:
        return (
            "⚠ " + md_text(shorten_words(unresolved_evidence[0], 130))
            + f"; [details]({detail_href})"
        )
    return f"⚠ no exact occurrence recorded; [details]({detail_href})"


def render_start_here_markdown(
    payload: dict,
    limit: int,
    priority_href_by_id: dict[str, str] | None = None,
    arabic_prefix: str = "../../../",
    reviewer_index_href: str = "reviewer-index",
) -> str:
    """Render a bounded, deterministic, risk-ranked reviewer queue."""

    ranked = review_risk_rows(payload)
    curated = [row for row in ranked if start_here_candidate(row)]
    check_first_count = min(START_HERE_CHECK_FIRST_COUNT, limit, len(curated))
    repair_quota = min(
        START_HERE_CHECK_FIRST_REPAIR_QUOTA,
        check_first_count // 3,
        sum(source_repair_signal(row["decision"]) for row in curated),
    )
    ordinary_quota = check_first_count - repair_quota
    check_first = list(curated[:ordinary_quota])
    selected_ids = {row["decision"]["decision_id"] for row in check_first}
    for row in curated:
        if len(check_first) >= check_first_count:
            break
        if (
            source_repair_signal(row["decision"])
            and row["decision"]["decision_id"] not in selected_ids
        ):
            check_first.append(row)
            selected_ids.add(row["decision"]["decision_id"])
    for row in curated:
        if len(check_first) >= check_first_count:
            break
        if row["decision"]["decision_id"] not in selected_ids:
            check_first.append(row)
            selected_ids.add(row["decision"]["decision_id"])
    specialists = []
    for row in curated:
        if len(check_first) + len(specialists) >= limit:
            break
        if row["decision"]["decision_id"] not in selected_ids:
            specialists.append(row)
            selected_ids.add(row["decision"]["decision_id"])
    selected = check_first + specialists
    tiers = [
        (
            "Tier 1 — Check first / المستوى الأول — ابدأ بهذه",
            check_first,
            "The most consequential conflicts, repair choices, authority gaps and unresolved exact locators.",
        ),
        (
            "Tier 2 — Specialist review / المستوى الثاني — مراجعة متخصصة",
            specialists,
            "The next technical choices worth specialist attention after Tier 1.",
        ),
    ]
    lines = [
        "# Start here: technical choices to double-check / ابدأ هنا: مصطلحات تقنية يُرجى تدقيقها",
        "",
        f"This is the short human queue: **{len(selected)}** genuinely technical or repair-related choices selected from **{len(ranked)}** ledger flags. Routine auto-mined prose stays in the exhaustive archive instead of filling this first screen. Each term links to every distinct recorded occurrence.",
        "",
        '<p lang="ar" dir="rtl">هذه قائمة قصيرة للمراجعة البشرية، لا تعرض في بدايتها إلا المصطلحات التقنية أو اختيارات الإصلاح الجديرة بالتدقيق. أما المواد الآلية الاعتيادية فتبقى محفوظة في الفهرس الكامل، ولا يُحذف منها شيء.</p>',
        "",
        "## Three review tiers / ثلاثة مستويات للمراجعة",
        "",
        f"1. **Check first:** **{len(check_first)}** choices: the highest-scoring technical conflicts plus up to **{repair_quota}** explicit translation/source-repair choices.",
        f"2. **Specialist review:** the next **{len(specialists)}** technical choices below.",
        f"3. **Exhaustive archive:** all **{len(ranked)}** flagged choices remain in the browser shards, monolithic sheet, CSV and JSON.",
        "",
        "The deterministic score uses confidence, authority evidence, conflicting Arabic forms, exact-locator quality, explicit terminology hazards, AI-proposed/inherited wording and translation/source repairs. Occurrence frequency is **not** a promotion signal. Ties use the displayed English term and stable decision ID.",
        "",
        f"Short-queue cap / الحد الأقصى للقائمة القصيرة: **{limit}**. Technical candidates before the cap: **{len(curated)}**.",
    ]
    rank_lookup = {row["decision"]["decision_id"]: index for index, row in enumerate(selected, 1)}
    for title, rows, note in tiers:
        if not rows:
            continue
        lines += [
            "",
            f"## {title}",
            "",
            note,
            "",
            "| Rank / score | Term / المصطلح | Arabic in use / العربية | Why; what to check / السبب وما ينبغي تدقيقه | First exact place, then +N / أول موضع دقيق ثم البقية |",
            "| ---: | --- | --- | --- | --- |",
        ]
        for row in rows:
            decision = row["decision"]
            anchor = "priority-" + re.sub(
                r"[^a-z0-9-]+", "-", decision["decision_id"].casefold()
            ).strip("-")
            href = (priority_href_by_id or {}).get(
                decision["decision_id"],
                "EXPERT_REVIEW_PRIORITY_ONLY.md#" + anchor,
            )
            why = shorten_words(human_decision_field(decision, "rationale"), 105)
            question = shorten_words(review_question(decision), 115)
            detail = f"{row['issue']}. Why: {why} Check: {question}"
            lines.append(
                f"| #{rank_lookup[decision['decision_id']]} / {row['score']} | "
                f"[{markdown_cell(human_english_term(decision))}]({href})<br>`{markdown_cell(decision['decision_id'])}` | "
                f"{rtl(human_chosen_arabic(decision))} | {markdown_cell(detail)} | "
                f"{start_here_where(decision, href, arabic_prefix=arabic_prefix)} |"
            )
    lines += [
        "",
        f"Continue with Tier 3 in the [browser-friendly shard index]({reviewer_index_href}/README.md). The canonical `EXPERT_REVIEW_PRIORITY_ONLY.md` retains every flagged choice in one large archival sheet, and `EXPERT_REVIEW_OCCURRENCES.csv` supports sorting and assignment.",
        "",
    ]
    return "\n".join(lines)


# These are caps, not promises that every shard reaches the cap.  A second
# deterministic byte budget keeps unusually location-rich decisions from
# creating multi-megabyte files that GitHub declines to render.
PRIORITY_SHARD_SIZE = 10
COMPLETE_SHARD_SIZE = 15
REVIEWER_SHARD_TARGET_BYTES = 180 * 1024
REVIEWER_SHARD_HARD_LIMIT_BYTES = 225 * 1024
REVIEWER_SHARD_ESTIMATED_OVERHEAD_BYTES = 8 * 1024


def decision_anchor(decision: dict, prefix: str) -> str:
    slug = re.sub(
        r"[^a-z0-9-]+", "-", decision["decision_id"].casefold()
    ).strip("-")
    digest = hashlib.sha256(decision["decision_id"].encode("utf-8")).hexdigest()[:10]
    return prefix + (slug[:96] or "choice") + "-" + digest


def chunked(rows: Sequence[dict], size: int) -> list[list[dict]]:
    return [list(rows[index:index + size]) for index in range(0, len(rows), size)]


def estimate_review_decision_bytes(decision: dict, priority: bool) -> int:
    """Conservatively estimate one rendered decision with inline source URLs."""

    lines: list[str] = []
    # A zero-count registry always emits inline URLs.  Group rendering can
    # replace repeated URLs with shorter reference links, so this is normally
    # an upper bound for the decision body.
    append_shard_decision(
        lines,
        decision,
        "priority-" if priority else "decision-",
        readers_present=False,
        link_registry=LinkRegistry(Counter()),
        arabic_prefix="../../../../",
        priority_rank=(9999, 999) if priority else None,
    )
    return len(("\n".join(lines) + "\n").encode("utf-8"))


def partition_reviewer_rows(
    rows: Sequence[dict], max_choices: int, priority: bool
) -> list[list[dict]]:
    """Greedily partition in stable order by both choice count and byte weight."""

    groups: list[list[dict]] = []
    current: list[dict] = []
    current_bytes = REVIEWER_SHARD_ESTIMATED_OVERHEAD_BYTES
    for decision in rows:
        weight = estimate_review_decision_bytes(decision, priority)
        if weight + REVIEWER_SHARD_ESTIMATED_OVERHEAD_BYTES > REVIEWER_SHARD_HARD_LIMIT_BYTES:
            raise RuntimeError(
                "one terminology decision cannot fit in a browser-renderable shard: "
                f"{decision['decision_id']} ({weight} estimated bytes)"
            )
        if current and (
            len(current) >= max_choices
            or current_bytes + weight > REVIEWER_SHARD_TARGET_BYTES
        ):
            groups.append(current)
            current = []
            current_bytes = REVIEWER_SHARD_ESTIMATED_OVERHEAD_BYTES
        current.append(decision)
        current_bytes += weight
    if current:
        groups.append(current)
    return groups


def reviewer_shard_groups(payload: dict) -> dict[str, list[list[dict]]]:
    priority_rows = [row["decision"] for row in review_risk_rows(payload)]
    complete_rows = sorted(
        (
            row for row in payload["decisions"]
            if row["index_metadata"]["human_index_included"]
        ),
        key=lambda row: (
            human_english_term(row).casefold(), row["decision_id"]
        ),
    )
    return {
        "priority": partition_reviewer_rows(
            priority_rows, PRIORITY_SHARD_SIZE, priority=True
        ),
        "complete": partition_reviewer_rows(
            complete_rows, COMPLETE_SHARD_SIZE, priority=False
        ),
    }


def priority_shard_href_map(
    payload: dict,
    shard_size: int = PRIORITY_SHARD_SIZE,
    reviewer_index_href: str = "reviewer-index",
    groups: Sequence[Sequence[dict]] | None = None,
) -> dict[str, str]:
    # ``shard_size`` remains a supported test/embedding override.  Normal
    # generation passes the exact byte-budgeted groups used to render files.
    rows = [row["decision"] for row in review_risk_rows(payload)]
    selected_groups = (
        [list(group) for group in groups]
        if groups is not None else
        partition_reviewer_rows(rows, shard_size, priority=True)
    )
    result = {}
    for index, group in enumerate(selected_groups, 1):
        filename = f"{reviewer_index_href}/priority-{index:03d}.md"
        for decision in group:
            result[decision["decision_id"]] = (
                filename + "#" + decision_anchor(decision, "priority-")
            )
    return result


def shard_navigation(
    previous_name: str | None, next_name: str | None
) -> str:
    parts = []
    if previous_name:
        parts.append(f"[← Previous / السابق]({previous_name})")
    parts.append("[Shard index / فهرس الأجزاء](README.md)")
    if next_name:
        parts.append(f"[Next / التالي →]({next_name})")
    return " · ".join(parts)


def append_shard_decision(
    lines: list[str],
    decision: dict,
    prefix: str,
    readers_present: bool,
    link_registry: LinkRegistry,
    arabic_prefix: str,
    priority_rank: tuple[int, int] | None = None,
) -> None:
    anchor = decision_anchor(decision, prefix)
    lines += [
        "",
        f'<a id="{anchor}"></a>',
        f"## {md_text(human_english_term(decision))} — {rtl(human_chosen_arabic(decision))}",
        "",
        f"- **ID / الرقم:** `{md_text(decision['decision_id'])}`",
        f"- **Sense / المعنى:** {md_text(human_decision_field(decision, 'sense') or 'No separate sense note recorded / لم يسجل بيان مستقل للمعنى')}",
        f"- **Why this choice / سبب الاختيار:** {md_text(human_decision_field(decision, 'rationale'))}",
    ]
    if priority_rank:
        lines.insert(
            len(lines) - 2,
            f"- **Global priority rank / score:** #{priority_rank[0]} / {priority_rank[1]}",
        )
    append_assessment_provenance(lines, decision, arabic_prefix)
    alternatives = alternatives_text(decision)
    if alternatives:
        lines.append(
            "- **Useful alternatives / البدائل المفيدة:** "
            + "; ".join(md_text(item) for item in alternatives)
        )
    lines += [
        f"> ⚑ **PLEASE DOUBLE-CHECK THIS CHOICE / يُرجى التحقق من هذا الاختيار:** {md_text(review_question(decision))}",
        "",
        "- **Where first / أول موضع:** "
        + start_here_where(
            decision, "#" + anchor, arabic_prefix=arabic_prefix
        ),
        "- **Every distinct recorded occurrence / كل موضع مسجل متميز:**",
    ]
    occurrences = human_occurrence_rows(decision)
    if not occurrences:
        if human_global_source_rows(decision):
            append_global_source_markdown(
                lines, decision, link_registry, arabic_prefix, indent="  "
            )
        else:
            lines.append(
                "  - ⚠ No exact occurrence record is present / لا يوجد موضع دقيق مسجل."
            )
            lines.extend(
                "    - ⚠ " + md_text(item)
                for item in unresolved_decision_locator_lines(decision)
            )
    for occurrence in grouped_human_occurrence_rows(decision):
        unit = occurrence["unit"]
        locations = occurrence["locations"]
        lines.append(
            f"  - **{md_text(unit['unit_id'])} — {md_text(unit['title'])}**"
        )
        if occurrence["occurrence_record_count"] > 1:
            lines.append(
                "    - Grouped here: "
                f"{occurrence['occurrence_record_count']} recorded occurrence records; "
                "every distinct source locator is listed below."
            )
        for missing_note in occurrence["missing_language_notes"]:
            if locations:
                lines.append(f"    - {md_text(missing_note)}")
        if not locations:
            for note in occurrence["locationless_notes"] or [""]:
                lines.append(
                    "    - ℹ No discrete source occurrence supplied / لم يُسجّل موضع نصي منفصل."
                    + (" " + md_text(note) if note else "")
                )
        lines.extend(
            location_lines_markdown(
                locations,
                readers_present,
                link_registry,
                arabic_prefix=arabic_prefix,
            )
        )
    if occurrences and human_global_source_rows(decision):
        append_global_source_markdown(
            lines, decision, link_registry, arabic_prefix, indent="  "
        )
    append_unresolved_component_markdown(lines, decision, indent="  ")


def render_decision_shard(
    payload: dict,
    rows: list[dict],
    kind: str,
    index: int,
    total: int,
    previous_name: str | None,
    next_name: str | None,
    arabic_prefix: str,
) -> str:
    priority = kind == "priority"
    prefix = "priority-" if priority else "decision-"
    label = (
        "Priority terminology review" if priority
        else "Complete terminology review"
    )
    navigation = shard_navigation(previous_name, next_name)
    reader_names = [row["name"] for row in payload["reader_evidence"]]
    link_registry = make_link_registry(rows, arabic_prefix=arabic_prefix)
    risk_rows = review_risk_rows(payload) if priority else []
    risk_by_id = {
        row["decision"]["decision_id"]: (rank, row["score"])
        for rank, row in enumerate(risk_rows, 1)
    }
    lines = [
        f"# {label}: part {index} of {total}",
        "",
        navigation,
        "",
        f"This renderable shard contains **{len(rows)}** choices. It preserves every distinct recorded occurrence for those choices. The canonical monolithic sheets remain one directory above for archival use.",
        "",
        (
            "Final-reader page evidence is loaded; exact pages below are shown only when backed by SyncTeX."
            if reader_names else
            "No final-reader PDF/AUX/SyncTeX evidence was supplied; source locations are shown, and final PDF pages remain unclaimed."
        ),
        "",
        (
            "| Global rank / score | Term / المصطلح | Arabic in use / العربية | Where / الموضع |"
            if priority else
            "| Term / المصطلح | Arabic in use / العربية | Where / الموضع |"
        ),
        (
            "| ---: | --- | --- | --- |"
            if priority else
            "| --- | --- | --- |"
        ),
    ]
    for decision in rows:
        anchor = decision_anchor(decision, prefix)
        where = start_here_where(
            decision, "#" + anchor, arabic_prefix=arabic_prefix
        )
        term_cell = f"[{markdown_cell(human_english_term(decision))}](#{anchor})"
        if priority:
            rank, score = risk_by_id[decision["decision_id"]]
            lines.append(
                f"| #{rank} / {score} | {term_cell} | "
                f"{rtl(human_chosen_arabic(decision))} | {where} |"
            )
        else:
            lines.append(
                f"| {term_cell} | {rtl(human_chosen_arabic(decision))} | {where} |"
            )
    for decision in rows:
        append_shard_decision(
            lines,
            decision,
            prefix,
            bool(reader_names),
            link_registry,
            arabic_prefix,
            risk_by_id.get(decision["decision_id"]),
        )
    lines += ["", navigation, ""]
    if link_registry.references:
        lines += ["<!-- Compact repeated source-link definitions -->", ""]
        lines.extend(link_registry.definitions())
        lines.append("")
    return "\n".join(lines)


def render_review_shards(
    payload: dict,
    arabic_prefix: str = "../../../../",
    start_here_href: str = "../EXPERT_REVIEW_START_HERE.md",
    groups: dict[str, list[list[dict]]] | None = None,
) -> dict[str, str]:
    selected_groups = groups or reviewer_shard_groups(payload)
    priority_groups = selected_groups["priority"]
    complete_groups = selected_groups["complete"]
    files: dict[str, str] = {}
    for kind, groups in (("priority", priority_groups), ("complete", complete_groups)):
        for index, rows in enumerate(groups, 1):
            name = f"{kind}-{index:03d}.md"
            previous_name = f"{kind}-{index - 1:03d}.md" if index > 1 else None
            next_name = f"{kind}-{index + 1:03d}.md" if index < len(groups) else None
            files[name] = render_decision_shard(
                payload,
                rows,
                kind,
                index,
                len(groups),
                previous_name,
                next_name,
                arabic_prefix,
            )
    landing = [
        "# Renderable terminology review shards / أجزاء مراجعة المصطلحات",
        "",
        "These small, deterministic files are the browser-friendly review surface. Start with the ranked queue one directory above; it links directly into the appropriate priority shard. Canonical monolithic Markdown, JSON and CSV remain available for preservation and bulk processing.",
        "",
        f"Each generated detail shard is capped at **{REVIEWER_SHARD_HARD_LIMIT_BYTES // 1024} KiB** and is normally partitioned near **{REVIEWER_SHARD_TARGET_BYTES // 1024} KiB**, while a location-rich decision is never split or truncated.",
        "",
        "No final PDF page is inferred. A page appears only when the generator receives final PDF, AUX and SyncTeX evidence.",
        "",
        "## Priority shards / أجزاء الأولوية",
        "",
    ]
    for index, rows in enumerate(priority_groups, 1):
        first_rank = (index - 1) * PRIORITY_SHARD_SIZE + 1
        last_rank = first_rank + len(rows) - 1
        landing.append(
            f"- [Part {index:03d}](priority-{index:03d}.md) — global ranks {first_rank}–{last_rank}; {len(rows)} choices"
        )
    landing += ["", "## Complete shards / الأجزاء الكاملة", ""]
    for index, rows in enumerate(complete_groups, 1):
        first = human_english_term(rows[0])
        last = human_english_term(rows[-1])
        landing.append(
            f"- [Part {index:03d}](complete-{index:03d}.md) — {len(rows)} choices; {md_text(first)} … {md_text(last)}"
        )
    landing += [
        "",
        f"[Back to start-here queue / العودة إلى قائمة البدء]({start_here_href})",
        "",
    ]
    files["README.md"] = "\n".join(landing)
    return files


CSV_COLUMNS = [
    "Review priority / أولوية المراجعة",
    "Decision ID / رقم القرار",
    "English term / sense / المصطلح الإنجليزي ومعناه",
    "Chosen Arabic / العربية المختارة",
    "Alternatives / البدائل",
    "Short rationale / موجز سبب الاختيار",
    "Edition / النسخة",
    "Unit ID / title / رقم الوحدة وعنوانها",
    "Source file + line + link / ملف المصدر والسطر والرابط",
    "Component printed page / رقم الصفحة المطبوع في المكوّن",
    "Assembled PDF page / صفحة PDF المجمّع",
    "Evidence grade / درجة الدليل",
    "Please double-check / يُرجى التحقق",
]


def source_locator_csv(location: dict) -> str:
    source = SOURCE_LABELS.get(location["source_kind"], location["source_kind"])
    logical = collapse(location.get("logical_path") or location.get("recorded_path"))
    logical = logical.replace("\\", "/")
    if re.match(r"^[A-Za-z]:/", logical) or logical.startswith("/"):
        logical = logical.rsplit("/", 1)[-1]
    reconciliation = location["line_reconciliation"]
    if reconciliation["resolved"]:
        start = reconciliation["current_line_start"]
        end = reconciliation["current_line_end"]
        line = f"L{start}" if start == end else f"L{start}–L{end}"
        link = collapse(location.get("source_url"))
        return " | ".join(item for item in (source, f"{logical}:{line}", link) if item)
    if non_locator_reconciliation_status(reconciliation["status"]):
        link = collapse(location.get("file_url"))
        return " | ".join(
            item for item in (
                source,
                logical,
                "UNIT-WIDE / NO DISCRETE LEXICAL OCCURRENCE",
                collapse(reconciliation.get("non_locator_reason")),
                link,
            )
            if item
        )
    start = location.get("line_start")
    end = location.get("line_end")
    line = "no exact line"
    if start is not None:
        line = f"recorded L{start}" + (f"–L{end}" if end != start else "")
    status = collapse(reconciliation.get("status"))
    link = collapse(location.get("file_url"))
    rendered = " | ".join(
        item for item in (source, f"{logical}:{line}", f"UNRESOLVED: {status}", link)
        if item
    )
    candidates = (
        reconciliation.get("candidate_line_ranges")
        or reconciliation.get("exact_search_candidate_line_ranges")
        or []
    )
    if candidates and link:
        candidate_links = []
        for first, last in candidates[:12]:
            label = f"L{first}" if first == last else f"L{first}–L{last}"
            href = link + f"#L{first}" + (f"-L{last}" if last != first else "")
            candidate_links.append(f"{label} {href}")
        rendered += (
            " | EXACT-SEARCH CANDIDATES, NOT YET SENSE-RESOLVED: "
            + "; ".join(candidate_links)
        )
        if len(candidates) > 12:
            rendered += f"; … (+{len(candidates) - 12})"
    return rendered


def occurrence_page_cells(locations: Sequence[dict]) -> tuple[str, str, str]:
    """Flatten only explicit page evidence; never infer a missing page."""

    printed: list[str] = []
    assembled: list[str] = []
    grades: list[str] = []

    def add_unique(rows: list[str], value: str) -> None:
        if value and value not in rows:
            rows.append(value)

    for location in locations:
        source = SOURCE_LABELS.get(location["source_kind"], location["source_kind"])
        reconciliation = location["line_reconciliation"]
        page_rows = location.get("page_evidence") or []
        if not page_rows:
            if non_locator_reconciliation_status(reconciliation["status"]):
                grade = (
                    "unit-wide / no discrete lexical occurrence; no exact page / "
                    "على مستوى الوحدة / لا موضع لفظي منفصل؛ لا صفحة دقيقة"
                )
            else:
                grade = (
                "exact current source line; PDF page unavailable / "
                "سطر مصدر حالي دقيق؛ صفحة PDF غير متاحة"
                if reconciliation["resolved"] else
                "unresolved source locator; no page claim / "
                "موضع مصدر غير محسوم؛ لا ادعاء للصفحة"
                )
            add_unique(grades, f"{source}: {grade}")
            continue
        for page in page_rows:
            reader = collapse(page.get("reader"))
            prefix = f"{source}/{reader}" if reader else source
            method = page.get("method")
            if method == "synctex-exact":
                marker = "exact SyncTeX / SyncTeX دقيق"
                add_unique(grades, f"{prefix}: exact occurrence page (SyncTeX) / صفحة موضع دقيقة")
            elif method == "unit-start-fallback":
                marker = "unit-start fallback / بداية الوحدة فقط"
                add_unique(
                    grades,
                    f"{prefix}: unit-start fallback, not exact term page / بداية الوحدة، وليست صفحة المصطلح بدقة",
                )
            else:
                marker = "unavailable / غير متاح"
                add_unique(
                    grades,
                    f"{prefix}: page unavailable; no page claim / الصفحة غير متاحة؛ لا ادعاء للصفحة",
                )
            for item in page.get("printed_pages") or []:
                label = collapse(item.get("printed_page"))
                if label:
                    add_unique(printed, f"{prefix}: {label} [{marker}]")
            for pdf_page in page.get("assembled_pdf_pages") or page.get("pdf_pages") or []:
                add_unique(assembled, f"{prefix}: {pdf_page} [{marker}]")
    return " || ".join(printed), " || ".join(assembled), " || ".join(grades)


def occurrence_review_question(decision: dict, occurrence: dict | None) -> str:
    """Tie a CSV prompt to its own row instead of a different repeated unit.

    Some decision-level questions legitimately cite the first recorded unit.
    Reusing that sentence verbatim on every repeated-occurrence row can make a
    later row appear to point at the wrong unit.  Keep the explicit question
    when it is compatible with the row; otherwise use the neutral decision
    question and prefix the exact unit/line context proved for this row.
    """

    base = review_question(decision)
    components = expert_unresolved_components(decision)

    def with_components(value: str) -> str:
        if not components:
            return value
        return (
            value
            + " Unresolved component / جزء غير مربوط بموضع: "
            + "; ".join(components)
        )

    cited_units = set(re.findall(r"\bOLP-\d{4}\b", base))
    if occurrence is None:
        if cited_units:
            base = default_review_question(decision)
        prefix = (
            "Exact global source location; no OLP unit / موضع عام دقيق؛ بلا وحدة OLP — "
            if human_global_source_rows(decision) else
            "Location not recorded / لم يُسجّل الموضع — "
        )
        return with_components(prefix + base)

    unit = occurrence["unit"]
    unit_id = collapse(unit.get("unit_id")) or "unit not recorded"
    if cited_units and cited_units != {unit_id}:
        base = default_review_question(decision)
    elif unit_id in cited_units:
        # The decision-level wording already names this row's unit; avoid a
        # redundant prefix while leaving exact lines in their dedicated cell.
        return with_components(base)

    exact_lines: list[str] = []
    unresolved = False
    for location in human_location_rows(occurrence):
        source = SOURCE_LABELS.get(location["source_kind"], location["source_kind"])
        reconciliation = location["line_reconciliation"]
        if reconciliation["resolved"]:
            start = reconciliation["current_line_start"]
            end = reconciliation["current_line_end"]
            label = f"L{start}" if start == end else f"L{start}–L{end}"
            rendered = f"{source} {label}"
            if rendered not in exact_lines:
                exact_lines.append(rendered)
        elif not non_locator_reconciliation_status(reconciliation["status"]):
            unresolved = True
    if exact_lines:
        where = "; ".join(exact_lines)
        if unresolved:
            where += "; another locator remains unresolved"
    else:
        where = (
            "unit-wide/no discrete lexical occurrence"
            if any(
                non_locator_reconciliation_status(
                    location["line_reconciliation"]["status"]
                )
                for location in human_location_rows(occurrence)
            )
            else "exact source line unresolved"
        )
    return with_components(f"{unit_id} ({where}) — {base}")


def render_occurrence_csv(payload: dict) -> str:
    """Render each occurrence, plus one explicit row for every unplaced choice."""

    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=CSV_COLUMNS, lineterminator="\n")
    writer.writeheader()
    decisions = [
        row for row in payload["decisions"]
        if row["index_metadata"]["human_index_included"]
    ]
    for decision in decisions:
        priority = (
            "Priority: please double-check / أولوية: يُرجى التحقق"
            if decision.get("expert_review_useful") is True else
            "Open to correction / قابل للتصحيح"
        )
        sense = human_decision_field(decision, "sense")
        term_sense = human_english_term(decision)
        if sense:
            term_sense += f" — sense: {sense}"
        alternatives = " | ".join(alternatives_text(decision))
        common = {
            CSV_COLUMNS[0]: priority,
            CSV_COLUMNS[1]: decision["decision_id"],
            CSV_COLUMNS[2]: term_sense,
            CSV_COLUMNS[3]: human_chosen_arabic(decision),
            CSV_COLUMNS[4]: alternatives or "none recorded / لم يُسجّل بديل",
            # CSV is a complete expert-review surface, not a teaser for the JSON.
            # Keep every recorded motivation; presentation may wrap the cell.
            CSV_COLUMNS[5]: human_prose(human_decision_field(decision, "rationale")),
            CSV_COLUMNS[6]: human_decision_field(decision, "edition") or "not recorded",
        }
        occurrences = distinct_human_occurrence_rows(decision)
        for occurrence in occurrences:
            unit = occurrence["unit"]
            locations = human_location_rows(occurrence)
            printed, assembled, grade = occurrence_page_cells(locations)
            locator_parts = [source_locator_csv(location) for location in locations]
            missing_note = missing_language_note(occurrence)
            if missing_note and locations:
                locator_parts.append(missing_note)
            locationless_note = locationless_occurrence_note(occurrence)
            row = dict(common)
            row.update(
                {
                    CSV_COLUMNS[7]: f"{unit['unit_id']} — {collapse(unit.get('title'))}",
                    CSV_COLUMNS[8]: " || ".join(locator_parts)
                    or (
                        "Unit known; source edition/path/line not proved / "
                        "الوحدة معلومة؛ ولم تثبت نسخة المصدر أو مساره أو سطره"
                        + (f" | {locationless_note}" if locationless_note else "")
                    ),
                    CSV_COLUMNS[9]: printed,
                    CSV_COLUMNS[10]: assembled,
                    CSV_COLUMNS[11]: grade or (
                        "Unit-only evidence; no exact source line or page claim / "
                        "دليل على مستوى الوحدة فقط؛ لا ادعاء لسطر مصدر أو صفحة دقيقة"
                    ),
                    CSV_COLUMNS[12]: occurrence_review_question(decision, occurrence),
                }
            )
            writer.writerow(row)
        if not occurrences:
            unresolved = unresolved_decision_locator_lines(decision)
            global_locations = human_global_source_rows(decision)
            row = dict(common)
            if global_locations:
                row.update(
                    {
                        CSV_COLUMNS[7]: (
                            "Global/front matter; no OLP unit / "
                            "مصدر عام أو صفحات تمهيدية؛ بلا وحدة OLP"
                        ),
                        CSV_COLUMNS[8]: " || ".join(
                            source_locator_csv(location)
                            for location in global_locations
                        ),
                        CSV_COLUMNS[9]: "",
                        CSV_COLUMNS[10]: "",
                        CSV_COLUMNS[11]: (
                            "Exact hash-bound global source line; no OLP unit or reader-page claim / "
                            "سطر دقيق مربوط بتجزئة المصدر العام؛ بلا وحدة OLP ولا ادعاء لصفحة القارئ"
                        ),
                        CSV_COLUMNS[12]: occurrence_review_question(decision, None),
                    }
                )
            else:
                row.update(
                    {
                        CSV_COLUMNS[7]: "Location not recorded / لم يُسجّل الموضع",
                        CSV_COLUMNS[8]: " || ".join(unresolved) or (
                            "No unit, source path or exact line was proved / "
                            "لم تثبت وحدة أو مسار مصدر أو سطر دقيق"
                        ),
                        CSV_COLUMNS[9]: "",
                        CSV_COLUMNS[10]: "",
                        CSV_COLUMNS[11]: (
                            "Decision recorded; occurrence unresolved; no source-line or page claim / "
                            "القرار مسجل؛ والموضع غير محسوم؛ ولا ادعاء لسطر أو صفحة"
                        ),
                        CSV_COLUMNS[12]: occurrence_review_question(decision, None),
                    }
                )
            writer.writerow(row)
    return stream.getvalue()


def build_payload(
    repo: Path,
    baseline_path: Path,
    ledger_paths: Sequence[Path],
    english_root: Path | None,
    readers: Sequence[ReaderEvidence],
    repo_web_root: str,
    english_web_root: str,
) -> tuple[dict, dict[Path, str]]:
    baseline_data, baseline_raw = read_json_bytes(baseline_path)
    if not isinstance(baseline_data, dict) or not isinstance(baseline_data.get("units"), list):
        raise ValueError("baseline must contain a units array")
    units = baseline_data["units"]
    if len(units) != 722 or [unit_number(str(row.get("id"))) for row in units] != list(range(1, 723)):
        raise ValueError("baseline is not the exact ordered OLP-0001--OLP-0722 inventory")
    token_registries = load_review_token_registries(repo)
    unit_meta = {
        str(row["id"]): derive_unit_meta(repo, row, token_registries["english"])
        for row in units
    }
    decisions, ledger_inventory, source_hashes = load_decisions(
        repo, ledger_paths, units, english_root
    )
    (
        expert_source_binding_identity,
        expert_source_binding_path,
        expert_source_binding_sha256,
    ) = apply_expert_source_bindings(
        repo, baseline_path, units, decisions, english_root
    )
    if expert_source_binding_path is not None and expert_source_binding_sha256:
        source_hashes[expert_source_binding_path] = expert_source_binding_sha256
    assessment_identities, assessment_hashes = apply_expert_review_amendments(
        repo, decisions, english_root, units
    )
    source_hashes.update(assessment_hashes)
    locale_ledger_records = [
        copy.deepcopy(record)
        for identity in ledger_inventory
        for record in identity.get("_locale_records") or []
    ]
    locale_adapter = next(
        (
            identity.get("adapter", {})
            for identity in ledger_inventory
            if identity.get("adapter", {}).get("kind")
            == "locale-ar-terminology-and-adverse-csv-v1"
        ),
        {},
    )
    for registry in token_registries.values():
        for source in registry.identity["sources"]:
            path = (repo / source["path"]).resolve()
            source_hashes[path] = source["sha256"]
    cache = SourceCache()
    resolved_counter: Counter[str] = Counter()
    human_counter: Counter[str] = Counter()
    human_locations = 0
    expert_requested = 0
    generic_count = 0
    semantic_mismatch_exclusions = 0
    output_decisions: list[dict] = []
    for decision in decisions:
        record = copy.deepcopy(decision)
        attach_review_display(record, token_registries)
        generic = is_generic_passage(record)
        generic_count += int(generic)
        if record.get("expert_review_useful") is True and not generic:
            expert_requested += 1
        normalized_global_locations = []
        for location_index, raw in enumerate(
            record.pop("_expert_global_source_raw", []) or [], 1
        ):
            location = reconcile_location(
                raw, repo, english_root, cache, repo_web_root, english_web_root
            )
            invalidate_broad_excerpt_without_recorded_term(location, record)
            if not location["line_reconciliation"]["resolved"]:
                raise ValueError(
                    f"{record['decision_id']}: validated global source binding no longer resolves"
                )
            location["location_id"] = (
                f"{record['decision_id']}:global:"
                f"{location['source_kind']}:loc{location_index:03d}"
            )
            location["human_review_included"] = True
            location["human_review_exclusion_reason"] = None
            # Global/front-matter declarations deliberately make no reader-page
            # claim, even when a runner invocation happens to be in a reader.
            location["page_evidence"] = []
            normalized_global_locations.append(location)
        record["global_source_bindings"] = normalized_global_locations
        normalized_occurrences = []
        for occurrence_index, occurrence in enumerate(record.get("occurrences") or [], 1):
            if not isinstance(occurrence, dict):
                continue
            unit_id = str(occurrence.get("unit_id") or "")
            unit = unit_meta.get(unit_id)
            if unit is None:
                raise ValueError(f"{record['decision_id']}: occurrence has unknown unit {unit_id!r}")
            locations = []
            raw_locations = normalize_occurrence_sources(occurrence)
            recorded_source_kinds = [
                kind for kind in ("english", "msa", "classical")
                if any(raw["source_kind"] == kind for raw in raw_locations)
            ]
            not_recorded_source_kinds = [
                kind for kind in ("english", "msa", "classical")
                if kind not in recorded_source_kinds
            ]
            for location_index, raw in enumerate(raw_locations, 1):
                location = reconcile_location(
                    raw, repo, english_root, cache, repo_web_root, english_web_root
                )
                invalidate_broad_excerpt_without_recorded_term(location, record)
                location = recover_location_by_exact_search(
                    location,
                    record,
                    occurrence,
                    cache,
                    repo_web_root,
                    english_web_root,
                )
                location["location_id"] = (
                    f"{record['decision_id']}:occ{occurrence_index:03d}:"
                    f"{location['source_kind']}:loc{location_index:03d}"
                )
                locations.append(location)
            recover_by_cross_language_exact_structure(
                locations, cache, repo_web_root, english_web_root
            )
            recover_unique_monotone_sequences(
                locations, cache, repo_web_root, english_web_root
            )
            for location in locations:
                apply_location_quality_guards(location, record, unit)
                page_evidence = [
                    reader.locate(location, unit)
                    for reader in readers
                    if reader.source_kind == location["source_kind"]
                ]
                # One assembled edition can have multiple component configs.
                # Keep the strongest successful evidence and suppress noisy
                # unavailable siblings from components that do not contain
                # this unit.
                if any(row["method"] == "synctex-exact" for row in page_evidence):
                    page_evidence = [
                        row for row in page_evidence if row["method"] == "synctex-exact"
                    ]
                elif any(row["method"] == "unit-start-fallback" for row in page_evidence):
                    page_evidence = [
                        row for row in page_evidence
                        if row["method"] == "unit-start-fallback"
                    ]
                location["page_evidence"] = page_evidence
            included_locations = [
                location for location in locations if location["human_review_included"]
            ]
            occurrence_human_included = bool(included_locations) or not locations
            normalized_occurrences.append(
                {
                    "occurrence_index": occurrence_index,
                    "unit": {
                        "unit_id": unit.unit_id,
                        "title": unit.title,
                        "source_role": unit.source_role,
                        "target_path": unit.target_path,
                        "aux_label": unit.aux_label,
                    },
                    "context_note": occurrence.get("context_note"),
                    "language_coverage": {
                        "recorded_source_kinds": recorded_source_kinds,
                        "not_recorded_source_kinds": not_recorded_source_kinds,
                        "not_recorded_classification": (
                            "No occurrence was supplied for this language in the source ledger; "
                            "this is distinct from a supplied but unresolved locator."
                        ),
                    },
                    "human_review_included": occurrence_human_included,
                    "human_review_location_count": len(included_locations),
                    "machine_location_count": len(locations),
                    "locations": locations,
                    "raw_occurrence": occurrence,
                }
            )
        suppress_duplicate_locator_stubs(normalized_occurrences)
        suppress_repeated_human_locations(normalized_occurrences)
        record["index_metadata"] = {
            "human_index_included": not generic,
            "human_index_exclusion_reason": (
                "generic whole-passage placeholder; preserved in JSON but not a word/term choice"
                if generic else None
            ),
            "review_question": review_question(record),
            "occurrence_group_count": sum(
                1 for item in normalized_occurrences if item["human_review_included"]
            ),
            "machine_occurrence_group_count": len(normalized_occurrences),
            "location_count": sum(
                item["human_review_location_count"] for item in normalized_occurrences
                if item["human_review_included"]
            ) + len(normalized_global_locations),
            "global_source_location_count": len(normalized_global_locations),
            "machine_location_count": sum(
                item["machine_location_count"] for item in normalized_occurrences
            ),
            "occurrences": normalized_occurrences,
        }
        output_decisions.append(record)

    suppress_cross_decision_locator_stubs(output_decisions)
    resolved_counter.clear()
    human_counter.clear()
    human_locations = 0
    semantic_mismatch_exclusions = 0
    duplicate_stub_occurrences = 0
    duplicate_location_exclusions = 0
    generic_counter: Counter[str] = Counter()
    for record in output_decisions:
        generic = is_generic_passage(record)
        human_record = record["index_metadata"]["human_index_included"]
        for occurrence in record["index_metadata"]["occurrences"]:
            if not generic and occurrence.get("human_review_exclusion_reason"):
                duplicate_stub_occurrences += int(
                    bool(occurrence.get("human_review_exclusion_reason"))
                )
            for location in occurrence["locations"]:
                status = location["line_reconciliation"]["status"]
                resolved_counter[status] += 1
                if generic:
                    generic_counter[status] += 1
                exclusion_reason = collapse(
                    location.get("human_review_exclusion_reason")
                )
                if not generic and exclusion_reason.startswith(
                    "Excluded after semantic audit:"
                ):
                    semantic_mismatch_exclusions += 1
                if not generic and (
                    exclusion_reason.startswith("Duplicate human locator")
                    or exclusion_reason.startswith("File-only locator stub")
                ):
                    duplicate_location_exclusions += 1
                if (
                    human_record
                    and occurrence["human_review_included"]
                    and location["human_review_included"]
                ):
                    human_counter[status] += 1
                    human_locations += 1

    human_decisions = sum(
        1 for row in output_decisions
        if row["index_metadata"]["human_index_included"]
    )
    superseded_human_decisions = len(output_decisions) - generic_count - human_decisions
    expert_requested = sum(
        1 for row in output_decisions
        if row["index_metadata"]["human_index_included"]
        and row.get("expert_review_useful") is True
    )
    all_resolved = sum(
        count for status, count in resolved_counter.items()
        if resolved_reconciliation_status(status)
    )
    human_resolved = sum(
        count for status, count in human_counter.items()
        if resolved_reconciliation_status(status)
    )
    all_nonlocators = sum(
        count for status, count in resolved_counter.items()
        if non_locator_reconciliation_status(status)
    )
    human_nonlocators = sum(
        count for status, count in human_counter.items()
        if non_locator_reconciliation_status(status)
    )
    human_unresolved = sum(human_counter.values()) - human_resolved - human_nonlocators
    generic_locations = sum(generic_counter.values())
    generic_resolved = sum(
        count for status, count in generic_counter.items()
        if resolved_reconciliation_status(status)
    )
    generic_nonlocators = sum(
        count for status, count in generic_counter.items()
        if non_locator_reconciliation_status(status)
    )
    generic_unresolved = generic_locations - generic_resolved - generic_nonlocators
    human_occurrences = sum(
        sum(
            1 for occurrence in row["index_metadata"]["occurrences"]
            if occurrence["human_review_included"]
        )
        for row in output_decisions
        if row["index_metadata"]["human_index_included"]
    )
    human_decisions_without_occurrence = sum(
        1
        for row in output_decisions
        if row["index_metadata"]["human_index_included"]
        and not human_occurrence_rows(row)
    )
    human_distinct_occurrences = sum(
        len(distinct_human_occurrence_rows(row))
        for row in output_decisions
        if row["index_metadata"]["human_index_included"]
    )
    human_csv_rows = human_distinct_occurrences + human_decisions_without_occurrence
    expert_occurrences = sum(
        sum(
            1 for occurrence in row["index_metadata"]["occurrences"]
            if occurrence["human_review_included"]
        )
        for row in output_decisions
        if row["index_metadata"]["human_index_included"]
        and row.get("expert_review_useful") is True
    )
    locale_decisions = [
        row for row in output_decisions
        if row["decision_id"].startswith("locale-ar-chosen-")
    ]
    locale_visible_locations = [
        location
        for row in locale_decisions
        for occurrence in human_occurrence_rows(row)
        for location in human_location_rows(occurrence)
    ]
    locale_resolved_locations = sum(
        location["line_reconciliation"]["resolved"]
        for location in locale_visible_locations
    )
    locale_unresolved_locations = sum(
        not location["line_reconciliation"]["resolved"]
        and not non_locator_reconciliation_status(
            location["line_reconciliation"]["status"]
        )
        for location in locale_visible_locations
    )
    locale_without_location = sum(
        not any(
            human_location_rows(occurrence)
            for occurrence in human_occurrence_rows(row)
        )
        for row in locale_decisions
    )
    locale_occurrences = [
        occurrence
        for row in locale_decisions
        for occurrence in human_occurrence_rows(row)
    ]
    locale_unit_only_occurrences = sum(
        not human_location_rows(occurrence)
        for occurrence in locale_occurrences
    )
    locale_decisions_with_named_unit = sum(
        bool(human_occurrence_rows(row)) for row in locale_decisions
    )
    locale_decisions_without_named_unit = (
        len(locale_decisions) - locale_decisions_with_named_unit
    )
    locale_global_source_locations = [
        location
        for row in locale_decisions
        for location in row.get("global_source_bindings") or []
        if location.get("human_review_included", True)
    ]
    locale_exact_global_source_locations = sum(
        location["line_reconciliation"]["resolved"]
        for location in locale_global_source_locations
    )
    locale_global_source_only_decisions = sum(
        collapse((row.get("expert_source_binding") or {}).get("disposition"))
        == "global-source-only"
        for row in locale_decisions
    )
    locale_partially_bound_decisions = sum(
        collapse((row.get("expert_source_binding") or {}).get("disposition"))
        == "partially-bound"
        for row in locale_decisions
    )
    locale_unresolved_binding_components = sum(
        len((row.get("expert_source_binding") or {}).get("unresolved_components") or [])
        for row in locale_decisions
    )
    payload = {
        "schema": "openlogic-arabic-expert-review-index-v1",
        "status": "GENERATED_FROM_CURRENT_RECORDED_DECISIONS",
        "purpose": "Human-review index with a lossless machine-readable companion; expert feedback is not a release gate.",
        "location_policy": {
            "source_lines": "Recorded excerpts are verified at their recorded lines or relocated only by a unique exact excerpt, exact context fragment, explicit term, retained source-language term, or exact recorded-sense match. Conflicting, ambiguous or absent exact matches remain unresolved; similarity and nearest-line guesses are forbidden.",
            "absent_language_occurrences": "A language with no occurrence supplied in the ledger is recorded separately from a supplied but unresolved locator and does not inflate unresolved-locator counts.",
            "exact_pdf_pages": "Only an exact SyncTeX source-line record is called an exact occurrence page.",
            "fallback_pdf_pages": "AUX labels and PDF named destinations establish only a unit-start fallback, never an exact occurrence page.",
            "page_guessing": False,
        },
        "baseline": {
            "path": baseline_path.resolve().relative_to(repo.resolve()).as_posix(),
            "bytes": len(baseline_raw),
            "sha256": sha256_bytes(baseline_raw),
            "source_commit": baseline_data.get("source_commit"),
            "unit_count": len(units),
        },
        "input_ledgers": ledger_inventory,
        "expert_review_source_bindings": expert_source_binding_identity,
        "expert_review_assessments": assessment_identities,
        "locale_terminology_and_adverse_records": locale_ledger_records,
        "review_display_token_registries": {
            key: registry.identity for key, registry in token_registries.items()
        },
        "reader_evidence": [reader.identity for reader in readers],
        "reviewer_sharding": {
            "directory": "evidence/classical/terminology/reviewer-index",
            "priority_order": "descending deterministic review-risk score, then displayed English term and stable decision ID",
            "complete_order": "displayed English term, then stable decision ID",
            "priority_choice_cap_per_file": PRIORITY_SHARD_SIZE,
            "complete_choice_cap_per_file": COMPLETE_SHARD_SIZE,
            "target_max_estimated_bytes_per_file": REVIEWER_SHARD_TARGET_BYTES,
            "hard_max_rendered_bytes_per_file": REVIEWER_SHARD_HARD_LIMIT_BYTES,
            "priority_file_count": (
                expert_requested + PRIORITY_SHARD_SIZE - 1
            ) // PRIORITY_SHARD_SIZE,
            "complete_file_count": (
                human_decisions + COMPLETE_SHARD_SIZE - 1
            ) // COMPLETE_SHARD_SIZE,
        },
        "summary": {
            "recorded_decisions": len(output_decisions),
            "locale_ledger_raw_records_preserved": int(
                locale_adapter.get("raw_records") or 0
            ),
            "locale_ledger_chosen_terminology_records_contributed": int(
                locale_adapter.get("chosen_terminology_records_contributed") or 0
            ),
            "locale_ledger_adverse_or_repair_records_machine_only": int(
                locale_adapter.get("adverse_or_repair_records_preserved_machine_only") or 0
            ),
            "locale_ledger_exact_semantic_duplicates_merged": int(
                locale_adapter.get("exact_semantic_duplicates_merged") or 0
            ),
            "locale_ledger_locator_precision_counts": copy.deepcopy(
                locale_adapter.get("parsed_locator_precision_counts") or {}
            ),
            "locale_ledger_chosen_locator_precision_counts": copy.deepcopy(
                locale_adapter.get("chosen_locator_precision_counts") or {}
            ),
            "locale_ledger_resolved_source_locations": locale_resolved_locations,
            "locale_ledger_unresolved_source_locations": locale_unresolved_locations,
            "locale_ledger_chosen_decisions_without_unit_bound_location": (
                locale_without_location
            ),
            "locale_ledger_chosen_decisions_with_named_unit": (
                locale_decisions_with_named_unit
            ),
            "locale_ledger_chosen_unit_only_occurrence_records": (
                locale_unit_only_occurrences
            ),
            "locale_ledger_chosen_decisions_without_named_unit": (
                locale_decisions_without_named_unit
            ),
            "locale_exact_global_source_locations": (
                locale_exact_global_source_locations
            ),
            "locale_global_source_only_decisions": (
                locale_global_source_only_decisions
            ),
            "locale_partially_bound_decisions": (
                locale_partially_bound_decisions
            ),
            "locale_unresolved_binding_components": (
                locale_unresolved_binding_components
            ),
            "exact_semantic_duplicates_merged_across_ledgers": int(
                locale_adapter.get("global_exact_semantic_duplicates_merged") or 0
            ),
            "human_index_decisions": human_decisions,
            "compact_schema_terminology_decisions_included": sum(
                row["decision_id"].startswith(("compact:", "repair-compact-"))
                for row in output_decisions
            ),
            "generic_passage_decisions_omitted": generic_count,
            "superseded_or_duplicate_decisions_omitted_from_human_index": (
                superseded_human_decisions
            ),
            "expert_review_requested": expert_requested,
            "priority_reviewer_shards": (
                expert_requested + PRIORITY_SHARD_SIZE - 1
            ) // PRIORITY_SHARD_SIZE,
            "complete_reviewer_shards": (
                human_decisions + COMPLETE_SHARD_SIZE - 1
            ) // COMPLETE_SHARD_SIZE,
            "human_occurrence_records": human_occurrences,
            "human_distinct_occurrence_rows": human_distinct_occurrences,
            "duplicate_occurrence_rows_suppressed_from_csv": (
                human_occurrences - human_distinct_occurrences
            ),
            "human_decisions_without_occurrence": human_decisions_without_occurrence,
            "human_csv_rows": human_csv_rows,
            "expert_review_occurrence_records": expert_occurrences,
            "human_location_records": human_locations,
            "real_term_resolved_source_locations": human_resolved,
            "real_term_unresolved_source_locations": human_unresolved,
            "real_term_unit_wide_or_nonlexical_records": human_nonlocators,
            "generic_placeholder_location_records": generic_locations,
            "generic_placeholder_resolved_source_locations": generic_resolved,
            "generic_placeholder_unresolved_source_locations": generic_unresolved,
            "semantic_mismatch_locations_excluded_from_human_index": (
                semantic_mismatch_exclusions
            ),
            "duplicate_locator_stub_occurrences_excluded_from_human_index": (
                duplicate_stub_occurrences
            ),
            "duplicate_or_superseded_location_rows_excluded_from_human_index": (
                duplicate_location_exclusions
            ),
            "all_location_records_including_generic": sum(resolved_counter.values()),
            "resolved_source_locations": human_resolved,
            "unresolved_source_locations": human_unresolved,
            "line_reconciliation_statuses": dict(sorted(human_counter.items())),
            "all_resolved_source_locations_including_generic": all_resolved,
            "all_unresolved_source_locations_including_generic": (
                sum(resolved_counter.values()) - all_resolved - all_nonlocators
            ),
            "all_line_reconciliation_statuses_including_generic": dict(
                sorted(resolved_counter.items())
            ),
        },
        "decisions": output_decisions,
    }
    source_hashes[baseline_path.resolve()] = sha256_bytes(baseline_raw)
    source_hashes.update(cache.observed_hashes())
    return payload, source_hashes


def verify_inputs_unchanged(hashes: dict[Path, str]) -> None:
    changed = [str(path) for path, digest in hashes.items() if sha256_file(path) != digest]
    if changed:
        raise RuntimeError("input changed while index was generated: " + ", ".join(changed))


def verify_human_surfaces(surfaces: dict[str, str]) -> None:
    """Fail closed if TeX/Open Logic implementation syntax reaches reviewers."""

    raw_macro = re.compile(
        r"(?:\\(?:use|print)token\b|!!(?:\^|a|\{)|\\[A-Za-z@]+)"
    )
    failures = []
    for name, text in surfaces.items():
        match = raw_macro.search(text)
        if match:
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 80)
            failures.append(f"{name}: {text[start:end]!r}")
    if failures:
        raise RuntimeError(
            "raw TeX/Open Logic macro syntax reached a human-facing surface: "
            + "; ".join(failures)
        )


def verify_occurrence_csv(payload: dict, text: str) -> int:
    """Prove the sortable layer is complete, unique and explicitly located."""

    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows or list(rows[0]) != CSV_COLUMNS:
        raise RuntimeError("occurrence CSV has missing or reordered columns")
    included = [
        row for row in payload["decisions"]
        if row["index_metadata"]["human_index_included"]
    ]
    expected_rows = sum(
        max(1, len(distinct_human_occurrence_rows(decision)))
        for decision in included
    )
    if len(rows) != expected_rows:
        raise RuntimeError(
            f"occurrence CSV row count mismatch: {len(rows)} != {expected_rows}"
        )
    serialized = [tuple(row[column] for column in CSV_COLUMNS) for row in rows]
    duplicates = len(serialized) - len(set(serialized))
    if duplicates:
        raise RuntimeError(f"occurrence CSV contains {duplicates} duplicate full rows")
    expected_ids = {decision["decision_id"] for decision in included}
    actual_ids = {row[CSV_COLUMNS[1]] for row in rows}
    if actual_ids != expected_ids:
        missing = sorted(expected_ids - actual_ids)
        extra = sorted(actual_ids - expected_ids)
        raise RuntimeError(
            f"occurrence CSV decision coverage mismatch; missing={missing}; extra={extra}"
        )
    required = (CSV_COLUMNS[1], CSV_COLUMNS[2], CSV_COLUMNS[3], CSV_COLUMNS[7], CSV_COLUMNS[11], CSV_COLUMNS[12])
    for index, row in enumerate(rows, 2):
        absent = [column for column in required if not collapse(row.get(column))]
        if absent:
            raise RuntimeError(f"occurrence CSV row {index} has blank required cells: {absent}")
    return len(rows)


def verify_reviewer_shards(
    payload: dict,
    shards: dict[str, str],
    groups: dict[str, list[list[dict]]],
) -> None:
    """Fail closed on oversized, missing, duplicated or mis-sharded choices."""

    expected_names = {"README.md"}
    for kind in ("priority", "complete"):
        expected_names.update(
            f"{kind}-{index:03d}.md"
            for index in range(1, len(groups[kind]) + 1)
        )
    if set(shards) != expected_names:
        raise RuntimeError(
            "reviewer shard inventory mismatch: "
            f"missing={sorted(expected_names - set(shards))}; "
            f"extra={sorted(set(shards) - expected_names)}"
        )

    rendered_sizes = {
        name: len(text.encode("utf-8"))
        for name, text in shards.items()
        if name != "README.md"
    }
    oversized = {
        name: size for name, size in rendered_sizes.items()
        if size > REVIEWER_SHARD_HARD_LIMIT_BYTES
    }
    if oversized:
        raise RuntimeError(f"reviewer shards exceed byte limit: {oversized}")

    for kind in ("priority", "complete"):
        prefix = "priority-" if kind == "priority" else "decision-"
        seen: list[str] = []
        for index, group in enumerate(groups[kind], 1):
            text = shards[f"{kind}-{index:03d}.md"]
            for decision in group:
                anchor = decision_anchor(decision, prefix)
                if text.count(f'id="{anchor}"') != 1:
                    raise RuntimeError(
                        f"reviewer shard anchor missing or duplicated: {kind} {anchor}"
                    )
                seen.append(decision["decision_id"])
        if len(seen) != len(set(seen)):
            raise RuntimeError(f"duplicate decision in {kind} reviewer shards")
        expected = (
            [row["decision"]["decision_id"] for row in review_risk_rows(payload)]
            if kind == "priority" else
            [
                row["decision_id"]
                for row in sorted(
                    (
                        item for item in payload["decisions"]
                        if item["index_metadata"]["human_index_included"]
                    ),
                    key=lambda item: (
                        human_english_term(item).casefold(), item["decision_id"]
                    ),
                )
            ]
        )
        if seen != expected:
            raise RuntimeError(f"{kind} reviewer shard order/coverage mismatch")

    payload["reviewer_sharding"]["priority_file_count"] = len(groups["priority"])
    payload["reviewer_sharding"]["complete_file_count"] = len(groups["complete"])
    payload["reviewer_sharding"]["largest_rendered_shard_bytes"] = max(
        rendered_sizes.values(), default=0
    )
    payload["reviewer_sharding"]["smallest_rendered_shard_bytes"] = min(
        rendered_sizes.values(), default=0
    )
    payload["summary"]["priority_reviewer_shards"] = len(groups["priority"])
    payload["summary"]["complete_reviewer_shards"] = len(groups["complete"])


def verify_exact_human_locations(payload: dict) -> None:
    """Prove every displayed exact locator names live, non-comment source text."""

    failures: list[str] = []
    for decision in payload["decisions"]:
        if not decision["index_metadata"]["human_index_included"]:
            continue
        location_sets = [
            human_location_rows(occurrence)
            for occurrence in human_occurrence_rows(decision)
        ]
        if human_global_source_rows(decision):
            location_sets.append(human_global_source_rows(decision))
        for locations in location_sets:
            for location in locations:
                reconciliation = location["line_reconciliation"]
                if not reconciliation["resolved"]:
                    continue
                path = location.get("_fs_path")
                start = reconciliation.get("current_line_start")
                end = reconciliation.get("current_line_end")
                label = f"{decision['decision_id']}:{location.get('location_id')}"
                if not isinstance(path, Path) or not path.is_file():
                    failures.append(f"{label}: resolved locator has no live source file")
                    continue
                source_lines = path.read_text(
                    encoding="utf-8-sig", errors="strict"
                ).splitlines()
                if (
                    not isinstance(start, int)
                    or not isinstance(end, int)
                    or start < 1
                    or end < start
                    or end > len(source_lines)
                ):
                    failures.append(
                        f"{label}: invalid current line range {start!r}-{end!r} "
                        f"for {len(source_lines)} lines"
                    )
                    continue
                segment = "\n".join(source_lines[start - 1:end])
                if not strip_tex_comments(segment).strip():
                    failures.append(
                        f"{label}: exact line range contains only blank/comment text"
                    )
    if failures:
        raise RuntimeError(
            "human exact-locator validation failed: " + "; ".join(failures[:25])
            + (f"; ... (+{len(failures) - 25})" if len(failures) > 25 else "")
        )


def verify_generated_markdown_links(surfaces: dict[Path, str]) -> None:
    """Resolve every local Markdown target and every non-line anchor pre-write."""

    normalized = {path.resolve(): text for path, text in surfaces.items()}
    failures: list[str] = []
    for path, text in normalized.items():
        definitions = dict(
            re.findall(r"^\[([^]]+)\]:\s+(\S+)\s*$", text, flags=re.MULTILINE)
        )
        used_references = set(
            re.findall(r"\[[^\]\n]+\]\[([^]\n]+)\]", text)
        )
        undefined = sorted(used_references - set(definitions))
        if undefined:
            failures.append(f"{path.name}: undefined reference links {undefined}")
        hrefs = re.findall(r"\]\(([^)]+)\)", text) + list(definitions.values())
        for href in hrefs:
            if re.match(r"^(?:https?|mailto):", href, flags=re.IGNORECASE):
                continue
            decoded = unquote(href)
            target_text, separator, fragment = decoded.partition("#")
            target = path if not target_text else (path.parent / target_text).resolve()
            target_body = normalized.get(target)
            if target_body is None:
                if not target.is_file():
                    failures.append(f"{path.name}: missing local target {href}")
                    continue
                if fragment and re.fullmatch(r"L\d+(?:-L\d+)?", fragment):
                    match = re.fullmatch(r"L(\d+)(?:-L(\d+))?", fragment)
                    assert match is not None
                    start = int(match.group(1))
                    end = int(match.group(2) or match.group(1))
                    line_count = len(
                        target.read_text(
                            encoding="utf-8-sig", errors="strict"
                        ).splitlines()
                    )
                    if start < 1 or end < start or end > line_count:
                        failures.append(
                            f"{path.name}: out-of-range local line link {href} "
                            f"({line_count} lines)"
                        )
                continue
            if fragment and not re.fullmatch(r"L\d+(?:-L\d+)?", fragment):
                if f'id="{fragment}"' not in target_body:
                    failures.append(f"{path.name}: missing local anchor {href}")
    if failures:
        raise RuntimeError(
            "generated Markdown link validation failed: " + "; ".join(failures[:50])
            + (f"; ... (+{len(failures) - 50})" if len(failures) > 50 else "")
        )


def write_outputs(
    payload: dict,
    markdown: str,
    start_here_markdown: str,
    priority_markdown: str,
    occurrence_csv: str,
    output_json: Path,
    output_md: Path,
    output_start_here_md: Path,
    output_priority_md: Path,
    output_csv: Path,
    reviewer_shards: dict[str, str],
    output_reviewer_index_dir: Path,
) -> None:
    serializable = strip_private(payload)
    canonical_bytes = {
        output_json: (
            json.dumps(serializable, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n"
        ).encode("utf-8"),
        output_md: markdown.encode("utf-8"),
        output_start_here_md: start_here_markdown.encode("utf-8"),
        output_priority_md: priority_markdown.encode("utf-8"),
        output_csv: b"\xef\xbb\xbf" + occurrence_csv.encode("utf-8"),
    }
    for path in canonical_bytes:
        path.parent.mkdir(parents=True, exist_ok=True)
    output_reviewer_index_dir.mkdir(parents=True, exist_ok=True)
    shard_bytes = {
        output_reviewer_index_dir / name: value.encode("utf-8")
        for name, value in reviewer_shards.items()
    }
    expected = set(reviewer_shards)
    existing_generated = {
        path.name
        for pattern in ("priority-*.md", "complete-*.md", "README.md")
        for path in output_reviewer_index_dir.glob(pattern)
        if path.is_file()
    }
    all_bytes = {**canonical_bytes, **shard_bytes}
    staged: list[tuple[Path, Path]] = []
    try:
        # Stage every byte sequence before replacing any public artifact. Each
        # individual replace is atomic on the same volume, so a failed stage
        # cannot truncate a prior usable file.
        for path in sorted(all_bytes, key=lambda item: str(item)):
            temporary = path.with_name(
                "." + path.name + ".expert-review-index.tmp"
            )
            staged.append((temporary, path))
            temporary.write_bytes(all_bytes[path])
        for temporary, path in staged:
            temporary.replace(path)
        # Remove obsolete generated shard names only after all expected files
        # have been installed. Unrelated reviewer notes are never touched.
        for stale_name in sorted(existing_generated - expected):
            (output_reviewer_index_dir / stale_name).unlink()
    finally:
        for temporary, _ in staged:
            if temporary.exists():
                temporary.unlink()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    default_repo = Path(__file__).resolve().parents[1]
    parser.add_argument("--repo", type=Path, default=default_repo)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument(
        "--ledger", type=Path, action="append", default=[],
        help="repeat to override automatic direct-ledger discovery",
    )
    parser.add_argument("--english-root", type=Path)
    parser.add_argument(
        "--repo-web-root",
        default="https://github.com/KokunoYumeto/OpenLogic-ar/blob/main",
    )
    parser.add_argument("--english-web-root")
    parser.add_argument(
        "--reader-pdf", action="append", default=[], metavar="NAME=PATH",
        help="repeat for each final assembled reader/component mapping",
    )
    parser.add_argument(
        "--reader-component-pdf", action="append", default=[], metavar="NAME=PATH",
        help="optional component PDF supplying page labels/named destinations",
    )
    parser.add_argument("--reader-aux", action="append", default=[], metavar="NAME=PATH")
    parser.add_argument("--reader-synctex", action="append", default=[], metavar="NAME=PATH")
    parser.add_argument(
        "--reader-page-offset", action="append", default=[], metavar="NAME=COUNT",
        help="component pages preceding this component in the assembled PDF",
    )
    parser.add_argument(
        "--reader-source", action="append", default=[], metavar="NAME=msa|classical",
    )
    parser.add_argument("--output-md", type=Path)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-start-here-md", type=Path)
    parser.add_argument("--output-priority-md", type=Path)
    parser.add_argument("--output-csv", type=Path)
    parser.add_argument(
        "--output-reviewer-index-dir",
        "--output-shard-dir",
        dest="output_reviewer_index_dir",
        type=Path,
        help="directory for small browser-renderable priority and complete Markdown shards",
    )
    parser.add_argument(
        "--start-here-limit",
        type=int,
        default=30,
        help="maximum choices in the curated technical/repair navigation queue",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.start_here_limit < 1:
        raise ValueError("--start-here-limit must be at least 1")
    repo = args.repo.resolve()
    output_md = (
        args.output_md
        or repo / "evidence/classical/terminology/EXPERT_REVIEW_INDEX.md"
    ).resolve()
    output_json = (
        args.output_json
        or repo / "evidence/classical/terminology/EXPERT_REVIEW_INDEX.json"
    ).resolve()
    output_start_here_md = (
        args.output_start_here_md
        or repo / "evidence/classical/terminology/EXPERT_REVIEW_START_HERE.md"
    ).resolve()
    output_priority_md = (
        args.output_priority_md
        or repo / "evidence/classical/terminology/EXPERT_REVIEW_PRIORITY_ONLY.md"
    ).resolve()
    output_csv = (
        args.output_csv
        or repo / "evidence/classical/terminology/EXPERT_REVIEW_OCCURRENCES.csv"
    ).resolve()
    output_reviewer_index_dir = (
        args.output_reviewer_index_dir
        or repo / "evidence/classical/terminology/reviewer-index"
    ).resolve()
    baseline = (args.baseline or repo / "evidence/classical/BASELINE.json").resolve()
    ledger_paths = [path.resolve() for path in args.ledger] or discover_ledgers(repo)
    english_root = args.english_root
    if english_root is None:
        conventional = repo.parents[1] / "openlogic-interfarsi/repo/source/upstream"
        english_root = conventional if conventional.is_dir() else None
    elif not english_root.is_dir():
        raise FileNotFoundError(english_root)
    baseline_data, _ = read_json_bytes(baseline)
    source_commit = baseline_data.get("source_commit") if isinstance(baseline_data, dict) else None
    english_web_root = args.english_web_root or (
        "https://github.com/OpenLogicProject/OpenLogic/blob/" + str(source_commit or "master")
    )
    readers = build_readers(args, repo)
    payload, hashes = build_payload(
        repo=repo,
        baseline_path=baseline,
        ledger_paths=ledger_paths,
        english_root=english_root.resolve() if english_root else None,
        readers=readers,
        repo_web_root=args.repo_web_root,
        english_web_root=english_web_root,
    )
    try:
        reviewer_directory_label = output_reviewer_index_dir.relative_to(
            repo
        ).as_posix()
    except ValueError:
        reviewer_directory_label = output_reviewer_index_dir.name
    payload["reviewer_sharding"]["directory"] = reviewer_directory_label
    shard_groups = reviewer_shard_groups(payload)
    payload["reviewer_sharding"]["priority_file_count"] = len(
        shard_groups["priority"]
    )
    payload["reviewer_sharding"]["complete_file_count"] = len(
        shard_groups["complete"]
    )
    payload["summary"]["priority_reviewer_shards"] = len(
        shard_groups["priority"]
    )
    payload["summary"]["complete_reviewer_shards"] = len(
        shard_groups["complete"]
    )
    verify_exact_human_locations(payload)
    public_payload = strip_private(payload)
    markdown_reviewer_href = (
        markdown_relative_directory(output_md.parent, output_reviewer_index_dir)
        or "."
    )
    start_reviewer_href = (
        markdown_relative_directory(
            output_start_here_md.parent, output_reviewer_index_dir
        )
        or "."
    )
    priority_reviewer_href = (
        markdown_relative_directory(
            output_priority_md.parent, output_reviewer_index_dir
        )
        or "."
    )
    markdown = render_markdown(
        public_payload,
        arabic_prefix=markdown_relative_prefix(output_md.parent, repo),
        reviewer_index_href=markdown_reviewer_href,
    )
    priority_href_by_id = priority_shard_href_map(
        public_payload,
        reviewer_index_href=start_reviewer_href,
        groups=shard_groups["priority"],
    )
    start_here_markdown = render_start_here_markdown(
        public_payload,
        args.start_here_limit,
        priority_href_by_id=priority_href_by_id,
        arabic_prefix=markdown_relative_prefix(output_start_here_md.parent, repo),
        reviewer_index_href=start_reviewer_href,
    )
    priority_markdown = render_priority_markdown(
        public_payload,
        arabic_prefix=markdown_relative_prefix(output_priority_md.parent, repo),
        reviewer_index_href=priority_reviewer_href,
    )
    occurrence_csv = render_occurrence_csv(public_payload)
    reviewer_shards = render_review_shards(
        public_payload,
        arabic_prefix=markdown_relative_prefix(output_reviewer_index_dir, repo),
        start_here_href=markdown_relative_file(
            output_reviewer_index_dir, output_start_here_md
        ),
        groups=shard_groups,
    )
    human_surfaces = {
        "full Markdown": markdown,
        "start-here Markdown": start_here_markdown,
        "priority Markdown": priority_markdown,
        "occurrence CSV": occurrence_csv,
    }
    human_surfaces.update(
        {f"reviewer shard {name}": value for name, value in reviewer_shards.items()}
    )
    verify_human_surfaces(human_surfaces)
    markdown_surfaces = {
        output_md: markdown,
        output_start_here_md: start_here_markdown,
        output_priority_md: priority_markdown,
    }
    markdown_surfaces.update(
        {
            output_reviewer_index_dir / name: value
            for name, value in reviewer_shards.items()
        }
    )
    verify_generated_markdown_links(markdown_surfaces)
    csv_row_count = verify_occurrence_csv(public_payload, occurrence_csv)
    if csv_row_count != payload["summary"]["human_csv_rows"]:
        raise RuntimeError(
            "occurrence CSV validation disagrees with payload summary: "
            f"{csv_row_count} != {payload['summary']['human_csv_rows']}"
        )
    verify_reviewer_shards(payload, reviewer_shards, shard_groups)
    verify_inputs_unchanged(hashes)
    write_outputs(
        payload,
        markdown,
        start_here_markdown,
        priority_markdown,
        occurrence_csv,
        output_json,
        output_md,
        output_start_here_md,
        output_priority_md,
        output_csv,
        reviewer_shards,
        output_reviewer_index_dir,
    )
    print(json.dumps(payload["summary"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
