# Paired acceptance receipt — OLP-0014

Accepted 2026-08-13 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`, tree
`f67757bb9305b173634082ab4cefd5601a707a34`.

- Source: `content/sets-functions-relations/relations/special-properties.tex`.
- Canonical LF Git blob: 3,081 bytes, SHA-256
  `006F2EA0D65E5069EF1509DE94DD35A477EA835C19962DA22F4BEF48CAFFBEE7`.
- Declared CRLF materialization: 3,165 bytes, SHA-256
  `F9BDFCB4C680EA58FDB209F0347C2F8055DE96558CAF69A26EC3CE8E1E7CE6A1`.
- Scope: complete scheduling unit 14 of 722, not a corpus checkpoint.

## Arabic (`ar`)

- Target SHA-256:
  `10C6E4D1845FCB0220553EBE25D77A5707E8E763F11A6445529C4C91C3464CBB`
  (4,304 bytes).
- Branch/commit: `codex/openlogic-ar`,
  `00010006efeb4b82cd8b29865a93e53a8ccf5371`.
- Terminology/adverse ledger SHA-256:
  `7FA120EE6D24B928043B08485AAE85EBDA46CD589F3487865AF84F0DE8A72735`.

## Iranian Persian (`fa-IR`)

- Target SHA-256:
  `2982561D7DBE451703FA9F71D034CB84E9E83C846EF4FA21B408079BA73D0860`
  (4,619 bytes).
- Branch/commit: `codex/openlogic-fa-ir`,
  `bce5699b55af18235c21b7d3222cbf6dd89731f5`.
- Terminology/adverse ledger SHA-256:
  `E35C9A563397810DAE0C7764EBAABEBE08F0439010E6D1BEE814EB45C3BBB767`.

## Gate result and caveats

Independent paired replay passed after a Persian connectivity phrase that
could imply exclusive disjunction was changed to explicit inclusive “at least
one.” Both final targets preserve the exact 59-command sequence, 22 environment
boundaries, seven definitions, 47 math spans, eight emphasis sites, all
quantifier/negation scopes, example, problem parts (a)--(d), and closing claims.

Semantic replay kept symmetric, antisymmetric, asymmetric and merely
nonsymmetric distinct; likewise irreflexive versus merely nonreflexive.
Connectedness applies only to distinct pairs and its disjunction is inclusive;
asymmetry quantifies all pairs, including equal arguments. The source's closing
scope/vacuity nuance was preserved, not silently strengthened. Unicode, bidi,
language-script separation and reader-facing-English checks passed.

Build remains deferred: OLP-0015--0019 are still absent from both locale
chapter closures, so cumulative compilation could import English. Independent
AI replay passed; human/native and specialist review are absent.

The shared cursor advances to OLP-0015,
`content/sets-functions-relations/relations/equivalence-relations.tex`, declared
CRLF SHA-256
`0B2167D0A9633938FD173D396F9E92B795826821471FF111483F7C7088A4BE46`.
