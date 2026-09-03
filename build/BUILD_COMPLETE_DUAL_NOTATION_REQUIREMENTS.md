# Build requirements — complete Arabic dual-notation PDFs

This is the current build route for version `OLP-0722-COMPLETE-DUAL-NOTATION-20260903`.

## Inputs and authority

- Frozen upstream content commit: `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`.
- `evidence/provenance/openlogic-control/CLOSURE_MANIFEST.csv`: exactly 722 accepted Arabic target rows.
- `source/locale/ar/content`: exactly 722 translated `.tex` files.
- One Arabic prose/formula-token source is used by both notation profiles.
- `evidence/notation/PROFILE_MAPPING.json` defines the typed presentation difference.

## TeX serialization

Every LuaLaTeX and BibTeX process tree must run while holding the machine-wide Windows mutex `Global\InterlanguageTeXSlotV1`. The supported entry point is:

```powershell
pwsh -NoProfile -File .\build\BUILD_DUAL_NOTATION.ps1 `
  -FinalOutputDirectory <empty-output-directory> `
  -WorkDirectory <empty-work-directory>
```

The wrapper acquires and releases the mutex around the complete TeX process tree. Do not launch the inner script directly.

## Component build

The build creates two profile-specific reader components and two profile-specific closure components, converges references with bounded passes, rejects rerun requests and missing glyphs, applies the fail-closed annotation-only RTL link-rectangle repair, and runs `qa_dual_notation_pdfs.py`.

The ordinary upstream reader graph reaches 642 translated files. The closure component reaches the remaining 80 tracked files with import edges suppressed, so the disjoint union is 722.

## Standalone assembly

`assemble_complete_722_reader.py` appends each closure component to its matching reader. It:

1. preserves every component page content stream and concatenated extracted text;
2. rebuilds a balanced catalog-reachable named-destination tree;
3. prefixes all closure-local destinations with `closure-80.`;
4. converts every closure-to-reader `/GoToR` action into an internal `/GoTo` action;
5. imports the closure outline beneath one internal section; and
6. fails if pages, text, links, destinations, rectangles, page mode, or layout violate the recorded invariants.

The two release outputs are:

- `00_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_INTERNATIONAL_NOTATION_OLP-0722.pdf`
- `01_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_MACHREK_NOTATION_OLP-0722.pdf`

Component PDFs are reproducibility evidence only and are not public companion downloads.

## Acceptance gates

- Source/profile audit: PASS, 722/722, UTF-8/NFC, no BOM or raw BiDi controls.
- Component structural QA: PASS, zero failures.
- Standalone assembly receipts: PASS.
- Final pages: 1,153 international and 1,154 Machrek.
- Final links: 3,154 each, with zero `/GoToR`, broken internal destinations, or outside-page rectangles.
- Independent assembly replay: byte-identical for both PDFs.
- Rendered title, boundary, content, and final pages: no clipping, overlap, missing glyph, black box, formula reversal, or profile leakage.
