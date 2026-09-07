"""Eight Sept-7 decisions: bounded producer/readback and adversarial fixtures.

Expectations originate in the three canonical ledgers and actual source bytes,
not in producer output. Only these decisions are normalized/reconciled/rendered
in memory. No full export, reader build, publication, or live file mutation.
"""
from __future__ import annotations

import copy
import csv
import hashlib
import html
import importlib.util
import io
import itertools
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
ENGLISH = ROOT.parent.parent / "openlogic-interfarsi/repo/source/upstream"
PREFIX = "semantic-propagation-20260907:"
COUNTS = {
    "AR-OLP-0375-ZERO-EXPONENT-20260907": 6,
    "AR-OLP-0375-PAIR-METHOD-20260907": 2,
    "AR-OLP-0376-TRUNCATED-SUBTRACTION-20260907": 2,
    "AR-OLP-0021-TWO-ROOTS-NOTE-20260907": 1,
    "AR-OLP-0321-FUNCTION-RELATION-20260907": 1,
    "AR-OLP-0326-COMPLEMENT-FIRST-ORDER-20260907": 2,
    "AR-OLP-0326-COMPLEMENT-SECOND-ORDER-20260907": 1,
    "AR-OLP-0368-CONDITIONAL-NORMAL-FORM-UNIQUENESS-20260907": 1,
}
PINNED = {
    "evidence/classical/repairs/OLP0375_0376_ARITHMETIC_SCOPE_20260907.json":
        "042822d86510960c3ae3fc9600ddf273f015bc00adc09e19c240a7071d265ff5",
    "evidence/classical/repairs/OLP0021_TWO_ROOTS_NOTE_20260907.json":
        "98b939cba500c9cbe8e591917709940ca0f685c61a0a4965535864e9aefd7120",
    "evidence/classical/repairs/OLP0321_0326_0368_SEMANTIC_SCOPE_20260907.json":
        "3cff7ba6901f09815be1ea4f42b2a29074639079fc21b09ae8cb4e6096e899da",
}


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value


ADD = load("consolidated_additional_fixture_helpers", "build/tests/test_expert_review_additional_repairs.py")
V = ADD.V
G = load("consolidated_producer_under_test", "build/generate_expert_review_index.py")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def fixture(key, spec):
    return ADD.fixture(key, spec)


def surface_fixture(row, spec):
    surfaces, csv_rows = ADD.readable_surfaces(dict(row, review_display={
        key: row[key] for key in ("english_term", "chosen_arabic", "before_arabic", "rationale", "expert_question")}), spec)
    for sections in surfaces.values():
        body = sections[row["decision_id"]][0].replace(
            "2026-09-06; not the original", "2026-09-07; not the original")
        for passage in row["literal_source_passages"]:
            body += "\n- **Literal source passage / اللفظ في موضعه:** " + " | ".join(
                phase + ": " + html.escape(passage[phase]["literal"], quote=False).replace("\n", " ")
                for phase in ("english", "before", "after"))
            if passage.get("before_role"):
                body += " | " + passage["before_role"]
        sections[row["decision_id"]][0] = body
    return surfaces, csv_rows


def record_errors(row, spec):
    errors = []
    V.validate_repair_record(row, spec, errors)
    return errors


def surface_errors(row, spec, surfaces, rows):
    errors = []
    display = row.get("review_display", row)
    V.validate_explanations(row["decision_id"], display["rationale"], display["expert_question"],
        surfaces, rows, errors, spec,
        locations=[loc for occ in row["index_metadata"]["occurrences"] for loc in occ["locations"]])
    return errors


