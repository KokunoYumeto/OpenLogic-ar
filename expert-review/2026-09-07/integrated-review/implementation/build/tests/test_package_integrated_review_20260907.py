"""Small adversarial packaging checks; no production package/network mutation."""
import csv
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import warnings
import zipfile

from build import package_integrated_review_20260907 as package


class PackagingTests(unittest.TestCase):
    def test_scope_rejects_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                package.safe_child(root, "../outside")
            self.assertEqual(package.safe_child(root, "inside"), root / "inside")

    def test_exact_zip_streamed_and_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            public = root / "public"
            public.mkdir()
            (public / "words.txt").write_text("أ 𝔳̅ ≥\n", encoding="utf-8")
            self.assertEqual(package.exact_zip(root / "one.zip", public), 1)
            package.exact_zip(root / "two.zip", public)
            self.assertEqual(package.digest(root / "one.zip"), package.digest(root / "two.zip"))

    def test_zip_rejects_duplicates_extras_missing_and_changed_bytes(self):
        expected = {"item": {"bytes": 1, "sha256": hashlib.sha256(b"x").hexdigest()}}
        with tempfile.TemporaryDirectory() as directory:
            for index, members in enumerate(([('item', b'x'), ('item', b'x')], [('item', b'x'), ('extra', b'y')], [], [('item', b'y')])):
                archive = Path(directory) / f"{index}.zip"
                with zipfile.ZipFile(archive, "w") as output, warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    for name, body in members:
                        output.writestr(name, body)
                with self.assertRaises(ValueError):
                    package.verify_zip(archive, expected)

    def test_links_require_references_anchors_and_valid_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.tex"
            source.write_text("one\ntwo\n", encoding="utf-8")
            target = root / "readme.md"
            good = '<a id="decision-one"></a>\n[x](#decision-one)\n[y][ref]\n[ref]: source.tex#L1-L2\n'
            target.write_text(good, encoding="utf-8")
            self.assertEqual(package.check_links(good, target, root, {}), 2)
            for bad in (good.replace("L1-L2", "L0-L2"), good.replace("L1-L2", "L1-L3"), good.replace("(#decision-one)", "(#absent)"), good.replace("[y][ref]", "[y][missing]"), good.replace("source.tex", "../source.tex")):
                with self.assertRaises(ValueError):
                    package.check_links(bad, target, root, {})

    def test_gzip_is_streamed_deterministic_and_keeps_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "index.json"
            body = '{"status":"proposed-unapplied","rationale":"أ ≥ 𝔳̅"}\n'
            source.write_text(body, encoding="utf-8")
            with patch.object(Path, "read_bytes", side_effect=AssertionError("whole-file allocation")):
                package.stream_gzip(source, root / "one.gz")
                package.stream_gzip(source, root / "two.gz")
            self.assertEqual(package.digest(root / "one.gz"), package.digest(root / "two.gz"))
            with gzip.open(root / "one.gz", "rt", encoding="utf-8") as compressed:
                self.assertEqual(compressed.read(), body)

    def test_proposals_are_derived_from_raw_exact_status(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "index.json"
            rows = [{"decision_id": f"P-{n}", "status": "proposed-unapplied"} for n in range(7)]
            rows.append({"decision_id": "applied", "status": "applied"})
            source.write_text(json.dumps({"decisions": rows, "end": 1}, indent=2), encoding="utf-8")
            self.assertEqual(package.proposal_ids(source), {f"P-{n}" for n in range(7)})
            rows[-1]["status"] = "proposed-unapplied"
            source.write_text(json.dumps({"decisions": rows, "end": 1}, indent=2), encoding="utf-8")
            with self.assertRaises(ValueError):
                package.proposal_ids(source)

    def test_proposal_sections_summary_and_reason_preserved(self):
        body = '| [sense](#decision-p-1) | word |\n<a id="decision-p-1"></a>\n### sense\n\n- **ID / الرقم:** `P-1`\n- **Why:** exact ≥ wording\n\n- **ID / الرقم:** `P-2`\n- **Why:** leave alone\n'
        rendered, receipt = package.annotate_proposals(body, {"P-1"})
        self.assertEqual(receipt, {"sections": {"P-1": 1}, "summaries": {"P-1": 1}})
        self.assertIn(package.PROPOSAL_NOTE + '\n- **Why:** exact ≥ wording', rendered)
        self.assertIn('`P-2`\n- **Why:** leave alone', rendered)
        self.assertEqual(rendered.replace("\n- " + package.PROPOSAL_NOTE, "").replace(" " + package.PROPOSAL_SHORT, ""), body)

    def test_hashed_relative_summary_and_trailing_spaces_are_reversible(self):
        body = '| [sense](complete-001.md#complete-p-1-cb28eeb0d4) |\n- **ID / الرقم:** `P-1`  \n- **Why:** untouched\n'
        rendered, receipt = package.annotate_proposals(body, {"P-1"})
        self.assertEqual(receipt, {"sections": {"P-1": 1}, "summaries": {"P-1": 1}})
        self.assertEqual(rendered.replace("\n- " + package.PROPOSAL_NOTE, "").replace(" " + package.PROPOSAL_SHORT, ""), body)

    def test_csv_labels_every_proposal_occurrence_without_changing_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, target = root / "old.csv", root / "new.csv"
            original = [["priority", "Decision ID / رقم القرار", "reason"], ["flag", "P-1", "أ ≥,\nwhy"], ["flag", "P-1", "second"], ["normal", "other", "keep"]]
            with source.open("w", encoding="utf-8-sig", newline="") as out:
                csv.writer(out).writerows(original)
            self.assertEqual(package.project_csv(source, target, {"P-1"}), {"P-1": 2})
            with target.open(encoding="utf-8-sig", newline="") as readback:
                projected = list(csv.reader(readback))
            self.assertEqual([row[:-1] for row in projected], original)
            self.assertTrue(all(row[-1].startswith("proposed-unapplied") for row in projected[1:3]))
            self.assertEqual(projected[-1][-1], "")
            with self.assertRaises(ValueError):
                package.project_csv(source, root / "missing.csv", {"P-1", "absent"})


if __name__ == "__main__":
    unittest.main()
