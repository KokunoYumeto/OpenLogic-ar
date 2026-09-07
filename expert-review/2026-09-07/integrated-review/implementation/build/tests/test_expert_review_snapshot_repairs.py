"""Independent readback tests: never import or execute the index generator.

Fixtures use the actual small canonical ledgers and declared source files. Only
temporary fixture copies are changed by negative probes; no source or PDF build.
"""
from __future__ import annotations

import copy
import csv
import html
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "validate_expert_review_snapshot.py"
MODULE = importlib.util.spec_from_file_location("independent_snapshot_readback", SCRIPT)
READBACK = importlib.util.module_from_spec(MODULE)
MODULE.loader.exec_module(READBACK)
REPO = SCRIPT.parent.parent
ENGLISH = REPO.parent.parent / "openlogic-interfarsi/repo/source/upstream"
PREFIX = "semantic-propagation-20260906:"
IDS = {PREFIX + item for item in ("0497-P1", "0079-P1", "0093-P1", "0005-P1", "0008-P1",
       "0016-P1", "0018-P1", "0033-P1", "0039-P1", "0039-P1-no-surjection-connective", "0072-P1", "0081-P1")}


def fixture_row(key, spec):
    """Build a literal output-format fixture directly from canonical evidence."""
    term, ledger = spec["terms"], spec["payload"]
    qualification = spec["qualification"]
    inherited = qualification and spec["unit_id"] != "OLP-0081"
    reason = ("New independent assessment dated 2026-09-06; not a reconstruction of "
              "the original translator's deliberation. ")
    if qualification:
        reason += ("Inherited-source qualification: this makes the mathematical qualification or logical scope explicit, "
                   "rather than claiming only a lexical mistranslation. " if inherited else
                   "Translation-scope clarification: the English condition is retained; this removes ambiguity in the "
                   "Arabic any-versus-none wording without claiming an error in the English source. ")
        reason += "Previous MSA wording: " + term["before_arabic"] + ". "
    reason += term["rationale"]
    row = {"decision_id": key, "recorded_decision_id": key[len(PREFIX):],
           "english_term": term["source_term"], "chosen_arabic": term["chosen_arabic"],
           "before_arabic": term["before_arabic"], "rationale": reason,
           "sense": term.get("sense", term.get("human_topic")),
           "expert_question": term["expert_review"]["question"], "expert_review_useful": True,
           "expert_review_non_blocking": True, "open_to_correction": True, "official_attestation_claimed": False,
           "status": ledger["status"], "recording_mode": ledger["recording_mode"], "assessed_on": ledger["assessed_on"],
           "printed_page": None, "page_status": "bind-after-final-reader-build",
           "alternatives": [{**alt, "status": alt["disposition"]} for alt in term.get("alternatives", [])],
           "source_record": copy.deepcopy(spec["identity"])}
    row["expert_review_reason"] = row["sense"]
    row["basis"] = ("authoritative-dated-inherited-source-qualification-repair" if inherited else
                    "authoritative-dated-translation-scope-clarification-repair" if qualification else
                    "authoritative-dated-semantic-propagation-repair")
    repair = {"ledger_path": spec["identity"]["path"], "ledger_sha256": spec["identity"]["sha256"],
              "finding_id": spec["finding_id"], "assessed_on": ledger["assessed_on"],
              "historical_before_source": copy.deepcopy(spec["historical"]), "source_ledger": copy.deepcopy(ledger)}
    if qualification:
        row["classical_arabic"] = term["classical_arabic"]
        repair.update(classification=spec["classification"], inherited_source_qualification=inherited,
                      translation_scope_clarification=not inherited)
    if "choice" in spec:
        repair.update(choice_id=term["choice_id"], parent_finding_id=spec["finding_id"],
                      choice_record=copy.deepcopy(term),
                      proof_scope="Exact subchoice within the complete unit repair; its patch is not applied twice.")
    if spec.get("witness_refreshes"):
        repair["current_witness_companions"] = [
            {"path": item["path"], "sha256": item["sha256"].upper(), "bytes": item["bytes"],
             "source_ledger": item["source_companion"]}
            for item in spec["witness_refreshes"]
        ]
    row["semantic_propagation_repair"] = repair
    raw = {"unit_id": spec["unit_id"]}
    human = {"unit": {"unit_id": spec["unit_id"]}, "locations": []}
    for kind, witness in spec["witnesses"].items():
        start, end = witness["line_start"], witness["line_end"]
        raw[kind] = {"path": witness["path"], "sha256": witness["sha256"], "locators": [
            {"line_start": start, "line_end": end, "excerpt": witness["excerpt"]}]}
        human["locations"].append({"source_kind": kind, "logical_path": witness["path"],
            "current_sha256": witness["sha256"], "current_excerpt": witness["excerpt"], "page_evidence": [],
            "line_reconciliation": {"current_line_start": start, "current_line_end": end,
                                    "resolved": True, "recorded_hash_matches_current": True}})
    row["occurrences"] = [raw]
    row["index_metadata"] = {"human_index_included": True, "occurrences": [human]}
    return row


