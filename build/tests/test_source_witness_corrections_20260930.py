"""Check the finite correction layer without inferring semantic approval."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
TERM=ROOT/'evidence/classical/terminology'
BASE=ROOT/'expert-review/2026-09-26-final-page-review'


class SourceWitnessCorrectionTests(unittest.TestCase):
    def test_59_removed_pointers_have_32_explicit_replacements(self):
        value=json.loads((TERM/'SOL6_SOURCE_WITNESS_CORRECTIONS_20260930.json').read_bytes())
        self.assertEqual(len(value['records']),32)
        self.assertEqual(len({r['decision_id'] for r in value['records']}),32)
        self.assertEqual(sum(len(r['removed_non_supporting_pointers']) for r in value['records']),59)
        for record in value['records']:
            self.assertTrue(record['replacement_bindings'])
            for b in record['replacement_bindings']:
                raw=(BASE/'reexamination-source/english'/b['logical_path']).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(),b['sha256'])
                selected='\n'.join(raw.decode('utf-8').splitlines()[b['line_start']-1:b['line_end']])
                self.assertEqual(selected,b['exact_passage'])
                self.assertTrue(any(line.strip() and not line.strip().startswith('%') for line in selected.splitlines()))

    def test_three_wrong_concept_explanations_are_explicitly_corrected(self):
        value=json.loads((TERM/'SOL6_REEXAMINATION_CORRECTIONS_20260930.json').read_bytes())
        records={r['decision_id']:r for r in value['records']}
        self.assertEqual(len(records),5)
        self.assertIn('نماذج منتهية',records['compact:T-OVERSPILL']['sense_ar'])
        for identifier in ('compact:T-REDUCT-EXPANSION','locale-ar-chosen-62c0c8a085b90bd0'):
            self.assertIn('المجال',records[identifier]['sense_ar'])
            self.assertIn('نفسه',records[identifier]['sense_ar'])
            self.assertTrue(records[identifier]['target_bindings'])

    def test_public_source_receipt_binds_current_layers(self):
        receipt=json.loads((BASE/'SOURCE_WITNESS_PUBLIC_READBACK_20260930.json').read_bytes())
        self.assertEqual(receipt['status'],'PASS_ANONYMOUS_EXACT_PINNED_SOURCE_READBACK')
        self.assertEqual(len(receipt['files']),44)
        for key,name in (('manifest_sha256','SOL6_SOURCE_WITNESS_CORRECTIONS_20260930.json'),
                         ('correction_sha256','SOL6_REEXAMINATION_CORRECTIONS_20260930.json')):
            self.assertEqual(receipt[key],hashlib.sha256((TERM/name).read_bytes()).hexdigest())


if __name__=='__main__':
    unittest.main()
