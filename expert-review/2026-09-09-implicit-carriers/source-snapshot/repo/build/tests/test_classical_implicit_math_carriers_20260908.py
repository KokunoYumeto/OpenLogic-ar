"""Bounded tests for three source-attested implicit math argument carriers."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "build"))
import materialize_classical_notation as m


class ImplicitCarriers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads((ROOT / m.DEFAULT_POLICY).read_bytes())
        cls.greek = {row["key"] for row in json.loads((ROOT / m.DEFAULT_LETTERS).read_bytes())["entries"]
                     if row["family"] == "greek-variable"}

    def transform(self, source, *, bom=False, unit="OLP-0001"):
        occurrences, replacements, summary = m.classify_unit(unit, source, bom, self.policy, self.greek)
        target, spans = m.apply_replacements(source, replacements)
        restored = m.inverse_reconstruct(target, replacements, spans)
        self.assertEqual(m.encode_exact(restored, bom), m.encode_exact(source, bom))
        self.assertEqual(summary["untreated_candidates"], 0)
        starts = [o.source_char_start for o in occurrences]
        self.assertEqual(len(starts), len(set(starts)), "Duplicate occurrence source start")
        for occurrence in occurrences:
            self.assertEqual(source[occurrence.source_char_start:occurrence.source_char_end], occurrence.source)
        return occurrences, replacements, target, summary

    def test_exact_consulted_authority_is_bound(self):
        receipt = m.validate_implicit_carrier_authority(ROOT)
        self.assertEqual(receipt["sha256"], m.IMPLICIT_CARRIER_CONFIG_SHA)
        self.assertEqual(set(receipt["contracts"]), {"mTrue", "mFalse", "TMtrans"})
        self.assertEqual([receipt["contracts"][name]["required_math_arguments"]
                          for name in ("mTrue", "mFalse", "TMtrans")], [1, 1, 3])

    def test_changed_primary_configuration_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / m.IMPLICIT_CARRIER_CONFIG
            path.parent.mkdir(parents=True)
            path.write_bytes((ROOT / m.IMPLICIT_CARRIER_CONFIG).read_bytes() + b"% changed\n")
            with self.assertRaisesRegex(m.MaterializationError, "configuration identity changed"):
                m.validate_implicit_carrier_authority(root)

    def test_prose_carriers_and_subscripts_become_math_not_text_numerals(self):
        occurrences, _, target, _ = self.transform(r"Prose \mTrue{p_12} and \mFalse{q}.")
        self.assertIn(r"\mTrue{{\OLId{latin-ordinary}{p}}_{\OLMathNumeral{1}}{\OLMathNumeral{2}}}", target)
        self.assertIn(r"\mFalse{{\OLId{latin-ordinary}{q}}}", target)
        self.assertNotIn("OLClassicalDigits", target)
        for occurrence in occurrences:
            self.assertEqual(occurrence.carrier_evidence[0]["authority_sha256"], m.IMPLICIT_CARRIER_CONFIG_SHA)

    def test_diagram_labels_reenter_without_touching_keys_or_dimensions(self):
        source = (r"\begin{tikzpicture}[node distance=2cm]"
                  r"\node (w1) [label=right:\mFalse{p_2},right of=w2] {$w_1$};"
                  r"\end{tikzpicture}")
        _, _, target, _ = self.transform(source)
        for literal in ("node distance=2cm", "(w1)", "right of=w2"):
            self.assertIn(literal, target)
        self.assertIn(r"\mFalse{{\OLId{latin-ordinary}{p}}_{\OLMathNumeral{2}}}", target)

    def test_carriers_inside_outer_math_diagram_and_text_reenter(self):
        source = (r"\begin{align*}x&=\begin{tikzpicture}[scale=2]"
                  r"\node(A){\text{A1 \mTrue{p}}};\end{tikzpicture}\end{align*}")
        _, _, target, _ = self.transform(source)
        self.assertIn(r"\text{A1 \mTrue{{\OLId{latin-ordinary}{p}}}}", target)
        self.assertIn("scale=2", target)

    def test_independent_international_style_and_key_protections_survive(self):
        source = (r"\mTrue{\mathbf A+\OLInternationalMath{B+2}+p} "
                  r"\OLInternationalMath{\mFalse{q+3}} "
                  r"\label{\mTrue{r4}}")
        _, _, target, _ = self.transform(source)
        self.assertIn(r"\mathbf A+\OLInternationalMath{B+2}", target)
        self.assertIn(r"\OLInternationalMath{\mFalse{q+3}}", target)
        self.assertIn(r"\label{\mTrue{r4}}", target)
        self.assertIn(r"\OLId{latin-ordinary}{p}", target)

    def test_literal_direction_exception_is_not_blanket_third_argument_exemption(self):
        source = r"\TMtrans{A}{3}{R} \TMtrans{L}{N}{x} \TMtrans{1}{2}{3}"
        occurrences, _, target, _ = self.transform(source)
        self.assertIn(r"\TMtrans{{\OLId{latin-looped}{A}}}{{\OLMathNumeral{3}}}{R}", target)
        self.assertIn(r"\TMtrans{{\OLId{latin-looped}{L}}}{{\OLId{latin-looped}{N}}}{{\OLId{latin-ordinary}{x}}}", target)
        direction = [o for o in occurrences if o.source == "R"]
        self.assertEqual(len(direction), 1)
        self.assertEqual(direction[0].disposition, "explicit-international-exemption")
        self.assertIn("machine-direction", direction[0].reason)
        self.assertIn(r"\TMtrans{{\OLMathNumeral{1}}}{{\OLMathNumeral{2}}}{{\OLMathNumeral{3}}}", target)

    def test_all_three_direction_literals_and_symbol_macros_are_retained(self):
        source = r"\TMtrans{\TMstroke}{\TMblank}{R} \TMtrans{1}{0}{L} \TMtrans{1}{0}{N}"
        occurrences, _, target, _ = self.transform(source)
        self.assertIn(r"\TMtrans{\TMstroke}{\TMblank}{R}", target)
        directions = [o for o in occurrences if o.reason.startswith("typed machine-direction literal")]
        self.assertEqual([o.source for o in directions], ["R", "L", "N"])

    def test_naked_macro_arguments_preserve_original_single_token_scope(self):
        _, _, target, _ = self.transform(r"\TMtrans1234 \mTrue p \mFalse q")
        self.assertIn(r"\TMtrans{\OLMathNumeral{1}}{\OLMathNumeral{2}}{\OLMathNumeral{3}}4", target)
        self.assertIn(r"\mTrue {\OLId{latin-ordinary}{p}}", target)

    def test_original_formula_indices_unchanged_and_new_segments_appended(self):
        source = r"\mTrue{p} before $x$ after \mFalse{q} and $y$"
        original = m.analyze(source).formulas
        occurrences, _, _, summary = self.transform(source)
        by_source = {o.source: o for o in occurrences}
        self.assertEqual((by_source["x"].formula_index, by_source["y"].formula_index), (0, 1))
        self.assertGreaterEqual(by_source["p"].formula_index, len(original))
        self.assertIn("source-char-0", by_source["p"].formula_kind)
        self.assertEqual(summary["implicit_carrier_segments"], 2)

    def test_nested_carriers_and_explicit_islands_have_no_duplicate_assignment(self):
        source = r"\mTrue{p+\text{A1 $x$ and \mFalse{q_2}}} $\TMtrans{1}{2}{R}$"
        occurrences, _, target, _ = self.transform(source)
        self.assertEqual(sum(o.source == "x" for o in occurrences), 1)
        self.assertEqual(sum(o.source == "q" for o in occurrences), 1)
        self.assertIn("A1", target)
        self.assertIn(r"\OLId{latin-ordinary}{q}", target)

    def test_bom_crlf_comments_and_literal_examples_are_preserved(self):
        source = "% \\mTrue{p}\r\n\\verb|\\mFalse{q}|\r\n\\mTrue{p_1}\r\n"
        occurrences, _, target, _ = self.transform(source, bom=True)
        self.assertIn("% \\mTrue{p}\r\n", target)
        self.assertIn(r"\verb|\mFalse{q}|", target)
        self.assertEqual(occurrences[0].source_utf8_byte_start,
                         3 + len(source[:occurrences[0].source_char_start].encode("utf-8")))

    def test_macro_definition_bodies_and_aliases_are_not_expanded(self):
        source = (r"\def\example#1{\mTrue{p}} \newcommand{\other}[1]{\mFalse{q}} "
                  r"\let\alias\mTrue \mTrue{r}")
        _, _, target, _ = self.transform(source)
        self.assertIn(r"\def\example#1{\mTrue{p}}", target)
        self.assertIn(r"\newcommand{\other}[1]{\mFalse{q}}", target)
        self.assertIn(r"\let\alias\mTrue", target)
        self.assertIn(r"\mTrue{{\OLId{latin-ordinary}{r}}}", target)
        _, _, only_definition, _ = self.transform(r"\def\example{\mTrue{$p$}}")
        self.assertEqual(only_definition, r"\def\example{\mTrue{$p$}}")

    def test_missing_arguments_and_shadowed_carriers_fail_closed(self):
        for source in (r"\mTrue", r"\TMtrans{1}{2}", r"$\TMtrans{1}{2}$",
                       r"\def\mTrue#1{#1} \mTrue{p}",
                       r"\renewcommand{\mFalse}[1]{#1}", r"\let\TMtrans\other"):
            with self.subTest(source=source), self.assertRaises(m.MaterializationError):
                self.transform(source)

    def test_empty_arguments_are_valid_and_unknown_macros_are_not_inferred(self):
        _, _, target, _ = self.transform(r"\mTrue{} \TMtrans{}{}{R} \unknown{p}")
        self.assertEqual(target, r"\mTrue{} \TMtrans{}{}{R} \unknown{p}")

    def test_live_relational_model_and_turing_edge_gaps(self):
        for relative in ("normal-modal-logic/syntax-and-semantics/relational-models.tex",
                         "turing-machines/undecidability/enumerating-tms.tex"):
            source = (ROOT / m.SOURCE_PREFIX / relative).read_bytes().decode("utf-8")
            _, _, target, _ = self.transform(source)
            if relative.endswith("relational-models.tex"):
                self.assertNotIn(r"\mTrue{p}", target)
                self.assertNotIn(r"\mFalse{q}", target)
                self.assertIn("[align=right]right:", target)
            else:
                self.assertNotIn(r"\TMtrans{A}{A}", target)
                self.assertNotIn(r"\TMtrans{3}{3}", target)
                self.assertIn(r"\TMright", target)

    def test_every_qualified_gap_and_direction_question_has_an_exact_disposition(self):
        path = ROOT / "evidence/classical/repairs/implicit-math-intake-qualified-96175312/IMPLICIT_MATH_FINDINGS.json"
        raw = path.read_bytes()
        self.assertLess(len(raw), 1024 * 1024)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         "7e681300f50cdf8e68ce4572d34953a117a49da03b03037fa696da052f3647ad")
        intake = json.loads(raw)
        sources = {row["source"]["path"]: row["source"] for row in intake["captured_units"]}
        by_path = {}
        for finding in intake["findings"]:
            by_path.setdefault(finding["source_path"], []).append(finding)
        gaps = directions = 0
        for relative, findings in by_path.items():
            source_raw = (ROOT / relative).read_bytes()
            self.assertEqual(hashlib.sha256(source_raw).hexdigest(), sources[relative]["sha256"].lower())
            source, bom = m.decode_exact(source_raw)
            occurrences, _, _, _ = self.transform(source, bom=bom, unit=findings[0]["unit"])
            for finding in findings:
                with self.subTest(finding=finding["id"]):
                    matches = [o for o in occurrences if any(
                        e["call_source_char_start"] == finding["source_offset"] and
                        e["carrier"] == finding["command"] and e["argument"] == finding["argument"]
                        for e in o.carrier_evidence or [])]
                    self.assertTrue(matches)
                    if finding["status"] == "OPEN_SYMBOL_POLICY_REVIEW_NOT_AUTOMATIC_LETTER_MISS":
                        self.assertEqual(len(matches), 1)
                        self.assertEqual(matches[0].source, finding["source_argument"])
                        self.assertEqual(matches[0].disposition, "explicit-international-exemption")
                        self.assertIn("typed machine-direction", matches[0].reason)
                        directions += 1
                    else:
                        self.assertTrue(all(o.disposition in ("typed-arabic-letter-wrapper",
                                                             "typed-eastern-arabic-numeral-wrapper")
                                            for o in matches))
                        self.assertEqual(sum(o.candidate_scalars for o in matches),
                                         sum(c.isascii() and c.isalnum() for c in finding["source_argument"]))
                        gaps += 1
        self.assertEqual((gaps, directions), (87, 8))


if __name__ == "__main__":
    unittest.main(verbosity=2)
