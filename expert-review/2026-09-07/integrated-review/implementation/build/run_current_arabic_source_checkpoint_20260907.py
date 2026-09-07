"""One explicitly selected integration stage under the existing 1 GiB job guard.

Preserve exact predecessor source-output bytes before the source-only stage.
No TeX, automatic retry, source editing, or publication is performed here.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys

from build import finalize_classical_source_reconciliation as finalizer
from build import run_expert_review_readback_20260906 as guard


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--reviewer-source-checkpoint", type=Path)
    args = parser.parse_args()
    if not args.run_id or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in args.run_id):
        raise ValueError("Invalid bounded run ID")
    repo = guard.REPO
    out = repo / "tmp/redo-20260906-reviewer" / (args.run_id + "-guard")
    if out.exists():
        raise FileExistsError("Guard output exists; do not overwrite or resubmit")
    out.mkdir()
    receipt = {
        "schema": "openlogic-current-integration-hard-guard-v1",
        "status": "PREPARING", "pid": os.getpid(), "steps": [],
        "cap_bytes": guard.CAP, "peak_tree_rss_bytes": 0,
        "worker_sha256": guard.digest(Path(__file__)),
        "guard_sha256": guard.digest(Path(guard.__file__)),
        "preserved_predecessors": [],
    }
    arguments = ["build/run_arabic_review_integration_20260906.py", "--run-id", args.run_id]
    if args.reviewer_source_checkpoint:
        checkpoint = args.reviewer_source_checkpoint.resolve()
        if not checkpoint.is_relative_to(repo / "tmp/redo-20260906-reviewer"):
            raise ValueError("Source checkpoint escaped the bounded directory")
        arguments += ["--reviewer-only", "--source-checkpoint", str(checkpoint)]
        deadline = 1300
    else:
        arguments += ["--source-only"]
        deadline = 3100
        paths = list(finalizer.OUTPUTS.values()) + [
            "evidence/classical/FULL_TRANSLATION_ACCEPTANCE_AUDIT.json",
            "evidence/classical/FULL_TRANSLATION_ACCEPTANCE_AUDIT.md",
        ]
        for relative in paths:
            source = repo / relative
            target = out / "predecessors" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            if source.stat().st_size != target.stat().st_size or guard.digest(source) != guard.digest(target):
                raise ValueError("Predecessor preservation differs: " + relative)
            receipt["preserved_predecessors"].append({
                "path": relative, "bytes": target.stat().st_size,
                "sha256": guard.digest(target),
                "copy": target.relative_to(repo).as_posix(),
            })
    outer = None
    try:
        outer = guard.Job()
        outer.assign()
        receipt["aggregate_kernel_job_assigned_before_child_launch"] = True
        guard.execute(out, receipt, outer, arguments, name="integration", deadline=deadline)
        receipt["status"] = "PASS"
    except BaseException as exc:
        receipt.update(status="FAIL", failure=repr(exc))
    finally:
        if outer:
            receipt["peak_kernel_job_committed_bytes"] = outer.peak()
            receipt["owned_pids_not_drained"] = [pid for pid in outer.pids() if pid != os.getpid()]
            if receipt["owned_pids_not_drained"]:
                receipt.update(status="FAIL", failure="Owned process inventory not drained")
            outer.close()
        temporary = out / "RUN_RECEIPT.json.tmp"
        temporary.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(out / "RUN_RECEIPT.json")
    print(json.dumps(receipt, ensure_ascii=False), flush=True)
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
