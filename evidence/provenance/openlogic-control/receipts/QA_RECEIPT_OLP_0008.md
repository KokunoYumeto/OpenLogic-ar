# Paired acceptance receipt — OLP-0008

Accepted 2026-08-13 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`. Source unit
`content/sets-functions-relations/sets/unions-and-intersections.tex` has
SHA-256
`2AD0EEC70308CEEFF2A4158B2DEE60E59A9B1CF9268FC95C4BB1DA05F65AD60D`.
This accepts scheduling unit 8 of the declared 722-unit closure; it is not a
complete edition or publication checkpoint.

## Arabic (`ar`)

- Target SHA-256:
  `112BCA7B160608FE147114AE1BEE0EB4E18406B0BF9D312A705B8FA2D62D2025`.
- Branch/commit: `codex/openlogic-ar`,
  `949b35a5032397fc6efedf9c1e0f51fc439a3994`.
- Terminology ledger / locale build receipt SHA-256:
  `5D320247259B275FC70641EBB44FA19B9444E47C0F2BC52243A82BD781351915` /
  `52CD25CA55F3524F6D1D480D539C2BC78D3B3304A25FC3BA240C4364CE9F8D15`.
- PDF: three Letter pages, 134,996 bytes, SHA-256
  `324922ECA3469F4094C869ED877C3C95A22A5CEE813E9FAAE583CF167A6E5D05`.
- Log / extraction SHA-256:
  `0B9A7EF298EB5B45E0E971A7CE013BD7602380112E129FF9692E74F43D4081E3` /
  `149236ED2F00C2FF54706FF5BC3F0567F01E79BFB06A32FB8A1CB1139029E25D`.
- Three full-page render witness SHA-256 values:
  `CF8DCDCAA8C2EE9F376854B5DAE4404FFB6EBA8B4626DE3C5B85D132DB2F6CDA`,
  `ADB24E012AD428C1FA0BC3B23434144D4BF83A698D05BA9283F4C8F25D4FACF9`,
  `F56B501EE96265AC33C32559AD57A4456716AC1532006862620011C3F43CAF81`.

## Iranian Persian (`fa-IR`)

- Target SHA-256:
  `1015C403DB83903E04890FE7CB9B28ABF3AC2E2A4A32E652BCE62224C0A1EAD5`.
- Branch/commit: `codex/openlogic-fa-ir`,
  `82f2b7e043df973c68fb79d78d6746b8ae1f743e`.
- Terminology ledger / locale build receipt SHA-256:
  `F6B4A20C143B8CAFBA4ACF5C3DA5ECC8AB5DCFAEA173968E266579683012BF6A` /
  `BCB3D1BC498B6BECB3BD3A7904DB4974B48BEA6033840095D313BACED3A8588B`.
- PDF: three Letter pages, 134,566 bytes, SHA-256
  `23E5E6E25A1040449632A1F7644BCC6769FA104785BBB5346E940C4C4B3DD2CC`.
- Log / extraction SHA-256:
  `FCAFE87D39716EE6BD6D0E2E1DE5EF5322E7ACAD46AED23864418A474B20DBA6` /
  `F6ADE6DBD2BB1B94EB8052740C6F4154EF6D9F58DEB005F619673C85F6C4286E`.
- Three full-page render witness SHA-256 values:
  `AF80C0BC68EFBB72E5D8C5154B6337DCAE11D4B1BE7D41F889F96D964CCD6D55`,
  `0055CC8F23FE112A2B2A82744ACB789A279F4D66E78C7C0D294FD0EC3B660FDF`,
  `5903D707773EBA0BFA531644794672EAC753607888889BB544CEF233B3F7F91F`.

## Gate result and caveats

Both targets pass direct and independent source-bound semantic review; exact
213-command, 46-environment, 27-token and 72-math-segment replay; IDs, assets,
labels and references; script/Unicode checks; clean two-pass LuaLaTeX builds;
localized metadata and outlines; exact remote/internal link-action inspection;
and complete-page visual QA. The Persian token omission and the locale-level
English section name were corrected before acceptance.

The pinned source defines arbitrary intersection without an explicit
nonempty-family condition. Both targets preserve that source exactly and do
not silently repair or strengthen it. `human_review=none`. Neither PDF is
tagged-PDF or accessibility certified. Extraction contains bidi controls;
Persian extraction drops source ZWNJs. Editable TeX is authoritative.

The shared accepted cursor advances to `OLP-0009`,
`content/sets-functions-relations/sets/pairs-and-products.tex`, SHA-256
`3DB7F0241D387B49488F70E78062C24192B813873618F761565D97BD7249431C`.
`publication_checkpoint_ready=false`.
