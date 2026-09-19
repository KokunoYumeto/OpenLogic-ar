from __future__ import annotations

import csv
import copy
import gzip
import importlib.util
import io
import json
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from urllib.parse import unquote


SCRIPT = Path(__file__).resolve().parents[1] / "generate_expert_review_index.py"
SPEC = importlib.util.spec_from_file_location("expert_review_index", SCRIPT)
assert SPEC and SPEC.loader
INDEX = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = INDEX
SPEC.loader.exec_module(INDEX)


class ExpertReviewIndexTests(unittest.TestCase):
    def test_repair_previous_wording_uses_arabic_registry_without_changing_raw_history(self) -> None:
        repo = SCRIPT.parent.parent
        registries = INDEX.load_review_token_registries(repo)
        raw = r"!!^a{tableau} مع ال!!{signed formula}s و!!{element}s: $A \in B$"
        decision = {"english_term": "matching pair", "chosen_arabic": "صيغتين موقّعتين",
                    "before_arabic": raw, "rationale": "Preserve syntax and history.",
                    "expert_question": "Check the dual.", "assessed_on": "2026-09-06",
                    "semantic_propagation_repair": {"ledger_path": "evidence/fixture.json", "changed_edition": "classical"}}
        original = copy.deepcopy(decision)
        INDEX.attach_review_display(decision, registries)
        display = decision["review_display"]
        self.assertEqual(display["before_arabic"], "جدول دلالي مع الصيغ موقّعة وعناصر: A ∈ B")
        self.assertEqual([item["display"] for item in display["registry_expansions"]["before_arabic"]],
                         ["جدول دلالي", "صيغ موقّعة", "عناصر"])
        self.assertTrue(display["raw_fields_preserved"])
        lines = []
        INDEX.append_assessment_provenance(lines, decision, "../../")
        self.assertIn(display["before_arabic"], "\n".join(lines))
        self.assertNotRegex("\n".join(lines), r"atableau|elements|signed formulas|!!")
        decision.pop("review_display")
        self.assertEqual(decision, original)

    def test_repair_math_display_keeps_membership_subset_union_and_difference_distinct(self) -> None:
        raw = r"$A \in B$; $A \subseteq \bigcup B$; $A \setminus B$"
        self.assertEqual(INDEX.humanize_tex(raw), "A ∈ B; A ⊆ ⋃ B; A ∖ B")
        repo = SCRIPT.parent.parent
        registries = INDEX.load_review_token_registries(repo)
        decision = {"english_term": raw, "chosen_arabic": raw, "before_arabic": raw}
        INDEX.attach_review_display(decision, registries)
        for field in ("english_term", "chosen_arabic", "before_arabic"):
            self.assertEqual(decision["review_display"][field], "A ∈ B; A ⊆ ⋃ B; A ∖ B")
            self.assertEqual(decision[field], raw)

    def _expert_binding_fixture(self, root: Path) -> tuple[Path, Path, list[dict], Path]:
        repo = root / "repo"
        english_root = root / "english"
        english = english_root / "content/unit.tex"
        msa = repo / "source/locale/ar/content/unit.tex"
        classical = repo / "source/locale/ar-classical/content/unit.tex"
        global_source = repo / "source/locale/ar/open-logic-locale.sty"
        for path in (english, msa, classical, global_source):
            path.parent.mkdir(parents=True, exist_ok=True)
        english.write_text("technical witness\n", encoding="utf-8")
        msa.write_text("شاهد اصطلاحي\n", encoding="utf-8")
        classical.write_text("شاهد بياني\n", encoding="utf-8")
        global_source.write_text("\\setlocalecaption{arabic}{key}{عنوان عام}\n", encoding="utf-8")
        units = [
            {
                "id": "OLP-0001",
                "source_path": "content/unit.tex",
                "arabic_path": "source/locale/ar/content/unit.tex",
                "target_path": "source/locale/ar-classical/content/unit.tex",
            }
        ]
        baseline = repo / "evidence/classical/BASELINE.json"
        baseline.parent.mkdir(parents=True, exist_ok=True)
        baseline.write_text(
            json.dumps({"units": units}, ensure_ascii=False), encoding="utf-8"
        )

        def declared(kind: str, path: Path, logical: str) -> dict:
            text = path.read_text(encoding="utf-8").splitlines()[0]
            return {
                "source_kind": kind,
                "path": logical,
                "line_ranges": [[1, 1]],
                "file_sha256": INDEX.sha256_file(path),
                "cited_text_sha256": INDEX.sha256_bytes(text.encode("utf-8")),
                "semantic_basis": "The exact line instantiates the declared sense.",
            }

        english_decl = declared("english", english, "content/unit.tex")
        global_decl = declared(
            "msa", global_source, "source/locale/ar/open-logic-locale.sty"
        )
        bindings = []
        decisions = []
        for number in range(1, 71):
            decision_id = f"locale-ar-chosen-test-{number:02d}"
            decisions.append(
                {
                    "decision_id": decision_id,
                    "english_term": "technical witness",
                    "chosen_arabic": "شاهد",
                    "occurrences": [],
                }
            )
            if number == 2:
                disposition = "global-source-only"
                occurrences = []
                globals_ = [copy.deepcopy(global_decl)]
                unresolved = []
            else:
                disposition = "partially-bound" if number == 1 else "bound"
                occurrences = [
                    {
                        "unit_id": "OLP-0001",
                        "locations": [copy.deepcopy(english_decl)],
                    }
                ]
                globals_ = []
                unresolved = ["potential component"] if number == 1 else []
            bindings.append(
                {
                    "decision_id": decision_id,
                    "selected_index": number,
                    "disposition": disposition,
                    "binding_note": "Exact test binding.",
                    "occurrences": occurrences,
                    "global_locations": globals_,
                    "unresolved_components": unresolved,
                }
            )
        binding_path = repo / INDEX.EXPERT_SOURCE_BINDINGS_RELATIVE
        binding_path.parent.mkdir(parents=True, exist_ok=True)
        binding_payload = {
            "schema": INDEX.EXPERT_SOURCE_BINDING_SCHEMA,
            "authority": {
                "witness_rule": INDEX.EXPERT_SOURCE_BINDING_WITNESS,
                "baseline": {
                    "bytes": baseline.stat().st_size,
                    "sha256": INDEX.sha256_file(baseline),
                },
            },
            "totals": {
                "bindings": 70,
                "bound": 68,
                "partially_bound": 1,
                "global_source_only": 1,
                "unit_occurrences": 69,
                "unit_source_locations": 69,
                "global_source_locations": 1,
                "unresolved_components": 1,
            },
            "bindings": bindings,
        }
        binding_path.write_text(
            json.dumps(binding_payload, ensure_ascii=False), encoding="utf-8"
        )
        return repo, baseline, decisions, english_root

    def test_expert_source_bindings_attach_exact_occurrences_and_partial_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, baseline, decisions, english_root = self._expert_binding_fixture(Path(tmp))
            baseline_data = json.loads(baseline.read_text(encoding="utf-8"))
            identity, path, digest = INDEX.apply_expert_source_bindings(
                repo, baseline, baseline_data["units"], decisions, english_root
            )
            self.assertEqual(identity["totals"]["bindings"], 70)
            self.assertEqual(path, repo / INDEX.EXPERT_SOURCE_BINDINGS_RELATIVE)
            self.assertEqual(digest, INDEX.sha256_file(path))
            self.assertEqual(decisions[0]["expert_source_binding"]["disposition"], "partially-bound")
            self.assertEqual(
                decisions[0]["expert_source_binding"]["unresolved_components"],
                ["potential component"],
            )
            locator = decisions[0]["occurrences"][0]["english"]["locators"][0]
            self.assertEqual(locator["witness"]["rule"], INDEX.EXPERT_SOURCE_BINDING_WITNESS)
            self.assertTrue(locator["witness"]["validated"])
            self.assertEqual(decisions[1]["occurrences"], [])
            self.assertEqual(len(decisions[1]["_expert_global_source_raw"]), 1)

    def test_expert_source_bindings_reject_wrong_file_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, baseline, decisions, english_root = self._expert_binding_fixture(Path(tmp))
            path = repo / INDEX.EXPERT_SOURCE_BINDINGS_RELATIVE
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["bindings"][0]["occurrences"][0]["locations"][0]["file_sha256"] = "0" * 64
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "file hash mismatch"):
                INDEX.apply_expert_source_bindings(
                    repo,
                    baseline,
                    json.loads(baseline.read_text(encoding="utf-8"))["units"],
                    decisions,
                    english_root,
                )

    def test_expert_source_bindings_reject_wrong_excerpt_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, baseline, decisions, english_root = self._expert_binding_fixture(Path(tmp))
            path = repo / INDEX.EXPERT_SOURCE_BINDINGS_RELATIVE
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["bindings"][0]["occurrences"][0]["locations"][0]["cited_text_sha256"] = "0" * 64
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "excerpt hash mismatch"):
                INDEX.apply_expert_source_bindings(
                    repo,
                    baseline,
                    json.loads(baseline.read_text(encoding="utf-8"))["units"],
                    decisions,
                    english_root,
                )

    def test_expert_source_bindings_reject_unit_path_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, baseline, decisions, english_root = self._expert_binding_fixture(Path(tmp))
            path = repo / INDEX.EXPERT_SOURCE_BINDINGS_RELATIVE
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["bindings"][0]["occurrences"][0]["locations"][0]["path"] = "content/other.tex"
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "path/unit mismatch"):
                INDEX.apply_expert_source_bindings(
                    repo,
                    baseline,
                    json.loads(baseline.read_text(encoding="utf-8"))["units"],
                    decisions,
                    english_root,
                )

    def test_expert_witness_is_the_only_broad_span_bypass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            path = repo / "broad.tex"
            lines = [f"semantic statement {number}" for number in range(1, 21)]
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")

            def reconciled(validated: bool) -> dict:
                row = INDEX.reconcile_location(
                    {
                        "source_kind": "english",
                        "path": "broad.tex",
                        "recorded_sha256": INDEX.sha256_file(path),
                        "line_start": 1,
                        "line_end": 10,
                        "excerpt": "\n".join(lines[:10]),
                        "witness": {
                            "rule": INDEX.EXPERT_SOURCE_BINDING_WITNESS,
                            "validated": validated,
                        },
                    },
                    repo,
                    repo,
                    INDEX.SourceCache(),
                    "https://example.test/repo",
                    "https://example.test/en",
                )
                INDEX.invalidate_broad_excerpt_without_recorded_term(
                    row, {"english_term": "absent headword", "chosen_arabic": "غائب"}
                )
                return row

            self.assertTrue(reconciled(True)["line_reconciliation"]["resolved"])
            rejected = reconciled(False)
            self.assertFalse(rejected["line_reconciliation"]["resolved"])
            self.assertEqual(
                rejected["line_reconciliation"]["status"],
                "unresolved-broad-span-excerpt-not-term-occurrence",
            )

    def test_global_source_only_renders_exact_without_unit_or_page_claim(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, baseline, decisions, english_root = self._expert_binding_fixture(Path(tmp))
            units = json.loads(baseline.read_text(encoding="utf-8"))["units"]
            INDEX.apply_expert_source_bindings(repo, baseline, units, decisions, english_root)
            decision = decisions[1]
            normalized = []
            for raw in decision.pop("_expert_global_source_raw"):
                location = INDEX.reconcile_location(
                    raw,
                    repo,
                    english_root,
                    INDEX.SourceCache(),
                    "https://example.test/repo",
                    "https://example.test/en",
                )
                location["human_review_included"] = True
                location["page_evidence"] = []
                normalized.append(location)
            decision.update(
                edition="shared Arabic locale terminology ledger",
                sense="global front matter",
                rationale="An exact locale caption is used.",
                alternatives=[],
                expert_review_useful=True,
                global_source_bindings=normalized,
                index_metadata={
                    "human_index_included": True,
                    "occurrences": [],
                    "occurrence_group_count": 0,
                },
            )
            payload = {"decisions": [decision]}
            csv_text = INDEX.render_occurrence_csv(payload)
            row = list(csv.DictReader(io.StringIO(csv_text)))[0]
            self.assertIn("Global/front matter; no OLP unit", row[INDEX.CSV_COLUMNS[7]])
            self.assertIn("open-logic-locale.sty:L1", row[INDEX.CSV_COLUMNS[8]])
            self.assertIn("no OLP unit or reader-page claim", row[INDEX.CSV_COLUMNS[11]])
            self.assertNotIn("Location not recorded", row[INDEX.CSV_COLUMNS[12]])
            where = INDEX.start_here_where(decision, "#detail")
            self.assertIn("no OLP unit", where)
            self.assertIn("#L1", where)
            self.assertNotIn("PDF", where)

    def test_all_review_ledgers_and_legacy_locator_schema_are_supported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            terminology = repo / "evidence/classical/terminology"
            reviews = repo / "evidence/classical/reviews"
            batches = repo / "evidence/classical/batches"
            repairs = repo / "evidence/classical/repairs"
            terminology.mkdir(parents=True)
            reviews.mkdir(parents=True)
            batches.mkdir(parents=True)
            repairs.mkdir(parents=True)
            (terminology / "retro-0001-0150.json").write_text(
                json.dumps({"decisions": []}), encoding="utf-8"
            )
            (reviews / "0301-0400.json").write_text(
                json.dumps({"terminology_decisions": [{"decision_id": "TERM-X"}]}),
                encoding="utf-8",
            )
            (batches / "empty.json").write_text(
                json.dumps({"terminology_decisions": []}), encoding="utf-8"
            )
            (repairs / "0401-0500.json").write_text(
                json.dumps({"difficult_terminology_decisions": [{"id": "TERM-R"}]}),
                encoding="utf-8",
            )
            (repairs / "owner-followup.json").write_text(
                json.dumps(
                    {
                        "schema": "openlogic-classical-owner-followup-repairs-v1",
                        "findings": [{"finding_id": "TERM-F"}],
                    }
                ),
                encoding="utf-8",
            )
            (reviews / "0101-0200.json").write_text(
                json.dumps({"provisional_terminology_questions": [{"id": "T-COMPACT"}]}),
                encoding="utf-8",
            )
            locale = repo / "evidence/provenance/locale-ar"
            locale.mkdir(parents=True)
            (locale / "TERMINOLOGY_AND_ADVERSE_LEDGER.csv").write_text(
                "source_term,chosen_arabic,status,adverse_or_rejected,aliases_or_notes,domain_or_context,review_status,review_date,reviewer,evidence_or_rationale\n",
                encoding="utf-8",
            )
            discovered = [path.relative_to(repo).as_posix() for path in INDEX.discover_ledgers(repo)]
            self.assertEqual(
                discovered,
                [
                    "evidence/classical/repairs/0401-0500.json",
                    "evidence/classical/repairs/owner-followup.json",
                    "evidence/classical/reviews/0101-0200.json",
                    "evidence/classical/reviews/0301-0400.json",
                    "evidence/classical/terminology/retro-0001-0150.json",
                    "evidence/provenance/locale-ar/TERMINOLOGY_AND_ADVERSE_LEDGER.csv",
                ],
            )

            normalized = INDEX.normalize_occurrence_sources(
                {
                    "unit_id": "OLP-0306",
                    "english_path": "content/unit.tex",
                    "english_sha256": "1" * 64,
                    "msa_path": "source/locale/ar/content/unit.tex",
                    "msa_sha256": "2" * 64,
                    "classical_path": "source/locale/ar-classical/content/unit.tex",
                    "classical_sha256": "3" * 64,
                    "classical_lines": [11, 20],
                    "classical_excerpt": "exact passage",
                }
            )
            self.assertEqual([row["source_kind"] for row in normalized], ["english", "msa", "classical"])
            self.assertEqual(normalized[0]["ledger_locator_status"], "identity-only legacy record; no exact line asserted")
            self.assertEqual(normalized[2]["line_start"], 11)
            self.assertEqual(normalized[2]["line_end"], 20)
            self.assertEqual(normalized[2]["excerpt"], "exact passage")

    def test_owner_followup_findings_preserve_exact_review_locations(self) -> None:
        identity = {
            "path": "evidence/classical/repairs/OWNER_FOLLOWUP.json",
            "bytes": 1,
            "sha256": "A" * 64,
        }
        payload = {
            "schema": "openlogic-classical-owner-followup-repairs-v1",
            "findings": [
                {
                    "finding_id": "C184-01",
                    "unit_id": "OLP-0184",
                    "class": "technical_terminology_and_semantic_precision",
                    "source_term": "n-place predicate",
                    "problem": "Locality was confused with arity.",
                    "chosen_arabic": "محمول ذو n مواضع",
                    "rationale": "It states the number of argument places explicitly.",
                    "alternatives": ["n-موضعي"],
                    "expert_review": {
                        "sensitive": True,
                        "question": "ما المصطلح المعتمد؟",
                        "open_to_correction": True,
                    },
                    "english": {
                        "path": "content/unit.tex",
                        "lines": "60-64",
                        "sha256": "1" * 64,
                    },
                    "current": {
                        "msa": {
                            "path": "source/locale/ar/content/unit.tex",
                            "term_lines": "61-62",
                            "sha256": "2" * 64,
                        },
                        "classical": {
                            "path": "source/locale/ar-classical/content/unit.tex",
                            "term_lines": "62,64",
                            "sha256": "3" * 64,
                        },
                    },
                }
            ],
        }
        rows = INDEX.normalize_owner_followup_findings(payload, identity)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["recorded_decision_id"], "C184-01")
        self.assertEqual(row["english_term"], "n-place predicate")
        self.assertEqual(row["chosen_arabic"], "محمول ذو n مواضع")
        self.assertEqual(row["expert_question"], "ما المصطلح المعتمد؟")
        self.assertEqual(
            [key for occurrence in row["occurrences"] for key in occurrence if key != "unit_id"],
            ["english", "msa", "classical"],
        )
        classical = row["occurrences"][0]["classical"]
        self.assertEqual(
            [(item["line_start"], item["line_end"]) for item in classical["locators"]],
            [(62, 62), (64, 64)],
        )

    def test_compact_current_excerpt_requires_an_exact_term_witness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            path = repo / "source/locale/ar-classical/content/unit.tex"
            path.parent.mkdir(parents=True)
            path.write_text(
                "مقدمة\nالجدول الدلالي شجرة برهان\n% الجداول الدلالية\nخاتمة\n",
                encoding="utf-8",
            )
            decision = {
                "english_term": "tableau / tableaux",
                "chosen_arabic": "الجدول الدلالي / الجداول الدلالية",
            }
            self.assertEqual(
                INDEX.current_term_bearing_excerpt(
                    repo, path.relative_to(repo).as_posix(), 2, 2, "classical", decision
                ),
                "الجدول الدلالي شجرة برهان",
            )
            self.assertEqual(
                INDEX.current_term_bearing_excerpt(
                    repo, path.relative_to(repo).as_posix(), 3, 3, "classical", decision
                ),
                "",
            )
            self.assertEqual(
                INDEX.current_term_bearing_excerpt(
                    repo, path.relative_to(repo).as_posix(), 4, 4, "classical", decision
                ),
                "",
            )

    def test_exact_excerpt_relocation_and_ambiguity_are_distinct(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "source.tex"
            path.write_text("inserted\nunique phrase\nrepeat me\nrepeat me\n", encoding="utf-8")
            cache = INDEX.SourceCache()
            snapshot = cache.get(path, "source.tex")

            moved = INDEX.reconcile_lines(snapshot, 1, 1, "unique phrase", "0" * 64)
            self.assertTrue(moved["resolved"])
            self.assertEqual(moved["status"], "relocated-by-exact-excerpt")
            self.assertEqual((moved["current_line_start"], moved["current_line_end"]), (2, 2))

            ambiguous = INDEX.reconcile_lines(snapshot, 1, 1, "repeat me", "0" * 64)
            self.assertFalse(ambiguous["resolved"])
            self.assertEqual(ambiguous["status"], "unresolved-excerpt-ambiguous")
            self.assertEqual(ambiguous["candidate_line_ranges"], [[3, 3], [4, 4]])

            missing = INDEX.reconcile_lines(snapshot, 1, 1, "not present", "0" * 64)
            self.assertFalse(missing["resolved"])
            self.assertEqual(missing["status"], "unresolved-excerpt-not-found")

            stale_out_of_bounds = INDEX.reconcile_lines(
                snapshot, 99, 101, "unique phrase", "0" * 64
            )
            self.assertTrue(stale_out_of_bounds["resolved"])
            self.assertEqual(
                stale_out_of_bounds["status"], "relocated-by-exact-excerpt"
            )
            self.assertEqual(
                stale_out_of_bounds["current_line_start"], 2
            )

            invalid_hash_only = INDEX.reconcile_lines(
                snapshot, 1, 99, "", INDEX.sha256_file(path)
            )
            self.assertFalse(invalid_hash_only["resolved"])
            self.assertEqual(
                invalid_hash_only["status"], "unresolved-invalid-line-range"
            )

    def test_unique_exact_term_and_context_recovery_never_choose_ambiguity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            source = repo / "source.tex"
            source.write_text(
                "An active formula is consumed.\n"
                "repeat branch\n"
                "repeat branch\n"
                "one two three four CURRENT six seven eight nine ten\n",
                encoding="utf-8",
            )
            cache = INDEX.SourceCache()

            def unresolved(term: str, excerpt: str = "") -> dict:
                raw = {
                    "source_kind": "english",
                    "path": "source.tex",
                    "recorded_sha256": "0" * 64,
                    "line_start": None,
                    "line_end": None,
                    "excerpt": excerpt,
                }
                location = INDEX.reconcile_location(
                    raw, repo, repo, cache, "https://example.test/repo", "https://example.test/en"
                )
                return INDEX.recover_location_by_exact_search(
                    location,
                    {
                        "english_term": term,
                        "chosen_arabic": "مصطلح",
                        "sense": "",
                    },
                    {"context_note": ""},
                    cache,
                    "https://example.test/repo",
                    "https://example.test/en",
                )

            recovered_term = unresolved("active formula")
            self.assertTrue(recovered_term["line_reconciliation"]["resolved"])
            self.assertEqual(
                recovered_term["line_reconciliation"]["status"],
                "relocated-by-unique-exact-term",
            )
            self.assertEqual(recovered_term["line_reconciliation"]["current_line_start"], 1)
            self.assertTrue(recovered_term["source_url"].endswith("source.tex#L1"))

            ambiguous = unresolved("branch")
            self.assertFalse(ambiguous["line_reconciliation"]["resolved"])
            self.assertEqual(
                ambiguous["line_reconciliation"]["status"], "unresolved-no-line-locator"
            )

            context_raw = {
                "source_kind": "english",
                "path": "source.tex",
                "recorded_sha256": "0" * 64,
                "line_start": 1,
                "line_end": 1,
                "excerpt": "one two three four OLD six seven eight nine ten",
            }
            context_location = INDEX.reconcile_location(
                context_raw,
                repo,
                repo,
                cache,
                "https://example.test/repo",
                "https://example.test/en",
            )
            context_location = INDEX.recover_location_by_exact_search(
                context_location,
                {"english_term": "unused term", "chosen_arabic": "مصطلح", "sense": ""},
                {"context_note": ""},
                cache,
                "https://example.test/repo",
                "https://example.test/en",
            )
            self.assertTrue(context_location["line_reconciliation"]["resolved"])
            self.assertEqual(
                context_location["line_reconciliation"]["status"],
                "relocated-by-unique-exact-context-fragment",
            )
            self.assertEqual(context_location["line_reconciliation"]["current_line_start"], 4)

            repeated_locations = []
            for recorded_line in (10, 20):
                repeated_locations.append(
                    {
                        "source_kind": "english",
                        "logical_path": "source.tex",
                        "_fs_path": source,
                        "line_start": recorded_line,
                        "line_end": recorded_line,
                        "excerpt": "repeat me",
                        "line_reconciliation": {
                            "status": "unresolved-excerpt-ambiguous",
                            "resolved": False,
                            "current_line_start": None,
                            "current_line_end": None,
                            "candidate_line_ranges": [[2, 2], [3, 3]],
                            "recorded_hash_matches_current": False,
                        },
                    }
                )
            INDEX.recover_unique_monotone_sequences(
                repeated_locations,
                cache,
                "https://example.test/repo",
                "https://example.test/en",
            )
            self.assertEqual(
                [
                    row["line_reconciliation"]["current_line_start"]
                    for row in repeated_locations
                ],
                [2, 3],
            )
            self.assertTrue(
                all(
                    row["line_reconciliation"]["status"]
                    == "relocated-by-unique-exact-monotone-sequence"
                    for row in repeated_locations
                )
            )

    def test_registered_token_display_and_cross_language_structure_recovery(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            base = repo / "source/open-logic-config.sty"
            arabic = repo / "source/locale/ar/open-logic-config.sty"
            arabic.parent.mkdir(parents=True)
            base.parent.mkdir(parents=True, exist_ok=True)
            base.write_text(
                "\\settexttoken{element}*{element}{elements}\n"
                "\\settexttoken{bijection}{bijection}{bijections}\n",
                encoding="utf-8",
            )
            arabic.write_text(
                "\\settexttoken{element}{عنصر}{عناصر}[عنصر][عناصر]\n"
                "\\settexttoken{bijection}{دالة تقابلية}{دوال تقابلية}"
                "[دالة تقابلية][دوال تقابلية]\n",
                encoding="utf-8",
            )
            registries = INDEX.load_review_token_registries(repo)
            decision = {
                "english_term": r"a element; !!^{bijection}; \printtoken{S}{element}",
                "chosen_arabic": "!!^{bijection}",
                "rationale": r"Uses \Nat and \foreignlanguage{english}{K\H{o}nig}.",
                "expert_question": r"Check \printtoken{S}{bijection}.",
            }
            INDEX.attach_review_display(decision, registries)
            self.assertEqual(
                INDEX.human_english_term(decision), "an element; Bijection; Element"
            )
            self.assertEqual(INDEX.human_chosen_arabic(decision), "دالة تقابلية")
            self.assertEqual(
                {
                    row["token"]
                    for row in decision["review_display"]["registry_expansions"]["english"]
                },
                {"element", "bijection"},
            )
            self.assertNotRegex(
                " ".join(
                    str(decision["review_display"].get(field) or "")
                    for field in (
                        "english_term", "chosen_arabic", "sense", "rationale",
                        "edition", "expert_review_reason", "expert_question",
                        "expert_review_question", "alternatives",
                    )
                ),
                r"\\[A-Za-z@]+|!!(?:\^|a|\{)",
            )

            english = repo / "english.tex"
            english.write_text(
                "weakening elsewhere\n"
                "introduction\n"
                "If it was a weakening rule, apply\n"
                "\\olref[adm]{prop:weak-G3c-adm}.\n",
                encoding="utf-8",
            )
            cache = INDEX.SourceCache()
            unresolved = INDEX.reconcile_location(
                {
                    "source_kind": "english",
                    "path": "english.tex",
                    "recorded_sha256": "0" * 64,
                    "line_start": None,
                    "line_end": None,
                    "excerpt": "",
                },
                repo,
                repo,
                cache,
                "https://example.test/repo",
                "https://example.test/en",
            )
            unresolved = INDEX.recover_location_by_exact_search(
                unresolved,
                {"english_term": "weakening", "chosen_arabic": "الإضعاف", "sense": ""},
                {"context_note": ""},
                cache,
                "https://example.test/repo",
                "https://example.test/en",
            )
            self.assertFalse(unresolved["line_reconciliation"]["resolved"])
            companion = {
                "source_kind": "msa",
                "current_excerpt": "الإضعاف المقبول \\olref[adm]{prop:weak-G3c-adm}",
                "line_reconciliation": {"resolved": True},
            }
            INDEX.recover_by_cross_language_exact_structure(
                [unresolved, companion],
                cache,
                "https://example.test/repo",
                "https://example.test/en",
            )
            self.assertTrue(unresolved["line_reconciliation"]["resolved"])
            self.assertEqual(
                unresolved["line_reconciliation"]["status"],
                "relocated-by-cross-language-exact-structure",
            )
            self.assertEqual(unresolved["line_reconciliation"]["current_line_start"], 3)

    def test_actual_retrospective_ledger_quotes_use_their_declared_languages(self) -> None:
        repo = SCRIPT.parents[1]
        ledger = repo / "evidence/classical/terminology/retro-0005-0050.json"
        ledger_bytes = ledger.read_bytes()
        records = json.loads(ledger_bytes)["decisions"]
        cases = {
            "retro-0005-0050:named-defn:dfccada7aa85553b":
                ("دالة تقابلية", "Bijection"),
            "retro-0005-0050:named-defn:eeadedf7e81ef705":
                ("دالة متباينة", "Injective function"),
        }
        registries = INDEX.load_review_token_registries(repo)
        tested = set()
        for source in records:
            if source["decision_id"] not in cases:
                continue
            with self.subTest(decision_id=source["decision_id"]):
                decision = copy.deepcopy(source)
                arabic, english = cases[source["decision_id"]]
                INDEX.attach_review_display(decision, registries)
                display = decision.pop("review_display")
                self.assertEqual(decision, source)
                self.assertEqual(decision["recording_mode"], "retrospective-reconstruction")
                self.assertTrue(decision["open_to_correction"])
                self.assertEqual(display["chosen_arabic"], arabic)
                self.assertIn(f"retains «{arabic}»", display["rationale"])
                self.assertIn(f"for English «{english}»", display["rationale"])
                self.assertIn(f"does «{arabic}»", display["expert_question"])
                self.assertIn(f"sense of «{english}»", display["expert_question"])
                self.assertIn("present-tense retrospective justification", display["rationale"])
                if source["decision_id"].endswith("dfccada7aa85553b"):
                    # The same token bytes must become Arabic in one quote and
                    # English in the other; replacing every match is incorrect.
                    self.assertEqual(source["chosen_arabic"], source["english_term"])
                tested.add(source["decision_id"])
        self.assertEqual(tested, set(cases))
        self.assertEqual(ledger.read_bytes(), ledger_bytes)

    def test_unrecognized_retrospective_prose_does_not_infer_quote_languages(self) -> None:
        repo = SCRIPT.parents[1]
        records = json.loads(
            (repo / "evidence/classical/terminology/retro-0005-0050.json").read_bytes()
        )["decisions"]
        source = next(
            row for row in records
            if row["decision_id"] == "retro-0005-0050:named-defn:dfccada7aa85553b"
        )
        registries = INDEX.load_review_token_registries(repo)
        variants = []
        unrelated = copy.deepcopy(source)
        unrelated["rationale"] = "Review «!!^{bijection}» alongside «!!^{bijection}»."
        unrelated["expert_question"] = "Which language is «!!^{bijection}» here?"
        variants.append(("unrecognized wording", unrelated))
        mismatched = copy.deepcopy(source)
        mismatched["chosen_arabic"] = "a different recorded choice"
        variants.append(("quotation does not match chosen field", mismatched))
        other_mode = copy.deepcopy(source)
        other_mode["recording_mode"] = "contemporaneous"
        variants.append(("not the recorded retrospective mode", other_mode))
        for label, decision in variants:
            with self.subTest(case=label):
                original = copy.deepcopy(decision)
                INDEX.attach_review_display(decision, registries)
                display = decision.pop("review_display")
                self.assertEqual(decision, original)
                for field in ("rationale", "expert_question"):
                    self.assertEqual(
                        display[field],
                        INDEX.humanize_tex(original[field], registries["english"]),
                    )
                    self.assertNotIn("دالة تقابلية", display[field])

    def test_duplicate_decision_variants_merge_exact_occurrences_losslessly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            paths = []
            base = {
                "decision_id": "TERM-X",
                "english_term": "term",
                "chosen_arabic": "مصطلح",
                "rationale": "Reason.",
                "open_to_correction": True,
            }
            for name, occurrences in (
                ("a.json", [{"unit_id": "OLP-0001"}]),
                ("b.json", [{"unit_id": "OLP-0001"}, {"unit_id": "OLP-0002"}]),
            ):
                path = repo / name
                row = dict(base)
                row["occurrences"] = occurrences
                path.write_text(json.dumps({"decisions": [row]}), encoding="utf-8")
                paths.append(path)
            variant_path = repo / "c.json"
            variant = dict(base)
            variant["chosen_arabic"] = "لفظ آخر"
            variant["occurrences"] = [{"unit_id": "OLP-0003"}]
            variant_path.write_text(
                json.dumps({"decisions": [variant]}), encoding="utf-8"
            )
            paths.append(variant_path)

            decisions, _, _ = INDEX.load_decisions(repo, paths)
            self.assertEqual(len(decisions), 2)
            self.assertTrue(all("--variant-" in row["decision_id"] for row in decisions))
            merged = next(row for row in decisions if row["chosen_arabic"] == "مصطلح")
            self.assertEqual(len(merged["occurrences"]), 2)
            self.assertEqual(len(merged["source_records"]), 2)

    def test_exact_semantic_duplicate_prefers_richer_and_keeps_locale_provenance(self) -> None:
        occurrence = {
            "unit_id": "OLP-0001",
            "msa": {
                "path": "source/locale/ar/content/unit.tex",
                "sha256": "a" * 64,
                "locators": [
                    {"line_start": 7, "line_end": 7, "excerpt": "مصطلح"}
                ],
            },
        }
        locale = {
            "decision_id": "locale-ar-chosen-abc",
            "english_term": "Term",
            "sense": "same mathematical sense",
            "chosen_arabic": "لفظ قديم",
            "rationale": "brief",
            "occurrences": [occurrence],
            "alternatives": [],
            "source_record": {
                "path": "evidence/provenance/locale-ar/TERMINOLOGY_AND_ADVERSE_LEDGER.csv"
            },
        }
        authoritative = {
            "decision_id": "TERM-RICH",
            "english_term": " term ",
            "sense": "same mathematical sense",
            "chosen_arabic": "مصطلح",
            "rationale": "A much fuller recorded mathematical rationale.",
            "basis": "authoritative repair audit",
            "occurrences": [occurrence],
            "alternatives": [],
            "source_record": {"path": "evidence/classical/repairs/test.json"},
        }
        merged, count = INDEX.merge_exact_semantic_duplicates(
            [locale, authoritative]
        )
        self.assertEqual(count, 1)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["decision_id"], "TERM-RICH")
        self.assertEqual(
            merged[0]["deduplicated_source_decision_ids"],
            ["locale-ar-chosen-abc"],
        )
        self.assertEqual(
            {row["path"] for row in merged[0]["source_records"]},
            {
                "evidence/classical/repairs/test.json",
                "evidence/provenance/locale-ar/TERMINOLOGY_AND_ADVERSE_LEDGER.csv",
            },
        )
        self.assertIn(
            "لفظ قديم",
            [row["form"] for row in merged[0]["alternatives"]],
        )

    def test_cross_decision_empty_legacy_stub_is_machine_only(self) -> None:
        def occurrence(unit: str, locations: list[dict], raw: dict) -> dict:
            return {
                "unit": {"unit_id": unit},
                "locations": locations,
                "machine_location_count": len(locations),
                "human_review_location_count": len(locations),
                "human_review_included": True,
                "language_coverage": {"recorded_source_kinds": [] if not locations else ["classical"]},
                "raw_occurrence": raw,
            }

        stub = {
            "decision_id": "stub",
            "english_term": "weakening",
            "index_metadata": {
                "human_index_included": True,
                "occurrences": [
                    occurrence("OLP-0001", [], {"unit_id": "OLP-0001", "classical_lines": [4, 5]})
                ],
            },
        }
        located_location = {
            "human_review_included": True,
            "line_reconciliation": {"resolved": True},
        }
        rich = {
            "decision_id": "rich",
            "english_term": "weakening",
            "index_metadata": {
                "human_index_included": True,
                "occurrences": [
                    occurrence("OLP-0001", [located_location], {"unit_id": "OLP-0001"})
                ],
            },
        }
        INDEX.suppress_cross_decision_locator_stubs([stub, rich])
        self.assertFalse(stub["index_metadata"]["human_index_included"])
        self.assertEqual(
            stub["index_metadata"]["occurrences"][0]["superseded_by_located_decision_ids"],
            ["rich"],
        )
        self.assertTrue(rich["index_metadata"]["human_index_included"])

    def test_whole_file_boilerplate_and_reviewed_sense_mismatches_are_not_exact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "whole.tex"
            lines = [f"ordinary line {number}" for number in range(1, 31)]
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            snapshot = INDEX.SourceCache().get(path, "whole.tex")
            whole = INDEX.reconcile_lines(
                snapshot, 1, 30, "\n".join(lines), INDEX.sha256_file(path)
            )
            self.assertFalse(whole["resolved"])
            self.assertEqual(
                whole["status"], "unresolved-whole-file-span-not-exact-occurrence"
            )

            broad_source = Path(tmp) / "broad.tex"
            broad_source.write_text(
                "\\olsection{Rules for Other Accessibility Relations}\n"
                + "\n".join(
                    "a branch continues" if number in {8, 22}
                    else f"ordinary content {number}"
                    for number in range(2, 31)
                )
                + "\n",
                encoding="utf-8",
            )
            broad_cache = INDEX.SourceCache()
            broad = INDEX.reconcile_location(
                {
                    "source_kind": "english",
                    "path": "broad.tex",
                    "recorded_sha256": "0" * 64,
                    "line_start": 1,
                    "line_end": 30,
                    "excerpt": r"\olsection{Rules for Other Accessibility Relations}",
                },
                Path(tmp),
                Path(tmp),
                broad_cache,
                "https://example.test/repo",
                "https://example.test/en",
            )
            self.assertTrue(broad["line_reconciliation"]["resolved"])
            self.assertEqual(
                broad["line_reconciliation"]["current_line_start"], 1
            )
            INDEX.invalidate_broad_excerpt_without_recorded_term(
                broad, {"english_term": "branch", "chosen_arabic": "فرع"}
            )
            broad = INDEX.recover_location_by_exact_search(
                broad,
                {"english_term": "branch", "chosen_arabic": "فرع", "sense": ""},
                {"context_note": ""},
                broad_cache,
                "https://example.test/repo",
                "https://example.test/en",
            )
            self.assertFalse(broad["line_reconciliation"]["resolved"])
            self.assertEqual(
                broad["line_reconciliation"]["status"],
                "unresolved-broad-span-excerpt-not-term-occurrence",
            )
            self.assertEqual(
                broad["line_reconciliation"]["exact_search_candidate_line_ranges"],
                [[8, 8], [22, 22]],
            )

            def narrow_broad(raw: dict) -> dict:
                location = INDEX.reconcile_location(
                    raw,
                    Path(tmp),
                    Path(tmp),
                    INDEX.SourceCache(),
                    "https://example.test/repo",
                    "https://example.test/en",
                )
                self.assertTrue(location["line_reconciliation"]["resolved"])
                INDEX.invalidate_broad_excerpt_without_recorded_term(
                    location,
                    {
                        "english_term": "ordinary content 15",
                        "chosen_arabic": "محتوى",
                    },
                )
                return INDEX.recover_location_by_exact_search(
                    location,
                    {
                        "english_term": "ordinary content 15",
                        "chosen_arabic": "محتوى",
                        "sense": "",
                    },
                    {"context_note": ""},
                    INDEX.SourceCache(),
                    "https://example.test/repo",
                    "https://example.test/en",
                )

            hash_bound = narrow_broad(
                {
                    "source_kind": "english",
                    "path": "broad.tex",
                    "recorded_sha256": INDEX.sha256_file(broad_source),
                    "line_start": 1,
                    "line_end": 30,
                    "excerpt": "",
                }
            )
            self.assertEqual(
                (
                    hash_bound["line_reconciliation"]["current_line_start"],
                    hash_bound["line_reconciliation"]["current_line_end"],
                ),
                (15, 15),
            )

            nineteen_line_hash_bound = narrow_broad(
                {
                    "source_kind": "english",
                    "path": "broad.tex",
                    "recorded_sha256": INDEX.sha256_file(broad_source),
                    "line_start": 1,
                    "line_end": 19,
                    "excerpt": "",
                }
            )
            self.assertEqual(
                (
                    nineteen_line_hash_bound["line_reconciliation"]["current_line_start"],
                    nineteen_line_hash_bound["line_reconciliation"]["current_line_end"],
                ),
                (15, 15),
            )

            broad_excerpt = "\n".join(
                broad_source.read_text(encoding="utf-8").splitlines()[:25]
            )
            excerpt_bound = narrow_broad(
                {
                    "source_kind": "english",
                    "path": "broad.tex",
                    "recorded_sha256": "0" * 64,
                    "line_start": 1,
                    "line_end": 25,
                    "excerpt": broad_excerpt,
                }
            )
            self.assertEqual(
                (
                    excerpt_bound["line_reconciliation"]["current_line_start"],
                    excerpt_bound["line_reconciliation"]["current_line_end"],
                ),
                (15, 15),
            )

            unit = INDEX.UnitMeta(
                unit_id="OLP-0451",
                title="test",
                source_role="reader_unit",
                target_path="source.tex",
                aux_label=None,
            )
            boilerplate = {
                "source_kind": "english",
                "current_excerpt": r"\documentclass[../]{subfiles}",
                "source_url": "https://example.test/file#L5",
                "line_reconciliation": {
                    "status": "verified-recorded-lines",
                    "resolved": True,
                    "current_line_start": 5,
                    "current_line_end": 5,
                    "candidate_line_ranges": [],
                },
            }
            INDEX.apply_location_quality_guards(
                boilerplate,
                {"decision_id": "ar-classical-0451-0500-equivalence-class"},
                unit,
            )
            self.assertFalse(boilerplate["line_reconciliation"]["resolved"])
            self.assertEqual(
                boilerplate["line_reconciliation"]["status"],
                "unresolved-boilerplate-not-term-occurrence",
            )

            false_tableau = {
                "source_kind": "msa",
                "current_excerpt": "ننشئ جدول صدق للصيغة.",
                "line_reconciliation": {"resolved": True},
            }
            INDEX.apply_location_quality_guards(
                false_tableau,
                {"decision_id": "ar-classical-0451-0500-tableau-token"},
                unit,
            )
            self.assertFalse(false_tableau["human_review_included"])
            self.assertIn("truth table", false_tableau["human_review_exclusion_reason"])

            false_class = {
                "source_kind": "classical",
                "current_excerpt": "نختبر الفئة المقصودة من النماذج.",
                "line_reconciliation": {"resolved": True},
            }
            INDEX.apply_location_quality_guards(
                false_class,
                {"decision_id": "ar-classical-0451-0500-equivalence-class"},
                unit,
            )
            self.assertFalse(false_class["human_review_included"])

            true_class = {
                "source_kind": "classical",
                "current_excerpt": "هذه فئة تكافؤ للعلاقة.",
                "line_reconciliation": {"resolved": True},
            }
            INDEX.apply_location_quality_guards(
                true_class,
                {"decision_id": "ar-classical-0451-0500-equivalence-class"},
                unit,
            )
            self.assertTrue(true_class["human_review_included"])

            comment_only = {
                "source_kind": "english",
                "current_excerpt": "% tableau appears only in a disabled note",
                "source_url": "https://example.test/file#L9",
                "line_reconciliation": {
                    "status": "verified-recorded-lines",
                    "resolved": True,
                    "current_line_start": 9,
                    "current_line_end": 9,
                    "candidate_line_ranges": [],
                    "resolution_certificate": {"method": "fixture"},
                },
            }
            INDEX.apply_location_quality_guards(
                comment_only, {"decision_id": "other"}, unit
            )
            self.assertFalse(comment_only["line_reconciliation"]["resolved"])
            self.assertEqual(
                comment_only["line_reconciliation"]["status"],
                "unresolved-comment-only-not-term-occurrence",
            )
            self.assertNotIn(
                "resolution_certificate", comment_only["line_reconciliation"]
            )

    def test_component_only_hits_never_resolve_a_different_sense(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            source = repo / "unit.tex"
            source.write_text(
                "mathematical and logical sets\n"
                "قاعدة إثبات التالي\n"
                "غير أن النتيجة صحيحة\n"
                "the fixed-point theorem\n",
                encoding="utf-8",
            )
            cache = INDEX.SourceCache()

            def recover(kind: str, english: str, arabic: str) -> dict:
                location = INDEX.reconcile_location(
                    {
                        "source_kind": kind,
                        "path": "unit.tex",
                        "recorded_sha256": "0" * 64,
                        "line_start": None,
                        "line_end": None,
                        "excerpt": "",
                    },
                    repo,
                    repo,
                    cache,
                    "https://example.test/repo",
                    "https://example.test/en",
                )
                return INDEX.recover_location_by_exact_search(
                    location,
                    {"english_term": english, "chosen_arabic": arabic, "sense": ""},
                    {"context_note": ""},
                    cache,
                    "https://example.test/repo",
                    "https://example.test/en",
                )

            for location in (
                recover("english", "logical connective", "رابط منطقي"),
                recover("classical", "modus ponens", "إثبات المقدّم"),
                recover("classical", "undischarged assumption", "غير مسقط"),
                recover("english", "fixed-point combinator", "مركب النقطة الثابتة"),
            ):
                self.assertFalse(location["line_reconciliation"]["resolved"])
                attempts = location["line_reconciliation"]["exact_recovery_attempts"]
                self.assertTrue(
                    any(attempt.get("candidate_only") for attempt in attempts)
                )

    def test_locale_csv_adapter_is_lossless_stable_and_exact_only_when_proved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            source = repo / "source/locale/ar/content/unit.tex"
            source.parent.mkdir(parents=True)
            source.write_text("أول\nمصطلح\nثالث\n", encoding="utf-8")
            units = [
                {
                    "id": "OLP-0001",
                    "source_path": "content/unit.tex",
                    "english_sha256": "1" * 64,
                    "arabic_path": "source/locale/ar/content/unit.tex",
                    "target_path": "source/locale/ar-classical/content/unit.tex",
                }
            ]
            columns = [
                "source_term", "chosen_arabic", "status", "adverse_or_rejected",
                "aliases_or_notes", "domain_or_context", "review_status",
                "review_date", "reviewer", "evidence_or_rationale",
            ]
            stream = io.StringIO(newline="")
            writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
            writer.writeheader()
            chosen = {
                "source_term": "term", "chosen_arabic": "مصطلح", "status": "chosen",
                "adverse_or_rejected": "بديل مرفوض", "aliases_or_notes": "اسم آخر",
                "domain_or_context": "locale/ar/content/unit.tex lines 2--3; OLP-0001",
                "review_status": "expert review pending", "review_date": "2026-01-01",
                "reviewer": "reviewer", "evidence_or_rationale": "سبب مسجل",
            }
            writer.writerow(chosen)
            writer.writerow(
                dict(
                    chosen,
                    source_term="unit-only term",
                    chosen_arabic="مصطلح الوحدة",
                    domain_or_context="definition discussed in OLP-0001",
                )
            )
            writer.writerow(
                dict(chosen, source_term="source defect", status="source_correction_applied")
            )
            raw = stream.getvalue().encode("utf-8")
            identity = {"path": "ledger.csv", "bytes": len(raw), "sha256": INDEX.sha256_bytes(raw)}
            decisions = INDEX.normalize_locale_csv(repo, raw, identity, units)
            self.assertEqual(len(identity["_locale_records"]), 3)
            self.assertEqual(len(decisions), 2)
            decision = next(row for row in decisions if row["english_term"] == "term")
            self.assertEqual(decision["english_term"], "term")
            self.assertEqual(decision["chosen_arabic"], "مصطلح")
            self.assertEqual(len(decision["alternatives"]), 2)
            source_rows = INDEX.normalize_occurrence_sources(decision["occurrences"][0])
            self.assertEqual(source_rows[0]["path"], "source/locale/ar/content/unit.tex")
            self.assertEqual((source_rows[0]["line_start"], source_rows[0]["line_end"]), (2, 3))
            unit_only = next(
                row for row in decisions if row["english_term"] == "unit-only term"
            )
            self.assertEqual(unit_only["occurrences"][0]["unit_id"], "OLP-0001")
            self.assertEqual(
                unit_only["occurrences"][0]["locale_locator_status"],
                "The locale ledger explicitly names this OLP unit, but does not prove one source edition, path and line for the choice.",
            )
            self.assertEqual(
                INDEX.normalize_occurrence_sources(unit_only["occurrences"][0]), []
            )
            second_identity = {"path": "other.csv", "bytes": len(raw), "sha256": INDEX.sha256_bytes(raw)}
            second = INDEX.normalize_locale_csv(repo, raw, second_identity, units)
            second_decision = next(row for row in second if row["english_term"] == "term")
            self.assertEqual(second_decision["decision_id"], decision["decision_id"])
            self.assertEqual(
                identity["adapter"]["adverse_or_repair_records_preserved_machine_only"], 1
            )

    def test_locale_backtracking_requires_unique_exact_three_way_witness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            english_root = root / "english"
            paths = {
                "english": english_root / "content/unit.tex",
                "msa": repo / "source/locale/ar/content/unit.tex",
                "classical": repo / "source/locale/ar-classical/content/unit.tex",
            }
            for path in paths.values():
                path.parent.mkdir(parents=True, exist_ok=True)
            paths["english"].write_text(
                "% compactness in a comment must not count\n"
                "The compactness theorem applies.\n",
                encoding="utf-8",
            )
            paths["msa"].write_text("تثبت مبرهنة التراص هنا.\n", encoding="utf-8")
            paths["classical"].write_text("وهنا تثبت مبرهنة التراص.\n", encoding="utf-8")
            units = [
                {
                    "id": "OLP-0001",
                    "source_path": "content/unit.tex",
                    "english_sha256": INDEX.sha256_bytes(paths["english"].read_bytes()),
                    "arabic_path": "source/locale/ar/content/unit.tex",
                    "target_path": "source/locale/ar-classical/content/unit.tex",
                }
            ]

            occurrences, metadata = INDEX.backtrack_locale_choice_occurrences(
                repo, english_root, units, "compactness", "التراص", {}
            )
            self.assertEqual(metadata["status"], "resolved")
            self.assertEqual(metadata["resolved_unit_count"], 1)
            self.assertEqual(metadata["resolved_three_way_location_count"], 3)
            self.assertEqual(len(occurrences), 1)
            for kind in ("english", "msa", "classical"):
                locator = occurrences[0][kind]["locators"][0]
                self.assertEqual(locator["witness"]["rule"],
                                 "unique-exact-visible-hit-in-each-baseline-paired-file")

            paths["classical"].write_text(
                "وهنا التراص، ثم يرد التراص مرة أخرى.\n", encoding="utf-8"
            )
            occurrences, metadata = INDEX.backtrack_locale_choice_occurrences(
                repo, english_root, units, "compactness", "التراص", {}
            )
            self.assertEqual(occurrences, [])
            self.assertEqual(metadata["status"], "unresolved-no-unique-three-way-witness")
            self.assertEqual(metadata["rejection_counts"]["classical-hit-count-2"], 1)

            units[0]["english_sha256"] = "0" * 64
            occurrences, metadata = INDEX.backtrack_locale_choice_occurrences(
                repo, english_root, units, "compactness", "التراص", {}
            )
            self.assertEqual(occurrences, [])
            self.assertEqual(metadata["rejection_counts"]["english-pinned-hash-mismatch"], 1)

    def test_locale_backtracking_rejects_component_pairing_ambiguity(self) -> None:
        occurrences, metadata = INDEX.backtrack_locale_choice_occurrences(
            Path("."), Path("."), [], "set; relation", "مجموعة", {}
        )
        self.assertEqual(occurrences, [])
        self.assertEqual(
            metadata["status"], "unresolved-component-cardinality-mismatch"
        )

    def test_duplicate_human_locations_and_empty_stubs_render_once(self) -> None:
        def location() -> dict:
            return {
                "source_kind": "classical",
                "logical_path": "source/unit.tex",
                "line_start": 4,
                "line_end": 4,
                "current_excerpt": "مصطلح",
                "human_review_included": True,
                "line_reconciliation": {
                    "status": "verified-recorded-lines-by-hash",
                    "resolved": True,
                    "current_line_start": 4,
                    "current_line_end": 4,
                },
            }

        occurrences = [
            {
                "unit": {"unit_id": "OLP-0001"}, "locations": [location()],
                "human_review_included": True, "human_review_location_count": 1,
            },
            {
                "unit": {"unit_id": "OLP-0001"}, "locations": [location()],
                "human_review_included": True, "human_review_location_count": 1,
            },
            {
                "unit": {"unit_id": "OLP-0002"}, "locations": [],
                "human_review_included": True, "human_review_location_count": 0,
            },
            {
                "unit": {"unit_id": "OLP-0002"}, "locations": [],
                "human_review_included": True, "human_review_location_count": 0,
            },
        ]
        INDEX.suppress_repeated_human_locations(occurrences)
        self.assertEqual(sum(len(INDEX.human_location_rows(row)) for row in occurrences), 1)
        self.assertEqual(sum(row["human_review_included"] for row in occurrences[2:]), 1)

    def test_repeated_unit_headings_are_grouped_without_dropping_locations(self) -> None:
        def location(line: int) -> dict:
            return {
                "source_kind": "classical",
                "logical_path": "source/locale/ar-classical/content/unit.tex",
                "file_url": "https://example.test/unit.tex",
                "source_url": f"https://example.test/unit.tex#L{line}",
                "line_start": line,
                "line_end": line,
                "page_evidence": [],
                "human_review_included": True,
                "line_reconciliation": {
                    "status": "verified-recorded-lines-by-hash",
                    "resolved": True,
                    "current_line_start": line,
                    "current_line_end": line,
                    "recorded_hash_matches_current": True,
                },
            }

        decision = {
            "decision_id": "TERM-GROUPED",
            "english_term": "grouped term",
            "chosen_arabic": "مصطلح مجموع",
            "sense": "one sense repeated in one unit",
            "rationale": "The same sense is used at both exact lines.",
            "expert_review_useful": False,
            "index_metadata": {
                "human_index_included": True,
                "occurrences": [
                    {
                        "human_review_included": True,
                        "unit": {"unit_id": "OLP-0001", "title": "عنوان"},
                        "locations": [location(4)],
                        "language_coverage": {"not_recorded_source_kinds": []},
                    },
                    {
                        "human_review_included": True,
                        "unit": {"unit_id": "OLP-0001", "title": "عنوان"},
                        "locations": [location(9)],
                        "language_coverage": {"not_recorded_source_kinds": []},
                    },
                ],
            },
        }
        payload = {"reader_evidence": [], "decisions": [decision]}
        rendered = INDEX.render_decision_shard(
            payload, [decision], "complete", 1, 1, None, None, "../../../../"
        )
        self.assertEqual(rendered.count("**OLP-0001 — عنوان**"), 1)
        self.assertIn("Grouped here: 2 recorded occurrence records", rendered)
        self.assertIn("unit.tex#L4", rendered)
        self.assertIn("unit.tex#L9", rendered)

    def test_unplaced_choice_has_one_explicit_csv_row(self) -> None:
        decision = {
            "decision_id": "TERM-UNPLACED",
            "english_term": "unplaced term",
            "chosen_arabic": "مصطلح بلا موضع",
            "sense": "recorded wording whose source location is not yet proved",
            "rationale": "The wording is retained provisionally.",
            "expert_review_useful": True,
            "index_metadata": {
                "human_index_included": True,
                "occurrences": [],
            },
        }
        payload = {"decisions": [decision]}
        text = INDEX.render_occurrence_csv(payload)
        rows = list(csv.DictReader(io.StringIO(text)))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][INDEX.CSV_COLUMNS[1]], "TERM-UNPLACED")
        self.assertIn("Location not recorded", rows[0][INDEX.CSV_COLUMNS[7]])
        self.assertIn("occurrence unresolved", rows[0][INDEX.CSV_COLUMNS[11]])
        self.assertIn("Location not recorded", rows[0][INDEX.CSV_COLUMNS[12]])
        self.assertEqual(INDEX.verify_occurrence_csv(payload, text), 1)

    def test_csv_question_never_points_to_a_different_repeated_unit(self) -> None:
        decision = {
            "english_term": "non-enumerable sets",
            "chosen_arabic": "مجموعات غير قابلة للتعداد",
            "expert_question": "At OLP-0033, is this the best established wording?",
        }
        occurrence = {
            "unit": {"unit_id": "OLP-0039"},
            "locations": [],
        }
        rendered = INDEX.occurrence_review_question(decision, occurrence)
        self.assertIn("OLP-0039", rendered)
        self.assertNotIn("OLP-0033", rendered)
        self.assertIn("exact source line unresolved", rendered)

    def test_csv_question_preserves_deliberate_cross_section_comparison(self) -> None:
        question = ("OLP-0009: compare الجداء الديكارتي with الضرب الديكارتي, "
                    "and check consistency with OLP-0012.")
        decision = {"expert_question": question}
        for unit_id in ("OLP-0009", "OLP-0012"):
            with self.subTest(unit_id=unit_id):
                occurrence = {"unit": {"unit_id": unit_id}, "locations": []}
                self.assertEqual(INDEX.occurrence_review_question(decision, occurrence), question)

    def test_start_here_excludes_routine_fragments_and_exposes_tiers(self) -> None:
        def decision(decision_id: str, term: str, arabic: str, basis: str) -> dict:
            return {
                "decision_id": decision_id,
                "english_term": term,
                "chosen_arabic": arabic,
                "sense": "recorded sense",
                "rationale": "A concise reason for the current wording.",
                "basis": basis,
                "confidence": "low",
                "expert_review_useful": True,
                "index_metadata": {
                    "human_index_included": True,
                    "occurrence_group_count": 0,
                    "occurrences": [],
                },
            }

        routine = decision("TERM-MORE", "more", "أكثر", "ai-proposed")
        technical = decision(
            "TERM-FINITISTIC", "finitistic reasoning", "الاستدلال التناهي",
            "contextual-extension",
        )
        payload = {"decisions": [routine, technical]}
        rendered = INDEX.render_start_here_markdown(payload, 30)
        self.assertIn("Tier 1 — Check first", rendered)
        self.assertIn("finitistic reasoning", rendered)
        self.assertNotIn("[more]", rendered)
        self.assertIn("Occurrence frequency is **not** a promotion signal", rendered)

    def test_where_prefers_arabic_and_names_every_exact_reader_page(self) -> None:
        def location(kind: str, line: int, pages: list[dict]) -> dict:
            return {
                "source_kind": kind,
                "logical_path": (
                    "content/unit.tex"
                    if kind == "english" else
                    "source/locale/ar/content/unit.tex"
                ),
                "source_url": f"https://example.test/{kind}#L{line}",
                "page_evidence": pages,
                "human_review_included": True,
                "line_reconciliation": {
                    "resolved": True,
                    "status": "verified-recorded-lines-by-hash",
                    "current_line_start": line,
                    "current_line_end": line,
                },
            }

        decision = {
            "decision_id": "TERM-WHERE",
            "edition": "msa",
            "english_term": "term",
            "chosen_arabic": "مصطلح",
            "index_metadata": {
                "occurrences": [
                    {
                        "human_review_included": True,
                        "unit": {"unit_id": "OLP-0001", "title": "Unit title"},
                        "locations": [
                            location("english", 2, []),
                            location(
                                "msa",
                                7,
                                [
                                    {
                                        "reader": "International",
                                        "method": "synctex-exact",
                                        "assembled_pdf_pages": [12],
                                    },
                                    {
                                        "reader": "Machrek",
                                        "method": "synctex-exact",
                                        "assembled_pdf_pages": [13],
                                    },
                                ],
                            ),
                        ],
                    }
                ]
            },
        }
        rendered = INDEX.start_here_where(
            decision, "details.md", arabic_prefix="../../"
        )
        self.assertIn("MSA", rendered)
        self.assertIn("../../source/locale/ar/content/unit.tex#L7", rendered)
        self.assertNotIn("example.test/english", rendered)
        self.assertIn("International final PDF 12", rendered)
        self.assertIn("Machrek final PDF 13", rendered)
        self.assertIn("[+1 more source locations](details.md)", rendered)

    def test_aux_parser_handles_nested_title_and_unicode_page(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            aux = Path(tmp) / "reader.aux"
            aux.write_text(
                r"\newlabel{p:c:s:sec}{{1.2}{٤٢}{عنوان {ذو تفصيل}}{section*.9}{}}" + "\n",
                encoding="utf-8",
            )
            labels = INDEX.parse_aux_labels(aux)
            self.assertEqual(labels["p:c:s:sec"].printed_page, "٤٢")
            self.assertEqual(labels["p:c:s:sec"].title, "عنوان {ذو تفصيل}")
            self.assertEqual(labels["p:c:s:sec"].destination, "section*.9")

    def test_component_synctex_offset_and_unit_start_fallback(self) -> None:
        try:
            from pypdf import PdfWriter
            from pypdf.constants import PageLabelStyle
        except ImportError:  # pragma: no cover - bundled workspace has pypdf
            self.skipTest("pypdf unavailable")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source" / "unit.tex"
            source.parent.mkdir(parents=True)
            source.write_text("first\nterm here\nlast\n", encoding="utf-8")

            component = root / "component.pdf"
            writer = PdfWriter()
            for _ in range(3):
                writer.add_blank_page(width=100, height=100)
            writer.add_named_destination("section*.9", 0)
            writer.set_page_label(0, 2, style=PageLabelStyle.DECIMAL, start=40)
            with component.open("wb") as stream:
                writer.write(stream)

            assembled = root / "assembled.pdf"
            writer = PdfWriter()
            for _ in range(8):
                writer.add_blank_page(width=100, height=100)
            with assembled.open("wb") as stream:
                writer.write(stream)

            aux = root / "component.aux"
            aux.write_text(
                r"\newlabel{p:c:s:sec}{{1.2}{٤٠}{عنوان}{section*.9}{}}" + "\n",
                encoding="utf-8",
            )
            synctex = root / "component.synctex.gz"
            with gzip.open(synctex, "wt", encoding="utf-8") as stream:
                stream.write(
                    "SyncTeX Version:1\n"
                    f"Input:1:{source}\n"
                    "Content:\n"
                    "{2\n"
                    "[1,2:0,0:0,0,0\n"
                    "}2\n"
                )

            reader = INDEX.ReaderEvidence(
                name="Classical closure component",
                source_kind="classical",
                pdf_path=assembled,
                component_pdf_path=component,
                aux_path=aux,
                synctex_path=synctex,
                page_offset=4,
                repo=root,
            )
            unit = INDEX.UnitMeta(
                unit_id="OLP-0001",
                title="عنوان",
                source_role="reader_unit",
                target_path="source/unit.tex",
                aux_label="p:c:s:sec",
            )
            exact_location = {
                "logical_path": "source/unit.tex",
                "_fs_path": source,
                "line_reconciliation": {
                    "resolved": True,
                    "current_line_start": 2,
                    "current_line_end": 2,
                },
            }
            exact = reader.locate(exact_location, unit)
            self.assertEqual(exact["method"], "synctex-exact")
            self.assertEqual(exact["component_pdf_pages"], [2])
            self.assertEqual(exact["assembled_pdf_pages"], [6])
            self.assertEqual(exact["printed_pages"][0]["printed_page"], "41")

            fallback_location = {
                "logical_path": "source/unit.tex",
                "_fs_path": source,
                "line_reconciliation": {
                    "resolved": True,
                    "current_line_start": 3,
                    "current_line_end": 3,
                },
            }
            fallback = reader.locate(fallback_location, unit)
            self.assertEqual(fallback["method"], "unit-start-fallback")
            self.assertFalse(fallback["exact_occurrence_page"])
            self.assertEqual(fallback["component_pdf_pages"], [1])
            self.assertEqual(fallback["assembled_pdf_pages"], [5])
            self.assertEqual(fallback["printed_pages"][0]["printed_page"], "٤٠")

            printed, assembled_pages, grades = INDEX.occurrence_page_cells(
                [
                    {
                        "source_kind": "classical",
                        "line_reconciliation": {"resolved": True},
                        "page_evidence": [exact, fallback],
                    }
                ]
            )
            self.assertIn("41 [exact SyncTeX", printed)
            self.assertIn("٤٠ [unit-start fallback", printed)
            self.assertIn("6 [exact SyncTeX", assembled_pages)
            self.assertIn("5 [unit-start fallback", assembled_pages)
            self.assertIn("exact occurrence page", grades)
            self.assertIn("not exact term page", grades)

    def test_generated_index_is_bilingual_lossless_and_location_expanded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            target = repo / "source/locale/ar-classical/content/unit.tex"
            msa = repo / "source/locale/ar/content/unit.tex"
            target.parent.mkdir(parents=True)
            msa.parent.mkdir(parents=True)
            target.write_text(
                "\\olfileid{p}{c}{s}\n\\olsection{عنوان الوحدة}\nالمصطلح الأول\nالمصطلح الثاني\n",
                encoding="utf-8",
            )
            msa.write_text("مقدمة\nالمصطلح\n", encoding="utf-8")

            baseline_dir = repo / "evidence/classical"
            baseline_dir.mkdir(parents=True)
            units = []
            for number in range(1, 723):
                units.append(
                    {
                        "id": f"OLP-{number:04d}",
                        "source_path": "content/unit.tex",
                        "source_role": "reader_unit",
                        "target_path": "source/locale/ar-classical/content/unit.tex",
                    }
                )
            baseline = baseline_dir / "BASELINE.json"
            baseline.write_text(
                json.dumps(
                    {"source_commit": "a" * 40, "units": units},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            included = {
                "decision_id": "term-choice",
                "edition": "classical",
                "english_term": "technical term",
                "sense": "a precise test sense",
                "chosen_arabic": "المصطلح",
                "rationale": "It preserves the stated distinction.",
                "alternatives": [{"form": "بديل", "reason": "too broad"}],
                "basis": "contextual-extension",
                "confidence": "medium",
                "expert_review_useful": True,
                "expert_question": "Is this established specialist usage?",
                "open_to_correction": True,
                "occurrences": [
                    {
                        "unit_id": "OLP-0001",
                        "classical": {
                            "path": "source/locale/ar-classical/content/unit.tex",
                            "sha256": "0" * 64,
                            "locators": [
                                {"line_start": 3, "line_end": 3, "excerpt": "المصطلح الأول"},
                                {"line_start": 4, "line_end": 4, "excerpt": "المصطلح الثاني"},
                            ],
                        },
                        "msa": {
                            "path": "source/locale/ar/content/unit.tex",
                            "sha256": "0" * 64,
                            "locators": [
                                {"line_start": 2, "line_end": 2, "excerpt": "المصطلح"}
                            ],
                        },
                    }
                ],
            }
            generic = {
                "decision_id": "range-passage-OLP-0001",
                "edition": "classical",
                "english_term": "passage-level exposition and semantic qualification",
                "chosen_arabic": "صياغة المقطع",
                "rationale": "Whole-passage bookkeeping only.",
                "expert_review_useful": True,
                "open_to_correction": True,
                "occurrences": [],
            }
            optional = {
                "decision_id": "term-open",
                "edition": "msa",
                "english_term": "secondary term",
                "sense": "a non-priority test sense",
                "chosen_arabic": "مصطلح ثانوي",
                "rationale": "The recorded wording is adequate but remains open to correction.",
                "alternatives": [],
                "expert_review_useful": False,
                "open_to_correction": True,
                "occurrences": [
                    {
                        "unit_id": "OLP-0002",
                        "msa": {
                            "path": "source/locale/ar/content/unit.tex",
                            "sha256": "0" * 64,
                            "locators": [
                                {"line_start": 2, "line_end": 2, "excerpt": "المصطلح"}
                            ],
                        },
                    }
                ],
            }
            ledger = repo / "ledger.json"
            ledger.write_text(
                json.dumps({"decisions": [included, generic, optional]}, ensure_ascii=False),
                encoding="utf-8",
            )
            output_md = repo / "index.md"
            output_json = repo / "index.json"
            output_start_here_md = repo / "start-here.md"
            output_priority_md = repo / "priority.md"
            output_csv = repo / "occurrences.csv"
            output_reviewer_index_dir = repo / "reviewer-index"
            argv = [
                "--repo", str(repo),
                "--baseline", str(baseline),
                "--ledger", str(ledger),
                "--output-md", str(output_md),
                "--output-json", str(output_json),
                "--output-start-here-md", str(output_start_here_md),
                "--output-priority-md", str(output_priority_md),
                "--output-csv", str(output_csv),
                "--output-reviewer-index-dir", str(output_reviewer_index_dir),
            ]
            with redirect_stdout(io.StringIO()):
                result = INDEX.main(argv)
            self.assertEqual(result, 0)
            payload = json.loads(output_json.read_text(encoding="utf-8"))
            self.assertEqual(payload["summary"]["recorded_decisions"], 3)
            self.assertEqual(payload["summary"]["human_index_decisions"], 2)
            self.assertEqual(payload["summary"]["generic_passage_decisions_omitted"], 1)
            self.assertEqual(payload["summary"]["human_occurrence_records"], 2)
            self.assertEqual(payload["summary"]["human_decisions_without_occurrence"], 0)
            self.assertEqual(payload["summary"]["human_csv_rows"], 2)
            self.assertEqual(payload["summary"]["expert_review_occurrence_records"], 1)
            self.assertEqual(payload["summary"]["human_location_records"], 4)
            self.assertEqual(payload["summary"]["priority_reviewer_shards"], 1)
            self.assertEqual(payload["summary"]["complete_reviewer_shards"], 1)
            self.assertEqual(payload["summary"]["generic_placeholder_location_records"], 0)
            self.assertEqual(
                payload["summary"]["generic_placeholder_unresolved_source_locations"], 0
            )
            generic_out = next(row for row in payload["decisions"] if "passage-OLP" in row["decision_id"])
            self.assertFalse(generic_out["index_metadata"]["human_index_included"])

            markdown = output_md.read_text(encoding="utf-8")
            self.assertIn("Please double-check / يُرجى التحقق", markdown)
            self.assertIn("Why this choice / سبب الاختيار", markdown)
            self.assertIn("source/locale/ar-classical/content/unit.tex", markdown)
            self.assertIn("source/locale/ar/content/unit.tex", markdown)
            self.assertIn("unit.tex#L3", markdown)
            self.assertIn("unit.tex#L4", markdown)
            self.assertIn("unit.tex#L2", markdown)
            self.assertIn("OLP-0001", markdown)
            self.assertIn("عنوان الوحدة", markdown)
            self.assertNotIn("### passage-level exposition", markdown)
            self.assertIn("generic passage placeholders omitted", markdown.casefold())

            priority_markdown = output_priority_md.read_text(encoding="utf-8")
            self.assertIn("technical term", priority_markdown)
            self.assertIn("Please double-check / يُرجى التحقق", priority_markdown)
            self.assertIn("OLP-0001", priority_markdown)
            self.assertIn("unit.tex#L3", priority_markdown)
            self.assertIn("No occurrence supplied in the ledger for", priority_markdown)
            self.assertNotIn("secondary term", priority_markdown)
            self.assertNotIn("passage-level exposition", priority_markdown)

            start_here_markdown = output_start_here_md.read_text(encoding="utf-8")
            self.assertIn("technical choices to double-check", start_here_markdown)
            self.assertIn("Tier 1 — Check first", start_here_markdown)
            self.assertIn("Three review tiers", start_here_markdown)
            self.assertIn("technical term", start_here_markdown)
            shard_anchor = INDEX.decision_anchor(included, "priority-")
            self.assertIn(
                f"reviewer-index/priority-001.md#{shard_anchor}",
                start_here_markdown,
            )
            self.assertIn("First exact place, then +N", start_here_markdown)
            self.assertIn("OLP-0001", start_here_markdown)
            self.assertIn("classical", start_here_markdown)
            self.assertIn("unit.tex#L3", start_here_markdown)
            self.assertNotIn("secondary term", start_here_markdown)

            priority_shard = (
                output_reviewer_index_dir / "priority-001.md"
            ).read_text(encoding="utf-8")
            complete_shard = (
                output_reviewer_index_dir / "complete-001.md"
            ).read_text(encoding="utf-8")
            shard_landing = (
                output_reviewer_index_dir / "README.md"
            ).read_text(encoding="utf-8")
            self.assertIn("PLEASE DOUBLE-CHECK THIS CHOICE", priority_shard)
            self.assertIn("Global rank / score", priority_shard)
            self.assertIn("../source/locale/ar-classical/content/unit.tex#L3", priority_shard)
            self.assertIn("../source/locale/ar-classical/content/unit.tex#L4", priority_shard)
            self.assertIn("../source/locale/ar/content/unit.tex#L2", priority_shard)
            self.assertIn("secondary term", complete_shard)
            self.assertIn("priority-001.md", shard_landing)
            self.assertIn("complete-001.md", shard_landing)
            self.assertLessEqual(
                payload["reviewer_sharding"]["largest_rendered_shard_bytes"],
                INDEX.REVIEWER_SHARD_HARD_LIMIT_BYTES,
            )
            self.assertTrue(
                all(
                    path.stat().st_size <= INDEX.REVIEWER_SHARD_HARD_LIMIT_BYTES
                    for path in output_reviewer_index_dir.glob("priority-*.md")
                )
            )
            self.assertTrue(
                all(
                    path.stat().st_size <= INDEX.REVIEWER_SHARD_HARD_LIMIT_BYTES
                    for path in output_reviewer_index_dir.glob("complete-*.md")
                )
            )

            def assert_local_links_resolve(path: Path) -> None:
                text = path.read_text(encoding="utf-8")
                hrefs = re.findall(r"\]\(([^)]+)\)", text)
                hrefs += re.findall(r"^\[[^]]+\]:\s+(\S+)", text, re.M)
                for href in hrefs:
                    if re.match(r"^(?:https?|mailto):", href):
                        continue
                    if href.startswith("#"):
                        self.assertIn(f'id="{unquote(href[1:])}"', text)
                        continue
                    target_text, _, fragment = unquote(href).partition("#")
                    target = (path.parent / target_text).resolve()
                    self.assertTrue(target.is_file(), f"broken local link {href} in {path}")
                    if fragment and not re.fullmatch(r"L\d+(?:-L\d+)?", fragment):
                        target_markdown = target.read_text(encoding="utf-8")
                        self.assertIn(f'id="{fragment}"', target_markdown)

            assert_local_links_resolve(output_start_here_md)
            for shard_path in output_reviewer_index_dir.glob("*.md"):
                assert_local_links_resolve(shard_path)

            csv_bytes = output_csv.read_bytes()
            self.assertTrue(csv_bytes.startswith(b"\xef\xbb\xbf"))
            csv_rows = list(csv.DictReader(io.StringIO(csv_bytes.decode("utf-8-sig"))))
            self.assertEqual(len(csv_rows), 2)
            self.assertEqual(list(csv_rows[0]), INDEX.CSV_COLUMNS)
            priority_row = next(
                row for row in csv_rows if row[INDEX.CSV_COLUMNS[2]].startswith("technical term")
            )
            self.assertIn("Priority: please double-check", priority_row[INDEX.CSV_COLUMNS[0]])
            self.assertEqual(priority_row[INDEX.CSV_COLUMNS[1]], "term-choice")
            self.assertEqual(priority_row[INDEX.CSV_COLUMNS[3]], "المصطلح")
            self.assertIn("OLP-0001", priority_row[INDEX.CSV_COLUMNS[7]])
            self.assertIn("unit.tex:L3", priority_row[INDEX.CSV_COLUMNS[8]])
            self.assertIn("unit.tex:L4", priority_row[INDEX.CSV_COLUMNS[8]])
            self.assertIn("unit.tex:L2", priority_row[INDEX.CSV_COLUMNS[8]])
            self.assertIn("not counted as an unresolved locator", priority_row[INDEX.CSV_COLUMNS[8]])
            self.assertEqual(priority_row[INDEX.CSV_COLUMNS[9]], "")
            self.assertEqual(priority_row[INDEX.CSV_COLUMNS[10]], "")
            self.assertIn("PDF page unavailable", priority_row[INDEX.CSV_COLUMNS[11]])
            self.assertEqual(
                priority_row[INDEX.CSV_COLUMNS[12]],
                "OLP-0001 (MSA L2; CA L3; CA L4) — Is this established specialist usage?",
            )

            first_priority_bytes = output_priority_md.read_bytes()
            first_start_here_bytes = output_start_here_md.read_bytes()
            first_csv_bytes = output_csv.read_bytes()
            first_full_md_bytes = output_md.read_bytes()
            first_json_bytes = output_json.read_bytes()
            first_shard_bytes = {
                path.name: path.read_bytes()
                for path in sorted(output_reviewer_index_dir.glob("*.md"))
            }
            (output_reviewer_index_dir / "priority-999.md").write_text(
                "stale generated shard\n", encoding="utf-8"
            )
            (output_reviewer_index_dir / "complete-999.md").write_text(
                "stale generated shard\n", encoding="utf-8"
            )
            unrelated_note = output_reviewer_index_dir / "reviewer-notes.md"
            unrelated_note.write_text("retain me\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(INDEX.main(argv), 0)
            self.assertEqual(output_priority_md.read_bytes(), first_priority_bytes)
            self.assertEqual(output_start_here_md.read_bytes(), first_start_here_bytes)
            self.assertEqual(output_csv.read_bytes(), first_csv_bytes)
            self.assertEqual(output_md.read_bytes(), first_full_md_bytes)
            self.assertEqual(output_json.read_bytes(), first_json_bytes)
            self.assertEqual(
                {
                    path.name: path.read_bytes()
                    for path in sorted(output_reviewer_index_dir.glob("*.md"))
                    if path.name != unrelated_note.name
                },
                first_shard_bytes,
            )
            self.assertFalse((output_reviewer_index_dir / "priority-999.md").exists())
            self.assertFalse((output_reviewer_index_dir / "complete-999.md").exists())
            self.assertEqual(
                unrelated_note.read_text(encoding="utf-8"), "retain me\n"
            )


if __name__ == "__main__":
    unittest.main()
