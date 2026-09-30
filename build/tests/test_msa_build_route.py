"""Static, non-TeX safety checks for the fresh MSA acceptance route."""

from pathlib import Path
import re
import sys
import tempfile
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import profile_checkpoint


ROOT = Path(__file__).resolve().parents[2]


class MsaBuildRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wrapper = (ROOT / "build/BUILD_DUAL_NOTATION.ps1").read_text(
            encoding="utf-8"
        )
        cls.inner = (ROOT / "build/BUILD_DUAL_NOTATION_INNER.ps1").read_text(
            encoding="utf-8"
        )
        cls.renderer = (ROOT / "build/render_r3_samples.py").read_text(
            encoding="utf-8"
        )
        cls.checkpoint = (ROOT / "build/profile_checkpoint.py").read_text(
            encoding="utf-8"
        )

    def test_output_and_work_roots_are_explicit(self):
        for parameter in ("FinalOutputDirectory", "WorkDirectory"):
            pattern = (
                r"\[Parameter\(Mandatory\s*=\s*\$true\)\]\s*"
                r"\[ValidateNotNullOrEmpty\(\)\]\s*\[string\]\$"
                + parameter
            )
            self.assertRegex(self.wrapper, pattern)

    def test_roots_are_distinct_and_stale_tree_is_rejected(self):
        self.assertIn("distinct and non-nested", self.wrapper)
        self.assertIn("complete-722-r3-final-olsiz", self.wrapper)
        self.assertGreaterEqual(self.wrapper.count("Test-PathIsSameOrNested"), 4)

    def test_single_machine_wide_mutex_wraps_inner_build(self):
        self.assertIn("Invoke-WithInterlanguageTeXMutex.ps1", self.wrapper)
        self.assertIn('"TEX_MUTEX_RECEIPT.json"', self.wrapper)
        self.assertIn("-CommandArguments $arguments", self.wrapper)
        self.assertNotIn("lualatex", self.wrapper.lower())
        self.assertIn("Push-Location $releaseRoot", self.wrapper)

    def test_source_audit_precedes_first_tex_pass(self):
        audit_call = self.inner.index("& python $sourceAuditScript")
        profile_loop = self.inner.index("foreach ($profile in $profiles)", audit_call)
        first_runtime_tex = self.inner.index(
            "& lualatex @latexArguments $profile.ReaderDriver", profile_loop
        )
        self.assertLess(audit_call, first_runtime_tex)
        for token in (
            "--manifest $closureManifest",
            "--mapping $profileMapping",
            '"SOURCE_PROFILE_AUDIT.json"',
            '"rebind_msa_closure_manifest.py"',
            "MSA_CLOSURE_MANIFEST_REBIND_20260930_FORMULA_ANNOTATED.json",
            "SOL6_PROOF_QUANTIFICATION_RECHECK_20260930.json",
            "--successor-ledger $msaSuccessorLedger",
            '--action verify',
        ):
            self.assertIn(token, self.inner)

    def test_only_work_root_may_contain_guard_receipt_at_entry(self):
        self.assertIn("$isWorkDirectory", self.inner)
        self.assertIn(
            '$isWorkDirectory -and $_.Name -eq "TEX_MUTEX_RECEIPT.json"',
            self.inner,
        )

    def test_synctex_and_recorder_are_retained(self):
        match = re.search(r"\$latexArguments\s*=\s*@\((.*?)\n\)", self.inner, re.S)
        self.assertIsNotNone(match)
        arguments = match.group(1)
        self.assertIn('"-synctex=1"', arguments)
        self.assertIn('"-recorder"', arguments)

    def test_arabic_reference_lists_localize_all_seven_separators(self):
        locale = (ROOT / "source/locale/ar/open-logic-locale.sty").read_text(encoding="utf-8")
        hook = locale.split(r"\addto\extrasarabic{", 1)[1].split("\n}", 1)[0]
        for name, body in (
            ("crefrangeconjunction", r" إلى\nobreakspace"),
            ("crefpairconjunction", r" و\nobreakspace"),
            ("crefmiddleconjunction", "، "),
            ("creflastconjunction", r"، و\nobreakspace"),
            ("crefpairgroupconjunction", r" و\nobreakspace"),
            ("crefmiddlegroupconjunction", "، "),
            ("creflastgroupconjunction", r"، و\nobreakspace"),
        ):
            self.assertIn("\\def\\" + name + "{" + body + "}", hook)
        for name in ("enumi", "enumii", "enumiii", "enumiv"):
            self.assertIn("\\crefname{" + name + "}{بند}{بنود}", hook)
            self.assertIn("\\Crefname{" + name + "}{بند}{بنود}", hook)

    def test_render_output_must_be_fresh_and_inventory_is_hash_bound(self):
        self.assertIn("render output directory must be empty", self.renderer)
        self.assertRegex(self.renderer, r'"pdf_sha256"\s*:\s*digest')
        self.assertRegex(self.renderer, r'"png_sha256"\s*:\s*sha256\(png\)')
        self.assertRegex(self.renderer, r'"png_bytes"\s*:\s*png\.stat\(\)\.st_size')

    def test_checkpoint_validation_cannot_be_disabled_with_python_optimization(self):
        executable_lines = [
            line
            for line in self.checkpoint.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertFalse(
            any(re.match(r"\s*assert\b", line) for line in executable_lines)
        )
        self.assertIn("def require(condition, message):", self.checkpoint)
        self.assertIn("incomplete checkpoint file inventory", self.checkpoint)

    def test_converged_checkpoint_retains_exact_source_raw_and_state(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            job = "open-logic-complete-ar-readable-letter-international"
            (work / (job + ".pdf")).write_bytes(b"compiled-PDF")
            (work / (job + ".aux")).write_bytes(b"exact-state")
            log = "Output written on\nPDF statistics:\nOL-NOTATION-PROFILE=international\nOL-NOTATION-FORMULA-DIRECTION=LTR\n"
            (work / (job + ".log")).write_text(log, encoding="utf-8")
            args = SimpleNamespace(work=work, role="reader", profile="international", action="compiled-record")
            profile_checkpoint.compiled_checkpoint(args, "A" * 64)
            (work / (job + ".pdf")).rename(work / (job + ".raw-before-link-repair.pdf"))
            args.action = "compiled-verify"
            profile_checkpoint.compiled_checkpoint(args, "A" * 64)
            with self.assertRaisesRegex(ValueError, "stale converged"):
                profile_checkpoint.compiled_checkpoint(args, "B" * 64)
            (work / (job + ".aux")).write_bytes(b"changed-state")
            with self.assertRaisesRegex(ValueError, "converged state changed"):
                profile_checkpoint.compiled_checkpoint(args, "A" * 64)
            (work / (job + ".aux")).write_bytes(b"exact-state")
            (work / (job + ".raw-before-link-repair.pdf")).write_bytes(b"changed-PDF")
            with self.assertRaisesRegex(ValueError, "converged raw PDF changed"):
                profile_checkpoint.compiled_checkpoint(args, "A" * 64)
            args.action = "compiled-record"
            (work / (job + ".log")).write_text(log + "Missing character:\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Missing character"):
                profile_checkpoint.compiled_checkpoint(args, "A" * 64)


if __name__ == "__main__":
    unittest.main()
