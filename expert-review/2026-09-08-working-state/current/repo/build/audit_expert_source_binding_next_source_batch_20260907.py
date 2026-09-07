"""Exact 16-choice batch witness refresh, bounded to 190+257 declarations.

Read-only by default. --emit-patch PATH emits one approved artifact for
apply_patch; it never writes sources, exports, closures, or publications.
"""
from __future__ import annotations

import argparse
import copy
import difflib
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGLISH = ROOT.parent.parent / "openlogic-interfarsi/repo/source/upstream"
PROV = "evidence/provenance/locale-ar/"
BINDINGS = PROV + "EXPERT_REVIEW_SOURCE_BINDINGS.json"
HISTORY_DIR = PROV + "expert-review-binding-history/next-source-batch-20260907/"
RECEIPT = HISTORY_DIR + "REFRESH_RECEIPT.json"
AUTHORITY_KEY = "next_source_batch_refresh_20260907"
BASELINE_SHA = "c10a6321b79a210febba49b3fc216a7fb22b729a738af71d57dc1aea9e105beb"
PRIOR_FILES = {
    BINDINGS: ("a7677a5406f83686dc95438c64bfbac6c7c0a6101cfef40c19b4703c5b45ff7c", 159561),
    PROV + "expert-review-amendments/questions-031-035-20260906.json":
        ("935a4e556b3122a28a3f3c0dea7bbe983274a3f3574779ae77e16502cc7695f0", 25995),
    PROV + "expert-review-amendments/questions-next10-20260906.json":
        ("1e668cc453b5a5cee6df70a50a9c1d574af14e35e56379f8299519438199bd59", 249541),
    PROV + "expert-review-amendments/semantic-first20-20260906.json":
        ("b2fd9f02a17deef0320d1029a636fc000bda020018dde8e5d014bb61e962a3fc", 59864),
}
LEDGERS = {
    "evidence/classical/repairs/OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907.json":
        ("eb0e436d546c867a56d66767a24f66a2d687ea254ed83c9123aa0c2106a8e0c7", "openlogic-classical-construction-repairs-v1", 3, 7, 6),
    "evidence/classical/repairs/OLP0394_0399_0400_0404_0409_MODAL_SCOPE_20260907.json":
        ("6d29d66c0db082e2c348cf8a30219e9d6ae11b80e14d0ecfdd2cbc2c79a6f4cd", "openlogic-consolidated-modal-semantic-repairs-v1", 10, 15, 6),
    "evidence/classical/repairs/OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907.json":
        ("90364663431ea9dad27fef1a427acf033498f1cd95f8cbea29cc665f41186c79", "openlogic-classical-adjective-construction-repairs-v1", 3, 4, 4),
}
EXPECTED = {
    BINDINGS: {"/bindings/0/occurrences/0/locations/2", "/bindings/2/occurrences/0/locations/2",
        "/bindings/3/occurrences/0/locations/2", "/bindings/5/occurrences/0/locations/2", "/bindings/12/occurrences/0/locations/2"},
    PROV + "expert-review-amendments/questions-031-035-20260906.json": {"/amendments/2/witnesses/3"},
    PROV + "expert-review-amendments/questions-next10-20260906.json": {"/amendments/5/witnesses/2", "/amendments/9/witnesses/2"},
    PROV + "expert-review-amendments/semantic-first20-20260906.json": {"/amendments/8/witnesses/2", "/amendments/11/witnesses/2",
        "/amendments/11/witnesses/3", "/amendments/12/witnesses/1", "/amendments/18/witnesses/1"},
}
PRIOR_RECEIPTS = {
    PROV + "expert-review-binding-history/EXPERT_REVIEW_SOURCE_BINDINGS_CONSOLIDATED_REFRESH_20260907.json":
        "97e20804b29e275a35399488b9142790e2ffd22d08e26acf38ec8f82b149aa62",
    PROV + "expert-review-binding-history/EXPERT_REVIEW_SOURCE_BINDINGS_CLASSICAL_PROSE_REFRESH_20260907.json":
        "5386fc8d747358a14f97ef760e9cd9dd57cd6f87069ddcafed6b6600c9338e28",
    PROV + "expert-review-binding-history/EXPERT_REVIEW_SOURCE_BINDINGS_REFRESH_20260906.json":
        "eead494e692842463f08bef1e8f901c1aaf916a1430daffeca9f1b1d900d7ad7",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    target = ROOT / path
    require(target.is_relative_to(ROOT) and target.stat().st_size < 2 * 1024 * 1024, "Unbounded input: " + path)
    return target.read_bytes()


def dump(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def identity(path, raw):
    return {"path": path, "sha256": sha(raw), "bytes": len(raw)}


def snapshot_path(path):
    return HISTORY_DIR + "pre-refresh/" + Path(path).name


def declarations(payload, registry):
    if registry:
        for bi, row in enumerate(payload["bindings"]):
            for oi, occurrence in enumerate(row["occurrences"]):
                for li, witness in enumerate(occurrence["locations"]):
                    yield f"/bindings/{bi}/occurrences/{oi}/locations/{li}", row["decision_id"], occurrence["unit_id"], witness
            for gi, witness in enumerate(row["global_locations"]):
                yield f"/bindings/{bi}/global_locations/{gi}", row["decision_id"], None, witness
    else:
        for ai, row in enumerate(payload["amendments"]):
            for wi, witness in enumerate(row["witnesses"]):
                yield f"/amendments/{ai}/witnesses/{wi}", row["decision_id"], None, witness


def inverse(after, transaction):
    require((sha(after), len(after)) == (transaction["after_sha256"], transaction["after_bytes"]), "Exact after identity mismatch")
    before = after
    for patch in reversed(transaction["patches"]):
        a, b = patch["before"].encode(), patch["after"].encode()
        require(a != b and before.count(b) == 1 and patch["occurrences"] == 1, "Nonunique inverse patch")
        before = before.replace(b, a, 1)
    require((sha(before), len(before)) == (transaction["before_sha256"], transaction["before_bytes"]), "Exact predecessor identity mismatch")
    replay = before
    for patch in transaction["patches"]:
        a, b = patch["before"].encode(), patch["after"].encode()
        require(replay.count(a) == 1, "Nonunique forward patch")
        replay = replay.replace(a, b, 1)
    require(replay == after, "Forward replay mismatch")
    return before


def source_chains():
    chains, inputs, decisions = {}, [], {}
    for logical, contract in LEDGERS.items():
        raw = read(logical)
        require(sha(raw) == contract[0], "Pinned repair ledger mismatch")
        payload = json.loads(raw)
        require(payload["schema"] == contract[1] and len(payload["transactions"]) == contract[2]
            and sum(len(t["patches"]) for t in payload["transactions"]) == contract[3]
            and len(payload["decisions"]) == contract[4], "Exact repair ledger inventory mismatch")
        inputs.append(identity(logical, raw))
        decisions.update({d["decision_id"]: {"ledger": logical, "rationale": d["rationale"],
            "expert_question": d["expert_question"], "open_to_correction": d["open_to_correction"]} for d in payload["decisions"]})
        for transaction in payload["transactions"]:
            chains.setdefault(transaction["path"], []).append({"ledger": logical, "transaction": transaction})
    require(len(chains) == 15 and sum(map(len, chains.values())) == 16 and len(decisions) == 16, "Batch source/choice inventory differs")
    for path, chain in chains.items():
        after = read(path)
        for step in reversed(chain):
            t = step["transaction"]
            before = inverse(after, t)
            step.update(before=before, after=after)
            after = before
    return chains, inputs, decisions


def ranges_of(witness):
    return witness.get("line_ranges", [[witness.get("line_start"), witness.get("line_end")]])


def excerpt(raw, ranges):
    lines = raw.decode("utf-8-sig").splitlines()
    require(ranges and all(type(a) is int and type(b) is int and 1 <= a <= b <= len(lines) for a, b in ranges), "Invalid witness ranges")
    return "\n".join(line for a, b in ranges for line in lines[a-1:b])


def mapped_passage(before, chain, ranges):
    """Carry complete selected lines through exact byte replacements.

    A replacement crossing a selection edge fails; no fuzzy relocation is used.
    Complete contained replacements have explicit canonical decision identities.
    """
    current, current_ranges, affecting = before, copy.deepcopy(ranges), []
    for step in chain:
        require(current == step["before"], "Source chain disconnected")
        lines = current.splitlines(keepends=True)
        offsets = [0]
        for line in lines:
            offsets.append(offsets[-1] + len(line))
        spans = [[offsets[a-1], offsets[b] - len(lines[b-1]) + len(lines[b-1].rstrip(b"\r\n"))] for a, b in current_ranges]
        for patch in step["transaction"]["patches"]:
            old, new = patch["before"].encode(), patch["after"].encode()
            require(current.count(old) == 1, "Ambiguous source mapping patch")
            start, end = current.index(old), current.index(old) + len(old)
            delta = len(new) - len(old)
            for span in spans:
                if end <= span[0]:
                    span[0] += delta
                    span[1] += delta
                elif start >= span[1]:
                    pass
                elif span[0] <= start and end <= span[1]:
                    span[1] += delta
                    affecting.extend(patch["decision_ids"])
                else:
                    raise ValueError("Patch crosses witness selection edge")
            current = current.replace(old, new, 1)
        require(current == step["after"], "Source mapping replay mismatch")
        current_ranges = [[current[:a].count(b"\n") + 1,
            current[:b if current[b-1:b] == b"\n" else b-1].count(b"\n") + 1] for a, b in spans]
        for span, line_range in zip(spans, current_ranges):
            require(current[span[0]:span[1]].decode() == excerpt(current, [line_range]),
                "Mapped witness is not a complete line range: " + step["transaction"]["path"] + ": " + repr(current_ranges))
    return current, current_ranges, sorted(set(affecting))


def expected_documents():
    chains, inputs, decisions = source_chains()
    artifacts, documents, changes, snapshots = {}, {}, [], {}
    for logical, (digest, count) in PRIOR_FILES.items():
        historical = snapshot_path(logical)
        raw = read(historical) if (ROOT / historical).exists() else read(logical)
        require((sha(raw), len(raw)) == (digest, count), "Pinned previous review file differs: " + logical)
        old = json.loads(raw)
        require(dump(old) == raw, "Previous review bytes are not canonical LF JSON")
        new = copy.deepcopy(old)
        artifacts[historical] = raw
        changed = []
        for pointer, decision_id, unit, witness in declarations(new, logical == BINDINGS):
            root = ENGLISH if witness["source_kind"] == "english" else ROOT
            source = (root / witness["path"]).resolve()
            require(source.is_relative_to(root.resolve()), "Witness path escapes root")
            live = source.read_bytes()
            if sha(live) == witness["file_sha256"].lower():
                continue
            require(pointer in EXPECTED[logical] and witness["source_kind"] == "classical", "Unexpected stale witness")
            chain = chains[witness["path"]]
            before = chain[0]["before"]
            require(sha(before) == witness["file_sha256"].lower(), "Witness is not the exact oldest predecessor")
            prior_witness = copy.deepcopy(witness)
            before_excerpt = excerpt(before, ranges_of(witness))
            hash_key = "cited_text_sha256" if logical == BINDINGS else "excerpt_sha256"
            require(sha(before_excerpt.encode()) == witness[hash_key].lower(), "Historical quoted text identity differs")
            if "excerpt" in witness:
                require(witness["excerpt"] == before_excerpt, "Historical literal excerpt differs")
            mapped, ranges, affected = mapped_passage(before, chain, ranges_of(witness))
            require(mapped == live, "Live source differs from mapped chain")
            after_excerpt = excerpt(live, ranges)
            require((before_excerpt != after_excerpt) == bool(affected), "Wording changed without explicit decision")
            witness["file_sha256"] = sha(live)
            if "line_ranges" in witness:
                witness["line_ranges"] = ranges
            else:
                require(len(ranges) == 1, "Amendment witness became discontiguous")
                witness["line_start"], witness["line_end"] = ranges[0]
            witness[hash_key] = sha(after_excerpt.encode())
            if "excerpt" in witness:
                witness["excerpt"] = after_excerpt
            t = chain[0]["transaction"]
            snapshot = HISTORY_DIR + "sources/" + t["unit_id"] + "-" + t["edition"] + ".tex"
            artifacts[snapshot] = before
            snapshots[(t["edition"], witness["path"])] = identity(snapshot, before)
            new_assessment = (
                "New source-binding assessment, not the original translator's motive: the complete selected quotation is unchanged; only its current file identity and any line shift are refreshed. The original semantic_basis remains verbatim."
                if not affected else
                "New source-binding assessment, not the original translator's motive: this selected context contains the explicitly recorded corrections listed below. Their exact replacements are replayed; the quoted terminology and the original semantic_basis remain applicable. The canonical reasons/questions below remain provisional and open to correction, with no human-response gate.")
            changed.append(pointer)
            changes.append({"file": logical, "pointer": pointer, "decision_id": decision_id, "unit_id": unit,
                "before": prior_witness, "after": copy.deepcopy(witness), "before_excerpt": before_excerpt,
                "after_excerpt": after_excerpt, "quotation_unchanged": before_excerpt == after_excerpt,
                "changed_fields": [key for key in witness if prior_witness.get(key) != witness[key]],
                "canonical_wording_decisions": [{"decision_id": key, **decisions[key]} for key in affected],
                "new_assessment": new_assessment, "historical_source": identity(snapshot, before)})
        require(set(changed) == EXPECTED[logical], "Exact stale-pointer inventory differs")
        refresh = {"assessed_on": "2026-09-07", "recording_mode": "new-independent-current-source-witness-refresh",
            "previous_file": identity(historical, raw), "receipt": RECEIPT,
            "scope": "Exact current source identities and selected line/excerpt bindings only; previous wording/decisions/reasons and all historical receipts are preserved.",
            "changed_pointers": sorted(changed), "human_response_is_gate": False}
        if logical == BINDINGS:
            require(AUTHORITY_KEY not in new["authority"], "Refresh authority already in predecessor")
            new["authority"][AUTHORITY_KEY] = refresh
        else:
            new["source_identity_refreshes"] = [refresh] + old.get("source_identity_refreshes", [])
        documents[logical] = new
        artifacts[logical] = dump(new)
    return artifacts, documents, changes, snapshots, chains, inputs


def verify_current():
    from build import generate_expert_review_index as index
    artifacts, documents, changes, snapshots, chains, inputs = expected_documents()
    for path, expected in artifacts.items():
        require(read(path) == expected, "Current or preserved artifact differs: " + path)
    baseline_raw = read("evidence/classical/BASELINE.json")
    require(sha(baseline_raw) == BASELINE_SHA, "Frozen baseline differs")
    baseline = {u["id"]: u for u in json.loads(baseline_raw)["units"]}
    inventory, totals, all_rows = {}, Counter(), []
    registry = documents[BINDINGS]
    for pointer, decision_id, unit, w in declarations(registry, True):
        kind = w["source_kind"]
        expected_path = None if unit is None else baseline[unit][{"english": "source_path", "msa": "arabic_path", "classical": "target_path"}[kind]]
        index._validated_expert_source_group(w, ROOT, ENGLISH, expected_path, sha(artifacts[BINDINGS]).upper())
        target = (ENGLISH if kind == "english" else ROOT) / w["path"]
        raw = target.read_bytes()
        require(sha(raw) == w["file_sha256"].lower() and sha(excerpt(raw, w["line_ranges"]).encode()) == w["cited_text_sha256"].lower(), "Current registry bytes differ")
        inventory[str(target)] = sha(raw)
        totals[kind] += 1
        totals["unit" if unit else "global"] += 1
        all_rows.append({"file": BINDINGS, "pointer": pointer, "decision_id": decision_id, "witness": w, "status": "PASS"})
    require(len(registry["bindings"]) == 70 and len(all_rows) == 190 and dict(totals) ==
        {"english": 71, "unit": 179, "msa": 82, "classical": 37, "global": 11}, "Registry inventory changed")
    amendment_ids, amendment_count = set(), 0
    for path in sorted((ROOT / (PROV + "expert-review-amendments")).glob("*.json")):
        payload = json.loads(path.read_bytes())
        for row in payload["amendments"]:
            require(row["decision_id"] not in amendment_ids, "Duplicate amendment decision")
            amendment_ids.add(row["decision_id"])
        for pointer, decision_id, _, w in declarations(payload, False):
            root = ENGLISH if w["source_kind"] == "english" else ROOT
            target = (root / w["path"]).resolve()
            require(target.is_relative_to(root.resolve()), "Amendment source escapes root")
            raw = target.read_bytes()
            text = excerpt(raw, ranges_of(w))
            require(sha(raw) == w["file_sha256"].lower() and sha(text.encode()) == w["excerpt_sha256"].lower(), "Current amendment witness differs")
            require("excerpt" not in w or w["excerpt"] == text, "Current amendment literal differs")
            inventory[str(target)] = sha(raw)
            amendment_count += 1
            all_rows.append({"file": path.relative_to(ROOT).as_posix(), "pointer": pointer,
                "decision_id": decision_id, "witness": w, "status": "PASS"})
    require((len(amendment_ids), amendment_count) == (68, 257), "Amendment inventory changed")
    for path, digest in inventory.items():
        require(sha(Path(path).read_bytes()) == digest, "Source changed during current audit")
    prior_receipts = []
    for path, digest in PRIOR_RECEIPTS.items():
        raw = read(path)
        require(digest is None or sha(raw) == digest, "Historical audit receipt differs")
        prior_receipts.append(identity(path, raw))
    return {"schema": "openlogic-review-bindings-next-source-batch-v1", "assessed_on": "2026-09-07", "status": "PASS",
        "scope": "all-190-live-registry-and-257-live-amendment-witnesses-no-historical-source-substitution",
        "counts": {"bindings": 70, "registry_declarations": 190, "amendments": 68, "amendment_witnesses": 257,
            "changed_registry_declarations": 5, "changed_amendment_witnesses": 8,
            "unchanged_quotations": sum(c["quotation_unchanged"] for c in changes), "wording_reassessments": sum(not c["quotation_unchanged"] for c in changes),
            "source_files": 15, "source_transactions": 16, "source_patches": 26, **dict(totals)},
        "previous_files": [identity(snapshot_path(p), artifacts[snapshot_path(p)]) for p in PRIOR_FILES],
        "current_files": [identity(p, artifacts[p]) for p in PRIOR_FILES],
        "historical_sources": list(snapshots.values()), "repair_ledgers": inputs,
        "source_inverse_chains": [{"path": path, "steps": [{"ledger": s["ledger"], "before": identity(path, s["before"]),
            "after": identity(path, s["after"]), "patches": s["transaction"]["patches"]} for s in chain]} for path, chain in chains.items()],
        "pointer_changes": changes, "complete_live_locator_audit": all_rows, "preserved_prior_receipts": prior_receipts,
        "limits": ["No full reviewer index generation or closure; preserve all original raw records during owner integration.",
            "No PDF page binding, reader build, visual/replay QA, or publication is claimed."]}


def emit(path):
    if path == RECEIPT:
        expected = dump(verify_current())
    else:
        artifacts = expected_documents()[0]
        require(path in artifacts, "Unapproved artifact output")
        expected = artifacts[path]
    target = ROOT / path
    if target.exists():
        current = target.read_bytes()
        if current == expected:
            print("*** Begin Patch\n*** End Patch")
            return
        require(path in PRIOR_FILES, "Historical artifact is immutable")
        require((sha(current), len(current)) == PRIOR_FILES[path], "Unexpected live edit before refresh")
        diff = list(difflib.unified_diff(current.decode().splitlines(), expected.decode().splitlines(), n=3))
        print("*** Begin Patch\n*** Update File: " + target.as_posix())
        for line in diff[2:]:
            print("@@" if line.startswith("@@") else line)
    else:
        print("*** Begin Patch\n*** Add File: " + target.as_posix())
        for line in expected.decode().splitlines():
            print("+" + line)
    print("*** End Patch")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-patch")
    parser.add_argument("--plan", action="store_true")
    args = parser.parse_args()
    if args.emit_patch:
        emit(args.emit_patch)
    elif args.plan:
        artifacts, _, changes, _, _, _ = expected_documents()
        print(json.dumps({"artifacts": [identity(p, raw) for p, raw in artifacts.items()], "changes": changes}, ensure_ascii=False, indent=2))
    else:
        report = verify_current()
        print(json.dumps({"status": report["status"], "counts": report["counts"], "current_files": report["current_files"]}, indent=2))
