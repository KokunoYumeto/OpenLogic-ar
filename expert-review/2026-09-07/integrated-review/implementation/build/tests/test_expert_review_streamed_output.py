"""Byte fidelity and failed-stage preservation for the bounded index writer."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from build import generate_expert_review_index as index


class StreamedOutput(unittest.TestCase):
    def write(self, root, payload):
        index.write_outputs(
            payload, "الاختيار\ntext\n", "Start\n", "Priority\n", "أ,≥,𝔳̅\n",
            root / "index.json", root / "index.md", root / "start.md",
            root / "priority.md", root / "table.csv",
            {"README.md": "Navigation\n", "complete-001.md": "السبب\n"},
            root / "shards",
        )

    def test_exact_legacy_bytes_without_materialized_json(self):
        payload = {"z": ["𝔳̅", "أ", {"_hidden": Path("private"), "n": 3}],
                   "a": "line\nline", "_private": Path("not-json")}
        expected = (json.dumps(index.strip_private(payload), ensure_ascii=False,
                               indent=2, sort_keys=True) + "\n").encode("utf-8")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(index.json, "dumps", side_effect=AssertionError("whole JSON allocation")):
                self.write(root, payload)
            self.assertEqual((root / "index.json").read_bytes(), expected)
            self.assertEqual((root / "index.md").read_bytes(), "الاختيار\ntext\n".encode())
            self.assertEqual((root / "table.csv").read_bytes(), b"\xef\xbb\xbf" + "أ,≥,𝔳̅\n".encode())
            self.assertEqual((root / "shards/complete-001.md").read_bytes(), "السبب\n".encode())
            self.assertFalse(list(root.rglob("*.tmp")))

    def test_failed_json_stage_preserves_every_previous_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, {"old": "data"})
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            with self.assertRaises(TypeError):
                self.write(root, {"cannot_encode": object()})
            after = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            self.assertEqual(before, after)

    def test_only_obsolete_generated_shards_are_removed_after_success(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shards = root / "shards"
            shards.mkdir()
            (shards / "complete-999.md").write_text("old", encoding="utf-8")
            (shards / "human-note.md").write_text("keep", encoding="utf-8")
            self.write(root, {"current": True})
            self.assertFalse((shards / "complete-999.md").exists())
            self.assertEqual((shards / "human-note.md").read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
