"""Prove the new gate rejects the preserved, actually defective v6 PDFs."""
import copy
import json
from pathlib import Path
import unittest
import pdfplumber
from build import qa_classical_rtl_math_probe as qa

ROOT = Path(__file__).resolve().parents[2]


class VisibleGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads((ROOT / 'evidence/classical/RTL_MATH_PROBE_V6_OWNER_20260907.json').read_bytes())
        cls.primary = Path(cls.receipt['build_manifests']['primary']['path']).parent

    def actual(self, job):
        row = self.receipt['artifacts']['primary'][job]
        path = self.primary / (job + '.pdf')
        self.assertEqual(qa.sha256(path).lower(), row['sha256'].lower())
        with pdfplumber.open(path) as document:
            return qa.visible_semantic_checks(document, row['geometry_anchors'], job)

    def test_old_control_has_all_fourteen_real_glyph_checks(self):
        checks = self.actual('control')
        self.assertEqual(len(checks), 14)
        self.assertTrue(all(c['pass'] for c in checks))

    def test_historical_rtl_rejected_at_all_eight_fences_and_six_nodes(self):
        checks = self.actual('rtl')
        self.assertEqual(sum(not c['pass'] for c in checks), 14)
        self.assertEqual(sum(c['kind'] == 'inward-facing-delimiter' for c in checks), 8)

    def test_positive_render_model_and_coincident_extra_wrong_glyph_rejection(self):
        # Artificial glyph model tests the predicate only, not engine rendering.
        row = self.receipt['artifacts']['primary']['control']
        anchors = copy.deepcopy(row['geometry_anchors'])
        with pdfplumber.open(self.primary / 'control.pdf') as document:
            self.assertTrue(all(c['pass'] for c in qa.visible_semantic_checks(document, anchors, 'control')))
            # Moving all three node anchors to one operand cannot be accepted.
            for suffix in ('op', 'B'):
                anchors['P11-root-' + suffix]['rect'] = anchors['P11-root-A']['rect'][:]
            checks = qa.visible_semantic_checks(document, anchors, 'control')
            self.assertFalse(next(c for c in checks if c['key'] == 'P11-root')['pass'])

    def test_new_schema_and_no_silent_success_on_old_contract(self):
        self.assertEqual(qa.SCHEMA, 'openlogic-classical-rtl-math-runtime-probe-v7')
        self.assertNotEqual(self.receipt['schema'], qa.SCHEMA)


if __name__ == '__main__':
    unittest.main()
