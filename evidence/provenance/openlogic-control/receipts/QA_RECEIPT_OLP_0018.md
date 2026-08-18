# Paired acceptance receipt — OLP-0018

Accepted 2026-08-13 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`, tree
`f67757bb9305b173634082ab4cefd5601a707a34`.

- Source: `content/sets-functions-relations/relations/trees.tex`.
- Canonical LF Git blob: 5,102 bytes, SHA-256
  `A158F1CE5B84C8C3F681DD6347B22491D1B67A91E110138B9CB6833E3D9DC23C`.
- Declared CRLF materialization: 5,232 bytes, SHA-256
  `57CC56EE55506AA19E7BE6129D2CAD6B8635FD2D6407399D4F774782F2CDD588`.
- Scope: complete scheduling unit 18 of 722, not a corpus checkpoint.

## Arabic (`ar`)

- Target SHA-256:
  `FD4BC394C59ED5044038788E5A79F93166BC724385A974DF60EF638218888F69`
  (6,973 bytes).
- Branch/commit: `codex/openlogic-ar`,
  `d68f3d53c6310343eb3f4964c7a373f8525f2f5a`.
- Terminology/adverse ledger SHA-256:
  `F917A02806E55EFF6D33AE032A3A89FF9C99EFA9C40953B9509667C508E08F27`.

## Iranian Persian (`fa-IR`)

- Target SHA-256:
  `00CA638DF2B0753439EE7F6D3C976A0B26ABC8899A7695EFBB904841FAB4F39C`
  (7,347 bytes).
- Branch/commit: `codex/openlogic-fa-ir`,
  `ad642569359f52525300a97cfd9800428d310a79`.
- Terminology/adverse ledger SHA-256:
  `3D014B30765FB9116BC215B72D08312DAB291EE39AF60DCEAA39D5D7E8BCD04F`.

## Gate result and caveats

Independent final replay passed after Arabic universal-scope/terminology
hardening and three Persian prose corrections: least-element syntax,
finite-successor phrasing and removal of English plural suffixes from the
binary-sequence prose. Both targets preserve all 109 math spans, the exact
119-command and 24-environment sequences, four definitions, two propositions,
one proof, two examples and four OLP marker tokens.

Semantic replay passed the tree/root/ancestor order, least element and
well-order definitions, successor/predecessor direction, uniqueness proof,
finite branching, maximal branches, binary and natural-sequence trees, and
both König statements. The source uses undefined `X` in
`z \in X \setminus B` after declaring carrier `A`; both translations preserve
the exact source token and ledger the likely defect instead of silently fixing
it. The complete TikZ block is byte-identical in both targets, SHA-256
`F122123B1F5663CDDCF11087601733429738DAA819BFA509887E9750EFCF8E7C`.
Unicode, bidi, script and reader-facing-English gates passed.

Cumulative build/render remains deferred because OLP-0019 is still absent;
English fallback is prohibited. Independent AI replay passed; human/native and
specialist review are absent.

The shared cursor advances to OLP-0019,
`content/sets-functions-relations/relations/operations.tex`, declared CRLF
SHA-256 `5E6F57E9DDF53E1624955ADABD594EA3855AD787C1074BA12421B0025B432372`.
