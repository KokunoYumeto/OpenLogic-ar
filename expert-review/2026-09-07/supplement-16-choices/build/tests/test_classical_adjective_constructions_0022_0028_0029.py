"""Exact-byte, source-witness and formal checks for four Classical repairs.

No TeX, export, subprocess, network or central-metadata writes are performed.
The tests establish this batch's preservation contract, not full-edition QA.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import sys
import unittest


REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "evidence/classical/repairs/OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907.json"
SPEC = importlib.util.spec_from_file_location(
    "adjective_constructions_static", REPO / "build/validate_classical_overlay.py"
)
STATIC = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = STATIC
SPEC.loader.exec_module(STATIC)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def locate(text, literal):
    if text.count(literal) != 1:
        raise AssertionError("Nonunique literal: " + repr(literal))
    offset = text.index(literal)
    start = text[:offset].count("\n") + 1
    end = text[:offset + len(literal)].count("\n") + 1
    return {
        "line_start": start,
        "line_end": end,
        "byte_start": len(text[:offset].encode()),
        "byte_end": len(text[:offset + len(literal)].encode()),
        "literal": literal,
        "excerpt": "\n".join(text.splitlines()[start - 1:end]),
    }


class ClassicalAdjectiveConstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        cls.transactions = {r["path"]: r for r in cls.ledger["transactions"]}
        cls.before, cls.after = {}, {}
        for row in cls.ledger["primary_source_inventory"]:
            path = Path(row["path"])
            raw = (path if path.is_absolute() else REPO / path).read_bytes()
            text = raw.decode("utf-8")
            cls.after[row["path"]] = text
            for patch in reversed(cls.transactions.get(row["path"], {}).get("patches", [])):
                if text.count(patch["after"]) != 1:
                    raise AssertionError("Ambiguous inverse: " + row["path"])
                text = text.replace(patch["after"], patch["before"], 1)
            cls.before[row["path"]] = text

    def test_exact_scope_and_four_decisions(self):
        self.assertEqual(len(self.transactions), 3)
        self.assertEqual(sum(len(t["patches"]) for t in self.transactions.values()), 4)
        self.assertEqual(len(self.ledger["primary_source_inventory"]), 10)
        expected = {
            "AR-OLP-0022-CLASSICAL-SURJECTIVE-OPENING-20260907",
            "AR-OLP-0028-CLASSICAL-ENUMERABLE-OPENING-20260907",
            "AR-OLP-0029-CLASSICAL-DUAL-SURJECTIVE-20260907",
            "AR-OLP-0029-CLASSICAL-ZERO-INDEXED-ELEMENTS-20260907",
        }
        self.assertEqual({d["decision_id"] for d in self.ledger["decisions"]}, expected)
        self.assertEqual(
            {(t["unit_id"], t["edition"]) for t in self.transactions.values()},
            {("OLP-0022", "classical"), ("OLP-0028", "classical"), ("OLP-0029", "classical")},
        )

    def test_complete_hashes_inverse_and_forward_replay(self):
        for row in self.ledger["primary_source_inventory"]:
            with self.subTest(path=row["path"]):
                before, after = self.before[row["path"]], self.after[row["path"]]
                for phase, text in (("before", before), ("after", after)):
                    self.assertEqual(sha(text.encode()), row[phase + "_sha256"])
                    self.assertEqual(len(text.encode()), row[phase + "_bytes"])
                self.assertTrue(row["read_complete_before_edit"])
                replay = before
                for patch in self.transactions.get(row["path"], {}).get("patches", []):
                    self.assertEqual(replay.count(patch["before"]), 1)
                    replay = replay.replace(patch["before"], patch["after"], 1)
                self.assertEqual(replay.encode(), after.encode())
                self.assertTrue(after.endswith("\n"))
                if row["edition"] != "classical":
                    self.assertEqual(before, after)

    def test_every_patch_location_and_only_literal_scoped_change(self):
        for transaction in self.transactions.values():
            before, after = self.before[transaction["path"]], self.after[transaction["path"]]
            with self.subTest(path=transaction["path"]):
                for phase, text in (("before", before), ("after", after)):
                    self.assertEqual(sha(text.encode()), transaction[phase + "_sha256"])
                    self.assertEqual(len(text.encode()), transaction[phase + "_bytes"])
                for patch in transaction["patches"]:
                    self.assertEqual(patch["occurrences"], 1)
                    for phase, text in (("before", before), ("after", after)):
                        self.assertEqual(locate(text, patch[phase]), patch[phase + "_location"])
                        self.assertNotIn("$", patch[phase])
                        self.assertNotIn("\\", patch[phase])
                    self.assertEqual(
                        re.findall(r"!![A-Za-z^]*\{[^}]+\}s?", patch["before"]),
                        re.findall(r"!![A-Za-z^]*\{[^}]+\}s?", patch["after"]),
                    )

    def assert_witness(self, witness):
        text = (self.before if witness.get("phase") == "before" else self.after)[witness["path"]]
        raw = text.encode()
        self.assertEqual((sha(raw), len(raw)), (witness["sha256"], witness["bytes"]))
        location = locate(text, witness["literal"])
        for key, value in location.items():
            self.assertEqual(witness[key], value, (witness["path"], key))
        self.assertEqual(raw[witness["byte_start"]:witness["byte_end"]].decode(), witness["literal"])

    def test_all_twenty_exact_source_and_token_witnesses(self):
        count = 0
        for decision in self.ledger["decisions"]:
            for witness in decision["source_witnesses"] + [decision["shared_token_witness"]]:
                with self.subTest(decision=decision["decision_id"], path=witness["path"]):
                    self.assert_witness(witness)
                    count += 1
            for binding in decision["occurrence_bindings"]:
                text = self.after[binding["path"]]
                self.assertEqual(sha(text.encode()), binding["sha256"])
                for location in binding["locations"]:
                    self.assertEqual(locate(text, location["literal"]), location)
        self.assertEqual(count, 20)

    def test_formal_comparison_and_exact_math_bodies_without_exceptions(self):
        for path in self.transactions:
            with self.subTest(path=path):
                before, after = self.before[path], self.after[path]
                result = STATIC.compare(before, after)
                self.assertEqual(result["failures"], [], result)
                self.assertTrue(all(result["checks"].values()), result)
                self.assertEqual(result["declared_exceptions"], [])
                a, b = STATIC.analyze(before), STATIC.analyze(after)
                self.assertEqual(
                    [(kind, STATIC.raw_body(a, tokens)) for kind, tokens in a.formulas],
                    [(kind, STATIC.raw_body(b, tokens)) for kind, tokens in b.formulas],
                )
                self.assertEqual(a.keys, b.keys)
                self.assertEqual(a.terminology, b.terminology)
                self.assertEqual(a.formal_commands, b.formal_commands)

    def test_thirteen_preserved_passages(self):
        self.assertEqual(len(self.ledger["preserved_passages"]), 13)
        for passage in self.ledger["preserved_passages"]:
            with self.subTest(label=passage["label"], literal=passage["literal"][:40]):
                for phase, mapping in (("before", self.before), ("after", self.after)):
                    text = mapping[passage["path"]]
                    self.assertEqual(sha(text.encode()), passage[phase + "_sha256"])
                    self.assertEqual(locate(text, passage["literal"]), passage[phase + "_location"])

    def test_exact_predecessor_chain_and_five_prior_constructions(self):
        history = self.ledger["predecessor_history"]
        predecessor = history["transaction"]
        current_transaction = self.transactions[predecessor["path"]]
        self.assertEqual(predecessor["after_sha256"], current_transaction["before_sha256"])
        self.assertEqual(predecessor["after_bytes"], current_transaction["before_bytes"])
        self.assertEqual(history["this_batch_before_sha256"], predecessor["after_sha256"])
        self.assertEqual(len(predecessor["patches"]), 5)
        before = self.before[predecessor["path"]]
        after = self.after[predecessor["path"]]
        earlier = before
        for patch in reversed(predecessor["patches"]):
            self.assertEqual(earlier.count(patch["after"]), 1)
            earlier = earlier.replace(patch["after"], patch["before"], 1)
            self.assertEqual(after.count(patch["after"]), 1)
            self.assertEqual(locate(after, patch["after"])["line_start"],
                             patch["after_location"]["line_start"] - 1)
        self.assertEqual(sha(earlier.encode()), predecessor["before_sha256"])
        self.assertEqual(len(earlier.encode()), predecessor["before_bytes"])
        for patch in predecessor["patches"]:
            self.assertEqual(earlier.count(patch["before"]), 1)
            earlier = earlier.replace(patch["before"], patch["after"], 1)
        self.assertEqual(earlier, before)

    def test_readable_reasons_questions_and_four_current_source_links(self):
        guide = LEDGER.with_suffix(".md")
        text = guide.read_text(encoding="utf-8")
        links = re.findall(r"\]\(([^)]+\.tex)#L(\d+)\)", text)
        expected = {(t["path"], p["after_location"]["line_start"])
                    for t in self.transactions.values() for p in t["patches"]}
        actual = set()
        for relative, line in links:
            source = (guide.parent / relative).resolve()
            self.assertTrue(source.is_relative_to(REPO / "source/locale/ar-classical"))
            self.assertTrue(source.read_text(encoding="utf-8").splitlines()[int(line)-1].strip())
            actual.add((source.relative_to(REPO).as_posix(), int(line)))
        self.assertEqual(len(links), 4)
        self.assertEqual(actual, expected)
        for decision in self.ledger["decisions"]:
            self.assertIn(decision["decision_id"], text)
            self.assertIn(decision["rationale"], text)
            self.assertIn(decision["expert_question"], text)
            self.assertTrue(decision["open_to_correction"])
            self.assertFalse(decision["human_response_is_gate"])
            self.assertEqual(decision["recording_mode"], "contemporaneous")
            self.assertIsNone(decision["printed_page"])

    def test_shared_expansions_and_corrected_local_predications(self):
        config = self.after["source/locale/ar/open-logic-config.sty"]
        for definition in (
            r"\settexttoken{surjective}{شاملة}{شاملة}[شاملة][شاملة]",
            r"\settexttoken{enumerable}{قابلة للتعداد}{قابلة للتعداد}[قابلة للتعداد][قابلة للتعداد]",
            r"\settexttoken{element}{عنصر}{عناصر}[عنصر][عناصر]",
        ):
            self.assertIn(definition, config)
        for decision in self.ledger["decisions"]:
            transaction = next(t for t in self.transactions.values() if t["unit_id"] == decision["unit_id"])
            patch = next(p for p in transaction["patches"] if decision["decision_id"] in p["decision_ids"])
            expanded = patch["after"].replace("!!{surjective}", "شاملة").replace(
                "!!{enumerable}", "قابلة للتعداد").replace("!!{element}s", "عناصر")
            self.assertEqual(expanded, decision["chosen_arabic"])
            self.assertNotIn(patch["before"], self.after[transaction["path"]])


if __name__ == "__main__":
    unittest.main()
