"""Static/model checks only: these tests do NOT execute or validate TeX."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
FORMATTER = ROOT / "source/locale/ar-classical/open-logic-numerals-ar-classical.tex"
SOURCE = FORMATTER.read_text(encoding="utf-8")
# The implementation has no escaped percent signs in executable code.
CODE = "\n".join(line.split("%", 1)[0] for line in SOURCE.splitlines())
DIGITS = dict(re.findall(r"\{([0-9])\}\{([\u0660-\u0669])\}", CODE))


def display_model(value):
    """Model only the digit table actually declared in the TeX source."""
    return "".join(DIGITS.get(char, char) for char in str(value))


def brace_argument_after(marker):
    """Extract one source argument for structural assertions, not TeX parsing."""
    start = CODE.index("{", CODE.index(marker) + len(marker))
    level = 0
    for i in range(start, len(CODE)):
        if CODE[i] == "{":
            level += 1
        elif CODE[i] == "}":
            level -= 1
            if level == 0:
                return CODE[start + 1:i]
    raise AssertionError("unbalanced source argument")


class DigitTableTests(unittest.TestCase):
    def test_exact_eastern_arabic_codepoints(self):
        self.assertEqual(DIGITS, {str(i): chr(0x660 + i) for i in range(10)})

    def test_zero_negative_multidigit_and_hierarchy(self):
        for before, after in [(0, "٠"), (-120, "-١٢٠"), (1234567890, "١٢٣٤٥٦٧٨٩٠"),
                              ("12.30.4", "١٢.٣٠.٤"), ("(27)", "(٢٧)")]:
            with self.subTest(before=before):
                self.assertEqual(display_model(before), after)

    def test_idempotent_for_nested_counter_wrappers(self):
        for value in ["1.23", "١.23", "١.٢٣", "A.12", "iv", "-09"]:
            self.assertEqual(display_model(display_model(value)), display_model(value))

    def test_non_digits_not_remapped(self):
        self.assertEqual(display_model("A.iv-۲۳.١٢"), "A.iv-۲۳.١٢")

    def test_representation_does_not_change_model_counter(self):
        counter = 19
        self.assertEqual(display_model(counter), "١٩")
        self.assertEqual(counter + 1, 20)


class StaticContractTests(unittest.TestCase):
    def test_expandable_public_formatter_and_numeric_read(self):
        self.assertIn(r"\NewExpandableDocumentCommand \OLClassicalDigits", CODE)
        self.assertIn(r"\NewExpandableDocumentCommand \OLClassicalCounter", CODE)
        self.assertIn(r"\int_use:c { c@#1 }", CODE)
        self.assertIn(r"\exp_args:Ne \str_map_function:nN", CODE)

    def test_no_numeric_state_writes(self):
        self.assertNotRegex(CODE, r"\\(?:setcounter|addtocounter|stepcounter|refstepcounter|advance|newcounter)\b")

    def test_no_global_digit_or_identifier_redefinition(self):
        # These identifiers need not occur at all in this narrow layer.
        self.assertNotRegex(CODE, r"\\(?:arabic|@arabic|theolpart|theolchapter|theolsection|olfileid|ollabel|olref|href|url|label)\b")
        self.assertNotRegex(CODE, r"\\theH[A-Za-z@]*")

    def test_explicit_idempotent_preamble_installation(self):
        self.assertIn(r"\bool_if:NF \g__olc_installed_bool", CODE)
        self.assertIn(r"\@onlypreamble \OLClassicalInstallNumerals", CODE)
        # No unconditional invocation is hidden after the installer's body.
        self.assertRegex(CODE, r"\\@onlypreamble\s+\\OLClassicalInstallNumerals\s+\\ExplSyntaxOff\s+\\makeatother\s+\\endinput\s*$")

    def test_grouped_installation_rejected(self):
        self.assertIn(r"\int_compare:nNnF { \tex_currentgrouplevel:D } = {0}", CODE)
        self.assertIn("A~grouped~installation", CODE)

    def test_required_counter_display_inventory(self):
        inventory = brace_argument_after(r"\clist_const:Nn \c__olc_wrapped_counters_clist")
        names = set(re.split(r"\s*,\s*", inventory.strip()))
        self.assertTrue({"chapter", "section", "subsection", "thm", "ex", "lem", "prop",
                         "cor", "defn", "prob", "probd", "equation"} <= names)
        self.assertIn("enumi,enumii,enumiii,enumiv,footnote,mpfootnote", CODE)

    def test_page_wrapper_preserves_star_and_explicit_gobble(self):
        self.assertIn(r"\NewCommandCopy \OLClassicalOriginalPageNumbering \pagenumbering", CODE)
        self.assertIn(r"\RenewDocumentCommand \pagenumbering { s m }", CODE)
        self.assertIn(r"\OLClassicalOriginalPageNumbering * {##2}", CODE)
        self.assertIn(r"\OLClassicalOriginalPageNumbering {##2}", CODE)
        self.assertIn(r"\str_if_eq:nnF {##2} {gobble}", CODE)
        self.assertIn(r"\settitlingpagenumbering { \OLClassicalCounter }", CODE)

    def test_matter_hooks_avoid_star_parsers(self):
        for command in ["@smemfront", "@smemmain", "appendix"]:
            self.assertIn("cmd/" + command + "/after", CODE)
        self.assertNotIn("cmd/frontmatter/after", CODE)
        self.assertNotIn("cmd/mainmatter/after", CODE)

    def test_hyperref_ascii_mode_not_theHpage_workaround(self):
        self.assertIn("hypertexnames=false", CODE)
        self.assertIn("unicode=true", CODE)
        self.assertIn("bookmarksnumbered=true", CODE)
        self.assertIn(r"\ifHy@hypertexnames", CODE)
        self.assertIn("shipout/before", CODE)
        self.assertNotIn(r"\Hy@EveryPageAnchor", CODE)

    def test_memoir_list_marker_adapter_and_enumitem_rejection(self):
        self.assertIn(r"\cs_set:Npn \@enLabel ##1##2", CODE)
        self.assertIn(r"\__olc_original_enlabel: \OLClassicalCounter ##2", CODE)
        self.assertIn(r"\@ifpackageloaded {enumitem}", CODE)
        self.assertIn("package/enumitem/before", CODE)
        self.assertIn(r"\bool_set_false:N \l__olc_supported_bool", CODE)

    def test_source_braces_balanced(self):
        level = 0
        for char in CODE:
            if char == "{":
                level += 1
            elif char == "}":
                level -= 1
                self.assertGreaterEqual(level, 0)
        self.assertEqual(level, 0)


if __name__ == "__main__":
    unittest.main()
