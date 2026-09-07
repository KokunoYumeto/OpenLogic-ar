"""Read-only proofs for seven saved function-prose patches; no TeX/export.

Whole-file bytes, exact inverse/forward replay and literal witnesses are checked
independently of the ledger's reported status. Finite examples supplement, not
replace, the elementary arguments and do not certify the complete edition.
"""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import re
import sys
import unittest

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "evidence/classical/repairs/OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907.json"
SPEC = importlib.util.spec_from_file_location(
    "function_constructions_static", REPO / "build/validate_classical_overlay.py"
)
STATIC = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = STATIC
SPEC.loader.exec_module(STATIC)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def lines(raw, start, end):
    return "\n".join(raw.decode("utf-8").splitlines()[start - 1:end])


def exact_replace(raw, old, new):
    old, new = old.encode("utf-8"), new.encode("utf-8")
    if raw.count(old) != 1:
        raise ValueError("Expected exactly one literal replacement")
    return raw.replace(old, new, 1)


class FunctionConstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(LEDGER.read_bytes())
        cls.transactions = {x["path"]: x for x in cls.data["transactions"]}
        cls.before, cls.after, cls.live = {}, {}, {}
        for row in cls.data["primary_source_inventory"]:
            raw = (REPO / row["path"]).read_bytes()
            cls.live[row["path"]] = raw
            if sha(raw) != row["after_sha256"]:
                # One separately recorded successor changes the opening, not
                # these seven saved patches. Recover this transaction's stage
                # by an exact, hash-pinned inverse, never by relaxing hashes.
                if (row["path"] != "source/locale/ar-classical/content/sets-functions-relations/functions/function-kinds.tex"
                        or sha(raw) != "3a74dd4fc979afc520df1954cc09c78327ac63c6954852f77e0a8cb9b9a38922"):
                    raise AssertionError("Unrecognized later source transition: " + row["path"])
                raw = exact_replace(raw,
                    "وتسمى هذه الدوال !!{surjective}، وصورتها",
                    "هذا الصنف\nيسمى !!{surjective}، وصورته")
                if sha(raw) != row["after_sha256"]:
                    raise AssertionError("Opening inverse does not recover recorded phase")
            cls.after[row["path"]] = raw
            for patch in reversed(cls.transactions.get(row["path"], {}).get("patches", [])):
                raw = exact_replace(raw, patch["after"], patch["before"])
            cls.before[row["path"]] = raw

    def assert_location(self, raw, loc, literal):
        self.assertGreaterEqual(loc["line_start"], 1)
        self.assertGreaterEqual(loc["line_end"], loc["line_start"])
        self.assertLessEqual(loc["line_end"], len(raw.decode().splitlines()))
        self.assertEqual(lines(raw, loc["line_start"], loc["line_end"]), loc["excerpt"])
        self.assertGreaterEqual(loc["byte_start"], 0)
        self.assertLessEqual(loc["byte_end"], len(raw))
        self.assertGreater(loc["byte_end"], loc["byte_start"])
        self.assertEqual(raw[loc["byte_start"]:loc["byte_end"]], literal.encode("utf-8"))

    def test_exact_immutable_ledger_identity_and_scope(self):
        raw = (LEDGER.parent / "history" / (LEDGER.stem + ".pre-verification.json")).read_bytes()
        self.assertEqual(len(raw), 135848)
        self.assertEqual(sha(raw), "47f5c3d9b26fd81ff1c42f3dfaa8baaec6ba44c2240477465c2fe64756c288b1")
        self.assertEqual(len(self.data["primary_source_inventory"]), 12)
        self.assertEqual(len(self.transactions), 3)
        self.assertEqual(sum(len(t["patches"]) for t in self.transactions.values()), 7)
        self.assertEqual({t["unit_id"] for t in self.transactions.values()},
                         {"OLP-0021", "OLP-0022", "OLP-0024"})
        self.assertEqual({t["edition"] for t in self.transactions.values()}, {"classical"})

    def test_owner_amendment_changes_only_proved_witness_and_dependency(self):
        old = json.loads((LEDGER.parent / "history" / (LEDGER.stem + ".pre-verification.json")).read_bytes())
        revised = copy.deepcopy(self.data)
        correction = revised.pop("owner_verification")
        current_binding = revised["dependent_choices"][0].pop("current_binding")
        self.assertEqual(correction["prior_ledger"]["sha256"],
                         "47f5c3d9b26fd81ff1c42f3dfaa8baaec6ba44c2240477465c2fe64756c288b1")
        old["decisions"][4]["literal_review_occurrences"][0]["english"]["line_end"] = 118
        witness = old["decisions"][4]["source_witnesses"][0]
        self.assertEqual(witness["line_end"], 119)
        self.assertTrue(witness["excerpt"].endswith("\n"))
        witness["line_end"] = 118
        witness["excerpt"] = witness["excerpt"][:-1]
        self.assertEqual(revised, old)
        raw = self.after[current_binding["path"]]
        self.assertEqual(sha(raw), current_binding["sha256"])
        self.assertEqual(raw[current_binding["byte_start"]:current_binding["byte_end"]],
                         current_binding["text"].encode())
        self.assertEqual(raw[:current_binding["byte_start"]].count(b"\n") + 1,
                         current_binding["line_start"])
        self.assertEqual(raw[:current_binding["byte_end"] - 1].count(b"\n") + 1,
                         current_binding["line_end"])

    def test_all_twelve_complete_file_identities_and_forward_replay(self):
        for row in self.data["primary_source_inventory"]:
            with self.subTest(path=row["path"]):
                for phase, inventory in (("before", self.before), ("after", self.after)):
                    raw = inventory[row["path"]]
                    self.assertEqual((len(raw), sha(raw)),
                                     (row[phase + "_bytes"], row[phase + "_sha256"]))
                replay = self.before[row["path"]]
                for patch in self.transactions.get(row["path"], {}).get("patches", []):
                    replay = exact_replace(replay, patch["before"], patch["after"])
                self.assertEqual(replay, self.after[row["path"]])
                if row["path"] not in self.transactions:
                    self.assertEqual(self.before[row["path"]], self.after[row["path"]])

    def test_exact_patch_bytes_line_locations_and_decision_ownership(self):
        ids = {d["decision_id"] for d in self.data["decisions"]}
        covered = set()
        for tx in self.transactions.values():
            with self.subTest(path=tx["path"]):
                for phase, inventory in (("before", self.before), ("after", self.after)):
                    raw = inventory[tx["path"]]
                    self.assertEqual((len(raw), sha(raw)),
                                     (tx[phase + "_bytes"], tx[phase + "_sha256"]))
                    for patch in tx["patches"]:
                        self.assertEqual(patch["occurrences"], 1)
                        self.assert_location(raw, patch[phase + "_location"], patch[phase])
                        self.assertTrue(set(patch["decision_ids"]) <= ids)
                        covered.update(patch["decision_ids"])
        self.assertEqual(covered, ids)

    def test_no_mathematics_reference_token_or_comment_changes(self):
        for tx in self.transactions.values():
            with self.subTest(path=tx["path"]):
                before, after = self.before[tx["path"]].decode(), self.after[tx["path"]].decode()
                comparison = STATIC.compare(before, after)
                self.assertEqual(comparison["failures"], [])
                self.assertTrue(all(comparison["checks"].values()), comparison)
                self.assertEqual(comparison["declared_exceptions"], [])
                a, b = STATIC.analyze(before), STATIC.analyze(after)
                self.assertEqual([(k, STATIC.raw_body(a, t)) for k, t in a.formulas],
                                 [(k, STATIC.raw_body(b, t)) for k, t in b.formulas])
                for field in ("keys", "terminology", "formal_commands"):
                    self.assertEqual(getattr(a, field), getattr(b, field), field)
                self.assertEqual([x for x in before.splitlines() if x.lstrip().startswith("%")],
                                 [x for x in after.splitlines() if x.lstrip().startswith("%")])

    def test_every_source_witness_exact_bytes_and_separate_line_context(self):
        count = 0
        for d in self.data["decisions"]:
            self.assertEqual({w["edition"] for w in d["source_witnesses"]},
                             {"english", "classical"})
            for witness in d["source_witnesses"]:
                with self.subTest(decision=d["decision_id"], phase=witness["phase"]):
                    raw = (self.before if witness["phase"] == "before" else self.after)[witness["path"]]
                    self.assertEqual((len(raw), sha(raw)), (witness["bytes"], witness["sha256"]))
                    # English CRLF byte slices are not silently normalized; the
                    # separately declared excerpt is a LF-normalized line window.
                    self.assert_location(raw, witness, witness["literal"])
                    self.assertIsNone(witness["printed_page"])
                    count += 1
        self.assertEqual(count, 20)

    def test_all_six_protected_passages_preserve_exact_bytes(self):
        self.assertEqual(len(self.data["preserved_passages"]), 6)
        for p in self.data["preserved_passages"]:
            for phase, inventory in (("before", self.before), ("after", self.after)):
                with self.subTest(label=p["label"], phase=phase):
                    raw = inventory[p["path"]]
                    self.assertEqual(sha(raw), p[phase + "_sha256"])
                    self.assert_location(raw, p[phase + "_location"], p["literal"])

    def test_six_complete_provisional_review_records_and_occurrences(self):
        decisions = self.data["decisions"]
        self.assertEqual(len(decisions), 6)
        self.assertEqual(len({d["decision_id"] for d in decisions}), 6)
        for d in decisions:
            self.assertTrue(d["open_to_correction"])
            self.assertTrue(d["expert_review_useful"])
            self.assertFalse(d["human_response_is_gate"])
            self.assertIsNone(d["printed_page"])
            self.assertEqual(d["recording_mode"], "contemporaneous")
            for field in ("english_term", "chosen_arabic", "rationale", "sense",
                          "grammatical_realization", "expert_question", "expert_review_reason"):
                self.assertTrue(d[field].strip(), field)
            self.assertTrue(d["alternatives"])
            self.assertEqual(d["authority_checks"][-1]["result"], "not-checked")
            self.assertIn("not independently reinspected", d["authority_checks"][1]["note"])
            for occurrence in d["occurrence_bindings"]:
                tx = self.transactions[occurrence["path"]]
                self.assertEqual(occurrence["sha256"], tx["after_sha256"])
                self.assertEqual(occurrence["locations"],
                                 [tx["patches"][i]["after_location"] for i in occurrence["patch_indices"]])

    def test_supported_dependent_choice_is_preserved_and_rebindable(self):
        self.assertEqual(len(self.data["dependent_choices"]), 1)
        d = self.data["dependent_choices"][0]
        self.assertEqual(d["choice_id"], "AR-OLP-0022-CLASSICAL-015")
        self.assertEqual(d["status"], "supported")
        self.assertFalse(d["counts_as_new_defect"])
        self.assertTrue(d["preserve_prior_status_and_reason"])
        self.assertTrue(d["rebind_required"])
        self.assertTrue(d["justification"])
        tx = next(t for t in self.transactions.values() if t["unit_id"] == "OLP-0022")
        old = d["target"]
        self.assertEqual(old["sha256"], sha(self.before[tx["path"]]))
        self.assertEqual(self.before[tx["path"]][old["byte_start"]:old["byte_end"]], old["text"].encode())
        replacement = tx["patches"][1]
        current = exact_replace(old["text"].encode(), replacement["before"], replacement["after"])
        self.assertEqual(self.after[tx["path"]].count(current), 1)
        self.assertIn(d["choice_id"], replacement["source_choice_ids"])

    def test_readable_guide_all_seven_locations_six_ids_and_questions(self):
        guide = LEDGER.with_suffix(".md")
        text = guide.read_text(encoding="utf-8")
        links = re.findall(r"\]\(([^)]+\.tex)#L(\d+)\)", text)
        actual = set()
        for relative, line in links:
            path = (guide.parent / relative).resolve()
            self.assertTrue(path.is_relative_to(REPO / "source/locale/ar-classical"))
            self.assertTrue(path.read_text(encoding="utf-8").splitlines()[int(line) - 1].strip())
            actual.add((path.relative_to(REPO).as_posix(), int(line)))
        expected = set()
        for tx in self.transactions.values():
            raw = self.live[tx["path"]]
            for patch in tx["patches"]:
                literal = patch["after"].encode()
                self.assertEqual(raw.count(literal), 1)
                expected.add((tx["path"], raw[:raw.index(literal)].count(b"\n") + 1))
        self.assertEqual(len(links), 7)
        self.assertEqual(actual, expected)
        for d in self.data["decisions"]:
            self.assertIn(d["decision_id"], text)
            self.assertIn(d["expert_question"], text)

    def test_nested_successor_and_piecewise_examples_including_zero(self):
        basics = next(p for p in self.after if p.startswith("source/locale/ar-classical/")
                      and p.endswith("/function-basics.tex"))
        kinds = next(p for p in self.after if p.startswith("source/locale/ar-classical/")
                     and p.endswith("/function-kinds.tex"))
        self.assertIn(b"g(x) = x+2-1", self.after[basics])
        self.assertIn(br"\frac{x}{2}", self.after[kinds])
        self.assertIn(br"\frac{x+1}{2}", self.after[kinds])
        def piecewise(x):
            return x // 2 if x % 2 == 0 else (x + 1) // 2
        for x in range(1001):
            self.assertEqual(((x + 1) + 1) - 1, x + 1)
            self.assertEqual(piecewise(2 * x), x)
        self.assertEqual(piecewise(0), 0)
        self.assertEqual(piecewise(1), piecewise(2))
        # These finite checks accompany the ledger's quantified argument 2y -> y.

    def test_inverse_rejects_missing_or_ambiguous_literal(self):
        with self.assertRaises(ValueError):
            exact_replace(b"old old", "old", "new")
        with self.assertRaises(ValueError):
            exact_replace(b"unrelated", "old", "new")


if __name__ == "__main__":
    unittest.main()
