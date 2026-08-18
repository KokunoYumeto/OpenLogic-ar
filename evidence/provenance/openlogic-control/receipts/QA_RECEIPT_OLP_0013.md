# Paired acceptance receipt — OLP-0013

Accepted 2026-08-13 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`, tree
`f67757bb9305b173634082ab4cefd5601a707a34`.

- Source: `content/sets-functions-relations/relations/reflections.tex`.
- Canonical LF Git blob: 3,989 bytes, SHA-256
  `75047E8806A58C0A0C07AE2E55554D9AD2AFFB9D5297B1D5585EBE0B2F3DE651`.
- Declared CRLF materialization: 4,065 bytes, SHA-256
  `1F94C1032EAEDB73B1DE69E6F010B8E0C7437FE240AB280583FF358896FA4B27`.
- Scope: complete scheduling unit 13 of 722, not a corpus checkpoint.

## Arabic (`ar`)

- Target SHA-256:
  `C93FD3EF2CCEF6F3B0142174F955F93C05B6419A4484631EBB846A248BC0DA8A`
  (5,542 bytes).
- Branch/commit: `codex/openlogic-ar`,
  `2d8b67f9709562a751e79d730e265afeca9fcaeb`.
- Terminology/adverse ledger SHA-256:
  `B26309C656D3770CC80F2FCF72E0040B82315EC5E1C14FC512031995857B4D23`.

## Iranian Persian (`fa-IR`)

- Target SHA-256:
  `4A5D69C3C121AFD90C5BD54EB4A7D66128844F76ECED7D6BDBD7D38C3F5BF657`
  (5,998 bytes).
- Branch/commit: `codex/openlogic-fa-ir`,
  `516e06ebfbf8f2f583b56aff87f847e2567954c0`.
- Terminology/adverse ledger SHA-256:
  `E40FF4A3EB617C51BF2DF50067AE946BE4E3A47CE0E8A8DAEF229DF9CFC8AA9D`.

## Gate result and caveats

Final independent read-only replay passed. Both targets preserve the exact
87-command sequence, environment sequence, 24 inline math segments, two-row
aligned display, five references, citation, three-argument conditional and its
branch-local footnote. Formula order, tuple reversal, inequalities, membership
construction, reductio, double union and `Rxy` equivalence remain invariant.

Independent semantic replay preserved the source's distinction between a
discovered metaphysical identity and a contextual treatment, the two proposed
representations and extensionality dilemma, Benacerraf's reductionism point,
the membership-set special case, predicate/singular-name/proposition contrast,
Frege/Wittgenstein attribution and final treat-as conclusion. Persian register
and relative-clause corrections were incorporated before freeze. Arabic is
formal MSA. Unicode, bidi, script-separation and reader-facing-English gates
passed.

Build remains deferred: the relations chapter imports eight units and only
OLP-0012--0013 now exist in both locales, so compilation could import English
for OLP-0014--0019. Independent AI replay passed; no native Arabic/Persian
philosophical-logic review and no fresh render/extraction QA yet.

The shared cursor advances to OLP-0014,
`content/sets-functions-relations/relations/special-properties.tex`, declared
CRLF SHA-256
`F9BDFCB4C680EA58FDB209F0347C2F8055DE96558CAF69A26EC3CE8E1E7CE6A1`.
