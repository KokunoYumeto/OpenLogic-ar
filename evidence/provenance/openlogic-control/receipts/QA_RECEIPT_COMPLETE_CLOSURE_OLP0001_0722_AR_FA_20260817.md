# QA receipt — complete Open Logic direct-file closure, Arabic and Persian

Date: 2026-08-17

Status: `COMPLETE_FROZEN_722_FILE_CLOSURE_LOCAL`

## Frozen scope

- English authority: Open Logic commit
  `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`, tree
  `f67757bb9305b173634082ab4cefd5601a707a34`.
- Closure: OLP-0001 through OLP-0722; 722 source files, 722 Arabic targets
  and 722 independently authored Iranian-Persian targets.
- Remaining direct-file units: zero. There is no next translation cursor for
  this frozen source release.

## Exact replay

- Source bytes: 3,051,826; LF bytes: 75,457; manifest physical-line sum:
  76,179.
- Arabic target bytes: 3,643,076; LF bytes: 73,207.
- Persian target bytes: 3,948,079; LF bytes: 75,389.
- Complete source binding, over stable-order rows
  `closure_id|source_path|UPPER_SHA256|bytes` joined by LF with no final LF:
  `E5FBD3773FF80F2195E6EFA023EE51573E778BDF20629D3377B16FA09883FE51`.
- Complete paired target binding, over stable-order Arabic-then-Persian rows
  `closure_id|locale|target_path|UPPER_SHA256|bytes|LF_count` joined by LF
  with no final LF:
  `B6FEFA17CAA8B1BCDF891DC92B43CFDD9B3B2274830C1D024FE2AA0AB177B944`.

The replay resolved only the 722 source paths and 1,444 target paths named by
the lane-owned closure manifest. It found zero missing files, source pin
mismatches or target hash mismatches. Every target decoded as strict UTF-8,
used LF line endings, was NFC-normalized, contained no BOM or forbidden bidi
controls, and passed its Arabic/Persian glyph policy.

## Review authority and limits

The per-tranche paired receipts preserve the exact structural, carrier,
semantic-repair and independent-replay evidence for every unit. The terminal
OLP-0715--0722 receipt is
`QA_RECEIPT_OLP0715_0722_AR_FA_20260817.md`, SHA-256
`B46E55EE43FA7E585C1316ABDC49278263E67CD4335FD90E824FC17F4E134ABB`.
The final Arabic tranche also passed a separate read-only review. Neither
locale was used as a natural-language pivot for the other.

This receipt closes the direct-file translation and static-admission loop
only. A complete dependency build, PDF convergence, font/ToUnicode inspection,
text extraction, all-page rendering, accessibility audit and native/human
review remain separate gates. No Git operation, publication, upload or
external release occurred.
