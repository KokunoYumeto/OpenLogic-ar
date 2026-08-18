# Paired Relations integration receipt — OLP-0011--OLP-0019

Frozen 2026-08-14 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`, tree
`f67757bb9305b173634082ab4cefd5601a707a34`.

This is a dependency-closure and QA receipt, not a publication checkpoint.
The two 18-page readers include the already accepted Sets chapter only as
cross-reference context, followed by the complete Relations chapter driver and
all eight imported Relations units. The source-order production cursor remains
OLP-0020.

## Build-discovered remediation

The first dependency-closed build exposed three runtime defects that isolated
static checks could not establish:

1. OLP-0012--OLP-0019 lacked explicit locale-admission arguments on
   `\olfileid`, so the framework skipped localized bodies.
2. the Latin proper name `K\H{o}nig` inherited the Arabic-script body font,
   which lacks U+030B;
3. glossary heads `formula` and `derivation` fell back visibly to English.

The remediation adds only `[ar]` or `[fa-IR]` unit markers, typed
`\foreignlanguage{english}{K\H{o}nig}` wrappers at the three existing name
occurrences in each OLP-0018 target, and independent locale token values. It
does not change any formula, quantifier, relation orientation, source defect,
diagram geometry or translated mathematical claim.

Arabic remediation/integration commit:
`28506ad5f6374ddb7662962458febaac6759e5de`.
Persian remediation/integration commit:
`8485e7e2b94141562050a860680497dff8f25818`.

## Current target hashes

| Unit | Arabic SHA-256 | Iranian-Persian SHA-256 |
| --- | --- | --- |
| OLP-0011 | `9C8A89C1E7A5AE14A2E917C358920E5FB1FBEBB51488FA4CAE326E3DE50DD303` | `3FE8611344F06A83F8CDADF3E96B4867F06511E551E9770602A14475FFA291E6` |
| OLP-0012 | `15153FC56FE633AAFCE519B0B35AD462CC7203BDB71636617E8DF2543C5E02B5` | `481C3BBC5EBD8758EAD1C7570A6436F67F15413207E281A07EC98F344AA95F0E` |
| OLP-0013 | `5498EF36398EF7EDA3890063CA562A6EBD3A40C4806B87FCD95FA3EEE7649FF0` | `8E9F418E34A61EC9AA779FA87CAF6243FAA13A8F5421693C677B281369858539` |
| OLP-0014 | `71C5D1A7E5D98F0C774812917FF58450F66A62674031EF09115006969F1B6A22` | `ABDEC2AE02FFA0668B36EF0CD4BD521BC5357C9C6A7ACB5465589196E7C28D7C` |
| OLP-0015 | `52298E1712E991A79D5575BF1E3F8F04DC0E98B47B396EABA3271BEF4CCFDF5B` | `B1FDAAC070C36B48CCDA7E5DE03FDC338D049A35A7D57791174E74019ECF40AB` |
| OLP-0016 | `1CC56A15B577360493DF723D9DEE4C7CBB63911A900CCFC78FD9B8C2A2DBFDFC` | `0B3DC4C4959237688268FAEE51B97B33EE9574E1E89E8CE564EA1D6C1E811168` |
| OLP-0017 | `DC66FB221DBB54E6C6840565403AE578047DAE9B48C203CF3612434FE8115AE0` | `ECC7C9249EA6E996E46DE7788780925A8EC7CD0768CE24AB91876D3ACC9E9BF9` |
| OLP-0018 | `D055AFDAC6A12E379A74654C02D12360E4C8F8729135B89807D3F93717EF3186` | `15A3CCAD1E07EE0FCF9508E1B5A806B9140961B048AF5C30717C4D8717B3F111` |
| OLP-0019 | `3AB722CFD8B2B8379AD83E183F1807B825ED0638423F202FBF407BA1B0A4EF8A` | `E856C2A5169B4A7827113178D7A2574436668D2DC570DC99EC0C5DB4FFB95058` |

The OLP-0012--0019 hashes supersede the pre-integration target hashes in the
individual unit receipts only for build-layer metadata and the documented
OLP-0018 Latin-name font wrapper. Their source/semantic acceptance evidence
remains applicable.

Arabic locale config SHA-256:
`9D29E9D240E46297B0F395ABB3B55EB033AA8850F345A680091611485D5BDAEB`.
Arabic wrapper SHA-256:
`9A4195A2552A841D6863F12D963848C592759C64222446EBE5AE1B1FFFC64FE4`.
Persian locale config SHA-256:
`D3D6B4EFE289A0D2ECD751D64FEFF53FB4228C60805F29491EC45A872CDB5D8E`.
Persian wrapper SHA-256:
`6C87D851BCA5198743F85D1DCED88EDEED006C758CC867D8FE9407019CDA3A42`.

## Serial build and PDF evidence

Both builds began from empty build directories and ran LuaLaTeX, BibTeX,
LuaLaTeX, LuaLaTeX serially.

Arabic:

- PDF: 18 Letter pages, 362,614 bytes, SHA-256
  `CD0E61414452C9798C970E184D9E8E8233646A324E5F6B77131CAC1DA9AC7245`.
- Log: 97,489 bytes, SHA-256
  `2261FC64093CCC604FF68321CCB3F51C20E86E231F3E0FE87A2F6C2B3E6BF14F`.
- Poppler layout extraction: 92,128 bytes, SHA-256
  `B4B9F788CFD1E2E1641EC6DC6493E1D72F116B02E0997437CDADC50C91E6AA27`.
- PDF metadata `/Lang=ar`; 14 valid internal link annotations.

Iranian Persian:

- PDF: 18 Letter pages, 351,387 bytes, SHA-256
  `B3012D9E2F804D9FA63F313B760D1DF5D65D553351094339F4C300DBC1672C17`.
- Log: 103,583 bytes, SHA-256
  `703D1FC056F440911E4CB73F32AC256C0F83B0EFC44DE0EB5E58D06C56AF9143`.
- Poppler layout extraction: 95,930 bytes, SHA-256
  `67C59962B7485550921E6E70D251D0FC59727683A58BFDF23067F17CA798C8D0`.
- PDF metadata `/Lang=fa-IR`; 14 valid internal link annotations.

Final logs have zero fatal errors, undefined controls, LaTeX errors, missing
characters, unresolved references/citations, rerun requests, overfull boxes or
underfull boxes. Both Poppler extractions have zero U+FFFD, zero Arabic
Presentation Forms and zero English `formula(s)`/`derivation(s)` fallback.
PyPDF independently reports 18 pages, exact `/Lang`, zero U+FFFD, zero
Presentation Forms, zero bidi controls and the same 14 internal annotations in
each PDF.

## Render and review evidence

All 18 final pages per locale were rendered at 144 dpi. Three six-page contact
sheets per locale were inspected after the final glossary-token rebuild.
Arabic contact-sheet SHA-256 values are
`90F57882ADD93241F09DFAA7BB7F3CA24ABB5A0AA5BBA15042FDD3531BDBA6C5`,
`37907A6C2F21EAD98A26E2B27B9C60FA7C992BAF2288FBD59A652C3B11D4AADC`
and
`404D11AC0837488565F5D3BBD136732EEDD7D5DD009CE4FCAFF44A8FF7BED0F1`.
Persian values are
`92CFFB09C9678CD8E91F879F618A98E1239FB085C2862A72854B59B5DE5303F1`,
`352485878E3485056348E0E166B13E4E91958E8FB026CB451AE2CC61D6995D4B`
and
`B22CC34C0CD0AD2C63FBE378242B3D6C7825307238E510F11C70A0E0DA0A19D3`.
The full replay found no clipping, overlap, tofu, black boxes, malformed
shaping, broken diagrams, counter reversal or hidden English body fallback.
An independent read-only remediation replay bound the current target, config,
wrapper, PDF, log and extraction hashes above and found no semantic, formal,
fallback, page-count or visual blocker.

## Honest residuals

Neither PDF is tagged or PDF-UA. Poppler inserts directional controls in layout
extraction; PyPDF and Poppler logical order must not be treated as authoritative
RTL text. Persian extraction drops source ZWNJ. Editable TeX plus the visually
checked PDF are authoritative. No native Arabic/Persian human, regional,
philosophical-logic or mathematical specialist review is present.

The logs are clean at the declared error/reference/glyph/box gates, but each
retains four nonfatal upstream/toolchain warnings: duplicate Hyperref bookmark
option, two package-name mismatches and deprecated memoir `\addtodef`. Embedded
legacy Type-1 mathematics lacks complete Unicode maps. The readers use US
Letter. The visible proper name remains source-exact `Kőnig` because upstream
spells it `K\H{o}nig`; no silent normalization to `König` was made.
