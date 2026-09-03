# OLP-0722 complete Arabic dual-notation release

Version: `OLP-0722-COMPLETE-DUAL-NOTATION-20260903`

This release replaces the public reader-plus-companion packaging with exactly two standalone complete-project PDFs. Each contains Arabic coverage for all 722 tracked English content `.tex` files; no companion download is required.

## Primary files

- `00_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_INTERNATIONAL_NOTATION_OLP-0722.pdf` — 1,153 pages; 10,601,905 bytes; SHA-256 `615B7FAA68C4892FE0295E570C0A25580BFEDEA440BA9E2940C0B3A740D13F22`.
- `01_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_MACHREK_NOTATION_OLP-0722.pdf` — 1,154 pages; 10,602,795 bytes; SHA-256 `1C316FF7BAFCCAB1D6D144264B6B5B623FD0B450474E54DFB0A2DAF8F78A5F8E`.

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
- Ten rendered pages covering titles, reader terminal pages, append boundaries, first appended content, and final pages passed visual inspection.
- The PDFs are fixed-layout and untagged; no PDF/UA claim is made.

Prior GitHub releases and Zenodo versions remain preserved in their existing public histories.
