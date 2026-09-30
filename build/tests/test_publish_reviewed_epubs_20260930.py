"""Bounded EPUB successor metadata and failure-closed creation checks."""
import unittest
from unittest.mock import Mock, patch
from build import publish_reviewed_epubs_20260930 as publisher


class ReviewedEPUBPublicationTests(unittest.TestCase):
    def test_description_is_html_with_direct_source_and_reading_links(self):
        value=publisher.description_html()
        self.assertNotIn('## ',value)
        self.assertNotIn('](',value)
        self.assertIn('<div lang="ar" dir="rtl">',value)
        for model in ('GPT-5.6 Sol','GPT-6 Sol','GPT-6.1 Sol'):
            self.assertIn(model,value)
        self.assertIn('Ultra',value)
        for profile in ('international','machrek','classical'):
            self.assertIn(f'-{profile}.epub',value)
        self.assertEqual(value.count('_SOURCES.zip'),3)
        self.assertEqual(value.count('.tex'),3)
        self.assertIn('ما زالت جارية',value)

    def test_github_network_failure_is_not_treated_as_missing_release(self):
        with (patch.object(publisher,'all_assets',return_value=[]),
              patch.object(publisher.requests,'get',return_value=Mock(status_code=503)),
              patch.object(publisher.subprocess,'run') as create):
            with self.assertRaises(ValueError):
                publisher.github()
            create.assert_not_called()

    def test_existing_release_is_not_recreated(self):
        with (patch.object(publisher,'all_assets',return_value=[]),
              patch.object(publisher.requests,'get',return_value=Mock(status_code=200)),
              patch.object(publisher.subprocess,'run') as create):
            with self.assertRaises(ValueError):
                publisher.github()
            create.assert_not_called()


if __name__=='__main__':
    unittest.main()
