"""Finite source/semantic checks for the consolidated modal repair batch.

No TeX, subprocess, export, network, or central metadata writes. Infinite claims
are justified by the ledger's algebraic proofs, not by these finite tests alone.
"""
from pathlib import Path
from fractions import Fraction
import hashlib
import importlib.util
import json
import re
import sys
import unittest

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "evidence/classical/repairs/OLP0394_0399_0400_0404_0409_MODAL_SCOPE_20260907.json"
SPEC = importlib.util.spec_from_file_location("modal_scope_static", REPO / "build/validate_classical_overlay.py")
STATIC = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = STATIC
SPEC.loader.exec_module(STATIC)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def imp(a, b):
    return min(Fraction(1), 1 - a + b)


def eq(a, b):
    return min(imp(a, b), imp(b, a))


def twice(a):
    return imp(1 - a, a)


class ModalScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(LEDGER.read_bytes())
        cls.transactions = {t["path"]: t for t in cls.data["transactions"]}
        cls.before, cls.after = {}, {}
        for row in cls.data["primary_source_inventory"]:
            raw = (REPO / row["path"]).read_bytes()
            cls.after[row["path"]] = raw
            for patch in reversed(cls.transactions.get(row["path"], {}).get("patches", [])):
                a, b = patch["after"].encode(), patch["before"].encode()
                if raw.count(a) != 1:
                    raise AssertionError("Nonunique inverse: " + row["path"])
                raw = raw.replace(a, b, 1)
            cls.before[row["path"]] = raw

    def test_exact_finite_scope_and_all_fifteen_source_identities(self):
        self.assertEqual(len(self.transactions), 10)
        self.assertEqual(sum(len(t["patches"]) for t in self.transactions.values()), 15)
        self.assertEqual(len(self.data["decisions"]), 6)
        self.assertEqual(len(self.data["primary_source_inventory"]), 15)
        self.assertEqual({t["edition"] for t in self.transactions.values()}, {"msa", "classical"})
        for row in self.data["primary_source_inventory"]:
            for phase, objects in (("before", self.before), ("after", self.after)):
                raw = objects[row["path"]]
                self.assertEqual((len(raw), sha(raw)), (row[phase + "_bytes"], row[phase + "_sha256"]))
            if row["edition"] == "english":
                self.assertEqual(self.before[row["path"]], self.after[row["path"]])

    def test_every_exact_patch_location_and_full_forward_replay(self):
        for tx in self.transactions.values():
            with self.subTest(path=tx["path"]):
                replay = self.before[tx["path"]]
                for patch in tx["patches"]:
                    self.assertEqual(replay.count(patch["before"].encode()), 1)
                    replay = replay.replace(patch["before"].encode(), patch["after"].encode(), 1)
                    for phase, objects in (("before", self.before), ("after", self.after)):
                        raw, loc = objects[tx["path"]], patch[phase + "_location"]
                        self.assertEqual(raw[loc["byte_start"]:loc["byte_end"]], patch[phase].encode())
                        self.assertEqual(raw[:loc["byte_start"]].count(b"\n") + 1, loc["line_start"])
                        self.assertEqual(raw[:loc["byte_end"] - 1].count(b"\n") + 1, loc["line_end"])
                        self.assertEqual("\n".join(raw.decode().splitlines()[loc["line_start"] - 1:loc["line_end"]]), loc["excerpt"])
                self.assertEqual(replay, self.after[tx["path"]])

    def test_exactly_two_declared_types_of_formal_change(self):
        self.assertEqual({r["unit_id"] for r in self.data["formal_change_allowlist"]}, {"OLP-0394", "OLP-0399"})
        for tx in self.transactions.values():
            before, after = self.before[tx["path"]].decode(), self.after[tx["path"]].decode()
            normalized = after
            if tx["unit_id"] in {"OLP-0394", "OLP-0399"}:
                self.assertEqual(len(tx["patches"]), 1)
                patch = tx["patches"][0]
                if tx["unit_id"] == "OLP-0394":
                    self.assertEqual(patch["after"].splitlines()[-1], patch["before"].replace(r"= \Undef$", r"= \False$"))
                else:
                    self.assertEqual(patch["after"], r"النظر أيضًا، لكل عدد طبيعي~$m\ge2$، في المجموعات الجزئية}")
                normalized = normalized.replace(patch["after"], patch["before"], 1)
            report = STATIC.compare(before, normalized)
            self.assertEqual(report["failures"], [], tx["path"])
            self.assertEqual(report["declared_exceptions"], [])
            self.assertTrue(all(report["checks"].values()), report)
            a, b = STATIC.analyze(before), STATIC.analyze(normalized)
            self.assertEqual([(k, STATIC.raw_body(a, t)) for k, t in a.formulas],
                             [(k, STATIC.raw_body(b, t)) for k, t in b.formulas], tx["path"])

    def test_thirty_one_prior_quotes_remain_exact_historical_witnesses(self):
        count = 0
        for decision in self.data["decisions"]:
            for witness in decision["primary_evidence_before"]:
                path = witness["path"]
                key = path[len(REPO.as_posix()) + 1:] if path.startswith(REPO.as_posix() + "/") else path
                raw = self.before.get(key)
                if raw is None:
                    raw = Path(path).read_bytes()
                self.assertEqual((len(raw), sha(raw)), (witness["bytes"], witness["sha256"]))
                self.assertEqual("\n".join(raw.decode().splitlines()[witness["start_line"] - 1:witness["end_line"]]), witness["quote"])
                count += 1
        self.assertEqual(count, 31)

    def test_review_choices_have_reasons_questions_and_live_locations(self):
        seen = set()
        for d in self.data["decisions"]:
            self.assertTrue(d["open_to_correction"])
            self.assertFalse(d["human_response_is_gate"])
            self.assertIsNone(d["printed_page"])
            for field in ("rationale", "expert_question", "reader_prompt_ar", "propagation"):
                self.assertTrue(d[field].strip(), field)
            self.assertEqual(d["authority_checks"][1]["result"], "not-consulted-for-this-semantic-correction")
            self.assertTrue(d["occurrence_bindings"])
            for o in d["occurrence_bindings"]:
                tx = self.transactions[o["path"]]
                patch = tx["patches"][o["patch_index"]]
                self.assertEqual(o["sha256"], tx["after_sha256"])
                self.assertEqual(o["location"], patch["after_location"])
                self.assertEqual(o["chosen_arabic"], patch["after"])
                self.assertIn(d["decision_id"], patch["decision_ids"])
                seen.add((o["path"], o["patch_index"]))
        self.assertEqual(len(seen), 15)

    def test_semantic_definitions_do_not_impose_finite_premises(self):
        self.assertEqual(len(self.data["proof_support"]), 2)
        for row in self.data["proof_support"]:
            raw = Path(row["path"]).read_bytes()
            self.assertEqual((len(raw), sha(raw)), (row["bytes"], row["sha256"]))
            self.assertIn(r"If $\Gamma$ is a set of !!{formula}s", raw.decode())
        proof = self.data["mathematical_disposition"]["F03"]
        self.assertIn("by contraposition", proof["finite_premise_proof"])
        self.assertIn("not claimed necessary", proof["scope"])

    def test_human_guide_has_all_fifteen_actual_word_locations(self):
        guide = LEDGER.with_suffix(".md")
        text = guide.read_text(encoding="utf-8")
        links = re.findall(r"\]\(([^)]+\.tex)#L(\d+)\)", text)
        expected = set()
        for tx in self.transactions.values():
            for p in tx["patches"]:
                # Point to the words/formula, not to the preceding correction comment.
                line = p["after_location"]["line_start"] + int(p["after"].startswith("%"))
                expected.add((tx["path"], line))
        actual = set()
        for relative, line in links:
            path = (guide.parent / relative).resolve()
            self.assertTrue(path.is_relative_to(REPO / "source/locale"))
            literal_line = path.read_text(encoding="utf-8").splitlines()[int(line) - 1]
            self.assertTrue(literal_line.strip())
            self.assertFalse(literal_line.lstrip().startswith("%"))
            actual.add((path.relative_to(REPO).as_posix(), int(line)))
        self.assertEqual(len(links), 15)
        self.assertEqual(actual, expected)
        for decision in self.data["decisions"]:
            self.assertIn(decision["decision_id"], text)
            self.assertIn(decision["reader_prompt_ar"], text)

    def test_global_necessity_does_not_make_atomic_truth_world_invariant(self):
        worlds, true_at = {0, 1}, {0}
        atomic = {w: w in true_at for w in worlds}
        global_necessity = {w: all(v in true_at for v in worlds) for w in worlds}
        self.assertNotEqual(atomic[0], atomic[1])
        self.assertEqual(global_necessity[0], global_necessity[1])
        self.assertFalse(global_necessity[0])

    def test_three_valued_counterexample_from_recorded_tables(self):
        u = Fraction(1, 2)
        neg = lambda x: 1 - x
        possibility = lambda x: Fraction(int(x > 0))
        self.assertEqual(neg(u), u)
        self.assertEqual(min(u, neg(u)), u)
        self.assertEqual(possibility(min(u, neg(u))), 1)
        self.assertEqual(neg(possibility(min(u, neg(u)))), 0)
        ca = next(p for p in self.after if p.startswith("source/locale/ar-classical/") and "/three-valued-logics/" in p)
        raw = self.after[ca].decode()
        self.assertIn(r"$\Undef$ & $\True$", raw)
        self.assertIn(r"$\Undef$ & $\Undef$", raw)
        self.assertIn(r"$\pValue v(\lnot \Diamond(p \land \lnot p)) = \False$", raw)

    def test_grid_cardinality_closure_and_zero_boundary(self):
        for m in range(2, 17):
            grid = {Fraction(n, m - 1) for n in range(m)}
            self.assertEqual(len(grid), m)
            self.assertEqual((min(grid), max(grid)), (0, 1))
            for a in grid:
                self.assertIn(1 - a, grid)
                for b in grid:
                    for value in (min(a, b), max(a, b), imp(a, b)):
                        self.assertIn(value, grid)
                    self.assertEqual(eq(a, b) == 1, a == b)
        with self.assertRaises(ZeroDivisionError):
            Fraction(0, 1 - 1)
        for tx in self.transactions.values():
            if tx["unit_id"] == "OLP-0399":
                text = self.after[tx["path"]].decode()
                self.assertIn(r"m>0", text)
                self.assertIn(r"n<m", text)
                self.assertIn(r"$m\ge2$", text)

    def test_dyadic_constraints_and_missing_finite_grid_values(self):
        p = {i: Fraction(1, 2 ** i) for i in range(1, 65)}
        self.assertEqual(eq(p[1], 1 - p[1]), 1)
        for i in range(1, 64):
            self.assertEqual(eq(p[i], twice(p[i + 1])), 1)
            self.assertLess(p[i], 1)
        for m in range(2, 100):
            i = (m - 1).bit_length()
            self.assertGreater(p[i], 0)
            self.assertLess(p[i], Fraction(1, m - 1))
            self.assertNotIn(p[i], {Fraction(n, m - 1) for n in range(m)})

    def test_modal_order_has_a_concrete_distinguishing_frame(self):
        # w->u and u->{v,z}; only v satisfies p. Every world has a successor,
        # so this separates the orders without relying on dead-end vacuity.
        edges = {"w": {"u"}, "u": {"v", "z"}, "v": {"v"}, "z": {"z"}}
        p = {"v"}
        box = lambda s: {w for w, targets in edges.items() if targets <= s}
        diamond = lambda s: {w for w, targets in edges.items() if targets & s}
        self.assertIn("w", box(diamond(p)))
        self.assertNotIn("w", diamond(box(p)))
        self.assertNotEqual(box(diamond(p)), diamond(box(p)))
        for tx in self.transactions.values():
            if tx["unit_id"] == "OLP-0409":
                text = self.after[tx["path"]].decode()
                self.assertIn("من الضروري أن يكون من الممكن أن تمطر", text)
                self.assertIn(r"من الممكن أن يكون من الضروري \ldots", text)
                self.assertIn("صدق عبارة الضرورة في عالم", text)

    def test_n_sequent_empty_premises_has_exact_designated_slots(self):
        for n in range(2, 6):
            for mask in range(1, 2 ** n - 1):
                designated = {i for i in range(n) if mask & (1 << i)}
                theorem = [("A",) if i in designated else () for i in range(n)]
                self.assertNotEqual(theorem, [("A",)] * n)
                for i, slot in enumerate(theorem):
                    self.assertEqual(slot, ("A",) if i in designated else ())
        for tx in self.transactions.values():
            if tx["unit_id"] == "OLP-0404":
                text = self.after[tx["path"]].decode()
                self.assertIn("وتخلو سائر المواضع. ونكتب", text)
                self.assertIn(r"تحتوي~$!A$ وحدها", text)


if __name__ == "__main__":
    unittest.main()
