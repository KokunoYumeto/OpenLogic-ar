import unittest

from build.audit_classical_rtl_visible_semantics_20260907 import FENCES, fence_ok, tableau_ok


class VisibleSemanticsTests(unittest.TestCase):
    def test_all_fences_require_both_position_and_face_change(self):
        for pair in FENCES.values():
            for role, index in (("open", 0), ("close", 1)):
                self.assertTrue(fence_ok(pair[index], pair, role, False))
                self.assertTrue(fence_ok(pair[1-index], pair, role, True))
                self.assertFalse(fence_ok(pair[index], pair, role, True))
                self.assertFalse(fence_ok(pair[1-index], pair, role, False))

    def test_rtl_rejects_mirrored_relation_with_unreversed_operands(self):
        wrong = [{"text": c, "x": x} for x, c in enumerate("A←B")]
        right = [{"text": c, "x": x} for x, c in enumerate("B←A")]
        self.assertFalse(tableau_ok(wrong, "←", True))
        self.assertTrue(tableau_ok(right, "←", True))

    def test_ltr_and_relation_face_are_checked_separately(self):
        ltr = [{"text": c, "x": x} for x, c in enumerate("A→B")]
        self.assertTrue(tableau_ok(ltr, "→", False))
        self.assertFalse(tableau_ok(ltr, "←", False))
        self.assertFalse(tableau_ok(ltr, "→", True))

    def test_extra_missing_duplicated_or_coincident_glyphs_fail(self):
        for text in ("A←", "A←BA", "A⇐B", "A←BB"):
            self.assertFalse(tableau_ok([{"text": c, "x": x} for x, c in enumerate(text)], "←", True))
        self.assertFalse(tableau_ok([{"text": c, "x": 1} for c in "B←A"], "←", True))


if __name__ == "__main__":
    unittest.main()
