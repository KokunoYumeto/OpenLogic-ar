import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'render_readable_review_20260930.py'
SPEC = importlib.util.spec_from_file_location('readable', SCRIPT)
M = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)


class ReadingTests(unittest.TestCase):
    def test_fenced_example_is_not_split(self):
        text = 'intro\n\n```tex\nA\n\nB\n```\n\nafter\n'
        self.assertEqual(M.blocks(text), ['intro\n\n', '```tex\nA\n\nB\n```\n\n', 'after\n'])

    def test_relocation_preserves_public_urls_and_fragments(self):
        original = M.BASE / 'arabic-test/CARDS.md'
        new = M.PAGES / 'test.md'
        value = '[local](../INDEX_AR.md#heading) [public](https://example.org/x#x)'
        self.assertEqual(M.relocate(value, original, new),
                         '[local](../INDEX_AR.md#heading) [public](https://example.org/x#x)')

    def test_chunking_preserves_every_character(self):
        text = ('نص عربي\n\n' * 30_000)
        values = M.chunks(text)
        self.assertGreater(len(values), 1)
        self.assertEqual(''.join(values), text)
        self.assertTrue(all(len(v.encode()) <= M.PAYLOAD_LIMIT for v in values))


if __name__ == '__main__':
    unittest.main()
