"""Independent rendered-explanation readback, bounded to 23 cardinality choices.

The real producer renders only this finite batch in memory. Expected rationale
and question fields come from the validator's independently pinned raw ledgers,
not the producer's already rendered fields. No full export or source writes.
"""
from __future__ import annotations

import copy
import csv
import io
from pathlib import Path
import unittest
from unittest.mock import patch

from build import cardinality_repair_batch_20260908 as C
from build import generate_expert_review_index as G
from build import validate_expert_review_snapshot as V
from build.tests import test_expert_review_cardinality_batch as P
from build.tests import test_expert_review_qualification_batch2 as Q


KEY = V.CONSOLIDATED_PREFIX + "AR-OLP-0031-MSA-COFINITE-SOURCE-NOTE-20260907"
WHY = "**Why this choice / سبب الاختيار:**"
QUESTION = "**PLEASE DOUBLE-CHECK THIS CHOICE / يُرجى التحقق من هذا الاختيار:**"


class ExplanationDisplayReadback(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        P.CardinalityReviewGenerator.setUpClass()
        producer = P.CardinalityReviewGenerator
        cls.rows = {r["decision_id"]: r for r in producer.current}
        cls.specs, _, _ = V.cardinality_repair_expectations(C.REPO, C.ENGLISH)
        payload = {"decisions": producer.rows, "reader_evidence": []}
        full = G.render_decision_shard(payload, producer.current, "full", 1, 1, None, None, "")
        priority_rows = [r for r in producer.current if r["expert_review_useful"]]
        priority = G.render_decision_shard(payload, priority_rows, "priority", 1, 1, None, None, "")
        cls.surfaces = {"complete": V.decision_sections(full), "complete-001": V.decision_sections(full),
                        "priority": V.decision_sections(priority), "priority-001": V.decision_sections(priority)}
        cls.csv_rows = {}
        values = list(csv.reader(io.StringIO(G.render_occurrence_csv(payload))))
        for row in values[1:]:
            cls.csv_rows.setdefault(row[1], []).append(row)

    def errors_for(self, key, *, spec=None, surfaces=None, csv_rows=None):
        spec = self.specs[key] if spec is None else spec
        fields = spec["expected_fields"]
        errors = []
        V.validate_explanations(key, fields["rationale"], fields["expert_question"],
            self.surfaces if surfaces is None else surfaces,
            self.csv_rows if csv_rows is None else csv_rows, errors, spec,
            flagged=fields["expert_review_useful"], locations=[
                loc for occurrence in self.rows[key]["index_metadata"]["occurrences"]
                for loc in occurrence["locations"]])
        return errors

    def replace_line(self, section, label, transform):
        lines = section.splitlines()
        matches = [i for i, line in enumerate(lines) if label in line]
        self.assertEqual(len(matches), 1)
        index = matches[0]
        changed = transform(lines[index])
        self.assertNotEqual(changed, lines[index])
        lines[index] = changed
        return "\n".join(lines)

    def test_actual_raw_expected_explanations_pass_all_23_rendered_choices(self):
        self.assertEqual(set(self.rows), set(self.specs))
        self.assertEqual(len(self.rows), 23)
        self.assertEqual(sum(len(rows) for rows in self.csv_rows.values()), 25)
        for key in self.rows:
            self.assertEqual(self.errors_for(key), [], key)

    def test_raw_setminus_and_visible_operator_are_equivalent_not_identical(self):
        raw = self.specs[KEY]["expected_fields"]["rationale"]
        rendered = self.rows[KEY]["review_display"]["rationale"]
        self.assertNotEqual(raw, rendered)
        self.assertIn(r"A=Nat\setminus F", raw)
        self.assertIn("A=Nat∖ F", rendered)
        self.assertEqual(self.errors_for(KEY), [])

    def test_missing_or_changed_reason_operator_fails_each_markdown_surface(self):
        for surface in self.surfaces:
            for replacement in ("", "∪"):
                with self.subTest(surface=surface, replacement=replacement):
                    surfaces = copy.deepcopy(self.surfaces)
                    surfaces[surface][KEY][0] = self.replace_line(surfaces[surface][KEY][0], WHY,
                        lambda line: line.replace("∖", replacement))
                    self.assertIn(KEY + ": missing/truncated full reason: " + surface,
                                  self.errors_for(KEY, surfaces=surfaces))

    def test_missing_or_changed_reason_operator_fails_csv(self):
        for replacement in ("", "∪"):
            rows = copy.deepcopy(self.csv_rows)
            self.assertIn("∖", rows[KEY][0][5])
            rows[KEY][0][5] = rows[KEY][0][5].replace("∖", replacement)
            self.assertIn(KEY + ": missing/truncated full CSV reason",
                          self.errors_for(KEY, csv_rows=rows))

    def question_fixture(self, raw, rendered):
        # Synthetic question isolates notation equivalence without rewriting a
        # real ledger or attributing this test question to any translation.
        spec = copy.deepcopy(self.specs[KEY])
        spec["expected_fields"]["expert_question"] = raw
        surfaces = copy.deepcopy(self.surfaces)
        for sections in surfaces.values():
            sections[KEY][0] = self.replace_line(sections[KEY][0], QUESTION,
                lambda line: line.split(QUESTION, 1)[0] + QUESTION + " " + rendered)
        rows = copy.deepcopy(self.csv_rows)
        for row in rows[KEY]:
            row[12] = rendered
        return spec, surfaces, rows

    def test_canonical_composition_question_accepts_actual_equivalent_rendering(self):
        raw = r"Does \comp{f}{g} retain the required order?"
        rendered = G.render_cardinality_review_text(raw, P.CardinalityReviewGenerator.registries["english"])
        self.assertEqual(rendered, "Does (g ∘ f) retain the required order?")
        spec, surfaces, rows = self.question_fixture(raw, rendered)
        self.assertEqual(self.errors_for(KEY, spec=spec, surfaces=surfaces, csv_rows=rows), [])

    def test_lost_question_operator_and_reversed_operands_fail(self):
        raw = r"Does \comp{f}{g} retain the required order?"
        for rendered in ("Does (g f) retain the required order?", "Does (f ∘ g) retain the required order?"):
            spec, surfaces, rows = self.question_fixture(raw, rendered)
            errors = self.errors_for(KEY, spec=spec, surfaces=surfaces, csv_rows=rows)
            self.assertEqual(sum("full expert question:" in e for e in errors), 4)
            self.assertIn(KEY + ": missing/truncated full CSV expert question", errors)

    def test_unknown_question_operator_cannot_disappear_as_formatting(self):
        spec, surfaces, rows = self.question_fixture(r"Is A\unknownop B intended?", "Is A B intended?")
        errors = self.errors_for(KEY, spec=spec, surfaces=surfaces, csv_rows=rows)
        self.assertEqual(sum("full expert question:" in e for e in errors), 4)
        self.assertIn(KEY + ": missing/truncated full CSV expert question", errors)

    def test_archived_fixture_sources_match_exact_historical_declarations(self):
        sources = Q.archived_pre_cardinality_sources(C.REPO)
        self.assertEqual(set(sources), {"msa", "classical"})
        self.assertEqual({kind: (len(data), C.sha(data)) for kind, data in sources.items()}, {
            "msa": (12479, "82014f0a1361ae5462c5dd7d082e18a2e701dd23aa730a5550bd362ceb2b77e8"),
            "classical": (11568, "6aea9fd0baec506686a0c45153e8dfdf7d556f89878f9bd2ea9f90c7b4e8f3e9")})

    def test_changed_archive_or_transition_ledger_fails_closed(self):
        original = Path.read_bytes
        targets = [C.REPO / Q.CARDINALITY_LEDGER] + [
            C.REPO / (Q.CARDINALITY_HISTORY + "OLP-0033-" + kind + ".tex") for kind in ("msa", "classical")]
        for target in targets:
            def mutated(path):
                data = original(path)
                return data + b" " if path.resolve() == target.resolve() else data
            with patch.object(Path, "read_bytes", mutated), self.assertRaises(ValueError):
                Q.archived_pre_cardinality_sources(C.REPO)


if __name__ == "__main__":
    unittest.main()
