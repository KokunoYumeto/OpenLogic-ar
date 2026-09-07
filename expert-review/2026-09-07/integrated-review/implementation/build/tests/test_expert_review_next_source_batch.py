"""Bounded 16-choice source/reviewer contract; no export, TeX or source writes."""
from __future__ import annotations

import copy
import csv
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from build.tests import test_expert_review_consolidated_repairs as H

G, V, ROOT, ENGLISH = H.G, H.V, H.ROOT, H.ENGLISH


class NextSourceBatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.specs, cls.identities, cls.inventory = V.next_repair_expectations(ROOT, ENGLISH)
        cls.baseline = {u["id"]: u for u in json.loads((ROOT / "evidence/classical/BASELINE.json").read_bytes())["units"]}
        cls.raw, cls.rows = {}, {}
        for identity in cls.identities:
            payload = json.loads((ROOT / identity["path"]).read_bytes())
            rows, _ = G.normalize_applied_repairs(payload, copy.deepcopy(identity), ROOT, cls.baseline, ENGLISH)
            for row in rows:
                cls.raw[row["decision_id"]] = row
                cls.rows[row["decision_id"]] = H.reconcile_generated(row, cls.baseline)

    def test_exact_sixteen_choices_twenty_six_groups_three_pinned_ledgers(self):
        self.assertEqual(len(self.specs), 16)
        self.assertEqual(set(self.specs), set(self.rows))
        self.assertEqual(sum(len(s["occurrence_specs"]) for s in self.specs.values()), 26)
        self.assertEqual(sum(len(r["occurrences"]) for r in self.rows.values()), 26)
        self.assertEqual(len(self.identities), 3)
        for identity in self.identities:
            path = identity["path"]
            self.assertEqual(identity["sha256"].upper(), G.NEXT_BATCH_LEDGERS[path][0])
            self.assertEqual(identity["sha256"], V.NEXT_REPAIR_LEDGERS[path][0])

    def test_all_actual_reconciled_records_pass_independent_readback(self):
        for key, row in self.rows.items():
            with self.subTest(key=key):
                self.assertEqual(H.record_errors(row, self.specs[key]), [])
                for occurrence in row["index_metadata"]["occurrences"]:
                    self.assertTrue(occurrence["human_review_included"])
                    self.assertTrue(all(loc["human_review_included"] for loc in occurrence["locations"]))

    def test_all_canonical_rows_complete_ledgers_and_motivations_remain_unchanged(self):
        for key, row in self.rows.items():
            spec = self.specs[key]
            self.assertEqual(row["semantic_propagation_repair"]["source_ledger"], spec["payload"])
            self.assertEqual(row["semantic_propagation_repair"]["choice_record"], spec["canonical_choice"])
            self.assertEqual(row["rationale"], spec["canonical_choice"]["rationale"])
            self.assertEqual(row["expert_question"], spec["canonical_choice"]["expert_question"])
            self.assertFalse(row["official_attestation_claimed"])
            self.assertIsNone(row["printed_page"])

    def test_current_and_historical_literal_source_identity_and_context(self):
        historical_shifts = 0
        for row in self.rows.values():
            histories = {h["path"]: h["text_utf8"].encode() for h in row["semantic_propagation_repair"]["historical_before_source"]["sources"]}
            for p in row["literal_source_passages"]:
                for phase in ("english", "before", "after"):
                    w = p[phase]
                    data = histories[w["path"]] if phase == "before" else ((ENGLISH if phase == "english" else ROOT) / w["path"]).read_bytes()
                    self.assertEqual(H.digest(data).upper(), w["sha256"])
                    self.assertEqual(V.exact_excerpt(data, w["line_start"], w["line_end"]), w["excerpt"])
                    self.assertTrue(V.active_phrase(w["excerpt"], w["literal"], "english" if phase == "english" else p["edition"]))
                if "assessed_after" in p:
                    historical_shifts += 1
                    old = p["assessed_after"]
                    data = V.historical_version_bytes(ROOT, old, {})
                    self.assertEqual(V.exact_excerpt(data, old["line_start"], old["line_end"]), old["excerpt"])
                    self.assertEqual(old["literal"], p["after"]["literal"])
                    self.assertEqual(old["line_start"] - 1, p["after"]["line_start"])
                    self.assertIn("historical", p["before_role"])
        self.assertEqual(historical_shifts, 5)

    def test_actual_human_provenance_and_csv_preserve_every_pair(self):
        for key, row in self.rows.items():
            with self.subTest(key=key):
                spec = self.specs[key]
                surfaces, _ = H.surface_fixture(row, spec)
                lines = []
                G.append_assessment_provenance(lines, row, "")
                for sections in surfaces.values():
                    body = "\n".join(line for line in sections[key][0].splitlines()
                        if "**New repair assessment / تقييم تصحيحي جديد:**" not in line
                        and "**Literal source passage / اللفظ في موضعه:**" not in line)
                    sections[key][0] = body + "\n" + "\n".join(lines)
                rows = list(csv.reader(io.StringIO(G.render_occurrence_csv({"decisions": [row]}))))[1:]
                self.assertEqual(len(rows), len(spec["occurrence_specs"]))
                self.assertEqual(H.surface_errors(row, spec, surfaces, {key: rows}), [])

    def test_reasons_questions_authority_and_historical_or_live_fields_cannot_be_forged(self):
        for key, row in self.rows.items():
            for field in ("rationale", "expert_question", "chosen_arabic", "before_arabic", "sense", "official_attestation_claimed"):
                wrong = copy.deepcopy(row)
                wrong[field] = "invented"
                self.assertTrue(H.record_errors(wrong, self.specs[key]), (key, field))
            for phase in ("english", "before", "after"):
                wrong = copy.deepcopy(row)
                wrong["literal_source_passages"][0][phase]["line_start"] += 1
                self.assertTrue(H.record_errors(wrong, self.specs[key]), (key, phase))
            wrong = copy.deepcopy(row)
            wrong["semantic_propagation_repair"]["choice_record"] = {}
            self.assertTrue(H.record_errors(wrong, self.specs[key]))

    def test_missing_duplicate_and_cross_paired_occurrences_fail(self):
        for key, row in self.rows.items():
            for collection in ("raw", "human"):
                wrong = copy.deepcopy(row)
                groups = wrong["occurrences"] if collection == "raw" else wrong["index_metadata"]["occurrences"]
                groups.pop()
                self.assertTrue(H.record_errors(wrong, self.specs[key]))
            if len(row["occurrences"]) > 1:
                wrong = copy.deepcopy(row)
                wrong["occurrences"][0] = copy.deepcopy(wrong["occurrences"][1])
                self.assertTrue(H.record_errors(wrong, self.specs[key]))

    def test_ledger_payload_schema_ids_and_hash_mutations_fail_closed(self):
        for identity in self.identities:
            payload = json.loads((ROOT / identity["path"]).read_bytes())
            with self.assertRaises(ValueError):
                G.normalize_applied_repairs(payload, dict(identity, path="evidence/classical/repairs/unapproved.json"),
                    ROOT, self.baseline, ENGLISH)
            for field, value in (("schema", "forged"), ("assessed_on", "2027-01-01"), ("decisions", payload["decisions"][:-1])):
                wrong = dict(payload, **{field: value})
                with self.assertRaises(ValueError):
                    G.normalize_applied_repairs(wrong, copy.deepcopy(identity), ROOT, self.baseline, ENGLISH)
            original = Path.read_bytes
            target = (ROOT / identity["path"]).resolve()
            def changed(path):
                data = original(path)
                return data + b" " if path.resolve() == target else data
            with patch.object(Path, "read_bytes", changed):
                with self.assertRaises(ValueError):
                    V.next_repair_expectations(ROOT, ENGLISH)

    def test_formula_display_preserves_operator_meaning_without_raw_commands(self):
        key = next(k for k in self.rows if "FINITE-GRID" in k)
        row = self.rows[key]
        self.assertIn("m≥2", G.human_chosen_arabic(row))
        self.assertIn("m≥2", G.rtl(G.human_chosen_arabic(row)))
        wrong = copy.deepcopy(row)
        wrong["review_display"]["chosen_arabic"] = wrong["review_display"]["chosen_arabic"].replace("≥", "≤")
        self.assertTrue(H.record_errors(wrong, self.specs[key]))

    def test_actual_display_alternatives_provenance_and_csv_pass_raw_syntax_gate(self):
        for key, row in self.rows.items():
            lines = []
            G.append_assessment_provenance(lines, row, "")
            values = {"provenance": "\n".join(lines),
                      "alternatives": "\n".join(G.alternatives_text(row)),
                      "csv": G.render_occurrence_csv({"decisions": [row]})}
            for field in ("english_term", "chosen_arabic", "before_arabic", "rationale", "expert_question"):
                values[field] = row["review_display"][field]
            G.verify_human_surfaces(values)

    def test_unknown_operator_fails_and_valuation_extension_is_not_erased(self):
        registry = G.load_review_token_registries(ROOT)["english"]
        with self.assertRaises(ValueError):
            G.render_next_source_review_text(r"$m\unknownrelation 2$", registry)
        self.assertEqual(G.render_next_source_review_text(r"\pValue v(p) = \False", registry), "𝔳̅(p) = 𝔽")
        self.assertEqual(G.render_next_source_review_text(r"\pAssign v(p) = \Undef", registry), "𝔳(p) = 𝕌")

    def test_historical_hashes_require_exact_transition_not_matching_phrase(self):
        for (logical, old_sha), _ in V.HISTORICAL_TRANSITIONS.items():
            candidate = next(i for i in self.identities if i["path"] == V.HISTORICAL_TRANSITIONS[(logical, old_sha)])
            payload = json.loads((ROOT / candidate["path"]).read_bytes())
            t = next(t for t in payload["transactions"] if t["path"] == logical)
            old_id = {"path": logical, "sha256": old_sha, "bytes": t["before_bytes"]}
            recovered = V.historical_version_bytes(ROOT, old_id, {})
            self.assertEqual(H.digest(recovered), old_sha)
            self.assertEqual(G.next_batch_version_source(ROOT, old_id, {}), recovered)
            target, original = (ROOT / logical).resolve(), Path.read_bytes
            def changed(path):
                data = original(path)
                return data + b"% unrelated later mutation\n" if path.resolve() == target else data
            with patch.object(Path, "read_bytes", changed):
                with self.assertRaises(ValueError):
                    V.historical_version_bytes(ROOT, old_id, {})
                with self.assertRaises(ValueError):
                    G.next_batch_version_source(ROOT, old_id, {})
            with self.assertRaises(ValueError):
                G.next_batch_version_source(ROOT, dict(old_id, sha256="0" * 64), {})

    def test_earlier_roots_record_still_passes_with_live_classical_companion(self):
        specs, identities, _ = V.consolidated_repair_expectations(ROOT, ENGLISH)
        identity = next(i for i in identities if "TWO_ROOTS" in i["path"])
        records, _ = G.normalize_consolidated_repairs(json.loads((ROOT / identity["path"]).read_bytes()),
            copy.deepcopy(identity), ROOT, self.baseline, ENGLISH)
        row = H.reconcile_generated(records[0], self.baseline)
        self.assertEqual(H.record_errors(row, specs[row["decision_id"]]), [])
        companion = row["literal_source_passages"][0]["classical"]
        self.assertEqual(companion["assessed_source_witness"]["sha256"],
            "8183C83E20FC04CED33D83554EBB142F94B7C8BF323B992336A25B9153DB2498")
        self.assertNotEqual(companion["sha256"], companion["assessed_source_witness"]["sha256"])


if __name__ == "__main__":
    unittest.main()
