#!/usr/bin/env python3
"""Build an honest, hash-bound working Arabic translation-decision register."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from copy import deepcopy
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def unit_number(unit_id: str) -> int:
    match = re.fullmatch(r"OLP-(\d{4})", unit_id)
    if not match:
        raise ValueError(f"invalid unit id: {unit_id!r}")
    return int(match.group(1))


def list_value(record: dict, *names: str) -> list:
    for name in names:
        value = record.get(name)
        if isinstance(value, list):
            return value
    return []


def text_value(value) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return str(value.get("level") or value.get("value") or "")
    return ""


def markdown_cell(value) -> str:
    text = str(value or "").replace("|", "\\|").replace("\n", " ").strip()
    return " ".join(text.split())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    args = ap.parse_args()
    repo = args.repo.resolve()
    evidence = repo / "evidence/classical"
    terminology = evidence / "terminology"
    baseline_path = evidence / "BASELINE.json"
    baseline = read(baseline_path)
    units = baseline["units"]
    if len(units) != 722 or [unit_number(row["id"]) for row in units] != list(range(1, 723)):
        raise ValueError("baseline is not the exact ordered 722-unit inventory")

    sources = sorted(terminology.glob("retro-*.json"))
    sources.append(evidence / "reviews/0051-0100.json")
    for path in sorted((evidence / "batches").glob("*.json")):
        data = read(path)
        if list_value(data, "terminology_decisions", "decisions"):
            sources.append(path)

    decisions: dict[str, dict] = {}
    source_inventory = []
    coverage_inputs: dict[str, list[dict]] = {row["id"]: [] for row in units}
    for path in sources:
        data = read(path)
        relative = path.relative_to(repo).as_posix()
        identity = {"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)}
        source_inventory.append(identity)
        for original in list_value(data, "terminology_decisions", "decisions"):
            if not isinstance(original, dict):
                raise ValueError(f"non-object decision in {relative}")
            decision = deepcopy(original)
            decision_id = decision.get("decision_id")
            required = ("english_term", "chosen_arabic", "rationale", "recording_mode")
            if not isinstance(decision_id, str) or not decision_id.strip():
                raise ValueError(f"missing decision_id in {relative}")
            if any(not isinstance(decision.get(key), str) or not decision[key].strip() for key in required):
                raise ValueError(f"incomplete decision {decision_id} in {relative}")
            if decision.get("open_to_correction") is not True:
                raise ValueError(f"decision is not open to correction: {decision_id}")
            decision["source_record"] = identity
            if decision_id in decisions and decisions[decision_id] != decision:
                raise ValueError(f"conflicting duplicate decision id: {decision_id}")
            decisions[decision_id] = decision
        raw_coverage = data.get("terminology_coverage", data.get("coverage", []))
        if isinstance(raw_coverage, list):
            for item in raw_coverage:
                if isinstance(item, dict) and item.get("unit_id") in coverage_inputs:
                    coverage_inputs[item["unit_id"]].append(
                        {"source_record": identity, "observation": item}
                    )

    ordered_decisions = sorted(decisions.values(), key=lambda d: d["decision_id"])
    decision_units: dict[str, set[str]] = {row["id"]: set() for row in units}
    for decision in ordered_decisions:
        for occurrence in decision.get("occurrences", []):
            if isinstance(occurrence, dict) and occurrence.get("unit_id") in decision_units:
                decision_units[occurrence["unit_id"]].add(decision["decision_id"])

    coverage = []
    counts = Counter()
    for row in units:
        unit_id = row["id"]
        target = repo / row["target_path"]
        observations = coverage_inputs[unit_id]
        complete = any(
            obs["observation"].get("occurrence_coverage_complete") is True
            or obs["observation"].get("status") == "contextually-reviewed"
            for obs in observations
        )
        ids = sorted(decision_units[unit_id])
        state = "contextually-reviewed" if complete else (
            "partial-decisions-recorded" if ids else "pending-contextual-review"
        )
        counts[state] += 1
        target_identity = None
        if target.is_file():
            target_identity = {
                "path": row["target_path"],
                "bytes": target.stat().st_size,
                "sha256": sha256(target),
            }
        coverage.append(
            {
                "unit_id": unit_id,
                "state": state,
                "decision_ids": ids,
                "decision_count": len(ids),
                "classical_target": target_identity,
                "input_identity": {
                    "english_path": row["source_path"],
                    "english_sha256": row["english_sha256"].upper(),
                    "msa_path": row["arabic_path"],
                    "msa_sha256": row["arabic_sha256"].upper(),
                },
                "source_observations": observations,
                "open_to_correction": True,
            }
        )

    queue = []
    for decision in ordered_decisions:
        if decision.get("expert_review_useful") is True:
            queue.append(
                {
                    "decision_id": decision["decision_id"],
                    "english_term": decision["english_term"],
                    "sense": decision.get("sense"),
                    "chosen_arabic": decision["chosen_arabic"],
                    "rationale": decision["rationale"],
                    "alternatives": decision.get("alternatives", []),
                    "confidence": decision.get("confidence"),
                    "question": decision.get("expert_question")
                    or decision.get("expert_review_question")
                    or decision.get("expert_review_reason"),
                    "source_record": decision["source_record"],
                    "open_to_correction": True,
                    "status": decision.get("status", "provisional-in-use"),
                }
            )

    common = {
        "date": "2026-09-04",
        "baseline": {
            "path": baseline_path.relative_to(repo).as_posix(),
            "bytes": baseline_path.stat().st_size,
            "sha256": sha256(baseline_path),
            "units": 722,
        },
        "source_records": source_inventory,
        "recording_policy": {
            "translation_continues_without_expert_hold": True,
            "all_choices_open_to_correction": True,
            "retrospective_reasons_are_not_claimed_as_original_motives": True,
            "dictionary_absence_requires_bounded_source_qualification": True,
        },
    }
    decision_payload = {
        "schema": "openlogic-arabic-translation-decisions-working-v1",
        "status": "PARTIAL_WORKING_REGISTER",
        **common,
        "decision_count": len(ordered_decisions),
        "decisions": ordered_decisions,
        "exhaustive": False,
        "qualification": "This snapshot consolidates decisions actually recorded so far. It is public for asynchronous review but does not claim that every decision in 722 units has been reconstructed.",
    }
    coverage_payload = {
        "schema": "openlogic-arabic-translation-decision-coverage-working-v1",
        "status": "INCOMPLETE",
        **common,
        "counts": dict(sorted(counts.items())),
        "classical_targets_present": sum(item["classical_target"] is not None for item in coverage),
        "units": coverage,
        "exhaustive": False,
    }
    queue_payload = {
        "schema": "openlogic-arabic-expert-review-queue-working-v1",
        "status": "OPEN_ASYNCHRONOUS_REVIEW",
        **common,
        "queued_decision_count": len(queue),
        "decisions": queue,
        "review_is_a_release_gate": False,
        "exhaustive": False,
    }
    write_json(terminology / "DECISIONS_WORKING.json", decision_payload)
    write_json(terminology / "COVERAGE_WORKING.json", coverage_payload)
    write_json(terminology / "EXPERT_REVIEW_QUEUE_WORKING.json", queue_payload)

    lines = [
        "# Arabic translation decisions — working public register",
        "",
        "Snapshot: 2026-09-04. Status: **partial and actively being backfilled**.",
        "",
        "This register exposes the Arabic Open Logic terminology and difficult translation choices recorded so far so specialists can review them asynchronously. Translation continues when no official-dictionary entry or expert is available; reasoned choices stay provisional and explicitly open to correction. Expert feedback is welcome but is not a production or publication hold.",
        "",
        "Retrospective entries record the present evidence-based reason for retaining or revising a choice. They do **not** claim to recover an earlier translator's private or contemporaneous thought process. A bounded unsuccessful lookup is never described as proof that a term is absent from all official dictionaries.",
        "",
        "## Current coverage",
        "",
        "- Frozen source inventory: 722 units.",
        f"- Decisions consolidated: {len(ordered_decisions)}.",
        f"- Contextually reviewed units with declared occurrence coverage: {counts['contextually-reviewed']}.",
        f"- Units with at least one recorded decision but incomplete contextual coverage: {counts['partial-decisions-recorded']}.",
        f"- Units still awaiting contextual decision review: {counts['pending-contextual-review']}.",
        f"- Classical target snapshots currently present: {coverage_payload['classical_targets_present']}/722.",
        f"- Decisions explicitly queued for potentially useful expert input: {len(queue)}.",
        "",
        "These figures are deliberately not an exhaustive-completion claim. Machine-readable files preserve all source records, occurrence hashes and pending-unit states.",
        "",
        "## How to review",
        "",
        "Open EXPERT_REVIEW_QUEUE_WORKING.json for focused questions, DECISIONS_WORKING.json for the full current decision records, and COVERAGE_WORKING.json for every unit's reviewed/pending state. Corrections should cite a decision ID, mathematical sense, proposed wording and supporting source when available.",
        "",
        "Public review surfaces: [GitHub terminology directory](https://github.com/KokunoYumeto/OpenLogic-ar/tree/main/evidence/classical/terminology), [GitHub issue form](https://github.com/KokunoYumeto/OpenLogic-ar/issues/new), and the stable [Zenodo concept DOI](https://doi.org/10.5281/zenodo.21921850). The DOI always resolves to the latest published snapshot in the existing Arabic-edition lineage.",
        "",
        "## Recorded decisions",
        "",
        "| Decision ID | English term / sense | Arabic in use | Basis | Confidence | Expert input |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for decision in ordered_decisions:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(decision["decision_id"]),
                    markdown_cell(decision["english_term"]),
                    markdown_cell(decision["chosen_arabic"]),
                    markdown_cell(decision.get("basis")),
                    markdown_cell(text_value(decision.get("confidence"))),
                    "useful" if decision.get("expert_review_useful") is True else "not specifically requested",
                ]
            )
            + " |"
        )
    lines += [
        "",
        "## Limits",
        "",
        "- This is a working evidence publication, not expert endorsement, a completed lexicon, or full linguistic QA.",
        "- Source-audit findings and inherited defects remain distinct from translation choices.",
        "- The international and Machrek MSA readers share terminology; the classical edition can use different grammatical realization while preserving mathematical distinctions.",
        "- Later snapshots preserve superseded decisions and identify replacements rather than rewriting history.",
        "",
    ]
    (terminology / "WORKING_REGISTER.md").write_text(
        "\n".join(lines), encoding="utf-8", newline="\n"
    )

    public_outputs = [
        terminology / "README.md",
        terminology / "WORKING_REGISTER.md",
        terminology / "DECISIONS_WORKING.json",
        terminology / "COVERAGE_WORKING.json",
        terminology / "EXPERT_REVIEW_QUEUE_WORKING.json",
    ]
    manifest_lines = ["# SHA-256  bytes  repository-relative path"]
    for path in sorted(public_outputs, key=lambda p: p.relative_to(repo).as_posix()):
        manifest_lines.append(
            f"{sha256(path)}  {path.stat().st_size}  {path.relative_to(repo).as_posix()}"
        )
    manifest = terminology / "WORKING_SNAPSHOT_SHA256.txt"
    manifest.write_text("\n".join(manifest_lines) + "\n", encoding="ascii", newline="\n")
    receipt = {
        "schema": "openlogic-arabic-translation-decision-working-snapshot-v1",
        "status": "PASS_PARTIAL_SNAPSHOT",
        "date": "2026-09-04",
        "outputs": [
            {
                "path": path.relative_to(repo).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in public_outputs + [manifest]
        ],
        "input_records": source_inventory,
        "decision_count": len(ordered_decisions),
        "expert_queue_count": len(queue),
        "coverage_counts": dict(sorted(counts.items())),
        "classical_targets_present": coverage_payload["classical_targets_present"],
        "exhaustive": False,
        "remote_publication": None,
        "failures": [],
    }
    write_json(terminology / "WORKING_SNAPSHOT.json", receipt)
    print(json.dumps(
        {k: receipt[k] for k in (
            "status", "decision_count", "expert_queue_count",
            "coverage_counts", "classical_targets_present"
        )},
        ensure_ascii=False,
        sort_keys=True,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
