import unittest
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


if __name__=='__main__':
    unittest.main()
