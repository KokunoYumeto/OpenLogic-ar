import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from recover_remaining_arabic_review_witnesses import ranked_line


class CandidateSelectionTests(unittest.TestCase):
    def test_comments_and_section_names_are_not_definition_witnesses(self):
        rows = ['% Section: computably-axiomatizable', r'\olsection{axiomatizable Theories}',
                'A theory is axiomatizable if it has a computable set of axioms.']
        found = ranked_line(rows, 'axiomatizable / axiomatized', False)
        self.assertEqual(found['line'], 3)
        self.assertEqual(found['status'], 'token-candidate-not-yet-verified')

    def test_a_heading_only_hit_is_not_fabricated_as_prose(self):
        found = ranked_line(['% Section: cardinality', r'\olsection{Cardinality}', 'Other content.'], 'cardinality', False)
        self.assertIsNone(found['line'])
        self.assertEqual(found['status'], 'term-not-found')


if __name__ == '__main__':
    unittest.main()
