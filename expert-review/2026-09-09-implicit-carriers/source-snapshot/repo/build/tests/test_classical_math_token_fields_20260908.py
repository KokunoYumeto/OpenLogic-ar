"""Source-token grouping regressions; exact inverse is necessary, not sufficient."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'build'))
import materialize_classical_notation as m


def letter(key):
    family = 'latin-ordinary' if key.islower() else 'latin-looped'
    return '{' + rf'\OLId{{{family}}}{{{key}}}' + '}'


def numeral(value):
    return '{' + rf'\OLMathNumeral{{{value}}}' + '}'


def greek(key):
    return '{' + rf'\OLId{{greek-variable}}{{{key}}}' + '}'


class MathTokenFields(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads((ROOT / m.DEFAULT_POLICY).read_bytes())
        registry = json.loads((ROOT / m.DEFAULT_LETTERS).read_bytes())
        cls.greek = {r['key'] for r in registry['entries'] if r['family'] == 'greek-variable'}

    def transform(self, source, *, bom=False):
        occurrences, replacements, summary = m.classify_unit('OLP-0001', source, bom, self.policy, self.greek)
        output, spans = m.apply_replacements(source, replacements)
        self.assertEqual(m.encode_exact(m.inverse_reconstruct(output, replacements, spans), bom), m.encode_exact(source, bom))
        self.assertEqual(summary['untreated_candidates'], 0)
        ordered = sorted(replacements, key=lambda r: r.source_start)
        self.assertTrue(all(a.source_end <= b.source_start for a, b in zip(ordered, ordered[1:])))
        return output

    def test_naked_script_atoms(self):
        cases = {
            'a_1': letter('a') + '_' + numeral('1'),
            'a_n': letter('a') + '_' + letter('n'),
            'x^2': letter('x') + '^' + numeral('2'),
            r'x^\Gamma': letter('x') + '^' + greek('Gamma'),
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertEqual(self.transform('$' + source + '$'), '$' + expected + '$')

    def test_source_single_token_digit_boundaries(self):
        cases = {
            'x_12': letter('x') + '_' + numeral('1') + numeral('2'),
            'x^23': letter('x') + '^' + numeral('2') + numeral('3'),
            r'\sqrt12': r'\sqrt' + numeral('1') + numeral('2'),
            r'\frac12': r'\frac' + numeral('1') + numeral('2'),
            r'\frac1234': r'\frac' + numeral('1') + numeral('2') + numeral('34'),
            r'\frac1{2}': r'\frac' + numeral('1') + '{' + numeral('2') + '}',
            r'\frac{1}2': r'\frac{' + numeral('1') + '}' + numeral('2'),
            r'\frac x2': r'\frac ' + letter('x') + numeral('2'),
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertEqual(self.transform('$' + source + '$'), '$' + expected + '$')

    def test_normal_and_grouped_digit_runs_stay_whole(self):
        cases = {
            '12': numeral('12'),
            'x_{12}': letter('x') + '_{' + numeral('12') + '}',
            r'\frac{12}{34}': r'\frac{' + numeral('12') + '}{' + numeral('34') + '}',
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertEqual(self.transform('$' + source + '$'), '$' + expected + '$')

    def test_accents_and_optional_root(self):
        cases = {
            r'\vec x': r'\vec ' + letter('x'),
            r'\bar n': r'\bar ' + letter('n'),
            r'\hat\alpha': r'\hat' + greek('alpha'),
            r'\sqrt[12]34': r'\sqrt[' + numeral('12') + ']' + numeral('3') + numeral('4'),
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertEqual(self.transform('$' + source + '$'), '$' + expected + '$')

    def test_comments_and_whitespace_do_not_expand_field(self):
        source = '$x_ %keep\r\n12$\r\n'
        expected = '$' + letter('x') + '_ %keep\r\n' + numeral('1') + numeral('2') + '$\r\n'
        self.assertEqual(self.transform(source, bom=True), expected)

    def test_protected_command_arguments_and_text_numerals(self):
        source = r'رقم 12: $\mathbf x+\Obj p_0+\formula{A}+\hspace{1em}+\fn{rank}$'
        presented = self.transform(source)
        for unchanged in (r'\mathbf x', r'\Obj p', r'\formula{A}', r'\hspace{1em}', r'\fn{rank}'):
            self.assertIn(unchanged, presented)
        self.assertIn(r'رقم \OLClassicalDigits{12}:', presented)

    def test_live_canonical_failure_is_grouped(self):
        path = ROOT / 'source/locale/ar-classical/content/sets-functions-relations/sets/basics.tex'
        source, bom = m.decode_exact(path.read_bytes())
        presented = self.transform(source, bom=bom)
        self.assertNotRegex(presented, r'[_^]\s*\\OL(?:Id|MathNumeral)')
        self.assertIn(letter('a') + '_' + numeral('1'), presented)


if __name__ == '__main__':
    unittest.main()