def fixture_surfaces(row, spec, link_prefix=""):
    quote = lambda text: html.escape(text, quote=False)
    body = (f'<a id="{row["recorded_decision_id"]}"></a>\n'
            f'- **ID / الرقم:** `{row["decision_id"]}`\n'
            f'- **Why this choice / سبب الاختيار:** {quote(row["rationale"])}\n'
            "- **New repair assessment / تقييم تصحيحي جديد:** 2026-09-06; not the original translator's deliberation. "
            f'Previous MSA wording / اللفظ السابق: <span dir="rtl">{quote(row["before_arabic"])}</span>. '
            f'[Evidence]({link_prefix}{spec["identity"]["path"]})\n')
    if spec["qualification"]:
        body += ("- **Translation-scope clarification / توضيح نطاق الترجمة:** English retained.\n"
                 if spec["unit_id"] == "OLP-0081" else
                 "- **Inherited-source qualification / تقييد عبارة الأصل:** Qualification made explicit.\n")
    body += f'- **Please double-check / يُرجى التحقق:** {quote(row["expert_question"])}\n'
    locators = []
    for location in row["index_metadata"]["occurrences"][0]["locations"]:
        rec = location["line_reconciliation"]
        start, end = rec["current_line_start"], rec["current_line_end"]
        suffix = "#L" + str(start) + ("-L" + str(end) if end != start else "")
        link = ("https://example.test/" if location["source_kind"] == "english" else link_prefix) + location["logical_path"] + suffix
        body += f'- [Source]({link})\n'
        locators.append(location["logical_path"] + ":L" + str(start) + ("–L" + str(end) if end != start else ""))
    values = ["priority", row["decision_id"], row["english_term"] + " — sense: " + row["sense"],
              row["chosen_arabic"], "alternatives", row["rationale"], "shared", spec["unit_id"],
              " | ".join(locators), "", "", "source-only", spec["unit_id"] + " — " + row["expert_question"]]
    return body, values


class IndependentRepairReadbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.specs, cls.ledgers, cls.inputs = READBACK.repair_expectations(REPO, ENGLISH)

    def setUp(self):
        self.key = PREFIX + "0081-P1"
        self.spec = self.specs[self.key]
        self.row = fixture_row(self.key, self.spec)

    def errors(self, row=None, spec=None):
        errors = []
        READBACK.validate_repair_record(row or self.row, spec or self.spec, errors)
        return errors

    def presentation(self, row=None, spec=None):
        row, spec = row or self.row, spec or self.spec
        body, values = fixture_surfaces(row, spec)
        return {name: READBACK.decision_sections(body) for name in
                ("complete", "priority", "complete-001", "priority-001")}, {row["decision_id"]: [values]}

    def presentation_errors(self, surfaces, csv_rows, row=None, spec=None):
        row, spec = row or self.row, spec or self.spec
        errors = []
        READBACK.validate_explanations(row["decision_id"], row["rationale"], row["expert_question"],
                                      surfaces, csv_rows, errors, spec,
                                      locations=row["index_metadata"]["occurrences"][0]["locations"])
        return errors

    def test_all_twelve_live_decisions_four_ledgers_and_sources(self):
        self.assertEqual(set(self.specs), IDS)
        self.assertEqual(len(self.ledgers), 4)
        # The current canonical input inventory includes the dated Classical
        # qualification-witness companion introduced by the prose refresh.
        # Both independently pinned reader token registries are also checked.
        self.assertEqual(len(self.inputs), 44)
        self.assertEqual(sum(len(s["witnesses"]) for s in self.specs.values()), 36)
        for key, spec in self.specs.items():
            with self.subTest(key=key):
                self.assertEqual(self.errors(fixture_row(key, spec), spec), [])

    def test_every_literal_field_comes_from_its_own_canonical_choice(self):
        for key, spec in self.specs.items():
            fields = READBACK.expected_repair_fields(spec)
            for output, original in (("english_term", "source_term"), ("chosen_arabic", "chosen_arabic"),
                                     ("before_arabic", "before_arabic")):
                self.assertEqual(fields[output], spec["terms"][original], key)
            self.assertTrue(fields["rationale"].endswith(spec["terms"]["rationale"]), key)
            self.assertEqual(fields["expert_question"], spec["terms"]["expert_review"]["question"], key)

    def test_all_full_human_surfaces_pass(self):
        for key, spec in self.specs.items():
            row = fixture_row(key, spec)
            self.assertEqual(self.presentation_errors(*self.presentation(row, spec), row, spec), [], key)

    def test_older_repairs_preserve_both_passage_and_exact_literal_line_locations(self):
        for key, spec in self.specs.items():
            row = fixture_row(key, spec)
            human = row["index_metadata"]["occurrences"][0]
            human["locations"] = []
            for kind, witness in spec["witnesses"].items():
                group = row["occurrences"][0][kind]
                group["locators"] = []
                for start, end in sorted(READBACK.literal_ranges(witness, kind)):
                    excerpt = READBACK.exact_excerpt(witness["data"], start, end)
                    group["locators"].append({"line_start": start, "line_end": end, "excerpt": excerpt})
                    human["locations"].append({"source_kind": kind, "logical_path": witness["path"],
                        "current_sha256": witness["sha256"], "current_excerpt": excerpt, "page_evidence": [],
                        "line_reconciliation": {"current_line_start": start, "current_line_end": end,
                                                "resolved": True, "recorded_hash_matches_current": True}})
            self.assertEqual(self.errors(row, spec), [], key)
            self.assertEqual(self.presentation_errors(*self.presentation(row, spec), row, spec), [], key)

    def test_0039_connective_is_a_separate_literal_choice(self):
        spec = self.specs[PREFIX + "0039-P1-no-surjection-connective"]
        self.assertEqual(spec["terms"]["source_term"], "that is")
        self.assertEqual(spec["terms"]["chosen_arabic"], "بل لا توجد دالة")
        self.assertEqual(spec["witnesses"]["english"]["line_start"], 28)
        self.assertEqual(spec["witnesses"]["msa"]["line_start"], 27)
        self.assertEqual(spec["witnesses"]["classical"]["line_start"], 21)
        self.assertEqual(spec["historical"], self.specs[PREFIX + "0039-P1"]["historical"])

    def test_0081_is_not_an_inherited_english_fault(self):
        self.assertTrue(self.spec["classification"].startswith("translation-"))
        repair = self.row["semantic_propagation_repair"]
        repair["inherited_source_qualification"] = True
        repair["translation_scope_clarification"] = False
        self.assertTrue(any("classification mismatch" in e for e in self.errors()))

    def test_rejects_every_altered_literal_or_explanation_field(self):
        for field in ("english_term", "chosen_arabic", "before_arabic", "classical_arabic",
                      "sense", "rationale", "expert_question", "basis", "recording_mode"):
            with self.subTest(field=field):
                row = copy.deepcopy(self.row)
                row[field] = "invented or truncated"
                self.assertTrue(any("field mismatch: " + field in e for e in self.errors(row)))

    def test_rejects_official_attestation_and_original_deliberation_claims(self):
        for field, value in (("official_attestation_claimed", True), ("open_to_correction", False),
                             ("recording_mode", "original-translator-deliberation")):
            row = copy.deepcopy(self.row)
            row[field] = value
            self.assertTrue(self.errors(row), field)

    def test_full_ledger_provenance_cannot_be_truncated(self):
        del self.row["semantic_propagation_repair"]["source_ledger"]["units"][0]["rationale"]
        self.assertTrue(any("complete canonical repair provenance" in e for e in self.errors()))

    def test_ledger_identity_must_match_actual_bytes(self):
        self.row["source_record"]["sha256"] = "0" * 64
        self.assertTrue(any("source ledger identity mismatch" in e for e in self.errors()))

    def test_inverse_proved_history_cannot_be_replaced(self):
        for field in ("sha256", "bytes", "text_utf8", "patches", "identity_basis"):
            row = copy.deepcopy(self.row)
            row["semantic_propagation_repair"]["historical_before_source"][field] = "invented"
            self.assertTrue(any("historical before source mismatch: " + field in e for e in self.errors(row)))

    def test_connective_cannot_borrow_parent_question_or_phrase(self):
        key = PREFIX + "0039-P1-no-surjection-connective"
        spec = self.specs[key]
        row = fixture_row(key, spec)
        row["expert_question"] = self.specs[PREFIX + "0039-P1"]["terms"]["expert_review"]["question"]
        row["chosen_arabic"] = "يقتضي"
        self.assertGreaterEqual(len(self.errors(row, spec)), 2)

    def test_connective_cannot_lose_own_provenance(self):
        key = PREFIX + "0039-P1-no-surjection-connective"
        spec = self.specs[key]
        row = fixture_row(key, spec)
        del row["semantic_propagation_repair"]["choice_record"]
        self.assertTrue(any("separate connective provenance" in e for e in self.errors(row, spec)))

    def test_live_location_hash_and_excerpt_are_independent_checks(self):
        for field in ("current_sha256", "current_excerpt", "logical_path"):
            row = copy.deepcopy(self.row)
            row["index_metadata"]["occurrences"][0]["locations"][1][field] = "invented"
            self.assertTrue(any("human locator invalid" in e for e in self.errors(row)), field)

    def test_wrong_actual_phrase_line_cannot_pass_matching_file_hash(self):
        witness = self.spec["witnesses"]["msa"]
        start = witness["line_start"]
        group = self.row["occurrences"][0]["msa"]
        group["locators"] = [{"line_start": start, "line_end": start,
                              "excerpt": READBACK.exact_excerpt(witness["data"], start, start)}]
        self.assertTrue(any("active literal phrase absent" in e for e in self.errors()))

    def test_english_compound_is_not_the_selected_term(self):
        self.assertFalse(READBACK.active_phrase("nonenumerable", "enumerable", "english"))
        self.assertFalse(READBACK.active_phrase("non-enumerable", "enumerable", "english"))
        self.assertTrue(READBACK.active_phrase("enumerable set", "enumerable", "english"))

    def test_comment_only_and_ellipsis_phrases_are_rejected(self):
        self.assertFalse(READBACK.active_phrase("Text % modus ponens\n", "modus ponens", "english"))
        self.assertFalse(READBACK.active_phrase("modus ... ponens", "modus ponens", "english"))
        self.assertTrue(READBACK.active_phrase("modus\n ponens", "modus ponens", "english"))
        self.assertTrue(READBACK.active_phrase(r"\% modus ponens", "modus ponens", "english"))

    def test_arabic_clitics_allowed_but_words_not_invented(self):
        self.assertTrue(READBACK.active_phrase("وكل مجموعة غير خالية", "كل مجموعة غير خالية", "msa"))
        self.assertFalse(READBACK.active_phrase("كل مجموعة ... غير خالية", "كل مجموعة غير خالية", "msa"))

    def test_raw_and_human_occurrences_must_both_cover_three_languages(self):
        self.row["index_metadata"]["occurrences"][0]["locations"].pop()
        self.assertTrue(any("locator coverage differs" in e for e in self.errors()))

    def test_source_only_repair_cannot_assert_a_pdf_page(self):
        self.row["printed_page"] = 14
        self.row["index_metadata"]["occurrences"][0]["locations"][0]["page_evidence"] = [{"printed_page": 14}]
        errors = self.errors()
        self.assertTrue(any("field mismatch: printed_page" in e for e in errors))
        self.assertTrue(any("unverified final PDF page" in e for e in errors))

    def test_each_md_surface_detects_its_own_truncated_reason_and_question(self):
        for name in ("complete", "priority", "complete-001", "priority-001"):
            for field in ("rationale", "expert_question"):
                with self.subTest(surface=name, field=field):
                    surfaces, rows = self.presentation()
                    surfaces[name][self.key][0] = surfaces[name][self.key][0].replace(html.escape(self.row[field], quote=False), "short")
                    self.assertTrue(any(name in e and "truncated" in e for e in self.presentation_errors(surfaces, rows)))

    def test_a_shared_reason_elsewhere_does_not_certify_missing_id(self):
        surfaces, rows = self.presentation()
        surfaces["complete"]["another-decision"] = surfaces["complete"].pop(self.key)
        self.assertTrue(any("missing decision section: complete" in e for e in self.presentation_errors(surfaces, rows)))

    def test_duplicate_bad_shard_is_not_hidden_by_good_shard(self):
        surfaces, rows = self.presentation()
        surfaces["complete-002"] = {self.key: ["truncated"]}
        self.assertTrue(any("complete-002" in e for e in self.presentation_errors(surfaces, rows)))

    def test_missing_complete_and_priority_shards_fail(self):
        surfaces, rows = self.presentation()
        del surfaces["complete-001"]
        del surfaces["priority-001"]
        self.assertEqual(sum("missing detailed shard" in e for e in self.presentation_errors(surfaces, rows)), 2)

    def test_csv_requires_full_reason_and_full_question(self):
        for column, label in ((5, "reason"), (12, "question")):
            surfaces, rows = self.presentation()
            rows[self.key][0][column] = "short"
            self.assertTrue(any("CSV" in e and label in e for e in self.presentation_errors(surfaces, rows)))

    def test_csv_requires_literal_word_and_no_invented_page(self):
        for column in (3, 9, 10):
            surfaces, rows = self.presentation()
            rows[self.key][0][column] = "17"
            self.assertTrue(self.presentation_errors(surfaces, rows), column)

    def test_exact_human_source_location_links_cannot_disappear(self):
        for name in ("complete", "priority", "complete-001", "priority-001"):
            surfaces, rows = self.presentation()
            surfaces[name][self.key][0] = surfaces[name][self.key][0].replace("#L20-L29", "#L20-L28")
            self.assertTrue(any("missing exact human source link" in e for e in self.presentation_errors(surfaces, rows)), name)

    def test_exact_csv_source_locators_cannot_disappear(self):
        surfaces, rows = self.presentation()
        rows[self.key][0][8] = "wrong-file.tex:L999"
        self.assertTrue(any("missing exact CSV source locator" in e for e in self.presentation_errors(surfaces, rows)))

    def test_reference_links_are_resolved_only_for_the_current_decision(self):
        body, _ = fixture_surfaces(self.row, self.spec)
        literal = "source/locale/ar/content/first-order-logic/sequent-calculus/soundness.tex#L20-L29"
        body = body.replace("[Source](" + literal + ")", "[Source][this-source]")
        body += "\n[this-source]: " + literal + "\n[unused]: source/elsewhere.tex#L999\n"
        section = READBACK.decision_sections(body)[self.key][0]
        self.assertIn(literal, section)
        self.assertNotIn("source/elsewhere.tex#L999", section)

    def test_0081_rendering_cannot_claim_inherited_source_error(self):
        surfaces, rows = self.presentation()
        surfaces["priority"][self.key][0] = surfaces["priority"][self.key][0].replace(
            "Translation-scope clarification", "Inherited-source qualification")
        self.assertTrue(any("wrong rendered scope classification" in e for e in self.presentation_errors(surfaces, rows)))

    def test_retained_raw_history_is_stable_across_a_new_assessment(self):
        old = {"english_term": "term", "chosen_arabic": "عربية", "rationale": "old reason", "sense": "old sense"}
        new = {**old, "rationale": "new dated reason", "sense": "new assessed sense",
               "expert_review_assessment": {"original_fields": {"rationale": "old reason", "sense": "old sense"}}}
        self.assertEqual(READBACK.history_fingerprint(old), READBACK.history_fingerprint(new))
        new["chosen_arabic"] = "invented"
        self.assertNotEqual(READBACK.history_fingerprint(old), READBACK.history_fingerprint(new))

    def test_ambiguous_inverse_or_forward_patch_is_rejected(self):
        for data, patches in ((b"after after", [{"before": "before", "after": "after"}]),
                              (b"after before", [{"before": "before", "after": "after"}])):
            with self.assertRaises(ValueError):
                READBACK.inverse_source(data, patches)

    def test_source_bytes_drift_and_comment_only_witness_rejected(self):
        witness = self.spec["witnesses"]["msa"]
        declaration = copy.deepcopy(self.spec["terms"]["locations"]["msa"])
        with self.assertRaisesRegex(ValueError, "source hash mismatch"):
            READBACK.declared_witness(witness["data"] + b"\n", declaration, witness["term"], "msa")
        data = ("% " + witness["term"] + "\n").encode("utf-8")
        declaration = {"path": "fixture.tex", "sha256": READBACK.byte_digest(data), "line_start": 1, "line_end": 1}
        with self.assertRaisesRegex(ValueError, "active literal phrase missing"):
            READBACK.declared_witness(data, declaration, witness["term"], "msa")

    def make_snapshot(self, temp):
        repo, english = Path(temp) / "repo", Path(temp) / "english"
        for source in map(Path, self.inputs):
            destination = ((english / source.relative_to(ENGLISH)) if source.is_relative_to(ENGLISH) else
                           (repo / source.relative_to(REPO)))
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source.read_bytes())
        snapshot, previous = repo / "tmp/snapshot", repo / "tmp/previous"
        snapshot.mkdir(parents=True)
        previous.mkdir(parents=True)
        (snapshot / "reviewer-index").mkdir()
        rows = [fixture_row(key, spec) for key, spec in self.specs.items()]
        old = {"decision_id": "retained-raw-decision", "english_term": "retained", "chosen_arabic": "قديم",
               "rationale": "Retained recorded motivation.", "index_metadata": {"human_index_included": False}}
        rows.append(old)
        self.write_index(snapshot, rows)
        self.write_index(previous, [old])
        body, shard_body, csv_values = [], [], []
        for row in rows[:-1]:
            spec = self.specs[row["decision_id"]]
            section, values = fixture_surfaces(row, spec, "../../")
            body.append(section)
            shard_body.append(fixture_surfaces(row, spec, "../../../")[0])
            csv_values.append(values)
        for name in ("EXPERT_REVIEW_INDEX.md", "EXPERT_REVIEW_PRIORITY_ONLY.md"):
            (snapshot / name).write_text("\n".join(body), encoding="utf-8")
        for name in ("complete-001.md", "priority-001.md"):
            (snapshot / "reviewer-index" / name).write_text("\n".join(shard_body), encoding="utf-8")
        with (snapshot / "EXPERT_REVIEW_OCCURRENCES.csv").open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["Priority", "Decision ID", "Term", "Arabic", "Alternatives", "Short rationale",
                             "Edition", "Unit", "Source", "Component page", "PDF page", "Grade", "Please double-check"])
            writer.writerows(csv_values)
        return repo, english, snapshot, previous, rows

    @staticmethod
    def write_index(path, rows):
        (path / "EXPERT_REVIEW_INDEX.json").write_text(json.dumps(
            {"decisions": rows, "fixture": True}, ensure_ascii=False, indent=2), encoding="utf-8")

    def test_end_to_end_readback_without_generator(self):
        with tempfile.TemporaryDirectory(prefix="independent-repair-readback-") as temp:
            repo, english, snapshot, previous, _ = self.make_snapshot(temp)
            result = READBACK.check(repo, snapshot, previous, english, include_new_repairs=False)
            self.assertEqual(result["errors"], [])
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["counts"]["independently_verified_repair_assessments"], 12)
            self.assertEqual(result["counts"]["previous_raw_decisions_preserved"], 1)

    def test_end_to_end_detects_missing_connective_and_overwritten_history(self):
        with tempfile.TemporaryDirectory(prefix="independent-repair-readback-") as temp:
            repo, english, snapshot, previous, rows = self.make_snapshot(temp)
            rows = [row for row in rows if row["decision_id"] != PREFIX + "0039-P1-no-surjection-connective"]
            rows[-1]["rationale"] = "History silently replaced."
            self.write_index(snapshot, rows)
            result = READBACK.check(repo, snapshot, previous, english, include_new_repairs=False)
            self.assertEqual(result["status"], "FAIL")
            self.assertTrue(any("commissioned repair assessments missing" in e for e in result["errors"]))
            self.assertTrue(any("previous raw decision history overwritten" in e for e in result["errors"]))

    def test_end_to_end_detects_live_source_drift(self):
        with tempfile.TemporaryDirectory(prefix="independent-repair-readback-") as temp:
            repo, english, snapshot, previous, _ = self.make_snapshot(temp)
            source = repo / self.spec["witnesses"]["msa"]["path"]
            source.write_bytes(source.read_bytes() + b"\n")
            result = READBACK.check(repo, snapshot, previous, english, include_new_repairs=False)
            self.assertEqual(result["status"], "FAIL")
            self.assertTrue(any("source hash mismatch" in e for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
