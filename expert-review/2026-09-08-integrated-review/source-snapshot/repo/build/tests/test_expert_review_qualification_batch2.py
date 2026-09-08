from __future__ import annotations

import copy
import csv
import hashlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "generate_expert_review_index.py"
SPEC = importlib.util.spec_from_file_location("qualification_batch2_index", SCRIPT)
assert SPEC and SPEC.loader
INDEX = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = INDEX
SPEC.loader.exec_module(INDEX)
REPO = SCRIPT.parent.parent
ENGLISH = Path("source-snapshot/english")
LOGICAL = "evidence/classical/repairs/OLP0033_0039_0072_0081_QUALIFICATION_PROPAGATION_20260906.json"
SCHEMA, EXPECTED = INDEX.QUALIFICATION_PROPAGATION_REPAIRS[LOGICAL]
EXTRA_CHOICE = "0039-P1-no-surjection-connective"
DECISION_IDS = {u[4:] + "-P1" for u in EXPECTED} | {EXTRA_CHOICE}
CARDINALITY_LEDGER = "evidence/classical/repairs/OLP0033_NONENUMERABILITY_CONSTRUCTIONS_20260907.json"
CARDINALITY_LEDGER_SHA256 = "13aa46d70ae164ca7b2be107503238027c2fadc3d0204a3bc0c68d9feb26aecc"
CARDINALITY_HISTORY = ("evidence/provenance/locale-ar/expert-review-binding-history/"
                       "cardinality-source-batch-20260907/sources/")


def archived_pre_cardinality_sources(repo):
    """Recover this historical test fixture, never a mutable current substitute.

    The pinned later ledger independently identifies the archived sources that
    already contain the September 6 qualification but precede the cardinality
    repairs. The current-source transition has separate focused tests.
    """
    raw = (repo / CARDINALITY_LEDGER).read_bytes()
    if hashlib.sha256(raw).hexdigest() != CARDINALITY_LEDGER_SHA256:
        raise ValueError("Historical fixture cardinality ledger identity differs")
    ledger = json.loads(raw)
    transactions = ledger["transactions"]
    if (ledger["schema"] != "arabic-bounded-source-repairs.v1"
            or [(t["unit_id"], t["edition"]) for t in transactions]
            != [("OLP-0033", "msa"), ("OLP-0033", "classical")]):
        raise ValueError("Historical fixture cardinality transaction inventory differs")
    result = {}
    for transaction in transactions:
        kind = transaction["edition"]
        data = (repo / (CARDINALITY_HISTORY + "OLP-0033-" + kind + ".tex")).read_bytes()
        if ((len(data), hashlib.sha256(data).hexdigest())
                != (transaction["before_bytes"], transaction["before_sha256"])):
            raise ValueError("Historical fixture archived before-source identity differs: " + kind)
        result[kind] = data
    return result


