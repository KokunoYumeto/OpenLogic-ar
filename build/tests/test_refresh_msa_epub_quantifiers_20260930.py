import copy
import unittest
from lxml import etree
from build import refresh_msa_epub_quantifiers_20260930 as refresh


class FiniteEPUBSuccessorTests(unittest.TestCase):
    def test_frozen_identities_and_two_profiles_only(self):
        self.assertEqual(set(refresh.EXPECTED), {'international', 'machrek'})
        self.assertEqual(len(refresh.EXPECTED['international']), 64)
        self.assertEqual(refresh.BODY, 'OEBPS/modern-reader-3-7-3.xhtml')

    def test_native_comparison_does_not_remove_math_content(self):
        xml = ('<span xmlns="http://www.w3.org/1999/xhtml" id="old">'
               '<math xmlns="http://www.w3.org/1998/Math/MathML" dir="ltr" data-expression-id="old">'
               '<semantics><mrow><mi>a</mi></mrow><annotation encoding="application/x-openlogic-source-tex">a</annotation>'
               '</semantics></math></span>')
        original = etree.fromstring(xml.encode())
        changed = copy.deepcopy(original)
        changed.set('id', 'new')
        changed.find('{'+refresh.M+'}math').set('data-expression-id', 'new')
        self.assertEqual(refresh.native(original), refresh.native(changed))
        changed.find('.//{'+refresh.M+'}mi').text = 'b'
        self.assertNotEqual(refresh.native(original), refresh.native(changed))

    def test_source_annotation_is_required_and_unique(self):
        with self.assertRaisesRegex(ValueError, 'annotation is ambiguous'):
            refresh.expression(etree.fromstring(b'<span/>'))

    def test_target_paragraphs_must_be_unique(self):
        xml = '<section xmlns="http://www.w3.org/1999/xhtml"><p>يسمى الشرط</p><p>يسمى الشرط</p><p>لا توجد قيود</p></section>'
        with self.assertRaisesRegex(ValueError, 'not unique'):
            refresh.paragraphs(etree.fromstring(xml.encode()))

    def test_disclosure_names_actual_roles_and_incomplete_semantic_scope(self):
        for model in ('GPT-5.6 Sol', 'GPT-6 Sol', 'GPT-6.1 Sol'):
            self.assertIn(model, refresh.DISCLOSURE)
        self.assertIn('Ultra', refresh.DISCLOSURE)
        self.assertIn('لا يدعي', refresh.DISCLOSURE)


if __name__ == '__main__':
    unittest.main()
