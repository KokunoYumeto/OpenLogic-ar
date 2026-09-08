"""One finite, owned-tree readback of a receipted snapshot; no generator or retry.

Windows nested jobs enforce a 1 GiB aggregate committed-memory ceiling before
the child starts. RSS is also sampled for the complete owned tree. A separate
inner job permits draining the validator and all descendants without killing the
receipt writer or touching a foreign worker. All stage receipts are retained.
"""
from __future__ import annotations

import argparse
import ctypes
from ctypes import wintypes
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
SNAPSHOT = REPO / "tmp/expert-index-redo-r7b"
PREVIOUS = REPO / "tmp/expert-index-redo-r6"
GENERATION = REPO / "tmp/redo-20260906-reviewer/redo-r7b/RUN_RECEIPT.json"
EXPECTED_JSON = "6fa301bed229852e94b2568af96dc77577f8f2e4a89d1ff958b89018d8d3f905"
OUTPUT = SNAPSHOT / "READBACK_VALIDATION.json"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


class Job:
    """Small Windows job wrapper; no PID-directed termination is used."""
    def __init__(self, *, kill_on_close=False):
        if os.name != "nt":
            raise RuntimeError("This guarded runner requires Windows job-object enforcement")
        self.api = ctypes.WinDLL("kernel32", use_last_error=True)
        self.api.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        self.api.CreateJobObjectW.restype = wintypes.HANDLE
        self.api.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        self.api.SetInformationJobObject.restype = wintypes.BOOL
        self.api.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD, ctypes.c_void_p]
        self.api.QueryInformationJobObject.restype = wintypes.BOOL
        self.api.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        self.api.AssignProcessToJobObject.restype = wintypes.BOOL
        self.api.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
        self.api.TerminateJobObject.restype = wintypes.BOOL
        self.api.GetCurrentProcess.restype = wintypes.HANDLE
        self.api.CloseHandle.argtypes = [wintypes.HANDLE]
        self.api.CloseHandle.restype = wintypes.BOOL

        class BasicLimits(ctypes.Structure):
            _fields_ = [("process_time", ctypes.c_longlong), ("job_time", ctypes.c_longlong),
                        ("flags", wintypes.DWORD), ("minimum_working_set", ctypes.c_size_t),
                        ("maximum_working_set", ctypes.c_size_t), ("active_process_limit", wintypes.DWORD),
                        ("affinity", ctypes.c_size_t), ("priority", wintypes.DWORD), ("scheduling", wintypes.DWORD)]

        class IoCounters(ctypes.Structure):
            _fields_ = [(name, ctypes.c_ulonglong) for name in
                        ("read_ops", "write_ops", "other_ops", "read_bytes", "write_bytes", "other_bytes")]

        class ExtendedLimits(ctypes.Structure):
            _fields_ = [("basic", BasicLimits), ("io", IoCounters),
                        ("process_memory_limit", ctypes.c_size_t), ("job_memory_limit", ctypes.c_size_t),
                        ("peak_process_memory", ctypes.c_size_t), ("peak_job_memory", ctypes.c_size_t)]

        self.limits_type = ExtendedLimits
        self.handle = self.api.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = ExtendedLimits()
        limits.basic.flags = 0x200 | (0x2000 if kill_on_close else 0)  # JOB_MEMORY, KILL_ON_JOB_CLOSE
        limits.job_memory_limit = CAP
        if not self.api.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            error = ctypes.WinError(ctypes.get_last_error())
            self.close()
            raise error

    def assign(self, process_handle=None):
        handle = self.api.GetCurrentProcess() if process_handle is None else wintypes.HANDLE(int(process_handle))
        if not self.api.AssignProcessToJobObject(self.handle, handle):
            raise ctypes.WinError(ctypes.get_last_error())

    def pids(self):
        class PidList(ctypes.Structure):
            _fields_ = [("assigned", wintypes.DWORD), ("count", wintypes.DWORD),
                        ("values", ctypes.c_size_t * 64)]
        result = PidList()
        if not self.api.QueryInformationJobObject(self.handle, 3, ctypes.byref(result), ctypes.sizeof(result), None):
            raise ctypes.WinError(ctypes.get_last_error())
        if result.assigned > 64 or result.count > 64:
            raise RuntimeError("Owned process inventory exceeds the finite 64-process guard")
        return list(result.values[:result.count])

    def peak(self):
        result = self.limits_type()
        if not self.api.QueryInformationJobObject(self.handle, 9, ctypes.byref(result), ctypes.sizeof(result), None):
            raise ctypes.WinError(ctypes.get_last_error())
        return int(result.peak_job_memory)

    def terminate(self):
        if not self.api.TerminateJobObject(self.handle, 1):
            raise ctypes.WinError(ctypes.get_last_error())

    def close(self):
        if self.handle:
            self.api.CloseHandle(self.handle)
            self.handle = None


