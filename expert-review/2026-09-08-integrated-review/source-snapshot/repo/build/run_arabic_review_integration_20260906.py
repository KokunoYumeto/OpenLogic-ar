"""Finite source/index integration with a 1 GiB owned-tree cap; no TeX/retries."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import psutil


REPO = Path(__file__).resolve().parents[1]
CAP = 1_073_741_824
DRAIN_SECONDS = 5.0
DRAIN_POLL_SECONDS = 0.1


def capture_descendants(parent: psutil.Process,
                        captured: set[tuple[int, float]]) -> None:
    """Remember identities while descendants still have the owned parent."""
    for member in parent.children(recursive=True):
        try:
            captured.add((member.pid, member.create_time()))
        except psutil.NoSuchProcess:
            pass


def live_captured(captured: set[tuple[int, float]]) -> list[psutil.Process]:
    """Reopen each PID and reject reuse; a PID alone never grants ownership."""
    live = []
    for pid, created in sorted(captured):
        try:
            member = psutil.Process(pid)
            if member.create_time() == created and member.is_running():
                live.append(member)
        except psutil.NoSuchProcess:
            pass
    # AccessDenied and other observation failures deliberately propagate.
    return live


def captured_tree_rss(parent: psutil.Process,
                      members: list[psutil.Process]) -> int:
    rss = 0
    for member in [parent, *members]:
        try:
            rss += member.memory_info().rss
        except psutil.NoSuchProcess:
            pass
    return rss


def terminate_captured(captured: set[tuple[int, float]]) -> list[int]:
    """Failure cleanup only; fresh psutil handles retain PID-reuse guards."""
    owned = live_captured(captured)
    for child in reversed(owned):
        try:
            child.kill()
        except psutil.NoSuchProcess:
            pass
    psutil.wait_procs(owned, timeout=15)
    return [child.pid for child in live_captured(captured)]


def drain_captured(parent: psutil.Process, captured: set[tuple[int, float]], *,
                   timeout: float = DRAIN_SECONDS,
                   poll_interval: float = DRAIN_POLL_SECONDS) -> dict:
    """Bounded natural-exit grace period; never signal or kill a process.

    Previously observed descendants stay tracked after reparenting. New
    descendants are captured while this worker remains alive. The outer
    kernel job guard remains responsible for complete kernel containment.
    """
    if not 0 < timeout <= DRAIN_SECONDS or not 0 < poll_interval <= timeout:
        raise ValueError("Invalid bounded natural-drain interval")
    started = time.monotonic()
    peak = 0
    while True:
        capture_descendants(parent, captured)
        live = live_captured(captured)
        rss = captured_tree_rss(parent, live)
        peak = max(peak, rss)
        if rss >= CAP:
            raise RuntimeError("Captured owned tree reached the 1 GiB cap during drain")
        elapsed = time.monotonic() - started
        if not live or elapsed >= timeout:
            return {
                "status": "PASS" if not live else "FAIL_TIMEOUT",
                "timeout_seconds": timeout, "elapsed_seconds": elapsed,
                "peak_observed_bytes": peak,
                "captured_process_identities": [
                    {"pid": pid, "process_create_time": created}
                    for pid, created in sorted(captured)
                ],
                "owned_pids_not_drained": [member.pid for member in live],
            }
        time.sleep(min(poll_interval, timeout - elapsed))


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verified_source_resume(checkpoint: Path | None = None,
                           explicit_closure_sha256: str | None = None) -> dict:
    """Resume only the exact completed source checkpoint, not its failed export."""
    previous = checkpoint or REPO / "tmp/redo-20260906-reviewer/redo-r7/RUN_RECEIPT.json"
    previous = previous.resolve()
    if not previous.is_relative_to(REPO / "tmp/redo-20260906-reviewer"):
        raise ValueError("Source checkpoint is outside the bounded integration directory")
    old = json.loads(previous.read_text(encoding="utf-8"))
    if (old.get("schema") != "openlogic-bounded-review-integration-v1" or
            old.get("status") not in {"FAIL", "PASS_SOURCE_RECONCILED_PENDING_PRESENTATION_AND_REVIEW"} or
            old.get("owned_pids_not_drained") != [] or old.get("cleanup_failure") is not None):
        raise ValueError("Prior transaction is not terminal and drained")
    if psutil.pid_exists(old["pid"]):
        live = psutil.Process(old["pid"])
        if abs(live.create_time() - old["process_create_time"]) < 0.01:
            raise ValueError("Prior captured worker remains live")
    completed = old.get("steps", [])[:3]
    if [s.get("name") for s in completed] != ["acceptance", "reconciliation", "source-readback-replay"]:
        raise ValueError("Prior source stage inventory differs")
    for stage in completed:
        log = previous.parent / (stage["name"] + ".log")
        if stage.get("status") != "PASS" or stage.get("exit_code") != 0 or digest(log) != stage["log_sha256"]:
            raise ValueError("Prior successful source stage is unverifiable")
    closure_path = REPO / "evidence/classical/SOURCE_RECONCILIATION_CLOSURE_MANIFEST_20260905.json"
    recorded = old.get("source_checkpoint", {}).get("closure_sha256")
    if recorded and explicit_closure_sha256 and recorded != explicit_closure_sha256:
        raise ValueError("Explicit closure identity conflicts with completed checkpoint")
    # A full transaction can fail during export after all three source stages
    # succeeded. Its immutable receipt need not be rewritten to resume export:
    # require an explicit closure identity, the exact successful replay log,
    # and all current authority/source bytes below. Never repeat source writes.
    expected = ((recorded or explicit_closure_sha256) if checkpoint else
                "1970afcd573ace21d0a40c170ef912c581a8c1c6fad323441ea013506d1d6e36")
    if (not isinstance(expected, str) or len(expected) != 64 or
            any(char not in "0123456789abcdef" for char in expected)):
        raise ValueError("Source checkpoint lacks its exact closure identity")
    if digest(closure_path) != expected:
        raise ValueError("Exact completed source manifest changed")
    closure = json.loads(closure_path.read_text(encoding="utf-8"))
    replay = json.loads((previous.parent / "source-readback-replay.log").read_text(encoding="utf-8"))
    if (replay.get("status") != "PASS" or replay.get("output_count") != 8
            or replay.get("mismatches") != [] or replay.get("snapshot") != closure["source_snapshot_sha256"]):
        raise ValueError("Completed eight-output source replay is not exact")
    identities = list(closure["authority_files"])
    for key in ("frozen_baseline", "baseline_correction_overlay", "math_text_declarations",
                "structural_reviews", "formal_repairs", "general_reviews"):
        identities.append(closure[key])
    for identity in identities:
        target = (REPO / identity["path"]).resolve()
        if not target.is_relative_to(REPO) or digest(target) != identity["sha256"] or target.stat().st_size != identity["bytes"]:
            raise ValueError("Completed source authority changed: " + identity["path"])
    english_root = Path("source-snapshot/english")
    source_count = 0
    if len(closure["units"]) != 722:
        raise ValueError("Completed source unit count differs")
    for unit in closure["units"]:
        english_path = (english_root / unit["source_path"]).resolve()
        if not english_path.is_relative_to(english_root) or digest(english_path) != unit["english_sha256"]:
            raise ValueError("Completed English source changed: " + unit["id"])
        source_count += 1
        for kind in ("msa", "classical"):
            identity = unit[kind]
            target = (REPO / identity["path"]).resolve()
            if (not target.is_relative_to(REPO / "source/locale") or digest(target) != identity["sha256"]
                    or target.stat().st_size != identity["bytes"]):
                raise ValueError("Completed Arabic source changed: " + unit["id"])
            source_count += 1
    return {"receipt": previous.relative_to(REPO).as_posix(), "receipt_sha256": digest(previous),
            "closure_sha256": expected, "source_files_rehashed": source_count,
            "authority_identities_rechecked": len(identities), "status": "PASS"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--reviewer-only", action="store_true",
                       help="Resume an exact verified source checkpoint; do not repeat source derivation")
    modes.add_argument("--source-only", action="store_true",
                       help="Finish source derivation/replay without starting the reviewer export")
    parser.add_argument("--source-checkpoint", type=Path,
                        help="Explicit terminal source-only receipt for --reviewer-only")
    parser.add_argument("--source-closure-sha256",
                        help="Exact completed closure hash when a full transaction failed only at export")
    args = parser.parse_args()
    if args.source_checkpoint and not args.reviewer_only:
        raise ValueError("--source-checkpoint requires --reviewer-only")
    if args.source_closure_sha256 and not (args.source_checkpoint and args.reviewer_only):
        raise ValueError("--source-closure-sha256 requires an explicit reviewer-only checkpoint")
    if not args.run_id or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in args.run_id):
        raise ValueError("run-id must contain only lowercase letters, digits and hyphens")
    out = REPO / "tmp/redo-20260906-reviewer" / args.run_id
    snapshot = REPO / "tmp" / ("expert-index-" + args.run_id)
    if out.exists() or snapshot.exists():
        raise FileExistsError("Unique integration output already exists; do not overwrite/resubmit")
    resumed = verified_source_resume(args.source_checkpoint, args.source_closure_sha256) if args.reviewer_only else None
    out.mkdir()
    receipt = {
        "schema": "openlogic-bounded-review-integration-v1", "status": "RUNNING",
        "pid": os.getpid(), "process_create_time": psutil.Process().create_time(),
        "cap_bytes": CAP, "peak_observed_bytes": 0, "steps": [],
        "snapshot": snapshot.relative_to(REPO).as_posix(),
        "worker_sha256": digest(Path(__file__)),
        "scope": "Current source identity reconciliation and working reviewer-index generation; no final semantic/PDF/publication acceptance.",
    }
    if resumed:
        receipt["resumed_source_checkpoint"] = resumed

    def save() -> None:
        temporary = out / "RUN_RECEIPT.json.tmp"
        temporary.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        temporary.replace(out / "RUN_RECEIPT.json")

    steps = [
        ("acceptance", ["build/generate_full_translation_acceptance_audit.py", "--repo", ".", "--write", "--json"], 1200),
        ("reconciliation", ["build/finalize_classical_source_reconciliation.py", "--repo", ".", "--write", "--json"], 900),
        ("source-readback-replay", ["-c", "from pathlib import Path; import json; from build import finalize_classical_source_reconciliation as f; r=Path('.').resolve(); o,s=f.derive(r,r/'evidence/classical/SOURCE_RECONCILIATION_METADATA_20260905.json'); bad=[p for p,b in o.items() if (r/p).read_bytes()!=b]; print(json.dumps({'status':'FAIL' if bad else 'PASS','output_count':len(o),'mismatches':bad,'snapshot':s['source_snapshot_sha256']},indent=2)); raise SystemExit(bool(bad))"], 900),
        ("reviewer-generation", ["build/generate_expert_review_index.py", "--repo", ".",
            "--output-json", str(snapshot / "EXPERT_REVIEW_INDEX.json"),
            "--output-md", str(snapshot / "EXPERT_REVIEW_INDEX.md"),
            "--output-start-here-md", str(snapshot / "EXPERT_REVIEW_START_HERE.md"),
            "--output-priority-md", str(snapshot / "EXPERT_REVIEW_PRIORITY_ONLY.md"),
            "--output-csv", str(snapshot / "EXPERT_REVIEW_OCCURRENCES.csv"),
            "--output-reviewer-index-dir", str(snapshot / "reviewer-index")], 1200),
    ]
    if args.reviewer_only:
        steps = steps[-1:]
    elif args.source_only:
        steps = steps[:3]
    save()
    parent = psutil.Process()
    captured: set[tuple[int, float]] = set()
    process = None
    try:
        for name, arguments, deadline in steps:
            entry = {"name": name, "status": "RUNNING", "arguments": arguments}
            receipt["steps"].append(entry)
            if arguments[0] != "-c":
                entry["script_sha256"] = digest(REPO / arguments[0])
            log_path = out / (name + ".log")
            with log_path.open("xb") as log:
                process = subprocess.Popen([sys.executable, "-X", "utf8", "-B", *arguments],
                    cwd=REPO, stdout=log, stderr=subprocess.STDOUT)
                entry["pid"] = process.pid
                entry["process_create_time"] = psutil.Process(process.pid).create_time()
                captured.add((entry["pid"], entry["process_create_time"]))
                save()
                started = time.monotonic()
                last_saved = started
                while process.poll() is None:
                    capture_descendants(parent, captured)
                    rss = captured_tree_rss(parent, live_captured(captured))
                    receipt["peak_observed_bytes"] = max(receipt["peak_observed_bytes"], rss)
                    if rss >= CAP:
                        raise RuntimeError("Captured owned tree reached the 1 GiB cap")
                    if time.monotonic() - started >= deadline:
                        raise RuntimeError("Bounded step deadline reached: " + name)
                    if time.monotonic() - last_saved >= 5:
                        save()
                        last_saved = time.monotonic()
                    time.sleep(0.25)
            entry.update(exit_code=process.returncode, log_sha256=digest(log_path),
                         status="PASS" if process.returncode == 0 else "FAIL")
            save()
            print(json.dumps(entry), flush=True)
            if process.returncode:
                raise RuntimeError("Integration step failed: " + name)
        if args.source_only:
            closure = REPO / "evidence/classical/SOURCE_RECONCILIATION_CLOSURE_MANIFEST_20260905.json"
            receipt["source_checkpoint"] = {
                "closure_path": closure.relative_to(REPO).as_posix(),
                "closure_sha256": digest(closure),
            }
            receipt["status"] = "PASS_SOURCE_RECONCILED_PENDING_PRESENTATION_AND_REVIEW"
        else:
            receipt["status"] = "PASS_GENERATED_PENDING_INDEPENDENT_READBACK"
            receipt["snapshot_json_sha256"] = digest(snapshot / "EXPERT_REVIEW_INDEX.json")
        receipt["natural_exit_drain"] = drain_captured(parent, captured)
        receipt["peak_observed_bytes"] = max(
            receipt["peak_observed_bytes"], receipt["natural_exit_drain"]["peak_observed_bytes"])
        receipt["owned_pids_not_drained"] = receipt["natural_exit_drain"]["owned_pids_not_drained"]
        if receipt["owned_pids_not_drained"]:
            raise RuntimeError("Completed steps exceeded bounded natural-exit drain")
    except BaseException as error:
        receipt.update(status="FAIL", failure=str(error))
        # Cleanup remains fail-closed and only targets freshly revalidated
        # captured identities. A recycled PID is never a cleanup target.
        try:
            capture_descendants(parent, captured)
            receipt["owned_pids_not_drained"] = terminate_captured(captured)
        except Exception as cleanup_error:
            receipt["cleanup_failure"] = str(cleanup_error)
            # Unknown liveness must never be serialized as a drained worker.
            receipt["owned_pids_not_drained"] = sorted({pid for pid, _created in captured})
        if process is not None:
            process.poll()
        save()
        raise
    save()
    print(json.dumps(receipt), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
