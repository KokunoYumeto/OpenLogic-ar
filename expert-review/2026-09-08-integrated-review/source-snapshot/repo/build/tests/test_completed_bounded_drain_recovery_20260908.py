"""Exact completed-generation recovery, never dispatching a full exporter."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from build import run_expert_review_readback_20260906 as R


class BoundedDrainRecovery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generation = R.REPO / 'tmp/redo-20260906-reviewer/cardinality-review-93846854/RUN_RECEIPT.json'
        cls.raw = cls.generation.read_bytes()
        cls.receipt = json.loads(cls.raw)
        cls.digest = hashlib.sha256(cls.raw).hexdigest()
        if cls.digest != 'a9f64552d0b02e177c1f8f859e4535575f742dbf0f4cae4e2c6dea40c4f1e474':
            raise AssertionError('Historical failed wrapper bytes changed')

    def test_exact_drained_current_output_can_be_read_back_without_regeneration(self):
        snapshot = R.REPO / self.receipt['snapshot']
        with patch.object(R.subprocess, 'Popen', side_effect=AssertionError('No dispatch')):
            facts = R.verify_terminal_generation(self.generation, snapshot,
                self.receipt['snapshot_json_sha256'], snapshot/'NEVER_WRITTEN_BY_THIS_TEST.json', self.digest)
        self.assertTrue(facts['completed_generation_drain_recovery'])
        self.assertEqual(facts['original_status'], 'FAIL')

    def test_explicit_hash_is_required_and_must_match(self):
        for supplied in (None, '0'*64):
            with self.subTest(hash=supplied), self.assertRaises(ValueError):
                R.completed_generation_admission(self.receipt, self.raw, supplied)

    def test_failed_work_undrained_or_uncertain_cleanup_is_rejected_even_with_new_hash(self):
        mutations = (
            lambda r:r['steps'][0].update(status='FAIL', exit_code=1),
            lambda r:r.update(owned_pids_not_drained=[42444]),
            lambda r:r.update(cleanup_failure='unknown liveness'),
            lambda r:r.update(failure='Unrelated deterministic failure'),
            lambda r:r['natural_exit_drain'].update(status='PASS'),
            lambda r:r['natural_exit_drain'].update(timeout_seconds=100),
            lambda r:r['natural_exit_drain'].update(elapsed_seconds=0),
            lambda r:r['natural_exit_drain'].update(captured_process_identities=[]),
        )
        for i, mutate in enumerate(mutations):
            with self.subTest(mutation=i), self.assertRaises(ValueError):
                value=copy.deepcopy(self.receipt)
                mutate(value)
                raw=json.dumps(value).encode()
                R.completed_generation_admission(value, raw, hashlib.sha256(raw).hexdigest())


if __name__ == '__main__':
    unittest.main()
