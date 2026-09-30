from __future__ import annotations

import csv
import copy
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "rebind_msa_closure_manifest.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("rebind_msa", SCRIPT)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MOD
SPEC.loader.exec_module(MOD)


class MSARebindTests(unittest.TestCase):
    def successor_fixture(self, root: Path):
        repo, manifest, authority, receipt = self.fixture(root)
        real = SCRIPT.parents[1]
        closure = MOD.load_json(authority)
        original = MOD.load_json(real / MOD.DEFAULT_AUTHORITY)["units"][86]
        closure["units"][86] = copy.deepcopy(original)
        authority.write_text(json.dumps(closure), encoding="utf-8")
        fields, rows = MOD.read_csv(manifest.read_bytes())
        rows[0]["ar_sha256"] = closure["units"][0]["msa"]["sha256"]
        rows[86].update(source_path=original["source_path"],
                        source_sha256=original["english_sha256"],
                        ar_target_path=MOD.PROOF_SOURCE.removeprefix("source/"),
                        ar_sha256=MOD.PROOF_BEFORE[1])
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=fields, quoting=csv.QUOTE_ALL, lineterminator="\r\n")
        writer.writeheader(); writer.writerows(rows)
        manifest.write_bytes(stream.getvalue().encode("utf-8"))
        for relative in (MOD.PROOF_LEDGER, MOD.PROOF_SOURCE, MOD.PROOF_CLASSICAL):
            target = repo / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(real / relative, target)
        return repo, manifest, authority, repo / MOD.PROOF_LEDGER, repo / "new-rebind.json"

    def fixture(self, root: Path):
        repo = root / "repo"
        manifest = repo / MOD.DEFAULT_MANIFEST
        authority = repo / MOD.DEFAULT_AUTHORITY
        receipt = repo / MOD.DEFAULT_RECEIPT
        units = []
        rows = []
        fields = [
            "closure_id", "stable_order", "source_path", "source_sha256",
            "ar_target_path", "ar_status", "ar_sha256", "ar_qa",
            "fa_IR_target_path", "fa_IR_status", "fa_IR_sha256", "fa_IR_qa",
        ]
        for number in range(1, 723):
            unit_id = f"OLP-{number:04d}"
            rel = f"content/u{number:04d}.tex"
            msa_rel = f"source/locale/ar/{rel}"
            source_hash = f"{number:064x}"[-64:]
            live = repo / msa_rel
            live.parent.mkdir(parents=True, exist_ok=True)
            live.write_text(f"وحدة {number}\n", encoding="utf-8")
            data = live.read_bytes()
            digest = MOD.sha256_bytes(data)
            units.append({
                "id": unit_id, "source_path": rel, "english_sha256": source_hash,
                "msa": {"path": msa_rel, "sha256": digest.lower(), "bytes": len(data)},
            })
            rows.append({
                "closure_id": unit_id, "stable_order": str(number),
                "source_path": rel, "source_sha256": source_hash,
                "ar_target_path": msa_rel.removeprefix("source/"),
                "ar_status": "ACCEPTED",
                "ar_sha256": (
                    "A" * 64 if number == 1 else
                    digest.lower() if number == 2 else
                    digest
                ),
                "ar_qa": "PASS", "fa_IR_target_path": f"locale/fa-IR/{rel}",
                "fa_IR_status": "ACCEPTED", "fa_IR_sha256": "B" * 64,
                "fa_IR_qa": "PRESERVE EXACTLY",
            })
        manifest.parent.mkdir(parents=True, exist_ok=True)
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=fields, quoting=csv.QUOTE_ALL, lineterminator="\r\n")
        writer.writeheader(); writer.writerows(rows)
        manifest.write_bytes(stream.getvalue().encode("utf-8"))
        authority.parent.mkdir(parents=True, exist_ok=True)
        authority.write_text(json.dumps({
            "schema": "openlogic-classical-source-closure-manifest-v1",
            "status": "PASS", "total_units": 722,
            "source_snapshot_sha256": "C" * 64, "units": units,
        }), encoding="utf-8")
        return repo, manifest, authority, receipt

    def test_write_changes_only_stale_ar_hash_and_verify_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest, authority, receipt = self.fixture(Path(tmp))
            before_fields, before_rows = MOD.read_csv(manifest.read_bytes())
            result = MOD.derive(repo, manifest, authority)
            self.assertEqual([row["id"] for row in result["changed"]], ["OLP-0001"])
            payload = MOD.receipt_payload(repo, manifest, authority, result)
            manifest.write_bytes(result["after"])
            receipt.parent.mkdir(parents=True, exist_ok=True)
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            MOD.verify_receipt(repo, manifest, authority, receipt)
            after_fields, after_rows = MOD.read_csv(manifest.read_bytes())
            self.assertEqual(before_fields, after_fields)
            for before, after in zip(before_rows, after_rows):
                self.assertEqual(
                    {k: v for k, v in before.items() if k != "ar_sha256"},
                    {k: v for k, v in after.items() if k != "ar_sha256"},
                )
            self.assertEqual(before_rows[0]["fa_IR_qa"], after_rows[0]["fa_IR_qa"])
            self.assertEqual(before_rows[1]["ar_sha256"], after_rows[1]["ar_sha256"])

    def test_live_source_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest, authority, _ = self.fixture(Path(tmp))
            (repo / "source/locale/ar/content/u0002.tex").write_text("drift\n", encoding="utf-8")
            with self.assertRaisesRegex(MOD.RebindError, "does not match live bytes"):
                MOD.derive(repo, manifest, authority)

    def test_duplicate_authority_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest, authority, _ = self.fixture(Path(tmp))
            authority.write_text('{"schema":"x","schema":"y"}', encoding="utf-8")
            with self.assertRaisesRegex(MOD.RebindError, "duplicate JSON key"):
                MOD.derive(repo, manifest, authority)

    def test_successor_changes_one_cell_preserving_historical_closure(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest, authority, ledger, receipt = self.successor_fixture(Path(tmp))
            old_authority = authority.read_bytes()
            result = MOD.derive(repo, manifest, authority, ledger)
            self.assertEqual([r["id"] for r in result["changed"]], ["OLP-0087"])
            payload = MOD.receipt_payload(repo, manifest, authority, result)
            self.assertNotIn("all_live_msa_hashes_equal_canonical_closure", payload["invariants"])
            self.assertEqual(payload["msa_source_successor"]["ledger"]["sha256"], MOD.PROOF_LEDGER_SHA256)
            comparison = payload["msa_source_successor"]["cross_edition_comparison"]
            self.assertEqual(comparison["raw_status"], "flagged")
            self.assertEqual(comparison["previous_formula_segments"], 57)
            self.assertEqual(comparison["current_formula_segments"], 58)
            manifest.write_bytes(result["after"])
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            MOD.verify_receipt(repo, manifest, authority, receipt, ledger)
            self.assertEqual(authority.read_bytes(), old_authority)
            with self.assertRaisesRegex(MOD.RebindError, "does not match live bytes"):
                MOD.derive(repo, manifest, authority)

    def test_successor_rejects_extra_body_or_classical_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest, authority, ledger, _ = self.successor_fixture(Path(tmp))
            target = repo / MOD.PROOF_SOURCE
            original = target.read_bytes()
            target.write_bytes(original + b"% unsupported change\n")
            with self.assertRaisesRegex(MOD.RebindError, "current source drifted"):
                MOD.derive(repo, manifest, authority, ledger)
            target.write_bytes(original)
            target = repo / MOD.PROOF_CLASSICAL
            target.write_bytes(target.read_bytes() + b"% unsupported change\n")
            with self.assertRaisesRegex(MOD.RebindError, "counterpart changed"):
                MOD.derive(repo, manifest, authority, ledger)

    def test_successor_rejects_changed_ledger_other_unit_and_missing_receipt_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest, authority, ledger, receipt = self.successor_fixture(Path(tmp))
            original = ledger.read_bytes()
            ledger.write_bytes(original + b"\n")
            with self.assertRaisesRegex(MOD.RebindError, "ledger identity changed"):
                MOD.derive(repo, manifest, authority, ledger)
            ledger.write_bytes(original)
            result = MOD.derive(repo, manifest, authority, ledger)
            payload = MOD.receipt_payload(repo, manifest, authority, result)
            manifest.write_bytes(result["after"])
            payload.pop("msa_source_successor")
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(MOD.RebindError, "exact current MSA successor"):
                MOD.verify_receipt(repo, manifest, authority, receipt, ledger)
            target = repo / "source/locale/ar/content/u0002.tex"
            target.write_text("arbitrary drift\n", encoding="utf-8")
            with self.assertRaisesRegex(MOD.RebindError, "does not match live bytes"):
                MOD.derive(repo, manifest, authority, ledger)


if __name__ == "__main__":
    unittest.main()
