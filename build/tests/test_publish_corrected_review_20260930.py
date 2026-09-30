import unittest
import hashlib
import json
from pathlib import Path
import tempfile
from unittest.mock import patch
from build import publish_corrected_review_20260930 as publication


class CorrectedReviewPublicationTests(unittest.TestCase):
    def test_five_replacements_and_two_additions_fit_100_file_cap(self):
        self.assertEqual(len(publication.NAMES),7)
        self.assertEqual(len(publication.REPLACED),5)
        self.assertTrue(set(publication.REPLACED)<=set(publication.NAMES))
        self.assertEqual(98-len(publication.REPLACED)+len(publication.NAMES),100)

    def test_public_notes_distinguish_batch_from_full_semantic_recheck(self):
        self.assertIn('كلها ما زالت جارية',publication.NOTES)
        for model in ('GPT-5.6 Sol','GPT-6 Sol','GPT-6.1 Sol'):
            self.assertIn(model,publication.NOTES)
        self.assertIn('Ultra',publication.NOTES)
        self.assertIn(publication.ENTRY,publication.NOTES)
        self.assertIn(publication.FULL,publication.NOTES)

    def test_staged_files_are_independent_of_later_source_edits(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); base=root/'base'; base.mkdir()
            for name in publication.NAMES[:-1]:
                (base/name).write_bytes(('snapshot '+name).encode())
            sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
            fresh={'all_frozen_occurrences_preserved':True,'verified_machine_records':1095,
                   'directory_sha256':sha(base/'DIRECTORY_AR.md').upper(),
                   'machine_record_sha256':sha(base/'DECISION_RECORD_AR.jsonl.gz').upper()}
            cold={'status':'PASS_COLD_REPLAY_FROM_EXACT_CORRECTED_REVIEW_ZIP',
                  'source_zip_sha256':sha(base/publication.NAMES[-2]),
                  'byte_identical_outputs':{name:sha(base/name) for name in publication.NAMES[:-1]}}
            (base/publication.STRUCTURAL_RECEIPT).write_text(json.dumps(fresh))
            (base/publication.COLD_RECEIPT).write_text(json.dumps(cold))
            with patch.multiple(publication,BASE=base,STAGE=root/'stage',STATE=root/'state'):
                publication.stage()
                accepted=(root/'stage'/'INDEX_AR.md').read_bytes()
                (base/'INDEX_AR.md').write_bytes(b'later independent edit')
                self.assertEqual((root/'stage'/'INDEX_AR.md').read_bytes(),accepted)
                self.assertEqual((base/'INDEX_AR.md').stat().st_nlink,1)
                self.assertEqual((root/'stage'/'INDEX_AR.md').stat().st_nlink,1)


if __name__=='__main__':
    unittest.main()
