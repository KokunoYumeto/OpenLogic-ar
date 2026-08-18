# Paired Functions integration receipt — OLP-0020--OLP-0026

Frozen 2026-08-14 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`, tree
`f67757bb9305b173634082ab4cefd5601a707a34`.

This is a dependency-closure and internal integration-QA receipt, not a
publication checkpoint and not a complete Open Logic edition. Each 26-page
reader includes the accepted Sets and Relations chapters as cross-reference
context and then the complete Functions chapter driver plus its six imported
units. Translation production continues independently in Arabic and Iranian
Persian from OLP-0027.

## Accepted target bindings

| Unit | Arabic SHA-256 / commit | Iranian-Persian SHA-256 / commit |
| --- | --- | --- |
| OLP-0020 | `87007C764C936301137307BC9F64660D9380A171A7D72E60D0E775F017E9E635` / `23028b77bd0594e3ee9fb305fedd35b828922837` | `D788EBF360B902A4EE9B4EE92E6EA1B59499EDB8AEB6DE00E88B0FDAD0144964` / `96370559bb0b5d705a46bfe9e93c44503c0f3c74` |
| OLP-0021 | `A65EA58E8BDA3DAD299C8966FFFD7EA44D0B09FF7CDDE403F7A1A5D22539815D` / `eeddc443d7d51fa78f2747fb715d1d835a66e04b` | `D66599BDC39E09D80BCD3D02C257AEF308A2589E8B6F23C7791CB938E1F0EC83` / `c7212ea7f10d444d71160c76a9f8d9c57191cb96` |
| OLP-0022 | `6E4C12350566A5660C246B496A0F2A74E10BCE84B82977ED0D56FBA02FA049E8` / `15aaed24e40bbfcaf73e260162f1ea6ef2c8cc2d` | `335907D98A138C5062689AEAEC381AADE7BC3E1EE9CBD5371FB3A9C96F002180` / `1dbea9a03604bab77ce0ea955302b091251eb544` |
| OLP-0023 | `815239F35EABA9B26E98E830DE592A941018398E6C77FF2E12311F2C7095777D` / `d88b4f8812d369dea5b92c3556f56142ed744773` | `6E173BD7F87658E80B293AC6D7F95A36F68CD80B5BDDF3D0F628C701E6685BBA` / `3f48f64750920c09502f59d8b47b458d1d8712fd` |
| OLP-0024 | `DAD5E72D573210420017AF88BD69BB2A7C3EE4C59AAB81C49F272E7957B0521E` / `636e250ea9f28a898ce65b1f69426aeace05140e` | `6F81EED36763FBF88C1C6A2D67603C436567E46D02C45FCB5CB27C85D332556B` / `8edd53a8875f1243db01573b042f24667e237896` |
| OLP-0025 | `F78572FF393926BB193A99F5ABD990C490F5113494582C89FF1F06E22EFCAA4E` / `23b338ab1c2d83ca8d6f102632138d70971e73eb` | `8E6BF05BFF3DF56824BCD878602CA4E397A6820A715B69AFC9353D9932DAAEEA` / `a9392f0ae9ee0a8365ea0c52b1a247610be83965` |
| OLP-0026 | `38FD8C03F401637335C644240FCF465E9A23BECCEABC672BB1C319524FB1094E` / `eae9af417ad2be63429608daad85cd44ea107a1e` | `D32ED3E6F2057FA04076350CEB1E1F94E070C4B6DC239C18256D3FDD9B9FA626` / `d68ce3d6ddda4ececf3ae1f9168a11f33edd30b8` |

All fourteen target hashes were replayed from current target files and match
the closure manifest. Their per-unit formal, formula, token, asset, semantic,
script and independent-AI receipts remain applicable.

## Integration wrapper and RTL asset remediation

Arabic wrapper commit: `e48d15a2e04f860cf104d3f07bf0b1e37b34837b`.
Wrapper SHA-256:
`5377692E29F156E6D5AD9BED5600F83E11C8BE53319825CCF1C99974E8EA297C`.

Iranian-Persian wrapper commit:
`e73a6205d7bdd9425b8ab8d18e30b57e195805a1`.
Wrapper SHA-256:
`B7240F2508E280F23A35D3A382D090DE1A37CB71B9BF727611DB15E1CB60969E`.

The first final-candidate render exposed one build-layer defect in both RTL
readers: upstream `\centerline` inside `\olasset` inherited the surrounding RTL
direction and shifted the wide composition diagram on page 24 beyond the
physical right edge. Each wrapper now centers the unchanged requested asset
and width inside an explicit LTR `\makebox`. No source asset, diagram content,
formula, label, translated sentence or mathematical claim changed.

Independent delta replay measured zero nonwhite pixels in the outermost right
20 pixels after the repair (previous Arabic witness: 398); the full blue
codomain and curves are visible with page-edge whitespace in both editions.

## Serial build and artifact evidence

Both integration readers were built serially with LuaLaTeX, BibTeX, LuaLaTeX
and LuaLaTeX. Final logs report zero fatal errors, emergency stops, undefined
controls, unresolved references/citations, missing characters or glyphs,
rerun requests, overfull boxes or underfull boxes.

Arabic:

- PDF: 26 Letter pages, 486,507 bytes, SHA-256
  `73467187C77C310D82F6A5D42E5170847CB2EFD70646AADDDAA4375D9EDD530A`.
- Log: 100,184 bytes, SHA-256
  `5372FB733F9BA08A565E31E288537ACE84F527814D8BDCC1D8FFB4718909ADBE`.
- Poppler layout extraction: 133,139 bytes, SHA-256
  `4D6E47CCCFAC601D13AFC7D58171A4E033101FAF5562D8CDB79AEF2597537FFE`.
- PDF audit JSON: 7,159 bytes, SHA-256
  `5C4F548AD9F8E27FC47C5D2CC7DC475CF7AAE192C18FED0601F113C35229358B`.
- Metadata `/Lang=ar`; 327 valid named destinations; 33 valid internal
  GoTo annotations; zero invalid or out-of-bounds link rectangles.

Iranian Persian:

- PDF: 26 Letter pages, 467,561 bytes, SHA-256
  `FFD35343A76E8F12FF45D6ED2D43273E5ADF8CFE2E2FA1928EBEF022F97CD457`.
- Log: 106,327 bytes, SHA-256
  `5DC68CCA2FB597518E25C4B1B7D9DD40BAE5F2D0590EC18440AE52F5DC0ABD23`.
- Saved Poppler layout extraction: 138,823 bytes, SHA-256
  `AE50D5ACCC51A1F6C5C9138F57B6BA28F840FE580CE4168E8A3D0E042B3A6A0A`.
  A separate default-Poppler replay produced SHA-256
  `C692B19EE2E684E23EFE9605841A145DF6FEB6E37B926388BC57A53BD47397C1`;
  the hashes are method-specific and are not claimed to be byte-identical.
- PDF audit JSON: 7,176 bytes, SHA-256
  `381536514C8EBA5FF3DF3EA98F474BB9851B3E6EA087FA833D7330D627971F54`.
- Metadata `/Lang=fa-IR`; 327 valid named destinations; 24 outlines; 33 valid
  internal GoTo annotations; zero invalid targets.

The retained log advisories are nonfatal and explicit: duplicate Hyperref
bookmark option, two package-provider-name mismatches, memoir `\addtodef`
deprecation and font-language support information. They are not relabelled as
errors, and no clean-log claim suppresses them.

## Render and visual replay

Every final page was rendered at 144 dpi and visually reviewed in seven
ordered contact sheets per locale. Arabic contact-sheet SHA-256 values:

1. `F89AB9FEF8C527095A1950D45C77216E650FF23A17740891D154059480AA94D0`
2. `B8BE38A192970959597A789B77D3092C4C82BEE488DA920FC96DCAFF968A76FE`
3. `E4624280CE7A54FC5C84737041BDCF827C4B2DFE2F52F79E40C8D44BDC44768A`
4. `14220F509DFD499FC920B95D84A4FA1F8F2ED5245CB8491B4C8A3433465156F4`
5. `7A0ABB9092276336617AEFBDEC4499761B81510B5D0CDC6490DC32E579E49F1F`
6. `E400C604EE7A5BF6F719C477C1A74804028F48FC7EEECA42A9D364CF2986C92D`
7. `0B8D6EDF518289E07A4E16008F2A74B74E8EE4FE40AD2CD85893EEC72724E6E4`

Persian contact-sheet SHA-256 values:

1. `B5736CDBF6F820B75C6FC1BB072ABCEC04C4B029280429F87168E9527E144C81`
2. `34A7BB616289EE0B6AE4B291D17E85DBE17DF44BF87D80A856685F218188849D`
3. `36DB3511482B93D0476BD18138644ED01B51F97F3F755B71976F251848BBEE0B`
4. `8BA1F27CB25F8D05486F4332D80ABAE38D88AFF982D130DE1FF056926C200AB7`
5. `3871BAF93FE13EE5DD4C0B9E58153AB3B8E6F98B7088EC714323B2D0EAC4F8FE`
6. `6F80721E6E1E0A89328FF191AFFCF4A5B419A90CC84BBC47BD8FE37387DAA0A0`
7. `B073E3296E7EBAAE8BFED94EB0BAF671295BB4BC2AB3281E5FB4B22C83F5C0BD`

The final replay found no clipping, overlap, tofu, black boxes, malformed
shaping, counter reversal, broken diagram or hidden English glossary fallback.
All Arabic/Persian source formulas, stable identifiers, labels and asset
bindings remain unchanged.

## Preserved source findings

The translations preserve rather than silently repair these source-bound
issues, each of which is recorded in both language-specific adverse ledgers:

- OLP-0021: the example shifts from `n` to `x`; the natural-number domain also
  includes zero while the prose calls the selected root positive.
- OLP-0022: malformed range `\Setabs` argument structure.
- OLP-0023: malformed restriction `\Setabs` argument structure.
- OLP-0024: injective implies left inverse is missing `A \ne \emptyset`; the
  proof's choice of `a \in A` fails for `A=\emptyset`, `B\ne\emptyset`.
- OLP-0026: malformed partial-domain `\Setabs` structure and an implicit,
  rather than newly defined, scope for injectivity of a partial function.

## Honest residuals

Neither PDF is tagged or PDF-UA. Poppler inserts balanced bidi controls in
layout extraction. Persian source ZWNJ does not survive either audited PDF
extractor, and logical order from PDF extraction is not authoritative. The
editable UTF-8 TeX plus visually checked PDF are the authoritative surfaces.
Legacy Type-1 mathematical fonts have incomplete Unicode maps.

No native Arabic or Persian human review, regional review, accessibility
certification or mathematical-specialist human review is present. This receipt
establishes exact source binding, formal/static/semantic independent-AI replay,
dependency-closed serial build, link/extraction checks and every-page visual QA
for this internal Functions integration checkpoint only.
