import unittest
from build.review_sol6_epub_20260930 import correct, DISCLOSURE_AR


class DisclosureTests(unittest.TestCase):
    def members(self):
        return {
            "OEBPS/package.opf": b'<package xmlns="http://www.idpf.org/2007/opf"><metadata><meta property="dcterms:provenance">GPT-5.6 Sol, Ultra</meta><meta property="dcterms:modified">2026-09-25T00:00:00Z</meta></metadata></package>',
            "OEBPS/provenance.xhtml": b'<html><p>GPT-5.6 Sol, Ultra</p></html>',
            "OEBPS/body.xhtml": '<html><p>اختيار</p></html>'.encode(),
        }

    def test_only_disclosure_members_change(self):
        old = self.members()
        new = correct(old)
        self.assertEqual(old['OEBPS/body.xhtml'], new['OEBPS/body.xhtml'])
        self.assertIn(DISCLOSURE_AR.encode(), new['OEBPS/provenance.xhtml'])
        self.assertNotEqual(old['OEBPS/package.opf'], new['OEBPS/package.opf'])
        self.assertEqual(old['OEBPS/provenance.xhtml'], self.members()['OEBPS/provenance.xhtml'])

    def test_rejects_missing_or_ambiguous_disclosure(self):
        for replacement in (b'<html/>', b'<html><p>GPT-5.6 Sol, Ultra</p><p>GPT-5.6 Sol, Ultra</p></html>'):
            old = self.members()
            old['OEBPS/provenance.xhtml'] = replacement
            with self.assertRaises(ValueError):
                correct(old)

    def test_rejects_repeated_opf_provenance(self):
        old = self.members()
        old['OEBPS/package.opf'] = old['OEBPS/package.opf'].replace(b'</metadata>', b'<meta property="dcterms:provenance">duplicate</meta></metadata>')
        with self.assertRaises(ValueError):
            correct(old)


if __name__ == '__main__':
    unittest.main()
