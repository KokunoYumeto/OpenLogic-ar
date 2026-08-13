# OLP-0009 Arabic build and QA receipt

- Locale/register: `ar`, global formal Modern Standard Arabic.
- Unit: `OLP-0009`,
  `content/sets-functions-relations/sets/pairs-and-products.tex`.
- Source authority: official Open Logic commit
  `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`.
- Source SHA-256:
  `3DB7F0241D387B49488F70E78062C24192B813873618F761565D97BD7249431C`.
- Target SHA-256:
  `0209ACCAD5BA65DA9955892285D637EC9B4DA5B98D8C7830695BE6F8161B6809`.
- Unit build config / locale layer / terminology ledger SHA-256:
  `068CBD908E970B31CE9FFD3BA42E093605535B0137B4594D8A3B62D24485CF3E` /
  `E525E38108ED0612140E7A4191DE2EF27FB1B76B2B35163431C123F0076AFCE1` /
  `4C070E93E6AAAC9DC3AC9EC001B20437B3AABC087D722E01B88C93FDF7CB634D`.

## Checks completed

- Direct and independent semantic replay: PASS. Ordered-pair equality and
  coordinate order, the exact Wiener--Kuratowski coding, left-associated
  tuples, Cartesian-product membership and enumeration, recursive powers,
  the `nm` and `n^k` counting claims, words over a set and the source's
  length-zero-sequence convention all preserve the pinned source.
- Structural replay: PASS for 177 TeX commands in exact order, 30 environment
  events, 12 Open Logic text tokens and 78 invariant math segments (72 inline,
  five display and one `align*`). Both labels, the same-unit reference, the
  `rcccc` array and the localized file ID are exact. Checker SHA-256:
  `91387B8796F5F44E682F4D7C6D1C11B3AD678DACCAFFAD04D3778786FDB0BD12`.
- Unicode/source checks: NFC, balanced braces, Arabic/Persian separation, no
  source bidi controls or Presentation Forms and no English reader fallback.
- Independent AI review directly against English: PASS. Nonblocking adverse
  distinctions for ordered pair, ordered tuple, Cartesian product, word and
  sequence remain ledgered. `human_review=none`.
- Build: two clean serial LuaLaTeX passes using LuaHBTeX 1.25.7 / MiKTeX 26.5;
  no fatal error, undefined reference or control sequence, missing character,
  overfull box or underfull box. Only unchanged upstream hyperref and class
  warnings remain.
- PDF: two Letter pages, 135,231 bytes, SHA-256
  `EA09C95D64030EE95C6210B21546C602F9F7A93DBB641168689EE80C8A637030`.
  `/Lang=ar`; localized title/author and one localized outline; the same-unit
  reference is one internal `/GoTo` annotation.
- Log SHA-256:
  `C390388743897FE26C209811CDDD7B8029AD0B6C8100844895BEC8107340A7A8`.
- Every page was rendered at 180 dpi and visually inspected: PASS for shaping,
  margins, mixed-direction tuple and product formulae, the product grid,
  proof-end marker, stable counters, clipping, overlap and tofu. Page render
  witness SHA-256 values:
  `F0A8BF210618AD52B3F0EEF0457C224DDE311D327DFF30604DD8F3606BE494F0`,
  `D04FD20C8616730F8DB4C5343CF52999F925ACCB429B3DCF36EE834582F35714`.
  Temporary PNGs are not release files.
- Poppler layout extraction: 4,873 characters, zero U+FFFD, zero Presentation
  Forms and no `??`; SHA-256
  `57DDAD0B4355B551B1A80657A69BCF8FB220C95C36669AFF2C2EE8C398A305F0`.

## Source oddities preserved

The disjointness proof reuses the same second-coordinate name where arbitrary
second coordinates are implicit; the product grid silently assumes an
enumeration of `B` and omits visible commas; “any sequence” is broader than
the later finite-power display; and this unit writes `\emptyset` for the empty
sequence despite an earlier `\Lambda` convention. None was silently repaired.

## Honest limits

The PDF is not tagged-PDF or accessibility certified. Extraction inserts
directional controls (U+202A/U+202B/U+202C: 154/58/212) and may serialize
punctuation or mixed mathematics in visual rather than logical order. Poppler
has no replacement characters, but pypdf emits two U+FFFD characters; copied
mathematics also approximates some angle brackets and inequality signs.
Editable TeX is authoritative. This is unit 9 of 722, not a complete Arabic
edition or public checkpoint.
