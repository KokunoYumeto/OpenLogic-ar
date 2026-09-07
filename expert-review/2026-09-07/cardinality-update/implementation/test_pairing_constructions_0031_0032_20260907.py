"""Strict candidate/live-source modes for the seven-decision pairing batch.

OPENLOGIC_PAIRING_TEST_MODE=candidate: require exact pre-repair live
bytes and validate proposed after bytes in memory. This is not applied PASS.
OPENLOGIC_PAIRING_TEST_MODE=applied (default): require exact post-repair live bytes, then
reverse them to the predecessor. Never silently fall back to candidate mode.
No source writes, TeX, subprocess, export or network operations are performed.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import re
import sys
import unittest


REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "evidence/classical/repairs/OLP0031_0032_PAIRING_CONSTRUCTIONS_20260907.json"
SPEC = importlib.util.spec_from_file_location(
    "pairing_construction_static", REPO / "build/validate_classical_overlay.py"
)
STATIC = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = STATIC
SPEC.loader.exec_module(STATIC)
MODE = os.environ.get("OPENLOGIC_PAIRING_TEST_MODE", "applied")
INTAKE_SHA = "f59121db6aeaedaf81c35a25a9877fdbf384164e98bbbfb6df9f248da7d283bd"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def exact_identity(raw, expected_hash, expected_bytes, label):
    if (sha(raw), len(raw)) != (expected_hash, expected_bytes):
        raise AssertionError(label + ": exact live-source identity mismatch")


def replay(text, patches, inverse=False):
    for patch in reversed(patches) if inverse else patches:
        old, new = (patch["after"], patch["before"]) if inverse else (patch["before"], patch["after"])
        if text.count(old) != 1:
            raise AssertionError("Nonunique exact patch: " + patch["patch_id"])
        text = text.replace(old, new, 1)
    return text


def source_pair(transaction, raw, mode):
    """Require the requested live state before constructing any other view."""
    if mode not in {"candidate", "applied"}:
        raise ValueError("OPENLOGIC_PAIRING_TEST_MODE must be candidate or applied")
    if mode == "candidate":
        exact_identity(raw, transaction["before_sha256"], transaction["before_bytes"], "candidate mode")
        before = raw.decode("utf-8")
        after = replay(before, transaction["patches"])
    else:
        exact_identity(raw, transaction["after_sha256"], transaction["after_bytes"], "applied mode")
        after = raw.decode("utf-8")
        before = replay(after, transaction["patches"], inverse=True)
    exact_identity(before.encode(), transaction["before_sha256"], transaction["before_bytes"], "inverse")
    exact_identity(after.encode(), transaction["after_sha256"], transaction["after_bytes"], "forward")
    return before, after


def location(text, literal):
    if text.count(literal) != 1:
        raise AssertionError("Nonunique witness literal")
    start = text.index(literal)
    end = start + len(literal)
    first, last = text[:start].count("\n") + 1, text[:end].count("\n") + 1
    return {
        "line_start": first, "line_end": last,
        "byte_start": len(text[:start].encode()), "byte_end": len(text[:end].encode()),
        "literal": literal, "excerpt": "\n".join(text.splitlines()[first-1:last]),
    }


class PairingConstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if MODE not in {"candidate", "applied"}:
            raise ValueError("Explicit mode must be candidate or applied")
        cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        cls.transactions = {t["path"]: t for t in cls.ledger["transactions"]}
        cls.before, cls.after, cls.live = {}, {}, {}
        for row in cls.ledger["primary_source_inventory"]:
            path = Path(row["path"])
            raw = (path if path.is_absolute() else REPO / path).read_bytes()
            cls.live[row["path"]] = raw
            if row["path"] in cls.transactions:
                before, after = source_pair(cls.transactions[row["path"]], raw, MODE)
            else:
                exact_identity(raw, row["before_sha256"], row["before_bytes"], "unchanged input")
                before = after = raw.decode("utf-8")
            cls.before[row["path"]], cls.after[row["path"]] = before, after
        if MODE == "candidate":
            print("MODE candidate: exact pre-repair live sources; proposed after bytes simulated. NOT live-source applied PASS.", file=sys.stderr)
        else:
            print("MODE applied: all four live files match exact after hashes. No candidate fallback.", file=sys.stderr)

    def test_seven_decisions_eight_patches_four_targets(self):
        self.assertEqual(len(self.ledger["decisions"]), 7)
        self.assertEqual(len(self.transactions), 4)
        self.assertEqual(sum(len(t["patches"]) for t in self.transactions.values()), 8)
        self.assertEqual(len(self.ledger["primary_source_inventory"]), 7)
        self.assertEqual({(t["unit_id"], t["edition"]) for t in self.transactions.values()},
                         {("OLP-0031", "msa"), ("OLP-0031", "classical"),
                          ("OLP-0032", "msa"), ("OLP-0032", "classical")})
        self.assertEqual({d["decision_id"] for d in self.ledger["decisions"]}, {
            "AR-OLP-0031-MSA-ARABIC-ORDINAL-20260907",
            "AR-OLP-0031-CLASSICAL-ARABIC-ORDINAL-20260907",
            "AR-OLP-0031-MSA-COFINITE-SOURCE-NOTE-20260907",
            "AR-OLP-0031-CLASSICAL-COFINITE-SOURCE-NOTE-20260907",
            "AR-OLP-0031-CLASSICAL-UNION-PREDICATE-20260907",
            "AR-OLP-0032-MSA-SOURCE-CORRECTION-DISCLOSURE-20260907",
            "AR-OLP-0032-CLASSICAL-SOURCE-CORRECTION-DISCLOSURE-20260907",
        })

    def test_applied_mode_rejects_predecessor_and_never_falls_back(self):
        for path, transaction in self.transactions.items():
            before, after = self.before[path].encode(), self.after[path].encode()
            with self.subTest(path=path):
                with self.assertRaises(AssertionError):
                    source_pair(transaction, before, "applied")
                with self.assertRaises(AssertionError):
                    source_pair(transaction, after, "candidate")
                for mode in ("candidate", "applied"):
                    with self.assertRaises(AssertionError):
                        source_pair(transaction, b"not either source state", mode)
                with self.assertRaises(ValueError):
                    source_pair(transaction, before, "automatic")

    def test_complete_source_hashes_and_both_replay_directions(self):
        for row in self.ledger["primary_source_inventory"]:
            before, after = self.before[row["path"]], self.after[row["path"]]
            with self.subTest(path=row["path"]):
                for phase, text in (("before", before), ("after", after)):
                    self.assertEqual((sha(text.encode()), len(text.encode())),
                                     (row[phase+"_sha256"], row[phase+"_bytes"]))
                if row["path"] in self.transactions:
                    # Require the existing target newline, not an invented
                    # newline in the byte-frozen English pairing-alt source.
                    self.assertTrue(before.endswith("\n"))
                    self.assertTrue(after.endswith("\n"))
                    transaction = self.transactions[row["path"]]
                    self.assertEqual(replay(before, transaction["patches"]), after)
                    self.assertEqual(replay(after, transaction["patches"], inverse=True), before)
                    self.assertEqual(self.live[row["path"]],
                                     (before if MODE == "candidate" else after).encode())
                else:
                    self.assertEqual(before, after)

    def test_exact_pinned_intake_and_literal_plan_history(self):
        authority = self.ledger["authority"]
        raw = Path(authority["intake_path"]).read_bytes()
        self.assertEqual((sha(raw), len(raw)), (INTAKE_SHA, 130933))
        self.assertEqual(authority["intake_sha256"], INTAKE_SHA)
        plan = json.loads(raw)
        for transaction in self.transactions.values():
            original = next(t for t in plan["transactions"]
                            if t["path"] == (REPO / transaction["path"]).as_posix())
            self.assertEqual(transaction["before_sha256"], original["before_sha256"])
            self.assertEqual(transaction["after_sha256"], original["candidate_sha256"])
            self.assertEqual([(p["patch_id"], p["before"], p["after"]) for p in transaction["patches"]],
                             [(p["patch_id"], p["before"], p["after"]) for p in original["patches"]])

    def test_every_patch_location_and_exact_occurrence_count(self):
        for path, transaction in self.transactions.items():
            for patch in transaction["patches"]:
                with self.subTest(patch=patch["patch_id"]):
                    self.assertEqual(patch["occurrences"], 1)
                    self.assertEqual(location(self.before[path], patch["before"]), patch["before_location"])
                    self.assertEqual(location(self.after[path], patch["after"]), patch["after_location"])

    def test_all_thirty_four_primary_witnesses_and_candidate_bindings(self):
        count = 0
        for decision in self.ledger["decisions"]:
            for witness in decision["source_witnesses"]:
                text = (self.after if witness["phase"] == "candidate" else self.before)[witness["path"]]
                with self.subTest(decision=decision["decision_id"], role=witness["role"]):
                    self.assertEqual((sha(text.encode()), len(text.encode())),
                                     (witness["sha256"], witness["bytes"]))
                    for key, value in location(text, witness["literal"]).items():
                        self.assertEqual(witness[key], value)
                    self.assertEqual(text.encode()[witness["byte_start"]:witness["byte_end"]].decode(), witness["literal"])
                count += 1
            for binding in decision["occurrence_bindings"]:
                text = self.after[binding["path"]]
                self.assertEqual(sha(text.encode()), binding["sha256"])
                for loc in binding["locations"]:
                    self.assertEqual(location(text, loc["literal"]), loc)
        self.assertEqual(count, 34)

    def test_all_twenty_six_preserved_passages(self):
        self.assertEqual(len(self.ledger["preserved_passages"]), 26)
        for passage in self.ledger["preserved_passages"]:
            for phase, view in (("before", self.before), ("after", self.after)):
                with self.subTest(label=passage["label"], phase=phase):
                    text = view[passage["path"]]
                    self.assertEqual(sha(text.encode()), passage[phase+"_sha256"])
                    self.assertEqual(location(text, passage["literal"]), passage[phase+"_location"])

    def test_exact_local_formal_allowances_not_unconditional_raw_equality(self):
        ordinal_count = editorial_count = 0
        for path, transaction in self.transactions.items():
            before, after = self.before[path], self.after[path]
            allowance = next(a for a in self.ledger["formal_allowances"] if a["path"] == path)
            expected_ids = {a["patch_id"] for a in allowance["language_owned_ordinal_changes"]
                            + allowance["editorial_only_additions"]}
            projected = before
            seen = set()
            for patch in transaction["patches"]:
                if patch["change_kind"] == "prose-only":
                    self.assertNotIn("$", patch["before"] + patch["after"])
                    self.assertNotIn("\\", patch["before"] + patch["after"])
                    continue
                self.assertIn(patch["patch_id"], expected_ids)
                seen.add(patch["patch_id"])
                old_math = re.findall(r"\$([^$]+)\$", patch["before"])
                new_math = re.findall(r"\$([^$]+)\$", patch["after"])
                if patch["change_kind"] == "language-owned-ordinal-removal":
                    self.assertEqual(old_math, [r"(n+m)^\text{th}"])
                    self.assertEqual(new_math, ["(n+m)"])
                    ordinal_count += 1
                elif patch["change_kind"] == "editorial-disclosure-extension":
                    self.assertEqual(old_math, [r"\tuple{2,m}", r"\tuple{3,m}"])
                    self.assertEqual(new_math, [r"\tuple{0,2}", r"\tuple{0,1}",
                                               r"\tuple{2,m}", r"\tuple{3,m}", r"\tuple{3,0}"])
                    begin = before.rfind(r"\begin{editorial}", 0, before.index(patch["before"]))
                    end = before.index(r"\end{editorial}", begin)
                    self.assertIn("OLSIZ-003", before[begin:end])
                    self.assertIn(patch["before"], before[begin:end])
                    editorial_count += 1
                else:
                    self.fail("Undeclared formal allowance type")
                self.assertEqual(projected.count(patch["before"]), 1)
                projected = projected.replace(patch["before"], patch["after"], 1)
            self.assertEqual(seen, expected_ids)
            self.assertTrue(STATIC.compare(before, after)["failures"],
                            "Do not misreport the raw ordinal/editorial changes as equality")
            normalized = STATIC.compare(projected, after)
            self.assertEqual(normalized["failures"], [], normalized)
            self.assertTrue(all(normalized["checks"].values()), normalized)
            self.assertEqual(normalized["declared_exceptions"], [])
            a, b = STATIC.analyze(projected), STATIC.analyze(after)
            self.assertEqual([(k, STATIC.raw_body(a, t)) for k, t in a.formulas],
                             [(k, STATIC.raw_body(b, t)) for k, t in b.formulas])
            self.assertEqual(a.keys, b.keys)
            self.assertEqual(a.terminology, b.terminology)
            self.assertEqual(a.formal_commands, b.formal_commands)
        self.assertEqual((ordinal_count, editorial_count), (2, 2))

    def test_arabic_guide_has_seven_reasons_and_eight_candidate_locations(self):
        guide = LEDGER.with_suffix(".md")
        text = guide.read_text(encoding="utf-8")
        self.assertIn("أرقام الأسطر", text)
        self.assertIn("candidate", text)
        self.assertIn("applied", text)
        links = re.findall(r"\]\(([^)]+\.tex)#L(\d+)\)", text)
        expected = {(t["path"], p["after_location"]["line_start"])
                    for t in self.transactions.values() for p in t["patches"]}
        actual = set()
        for relative, line in links:
            source = (guide.parent / relative).resolve()
            path = source.relative_to(REPO).as_posix()
            self.assertIn(path, self.transactions)
            self.assertTrue(self.after[path].splitlines()[int(line)-1].strip())
            actual.add((path, int(line)))
        self.assertEqual(len(links), 8)
        self.assertEqual(actual, expected)
        for decision in self.ledger["decisions"]:
            self.assertIn(decision["decision_id"], text)
            self.assertIn(decision["rationale_arabic"], text)
            self.assertIn(decision["expert_question"], text)
            self.assertTrue(decision["open_to_correction"])
            self.assertFalse(decision["human_response_is_gate"])
            self.assertIsNone(decision["printed_page"])

    def test_shared_enumerable_token_unchanged(self):
        witness = self.ledger["shared_token_witness"]
        text = self.before[witness["path"]]
        self.assertEqual(text, self.after[witness["path"]])
        self.assertEqual((sha(text.encode()), len(text.encode())), (witness["sha256"], witness["bytes"]))
        definition = witness["enumerable_definition"]
        self.assertEqual(location(text, definition["literal"]), definition)
        self.assertEqual(definition["literal"],
                         r"\settexttoken{enumerable}{قابلة للتعداد}{قابلة للتعداد}[قابلة للتعداد][قابلة للتعداد]")

    def test_bounded_arithmetic_and_completed_pairing_prefix(self):
        def g(n, m):
            return (n+m)*(n+m+1)//2 + n

        def slot(n, m):
            return 2**n * (2*m+1)

        for k in range(101):
            self.assertEqual(sum(range(k+1)), k*(k+1)//2)
        for n in range(64):
            for m in range(1, 65):
                self.assertEqual(g(n+1, m-1), g(n, m)+1)
        self.assertEqual(g(1, 2), 7)
        expected = [(0,0), (1,0), (0,1), (2,0), (0,2),
                    (1,1), (0,3), (3,0), (0,4), (1,2)]
        self.assertEqual([slot(n,m) for n,m in expected], list(range(1,11)))
        self.assertEqual([slot(n,m)-1 for n,m in [(0,0),(1,2),(2,6)]], [0,9,51])
        for path in self.transactions:
            if not path.endswith("pairing-alt.tex"):
                continue
            arrays = re.findall(r"\\begin\{array\}[\s\S]*?\\end\{array\}", self.after[path])
            self.assertEqual(len(arrays), 4)
            pairs = [(int(n), int(m)) for n,m in re.findall(r"\\tuple\{(\d+),(\d+)\}", arrays[2])]
            self.assertEqual(pairs, expected)


if __name__ == "__main__":
    unittest.main()
