# Bounded integration shutdown and exact source resume

## Observed failure

The immutable receipt
`tmp/redo-20260906-reviewer/cardinality-source-93412578/RUN_RECEIPT.json`
has SHA-256
`63ef60cbbfe0b1ffae718b9a6d0ef1cd6d430fa2c13deadbabe6d5e103bf2aed`.
Acceptance, reconciliation, and source-readback-replay all exited zero and
were recorded PASS. The eight-output replay recorded no mismatches and source
snapshot `bb45cdb8403f90d69897994429083c846522e7720265c45b3b9e513aad391694`.

The wrapper then immediately sampled `parent.children(recursive=True)` and
raised `Completed steps left captured descendants live` if any child remained.
It provided no natural-exit grace period. Its exception handler then attempted
to kill descendants and wrote a final empty `owned_pids_not_drained` list.
The receipt does not preserve the intermediate descendant identities or their
exit timing. Therefore it cannot prove whether those historical processes
would have exited naturally or required cleanup. The evidenced workflow defect
is the immediate terminal check, not a demonstrated mathematical-stage failure.
The historical FAIL receipt was not rewritten or erased.

## Repair

Only `build/run_arabic_review_integration_20260906.py` was changed in production.
Its predecessor SHA-256 was
`9c3b6ea79254504b6b735142d86079e07f39a45ca391628c512f6c416d1b5df9`.

The wrapper now captures each descendant by PID **and creation time** during
execution, retains previously captured descendants after reparenting, and
uses fresh process handles to reject recycled PIDs. Its final natural-exit
drain is bounded to five seconds with 0.1-second polling. It does not signal
processes during that grace period. The aggregate 1 GiB memory cap remains
active during execution and drain. New descendants observed during drain are
captured too.

The drain records elapsed time, the captured identities, remaining owned PIDs,
and peak observed memory. Timeout or an observation error fails closed.
Existing failure cleanup is restricted to freshly revalidated captured
identities; recycled foreign PIDs are never cleanup targets. The installed
Windows `psutil.Process.kill` implementation was inspected and retains its
pre-emptive PID-reuse check. Cleanup uncertainty is explicitly recorded and
cannot qualify as a drained resume checkpoint.

The outer kernel Job Object guard was not edited. It remains responsible for
kernel-level containment; the polling logic does not claim to replace it.
No source or reviewer exporter, TeX engine, full integration run, or publication
was launched. One small, owned Python child was used only for a natural-exit
smoke test and exited zero without a signal.

## Tests and actual checkpoint admission

Executed:

```text
python -B -m unittest build.tests.test_arabic_review_integration_drain_20260908 -q
```

**15 tests passed in 1.085 seconds.** Coverage includes natural exit, timeout,
reparented descendants, children appearing during drain, process disappearance,
PID reuse, restricted failure cleanup, observation failure, memory cap,
invalid intervals, and the actual short-lived Python process. Resume tests
cover live-worker rejection, uncertain/non-drained receipt rejection, closure
conflict, source drift, and the exact existing source checkpoint.

The real `verified_source_resume` function admitted the current checkpoint,
without source derivation or export. The test forbids subprocess dispatch
during that admission. Observed result:

```json
{
  "receipt": "tmp/redo-20260906-reviewer/cardinality-source-93412578/RUN_RECEIPT.json",
  "receipt_sha256": "63ef60cbbfe0b1ffae718b9a6d0ef1cd6d430fa2c13deadbabe6d5e103bf2aed",
  "closure_sha256": "274bdb05f2bbe34ad447cebccb998dc5c3637b714384b45009c69257c4f288e2",
  "source_files_rehashed": 2166,
  "authority_identities_rechecked": 91,
  "status": "PASS"
}
```

This permits the owner to resume only the reviewer-generation lane from the
existing checkpoint after its separate reviewer fixes are ready. It does not
reclassify the old wrapper transaction as PASS, rerun its three source stages,
or establish reviewer/full-reader/publication acceptance.

## File identities

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `build/run_arabic_review_integration_20260906.py` | 16570 | `1d26de045d02945df1c310c1a288a7b20309c8ae0d347d14495515b4067c1e58` |
| `build/tests/test_arabic_review_integration_drain_20260908.py` | 10427 | `c01ebe99f071b9d7d5a0b13bba7d30359dc2778fc9f47dbbbc5d79fc9a16e8a0` |

Scope boundary: no outer-guard, source, generator, validator, RTL, reader, or
publication changes were made in this bounded task. No additional agents were
spawned.
