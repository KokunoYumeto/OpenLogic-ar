"""Finite normalizer checks and in-memory adversaries; no writes or exports."""
import copy
from dataclasses import replace
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from build import cardinality_repair_batch_20260908 as batch


class CardinalityBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = batch.normalize()
        cls.bytes = {Path(row.path): Path(row.path).read_bytes() for row in cls.result.input_identities}

    def mutate_ledger(self, index, change, *, repin_for_structural_test=False):
        contract = batch.CONTRACTS[index]
        path = batch.REPO / batch.REPAIRS / (contract.stem + ".json")
        data = batch.parse(self.bytes[path])
        change(data)
        raw = json.dumps(data, ensure_ascii=False, indent=2).encode()
        reader = lambda target: raw if target == path else self.bytes[target]
        contracts = list(batch.CONTRACTS)
        if repin_for_structural_test:
            # Tests only: get beyond the public immutable-byte pin to prove the
            # lower-level ownership/boundary checks reject the adverse content.
            contracts[index] = replace(contract, sha256=batch.sha(raw), bytes=len(raw))
        with patch.object(batch, "CONTRACTS", tuple(contracts)):
            return batch.normalize(read=reader)

    def test_exact_scope_and_repeatability(self):
        result = self.result
        self.assertEqual((len(result.ledgers), len(result.decisions), len(result.sources)), (4, 23, 10))
        self.assertEqual(sum(len(s.patches) for s in result.sources), 25)
        self.assertEqual(len(result.supersessions), 7)
        self.assertEqual(len(result.input_identities), 23)
        self.assertEqual(result, batch.normalize(read=self.bytes.__getitem__))

    def test_complete_original_ledgers_reasons_statuses_and_authorities_preserved(self):
        for ledger in self.result.ledgers:
            raw = self.bytes[batch.REPO / ledger.identity.path]
            self.assertEqual(raw, ledger.raw_bytes)
            data = batch.parse(raw)
            self.assertEqual(ledger.status, data["status"])
            for normalized, original in zip(ledger.decisions, data["decisions"]):
                self.assertEqual(json.loads(normalized.raw_json), original)
                self.assertEqual(normalized.rationale, original["rationale"])
                self.assertEqual(normalized.status, original["status"])
                self.assertEqual(normalized.recording_mode, original.get("recording_mode", data.get("recording_mode", "")))

    def test_exact_source_inverse_forward_and_25_locations(self):
        count = 0
        for source in self.result.sources:
            self.assertEqual(batch.sha(source.before_bytes), source.before.sha256)
            self.assertEqual(batch.sha(source.after_bytes), source.after.sha256)
            replay = source.before_bytes
            for change in source.patches:
                replay = replay.replace(change.before.literal.encode(), change.after.literal.encode(), 1)
                for raw, location in ((source.before_bytes, change.before), (source.after_bytes, change.after)):
                    self.assertEqual(raw[location.byte_start:location.byte_end], location.literal.encode())
                    self.assertEqual(raw[:location.byte_start].count(b"\n") + 1, location.line_start)
                    self.assertEqual(raw[:location.byte_end - 1].count(b"\n") + 1, location.line_end)
                    self.assertEqual("\n".join(raw.decode().splitlines()[location.line_start - 1:location.line_end]), location.excerpt)
                count += 1
            self.assertEqual(replay, source.after_bytes)
            for change in reversed(source.patches):
                replay = replay.replace(change.after.literal.encode(), change.before.literal.encode(), 1)
            self.assertEqual(replay, source.before_bytes)
        self.assertEqual(count, 25)

    def test_application_order_and_physical_order_are_distinct_and_preserved(self):
        reduction = next(s for s in self.result.sources if s.unit_id == "OLP-0034" and s.edition == "classical")
        self.assertEqual(tuple(p.patch_id for p in reduction.patches), batch.CONTRACTS[2].transaction_patches[1])
        self.assertEqual(reduction.source_order_patch_ids,
            ("RED-0034-INSTRUMENTAL-ANTECEDENT", "RED-0034-DIRECT-CONDITIONAL", "RED-0034-CODOMAIN-CLASSICAL"))
        equi = next(s for s in self.result.sources if s.unit_id == "OLP-0035" and s.edition == "classical")
        self.assertEqual(equi.source_order_patch_ids[0], "OLP0035-classical-P6")

    def test_seven_exact_supersessions_do_not_rewrite_original_motives(self):
        self.assertEqual(tuple(s.decision_id for s in self.result.supersessions), batch.PAIRING_IDS)
        for row in self.result.supersessions:
            before, after = json.loads(row.previous_decision_json), json.loads(row.current_decision_json)
            self.assertEqual((row.previous_status, row.current_status), ("proposed-unapplied", "provisional-in-use"))
            self.assertEqual(set(row.changed_fields), {"status", "page_status", "occurrence_bindings"})
            for name in before.keys() - set(row.changed_fields):
                self.assertEqual(before[name], after[name])
        candidates = [w for d in self.result.decisions for w in d.witnesses if w.recorded_phase == "candidate"]
        self.assertTrue(candidates)
        self.assertTrue(all(w.verified_phase == "applied-current-source" for w in candidates))

    def test_corrupt_ledger_is_rejected_even_if_json_still_valid(self):
        with self.assertRaisesRegex(ValueError, "Pinned ledger"):
            self.mutate_ledger(0, lambda data: data.update(status="other"))

    def test_reordered_commuting_patches_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "order differs"):
            self.mutate_ledger(2, lambda data: data["transactions"][1]["patches"].reverse(), repin_for_structural_test=True)

    def test_wrong_decision_id_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Decision inventory"):
            self.mutate_ledger(1, lambda data: data["decisions"][0].update(decision_id="invented"), repin_for_structural_test=True)

    def test_missing_explicit_patch_ownership_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "patch owners"):
            self.mutate_ledger(1, lambda data: data["transactions"][0]["patches"][0].update(decision_ids=[]), repin_for_structural_test=True)

    def test_wrong_same_edition_patch_ownership_is_rejected(self):
        def corrupt(data):
            data["transactions"][1]["patches"][0]["decision_ids"] = [data["decisions"][1]["decision_id"]]
        with self.assertRaises(ValueError):
            self.mutate_ledger(1, corrupt, repin_for_structural_test=True)

    def test_ambiguous_reduction_join_is_rejected(self):
        ledger = batch.parse(self.result.ledgers[2].raw_bytes)
        t = ledger["transactions"][0]
        choices = copy.deepcopy(ledger["decisions"])
        choices.append(copy.deepcopy(choices[0]))
        choices[-1]["decision_id"] = "duplicate-content"
        with self.assertRaisesRegex(ValueError, "ambiguous exact reduction"):
            batch.patch_owners(t, t["patches"][0], choices)

    def test_wrong_patch_and_wrong_boundary_are_rejected(self):
        def wrong_patch(data):
            data["transactions"][0]["patches"][0]["after"] += "!"
        def wrong_boundary(data):
            data["transactions"][0]["patches"][0]["before_location"]["byte_end"] += 1
        for change in (wrong_patch, wrong_boundary):
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.mutate_ledger(2, change, repin_for_structural_test=True)

    def test_live_source_and_stored_predecessor_corruption_are_rejected(self):
        targets = [batch.REPO / self.result.sources[0].after.path,
            batch.REPO / "evidence/classical/repairs/history/reduction-before-applied-20260907/msa-reduction.tex"]
        for target in targets:
            with self.subTest(target=target), self.assertRaises(ValueError):
                batch.normalize(read=lambda path: self.bytes[path] + (b"!" if path == target else b""))

    def test_wrong_proposal_history_bytes_are_rejected(self):
        target = batch.REPO / batch.PROPOSAL_HISTORY
        with self.assertRaisesRegex(ValueError, "Proposal predecessor bytes"):
            batch.normalize(read=lambda path: self.bytes[path] + (b"\n" if path == target else b""))

    def test_concurrent_input_change_rejected_at_final_readback(self):
        counts = {}
        target = batch.REPO / self.result.sources[0].after.path
        def reader(path):
            counts[path] = counts.get(path, 0) + 1
            return self.bytes[path] + (b"!" if path == target and counts[path] == 2 else b"")
        with self.assertRaisesRegex(ValueError, "changed during finite"):
            batch.normalize(read=reader)

    def test_unique_literals_and_strict_patch_newline_boundaries(self):
        raw = "أول\nثان\nخاتمة".encode()
        identity = batch.Identity("example", len(raw), batch.sha(raw))
        loc = batch.exact_location(raw, identity, "أول\n")
        recorded = {"byte_start": loc.byte_start, "byte_end": loc.byte_end,
                    "line_start": 1, "line_end": 2, "literal": "أول\n", "excerpt": "أول\nثان"}
        with self.assertRaises(ValueError):
            batch.exact_location(raw, identity, "أول\n", recorded)
        self.assertEqual(batch.exact_location(raw, identity, "أول\n", recorded, witness_newline_endpoint=True).line_end, 1)
        recorded["line_end"] = 3
        with self.assertRaises(ValueError):
            batch.exact_location(raw, identity, "أول\n", recorded, witness_newline_endpoint=True)
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            batch.exact_location(b"word word", identity, "word")


if __name__ == "__main__":
    unittest.main()
