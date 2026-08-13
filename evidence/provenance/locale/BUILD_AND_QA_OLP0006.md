# OLP-0006 Arabic build and QA receipt

- Locale/register: `ar`, global formal Modern Standard Arabic.
- Unit: `OLP-0006`, `content/sets-functions-relations/sets/subsets.tex`.
- Source authority: official Open Logic commit
  `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`.
- Source SHA-256:
  `5D982F62C40325CF75DA4517ADD45CA073E23FB9463CFB3ADFB9AAFBB8582E46`.
- Target SHA-256:
  `1DC4A005B7F44CDFC46DBF485626BF76551EECBB108C7F822F41A2DF8A883AE5`.
- Locale config SHA-256:
  `744C2E9590E24E91D22FF31E825CC3D9575FDEC307B95069FF6E86DCB6B90BC2`.
- Terminology/adverse ledger SHA-256:
  `81D5C40A1ED0D749EB7305BECD425AB1905E6C91E629CB1E3C8AB96C6E7F04B5`.
- Localized section wrapper SHA-256:
  `19624BA16F68F26DF9732588668083E85D03B0FC6DDA4077EB43DD4EA734D3B3`.
- Unit build-config SHA-256:
  `FCBEF24C18BDD0DE6994757D07CD71E27C63E081344A70DA2CC147708D98E1D9`.

## Checks completed

- Direct semantic replay: PASS. The distinctions among membership, subset and
  proper subset; both inclusion/equality directions; the mutual-inclusion
  proposition; bounded universal and existential quantifiers; power-set
  inclusion; the eight subsets of a three-element set; and both unsolved
  problems are preserved.
- Structural replay: PASS for the exact 137-command sequence, 22 environment
  events, 14 semantic text tokens and all 65 math segments. The source label
  `forallxina` is retained and the localized ID is exactly
  `\olfileid[ar]{sfr}{set}{sub}`.
- Unicode/source checks: NFC, balanced braces, Arabic/Persian separation, no
  source-level bidi controls, no Arabic Presentation Forms and no unapproved
  English reader prose.
- Independent AI review directly against English: PASS; no correction
  required after the final faithful line-shortening. `human_review=none`.
- Build: two clean serial LuaLaTeX passes using LuaHBTeX 1.25.7 / MiKTeX 26.5.
  The final log has no fatal error, undefined control sequence, missing
  character, overfull box or underfull box.
- PDF: one Letter page, 98,662 bytes, SHA-256
  `D741C747D0EDEC7F11CAB964E60E26CB879B32629E7CAC7C53A0AB44E3043750`.
- PDF `/Lang` is `ar`; title is `المجموعات الجزئية ومجموعات القوى`;
  author is `مشروع المنطق المفتوح`; one localized outline entry and zero link
  annotations.
- Two-pass log SHA-256:
  `5E8836C33379D9AF63963CF42B5089A71851F2DA6CB5B936CB74F7F7D0BD04A5`.
- Complete-page visual QA at 144 dpi: PASS. No clipping, overlap, tofu,
  shaping failure, formula loss or mixed-direction collision was observed.
  Render witness SHA-256:
  `904E254718C09F95B3F3B767DF230DCD13E7866A180A56C0625CA8336B4C8C20`;
  the temporary PNG was deleted after inspection.
- Poppler layout extraction: 3,731 characters, zero U+FFFD and zero Arabic
  Presentation Forms; SHA-256
  `1AC1BB12C53596C5C4C080130741E876C1F6D8CE1D06FB57E06D65C32150948B`.

## Honest limits

The PDF is not tagged-PDF or accessibility certified. Extraction contains
Babel/LuaTeX directional controls (U+202A/U+202B/U+202C: 101/34/135), and
combining marks or punctuation may round-trip differently in other extractors.
The editable TeX is authoritative. This is unit 6 of a 722-unit closure, not a
complete Arabic edition or publication checkpoint.
