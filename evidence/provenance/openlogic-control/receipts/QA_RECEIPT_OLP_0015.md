# Paired acceptance receipt — OLP-0015

Accepted 2026-08-13 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`, tree
`f67757bb9305b173634082ab4cefd5601a707a34`.

- Source: `content/sets-functions-relations/relations/equivalence-relations.tex`.
- Canonical LF Git blob: 3,387 bytes, SHA-256
  `D9531AA5CD774C12090FBD5C9FB289181E93CF7E9A96ECF7D4FD3FCDF5D250C7`.
- Declared CRLF materialization: 3,470 bytes, SHA-256
  `0B2167D0A9633938FD173D396F9E92B795826821471FF111483F7C7088A4BE46`.
- Scope: complete scheduling unit 15 of 722, not a corpus checkpoint.

## Arabic (`ar`)

- Target SHA-256:
  `6FDABF925A0040885042AC199609C5FCBB09C0BA6FBA50F08EA5997AEF9397B9`
  (4,364 bytes).
- Branch/commit: `codex/openlogic-ar`,
  `2894cb5d62609a854d2f0adb80c1f7e65d8b233c`.
- Terminology/adverse ledger SHA-256:
  `6D45C3E1420E0B038C3848616203EDD39AD4332B62FC74710782F0D53473C1DE`.

## Iranian Persian (`fa-IR`)

- Target SHA-256:
  `31012B00F34DF9F98B42C1A4A4F5C568A1304BFC35F886E07957731E7F72E623`
  (4,807 bytes).
- Branch/commit: `codex/openlogic-fa-ir`,
  `eb5107dc5fcd69cf20325486e576f0da645e8248`.
- Terminology/adverse ledger SHA-256:
  `2A532AAB12E8FBC36E2A89C220EBC74FF60A5089FABF3DD01E1DA02CA46F6C63`.

## Gate result and caveats

Independent paired replay passed after an opening sentence in each language
was made syntactically unambiguous that reflexivity, symmetry and transitivity
predicate the identity relation, not the underlying set. Both targets preserve
the exact 81-command sequence, 70 math spans, 14 environment events, label,
two glossary tokens and all formal notation.

Semantic replay passed the equivalence relation/class/quotient definitions,
the proposition's iff, both proof directions and inclusions, extensionality,
the modular-arithmetic existential witness, exact `n` class/member claims and
exercise. The source informally calls individual blocks “partitions”; each
translation distinguishes blocks from the whole partition. The source does
not explicitly state or prove coverage or pairwise disjoint-or-equal, so no
absent theorem was invented. Unicode, bidi, script and leakage gates passed.

Build remains deferred: OLP-0016--0019 are absent from the locale chapter
closures, so compiling now could import English. Independent AI replay passed;
human/native and specialist review are absent.

The shared cursor advances to OLP-0016,
`content/sets-functions-relations/relations/orders.tex`, declared CRLF SHA-256
`C6B7F7F49379F9CAC28D844270639EAE141152978EF8AD68065D0CFD83CCBD38`.
