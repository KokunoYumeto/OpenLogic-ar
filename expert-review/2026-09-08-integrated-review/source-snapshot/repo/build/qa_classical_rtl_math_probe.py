#!/usr/bin/env python3
"""Fail-closed runtime QA for the isolated classical RTL-math probe.

The producer manifest and recorder files bind the guarded TeX invocations to
their inputs.  PDF checks cover directions, geometry, links, destinations,
logical extraction, fonts, and deterministic replay.  This is deliberately an
isolated-probe receipt, not acceptance evidence for a complete reader.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import unicodedata
import uuid

import pdfplumber
import pypdf


SCHEMA = "openlogic-classical-rtl-math-runtime-probe-v7"
BUILD_SCHEMA = "openlogic-classical-rtl-math-probe-build-v1"
GUARD_SCHEMA = "interlanguage-tex-mutex/v2"
MUTEX_NAME = r"Global\InterlanguageTeXSlotV1"
CONTAINMENT = (
    "Windows Job Object; atomic job assignment; suspended start; "
    "kill-on-close; no breakaway"
)
OUTPUT_TRANSPORT = (
    "inherited native standard handles (outer-process redirection supported)"
)
EXPECTED_URI = "https://example.org/rtl-math/A-to-B"
GEOMETRY_URI_PREFIX = "https://example.org/rtl-geom/"
EXPECTED_INTERNAL_TARGETS = ("probe-eq-one", "probe-eq-align")
SOURCE_SIGNATURE = "OLC-RTL-SOURCE-SIGNATURE=P01-P20-v9"
PROBE_IDS = tuple(f"P{i:02d}" for i in range(1, 21))
EXPECTED_PAGE_COUNT = 10
PAGE_BY_PROBE = {
    **{f"P{i:02d}": 1 for i in range(1, 10)},
    **{f"P{i:02d}": 2 for i in range(10, 15)},
    # P15 and P18 deliberately split their exhaustive registry tables across
    # two pages so deep legacy glyphs and link rectangles never crowd a
    # neighboring row.  P15 still occupies pages 3--4; P18 occupies 7--8.
    "P15": 3, "P16": 5, "P17": 6, "P18": 7,
    "P19": 9, "P20": 10,
}

# This is the complete, finite presentation registry.  The exact same order
# must be logged once by the TeX layer.  Adding a plausible-looking symbol is
# a failure until it has an evidence-backed type and two-sided probe coverage.
REGISTRY_PAIRS = (
    ("arrow", "rightarrow", "leftarrow", "simple", "mathrel", "UTR25-formula-relative"),
    ("long-arrow", "longrightarrow", "longleftarrow", "long-single", "mathrel", "UTR25-formula-relative"),
    ("double-arrow", "Rightarrow", "Leftarrow", "simple", "mathrel", "UTR25-formula-relative"),
    ("long-double-arrow", "Longrightarrow", "Longleftarrow", "long-double", "mathrel", "UTR25-formula-relative"),
    ("x-arrow", "xrightarrow", "xleftarrow", "boxed-x-arrow", "mathrel", "pinned-amsmath-extensible-pair"),
    ("x-long-double-arrow", "xLongrightarrow", "xLongleftarrow", "boxed-x-long-double-arrow", "mathrel", "pinned-extarrows-extensible-pair"),
    ("mapsto", "mapsto", "OLClassicalMapsFrom", "mapsto", "mathrel", "formula-relative-map"),
    ("long-mapsto", "longmapsto", "OLClassicalLongMapsFrom", "long-mapsto", "mathrel", "formula-relative-map"),
    ("counterfactual", "boxright", "OLClassicalBoxLeft", "simple", "mathbin", "pinned-ntxsyc-slot-pair"),
    ("strict-conditional", "fishhookright", "OLClassicalFishhookLeft", "simple", "mathbin", "pinned-ntxsyc-slot-pair"),
    ("literal-order", "literal-lt", "literal-gt", "literal", "mathrel", "Unicode-BidiMirroring"),
    ("order-eq", "leq", "geq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("membership", "in", "ni", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("precedence", "prec", "succ", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("precedence-eq", "preceq", "succeq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("negated-precedence-eq", "npreceq", "nsucceq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("curly-precedence-eq", "preccurlyeq", "succcurlyeq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("precedence-sim", "precsim", "succsim", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("negated-order", "nless", "ngtr", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("dotted-order", "lessdot", "gtrdot", "simple", "mathbin", "pinned-ams-symbol-pair"),
    ("nonstandard-order", "varolessthan", "varogreaterthan", "simple", "mathbin", "pinned-stmaryrd-pair"),
    ("subset", "subset", "supset", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("subset-eq", "subseteq", "supseteq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("negated-subset-eq", "nsubseteq", "nsupseteq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("proper-subset", "subsetneq", "supsetneq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("square-subset", "sqsubset", "sqsupset", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("square-subset-eq", "sqsubseteq", "sqsupseteq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("restriction", "upharpoonright", "upharpoonleft", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("triangle-order", "lhd", "rhd", "simple", "mathbin", "Unicode-BidiMirroring"),
    ("turnstile", "vdash", "dashv", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("over-accent", "overrightarrow", "overleftarrow", "over-accent", "mathord", "formula-relative-accent"),
    ("under-accent", "underrightarrow", "underleftarrow", "under-accent", "mathord", "formula-relative-accent"),
)
REGISTRY_ALIASES = (
    ("to", "rightarrow", "leftarrow"),
    ("gets", "leftarrow", "rightarrow"),
    ("le", "leq", "geq"),
    ("ge", "geq", "leq"),
    ("owns", "ni", "in"),
    ("restriction", "upharpoonright", "upharpoonleft"),
)
REGISTRY_INVARIANTS = (
    ("leftrightarrow", "symmetric"),
    ("longleftrightarrow", "derived-symmetric"),
    ("Leftrightarrow", "symmetric"),
    ("Longleftrightarrow", "derived-symmetric"),
    ("equiv", "symmetric"), ("sim", "symmetric"),
    ("simeq", "symmetric"), ("approx", "symmetric"),
    ("land", "symmetric"), ("lor", "symmetric"),
    ("models", "engine-composite"),
    ("ddots", "engine-composite-mirror"),
    ("iddots", "engine-composite-mirror"),
    ("triangleright", "semantic-left-end-sentinel"),
)
REGISTRY_FALLBACKS = (
    ("nvdash", "scoped-ltr-atom", "mathrel", "no-proven-negated-left-tack-peer"),
    ("vDash", "scoped-ltr-atom", "mathrel", "no-proven-reverse-semantic-tack-peer"),
    ("nvDash", "scoped-ltr-atom", "mathrel", "no-proven-negated-reverse-semantic-tack-peer"),
    ("Vdash", "scoped-ltr-atom", "mathrel", "no-proven-reverse-forcing-tack-peer"),
    ("nVdash", "scoped-ltr-atom", "mathrel", "no-proven-negated-reverse-forcing-tack-peer"),
    ("notin", "scoped-ltr-atom", "mathrel", "no-proven-negated-reverse-membership-peer"),
    ("pto", "scoped-ltr-atom", "mathrel", "preserve-custom-partial-map-overlay"),
    ("rlexless", "scoped-ltr-atom", "mathrel", "preserve-project-spherical-order-glyph"),
    ("xrightarrowdbl", "scoped-ltr-optional-mandatory", "mathrel", "preserve-custom-double-shaft-overlay"),
)
REGISTRY_BOXED_ACCENTS = (
    ("acute", "mathord", "kernel-mathaccent-placement-repair"),
    ("grave", "mathord", "kernel-mathaccent-placement-repair"),
    ("ddot", "mathord", "kernel-mathaccent-placement-repair"),
    ("tilde", "mathord", "kernel-mathaccent-placement-repair"),
    ("bar", "mathord", "kernel-mathaccent-placement-repair"),
    ("breve", "mathord", "kernel-mathaccent-placement-repair"),
    ("check", "mathord", "kernel-mathaccent-placement-repair"),
    ("hat", "mathord", "kernel-mathaccent-placement-repair"),
    ("vec", "mathord", "notation-invariant-vector-accent-placement-repair"),
    ("dot", "mathord", "kernel-mathaccent-placement-repair"),
    ("widetilde", "mathord", "kernel-mathaccent-placement-repair"),
    ("widehat", "mathord", "kernel-mathaccent-placement-repair"),
    ("mathring", "mathord", "kernel-mathaccent-placement-repair"),
)
PAIR_IDS = tuple(row[0] for row in REGISTRY_PAIRS)
ROW_PAIR_IDS = tuple(row[0] for row in REGISTRY_PAIRS
                     if row[3] not in {"over-accent", "under-accent"})
ALIAS_IDS = tuple(row[0] for row in REGISTRY_ALIASES)
INVARIANT_IDS = tuple(row[0] for row in REGISTRY_INVARIANTS)
FALLBACK_IDS = tuple(row[0] for row in REGISTRY_FALLBACKS)
BOXED_ACCENT_IDS = tuple(row[0] for row in REGISTRY_BOXED_ACCENTS)

DIRECT_INPUTS = (
    "tmp/pdfs/classical-rtl-math-probe/common.tex",
    "tmp/pdfs/classical-rtl-math-probe/control.tex",
    "tmp/pdfs/classical-rtl-math-probe/rtl.tex",
    "tmp/pdfs/classical-rtl-math-probe/BUILD_PROBE.ps1",
    "tmp/pdfs/classical-rtl-math-probe/RUN_PROBE.ps1",
    "tmp/pdfs/classical-rtl-math-probe/cache-seed/SEED_MANIFEST.json",
    "source/locale/ar-classical/open-logic-rtl-math.tex",
    "source/sty/open-logic.sty",
    "source/sty/open-logic-defer.sty",
    "source/open-logic-envs.sty",
    "source/locale/ar/open-logic-config.sty",
    "build/qa_classical_rtl_math_probe.py",
    "build/Invoke-WithInterlanguageTeXMutex.ps1",
    "build/InterlanguageTeXCapturedTree.cs",
    "00_control/fonts/scheherazade-2.100/Scheherazade-Regular.ttf",
    "00_control/fonts/scheherazade-2.100/Scheherazade-Bold.ttf",
)
REQUIRED_PRODUCTS = ("aux", "out", "fls", "log", "pdf")
CONVERGENCE_STATE = ("aux", "out", "toc", "lof", "lot", "loe")
KNOWN_DIAGNOSTICS = {
    "MissingGlyph", "OverfullHBox", "OverfullVBox", "UndefinedReference",
    "UndefinedCitation", "MultiplyDefined", "Rerun", "Fatal",
}

def triple_keys(prefix: str) -> tuple[str, str, str]:
    return tuple(f"{prefix}-{part}" for part in ("A", "op", "B"))


GEOMETRY_KEYS = (
    "P01-A", "P01-arrow", "P01-B",
    *(f"P02-{relation}-{part}" for relation in ("lt", "le", "in", "subset")
      for part in ("A", "op", "B")),
    *(f"P03-{fence}-{part}" for fence in ("round", "square", "brace")
      for part in ("open", "A", "B", "close")),
    *(f"P03-angle-{part}" for part in ("open", "A", "B", "close")),
    *(f"P04-{arrow}-{part}" for arrow in ("left", "long", "implies", "iff", "map")
      for part in ("A", "op", "B")),
    "P05-overright", "P05-overleft", "P05-underright", "P05-underleft",
    "P05-widehat", "P05-overline",
    "P06-fraction", "P06-root", "P06-cuberoot", "P06-scripts", "P06-sum",
    *(f"P07-{kind}-{letter}" for kind in ("matrix", "array")
      for letter in ("A", "B", "C", "D")),
    "P08-function", "P08-case-B", *triple_keys("P08-condition-one"),
    "P08-case-D", *triple_keys("P08-condition-two"),
    "P10-premise-one", "P10-premise-two", "P10-conclusion",
    *(key for node in ("root", "left", "right")
      for key in triple_keys(f"P11-{node}")),
    "P12-row-one", "P12-row-two", "P12-row-three",
    "P13-node-one", "P13-node-two", "P13-edge",
    "P14-A", "P14-arrow", "P14-B",
    *(key for pair in ROW_PAIR_IDS for side in ("right", "left")
      for key in triple_keys(f"P15-{pair}-{side}")),
    *(f"P15-{kind}-accent-{side}" for kind in ("over", "under")
      for side in ("right", "left")),
    *(key for alias in ALIAS_IDS for key in triple_keys(f"P15-alias-{alias}")),
    *(key for invariant in INVARIANT_IDS
      for key in triple_keys(f"P15-invariant-{invariant}")),
    "P16-global-function",
    *(key for name in ("global-case-one", "global-case-two",
                       "global-array-one", "global-array-two",
                       "global-tableau-root", "global-tableau-left",
                       "global-tableau-right")
      for key in triple_keys(f"P16-{name}")),
    "P16-local-function", *triple_keys("P16-local-case"),
    *triple_keys("P16-local-array"), *triple_keys("P16-restored-global"),
    "P17-equation-formula", "P17-equation-tag",
    "P17-align-formula", "P17-align-tail", "P17-align-tag",
    "P17-gather-formula", "P17-gather-tag",
    "P17-multline-formula", "P17-multline-tail", "P17-multline-tag",
    "P17-split-formula", "P17-split-tail", "P17-split-tag",
    *(key for pair in ROW_PAIR_IDS for side in ("right", "left")
      for key in triple_keys(f"P18-{pair}-{side}")),
    *(f"P18-{kind}-accent-{side}" for kind in ("over", "under")
      for side in ("right", "left")),
    *(key for alias in ALIAS_IDS for key in triple_keys(f"P18-alias-{alias}")),
    *triple_keys("P18-invariant-models"),
    *(f"P19-fallback-{name}" for name in FALLBACK_IDS),
    *(f"P19-boxed-accent-{name}" for name in BOXED_ACCENT_IDS),
    *(f"P20-fallback-{name}" for name in FALLBACK_IDS),
    *(f"P20-boxed-accent-{name}" for name in BOXED_ACCENT_IDS),
)
GEOMETRY_KEY_SET = set(GEOMETRY_KEYS)
require_unique_geometry_keys = len(GEOMETRY_KEYS) == len(GEOMETRY_KEY_SET)
if not require_unique_geometry_keys:
    raise RuntimeError("duplicate RTL-math geometry key in QA contract")

GLOBAL_TRIPLES = (
    ("P01-A", "P01-arrow", "P01-B"),
    *((f"P02-{relation}-A", f"P02-{relation}-op", f"P02-{relation}-B")
      for relation in ("lt", "le", "in", "subset")),
    *((f"P04-{arrow}-A", f"P04-{arrow}-op", f"P04-{arrow}-B")
      for arrow in ("left", "long", "implies", "iff", "map")),
    *(triple_keys(f"P08-condition-{word}") for word in ("one", "two")),
    *(triple_keys(f"P15-{pair}-{side}") for pair in ROW_PAIR_IDS
      for side in ("right", "left")),
    *(triple_keys(f"P15-alias-{alias}") for alias in ALIAS_IDS),
    *(triple_keys(f"P15-invariant-{invariant}") for invariant in INVARIANT_IDS),
    *(triple_keys(f"P16-{name}") for name in (
        "global-case-one", "global-case-two", "global-array-one",
        "global-array-two", "restored-global")),
)
# Forest/TikZ applies a node transformation after hyperref constructs link
# annotations.  Consequently the three link rectangles inside a node are
# cumulative/transformed rather than per-atom boxes.  Their exact extracted
# operator faces and the parent/child topology remain machine-checked, while
# within-node visual order belongs to the mandatory rendered-page audit.
TRANSFORMED_TABLEAU_TRIPLES = (
    *(triple_keys(f"P11-{node}") for node in ("root", "left", "right")),
    *(triple_keys(f"P16-global-tableau-{node}")
      for node in ("root", "left", "right")),
)
LOCAL_LTR_TRIPLES = (
    ("P14-A", "P14-arrow", "P14-B"),
    triple_keys("P16-local-case"), triple_keys("P16-local-array"),
    *(triple_keys(f"P18-{pair}-{side}") for pair in ROW_PAIR_IDS
      for side in ("right", "left")),
    *(triple_keys(f"P18-alias-{alias}") for alias in ALIAS_IDS),
    triple_keys("P18-invariant-models"),
)
GLOBAL_ROWS = (
    *( (f"P03-{fence}-open", f"P03-{fence}-A", f"P03-{fence}-B",
        f"P03-{fence}-close") for fence in ("round", "square", "brace") ),
    ("P03-angle-open", "P03-angle-close"),
    *( (f"P07-{kind}-A", f"P07-{kind}-B") for kind in ("matrix", "array") ),
    *( (f"P07-{kind}-C", f"P07-{kind}-D") for kind in ("matrix", "array") ),
    ("P08-case-B", "P08-condition-one-A"),
    ("P08-case-D", "P08-condition-two-A"),
)
OUTER_SEQUENCES = (
    ("P05-overright", "P05-overleft", "P05-widehat", "P05-overline"),
    ("P06-fraction", "P06-root", "P06-cuberoot", "P06-scripts", "P06-sum"),
)

EXPECTED_STABLE_TEXT = {
    "P01-A": "A", "P01-B": "B",
    "P03-round-open": "(", "P03-round-close": ")",
    "P03-square-open": "[", "P03-square-close": "]",
    "P03-brace-open": "{", "P03-brace-close": "}",
    "P03-angle-open": "⟨", "P03-angle-close": "⟩",
    "P04-iff-op": "⇔",
    "P14-A": "A", "P14-arrow": "→", "P14-B": "B",
    "P17-equation-tag": "EQ", "P17-align-tag": "AL",
    "P17-gather-tag": "GA", "P17-multline-tag": "MU",
    "P17-split-tag": "SP",
}
for _prefix in (
    *(f"P02-{relation}" for relation in ("lt", "le", "in", "subset")),
    *(f"P03-{fence}" for fence in ("round", "square", "brace", "angle")),
    *(f"P04-{arrow}" for arrow in ("left", "long", "implies", "iff", "map")),
):
    for _letter in ("A", "B"):
        EXPECTED_STABLE_TEXT[f"{_prefix}-{_letter}"] = _letter

FACE_BY_ENDPOINT = {
    "rightarrow": "→", "leftarrow": "←",
    "longrightarrow": "→", "longleftarrow": "←",
    "Rightarrow": "⇒", "Leftarrow": "⇐",
    "Longrightarrow": "⇒", "Longleftarrow": "⇐",
    "xrightarrow": ("α−→", "→−α", "α→", "→α"),
    "xleftarrow": ("α←−", "−←α", "α←", "←α"),
    "xLongrightarrow": ("α==⇒", "⇒==α", "α⇒", "⇒α"),
    "xLongleftarrow": ("α⇐==", "==⇐α", "α⇐", "⇐α"),
    # Composite glyphs can be extracted in content-stream order or visual order
    # under TRT.  Both spellings retain the same visible arrow orientation;
    # accepting both does not accept the converse face.
    "mapsto": ("|→", "→|", "↦"),
    "OLClassicalMapsFrom": ("←|", "|←", "↤"),
    "longmapsto": ("|−→", "→−|", "|→", "→|", "↦"),
    "OLClassicalLongMapsFrom": ("←−|", "|−←", "←|", "|←", "↤"),
    "boxright": ("□→", "→□"), "OLClassicalBoxLeft": ("←□", "□←"),
    "fishhookright": "⥽", "OLClassicalFishhookLeft": "⥼",
    "literal-lt": "<", "literal-gt": ">",
    "leq": "≤", "geq": "≥", "in": "∈", "ni": "∋",
    "prec": "≺", "succ": "≻", "preceq": "⪯", "succeq": "⪰",
    "npreceq": "⋠", "nsucceq": "⋡",
    "preccurlyeq": "≼", "succcurlyeq": "≽",
    "precsim": "≾", "succsim": "≿", "nless": "≮", "ngtr": "≯",
    "lessdot": "⋖", "gtrdot": "⋗",
    "varolessthan": "⧀", "varogreaterthan": "⧁",
    "subset": "⊂", "supset": "⊃", "subseteq": "⊆", "supseteq": "⊇",
    "nsubseteq": "⊈", "nsupseteq": "⊉", "subsetneq": "⊊", "supsetneq": "⊋",
    "sqsubset": "⊏", "sqsupset": "⊐",
    "sqsubseteq": "⊑", "sqsupseteq": "⊒",
    "upharpoonright": "↾", "upharpoonleft": "↿",
    "lhd": ("◁", "⊲"), "rhd": ("▷", "⊳"),
    "ddots": ("⋱", "..."), "iddots": ("⋰", "..."),
    "vdash": "⊢", "dashv": "⊣",
    "models": ("⊨", "|="),
    # The mirrored composite is drawn as =|, but a TRT content stream may
    # expose its two primitive glyphs in source order as |=.  The mandatory
    # rendered-page audit distinguishes that ambiguous extraction spelling.
    "models-mirrored-face": ("⫤", "=|", "|="),
    "overrightarrow": "→", "overleftarrow": "←",
    "underrightarrow": "→", "underleftarrow": "←",
}
OPPOSITE_ENDPOINT = {
    endpoint: opposite
    for _pair_id, right, left, _kind, _atom, _reason in REGISTRY_PAIRS
    for endpoint, opposite in ((right, left), (left, right))
}
OPPOSITE_ENDPOINT.update({
    "models": "models-mirrored-face",
    "models-mirrored-face": "models",
})


def face_options(endpoint: str) -> tuple[str, ...]:
    """Return every accepted extraction spelling for one visible endpoint."""
    value = FACE_BY_ENDPOINT[endpoint]
    return (value,) if isinstance(value, str) else value

# Each value is (control/LTR endpoint, installed-RTL endpoint).  The text in
# these annotations is intentionally the visible presentation, not fabricated
# per-symbol ActualText.  Canonical logical order is bound by the hashed source.
EXPECTED_DIRECTIONAL_ENDPOINTS: dict[str, tuple[str, str]] = {
    "P01-arrow": ("rightarrow", "leftarrow"),
    "P02-lt-op": ("literal-lt", "literal-gt"),
    "P02-le-op": ("leq", "geq"),
    "P02-in-op": ("in", "ni"),
    "P02-subset-op": ("subseteq", "supseteq"),
    "P04-left-op": ("leftarrow", "rightarrow"),
    "P04-long-op": ("longrightarrow", "longleftarrow"),
    "P04-implies-op": ("Rightarrow", "Leftarrow"),
    "P04-map-op": ("mapsto", "OLClassicalMapsFrom"),
    "P05-overright": ("overrightarrow", "overleftarrow"),
    "P05-overleft": ("overleftarrow", "overrightarrow"),
    "P05-underright": ("underrightarrow", "underleftarrow"),
    "P05-underleft": ("underleftarrow", "underrightarrow"),
    "P08-condition-one-op": ("rightarrow", "leftarrow"),
    "P08-condition-two-op": ("in", "ni"),
    "P10-premise-one": ("rightarrow", "leftarrow"),
    "P11-root-op": ("rightarrow", "leftarrow"),
    "P11-left-op": ("in", "ni"),
    "P11-right-op": ("subseteq", "supseteq"),
    "P12-row-one": ("rightarrow", "leftarrow"),
    "P13-node-one": ("rightarrow", "leftarrow"),
    "P13-node-two": ("rightarrow", "leftarrow"),
    "P13-edge": ("rightarrow", "leftarrow"),
    "P16-global-case-one-op": ("rightarrow", "leftarrow"),
    "P16-global-case-two-op": ("subseteq", "supseteq"),
    "P16-global-array-one-op": ("in", "ni"),
    "P16-global-array-two-op": ("leq", "geq"),
    "P16-global-tableau-root-op": ("Rightarrow", "Leftarrow"),
    "P16-global-tableau-left-op": ("prec", "succ"),
    "P16-global-tableau-right-op": ("sqsubseteq", "sqsupseteq"),
    "P16-local-case-op": ("rightarrow", "rightarrow"),
    "P16-local-array-op": ("in", "in"),
    "P16-restored-global-op": ("rightarrow", "leftarrow"),
    "P17-equation-formula": ("rightarrow", "leftarrow"),
    "P17-align-formula": ("in", "ni"),
    "P17-gather-formula": ("subseteq", "supseteq"),
    "P17-multline-formula": ("Rightarrow", "Leftarrow"),
    "P17-split-formula": ("rightarrow", "leftarrow"),
}
for _pair_id, _right, _left, _kind, _atom, _reason in REGISTRY_PAIRS:
    if _kind in {"over-accent", "under-accent"}:
        _stem = "over" if _kind == "over-accent" else "under"
        EXPECTED_DIRECTIONAL_ENDPOINTS[f"P15-{_stem}-accent-right"] = (_right, _left)
        EXPECTED_DIRECTIONAL_ENDPOINTS[f"P15-{_stem}-accent-left"] = (_left, _right)
        EXPECTED_DIRECTIONAL_ENDPOINTS[f"P18-{_stem}-accent-right"] = (_right, _right)
        EXPECTED_DIRECTIONAL_ENDPOINTS[f"P18-{_stem}-accent-left"] = (_left, _left)
    else:
        EXPECTED_DIRECTIONAL_ENDPOINTS[f"P15-{_pair_id}-right-op"] = (_right, _left)
        EXPECTED_DIRECTIONAL_ENDPOINTS[f"P15-{_pair_id}-left-op"] = (_left, _right)
        EXPECTED_DIRECTIONAL_ENDPOINTS[f"P18-{_pair_id}-right-op"] = (_right, _right)
        EXPECTED_DIRECTIONAL_ENDPOINTS[f"P18-{_pair_id}-left-op"] = (_left, _left)
for _alias, _ltr, _rtl in REGISTRY_ALIASES:
    EXPECTED_DIRECTIONAL_ENDPOINTS[f"P15-alias-{_alias}-op"] = (_ltr, _rtl)
    EXPECTED_DIRECTIONAL_ENDPOINTS[f"P18-alias-{_alias}-op"] = (_ltr, _ltr)
EXPECTED_DIRECTIONAL_ENDPOINTS["P15-invariant-models-op"] = (
    "models", "models-mirrored-face")
EXPECTED_DIRECTIONAL_ENDPOINTS["P18-invariant-models-op"] = ("models", "models")

INVARIANT_FACE_OPTIONS = {
    "leftrightarrow": (("↔",), ("←", "→")),
    "longleftrightarrow": (("↔",), ("←", "→")),
    "Leftrightarrow": (("⇔",), ("⇐", "⇒")),
    "Longleftrightarrow": (("⇔",), ("⇐", "⇒")),
    "equiv": (("≡",),), "sim": (("∼",),), "simeq": (("≃",),),
    "approx": (("≈",),), "land": (("∧",),), "lor": (("∨",),),
    "ddots": (("⋱",), ("...",)),
    "iddots": (("⋰",), ("...",)),
    "triangleright": (("▷",), ("⊳",)),
}

# These atoms are deliberately boxed in a complete local-TLT math list when
# the surrounding Classical formula is TRT.  Their visible extraction must be
# identical in control, global-RTL, and explicit local-LTR probes: this is a
# preservation contract, not a guessed converse.
PRESERVED_FACE_KEYS = tuple(
    f"P{probe}-{kind}-{name}"
    for probe in (19, 20)
    for kind, names in (("fallback", FALLBACK_IDS),
                        ("boxed-accent", BOXED_ACCENT_IDS))
    for name in names
)

EXPECTED_LOGICAL_MINIMUM = {
    "P01": Counter(A=1, B=1),
    "P02": Counter(A=4, B=4),
    "P03": Counter(A=4, B=4),
    "P04": Counter(A=5, B=5),
    "P05": Counter(A=4, B=4),
    "P06": Counter(A=5, B=4),
    "P07": Counter(A=2, B=2, C=2, D=2),
    "P08": Counter(A=3, B=3, D=1, f=1),
    "P09": Counter(P=1),
    "P10": Counter(A=2, B=2),
    "P11": Counter(A=3, B=3),
    "P12": Counter(A=2, B=2),
    "P13": Counter(A=2, B=3, C=1, f=1),
    "P14": Counter(A=1, B=1),
    "P15": Counter(A=60, B=60),
    "P16": Counter(A=15, B=12, f=1, g=1),
    "P17": Counter(A=5, B=5),
    "P18": Counter(A=50, B=50),
    "P19": Counter(A=13, B=13),
    "P20": Counter(A=13, B=13),
}
LOGICAL_SYMBOLS = set(
    "<>=+−-/|¬∨∧∈∉∋⊂⊃⊆⊇⊈⊉⊊⊋⊏⊐⊑⊒"
    "≤≥≺≻≼≽⪯⪰⋠⋡≾≿≮≯⋖⋗⧀⧁"
    "⊢⊣⊨⊬⊭⊩⊮⫤→←⇒⇐⇔↔↦↤↾↿⥽⥼□"
    "◁▷⊲⊳∢≡∼≃≈()[]{}⟨⟩:."
)


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def integer(value: object, minimum: int = 0) -> bool:
    return type(value) is int and value >= minimum


def digest(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9A-F]{64}", value) is not None


def sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest().upper()


def strict_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=strict_object)
    require(type(value) is dict, f"JSON root must be an object: {path}")
    return value


def utc(value: object) -> datetime:
    require(isinstance(value, str), "missing lifecycle timestamp")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(result.tzinfo is not None, "lifecycle timestamp lacks timezone")
    return result.astimezone(timezone.utc)


def same_path(one: object, two: object) -> bool:
    if not isinstance(one, (str, os.PathLike)) or not isinstance(two, (str, os.PathLike)):
        return False
    return os.path.normcase(str(Path(one).resolve())) == os.path.normcase(str(Path(two).resolve()))


def exact_keys(value: object, expected: set[str], label: str) -> None:
    require(type(value) is dict and set(value) == expected, f"{label} schema")


def validate_identity(record: object, path: Path, recorded_path: str, label: str) -> dict:
    exact_keys(record, {"Path", "Bytes", "SHA256"}, label)
    assert isinstance(record, dict)
    require(record["Path"] == recorded_path, f"{label} path")
    require(integer(record["Bytes"], 0) and record["Bytes"] == path.stat().st_size,
            f"{label} byte count")
    require(digest(record["SHA256"]) and record["SHA256"] == sha256(path),
            f"{label} hash")
    return record


def validate_manifest(directory: Path, repo: Path) -> dict:
    manifest_path = directory / "BUILD_MANIFEST.json"
    value = read_json(manifest_path)
    exact_keys(value, {
        "Schema", "Status", "StartedAtUtc", "FinishedAtUtc", "OutputDirectory",
        "WorkingDirectory", "Engine", "GuardInvocation", "Environment",
        "MaximumPasses", "RequiredProducts", "ConvergenceState",
        "InputsCapturedAtUtc", "Inputs", "Jobs",
    }, "build manifest")
    require(value["Schema"] == BUILD_SCHEMA and value["Status"] == "PASS",
            "build manifest did not pass")
    require(same_path(value["OutputDirectory"], directory), "build output directory binding")
    expected_working = repo / "source/locale/ar"
    require(same_path(value["WorkingDirectory"], expected_working), "build working directory")
    started, captured, finished = (utc(value[key]) for key in
                                   ("StartedAtUtc", "InputsCapturedAtUtc", "FinishedAtUtc"))
    require(started <= captured <= finished, "build manifest lifecycle ordering")
    require(value["MaximumPasses"] == 4 and type(value["MaximumPasses"]) is int,
            "build pass limit")
    require(value["RequiredProducts"] == list(REQUIRED_PRODUCTS), "required-product contract")
    require(value["ConvergenceState"] == list(CONVERGENCE_STATE), "convergence-state contract")
    require(value["Environment"] == {
        "SOURCE_DATE_EPOCH": "1783874174", "FORCE_SOURCE_DATE": "1",
        "TZ": "UTC", "TEXINPUTS": f"{directory};",
        "TEMP": str(directory), "TMP": str(directory),
        "TEXMFCACHE": str(directory / "texmf-cache"),
    }, "deterministic environment")

    engine = value["Engine"]
    exact_keys(engine, {"Path", "Bytes", "SHA256"}, "engine identity")
    engine_path = Path(engine["Path"])
    require(engine_path.is_absolute() and engine_path.is_file(), "engine path")
    validate_identity(engine, engine_path, str(engine["Path"]), "engine identity")

    guard_invocation = value["GuardInvocation"]
    exact_keys(guard_invocation, {"Command", "Arguments", "WorkingDirectory"},
               "guard invocation")
    build_script = repo / "tmp/pdfs/classical-rtl-math-probe/BUILD_PROBE.ps1"
    expected_arguments = ["-NoProfile", "-File", str(build_script),
                          "-OutputDirectory", str(directory)]
    require(Path(guard_invocation["Command"]).is_absolute(), "guard command path")
    require(guard_invocation["Arguments"] == expected_arguments, "guard command arguments")
    require(isinstance(guard_invocation["WorkingDirectory"], str) and
            Path(guard_invocation["WorkingDirectory"]).is_absolute(),
            "guard working directory")

    inputs = value["Inputs"]
    require(type(inputs) is list and [item.get("Path") if isinstance(item, dict) else None
                                      for item in inputs] == list(DIRECT_INPUTS),
            "build input inventory")
    for item, relative in zip(inputs, DIRECT_INPUTS, strict=True):
        validate_identity(item, repo / relative, relative, f"build input {relative}")

    jobs = value["Jobs"]
    exact_keys(jobs, {"control", "rtl"}, "build jobs")
    for job in ("control", "rtl"):
        record = jobs[job]
        exact_keys(record, {"Source", "Arguments", "Passes", "Converged",
                            "StablePass", "Outputs"}, f"{job} build job")
        source = repo / f"tmp/pdfs/classical-rtl-math-probe/{job}.tex"
        expected_arguments = [
            "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
            "-recorder", f"-output-directory={directory}", str(source),
        ]
        require(same_path(record["Source"], source) and
                record["Arguments"] == expected_arguments,
                f"{job} exact engine arguments")
        require(record["Converged"] is True and integer(record["StablePass"], 2) and
                record["StablePass"] <= value["MaximumPasses"], f"{job} convergence")
        passes = record["Passes"]
        require(type(passes) is list and len(passes) == record["StablePass"] and
                [item.get("Pass") if isinstance(item, dict) else None for item in passes]
                == list(range(1, record["StablePass"] + 1)), f"{job} pass sequence")
        for index, pass_record in enumerate(passes, 1):
            exact_keys(pass_record, {"Pass", "ExitCode", "Terminal", "Log",
                                     "Diagnostics", "StateFingerprint"},
                       f"{job} pass {index}")
            require(type(pass_record["ExitCode"]) is int and pass_record["ExitCode"] == 0,
                    f"{job} pass {index} exit")
            validate_identity(pass_record["Terminal"],
                              directory / f"{job}-pass-{index}.terminal.txt",
                              f"{job}-pass-{index}.terminal.txt",
                              f"{job} pass {index} terminal")
            validate_identity(pass_record["Log"], directory / f"{job}-pass-{index}.log",
                              f"{job}-pass-{index}.log", f"{job} pass {index} log")
            diagnostics = pass_record["Diagnostics"]
            require(type(diagnostics) is list and len(diagnostics) == len(set(diagnostics)) and
                    all(isinstance(item, str) and item in KNOWN_DIAGNOSTICS
                        for item in diagnostics), f"{job} pass {index} diagnostics")
            fingerprint = pass_record["StateFingerprint"]
            require(isinstance(fingerprint, str) and re.fullmatch(
                r"(?:aux|out|toc|lof|lot|loe)=[0-9A-F]{64}"
                r"(?:;(?:aux|out|toc|lof|lot|loe)=[0-9A-F]{64})+", fingerprint),
                f"{job} pass {index} convergence fingerprint")
        require(passes[-1]["StateFingerprint"] == passes[-2]["StateFingerprint"],
                f"{job} final states are not stable")
        require(passes[-1]["Diagnostics"] == [], f"{job} final diagnostics are not empty")

        expected_outputs = [f"{job}.{suffix}" for suffix in REQUIRED_PRODUCTS]
        expected_outputs += [f"{job}.{suffix}" for suffix in CONVERGENCE_STATE
                             if suffix not in ("aux", "out") and
                             (directory / f"{job}.{suffix}").is_file()]
        outputs = record["Outputs"]
        require(type(outputs) is list and
                [item.get("Path") if isinstance(item, dict) else None for item in outputs]
                == expected_outputs, f"{job} output inventory")
        for item, name in zip(outputs, expected_outputs, strict=True):
            validate_identity(item, directory / name, name, f"{job} output {name}")
    return value


def validate_guard(path: Path, manifest: dict) -> dict:
    value = read_json(path)
    exact_keys(value, {
        "Schema", "Mutex", "Acquired", "AbandonedMutexRecovered", "StartedAtUtc",
        "Status", "Containment", "OutputTransport", "AcquiredAtUtc", "Command",
        "WorkingDirectory", "Tree", "FinishedAtUtc", "ExitCode",
    }, "guard receipt")
    require(value["Schema"] == GUARD_SCHEMA and value["Mutex"] == MUTEX_NAME,
            "guard identity")
    require(value["Status"] == "PASS" and value["Acquired"] is True,
            "guard did not pass")
    require(type(value["AbandonedMutexRecovered"]) is bool,
            "abandoned-mutex observation type")
    require(type(value["ExitCode"]) is int and value["ExitCode"] == 0,
            "guard exit code")
    require(value["Containment"] == CONTAINMENT and
            value["OutputTransport"] == OUTPUT_TRANSPORT, "guard containment/transport")
    require(same_path(value["Command"], manifest["GuardInvocation"]["Command"]) and
            same_path(value["WorkingDirectory"],
                      manifest["GuardInvocation"]["WorkingDirectory"]),
            "guard command/working-directory binding")

    tree = value["Tree"]
    exact_keys(tree, {
        "RootProcessId", "AssignedBeforeResume", "CreatedSuspendedAtUtc",
        "ResumedAtUtc", "RootExitedAtUtc", "RootExitCode", "TreeEmptyAtUtc",
        "FinalActiveProcesses", "TotalProcesses", "PeakObservedActiveProcesses",
        "TerminationRequested", "TerminationRequestedAtUtc", "JobClosedAtUtc",
        "DrainVerified",
    }, "guard tree")
    require(tree["AssignedBeforeResume"] is True and tree["DrainVerified"] is True,
            "guard tree assignment/drain")
    require(type(tree["RootExitCode"]) is int and tree["RootExitCode"] == 0,
            "guard root exit")
    require(type(tree["FinalActiveProcesses"]) is int and
            tree["FinalActiveProcesses"] == 0, "guard tree not empty")
    require(tree["TerminationRequested"] is False and
            tree["TerminationRequestedAtUtc"] is None, "guard termination")
    require(integer(tree["RootProcessId"], 1) and integer(tree["TotalProcesses"], 1) and
            integer(tree["PeakObservedActiveProcesses"], 1) and
            tree["PeakObservedActiveProcesses"] <= tree["TotalProcesses"],
            "guard process accounting")
    lifecycle = [utc(value["StartedAtUtc"]), utc(value["AcquiredAtUtc"]),
                 utc(tree["CreatedSuspendedAtUtc"]), utc(tree["ResumedAtUtc"]),
                 utc(tree["RootExitedAtUtc"]), utc(tree["TreeEmptyAtUtc"]),
                 utc(tree["JobClosedAtUtc"]), utc(value["FinishedAtUtc"])]
    require(lifecycle == sorted(lifecycle), "guard lifecycle ordering")
    require(lifecycle[0] <= utc(manifest["StartedAtUtc"]) <=
            utc(manifest["FinishedAtUtc"]) <= lifecycle[-1],
            "build lifecycle is outside guard")
    return value


def bind_guard_file_times(directory: Path, manifest: dict, guard: dict) -> None:
    lower = utc(guard["StartedAtUtc"]).timestamp() - 2
    upper = utc(guard["FinishedAtUtc"]).timestamp() + 2
    paths = [directory / "BUILD_MANIFEST.json"]
    for job in ("control", "rtl"):
        paths.extend(directory / item["Path"] for item in manifest["Jobs"][job]["Outputs"])
        for pass_record in manifest["Jobs"][job]["Passes"]:
            paths.extend((directory / pass_record["Terminal"]["Path"],
                          directory / pass_record["Log"]["Path"]))
    for path in paths:
        require(lower <= path.stat().st_mtime <= upper,
                f"build member outside guard lifecycle: {path.name}")


def unwrap_tex_typeout_records(log: str, prefix: str) -> str:
    """Recover exact prefixed typeout records wrapped at TeX's 79 columns."""
    lines = log.splitlines()
    records: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.startswith(prefix):
            index += 1
            continue
        record = line
        while len(lines[index]) == 79 and index + 1 < len(lines):
            index += 1
            record += lines[index]
        records.append(record)
        index += 1
    return "\n".join(records)