class ExpertReviewQualificationBatch2Tests(unittest.TestCase):
    """Use bounded byte-for-byte fixture copies, never alter the live corpus."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="expert-qualification-batch2-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.english = Path(self.temp.name) / "english"
        self.payload = json.loads((REPO / LOGICAL).read_text(encoding="utf-8"))
        baseline_bytes = (REPO / "evidence/classical/BASELINE.json").read_bytes()
        self.baseline = json.loads(baseline_bytes)
        self.baseline_path = self.repo / "evidence/classical/BASELINE.json"
        self.baseline_path.parent.mkdir(parents=True, exist_ok=True)
        self.baseline_path.write_bytes(baseline_bytes)
        self.units = self.baseline["units"]
        self.baseline_by_id = {u["id"]: u for u in self.units}
        self.prior_path = self.repo / INDEX.QUALIFICATION_PRIOR_MANIFEST_RELATIVE
        self.prior_bytes = (REPO / INDEX.QUALIFICATION_PRIOR_MANIFEST_RELATIVE).read_bytes()
        self.prior_path.write_bytes(self.prior_bytes)
        self.prior = json.loads(self.prior_bytes)
        self.prior_by_id = {u["id"]: u for u in self.prior["units"]}
        historical_sources = archived_pre_cardinality_sources(REPO)
        for row in self.payload["units"]:
            for kind, prefix in (("english", ""), ("msa", "source/locale/ar/"),
                                 ("classical", "source/locale/ar-classical/")):
                relative = prefix + EXPECTED[row["unit_id"]]
                self.assertEqual(row["locations"][kind]["path"], relative)
                source = (ENGLISH if kind == "english" else REPO) / relative
                target = (self.english if kind == "english" else self.repo) / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                if row["unit_id"] == "OLP-0033" and kind in historical_sources:
                    data = historical_sources[kind]
                    declaration = row["locations"][kind]
                    phase = "after_" if kind == "msa" else ""
                    self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                                     (declaration[phase + "bytes"], declaration[phase + "sha256"]))
                else:
                    data = source.read_bytes()
                target.write_bytes(data)
        self.path = self.repo / LOGICAL
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.write_ledger()

    def write_ledger(self):
        self.path.write_text(json.dumps(self.payload, ensure_ascii=False), encoding="utf-8")

    def load(self):
        self.write_ledger()
        return INDEX.load_decisions(self.repo, [self.path], self.units, self.english)

    def row(self, unit_id):
        return next(r for r in self.payload["units"] if r["unit_id"] == unit_id)

    def test_live_batch2_admission_binds_all_predecessor_and_current_bytes(self):
        decisions, inventory, hashes = self.load()
        self.assertEqual({d["recorded_decision_id"] for d in decisions}, DECISION_IDS)
        self.assertEqual(len(hashes), 14)  # ledger + twelve sources + immutable prior manifest
        self.assertEqual(hashes[self.prior_path.resolve()], INDEX.QUALIFICATION_PRIOR_MANIFEST_SHA256)
        self.assertEqual(inventory[0]["adapter"]["kind"], "dated-semantic-qualification-repair-v1")
        self.assertEqual(inventory[0]["adapter"]["prior_source_manifest"]["sha256"], INDEX.QUALIFICATION_PRIOR_MANIFEST_SHA256)
        for d in decisions:
            unit_id = d["occurrences"][0]["unit_id"]
            repair = d["semantic_propagation_repair"]
            self.assertEqual(repair["source_ledger"], self.payload)
            old = repair["historical_before_source"]
            before = old["text_utf8"].encode("utf-8")
            prior = self.prior_by_id[unit_id]
            self.assertEqual(INDEX.sha256_bytes(before), prior["msa"]["sha256"].upper())
            self.assertEqual(len(before), prior["msa"]["bytes"])
            self.assertEqual(old["path"], prior["msa"]["path"])
            self.assertEqual(old["identity_basis"]["unit"], prior)
            self.assertEqual(old["identity_basis"]["manifest"]["sha256"], INDEX.QUALIFICATION_PRIOR_MANIFEST_SHA256)
            if unit_id in {"OLP-0039", "OLP-0081"}:
                self.assertNotEqual(INDEX.sha256_bytes(before), self.baseline_by_id[unit_id]["arabic_sha256"].upper())
                self.assertEqual(prior["msa"]["identity_mode"], "baseline-correction")
            else:
                self.assertEqual(INDEX.sha256_bytes(before), self.baseline_by_id[unit_id]["arabic_sha256"].upper())
            self.assertIsNone(d["printed_page"])
            self.assertEqual(d["page_status"], "bind-after-final-reader-build")
            self.assertFalse(d["official_attestation_claimed"])
            self.assertTrue(d["expert_review_non_blocking"] and d["open_to_correction"])
        INDEX.verify_inputs_unchanged(hashes)

    def test_missing_or_modified_immutable_manifest_fails_closed(self):
        self.prior_path.unlink()
        with self.assertRaisesRegex(ValueError, "missing/out-of-scope immutable qualification prior manifest"):
            self.load()
        self.prior_path.write_bytes(self.prior_bytes + b"\n")
        with self.assertRaisesRegex(ValueError, "immutable qualification prior manifest hash mismatch"):
            self.load()

    def test_oversized_prior_manifest_is_rejected_before_json_loading(self):
        self.prior_path.write_bytes(b" " * (2 * 1024 * 1024 + 1))
        with self.assertRaisesRegex(ValueError, "oversized immutable qualification prior manifest"):
            self.load()

    def test_manifest_drift_after_admission_is_included_in_input_guard(self):
        _, _, hashes = self.load()
        self.prior_path.write_bytes(self.prior_bytes + b"\n")
        with self.assertRaisesRegex(RuntimeError, "input"):
            INDEX.verify_inputs_unchanged(hashes)

    def test_mutable_overlay_is_neither_a_dependency_nor_a_substitute(self):
        relative = self.prior["baseline_correction_overlay"]["path"]
        overlay = self.repo / relative
        overlay.parent.mkdir(parents=True, exist_ok=True)
        overlay.write_text('{"not_the_immutable_predecessor": true}', encoding="utf-8")
        _, _, hashes = self.load()
        self.assertNotIn(overlay.resolve(), hashes)
        self.prior_path.unlink()
        with self.assertRaisesRegex(ValueError, "missing/out-of-scope immutable qualification prior manifest"):
            self.load()

    def test_self_consistent_forged_before_hash_cannot_erase_prior_repairs(self):
        for unit_id in ("OLP-0039", "OLP-0081"):
            original = copy.deepcopy(self.payload)
            row = self.row(unit_id)
            row["patches"][0]["before"] += "\n% fabricated replacement for a prior correction"
            loc = row["locations"]["msa"]
            before = (self.repo / loc["path"]).read_bytes()
            for patch in reversed(row["patches"]):
                after = patch["after"].encode("utf-8")
                self.assertEqual(before.count(after), 1)
                before = before.replace(after, patch["before"].encode("utf-8"), 1)
            loc.update(before_sha256=INDEX.sha256_bytes(before), before_bytes=len(before))
            # Even a matching mutable baseline declaration cannot replace the
            # independent, pinned predecessor manifest for this second batch.
            self.baseline_by_id[unit_id].update(arabic_sha256=INDEX.sha256_bytes(before), arabic_bytes=len(before))
            with self.assertRaisesRegex(ValueError, "immutable prior-manifest before identity mismatch"):
                self.load()
            self.payload = original

    def test_wrong_recorded_original_baseline_is_not_accepted_as_predecessor(self):
        for unit_id in ("OLP-0039", "OLP-0081"):
            original = copy.deepcopy(self.payload)
            loc = self.row(unit_id)["locations"]["msa"]
            baseline = self.baseline_by_id[unit_id]
            loc.update(before_sha256=baseline["arabic_sha256"], before_bytes=baseline["arabic_bytes"])
            with self.assertRaisesRegex(ValueError, "qualification inverse/before hash mismatch"):
                self.load()
            self.payload = original

    def test_english_and_classical_identities_cannot_drift_with_refreshed_ledger_hashes(self):
        for kind in ("english", "classical"):
            row = self.row("OLP-0033")
            loc = row["locations"][kind]
            target = (self.english if kind == "english" else self.repo) / loc["path"]
            original = target.read_bytes()
            loc_before = copy.deepcopy(loc)
            baseline_hash = self.baseline_by_id["OLP-0033"]["english_sha256"]
            changed = original + b"% unexpected source drift\n"
            target.write_bytes(changed)
            loc.update(sha256=INDEX.sha256_bytes(changed), bytes=len(changed))
            if kind == "english":
                self.baseline_by_id["OLP-0033"]["english_sha256"] = loc["sha256"]
                pattern = "prior-manifest English baseline identity mismatch"
            else:
                pattern = "Classical immutable prior-manifest identity mismatch"
            with self.assertRaisesRegex(ValueError, pattern):
                self.load()
            target.write_bytes(original)
            row["locations"][kind] = loc_before
            self.baseline_by_id["OLP-0033"]["english_sha256"] = baseline_hash

    def test_classification_is_unit_specific_not_assumed_inherited_english_error(self):
        original = copy.deepcopy(self.payload)
        for unit_id, false_classification in (
            ("OLP-0081", "inherited-source-qualification-already-correct-in-classical"),
            ("OLP-0039", "translation-any-versus-none-scope-ambiguity-already-correct-in-classical"),
            ("OLP-0072", "inherited-source-qualification-already-correct-in-classical"),
        ):
            self.row(unit_id)["classification"] = false_classification
            with self.assertRaisesRegex(ValueError, "qualification origin classification mismatch"):
                self.load()
            self.payload = copy.deepcopy(original)

    def test_literal_term_contracts_reject_compound_heading_and_wrong_excerpt(self):
        original = copy.deepcopy(self.payload)
        for edit in (
            lambda r: r.update(source_term="enumerable set / surjection"),
            lambda r: r.update(before_arabic="هو القول ...؛ أي"),
            lambda r: r.update(chosen_arabic="غير خالية"),
            lambda r: r["locations"]["classical"].update(excerpt="a different source passage"),
            lambda r: r["locations"]["msa"].update(changed_ranges=[[1, 2]]),
        ):
            edit(self.row("OLP-0033"))
            with self.assertRaises(ValueError):
                self.load()
            self.payload = copy.deepcopy(original)

    def test_english_substring_is_not_a_literal_enumerable_occurrence(self):
        row = self.row("OLP-0033")
        loc = row["locations"]["english"]
        lines = (self.english / loc["path"]).read_text(encoding="utf-8").splitlines()
        self.assertIn("!!{nonenumerable}", lines[27])
        self.assertNotIn("!!{enumerable}", lines[27])
        loc.update(line_start=28, line_end=28, excerpt=lines[27],
                   excerpt_sha256=INDEX.sha256_bytes(lines[27].encode("utf-8")))
        with self.assertRaisesRegex(ValueError, "lines lack the recorded term"):
            self.load()

    def test_primary_and_additional_choice_locators_point_at_the_actual_words(self):
        decisions, _, _ = self.load()
        expected = {
            "0039-P1": {"english": {27, 30}, "msa": {26}, "classical": {20}},
            EXTRA_CHOICE: {"english": {28}, "msa": {27}, "classical": {21}},
            "0081-P1": {"english": {28}, "msa": {27}, "classical": {26}},
        }
        for decision in decisions:
            key = decision["recorded_decision_id"]
            if key not in expected:
                continue
            actual = {kind: set() for kind in INDEX.SOURCE_LABELS}
            for loc in INDEX.normalize_occurrence_sources(decision["occurrences"][0]):
                actual[loc["source_kind"]].add(loc["line_start"])
                self.assertEqual(loc["line_start"], loc["line_end"])
                self.assertTrue(loc["excerpt"])
            self.assertEqual(actual, expected[key])

    def test_additional_connective_cannot_be_silently_omitted_or_duplicated(self):
        original = copy.deepcopy(self.payload)
        for change in (
            lambda row: row.pop("additional_phrase_choices"),
            lambda row: row.update(additional_phrase_choices=[]),
            lambda row: row["additional_phrase_choices"].append(copy.deepcopy(row["additional_phrase_choices"][0])),
            lambda row: row["additional_phrase_choices"][0].update(choice_id="uncommissioned-choice"),
        ):
            change(self.row("OLP-0039"))
            with self.assertRaisesRegex(ValueError, "commissioned 0039 connective choice"):
                self.load()
            self.payload = copy.deepcopy(original)

    def test_additional_choice_terms_prior_witness_and_patch_scope_are_verified(self):
        original = copy.deepcopy(self.payload)
        for change in (
            lambda e: e.update(source_term="that is / implication"),
            lambda e: e.update(unit_patch_indices=[1]),
            lambda e: e.update(unit_patch_indices=[False]),
            lambda e: e["patches"][0].update(before="unrelated text"),
            lambda e: e["expert_review"].update(open_to_correction=False),
            lambda e: e["locations"]["msa_before"].update(sha256="0" * 64),
            lambda e: e["locations"]["msa_before"].update(excerpt="invented predecessor"),
            lambda e: e["locations"]["msa"].update(path="source/locale/ar/unrelated.tex"),
            lambda e: e["locations"]["english"].update(line_start=26, line_end=100),
        ):
            change(self.row("OLP-0039")["additional_phrase_choices"][0])
            with self.assertRaises(ValueError):
                self.load()
            self.payload = copy.deepcopy(original)

    def test_before_excerpt_cannot_be_fabricated_despite_valid_whole_before_hash(self):
        original = copy.deepcopy(self.payload)
        for key, value in (("before_excerpt", "invented text"), ("before_excerpt_sha256", "0" * 64),
                           ("before_line_start", True), ("before_line_end", 9000)):
            self.row("OLP-0039")["locations"]["msa"][key] = value
            with self.assertRaisesRegex(ValueError, "qualification before excerpt"):
                self.load()
            self.payload = copy.deepcopy(original)

    def test_phrase_line_finder_excludes_comments_and_english_word_substrings(self):
        self.assertEqual(INDEX.qualification_active_phrase_ranges("% enumerable", "enumerable", "english", 1), [])
        self.assertEqual(INDEX.qualification_active_phrase_ranges("nonenumerable", "enumerable", "english", 1), [])
        self.assertEqual(INDEX.qualification_active_phrase_ranges("!!{enumerable}", "enumerable", "english", 1), [(1, 1)])
        self.assertEqual(INDEX.qualification_active_phrase_ranges("% بل لا توجد دالة", "بل لا توجد دالة", "msa", 1), [])
        self.assertEqual(INDEX.qualification_active_phrase_ranges("وكل مجموعة غير خالية", "كل مجموعة غير خالية", "msa", 7), [(7, 7)])

    def test_schema_ids_duplicates_paths_and_pages_fail_closed(self):
        original = copy.deepcopy(self.payload)
        for edit in (
            lambda p: p.update(schema="unrecognized-v1"),
            lambda p: p["units"][0].update(finding_id="0039-P1"),
            lambda p: p["units"].__setitem__(1, copy.deepcopy(p["units"][0])),
            lambda p: p["units"][0]["locations"]["msa"].update(path="source/locale/ar/../wrong.tex"),
            lambda p: p["units"][0].update(printed_page=52),
            lambda p: p.update(published_pdf_verified=True),
        ):
            edit(self.payload)
            with self.assertRaises(ValueError):
                self.load()
            self.payload = copy.deepcopy(original)
        self.write_ledger()
        with self.assertRaisesRegex(ValueError, "unexpected/duplicate dated propagation decision ID"):
            INDEX.load_decisions(self.repo, [self.path, self.path], self.units, self.english)

    def test_manifest_validation_rejects_malformed_inventory_and_selected_paths(self):
        # Testing the schema layer under an explicitly patched test-only digest
        # does not weaken production's fixed immutable SHA-256 contract.
        for edit in (
            lambda m: m.update(schema="wrong-v1"),
            lambda m: m["units"].pop(),
            lambda m: m["units"].__setitem__(33, copy.deepcopy(m["units"][32])),
            lambda m: m["units"][32].update(source_path="content/../outside.tex"),
            lambda m: m["units"][32]["msa"].update(path="source/locale/ar/foreign.tex"),
            lambda m: m["units"][32]["classical"].update(bytes=True),
        ):
            changed = copy.deepcopy(self.prior)
            edit(changed)
            raw = json.dumps(changed, ensure_ascii=False).encode("utf-8")
            self.prior_path.write_bytes(raw)
            with mock.patch.object(INDEX, "QUALIFICATION_PRIOR_MANIFEST_SHA256", INDEX.sha256_bytes(raw)):
                with self.assertRaises(ValueError):
                    self.load()

    def test_discovery_requires_the_commissioned_batch2_ledger(self):
        metadata = self.repo / "evidence/classical/SOURCE_RECONCILIATION_METADATA_20260905.json"
        metadata.write_text(json.dumps({"correction_metadata": [{"authority_refs": [LOGICAL + "#0033-P1"]}]}), encoding="utf-8")
        self.assertEqual(INDEX.discover_ledgers(self.repo), [self.path])
        self.path.unlink()
        with self.assertRaisesRegex(ValueError, "missing commissioned propagation ledger"):
            INDEX.discover_ledgers(self.repo)

    def test_human_index_csv_and_provenance_keep_0081_translation_scope_distinct(self):
        payload, hashes = INDEX.build_payload(self.repo, self.baseline_path, [self.path], self.english, [],
            "https://example.invalid/ar/blob/pinned/", "https://example.invalid/en/blob/pinned/")
        self.assertEqual(len(payload["decisions"]), 5)
        rows = list(csv.DictReader(io.StringIO(INDEX.render_occurrence_csv(payload))))
        self.assertEqual(len(rows), 5)
        for d in payload["decisions"]:
            self.assertTrue(d["index_metadata"]["human_index_included"])
            inherited = d["recorded_decision_id"] != "0081-P1"
            repair = d["semantic_propagation_repair"]
            self.assertEqual(repair["inherited_source_qualification"], inherited)
            self.assertEqual(repair["translation_scope_clarification"], not inherited)
            lines = []
            INDEX.append_assessment_provenance(lines, d, "../../")
            csv_row = next(r for r in rows if r[INDEX.CSV_COLUMNS[1]] == d["decision_id"])
            if inherited:
                self.assertIn("Inherited-source qualification", d["rationale"])
                self.assertIn("Inherited-source qualification", lines[1])
            else:
                self.assertIn("Translation-scope clarification", d["rationale"])
                self.assertIn("Translation-scope clarification", lines[1])
                self.assertNotIn("Inherited-source qualification", d["rationale"])
                self.assertNotIn("Inherited-source qualification", "\n".join(lines))
                self.assertNotIn("Inherited-source qualification", csv_row[INDEX.CSV_COLUMNS[5]])
                self.assertIn("English condition is retained", d["rationale"])
            self.assertEqual(csv_row[INDEX.CSV_COLUMNS[5]], INDEX.human_prose(INDEX.human_decision_field(d, "rationale")))
            self.assertIn(d["before_arabic"], csv_row[INDEX.CSV_COLUMNS[5]])
            self.assertEqual(csv_row[INDEX.CSV_COLUMNS[9]], "")
            self.assertEqual(csv_row[INDEX.CSV_COLUMNS[10]], "")
            for loc in d["index_metadata"]["occurrences"][0]["locations"]:
                self.assertTrue(loc["line_reconciliation"]["resolved"])
                self.assertTrue(loc["line_reconciliation"]["recorded_hash_matches_current"])
                self.assertFalse(loc["page_evidence"])
        INDEX.verify_inputs_unchanged(hashes)

    def test_canonical_live_batch2_read_only_admission(self):
        path = REPO / LOGICAL
        prior = REPO / INDEX.QUALIFICATION_PRIOR_MANIFEST_RELATIVE
        before = {p: p.read_bytes() for p in (path, prior)}
        decisions, _, hashes = INDEX.load_decisions(REPO, [path], self.units, ENGLISH)
        self.assertEqual({d["recorded_decision_id"] for d in decisions}, DECISION_IDS)
        for p, raw in before.items():
            self.assertEqual(p.read_bytes(), raw)
        INDEX.verify_inputs_unchanged(hashes)


if __name__ == "__main__":
    unittest.main()
