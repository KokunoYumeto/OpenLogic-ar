"""Check the real eleven-choice batch, source bindings and human display.

Byte checks do not prove the correctness of manual Arabic scholarly judgment.
No translation mutation, TeX process or entire-index JSON load is performed.
"""
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from build import amend_relation_decisions_20260919 as batch
from build import generate_expert_review_index as index
from build.validate_expert_review_snapshot import verify_canon_amendment_v2


class ElevenRelationChoicesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload=batch.build()
        cls.entries=cls.payload['amendments']

    def test_eleven_actual_templates_all_supplied_occurrences_and_no_source_edits(self):
        self.assertEqual(len(self.entries),11)
        self.assertEqual(len({r['decision_id'] for r in self.entries}),11)
        self.assertEqual(sum(len(r['checked_occurrences'][0]['locations']) for r in self.entries),33)
        for entry in self.entries:
            self.assertIn('This is a present-tense retrospective justification',entry['expected']['rationale'])
            self.assertNotIn('This is a present-tense retrospective justification',entry['changes']['rationale'])
            self.assertEqual(entry['proposed_source_edits'],[])
            self.assertFalse(entry['current_editorial_assessment']['source_edit_applied'])
            self.assertTrue(entry['contextual_coverage']['all_supplied_occurrences_checked'])

    def test_current_source_excerpts_and_term_locations_are_exact(self):
        files=set()
        for entry in self.entries:
            for witness,loc in zip(entry['witnesses'],entry['checked_occurrences'][0]['locations'],strict=True):
                root=batch.ENGLISH if witness['source_kind']=='english' else batch.REPO
                path=root/witness['path']; files.add(path)
                raw=path.read_bytes(); lines=raw.decode('utf-8-sig').splitlines()
                self.assertEqual(hashlib.sha256(raw).hexdigest(),witness['file_sha256'])
                self.assertEqual('\n'.join(lines[witness['line_start']-1:witness['line_end']]),witness['excerpt'])
                self.assertEqual(witness['file_sha256'],loc['sha256'])
                self.assertTrue(witness['line_start']<=loc['line_start']<=loc['line_end']<=witness['line_end'])
                ev=entry['canon_evidence'][0]
                phrase=ev['english_source_phrase'] if witness['source_kind']=='english' else ev['chosen_arabic_form']
                self.assertIn(phrase.casefold(),'\n'.join(lines[loc['line_start']-1:loc['line_end']]).casefold())
        self.assertEqual(len(files),12)

    def test_independent_verifier_and_nonliteral_claims(self):
        for entry in self.entries:
            self.assertTrue(verify_canon_amendment_v2(batch.REPO,entry,batch.ENGLISH))
            self.assertFalse(entry['official_attestation_claimed'])
            self.assertEqual(entry['canon_evidence'][0]['relation'],'related-not-exact')

    def test_fresh_ledger_admission_and_readable_explanation(self):
        rows,_,_=index.load_decisions(batch.REPO,[batch.REPO/'evidence/classical/terminology/retro-0005-0050.json'],[],batch.ENGLISH)
        wanted={r['decision_id'] for r in self.entries}
        rows=[r for r in rows if r['decision_id'] in wanted]
        self.assertEqual(len(rows),11)
        with tempfile.TemporaryDirectory(prefix='relation-amendment-test-',dir=batch.REPO/'tmp') as directory:
            root=Path(directory)
            (root/'batch.json').write_text(json.dumps(self.payload,ensure_ascii=False),encoding='utf-8')
            with patch.object(index,'EXPERT_AMENDMENTS_RELATIVE',root.relative_to(batch.REPO)):
                identities,_=index.apply_expert_review_amendments(batch.REPO,rows,batch.ENGLISH)
        self.assertEqual(identities[0]['amendment_count'],11)
        for row in rows:
            human=index.human_decision_field(row,'rationale')
            self.assertIn('physical PDF page',human)
            self.assertIn('printed page',human)
            self.assertIn('current form is not literally attested',human)
            self.assertNotIn('This is a present-tense retrospective justification',human)
            assessment=row['expert_review_assessment']
            old_alternatives=copy.deepcopy(row.get('alternatives'))
            unit_id=assessment['checked_occurrences'][0]['unit_id']
            row['index_metadata']={'human_index_included':True,'occurrences':[
                {'unit':{'unit_id':unit_id,'title':'test occurrence'},'locations':[],
                 'human_review_included':True,'language_coverage':{'not_recorded_source_kinds':[]}}]}
            exported=list(csv.reader(io.StringIO(index.render_occurrence_csv({'decisions':[row]}))))
            self.assertEqual(len(exported),2)
            self.assertIn(assessment['changes']['expert_question'],exported[1][12])
            self.assertIn(assessment['current_editorial_assessment']['alternative_comparison'],exported[1][4])
            self.assertIn('Current alternative comparison',exported[1][4])
            self.assertEqual(row.get('alternatives'),old_alternatives)

    def test_changed_witness_and_false_exact_attestation_rejected(self):
        for field in ('witness','claim','image'):
            entry=copy.deepcopy(self.entries[0])
            if field=='witness': entry['witnesses'][0]['file_sha256']='0'*64
            elif field=='claim': entry['official_attestation_claimed']=True
            else: entry['canon_evidence'][0]['page_image']['sha256']='0'*64
            with self.assertRaises(ValueError):
                verify_canon_amendment_v2(batch.REPO,entry,batch.ENGLISH)

    def test_discretionary_hyphens_are_bound_not_invented_lexical_content(self):
        entry=next(r for r in self.entries if r['decision_id'].endswith('91e56faf5ecdc898'))
        self.assertEqual(entry['expected']['chosen_arabic'],'مضادّة للتناظر')
        self.assertEqual(entry['observed_arabic_forms'][0]['form'],r'مضادّة\- للتناظر\-')
        self.assertIn('discretionary',entry['changes']['rationale'])

    def test_sensitive_distinctions_and_alternatives_remain_explicit(self):
        rows={r['decision_id'].rsplit(':',1)[-1]:r for r in self.entries}
        self.assertIn('diagonal',rows['a41652349417a154']['changes']['rationale'])
        self.assertIn('x≠y',rows['aae883d44b7db318']['changes']['rationale'])
        self.assertIn('الجداء الديكارتي',rows['f7c277e69d8cf7d5']['changes']['expert_question'])
        self.assertIn('ring',rows['3f36b6b993e1028e']['changes']['rationale'])


if __name__=='__main__': unittest.main()
