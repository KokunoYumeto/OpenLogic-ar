# Paired acceptance receipt — OLP-0010

Accepted 2026-08-13 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`. Source unit
`content/sets-functions-relations/sets/russells-paradox.tex` has SHA-256
`9A76315CD0D9CF89D27E90A9B87138B1C95AEA98E0D26DE3FE12D897B8C4D10D`.
This accepts scheduling unit 10 of the declared 722-unit closure. It closes
the first translated chapter but is not a complete corpus edition.

## Arabic (`ar`)

- Target SHA-256:
  `842DBAA2AAE165CE42B1999DDE89D621F4E90E4A60D72781879C5B878E9B9D56`.
- Branch/commit: `codex/openlogic-ar`,
  `1b681e8e41402b8e2dd5b29958daa6e05227a246`.
- Terminology ledger / locale build receipt SHA-256:
  `E1EB3362355C45781E4905E0C29A25929EF40A0BE7848D977E22687F218FB64C` /
  `71D6291FDBF0A7FC0D82D4D1BB35575BC931DBF524FCCC5553F745412FCD871A`.
- PDF: one Letter page, 79,349 bytes, SHA-256
  `F379234EAB22DF89DD27A6E5BFA21580C09FB4AB58F955421D0C78EA83BE0FED`.
- Log / extraction SHA-256:
  `DFA08437E223B6FB73CCE8322E3AB03E961DC4905BD16EF5C479A1FB50366A24` /
  `99F86808994759DA5332FB31A5B64A3E301FD7CFD85120C4724FAF375D4FE377`.
- Full-page 180-dpi render witness SHA-256:
  `6BFA0AFED4B0290C990980F945FB69643AC445FBF40C485608F9BE98D5E95BF1`.

## Iranian Persian (`fa-IR`)

- Target SHA-256:
  `040B0431DA0D24CE6CFC12BDFCBD1B0970E8FD9397A4A6FB3D8EF36B93287886`.
- Branch/commit: `codex/openlogic-fa-ir`,
  `f9494a5123d7c2802859b700067af1d519f4bf26`.
- Terminology ledger / locale build receipt SHA-256:
  `E71B8975B1278D687B040C552AB75F1E3DBF49F9CD4B377594DAD10DB52821B0` /
  `0070B8F3482886DD9192D16E2842D95FA96EDAEBC75E0882DA2E8D5001CEA9FA`.
- PDF: one Letter page, 79,593 bytes, SHA-256
  `31A1E1D8319DAE9F04536ACC1C129B49184E7C69B369F8A6D7323C8EEF204368`.
- Log / extraction SHA-256:
  `C8A26C046EDC72DD48153E1A08CD600F64801EB83D3C2D4219C532F56A26BB79` /
  `E7A0E9E8DD4EBB7547A35D8F8F02C43F025159F97CE7098B394C013F8574800A`.
- Full-page 180-dpi render witness SHA-256:
  `230E2DBE13B73ABB006B25C766803AC105966E4BA33ABD08C71B0EA86BDE9FC0`.

## Gate result and caveats

Both targets pass direct and independent source-bound semantic review; exact
55-command, 12-environment, 10-token and 34-math-segment replay; label and
conditional-reference checks; script/Unicode checks; clean two-pass LuaLaTeX
builds; localized metadata/outlines; and complete-page visual QA. The Arabic
target passed a post-correction replay after an initially ambiguous final
membership sentence was made explicitly bipolar. `human_review=none`.

The source's typographic oddities were preserved or recorded rather than
silently repaired. Neither PDF is tagged-PDF or accessibility certified.
Persian extraction drops all source ZWNJs; all visible `\notin` symbols
serialize imperfectly from the Type-1 math fonts; and cross-extractor RTL order
is inconsistent. Editable TeX is authoritative.

The shared accepted cursor advances to `OLP-0011`,
`content/sets-functions-relations/relations/relations-complete.tex`, SHA-256
`7E1363F3E757004246334478742E4199101DBB2551FAC272462454CD40161E23`.
Before translating that unit, the lane will issue separately discoverable
Arabic and Persian cumulative reader checkpoints through OLP-0010, each with
editable-source and complete audit/provenance bundles.