def direction_trace(log: str, job: str) -> dict[str, dict[str, int]]:
    trace_lines = re.findall(r"^OLC-RTL-DIRECTION=[^\r\n]*$", log, flags=re.MULTILINE)
    parsed: list[tuple[str, int, int]] = []
    for line in trace_lines:
        match = re.fullmatch(
            r"OLC-RTL-DIRECTION=([a-z-]+);primitive=(\d+);desired=(\d+)", line)
        require(match is not None, f"{job} malformed direction trace")
        parsed.append((match.group(1), int(match.group(2)), int(match.group(3))))
    if job == "rtl":
        expected = [
            ("begin-document", 1, 1), ("inside-local-ltr-scope", 0, 0),
            ("after-local-ltr-scope", 1, 1),
            ("inside-local-ltr-nested-scope", 0, 0),
            ("after-local-ltr-nested-scope", 1, 1),
            ("inside-local-ltr-registry-scope", 0, 0),
            ("after-local-ltr-registry-scope", 1, 1),
            ("end-document", 1, 1),
        ]
    else:
        expected = [
            ("begin-document", 0, 0), ("inside-local-ltr-scope", 0, 0),
            ("after-local-ltr-scope", 0, 0),
            ("inside-local-ltr-nested-scope", 0, 0),
            ("after-local-ltr-nested-scope", 0, 0),
            ("inside-local-ltr-registry-scope", 0, 0),
            ("after-local-ltr-registry-scope", 0, 0),
            ("end-document", 0, 0),
        ]
    require(parsed == expected, f"{job} direction trace is missing, duplicated, or out of order")
    require(len(re.findall(rf"^{re.escape(SOURCE_SIGNATURE)}$", log, flags=re.MULTILINE)) == 1,
            f"{job} exact source signature")
    forbidden = (
        "Missing character:", "Overfull \\hbox", "Overfull \\vbox",
        "There were undefined references", "There were undefined citations",
        "Label(s) may have changed", "Rerun to get", "rerunfilecheck Warning",
        "multiply defined", "destination with the same identifier",
        "Undefined control sequence", "Emergency stop", "Fatal error occurred",
    )
    require(not any(marker in log for marker in forbidden), f"{job} unresolved final log diagnostic")
    require("Output written on" in log, f"{job} incomplete log")
    install = "OL-CLASSICAL-RTL-MATH=native-mathdirection-TRT"
    source_order = "OL-CLASSICAL-RTL-MATH-SOURCE-ORDER=unchanged"
    if job == "rtl":
        require(log.count(install) == 1 and log.count(source_order) == 1,
                "RTL install/source-order marker")
        expected_pairs = [(right, left, kind, atom, reason)
                          for _identifier, right, left, kind, atom, reason
                          in REGISTRY_PAIRS]
        registry_log = unwrap_tex_typeout_records(log, "OLC-RTL-REGISTRY")
        actual_pairs = re.findall(
            r"^OLC-RTL-REGISTRY-PAIR=([^/\r\n]+)/([^/\r\n]+)/"
            r"([^/\r\n]+)/([^/\r\n]+)/([^\r\n]+)$",
            registry_log, flags=re.MULTILINE)
        require(actual_pairs == expected_pairs, "RTL typed-pair log inventory/order")
        actual_aliases = re.findall(
            r"^OLC-RTL-REGISTRY-ALIAS=([^/\r\n]+)/([^/\r\n]+)/([^\r\n]+)$",
            registry_log, flags=re.MULTILINE)
        require(actual_aliases == list(REGISTRY_ALIASES), "RTL alias log inventory/order")
        actual_invariants = re.findall(
            r"^OLC-RTL-REGISTRY-INVARIANT=([^/\r\n]+)/([^\r\n]+)$",
            registry_log, flags=re.MULTILINE)
        require(actual_invariants == list(REGISTRY_INVARIANTS),
                "RTL invariant log inventory/order")
        actual_fallbacks = re.findall(
            r"^OLC-RTL-REGISTRY-FALLBACK=([^/\r\n]+)/([^/\r\n]+)/"
            r"([^/\r\n]+)/([^\r\n]+)$",
            registry_log, flags=re.MULTILINE)
        require(actual_fallbacks == list(REGISTRY_FALLBACKS),
                "RTL fallback log inventory/order")
        actual_boxed_accents = re.findall(
            r"^OLC-RTL-REGISTRY-BOXED-ACCENT=([^/\r\n]+)/"
            r"([^/\r\n]+)/([^\r\n]+)$",
            registry_log, flags=re.MULTILINE)
        require(actual_boxed_accents == list(REGISTRY_BOXED_ACCENTS),
                "RTL boxed-accent log inventory/order")
        for marker, count in (
            ("OLC-RTL-REGISTRY=typed-coverage-v5", 1),
            ("OLC-RTL-REGISTRY-COUNTS=pairs-32;aliases-6;invariants-14;"
             "fallbacks-9;boxed-accents-13", 1),
            ("OLC-RTL-MATH-LIST-HOOKS=everymath+everydisplay-tail-v1", 1),
            ("OLC-RTL-MLIST-CALLBACK=installed-once", 1),
            ("OLC-RTL-MLIST-CALLBACK-OWNERSHIP=PASS", 3),
            ("OLC-RTL-OWNERSHIP=PASS", 3),
            ("OL-CLASSICAL-RTL-MATH-MIRRORING=typed-registry-and-scoped-ltr-v5", 1),
            ("OL-CLASSICAL-RTL-MATH-NONDIRECTIONAL-ACCENTS=boxed-registry-v3", 1),
            ("OL-CLASSICAL-RTL-MATH-TAGS=physical-left-v1", 1),
        ):
            marker_log = registry_log if marker.startswith("OLC-RTL-REGISTRY") else log
            require(marker_log.count(marker) == count,
                    f"RTL owner marker count {marker}")
    else:
        require(install not in log and source_order not in log,
                 "RTL layer leaked into control")
        require("OLC-RTL-REGISTRY" not in log and
                "OLC-RTL-MLIST-CALLBACK" not in log and
                "OLC-RTL-MATH-LIST-HOOKS" not in log,
                "RTL registry/list owner leaked into control")
    return {name: {"primitive": primitive, "desired": desired}
            for name, primitive, desired in parsed}


