"""One capped write/verify transaction for the frozen Classical presentation.

This generates TeX source, not PDFs. No TeX engine, publication or retry runs.
The existing Windows job guard limits the complete owned tree to one GiB.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re

import psutil

from run_expert_review_readback_20260906 import CAP, Job, digest, execute


REPO = Path(__file__).resolve().parents[1]
CLOSURE = REPO / "evidence/classical/SOURCE_RECONCILIATION_CLOSURE_MANIFEST_20260905.json"
MATERIALIZATION = REPO / "evidence/classical/NOTATION_MATERIALIZATION_RECEIPT.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--source-closure-sha256", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{7,79}", args.run_id):
        raise ValueError("Invalid finite run ID")
    expected = args.source_closure_sha256
    if not re.fullmatch(r"[0-9a-f]{64}", expected) or digest(CLOSURE) != expected:
        raise ValueError("Explicit frozen source-closure identity differs")
    out = REPO / "tmp/redo-20260906-reviewer" / args.run_id
    if out.exists():
        raise FileExistsError("Run directory already exists; no overwrite or resubmission")
    out.mkdir()
    receipt = {
        "schema": "openlogic-bounded-classical-materialization-v1",
        "status": "RUNNING", "pid": os.getpid(),
        "process_create_time": psutil.Process().create_time(),
        "cap_bytes": CAP, "steps": [], "peak_tree_rss_bytes": 0,
        "worker_sha256": digest(Path(__file__)),
        "guard_sha256": digest(REPO / "build/run_expert_review_readback_20260906.py"),
        "materializer_sha256": digest(REPO / "build/materialize_classical_notation.py"),
        "source_closure_sha256": expected,
        "previous_materialization_receipt_sha256": digest(MATERIALIZATION) if MATERIALIZATION.exists() else None,
        "scope": "One source-addressed final presentation write and byte verification; no TeX, PDF acceptance, publication or retry.",
    }
    outer = None
    try:
        outer = Job()
        outer.assign()
        receipt["aggregate_kernel_job_assigned_before_child_launch"] = True
        for action in ("write", "verify"):
            if digest(CLOSURE) != expected:
                raise ValueError("Frozen closure changed before " + action)
            execute(out, receipt, outer, [
                "build/materialize_classical_notation.py", "--repo", str(REPO),
                "--mode", "final", "--action", action,
                "--source-closure", str(CLOSURE),
            ], name="presentation-" + action, deadline=900)
        data = json.loads(MATERIALIZATION.read_bytes())
        summary = data["summary"]
        if (data.get("status") != "PASS" or data.get("mode") != "final"
                or data.get("release_eligible") is not True
                or summary.get("units") != 722
                or summary.get("untreated_candidates") != 0
                or summary.get("source_files_with_failed_inverse") != 0
                or data.get("authority", {}).get("source_closure", {}).get("sha256", "").lower() != expected
                or digest(CLOSURE) != expected):
            raise ValueError("Final materialization inventory or source identity failed")
        receipt.update(status="PASS_PRESENTATION_BYTES_VERIFIED", summary=summary,
                       materialization_receipt_sha256=digest(MATERIALIZATION),
                       source_tree_sha256=data["source_tree_sha256"],
                       presentation_tree_sha256=data["presentation_tree_sha256"])
    except BaseException as error:
        receipt.update(status="FAIL", failure=repr(error))
    finally:
        if outer is not None:
            receipt["peak_kernel_job_committed_bytes"] = outer.peak()
            receipt["owned_pids_not_drained"] = [pid for pid in outer.pids() if pid != os.getpid()]
            if receipt["owned_pids_not_drained"]:
                receipt.update(status="FAIL", failure="Owned process inventory not drained")
            outer.close()
        temporary = out / "RUN_RECEIPT.json.tmp"
        temporary.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        temporary.replace(out / "RUN_RECEIPT.json")
    print(json.dumps(receipt), flush=True)
    return 0 if receipt["status"] == "PASS_PRESENTATION_BYTES_VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
