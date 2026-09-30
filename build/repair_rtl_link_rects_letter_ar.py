#!/usr/bin/env python3
"""Fail-closed RTL link-rectangle repair for the Arabic US-Letter readers.

LuaTeX/hyperref occasionally adds the active line width to the right edge of
an RTL link annotation.  The page contents and link target remain correct,
but the clickable rectangle becomes one of a small set of audited inflated
widths.  It often extends beyond the page, but can remain inside the page after
reflow and is still malformed there.  This tool changes only those malformed
``/Rect`` arrays.  It reuses the audited glyph-run inference
and semantic-preservation checks from the repository's released 16:9 repair.

Some cross-document references and bibliography fragments have disjoint BiDi
colour runs that cannot be inferred from colour alone.  Historical fallback
spans are independently witnessed by the prior public R2 PDFs (reader
SHA-256 FB1EAB6294FC62E0C7B2C1B793EA8CDB5F8EBE8A85683DA6DD5BFEE599CFB4E6;
supplement SHA-256 40ED33C1043EDD17603BDCC2E996A3E6CA51BBCE9D433399699F155D8BC4455A).
Current Classical fallbacks additionally require their exact source-reconciled
page, target, rectangle, colour, glyph text and glyph bounds.  Changed input
therefore fails closed rather than invoking a broad colour-space equivalence.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import pdfplumber
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, FloatObject, NameObject


PAGE_WIDTH = 612.0
PAGE_HEIGHT = 792.0
# Counts cover every malformed GoTo/GoToR rectangle, including in-page
# instances.  The current reader has 159 inflated destination links plus one
# exact audited undersized citation-author rectangle.  Three valid full-line
# bibliography URI rectangles happen to share the 453.898 pt width signature;
# they are excluded only by the exact audited collision inventory below.
EXPECTED_COUNTS = {"reader": 160, "supplement": 11}
# The two independently hashed MSA inputs have 161 inflated rectangles and
# no Classical Button sliver. Keep the existing historical/Classical guards;
# this is an artifact-specific admission, never a user-supplied count override.
AUDITED_MSA_READER_INPUTS = {
    "4B9EB245CEBC71042B30824F3EB8B416DF8FEB899F1686C9C83188B0CFF8494C":
        "msa-international-20260922",
    "1BD82914E17B9BCCD07D15335C2CEDD20F653FA89CDC40F873BCF0C8DAE91044":
        "msa-international-quantifier-20260930",
    "4247C4DE922D6E96B5D3F14DBAEF6D3A35425FB731A558DA26BD068FCEA43672":
        "msa-international-quantifier-reference-localized-20260930",
    "D2D4865B539533858C9A3E9D4797A956A6850CC50476F2EB40069E5955A87B2A":
        "msa-international-quantifier-reference-items-20260930",
    "728D4CC5EC51ECB24FFE90F76A580F628B79B23CD88DADD234DDE335F47D5312":
        "msa-machrek-quantifier-reference-items-20260930",
}
AUDITED_MSA_READER_COUNTS = {
    "4247C4DE922D6E96B5D3F14DBAEF6D3A35425FB731A558DA26BD068FCEA43672": 121,
    "D2D4865B539533858C9A3E9D4797A956A6850CC50476F2EB40069E5955A87B2A": 121,
    "728D4CC5EC51ECB24FFE90F76A580F628B79B23CD88DADD234DDE335F47D5312": 121,
}
AUDITED_MSA_READER_PAGES = {
    "728D4CC5EC51ECB24FFE90F76A580F628B79B23CD88DADD234DDE335F47D5312": 1020,
}
AUDITED_MSA_SUPPLEMENT_INPUTS = {
    "5DA0247A7676BBF426459455BC373BB669CED47C6F6CADED4AEA3166749A01B1": {
        "layout": "msa-machrek-quantifier-reference-items-20260930",
        "pages": 146, "expected_count": 0,
    },
    "9BBAC5FC7EF3DEF2A7A0FD64D070675A12E8F799763AC1829CAB0EB727382CEB": {
        "layout": "msa-international-quantifier-reference-items-20260930",
        "pages": 145, "expected_count": 0,
    },
}
EXPECTED_INFLATIONS = (
    396.513,
    432.378,
    432.379,
    453.898,
    468.244,
    468.245,
    473.093,
    473.094,
)


# These are valid, full-line URL annotations rather than inflated destination
# links.  Build C reflowed each URL from three physical lines to two, making
# its first line exactly the 453.898 pt bibliography measure. The compact
# Classical formula-registry build shortens the reader by exactly 41 pages
# before this bibliography; the three URLs retain their exact action, URI,
# rectangle and colour on pages 991/996/997. Keep both exact page identities
# so a different non-GoTo action with the same width still fails closed.
AUDITED_VALID_WIDTH_COLLISIONS: tuple[dict[str, Any], ...] = (
    {
        "role": "reader",
        "page": 1032,
        "uri": "http://www.nasonline.org/publications/biographical-memoirs/memoir-pdfs/robinson-julia.pdf",
        "rect": [72.376, 86.239, 526.274, 101.473],
        "annotation_colour": [0.0, 1.0, 1.0],
    },
    {
        "role": "reader",
        "page": 1037,
        "uri": "https://books.google.ca/books?id=6V3wNs4uv_4C&lpg=PP1&ots=BkQZaHcR99&lr&pg=PP1#v=onepage&q&f=false",
        "rect": [72.376, 326.903, 526.274, 342.137],
        "annotation_colour": [0.0, 1.0, 1.0],
    },
    {
        "role": "reader",
        "page": 1038,
        "uri": "https://web.archive.org/web/20151010184939/http://www4.ncsu.edu/~njrose/pdfFiles/HilbertCurve.pdf",
        "rect": [72.376, 405.066, 526.274, 420.300],
        "annotation_colour": [0.0, 1.0, 1.0],
    },
    {
        "role": "reader",
        "page": 991,
        "uri": "http://www.nasonline.org/publications/biographical-memoirs/memoir-pdfs/robinson-julia.pdf",
        "rect": [72.376, 86.239, 526.274, 101.473],
        "annotation_colour": [0.0, 1.0, 1.0],
    },
    {
        "role": "reader",
        "page": 996,
        "uri": "https://books.google.ca/books?id=6V3wNs4uv_4C&lpg=PP1&ots=BkQZaHcR99&lr&pg=PP1#v=onepage&q&f=false",
        "rect": [72.376, 326.903, 526.274, 342.137],
        "annotation_colour": [0.0, 1.0, 1.0],
    },
    {
        "role": "reader",
        "page": 997,
        "uri": "https://web.archive.org/web/20151010184939/http://www4.ncsu.edu/~njrose/pdfFiles/HilbertCurve.pdf",
        "rect": [72.376, 405.066, 526.274, 420.300],
        "annotation_colour": [0.0, 1.0, 1.0],
    },
)


def load_core() -> Any:
    path = Path(__file__).with_name("repair_rtl_link_rects_ar.py")
    spec = importlib.util.spec_from_file_location("openlogic_rtl_link_core", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load shared repair implementation: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load_core()


# Coordinates are for the raw dual-profile Letter build.  The international
# and Machrek PDFs have the same affected text geometry; only their page index
# may diverge after profile-specific formula reflow.
AUDITED_SPANS: tuple[dict[str, Any], ...] = (
    {
        "role": "reader",
        "target": "cite.ButtonLT1",
        "old_rect": [517.716, 73.297, 985.960, 87.443],
        "glyph_x0": 518.712,
        "glyph_x1": 539.625985,
        "text_ascii": ")2021",
    },
    {
        # The final Classical source-reconciled reader places the same exact
        # BiDi citation span 1.630 pt lower.  Its adjacent-line annotation for
        # the same destination overlaps vertically by 1.180 pt but is not a
        # split same-baseline companion.
        "role": "reader",
        "target": "cite.ButtonLT1",
        "old_rect": [517.716, 71.667, 985.960, 85.813],
        "glyph_x0": 518.712,
        "glyph_x1": 539.625985,
        "text_ascii": ")2021",
        "method": "current-classical-source-reconciled-bidi-glyph-span",
    },
    {
        # The author half of the same \citet citation collapsed to a 1.993 pt
        # end-of-run sliver.  It contains no glyph centre, whereas all three
        # other author links on this baseline, and three other Button author
        # links in this reader, begin 0.996--0.997 pt before their exact green
        # glyph runs.  Keep the already-correct right edge and restore that
        # witnessed 0.996 pt left padding.
        "role": "reader",
        "page": 931,
        "target": "cite.ButtonLT1",
        "old_rect": [96.423, 84.633, 98.416, 100.738],
        "annotation_colour": [0.0, 1.0, 0.0],
        "glyph_x0": 73.372,
        "glyph_x1": 97.421050984,
        "text_ascii": "Button",
        "new_x0": 72.376,
        "new_x1": 98.416,
        "force_scan": True,
        "malformation_kind": "audited-undersized",
        "method": "current-classical-source-reconciled-bidi-glyph-span",
    },
    {
        # Compact formula labels reflow this unchanged Button citation from
        # reader page 931 to page 890. Its 1.993 pt sliver and the witnessed
        # green glyph bounds are otherwise byte-for-byte the same.
        "role": "reader",
        "page": 890,
        "target": "cite.ButtonLT1",
        "old_rect": [96.423, 84.633, 98.416, 100.738],
        "annotation_colour": [0.0, 1.0, 0.0],
        "glyph_x0": 73.372,
        "glyph_x1": 97.421050984,
        "text_ascii": "Button",
        "new_x0": 72.376,
        "new_x1": 98.416,
        "force_scan": True,
        "malformation_kind": "audited-undersized",
        "method": "current-classical-source-reconciled-bidi-glyph-span",
    },
    {
        # In the compact reader the black conjunction and red proposition
        # number share one link, while another red number is present on the
        # same baseline. The generic colour-run selector correctly declines
        # to guess. Exact mixed-colour glyphs witness this bounded fallback.
        "role": "reader",
        "page": 195,
        "target": "prop*.1367",
        "old_rect": [452.929, 620.353, 885.308, 638.406],
        "annotation_colour": [1.0, 0.0, 0.0],
        "glyph_x0": 453.925,
        "glyph_x1": 503.758285,
        "text_ascii": "and\\u0661\\u0662.\\u0662\\u0668",
        "method": "compact-classical-exact-mixed-colour-citation",
    },
    {
        "role": "reader",
        "page": 357,
        "target": "prop*.2765",
        "old_rect": [452.929, 170.758, 885.308, 188.812],
        "annotation_colour": [1.0, 0.0, 0.0],
        "glyph_x0": 453.925,
        "glyph_x1": 503.758285,
        "text_ascii": "and\\u0662\\u0662.\\u0663\\u0663",
        "method": "compact-classical-exact-mixed-colour-citation",
    },
    {
        "role": "reader",
        "target": "cite.Peter1935a",
        "old_rect": [505.938, 427.820, 974.182, 446.902],
        "glyph_x0": 506.934,
        "glyph_x1": 539.627295,
        "text_ascii": ")1935a",
    },
    {
        "role": "supplement",
        "target": "prop*.2290",
        "old_rect": [210.531, 302.906, 642.910, 321.098],
        "glyph_x0": 211.536,
        "glyph_x1": 239.750307,
        "text_ascii": "19.18",
    },
    {
        "role": "supplement",
        "target": "prop*.2299",
        "old_rect": [453.581, 196.050, 885.960, 214.119],
        "glyph_x0": 454.578,
        "glyph_x1": 503.761428,
        "text_ascii": "and20.21",
    },
    {
        "role": "supplement",
        "target": "prop*.2310",
        "old_rect": [453.807, 597.703, 886.185, 614.042],
        "glyph_x0": 454.803,
        "glyph_x1": 503.761428,
        "text_ascii": "and20.23",
    },
    {
        "role": "supplement",
        "target": "Item*.2318",
        "old_rect": [208.066, 522.825, 640.445, 540.893],
        "glyph_x0": 209.062,
        "glyph_x1": 244.741399,
        "text_ascii": "Items1",
    },
    {
        "role": "supplement",
        "target": "Item*.2319",
        "old_rect": [436.610, 464.621, 868.989, 480.960],
        "glyph_x0": 437.607,
        "glyph_x1": 473.286399,
        "text_ascii": "Items2",
    },
    {
        "role": "supplement",
        "target": "Item*.2319",
        "old_rect": [228.027, 440.096, 660.406, 457.053],
        "glyph_x0": 229.024,
        "glyph_x1": 264.021666,
        "text_ascii": "Items2",
    },
    # Final source-reconciled layout.  These nine spans include the six
    # reflowed historical fallbacks above plus three inflated-but-inside
    # annotations that the older outside-page-only scan never reached.  Each
    # fallback still verifies exact target, rectangle, glyph bounds and text.
    {
        "role": "supplement",
        "target": "prop*.2291",
        "old_rect": [210.531, 533.377, 642.910, 551.568],
        "glyph_x0": 211.535879,
        "glyph_x1": 239.750307,
        "text_ascii": "19.18",
    },
    {
        "role": "supplement",
        "target": "prop*.2300",
        "old_rect": [453.581, 424.412, 885.960, 442.481],
        "glyph_x0": 454.578,
        "glyph_x1": 503.761428,
        "text_ascii": "and20.21",
    },
    {
        "role": "supplement",
        "target": "Item*.2305",
        "old_rect": [137.030, 351.387, 569.409, 371.339],
        "glyph_x0": 138.027,
        "glyph_x1": 172.652812,
        "text_ascii": "Items1",
    },
    {
        "role": "supplement",
        "target": "Item*.2306",
        "old_rect": [77.226, 308.963, 509.604, 327.031],
        "glyph_x0": 78.222,
        "glyph_x1": 114.226771,
        "text_ascii": "Items2",
    },
    {
        "role": "supplement",
        "target": "prop*.2311",
        "old_rect": [77.226, 220.831, 509.604, 237.170],
        "glyph_x0": 78.229637,
        "glyph_x1": 106.444066,
        "text_ascii": "19.23",
    },
    {
        "role": "supplement",
        "target": "prop*.2311",
        "old_rect": [453.807, 160.101, 886.185, 176.440],
        "glyph_x0": 454.803,
        "glyph_x1": 503.761428,
        "text_ascii": "and20.23",
    },
    {
        "role": "supplement",
        "target": "Item*.2319",
        "old_rect": [208.066, 85.223, 640.445, 103.291],
        "glyph_x0": 209.062,
        "glyph_x1": 244.741399,
        "text_ascii": "Items1",
    },
    {
        "role": "supplement",
        "target": "Item*.2320",
        "old_rect": [436.610, 682.550, 868.989, 698.889],
        "glyph_x0": 437.607,
        "glyph_x1": 473.286399,
        "text_ascii": "Items2",
    },
    {
        "role": "supplement",
        "target": "Item*.2320",
        "old_rect": [228.027, 658.025, 660.406, 674.982],
        "glyph_x0": 229.024,
        "glyph_x1": 264.021666,
        "text_ascii": "Items2",
    },
    # The final Classical closure source reflowed all eleven inflated links
    # away from the prior audited coordinates and typeset Eastern Arabic
    # digits.  Its annotation colours are RGB, while the intended linked
    # glyphs are emitted in CMYK, so colour-only inference is impossible.
    # These fallbacks therefore require the exact page, target, old rectangle,
    # annotation colour, glyph text and glyph bounds observed in that source.
    {
        "role": "supplement",
        "page": 9,
        "target": "prop*.2291",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [169.848, 561.742, 602.226, 578.080],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 170.846712064,
        "glyph_x1": 199.934997472,
        "text_ascii": r"\u0661\u0669.\u0661\u0668",
        "method": "current-classical-source-reconciled-bidi-glyph-span",
    },
    {
        "role": "supplement",
        "page": 9,
        "target": "prop*.2300",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [166.982, 417.170, 599.360, 433.509],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 167.989021824,
        "glyph_x1": 197.077307232,
        "text_ascii": r"\u0661\u0669.\u0662\u0661",
        "method": "current-classical-source-reconciled-bidi-glyph-span",
    },
    {
        "role": "supplement",
        "page": 9,
        "target": "Item*.2305",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [353.942, 291.003, 786.321, 307.120],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 354.939,
        "glyph_x1": 391.348162608,
        "text_ascii": r"Items\u0661",
        "method": "current-classical-source-reconciled-bidi-glyph-span",
    },
    {
        "role": "supplement",
        "page": 9,
        "target": "Item*.2306",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [159.160, 230.609, 591.539, 246.726],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 160.156,
        "glyph_x1": 194.767867888,
        "text_ascii": r"Items\u0662",
        "method": "current-classical-source-reconciled-bidi-glyph-span",
    },
    {
        "role": "supplement",
        "page": 9,
        "target": "prop*.2311",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [450.687, 84.660, 883.065, 102.276],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 451.683,
        "glyph_x1": 503.758285408,
        "text_ascii": r"and\u0662\u0660.\u0662\u0663",
        "method": "current-classical-source-reconciled-bidi-glyph-span",
    },
    {
        "role": "supplement",
        "page": 10,
        "target": "prop*.2311",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [77.226, 682.649, 509.604, 698.766],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 78.229108704,
        "glyph_x1": 107.317394112,
        "text_ascii": r"\u0661\u0669.\u0662\u0663",
        "method": "current-classical-source-reconciled-bidi-glyph-span",
    },
    {
        "role": "supplement",
        "page": 10,
        "target": "Item*.2319",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [225.022, 537.072, 657.401, 553.189],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 226.018,
        "glyph_x1": 262.473644368,
        "text_ascii": r"Items\u0661",
        "method": "current-classical-source-reconciled-bidi-glyph-span",
    },
    {
        "role": "supplement",
        "page": 10,
        "target": "Item*.2320",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [176.825, 474.314, 609.203, 492.459],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 177.821,
        "glyph_x1": 212.789228048,
        "text_ascii": r"Items\u0662",
        "method": "current-classical-source-reconciled-bidi-glyph-span",
    },
    {
        "role": "supplement",
        "page": 10,
        "target": "Item*.2320",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [475.133, 395.278, 907.512, 413.545],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 476.129,
        "glyph_x1": 503.758672112,
        "text_ascii": r"and\u0662",
        "method": "current-classical-source-reconciled-bidi-glyph-span",
    },
    {
        "role": "supplement",
        "page": 23,
        "target": "lem*.519",
        "old_rect": [260.817, 178.996, 729.061, 198.949],
        "annotation_colour": [1.0, 0.0, 0.0],
        "glyph_x0": 261.816134048,
        "glyph_x1": 284.844747344,
        "text_ascii": r"\u0666.\u0661\u0664",
        "method": "current-classical-source-reconciled-bidi-glyph-span",
    },
    {
        "role": "supplement",
        "page": 123,
        "target": "table.502",
        "old_rect": [436.208, 174.943, 904.452, 194.896],
        "annotation_colour": [1.0, 0.0, 0.0],
        "glyph_x0": 437.218128912,
        "glyph_x1": 454.187070096,
        "text_ascii": r"\u0666.\u0663",
        "method": "current-classical-source-reconciled-bidi-glyph-span",
    },
    # The compact-symbol registry moves the same eleven closure references
    # from the 157-page layout to a 145-page layout. Each of these fresh
    # fallbacks is bound to the exact raw PDF's page, target, external file
    # when present, rectangle, annotation colour, and painted glyph span.
    {
        "role": "supplement", "page": 8, "target": "prop*.2291",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [219.863, 569.851, 652.242, 586.190],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 220.868572, "glyph_x1": 249.956857,
        "text_ascii": r"\u0661\u0669.\u0661\u0668",
        "method": "compact-classical-closure-exact-bidi-glyph-span",
    },
    {
        "role": "supplement", "page": 8, "target": "prop*.2300",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [452.037, 461.676, 884.415, 478.300],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 453.033, "glyph_x1": 503.758285,
        "text_ascii": r"and\u0662\u0660.\u0662\u0661",
        "method": "compact-classical-closure-exact-bidi-glyph-span",
    },
    {
        "role": "supplement", "page": 8, "target": "Item*.2305",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [135.894, 389.653, 568.273, 407.480],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 136.891, "glyph_x1": 173.455102,
        "text_ascii": r"Items\u0661",
        "method": "compact-classical-closure-exact-bidi-glyph-span",
    },
    {
        "role": "supplement", "page": 8, "target": "Item*.2306",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [77.226, 348.725, 509.604, 365.123],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 78.222, "glyph_x1": 115.560798,
        "text_ascii": r"Items\u0662",
        "method": "compact-classical-closure-exact-bidi-glyph-span",
    },
    {
        "role": "supplement", "page": 8, "target": "prop*.2311",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [176.178, 259.446, 608.556, 275.785],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 177.188689, "glyph_x1": 206.276974,
        "text_ascii": r"\u0661\u0669.\u0662\u0663",
        "method": "compact-classical-closure-exact-bidi-glyph-span",
    },
    {
        "role": "supplement", "page": 8, "target": "prop*.2311",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [77.226, 217.287, 509.604, 233.638],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 78.230587, "glyph_x1": 107.318872,
        "text_ascii": r"\u0661\u0669.\u0662\u0663",
        "method": "compact-classical-closure-exact-bidi-glyph-span",
    },
    {
        "role": "supplement", "page": 8, "target": "Item*.2319",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [300.541, 127.781, 732.920, 144.178],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 301.537, "glyph_x1": 337.512333,
        "text_ascii": r"Items\u0661",
        "method": "compact-classical-closure-exact-bidi-glyph-span",
    },
    {
        "role": "supplement", "page": 8, "target": "Item*.2320",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [436.172, 67.110, 868.550, 83.970],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 437.168, "glyph_x1": 473.081357,
        "text_ascii": r"Items\u0662",
        "method": "compact-classical-closure-exact-bidi-glyph-span",
    },
    {
        "role": "supplement", "page": 9, "target": "Item*.2320",
        "target_file": "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf",
        "old_rect": [221.332, 698.330, 653.711, 717.073],
        "annotation_colour": [0.0, 0.5, 0.5],
        "glyph_x0": 222.329, "glyph_x1": 258.366309,
        "text_ascii": r"Items\u0662",
        "method": "compact-classical-closure-exact-bidi-glyph-span",
    },
    {
        "role": "supplement", "page": 21, "target": "lem*.519",
        "old_rect": [260.817, 371.946, 729.061, 391.898],
        "annotation_colour": [1.0, 0.0, 0.0],
        "glyph_x0": 261.816134, "glyph_x1": 284.844747,
        "text_ascii": r"\u0666.\u0661\u0664",
        "method": "compact-classical-closure-exact-bidi-glyph-span",
    },
    {
        "role": "supplement", "page": 113, "target": "table.502",
        "old_rect": [436.208, 401.094, 904.452, 421.047],
        "annotation_colour": [1.0, 0.0, 0.0],
        "glyph_x0": 437.218129, "glyph_x1": 454.187070,
        "text_ascii": r"\u0666.\u0663",
        "method": "compact-classical-closure-exact-bidi-glyph-span",
    },
)


def document_role(path: Path) -> str:
    normalized = path.name.lower().replace("_", "-")
    return "supplement" if "closure-supplement" in normalized else "reader"


def input_count_authority(input_path: Path, reader: PdfReader, role: str) -> dict:
    """Artifact-specific counts; unknown layouts retain the original guard."""
    digest = CORE.sha256_file(input_path).upper()
    supplement = AUDITED_MSA_SUPPLEMENT_INPUTS.get(digest)
    if supplement is not None:
        if role != "supplement" or len(reader.pages) != supplement["pages"]:
            CORE.die("audited MSA input has an unexpected role or page count")
        return {"kind": "exact-audited-msa-input", "role": role,
                "input_sha256": digest, **supplement,
                "scope_ar": "إقرار خاص ببايتات الملحق المعين: جميع الإحالات سليمة ولا مستطيل يحتاج إلى إصلاح. لا يتغير الحارس التاريخي لمدخل آخر."}
    layout = AUDITED_MSA_READER_INPUTS.get(digest)
    if layout is None:
        return {"kind": "legacy-role-guard", "role": role,
                "expected_count": EXPECTED_COUNTS[role]}
    expected_pages = AUDITED_MSA_READER_PAGES.get(digest, 1019)
    if role != "reader" or len(reader.pages) != expected_pages:
        CORE.die("audited MSA input has an unexpected role or page count")
    return {"kind": "exact-audited-msa-input", "layout": layout,
            "input_sha256": digest, "pages": expected_pages,
            "expected_count": AUDITED_MSA_READER_COUNTS.get(digest, 161),
            "scope_ar": "إقرار خاص ببايتات القارئ المعياري المعين، لا توسعة عامة لعدد المستطيلات ولا تغيير لإقرارات الطبعة التراثية. تظل كل إحالة خاضعة لشاهد الحروف والتحقق من حفظ الوجهة والمحتوى."}


def target_destination(annot: Any) -> str:
    action = annot.get("/A")
    if action is not None:
        return str(action.get_object().get("/D"))
    return str(annot.get("/Dest"))


def target_file(annot: Any) -> str | None:
    action = annot.get("/A")
    if action is None:
        return None
    value = action.get_object().get("/F")
    return None if value is None else str(value)


def close(left: float, right: float, tolerance: float = 0.01) -> bool:
    return abs(left - right) <= tolerance


def match_audited_valid_width_collision(
    role: str, annot: Any, page_number: int
) -> dict[str, Any] | None:
    action = annot.get("/A")
    action_object = action.get_object() if action is not None else None
    if action_object is None or str(action_object.get("/S")) != "/URI":
        return None
    uri = str(action_object.get("/URI"))
    rect = CORE.rect_values(annot)
    matches = [
        collision
        for collision in AUDITED_VALID_WIDTH_COLLISIONS
        if collision["role"] == role
        and collision["page"] == page_number
        and collision["uri"] == uri
        and CORE.colours_match(
            annot.get("/C"), collision["annotation_colour"]
        )
        and all(
            close(left, right)
            for left, right in zip(rect, collision["rect"])
        )
    ]
    if len(matches) > 1:
        CORE.die(f"ambiguous audited URI width collision on p{page_number}: {rect}")
    return matches[0] if matches else None


def scan_bad_annotations(
    reader: PdfReader, *, expected_count: int | None, role: str | None = None
) -> tuple[list[dict[str, Any]], Counter]:
    bad: list[dict[str, Any]] = []
    signatures: Counter = Counter()
    for page_index, page in enumerate(reader.pages):
        box = [CORE.f(value) for value in page.mediabox]
        observed = (box[0], box[1], box[2] - box[0], box[3] - box[1])
        expected = (0.0, 0.0, PAGE_WIDTH, PAGE_HEIGHT)
        if any(not close(left, right, 0.001) for left, right in zip(observed, expected)):
            CORE.die(f"p{page_index + 1}: MediaBox is not [0,0,612,792]: {box}")
        for annotation_index, ref in enumerate(page.get("/Annots") or []):
            annot = ref.get_object()
            if str(annot.get("/Subtype")) != "/Link":
                continue
            rect = CORE.rect_values(annot)
            outside = (
                rect[0] < -0.01
                or rect[1] < -0.01
                or rect[2] > PAGE_WIDTH + 0.01
                or rect[3] > PAGE_HEIGHT + 0.01
            )
            if outside and not (
                rect[2] > PAGE_WIDTH + 0.01
                and rect[0] >= -0.01
                and rect[1] >= -0.01
                and rect[3] <= PAGE_HEIGHT + 0.01
            ):
                CORE.die(
                    f"p{page_index + 1} a{annotation_index}: "
                    f"unknown outside-page direction {rect}"
                )
            signature = rect[2] - rect[0]
            nearest = min(EXPECTED_INFLATIONS, key=lambda value: abs(value - signature))
            known_inflation = close(nearest, signature)
            audited_span = (
                match_audited_span(role, annot, page_index + 1)
                if role is not None
                else None
            )
            forced_audited = bool(
                audited_span is not None and audited_span.get("force_scan")
            )
            if not known_inflation and not forced_audited:
                if outside:
                    CORE.die(
                        f"p{page_index + 1} a{annotation_index}: "
                        f"unknown width signature {signature:.6f}"
                    )
                continue
            action = annot.get("/A")
            action_kind = (
                str(action.get_object().get("/S"))
                if action is not None
                else None
            )
            if action_kind not in ("/GoTo", "/GoToR"):
                valid_collision = (
                    match_audited_valid_width_collision(
                        role, annot, page_index + 1
                    )
                    if role is not None and not outside and known_inflation
                    else None
                )
                if valid_collision is not None:
                    continue
                CORE.die(
                    f"p{page_index + 1} a{annotation_index}: "
                    "malformed rectangle is not a GoTo/GoToR link"
                )
            kind = "inflated-width" if known_inflation else "audited-undersized"
            if known_inflation:
                signatures[round(signature, 3)] += 1
            bad.append(
                {
                    "page_index": page_index,
                    "annotation_index": annotation_index,
                    "annot": annot,
                    "kind": kind,
                }
            )
    if expected_count is not None and len(bad) != expected_count:
        CORE.die(
            f"malformed link count changed: expected {expected_count}, got {len(bad)}"
        )
    return bad, signatures


def match_audited_span(
    role: str, annot: Any, page_number: int | None = None
) -> dict[str, Any] | None:
    destination = target_destination(annot)
    destination_file = target_file(annot)
    old_rect = CORE.rect_values(annot)
    matches = [
        span
        for span in AUDITED_SPANS
        if span["role"] == role
        and span["target"] == destination
        and ("page" not in span or span["page"] == page_number)
        and ("target_file" not in span or span["target_file"] == destination_file)
        and (
            "annotation_colour" not in span
            or CORE.colours_match(annot.get("/C"), span["annotation_colour"])
        )
        and all(close(left, right) for left, right in zip(old_rect, span["old_rect"]))
    ]
    if len(matches) > 1:
        CORE.die(f"ambiguous audited span for {destination}: {old_rect}")
    return matches[0] if matches else None


def audited_mapping(
    page_number: int,
    annotation_index: int,
    annot: Any,
    chars: list[dict[str, Any]],
    span: dict[str, Any],
) -> dict[str, Any]:
    old_rect = CORE.rect_values(annot)
    band_top = PAGE_HEIGHT - old_rect[3]
    band_bottom = PAGE_HEIGHT - old_rect[1]
    witnesses = []
    for char in chars:
        centre_y = (CORE.f(char["top"]) + CORE.f(char["bottom"])) / 2.0
        centre_x = (CORE.f(char["x0"]) + CORE.f(char["x1"])) / 2.0
        if (
            band_top - 0.5 <= centre_y <= band_bottom + 0.5
            and span["glyph_x0"] - 0.25 <= centre_x <= span["glyph_x1"] + 0.25
        ):
            witnesses.append(char)
    if not witnesses:
        CORE.die(f"p{page_number} a{annotation_index}: audited span has no glyph witnesses")
    witnesses.sort(key=lambda char: (CORE.f(char["x0"]), CORE.f(char["x1"])))
    text = "".join(str(char.get("text", "")) for char in witnesses)
    observed_ascii = CORE.text_ascii(text).replace(" ", "")
    if observed_ascii != span["text_ascii"]:
        CORE.die(
            f"p{page_number} a{annotation_index}: audited glyph text changed: "
            f"expected {span['text_ascii']!r}, got {observed_ascii!r}"
        )
    glyph_x0 = min(CORE.f(char["x0"]) for char in witnesses)
    glyph_x1 = max(CORE.f(char["x1"]) for char in witnesses)
    if not close(glyph_x0, span["glyph_x0"], 0.02) or not close(
        glyph_x1, span["glyph_x1"], 0.02
    ):
        CORE.die(
            f"p{page_number} a{annotation_index}: audited glyph bounds changed: "
            f"{glyph_x0:.6f}..{glyph_x1:.6f}"
        )
    new_x0 = CORE.f(span.get("new_x0", old_rect[0]))
    new_x1 = CORE.f(span.get("new_x1", span["glyph_x1"] + 1.0))
    if new_x0 > glyph_x0 + 0.01 or new_x1 < glyph_x1 - 0.01:
        CORE.die(
            f"p{page_number} a{annotation_index}: audited repaired rectangle "
            "does not contain its exact glyph span"
        )
    new_rect = [new_x0, old_rect[1], new_x1, old_rect[3]]
    return {
        "page": page_number,
        "annotation_index": annotation_index,
        "target": CORE.action_summary(annot),
        "old_rect": [round(value, 6) for value in old_rect],
        "new_rect": [round(value, 6) for value in new_rect],
        "inflation_signature": round(old_rect[2] - old_rect[0], 6),
        "glyph_bbox_top_coordinates": [
            round(glyph_x0, 6),
            round(min(CORE.f(char["top"]) for char in witnesses), 6),
            round(glyph_x1, 6),
            round(max(CORE.f(char["bottom"]) for char in witnesses), 6),
        ],
        "glyph_text_ascii": observed_ascii,
        "annotation_colour": list(CORE.colour_tuple(annot.get("/C"))),
        "malformation_kind": span.get("malformation_kind", "inflated-width"),
        "method": span.get("method", "prior-r2-witnessed-bidi-glyph-span"),
        "companion_rects": [],
        "candidate_runs": [
            {
                "x0": round(glyph_x0, 6),
                "x1": round(glyph_x1, 6),
                "text_ascii": observed_ascii,
            }
        ],
    }


def verify_existing_repair(input_path: Path, output_path: Path, receipt_path: Path,
                           role: str, authority: dict) -> None:
    """Reuse only the exact, previously verified postprocessor result."""
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if (receipt.get("schema") != "arabic-letter-rtl-link-rect-repair-v1"
            or receipt.get("dry_run") is not False
            or receipt.get("document_role") != role
            or receipt.get("input_sha256") != CORE.sha256_file(input_path)
            or receipt.get("output_sha256") != CORE.sha256_file(output_path)
            or receipt.get("output_bytes") != output_path.stat().st_size
            or receipt.get("malformed_link_rectangles") != authority["expected_count"]):
        CORE.die("existing repair checkpoint identity differs")
    invariants = receipt.get("semantic_invariants", {})
    required = ("strict_reopen", "page_count_equal", "all_page_content_stream_hashes_equal",
                "text_extraction_fingerprint_equal", "metadata_fingerprint_equal",
                "named_destinations_fingerprint_equal", "outline_fingerprint_equal",
                "font_resource_fingerprint_equal", "page_box_fingerprint_equal",
                "catalog_view_equal", "all_link_targets_valid", "annotation_counts_equal",
                "non_rect_annotation_semantics_equal")
    if not all(invariants.get(key) is True for key in required):
        CORE.die("existing repair checkpoint lacks preservation evidence")
    if (invariants.get("changed_pdf_keys") != ["page /Annots[n] /Rect"]
            or invariants.get("rectangles_changed_exactly") != authority["expected_count"]):
        CORE.die("existing repair checkpoint change scope differs")
    final = PdfReader(str(output_path), strict=True)
    if len(final.pages) != receipt.get("pages"):
        CORE.die("existing repaired page count differs")
    scan_bad_annotations(final, expected_count=0, role=role)
    if CORE.validate_link_targets(final, output_path) != invariants.get("link_target_counts"):
        CORE.die("existing repaired link inventory differs")
    print(json.dumps({"status": "PASS", "reused": True,
                      "output_sha256": receipt["output_sha256"]}))


def run(input_path: Path, output_path: Path, receipt_path: Path, dry_run: bool,
        resume_verified: bool = False) -> None:
    role = document_role(input_path)
    reader = PdfReader(str(input_path), strict=True)
    count_authority = input_count_authority(input_path, reader, role)
    if resume_verified and not dry_run and output_path.exists():
        verify_existing_repair(input_path, output_path, receipt_path, role, count_authority)
        return
    bad, signatures = scan_bad_annotations(
        reader, expected_count=count_authority["expected_count"], role=role
    )
    by_page: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for entry in bad:
        by_page[entry["page_index"]].append(entry)

    mappings: list[dict[str, Any]] = []
    used_audited: list[dict[str, Any]] = []
    with pdfplumber.open(str(input_path)) as plumber:
        for page_index in sorted(by_page):
            page = reader.pages[page_index]
            annots = [ref.get_object() for ref in (page.get("/Annots") or [])]
            chars = plumber.pages[page_index].chars
            for entry in by_page[page_index]:
                span = match_audited_span(
                    role, entry["annot"], page_index + 1
                )
                if span is not None:
                    mappings.append(
                        audited_mapping(
                            page_index + 1,
                            entry["annotation_index"],
                            entry["annot"],
                            chars,
                            span,
                        )
                    )
                    used_audited.append(span)
                else:
                    mappings.append(
                        CORE.infer_mapping(
                            page_index + 1,
                            entry["annotation_index"],
                            entry["annot"],
                            annots,
                            chars,
                            PAGE_WIDTH,
                            PAGE_HEIGHT,
                        )
                    )
            plumber.pages[page_index].close()

    # AUDITED_SPANS are coordinate-specific fallbacks for layouts where the
    # generic glyph-run inference was ambiguous.  A reflowed occurrence need
    # not retain the old coordinates; when it does not, the same strict generic
    # inference must succeed.  Exact matches are still forced through the
    # audited fallback by match_audited_span().
    if len(mappings) != len(bad):
        CORE.die("mapping count does not equal malformed annotation count")

    receipt: dict[str, Any] = {
        "schema": "arabic-letter-rtl-link-rect-repair-v1",
        "document_role": role,
        "count_authority": count_authority,
        "input": str(input_path.resolve()),
        "output": str(output_path.resolve()),
        "input_sha256": CORE.sha256_file(input_path),
        "pages": len(reader.pages),
        "malformed_link_rectangles": len(bad),
        "outside_page_before_repair": sum(
            1 for entry in bad
            if CORE.rect_values(entry["annot"])[2] > PAGE_WIDTH + 0.01
        ),
        "inside_page_inflated_before_repair": sum(
            1 for entry in bad
            if entry["kind"] == "inflated-width"
            and CORE.rect_values(entry["annot"])[2] <= PAGE_WIDTH + 0.01
        ),
        "audited_undersized_before_repair": sum(
            1 for entry in bad if entry["kind"] == "audited-undersized"
        ),
        "width_signatures": dict(sorted(signatures.items())),
        "audited_span_count": len(used_audited),
        "mappings": mappings,
        "dry_run": dry_run,
    }
    if dry_run:
        print(json.dumps(receipt, ensure_ascii=True, indent=2, sort_keys=True))
        return
    if output_path.exists():
        CORE.die(f"refusing to overwrite output: {output_path}")

    before_content = CORE.content_hashes(reader)
    before_annots = CORE.annotation_snapshot(reader)
    before_text = CORE.text_extraction_fingerprint(reader)
    before_metadata = CORE.metadata_fingerprint(reader)
    before_destinations = CORE.named_destination_fingerprint(reader)
    before_outline = CORE.outline_fingerprint(reader)
    before_fonts = CORE.font_fingerprint(reader)
    before_boxes = CORE.page_box_fingerprint(reader)
    before_catalog = CORE.catalog_view(reader)

    for mapping in mappings:
        page = reader.pages[mapping["page"] - 1]
        annot = (page.get("/Annots") or [])[mapping["annotation_index"]].get_object()
        current = [round(value, 6) for value in CORE.rect_values(annot)]
        if current != mapping["old_rect"]:
            CORE.die(
                f"p{mapping['page']} a{mapping['annotation_index']}: "
                "/Rect changed before write"
            )
        annot[NameObject("/Rect")] = ArrayObject(
            [FloatObject(value) for value in mapping["new_rect"]]
        )

    writer = PdfWriter(clone_from=reader)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        writer.write(handle)

    final_reader = PdfReader(str(output_path), strict=True)
    remaining, _ = scan_bad_annotations(
        final_reader, expected_count=0, role=role
    )
    if remaining:
        CORE.die(f"final PDF still contains {len(remaining)} outside-page links")
    if before_content != CORE.content_hashes(final_reader):
        CORE.die("page content streams changed during annotation-only rewrite")

    after_annots = CORE.annotation_snapshot(final_reader)
    expected_changes = {
        (mapping["page"], mapping["annotation_index"]): mapping for mapping in mappings
    }
    observed_changes: list[tuple[int, int]] = []
    if len(before_annots) != len(after_annots):
        CORE.die("page count changed in annotation snapshot")
    for page_index, (before_page, after_page) in enumerate(
        zip(before_annots, after_annots), 1
    ):
        if len(before_page) != len(after_page):
            CORE.die(f"p{page_index}: annotation count changed")
        for annotation_index, (before_annot, after_annot) in enumerate(
            zip(before_page, after_page)
        ):
            if before_annot["semantic"] != after_annot["semantic"]:
                CORE.die(
                    f"p{page_index} a{annotation_index}: "
                    "non-/Rect annotation semantics changed"
                )
            if before_annot["rect"] != after_annot["rect"]:
                observed_changes.append((page_index, annotation_index))
                mapping = expected_changes.get((page_index, annotation_index))
                if mapping is None or after_annot["rect"] != mapping["new_rect"]:
                    CORE.die(
                        f"p{page_index} a{annotation_index}: unexpected /Rect delta"
                    )
    if set(observed_changes) != set(expected_changes):
        CORE.die("observed /Rect changes do not equal the fail-closed mapping")

    comparisons = {
        "text_extraction_fingerprint_equal": (
            before_text == CORE.text_extraction_fingerprint(final_reader)
        ),
        "metadata_fingerprint_equal": (
            before_metadata == CORE.metadata_fingerprint(final_reader)
        ),
        "named_destinations_fingerprint_equal": (
            before_destinations == CORE.named_destination_fingerprint(final_reader)
        ),
        "outline_fingerprint_equal": (
            before_outline == CORE.outline_fingerprint(final_reader)
        ),
        "font_resource_fingerprint_equal": (
            before_fonts == CORE.font_fingerprint(final_reader)
        ),
        "page_box_fingerprint_equal": (
            before_boxes == CORE.page_box_fingerprint(final_reader)
        ),
        "catalog_view_equal": before_catalog == CORE.catalog_view(final_reader),
    }
    failed = [name for name, value in comparisons.items() if not value]
    if failed:
        CORE.die(f"semantic post-write comparisons failed: {failed}")
    target_counts = CORE.validate_link_targets(final_reader, output_path)

    receipt.update(
        {
            "dry_run": False,
            "output_sha256": CORE.sha256_file(output_path),
            "output_bytes": output_path.stat().st_size,
            "semantic_invariants": {
                "strict_reopen": True,
                "page_count_equal": len(reader.pages) == len(final_reader.pages),
                "all_page_content_stream_hashes_equal": True,
                **comparisons,
                "text_extraction_sha256": CORE.text_extraction_fingerprint(final_reader),
                "metadata_sha256": CORE.metadata_fingerprint(final_reader),
                "named_destinations_sha256": CORE.named_destination_fingerprint(final_reader)[0],
                "named_destinations_count": CORE.named_destination_fingerprint(final_reader)[1],
                "outline_sha256": CORE.outline_fingerprint(final_reader)[0],
                "outline_count": CORE.outline_fingerprint(final_reader)[1],
                "font_resources_sha256": CORE.font_fingerprint(final_reader)[0],
                "font_resource_occurrences": CORE.font_fingerprint(final_reader)[1],
                "page_boxes_sha256": CORE.page_box_fingerprint(final_reader),
                "catalog_view": CORE.catalog_view(final_reader),
                "link_target_counts": target_counts,
                "all_link_targets_valid": True,
                "outside_page_link_rectangles_final": 0,
                "annotation_counts_equal": True,
                "non_rect_annotation_semantics_equal": True,
                "rectangles_changed_exactly": len(observed_changes),
                "changed_pdf_keys": ["page /Annots[n] /Rect"],
            },
        }
    )
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output_path),
                "receipt": str(receipt_path),
                "changed": len(mappings),
                "sha256": receipt["output_sha256"],
            },
            sort_keys=True,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume-verified", action="store_true",
                        help="Reuse an existing exact output only after its repair receipt and link inventory validate.")
    args = parser.parse_args()
    try:
        run(args.input, args.output, args.receipt, args.dry_run, args.resume_verified)
    except Exception as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
