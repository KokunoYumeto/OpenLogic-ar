"""Finite coverage and source integrity, not full semantic certification."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'build'))
import assemble_complete_arabic_review as assembly
import render_contextual_recheck_20260930 as review


class ContextualRecheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(review.LEDGER.read_bytes())
        cls.frozen=review.frozen_records()

    def test_exact_seven_groups_and_twenty_one_locations(self):
        self.assertEqual(review.bind(self.data,self.frozen),self.data)
        self.assertEqual(sum(len(r['checked_occurrences']) for r in self.data['records']),21)
        self.assertEqual(sum(len(r['original_occurrences']) for r in self.data['records']),7)

    def test_additional_or_missing_occurrence_rejected(self):
        old=copy.deepcopy(self.frozen)
        old[0]['index_metadata']['occurrences'].append(copy.deepcopy(old[0]['index_metadata']['occurrences'][0]))
        with self.assertRaisesRegex(ValueError,'identities changed'):
            review.bind(self.data,old)

    def test_changed_source_and_context_definition_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);english=root/'english'
            for row in self.data['records']:
                for field in ['source_bindings','target_bindings','context_bindings']:
                    for w in row.get(field,[]):
                        is_en=field=='source_bindings' or w.get('source_kind')=='english'
                        source=(review.ENGLISH if is_en else ROOT)/w['logical_path']
                        target=(english if is_en else root)/w['logical_path']
                        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes())
            row=next(r for r in self.data['records'] if 'context_bindings' in r)
            w=row['context_bindings'][0];target=english/w['logical_path']
            target.write_bytes(target.read_bytes().replace(b'surjective',b'injective',1))
            with self.assertRaisesRegex(ValueError,'Changed inspected source'):
                review.bind(self.data,self.frozen,root,english)

    def test_retention_cannot_substitute_term(self):
        data=copy.deepcopy(self.data);data['records'][0]['surface_ar']='تطبيق تقابلي'
        with self.assertRaisesRegex(ValueError,'substitute wording'):
            review.bind(data,self.frozen)

    def test_glossary_correction_and_countability_limits_are_explicit(self):
        glossary=next(r for r in self.data['records'] if r['decision_id'].endswith(':glossary'))
        self.assertIn('ليس قائمة مصطلحات أطول',glossary['rationale_ar'])
        self.assertIn('لا يلزم من لفظ معجم',glossary['rationale_ar'])
        self.assertEqual(glossary['canon_evidence'],[])
        self.assertIn('فجوة',glossary['canon_limit_ar'])
        countable=next(r for r in self.data['records'] if '7a619a6b3e5be629' in r['decision_id'])
        self.assertEqual(len(countable['context_bindings']),12)
        self.assertIn('الخالية',countable['sense_ar'])
        self.assertIn('خوارزمية',countable['sense_ar'])
        bijective=next(r for r in self.data['records'] if '895d9bd2ecaafef3' in r['decision_id'])
        approximate=[p for loc in bijective['checked_occurrences'] for p in loc['page_evidence'] if not p['exact_occurrence_page']]
        self.assertEqual(len(approximate),3)
        self.assertIn('صفحة بدء فقط',self.data['source_identity_note_ar'])

    def test_full_index_integration_keeps_originals_and_readable_card(self):
        notes,cards=assembly.note_map(),assembly.card_map()
        self.assertEqual(len(cards),1095)
        for row in self.data['records']:
            self.assertEqual(cards[row['decision_id']],review.CARD)
            self.assertEqual(notes[row['decision_id']]['checked_occurrences'],row['checked_occurrences'])
        card=(review.BASE/review.CARD).read_text(encoding='utf-8')
        self.assertEqual(card,review.render(self.data))
        self.assertEqual(card.count('**أين وما الذي يراجع؟**'),5)
        self.assertIn('بدء القسم فقط، ليس وقوع اللفظ',card)


class ProofQuantificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path=ROOT/'evidence/classical/terminology/SOL6_PROOF_QUANTIFICATION_RECHECK_20260930.json'
        cls.data=json.loads(cls.path.read_bytes())
        cls.frozen=review.frozen_records(cls.data['finite_scope']['decision_ids'])

    def test_exact_nine_groups_and_sixty_nine_locations(self):
        self.assertEqual(review.bind(self.data,self.frozen),self.data)
        self.assertEqual(sum(len(r['original_occurrences']) for r in self.data['records']),9)
        self.assertEqual(sum(len(r['checked_occurrences']) for r in self.data['records']),69)
        self.assertEqual(len({l['location_id'] for r in self.data['records'] for l in r['checked_occurrences']}),69)

    def test_new_context_does_not_overwrite_five_unresolved_originals(self):
        unresolved=[l for r in self.data['records'] for g in r['original_occurrences'] for l in g['locations'] if not l['line_reconciliation']['resolved']]
        self.assertEqual(len(unresolved),5)
        for loc in unresolved:
            self.assertIsNone(loc['line_reconciliation']['current_line_start'])
        checked=[l for r in self.data['records'] for l in r['checked_occurrences'] if l['location_id'] in {l['location_id'] for l in unresolved}]
        self.assertEqual(sum(l['literal_term_in_english'] for l in checked),2)
        translation=next(l for l in checked if 'quantifier:occ003:' in l['location_id'])
        self.assertFalse(translation['literal_term_in_english'])
        self.assertNotIn('quantifier',translation['exact_passage'])
        self.assertIn('غير حرفي',translation['binding_reason_ar'])

    def test_exact_predecessor_inverse_and_rule_blocks(self):
        t=self.data['source_transitions'][0]
        before=review.transition_predecessor(t)
        self.assertEqual(review.sha(before),'4a35f7a7a408828a889a9df3233addcc625b4ff2551af04ad4d8f0b248983b23')
        self.assertEqual(len(before),4709)
        self.assertEqual(len(t['edits']),2)
        self.assertIn('الحد المغلق',t['edits'][1]['after_text'])
        self.assertIn('استثناء الافتراضات',t['edits'][0]['after_text'])

    def test_declaring_a_new_hash_cannot_admit_arbitrary_drift(self):
        t=copy.deepcopy(self.data['source_transitions'][0])
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);target=root/t['logical_path'];target.parent.mkdir(parents=True)
            raw=(ROOT/t['logical_path']).read_bytes()+b'% arbitrary new change\n'
            target.write_bytes(raw);t['after_sha256']=review.sha(raw);t['after_bytes']=len(raw)
            with self.assertRaisesRegex(ValueError,'inverse differs'):
                review.transition_predecessor(t,root)

    def test_missing_context_or_forged_frozen_occurrence_rejected(self):
        data=copy.deepcopy(self.data)
        row=next(r for r in data['records'] if r['decision_id'].endswith('logical-connective'))
        row['fresh_location_bindings'].clear()
        with self.assertRaisesRegex(ValueError,'Missing explicit new context'):
            review.bind(data,self.frozen)
        data=copy.deepcopy(self.data);data['records'][0]['original_occurrences'][0]['locations'].pop()
        with self.assertRaisesRegex(ValueError,'identities changed'):
            review.bind(data,self.frozen)

    def test_assembly_and_links_distinguish_current_source_from_old_reader(self):
        notes,cards=assembly.note_map(),assembly.card_map()
        self.assertEqual(len(cards),1095)
        for row in self.data['records']:
            self.assertEqual(cards[row['decision_id']],self.data['review_card'])
            self.assertEqual(notes[row['decision_id']]['checked_occurrences'],row['checked_occurrences'])
        card=(review.BASE/self.data['review_card']).read_text(encoding='utf-8')
        self.assertEqual(card,review.render(self.data))
        self.assertIn('لم يُبن أو يُنشر بعد PDF/EPUB',card)
        relative=self.data['source_transitions'][0]['logical_path']
        self.assertIn('../../'+relative+'#L57-L59',card)
        self.assertNotIn(self.data['arabic_source_commit']+'/'+relative,card)
        eigen=next(r for r in self.data['records'] if 'eigenvariable' in r['decision_id'])
        self.assertIn('الاستنتاج الطبيعي',eigen['sense_ar'])
        self.assertIn('فجوة توثيق',eigen['canon_limit_ar'])
        quantifier=next(r for r in self.data['records'] if r['decision_id'].endswith('-quantifier'))
        self.assertIn('لعلاقة أو دالة',quantifier['sense_ar'])


if __name__=='__main__':unittest.main()
