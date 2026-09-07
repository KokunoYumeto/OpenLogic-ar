"""Exact applied-source and mathematical-preservation checks for OLP0034."""
import hashlib
import json
from pathlib import Path
import re
import unittest

from build import validate_classical_overlay as static

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "evidence/classical/repairs/OLP0034_REDUCTION_CONSTRUCTIONS_20260907.json"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def check_location(test, text, location):
    literal = location["literal"]
    test.assertEqual(text.count(literal), 1)
    index = text.index(literal)
    end = index + len(literal)
    test.assertEqual(location["line_start"], text[:index].count("\n") + 1)
    test.assertEqual(location["line_end"], text[:end].count("\n") + 1)
    test.assertEqual(location["byte_start"], len(text[:index].encode("utf-8")))
    test.assertEqual(location["byte_end"], len(text[:end].encode("utf-8")))
    test.assertEqual(text.encode()[location["byte_start"]:location["byte_end"]].decode(), literal)


class ReductionConstructions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER.read_bytes())
        cls.views = {}
        for transaction in cls.ledger["transactions"]:
            before = (REPO / transaction["before_path"]).read_bytes()
            after = (REPO / transaction["path"]).read_bytes()
            cls.views[transaction["edition"]] = (before, after)

    def test_exact_inventory_and_live_hashes(self):
        self.assertEqual(len(self.ledger["decisions"]), 4)
        self.assertEqual(len(self.ledger["transactions"]), 2)
        self.assertEqual(sum(len(t["patches"]) for t in self.ledger["transactions"]), 4)
        for t in self.ledger["transactions"]:
            for phase, raw in zip(("before", "after"), self.views[t["edition"]]):
                self.assertEqual((sha(raw), len(raw)), (t[phase + "_sha256"], t[phase + "_bytes"]))
        self.assertEqual(self.ledger["english_source"]["sha256"], "33f0cbb35c8c1fa3ff0e4f44fa626fdc298d1c4612aeaafb41bcb920e5d18ac8")

    def test_exact_replay_both_directions_and_every_patch_location(self):
        for t in self.ledger["transactions"]:
            before, after = (raw.decode() for raw in self.views[t["edition"]])
            forward, inverse = before, after
            for p in t["patches"]:
                check_location(self, before, p["before_location"])
                check_location(self, after, p["after_location"])
                self.assertEqual(forward.count(p["before"]), 1)
                forward = forward.replace(p["before"], p["after"], 1)
            for p in reversed(t["patches"]):
                self.assertEqual(inverse.count(p["after"]), 1)
                inverse = inverse.replace(p["after"], p["before"], 1)
            self.assertEqual(forward, after)
            self.assertEqual(inverse, before)

    def test_all_formulas_references_macros_and_exercises_unchanged(self):
        for edition, pair in self.views.items():
            before, after = (raw.decode() for raw in pair)
            result = static.compare(before, after)
            self.assertEqual(result["failures"], [], (edition, result))
            self.assertEqual(result["declared_exceptions"], [])
            self.assertTrue(all(result["checks"].values()))
            a, b = static.analyze(before), static.analyze(after)
            self.assertEqual([(k, static.raw_body(a, t)) for k, t in a.formulas],
                             [(k, static.raw_body(b, t)) for k, t in b.formulas])
            self.assertEqual((a.keys, a.terminology, a.formal_commands), (b.keys, b.terminology, b.formal_commands))
            self.assertEqual(before.count(r"\begin{prob}"), 7)
            self.assertEqual(re.findall(r"\\begin\{prob\}[\s\S]*?\\end\{prob\}", before),
                             re.findall(r"\\begin\{prob\}[\s\S]*?\\end\{prob\}", after))

    def test_english_and_current_occurrence_witnesses(self):
        source = self.ledger["english_source"]
        raw = Path(source["path"]).read_bytes()
        self.assertEqual((sha(raw), len(raw)), (source["sha256"], source["bytes"]))
        for decision in self.ledger["decisions"]:
            self.assertTrue(decision["open_to_correction"])
            self.assertEqual(decision["recording_mode"], "contemporaneous-repair-reasons")
            self.assertTrue(decision["rationale"] and decision["rationale_arabic"] and decision["expert_question"])
            o = decision["occurrences"][0]
            check_location(self, raw.decode(), o["english"])
            after = self.views[decision["edition"]][1]
            self.assertEqual(sha(after), o["target_sha256"])
            check_location(self, after.decode(), o)
            self.assertIsNone(o["printed_page"])

    def test_codomain_notes_and_previous_source_repairs_survive(self):
        for before, after in self.views.values():
            text = after.decode()
            self.assertEqual(text.count("مع أن المجال المقابل"), 1)
            self.assertNotIn("مع أن المدى", text)
            self.assertIn(r"h(n) = \underbrace{00\dots0}_{\text{$n$ أصفار}}111\dots", text)
            self.assertIn(r"h\colon \PosInt \to \Bin^\omega", text)
            old_note = re.search(r"\\begin\{editorial\}(?:(?!\\end\{editorial\})[\s\S])*OLSIZ-004(?:(?!\\end\{editorial\})[\s\S])*\\end\{editorial\}", before.decode())
            self.assertIsNotNone(old_note)
            self.assertIn(old_note[0], text)
            # Universal source argument: n is positive, hence position1 is in
            # the zero prefix for every n, while the constant-one sequence has1.
            self.assertIn("positive input n implies h(n)(1)=0", " ".join(self.ledger["semantic_invariants"]))

    def test_four_human_guide_locations_and_reasons(self):
        guide = LEDGER.with_suffix(".md").read_text(encoding="utf-8")
        links = re.findall(r"\]\(\.\./\.\./\.\./([^#]+)#L(\d+)\)", guide)
        self.assertEqual(len(links), 4)
        for decision in self.ledger["decisions"]:
            self.assertIn(decision["decision_id"], guide)
            self.assertIn(decision["rationale_arabic"], guide)
            self.assertIn(decision["expert_question"], guide)
            o = decision["occurrences"][0]
            self.assertIn((o["target_path"], str(o["line_start"])), links)


if __name__ == "__main__":
    unittest.main()
