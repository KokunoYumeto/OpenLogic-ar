"""Bounded owned-process drain and exact source-resume tests; no derivation."""

from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest import mock

from build import run_arabic_review_integration_20260906 as worker


CHECKPOINT = worker.REPO / "tmp/redo-20260906-reviewer/cardinality-source-93412578/RUN_RECEIPT.json"
CHECKPOINT_SHA256 = "63ef60cbbfe0b1ffae718b9a6d0ef1cd6d430fa2c13deadbabe6d5e103bf2aed"
CLOSURE_SHA256 = "274bdb05f2bbe34ad447cebccb998dc5c3637b714384b45009c69257c4f288e2"


class FakeProcess:
    def __init__(self, pid, created, rss=100):
        self.pid, self.created, self.rss = pid, created, rss
        self.alive, self.kills = True, 0
        self.descendants = []

    def create_time(self):
        return self.created

    def is_running(self):
        return self.alive

    def memory_info(self):
        return SimpleNamespace(rss=self.rss)

    def children(self, recursive=False):
        if not recursive:
            raise AssertionError("Only recursive owned-tree capture is supported")
        return self.descendants[:]

    def kill(self):
        self.kills += 1
        self.alive = False


class FakeClock:
    def __init__(self, callback=lambda _now: None):
        self.now = 0.0
        self.callback = callback

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds
        self.callback(self.now)


