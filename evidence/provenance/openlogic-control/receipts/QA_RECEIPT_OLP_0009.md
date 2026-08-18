# Paired acceptance receipt — OLP-0009

Accepted 2026-08-13 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`. Source unit
`content/sets-functions-relations/sets/pairs-and-products.tex` has SHA-256
`3DB7F0241D387B49488F70E78062C24192B813873618F761565D97BD7249431C`.
This accepts scheduling unit 9 of the declared 722-unit closure; it is not a
complete edition or publication checkpoint.

## Arabic (`ar`)

- Target SHA-256:
  `0209ACCAD5BA65DA9955892285D637EC9B4DA5B98D8C7830695BE6F8161B6809`.
- Branch/commit: `codex/openlogic-ar`,
  `d0c5df46857ed209376dc4b08f1c18e066394e0b`.
- Terminology ledger / locale build receipt SHA-256:
  `4C070E93E6AAAC9DC3AC9EC001B20437B3AABC087D722E01B88C93FDF7CB634D` /
  `1667E9CD7EE91767F4E8BFB94C317F6965C7F41D2DFE3AECB291163CD2C2B927`.
- PDF: two Letter pages, 135,231 bytes, SHA-256
  `EA09C95D64030EE95C6210B21546C602F9F7A93DBB641168689EE80C8A637030`.
- Log / extraction SHA-256:
  `C390388743897FE26C209811CDDD7B8029AD0B6C8100844895BEC8107340A7A8` /
  `57DDAD0B4355B551B1A80657A69BCF8FB220C95C36669AFF2C2EE8C398A305F0`.
- Two full-page render witness SHA-256 values:
  `F0A8BF210618AD52B3F0EEF0457C224DDE311D327DFF30604DD8F3606BE494F0`,
  `D04FD20C8616730F8DB4C5343CF52999F925ACCB429B3DCF36EE834582F35714`.

## Iranian Persian (`fa-IR`)

- Target SHA-256:
  `9474699C22D159D4F715B48E49B727E9BEAD8AE93F3BEBBD62C1CBD186C92BC5`.
- Branch/commit: `codex/openlogic-fa-ir`,
  `019a8c592ce5797e7f73e277d42871487327d1de`.
- Terminology ledger / locale build receipt SHA-256:
  `3FC6A4B6D0F8AC569C4362E36A2BC1DCEBBD39827CF52761E03CB2E415D97189` /
  `B0E8890ABB35FBADB6CB63544DB727D300461DA5670FFA2F41F0F320C26449FE`.
- PDF: two Letter pages, 133,844 bytes, SHA-256
  `94D935230548E75B1E411C12FA24A4154F22DA923A96CC42743F84A3D705F4FB`.
- Log / extraction SHA-256:
  `82CE0EF56563CAC5B02045D27CC4B3705678233DC42A73A248FC8F573F952B8D` /
  `C4B951A613CC0008AFECFD67BEEA5B596B376058EDD259E1F39EE1BF44A1F40F`.
- Two full-page render witness SHA-256 values:
  `7E3F3D0C345755150FB534AC3C668113AC4D433E2494DE81A96BB3BC199191E7`,
  `CDB92623EC2BA39043ED1C60EB209FA196601C1910146DA3481411ACB47129BE`.

## Gate result and caveats

Both targets pass direct and independent source-bound semantic review; exact
177-command, 30-environment, 12-token and 78-math-segment replay; labels,
reference, array and localized IDs; script/Unicode checks; clean two-pass
LuaLaTeX builds; localized metadata and outlines; internal-link inspection;
and complete-page visual QA.

The source's same-coordinate notation in the disjointness proof, implicit
enumeration of `B`, broad “any sequence” wording and `\emptyset` empty-sequence
convention were preserved and documented rather than silently repaired.
`human_review=none`. Neither PDF is tagged-PDF or accessibility certified.
Extraction contains bidi controls; Persian extraction drops source ZWNJs;
pypdf emits two U+FFFD characters from the Arabic body; and mathematical
copy/paste is imperfect. Editable TeX is authoritative.

The shared accepted cursor advances to `OLP-0010`,
`content/sets-functions-relations/sets/russells-paradox.tex`, SHA-256
`9A76315CD0D9CF89D27E90A9B87138B1C95AEA98E0D26DE3FE12D897B8C4D10D`.
`publication_checkpoint_ready=false`.
