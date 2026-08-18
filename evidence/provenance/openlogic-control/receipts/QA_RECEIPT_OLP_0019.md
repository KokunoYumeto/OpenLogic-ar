# Paired acceptance receipt — OLP-0019

Accepted 2026-08-13 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`, tree
`f67757bb9305b173634082ab4cefd5601a707a34`.

- Source: `content/sets-functions-relations/relations/operations.tex`.
- Canonical LF Git blob: 2,163 bytes, SHA-256
  `73C8BDB301ACA93F687A06A045533D75D30088AE711F5E1DFD577B7864F8D3D5`.
- Declared CRLF materialization: 2,234 bytes, SHA-256
  `5E6F57E9DDF53E1624955ADABD594EA3855AD787C1074BA12421B0025B432372`.
- Scope: complete scheduling unit 19 of 722 and final dependency of the
  Relations chapter, not a corpus publication checkpoint.

## Arabic (`ar`)

- Target SHA-256:
  `C5C15F3B96FA635EB83E07675AD759E86EFA699A40314C76748CF8881C44F58D`
  (2,773 bytes).
- Branch/commit: `codex/openlogic-ar`,
  `4dda6571d6a982f6546596728e661c9118206e07`.
- Terminology/adverse ledger SHA-256:
  `C8D6B7E16DDB726726BA325CB069369399B474D14431073A879518E6B7EE869E`.

## Iranian Persian (`fa-IR`)

- Target SHA-256:
  `778A36272674FACCA8E2A2F77D2A1D299D073FD67B001F9E8813AB354B8F8A31`
  (3,047 bytes).
- Branch/commit: `codex/openlogic-fa-ir`,
  `7a39a16f4b15558d196a754456e8329611ed64aa`.
- Terminology/adverse ledger SHA-256:
  `646E81FB53721E7629B9C38C735DBB6F1136FB43CE60F210D42C8E01D4895429`.

## Gate result and caveats

Both targets preserve the exact 78-command, 12-environment and 48-math-span
sequences, the two references, one label and three source comments. Semantic
replay passed the swapped coordinates in the inverse relation, relative-product
order through the witness `y`, restriction to `A^2`, relational application,
successor/predecessor direction, recursive powers, transitive closure and
reflexive-transitive closure. Unicode, script separation, bidi-control,
presentation-form and reader-facing-English gates passed. Cross-locale
independent AI replay found no correction.

The complete historical Arabic terminology ledger has pre-existing non-NFC
combining-mark order at rows 90 and 103; the target and all five new OLP-0019
rows are NFC, so no broad unrelated normalization was performed. Human/native
and specialist review are absent. Build evidence is intentionally recorded in
the separate Relations chapter-integration receipt after both locale builds.

The shared cursor advances to OLP-0020,
`content/sets-functions-relations/functions/functions.tex`, declared CRLF
SHA-256 `CE481E97A8F301C749D1461326B4EE3D0792B4ADC15A1FCEB7C6ED3B58CECA54`.
