from __future__ import annotations

import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from build import generate_expert_review_index as index


REPO = Path(__file__).resolve().parents[2]
ENGLISH = Path("source-snapshot/english")
LEDGERS = [index.APPLIED_SCOPE_LEDGER, index.APPLIED_DUAL_LEDGER, index.APPLIED_CLASSICAL_LEDGER]
OLD_QUALIFICATION = next(iter(index.QUALIFICATION_PROPAGATION_REPAIRS))


class AppliedRepairIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline_bytes = (REPO / "evidence/classical/BASELINE.json").read_bytes()
        cls.units = json.loads(cls.baseline_bytes)["units"]
        # Read-only admission discovers only the bounded dependencies used by
        # these four ledgers. Tests mutate isolated copies, never live sources.
        _, _, hashes = index.load_decisions(REPO, [REPO / p for p in LEDGERS + [OLD_QUALIFICATION]], cls.units, ENGLISH)
        cls.files = {}
        for path in hashes:
            if path.is_relative_to(ENGLISH):
                cls.files[("english", path.relative_to(ENGLISH))] = path.read_bytes()
            else:
                cls.files[("repo", path.relative_to(REPO))] = path.read_bytes()

    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="expert-applied-repairs-")
        self.addCleanup(temp.cleanup)
        self.repo, self.english = Path(temp.name) / "repo", Path(temp.name) / "english"
        for (kind, relative), data in self.files.items():
            path = (self.repo if kind == "repo" else self.english) / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.baseline = self.repo / "evidence/classical/BASELINE.json"
        self.baseline.write_bytes(self.baseline_bytes)

    def load(self, paths=LEDGERS):
        return index.load_decisions(self.repo, [self.repo / p for p in paths], self.units, self.english)

    def payload(self, logical):
        return json.loads((self.repo / logical).read_text(encoding="utf-8"))

    def save(self, logical, payload):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        (self.repo / logical).write_bytes(raw)
        return index.sha256_bytes(raw)

    def test_fourteen_separate_choices_retain_canonical_explanations_and_full_history(self):
        rows, _, hashes = self.load()
        self.assertEqual(len(rows), 14)
        self.assertEqual(len({r["decision_id"] for r in rows}), 14)
        self.assertEqual(sum(len(r["occurrences"]) for r in rows), 15)
        for row in rows:
            repair = row["semantic_propagation_repair"]
            self.assertEqual(repair["source_ledger"], self.payload(repair["ledger_path"]))
            choice = repair["choice_record"]
            self.assertEqual(row["recorded_decision_id"], choice["decision_id"])
            self.assertEqual(row["rationale"], choice["rationale"])
            self.assertEqual(row["chosen_arabic"], choice["chosen_arabic"])
            self.assertEqual(row["decision_id"], "semantic-propagation-20260906:" + choice["decision_id"])
            self.assertTrue(row["open_to_correction"] and row["expert_review_non_blocking"])
            self.assertTrue(row["expert_question"])
            self.assertFalse(row["official_attestation_claimed"])
            self.assertIsNone(row["printed_page"])
            history = repair["historical_before_source"]
            self.assertEqual(index.sha256_bytes(history["text_utf8"].encode("utf-8")), history["sha256"])
            self.assertEqual(len(history["text_utf8"].encode("utf-8")), history["bytes"])
        index.verify_inputs_unchanged(hashes)

    def test_small_human_export_preserves_all_raw_occurrences_and_complete_csv_reasons(self):
        payload, hashes = index.build_payload(self.repo, self.baseline, [self.repo / p for p in LEDGERS], self.english, [],
            "https://example.invalid/ar/blob/pinned/", "https://example.invalid/en/blob/pinned/")
        self.assertEqual(len(payload["decisions"]), 14)
        csv_rows = list(csv.DictReader(io.StringIO(index.render_occurrence_csv(payload))))
        for row in payload["decisions"]:
            self.assertTrue(row["index_metadata"]["human_index_included"])
            raw = set()
            for occurrence in row["occurrences"]:
                for loc in index.normalize_occurrence_sources(occurrence):
                    raw.add((loc["source_kind"], loc["path"], loc["line_start"], loc["line_end"]))
            human = set()
            for occurrence in row["index_metadata"]["occurrences"]:
                for loc in occurrence["locations"]:
                    rec = loc["line_reconciliation"]
                    self.assertTrue(rec["resolved"] and rec["recorded_hash_matches_current"], (row["decision_id"], loc))
                    self.assertIsNot(loc.get("human_review_included"), False)
                    self.assertFalse(loc["page_evidence"])
                    human.add((loc["source_kind"], loc["logical_path"], rec["current_line_start"], rec["current_line_end"]))
            self.assertEqual(raw, human, row["decision_id"])
            rendered = [r for r in csv_rows if r[index.CSV_COLUMNS[1]] == row["decision_id"]]
            self.assertTrue(rendered)
            for r in rendered:
                self.assertEqual(r[index.CSV_COLUMNS[5]], index.human_prose(index.human_decision_field(row, "rationale")))
            notes = []
            index.append_assessment_provenance(notes, row, "../../")
            label = "Classical" if row["semantic_propagation_repair"]["changed_edition"] == "classical" else "MSA"
            self.assertIn("Previous " + label + " wording", notes[0])
            if row["semantic_propagation_repair"]["ledger_path"] == index.APPLIED_CLASSICAL_LEDGER:
                rendered_notes = "\n".join(notes)
                for occurrence in row["semantic_propagation_repair"]["choice_record"]["occurrences"]:
                    self.assertIn(index.md_text(occurrence["rationale"]), rendered_notes)
                    self.assertIn(index.md_text(occurrence["expert_review_question"]), rendered_notes)
                    for alternative in occurrence["alternatives"]:
                        self.assertIn(index.md_text(alternative["reason"]), rendered_notes)
        index.verify_inputs_unchanged(hashes)

    def test_historical_0008_qualification_is_preserved_with_separate_proved_current_witness(self):
        old = (self.repo / OLD_QUALIFICATION).read_bytes()
        rows, _, hashes = self.load([OLD_QUALIFICATION])
        row = next(r for r in rows if r["recorded_decision_id"] == "0008-P1")
        repair = row["semantic_propagation_repair"]
        self.assertEqual(repair["source_ledger"], json.loads(old))
        self.assertEqual((self.repo / OLD_QUALIFICATION).read_bytes(), old)
        companions = repair["current_witness_companions"]
        self.assertEqual(len(companions), 1)
        new = companions[0]["source_ledger"]["qualification_witness"]["current_declaration"]
        self.assertEqual(row["occurrences"][0]["classical"]["sha256"], new["sha256"].upper())
        self.assertEqual([(l["line_start"], l["line_end"]) for l in row["occurrences"][0]["classical"]["locators"]], [(113, 113)])
        index.verify_inputs_unchanged(hashes)

    def test_changed_canonical_motivation_is_not_silently_readmitted(self):
        for logical in LEDGERS:
            with self.subTest(logical=logical):
                original = (self.repo / logical).read_bytes()
                data = self.payload(logical)
                data["units" if logical == index.APPLIED_SCOPE_LEDGER else "decisions"][0]["rationale"] = "Fabricated replacement explanation."
                self.save(logical, data)
                with self.assertRaisesRegex(ValueError, "unapproved"):
                    self.load([logical])
                (self.repo / logical).write_bytes(original)

    def test_omitted_new_choice_and_duplicate_reserved_ids_fail(self):
        data = self.payload(index.APPLIED_DUAL_LEDGER)
        data["decisions"].pop()
        digest = self.save(index.APPLIED_DUAL_LEDGER, data)
        with mock.patch.object(index, "APPLIED_DUAL_SHA256", digest):
            with self.assertRaisesRegex(ValueError, "six-choice inventory"):
                self.load([index.APPLIED_DUAL_LEDGER])
        with self.assertRaisesRegex(ValueError, "duplicate dated propagation"):
            self.load([index.APPLIED_SCOPE_LEDGER, index.APPLIED_SCOPE_LEDGER])

    def test_fabricated_pages_are_rejected_before_ledger_pin(self):
        for logical in LEDGERS:
            data = self.payload(logical)
            data["printed_page"] = 15
            self.save(logical, data)
            with self.assertRaisesRegex(ValueError, "unverified final page"):
                self.load([logical])

    def test_current_source_drift_fails_even_though_canonical_ledger_is_unchanged(self):
        for logical in LEDGERS:
            data = self.payload(logical)
            loc = (data["units"][0]["locations"]["msa"] if logical == index.APPLIED_SCOPE_LEDGER else
                   data["editions"]["classical"]["after"] if logical == index.APPLIED_DUAL_LEDGER else data["source"])
            path = self.repo / loc["path"]
            before = path.read_bytes()
            path.write_bytes(before + b"% drift\n")
            with self.assertRaisesRegex(ValueError, "source identity hash/bytes"):
                self.load([logical])
            path.write_bytes(before)

    def test_scope_predecessor_and_exact_inverse_cannot_be_forged(self):
        data = self.payload(index.APPLIED_SCOPE_LEDGER)
        data["units"][0]["patches"][0]["before"] += " forged"
        digest = self.save(index.APPLIED_SCOPE_LEDGER, data)
        with mock.patch.object(index, "APPLIED_SCOPE_SHA256", digest):
            with self.assertRaisesRegex(ValueError, "patch hash mismatch"):
                self.load([index.APPLIED_SCOPE_LEDGER])
        path = self.repo / index.QUALIFICATION_PRIOR_MANIFEST_RELATIVE
        path.write_bytes(path.read_bytes() + b"\n")
        with self.assertRaisesRegex(ValueError, "pinned predecessor manifest hash"):
            self.load([index.APPLIED_DUAL_LEDGER])

    def test_byte_locator_and_dual_literal_forgery_are_rejected(self):
        data = self.payload(index.APPLIED_CLASSICAL_LEDGER)
        data["decisions"][0]["occurrences"][0]["english"]["byte_start"] += 1
        digest = self.save(index.APPLIED_CLASSICAL_LEDGER, data)
        with mock.patch.object(index, "APPLIED_CLASSICAL_SHA256", digest):
            with self.assertRaisesRegex(ValueError, "byte witness exact excerpt"):
                self.load([index.APPLIED_CLASSICAL_LEDGER])
        data = self.payload(index.APPLIED_DUAL_LEDGER)
        data["decisions"][0]["english_source_literal"] = "signed"
        digest = self.save(index.APPLIED_DUAL_LEDGER, data)
        with mock.patch.object(index, "APPLIED_DUAL_SHA256", digest):
            with self.assertRaisesRegex(ValueError, "literal source phrase mismatch"):
                self.load([index.APPLIED_DUAL_LEDGER])

    def test_refresh_cannot_rewrite_original_reason_or_unproved_passage(self):
        data = self.payload(index.APPLIED_CLASSICAL_REFRESH)
        data["qualification_witness"]["historical_rationale"] = "Changed reason"
        digest = self.save(index.APPLIED_CLASSICAL_REFRESH, data)
        with mock.patch.object(index, "APPLIED_CLASSICAL_REFRESH_SHA256", digest):
            with self.assertRaisesRegex(ValueError, "historical provenance mismatch"):
                self.load([OLD_QUALIFICATION])

    def test_missing_new_ledger_named_in_metadata_fails_discovery(self):
        metadata = self.repo / "evidence/classical/SOURCE_RECONCILIATION_METADATA_20260905.json"
        metadata.write_text(json.dumps({"correction_metadata": [{"authority_refs": [index.APPLIED_SCOPE_LEDGER]}]}), encoding="utf-8")
        (self.repo / index.APPLIED_SCOPE_LEDGER).unlink()
        with self.assertRaisesRegex(ValueError, "missing commissioned propagation ledger"):
            index.discover_ledgers(self.repo)

    def test_foreign_path_cannot_bypass_strict_new_ledger_admission(self):
        foreign = self.repo / "foreign.json"
        for logical in LEDGERS:
            foreign.write_bytes((self.repo / logical).read_bytes())
            with self.assertRaises(ValueError):
                index.load_decisions(self.repo, [foreign], self.units, self.english)

    def test_complete_current_source_rehash_still_cannot_erase_prior_correction(self):
        logical = index.APPLIED_SCOPE_LEDGER
        data = self.payload(logical)
        row = data["units"][0]
        path = self.repo / row["locations"]["msa"]["path"]
        changed = path.read_bytes() + b"% unauthorized unrelated edit\n"
        path.write_bytes(changed)
        row["locations"]["msa"].update(sha256=index.sha256_bytes(changed), bytes=len(changed),
                                        after_sha256=index.sha256_bytes(changed), after_bytes=len(changed))
        digest = self.save(logical, data)
        with mock.patch.object(index, "APPLIED_SCOPE_SHA256", digest):
            with self.assertRaisesRegex(ValueError, "source identity hash/bytes mismatch"):
                self.load([logical])

    def test_source_change_after_admission_is_guarded(self):
        _, _, hashes = self.load()
        path = self.repo / "source/locale/ar/open-logic-config.sty"
        self.assertIn(path, hashes)
        path.write_bytes(path.read_bytes() + b"% changed tokenizer definition\n")
        with self.assertRaises(RuntimeError):
            index.verify_inputs_unchanged(hashes)

    def test_missing_refresh_cannot_silently_accept_old_0008_full_hash(self):
        (self.repo / index.APPLIED_CLASSICAL_REFRESH).unlink()
        with self.assertRaisesRegex(ValueError, "classical qualification source hash mismatch"):
            self.load([OLD_QUALIFICATION])

    def test_0008_preserved_snapshot_and_refresh_excerpts_are_independently_checked(self):
        data = self.payload(index.APPLIED_CLASSICAL_LEDGER)
        prior = self.repo / data["source"]["prior_snapshot"]["path"]
        original = prior.read_bytes()
        prior.write_bytes(original + b"\n")
        with self.assertRaisesRegex(ValueError, "source identity hash/bytes mismatch"):
            self.load([index.APPLIED_CLASSICAL_LEDGER])
        prior.write_bytes(original)
        data = self.payload(index.APPLIED_CLASSICAL_REFRESH)
        data["qualification_witness"]["current_declaration"]["line_start"] = 114
        digest = self.save(index.APPLIED_CLASSICAL_REFRESH, data)
        with mock.patch.object(index, "APPLIED_CLASSICAL_REFRESH_SHA256", digest):
            with self.assertRaisesRegex(ValueError, "exact excerpt/hash mismatch"):
                self.load([OLD_QUALIFICATION])


if __name__ == "__main__":
    unittest.main()
