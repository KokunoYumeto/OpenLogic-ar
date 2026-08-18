# Paired acceptance receipt — OLP-0017

Accepted 2026-08-13 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`, tree
`f67757bb9305b173634082ab4cefd5601a707a34`.

- Source: `content/sets-functions-relations/relations/graphs.tex`.
- Canonical LF Git blob: 2,939 bytes, SHA-256
  `DEC624EF4E71903B72A9F0B5FCC6A15A2E0F897F9EBE881DD9C9E21333AEEE75`.
- Declared CRLF materialization: 3,016 bytes, SHA-256
  `A538018608CE97D0B371A392912C3D6825D8F3B17719BCECA5744A77ACE26351`.
- Scope: complete scheduling unit 17 of 722, not a corpus checkpoint.

## Arabic (`ar`)

- Target SHA-256:
  `7F6F4A3E5FDC836DC728C076FC7B950D0C021420C60030434EC5D4C874EC55B7`
  (3,838 bytes).
- Branch/commit: `codex/openlogic-ar`,
  `291deeaea0124e599a7086d512148463fd863abc`.
- Terminology/adverse ledger SHA-256:
  `883631255B4D13428FBA7FD87B447267B611F9C7094FC696A266D1746CE0A236`.

## Iranian Persian (`fa-IR`)

- Target SHA-256:
  `AC1720531D8C88A61AFF40CE8A073BE18A8176016527EC906F8D7B493330D1B1`
  (4,075 bytes).
- Branch/commit: `codex/openlogic-fa-ir`,
  `c55bd17c61eac8d707c988e067845838c1df3fc8`.
- Terminology/adverse ledger SHA-256:
  `803AAD43B89AD079E0A7830C4DA4AC547ED95C3AD21C57F4FC18391427259456`.

## Gate result and caveats

Independent paired replay required both translations to state explicitly that
the directed edge is drawn from `v_1` to `v_2`; the corrected files then
passed. Graph/node/vertex/edge distinctions, `G=(V,E)`, `E\subseteq V^2`,
isolated vertices, relation-to-graph and graph-to-relation directions, both
examples and the problem are exact.

Both complete `tikzpicture` blocks are byte-identical to the canonical source:
seven node statements, eight draw statements, all arrows, loop, styles,
coordinates, identifiers and numeric labels. Exact command and environment
sequences pass. The source contains 52 dollar delimiters, hence 26 dollar-math
spans; the manifest's 27 counts those plus the containing `align*` surface.
Unicode, bidi, language-script and reader-facing-English gates passed.

Build and visual QA remain deferred because cumulative chapter dependency
closure is incomplete; no hidden English fallback is allowed. Independent AI
replay passed; human/native review is absent.

The shared cursor advances to OLP-0018,
`content/sets-functions-relations/relations/trees.tex`, declared CRLF SHA-256
`57CC56EE55506AA19E7BE6129D2CAD6B8635FD2D6407399D4F774782F2CDD588`.
