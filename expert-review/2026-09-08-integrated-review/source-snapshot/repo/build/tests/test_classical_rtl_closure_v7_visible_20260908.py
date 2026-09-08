"""Adversarial v7 consumer tests using actual PDFs without launching TeX.

Temporary receipt layouts are synthetic. Their PDF bytes are preserved actual
probe artifacts, not newly rendered or certified readers.
"""

from __future__ import annotations

import copy
import os
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest import mock

from build.tests.test_classical_rtl_closure_receipt import (
    CURRENT, ROOT, ReceiptFixture, lower_identity, upper_identity,
    validator, write_json,
)


OLD_V6 = ROOT / "evidence/classical/RTL_MATH_PROBE_V6_OWNER_20260907.json"
HISTORY = ROOT / "evidence/classical/rtl-history/before-v7-reader-gate-20260908"


class V7VisibleReadbackTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.fixture = ReceiptFixture(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_predecessor_files_preserved_byte_for_byte(self):
        expected = {
            "validate_classical_rtl_closure_receipt.py":
                "DA3FB9639A10ED7F376ED6360848683FCAABFFE4D15C6F91DD2DE23F8D1E7552",
            "test_classical_rtl_closure_receipt.py":
                "B3B85E91213C244ED6D91AFC7E54AF4BA17C2FEDB542C11C1A5033BE830AD271",
        }
        for name, digest in expected.items():
            self.assertEqual(validator.sha256(HISTORY / name), digest)

    def test_forged_face_order_inventory_and_boolean_types_are_rejected(self):
        original = copy.deepcopy(self.fixture.payload)
        mutations = (
            lambda a: a.pop("visible_semantic_checks"),
            lambda a: a["visible_semantic_checks"].pop(),
            lambda a: a["visible_semantic_checks"].append(
                copy.deepcopy(a["visible_semantic_checks"][0])),
            lambda a: a["visible_semantic_checks"][0].__setitem__("observed", "("),
            lambda a: a["visible_semantic_checks"][0].__setitem__("expected", "("),
            lambda a: a["visible_semantic_checks"][0].update(
                observed="(", expected="(", **{"pass": True}),
            lambda a: a["visible_semantic_checks"][8].update(
                observed="A\u2190B", expected="A\u2190B", **{"pass": True}),
            lambda a: a["visible_semantic_checks"][0].__setitem__("key", "forged"),
            lambda a: a["visible_semantic_checks"][0].__setitem__("kind", "forged"),
            lambda a: a["visible_semantic_checks"][0].__setitem__("pass", 1),
        )
        for index, mutate in enumerate(mutations):
            with self.subTest(mutation=index):
                self.fixture.payload = copy.deepcopy(original)
                mutate(self.fixture.payload["artifacts"]["primary"]["rtl"])
                self.fixture.write_receipt()
                with self.assertRaisesRegex(validator.ValidationError,
                                            "primary/rtl PDF facts"):
                    validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_replay_only_visible_fact_forgery_is_rejected(self):
        self.fixture.payload["artifacts"]["replay"]["rtl"][
            "visible_semantic_checks"
        ][8]["observed"] = "A\u2190B"
        self.fixture.write_receipt()
        with self.assertRaisesRegex(validator.ValidationError, "replay/rtl PDF facts"):
            validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_actual_defective_v6_pdfs_cannot_masquerade_as_v7_with_updated_hashes(self):
        old = validator.read_json(OLD_V6)
        old_directory = Path(old["build_manifests"]["primary"]["path"]).parent
        # Bind the old actual RTL PDF in BOTH runs, including refreshed file,
        # manifest and recorded artifact identities. No hash/schema mismatch
        # may be the reason this adversarial fixture fails.
        for run in ("primary", "replay"):
            manifest_path = self.fixture.manifests[run]
            manifest = validator.read_json(manifest_path)
            target = manifest_path.parent / "rtl.pdf"
            target.write_bytes((old_directory / "rtl.pdf").read_bytes())
            guarded_time = validator.utc("2026-09-05T00:00:05Z", "fixture").timestamp()
            os.utime(target, (guarded_time, guarded_time))
            manifest["Jobs"]["rtl"]["Outputs"] = [
                upper_identity(target, target.name) if row["Path"] == "rtl.pdf" else row
                for row in manifest["Jobs"]["rtl"]["Outputs"]
            ]
            write_json(manifest_path, manifest)
            os.utime(manifest_path, (guarded_time, guarded_time))
            self.fixture.payload["build_manifests"][run] = lower_identity(manifest_path, "path")
            self.fixture.payload["artifacts"][run]["rtl"].update(
                bytes=target.stat().st_size, sha256=validator.sha256(target))
        self.fixture.write_receipt()
        with self.assertRaisesRegex(validator.ValidationError,
                                    "v7 bound-artifact readback failed: stable operand/fence/tag extraction"):
            validator.validate_receipt(ROOT, self.fixture.receipt)

    def test_consumer_recomputes_visible_checks_from_pdf_not_recorded_anchors(self):
        contract = validator.load_readback_contract(ROOT)
        with mock.patch.object(contract, "visible_semantic_checks",
                               wraps=contract.visible_semantic_checks) as check:
            with mock.patch.object(validator, "load_readback_contract", return_value=contract):
                result = validator.validate_receipt(ROOT, self.fixture.receipt)
        self.assertEqual([call.args[2] for call in check.call_args_list], ["control", "rtl"])
        self.assertEqual(result["visible_semantic_checks_recomputed"],
                         {"control": 14, "rtl": 14})
        for call in check.call_args_list:
            job = call.args[2]
            self.assertIsNot(call.args[1],
                             self.fixture.payload["artifacts"]["primary"][job]["geometry_anchors"])

    def test_same_schema_unpinned_producer_is_rejected(self):
        real_sha256 = validator.sha256
        producer = ROOT / "build/qa_classical_rtl_math_probe.py"

        def forged(path):
            return "0" * 64 if path == producer else real_sha256(path)

        with mock.patch.object(validator, "sha256", side_effect=forged):
            with self.assertRaisesRegex(validator.ValidationError, "unsupported v7 producer contract hash"):
                validator.load_readback_contract(ROOT)

    def test_actual_glyph_order_coincidence_and_extra_glyph_are_rejected(self):
        contract = validator.load_readback_contract(ROOT)
        receipt = validator.read_json(CURRENT)
        row = receipt["artifacts"]["primary"]["rtl"]
        pdf = Path(receipt["build_manifests"]["primary"]["path"]).parent / "rtl.pdf"
        self.assertEqual(validator.sha256(pdf), row["sha256"])
        with contract.pdfplumber.open(pdf) as original:
            pages = [SimpleNamespace(height=page.height, chars=copy.deepcopy(page.chars))
                     for page in original.pages]
        document = SimpleNamespace(pages=pages)
        anchors = row["geometry_anchors"]
        self.assertTrue(all(c["pass"] for c in contract.visible_semantic_checks(document, anchors, "rtl")))
        selected = [anchors["P11-root-" + suffix] for suffix in ("A", "op", "B")]
        x0, y0 = min(r["rect"][0] for r in selected), min(r["rect"][1] for r in selected)
        x1, y1 = max(r["rect"][2] for r in selected), max(r["rect"][3] for r in selected)
        page = pages[selected[0]["page"] - 1]
        top, bottom = float(page.height) - y1, float(page.height) - y0
        chars = [c for c in page.chars if c["text"] in ("A", "B", "\u2190")
                 and x0 <= (c["x0"] + c["x1"]) / 2 <= x1
                 and top <= (c["top"] + c["bottom"]) / 2 <= bottom]
        self.assertEqual(sorted(c["text"] for c in chars), ["A", "B", "\u2190"])
        a, b = next(c for c in chars if c["text"] == "A"), next(c for c in chars if c["text"] == "B")
        original_chars = copy.deepcopy(page.chars)

        # The annotation boxes and mirrored operator remain unchanged.
        a["x0"], b["x0"] = b["x0"], a["x0"]
        a["x1"], b["x1"] = b["x1"], a["x1"]
        checks = contract.visible_semantic_checks(document, anchors, "rtl")
        self.assertFalse(next(c for c in checks if c["key"] == "P11-root")["pass"])

        page.chars = copy.deepcopy(original_chars)
        for c in page.chars:
            if x0 <= (c["x0"] + c["x1"]) / 2 <= x1 and top <= (c["top"] + c["bottom"]) / 2 <= bottom:
                c["x0"], c["x1"] = x0, x1
        checks = contract.visible_semantic_checks(document, anchors, "rtl")
        self.assertFalse(next(c for c in checks if c["key"] == "P11-root")["pass"])

        page.chars = copy.deepcopy(original_chars)
        page.chars.append(copy.deepcopy(chars[0]))
        checks = contract.visible_semantic_checks(document, anchors, "rtl")
        self.assertFalse(next(c for c in checks if c["key"] == "P11-root")["pass"])


if __name__ == "__main__":
    unittest.main()