def parse_pdffonts(output: str, pdf_name: str) -> list[dict]:
    rows: list[dict] = []
    for line in output.splitlines():
        if not line.strip() or line.lstrip().startswith(("name", "---")):
            continue
        match = re.fullmatch(
            r"\s*(?P<descriptor>.+?)\s+(?P<embedded>yes|no)\s+"
            r"(?P<subset>yes|no)\s+(?P<unicode>yes|no)\s+"
            r"(?P<object>\d+)\s+(?P<generation>\d+)\s*", line,
        )
        require(match is not None, f"unparseable pdffonts row in {pdf_name}: {line}")
        descriptor = re.split(r"\s{2,}", match.group("descriptor").strip(), maxsplit=2)
        require(len(descriptor) == 3 and all(descriptor),
                f"ambiguous pdffonts descriptor in {pdf_name}: {line}")
        rows.append({
            "name": descriptor[0], "type": descriptor[1], "encoding": descriptor[2],
            "embedded": match.group("embedded"), "subset": match.group("subset"),
            "unicode": match.group("unicode"), "object": int(match.group("object")),
            "generation": int(match.group("generation")),
        })
    require(rows, f"no fonts reported for {pdf_name}")
    require(all(row["embedded"] == "yes" for row in rows),
            f"unembedded font in {pdf_name}")
    require(all(row["unicode"] == "yes" for row in rows),
            f"font without ToUnicode in {pdf_name}")
    names = [re.sub(r"^[A-Z]{6}\+", "", row["name"], flags=re.ASCII).casefold()
             for row in rows]
    require(any(name.startswith("scheherazade") for name in names),
            f"Scheherazade Arabic font missing from {pdf_name}")
    return rows


