# Current working sources and audit evidence — 8 September 2026

This is a preservation snapshot of ongoing work, not a new completed book or a replacement for the existing international-notation and Machrek-notation reader PDFs. It includes the earlier human-readable register and corrected content sources, with an additive snapshot of the newer work.

## Checked work

- The existing public snapshot plus the cardinality supplement matches all 2,166 current content files: 722 English reference files and 1,444 Arabic files across the two source trees. Ten Arabic files carry the already published corrections.
- The finite cardinality adapter admits exactly four preserved ledgers: 23 decisions, 25 patches, ten current Arabic sources and seven explicit proposal supersessions. It verifies exact byte identities, inverse/forward replay and source locations. It does not newly attest dictionary authority or replace mathematical semantic checks.
- The source-reference audit verifies 190 registry declarations and 257 amendment witnesses, 447 in total. Two registry references were refreshed; their quoted wording is unchanged. No amendment wording was changed.
- 58 focused tests pass: 16 adapter tests, four new visible-glyph regression tests, four independent visible-semantics tests and 34 existing RTL source tests. These are limited tests, not certification of a complete book.

## Explicitly unfinished work

- The adapter is not yet integrated into the complete acceptance and review-export pipeline.
- The new v7 visible-glyph check rejects all 14 known failing checks in the preserved older RTL probe; the control passes all 14. An old v6 PASS receipt therefore must not be read as a pass of the stronger v7 check.
- The delimiter-face candidate and corrected tableau fixture have not been rendered successfully. The last bounded TeX attempt could not acquire the machine-wide mutex and launched no engine. This snapshot does not claim that the RTL defects are fixed. The experimental code is supplied for inspection, separately from released reader files.
- The Classical-style reader, exhaustive decision review and final PDF page mapping remain unfinished. No reader PDF was rebuilt for this snapshot.

## Files and reproducibility

`SNAPSHOT_MANIFEST.json` identifies every selected live input and every exported byte sequence. `current/repo/` contains the current candidate files, source-reference history and selected supporting evidence. The previous public review material remains unchanged under `../2026-09-07/`.

The ZIP is an offline mirror of both dated directories. These are preservation copies, not a standalone runnable checkout. Where a local account name occurs in an implementation or evidence path, it is replaced by `LOCAL_USER`; the manifest records both original and exported hashes and marks the change. No credential file or private user-input log is included. Historical failure evidence remains failure evidence.

Human-readable entry points: [start here](START_HERE.md) and [full list](FULL_LIST.md).
