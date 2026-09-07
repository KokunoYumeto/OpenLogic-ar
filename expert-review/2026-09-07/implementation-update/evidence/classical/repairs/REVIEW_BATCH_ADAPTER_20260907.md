# Next Arabic source batch: reviewer adapter and independent readback

Date: 2026-09-07. Status: bounded source/reviewer-code checks passed; no export,
reader build, page certification, or publication performed by this lane.

## Scope and result

The complete active objective was read before implementation. The current
consolidated cursor was read, including its explicit warning that the accepted
closure, review snapshot, and public package predate the new source changes.
The full Arabic commission remains unfinished. This work only implements the
review admission/readback needed for the next substantive source batch.

The producer now admits exactly 16 new choices from three pinned ledgers:
six function constructions, six modal/many-valued semantic decisions, and four
adjective constructions. It contributes 26 exact English–Arabic passage pairs,
not 26 new decisions. Complete canonical choice rows and complete source ledgers
remain embedded unchanged. Motivations and expert questions come from the
canonical rows. Modal-schema display choices are explicitly projected from its
actual source patches; the semantic heading is not presented as an English
quotation. No original translator motive, new dictionary consultation, historical
attestation, rendered page, or finished-reader claim is invented.

The independent validator does not import or execute the producer. It reads
the three separately pinned ledgers, frozen English baseline, source bytes,
inverse/forward patches, exact recorded contexts, and source phrases itself.
Both modules verify identities before adapting. A known schema under an
unapproved path, a changed ledger, an unknown stale source identity, or source
drift fails closed.

Two exact historical transitions are supported, not a general stale-hash
exception:

- Classical function-basics: `8183c83e20fc04ced33d83554ebb142f94b7c8bf323b992336a25b9153db2498`
  is recovered from the current `0b2c8cf8289e439ad35305560c6887529d7e0505b66d46363914caad6d583d87`
  by the pinned functions ledger. The earlier roots note remains intact and its
  unchanged Classical companion receives a current location plus an explicitly
  historical assessed witness.
- Classical function-kinds: `8a73d76a7d09e54a6956468280c054ded5243f4f4a43ed05aee76de126dd9ca9`
  is recovered from current `3a74dd4fc979afc520df1954cc09c78327ac63c6954852f77e0a8cb9b9a38922`
  by the pinned adjective ledger. The five affected function-review passages
  retain their assessed-after locations separately and link the current exact
  wording one line earlier. The old full-file identities are not relabelled live.

English display anchors were narrowed to exact relevant clauses already contained
in the canonical evidence. In particular, the iterated-modality repair quotes
“Possibly necessarily” from its own English paragraph, not the adjacent rain
example. All broader original contexts remain in the canonical records.

A pre-existing double-rendering path would turn `m\ge2` into `mge2` and discard
other formula syntax. For these admitted new records only, registered prose
tokens are expanded but exact TeX operators/braces are retained through the
Arabic span and CSV rendering. This is a faithful source-review display, not a
claim of typeset mathematical layout. The older display contracts are unchanged.

## Fixed input identities

| Ledger | Bytes | SHA-256 |
|---|---:|---|
| `OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907.json` | 137782 | `eb0e436d546c867a56d66767a24f66a2d687ea254ed83c9123aa0c2106a8e0c7` |
| `OLP0394_0399_0400_0404_0409_MODAL_SCOPE_20260907.json` | 98459 | `6d29d66c0db082e2c348cf8a30219e9d6ae11b80e14d0ecfdd2cbc2c79a6f4cd` |
| `OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907.json` | 64402 | `90364663431ea9dad27fef1a427acf033498f1cd95f8cbea29cc665f41186c79` |

## Executed verification

Final command from the production repository:

```text
python -X utf8 -B -m unittest build.tests.test_expert_review_next_source_batch build.tests.test_expert_review_consolidated_repairs build.tests.test_expert_review_applied_repairs build.tests.test_expert_review_snapshot_repairs -v
```

Result: **82 tests passed**, exit 0, 16.472 seconds. The new module has 11 tests.
Earlier exploratory runs exposed and then corrected the long-English-context
locator problem and the double-rendering defect; their failures were not treated
as source acceptance. The final combined run is the evidence cited here.

Coverage includes all 16 normalized records, all 26 pairs, actual bounded
reconciliation, actual in-memory provenance and CSV rendering, complete canonical
reasons/questions, exact before/current/historical-after identities, all five
shifted function-kinds locations, the earlier roots companion, ledger/schema/path
forgeries, altered operator, dropped/duplicated occurrences, forged provenance,
and changed source bytes outside the selected phrase. Existing earlier repair
regressions also pass. No full 1,050-entry export was generated or certified.

## Implementation identities at handoff

| File | Bytes | SHA-256 |
|---|---:|---|
| `build/generate_expert_review_index.py` | 469316 | `5c17b0657b524c85cae87d9b99d85ab6dfadbd8e5eac2a2996cc9d8dc470d9f0` |
| `build/validate_expert_review_snapshot.py` | 112480 | `8ec0dad34d2415a6424d57b31a67a726fb54e9235c37ed1230433611e905e3f3` |
| `build/tests/test_expert_review_next_source_batch.py` | 10974 | `b2cff603459e66eae28888a3ae23a19c533b84905bc0aa3b6db38718385993b5` |

## Remaining owner integration

No source, source ledger, registry, acceptance metadata, closure manifest, or
public artifact was edited by this lane. Full index regeneration must wait for
the owner's consolidated source-binding/amendment integration, then undergo
the full independent readback including preservation of all original raw rows.
This code/test result must not be described as that full export having happened.
Materialization, TeX/RTL/font/link/visual/replay QA, actual final page bindings,
remaining whole-corpus review coverage, and worthwhile public release remain
separate required work. A labelled source-review supplement can be preserved
without pretending it is a new finished book or redoing a book for each repair.

## Latest bounded delivery instruction, preserved verbatim

> Root revalidated 61 source/admission tests PASS (9.004s). Current direct user request prioritizes online preservation and two shareable links. Source-admission worker is packaging the checked 16-choice batch as a clearly labelled supplement to existing 1,050-entry public snapshot; no full index regeneration or new book is implied. Please finish your bounded adapter tests and note, then stop at saved-code boundary. Do not expand into registry refresh, export, closure, or builds. Root will preserve your tested code if ready, but public supplement will honestly distinguish pending full integration.

Next action: owner readback of these three implementation files and this note;
then consolidated integration when its remaining source-binding work is ready.
This lane stops at the requested saved-code boundary, not at goal completion.
