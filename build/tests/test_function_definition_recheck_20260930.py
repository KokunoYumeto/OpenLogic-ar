"""Finite source/card checks; do not equate them with whole-book approval."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'build'))
import assemble_complete_arabic_review as assembly
import render_function_definition_recheck_20260930 as review
from stream_expert_review_decisions import iter_decisions


class FunctionDefinitionRecheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(review.LEDGER.read_bytes())
        ids = {r['decision_id'] for r in cls.data['records']}
        cls.frozen = [r for r in iter_decisions(review.INDEX) if r['decision_id'] in ids]

    def test_all_nine_frozen_locations_bound_without_body_substitution(self):
        bound = review.bind(self.data, self.frozen)
        self.assertEqual(bound, self.data)
        self.assertEqual(sum(len(r['checked_occurrences']) for r in bound['records']), 9)
        for row in bound['records']:
            old = next(r for r in self.frozen if r['decision_id'] == row['decision_id'])
            self.assertEqual(row['original_occurrences'], old['index_metadata']['occurrences'])
            self.assertEqual(len(row['source_bindings']), 1)
            self.assertEqual(len(row['target_bindings']), 2)
            self.assertTrue(row['open_to_correction'])

    def test_uninspected_additional_occurrence_rejected(self):
        old = copy.deepcopy(self.frozen)
        old[0]['index_metadata']['occurrences'][0]['locations'].append(
            copy.deepcopy(old[0]['index_metadata']['occurrences'][0]['locations'][0]))
        with self.assertRaisesRegex(ValueError, 'additional location'):
            review.bind(self.data, old)

    def test_changed_source_bytes_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            english = root / 'english'
            for row in self.data['records']:
                for field, source, destination in (
                        ('source_bindings', review.ENGLISH, english),
                        ('target_bindings', ROOT, root)):
                    for witness in row[field]:
                        target = destination / witness['logical_path']
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes((source / witness['logical_path']).read_bytes())
            changed = root / self.data['records'][0]['target_bindings'][0]['logical_path']
            changed.write_bytes(changed.read_bytes().replace('معًا'.encode(), 'فقط'.encode(), 1))
            with self.assertRaisesRegex(ValueError, 'Changed source bytes'):
                review.bind(self.data, self.frozen, english, root)

    def test_retention_cannot_silently_change_term(self):
        data = copy.deepcopy(self.data)
        data['records'][0]['surface_ar'] = 'تطبيق تقابلي'
        with self.assertRaisesRegex(ValueError, 'silently substitute'):
            review.bind(data, self.frozen)

    def test_independent_injection_witness_and_surjection_gap_remain_explicit(self):
        rows = {r['surface_ar']: r for r in self.data['records']}
        injection = rows['دالة متباينة']
        self.assertEqual([e['physical_pdf_page'] for e in injection['canon_evidence']
                          if e['source_id'] == 'DAM2018ENAR'], [361, 362])
        surjection = rows['دالة شاملة']
        self.assertIn('لم تثبت', surjection['canon_limit_ar'])
        self.assertIn('غامر', surjection['canon_limit_ar'])
        self.assertIn('وحدانيته غير مطلوبة', surjection['sense_ar'])
        self.assertIn('هوية الطبعات الفعلية غير مثبتة', self.data['register_comparison']['limits_ar'])

    def test_integrated_notes_use_new_card_and_canon_without_replacing_frozen_occurrences(self):
        notes, cards = assembly.note_map(), assembly.card_map()
        for row in self.data['records']:
            identifier = row['decision_id']
            self.assertEqual(notes[identifier]['canon_evidence'], row['canon_evidence'])
            self.assertEqual(cards[identifier], self.data['review_card'])
        self.assertEqual(len(cards), 1095)
        actual = (review.BASE / self.data['review_card']).read_text(encoding='utf-8')
        self.assertEqual(actual, review.render(self.data))
        self.assertEqual(actual.count('**ما الذي يستحق المراجعة؟**'), 3)
        for row in self.data['records']:
            self.assertIn(row['decision_id'], actual)
            self.assertIn(row['expert_question_ar'], actual)


if __name__ == '__main__':
    unittest.main()