def pdffonts_version() -> str:
    completed = subprocess.run(["pdffonts", "-v"], check=True, capture_output=True,
                               text=True, encoding="utf-8", errors="strict")
    lines = [line.strip() for line in (completed.stdout + completed.stderr).splitlines()
             if line.strip()]
    require(lines, "pdffonts version unavailable")
    return lines[0]


def font_facts(pdf: Path) -> list[dict]:
    command = subprocess.run(["pdffonts", str(pdf)], check=True, capture_output=True,
                             text=True, encoding="utf-8", errors="strict")
    return parse_pdffonts(command.stdout, pdf.name)


def logical_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text)
    return "".join(char for char in normalized
                   if char.isalnum() or char in LOGICAL_SYMBOLS)


def rectangle(annotation: object, media: list[float], label: str) -> list[float]:
    require(annotation is not None and len(annotation) == 4, f"missing link rectangle: {label}")
    rect = [float(value) for value in annotation]
    require(all(float("-inf") < value < float("inf") for value in rect),
            f"non-finite link rectangle: {label}")
    require(rect[0] >= media[0] and rect[1] >= media[1] and
            rect[2] <= media[2] and rect[3] <= media[3] and
            rect[2] > rect[0] and rect[3] > rect[1],
            f"outside/empty link rectangle: {label}")
    return rect


