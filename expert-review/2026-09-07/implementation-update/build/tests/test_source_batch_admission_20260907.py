"""Finite non-TeX tests for exact consolidated source-batch admission.

No source-closure generation, materialization, export, network, or subprocess.
The checks cover admission contracts, not the final reader's visual semantics.
"""
import copy
import importlib.util
from pathlib import Path
import sys
import unittest
from unittest import mock

REPO = Path(__file__).resolve().parents[2]


def load(name, value):
    spec = importlib.util.spec_from_file_location(name, REPO / "build" / value)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


FINAL = load("source_batch_admission_finalizer", "finalize_classical_source_reconciliation.py")
AUDIT = load("source_batch_admission_acceptance", "generate_full_translation_acceptance_audit.py")
CHECKER = FINAL.load_checker(REPO)
BASELINE, _ = CHECKER.load_baseline(REPO / "evidence/classical/BASELINE.json")
METADATA_PATH = REPO / "evidence/classical/SOURCE_RECONCILIATION_METADATA_20260905.json"


class SourceBatchAdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = FINAL.validate_source_repair_batch_20260907(REPO, CHECKER, BASELINE)

    def test_exact_scope_and_deterministic_replay(self):
        result = self.result
        self.assertEqual(result["status"], "PASS")
        self.assertEqual((result["decision_count"], result["transaction_count"],
                          result["patch_count"], result["changed_file_count"]), (16, 16, 26, 15))
        self.assertEqual(len(result["ledger_identities"]), 3)
        self.assertEqual(result, FINAL.validate_source_repair_batch_20260907(REPO, CHECKER, BASELINE))

    def test_function_successor_recovers_exact_historical_phase(self):
        rows = [r for r in self.result["historical_transitions_in_inverse_order"]
                if r["unit_id"] == "OLP-0022"]
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["after_sha256"],
                         "3a74dd4fc979afc520df1954cc09c78327ac63c6954852f77e0a8cb9b9a38922")
        self.assertEqual(rows[0]["before_sha256"], rows[1]["after_sha256"])
        self.assertEqual(rows[1]["after_sha256"],
                         "8a73d76a7d09e54a6956468280c054ded5243f4f4a43ed05aee76de126dd9ca9")
        self.assertEqual(rows[1]["before_sha256"],
                         "56dbda2e3f9203b25e9503c465653e35254a4f7dce843068ca6ee909ed28944c")

    def test_ledger_byte_change_fails_closed_even_when_json_semantics_match(self):
        original = FINAL.load_unique_json

        def altered(path, label):
            data, raw = original(path, label)
            return data, raw + b"\n"

        with mock.patch.object(FINAL, "load_unique_json", side_effect=altered):
            with self.assertRaisesRegex(FINAL.ReconciliationError, "ledger identity drifted"):
                FINAL.validate_source_repair_batch_20260907(REPO, CHECKER, BASELINE)

    def test_current_source_drift_cannot_be_accepted_by_replaying_old_after_hash(self):
        relative = "source/locale/ar-classical/content/sets-functions-relations/functions/function-kinds.tex"
        chosen = (REPO / relative).resolve()
        original = Path.read_bytes

        def changed(path):
            raw = original(path)
            return raw + b"\n" if path.resolve() == chosen else raw

        with mock.patch.object(Path, "read_bytes", changed):
            with self.assertRaisesRegex(FINAL.ReconciliationError, "after identity drifted"):
                FINAL.validate_source_repair_batch_20260907(REPO, CHECKER, BASELINE)

    def test_corrupt_inverse_is_not_a_hash_alias(self):
        original = FINAL.load_unique_json

        def changed(path, label):
            data, raw = original(path, label)
            if path.stem == FINAL.SOURCE_REPAIR_BATCH_20260907[-1][0]:
                data = copy.deepcopy(data)
                data["transactions"][0]["patches"][0]["before"] += "!"
            return data, raw

        with mock.patch.object(FINAL, "load_unique_json", side_effect=changed):
            with self.assertRaisesRegex(FINAL.ReconciliationError, "before identity drifted"):
                FINAL.validate_source_repair_batch_20260907(REPO, CHECKER, BASELINE)

    def test_english_and_shared_macro_inputs_are_preserved(self):
        transitions = self.result["historical_transitions_in_inverse_order"]
        self.assertEqual({t["edition"] for t in transitions}, {"msa", "classical"})
        shared = next(x for x in self.result["live_input_identities"]
                      if x["path"] == "source/locale/ar/open-logic-config.sty")
        self.assertEqual(shared["sha256"],
                         "018ce747a3957ce35eb05820e919d46fe4af0f3452ecdbe4d1ddc7e95bf33280")
        self.assertFalse(any("/upstream/" in t["path"] for t in transitions))

    def test_only_two_proved_formula_changes_and_five_shared_msa_units(self):
        changes = self.result["formula_changes"]
        self.assertEqual([x["unit_id"] for x in changes], ["OLP-0394", "OLP-0399"])
        self.assertTrue(all(x["editions"] == ["msa", "classical"] for x in changes))
        self.assertEqual({t["unit_id"] for t in self.result["historical_transitions_in_inverse_order"]
                          if t["edition"] == "msa"},
                         {"OLP-0394", "OLP-0399", "OLP-0400", "OLP-0404", "OLP-0409"})

    def test_metadata_retains_prior_repairs_and_binds_precise_new_authorities(self):
        metadata, _ = FINAL.load_metadata(REPO, METADATA_PATH)
        corrections, _, _, _ = FINAL.metadata_maps(REPO, metadata)
        expected = {"OLP-0394": ["C391-0410-F01"], "OLP-0399": ["C391-0410-F02"],
                    "OLP-0400": ["C391-0410-F03"], "OLP-0404": ["C391-0410-F04"],
                    "OLP-0409": ["C391-0410-F05", "C391-0410-F06"]}
        for uid, findings in expected.items():
            row = corrections[uid]
            self.assertTrue(set(findings) <= set(row["finding_ids"]))
            self.assertEqual(row["metadata_source"], "explicit")
            self.assertTrue(any("MODAL_SCOPE_20260907.json#/decisions/" in ref
                                for ref in row["authority_refs"]))
            self.assertGreater(len(row["rationale"]), 150)
        for uid, finding in (("OLP-0021", "OLFUN-002"), ("OLP-0021", "OLFUN-003"),
                             ("OLP-0024", "OLFUN-001"), ("OLP-0029", "OLSIZ-001"),
                             ("OLP-0394", "MVL-L0-I1"), ("OLP-0400", "MVL-L0-I1"),
                             ("OLP-0404", "C404-01")):
            self.assertIn(finding, corrections[uid]["finding_ids"])

    def test_all_three_ledgers_and_human_guides_are_in_acceptance_inventory(self):
        ranges = {spec[0]: set(spec[4]) for spec in AUDIT.RANGE_SPECS}
        for name, *_ in FINAL.SOURCE_REPAIR_BATCH_20260907:
            for suffix in (".json", ".md"):
                value = "evidence/classical/repairs/" + name + suffix
                self.assertIn(value, FINAL.ACCEPTANCE_RANGE_ARTIFACTS)
                for range_name in (["0301-0400", "0401-0500"] if "MODAL" in name else ["0001-0100"]):
                    self.assertIn(value, ranges[range_name])
                self.assertTrue((REPO / value).is_file())


if __name__ == "__main__":
    unittest.main()
