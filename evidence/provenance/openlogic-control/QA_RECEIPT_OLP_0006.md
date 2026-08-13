# Paired acceptance receipt — OLP-0006

Accepted 2026-08-13 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`. Source unit
`content/sets-functions-relations/sets/subsets.tex` has SHA-256
`5D982F62C40325CF75DA4517ADD45CA073E23FB9463CFB3ADFB9AAFBB8582E46`.
This accepts scheduling unit 6 of the declared 722-unit closure; it is not a
complete edition or publication checkpoint.

## Arabic (`ar`)

- Target: `ar/locale/ar/content/sets-functions-relations/sets/subsets.tex`.
- Target SHA-256:
  `1DC4A005B7F44CDFC46DBF485626BF76551EECBB108C7F822F41A2DF8A883AE5`.
- Branch/commit: `codex/openlogic-ar`,
  `b0aac1d674eb68036b0f3691e5888742c64a754d`.
- Terminology/adverse ledger SHA-256:
  `81D5C40A1ED0D749EB7305BECD425AB1905E6C91E629CB1E3C8AB96C6E7F04B5`.
- Build/QA receipt SHA-256:
  `EDDA8A2E96FFB8AA7DDB25D400F199FACEF2D89743E99197D0936F9A9352B26B`.
- PDF: `ar/locale/ar/output/pdf/open-logic-olp0006-ar.pdf`, one Letter
  page, 98,662 bytes, SHA-256
  `D741C747D0EDEC7F11CAB964E60E26CB879B32629E7CAC7C53A0AB44E3043750`.
- Log/extraction SHA-256:
  `5E8836C33379D9AF63963CF42B5089A71851F2DA6CB5B936CB74F7F7D0BD04A5` /
  `1AC1BB12C53596C5C4C080130741E876C1F6D8CE1D06FB57E06D65C32150948B`.
- Complete-page render witness SHA-256:
  `904E254718C09F95B3F3B767DF230DCD13E7866A180A56C0625CA8336B4C8C20`.

## Iranian Persian (`fa-IR`)

- Target: `fa-IR/locale/fa-IR/content/sets-functions-relations/sets/subsets.tex`.
- Target SHA-256:
  `B8755941AFB97FC801C6FF9F03B54522AE64AC4D321DF207D77C1CE85AC1B4F4`.
- Branch/commit: `codex/openlogic-fa-ir`,
  `9913a32aa6383a82542e9e06a88cbb9e352f5caa`.
- Terminology/adverse ledger SHA-256:
  `2798CCB74460E6F5938F56E58714BB591BD13AE970DFD2FDA66CC7A2C3D249FB`.
- Build/QA receipt SHA-256:
  `C97884E50544AA7F1B68DCD0758E1B05C3DB776D7A3661BEFD4FBEEFC6BE197C`.
- PDF: `fa-IR/locale/fa-IR/output/pdf/open-logic-olp0006-fa-IR.pdf`, one
  Letter page, 97,145 bytes, SHA-256
  `43F48D1014ADD993170439E43ECF10D83E2C3DEAC3ABFD72F4405FEFC3BC76D6`.
- Log/extraction SHA-256:
  `C831B596B6E1CCB78CA859D30BF4110269C427CF7BD08628DC54A9A82EE724CE` /
  `3EF42D6D32A37A0AECA51D1D25AE10ACD1DB8AC8B5866A33CF60A613CC5F9A5E`.
- Complete-page render witness SHA-256:
  `9836AAC16953DB4FA263ECCE047DDEF01DB028B7E901FC513D51015A9E6AEDCC`.

## Gate result and caveats

Both targets pass direct source-bound semantic review; exact command,
environment, token and 65-math-segment replay; localized stable IDs; script and
Unicode checks; clean two-pass LuaLaTeX builds; localized `/Lang`, title,
author and outline inspection; complete-page visual QA; and final independent
AI admission replay. The Persian wrapper additionally passed a read-only delta
review after isolating complete Latin counter strings so the visual PDF keeps
`set.1` order in RTL headings.

`human_review=none`. Neither PDF is tagged-PDF or accessibility certified.
Arabic extraction can alter mark/punctuation order; Persian extraction drops
source ZWNJs and may serialize visually correct counters as `1.set`. Editable
TeX is authoritative for text. The shared accepted cursor now advances to
`OLP-0007`, `content/sets-functions-relations/sets/important-sets.tex`,
SHA-256
`B1B998CAD3FA5AEF48670F755245F86EFE00B239D332A50E764147602405FB32`.
`publication_checkpoint_ready=false`.
