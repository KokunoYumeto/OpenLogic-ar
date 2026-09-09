"""Diagram syntax must stay literal while explicitly printed math is localized."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'build'))
import materialize_classical_notation as m


class DiagramFields(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads((ROOT / m.DEFAULT_POLICY).read_bytes())
        cls.greek = {r['key'] for r in json.loads((ROOT / m.DEFAULT_LETTERS).read_bytes())['entries']
                     if r['family'] == 'greek-variable'}

    def transform(self, source, bom=False):
        occurrences, replacements, summary = m.classify_unit('OLP-0001', source, bom, self.policy, self.greek)
        target, spans = m.apply_replacements(source, replacements)
        self.assertEqual(m.encode_exact(m.inverse_reconstruct(target, replacements, spans), bom),
                         m.encode_exact(source, bom))
        self.assertEqual(summary['untreated_candidates'], 0)
        return target

    def test_nested_picture_syntax_stays_literal_but_math_labels_change(self):
        source = (r'\begin{align*}&\begin{tikzpicture}[->,node distance=2cm]'
                  r'\node[draw,circle] (A) {$1$};'
                  r'\node (B) [right of=A] at (2,3) {\(x_1\)};'
                  r'\draw (A) to [loop above] (B);'
                  r'\end{tikzpicture}\end{align*}')
        target = self.transform(source)
        for literal in ['node distance=2cm', '(A)', '(B)', '[right of=A]', 'at (2,3)',
                        r'\draw (A) to [loop above] (B);']:
            self.assertIn(literal, target)
        self.assertIn(r'${\OLMathNumeral{1}}$', target)
        self.assertIn(r'\({\OLId{latin-ordinary}{x}}_{\OLMathNumeral{1}}\)', target)

    def test_picture_outside_outer_math_with_ensuremath_label(self):
        source = r'\begin{tikzpicture}[scale=2]\node(A) {\ensuremath{x+12}};\end{tikzpicture}'
        target = self.transform(source)
        self.assertIn('[scale=2]', target)
        self.assertIn(r'\node(A)', target)
        self.assertIn(r'\OLId{latin-ordinary}{x}', target)
        self.assertIn(r'\OLMathNumeral{12}', target)

    def test_intertext_reenters_math_without_translating_literal_text(self):
        source = (r'\begin{align*}x&=1\intertext{English A1 and $V_2$ '
                  r'and \(E=3\).}y&=2\end{align*}')
        target = self.transform(source)
        self.assertIn('English A1 and', target)
        self.assertIn(r'${\OLId{latin-looped}{V}}_{\OLMathNumeral{2}}$', target)
        self.assertIn(r'\({\OLId{latin-looped}{E}}={\OLMathNumeral{3}}\)', target)

    def test_text_boxes_reenter_math_and_keep_inner_key_contracts(self):
        source = r'$x+\text{A1 $\mathbf A+\OLInternationalMath{B+2}+c$}+\hbox{\ensuremath{d_2}}$'
        target = self.transform(source)
        self.assertIn(r'\text{A1 $\mathbf A+\OLInternationalMath{B+2}', target)
        for key in ['c', 'd']:
            self.assertIn(r'\OLId{latin-ordinary}{' + key + '}', target)

    def test_comment_bom_and_crlf_preserved(self):
        source = '\\[\\begin{tikzpicture}[scale=2]\r\n% $A$ ignored\r\n\\node(A){$x_1$};\r\n\\end{tikzpicture}\\]\r\n'
        target = self.transform(source, True)
        self.assertIn('% $A$ ignored\r\n', target)
        self.assertIn('[scale=2]', target)
        self.assertIn(r'\OLMathNumeral{1}', target)

    def test_live_graph_example(self):
        source = (ROOT / 'source/locale/ar-classical/content/sets-functions-relations/relations/graphs.tex').read_text(encoding='utf-8')
        target = self.transform(source)
        self.assertEqual(target.count('node distance=2cm'), 2)
        self.assertEqual(target.count(r'\node[draw,circle] (A)'), 2)
        self.assertEqual(target.count(r'\node[draw,circle] (B) [right of=A]'), 2)
        self.assertEqual(target.count(r'\draw (A) to  (C);'), 2)
        self.assertEqual(target.count(r'${\OLMathNumeral{1}}$'), 2)
        intertext = target.split(r'\intertext', 1)[1].split(r'& \begin{tikzpicture}', 1)[0]
        self.assertIn(r'\OLId{latin-looped}{V}', intertext)
        self.assertIn(r'\OLId{latin-looped}{E}', intertext)
        self.assertIn(r'\OLMathNumeral{3}', intertext)


if __name__ == '__main__':
    unittest.main()
