# OLP-0008 Arabic build and QA receipt

- Locale/register: `ar`, global formal Modern Standard Arabic.
- Unit: `OLP-0008`,
  `content/sets-functions-relations/sets/unions-and-intersections.tex`.
- Source authority: official Open Logic commit
  `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`.
- Source SHA-256:
  `2AD0EEC70308CEEFF2A4158B2DEE60E59A9B1CF9268FC95C4BB1DA05F65AD60D`.
- Target SHA-256:
  `112BCA7B160608FE147114AE1BEE0EB4E18406B0BF9D312A705B8FA2D62D2025`.
- Unit build config / locale layer / terminology ledger SHA-256:
  `D56E7994CBCFBAD680AD9D0E9E6FEA052B5FCF5BC23C404BA86BFCFA27C18F64` /
  `E525E38108ED0612140E7A4191DE2EF27FB1B76B2B35163431C123F0076AFCE1` /
  `5D320247259B275FC70641EBB44FA19B9444E47C0F2BC52243A82BD781351915`.
- Section wrapper SHA-256:
  `19624BA16F68F26DF9732588668083E85D03B0FC6DDA4077EB43DD4EA734D3B3`.

## Checks completed

- Direct and independent semantic replay: PASS. Inclusive union, repetition,
  subset and empty-set examples, intersection and disjointness, arbitrary
  union's existential condition, arbitrary intersection's universal
  condition, the finite family example, the `A in B` problem, indexed-family
  progression, directional set difference and the proper-subset problem all
  preserve the pinned source. The source does not impose a nonempty-family
  condition on arbitrary intersection; none was silently added.
- Structural replay: PASS for 213 TeX commands in exact order, 46 environment
  events, 27 Open Logic text tokens and all 72 math segments. All three TikZ
  assets, three labels, four references and the localized file ID are exact.
  Checker SHA-256:
  `B8DA8841A80CFF3739B4074E8D7F1838BE714479D56C8A67BA9B45DBC02EA9E5`.
- Unicode/source checks: NFC, balanced braces, Arabic/Persian separation, no
  source bidi controls or Presentation Forms and no English reader fallback.
- Locale correction: added lower- and upper-case cleveref names for `section`.
  The prior accepted Extensionality label is imported with `xr`; the resulting
  reader link is a real `/GoToR` action to the admitted OLP-0005 PDF, while the
  three figure references are internal `/GoTo` actions.
- Independent AI review directly against English: PASS. Nonblocking adverse
  terms `مجموعات متباينة` and `فرق المجموعتين` remain explicitly defined and
  ledgered. `human_review=none`.
- Build: two clean serial LuaLaTeX passes using LuaHBTeX 1.25.7 / MiKTeX 26.5;
  no fatal error, undefined reference or control sequence, missing character,
  overfull box or underfull box. Only unchanged upstream hyperref and class
  warnings remain.
- PDF: three Letter pages, 134,996 bytes, SHA-256
  `324922ECA3469F4094C869ED877C3C95A22A5CEE813E9FAAE583CF167A6E5D05`.
  `/Lang=ar`; localized title/author and one localized outline; four links.
- Log SHA-256:
  `0B9A7EF298EB5B45E0E971A7CE013BD7602380112E129FF9692E74F43D4081E3`.
- Every page was rendered at 180 dpi and visually inspected: PASS for shaping,
  margins, mixed-direction set formulas, all three union/intersection/difference
  diagrams and their captions, stable counters, cross-reference localization,
  clipping, overlap and tofu. Page render witness SHA-256 values:
  `CF8DCDCAA8C2EE9F376854B5DAE4404FFB6EBA8B4626DE3C5B85D132DB2F6CDA`,
  `ADB24E012AD428C1FA0BC3B23434144D4BF83A698D05BA9283F4C8F25D4FACF9`,
  `F56B501EE96265AC33C32559AD57A4456716AC1532006862620011C3F43CAF81`.
  Temporary PNGs are not release files.
- Poppler layout extraction: 6,495 characters, zero U+FFFD, zero Presentation
  Forms, no `??` or English `Section`; SHA-256
  `149236ED2F00C2FF54706FF5BC3F0567F01E79BFB06A32FB8A1CB1139029E25D`.

## Honest limits

The PDF is not tagged-PDF or accessibility certified. Extraction inserts
directional controls (U+202A/U+202B/U+202C: 151/78/229) and may serialize
punctuation or mixed math in visual rather than logical order. Editable TeX is
authoritative. This is unit 8 of 722, not a complete Arabic edition or public
checkpoint.
