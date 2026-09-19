"""A presentation recovery must not silently admit new scholarly inputs."""
import copy
import unittest
from build import resume_review_surfaces_20260920 as recovery


class RecoveryAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.old={'schema':'test', 'semantic_amendments':[{'path':'decision.json','sha256':'old'}],
            'supporting_inputs':[{'path':p,'sha256':'old'} for p in sorted(recovery.CODE_SUCCESSORS)]
                +[{'path':'unchanged.tex','sha256':'fixed'}]}
        self.new=copy.deepcopy(self.old)
        for row in self.new['supporting_inputs'][:2]: row['sha256']='new'

    def test_exact_two_code_successors_are_admitted(self):
        self.assertEqual(len(recovery.admit_inventory(self.old,self.new)),2)

    def test_changed_amendment_unrelated_input_and_duplicate_are_rejected(self):
        for mode in ('amendment','unrelated','duplicate','missing-fix'):
            changed=copy.deepcopy(self.new)
            if mode=='amendment': changed['semantic_amendments'][0]['sha256']='new'
            elif mode=='unrelated': changed['supporting_inputs'][-1]['sha256']='new'
            elif mode=='duplicate': changed['supporting_inputs'].append(changed['supporting_inputs'][0])
            else: changed['supporting_inputs'][0]['sha256']='old'
            with self.subTest(mode=mode),self.assertRaises(ValueError):
                recovery.admit_inventory(self.old,changed)

    def test_record_fingerprint_detects_wording_or_order_change(self):
        rows=[{'id':'a','rationale':'سبب'}, {'id':'b','rationale':'سبب ثان'}]
        expected=recovery.record_digest(rows)
        self.assertEqual(expected,recovery.record_digest(copy.deepcopy(rows)))
        self.assertNotEqual(expected,recovery.record_digest(list(reversed(rows))))
        changed=copy.deepcopy(rows); changed[0]['rationale']='different'
        self.assertNotEqual(expected,recovery.record_digest(changed))


if __name__=='__main__': unittest.main()
