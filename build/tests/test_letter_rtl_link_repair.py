"""Focused regression tests for Letter Arabic inflated-link detection."""

import importlib.util
import json
import tempfile
from pathlib import Path
import sys
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "repair_rtl_link_rects_letter_ar.py"
SPEC = importlib.util.spec_from_file_location("letter_rtl_link_repair", SCRIPT)
repair = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = repair
SPEC.loader.exec_module(repair)


class Ref:
    def __init__(self, value):
        self.value = value

    def get_object(self):
        return self.value


class Page(dict):
    mediabox = [0.0, 0.0, 612.0, 792.0]


def link_annotation(
    rect,
    *,
    target="cite.Peter1935a",
    colour=None,
    target_file=None,
    uri=None,
):
    if uri is not None:
        action_value = {"/S": "/URI", "/URI": uri}
    else:
        action_value = {"/S": "/GoToR" if target_file else "/GoTo", "/D": target}
        if target_file:
            action_value["/F"] = target_file
    annotation = {"/Subtype": "/Link", "/Rect": rect, "/A": Ref(action_value)}
    if colour is not None:
        annotation["/C"] = colour
    return annotation


def reader_with(rect, *, page_number=1, **annotation_kwargs):
    annotation = link_annotation(rect, **annotation_kwargs)
    pages = [Page() for _ in range(page_number - 1)]
    pages.append(Page({"/Annots": [Ref(annotation)]}))
    return type("Reader", (), {"pages": pages})()


