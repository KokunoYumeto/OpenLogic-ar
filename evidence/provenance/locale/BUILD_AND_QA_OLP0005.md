# OLP-0005 Arabic build and QA receipt

- Locale/register: `ar`, global formal Modern Standard Arabic.
- Unit: `OLP-0005`, `content/sets-functions-relations/sets/basics.tex`.
- Source authority: official Open Logic commit
  `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`.
- Source SHA-256:
  `8BC9151AF0985E6E20C374AA38CDDD1ADD7A8DFFBABCCC94B89F324F62C40F8C`.
- Target SHA-256:
  `1175854930480BAFE2EAA2853E068665C083589A4BAF03ACBF55E781FF3E013F`.
- Locale config SHA-256:
  `744C2E9590E24E91D22FF31E825CC3D9575FDEC307B95069FF6E86DCB6B90BC2`.
- Terminology/adverse ledger SHA-256:
  `2D292C0BE45D720C47DE5E00FD59E7A311B633902337BC0120A6B0D9F61A91E2`.
- Localized section wrapper SHA-256:
  `19624BA16F68F26DF9732588668083E85D03B0FC6DDA4077EB43DD4EA734D3B3`.
- Unit build-config SHA-256:
  `BCE7C8209E2D735F5C86581F93F29A1415CA010F4438FDEA35C619D04ADA6355`.

## Checks completed

- Direct semantic replay: PASS. Set, element/member, membership and empty-set
  definitions; order and multiplicity independence; both directions of
  extensionality; uniqueness; all three examples; set-builder notation;
  perfect number and proper divisor; equality proof method; and the
  at-most-one-empty-set problem are preserved.
- The source mismatch between prose “less than 10” and the displayed
  `0 \leq x \leq 10` is preserved exactly and recorded as adverse evidence.
- Structural replay: PASS for the 91-command sequence, 20 environment events,
  three tagblocks, 14 text tokens and all 52 math skeletons. The base ID is
  unchanged and the upstream-required locale marker is
  `\olfileid[ar]{sfr}{set}{bas}`.
- Unicode/source checks: NFC, balanced braces, Arabic/Persian separation, no
  source-level bidi controls, no Arabic Presentation Forms, and no unapproved
  English reader prose.
- Independent AI review directly against English: PASS; no correction
  required. `human_review=none`.
- Build: two clean serial LuaLaTeX passes using LuaHBTeX 1.25.7 / MiKTeX 26.5.
  The log has no fatal error, undefined control sequence, missing character,
  overfull box or underfull box.
- The reader wrapper intentionally omits upstream `open-logic-debug.sty`,
  which adds coloured token/margin diagnostics and is not reader content.
- PDF: one Letter page, 101,398 bytes, SHA-256
  `16A2BABF64BBCF5828AEAF6B25FA385A9CB270F7B5DBA4BDBC6836BA8E205F6C`.
- PDF `/Lang` is `ar`; title is `الامتدادية`; author is
  `مشروع المنطق المفتوح`; one localized outline entry and zero link
  annotations.
- Two-pass log SHA-256:
  `57B5A40790A5D08402FDD5DC7FB080614764149837BE80BE5290DE622F2C8E9A`.
- Complete-page visual QA at 144 dpi: PASS. No clipping, overlap, tofu,
  shaping failure, formula loss or mixed-direction collision was observed.
  Render witness SHA-256:
  `D26340E9B90744A328716CFF4106BE2AAAC1843C82E55E9FC119630E9BDE2B57`;
  the temporary PNG was deleted after inspection.
- Poppler layout extraction: 3,782 characters, zero U+FFFD and zero Arabic
  Presentation Forms; SHA-256
  `A8AB917657C2E5619B4B0992606A0D4BAAD78BD30A051DDD9D83349CD95BF62D`.

## Honest limits

The PDF is not tagged-PDF or accessibility certified. Extraction contains
Babel/LuaTeX directional controls (U+202A/U+202B/U+202C: 106/34/140), and
combining marks or punctuation may round-trip differently in other extractors.
The editable TeX is authoritative. This is unit 5 of a 722-unit closure, not a
complete Arabic edition or publication checkpoint.
