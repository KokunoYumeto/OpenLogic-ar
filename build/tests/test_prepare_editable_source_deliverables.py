"""Focused non-TeX tests for the three editable-source deliverables."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest
import zipfile


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import prepare_editable_source_deliverables as sources


class EditableSourceDeliverableTests(unittest.TestCase):
    def test_v5_namespace_is_bound_to_the_accepted_classical_authorities(self) -> None:
        self.assertEqual(
            sources.EXPECTED_RECONCILIATION_SHA256,
            "7efe0a46648cff60f0f179c98ab01d948630bfe4b7dd944f0f8061b728c18ef1",
        )
        self.assertEqual(
            sources.EXPECTED_PRESENTATION_SHA256,
            "a3817d79ed98a104594c9db428f72a0c590162dfed02c59a3d2c47bf69a7a5a4",
        )
        self.assertEqual(
            sources.EXPECTED_CLASSICAL_SOURCE_TREE_SHA256,
            "F6590340CFD3B0FC291A535BCF124849AEA8DF08F45FA6DAE59FE7FF061DCA4F",
        )
        self.assertEqual(
            sources.EXPECTED_CLASSICAL_PRESENTATION_TREE_SHA256,
            "B6D83898A2F648C149E15BC485F52A047F8302ABB390A28A1187FC79BB85FB37",
        )

    def test_release_surface_is_exactly_six_and_within_inherited_cap(self) -> None:
        self.assertEqual(tuple(sources.ROLE_STEMS), sources.ROLE_ORDER)
        self.assertEqual(sources.NEW_RELEASE_FILES, 2 * len(sources.ROLE_ORDER))
        self.assertEqual(sources.MAX_NEW_FILES, 29)
        self.assertLessEqual(sources.NEW_RELEASE_FILES, sources.MAX_NEW_FILES)
        self.assertLessEqual(
            sources.INHERITED_ZENODO_FILES + sources.NEW_RELEASE_FILES,
            sources.ZENODO_FILE_CAP,
        )

    def test_current_msa_scope_is_explicit_finite_and_restores_legacy_defaults(self):
        original = (sources.ROLE_ORDER, sources.GRAPH_ROOT, sources.RECONCILIATION,
                    sources.MSA_REBIND, sources.NEW_RELEASE_FILES, sources.MSA_EVIDENCE_FILES)
        with sources.current_msa_scope():
            self.assertEqual(sources.ROLE_ORDER, ("msa-international", "msa-machrek"))
            self.assertEqual(sources.NEW_RELEASE_FILES, 4)
            self.assertEqual(len(sources._expected_graph_paths()), 4)
            self.assertEqual(sources.RECONCILIATION, sources.CURRENT_MSA_MANIFEST)
            self.assertNotEqual(sources.GRAPH_ROOT, original[1])
            self.assertIn(sources.CURRENT_MSA_REBIND, sources.MSA_EVIDENCE_FILES)
            self.assertIn(sources.CURRENT_REFERENCE_LEDGER, sources.MSA_EVIDENCE_FILES)
            self.assertNotIn(sources.ACCEPTANCE, sources.MSA_EVIDENCE_FILES)
        self.assertEqual(original, (sources.ROLE_ORDER, sources.GRAPH_ROOT, sources.RECONCILIATION,
                                  sources.MSA_REBIND, sources.NEW_RELEASE_FILES, sources.MSA_EVIDENCE_FILES))

    def test_arabic_instructions_identify_role_direct_tex_and_provenance(self) -> None:
        for role in sources.ROLE_ORDER:
            name = f"{sources.ROLE_STEMS[role]}.tex"
            text = sources._build_instructions(role, name).decode("utf-8")
            self.assertIn(role, text)
            self.assertIn(name, text)
            self.assertIn("٧٢٢ = ٦٤٢ + ٨٠", text)
            self.assertIn("Global\\InterlanguageTeXSlotV1", text)
            self.assertIn(sources.GRAPH_ROOT, text)
            self.assertNotIn("editable-source-deliverables-20260922", text)
            self.assertIn(sources.AI_DISCLOSURE, text)
            self.assertIn(sources.AI_INHERITED_DISCLOSURE, text)
            self.assertNotIn("PLACEHOLDER", text)

    def test_classical_graph_support_does_not_admit_msa_content(self) -> None:
        files = sources._role_graph_support("classical-eastern-rtl")
        self.assertIn(
            "source/locale/ar/fonts/vendor/xits-1.302/XITSMath-Regular.otf",
            files,
        )
        self.assertIn(
            "source/locale/ar/open-logic-readable-letter-r2-layout-ar.tex", files
        )
        self.assertFalse(
            any(path.startswith("source/locale/ar/content/") for path in files)
        )

    def test_deterministic_zip_has_fixed_order_time_mode_and_bytes(self) -> None:
        members = {
            "zeta.txt": "زيتا\n".encode("utf-8"),
            "alpha.txt": b"alpha\n",
            "nested/beta.txt": b"beta\n",
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "first.zip"
            second = root / "second.zip"
            sources._write_zip(first, "ROOT", members)
            sources._write_zip(second, "ROOT", members)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first, "r") as archive:
                infos = archive.infolist()
                self.assertEqual(
                    [item.filename for item in infos],
                    [
                        "ROOT/alpha.txt",
                        "ROOT/nested/beta.txt",
                        "ROOT/zeta.txt",
                    ],
                )
                self.assertTrue(all(item.date_time == sources.FIXED_ZIP_TIME for item in infos))
                self.assertTrue(
                    all((item.external_attr >> 16) == sources.ZIP_MODE for item in infos)
                )

    def test_source_lists_exclude_cache_and_work_trees(self) -> None:
        combined = (
            *sources.MSA_SOURCE_SUPPORT,
            *sources.CLASSICAL_SOURCE_SUPPORT,
            *sources.COMMON_BUILD_FILES,
            *sources.MSA_EVIDENCE_FILES,
            *sources.CLASSICAL_EVIDENCE_FILES,
        )
        for path in combined:
            self.assertFalse(path.startswith(("tmp/", "output/", ".git/")), path)
            self.assertNotIn("cache", path.casefold())


if __name__ == "__main__":
    unittest.main()
