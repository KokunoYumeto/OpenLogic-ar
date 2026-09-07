"""Static and policy-model tests for the isolated Classical RTL-math layer.

No test in this module launches TeX. Runtime geometry, font, link, extraction,
callback, and tag-side acceptance belongs to the guarded paired-probe QA.
"""

from dataclasses import dataclass
from pathlib import Path
import re
import runpy
import unittest


ROOT = Path(__file__).resolve().parents[2]
LAYER = ROOT / "source/locale/ar-classical/open-logic-rtl-math.tex"
DESIGN = ROOT / "evidence/classical/RTL_MATH_DESIGN.md"
IMPLEMENTATION = ROOT / "evidence/classical/RTL_REGISTRY_IMPLEMENTATION.md"
FIXTURE = ROOT / "tmp/pdfs/classical-rtl-math-probe/common.tex"
CONTROL = ROOT / "tmp/pdfs/classical-rtl-math-probe/control.tex"
RTL = ROOT / "tmp/pdfs/classical-rtl-math-probe/rtl.tex"
QA = ROOT / "build/qa_classical_rtl_math_probe.py"

SOURCE = LAYER.read_text(encoding="utf-8")
FIXTURE_SOURCE = FIXTURE.read_text(encoding="utf-8")
QA_SOURCE = QA.read_text(encoding="utf-8")
CODE = "\n".join(line.split("%", 1)[0] for line in SOURCE.splitlines())

