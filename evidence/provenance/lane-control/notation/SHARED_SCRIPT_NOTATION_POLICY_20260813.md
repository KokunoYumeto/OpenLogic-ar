# Shared-script mathematical notation policy

Status: active architecture, version 1.2, 2026-08-13. This policy standardizes semantic identity and rendering contracts. It does **not** create a common Arabic–Persian mathematical language. The current registry is a seven-entry worked foundation, not a complete inventory of Open Logic notation.

## Decision

Arabic, Iranian Persian, and other languages written in Arabic-derived scripts may share:

1. stable semantic IDs for mathematical objects and relations;
2. source TeX/MathML, operand order, quantifier scope, labels, and hashes;
3. typed rendering and QA infrastructure for mixed RTL/LTR text;
4. non-destructive search aliases.

They must not automatically share prose, terminology, orthography, digits, formula direction, operator names, spoken mathematics, or regional usage evidence. Script similarity is an engineering fact, not linguistic evidence.

This is the useful analogue to CJK coordination: share machine identity and infrastructure; preserve independently evidenced language and locale surfaces.

## Layer model

| Layer | Shared status | Rule |
|---|---|---|
| Semantic mathematics | global | Preserve AST, logical operands, quantifier scope, source formula and stable IDs. |
| Symbol identity | global | Bind TeX commands and Unicode identities without silently changing operands. |
| Script capability | reusable, explicitly inherited | Share bidi, shaping, font, extraction and accessibility test machinery. |
| Notation profile | locale-specific | Declare formula direction, digits, separators, mirroring and operator-name behavior. |
| Language surface | never pooled | Translate prose, terms, orthography and speech independently. |
| Regional aliases | evidence-bound | Keep aliases separate from the canonical surface and label their country/discipline evidence. |

## Governing rules

- Store text in Unicode logical order. Use directional isolation through markup or engine facilities, not copied visual order.
- For an `upstream-source` binding, `source_binding.sha256` is the SHA-256 of the exact LF Git-blob bytes at the declared commit. A checkout-materialization hash may be recorded separately, but must never be presented as the canonical Git-blob hash.
- Store counters as ordered integer components and render the complete counter as one directional run. Never isolate each component independently.
- Preserve source Latin identifiers and TeX commands unless an explicitly selected notation profile authorizes a different reader-facing representation.
- Never exchange `\in` and `\ni` merely because a layout is RTL. Operand order and the formula's declared direction control rendering.
- Keep semantic code-point rewriting separate from renderer-level glyph mirroring. A source relation is never replaced merely because Unicode's bidi renderer selects a mirrored glyph in an RTL formula profile.
- Never mirror an arrow automatically. Arrow direction may encode implication, morphism, a map, a transition, or absolute geometry.
- Treat CLDR number defaults as interface-localization evidence, not as a mathematical-notation mandate.
- Treat the 2006 W3C Arabic-mathematics Note as useful descriptive evidence, not as a universal or current regional default.
- Search aliases may bridge digit sets, transliterations, or regional terms. They must not rewrite canonical TeX/source or erase orthographic distinctions.
- Spoken-math and accessibility strings are language-specific even when a visible symbol is shared.
- A new Arabic-script language may inherit the engineering capability profile only. It must declare its own language, notation, orthography, terminology, and review evidence.

## Active Open Logic profiles

### `ar-core`

- Language surface: global formal Modern Standard Arabic (`ar`), RTL prose.
- Current source-faithful mathematics: LTR formula islands; source Latin identifiers and source digits retained.
- Canonical text is one pan-Arab MSA surface. Mashriq and Maghreb usages are search/terminology profiles unless a material incompatibility requires a sidecar.
- `ar-mashriq`, `ar-morocco-ltr`, and `ar-maghreb-rtl` are distinct evidence slots. None is inferred from another.

### `fa-IR`

- Language surface: scholarly Iranian Persian (`fa-IR`), RTL prose, independent from Arabic.
- Current source-faithful mathematics: LTR formula islands; source Latin identifiers and source digits retained.
- Persian `ی`/`ک` and meaningful ZWNJ are preserved. Arabic `ي`/`ك` are rejected in Persian prose.
- `arabext` digits are a supported future display/search profile, not an automatic rewrite of the accepted source-faithful edition.

## Required QA by surface

| Surface | Minimum tests |
|---|---|
| Prose | NFC; language-script leakage; shaping; line breaks; punctuation; copy/search witness. |
| Inline/display math | source token and operand parity; formula direction; delimiters; negation; quantifier scope. |
| Counters | `1.2`, `1.10`, `1.28`, `1.29`-class multi-digit replay in headings, references, TOC and extraction. |
| Diagrams | arrow semantics; labels; geometry; exact-resolution crops. |
| Search | aliases are additive; canonical orthography remains unchanged. |
| Speech/accessibility | language-specific strings; PDF/HTML tagging status stated honestly. |

The Persian Open Logic OLP-0001–0010 release supplied the first adverse test: theorem siblings rendered `1.10` as `10.1` when their numeric components were wrapped separately. The accepted remedy renders the entire chapter-relative counter in one LTR run and overrides every `thmtools` sibling presentation macro. This incident is retained as a regression case, not generalized into a claim that Persian and Arabic share one notation.

## Durable artifacts

- `notation-registry.schema.json`: type contract for semantic entries.
- `notation-profile.schema.json`: type contract for independent locale profiles.
- `SEMANTIC_NOTATION_REGISTRY.jsonl`: append-only source/release-bound entries.
- `ar.NOTATION_PROFILE.json` and `fa-IR.NOTATION_PROFILE.json`: current independent surfaces.

## Standards and evidence basis

- Normative Unicode algorithm: UAX #9, Unicode Bidirectional Algorithm, Unicode 17.0.0, revision 51: <https://www.unicode.org/reports/tr9/tr9-51.html>
- Normative Unicode data used for mirroring tests: BidiMirroring 17.0.0: <https://www.unicode.org/Public/17.0.0/ucd/BidiMirroring.txt>
- Normative Unicode script context: Unicode 17.0.0, Chapter 9: <https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-9/>
- W3C working draft, not a Recommendation: MathML 4 Working Draft, 4 June 2026: <https://www.w3.org/TR/2026/WD-mathml4-20260604/>
- Unicode proposed-draft guidance, not a normative language profile: UTR #25 revision 16 draft 2, mathematics and bidi layout: <https://www.unicode.org/reports/tr25/tr25-16d2.html>
- Historical descriptive evidence: W3C Arabic mathematical notation Note (2006): <https://www.w3.org/TR/2006/NOTE-arabic-math-20060131/arabic.html>
- Locale data, not mathematical authority: Unicode CLDR commit `8e4ea1bfdb01d2aa2e62f065eb49611cfc27a9f9`, for the declared `ar*` and `fa` profiles: <https://github.com/unicode-org/cldr/tree/8e4ea1bfdb01d2aa2e62f065eb49611cfc27a9f9/common/main>

No human/native review or community certification is claimed for this policy or the current profiles.
