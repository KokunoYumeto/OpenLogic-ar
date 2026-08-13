# Cumulative release-QA receipt — OLP-0001 through OLP-0010

Date: 2026-08-13. Scope: the separately built Arabic (`ar`) and Iranian
Persian (`fa-IR`) cumulative Open Logic readers through paired-accepted unit
`OLP-0010`. This is 10 of 722 frozen source units, not complete-corpus
closure. Source authority is commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`, tree
`f67757bb9305b173634082ab4cefd5601a707a34`. All ten source hashes and all
twenty target hashes match `CLOSURE_MANIFEST.csv`; the ten unit checkers and
independent semantic replays pass. Human/native review is `none`.

## Arabic release reader

- Path: `ar/locale/ar/output/build/cumulative-olp0010/open-logic-through-olp0010-ar.pdf`.
- SHA-256 / bytes / pages:
  `B2C54B11B66ACF5FD1141B7A3BCB42C8F61F32AE78BDA81620D18F9A2C3B2BB0` /
  269,474 / 13 Letter pages.
- Build: five LuaHBTeX passes; passes 2--5 are byte-identical at the console
  level, SHA-256
  `533C8E3D770D6917A24AC64A4A9DB214A30AE1B6B8D12FA2D837449EA7399AFE`.
  Final log/FLS SHA-256:
  `B3B75CFEBD036FB2ECB0F4C0CB86B01AC397C941307EB3825AB783688204A079` /
  `54AB16B7CDDCD5FCBB42049762C45AE28035D61CF557A3D9A40BC199E9D8EC9D`.
- Structure: `/Lang=ar`, nine localized outline entries, 113 named
  destinations, 14 valid internal and seven expected external link actions,
  no invalid internal destination, encryption, form, attachment, JavaScript,
  remote launch or hidden English target fallback.
- Visual QA: all 13 pages rendered at 180 dpi and inspected; shaping, RTL
  prose, LTR formulas and identifiers, diagrams, headings, counters and page
  boundaries are legible with no clipping, overlap or tofu.
- Extraction: Poppler output has zero U+FFFD and zero Arabic Presentation
  Forms. One pypdf mode reports one replacement character; combining-mark
  order and legacy Type-1 math mappings are extractor-dependent. Editable TeX
  is authoritative for exact Unicode text.

## Iranian-Persian release reader

- Path: `fa-IR/locale/fa-IR/output/build/cumulative-olp0010-release/open-logic-through-olp0010-fa-IR.pdf`.
- SHA-256 / bytes / pages:
  `5A27399381186EBC41A2E8CE163A915695FC8BE895B8E6E5BB3297C841475330` /
  257,248 / 13 Letter pages.
- Wrapper SHA-256:
  `0A74FF0126F958B888BB7C928F8954D3249D5E368353E4FE840AF8F970533A89`.
  Six LuaHBTeX passes were run; passes 2--6 are byte-identical at the console
  level, SHA-256
  `9EBFBED4A3057E8D1D7FC630CA7470C521F7CCE29F673AA55B661352593BED21`.
  Final log/FLS/.thm SHA-256:
  `86D349A85D22239E26C6583A356C7D1AB7C4AC4B332F931556E0A523BCED5891` /
  `AEBCD922F39ED46DEC3D0A0392EA093134EC9F4A7840D6A0002AE9F204DD069E` /
  `59C3941094F9D93136F34E3A655919C23C6886ADC82A53650804CFA419732A46`.
- Counter replay: theorem-like sequence is exactly `1.1`--`1.29`; the
  problem sequence is `1.1`--`1.10`. Visual sentinels pass for Example 1.2,
  Definition 1.10, Example 1.28 and Theorem 1.29. The superseded PDF with
  reversed counters must never be published.
- Structure: `/Lang=fa-IR`, nine localized outline entries, 113 named
  destinations, 14 valid internal and six expected external link actions, no
  invalid destination, encryption, form, attachment, JavaScript, remote
  launch, Arabic target leakage or hidden English target fallback.
- Visual QA: all 13 pages were inspected independently at 240 dpi and again
  from the durable 180-dpi render set; shaping, RTL prose, LTR mathematics,
  diagrams and corrected multi-digit counters pass with no clipping, overlap
  or tofu. The ordered 240-dpi render-manifest SHA-256 is
  `B2B39C8D419524AC8DFE146262F290DC8E023434A1E9E0C16158E2F766E9ED3A`.
- Extraction: zero U+FFFD and zero Arabic Presentation Forms in the final
  Poppler witness, but all 389 source ZWNJs are absent from extracted text and
  legacy math symbols do not round-trip completely. Editable Persian TeX is
  authoritative.

## Shared caveats and bundle gate

Neither reader is tagged PDF and neither carries a PDF/UA or accessibility
certification. The release is model/agent checked, not native/community
certified. Publication packaging must use the exact committed LF `LICENSE.md`
Git blob, 17,068 bytes, SHA-256
`BB5E0179A1E9BDB55634A4303784CF73C297A1DCEE27B92CD546BF398075531C`;
the contaminated source-cache working file is prohibited. Each language must
receive its own DOI lineage, repository, sources, evidence archive, manifest
and remote readback receipt.

## Standalone publication-tree rebuilds

The historical workbench PDFs above remain immutable QA witnesses. Rebuilding
from each self-contained publication tree changed only path-dependent PDF
trailer identity; it did not change rendered pages, metadata, links or the
saved Poppler text surface.

- Arabic publication-tree PDF: 269,462 bytes, 13 pages, SHA-256
  `AFFF3F21E71060462FD842C18E48B15F7C8284175FB2D39C23920B870DA57ABD`.
  All 13 ordered 180-dpi page images and the Poppler layout extraction match
  the workbench witnesses exactly.
- Iranian-Persian publication-tree PDF: 257,248 bytes, 13 pages, SHA-256
  `6CF8F82A0C05775C9C4852C3C8D3D09D1B5E08DAEB6E6942E75C3487F0C2229D`.
  All 13 ordered 180-dpi page images and the Poppler layout extraction
  (SHA-256
  `14D2BC499F0D5150E1E77A15B470DF60AD6066E443B82FACB347333A8111DCF2`)
  match the corrected workbench witnesses exactly.
