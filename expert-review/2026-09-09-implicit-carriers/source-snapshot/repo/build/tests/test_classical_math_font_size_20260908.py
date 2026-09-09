"""The native font filename must end before its requested point-size keyword.

Under ExplSyntaxOn ordinary source spaces disappear, while ~ supplies a space
token. Installed fontspec-luatex.sty uses `#2 ~at~ <dimension>` in both primitive
font setters (lines 478 and 482). This static guard does not replace the runtime
check that base, script and scriptscript glyph sizes actually differ.
"""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
RUNTIME_FILES = (
    "source/locale/ar-classical/open-logic-numerals-ar-classical.tex",
    "source/locale/ar-classical/open-logic-letters-ar-classical.tex",
)


def explicit_font_size_tail(source_line):
    """Inspect the bounded quoted native-font assignment syntax used here."""
    match = re.search(r'=\s*"[^"\r\n]+"([^\r\n]*)', source_line)
    if match is None:
        raise ValueError("no quoted native-font assignment")
    # These two assignments contain no escaped spaces or percent characters.
    tail = re.sub(r"\s+", "", match.group(1).split("%", 1)[0]).replace("~", " ")
    return re.fullmatch(r" +at +#1pt\\scan_stop:", tail) is not None


class TypedMathFontSize(unittest.TestCase):
    def test_each_native_font_load_separates_filename_from_size(self):
        for relative in RUNTIME_FILES:
            with self.subTest(path=relative):
                source = (ROOT / relative).read_text(encoding="utf-8")
                assignments = [line for line in source.splitlines()
                               if re.search(r'=\s*".*:mode=base"', line)]
                self.assertEqual(len(assignments), 1)
                self.assertTrue(explicit_font_size_tail(assignments[0]),
                                "font filename can absorb at<size>pt when expl3 spaces disappear")

    def test_original_space_only_assignment_is_rejected(self):
        self.assertFalse(explicit_font_size_tail(
            r'= "[example.otf]:mode=base" at #1pt\scan_stop:'))
        self.assertTrue(explicit_font_size_tail(
            r'= "[example.otf]:mode=base"~at~#1pt\scan_stop:'))


if __name__ == "__main__":
    unittest.main()
