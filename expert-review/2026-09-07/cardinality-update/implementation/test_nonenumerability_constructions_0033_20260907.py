"""Read-only tests of six exact OLP0033 repairs; no TeX or public writes.

Reconstruct the complete before bytes by unique inverses, then independently
compare actual source math containers, including whole display arrays/cases.
These tests establish only the bounded repair, not full-edition acceptance.
"""
from pathlib import Path
import hashlib
import json
import re
import unittest
import unicodedata

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "evidence/classical/repairs/OLP0033_NONENUMERABILITY_CONSTRUCTIONS_20260907.json"
TARGET = "content/sets-functions-relations/size-of-sets/non-enumerability.tex"
EN = Path("source-snapshot/english") / TARGET
EXPECTED = {
    "english": (9412, "a272a841f8c50bda6589aac40278b9bff7f8a1f5284730c7195423b09ac3ba2e", 9412, "a272a841f8c50bda6589aac40278b9bff7f8a1f5284730c7195423b09ac3ba2e"),
    "msa": (12479, "82014f0a1361ae5462c5dd7d082e18a2e701dd23aa730a5550bd362ceb2b77e8", 12482, "e8200b58dba20accc5ec21a6a1ed05889b633b7136088a0a8cddc5a839198b1a"),
    "classical": (11568, "6aea9fd0baec506686a0c45153e8dfdf7d556f89878f9bd2ea9f90c7b4e8f3e9", 11611, "d06a2d5dd573e4808c94eeabe97c39b92966c1cf1966f7b5272e6c58af89d263"),
}
MATH = re.compile(r"\\\[.*?\\\]|\\begin\{align\*\}.*?\\end\{align\*\}|(?<!\\)\$.*?(?<!\\)\$", re.S)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def exact_replace(raw, old, new):
    old, new = old.encode("utf-8"), new.encode("utf-8")
    if raw.count(old) != 1:
        raise ValueError("Expected one exact occurrence")
    return raw.replace(old, new, 1)


def math_containers(text, english_comparison=False):
    result = []
    for match in MATH.finditer(text):
        body = match.group()
        if english_comparison:
            body = body.replace(r"\text{إذا كان ", r"\text{if ")
        result.append(re.sub(r"\s+", "", body))
    return result


def require_source_math(english, arabic):
    if len(math_containers(english)) != 173:
        raise ValueError("Unexpected source math-container count")
    if english.count(r"\text{if ") != 2 or arabic.count(r"\text{إذا كان ") != 2:
        raise ValueError("Unexpected localized case-label count")
    if math_containers(english) != math_containers(arabic, True):
        raise ValueError("Ordered source math differs")


class NonenumerabilityConstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(LEDGER.read_bytes())
        cls.before, cls.after = {}, {}
        for row in cls.data["primary_source_inventory"]:
            path = row["path"]
            cls.after[path] = (REPO / path).read_bytes()
            cls.before[path] = cls.after[path]
        for tx in cls.data["transactions"]:
            raw = cls.after[tx["path"]]
            for patch in reversed(tx["patches"]):
                raw = exact_replace(raw, patch["after"], patch["before"])
            cls.before[tx["path"]] = raw

    def check_location(self, raw, location, literal):
        self.assertEqual(raw[location["byte_start"]:location["byte_end"]], literal.encode("utf-8"))
        self.assertEqual(raw[:location["byte_start"]].count(b"\n") + 1, location["line_start"])
        self.assertEqual(raw[:location["byte_end"] - 1].count(b"\n") + 1, location["line_end"])
        self.assertEqual("\n".join(raw.decode().splitlines()[location["line_start"] - 1:location["line_end"]]), location["excerpt"])

    def test_independent_exact_whole_file_hashes_and_scope(self):
        self.assertEqual(len(self.data["transactions"]), 2)
        self.assertEqual(len(self.data["primary_source_inventory"]), 3)
        self.assertEqual(sum(len(t["patches"]) for t in self.data["transactions"]), 6)
        for row in self.data["primary_source_inventory"]:
            expected = EXPECTED[row["edition"]]
            self.assertEqual((len(self.before[row["path"]]), sha(self.before[row["path"]])), expected[:2])
            self.assertEqual((len(self.after[row["path"]]), sha(self.after[row["path"]])), expected[2:])
            self.assertEqual((row["before_bytes"], row["before_sha256"], row["after_bytes"], row["after_sha256"]), expected)

    def test_inverse_forward_replay_and_all_patch_locations(self):
        for tx in self.data["transactions"]:
            path = tx["path"]
            replay = self.before[path]
            for patch in tx["patches"]:
                self.assertEqual(patch["occurrences"], 1)
                self.check_location(self.before[path], patch["before_location"], patch["before"])
                self.check_location(self.after[path], patch["after_location"], patch["after"])
                replay = exact_replace(replay, patch["before"], patch["after"])
            self.assertEqual(replay, self.after[path])
            self.assertEqual((len(replay), sha(replay)), (tx["after_bytes"], tx["after_sha256"]))

    def test_all_decision_source_witnesses_and_page_honesty(self):
        ids = {d["decision_id"] for d in self.data["decisions"]}
        self.assertEqual(len(ids), 6)
        self.assertEqual(ids, {i for tx in self.data["transactions"] for p in tx["patches"] for i in p["decision_ids"]})
        for d in self.data["decisions"]:
            self.assertTrue(d["open_to_correction"])
            self.assertFalse(d["human_response_is_gate"])
            self.assertTrue(d["rationale"] and d["rationale_ar"] and d["expert_question"])
            self.assertEqual(len(d["source_witnesses"]), 3)
            for w in d["source_witnesses"]:
                raw = (self.before if w["phase"] == "before" else self.after)[w["path"]]
                self.assertEqual((len(raw), sha(raw)), (w["bytes"], w["sha256"]))
                self.check_location(raw, w, w["literal"])
                self.assertIsNone(w["printed_page"])

    def test_packet_unchanged_and_exact_recorded_canon_evidence(self):
        for item in self.data["packet_inventory"]:
            raw = Path(item["path"]).read_bytes()
            self.assertEqual((len(raw), sha(raw)), (item["bytes"], item["sha256"]))
        choices_path = next(p["path"] for p in self.data["packet_inventory"] if p["path"].endswith("CHOICES.jsonl"))
        originals = {x["choice_id"]: x for x in map(json.loads, Path(choices_path).read_text(encoding="utf-8").splitlines())}
        for d in self.data["decisions"]:
            if d["normalization"] is not None:
                continue
            original = originals[d["source_choice_id"]]
            self.assertEqual(len(original["canon_consulted"]), len(d["authority_checks"]))
            for old, new in zip(original["canon_consulted"], d["authority_checks"]):
                self.assertEqual((old["source_id"], old["text"], old["locator"], old["use"]),
                                 (new["source_id"], new["excerpt"], new["locator"], new["use_limits"]))
                self.assertEqual(sha(Path(new["source_path"]).read_bytes()), new["source_sha256"])
                image = new["visual_evidence"]
                raw = Path(image["path"]).read_bytes()
                self.assertEqual((len(raw), sha(raw)), (image["bytes"], image["sha256"]))
                self.assertIn("did not newly inspect", new["evidence_origin"])

    def test_all_173_ordered_math_containers_against_english(self):
        english = EN.read_text(encoding="utf-8")
        for tx in self.data["transactions"]:
            for phase in (self.before, self.after):
                require_source_math(english, phase[tx["path"]].decode())
            self.assertEqual([m.group() for m in MATH.finditer(self.before[tx["path"]].decode())],
                             [m.group() for m in MATH.finditer(self.after[tx["path"]].decode())])

    def test_whole_arrays_and_cases_remain_literal(self):
        for tx in self.data["transactions"]:
            old, new = self.before[tx["path"]].decode(), self.after[tx["path"]].decode()
            for env, count in (("array", 2), ("cases", 1)):
                pattern = r"\\begin\{" + env + r"\}.*?\\end\{" + env + r"\}"
                before = re.findall(pattern, old, re.S)
                self.assertEqual(len(before), count)
                self.assertEqual(before, re.findall(pattern, new, re.S))
            self.assertIn(r"\overline{s}(n) = 1 - s_n(n)", new)
            self.assertIn(r"\Pow{\Nat}", new)

    def test_structure_macros_comments_and_reference_identity(self):
        patterns = [r"\\(?:begin|end)\{[^}]+\}", r"\\(?:ol)?label\{[^}]+\}",
                    r"\\olref(?:\[[^\]]*\])*\{[^}]+\}", r"\\(?:cite|url|href)\{[^}]+\}",
                    r"!![^\s{]*\{[^}]+\}s?", r"\\(?:use|print)token\{[^}]+\}\{[^}]+\}",
                    r"\\documentclass\[[^\]]*\]\{[^}]+\}", r"\\olfileid.*"]
        for tx in self.data["transactions"]:
            old, new = self.before[tx["path"]].decode(), self.after[tx["path"]].decode()
            for pattern in patterns:
                self.assertEqual(re.findall(pattern, old), re.findall(pattern, new), pattern)
            self.assertEqual([s for s in old.splitlines() if s.lstrip().startswith("%")],
                             [s for s in new.splitlines() if s.lstrip().startswith("%")])

    def test_three_targeted_constructions_and_shared_token(self):
        classical = self.after["source/locale/ar-classical/" + TARGET].decode()
        msa = self.after["source/locale/ar/" + TARGET].decode()
        self.assertIn(r"فالمجموعة التي تنتفي عنها هذه الخاصية هي \emph{!!{nonenumerable}}", classical)
        self.assertIn("وطريق إثبات أن المجموعة غير الخالية !!{nonenumerable}", classical)
        self.assertIn("بقراءة عناصر قطر المصفوفة\nأعلاه على التوالي", msa)
        self.assertNotIn("من أوله إلى آخره", msa)
        config = (REPO / "source/locale/ar/open-logic-config.sty").read_bytes()
        self.assertEqual(sha(config), "018ce747a3957ce35eb05820e919d46fe4af0f3452ecdbe4d1ddc7e95bf33280")
        self.assertIn(r"\settexttoken{nonenumerable}{غير قابلة للتعداد}{غير قابلة للتعداد}", config.decode())

    def test_earlier_empty_set_correction_remains_exact(self):
        for saved in self.data["preserved_passages"]:
            for name, phase in (("before", self.before), ("after", self.after)):
                self.check_location(phase[saved["path"]], saved[name + "_location"], saved["literal"])
            self.assertIn("إذ لا توجد دالة كلية من الصحيحات الموجبة إلى المجموعة الخالية", saved["literal"])
        self.assertIn("أن المجموعة غير الخالية !!{enumerable}", self.after["source/locale/ar-classical/" + TARGET].decode())
        self.assertIn("فلكل مجموعة غير خالية\n!!{enumerable}", self.after["source/locale/ar/" + TARGET].decode())

    def test_exact_three_nfc_words_and_no_other_unicode_changes(self):
        nfc = [d for d in self.data["decisions"] if d["normalization"] is not None]
        self.assertEqual([d["normalization"]["line"] for d in nfc], [25, 40, 78])
        for d in nfc:
            normal = d["normalization"]
            self.assertEqual(unicodedata.normalize("NFC", d["raw_before"]), d["raw_after"])
            self.assertEqual([f"U+{ord(c):04X}" for c in d["raw_before"]], normal["raw_codepoints"])
            self.assertEqual([f"U+{ord(c):04X}" for c in d["raw_after"]], normal["normalized_codepoints"])
        for tx in self.data["transactions"]:
            new = self.after[tx["path"]].decode()
            self.assertEqual(unicodedata.normalize("NFC", new), new)
            self.assertNotIn("\ufffd", new)
            self.assertFalse(any(c in new for c in "\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069"))

    def test_adversarial_ambiguous_or_missing_inverse_is_rejected(self):
        with self.assertRaises(ValueError):
            exact_replace(b"aa aa", "aa", "bb")
        with self.assertRaises(ValueError):
            exact_replace(b"aa", "cc", "bb")
        for tx in self.data["transactions"]:
            self.assertNotEqual(sha(self.after[tx["path"]] + b" "), tx["after_sha256"])

    def test_adversarial_case_array_operator_and_label_corruption_rejected(self):
        text = self.after["source/locale/ar-classical/" + TARGET].decode()
        english = EN.read_text(encoding="utf-8")
        replacements = [(r"s_{n}(n) = 0", r"s_{n}(n) = 1"),
                        (r"\mathbf{s_{2}(2)}", r"\mathbf{s_{2}(3)}"),
                        (r"n \notin Z_n", r"n \in Z_n"),
                        (r"\text{إذا كان ", r"\text{إذا لم يكن ")]
        for old, new in replacements:
            self.assertIn(old, text)
            with self.assertRaises(ValueError):
                require_source_math(english, text.replace(old, new, 1))


if __name__ == "__main__":
    unittest.main()
