#!/usr/bin/env python3
"""Validate completed profile stages before reuse after an interrupted host call."""
import argparse
import hashlib
import json
from pathlib import Path
from qa_dual_notation_pdfs import EXPECTED_COMPONENT_LINKS, inspect, sha256


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key {key!r} in {path}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)

def source_identity(repo):
    # The independently written third-edition overlay is not an input of
    # either MSA driver. Do not invalidate reproducibility as it progresses.
    # All shared source, fonts and the complete ar locale remain covered.
    root = repo / "source"
    files = sorted(p for p in root.rglob("*") if p.is_file()
                   and p.relative_to(root).parts[:2] != ("locale", "ar-classical"))
    records = [(p.relative_to(repo).as_posix(), sha256(p)) for p in files]
    return hashlib.sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest().upper(), files

def compiled_checkpoint(args, digest):
    """Retain a converged TeX stage if only downstream PDF repair fails."""
    prefix = "open-logic-complete-ar" if args.role == "reader" else "open-logic-closure-supplement-ar"
    job = f"{prefix}-readable-letter-{args.profile}"
    receipt_path = args.work / (job + ".compiled-checkpoint.json")
    raw_name = job + ".raw-before-link-repair.pdf"
    extensions = ("aux", "bbl", "out", "pcr", "prb", "thm", "toc", "log", "fls")
    if args.action == "compiled-verify":
        receipt = read_json(receipt_path)
        require(receipt.get("schema") == "openlogic-converged-tex-stage-v1"
                and receipt.get("profile") == args.profile
                and receipt.get("role") == args.role
                and receipt.get("source_tree_sha256") == digest,
                "stale converged TeX checkpoint")
        require(sha256(args.work / raw_name) == receipt.get("raw_pdf_sha256"),
                "converged raw PDF changed")
        records = receipt.get("files", [])
        require(isinstance(records, list) and records
                and len({r.get("file") for r in records}) == len(records),
                "invalid converged state inventory")
        expected = {job + "." + ext for ext in extensions
                    if (args.work / (job + "." + ext)).is_file()}
        require({r.get("file") for r in records} == expected,
                "converged state inventory changed")
        for record in records:
            require(sha256(args.work / record["file"]) == record.get("sha256"),
                    f"converged state changed: {record['file']}")
    else:
        log = (args.work / (job + ".log")).read_text(encoding="utf-8", errors="replace")
        require("Output written on" in log and "PDF statistics:" in log,
                "incomplete compiled log")
        for token in ("Missing character:", "Rerun to get", "Label(s) may have changed."):
            require(token not in log, f"compiled log contains {token}")
        require(f"OL-NOTATION-PROFILE={args.profile}" in log
                and "OL-NOTATION-FORMULA-DIRECTION=LTR" in log,
                "compiled notation markers missing")
        files = [{"file": job + "." + ext,
                  "sha256": sha256(args.work / (job + "." + ext))}
                 for ext in extensions if (args.work / (job + "." + ext)).is_file()]
        require(any(r["file"] == job + ".aux" for r in files), "compiled AUX missing")
        receipt = {"schema": "openlogic-converged-tex-stage-v1", "profile": args.profile,
                   "role": args.role, "source_tree_sha256": digest,
                   "raw_pdf_sha256": sha256(args.work / (job + ".pdf")), "files": files,
                   "scope": "Converged TeX only; PDF repair, final QA and release remain pending."}
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "stage": "converged-tex", "profile": args.profile,
                      "role": args.role, "reused": args.action == "compiled-verify"}))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--profile", choices=("international", "machrek"), required=True)
    ap.add_argument("--action", choices=("record", "verify", "adopt", "compiled-record", "compiled-verify"), required=True)
    ap.add_argument("--role", choices=("reader", "supplement"))
    args = ap.parse_args()
    digest, sources = source_identity(args.repo)
    if args.action.startswith("compiled-"):
        require(args.role is not None, "converged checkpoint requires an explicit role")
        compiled_checkpoint(args, digest)
        return
    profile = args.profile
    first = "00" if profile == "international" else "02"
    second = "01" if profile == "international" else "03"
    assets = [f"{first}_OPENLOGIC_ar_COMPLETE_LINKED_READER_{profile.upper()}_NOTATION_OLP-0722.pdf",
              f"{second}_OPENLOGIC_ar_CLOSURE_SUPPLEMENT_80_UNITS_{profile.upper()}_NOTATION_OLP-0722.pdf"]
    jobs = [f"open-logic-complete-ar-readable-letter-{profile}", f"open-logic-closure-supplement-ar-readable-letter-{profile}"]
    receipt_path = args.output / f"PROFILE_CHECKPOINT_{profile}.json"
    if args.action == "verify":
        receipt = read_json(receipt_path)
        require(
            receipt.get("schema") == "openlogic-profile-checkpoint-v2"
            and receipt.get("status") == "PASS"
            and receipt.get("profile") == profile
            and receipt.get("source_tree_sha256") == digest,
            f"stale or invalid profile checkpoint: {profile}",
        )
        expected_records = {
            (root_name, name)
            for asset, job in zip(assets, jobs)
            for root_name, name in (
                ("output", asset),
                ("work", job + ".log"),
                ("work", job + ".aux"),
                ("work", job + ".rtl-link-rect-repair.json"),
            )
        }
        records = receipt.get("files")
        require(isinstance(records, list), "checkpoint file inventory is not a list")
        require(
            len(records) == len(expected_records)
            and {(record.get("root"), record.get("file")) for record in records}
            == expected_records,
            f"incomplete checkpoint file inventory: {profile}",
        )
        for record in records:
            root = args.work if record["root"] == "work" else args.output
            require(
                sha256(root / record["file"]) == record.get("sha256"),
                f"checkpoint member changed: {record['file']}",
            )
        print(json.dumps({"status": "PASS", "profile": profile, "reused": True}))
        return
    facts = []
    for asset, job, links in zip(
        assets,
        jobs,
        (EXPECTED_COMPONENT_LINKS["reader"], EXPECTED_COMPONENT_LINKS["supplement"]),
    ):
        text = (args.work / (job + ".log")).read_text(encoding="utf-8", errors="replace")
        require(
            "Output written on" in text and "PDF statistics:" in text,
            "incomplete final log",
        )
        for forbidden in ("Missing character:", "Rerun to get", "Label(s) may have changed."):
            require(forbidden not in text, f"final log contains {forbidden}")
        require(
            f"OL-NOTATION-PROFILE={profile}" in text,
            "notation-profile marker is missing",
        )
        require(
            "OL-NOTATION-FORMULA-DIRECTION=LTR" in text,
            "formula-direction marker is missing",
        )
        result = inspect(args.output / asset, None, profile, links)
        require(result["status"] == "PASS", "; ".join(result["failures"]))
        require(
            sha256(args.work / (job + ".pdf")) == result["sha256"],
            f"work/output PDF mismatch: {job}",
        )
        facts.append({k: result[k] for k in ("sha256", "pages", "links", "source_hash_pages", "status")})
    if args.action == "adopt":
        # The completed artifacts predate the interruption; no source (except
        # the deterministic regenerated font) may be newer than the first PDF.
        first_output_time = (args.output / assets[0]).stat().st_mtime
        require(
            all(
                p.stat().st_mtime <= first_output_time
                for p in sources
                if p.suffix != ".otf"
            ),
            "source is newer than the checkpoint being adopted",
        )
    records = []
    for asset, job in zip(assets, jobs):
        for root_name, root, name in (("output", args.output, asset), ("work", args.work, job + ".log"),
                                      ("work", args.work, job + ".aux"), ("work", args.work, job + ".rtl-link-rect-repair.json")):
            records.append({"root": root_name, "file": name, "sha256": sha256(root / name)})
    receipt = {"schema": "openlogic-profile-checkpoint-v2", "status": "PASS", "profile": profile,
               "source_scope": "source/** excluding the independent, unused source/locale/ar-classical/** overlay",
               "source_tree_sha256": digest, "files": records, "pdf_qa": facts,
               "completion_evidence": "complete final TeX logs, no rerun/glyph diagnostics, repaired PDF identity and full structural QA",
               "adopted_after_host_interruption": args.action == "adopt"}
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "profile": profile, "source_tree_sha256": digest}))

if __name__ == "__main__":
    main()
