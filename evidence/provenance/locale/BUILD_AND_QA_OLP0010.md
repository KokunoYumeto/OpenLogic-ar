# OLP-0010 Arabic build and QA receipt

- Locale/register: `ar`, global formal Modern Standard Arabic.
- Unit: `OLP-0010`,
  `content/sets-functions-relations/sets/russells-paradox.tex`.
- Source authority: official Open Logic commit
  `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`.
- Source SHA-256:
  `9A76315CD0D9CF89D27E90A9B87138B1C95AEA98E0D26DE3FE12D897B8C4D10D`.
- Target SHA-256:
  `842DBAA2AAE165CE42B1999DDE89D621F4E90E4A60D72781879C5B878E9B9D56`.
- Unit build config / locale layer / terminology ledger SHA-256:
  `5E22EFBFFE48ACCC799C0482BC4FE3E2641149E6763AC932AD44C8E94FE94DBB` /
  `E525E38108ED0612140E7A4191DE2EF27FB1B76B2B35163431C123F0076AFCE1` /
  `E1EB3362355C45781E4905E0C29A25929EF40A0BE7848D977E22687F218FB64C`.

## Checks completed

- Direct and independent semantic replay: PASS after correcting one initially
  ambiguous Arabic membership-polarity sentence. Extensionality remains a
  conditional uniqueness principle, not an existence/comprehension axiom;
  unrestricted comprehension, Russell's set, the biconditional contradiction,
  both directions of the novice explanation and the hypothetical universal set
  all preserve the pinned source.
- Structural replay: PASS for 55 invariant TeX commands, 12 environment
  events, 10 Open Logic text tokens and 34 invariant math segments (33 inline
  and one display). The label and conditional cross-reference are exact.
  Checker SHA-256:
  `F76F4AC4692CB492F1C2FA19A7FF38ECCBA5611D8623530FBB38209BCC02756A`.
- Unicode/source checks: NFC, balanced braces, Arabic/Persian separation, no
  source bidi controls or Presentation Forms, and no English reader fallback.
- Independent AI review directly against English: PASS. `human_review=none`.
- Build: two clean serial LuaLaTeX passes using LuaHBTeX 1.25.7 / MiKTeX 26.5;
  no fatal error, undefined reference or control sequence, missing character,
  overfull box, underfull box or emergency stop.
- PDF: one Letter page, 79,349 bytes, SHA-256
  `F379234EAB22DF89DD27A6E5BFA21580C09FB4AB58F955421D0C78EA83BE0FED`.
  `/Lang=ar`; localized title/author and outline; zero annotations, forms or
  JavaScript.
- Log / Poppler extraction SHA-256:
  `DFA08437E223B6FB73CCE8322E3AB03E961DC4905BD16EF5C479A1FB50366A24` /
  `99F86808994759DA5332FB31A5B64A3E301FD7CFD85120C4724FAF375D4FE377`.
- The complete page was rendered at 180 dpi and independently inspected:
  PASS for shaping, margins, mixed-direction formulas, proof-end marker,
  clipping, overlap and tofu. Render witness SHA-256:
  `6BFA0AFED4B0290C990980F945FB69643AC445FBF40C485608F9BE98D5E95BF1`.

## Source oddities preserved

The source's doubled whitespace, “the phi's” shorthand, source-only accent
commands and explicit spacing groups were not silently normalized. The
conditional cumulative-part reference correctly produces no link in this
isolated unit build because the referenced part label is absent.

## Honest limits

The PDF is not tagged-PDF or accessibility certified and does not declare RTL
viewer direction. Poppler extraction contains 260 balanced directional
controls and serializes every visible `\notin` as slash plus `∈`, while other
extractors may reverse RTL runs or emit replacement characters. Editable TeX
is authoritative. This is unit 10 of 722, not a complete Arabic edition.
