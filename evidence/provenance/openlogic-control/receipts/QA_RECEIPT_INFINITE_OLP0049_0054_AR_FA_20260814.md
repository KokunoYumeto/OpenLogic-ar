# Paired Infinite Sets integration receipt — OLP-0049--OLP-0054

Frozen 2026-08-14 against Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`, tree
`f67757bb9305b173634082ab4cefd5601a707a34`. This is a dependency-closed
internal reader receipt, not a publication or native-language certification.

## Final artifacts

| Locale | Wrapper SHA-256 | PDF SHA-256 | Pages | Log SHA-256 | FLS SHA-256 |
| --- | --- | --- | ---: | --- | --- |
| `ar` | `F1516E940198BC3DA0993419D0011C7EFFCE8B674F52CB1216F60B25010B6898` | `69B19B10F1A3E9699C8CD8B042AB95129498C502239287ACAA09A5084BDFDFDD` | 62 | `FF7258D9D79029B6171461DE92A6A78CBDA803372D9F32AD353D8A14C5AC9641` | `F6BBB6A581E7E876D04B0B31049B158A116A13E7F43AE7535C8EFDD7C8EBCF5E` |
| `fa-IR` | `D5B082AFF20DD5E6815FAC9C4A5CFE03096EF4C1193395A903DB3726E32EBB9C` | `4ABB6F15330DA43E950E98A656334DBC35C7ABE1F5391511AAAD38EF0E3942E2` | 63 | `1F939A6DB5E34C0FB11EBF13925929A7979D6B69249BD6B6A1A55CC0083676E6` | `AA6453C228492928341359AE347D14990A313DBFDE3E827B40885160D81B6F67` |

Both readers were rebuilt serially with a fixed source-date epoch using
LuaLaTeX, BibTeX, and stable repeated LuaLaTeX passes. Final-pass and extra
stability-pass PDFs were byte-identical. Logs have zero fatal errors,
undefined controls, unresolved references/citations, missing glyphs, rerun
requests, or box warnings. Each recorder file resolves exactly 51 localized
content inputs and zero English project-content fallback.

## Bibliography-link repair

Both locale bibliography files are byte-identical, 36,023 bytes, SHA-256
`4B4249139C74DE1DF579B77B29F6D8EDF087450CC05F03F771E3661F5EAEB54F`.
Two dead upstream URLs were replaced without changing bibliographic claims:

- Conway 2006 chapter: `https://doi.org/10.1017/CBO9780511541407.004`;
- O'Connor/Robertson real-number history:
  `https://mathshistory.st-andrews.ac.uk/HistTopics/Real_numbers_2/`.

Live GET on the freeze date returned HTTP 200 for both final destinations.
Each PDF contains 131 links: 128 valid internal GoTo annotations and three
valid URI rectangles representing those two distinct URLs. The DOI has one
rectangle; the wrapped St Andrews URL has two. All rectangles have positive
area and lie within their page boxes. Arabic has 695 and Persian 696 resolving
named destinations; both have 52 valid outline entries.

## Visual and structural replay

All 125 pages had already passed full-page visual inspection. After the URL
repair, Arabic pages 61--62 and Persian pages 62--63 were independently
rendered twice at 180 dpi; repeated renders were byte-identical. The repaired
URLs wrap cleanly, all four pages have zero ink in the outer 20-pixel band,
and no clipping, overlap, tofu, malformed shaping, or diagram regression was
found. PDFs are unencrypted PDF 1.5 on 612-by-792-point pages, with `/Lang=ar`
and `/Lang=fa-IR` respectively.

## Residuals

The PDFs are untagged and are not PDF-UA. Twenty-two legacy Type-1 math fonts
lack ToUnicode maps. RTL extraction order is non-authoritative, and audited PDF
extractors do not preserve Persian ZWNJ. Editable UTF-8 TeX and the visually
checked PDFs remain authoritative. No native Arabic/Persian, regional,
mathematical-specialist, or accessibility human review is claimed.