REGISTRY_PAIRS = (
    ("rightarrow", "leftarrow", "simple", "mathrel", "UTR25-formula-relative"),
    ("longrightarrow", "longleftarrow", "long-single", "mathrel", "UTR25-formula-relative"),
    ("Rightarrow", "Leftarrow", "simple", "mathrel", "UTR25-formula-relative"),
    ("Longrightarrow", "Longleftarrow", "long-double", "mathrel", "UTR25-formula-relative"),
    ("xrightarrow", "xleftarrow", "boxed-x-arrow", "mathrel", "pinned-amsmath-extensible-pair"),
    ("xLongrightarrow", "xLongleftarrow", "boxed-x-long-double-arrow", "mathrel", "pinned-extarrows-extensible-pair"),
    ("mapsto", "OLClassicalMapsFrom", "mapsto", "mathrel", "formula-relative-map"),
    ("longmapsto", "OLClassicalLongMapsFrom", "long-mapsto", "mathrel", "formula-relative-map"),
    ("boxright", "OLClassicalBoxLeft", "simple", "mathbin", "pinned-ntxsyc-slot-pair"),
    ("fishhookright", "OLClassicalFishhookLeft", "simple", "mathbin", "pinned-ntxsyc-slot-pair"),
    ("literal-lt", "literal-gt", "literal", "mathrel", "Unicode-BidiMirroring"),
    ("leq", "geq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("in", "ni", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("prec", "succ", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("preceq", "succeq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("npreceq", "nsucceq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("preccurlyeq", "succcurlyeq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("precsim", "succsim", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("nless", "ngtr", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("lessdot", "gtrdot", "simple", "mathbin", "pinned-ams-symbol-pair"),
    ("varolessthan", "varogreaterthan", "simple", "mathbin", "pinned-stmaryrd-pair"),
    ("subset", "supset", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("subseteq", "supseteq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("nsubseteq", "nsupseteq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("subsetneq", "supsetneq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("sqsubset", "sqsupset", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("sqsubseteq", "sqsupseteq", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("upharpoonright", "upharpoonleft", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("lhd", "rhd", "simple", "mathbin", "Unicode-BidiMirroring"),
    ("vdash", "dashv", "simple", "mathrel", "Unicode-BidiMirroring"),
    ("overrightarrow", "overleftarrow", "over-accent", "mathord", "formula-relative-accent"),
    ("underrightarrow", "underleftarrow", "under-accent", "mathord", "formula-relative-accent"),
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
PAIR_IDS = (
    "arrow", "long-arrow", "double-arrow", "long-double-arrow", "x-arrow",
    "x-long-double-arrow", "mapsto", "long-mapsto", "counterfactual",
    "strict-conditional", "literal-order", "order-eq", "membership",
    "precedence", "precedence-eq", "negated-precedence-eq",
    "curly-precedence-eq", "precedence-sim", "negated-order", "dotted-order",
    "nonstandard-order", "subset", "subset-eq", "negated-subset-eq",
    "proper-subset", "square-subset", "square-subset-eq", "restriction",
    "triangle-order", "turnstile",
)


def registry_body(name: str) -> str:
    match = re.search(
        rf"\\newcommand\*\{{\\{name}\}}\[1\]\{{%(.*?)^\}}",
        SOURCE, flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"missing registry macro {name}")
    return match.group(1)


def parse_pair_registry() -> tuple[tuple[str, ...], ...]:
    return tuple(re.findall(
        r"#1\{([^{}]+)\}\{([^{}]+)\}\{([^{}]+)\}\{([^{}]+)\}\{([^{}]+)\}",
        registry_body("OLClassicalRTLRegistryPairs"),
    ))


def parse_alias_registry() -> tuple[tuple[str, ...], ...]:
    return tuple(re.findall(
        r"#1\{([^{}]+)\}\{([^{}]+)\}\{([^{}]+)\}",
        registry_body("OLClassicalRTLRegistryAliases"),
    ))


def parse_invariant_registry() -> tuple[tuple[str, ...], ...]:
    return tuple(re.findall(
        r"#1\{([^{}]+)\}\{([^{}]+)\}",
        registry_body("OLClassicalRTLRegistryInvariants"),
    ))


def parse_fallback_registry() -> tuple[tuple[str, ...], ...]:
    return tuple(re.findall(
        r"#1\{([^{}]+)\}\{([^{}]+)\}\{([^{}]+)\}\{([^{}]+)\}",
        registry_body("OLClassicalRTLRegistryFallbacks"),
    ))


def parse_boxed_accent_registry() -> tuple[tuple[str, ...], ...]:
    return tuple(re.findall(
        r"#1\{([^{}]+)\}\{([^{}]+)\}\{([^{}]+)\}",
        registry_body("OLClassicalRTLBoxedAccentInvariants"),
    ))


def parse_fixture_pair_ids(command: str) -> tuple[str, ...]:
    """Read only fixture IDs, leaving arbitrarily nested operator arguments opaque."""
    if command == "ProbePair":
        pattern = r"\\ProbePair\{([^{}]+)\}"
    elif command == "ProbePairAt":
        pattern = r"\\ProbePairAt\{P18\}\{([^{}]+)\}"
    else:
        raise AssertionError(f"unknown fixture pair command {command}")
    return tuple(re.findall(pattern, FIXTURE_SOURCE))


PRESENTATION_PAIRS = tuple(
    (f"\\{right}", f"\\{left}")
    for right, left, _kind, _atom, _reason in REGISTRY_PAIRS
    if not right.startswith("literal-")
) + (("<", ">"),)
PRESENTATION_MIRROR = {
    item: mate
    for pair in PRESENTATION_PAIRS
    for item, mate in (pair, pair[::-1])
}
ENGINE_FENCE_PAIRS = (
    ("(", ")"), ("[", "]"), (r"\lbrace", r"\rbrace"),
    (r"\langle", r"\rangle"),
)
ENGINE_FENCE_MIRROR = {
    item: mate
    for pair in ENGINE_FENCE_PAIRS
    for item, mate in (pair, pair[::-1])
}
INVARIANT = {f"\\{name}" for name, _kind in REGISTRY_INVARIANTS} | {
    "=", r"\neq", "+", "-", r"\times",
}


def visual_row(source_tokens, direction="rtl"):
    """Small policy model, not a renderer or token-rewrite implementation."""
    snapshot = tuple(source_tokens)
    if direction == "ltr":
        visual = snapshot
    elif direction == "rtl":
        visual = tuple(
            PRESENTATION_MIRROR.get(token, ENGINE_FENCE_MIRROR.get(token, token))
            for token in reversed(snapshot)
        )
    else:
        raise ValueError(direction)
    if tuple(source_tokens) != snapshot:
        raise AssertionError("policy model mutated canonical source")
    return visual


@dataclass(frozen=True)
class Fraction:
    numerator: tuple
    denominator: tuple

    def rtl_visual(self):
        return {"above": visual_row(self.numerator),
                "below": visual_row(self.denominator)}


@dataclass(frozen=True)
class Scripted:
    nucleus: str
    superscript: tuple
    subscript: tuple

    def rtl_visual(self):
        return {"nucleus": self.nucleus, "script_side": "visual-left",
                "superscript": visual_row(self.superscript),
                "subscript": visual_row(self.subscript)}


class StaticLayerContractTests(unittest.TestCase):
    def test_files_are_in_isolated_classical_evidence_and_probe_scopes(self):
        self.assertEqual(LAYER.relative_to(ROOT).as_posix(),
                         "source/locale/ar-classical/open-logic-rtl-math.tex")
        self.assertEqual(IMPLEMENTATION.relative_to(ROOT).as_posix(),
                         "evidence/classical/RTL_REGISTRY_IMPLEMENTATION.md")
        for path in (LAYER, DESIGN, IMPLEMENTATION, FIXTURE, CONTROL, RTL, QA):
            self.assertTrue(path.is_file(), path)

    def test_explicit_scope_order_mirroring_and_probe_markers(self):
        for marker in (
            "OL-RTL-SCOPE=ar-classical-only",
            "OL-RTL-ORDER=source-tokens-unchanged",
            "OL-RTL-MIRROR=typed-registry-once-visible-extraction",
            "OL-RTL-COMPLEX=guarded-probe-before-reader-integration",
        ):
            self.assertIn(marker, SOURCE)

    def test_input_is_inert_and_installation_is_preamble_only(self):
        self.assertIn(r"\ifdefined\OLClassicalInstallRTLMath\endinput\fi", CODE)
        self.assertEqual(CODE.count(r"\NewDocumentCommand{\OLClassicalInstallRTLMath}"), 1)
        self.assertEqual(len(re.findall(
            r"\\OLClassicalInstallRTLMath(?![A-Za-z@])", CODE)), 3)
        self.assertIn(r"\@onlypreamble\OLClassicalInstallRTLMath", CODE)

    def test_registry_is_exact_typed_finite_and_disjoint(self):
        self.assertEqual(parse_pair_registry(), REGISTRY_PAIRS)
        self.assertEqual(parse_alias_registry(), REGISTRY_ALIASES)
        self.assertEqual(parse_invariant_registry(), REGISTRY_INVARIANTS)
        self.assertEqual(parse_fallback_registry(), REGISTRY_FALLBACKS)
        self.assertEqual(parse_boxed_accent_registry(), REGISTRY_BOXED_ACCENTS)
        endpoints = [item for pair in REGISTRY_PAIRS for item in pair[:2]]
        aliases = [row[0] for row in REGISTRY_ALIASES]
        invariants = [row[0] for row in REGISTRY_INVARIANTS]
        fallbacks = [row[0] for row in REGISTRY_FALLBACKS]
        boxed_accents = [row[0] for row in REGISTRY_BOXED_ACCENTS]
        self.assertEqual(len(endpoints), len(set(endpoints)))
        self.assertTrue(set(aliases).isdisjoint(endpoints))
        self.assertTrue(set(invariants).isdisjoint(endpoints + aliases))
        classes = [set(endpoints), set(aliases), set(invariants),
                   set(fallbacks), set(boxed_accents)]
        for index, one in enumerate(classes):
            for other in classes[index + 1:]:
                self.assertTrue(one.isdisjoint(other))
        self.assertEqual({row[3] for row in REGISTRY_PAIRS},
                         {"mathrel", "mathord", "mathbin"})
        self.assertTrue(all(row[4] for row in REGISTRY_PAIRS))
        for _alias, ltr_endpoint, rtl_endpoint in REGISTRY_ALIASES:
            self.assertIn(ltr_endpoint, endpoints)
            self.assertIn(rtl_endpoint, endpoints)

    def test_registry_inventory_counts_and_exact_restore_ownership_exist(self):
        for token in (
            r"\chardef\OLClassicalExpectedRTLRegistryPairCount=32",
            r"\chardef\OLClassicalExpectedRTLRegistryInvariantCount=14",
            r"\chardef\OLClassicalExpectedRTLRegistryAliasCount=6",
            r"\chardef\OLClassicalExpectedRTLRegistryFallbackCount=9",
            r"\chardef\OLClassicalExpectedRTLRegistryAccentCount=13",
            r"\OLClassicalRTLRegistryEntries\OLClassicalRegistryCheckEntry",
            r"\OLClassicalRTLRegistryInvariants\OLClassicalRegistryCheckInvariant",
            r"\OLClassicalCheckLiteralRegistryOwnership",
            r"\OLClassicalRTLRegistryEntries\OLClassicalRestoreRegistryEntry",
            r"\OLClassicalRTLRegistryInvariants\OLClassicalRegistryForgetInvariant",
            r"\OLClassicalRestoreLiteralRegistry",
            r"\typeout{OLC-RTL-REGISTRY-PAIR=#1/#2/#3/#4/#5}",
            r"\typeout{OLC-RTL-REGISTRY-FALLBACK=#1/#2/#3/#4}",
            r"\typeout{OLC-RTL-REGISTRY-BOXED-ACCENT=#1/#2/#3}",
            r"\typeout{OLC-RTL-REGISTRY=typed-coverage-v5}",
            r"\typeout{OLC-RTL-REGISTRY-COUNTS=pairs-32;aliases-6;invariants-14;fallbacks-9;boxed-accents-13}",
        ):
            self.assertIn(token, CODE)
        self.assertIn("ownership or classification drift", SOURCE)
        self.assertIn("Unknown typed-registry implementation kind", SOURCE)
        self.assertIn("Unknown LTR registry endpoint", SOURCE)
        self.assertIn("Unknown RTL registry endpoint", SOURCE)
        self.assertIn("duplicate RTL-math geometry key in QA contract", QA_SOURCE)
        self.assertIn("exact Link/geometry inventory", QA_SOURCE)

    def test_literal_pair_saves_mathcodes_active_meanings_and_restores_them(self):
        for token in (
            r"\global\OLClassicalSavedLessMathCode=\mathcode60",
            r"\global\OLClassicalSavedGreaterMathCode=\mathcode62",
            r'\global\mathcode60="8000',
            r'\global\mathcode62="8000',
            r'\ifnum\mathcode60="1000000',
            r'\ifnum\mathcode62="1000000',
            r"\global\mathcode60=\OLClassicalSavedLessMathCode",
            r"\global\mathcode62=\OLClassicalSavedGreaterMathCode",
            r"\OLClassicalSavedActiveLessDefinedtrue",
            r"\OLClassicalSavedActiveGreaterDefinedtrue",
        ):
            self.assertIn(token, CODE)

    def test_optional_mandatory_fallback_builder_has_exact_signature(self):
        self.assertIn(
            r"\newcommand*{\OLClassicalBuildScopedLTRXrightarrowdbl}[3]",
            CODE,
        )
        self.assertNotIn(
            r"\newcommand*{\OLClassicalBuildScopedLTRXrightarrowdbl}[4]",
            CODE,
        )
        for style in (
            r"\displaystyle", r"\textstyle",
            r"\scriptstyle", r"\scriptscriptstyle",
        ):
            self.assertIn(
                rf"\OLClassicalBuildScopedLTRXrightarrowdbl{style}{{#1}}{{#2}}",
                CODE,
            )

    def test_desired_direction_is_reasserted_at_each_math_list_boundary(self):
        activate = re.search(
            r"\\newcommand\*\{\\OLClassicalActivateMathListHooks\}.*?^\}",
            SOURCE, flags=re.MULTILINE | re.DOTALL,
        ).group(0)
        compact = "\n".join(line.split("%", 1)[0] for line in activate.splitlines())
        self.assertIn(
            r"\global\everymath\expandafter{\the\everymath\OLClassicalApplyDesiredMathDirection}",
            compact,
        )
        self.assertIn(
            r"\global\everydisplay\expandafter{\the\everydisplay\OLClassicalApplyDesiredMathDirection}",
            compact,
        )
        for token in (
            r"\OLClassicalSetRTLMathHookOwnership",
            r"\OLClassicalInstalledEveryMath",
            r"\OLClassicalInstalledEveryDisplay",
            r"\global\everymath=\OLClassicalSavedEveryMath",
            r"\global\everydisplay=\OLClassicalSavedEveryDisplay",
        ):
            self.assertIn(token, CODE)

    def test_namespaced_post_mlist_owner_is_single_reversible_and_non_reversing(self):
        owner = "openlogic.classical.rtl_math.ensure_math_dir"
        self.assertEqual(SOURCE.count(f'local owner = "{owner}"'), 3)
        for token in (
            'luatexbase.add_to_callback(', '"post_mlist_to_hlist_filter"',
            "luatexbase.in_callback", "luatexbase.callback_descriptions",
            "luatexbase.remove_from_callback", 'node.new("dir")',
            'node.new("dir", 1)', "tex.mathdirection",
        ):
            self.assertIn(token, SOURCE)
        for forbidden in ("node.reverse", "node.slide", "mlist_to_hlist(head",
                          "pre_mlist_to_hlist_filter"):
            self.assertNotIn(forbidden, CODE)

    def test_callback_restore_checks_exact_function_and_readds_a_foreign_owner(self):
        for token in (
            "openlogic_classical_rtl_math.installed_function =",
            "openlogic_classical_rtl_math.ensure_math_dir",
            "local removed, description = luatexbase.remove_from_callback(",
            "and openlogic_classical_rtl_math.installed_function or nil",
            "if not (removed == expected) or not (description == owner) then",
            '"post_mlist_to_hlist_filter", removed, description)',
            "private callback identity drift",
            "callback function identity drift",
            "openlogic_classical_rtl_math.installed_function = nil",
        ):
            self.assertIn(token, SOURCE)
        removal = re.search(
            r"\\newcommand\*\{\\OLClassicalRemoveMathListDirectionCallback\}.*?^\}",
            SOURCE, flags=re.MULTILINE | re.DOTALL,
        ).group(0)
        self.assertLess(removal.index("luatexbase.add_to_callback("),
                        removal.index("callback function identity drift"))

    def test_local_ltr_and_accent_internal_lists_use_the_same_state_setter(self):
        self.assertIn(r"\OLClassicalDesiredMathDirection=#1", CODE)
        self.assertIn(r"\mathdirection=#1", CODE)
        accent = re.search(
            r"\\newcommand\*\{\\OLClassicalBuildRTLAccent\}.*?^\}",
            SOURCE, flags=re.MULTILINE | re.DOTALL,
        ).group(0)
        self.assertIn(r"\OLClassicalSetLocalMathDirection\z@", accent)
        self.assertIn(r"\OLClassicalSetLocalMathDirection\@ne", accent)
        self.assertIn(r"\NewDocumentEnvironment{OLClassicalLTRMathScope}{}", CODE)

    def test_physical_left_tag_policy_is_saved_checked_and_restored(self):
        self.assertIn(r"\PassOptionsToPackage{reqno}{amsmath}", FIXTURE_SOURCE)
        classical_preamble = (ROOT / "source/locale/ar-classical/"
                              "open-logic-ar-classical-eastern-rtl-preamble.tex").read_text(
                                  encoding="utf-8")
        self.assertIn(r"\PassOptionsToPackage{reqno}{amsmath}", classical_preamble)
        self.assertIn(r"\@ifpackagewith{amsmath}{reqno}", SOURCE)
        self.assertIn(r"\ifdefined\bbl@leqno@flip", SOURCE)
        self.assertIn(r"\newcommand*{\OLClassicalBabelPhysicalLeftEquationAdapter}", SOURCE)
        self.assertIn(r"\def\veqno##1##2{\bbl@leqno@flip{##1##2}}", SOURCE)
        self.assertIn(
            r"\global\let\bbl@ams@equation\OLClassicalBabelPhysicalLeftEquationAdapter",
            SOURCE,
        )
        self.assertIn(
            r"\global\let\bbl@ams@equation\OLClassicalSavedBabelEquationAdapter",
            SOURCE,
        )
        for token in (
            r"\iftagsleft@", r"\tagsleft@false",
            r"\global\OLClassicalSavedTagsLefttrue",
            r"\global\OLClassicalSavedTagsLeftfalse",
            r"\ifOLClassicalSavedTagsLeft\tagsleft@true\else\tagsleft@false\fi",
            "physical-left display-tag policy",
            "Refusing to overwrite a later display-tag policy change",
        ):
            self.assertIn(token, SOURCE)

    def test_runtime_registry_can_actually_be_restored_after_activation(self):
        self.assertNotIn(r"\@onlypreamble\OLClassicalRestoreMathDirection", CODE)
        self.assertIn(r"\ifnum\currentgrouplevel=\z@", CODE)
        self.assertIn(r"\OLClassicalRemoveMathListDirectionCallback", CODE)
        self.assertIn(r"\global\OLClassicalRTLMathRuntimeActivefalse", CODE)
        self.assertIn("runtime ownership transaction impossible to reverse", SOURCE)

    def test_no_forbidden_package_token_or_noad_reversal_or_actualtext(self):
        for forbidden in (
            r"\amreflect", r"\amrl", r"\afterassignment",
            r"\RequirePackage{luabidi}", r"\usepackage{luabidi}",
            r"\RequirePackage{RyDArab}", r"\usepackage{RyDArab}",
            r"\RequirePackage{RamzArab}", r"\usepackage{RamzArab}",
            "ActualText", "node.reverse", "token.reverse", "string.reverse",
        ):
            self.assertNotIn(forbidden, CODE)
            self.assertNotIn(forbidden, FIXTURE_SOURCE)

    def test_no_non_math_direction_counter_link_or_shared_config_mutation(self):
        for forbidden in (
            r"\textdir", r"\textdirection", r"\pardir", r"\pardirection",
            r"\bodydir", r"\bodydirection", r"\pagedir", r"\pagedirection",
            r"\thepage", r"\href", r"\url", r"\label", r"\pdfstringdef",
        ):
            self.assertNotIn(forbidden, CODE)
        self.assertNotIn("source/locale/ar/", SOURCE)
        self.assertNotIn("open-logic-config.sty", SOURCE)

    def test_probe_covers_complete_registry_nested_owners_and_tags(self):
        self.assertEqual(parse_fixture_pair_ids("ProbePair"), PAIR_IDS)
        self.assertEqual(parse_fixture_pair_ids("ProbePairAt"), PAIR_IDS)
        self.assertIn(r"\ProbePair{x-arrow}{\xrightarrow{\alpha}}{\xleftarrow{\alpha}}",
                      FIXTURE_SOURCE)
        self.assertIn(
            r"\ProbePairAt{P18}{x-long-double-arrow}{\xLongrightarrow{\alpha}}{\xLongleftarrow{\alpha}}",
            FIXTURE_SOURCE,
        )
        for alias, _ltr, _rtl in REGISTRY_ALIASES:
            self.assertIn(f"P15-alias-{alias}", FIXTURE_SOURCE)
            self.assertIn(f"P18-alias-{alias}", FIXTURE_SOURCE)
        for invariant, _kind in REGISTRY_INVARIANTS:
            self.assertIn(f"P15-invariant-{invariant}", FIXTURE_SOURCE)
        for fallback, _kind, _atom, _reason in REGISTRY_FALLBACKS:
            self.assertIn(f"P19-fallback-{fallback}", FIXTURE_SOURCE)
            self.assertIn(f"P20-fallback-{fallback}", FIXTURE_SOURCE)
        for accent, _atom, _reason in REGISTRY_BOXED_ACCENTS:
            self.assertIn(f"P19-boxed-accent-{accent}", FIXTURE_SOURCE)
            self.assertIn(f"P20-boxed-accent-{accent}", FIXTURE_SOURCE)
        for family in ("equation", "align", "gather", "multline", "split"):
            self.assertIn(f"P17-{family}-tag", FIXTURE_SOURCE)
        for marker in ("P16-global-case-one", "P16-global-tableau-root",
                       "P16-local-case", "P18-over-accent-right",
                       "P18-invariant-models"):
            self.assertIn(marker, FIXTURE_SOURCE)
        self.assertIn("OLC-RTL-SOURCE-SIGNATURE=P01-P20-v9", FIXTURE_SOURCE)

    def test_probe_maps_every_exercised_legacy_type1_glyph(self):
        for token in (
            r"\fixtounicode{tfm=txsyc,",
            "glyphs={strict,strictinverse,squareright,squareleft}",
            "unicodes={297D,297C,25A1 2192,2190 25A1}",
            r"\fixtounicode{tfm=msbm10,",
            "glyphs={notprecedesoreql,notfollowsoreql}",
            "unicodes={22E0,22E1}",
            r"\fixtounicode{tfm=stmary10,",
            "glyphs={varolessthan,varogreaterthan}",
            "unicodes={29C0,29C1}",
            r"\fixtounicode{tfm=cmex10,",
            "summationdisplay,hatwidest,tildewidest",
            "unicodes={0028,0029,007B,007B,2211,0302,0303}",
        ):
            self.assertIn(token, FIXTURE_SOURCE)

    def test_local_ltr_nested_formulas_have_matching_babel_embedding(self):
        self.assertIn(
            r"\babelsublr{\begin{OLClassicalLTRMathScope}",
            FIXTURE_SOURCE,
        )
        self.assertIn(r"$\ProbeBoxedMathAtom{P16-local-function}{g(A)}=\begin{cases}",
                      FIXTURE_SOURCE)
        self.assertIn("Babel's inline left-to-right embedding is unavailable", SOURCE)
        self.assertIn(r"\babelsublr{\begin{OLClassicalLTRMathScope}%", SOURCE)

    def test_exhaustive_tables_are_split_and_given_readable_row_spacing(self):
        self.assertGreaterEqual(FIXTURE_SOURCE.count(r"\renewcommand{\arraystretch}{1.15}"), 4)
        self.assertIn(
            "\\ProbePair{nonstandard-order}{\\varolessthan}{\\varogreaterthan}\n"
            "\\end{tabular}}\n\\end{center}\n\\clearpage",
            FIXTURE_SOURCE,
        )
        self.assertIn(
            "\\ProbePairAt{P18}{nonstandard-order}{\\varolessthan}{\\varogreaterthan}\n"
            "\\end{tabular}}\n\\end{center}\n\\clearpage",
            FIXTURE_SOURCE,
        )

    def test_control_and_rtl_jobs_share_one_canonical_fixture(self):
        common_path = (
            "C:/interlanguage-production/openlogic-arabic-dual-notation/repo/"
            "tmp/pdfs/classical-rtl-math-probe/common.tex"
        )
        self.assertEqual(CONTROL.read_text(encoding="utf-8").strip(),
                         rf"\input{{{common_path}}}")
        rtl = RTL.read_text(encoding="utf-8")
        self.assertEqual(rtl.count(common_path), 1)
        self.assertEqual(rtl.count(r"\newcommand*{\OLCProbeInstallRTL}{}"), 1)

    def test_runtime_qa_is_synchronized_with_ten_page_fixture(self):
        for token in (
            'SOURCE_SIGNATURE = "OLC-RTL-SOURCE-SIGNATURE=P01-P20-v9"',
            'PROBE_IDS = tuple(f"P{i:02d}" for i in range(1, 21))',
            "EXPECTED_PAGE_COUNT = 10",
            "require(len(reader.pages) == EXPECTED_PAGE_COUNT",
            '"P19": 9, "P20": 10',
            '"end_page": end_page',
            "probe marker order across pages",
            "EXPECTED_DIRECTIONAL_ENDPOINTS",
            "validate_directional_faces", "validate_invariant_faces",
            "validate_tag_policy", "GLOBAL_TRIPLES", "LOCAL_LTR_TRIPLES",
            "TRANSFORMED_TABLEAU_TRIPLES",
            "visible_directional_faces_checked_without_per_symbol_actualtext",
            '"pages": EXPECTED_PAGE_COUNT',
            "opaque CID token remains in extracted text",
        ):
            self.assertIn(token, QA_SOURCE)
        self.assertNotIn("control/RTL linked logical content differs", QA_SOURCE)
        self.assertNotIn("all_p01_p14_geometry_checked", QA_SOURCE)

    def test_fixture_annotation_inventory_exactly_matches_fail_closed_qa(self):
        expected = set()
        for key in re.findall(r"\\ProbeAtom\{([^{}]+)\}", FIXTURE_SOURCE):
            if "#" not in key:
                expected.add(key)
        for key in re.findall(r"\\ProbeBoxedMathAtom\{([^{}]+)\}", FIXTURE_SOURCE):
            if "#" not in key:
                expected.add(key)
        for prefix in re.findall(r"\\ProbeTriplet\{([^{}]+)\}", FIXTURE_SOURCE):
            if "#" not in prefix:
                expected.update(f"{prefix}-{part}" for part in ("A", "op", "B"))
        for pair_id in parse_fixture_pair_ids("ProbePair"):
            for side in ("right", "left"):
                expected.update(f"P15-{pair_id}-{side}-{part}"
                                for part in ("A", "op", "B"))
        for pair_id in parse_fixture_pair_ids("ProbePairAt"):
            for side in ("right", "left"):
                expected.update(f"P18-{pair_id}-{side}-{part}"
                                for part in ("A", "op", "B"))
        contract = runpy.run_path(str(QA))
        self.assertEqual(expected, contract["GEOMETRY_KEY_SET"])
        self.assertEqual(len(expected), 633)
        self.assertEqual(len(contract["EXPECTED_DIRECTIONAL_ENDPOINTS"]), 180)
        self.assertEqual(len(contract["TRANSFORMED_TABLEAU_TRIPLES"]), 6)
        self.assertTrue(all(
            keys not in contract["GLOBAL_TRIPLES"]
            for keys in contract["TRANSFORMED_TABLEAU_TRIPLES"]
        ))
        qa_pair_ids = PAIR_IDS + ("over-accent", "under-accent")
        self.assertEqual(contract["REGISTRY_PAIRS"], tuple(
            (identifier, *row)
            for identifier, row in zip(qa_pair_ids, REGISTRY_PAIRS)
        ))
        self.assertEqual(contract["REGISTRY_ALIASES"], REGISTRY_ALIASES)
        self.assertEqual(contract["REGISTRY_INVARIANTS"], REGISTRY_INVARIANTS)
        self.assertEqual(contract["REGISTRY_FALLBACKS"], REGISTRY_FALLBACKS)
        self.assertEqual(contract["REGISTRY_BOXED_ACCENTS"], REGISTRY_BOXED_ACCENTS)

    def test_link_text_falls_back_to_actual_glyph_rectangle_intersection(self):
        contract = runpy.run_path(str(QA))
        page = type("Page", (), {"chars": [{
            "x0": 2.0, "x1": 8.0,
            "y0": 8.0, "y1": 12.0,
            "text": "⧀",
        }]})()
        # The glyph centre (10) lies below the centre-selection tolerance for
        # this rectangle, but the drawn box intersects it by two points.
        self.assertEqual(contract["link_text"](page, [0.0, 11.0, 10.0, 20.0]), "⧀")

    def test_link_text_prefers_annotation_midline_over_adjacent_table_row(self):
        contract = runpy.run_path(str(QA))
        page = type("Page", (), {"chars": [
            {"x0": 2.0, "x1": 4.0, "y0": 18.0, "y1": 24.0, "text": "|"},
            {"x0": 4.0, "x1": 7.0, "y0": 18.0, "y1": 24.0, "text": "="},
            # Its centre is still inside the tall link rectangle, but its box
            # does not cross the link midline and must not contaminate '|='.
            {"x0": 2.0, "x1": 7.0, "y0": 11.0, "y1": 17.0, "text": "←"},
        ]})()
        self.assertEqual(
            contract["link_text"](page, [0.0, 10.0, 10.0, 26.0], True),
            "|=",
        )

    def test_runtime_qa_recovers_tex_wrapped_registry_typeouts(self):
        contract = runpy.run_path(str(QA))
        prefix = "OLC-RTL-REGISTRY-"
        first = prefix + "PAIR=xLongrightarrow/xLongleftarrow/boxed-x-long-double-arrow/"
        self.assertEqual(len(first), 79)
        log = "noise\n" + first + "\nmathrel/pinned-extarrows-extensible-pair\nend\n"
        self.assertEqual(
            contract["unwrap_tex_typeout_records"](log, prefix),
            first + "mathrel/pinned-extarrows-extensible-pair",
        )

    def test_end_document_ownership_check_uses_a_live_latex_hook(self):
        self.assertIn(
            r"\AddToHook{enddocument}[ol-classical-rtl-math-ownership]",
            SOURCE,
        )
        self.assertIn(
            r"\RemoveFromHook{enddocument}[ol-classical-rtl-math-ownership]",
            SOURCE,
        )
        self.assertNotIn("enddocument/before", SOURCE)

    def test_fixture_has_balanced_braces_math_delimiters_and_environments(self):
        fixture_code = "\n".join(
            line.split("%", 1)[0] for line in FIXTURE_SOURCE.splitlines())
        level = 0
        for character in fixture_code:
            if character == "{":
                level += 1
            elif character == "}":
                level -= 1
                self.assertGreaterEqual(level, 0)
        self.assertEqual(level, 0)
        self.assertEqual(len(re.findall(r"(?<!\\)\$", fixture_code)) % 2, 0)
        begins = re.findall(r"\\begin\{([^{}]+)\}", fixture_code)
        ends = re.findall(r"\\end\{([^{}]+)\}", fixture_code)
        self.assertEqual(sorted(begins), sorted(ends))

    def test_source_braces_are_balanced(self):
        level = 0
        for char in CODE:
            if char == "{":
                level += 1
            elif char == "}":
                level -= 1
                self.assertGreaterEqual(level, 0)
        self.assertEqual(level, 0)


class DirectionPolicyModelTests(unittest.TestCase):
    def test_presentation_map_is_total_disjoint_and_involutive(self):
        self.assertEqual(len(PRESENTATION_MIRROR), 2 * len(PRESENTATION_PAIRS))
        self.assertTrue(set(PRESENTATION_MIRROR).isdisjoint(ENGINE_FENCE_MIRROR))
        for token, mate in PRESENTATION_MIRROR.items():
            self.assertNotEqual(token, mate)
            self.assertEqual(PRESENTATION_MIRROR[mate], token)
        self.assertTrue(INVARIANT.isdisjoint(PRESENTATION_MIRROR))

    def test_simple_row_keeps_source_and_mirrors_once(self):
        source = ("A", r"\rightarrow", "B")
        self.assertEqual(visual_row(source), ("B", r"\leftarrow", "A"))
        self.assertEqual(source, ("A", r"\rightarrow", "B"))
        self.assertEqual(visual_row(visual_row(source)), source)
        self.assertEqual(visual_row(source, "ltr"), source)

    def test_relation_and_engine_owned_fence_row(self):
        source = ("(", "x", r"\in", "A", ")")
        self.assertEqual(visual_row(source), ("(", "A", r"\ni", "x", ")"))

    def test_fraction_keeps_vertical_roles_and_transforms_subrows(self):
        fraction = Fraction(("a", "+", "b"), ("c", r"\rightarrow", "d"))
        self.assertEqual(fraction.rtl_visual(), {
            "above": ("b", "+", "a"),
            "below": ("d", r"\leftarrow", "c"),
        })
        self.assertEqual(fraction.numerator, ("a", "+", "b"))
        self.assertEqual(fraction.denominator, ("c", r"\rightarrow", "d"))

    def test_scripts_remain_attached_and_each_sublist_has_rtl_order(self):
        scripted = Scripted("A", ("n", "+", "1"), ("i", r"\in", "I"))
        self.assertEqual(scripted.rtl_visual(), {
            "nucleus": "A", "script_side": "visual-left",
            "superscript": ("1", "+", "n"),
            "subscript": ("I", r"\ni", "i"),
        })

    def test_rows_change_without_vertical_or_topological_reordering(self):
        rows = (("a11", "a12", "a13"), ("a21", "a22", "a23"))
        self.assertEqual(tuple(visual_row(row) for row in rows),
                         (("a13", "a12", "a11"), ("a23", "a22", "a21")))
        premises = ("P1", "P2", "P3")
        self.assertEqual(tuple(reversed(premises)), ("P3", "P2", "P1"))
        self.assertEqual(premises, ("P1", "P2", "P3"))


if __name__ == "__main__":
    unittest.main()
