# QA receipt — post-closure Open Logic Arabic build repair, OLP-0697

Date: 2026-08-18

Status: `PASS_POST_CLOSURE_OLP0697_AR_TARGET_REBIND`

## Authority and predecessor

- English authority: Open Logic commit
  `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`, tree
  `f67757bb9305b173634082ab4cefd5601a707a34`.
- The complete source binding remains
  `E5FBD3773FF80F2195E6EFA023EE51573E778BDF20629D3377B16FA09883FE51`.
- This receipt is append-only and follows
  `QA_RECEIPT_POST_CLOSURE_BUILD_REPAIRS_OLP0001_0722_AR_FA_20260818.md`,
  SHA-256
  `96FE006DC28D9F6A72452E58637776E1C9BD1D8386669595809263F2D6BF1677`.
  That prior receipt remains unchanged.
- The immediately preceding closure-manifest SHA-256 was
  `20BEA057CAD50409B1B228EFA1D430BFE19833400F706EF4F4CDD631C446737B`;
  the immediately preceding complete paired target binding was
  `E356DA1C7D7AB7D61AA9CBFCC093EF567DC69D18839180C02352B234A1A3C6B3`.

## Exact retained correction

- Unit: OLP-0697, Arabic.
- Target:
  `locale/ar/content/proof-theory/propositions-as-types/types.tex`.
- Previous target identity: 6,423 bytes, 101 LF, SHA-256
  `10BB7EBFEB4F0D1C39276AD5E0D6C997F8064C3AC9109648F5802A279B969F3E`.
- Current target identity: 6,438 bytes, 101 LF, SHA-256
  `C49D9B5BE986873E0BAA2BC919C8866D7FB87C09EC92430E9936385D6AF07A30`.
- The only content delta is punctuation containment in one display-math
  formula: the first Arabic comma-plus-space was changed from `، ` to
  `\text{، }`, and the second Arabic comma at the line end was changed from
  `،` to `\text{، }`. Reversing exactly those two substitutions reconstructs
  the 6,423-byte predecessor and its recorded SHA-256 exactly.
- No Persian target and no other Arabic target was edited by this correction.

## Complete bounded replay

The replay resolved only the 722 source paths and 1,444 target paths named by
the closure manifest. It found zero missing files, source-pin mismatches,
target-hash mismatches, stable-order defects, strict-UTF-8 failures, CR bytes,
BOMs, NFC failures, or forbidden bidi controls.

- Source files: 722; bytes: 3,051,826; LF bytes: 75,457.
- Arabic targets: 722; bytes: 3,643,073; LF bytes: 73,206.
- Persian targets: 722; bytes: 3,948,090; LF bytes: 75,389.
- Updated closure-manifest SHA-256:
  `0CCA3735E506581BE93C87542FA1F8236281834B71831C9D767C4B43E5361952`.
- Updated complete paired target binding, over stable-order Arabic-then-Persian
  rows `closure_id|locale|target_path|UPPER_SHA256|bytes|LF_count`, joined by
  LF with no final LF:
  `C7ADBCC67F6D7C6ED79FF81EE2F12E8597A994EB4894BA1AAA2F6B1610B78BB4`.

## Limits

This receipt rebinds the current exact target bytes after one build-facing
punctuation repair. It does not rewrite or invalidate any earlier receipt. No
Git operation, publication, upload, or native/human review occurred. Completion
of the dependency build, PDF convergence, all-page rendering, extraction, and
accessibility replay remains a separate gate and is not claimed here.