def link_text(page: object, rect: list[float], prefer_midline: bool = False) -> str:
    selected: list[str] = []
    rect_midline = (rect[1] + rect[3]) / 2
    # Prefer glyphs whose drawn boxes cross the annotation's own vertical
    # midline.  Tall legacy symbols can make a link rectangle overlap the next
    # table row even though that row is not part of the link; centre-only
    # selection would then contaminate the operator spelling.
    if prefer_midline:
        for char in page.chars:
            x = (float(char["x0"]) + float(char["x1"])) / 2
            if (rect[0] - 0.5 <= x <= rect[2] + 0.5 and
                    float(char["y0"]) - 0.5 <= rect_midline <= float(char["y1"]) + 0.5):
                selected.append(str(char.get("text", "")))
        value = logical_text("".join(selected))
        if value:
            return value
        selected = []
    for char in page.chars:
        x = (float(char["x0"]) + float(char["x1"])) / 2
        y = (float(char["y0"]) + float(char["y1"])) / 2
        if rect[0] - 0.5 <= x <= rect[2] + 0.5 and rect[1] - 0.5 <= y <= rect[3] + 0.5:
            selected.append(str(char.get("text", "")))
    value = logical_text("".join(selected))
    if value:
        return value
    # A few Type 1 symbols (notably stmaryrd's deep var-order glyphs) draw
    # partly inside the hyperlink rectangle while their glyph-box centre lies
    # just below it.  Fall back only when the centre-based selection is empty,
    # and still require horizontal centring plus actual vertical intersection.
    for char in page.chars:
        x = (float(char["x0"]) + float(char["x1"])) / 2
        vertical_overlap = min(float(char["y1"]), rect[3]) - max(
            float(char["y0"]), rect[1])
        if rect[0] - 0.5 <= x <= rect[2] + 0.5 and vertical_overlap > 0:
            selected.append(str(char.get("text", "")))
    return logical_text("".join(selected))