def reconcile_generated(record, baseline):
    """Run actual bounded source reconciliation and display, with no readers."""
    row = copy.deepcopy(record)
    registries = G.load_review_token_registries(ROOT)
    G.attach_review_display(row, registries)
    cache, normalized = G.SourceCache(), []
    for number, occurrence in enumerate(row["occurrences"], 1):
        uid = occurrence["unit_id"]
        unit = G.derive_unit_meta(ROOT, baseline[uid], registries["english"])
        locations = []
        for raw in G.normalize_occurrence_sources(occurrence):
            loc = G.reconcile_location(raw, ROOT, ENGLISH, cache,
                "https://example.test/ar", "https://example.test/en")
            G.invalidate_broad_excerpt_without_recorded_term(loc, row)
            loc = G.recover_location_by_exact_search(loc, row, occurrence, cache,
                "https://example.test/ar", "https://example.test/en")
            locations.append(loc)
        G.recover_by_cross_language_exact_structure(locations, cache,
            "https://example.test/ar", "https://example.test/en")
        G.recover_unique_monotone_sequences(locations, cache,
            "https://example.test/ar", "https://example.test/en")
        for loc in locations:
            G.apply_location_quality_guards(loc, row, unit)
            loc["page_evidence"] = []
        kinds = {loc["source_kind"] for loc in locations}
        normalized.append({"occurrence_index": number, "unit": {
            "unit_id": uid, "title": unit.title, "source_role": unit.source_role,
            "target_path": unit.target_path, "aux_label": unit.aux_label},
            "context_note": occurrence.get("context_note"), "raw_occurrence": occurrence,
            "locations": locations, "human_review_included": True,
            "machine_location_count": len(locations), "human_review_location_count": len(locations),
            "language_coverage": {"recorded_source_kinds": sorted(kinds),
                "not_recorded_source_kinds": sorted({"english", "msa", "classical"} - kinds)}})
    G.suppress_duplicate_locator_stubs(normalized)
    G.suppress_repeated_human_locations(normalized)
    row["index_metadata"] = {"human_index_included": True, "occurrences": normalized}
    G.refresh_decision_index_counts(row)
    return row


class ConsolidatedRepairContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.specs, cls.ledgers, cls.inputs = V.consolidated_repair_expectations(ROOT, ENGLISH)
        cls.baseline = {r["id"]: r for r in json.loads((ROOT / "evidence/classical/BASELINE.json").read_text(encoding="utf-8"))["units"]}
        cls.generated = {}
        for identity in cls.ledgers:
            logical = identity["path"]
            payload = json.loads((ROOT / logical).read_text(encoding="utf-8"))
            rows, _ = G.normalize_consolidated_repairs(payload, copy.deepcopy(identity), ROOT, cls.baseline, ENGLISH)
            cls.generated.update((r["decision_id"], r) for r in rows)

    def test_exact_eight_choices_three_ledgers_sixteen_groups(self):
        self.assertEqual(set(self.specs), {PREFIX + key for key in COUNTS})
        self.assertEqual(set(self.generated), set(self.specs))
        self.assertEqual(len(self.ledgers), 3)
        self.assertEqual(sum(len(s["occurrence_specs"]) for s in self.specs.values()), 16)
        for key, count in COUNTS.items():
            self.assertEqual(len(self.specs[PREFIX + key]["occurrence_specs"]), count)
            self.assertEqual(len(self.generated[PREFIX + key]["occurrences"]), count)
        for logical, expected in PINNED.items():
            self.assertEqual(digest((ROOT / logical).read_bytes()), expected)
        for identity in self.ledgers:
            self.assertEqual(identity["sha256"].lower(), digest((ROOT / identity["path"]).read_bytes()))
            self.assertEqual(V.CONSOLIDATED_LEDGERS[identity["path"]][0].lower(), identity["sha256"].lower())
            self.assertEqual(G.CONSOLIDATED_REPAIR_LEDGERS[identity["path"]][0].lower(), identity["sha256"].lower())

    def test_every_independent_fixture_and_all_human_surfaces_pass(self):
        for key, spec in self.specs.items():
            with self.subTest(key=key):
                row = fixture(key, spec)
                self.assertEqual(record_errors(row, spec), [])
                self.assertEqual(surface_errors(row, spec, *surface_fixture(row, spec)), [])

    def test_actual_producer_records_and_reconciliation_pass_independent_readback(self):
        for key, generated in self.generated.items():
            with self.subTest(key=key):
                row = reconcile_generated(generated, self.baseline)
                self.assertEqual(record_errors(row, self.specs[key]), [])
                # Suppression must not lose one side of a canonical pair.
                for occ in row["index_metadata"]["occurrences"]:
                    self.assertTrue(occ["human_review_included"])
                    self.assertTrue(all(loc["human_review_included"] for loc in occ["locations"]))

    def test_actual_producer_provenance_and_csv_pass_independent_readback(self):
        for key, generated in self.generated.items():
            with self.subTest(key=key):
                row = reconcile_generated(generated, self.baseline)
                spec = self.specs[key]
                surfaces, _ = surface_fixture(row, spec)
                lines = []
                G.append_assessment_provenance(lines, row, "")
                for sections in surfaces.values():
                    text = sections[key][0]
                    text = "\n".join(line for line in text.splitlines() if
                        "**New repair assessment / تقييم تصحيحي جديد:**" not in line and
                        "**Literal source passage / اللفظ في موضعه:**" not in line)
                    sections[key][0] = text + "\n" + "\n".join(lines)
                values = list(csv.reader(io.StringIO(G.render_occurrence_csv({"decisions": [row]}))))[1:]
                self.assertEqual(len(values), COUNTS[key[len(PREFIX):]])
                self.assertEqual(surface_errors(row, spec, surfaces, {key: values}), [])
                self.assertTrue(all(not values[i][9] and not values[i][10] for i in range(len(values))))

    def test_reasons_choices_and_full_prior_sources_are_exact_canonical_records(self):
        for key, spec in self.specs.items():
            choice = spec["canonical_choice"]
            self.assertEqual(spec["expected_fields"]["rationale"], choice["rationale"])
            self.assertEqual(spec["expected_fields"]["chosen_arabic"], choice["chosen_arabic"])
            self.assertEqual(spec["expected_fields"]["expert_question"], choice["expert_question"])
            for history in spec["historical"]["sources"]:
                before = history["text_utf8"].encode()
                self.assertEqual((digest(before), len(before)), (history["sha256"].lower(), history["bytes"]))
                replay = before
                for item in history["patches"]:
                    old, new = item["before"].encode(), item["after"].encode()
                    self.assertEqual(replay.count(old), 1)
                    replay = replay.replace(old, new, 1)
                self.assertEqual(replay, (ROOT / history["path"]).read_bytes())

    def test_every_literal_group_binds_exact_english_before_and_after_bytes(self):
        for key, spec in self.specs.items():
            histories = {r["path"]: r["text_utf8"].encode() for r in spec["historical"]["sources"]}
            passages = spec["expected_fields"]["literal_source_passages"]
            self.assertEqual(len(passages), COUNTS[key[len(PREFIX):]])
            for passage, canonical in zip(passages, spec["canonical_choice"]["literal_review_occurrences"]):
                for phase in ("english", "before", "after"):
                    witness = passage[phase]
                    self.assertEqual(witness["literal"], canonical[phase]["literal"])
                    if phase == "before":
                        data = histories[witness["path"]]
                    else:
                        data = ((ENGLISH if phase == "english" else ROOT) / witness["path"]).read_bytes()
                    selected = "\n".join(data.decode().splitlines()[witness["line_start"]-1:witness["line_end"]])
                    self.assertEqual(selected, witness["excerpt"])
                    self.assertEqual(digest(data), witness["sha256"].lower())
                    self.assertEqual(digest(selected.encode()), witness["excerpt_sha256"].lower())
                    self.assertIn(" ".join(witness["literal"].split()), " ".join(selected.split()))

    def test_changed_canonical_fields_hash_and_prior_provenance_are_rejected(self):
        for key, spec in self.specs.items():
            for field in ("rationale", "expert_question", "chosen_arabic", "before_arabic", "english_term", "sense"):
                row = fixture(key, spec)
                row[field] = "borrowed or invented"
                self.assertTrue(record_errors(row, spec), (key, field))
            for field in ("historical_before_source", "choice_record", "source_ledger"):
                row = fixture(key, spec)
                row["semantic_propagation_repair"][field] = {}
                self.assertTrue(record_errors(row, spec), (key, field))
            row = fixture(key, spec)
            row["source_record"]["sha256"] = "0" * 64
            self.assertTrue(record_errors(row, spec), key)

    def test_wrong_date_namespace_and_recorded_id_are_rejected(self):
        for key, spec in self.specs.items():
            for field, value in (("decision_id", key.replace("20260907:", "20260906:")),
                                 ("recorded_decision_id", "invented"), ("assessed_on", "2026-09-06")):
                row = fixture(key, spec)
                row[field] = value
                self.assertTrue(record_errors(row, spec), (key, field))

    def test_literal_source_passage_record_cannot_lose_or_forge_any_phase(self):
        for key, spec in self.specs.items():
            for phase in ("english", "before", "after"):
                for field in ("sha256", "excerpt_sha256", "literal", "path", "line_start"):
                    row = fixture(key, spec)
                    row["literal_source_passages"][0][phase][field] = "invented"
                    self.assertTrue(record_errors(row, spec), (key, phase, field))
            row = fixture(key, spec)
            row["literal_source_passages"].pop()
            self.assertTrue(record_errors(row, spec), key)

    def test_missing_duplicate_and_forged_raw_human_occurrences_are_rejected(self):
        for key, spec in self.specs.items():
            for surface in ("raw", "human"):
                for mutation in ("missing", "duplicate", "forged"):
                    row = fixture(key, spec)
                    groups = row["occurrences"] if surface == "raw" else row["index_metadata"]["occurrences"]
                    if mutation == "missing":
                        groups.pop()
                    elif mutation == "duplicate":
                        groups.append(copy.deepcopy(groups[0]))
                    elif surface == "raw":
                        groups[0]["english"]["locators"][0]["line_start"] = 999
                    else:
                        groups[0]["locations"][0]["line_reconciliation"]["current_line_start"] = 999
                    self.assertTrue(record_errors(row, spec), (key, surface, mutation))

    def test_cross_paired_raw_and_human_groups_fail_even_if_all_locations_remain(self):
        key = PREFIX + "AR-OLP-0375-ZERO-EXPONENT-20260907"
        spec = self.specs[key]
        pristine = fixture(key, spec)
        for surface in ("raw", "human", "both"):
            detected = False
            for left, right in itertools.combinations(range(len(pristine["occurrences"])), 2):
                row = copy.deepcopy(pristine)
                if surface in {"raw", "both"}:
                    groups = row["occurrences"]
                    groups[left]["english"], groups[right]["english"] = groups[right]["english"], groups[left]["english"]
                if surface in {"human", "both"}:
                    groups = row["index_metadata"]["occurrences"]
                    a = next(i for i, loc in enumerate(groups[left]["locations"]) if loc["source_kind"] == "english")
                    b = next(i for i, loc in enumerate(groups[right]["locations"]) if loc["source_kind"] == "english")
                    groups[left]["locations"][a], groups[right]["locations"][b] = groups[right]["locations"][b], groups[left]["locations"][a]
                if record_errors(row, spec):
                    detected = True
                    break
            self.assertTrue(detected, surface)

    def test_independent_group_reordering_is_not_an_error(self):
        for key, spec in self.specs.items():
            row = fixture(key, spec)
            row["occurrences"].reverse()
            row["index_metadata"]["occurrences"] = row["index_metadata"]["occurrences"][1:] + row["index_metadata"]["occurrences"][:1]
            self.assertEqual(record_errors(row, spec), [], key)
            surfaces, rows = surface_fixture(row, spec)
            rows[key].reverse()
            self.assertEqual(surface_errors(row, spec, surfaces, rows), [], key)

    def test_csv_missing_duplicate_merged_and_forged_groups_are_rejected(self):
        for key, spec in self.specs.items():
            row = fixture(key, spec)
            for mutation in ("missing", "duplicate", "merge", "forged"):
                surfaces, rows = surface_fixture(row, spec)
                if mutation == "missing":
                    rows[key].pop()
                elif mutation == "duplicate":
                    rows[key].append(copy.deepcopy(rows[key][0]))
                elif mutation == "merge":
                    if len(rows[key]) < 2:
                        continue
                    rows[key][0][8] += " | " + rows[key][1][8]
                    rows[key].pop(1)
                else:
                    rows[key][0][8] += " | forged.tex:L999"
                self.assertTrue(surface_errors(row, spec, surfaces, rows), (key, mutation))

    def test_csv_cross_pairing_is_rejected_without_losing_any_locator(self):
        key = PREFIX + "AR-OLP-0375-ZERO-EXPONENT-20260907"
        spec, row = self.specs[key], fixture(key, self.specs[key])
        detected = False
        for left, right in itertools.combinations(range(6), 2):
            surfaces, rows = surface_fixture(row, spec)
            a, b = rows[key][left][8].split(" | "), rows[key][right][8].split(" | ")
            a[0], b[0] = b[0], a[0]
            rows[key][left][8], rows[key][right][8] = " | ".join(a), " | ".join(b)
            if surface_errors(row, spec, surfaces, rows):
                detected = True
                break
        self.assertTrue(detected)

    def test_human_surfaces_cannot_omit_or_alter_literal_groups(self):
        for key, spec in self.specs.items():
            row = fixture(key, spec)
            for surface in ("complete", "priority", "complete-001", "priority-001"):
                for phase in ("english", "before", "after"):
                    surfaces, rows = surface_fixture(row, spec)
                    text = surfaces[surface][key][0]
                    lines = text.splitlines()
                    index = next(i for i, line in enumerate(lines) if "**Literal source passage" in line)
                    literal = html.escape(row["literal_source_passages"][0][phase]["literal"], quote=False).replace("\n", " ")
                    lines[index] = lines[index].replace(literal, "invented passage")
                    surfaces[surface][key][0] = "\n".join(lines)
                    self.assertTrue(surface_errors(row, spec, surfaces, rows), (key, surface, phase))

    def test_final_page_claims_in_raw_human_or_csv_are_rejected(self):
        for key, spec in self.specs.items():
            row = fixture(key, spec)
            row["printed_page"] = 12
            row["index_metadata"]["occurrences"][0]["locations"][0]["page_evidence"] = [{"printed_page": 12}]
            errors = record_errors(row, spec)
            self.assertTrue(any("printed_page" in e for e in errors))
            self.assertTrue(any("unverified final PDF page" in e for e in errors))
            for column in (9, 10):
                row = fixture(key, spec)
                surfaces, rows = surface_fixture(row, spec)
                rows[key][0][column] = "12"
                self.assertTrue(surface_errors(row, spec, surfaces, rows), (key, column))

    def test_full_reasons_questions_dates_and_source_links_are_required(self):
        for key, spec in self.specs.items():
            row = fixture(key, spec)
            for surface in ("complete", "priority", "complete-001", "priority-001"):
                for field in ("rationale", "expert_question", "date", "source_link"):
                    surfaces, rows = surface_fixture(row, spec)
                    old = ("2026-09-07; not the original" if field == "date" else "#L" if field == "source_link"
                           else html.escape(row[field], quote=False))
                    surfaces[surface][key][0] = surfaces[surface][key][0].replace(old, "removed")
                    self.assertTrue(surface_errors(row, spec, surfaces, rows), (key, surface, field))
            for column in (5, 12):
                surfaces, rows = surface_fixture(row, spec)
                for values in rows[key]:
                    values[column] = "removed"
                self.assertTrue(surface_errors(row, spec, surfaces, rows), (key, column))

    def test_independent_admission_rejects_changed_ledger_bytes(self):
        original = V.bounded_bytes
        target = ROOT / self.ledgers[0]["path"]

        def changed(path, *args, **kwargs):
            raw = original(path, *args, **kwargs)
            return raw + b" " if path == target else raw

        with patch.object(V, "bounded_bytes", side_effect=changed):
            with self.assertRaisesRegex(ValueError, "unapproved consolidated ledger identity"):
                V.consolidated_repair_expectations(ROOT, ENGLISH)

    def test_producer_rejects_changed_identity_or_self_consistent_payload_mutation(self):
        for identity in self.ledgers:
            payload = json.loads((ROOT / identity["path"]).read_text(encoding="utf-8"))
            wrong_id = dict(identity, sha256="0" * 64)
            with self.assertRaises(ValueError):
                G.normalize_consolidated_repairs(payload, wrong_id, ROOT, self.baseline, ENGLISH)
            changed = copy.deepcopy(payload)
            changed["assessed_on"] = "2026-09-06"
            with self.assertRaises(ValueError):
                G.normalize_consolidated_repairs(changed, copy.deepcopy(identity), ROOT, self.baseline, ENGLISH)


if __name__ == "__main__":
    unittest.main()
