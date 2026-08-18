# Paired acceptance receipt — OLP-0016

Accepted 2026-08-13 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`, tree
`f67757bb9305b173634082ab4cefd5601a707a34`.

- Source: `content/sets-functions-relations/relations/orders.tex`.
- Canonical LF Git blob: 6,308 bytes, SHA-256
  `79593789022FEF31C0609B9C94856E2AEF5CD5E88E92864E782BB6E6E5F4BCE4`.
- Declared CRLF materialization: 6,476 bytes, SHA-256
  `C6B7F7F49379F9CAC28D844270639EAE141152978EF8AD68065D0CFD83CCBD38`.
- Scope: complete scheduling unit 16 of 722, not a corpus checkpoint.

## Arabic (`ar`)

- Target SHA-256:
  `3A377CA5628676ECAD841D6663EB54FC262CF069BA797897BA569BF327D5A707`
  (8,728 bytes).
- Branch/commit: `codex/openlogic-ar`,
  `bf71c217228ffcb4896dee440083e31a5aac86e1`.
- Terminology/adverse ledger SHA-256:
  `13224EF3FEB023B24C499A866025EDB57EE58C44DE5BE1CC4B1CE29CF947023C`.

## Iranian Persian (`fa-IR`)

- Target SHA-256:
  `0BC6ED0711D80BC87911CF1A71A9A357FC0E9320EE6B19E4A3B91F8A2416414C`
  (9,124 bytes).
- Branch/commit: `codex/openlogic-fa-ir`,
  `988f777fc60285c12c5bf7180521da61c836e1eb`.
- Terminology/adverse ledger SHA-256:
  `089B75B8C9A18EE3CCDA80B3920E8E974EE024DFCCE369414AC1BCAD1AE19B3B`.

## Gate result and caveats

Independent paired replay passed without correction. Both targets preserve the
exact 181-command sequence, 117 math spans and 40 environment events: five
definitions, six examples, three propositions with proofs and one problem.
The five labels, reference and glossary token are exact.

Semantic replay passed the preorder--partial-order--linear-order hierarchy,
strict/non-strict conversions, relation-property distinctions, every example
and direction, both `R^+` and `R^-` constructions, inclusive connectivity and
the final proposition/proof with all quantifier scopes. The pinned source has
no well-order or least/minimal/greatest/maximal content despite earlier task
wording; both ledgers record the mismatch and neither target invents it.
Unicode, bidi, language-script and reader-facing-English gates passed.

The standalone unit is import-free, but cumulative relations compilation is
deferred because OLP-0017--0019 remain absent and English fallback is
prohibited. Independent AI replay passed; human/native and specialist review
are absent.

The shared cursor advances to OLP-0017,
`content/sets-functions-relations/relations/graphs.tex`, declared CRLF SHA-256
`A538018608CE97D0B371A392912C3D6825D8F3B17719BCECA5744A77ACE26351`.
