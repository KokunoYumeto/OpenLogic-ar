# Paired acceptance receipt — OLP-0005

Accepted 2026-08-13 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`. Source unit
`content/sets-functions-relations/sets/basics.tex` has SHA-256
`8BC9151AF0985E6E20C374AA38CDDD1ADD7A8DFFBABCCC94B89F324F62C40F8C`.
This accepts scheduling unit 5 of the declared 722-unit closure; it is not a
complete edition or publication checkpoint.

## Arabic (`ar`)

- Target: `ar/locale/ar/content/sets-functions-relations/sets/basics.tex`.
- Target SHA-256:
  `1175854930480BAFE2EAA2853E068665C083589A4BAF03ACBF55E781FF3E013F`.
- Branch/commit: `codex/openlogic-ar`,
  `e9b739f5dd77ff18b3cb47924c6f168bb8a1e2e1`.
- Terminology/adverse ledger SHA-256:
  `2D292C0BE45D720C47DE5E00FD59E7A311B633902337BC0120A6B0D9F61A91E2`.
- Build/QA receipt SHA-256:
  `7D52FDEA45B3BBB05B55AA5BEA2966CB56DDDB818B7277DE148A35B81688FBA3`.
- PDF: `ar/locale/ar/output/pdf/open-logic-olp0005-ar.pdf`, one Letter
  page, 101,398 bytes, SHA-256
  `16A2BABF64BBCF5828AEAF6B25FA385A9CB270F7B5DBA4BDBC6836BA8E205F6C`.
- Log/extraction SHA-256:
  `57B5A40790A5D08402FDD5DC7FB080614764149837BE80BE5290DE622F2C8E9A` /
  `A8AB917657C2E5619B4B0992606A0D4BAAD78BD30A051DDD9D83349CD95BF62D`.
- Complete-page render witness SHA-256:
  `D26340E9B90744A328716CFF4106BE2AAAC1843C82E55E9FC119630E9BDE2B57`.

## Iranian Persian (`fa-IR`)

- Target: `fa-IR/locale/fa-IR/content/sets-functions-relations/sets/basics.tex`.
- Target SHA-256:
  `129320E9EEA66762B41C28C6970DBAC6A87D84433AEC529A18BDE8AE903F849C`.
- Branch/commit: `codex/openlogic-fa-ir`,
  `bd069c68afbe5e6793ae3868f50763491400aa4b`.
- Terminology/adverse ledger SHA-256:
  `57927CE90D40A51B21B4DAD86DBDDC4CD5A94D867CC0FD9C0E92A1940D3E5FD0`.
- Build/QA receipt SHA-256:
  `307F9DDC46CBF6CDC7FE1C8A2743E6834B84422B414B71C87535D297F9B7B719`.
- PDF: `fa-IR/locale/fa-IR/output/pdf/open-logic-olp0005-fa-IR.pdf`, one
  Letter page, 99,043 bytes, SHA-256
  `D6A1B72BC058E8B8B3A33CF6337E53B0128B4D63A6D4AA32520B18216BB49FD9`.
- Log/extraction SHA-256:
  `C4376540EB1BB3F00C8DC49ACA4F9AEA4267B758CB1978B8C8676D9EFF367F12` /
  `9B830BBCC8EA366BCB89137CA5AE69D2AD9477666A8D874DE2B3D5CC0FB858D9`.
- Complete-page render witness SHA-256:
  `E360255AF7C66088D7B87D20F66B3F31B78D1CAF85747758E7850A56335657F4`.

## Gate result and caveats

Both targets pass direct source-bound semantic review; exact command,
environment, token and 52-math-segment replay; localized stable IDs; script
and Unicode checks; clean two-pass LuaLaTeX builds; localized `/Lang`, title,
author and outline inspection; complete-page visual QA; and final independent
AI admission replay. The source inconsistency between “less than 10” and the
displayed `0 \leq x \leq 10` is preserved and ledgered in both targets.

`human_review=none`. Neither PDF is tagged-PDF or accessibility certified.
Arabic extraction can alter mark/punctuation order; Persian extraction drops
source ZWNJs. Editable TeX is authoritative. The shared accepted cursor now
advances to `OLP-0006`, `content/sets-functions-relations/sets/subsets.tex`,
SHA-256
`5D982F62C40325CF75DA4517ADD45CA073E23FB9463CFB3ADFB9AAFBB8582E46`.
`publication_checkpoint_ready=false`.
