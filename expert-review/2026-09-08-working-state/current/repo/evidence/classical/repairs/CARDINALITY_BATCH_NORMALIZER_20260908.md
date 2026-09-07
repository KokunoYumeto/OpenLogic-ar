# Finite cardinality repair normalizer — 2026-09-08

Implemented a read-only admission adapter for exactly four applied repair ledgers: 23 decisions, 25 patches, ten changed Arabic source files, and seven explicit proposal supersessions. This is implementation evidence, not completion of the translation audit, expert attestation, a PDF build, or publication.

## Scope and reconciliation

The current bounded instruction from the parent task was:

> Proceed now with the bounded shared normalizer implementation requested in my previous message: new build/cardinality_repair_batch_20260908.py, focused tests and evidence note ONLY. Preserve all exact four ledgers. Normalize23decisions25patches10sources with their heterogeneous schemas, inverse/forward proofs, typed normalized exact locations and rationale/authority/raw/status preserved, seven explicit proposal IDs. No existing generator/finalizer/validator/registry/source edits or exports/TeX/publication. Please reread previous message for full criteria; return actual implementation/tests. Date now2026-09-08.

After context reconstruction, the current instruction was reconciled against the complete new adapter and test file, then both executable checks below were rerun on live inputs. Only the new adapter, its focused test file, and this note were created for this subtask. Existing consumers, sources, ledgers, registries and historical records remain unchanged.

## API and evidence retained

`build.cardinality_repair_batch_20260908.normalize(repo=REPO, english_root=ENGLISH)` returns frozen typed `Batch`, `Ledger`, `Decision`, `SourceTransition`, `Patch`, `Location`, `Witness`, `Supersession` and `Identity` records. An optional read-only `read` callback supports in-memory tests. The module performs no file writes, scans, network requests, TeX or publication operations.

Each ledger remains available as exact original bytes. Each decision and patch also retains its complete original JSON object without dropping fields; the JSON string representation is compacted, not claimed byte-identical. Original rationale, authority claims, recording mode, provisional status and witness phase remain intact. Verified source phase is a separate field, so a historically recorded candidate is not silently relabelled.

All ten current sources must match their exact ledger byte count and SHA-256. Unique inverse substitutions recover exact predecessor identities, and forward replay in original application order must reproduce current bytes. The two saved reduction predecessors must also match byte-for-byte. Every patch has proved ownership and before/after UTF-8 byte boundaries, one-based inclusive occupied line ranges, exact literals and source-line excerpts. Declared owners are corroborated against independent per-decision wording/bindings; the reduction schema uses a unique exact unit/edition/path/before/after/occurrence join.

Original application order is retained separately from physical source order. This distinction matters for the Classical reduction patches and equinumerosity NFC patch. Patch boundary checks are strict. Legacy witnesses ending in a newline may retain their recorded endpoint on the following line only when exact bytes and the full recorded excerpt prove that convention; their normalized range uses occupied lines.

The seven pairing proposal IDs are explicit constants, joined to the exact historical ledger. Only `status`, `page_status` and `occurrence_bindings` differ between their preserved proposal and applied records. The status transition is exactly `proposed-unapplied` to `provisional-in-use`; previous and current complete objects are both retained. This is not a claim of expert approval.

Exactly 23 named inputs are read: four live ledgers, ten current Arabic sources, five frozen English sources, one shared configuration file, two saved reduction predecessors and one proposal-history ledger. Every input is reread after validation to detect concurrent changes. Each input is bounded below 2 MiB.

## Exact ledger admission

Paths below are relative to `evidence/classical/repairs/`.

| Ledger | Bytes | SHA-256 |
| --- | ---: | --- |
| `OLP0031_0032_PAIRING_CONSTRUCTIONS_20260907.json` | 155011 | `86da173ac4083f2effe84cf60efe0e726e6caf79023aa8fa3ae6d852d73c8bc9` |
| `OLP0033_NONENUMERABILITY_CONSTRUCTIONS_20260907.json` | 71615 | `13aa46d70ae164ca7b2be107503238027c2fadc3d0204a3bc0c68d9feb26aecc` |
| `OLP0034_REDUCTION_CONSTRUCTIONS_20260907.json` | 19497 | `8addb4be1b7b8cc92f7044ab4ef357de6ea8105e134ac4ad921d9e5348580631` |
| `OLP0035_EQUINUMEROSITY_CONSTRUCTIONS_20260907.json` | 78958 | `4615dbc5636212dc0c9ca3c2244afef44f13a49d8a330ffd5dd6ce51415f68ed` |

Proposal predecessor: `history/pairing-before-applied-20260907/OLP0031_0032_PAIRING_CONSTRUCTIONS_20260907.json`, SHA-256 `8ccc0f7f691271e37234d17812593df3748833efbd9578e4b01dfbbd217948af`.

## Executed checks

Run from `C:/interlanguage-production/openlogic-arabic-dual-notation/repo`:

```text
python -X utf8 -B -m unittest build.tests.test_cardinality_repair_batch_20260908
Ran 16 tests in 1.225s — OK

python -X utf8 -B -m build.cardinality_repair_batch_20260908
PASS_FINITE_CARDINALITY_ADMISSION
4 ledgers; 23 decisions; 25 patches; 10 changed sources;
7 explicit proposal supersessions; 23 inputs
```

Tests cover repeatability, full raw record preservation, every inverse/forward replay and exact location, distinct source/application order, seven explicit supersessions, corrupt ledgers/sources/history/predecessors, reordered patches, wrong IDs, missing/incorrect/ambiguous ownership, wrong patch/boundary, non-unique literals and concurrent input changes. Adversarial schema tests repin only in-memory test copies to exercise lower-level rejection beyond the production immutable ledger checks.

Implementation SHA-256: `c5d435217cf43502186ab66f63225094c920d9231cd43952f8cd6c5be30a0b89`.

Test SHA-256: `65fee2d131b002dd41a3013fcfa3be6de0af6cb989b47ac867eda7113459a57b`.

## Next integration boundary

The parent task owns connecting this finite adapter to source acceptance and reviewer generation. No consumer integration or complete export was performed here. Existing mathematical construction suites remain responsible for semantic/formula checks; this adapter does not newly attest dictionary authorities or mathematical correctness.