def region_facts(document: object, pdf_name: str) -> tuple[dict, dict[str, str]]:
    observations: dict[str, tuple[int, dict]] = {}
    for page_number, page in enumerate(document.pages, 1):
        for word in page.extract_words(use_text_flow=True, keep_blank_chars=False):
            if word.get("text") in PROBE_IDS:
                probe = word["text"]
                require(probe not in observations, f"duplicate extracted marker {probe}: {pdf_name}")
                observations[probe] = (page_number, word)
    require(set(observations) == set(PROBE_IDS), f"missing/unknown extracted markers: {pdf_name}")
    observed_positions = [
        (observations[probe][0], float(observations[probe][1]["top"]))
        for probe in PROBE_IDS
    ]
    require(observed_positions == sorted(observed_positions),
            f"probe marker order across pages: {pdf_name}")
    facts: dict[str, dict] = {}
    raw: dict[str, str] = {}
    for index, probe in enumerate(PROBE_IDS):
        page_number, marker = observations[probe]
        require(page_number == PAGE_BY_PROBE[probe],
                f"probe marker page drift for {probe}: {pdf_name}")
        top = float(marker["top"]) - 1
        if index + 1 < len(PROBE_IDS):
            end_page, next_marker = observations[PROBE_IDS[index + 1]]
            bottom = float(next_marker["top"]) - 1
        else:
            end_page = len(document.pages)
            bottom = float(document.pages[end_page - 1].height)
        require(end_page >= page_number,
                f"backward probe region for {probe}: {pdf_name}")
        chars: list[str] = []
        for region_page_number in range(page_number, end_page + 1):
            page = document.pages[region_page_number - 1]
            page_top = top if region_page_number == page_number else 0.0
            page_bottom = bottom if region_page_number == end_page else float(page.height)
            chars.extend(
                str(char.get("text", "")) for char in page.chars
                if page_top <= (float(char["top"]) + float(char["bottom"])) / 2 < page_bottom
            )
        signature = logical_text("".join(chars))
        require(signature.count(probe) == 1, f"region marker identity {probe}: {pdf_name}")
        counts = Counter(signature)
        for token, minimum in EXPECTED_LOGICAL_MINIMUM[probe].items():
            require(counts[token] >= minimum,
                    f"logical extraction lacks {token} for {probe}: {pdf_name}")
        raw[probe] = signature
        facts[probe] = {
            "page": page_number,
            "end_page": end_page,
            "logical_characters": len(signature),
            "logical_sha256": hashlib.sha256(signature.encode("utf-8")).hexdigest().upper(),
            "required_token_counts": {
                token: counts[token] for token in EXPECTED_LOGICAL_MINIMUM[probe]
            },
            "region_top": top,
            "region_bottom": bottom,
        }
    return facts, raw


