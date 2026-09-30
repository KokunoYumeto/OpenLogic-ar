import unittest
from build import publish_msa_epub_successor_20260930 as release


class EPubSuccessorScopeTests(unittest.TestCase):
    def test_replacements_are_exactly_seven_existing_assets(self):
        self.assertEqual(len(release.CHANGED), 7)
        self.assertEqual(len(set(release.CHANGED)), 7)
        self.assertTrue(all(not n.startswith(('26_', '27_', '28_')) for n in release.CHANGED))

    def test_preserved_pdf_preview_and_lineage(self):
        release.configure()
        self.assertEqual(release.zenodo.PREVIOUS, 23060802)
        self.assertEqual(release.zenodo.CONCEPT, 21921850)
        self.assertEqual(release.zenodo.EXPECTED_PREDECESSOR_FILES, 100)
        self.assertEqual(release.zenodo.PREVIEW, '00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf')
        self.assertEqual(release.zenodo.ORDER_PREFIX[1], '01_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.tex')

    def test_source_pairs_and_disclosures_have_honest_scope(self):
        self.assertEqual(len(release.SOURCE_IDS), 4)
        for model in ('GPT-5.6 Sol', 'GPT-6 Sol', 'GPT-6.1 Sol'):
            self.assertIn(model, release.NOTES)
        self.assertIn('Ultra', release.NOTES)
        self.assertIn('ما زالت جارية', release.NOTES)
        self.assertIn('لم تقع مراجعة بشرية', release.NOTES)

    def test_narrow_git_publication_never_selects_workspace_root(self):
        paths = release.git_paths()
        self.assertEqual(len(paths), len(set(paths)))
        self.assertTrue(all(p == 'README.md' or p.startswith('build/') for p in paths))
        self.assertNotIn('.', paths)


if __name__ == '__main__':
    unittest.main()
