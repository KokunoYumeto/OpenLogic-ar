# Reviewer explanation readback repairs — 8 September 2026

Two bounded integration defects are corrected. No translation, raw decision,
canon claim, generator, rendered reader, or public record was changed.

## Corrections

1. The independent snapshot validator now compares canonical repair rationales
   and questions with their displayed forms through its existing finite
   `surface_literal` contract. For example, the recorded `A=Nat\setminus F`
   and displayed `A=Nat∖ F` are equivalent. Missing or different operators and
   reversed composition operands remain errors. Exact raw-ledger equality is
   still checked separately; non-repair assessment readback is unchanged.
2. The historical qualification batch-two fixture now reads the archived
   pre-cardinality OLP-0033 MSA and Classical sources. It verifies the complete
   transition ledger hash, exact two-transaction inventory, both archive byte
   counts and hashes, and agreement with the original qualification source
   declarations. It no longer combines current source bytes with an incomplete
   historical fixture. Current-source transition tests remain separate.

## Verification

The following bounded command passed **94 tests in 20.007 seconds**:

```text
python -B -m unittest build.tests.test_expert_review_explanation_display_20260908 build.tests.test_expert_review_qualification_batch2 build.tests.test_expert_review_cardinality_validator_20260908 build.tests.test_expert_review_cardinality_batch build.tests.test_expert_review_consolidated_repairs build.tests.test_expert_review_qualification_repairs -q
```

The new nine-test module renders the actual finite batch in memory and submits
raw canonical expected explanations to independent readback: all **23 current
choices, 25 CSV occurrence rows**, complete and priority shards pass. Seven
historical proposal IDs and existing qualification history remain covered by
the other focused modules. Adversarial checks reject deleted/replaced set
difference in every Markdown surface and CSV, deleted composition, reversed
composition operands, deletion of an unknown operator, and changed archive or
transition-ledger bytes. Synthetic question fixtures are test data, not new
translation decisions. No full export, TeX process, or publication was run.

This verifies reviewer projection and historical fixture integrity, not fresh
canon consultation or completion of the full translation audit.

## Exact identities

Paths below are relative to the repository. SHA-256 values identify the tested
files; predecessor copies preserve the complete prior bytes.

| Artifact | SHA-256 |
| --- | --- |
| `build/validate_expert_review_snapshot.py` | `86ffa94f36df12942731e190b770b6c9426b0bae2a7e3e4e7d2ec7ce71cb8681` |
| `build/tests/test_expert_review_qualification_batch2.py` | `49abaf9ee36783c8cd5b6654066195e10e5236aa0b331cee2079998ddd2a66c7` |
| `build/tests/test_expert_review_explanation_display_20260908.py` | `e72343ecfb5d4125ad9665c77470e99d00fe3c3a942d300a4f5a5a335435482a` |
| `evidence/classical/repairs/history/reviewer-readback-before-20260908/validate_expert_review_snapshot.py` | `b2b1dab655be23090e9ac50728296730881fb9a6c81599ba6a354ae6a43d1cfb` |
| `evidence/classical/repairs/history/reviewer-readback-before-20260908/test_expert_review_qualification_batch2.py` | `ac650457d7efb5d07f5b55ab65a09280f62c06635dc7e7dea2aa9cd47bae6acc` |
| `evidence/classical/repairs/OLP0033_NONENUMERABILITY_CONSTRUCTIONS_20260907.json` | `13aa46d70ae164ca7b2be107503238027c2fadc3d0204a3bc0c68d9feb26aecc` |
| `evidence/provenance/locale-ar/expert-review-binding-history/cardinality-source-batch-20260907/sources/OLP-0033-msa.tex` (12,479 bytes) | `82014f0a1361ae5462c5dd7d082e18a2e701dd23aa730a5550bd362ceb2b77e8` |
| `evidence/provenance/locale-ar/expert-review-binding-history/cardinality-source-batch-20260907/sources/OLP-0033-classical.tex` (11,568 bytes) | `6aea9fd0baec506686a0c45153e8dfdf7d556f89878f9bd2ea9f90c7b4e8f3e9` |

The next integration step belongs to the owner: include these bounded repairs
in the consolidated snapshot validation. This note does not claim that a full
snapshot or reader has been regenerated.