class InflatedLinkDetectionTests(unittest.TestCase):
    def test_exact_msa_count_admission_does_not_change_other_guards(self):
        reader = type("Reader", (), {"pages": [None] * 1019})()
        digest = "1BD82914E17B9BCCD07D15335C2CEDD20F653FA89CDC40F873BCF0C8DAE91044"
        with mock.patch.object(repair.CORE, "sha256_file", return_value=digest):
            authority = repair.input_count_authority(Path("reader.pdf"), reader, "reader")
            self.assertEqual(authority["expected_count"], 161)
            self.assertEqual(authority["kind"], "exact-audited-msa-input")
            with self.assertRaisesRegex(RuntimeError, "unexpected role or page count"):
                repair.input_count_authority(Path("reader.pdf"), reader, "supplement")
            with self.assertRaisesRegex(RuntimeError, "unexpected role or page count"):
                repair.input_count_authority(Path("reader.pdf"), reader_with([1, 1, 2, 2]), "reader")
        with mock.patch.object(repair.CORE, "sha256_file", return_value="F" * 64):
            self.assertEqual(repair.input_count_authority(Path("unknown.pdf"), reader, "reader")["expected_count"], 160)
        self.assertEqual(repair.EXPECTED_COUNTS, {"reader": 160, "supplement": 11})
        with mock.patch.object(repair.CORE, "sha256_file", return_value="4247C4DE922D6E96B5D3F14DBAEF6D3A35425FB731A558DA26BD068FCEA43672"):
            self.assertEqual(repair.input_count_authority(Path("reader.pdf"), reader, "reader")["expected_count"], 121)
        with mock.patch.object(repair.CORE, "sha256_file", return_value="D2D4865B539533858C9A3E9D4797A956A6850CC50476F2EB40069E5955A87B2A"):
            self.assertEqual(repair.input_count_authority(Path("reader.pdf"), reader, "reader")["expected_count"], 121)

    def test_existing_repair_cannot_be_reused_with_changed_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory);raw=base/'raw.pdf';out=base/'out.pdf';receipt=base/'receipt.json'
            raw.write_bytes(b'raw');out.write_bytes(b'out')
            receipt.write_text(json.dumps({'schema':'arabic-letter-rtl-link-rect-repair-v1',
                'dry_run':False,'document_role':'reader','input_sha256':repair.CORE.sha256_file(raw),
                'output_sha256':repair.CORE.sha256_file(out),'output_bytes':3,
                'malformed_link_rectangles':121}),encoding='utf-8')
            with self.assertRaisesRegex(RuntimeError,'lacks preservation evidence'):
                repair.verify_existing_repair(raw,out,receipt,'reader',{'expected_count':121})
            out.write_bytes(b'altered')
            with self.assertRaisesRegex(RuntimeError,'identity differs'):
                repair.verify_existing_repair(raw,out,receipt,'reader',{'expected_count':121})

    def test_zero_repair_supplement_admission_is_exact(self):
        reader = type("Reader", (), {"pages": [None] * 145})()
        digest = "9BBAC5FC7EF3DEF2A7A0FD64D070675A12E8F799763AC1829CAB0EB727382CEB"
        with mock.patch.object(repair.CORE, "sha256_file", return_value=digest):
            self.assertEqual(repair.input_count_authority(Path("supplement.pdf"),reader,"supplement")["expected_count"],0)
            with self.assertRaisesRegex(RuntimeError,"unexpected role or page count"):
                repair.input_count_authority(Path("supplement.pdf"),reader,"reader")
        with mock.patch.object(repair.CORE,"sha256_file",return_value="F"*64):
            self.assertEqual(repair.input_count_authority(Path("unknown.pdf"),reader,"supplement")["expected_count"],11)

    def test_machrek_admission_retains_its_distinct_page_count(self):
        digest="728D4CC5EC51ECB24FFE90F76A580F628B79B23CD88DADD234DDE335F47D5312"
        reader=type("Reader",(),{"pages":[None]*1020})()
        with mock.patch.object(repair.CORE,"sha256_file",return_value=digest):
            authority=repair.input_count_authority(Path("machrek.pdf"),reader,"reader")
            self.assertEqual((authority['pages'],authority['expected_count']),(1020,121))
            reader.pages.pop()
            with self.assertRaisesRegex(RuntimeError,"unexpected role or page count"):
                repair.input_count_authority(Path("machrek.pdf"),reader,"reader")

    def test_known_inflation_is_detected_even_when_inside_page(self):
        # This exact failure mode appeared after the final reader reflow: the
        # bad rectangle stayed inside the media box but retained +468.245 pt.
        reader = reader_with([76.514, 446.126, 544.759, 464.868])
        bad, signatures = repair.scan_bad_annotations(reader, expected_count=1)
        self.assertEqual(len(bad), 1)
        self.assertEqual(signatures[468.245], 1)

    def test_ordinary_inside_link_is_not_selected(self):
        reader = reader_with([76.514, 446.126, 138.754, 464.868])
        bad, signatures = repair.scan_bad_annotations(reader, expected_count=0)
        self.assertEqual(bad, [])
        self.assertFalse(signatures)

    def test_unknown_outside_width_still_fails_closed(self):
        reader = reader_with([100.0, 100.0, 700.0, 120.0])
        with self.assertRaisesRegex(RuntimeError, "unknown width signature"):
            repair.scan_bad_annotations(reader, expected_count=None)

    def test_exact_full_line_uri_width_collision_is_not_selected(self):
        uri = (
            "http://www.nasonline.org/publications/biographical-memoirs/"
            "memoir-pdfs/robinson-julia.pdf"
        )
        reader = reader_with(
            [72.376, 86.239, 526.274, 101.473],
            page_number=1032,
            colour=[0.0, 1.0, 1.0],
            uri=uri,
        )
        bad, signatures = repair.scan_bad_annotations(
            reader, expected_count=0, role="reader"
        )
        self.assertEqual(bad, [])
        self.assertFalse(signatures)

    def test_full_line_uri_collision_inventory_is_exact(self):
        collisions = repair.AUDITED_VALID_WIDTH_COLLISIONS
        self.assertEqual(len(collisions), 6)
        self.assertEqual(
            {(item["page"], tuple(item["rect"])) for item in collisions},
            {
                (1032, (72.376, 86.239, 526.274, 101.473)),
                (1037, (72.376, 326.903, 526.274, 342.137)),
                (1038, (72.376, 405.066, 526.274, 420.300)),
                (991, (72.376, 86.239, 526.274, 101.473)),
                (996, (72.376, 326.903, 526.274, 342.137)),
                (997, (72.376, 405.066, 526.274, 420.300)),
            },
        )
        self.assertEqual(repair.EXPECTED_COUNTS["reader"], 160)

    def test_full_line_uri_collision_rejects_near_misses(self):
        uri = (
            "http://www.nasonline.org/publications/biographical-memoirs/"
            "memoir-pdfs/robinson-julia.pdf"
        )
        exact = link_annotation(
            [72.376, 86.239, 526.274, 101.473],
            colour=[0.0, 1.0, 1.0],
            uri=uri,
        )
        self.assertIsNotNone(
            repair.match_audited_valid_width_collision("reader", exact, 1032)
        )
        self.assertIsNotNone(
            repair.match_audited_valid_width_collision("reader", exact, 991)
        )
        self.assertIsNone(
            repair.match_audited_valid_width_collision("reader", exact, 1031)
        )
        self.assertIsNone(
            repair.match_audited_valid_width_collision("reader", exact, 990)
        )

        wrong_uri = link_annotation(
            [72.376, 86.239, 526.274, 101.473],
            colour=[0.0, 1.0, 1.0],
            uri=uri + "?changed=1",
        )
        self.assertIsNone(
            repair.match_audited_valid_width_collision("reader", wrong_uri, 1032)
        )

        wrong_colour = link_annotation(
            [72.376, 86.239, 526.274, 101.473],
            colour=[0.0, 1.0, 0.9],
            uri=uri,
        )
        self.assertIsNone(
            repair.match_audited_valid_width_collision(
                "reader", wrong_colour, 1032
            )
        )

        shifted = link_annotation(
            [72.396, 86.239, 526.294, 101.473],
            colour=[0.0, 1.0, 1.0],
            uri=uri,
        )
        self.assertIsNone(
            repair.match_audited_valid_width_collision("reader", shifted, 1032)
        )

        unmatched_reader = reader_with(
            [72.376, 86.239, 526.274, 101.473],
            colour=[0.0, 1.0, 1.0],
            uri=uri,
        )
        with self.assertRaisesRegex(
            RuntimeError, "malformed rectangle is not a GoTo/GoToR link"
        ):
            repair.scan_bad_annotations(
                unmatched_reader, expected_count=None, role="reader"
            )

    def test_outside_uri_width_collision_still_fails_closed(self):
        reader = reader_with(
            [200.0, 100.0, 653.898, 120.0],
            colour=[0.0, 1.0, 1.0],
            uri="https://example.invalid/",
        )
        with self.assertRaisesRegex(
            RuntimeError, "malformed rectangle is not a GoTo/GoToR link"
        ):
            repair.scan_bad_annotations(
                reader, expected_count=None, role="reader"
            )

    def test_current_classical_supplement_fallback_inventory_is_exact(self):
        current = [
            span for span in repair.AUDITED_SPANS
            if span["role"] == "supplement"
            and span.get("method")
            == "current-classical-source-reconciled-bidi-glyph-span"
        ]
        self.assertEqual({span["role"] for span in current}, {"supplement"})
        self.assertEqual(len(current), 11)
        self.assertEqual(
            {(span["page"], span["target"], span["text_ascii"]) for span in current},
            {
                (9, "prop*.2291", r"\u0661\u0669.\u0661\u0668"),
                (9, "prop*.2300", r"\u0661\u0669.\u0662\u0661"),
                (9, "Item*.2305", r"Items\u0661"),
                (9, "Item*.2306", r"Items\u0662"),
                (9, "prop*.2311", r"and\u0662\u0660.\u0662\u0663"),
                (10, "prop*.2311", r"\u0661\u0669.\u0662\u0663"),
                (10, "Item*.2319", r"Items\u0661"),
                (10, "Item*.2320", r"Items\u0662"),
                (10, "Item*.2320", r"and\u0662"),
                (23, "lem*.519", r"\u0666.\u0661\u0664"),
                (123, "table.502", r"\u0666.\u0663"),
            },
        )

    def test_classical_supplement_fallback_key_rejects_near_misses(self):
        target_file = (
            "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_"
            "EASTERN_ARABIC_RTL_OLP-0722.pdf"
        )
        exact = link_annotation(
            [169.848, 561.742, 602.226, 578.080],
            target="prop*.2291",
            colour=[0.0, 0.5, 0.5],
            target_file=target_file,
        )
        self.assertIsNotNone(repair.match_audited_span("supplement", exact, 9))
        self.assertIsNone(repair.match_audited_span("supplement", exact, 8))

        wrong_file = link_annotation(
            [169.848, 561.742, 602.226, 578.080],
            target="prop*.2291",
            colour=[0.0, 0.5, 0.5],
            target_file="wrong.pdf",
        )
        self.assertIsNone(repair.match_audited_span("supplement", wrong_file, 9))

        wrong_colour = link_annotation(
            [169.848, 561.742, 602.226, 578.080],
            target="prop*.2291",
            colour=[0.0, 0.5, 0.6],
            target_file=target_file,
        )
        self.assertIsNone(repair.match_audited_span("supplement", wrong_colour, 9))

        shifted = link_annotation(
            [169.868, 561.742, 602.226, 578.080],
            target="prop*.2291",
            colour=[0.0, 0.5, 0.5],
            target_file=target_file,
        )
        self.assertIsNone(repair.match_audited_span("supplement", shifted, 9))

    def test_compact_classical_closure_fallback_inventory_is_exact(self):
        compact = [
            span for span in repair.AUDITED_SPANS
            if span["role"] == "supplement"
            and span.get("method")
            == "compact-classical-closure-exact-bidi-glyph-span"
        ]
        self.assertEqual(len(compact), 11)
        self.assertEqual(
            [(span["page"], span["target"], span["old_rect"])
             for span in compact],
            [
                (8, "prop*.2291", [219.863, 569.851, 652.242, 586.190]),
                (8, "prop*.2300", [452.037, 461.676, 884.415, 478.300]),
                (8, "Item*.2305", [135.894, 389.653, 568.273, 407.480]),
                (8, "Item*.2306", [77.226, 348.725, 509.604, 365.123]),
                (8, "prop*.2311", [176.178, 259.446, 608.556, 275.785]),
                (8, "prop*.2311", [77.226, 217.287, 509.604, 233.638]),
                (8, "Item*.2319", [300.541, 127.781, 732.920, 144.178]),
                (8, "Item*.2320", [436.172, 67.110, 868.550, 83.970]),
                (9, "Item*.2320", [221.332, 698.330, 653.711, 717.073]),
                (21, "lem*.519", [260.817, 371.946, 729.061, 391.898]),
                (113, "table.502", [436.208, 401.094, 904.452, 421.047]),
            ],
        )

    def test_compact_classical_closure_fallback_rejects_near_misses(self):
        target_file = (
            "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_"
            "EASTERN_ARABIC_RTL_OLP-0722.pdf"
        )
        rect = [219.863, 569.851, 652.242, 586.190]
        exact = link_annotation(
            rect, target="prop*.2291", colour=[0.0, 0.5, 0.5],
            target_file=target_file,
        )
        self.assertIsNotNone(repair.match_audited_span("supplement", exact, 8))
        self.assertIsNone(repair.match_audited_span("supplement", exact, 9))
        for changed in (
            link_annotation(rect, target="prop*.2290", colour=[0.0, 0.5, 0.5],
                            target_file=target_file),
            link_annotation(rect, target="prop*.2291", colour=[0.0, 0.5, 0.5],
                            target_file="wrong.pdf"),
            link_annotation(rect, target="prop*.2291", colour=[0.0, 0.5, 0.6],
                            target_file=target_file),
            link_annotation([219.883, *rect[1:]], target="prop*.2291",
                            colour=[0.0, 0.5, 0.5], target_file=target_file),
        ):
            self.assertIsNone(repair.match_audited_span("supplement", changed, 8))

    def test_rgb_cmyk_mismatch_is_not_generically_broadened(self):
        annotation = link_annotation(
            [169.848, 561.742, 602.226, 578.080],
            target="prop*.2291",
            colour=[0.0, 0.5, 0.5],
            target_file=(
                "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_"
                "EASTERN_ARABIC_RTL_OLP-0722.pdf"
            ),
        )
        chars = [{
            "x0": 170.846712064,
            "x1": 199.934997472,
            "top": 212.70658896,
            "bottom": 228.20050896,
            "text": "١٩.١٨",
            "non_stroking_color": (1.0, 0.0, 0.0, 0.0),
        }]
        with self.assertRaisesRegex(RuntimeError, "no glyphs match colour"):
            repair.CORE.infer_mapping(
                9, 1, annotation, [annotation], chars, 612.0, 792.0
            )

    def test_exact_button_sliver_is_selected_and_repaired(self):
        reader = reader_with(
            [96.423, 84.633, 98.416, 100.738],
            page_number=931,
            target="cite.ButtonLT1",
            colour=[0.0, 1.0, 0.0],
        )
        bad, signatures = repair.scan_bad_annotations(
            reader, expected_count=1, role="reader"
        )
        self.assertEqual(bad[0]["kind"], "audited-undersized")
        self.assertFalse(signatures)

        annotation = bad[0]["annot"]
        span = repair.match_audited_span("reader", annotation, 931)
        chars = [{
            "x0": 73.372,
            "x1": 97.421050984,
            "top": 691.86161666,
            "bottom": 703.64343666,
            "text": "Button",
            "non_stroking_color": (0.0, 1.0, 0.0),
        }]
        mapping = repair.audited_mapping(931, 12, annotation, chars, span)
        self.assertEqual(
            mapping["new_rect"], [72.376, 84.633, 98.416, 100.738]
        )
        self.assertEqual(mapping["malformation_kind"], "audited-undersized")

        compact_span = repair.match_audited_span("reader", annotation, 890)
        self.assertIsNotNone(compact_span)
        compact_mapping = repair.audited_mapping(
            890, 12, annotation, chars, compact_span
        )
        self.assertEqual(compact_mapping["new_rect"], mapping["new_rect"])
        self.assertIsNone(repair.match_audited_span("reader", annotation, 889))

        changed_chars = [dict(chars[0], text="ButtoX")]
        with self.assertRaisesRegex(RuntimeError, "audited glyph text changed"):
            repair.audited_mapping(931, 12, annotation, changed_chars, span)

    def test_compact_reader_mixed_colour_citation_spans_are_exact(self):
        for page, target, rect, digits in (
            (195, "prop*.1367", [452.929, 620.353, 885.308, 638.406], "١٢.٢٨"),
            (357, "prop*.2765", [452.929, 170.758, 885.308, 188.812], "٢٢.٣٣"),
        ):
            with self.subTest(page=page):
                annotation = link_annotation(
                    rect, target=target, colour=[1.0, 0.0, 0.0]
                )
                span = repair.match_audited_span("reader", annotation, page)
                self.assertIsNotNone(span)
                self.assertIsNone(
                    repair.match_audited_span("reader", annotation, page - 1)
                )
                top = 157.0 if page == 195 else 607.0
                coordinates = [
                    (453.925, 459.115463, "a"),
                    (459.115463, 464.956671, "n"),
                    (464.956671, 470.797879, "d"),
                    (474.67, 480.729672, digits[0]),
                    (480.729672, 486.789344, digits[1]),
                    (486.789344, 491.638941, digits[2]),
                    (491.638941, 497.698613, digits[3]),
                    (497.698613, 503.758285, digits[4]),
                ]
                chars = [
                    {"x0": left, "x1": right, "top": top,
                     "bottom": top + 12.0, "text": letter}
                    for left, right, letter in coordinates
                ]
                mapped = repair.audited_mapping(
                    page, 8 if page == 195 else 31, annotation, chars, span
                )
                self.assertEqual(mapped["new_rect"],
                                 [452.929, rect[1], 504.758285, rect[3]])
                with self.assertRaisesRegex(RuntimeError,
                                            "audited glyph text changed"):
                    altered = [dict(item) for item in chars]
                    altered[-1]["text"] = "٩"
                    repair.audited_mapping(page, 8, annotation, altered, span)

    def test_button_sliver_key_rejects_near_misses(self):
        exact = link_annotation(
            [96.423, 84.633, 98.416, 100.738],
            target="cite.ButtonLT1",
            colour=[0.0, 1.0, 0.0],
        )
        self.assertIsNotNone(repair.match_audited_span("reader", exact, 931))
        self.assertIsNone(repair.match_audited_span("reader", exact, 930))

        wrong_target = link_annotation(
            [96.423, 84.633, 98.416, 100.738],
            target="cite.ButtonLT2",
            colour=[0.0, 1.0, 0.0],
        )
        self.assertIsNone(repair.match_audited_span("reader", wrong_target, 931))

        shifted = link_annotation(
            [96.443, 84.633, 98.416, 100.738],
            target="cite.ButtonLT1",
            colour=[0.0, 1.0, 0.0],
        )
        self.assertIsNone(repair.match_audited_span("reader", shifted, 931))

    def test_adjacent_line_same_target_is_not_a_companion(self):
        action = Ref({"/S": "/GoTo", "/D": "cite.ButtonLT1"})
        adjacent = {
            "/Subtype": "/Link",
            "/Rect": [96.423, 84.633, 98.416, 100.738],
            "/A": action,
            "/C": [0.0, 1.0, 0.0],
        }
        inflated = {
            "/Subtype": "/Link",
            "/Rect": [517.716, 71.667, 985.960, 85.813],
            "/A": action,
            "/C": [0.0, 1.0, 0.0],
        }
        chars = [{
            "x0": 518.712,
            "x1": 539.626,
            "top": 707.0,
            "bottom": 719.0,
            "text": "2021",
            "non_stroking_color": (0.0, 1.0, 0.0),
        }]
        mapping = repair.CORE.infer_mapping(
            931, 13, inflated, [adjacent, inflated], chars, 612.0, 792.0)
        self.assertEqual(mapping["method"], "sole-colour-run")
        self.assertEqual(mapping["companion_rects"], [])
        self.assertEqual(mapping["new_rect"], [517.716, 71.667, 540.626, 85.813])

    def test_current_classical_button_citation_span_is_exact(self):
        spans = [
            span for span in repair.AUDITED_SPANS
            if span["role"] == "reader"
            and span["target"] == "cite.ButtonLT1"
            and span["old_rect"] == [517.716, 71.667, 985.960, 85.813]
        ]
        self.assertEqual(len(spans), 1)
        self.assertEqual(spans[0]["glyph_x0"], 518.712)
        self.assertEqual(spans[0]["glyph_x1"], 539.625985)
        self.assertEqual(spans[0]["text_ascii"], ")2021")
        self.assertEqual(
            spans[0]["method"],
            "current-classical-source-reconciled-bidi-glyph-span",
        )


if __name__ == "__main__":
    unittest.main()
