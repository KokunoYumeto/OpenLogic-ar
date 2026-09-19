"""Freeze the finite amendment input list for one export/readback transaction."""
import hashlib
from pathlib import Path

DIRECTORY = "evidence/provenance/locale-ar/expert-review-amendments"
FIXED = ("build/generate_expert_review_index.py", "build/validate_expert_review_snapshot.py",
         "build/regenerate_review_snapshot_20260909.py", "build/reviewer_input_inventory_20260909.py",
         "build/three_exact_locator_amendments_20260909.py", "build/verify_three_exact_locators_20260909.py",
         "build/msa_mp_nfc_transition_20260909.py",
         "evidence/classical/repairs/five-locators-100017902/THREE_EXACT_LOCATOR_AMENDMENT.json",
         "evidence/classical/repairs/msa-mp-nfc-20260909/NORMALIZATION_TRANSITIONS.json",
         "build/olp0014_note_review_20260912.py", "build/verify_olp0014_note_review_20260912.py",
         "evidence/classical/repairs/olp0014-domain-size-20260909/REPAIR_RECORD.json",
         "evidence/classical/repairs/olp0014-domain-size-20260909/BEFORE_SOURCES.json")
SCHEMA = "openlogic-review-amendment-input-inventory-v1"


def capture(repo):
    root = repo.resolve()
    files = sorted((root / DIRECTORY).glob("*.json"))
    result = {"schema": SCHEMA, "semantic_amendments": [], "supporting_inputs": []}
    for group, paths in (("semantic_amendments", files),
                         ("supporting_inputs", [root / p for p in FIXED])):
        for path in paths:
            if group == "supporting_inputs" and not path.exists():
                continue
            raw = path.read_bytes()
            result[group].append({"path": path.relative_to(root).as_posix(), "bytes": len(raw),
                                  "sha256": hashlib.sha256(raw).hexdigest()})
    return result


def verify(repo, inventory):
    if capture(repo) != inventory:
        raise ValueError("frozen amendment inventory changed; stage future batches outside admitted directory")
    return [repo.resolve() / row["path"] for row in inventory["semantic_amendments"]]