def resume_suspended(process):
    api = ctypes.WinDLL("kernel32", use_last_error=True)
    api.OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    api.OpenThread.restype = wintypes.HANDLE
    api.ResumeThread.argtypes = [wintypes.HANDLE]
    api.ResumeThread.restype = wintypes.DWORD
    api.CloseHandle.argtypes = [wintypes.HANDLE]
    threads = psutil.Process(process.pid).threads()
    if len(threads) != 1:
        raise RuntimeError("New suspended validator has an unexpected thread inventory")
    handle = api.OpenThread(0x0002, False, threads[0].id)
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        if api.ResumeThread(handle) == 0xFFFFFFFF:
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        api.CloseHandle(handle)


def completed_generation_admission(receipt, raw, recovery_receipt_sha256=None):
    """Admit immutable completed output, never retry a successful generator.

    Explicit recovery covers immediate or bounded natural-drain checks failing
    after generation succeeded, with descendants then drained in the exception
    path. The historical FAIL is preserved and identified. A bounded timeout
    must also retain its exact failed-drain observations; cleanup uncertainty
    cannot be admitted.
    The caller must additionally verify process absence, output and log bytes.
    """
    drain = receipt.get("natural_exit_drain", {})
    drain_failure = receipt.get("failure") == "Completed steps left captured descendants live"
    if receipt.get("failure") == "Completed steps exceeded bounded natural-exit drain":
        drain_failure = (
            isinstance(drain, dict)
            and drain.get("status") == "FAIL_TIMEOUT"
            and type(drain.get("timeout_seconds")) in (int, float)
            and 0 < drain["timeout_seconds"] <= 5.0
            and type(drain.get("elapsed_seconds")) in (int, float)
            and drain["elapsed_seconds"] >= drain["timeout_seconds"]
            and bool(drain.get("owned_pids_not_drained"))
            and bool(drain.get("captured_process_identities"))
        )
    recovered = (
        recovery_receipt_sha256 is not None
        and hashlib.sha256(raw).hexdigest() == recovery_receipt_sha256
        and receipt.get("schema") == "openlogic-bounded-review-integration-v1"
        and receipt.get("status") == "FAIL"
        and drain_failure
        and receipt.get("owned_pids_not_drained") == []
        and receipt.get("cleanup_failure") is None
        and bool(receipt.get("steps"))
        and all(step.get("status") == "PASS" and step.get("exit_code") == 0
                for step in receipt["steps"])
    )
    if recovery_receipt_sha256 is not None and not recovered:
        raise ValueError("Explicit completed-generation recovery does not match the exact drained failure")
    if receipt.get("status") != "PASS_GENERATED_PENDING_INDEPENDENT_READBACK" and not recovered:
        raise ValueError("Generation is not successful or an explicitly authenticated drained recovery")
    return recovered


def verify_terminal_generation(generation=GENERATION, snapshot=SNAPSHOT,
                               expected_json=EXPECTED_JSON, output=OUTPUT,
                               recovery_receipt_sha256=None):
    raw = generation.read_bytes()
    receipt = json.loads(raw)
    recovered = completed_generation_admission(receipt, raw, recovery_receipt_sha256)
    if (receipt.get("snapshot") != snapshot.relative_to(REPO).as_posix() or
            receipt.get("snapshot_json_sha256") != expected_json or
            receipt.get("owned_pids_not_drained", []) != []):
        raise ValueError("The exact selected generation stage is not terminal and successful")
    identities = [(receipt["pid"], receipt["process_create_time"])]
    generation_steps = [step for step in receipt["steps"] if step["name"] == "reviewer-generation"]
    if len(generation_steps) != 1:
        raise ValueError("Unexpected completed generation step inventory")
    step = generation_steps[0]
    if step.get("status") != "PASS" or step.get("exit_code") != 0:
        raise ValueError("Generation step failed")
    identities.append((step["pid"], step["process_create_time"]))
    for pid, created in identities:
        try:
            process = psutil.Process(pid)
            if abs(process.create_time() - created) < 0.01:
                raise ValueError("The captured generation process remains live")
        except psutil.NoSuchProcess:
            pass
    log = generation.parent / "reviewer-generation.log"
    if digest(log) != step["log_sha256"] or digest(snapshot / "EXPERT_REVIEW_INDEX.json") != expected_json:
        raise ValueError("Terminal generation bytes differ from their receipt")
    if output.exists():
        raise FileExistsError("READBACK_VALIDATION.json already exists; never overwrite a completed receipt")
    return {"path": generation.relative_to(REPO).as_posix(), "sha256": hashlib.sha256(raw).hexdigest(),
            "snapshot_json_sha256": expected_json, "generation_log_sha256": digest(log),
            "original_status": receipt["status"],
            "completed_generation_drain_recovery": recovered}