def center(anchor: dict) -> tuple[float, float]:
    rect = anchor["rect"]
    return ((rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2)


def strictly_ordered(values: list[float], ascending: bool) -> bool:
    pairs = zip(values, values[1:])
    return all(one < two if ascending else one > two for one, two in pairs)


def validate_directional_faces(anchors: dict[str, dict], job: str) -> None:
    index = 0 if job == "control" else 1
    for key, endpoints in EXPECTED_DIRECTIONAL_ENDPOINTS.items():
        endpoint = endpoints[index]
        expected = face_options(endpoint)
        text = anchors[key]["logical_text"]
        require(any(option in text for option in expected),
                f"{job} directional face {key}: expected {endpoint}/{expected!r}, got {text!r}")
        opposite = face_options(OPPOSITE_ENDPOINT[endpoint])
        unambiguous_opposites = tuple(option for option in opposite if option not in expected)
        require(not any(option in text for option in unambiguous_opposites),
                f"{job} double/opposite directional face {key}: {text!r}")


def validate_invariant_faces(anchors: dict[str, dict], job: str) -> None:
    for name, options in INVARIANT_FACE_OPTIONS.items():
        key = f"P15-invariant-{name}-op"
        text = anchors[key]["logical_text"]
        require(any(all(character in text for character in option) for option in options),
                f"{job} invariant face {key}: {text!r}")


def validate_tag_policy(anchors: dict[str, dict], job: str) -> dict:
    groups = {
        "equation": ("P17-equation-tag", ("P17-equation-formula",)),
        "align": ("P17-align-tag", ("P17-align-formula", "P17-align-tail")),
        "gather": ("P17-gather-tag", ("P17-gather-formula",)),
        "multline": ("P17-multline-tag", ("P17-multline-formula", "P17-multline-tail")),
        "split": ("P17-split-tag", ("P17-split-formula", "P17-split-tail")),
    }
    facts = {}
    for family, (tag_key, formula_keys) in groups.items():
        tag = anchors[tag_key]["rect"]
        formulas = [anchors[key]["rect"] for key in formula_keys]
        physical_side = ("left" if tag[2] < min(rect[0] for rect in formulas)
                         else "right" if tag[0] > max(rect[2] for rect in formulas)
                         else "overlap")
        tag_y = (tag[1] + tag[3]) / 2
        require(min(rect[1] for rect in formulas) - 3 <= tag_y <=
                max(rect[3] for rect in formulas) + 3,
                f"{job} {family} tag baseline outside formula block")
        if job == "rtl":
            require(physical_side == "left",
                    f"RTL {family} tag is not on the physical left")
        facts[family] = {"physical_side": physical_side, "tag": tag_key,
                         "formula_anchors": list(formula_keys)}
    return facts


def validate_geometry(anchors: dict[str, dict], job: str) -> dict:
    require(set(anchors) == GEOMETRY_KEY_SET, f"{job} geometry-key inventory")
    outer_ltr = job == "control"
    for keys in GLOBAL_TRIPLES:
        require(strictly_ordered([center(anchors[key])[0] for key in keys], outer_ltr),
                 f"{job} geometry order {'/'.join(keys)}")
    for keys in TRANSFORMED_TABLEAU_TRIPLES:
        pages = {anchors[key]["page"] for key in keys}
        require(len(pages) == 1,
                f"{job} transformed tableau node split across pages: {'/'.join(keys)}")
    for keys in LOCAL_LTR_TRIPLES:
        require(strictly_ordered([center(anchors[key])[0] for key in keys], True),
                f"{job} local-LTR geometry order {'/'.join(keys)}")
    for keys in GLOBAL_ROWS:
        require(strictly_ordered([center(anchors[key])[0] for key in keys], outer_ltr),
                 f"{job} geometry order {'/'.join(keys)}")
    for keys in OUTER_SEQUENCES:
        require(strictly_ordered([center(anchors[key])[0] for key in keys], outer_ltr),
                f"{job} sequence geometry {'/'.join(keys)}")
    require(center(anchors["P03-angle-A"])[1] > center(anchors["P03-angle-B"])[1],
            f"{job} fraction vertical roles")
    for kind in ("matrix", "array"):
        require(center(anchors[f"P07-{kind}-A"])[1] > center(anchors[f"P07-{kind}-C"])[1] and
                center(anchors[f"P07-{kind}-B"])[1] > center(anchors[f"P07-{kind}-D"])[1],
                f"{job} {kind} row geometry")
    require((center(anchors["P07-matrix-A"])[0] < center(anchors["P07-array-A"])[0])
            == outer_ltr, f"{job} matrix/array outer order")
    require(center(anchors["P08-case-B"])[1] > center(anchors["P08-case-D"])[1] and
            center(anchors["P08-condition-one-A"])[1] >
            center(anchors["P08-condition-two-A"])[1], f"{job} cases vertical roles")
    require((center(anchors["P08-function"])[0] < center(anchors["P08-case-B"])[0])
            == outer_ltr, f"{job} function/cases outer order")
    require(center(anchors["P10-premise-one"])[1] > center(anchors["P10-conclusion"])[1] and
            center(anchors["P10-premise-two"])[1] > center(anchors["P10-conclusion"])[1] and
            center(anchors["P10-premise-one"])[0] != center(anchors["P10-premise-two"])[0],
            f"{job} proof-tree geometry")
    require(center(anchors["P11-root-A"])[1] > center(anchors["P11-left-A"])[1] and
            center(anchors["P11-root-A"])[1] > center(anchors["P11-right-A"])[1] and
            center(anchors["P11-left-A"])[0] != center(anchors["P11-right-A"])[0],
            f"{job} tableau geometry")
    require(strictly_ordered([center(anchors[key])[1] for key in
                              ("P12-row-one", "P12-row-two", "P12-row-three")], False),
            f"{job} derivation row geometry")
    node_one = center(anchors["P13-node-one"])
    node_two = center(anchors["P13-node-two"])
    edge = center(anchors["P13-edge"])
    require(node_one[0] < node_two[0] and node_one[0] < edge[0] < node_two[0] and
            edge[1] > min(node_one[1], node_two[1]), f"{job} non-mirrored TikZ geometry")
    validate_directional_faces(anchors, job)
    validate_invariant_faces(anchors, job)
    tag_policy = validate_tag_policy(anchors, job)
    return {
        "all_probe_regions_covered": True,
        "outer_direction": "LTR" if outer_ltr else "RTL",
        "local_scope_direction": "LTR",
        "tikz_coordinates_not_mirrored": True,
        "structural_vertical_roles_preserved": True,
        "transformed_tableau_nodes_checked_by_face_topology_and_visual_audit":
            len(TRANSFORMED_TABLEAU_TRIPLES),
        "directional_faces_checked": len(EXPECTED_DIRECTIONAL_ENDPOINTS),
        "invariant_faces_checked": len(INVARIANT_FACE_OPTIONS),
        "display_tag_policy": tag_policy,
    }


def destination_name(value: object) -> str:
    if hasattr(value, "get_object"):
        value = value.get_object()
    require(isinstance(value, (str, pypdf.generic.TextStringObject,
                               pypdf.generic.NameObject)), "GoTo target is not named")
    return str(value).lstrip("/")


def visible_semantic_checks(document, anchors: dict[str, dict], job: str) -> list[dict]:
    """Check actual glyph positions, not transformed tableau link-box order.

    Unlike the historical v6 geometry contract, both the delimiter face and
    within-node operand order are mandatory. This remains a bounded probe,
    not complete reader or unanchored radical/sized-delimiter acceptance.
    """
    pairs = {'round': ('(', ')'), 'square': ('[', ']'),
             'brace': ('{', '}'), 'angle': ('⟨', '⟩')}
    operators = {'P11-root': ('→', '←'), 'P11-left': ('∈', '∋'),
                 'P11-right': ('⊆', '⊇'), 'P16-global-tableau-root': ('⇒', '⇐'),
                 'P16-global-tableau-left': ('≺', '≻'),
                 'P16-global-tableau-right': ('⊑', '⊒')}
    rtl = job == 'rtl'
    require(job in ('control', 'rtl'), 'Unknown visible semantic job')

    def glyphs(page, rect):
        x0, y0, x1, y1 = rect
        top, bottom = float(page.height) - y1, float(page.height) - y0
        return [(c['text'], (c['x0'] + c['x1']) / 2) for c in page.chars
                if not c['text'].isspace()
                and x0 <= (c['x0'] + c['x1']) / 2 <= x1
                and top <= (c['top'] + c['bottom']) / 2 <= bottom]

    checks = []
    for family, pair in pairs.items():
        for index, role in enumerate(('open', 'close')):
            key = f'P03-{family}-{role}'
            anchor = anchors[key]
            actual = ''.join(c for c, _x in glyphs(document.pages[anchor['page'] - 1], anchor['rect']))
            expected = pair[1 - index if rtl else index]
            checks.append({'key': key, 'kind': 'inward-facing-delimiter',
                           'observed': actual, 'expected': expected, 'pass': actual == expected})
    for prefix, pair in operators.items():
        region = [anchors[prefix + '-' + suffix] for suffix in ('A', 'op', 'B')]
        require(len({r['page'] for r in region}) == 1, 'Tableau node crosses pages')
        rect = [min(r['rect'][0] for r in region), min(r['rect'][1] for r in region),
                max(r['rect'][2] for r in region), max(r['rect'][3] for r in region)]
        chars = glyphs(document.pages[region[0]['page'] - 1], rect)
        actual = ''.join(c for c, _x in sorted(chars, key=lambda c: c[1]))
        expected = 'B' + pair[1] + 'A' if rtl else 'A' + pair[0] + 'B'
        distinct = len({x for _c, x in chars}) == 3
        checks.append({'key': prefix, 'kind': 'actual-within-node-order-and-face',
                       'observed': actual, 'expected': expected,
                       'pass': actual == expected and distinct})
    require(len(checks) == 14, 'Visible semantic coverage drift')
    return checks


def pdf_facts(path: Path, fonts_version: str) -> tuple[dict, dict[str, str]]:
    links: list[dict] = []
    anchors: dict[str, dict] = {}
    internal: list[dict] = []
    with path.open("rb") as stream:
        reader = pypdf.PdfReader(stream, strict=True)
        require(not reader.is_encrypted, f"encrypted PDF: {path.name}")
        require(len(reader.pages) == EXPECTED_PAGE_COUNT,
                f"unexpected page count: {path.name}")
        named = reader.named_destinations
        require(set(EXPECTED_INTERNAL_TARGETS) <= set(named),
                f"internal destinations missing: {path.name}")
        target_pages = {target: reader.get_destination_page_number(named[target]) + 1
                        for target in EXPECTED_INTERNAL_TARGETS}
        require(target_pages == {target: 1 for target in EXPECTED_INTERNAL_TARGETS},
                f"internal destination page: {path.name}")
        page_boxes: list[list[float]] = []
        for page_number, page in enumerate(reader.pages, 1):
            media = [float(value) for value in page.mediabox]
            page_boxes.append(media)
            require(abs((media[2] - media[0]) - 612) < 0.1 and
                    abs((media[3] - media[1]) - 792) < 0.1,
                    f"non-letter page: {path.name}:{page_number}")
            for annotation_ref in page.get("/Annots", []):
                annotation = annotation_ref.get_object()
                if annotation.get("/Subtype") != "/Link":
                    continue
                rect = rectangle(annotation.get("/Rect"), media,
                                 f"{path.name}:{page_number}")
                action = annotation.get("/A")
                if action is not None and hasattr(action, "get_object"):
                    action = action.get_object()
                if action is not None and action.get("/S") == "/URI":
                    uri = str(action.get("/URI"))
                    record = {"kind": "URI", "page": page_number, "target": uri,
                              "rect": rect}
                    links.append(record)
                    if uri.startswith(GEOMETRY_URI_PREFIX):
                        key = uri[len(GEOMETRY_URI_PREFIX):]
                        require(key in GEOMETRY_KEY_SET and key not in anchors,
                                f"unknown/duplicate geometry URI: {path.name}:{key}")
                        anchors[key] = record
                elif ((action is not None and action.get("/S") == "/GoTo") or
                      annotation.get("/Dest") is not None):
                    target_value = (action.get("/D") if action is not None
                                    else annotation.get("/Dest"))
                    target = destination_name(target_value)
                    record = {"kind": "GoTo", "page": page_number, "target": target,
                              "target_page": target_pages.get(target), "rect": rect}
                    links.append(record)
                    internal.append(record)
                else:
                    raise ValueError(f"unsupported Link action: {path.name}:{page_number}")

        uri_targets = [item["target"] for item in links if item["kind"] == "URI"]
        require(uri_targets.count(EXPECTED_URI) == 1, f"probe URI missing/duplicated: {path.name}")
        require(Counter(item["target"] for item in internal) == Counter(EXPECTED_INTERNAL_TARGETS)
                and all(item["page"] == 1 and item["target_page"] == 1 for item in internal),
                f"internal GoTo inventory: {path.name}")
        require(set(anchors) == GEOMETRY_KEY_SET and
                len(links) == len(GEOMETRY_KEYS) + 3,
                f"exact Link/geometry inventory: {path.name}")

    with pdfplumber.open(path) as document:
        page_text = [page.extract_text(layout=True) or "" for page in document.pages]
        joined = "\n".join(page_text)
        require("(cid:" not in joined,
                f"opaque CID token remains in extracted text: {path.name}")
        regions, raw_regions = region_facts(document, path.name)
        for key, anchor in anchors.items():
            text = link_text(
                document.pages[anchor["page"] - 1],
                anchor["rect"],
                prefer_midline=key.endswith("invariant-models-op"),
            )
            require(text, f"geometry link has no extractable content: {path.name}:{key}")
            anchor["logical_text"] = text
        for key, expected in EXPECTED_STABLE_TEXT.items():
            if path.stem == 'rtl' and key.startswith('P03-') and key.endswith(('-open', '-close')):
                expected = {'(': ')', ')': '(', '[': ']', ']': '[',
                            '{': '}', '}': '{', '⟨': '⟩', '⟩': '⟨'}[expected]
            require(anchors[key]["logical_text"] == expected,
                    f"stable operand/fence/tag extraction: {path.name}:{key}")
        visible = visible_semantic_checks(document, anchors, path.stem)
        require(all(check['pass'] for check in visible),
                'Visible semantic failure: ' + repr([c for c in visible if not c['pass']]))

    job = path.stem
    geometry = validate_geometry(anchors, job)
    return ({
        "file": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "pages": EXPECTED_PAGE_COUNT,
        "page_boxes": page_boxes,
        "links": links,
        "internal_destination_pages": target_pages,
        "geometry": geometry,
        "geometry_anchors": anchors,
        "visible_semantic_checks": visible,
        "logical_regions": regions,
        "extracted_text_sha256": hashlib.sha256(joined.encode("utf-8")).hexdigest().upper(),
        "pdffonts_version": fonts_version,
        "font_facts": font_facts(path),
    }, raw_regions)


def normalize_fls_path(raw: str, working: Path) -> Path:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        value = value[1:-1]
    require(value and "\x00" not in value, "invalid recorder path")
    path = Path(value)
    if not path.is_absolute():
        path = working / path
    return path.resolve()


def normalized_inventory_path(path: Path, repo: Path, directory: Path) -> str:
    if path.is_relative_to(directory):
        return "@OUTPUT@/" + path.relative_to(directory).as_posix()
    if path.is_relative_to(repo):
        return path.relative_to(repo).as_posix()
    return os.path.normcase(str(path)).replace("\\", "/")


def inventory_digest(records: list[dict]) -> str:
    encoded = json.dumps(records, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()


def validate_fls(directory: Path, repo: Path, manifest: dict, job: str,
                 forbidden_directory: Path) -> dict:
    path = directory / f"{job}.fls"
    inputs: set[Path] = set()
    outputs: set[Path] = set()
    for line in path.read_text(encoding="utf-8", errors="strict").splitlines():
        if line.startswith("INPUT "):
            inputs.add(normalize_fls_path(line[6:], Path(manifest["WorkingDirectory"])))
        elif line.startswith("OUTPUT "):
            outputs.add(normalize_fls_path(line[7:], Path(manifest["WorkingDirectory"])))
    require(inputs and outputs, f"empty recorder inventory: {job}")
    expected_inputs = {
        repo / f"tmp/pdfs/classical-rtl-math-probe/{job}.tex",
        repo / "tmp/pdfs/classical-rtl-math-probe/common.tex",
        repo / "source/locale/ar-classical/open-logic-rtl-math.tex",
        repo / "source/sty/open-logic.sty",
        repo / "source/sty/open-logic-defer.sty",
        repo / "source/open-logic-envs.sty",
        repo / "source/locale/ar/open-logic-config.sty",
    }
    inputs = {item.resolve() for item in inputs}
    outputs = {item.resolve() for item in outputs}
    cache_inputs = {item for item in inputs if "luatex-cache" in item.parts}
    private_cache = (directory / "texmf-cache").resolve()
    require(cache_inputs and all(item.is_relative_to(private_cache) for item in cache_inputs),
            f"missing private or unexpected shared font-cache input: {job}")
    require(expected_inputs <= inputs, f"required recorder inputs missing: {job}")
    other_job = "rtl" if job == "control" else "control"
    require((repo / f"tmp/pdfs/classical-rtl-math-probe/{other_job}.tex").resolve()
            not in inputs, f"cross-job wrapper input: {job}")
    require(not any(item.is_relative_to(forbidden_directory) for item in inputs),
            f"recorder input crosses replay directories: {job}")
    # TEXMFCACHE also relocates MiKTeX's deleted write-test scratch file.
    # No recorded output may now escape the isolated build directory. Admit
    # only its one exact already-removed private scratch path as ephemeral.
    expected_miktex_scratch = private_cache / "m_t_x_t_e_s_t.tmp"
    external_outputs = {item for item in outputs if not item.is_relative_to(directory)}
    require(not external_outputs,
            f"unexpected or persistent recorder output outside build directory: {job}")
    require(expected_miktex_scratch in outputs and not expected_miktex_scratch.exists(),
            f"missing or persistent private recorder scratch: {job}")
    outputs.remove(expected_miktex_scratch)
    required_outputs = {directory / f"{job}.{suffix}"
                        for suffix in ("aux", "out", "log", "pdf")}
    require(required_outputs <= outputs, f"required recorder outputs missing: {job}")

    input_records = []
    for item in sorted(inputs, key=lambda candidate: os.path.normcase(str(candidate))):
        require(item.is_file(), f"recorder input is unavailable: {item}")
        input_records.append({
            "path": normalized_inventory_path(item, repo, directory),
            "bytes": item.stat().st_size,
            "sha256": sha256(item),
        })
    output_names = sorted(item.relative_to(directory).as_posix() for item in outputs)
    return {
        "fls_bytes": path.stat().st_size,
        "fls_sha256": sha256(path),
        "input_count": len(input_records),
        "input_inventory_sha256": inventory_digest(input_records),
        "inputs": input_records,
        "output_count": len(output_names),
        "output_inventory_sha256": hashlib.sha256(
            "\n".join(output_names).encode("utf-8")).hexdigest().upper(),
        "outputs": output_names,
        "external_ephemeral_outputs": [],
        "private_ephemeral_outputs": ["@OUTPUT@/texmf-cache/m_t_x_t_e_s_t.tmp"],
    }


def atomic_write_json(path: Path, payload: dict) -> None:
    require(not path.exists(), "refusing to overwrite QA receipt")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}-{uuid.uuid4().hex}")
    data = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
        except BaseException:
            try:
                os.close(descriptor)
            except OSError:
                pass
            raise
        os.link(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def guard_receipt_path(directory: Path) -> Path:
    return directory.parent / f"{directory.name}-TEX_MUTEX_RECEIPT.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    primary = args.primary.resolve()
    replay = args.replay.resolve()
    output = args.output.resolve()
    require(repo.is_dir(), "repository path")
    require(primary.is_dir() and replay.is_dir(), "primary/replay directory")
    require(primary != replay and not primary.is_relative_to(replay) and
            not replay.is_relative_to(primary), "primary/replay must be distinct")
    require(not output.exists(), "refusing to overwrite QA receipt")
    require(not output.is_relative_to(primary) and not output.is_relative_to(replay),
            "QA receipt must be outside build directories")

    manifests = {
        "primary": validate_manifest(primary, repo),
        "replay": validate_manifest(replay, repo),
    }
    guards = {}
    for run_name, directory in (("primary", primary), ("replay", replay)):
        receipt = guard_receipt_path(directory)
        guards[run_name] = validate_guard(receipt, manifests[run_name])
        bind_guard_file_times(directory, manifests[run_name], guards[run_name])

    fonts_version = pdffonts_version()
    facts: dict[str, dict] = {}
    raw_regions: dict[str, dict] = {}
    traces: dict[str, dict] = {}
    recorder: dict[str, dict] = {}
    for run_name, directory, other in (
        ("primary", primary, replay), ("replay", replay, primary),
    ):
        facts[run_name] = {}
        raw_regions[run_name] = {}
        traces[run_name] = {}
        recorder[run_name] = {}
        for job in ("control", "rtl"):
            log_path = directory / f"{job}.log"
            traces[run_name][job] = direction_trace(
                log_path.read_text(encoding="utf-8", errors="strict"), job)
            facts[run_name][job], raw_regions[run_name][job] = pdf_facts(
                directory / f"{job}.pdf", fonts_version)
            recorder[run_name][job] = validate_fls(
                directory, repo, manifests[run_name], job, other)

    for job in ("control", "rtl"):
        require(facts["primary"][job]["sha256"] == facts["replay"][job]["sha256"],
                f"{job} replay bytes differ")
        require(recorder["primary"][job]["input_inventory_sha256"] ==
                recorder["replay"][job]["input_inventory_sha256"],
                f"{job} replay recorder inputs differ")
        require(recorder["primary"][job]["outputs"] == recorder["replay"][job]["outputs"],
                f"{job} replay recorder outputs differ")
    require(manifests["primary"]["Inputs"] == manifests["replay"]["Inputs"] and
            manifests["primary"]["Engine"] == manifests["replay"]["Engine"],
            "primary/replay producer inputs differ")

    for probe in PROBE_IDS:
        # Directional faces must differ between the control and RTL rendering;
        # treating those visible glyphs as equal via per-symbol ActualText would
        # lie about the rendered relation.  Compare only letters/digits here.
        # Exact canonical tokens remain bound by the manifest's common.tex hash.
        control_alnum = Counter(character for character in
                                raw_regions["primary"]["control"][probe]
                                if character.isalnum())
        rtl_alnum = Counter(character for character in
                            raw_regions["primary"]["rtl"][probe]
                            if character.isalnum())
        require(control_alnum == rtl_alnum,
                f"control/RTL extracted alphanumeric inventory differs for {probe}")
    for key in GEOMETRY_KEYS:
        control_text = facts["primary"]["control"]["geometry_anchors"][key]["logical_text"]
        rtl_text = facts["primary"]["rtl"]["geometry_anchors"][key]["logical_text"]
        require(Counter(character for character in control_text if character.isalnum()) ==
                Counter(character for character in rtl_text if character.isalnum()),
                f"control/RTL linked alphanumeric content differs: {key}")
    for key in PRESERVED_FACE_KEYS:
        control_text = facts["primary"]["control"]["geometry_anchors"][key]["logical_text"]
        rtl_text = facts["primary"]["rtl"]["geometry_anchors"][key]["logical_text"]
        require(control_text == rtl_text,
                f"control/RTL scoped-preservation face differs: {key}")

    source_records = {
        item["Path"]: {"bytes": item["Bytes"], "sha256": item["SHA256"]}
        for item in manifests["primary"]["Inputs"]
    }
    payload = {
        "schema": SCHEMA,
        "status": "PASS",
        "scope": "isolated-probe-only",
        "visual_acceptance": "NOT_CLAIMED_BY_THIS_DETERMINISTIC_RECEIPT",
        "sources": source_records,
        "build_manifests": {
            run_name: {
                "path": str(directory / "BUILD_MANIFEST.json"),
                "bytes": (directory / "BUILD_MANIFEST.json").stat().st_size,
                "sha256": sha256(directory / "BUILD_MANIFEST.json"),
            }
            for run_name, directory in (("primary", primary), ("replay", replay))
        },
        "guards": {
            run_name: {
                "receipt": str(guard_receipt_path(directory)),
                "bytes": guard_receipt_path(directory).stat().st_size,
                "sha256": sha256(guard_receipt_path(directory)),
                "abandoned_mutex_recovered": guards[run_name]["AbandonedMutexRecovered"],
            }
            for run_name, directory in (("primary", primary), ("replay", replay))
        },
        "direction_traces": traces,
        "recorder": recorder,
        "artifacts": facts,
        "deterministic_replay": True,
        "extracted_alphanumeric_inventory_equal_by_probe": True,
        "visible_directional_faces_checked_without_per_symbol_actualtext": True,
        "all_p01_p20_geometry_checked": True,
        "links_and_named_destinations_checked": True,
        "font_embedding_and_tounicode_checked": True,
        "limitations": [
            "This receipt validates an isolated ten-page fixture, not the 722-unit reader.",
            "Visual inspection is outside this deterministic receipt; no visual-review claim is made.",
            "Canonical formula tokens are bound by source hashes; no structured formula-level ActualText is supplied.",
        ],
        "failures": [],
    }
    atomic_write_json(output, payload)
    print(json.dumps({
        "status": "PASS", "output": str(output),
        "control_sha256": facts["primary"]["control"]["sha256"],
        "rtl_sha256": facts["primary"]["rtl"]["sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
