"""Finite v2 admission/readback tests; synthetic identity fixtures, no PDF build."""
import copy
import json
from pathlib import Path
import unittest

from build.tests.test_expert_review_amendments import ExpertReviewAmendmentTests, INDEX
from build import validate_expert_review_snapshot as readback


class ExpertReviewAmendmentV2Tests(unittest.TestCase):
    def setUp(self):
        ExpertReviewAmendmentTests.setUp(self)
        self.decision['official_attestation_claimed'] = False
        self.decision['expert_review_useful'] = False
        self.decision['expert_review_reason'] = 'Historical automatic flag.'
        self.source = self.root.parent / 'sources/dictionary.pdf'
        self.image = self.root / 'tmp/pdfs/canon/page.png'
        for path, content in ((self.source, b'Synthetic dictionary identity fixture, not a PDF.'),
                              (self.image, b'Synthetic page identity fixture, not a raster.')):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        def identity(path, relative):
            return {'path': relative, 'bytes': path.stat().st_size, 'sha256': INDEX.sha256_file(path)}
        passage = 'injective function — دالة متباينة'
        self.canon = {
            'source': {**identity(self.source, '../sources/dictionary.pdf'),
                       'title': 'Synthetic bilingual dictionary', 'source_id': 'test-dictionary',
                       'url': 'https://example.test/dictionary'},
            'page_image': identity(self.image, 'tmp/pdfs/canon/page.png'),
            'physical_page': 3, 'printed_page': '1', 'entry': 'injective function',
            'exact_passage': passage, 'passage_sha256': INDEX.sha256_bytes(passage.encode('utf-8')),
            'transcription_mode': 'manual-visual-transcription-diacritics-normalized',
            'consulted_before_assessment': True, 'consulted_on': '2026-09-06',
            'recording_mode': 'retrospective-canon-check',
            'chosen_arabic_form': self.decision['chosen_arabic'],
            'attested_arabic_form': self.decision['chosen_arabic'],
            'english_headword': 'injective function', 'english_source_phrase': 'Distinct inputs',
            'english_sense': self.entry['changes']['sense'], 'relation': 'exact-chosen-form',
            'source_witness_indices': [1], 'english_witness_indices': [0],
            'relevance': 'The same distinct-input sense is compared in the cited source context.',
            'limits': 'Synthetic test only. Manual transcription correctness is not automated.',
        }
        self.entry['official_attestation_claimed'] = True
        self.entry['canon_evidence'] = [self.canon]

    def write_ledger(self, entries=None, schema=None):
        self.ledger.parent.mkdir(parents=True, exist_ok=True)
        self.ledger.write_text(json.dumps({
            'schema': schema or INDEX.EXPERT_AMENDMENT_SCHEMA_V2,
            'amendments': entries or [self.entry]}, ensure_ascii=False), encoding='utf-8')

    def apply(self):
        return INDEX.apply_expert_review_amendments(self.root, [self.decision], self.english)

    def independent(self):
        return readback.verify_canon_amendment_v2(self.root, self.entry, self.english)

    def reject_both(self):
        self.write_ledger()
        before = copy.deepcopy(self.decision)
        with self.assertRaises((ValueError, KeyError, TypeError, OSError)):
            self.apply()
        self.assertEqual(self.decision, before)
        with self.assertRaises((ValueError, KeyError, TypeError, OSError)):
            self.independent()

    def test_exact_attestation_preserves_history_and_hashes_every_input(self):
        self.write_ledger()
        identities, hashes = self.apply()
        self.assertEqual(len(identities), 1)
        self.assertEqual(len(hashes), 5)
        self.assertEqual(len(self.independent()), 4)
        assessment = self.decision['expert_review_assessment']
        self.assertIs(self.decision['official_attestation_claimed'], True)
        self.assertIs(assessment['original_fields']['official_attestation_claimed'], False)
        self.assertEqual(assessment['canon_evidence'], [self.canon])
        self.assertEqual(self.decision['chosen_arabic'], 'دالة متباينة')

    def test_v1_still_cannot_claim_attestation(self):
        self.write_ledger(schema=INDEX.EXPERT_AMENDMENT_SCHEMA)
        with self.assertRaisesRegex(ValueError, 'invalid assessment provenance'):
            self.apply()

    def test_ledger_cannot_spoof_generated_provenance_or_bypass_v1(self):
        for field in ('amendment_schema', 'original_fields', 'ledger_path'):
            with self.subTest(field=field):
                self.entry[field] = INDEX.EXPERT_AMENDMENT_SCHEMA_V2
                self.reject_both()
                del self.entry[field]
        self.entry['official_attestation_claimed'] = False
        self.entry['amendment_schema'] = INDEX.EXPERT_AMENDMENT_SCHEMA_V2
        self.write_ledger(schema=INDEX.EXPERT_AMENDMENT_SCHEMA)
        with self.assertRaisesRegex(ValueError, 'reserved generated'):
            self.apply()

    def test_unsupported_true_and_changed_literal_rejected_atomically(self):
        original = copy.deepcopy(self.entry)
        for mode in ('missing', 'related', 'different-form', 'not-chosen', 'sense', 'commented-context'):
            with self.subTest(mode=mode):
                self.entry = copy.deepcopy(original)
                evidence = self.entry['canon_evidence'][0]
                if mode == 'missing':
                    self.entry['canon_evidence'] = []
                elif mode == 'related':
                    evidence['relation'] = 'related-not-exact'
                elif mode == 'different-form':
                    evidence['chosen_arabic_form'] = 'الدالة المتباينة'
                elif mode == 'not-chosen':
                    evidence['attested_arabic_form'] = 'متباينة'
                elif mode == 'sense':
                    evidence['english_sense'] = 'Surjectivity.'
                else:
                    evidence['english_source_phrase'] = '% title'
                self.reject_both()

    def test_changed_source_image_or_passage_is_rejected(self):
        original = copy.deepcopy(self.entry)
        for mode in ('source-hash', 'source-bytes', 'image-hash', 'passage'):
            with self.subTest(mode=mode):
                self.entry = copy.deepcopy(original)
                evidence = self.entry['canon_evidence'][0]
                if mode == 'source-hash':
                    evidence['source']['sha256'] = '0' * 64
                elif mode == 'source-bytes':
                    evidence['source']['bytes'] += 1
                elif mode == 'image-hash':
                    evidence['page_image']['sha256'] = '0' * 64
                else:
                    evidence['exact_passage'] += ' altered'
                self.reject_both()

    def test_source_drift_rejected_by_both_paths(self):
        self.source.write_bytes(self.source.read_bytes() + b' changed')
        self.reject_both()

    def test_false_related_evidence_remains_explicit_without_certifying_current_form(self):
        self.entry['official_attestation_claimed'] = False
        self.canon['relation'] = 'related-not-exact'
        self.canon['attested_arabic_form'] = 'متباينة'
        self.write_ledger()
        self.apply()
        self.independent()
        self.assertIs(self.decision['official_attestation_claimed'], False)
        self.assertIn('current form is not literally attested', INDEX.human_decision_field(self.decision, 'rationale'))

    def test_dates_pages_provenance_and_context_indices_fail_closed(self):
        original = copy.deepcopy(self.entry)
        for field, value in [('physical_page', True), ('printed_page', ''),
                             ('consulted_on', '2026-09-07'), ('consulted_before_assessment', False),
                             ('recording_mode', 'original-translator-thought'),
                             ('transcription_mode', 'unspecified'),
                             ('source_witness_indices', [0]), ('english_witness_indices', [1]),
                             ('source_witness_indices', [True]), ('source_witness_indices', [1, 1])]:
            with self.subTest(field=field, value=value):
                self.entry = copy.deepcopy(original)
                self.entry['canon_evidence'][0][field] = value
                self.reject_both()

    def test_sensitive_choice_can_be_promoted_with_history_but_not_downgraded(self):
        self.entry['changes'].update(expert_review_useful=True, expert_review_reason='Dictionary/source divergence.')
        self.write_ledger()
        self.apply()
        self.independent()
        original = self.decision['expert_review_assessment']['original_fields']
        self.assertIs(original['expert_review_useful'], False)
        self.assertEqual(original['expert_review_reason'], 'Historical automatic flag.')
        self.assertIs(self.decision['expert_review_useful'], True)
        self.entry['changes']['expert_review_useful'] = False
        self.reject_both()

    def test_canon_readback_rejects_missing_human_evidence(self):
        self.write_ledger()
        self.apply()
        lines = []
        INDEX.append_assessment_provenance(lines, self.decision, '../../')
        rationale = INDEX.human_decision_field(self.decision, 'rationale')
        section = '\n'.join(lines)
        values = [''] * 13
        values[5] = rationale
        errors = []
        readback.verify_canon_surfaces('test', self.entry, self.decision['expert_review_assessment'],
            self.decision, {'complete': {'test': [section]}}, {'test': [values]}, errors)
        self.assertEqual(errors, [])
        readback.verify_canon_surfaces('test', self.entry, self.decision['expert_review_assessment'],
            self.decision, {'complete': {'test': ['no canon evidence']}}, {'test': [[''] * 13]}, errors)
        self.assertTrue(any('fresh canon evidence' in message for message in errors))


if __name__ == '__main__':
    unittest.main()