def execute(out, receipt, outer, arguments, *, name, deadline, expected_timeout=False):
    """One launch, bounded observation, and deterministic owned-inner-job drain."""
    def save():
        temporary = out / "RUN_RECEIPT.json.tmp"
        temporary.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(out / "RUN_RECEIPT.json")

    entry = {"name": name, "status": "RUNNING", "arguments": arguments, "deadline_seconds": deadline,
             "observed_processes": {}, "peak_tree_rss_bytes": 0}
    receipt["steps"].append(entry)
    save()
    inner, process, forced = None, None, None
    log_path = out / (name + ".log")
    started = time.monotonic()
    try:
        inner = Job(kill_on_close=True)
        with log_path.open("xb") as log:
            process = subprocess.Popen([sys.executable, "-X", "utf8", "-B", *arguments],
                cwd=REPO, stdout=log, stderr=subprocess.STDOUT,
                creationflags=0x08000000 | 0x00000004)  # hidden and suspended
            # The suspended child already inherits the aggregate outer job. The
            # inner job is assigned before any validator instructions execute.
            inner.assign(process._handle)
            entry.update(pid=process.pid, process_create_time=psutil.Process(process.pid).create_time(),
                         kernel_job_memory_limit_bytes=CAP, assigned_before_resume=True)
            save()
            resume_suspended(process)
            print(json.dumps({"event": "guarded-child-started", "runner_pid": os.getpid(),
                              "child_pid": process.pid, "step": name, "receipt": str(out / "RUN_RECEIPT.json")}), flush=True)
            last_saved = started
            while True:
                rss = 0
                for pid in outer.pids():
                    try:
                        member = psutil.Process(pid)
                        rss += member.memory_info().rss
                        entry["observed_processes"].setdefault(str(pid), member.create_time())
                    except psutil.NoSuchProcess:
                        pass
                entry["peak_tree_rss_bytes"] = max(entry["peak_tree_rss_bytes"], rss)
                receipt["peak_tree_rss_bytes"] = max(receipt["peak_tree_rss_bytes"], rss)
                receipt["peak_kernel_job_committed_bytes"] = outer.peak()
                if rss >= CAP:
                    forced = "memory-cap"
                    break
                if process.poll() is not None and not inner.pids():
                    break
                if time.monotonic() - started >= deadline:
                    forced = "deadline"
                    break
                if time.monotonic() - last_saved >= 2:
                    save()
                    last_saved = time.monotonic()
                time.sleep(0.1)
    except BaseException as exc:
        forced = "guard-or-child-failure: " + repr(exc)
    finally:
        if inner is not None:
            if forced or inner.pids():
                inner.terminate()
            drain_deadline = time.monotonic() + 10
            while inner.pids() and time.monotonic() < drain_deadline:
                time.sleep(0.1)
            entry["owned_pids_not_drained"] = inner.pids()
            inner.close()
        if process is not None:
            # Assignment failure can only leave our newly created suspended
            # process. Kill via its captured handle, never a sampled foreign PID.
            if process.poll() is None:
                process.kill()
            try:
                entry["exit_code"] = process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                entry["captured_process_drain_failed"] = True
        entry["elapsed_seconds"] = round(time.monotonic() - started, 3)
        entry["forced_stop"] = forced
        entry["log_sha256"] = digest(log_path) if log_path.exists() else None
        receipt["peak_kernel_job_committed_bytes"] = outer.peak()
        okay = (not entry.get("owned_pids_not_drained") and not entry.get("captured_process_drain_failed") and
                ((forced == "deadline") if expected_timeout else (forced is None and entry.get("exit_code") == 0)))
        entry["status"] = "PASS_EXPECTED_TIMEOUT_DRAIN" if okay and expected_timeout else "PASS" if okay else "FAIL"
        save()
    if not okay:
        raise RuntimeError("Bounded readback step failed: " + name)
    return entry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--self-test", action="store_true", help="Small success/timeout owned-tree probes; no snapshot validation")
    parser.add_argument("--snapshot", type=Path, default=SNAPSHOT)
    parser.add_argument("--previous", type=Path, default=PREVIOUS)
    parser.add_argument("--generation", type=Path, default=GENERATION)
    parser.add_argument("--expected-json", default=EXPECTED_JSON)
    parser.add_argument("--expected-assessments", type=int, default=58)
    parser.add_argument("--expected-repairs", type=int, default=12)
    parser.add_argument("--generation-recovery-sha256",
                        help="Explicit immutable receipt hash for completed output drained after a wrapper cleanup failure")
    args = parser.parse_args()
    snapshot, previous, generation = args.snapshot.resolve(), args.previous.resolve(), args.generation.resolve()
    for path in (snapshot, previous, generation):
        if not path.is_relative_to(REPO):
            raise ValueError("Snapshot, predecessor and generation receipt must remain inside this repository")
    expected_json = args.expected_json.lower()
    if len(expected_json) != 64 or any(c not in "0123456789abcdef" for c in expected_json):
        raise ValueError("Expected snapshot SHA-256 must be an explicit 64-character hex digest")
    if args.expected_assessments < 0 or args.expected_repairs < 1:
        raise ValueError("Invalid exact expected assessment or repair inventory")
    output = snapshot / "READBACK_VALIDATION.json"
    if not args.run_id or any(char not in "abcdefghijklmnopqrstuvwxyz0123456789-" for char in args.run_id):
        raise ValueError("run-id must be lowercase letters, digits and hyphens")
    out = REPO / "tmp/redo-20260906-reviewer" / args.run_id
    if out.exists():
        raise FileExistsError("Run directory already exists; do not overwrite/retry completed stages")
    terminal = None if args.self_test else verify_terminal_generation(
        generation, snapshot, expected_json, output, args.generation_recovery_sha256)
    out.mkdir()
    receipt = {"schema": "openlogic-bounded-expert-readback-v1", "status": "RUNNING", "pid": os.getpid(),
               "process_create_time": psutil.Process().create_time(), "cap_bytes": CAP, "steps": [],
               "peak_tree_rss_bytes": 0, "worker_sha256": digest(Path(__file__)),
               "validator_sha256": digest(REPO / "build/validate_expert_review_snapshot.py"),
               "snapshot": snapshot.relative_to(REPO).as_posix(), "previous": previous.relative_to(REPO).as_posix(),
               "expected_assessments": args.expected_assessments, "expected_repairs": args.expected_repairs,
               "self_test": args.self_test, "terminal_generation": terminal}
    outer = None
    try:
        outer = Job()
        outer.assign()
        receipt["aggregate_kernel_job_assigned_before_child_launch"] = True
        if args.self_test:
            probe = ("import subprocess,sys,time; allocation=bytearray(16*1024*1024); "
                     "p=subprocess.Popen([sys.executable,'-c','import time; a=bytearray(16*1024*1024); time.sleep(0.4)']); "
                     "p.wait(); print('owned-child-and-grandchild-probe-completed')")
            execute(out, receipt, outer, ["-c", probe], name="small-owned-tree", deadline=10)
            timeout = ("import subprocess,sys,time; p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)']); "
                       "print('owned-grandchild-started',flush=True); time.sleep(30)")
            execute(out, receipt, outer, ["-c", timeout], name="bounded-owned-tree-timeout", deadline=0.8, expected_timeout=True)
            receipt["status"] = "PASS_GUARD_SELF_TEST"
        else:
            arguments = ["build/validate_expert_review_snapshot.py", "--repo", str(REPO),
                         "--snapshot", str(snapshot), "--previous", str(previous), "--output", str(output)]
            execute(out, receipt, outer, arguments, name="independent-readback", deadline=300)
            validation = json.loads(output.read_text(encoding="utf-8"))
            if (validation.get("status") != "PASS" or validation.get("errors") or
                    validation.get("snapshot_json_sha256") != expected_json or
                    validation.get("counts", {}).get("applied_assessments") != args.expected_assessments or
                    validation.get("counts", {}).get("canonical_repair_assessments_expected") != args.expected_repairs or
                    validation.get("counts", {}).get("independently_verified_repair_assessments") != args.expected_repairs):
                raise ValueError("Independent readback did not verify the exact commissioned assessment and repair inventory")
            if digest(snapshot / "EXPERT_REVIEW_INDEX.json") != expected_json:
                raise ValueError("Generated snapshot changed during readback")
            receipt.update(status="PASS_INDEPENDENT_READBACK", validation_sha256=digest(output),
                           counts=validation["counts"], validation_errors=validation["errors"])
    except BaseException as exc:
        receipt.update(status="FAIL", failure=repr(exc))
        if output.exists() and not args.self_test:
            receipt["validation_sha256"] = digest(output)
            try:
                validation = json.loads(output.read_text(encoding="utf-8"))
                receipt.update(counts=validation.get("counts"), validation_errors=validation.get("errors"))
            except (ValueError, OSError):
                pass
    finally:
        if outer:
            receipt["peak_kernel_job_committed_bytes"] = outer.peak()
            receipt["owned_pids_not_drained"] = [pid for pid in outer.pids() if pid != os.getpid()]
            if receipt["owned_pids_not_drained"]:
                receipt.update(status="FAIL", failure="Owned process inventory not drained")
            outer.close()  # outer job does not kill its receipt-writing member
        temporary = out / "RUN_RECEIPT.json.tmp"
        temporary.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(out / "RUN_RECEIPT.json")
    print(json.dumps(receipt, ensure_ascii=False), flush=True)
    return 0 if receipt["status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
