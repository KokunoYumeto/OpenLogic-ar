"""Read-only, conservative checks for the Classical Arabic source overlay.

Usage: python build/validate_classical_overlay.py --ids 1-24 [--json]
       python build/validate_classical_overlay.py --all [--json]

Exit 0: selected targets satisfy STATIC checks; no unreviewed/unchanged units remain.
Exit 1: a hash, syntax, invariant or declaration check failed.
Exit 2: missing targets, unchanged prose or unreviewed structural candidates remain.
Exit 3: invalid arguments, baseline or declaration input.
No result certifies translation, semantic equivalence, review, rendering or release.
Nothing is written, compiled, downloaded or automatically repaired.

Optional --declarations JSON (no implicit shared ledger is consumed):
{"schema":"openlogic-classical-exceptions-v1", "units":[{
  "id":"OLP-0001", "arabic_sha256":"...", "target_sha256":"...",
  "math_text":[{"index":0, "command":"\\text", "source":"نص",
                "target":"عبارة", "note":"Explanation of equivalence"}],
  "terminology":[{"source":"!!{element}", "target":"عنصر",
                   "note":"Explicit grammatical realization"}]
}]}
Math-text indices are zero-based in ordered, outermost formula segments.
Declarations are byte-hash-bound, must be used exactly, and cannot waive changes
to non-Arabic/formal tokens. Terminology target phrases must occur uniquely in
unprotected prose. Declarations record an assertion, not proof of equivalence.

Optional --structural-reviews JSON is separate from formula exceptions and batch
receipts. Schema: openlogic-classical-structural-reviews-v1; units require id,
arabic_sha256, target_sha256, kind="heading-import-driver", and nonempty note.
Both actual files must fit the restricted driver grammar and preserve ordered
driver commands, in addition to ALL ordinary formal checks. Hash-bound records
attest a review; this checker cannot authenticate who performed it or its quality.

Optional --baseline-corrections JSON is an explicit, byte-bound continuation of
the otherwise frozen baseline. It is never discovered or loaded implicitly. Each
entry binds the frozen MSA identity, one corrected MSA identity, the corresponding
current Classical target identity, finding IDs, and a rationale. It changes no
comparison rule and grants no waiver: both effective source and target bytes must
match before the ordinary checks run.

Optional --formal-repairs JSON records a prior, explicit audit of intentional
formal differences. Each record is bound to the frozen baseline, the complete
baseline-correction overlay, the effective MSA and Classical bytes, the exact set
of failed formal checks, and a digest of the complete raw comparison. It cannot
accept syntax errors, import/terminology differences, new or changed failures, or
any subsequent byte change. Raw failed checks remain visible in the report.

Optional --general-reviews JSON can close only the otherwise incomplete
``unchanged-prose`` status. Every record is bound to the frozen/effective source,
the current target, the complete raw-comparison digest, and the exact correction,
math-text, formal-repair and structural-review companion bytes. It cannot accept
changed prose, formal or syntax failures, or a later byte/status change.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata


MATH_ENVS = frozenset("math displaymath equation equation* align align* alignat "
                     "alignat* flalign flalign* xalignat xalignat* xxalignat "
                     "gather gather* multline multline* eqnarray eqnarray* "
                     "aligned alignedat gathered split cases array matrix pmatrix "
                     "bmatrix Bmatrix vmatrix Vmatrix smallmatrix".split())
LITERAL_ENVS = frozenset("verbatim verbatim* Verbatim BVerbatim LVerbatim "
                        "lstlisting minted filecontents filecontents* luacode "
                        "luacode* comment".split())
PROGRAM_ENVS = frozenset("alltt program algorithm algorithmic algorithm2e "
                        "tikzpicture prooftree oltableau tableau derivation".split())
TEXT_COMMANDS = frozenset("text textrm textsf textnormal textbf textit textsl "
                         "textup texttt mbox hbox intertext shortintertext".split())
SIMPLE_KEYS = frozenset("label ollabel ref Ref pageref Pageref eqref autoref "
                        "Autoref cref Cref cpageref Cpageref nameref vref Vref "
                        "tagref url path nolinkurl bibliography bibliographystyle "
                        "externaldocument includeonly tagtrue tagfalse tagitem "
                        "tagsection includeenv excludeenv".split())
IMPORTS = frozenset("input include subfile subfileinclude import subimport "
                   "includefrom subincludefrom inputfrom subinputfrom olimport".split())
FORBIDDEN_DYNAMIC = frozenset("catcode scantokens endlinechar".split())
FORMAL_PROSE_MACROS = frozenset("Nat Int PosInt Real Rat Bin Struct Lang Log Obj "
                              "Atom Ax PIso fn Th True False Indet Undef".split())
PROOF_COMMANDS = frozenset("AxiomC UnaryInfC BinaryInfC TrinaryInfC QuaternaryInfC "
                          "QuinaryInfC RightLabel LeftLabel Axiom UnaryInf BinaryInf "
                          "TrinaryInf DisplayProof noLine singleLine doubleLine "
                          "dashedLine dottedLine rootAtTop rootAtBottom".split())
ARABIC_RANGES = ((0x0600, 0x06ff), (0x0750, 0x077f), (0x08a0, 0x08ff),
                 (0xfb50, 0xfdff), (0xfe70, 0xfeff))
LIMITATIONS = [
    "Lexical TeX checking only: no general macro expansion, conditional execution, or engine validation; identical environment signatures in the two branches of a literal \\iftag are normalized.",
    "Static agreement does not establish prose meaning, quality, completeness, or semantic equivalence.",
    "Arabic wording-change detection is lexical; changed prose always awaits separate semantic review.",
    "Formula order, delimiter kind, formal tokens and protected blocks are intentionally strict.",
    "Unknown macro argument semantics and external imported code are not fully modeled.",
    "This invocation checks only selected baseline units; extra overlay files are not enumerated.",
    "Structural review validates an explicit byte-bound record and narrow driver syntax, not reviewer authenticity or semantic equivalence.",
]

STRUCTURAL_SCHEMA = "openlogic-classical-structural-reviews-v1"
STRUCTURAL_FIELDS = frozenset(("id", "arabic_sha256", "target_sha256", "kind", "note"))
BASELINE_CORRECTIONS_SCHEMA = "openlogic-classical-baseline-corrections-v1"
BASELINE_CORRECTIONS_SCHEMA_V2 = "openlogic-classical-baseline-corrections-v2"
BASELINE_CORRECTIONS_SCHEMAS = frozenset((
    BASELINE_CORRECTIONS_SCHEMA,
    BASELINE_CORRECTIONS_SCHEMA_V2,
))
BASELINE_CORRECTIONS_TOP_FIELDS = frozenset(("schema", "baseline_sha256", "units"))
BASELINE_CORRECTION_FIELDS = frozenset((
    "id", "arabic_path", "target_path",
    "old_msa_sha256", "old_msa_bytes",
    "current_msa_sha256", "current_msa_bytes",
    "current_classical_target_sha256", "current_classical_target_bytes",
    "finding_ids", "rationale",
))
LEGACY_FINDING_ID_PATTERN = re.compile(
    r"(?:"
    r"(?:OLFUN|OLSIZ)-\d{3}|"          # bounded manager audits
    r"C\d{3}-\d{2}|"                   # correction-overlay audit, e.g. C287-01
    r"\d{4}-[A-Z]\d{1,3}|"             # unit review, e.g. 0391-I1
    r"[A-Z][A-Z0-9]{1,15}(?:-[A-Z0-9]{1,15}){0,3}-[A-Z]\d{1,3}"  # cross-unit review
    r")"
)
FINDING_ID_PATTERN = re.compile(
    r"(?:"
    r"(?:OLFUN|OLSIZ)-\d{3}|"          # bounded manager audits
    r"C\d{3}-\d{2}|"                   # correction-overlay audit, e.g. C287-01
    r"\d{4}-[A-Z]\d{1,3}|"             # unit review, e.g. 0391-I1
    r"(?:QNT|NML-TERM)-\d{2}|"          # exact shared terminology decisions
    r"R\d{3}-\d{2}|"                   # exact repair-review identifiers
    r"\d{4}-\d{4}-[A-Z]\d{1,3}|"      # exact multi-unit review finding
    r"[A-Z][A-Z0-9]{1,15}(?:-[A-Z0-9]{1,15}){0,3}-[A-Z]\d{1,3}"  # cross-unit review
    r")"
)
FORMAL_REPAIRS_SCHEMA = "openlogic-classical-formal-repairs-v1"
FORMAL_REPAIRS_TOP_FIELDS = frozenset((
    "schema", "baseline_sha256", "baseline_corrections_sha256", "units",
))
FORMAL_REPAIR_FIELDS = frozenset((
    "id", "effective_msa_sha256", "effective_msa_bytes",
    "target_sha256", "target_bytes", "accepted_failed_checks",
    "comparison_sha256", "authority_refs", "rationale",
))
FORMAL_REPAIR_ALLOWED_CHECKS = frozenset((
    "environment_sequence",
    "protected_reference_citation_and_macro_keys",
    "protected_program_and_literal_blocks",
    "ordered_proof_and_induction_commands",
    "ordered_formula_segments_and_tokens",
))
RAW_COMPARISON_CHECKS = frozenset((
    "environment_sequence",
    "protected_reference_citation_and_macro_keys",
    "ordered_import_identities",
    "protected_program_and_literal_blocks",
    "ordered_proof_and_induction_commands",
    "openlogic_terminology_inventory",
    "ordered_formula_segments_and_tokens",
))
GENERAL_REVIEWS_SCHEMA = "openlogic-classical-general-reviews-v1"
GENERAL_REVIEWS_TOP_FIELDS = frozenset((
    "schema", "baseline_sha256", "baseline_corrections_sha256",
    "declarations_sha256", "formal_repairs_sha256",
    "structural_reviews_sha256", "units",
))
GENERAL_REVIEW_FIELDS = frozenset((
    "id", "effective_msa_sha256", "effective_msa_bytes",
    "target_sha256", "target_bytes", "accepted_status",
    "comparison_sha256", "authority_refs", "rationale",
))
GENERAL_REVIEW_ALLOWED_STATUSES = frozenset(("unchanged-prose",))
DRIVER_HEADINGS = {"olchapter": 3, "olpart": 2, "olsection": 1, "part": 1,
                   "chapter": 1, "section": 1, "subsection": 1, "subsubsection": 1}
DRIVER_IDS = {"olfileid": 3, "olchapterid": 2, "olpartid": 1, "label": 1, "ollabel": 1}
DRIVER_IMPORTS = frozenset(("olimport", "input", "include", "subfile", "subfileinclude"))


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def arabic_letter(ch: str) -> bool:
    return unicodedata.category(ch).startswith("L") and any(a <= ord(ch) <= b for a, b in ARABIC_RANGES)


@dataclass(frozen=True)
class Token:
    value: str
    start: int
    end: int
    kind: str = "char"


@dataclass
class Analysis:
    text: str
    tokens: list[Token]
    errors: list[str] = field(default_factory=list)
    environments: list[tuple[str, str]] = field(default_factory=list)
    formulas: list[tuple[str, list[Token]]] = field(default_factory=list)
    protected: list[tuple[str, str]] = field(default_factory=list)
    keys: list[tuple[str, tuple[str, ...]]] = field(default_factory=list)
    imports: list[tuple[str, tuple[str, ...]]] = field(default_factory=list)
    terminology: list[str] = field(default_factory=list)
    masks: list[tuple[int, int]] = field(default_factory=list)
    math_text: list[tuple[str, list[Token]]] = field(default_factory=list)
    opaque_spans: list[tuple[int, int]] = field(default_factory=list)
    formal_commands: list[tuple[str, tuple[str, ...]]] = field(default_factory=list)


def command_at(text: str, pos: int) -> tuple[str, int]:
    match = re.match(r"\\(?:[A-Za-z@]+|[^\r\n])", text[pos:])
    if not match:
        return "\\", pos + 1
    return match.group(), pos + len(match.group())


def lex(text: str) -> tuple[list[Token], list[str]]:
    """Tokenize before dropping comments, preserving control-word boundaries."""
    tokens, errors = [], []
    pos = 0
    while pos < len(text):
        start, ch = pos, text[pos]
        if ch == "%":
            end = text.find("\n", pos)
            pos = len(text) if end < 0 else end + 1
            continue
        if ch.isspace():
            while pos < len(text) and text[pos].isspace():
                pos += 1
            tokens.append(Token(text[start:pos], start, pos, "space"))
            continue
        if ch == "\\":
            cmd, pos = command_at(text, pos)
            if cmd in (r"\url", r"\nolinkurl"):
                while pos < len(text) and text[pos].isspace():
                    pos += 1
                if pos < len(text):
                    delim, end = text[pos], pos + 1
                    if delim == "{":
                        depth = 1
                        while end < len(text) and depth:
                            if text[end] == "\\":
                                _, end = command_at(text, end)
                                continue
                            depth += (text[end] == "{") - (text[end] == "}")
                            end += 1
                        if depth:
                            errors.append(f"unclosed URL at character {start}")
                    else:
                        found = text.find(delim, end)
                        if found < 0:
                            errors.append(f"unclosed URL at character {start}")
                            end = len(text)
                        else:
                            end = found + 1
                    pos = end
                    tokens.append(Token(text[start:pos], start, pos, "literal-url"))
                    continue
            if cmd in (r"\verb", r"\lstinline", r"\mintinline"):
                if pos < len(text) and text[pos] == "*":
                    pos += 1
                if cmd != r"\verb":
                    while pos < len(text) and text[pos].isspace():
                        pos += 1
                    if pos < len(text) and text[pos] == "[":
                        option_end = text.find("]", pos + 1)
                        if option_end < 0 or "[" in text[pos + 1:option_end]:
                            errors.append(f"unsupported inline-literal options at character {start}")
                        else:
                            pos = option_end + 1
                    while pos < len(text) and text[pos].isspace():
                        pos += 1
                    if cmd == r"\mintinline":
                        language = re.match(r"\{[A-Za-z0-9_+.-]+\}", text[pos:])
                        if not language:
                            errors.append(f"unsupported mintinline language at character {start}")
                        else:
                            pos += len(language.group())
                    while pos < len(text) and text[pos].isspace():
                        pos += 1
                if pos >= len(text) or text[pos].isspace():
                    errors.append(f"unsupported/malformed inline literal at character {start}")
                else:
                    delim = text[pos]
                    if delim == "{" and cmd != r"\verb":
                        depth, end = 1, pos + 1
                        while end < len(text) and depth:
                            depth += (text[end] == "{") - (text[end] == "}")
                            end += 1
                        end = end - 1 if depth == 0 else -1
                    else:
                        end = text.find(delim, pos + 1)
                    if end < 0 or "\n" in text[pos:end]:
                        errors.append(f"unclosed inline literal at character {start}")
                        end = len(text) - 1
                    pos = end + 1
                    tokens.append(Token(text[start:pos], start, pos, "literal"))
                    continue
            if cmd == r"\begin":
                match = re.match(r"\s*\{([^{}]+)\}", text[pos:])
                if match and match.group(1) in LITERAL_ENVS:
                    name = match.group(1)
                    body_start = pos + len(match.group())
                    end_marker = "\\end{" + name + "}"
                    end = text.find(end_marker, body_start)
                    if end < 0:
                        errors.append(f"unclosed literal environment {name} at character {start}")
                        pos = len(text)
                    else:
                        pos = end + len(end_marker)
                    tokens.append(Token(text[start:pos], start, pos, "literal-env"))
                    continue
            tokens.append(Token(cmd, start, pos, "command"))
            continue
        pos += 1
        tokens.append(Token(ch, start, pos))
    return tokens, errors


def skip_space(tokens: list[Token], pos: int) -> int:
    while pos < len(tokens) and tokens[pos].kind == "space":
        pos += 1
    return pos


def group(tokens: list[Token], pos: int, opener: str = "{") -> tuple[list[Token], int] | None:
    pos = skip_space(tokens, pos)
    if pos >= len(tokens) or tokens[pos].value != opener:
        return None
    closer = "}" if opener == "{" else "]"
    start, depth, braces = pos + 1, 1, 0
    pos += 1
    while pos < len(tokens):
        val = tokens[pos].value
        if opener == "[":
            braces += (val == "{") - (val == "}")
        if opener == "{" or braces == 0:
            if val == opener:
                depth += 1
            elif val == closer:
                depth -= 1
                if depth == 0:
                    return tokens[start:pos], pos + 1
        pos += 1
    raise ValueError(f"unclosed {opener} group at character {tokens[start - 1].start}")


def canonical(tokens: list[Token], spaces: bool = False) -> tuple[str, ...]:
    result = []
    for tok in tokens:
        if tok.kind == "space":
            if spaces and (not result or result[-1] != " "):
                result.append(" ")
        else:
            result.append(tok.value)
    return tuple(result)


def raw_body(analysis: Analysis, tokens: list[Token]) -> str:
    return analysis.text[tokens[0].start:tokens[-1].end] if tokens else ""


def key_value(tokens: list[Token]) -> str:
    # Unlike formulas, spaces inside identifiers are not silently removed.
    return "".join(canonical(tokens, spaces=True))


def mask(analysis: Analysis, tokens: list[Token]) -> None:
    if tokens:
        analysis.masks.append((tokens[0].start, tokens[-1].end))


def conditional_environment_duplicates(tokens: list[Token]) -> set[int]:
    """Return environment-command indices duplicated by equivalent ``\\iftag`` branches.

    A source idiom may select only an environment's argument while leaving its
    shared body and closing command outside the conditional, for example::

        \\iftag{one-column}{\\begin{tabular}{|c|}}
                           {\\begin{tabular}{|c|c|}}
        ... \\end{tabular}

    Lexically counting both alternatives creates a spurious unclosed
    environment.  It is safe to retain the first branch's events and suppress
    the second branch's events only when their complete ordered (kind, name)
    signatures are identical.  Any unequal, malformed, or dynamic conditional
    remains untouched and therefore fails closed under the ordinary stack scan.
    """

    index_by_start = {tok.start: index for index, tok in enumerate(tokens)}
    literal_environment_name = re.compile(r"[A-Za-z@][A-Za-z0-9@*_.:-]*\Z")

    def events(body: list[Token]) -> list[tuple[int, str, str]] | None:
        found: list[tuple[int, str, str]] = []
        for local, tok in enumerate(body):
            if tok.value not in (r"\begin", r"\end"):
                continue
            try:
                parsed = group(body, local + 1)
            except ValueError:
                return None
            if not parsed:
                return None
            name_tokens, _ = parsed
            name = key_value(name_tokens)
            # Normalization is deliberately narrower than TeX itself.  A
            # computed or otherwise nonliteral environment name needs actual
            # macro expansion to reason about and must therefore take the
            # ordinary fail-closed lexical path.
            if not literal_environment_name.fullmatch(name):
                return None
            found.append((index_by_start[tok.start], tok.value[1:], name))
        return found

    duplicates: set[int] = set()
    for index, tok in enumerate(tokens):
        if tok.value != r"\iftag":
            continue
        try:
            first = group(tokens, index + 1)
            if not first:
                continue
            _, pos = first
            second = group(tokens, pos)
            if not second:
                continue
            true_branch, pos = second
            third = group(tokens, pos)
            if not third:
                continue
            false_branch, _ = third
        except ValueError:
            continue
        true_events, false_events = events(true_branch), events(false_branch)
        if true_events is None or false_events is None:
            continue
        true_signature = [(kind, name) for _, kind, name in true_events]
        false_signature = [(kind, name) for _, kind, name in false_events]
        if true_signature and true_signature == false_signature:
            duplicates.update(event_index for event_index, _, _ in false_events)
    return duplicates


def parse_keys(a: Analysis) -> None:
    ts = a.tokens
    for i, tok in enumerate(ts):
        if tok.kind != "command":
            continue
        if any(start <= tok.start < end for start, end in a.opaque_spans):
            continue
        name = tok.value[1:]
        if name in FORBIDDEN_DYNAMIC:
            a.errors.append(f"dynamic TeX lexical change {tok.value} is unsupported at character {tok.start}")
        # required-key count, optional count, required args consumed, key positions
        optional, required, key_positions = 0, 0, set()
        keep_optional = False
        if name in PROOF_COMMANDS:
            required = 0 if name in "Axiom UnaryInf BinaryInf TrinaryInf DisplayProof noLine singleLine doubleLine dashedLine dottedLine rootAtTop rootAtBottom".split() else 1
            key_positions = set(range(required))
        elif name == "indcase":
            required, key_positions = 2, {0, 1}
        elif name in SIMPLE_KEYS or name.startswith("cite") or name in ("nocite", "hyperlink", "hypertarget", "href"):
            optional, required, key_positions = 2, 1, {0}
        elif name in ("olref", "Olref"):
            optional, required, key_positions, keep_optional = 3, 1, {0}, True
        elif name in ("olfileid", "olchapterid", "olpartid"):
            optional = 1
            required = {"olfileid": 3, "olchapterid": 2, "olpartid": 1}[name]
            key_positions, keep_optional = set(range(required)), True
        elif name in ("olchapter", "olpart"):
            optional, required = 1, 3 if name == "olchapter" else 2
            key_positions = set(range(required - 1))
        elif name == "oliflabeldef" or name in ("iftag", "iftagged"):
            required, key_positions = 1, {0}
        elif name in IMPORTS:
            optional, required, keep_optional = 1, 2 if name in ("import", "subimport", "includefrom", "subincludefrom", "inputfrom", "subinputfrom") else 1, True
            key_positions = set(range(required))
        elif name in ("includegraphics", "documentclass", "usepackage", "RequirePackage"):
            optional, required, key_positions, keep_optional = 2, 1, {0}, True
        elif name == "hyperref":
            optional, keep_optional = 1, True
        elif name in FORMAL_PROSE_MACROS:
            # Formula segments already protect these fully; capture invocations
            # outside math too, including the customary one-token argument form.
            required = 2 if name == "Atom" else (0 if name in "Nat Int PosInt Real Rat Bin True False Indet Undef".split() else 1)
            key_positions = set(range(required))
        else:
            continue
        pos, values = skip_space(ts, i + 1), []
        if pos < len(ts) and ts[pos].value == "*":
            values.append("*")
            pos += 1
        if name == "indcase" and pos < len(ts) and ts[pos].value == "!":
            values.append("!")
            pos += 1
        for _ in range(optional):
            parsed = group(ts, pos, "[")
            if not parsed:
                break
            body, pos = parsed
            if keep_optional:
                values.append("[" + key_value(body) + "]")
                mask(a, body)
        for j in range(required):
            parsed = group(ts, pos)
            if parsed:
                body, pos = parsed
            else:
                pos = skip_space(ts, pos)
                if pos >= len(ts):
                    raise ValueError(f"missing argument of {tok.value} at character {tok.start}")
                if name in FORMAL_PROSE_MACROS:
                    body, pos = ts[pos:pos + 1], pos + 1
                elif name == "input":
                    end = pos
                    while end < len(ts) and ts[end].kind != "space" and ts[end].value not in ("{", "}"):
                        end += 1
                    body, pos = ts[pos:end], end
                else:
                    raise ValueError(f"unbraced/unsupported argument of {tok.value} at character {tok.start}")
            if j in key_positions:
                values.append("{" + key_value(body) + "}")
                mask(a, body)
        if name == "olimport":
            parsed = group(ts, pos, "[")
            if parsed:
                body, pos = parsed
                values.append("[" + key_value(body) + "]")
                mask(a, body)
        entry = (name, tuple(values))
        if name in PROOF_COMMANDS or name == "indcase":
            a.formal_commands.append(entry)
        else:
            (a.imports if name in IMPORTS else a.keys).append(entry)


def analyze(text: str) -> Analysis:
    ts, errors = lex(text)
    a = Analysis(text, ts, errors)
    stack, env_spans, brace_stack = [], {}, []
    duplicate_conditional_environments = conditional_environment_duplicates(ts)
    i = 0
    while i < len(ts):
        tok = ts[i]
        if tok.kind.startswith("literal"):
            a.protected.append((tok.kind, tok.value.replace("\r\n", "\n")))
            mask(a, [tok])
            if tok.kind == "literal-env":
                name = re.match(r"\\begin\s*\{([^{}]+)\}", tok.value).group(1)
                a.environments.extend((("begin", name), ("end", name)))
        elif tok.value == "{":
            brace_stack.append(tok.start)
        elif tok.value == "}":
            if brace_stack:
                brace_stack.pop()
            else:
                a.errors.append(f"unmatched closing brace at character {tok.start}")
        if tok.value in (r"\begin", r"\end") and i not in duplicate_conditional_environments:
            try:
                parsed = group(ts, i + 1)
                if not parsed:
                    raise ValueError(f"missing environment name at character {tok.start}")
                body, after = parsed
                name, kind = key_value(body), tok.value[1:]
                a.environments.append((kind, name))
                if kind == "begin":
                    stack.append((name, i))
                    if name in ("tagblock", "tagenumerate", "probtag"):
                        arg = group(ts, after)
                        if arg:
                            a.keys.append(("environment:" + name, (key_value(arg[0]),)))
                            mask(a, arg[0])
                elif not stack or stack[-1][0] != name:
                    a.errors.append(f"mismatched environment end {name} at character {tok.start}")
                else:
                    _, start = stack.pop()
                    env_spans[start] = (after, name)
            except ValueError as exc:
                a.errors.append(str(exc))
        i += 1
    a.errors.extend(f"unclosed environment {name} at character {ts[start].start}" for name, start in stack)
    a.errors.extend(f"unclosed brace at character {pos}" for pos in brace_stack)
    # Discover program blocks independently: a containing \[...\] or math
    # environment must not hide a nested tikzpicture from this protection.
    for start, (after, name) in sorted(env_spans.items()):
        if name in PROGRAM_ENVS:
            a.protected.append((name, text[ts[start].start:ts[after - 1].end].replace("\r\n", "\n")))
            a.opaque_spans.append((ts[start].start, ts[after - 1].end))
            mask(a, ts[start:after])
    i = 0
    while i < len(ts):
        tok = ts[i]
        if i in env_spans:
            after, name = env_spans[i]
            if name in MATH_ENVS:
                a.formulas.append(("environment:" + name, ts[i:after]))
                mask(a, ts[i:after])
                i = after
                continue
        if tok.value == r"\ensuremath":
            try:
                parsed = group(ts, i + 1)
                if not parsed:
                    raise ValueError(f"unbraced ensuremath at character {tok.start}")
                _, after = parsed
                a.formulas.append(("ensuremath", ts[i:after]))
                mask(a, ts[i:after])
                i = after
                continue
            except ValueError as exc:
                a.errors.append(str(exc))
        if tok.value in ("$", r"\(", r"\["):
            double = tok.value == "$" and i + 1 < len(ts) and ts[i + 1].value == "$"
            opener = "$$" if double else tok.value
            closer = {"$": "$", "$$": "$", r"\(": r"\)", r"\[": r"\]"}[opener]
            j, depth, found = i + (2 if double else 1), 0, False
            while j < len(ts):
                val = ts[j].value
                if val == closer and depth == 0:
                    if double and (j + 1 >= len(ts) or ts[j + 1].value != "$"):
                        a.errors.append(f"single dollar closes display math at character {ts[j].start}")
                    else:
                        after = j + (2 if double else 1)
                        a.formulas.append((opener, ts[i:after]))
                        mask(a, ts[i:after])
                        i, found = after, True
                        break
                depth += (val == "{") - (val == "}")
                j += 1
            if found:
                continue
            a.errors.append(f"unclosed math {opener} at character {tok.start}")
        elif tok.value in (r"\)", r"\]"):
            a.errors.append(f"unmatched math delimiter {tok.value} at character {tok.start}")
        i += 1
    try:
        parse_keys(a)
    except ValueError as exc:
        a.errors.append(str(exc))
    i = 0
    while i + 1 < len(ts):
        if ts[i].value == "!" and ts[i + 1].value == "!":
            start, pos = i, i + 2
            if pos < len(ts) and ts[pos].value == "^":
                pos += 1
            if pos < len(ts) and ts[pos].value == "a":
                pos += 1
            try:
                parsed = group(ts, pos)
                if not parsed:
                    raise ValueError(f"unsupported OpenLogic terminology at character {ts[start].start}")
                _, pos = parsed
                if pos < len(ts) and ts[pos].value == "s":
                    pos += 1
                a.terminology.append("".join(canonical(ts[start:pos])))
                mask(a, ts[start:pos])
                i = pos
                continue
            except ValueError as exc:
                a.errors.append(str(exc))
        i += 1
    for _, tokens in a.formulas:
        j = 0
        while j < len(tokens):
            if tokens[j].kind == "command" and tokens[j].value[1:] in TEXT_COMMANDS:
                try:
                    parsed = group(tokens, j + 1)
                    if parsed:
                        body, after = parsed
                        a.math_text.append((tokens[j].value, body))
                        j = after
                        continue
                except ValueError as exc:
                    a.errors.append(str(exc))
            j += 1
    return a


def math_signature(tokens: list[Token], replacements: dict[int, tuple[str, ...]]) -> tuple:
    result, i = [], 0
    while i < len(tokens):
        tok = tokens[i]
        if tok.kind == "command" and tok.value[1:] in TEXT_COMMANDS:
            parsed = group(tokens, i + 1)
            if parsed:
                body, after = parsed
                key = body[0].start if body else -1
                result.append((tok.value, replacements.get(key, canonical(body, spaces=True))))
                i = after
                continue
        if tok.kind != "space":
            result.append(tok.value)
        i += 1
    return tuple(result)


def arabic_words(text: str) -> tuple[str, ...]:
    # Marks belong to words; punctuation-only edits cannot count as rephrasing.
    words, current = [], []
    for ch in text:
        if arabic_letter(ch) or (current and unicodedata.category(ch).startswith("M")):
            current.append(ch)
        elif current:
            words.append("".join(current))
            current = []
    if current:
        words.append("".join(current))
    return tuple(words)


def prose_text(a: Analysis) -> str:
    chars = list(a.text)
    # Reconstruct from non-comment tokens; then remove protected/formal spans.
    retained = [False] * len(chars)
    for tok in a.tokens:
        if tok.kind == "command":
            continue
        for pos in range(tok.start, tok.end):
            retained[pos] = True
    for start, end in a.masks:
        retained[start:end] = [False] * (end - start)
    return "".join(ch if retained[i] else " " for i, ch in enumerate(chars))


def formal_text_projection(tokens: list[Token]) -> tuple[str, ...]:
    # Remove only Arabic letters/marks and Arabic punctuation from declared
    # prose changes; retain digits, Latin identifiers, TeX and math structure.
    return tuple(t.value for t in tokens if t.kind != "space" and not (
        t.kind == "char" and (arabic_letter(t.value) or
        (any(lo <= ord(t.value) <= hi for lo, hi in ARABIC_RANGES) and
         unicodedata.category(t.value)[0] in ("M", "P")))))


def compare(source: str, target: str, declaration: dict | None = None) -> dict:
    a, b = analyze(source), analyze(target)
    failures = ["source syntax: " + x for x in a.errors] + ["target syntax: " + x for x in b.errors]
    exceptions, replacements = [], {}
    decl = declaration or {}
    for item in decl.get("math_text", []):
        try:
            index = item["index"]
            if type(index) is not int or index < 0 or not item.get("note", "").strip():
                raise ValueError("nonnegative index and nonempty equivalence note required")
            scmd, st = a.math_text[index]
            tcmd, tt = b.math_text[index]
            if scmd != item["command"] or tcmd != scmd:
                raise ValueError("math-text command mismatch")
            if raw_body(a, st) != item["source"] or raw_body(b, tt) != item["target"]:
                raise ValueError("math-text declaration body mismatch")
            if canonical(st, True) == canonical(tt, True):
                raise ValueError("unused math-text declaration")
            if not arabic_words(item["source"]) or not arabic_words(item["target"]):
                raise ValueError("declaration must concern Arabic prose")
            if formal_text_projection(st) != formal_text_projection(tt):
                raise ValueError("declaration changes non-Arabic/formal tokens")
            key = tt[0].start if tt else -1
            if key in replacements:
                raise ValueError("duplicate math-text declaration")
            replacements[key] = canonical(st, True)
            exceptions.append({"kind": "math_text", "index": index, "note": item["note"]})
        except (KeyError, IndexError, TypeError, ValueError, AttributeError) as exc:
            failures.append("invalid math-text declaration: " + str(exc))
    left_terms, right_terms = Counter(a.terminology), Counter(b.terminology)
    for item in decl.get("terminology", []):
        try:
            original, replacement = item["source"], item["target"]
            if not item.get("note", "").strip() or not arabic_words(replacement):
                raise ValueError("Arabic replacement and nonempty note required")
            parsed = analyze(original)
            if parsed.errors or parsed.terminology != [original] or left_terms[original] <= right_terms[original]:
                raise ValueError("source terminology occurrence is not removed")
            if "\\" in replacement or "$" in replacement or "!!" in replacement:
                raise ValueError("replacement must be plain Arabic prose")
            if prose_text(b).count(replacement) != 1:
                raise ValueError("replacement must occur uniquely in unprotected target prose")
            left_terms[original] -= 1
            exceptions.append({"kind": "terminology", "source": original, "note": item["note"]})
        except (KeyError, TypeError, ValueError, AttributeError) as exc:
            failures.append("invalid terminology declaration: " + str(exc))
    checks = {
        "environment_sequence": a.environments == b.environments,
        "protected_reference_citation_and_macro_keys": Counter(a.keys) == Counter(b.keys),
        "ordered_import_identities": a.imports == b.imports,
        "protected_program_and_literal_blocks": a.protected == b.protected,
        "ordered_proof_and_induction_commands": a.formal_commands == b.formal_commands,
        "openlogic_terminology_inventory": +left_terms == +right_terms,
    }
    try:
        left_math = [(kind, math_signature(ts, {})) for kind, ts in a.formulas]
        right_math = [(kind, math_signature(ts, replacements)) for kind, ts in b.formulas]
        checks["ordered_formula_segments_and_tokens"] = left_math == right_math
    except ValueError as exc:
        checks["ordered_formula_segments_and_tokens"] = False
        failures.append("formula signature error: " + str(exc))
    for check, passed in checks.items():
        if not passed:
            failures.append(check + " differs")
    differences = []
    if not checks["ordered_formula_segments_and_tokens"]:
        for index in range(max(len(a.formulas), len(b.formulas))):
            left = a.formulas[index] if index < len(a.formulas) else None
            right = b.formulas[index] if index < len(b.formulas) else None
            try:
                if left and right and (left[0], math_signature(left[1], {})) == (right[0], math_signature(right[1], replacements)):
                    continue
            except ValueError:
                pass
            detail = {"kind": "formula", "index": index}
            for side, value, analysis in (("source", left, a), ("target", right, b)):
                detail[side] = None if value is None else {
                    "kind": value[0], "line": analysis.text.count("\n", 0, value[1][0].start) + 1,
                    "excerpt": raw_body(analysis, value[1])[:240]}
            differences.append(detail)
            if len(differences) == 8:
                break
    for label, left, right in (("protected_keys", Counter(a.keys), Counter(b.keys)),
                               ("terminology", +left_terms, +right_terms)):
        if left != right:
            differences.append({"kind": label, "removed": list((left - right).items())[:8],
                                "added": list((right - left).items())[:8]})
    source_words = arabic_words(prose_text(a)) + tuple(w for _, ts in a.math_text for w in arabic_words(raw_body(a, ts)))
    target_words = arabic_words(prose_text(b)) + tuple(w for _, ts in b.math_text for w in arabic_words(raw_body(b, ts)))
    has_prose = bool(source_words or a.terminology)
    changed = source_words != target_words
    if failures:
        status = "flagged"
    elif has_prose and not changed:
        status = "unchanged-prose"
    elif has_prose:
        status = "changed-prose-awaiting-semantic-review"
    else:
        status = "structural-only-candidate"
    return {"status": status, "checks": checks, "failures": failures,
            "arabic_prose_present": has_prose, "arabic_wording_changed": changed,
            "formula_segments": {"source": len(a.formulas), "target": len(b.formulas)},
            "math_text_segments": {"source": len(a.math_text), "target": len(b.math_text)},
            "declared_exceptions": exceptions, "differences": differences,
            "semantic_equivalence_proven": False}


def scoped_path(repo: Path, value: str, prefix: str) -> Path:
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts or ":" in value:
        raise ValueError(f"out-of-scope path: {value}")
    path, allowed = (repo / relative).resolve(), (repo / prefix).resolve()
    if not path.is_relative_to(allowed) or path.suffix != ".tex":
        raise ValueError(f"out-of-scope path: {value}")
    return path


def load_baseline(path: Path) -> tuple[dict, str]:
    raw = path.read_bytes()
    baseline = json.loads(raw.decode("utf-8-sig"))
    units = baseline.get("units")
    if baseline.get("schema") != "openlogic-classical-baseline-v1" or not isinstance(units, list):
        raise ValueError("unsupported baseline schema")
    if baseline.get("total_units") != len(units) or len({u["id"] for u in units}) != len(units):
        raise ValueError("baseline count/duplicate identity error")
    for unit in units:
        if not re.fullmatch(r"OLP-\d{4}", unit["id"]) or not re.fullmatch(r"[0-9a-fA-F]{64}", unit["arabic_sha256"]):
            raise ValueError("invalid baseline identity/hash")
        if type(unit["arabic_bytes"]) is not int or unit["arabic_bytes"] < 0:
            raise ValueError("invalid baseline byte count")
    return baseline, sha256(raw)


def load_baseline_corrections(path: Path) -> tuple[dict, str]:
    """Load an explicit correction overlay while rejecting duplicate JSON keys."""
    def unique_fields(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("duplicate JSON field in baseline corrections: " + key)
            value[key] = item
        return value

    raw = path.read_bytes()
    return json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_fields), sha256(raw)


def load_formal_repairs(path: Path) -> tuple[dict, str]:
    """Load formal-repair declarations while rejecting duplicate JSON keys."""
    def unique_fields(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("duplicate JSON field in formal repairs: " + key)
            value[key] = item
        return value

    raw = path.read_bytes()
    return json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_fields), sha256(raw)


def load_declarations(path: Path) -> tuple[dict, str]:
    """Load formula/prose declarations while rejecting duplicate JSON keys."""
    def unique_fields(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("duplicate JSON field in declarations: " + key)
            value[key] = item
        return value

    raw = path.read_bytes()
    return json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_fields), sha256(raw)


def load_general_reviews(path: Path) -> tuple[dict, str]:
    """Load general-review declarations while rejecting duplicate JSON keys."""
    def unique_fields(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("duplicate JSON field in general reviews: " + key)
            value[key] = item
        return value

    raw = path.read_bytes()
    return json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_fields), sha256(raw)


def baseline_correction_records(data: dict | None, baseline: dict,
                                baseline_sha256: str | None, repo: Path) -> dict:
    """Validate correction metadata against the frozen baseline, without reading content.

    Current content bytes are checked only for selected units in validate(), so entries
    outside the requested selection are reported as unused rather than silently attested.
    """
    if data is None:
        return {}
    if (not isinstance(data, dict) or set(data) != BASELINE_CORRECTIONS_TOP_FIELDS or
            data.get("schema") not in BASELINE_CORRECTIONS_SCHEMAS or
            not isinstance(data.get("units"), list)):
        raise ValueError("unsupported baseline corrections schema/fields")
    if (not isinstance(baseline_sha256, str) or
            not re.fullmatch(r"[0-9a-f]{64}", baseline_sha256)):
        raise ValueError("baseline corrections require the exact loaded baseline SHA-256")
    bound_hash = data.get("baseline_sha256")
    if not isinstance(bound_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", bound_hash):
        raise ValueError("invalid baseline corrections baseline SHA-256")
    if bound_hash != baseline_sha256:
        raise ValueError("baseline corrections bind a different frozen baseline")

    known = {unit["id"]: unit for unit in baseline["units"]}
    records, arabic_paths, target_paths, finding_ids = {}, set(), set(), set()
    finding_pattern = (LEGACY_FINDING_ID_PATTERN
                       if data["schema"] == BASELINE_CORRECTIONS_SCHEMA
                       else FINDING_ID_PATTERN)
    for item in data["units"]:
        if not isinstance(item, dict) or set(item) != BASELINE_CORRECTION_FIELDS:
            raise ValueError("baseline correction requires exactly the documented unit fields")
        uid = item["id"]
        if not isinstance(uid, str) or uid not in known or uid in records:
            raise ValueError("duplicate/unknown baseline correction identity")
        frozen = known[uid]
        for field in ("arabic_path", "target_path"):
            if not isinstance(item[field], str) or item[field] != frozen[field]:
                raise ValueError(f"baseline correction {field} differs from frozen baseline")
        scoped_path(repo, item["arabic_path"], "source/locale/ar/content")
        scoped_path(repo, item["target_path"], "source/locale/ar-classical/content")
        if item["arabic_path"] in arabic_paths or item["target_path"] in target_paths:
            raise ValueError("duplicate baseline correction path")
        arabic_paths.add(item["arabic_path"])
        target_paths.add(item["target_path"])

        for field in ("old_msa_sha256", "current_msa_sha256",
                      "current_classical_target_sha256"):
            if not isinstance(item[field], str) or not re.fullmatch(r"[0-9a-f]{64}", item[field]):
                raise ValueError("invalid baseline correction hash")
        for field in ("old_msa_bytes", "current_msa_bytes",
                      "current_classical_target_bytes"):
            if type(item[field]) is not int or item[field] < 0:
                raise ValueError("invalid baseline correction byte count")
        if (item["old_msa_sha256"] != frozen["arabic_sha256"].lower() or
                item["old_msa_bytes"] != frozen["arabic_bytes"]):
            raise ValueError("baseline correction old MSA identity differs from frozen baseline")
        if item["current_msa_sha256"] == item["old_msa_sha256"]:
            raise ValueError("baseline correction current MSA hash must differ from frozen MSA hash")

        findings = item["finding_ids"]
        if (not isinstance(findings, list) or not findings or
                any(not isinstance(value, str) or not finding_pattern.fullmatch(value)
                    for value in findings) or len(set(findings)) != len(findings)):
            raise ValueError("baseline correction requires unique supported bounded finding IDs")
        if (data["schema"] == BASELINE_CORRECTIONS_SCHEMA and
                any(value in finding_ids for value in findings)):
            raise ValueError("duplicate finding ID across baseline corrections")
        finding_ids.update(findings)
        if not isinstance(item["rationale"], str) or not item["rationale"].strip():
            raise ValueError("baseline correction requires a nonempty rationale")
        records[uid] = item
    return records


def formal_comparison_sha256(comparison: dict) -> str:
    """Digest every deterministic raw-comparison field relevant to acceptance."""
    # ``validate`` augments a comparison result with baseline-identity and
    # repair-binding checks.  A formal-repair record must bind the raw semantic
    # comparison only, regardless of whether the caller passes the direct
    # ``compare`` result or the augmented unit result returned by ``validate``.
    raw_checks = {
        name: comparison["checks"][name]
        for name in sorted(RAW_COMPARISON_CHECKS)
        if name in comparison["checks"]
    }
    if set(raw_checks) != RAW_COMPARISON_CHECKS:
        missing = sorted(RAW_COMPARISON_CHECKS - set(raw_checks))
        raise ValueError("formal comparison lacks raw checks: " + ", ".join(missing))
    payload = {
        "status": comparison["status"],
        "checks": raw_checks,
        "failures": comparison["failures"],
        "differences": comparison["differences"],
        "arabic_prose_present": comparison["arabic_prose_present"],
        "arabic_wording_changed": comparison["arabic_wording_changed"],
        "formula_segments": comparison["formula_segments"],
        "math_text_segments": comparison["math_text_segments"],
        "declared_exceptions": comparison["declared_exceptions"],
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":")).encode("utf-8")
    return sha256(canonical)


def formal_repair_records(data: dict | None, effective_baseline: dict,
                          baseline_sha256: str | None,
                          baseline_corrections_sha256: str | None) -> dict:
    """Validate exact, fail-closed formal-repair declarations without reading targets."""
    if data is None:
        return {}
    if (not isinstance(data, dict) or set(data) != FORMAL_REPAIRS_TOP_FIELDS or
            data.get("schema") != FORMAL_REPAIRS_SCHEMA or
            not isinstance(data.get("units"), list)):
        raise ValueError("unsupported formal repairs schema/fields")
    for field, expected in (("baseline_sha256", baseline_sha256),
                            ("baseline_corrections_sha256", baseline_corrections_sha256)):
        value = data.get(field)
        if (not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value) or
                not isinstance(expected, str) or value != expected):
            raise ValueError(f"formal repairs bind a different {field.replace('_', ' ')}")

    known = {unit["id"]: unit for unit in effective_baseline["units"]}
    records = {}
    for item in data["units"]:
        if not isinstance(item, dict) or set(item) != FORMAL_REPAIR_FIELDS:
            raise ValueError("formal repair requires exactly the documented unit fields")
        uid = item["id"]
        if not isinstance(uid, str) or uid not in known or uid in records:
            raise ValueError("duplicate/unknown formal repair identity")
        for field in ("effective_msa_sha256", "target_sha256", "comparison_sha256"):
            if not isinstance(item[field], str) or not re.fullmatch(r"[0-9a-f]{64}", item[field]):
                raise ValueError("invalid formal repair hash")
        for field in ("effective_msa_bytes", "target_bytes"):
            if type(item[field]) is not int or item[field] < 0:
                raise ValueError("invalid formal repair byte count")
        source = known[uid]
        if (item["effective_msa_sha256"] != source["arabic_sha256"].lower() or
                item["effective_msa_bytes"] != source["arabic_bytes"]):
            raise ValueError("formal repair effective MSA identity differs from effective baseline")
        accepted = item["accepted_failed_checks"]
        if (not isinstance(accepted, list) or not accepted or accepted != sorted(set(accepted)) or
                any(not isinstance(value, str) or value not in FORMAL_REPAIR_ALLOWED_CHECKS
                    for value in accepted)):
            raise ValueError("formal repair requires sorted unique permitted failed checks")
        refs = item["authority_refs"]
        if (not isinstance(refs, list) or not refs or len(set(refs)) != len(refs) or
                any(not isinstance(value, str) or not value.strip() for value in refs)):
            raise ValueError("formal repair requires unique nonempty authority references")
        if not isinstance(item["rationale"], str) or not item["rationale"].strip():
            raise ValueError("formal repair requires a nonempty rationale")
        records[uid] = item
    return records


def general_review_records(data: dict | None, effective_baseline: dict,
                           baseline_sha256: str | None,
                           baseline_corrections_sha256: str | None,
                           declarations_sha256: str | None,
                           formal_repairs_sha256: str | None,
                           structural_reviews_sha256: str | None) -> dict:
    """Validate exact reviews of unchanged prose; no other status is waivable."""
    if data is None:
        return {}
    if (not isinstance(data, dict) or set(data) != GENERAL_REVIEWS_TOP_FIELDS or
            data.get("schema") != GENERAL_REVIEWS_SCHEMA or
            not isinstance(data.get("units"), list)):
        raise ValueError("unsupported general reviews schema/fields")
    for field, expected in (
            ("baseline_sha256", baseline_sha256),
            ("baseline_corrections_sha256", baseline_corrections_sha256),
            ("declarations_sha256", declarations_sha256),
            ("formal_repairs_sha256", formal_repairs_sha256),
            ("structural_reviews_sha256", structural_reviews_sha256)):
        value = data.get(field)
        if (not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value) or
                not isinstance(expected, str) or value != expected):
            raise ValueError(f"general reviews bind a different {field.replace('_', ' ')}")

    known = {unit["id"]: unit for unit in effective_baseline["units"]}
    records = {}
    for item in data["units"]:
        if not isinstance(item, dict) or set(item) != GENERAL_REVIEW_FIELDS:
            raise ValueError("general review requires exactly the documented unit fields")
        uid = item["id"]
        if not isinstance(uid, str) or uid not in known or uid in records:
            raise ValueError("duplicate/unknown general review identity")
        for field in ("effective_msa_sha256", "target_sha256", "comparison_sha256"):
            if not isinstance(item[field], str) or not re.fullmatch(r"[0-9a-f]{64}", item[field]):
                raise ValueError("invalid general review hash")
        for field in ("effective_msa_bytes", "target_bytes"):
            if type(item[field]) is not int or item[field] < 0:
                raise ValueError("invalid general review byte count")
        source = known[uid]
        if (item["effective_msa_sha256"] != source["arabic_sha256"].lower() or
                item["effective_msa_bytes"] != source["arabic_bytes"]):
            raise ValueError("general review effective MSA identity differs from effective baseline")
        if item["accepted_status"] not in GENERAL_REVIEW_ALLOWED_STATUSES:
            raise ValueError("general review may accept only unchanged-prose")
        refs = item["authority_refs"]
        if (not isinstance(refs, list) or not refs or len(set(refs)) != len(refs) or
                any(not isinstance(value, str) or not value.strip() for value in refs)):
            raise ValueError("general review requires unique nonempty authority references")
        if not isinstance(item["rationale"], str) or not item["rationale"].strip():
            raise ValueError("general review requires a nonempty rationale")
        records[uid] = item
    return records


def apply_formal_repair(result: dict, source: bytes, target: bytes,
                        comparison: dict, record: dict) -> None:
    """Accept only the exact pre-audited raw comparison; preserve its failed checks."""
    raw_failed_checks = sorted(name for name, passed in comparison["checks"].items() if not passed)
    plain_failures = [name + " differs" for name, passed in comparison["checks"].items()
                      if not passed]
    binding = {
        "formal_repair_source_hash_and_bytes": (
            record["effective_msa_sha256"] == sha256(source) and
            record["effective_msa_bytes"] == len(source)),
        "formal_repair_target_hash_and_bytes": (
            record["target_sha256"] == sha256(target) and
            record["target_bytes"] == len(target)),
        "formal_repair_failed_check_scope": (
            raw_failed_checks == record["accepted_failed_checks"] and
            comparison["failures"] == plain_failures and
            set(raw_failed_checks) <= FORMAL_REPAIR_ALLOWED_CHECKS),
        "formal_repair_comparison_fingerprint": (
            record["comparison_sha256"] == formal_comparison_sha256(comparison)),
    }
    result["checks"].update(binding)
    result["formal_repair"] = {
        "record": record,
        "raw_status": comparison["status"],
        "raw_failed_checks": raw_failed_checks,
        "raw_failures": list(comparison["failures"]),
        "validated": all(binding.values()),
    }
    result["formal_repair_applied"] = all(binding.values())
    if all(binding.values()):
        result["accepted_failures"] = list(comparison["failures"])
        result["failures"] = []
        result["status"] = "formal-repair-reviewed"
    else:
        result["failures"] = list(comparison["failures"])
        result["failures"].extend(name + " differs" for name, passed in binding.items()
                                  if not passed)
        result["status"] = "flagged"


def apply_general_review(result: dict, source: bytes, target: bytes,
                         comparison: dict, record: dict) -> None:
    """Close only an exact, previously reviewed unchanged-prose comparison."""
    binding = {
        "general_review_source_hash_and_bytes": (
            record["effective_msa_sha256"] == sha256(source) and
            record["effective_msa_bytes"] == len(source)),
        "general_review_target_hash_and_bytes": (
            record["target_sha256"] == sha256(target) and
            record["target_bytes"] == len(target)),
        "general_review_status_scope": (
            comparison["status"] == record["accepted_status"] == "unchanged-prose" and
            not comparison["failures"]),
        "general_review_comparison_fingerprint": (
            record["comparison_sha256"] == formal_comparison_sha256(comparison)),
    }
    result["checks"].update(binding)
    result["general_review"] = {
        "record": record,
        "raw_status": comparison["status"],
        "validated": all(binding.values()),
    }
    result["general_review_applied"] = all(binding.values())
    if all(binding.values()):
        result["status"] = "unchanged-prose-reviewed"
    else:
        result["failures"] = list(result.get("failures", []))
        result["failures"].extend(name + " differs" for name, passed in binding.items()
                                  if not passed)
        result["status"] = "flagged"


def selected_units(units: list[dict], ids: str | None) -> list[dict]:
    if ids is None:
        return units
    match = re.fullmatch(r"(?:OLP-)?(\d{1,4})-(?:OLP-)?(\d{1,4})", ids, flags=re.I)
    if not match:
        raise ValueError("--ids requires FIRST-LAST, e.g. 1-24 or OLP-0001-OLP-0024")
    first, last = map(int, match.groups())
    if first > last:
        raise ValueError("--ids range is reversed")
    wanted = {f"OLP-{i:04d}" for i in range(first, last + 1)}
    if not wanted <= {u["id"] for u in units}:
        raise ValueError("--ids contains identities absent from baseline")
    return [u for u in units if u["id"] in wanted]


def structural_driver(text: str) -> dict:
    """Recognize a small grammar, not the absence of Arabic words or a role label.

    Reject executable/formatting macros inside arguments, formulas, prose bodies,
    conditionals, all environments except document, and unknown commands. Only
    plain heading text is omitted from the ordered structural signature.
    """
    ts, errors = lex(text)
    signature, imports, headings, pos = [], 0, 0, 0
    phase, wrapper, documentclass = "before", False, False

    def argument(opener="{", title=False):
        nonlocal pos
        parsed = group(ts, pos, opener)
        if parsed is None:
            raise ValueError("missing braced driver argument")
        body, pos = parsed
        value = key_value(body)
        if title:
            if not value.strip() or any(t.kind not in ("char", "space") or
                                       (t.kind == "char" and (t.value in "{}$!^&_~#" or
                                        unicodedata.category(t.value)[0] not in "LMNP")) for t in body):
                raise ValueError("heading must be nonempty plain text without TeX/formal syntax")
            return "<heading>"
        if not re.fullmatch(r"[A-Za-z0-9_./:+-]+", value):
            raise ValueError("driver identity/path must be a literal ASCII token")
        return value

    try:
        if errors:
            raise ValueError("; ".join(errors))
        while (pos := skip_space(ts, pos)) < len(ts):
            tok = ts[pos]
            if tok.kind != "command":
                raise ValueError(f"non-driver text at character {tok.start}")
            name, pos = tok.value[1:], pos + 1
            values = []
            if phase == "after":
                raise ValueError("content after end of document")
            if name == "documentclass":
                if signature or documentclass:
                    raise ValueError("documentclass must occur once at the start")
                documentclass = True
                if group(ts, pos, "[") is not None:
                    values.append("[" + argument("[") + "]")
                if argument() != "subfiles":
                    raise ValueError("only the subfiles driver class is supported")
                values.append("subfiles")
            elif name in ("begin", "end"):
                if argument() != "document":
                    raise ValueError("only the document wrapper is permitted")
                if name == "begin":
                    if wrapper or (signature and not documentclass):
                        raise ValueError("misplaced/duplicate document wrapper")
                    wrapper, phase = True, "body"
                elif not wrapper or phase != "body":
                    raise ValueError("unmatched end of document")
                else:
                    phase = "after"
                values.append("document")
            else:
                if documentclass and phase != "body":
                    raise ValueError("driver command outside document wrapper")
                if name in DRIVER_HEADINGS or name in DRIVER_IMPORTS or name in DRIVER_IDS:
                    at = skip_space(ts, pos)
                    starred = False
                    if at < len(ts) and ts[at].value == "*":
                        if name not in {"olimport", "part", "chapter", "section", "subsection", "subsubsection"}:
                            raise ValueError("star not supported by this driver command")
                        starred = True
                        values.append("*")
                        pos = at + 1
                    if group(ts, pos, "[") is not None:
                        if (name in ("label", "ollabel") or
                                (name in DRIVER_IMPORTS and name != "olimport") or
                                (starred and name != "olimport")):
                            raise ValueError("optional argument not supported by this driver command")
                        values.append("[" + argument("[", name in DRIVER_HEADINGS) + "]")
                    required = DRIVER_HEADINGS.get(name, DRIVER_IDS.get(name, 1))
                    for index in range(required):
                        values.append(argument(title=name in DRIVER_HEADINGS and index == required - 1))
                    if name == "olimport" and group(ts, pos, "[") is not None:
                        values.append("[" + argument("[") + "]")
                    imports += name in DRIVER_IMPORTS
                    headings += name in DRIVER_HEADINGS
                elif name not in ("OLEndChapterHook", "OLEndPartHook"):
                    raise ValueError(f"unsupported driver command {tok.value}")
            signature.append((name, tuple(values)))
        if (wrapper and phase != "after") or (documentclass and not wrapper):
            raise ValueError("unclosed/missing document wrapper")
        if not imports:
            raise ValueError("a structural driver must contain at least one import")
    except ValueError as exc:
        errors = [str(exc)]
    return {"eligible": not errors, "errors": errors, "signature": signature,
            "imports": imports, "headings": headings}


def structural_review_records(data: dict | None, baseline: dict) -> dict:
    if data is None:
        return {}
    if (not isinstance(data, dict) or set(data) != {"schema", "units"} or
            data.get("schema") != STRUCTURAL_SCHEMA or not isinstance(data.get("units"), list)):
        raise ValueError("unsupported structural reviews schema/fields")
    known, records = {u["id"]: u for u in baseline["units"]}, {}
    for item in data["units"]:
        if not isinstance(item, dict) or set(item) != STRUCTURAL_FIELDS:
            raise ValueError("structural review requires exactly id, hashes, kind and note")
        uid = item["id"]
        if not isinstance(uid, str) or uid not in known or uid in records:
            raise ValueError("duplicate/unknown structural review identity")
        if item["kind"] != "heading-import-driver" or not isinstance(item["note"], str) or not item["note"].strip():
            raise ValueError("structural review requires driver kind and nonempty note")
        for field in ("arabic_sha256", "target_sha256"):
            if not isinstance(item[field], str) or not re.fullmatch(r"[0-9a-fA-F]{64}", item[field]):
                raise ValueError("invalid structural review hash")
        if item["arabic_sha256"].lower() != known[uid]["arabic_sha256"].lower():
            raise ValueError("structural review source hash differs from frozen baseline")
        records[uid] = item
    return records


def load_structural_reviews(path: Path) -> tuple[dict, str]:
    def unique_fields(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("duplicate JSON field in structural reviews: " + key)
            value[key] = item
        return value
    raw = path.read_bytes()
    return json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_fields), sha256(raw)


def apply_structural_review(result: dict, source: bytes, target: bytes, record: dict) -> None:
    """Add checks after compare(); NEVER discard or waive existing failures."""
    left, right = structural_driver(source.decode("utf-8")), structural_driver(target.decode("utf-8"))
    checks = {
        "structural_review_hashes": (record["arabic_sha256"].lower() == sha256(source) and
                                     record["target_sha256"].lower() == sha256(target)),
        "structural_driver_syntax": left["eligible"] and right["eligible"],
        "ordered_structural_driver_commands": left["signature"] == right["signature"],
    }
    result["checks"].update(checks)
    result["failures"].extend(name + " differs" for name, passed in checks.items() if not passed)
    result["structural_review"] = {"record": record, "source_errors": left["errors"],
                                   "target_errors": right["errors"], "validated": not result["failures"]}
    if result["failures"]:
        result["status"] = "flagged"
    else:
        result.update(status="structural-reviewed", expository_prose_present=False)


def validate(repo: Path, baseline: dict, selected: list[dict], declarations: dict | None = None,
             structural_reviews: dict | None = None,
             baseline_corrections: dict | None = None,
             baseline_sha256: str | None = None,
             formal_repairs: dict | None = None,
             baseline_corrections_sha256: str | None = None,
             general_reviews: dict | None = None,
             declarations_sha256: str | None = None,
             formal_repairs_sha256: str | None = None,
             structural_reviews_sha256: str | None = None) -> dict:
    corrections = baseline_correction_records(
        baseline_corrections, baseline, baseline_sha256, repo)
    effective_baseline = baseline
    if corrections:
        effective_units = []
        for unit in baseline["units"]:
            effective = dict(unit)
            if unit["id"] in corrections:
                correction = corrections[unit["id"]]
                effective.update(arabic_sha256=correction["current_msa_sha256"],
                                 arabic_bytes=correction["current_msa_bytes"])
            effective_units.append(effective)
        effective_baseline = {**baseline, "units": effective_units}
    formally_reviewed = formal_repair_records(
        formal_repairs, effective_baseline, baseline_sha256,
        baseline_corrections_sha256)
    reviewed = structural_review_records(structural_reviews, effective_baseline)
    generally_reviewed = general_review_records(
        general_reviews, effective_baseline, baseline_sha256,
        baseline_corrections_sha256, declarations_sha256,
        formal_repairs_sha256, structural_reviews_sha256)
    declared = {}
    if declarations is not None:
        if declarations.get("schema") != "openlogic-classical-exceptions-v1" or not isinstance(declarations.get("units"), list):
            raise ValueError("unsupported declarations schema")
        known = {u["id"] for u in baseline["units"]}
        for item in declarations["units"]:
            uid = item["id"]
            if uid in declared or uid not in known:
                raise ValueError("duplicate/unknown declaration identity: " + uid)
            declared[uid] = item
    results = []
    for unit in selected:
        result = {"id": unit["id"], "arabic_path": unit["arabic_path"], "target_path": unit["target_path"]}
        correction = corrections.get(unit["id"])
        if correction:
            result.update(baseline_correction=correction,
                          baseline_correction_applied=False)
        if unit["id"] in formally_reviewed:
            result["formal_repair_applied"] = False
        if unit["id"] in generally_reviewed:
            result["general_review_applied"] = False
        results.append(result)
        try:
            source_path = scoped_path(repo, unit["arabic_path"], "source/locale/ar/content")
            target_path = scoped_path(repo, unit["target_path"], "source/locale/ar-classical/content")
            source_bytes = source_path.read_bytes()
            source_hash = sha256(source_bytes)
            frozen_match = (source_hash.lower() == unit["arabic_sha256"].lower() and
                            len(source_bytes) == unit["arabic_bytes"])
            result.update(arabic_sha256=source_hash, arabic_bytes=len(source_bytes),
                          frozen_baseline_source_verified=frozen_match)
            identity_checks = {}
            if correction:
                effective_match = (source_hash == correction["current_msa_sha256"] and
                                   len(source_bytes) == correction["current_msa_bytes"])
                identity_checks.update(
                    baseline_correction_old_msa_identity=True,
                    effective_source_hash_and_bytes=effective_match)
                result.update(effective_source_verified=effective_match,
                              baseline_verified=effective_match,
                              checks=identity_checks)
                if not effective_match:
                    result.update(status="baseline-mismatch",
                                  failures=["effective Arabic bytes/hash differ from baseline correction"])
                    continue
            else:
                identity_checks["frozen_baseline_source_hash_and_bytes"] = frozen_match
                result.update(effective_source_verified=frozen_match,
                              baseline_verified=frozen_match,
                              checks=identity_checks)
                if not frozen_match:
                    result.update(status="baseline-mismatch", failures=["frozen Arabic bytes/hash differ"])
                    continue
            if not target_path.is_file():
                if correction:
                    identity_checks["baseline_correction_target_hash_and_bytes"] = False
                    result.update(status="flagged",
                                  failures=["baseline correction target is missing"],
                                  target_sha256=None)
                else:
                    result.update(status="flagged" if unit["id"] in reviewed else "pending-missing",
                                  failures=["structural review target is missing"] if unit["id"] in reviewed else [],
                                  target_sha256=None)
                continue
            target_bytes = target_path.read_bytes()
            target_hash = sha256(target_bytes)
            result.update(target_sha256=target_hash, target_bytes=len(target_bytes), byte_identical=source_bytes == target_bytes)
            if correction:
                target_match = (target_hash == correction["current_classical_target_sha256"] and
                                len(target_bytes) == correction["current_classical_target_bytes"])
                identity_checks["baseline_correction_target_hash_and_bytes"] = target_match
                if not target_match:
                    result.update(status="flagged",
                                  failures=["Classical target bytes/hash differ from baseline correction"])
                    continue
                result["baseline_correction_applied"] = True
            decl = declared.get(unit["id"])
            if decl and (decl.get("arabic_sha256", "").lower() != source_hash or decl.get("target_sha256", "").lower() != target_hash):
                raise ValueError("declaration source/target hashes do not match current bytes")
            comparison = compare(source_bytes.decode("utf-8"), target_bytes.decode("utf-8"), decl)
            result.update(comparison)
            result["checks"] = {**identity_checks, **comparison["checks"]}
            if unit["id"] in formally_reviewed:
                apply_formal_repair(result, source_bytes, target_bytes, comparison,
                                    formally_reviewed[unit["id"]])
            if unit["id"] in reviewed:
                apply_structural_review(result, source_bytes, target_bytes, reviewed[unit["id"]])
            if unit["id"] in generally_reviewed:
                apply_general_review(result, source_bytes, target_bytes, comparison,
                                     generally_reviewed[unit["id"]])
        except (OSError, UnicodeError, ValueError, KeyError, TypeError, AttributeError) as exc:
            result.update(status="flagged", failures=[str(exc)])
    counts = dict(sorted(Counter(r["status"] for r in results).items()))
    failed = any(r["status"] in ("flagged", "baseline-mismatch") for r in results)
    pending = any(r["status"] in ("pending-missing", "unchanged-prose", "structural-only-candidate") for r in results)
    selected_ids = {unit["id"] for unit in selected}
    correction_entries_selected = sorted(set(corrections) & selected_ids)
    correction_entries_applied = sorted(
        result["id"] for result in results if result.get("baseline_correction_applied"))
    formal_entries_selected = sorted(set(formally_reviewed) & selected_ids)
    formal_entries_applied = sorted(
        result["id"] for result in results if result.get("formal_repair_applied"))
    general_entries_selected = sorted(set(generally_reviewed) & selected_ids)
    general_entries_applied = sorted(
        result["id"] for result in results if result.get("general_review_applied"))
    return {"schema": "openlogic-classical-static-validation-v1",
            "status": "FLAGGED" if failed else "INCOMPLETE" if pending else "STATIC_CHECKS_SATISFIED",
            "exit_code": 1 if failed else 2 if pending else 0,
            "baseline_total_units": len(baseline["units"]), "selected_units": len(selected),
            "baseline_verified_units": sum(r.get("baseline_verified", False) for r in results),
            "effective_source_verified_units": sum(r.get("effective_source_verified", False) for r in results),
            "frozen_baseline_source_verified_units": sum(r.get("frozen_baseline_source_verified", False) for r in results),
            "baseline_correction_entries_declared": len(corrections),
            "baseline_correction_entries_selected": correction_entries_selected,
            "baseline_correction_entries_applied": correction_entries_applied,
            "baseline_correction_entries_failed_binding": sorted(
                set(correction_entries_selected) - set(correction_entries_applied)),
            "baseline_correction_entries_unused": sorted(set(corrections) - selected_ids),
            "formal_repair_entries_declared": len(formally_reviewed),
            "formal_repair_entries_selected": formal_entries_selected,
            "formal_repair_entries_applied": formal_entries_applied,
            "formal_repair_entries_failed_binding": sorted(
                set(formal_entries_selected) - set(formal_entries_applied)),
            "formal_repair_entries_unused": sorted(set(formally_reviewed) - selected_ids),
            "general_review_entries_declared": len(generally_reviewed),
            "general_review_entries_selected": general_entries_selected,
            "general_review_entries_applied": general_entries_applied,
            "general_review_entries_failed_binding": sorted(
                set(general_entries_selected) - set(general_entries_applied)),
            "general_review_entries_unused": sorted(set(generally_reviewed) - selected_ids),
            "counts": counts, "units": results, "limitations": LIMITATIONS,
            "structural_review_records_not_selected": sorted(set(reviewed) - {u["id"] for u in selected}),
            "semantic_equivalence_proven": False, "translation_completion_claim": False}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--ids")
    selection.add_argument("--all", action="store_true")
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--baseline", type=Path, help="default: REPO/evidence/classical/BASELINE.json")
    parser.add_argument("--baseline-corrections", type=Path,
                        help="explicit hash-bound frozen-baseline correction overlay; never auto-loaded")
    parser.add_argument("--formal-repairs", type=Path,
                        help="exact hash-bound prior audit of intentional formal differences")
    parser.add_argument("--declarations", type=Path)
    parser.add_argument("--structural-reviews", type=Path, help="explicit hash-bound heading/import driver reviews")
    parser.add_argument("--general-reviews", type=Path,
                        help="exact companion-bound reviews of unchanged prose only")
    parser.add_argument("--json", action="store_true", help="emit full machine-readable report to stdout only")
    args = parser.parse_args(argv)
    try:
        repo = args.repo.resolve()
        baseline_path = args.baseline or repo / "evidence/classical/BASELINE.json"
        baseline, baseline_hash = load_baseline(baseline_path)
        selected = selected_units(baseline["units"], args.ids)
        declarations, declarations_hash = (load_declarations(args.declarations)
                                            if args.declarations else (None, None))
        structural, structural_hash = load_structural_reviews(args.structural_reviews) if args.structural_reviews else (None, None)
        corrections, corrections_hash = (load_baseline_corrections(args.baseline_corrections)
                                         if args.baseline_corrections else (None, None))
        formal_repairs, formal_repairs_hash = (load_formal_repairs(args.formal_repairs)
                                               if args.formal_repairs else (None, None))
        general_reviews, general_reviews_hash = (load_general_reviews(args.general_reviews)
                                                 if args.general_reviews else (None, None))
        report = validate(repo, baseline, selected, declarations, structural,
                          baseline_corrections=corrections,
                          baseline_sha256=baseline_hash,
                           formal_repairs=formal_repairs,
                           baseline_corrections_sha256=corrections_hash,
                           general_reviews=general_reviews,
                           declarations_sha256=declarations_hash,
                           formal_repairs_sha256=formal_repairs_hash,
                           structural_reviews_sha256=structural_hash)
        if args.structural_reviews:
            report.update(structural_reviews_sha256=structural_hash,
                          structural_reviews_path=str(args.structural_reviews.resolve()))
        if args.baseline_corrections:
            report.update(baseline_corrections_sha256=corrections_hash,
                          baseline_corrections_path=str(args.baseline_corrections.resolve()),
                          baseline_corrections_schema=corrections["schema"])
        if args.formal_repairs:
            report.update(formal_repairs_sha256=formal_repairs_hash,
                          formal_repairs_path=str(args.formal_repairs.resolve()),
                          formal_repairs_schema=FORMAL_REPAIRS_SCHEMA)
        if args.declarations:
            report.update(declarations_sha256=declarations_hash,
                          declarations_path=str(args.declarations.resolve()))
        if args.general_reviews:
            report.update(general_reviews_sha256=general_reviews_hash,
                          general_reviews_path=str(args.general_reviews.resolve()),
                          general_reviews_schema=GENERAL_REVIEWS_SCHEMA)
        report.update(baseline_sha256=baseline_hash, baseline_path=str(baseline_path.resolve()))
        if args.json:
            print(json.dumps(report, ensure_ascii=True, indent=2))
        else:
            print(f"{report['status']}: {len(selected)}/{len(baseline['units'])} selected; "
                  f"{report['effective_source_verified_units']} effective Arabic files verified; "
                  f"{len(report['baseline_correction_entries_applied'])} baseline corrections applied")
            print(json.dumps(report["counts"], ensure_ascii=True, sort_keys=True))
            for unit in report["units"]:
                print(f"{unit['id']} {unit['status']}: " + "; ".join(unit.get("failures", [])))
            print("STATIC ONLY: no claim of translation completion, semantic equivalence, review or release.")
        return report["exit_code"]
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, AttributeError) as exc:
        print("Validation input error: " + str(exc), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