class OwnedDrainTests(unittest.TestCase):
    def setUp(self):
        self.parent = FakeProcess(1, 1.0)
        self.child = FakeProcess(2, 2.0)
        self.parent.descendants = [self.child]
        self.processes = {2: self.child}

    def lookup(self, pid):
        if pid not in self.processes:
            raise worker.psutil.NoSuchProcess(pid)
        return self.processes[pid]

    def drain(self, captured, clock, **kwargs):
        with mock.patch.object(worker.psutil, "Process", side_effect=self.lookup):
            with mock.patch.object(worker.time, "monotonic", clock.monotonic):
                with mock.patch.object(worker.time, "sleep", clock.sleep):
                    return worker.drain_captured(self.parent, captured, **kwargs)

    def test_short_lived_descendant_drains_naturally_without_kill(self):
        clock = FakeClock(lambda now: setattr(self.child, "alive", now < 0.2))
        result = self.drain(set(), clock)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["owned_pids_not_drained"], [])
        self.assertAlmostEqual(result["elapsed_seconds"], 0.2)
        self.assertEqual(result["captured_process_identities"],
                         [{"pid": 2, "process_create_time": 2.0}])
        self.assertEqual(self.child.kills, 0)

    def test_stuck_descendant_times_out_without_kill_or_unbounded_wait(self):
        clock = FakeClock()
        result = self.drain(set(), clock, timeout=0.3)
        self.assertEqual(result["status"], "FAIL_TIMEOUT")
        self.assertEqual(result["owned_pids_not_drained"], [2])
        self.assertLessEqual(clock.now, 0.300001)
        self.assertEqual(self.child.kills, 0)

    def test_previously_captured_orphan_remains_tracked(self):
        self.parent.descendants = []
        clock = FakeClock(lambda now: setattr(self.child, "alive", now < 0.2))
        result = self.drain({(2, 2.0)}, clock)
        self.assertEqual(result["status"], "PASS")
        self.assertAlmostEqual(clock.now, 0.2)

    def test_reused_foreign_pid_is_not_waited_for_or_killed(self):
        self.parent.descendants = []
        self.child.created = 20.0
        result = self.drain({(2, 2.0)}, FakeClock())
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["elapsed_seconds"], 0)
        with mock.patch.object(worker.psutil, "Process", side_effect=self.lookup):
            with mock.patch.object(worker.psutil, "wait_procs", return_value=([], [])) as wait:
                self.assertEqual(worker.terminate_captured({(2, 2.0)}), [])
        self.assertEqual(wait.call_args.args[0], [])
        self.assertEqual(self.child.kills, 0)

    def test_new_descendant_during_drain_is_captured(self):
        second = FakeProcess(3, 3.0)
        self.processes[3] = second

        def advance(now):
            if now >= 0.1:
                self.parent.descendants = [second]
                self.child.alive = False
            second.alive = now < 0.3

        result = self.drain(set(), FakeClock(advance))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual([p["pid"] for p in result["captured_process_identities"]], [2, 3])
        self.assertGreaterEqual(result["elapsed_seconds"], 0.3)
        self.assertEqual(second.kills, 0)

    def test_memory_cap_stays_active_during_drain(self):
        self.child.rss = worker.CAP
        with self.assertRaisesRegex(RuntimeError, "1 GiB cap during drain"):
            self.drain(set(), FakeClock())
        self.assertEqual(self.child.kills, 0)

    def test_access_denied_fails_closed(self):
        with mock.patch.object(worker.psutil, "Process", side_effect=worker.psutil.AccessDenied(2)):
            with self.assertRaises(worker.psutil.AccessDenied):
                worker.drain_captured(self.parent, {(2, 2.0)})

    def test_missing_process_is_drained(self):
        self.parent.descendants = []
        self.processes = {}
        self.assertEqual(self.drain({(2, 2.0)}, FakeClock())["status"], "PASS")

    def test_failure_cleanup_only_signals_matching_captured_identities(self):
        foreign = FakeProcess(3, 30.0)
        self.processes[3] = foreign
        with mock.patch.object(worker.psutil, "Process", side_effect=self.lookup):
            with mock.patch.object(worker.psutil, "wait_procs", return_value=([], [])) as wait:
                self.assertEqual(worker.terminate_captured({(2, 2.0), (3, 3.0)}), [])
        self.assertEqual(self.child.kills, 1)
        self.assertEqual(foreign.kills, 0)
        self.assertEqual([p.pid for p in wait.call_args.args[0]], [2])
        self.assertEqual(wait.call_args.kwargs["timeout"], 15)

    def test_invalid_or_unbounded_intervals_are_rejected(self):
        for options in ({"timeout": 0}, {"timeout": 6}, {"poll_interval": 0},
                        {"timeout": 0.1, "poll_interval": 1}):
            with self.subTest(options=options):
                with self.assertRaisesRegex(ValueError, "bounded natural-drain interval"):
                    worker.drain_captured(self.parent, set(), **options)

    def test_actual_short_lived_python_child_drains_without_signal(self):
        # One small owned process only; no source derivation or exporter.
        with subprocess.Popen(
            [sys.executable, "-B", "-c", "import time; time.sleep(0.2)"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        ) as process:
            captured = {(process.pid, worker.psutil.Process(process.pid).create_time())}
            try:
                result = worker.drain_captured(worker.psutil.Process(), captured)
                self.assertEqual(result["status"], "PASS")
                self.assertEqual(result["owned_pids_not_drained"], [])
                self.assertEqual(process.wait(timeout=1), 0)
            finally:
                if process.poll() is None:
                    worker.terminate_captured(captured)


class ExactSourceResumeTests(unittest.TestCase):
    def test_actual_failed_but_drained_checkpoint_is_admitted_without_derivation(self):
        self.assertEqual(worker.digest(CHECKPOINT), CHECKPOINT_SHA256)
        with mock.patch.object(worker.subprocess, "Popen", side_effect=AssertionError("No derivation")):
            with mock.patch.object(worker.subprocess, "run", side_effect=AssertionError("No derivation")):
                result = worker.verified_source_resume(CHECKPOINT)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["receipt_sha256"], CHECKPOINT_SHA256)
        self.assertEqual(result["closure_sha256"], CLOSURE_SHA256)
        self.assertEqual(result["source_files_rehashed"], 2166)
        self.assertEqual(result["authority_identities_rechecked"], 91)
        self.assertEqual(worker.digest(CHECKPOINT), CHECKPOINT_SHA256)

    def test_live_original_worker_identity_blocks_resume(self):
        old = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
        live = FakeProcess(old["pid"], old["process_create_time"])
        with mock.patch.object(worker.psutil, "pid_exists", return_value=True):
            with mock.patch.object(worker.psutil, "Process", return_value=live):
                with self.assertRaisesRegex(ValueError, "captured worker remains live"):
                    worker.verified_source_resume(CHECKPOINT)

    def test_uncertain_cleanup_and_non_drained_checkpoint_are_rejected(self):
        real_read = Path.read_text
        old = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
        mutations = ({"cleanup_failure": "Access denied"},
                     {"owned_pids_not_drained": [2]}, {"status": "RUNNING"})
        for mutation in mutations:
            changed = copy.deepcopy(old)
            changed.update(mutation)

            def read(path, *args, **kwargs):
                return json.dumps(changed) if path == CHECKPOINT else real_read(path, *args, **kwargs)

            with self.subTest(mutation=mutation):
                with mock.patch.object(Path, "read_text", read):
                    with self.assertRaisesRegex(ValueError, "not terminal and drained"):
                        worker.verified_source_resume(CHECKPOINT)

    def test_conflicting_closure_identity_and_source_drift_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "closure identity conflicts"):
            worker.verified_source_resume(CHECKPOINT, "0" * 64)
        real_digest = worker.digest

        def drift(path):
            return "0" * 64 if "source/locale/ar-classical/content/" in path.as_posix() else real_digest(path)

        with mock.patch.object(worker, "digest", side_effect=drift):
            with self.assertRaisesRegex(ValueError, "Completed Arabic source changed"):
                worker.verified_source_resume(CHECKPOINT)


if __name__ == "__main__":
    unittest.main()
