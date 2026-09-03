# OLP-0722 complete Arabic dual-notation release

Version: `OLP-0722-COMPLETE-DUAL-NOTATION-R2-20260903`

This corrective release keeps the two standalone complete-project PDFs and removes the raw technical source-commit identifier from their reader-facing title pages. Source identity remains available in the technical provenance bundle. Each PDF contains Arabic coverage for all 722 tracked English content `.tex` files; no companion download is required.

## Primary files

- `00_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_INTERNATIONAL_NOTATION_OLP-0722.pdf` — 1,153 pages; 10,600,262 bytes; SHA-256 `8E2AA13D0B73464BDA7D3120CF78F8422D65C777C2C60808A196BB77D0D23F7B`.
- `01_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_MACHREK_NOTATION_OLP-0722.pdf` — 1,154 pages; 10,601,135 bytes; SHA-256 `8EF59F94D1E9E486408E72C9A55596B62532C208ECBA59C962DF59AEB50F33EA`.

The ordinary upstream book graph reaches 642 of the translated units. The other 80 tracked units are appended inside each PDF as a technical section. Their page streams and extracted text are unchanged from the separately built closure component, but all cross-document links are converted to internal links and all closure-local destinations are namespaced.

## Notation profiles

- International: mathematical digits display as `0–9`.
- Machrek: mathematical digits display with Arabic-Indic glyphs `٠–٩`. Formula order remains LTR; source digit tokens remain U+0030–U+0039; Latin/Greek variables, symbols, citations, identifiers, URLs, and prose are unchanged.

The historical RyDArab/RamzArab packages were retained as design and provenance evidence. They were not used as the production backend because their global token reversal, ArabTeX dependency, legacy encodings, and restricted-embedding font are incompatible with a source-faithful modern LuaLaTeX build.

## Verification

- 722 accepted manifest rows, 722 Arabic files on disk, and a 722-unit dependency union with zero overlap.
- 3,154 links in each final PDF; zero cross-document links, broken internal destinations, or outside-page rectangles.
- Every component page content stream and the concatenated extracted text are preserved by assembly.
- One independent assembly replay reproduced both final PDFs byte-for-byte.
- Six rendered pages covering both titles, both internal section covers, and the first appended content page in each profile passed visual inspection.
- The PDFs are fixed-layout and untagged; no PDF/UA claim is made.

Prior GitHub releases and Zenodo versions remain preserved in their existing public histories.
