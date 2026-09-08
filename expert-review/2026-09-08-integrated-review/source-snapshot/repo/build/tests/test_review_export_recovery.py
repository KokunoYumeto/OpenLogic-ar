"""Non-process tests for one authenticated post-generation drain recovery."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "run_expert_review_readback_20260906.py"
TREE = ast.parse(SCRIPT.read_text(encoding="utf-8"))
FUNCTION = next(node for node in TREE.body if isinstance(node, ast.FunctionDef)
                and node.name == "completed_generation_admission")
NAMESPACE = {"hashlib": hashlib}
exec(compile(ast.Module(body=[FUNCTION], type_ignores=[]), str(SCRIPT), "exec"), NAMESPACE)
admit = NAMESPACE["completed_generation_admission"]


class ExportRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.receipt = {
            "schema": "openlogic-bounded-review-integration-v1", "status": "FAIL",
            "failure": "Completed steps left captured descendants live",
            "owned_pids_not_drained": [],
            "steps": [{"name": "reviewer-generation", "status": "PASS", "exit_code": 0}],
        }

    def admitted(self, receipt=None):
        value = self.receipt if receipt is None else receipt
        raw = json.dumps(value, sort_keys=True).encode()
        return admit(value, raw, hashlib.sha256(raw).hexdigest())

    def test_only_explicit_exact_recovery_is_admitted(self):
        self.assertTrue(self.admitted())
        with self.assertRaises(ValueError):
            admit(self.receipt, b"original bytes")
        with self.assertRaises(ValueError):
            admit(self.receipt, b"changed bytes", "0" * 64)

    def test_failed_step_wrong_failure_or_live_descendant_are_rejected(self):
        for key, value in (("failure", "memory cap"), ("owned_pids_not_drained", [12]),
                           ("owned_pids_not_drained", None), ("steps", []),
                           ("steps", [{"status": "FAIL", "exit_code": 2}]),
                           ("schema", "unrecognised")):
            with self.subTest(key=key, value=value):
                changed = copy.deepcopy(self.receipt)
                changed[key] = value
                with self.assertRaises(ValueError):
                    self.admitted(changed)

    def test_normal_success_does_not_claim_recovery(self):
        self.assertFalse(admit({"status": "PASS_GENERATED_PENDING_INDEPENDENT_READBACK"}, b"normal"))


if __name__ == "__main__":
    unittest.main()
