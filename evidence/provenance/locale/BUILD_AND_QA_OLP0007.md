# OLP-0007 Arabic build and QA receipt

- Locale/register: `ar`, global formal Modern Standard Arabic.
- Unit: `OLP-0007`, `content/sets-functions-relations/sets/important-sets.tex`.
- Source authority: official Open Logic commit
  `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`.
- Source SHA-256:
  `B1B998CAD3FA5AEF48670F755245F86EFE00B239D332A50E764147602405FB32`.
- Target SHA-256:
  `C9A36E2DBBD89674A4F13784EC149DD93EF2F94881B67AAC62D38FF028C9A3EF`.
- Locale config / terminology ledger SHA-256:
  `744C2E9590E24E91D22FF31E825CC3D9575FDEC307B95069FF6E86DCB6B90BC2` /
  `8A7B0E58532106BA54282C022B2470DDD41F9110A1DA229C9324FF56DEF25343`.
- Section wrapper / unit build-config SHA-256:
  `19624BA16F68F26DF9732588668083E85D03B0FC6DDA4077EB43DD4EA734D3B3` /
  `B5DA16192152733F61E362DB81C65DCFB40FD6F558B3E52973AE2B046A0698A7`.

## Checks completed

- Direct semantic replay: PASS. The natural, integer, rational and real number
  systems; inclusion directions and strictness witnesses; conditional real-line
  reference; positive integers and binary digits; finite strings, empty string,
  enumeration and length; and one-way infinite sequences are preserved.
- Structural replay: PASS for 95 commands, 14 environment events, four text
  tokens and all 26 math segments, including both multiline displays and five
  localized math-internal text fields. Locale ID, `compsci` tag and conditional
  label/reference are exact.
- Unicode/source checks: NFC, balanced braces, Arabic/Persian separation, no
  source bidi controls or Presentation Forms and no English reader fallback.
- Independent AI review directly against English: PASS. `human_review=none`.
- Build: two clean serial LuaLaTeX passes using LuaHBTeX 1.25.7 / MiKTeX 26.5;
  no fatal error, undefined control sequence, missing character, overfull box or
  underfull box.
- PDF: one Letter page, 112,770 bytes, SHA-256
  `C0E896E10123AE76078A8B3147F6EC2D2822D32DBCA6127BE1F1D0138AF0AC62`.
  `/Lang=ar`; localized title/author and one localized outline; zero links.
- Log SHA-256:
  `2B23BEC9F6C77EAF0675EABDE1F9CB4AF002B13E133F4A9BDCCD941246D65C87`.
- Every page rendered at 144 dpi and visually inspected: PASS for shaping,
  margins, mixed-direction formulas, inclusion signs, binary enumeration and
  stable identifiers. Render witness SHA-256:
  `566ED56CDAE6ABC9C14021D5CA3C18B1B1927ADA34F9BF3E61179620DDB1F2A8`;
  temporary PNG deleted after inspection.
- Poppler layout extraction: 2,837 characters, zero U+FFFD and zero Arabic
  Presentation Forms; SHA-256
  `3C058A6D5AF7F36CBBDF1595DD1AB49990CDBDC750D87BE7D267CE31CF2C2C86`.

## Honest limits

The PDF is not tagged-PDF or accessibility certified. Extraction contains
directional controls (U+202A/U+202B/U+202C: 53/29/82) and may alter combining
marks or punctuation. Editable TeX is authoritative. This is unit 7 of 722,
not a complete Arabic edition or publication checkpoint.
