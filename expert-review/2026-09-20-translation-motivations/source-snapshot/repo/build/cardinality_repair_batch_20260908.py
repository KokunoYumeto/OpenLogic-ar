"""Read-only, finite admission of the applied OLP0031--0035 repair batch.

This is a byte/ownership/location adapter, not a semantic or PDF certificate.
Original ledgers and decision objects remain available verbatim. No source,
registry, export, network or publication write is performed by this module.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Callable, Literal

REPO = Path(__file__).resolve().parents[1]
ENGLISH = REPO.parent.parent / "openlogic-interfarsi/repo/source/upstream"
REPAIRS = "evidence/classical/repairs/"
CONTENT = "content/sets-functions-relations/size-of-sets/"
UNIT_FILES = {"OLP-0031": "pairing.tex", "OLP-0032": "pairing-alt.tex",
              "OLP-0033": "non-enumerability.tex", "OLP-0034": "reduction.tex",
              "OLP-0035": "equinumerous-sets.tex"}
ENGLISH_HASHES = {
    "OLP-0031": "345a39184e28af727e378d5b5883b5e7d2e1c27cd729329376d19426ddaed484",
    "OLP-0032": "fd523f5306e1fd0e5c03f4c572d244fb017d1c0be27939f180bc6867a214e425",
    "OLP-0033": "a272a841f8c50bda6589aac40278b9bff7f8a1f5284730c7195423b09ac3ba2e",
    "OLP-0034": "33f0cbb35c8c1fa3ff0e4f44fa626fdc298d1c4612aeaafb41bcb920e5d18ac8",
    "OLP-0035": "7b0444e3293b300b72b7a6d49638913a778f5131fd94650dd64a5f11040c91f2",
}
PAIRING_IDS = (
    "AR-OLP-0031-MSA-ARABIC-ORDINAL-20260907", "AR-OLP-0031-CLASSICAL-ARABIC-ORDINAL-20260907",
    "AR-OLP-0031-MSA-COFINITE-SOURCE-NOTE-20260907", "AR-OLP-0031-CLASSICAL-COFINITE-SOURCE-NOTE-20260907",
    "AR-OLP-0031-CLASSICAL-UNION-PREDICATE-20260907", "AR-OLP-0032-MSA-SOURCE-CORRECTION-DISCLOSURE-20260907",
    "AR-OLP-0032-CLASSICAL-SOURCE-CORRECTION-DISCLOSURE-20260907",
)
REDUCTION_IDS = (
    "AR-OLP-0034-CODOMAIN-MSA-20260907", "AR-OLP-0034-CODOMAIN-CLASSICAL-20260907",
    "AR-OLP-0034-INSTRUMENTAL-ANTECEDENT-20260907", "AR-OLP-0034-DIRECT-CONDITIONAL-20260907",
)
PROPOSAL_HISTORY = REPAIRS + "history/pairing-before-applied-20260907/OLP0031_0032_PAIRING_CONSTRUCTIONS_20260907.json"
PROPOSAL_SHA = "8ccc0f7f691271e37234d17812593df3748833efbd9578e4b01dfbbd217948af"
Edition = Literal["msa", "classical", "english", "shared"]


@dataclass(frozen=True)
class Contract:
    stem: str
    sha256: str
    bytes: int
    schema: str
    decision_ids: tuple[str, ...]
    # Preserve ledger/application order; it is deliberately not page order.
    transaction_patches: tuple[tuple[str, ...], ...]


CONTRACTS = (
    Contract("OLP0031_0032_PAIRING_CONSTRUCTIONS_20260907", "86da173ac4083f2effe84cf60efe0e726e6caf79023aa8fa3ae6d852d73c8bc9", 155011,
        "openlogic-pairing-construction-repairs-v1", PAIRING_IDS,
        (("PAIR-0031-MSA-RANK", "PAIR-0031-MSA-SOURCE-REFERENT"),
         ("PAIR-0031-CLASSICAL-RANK", "PAIR-0031-CLASSICAL-SOURCE-REFERENT", "PAIR-0031-CLASSICAL-UNION-1", "PAIR-0031-CLASSICAL-UNION-2"),
         ("PAIR-0032-MSA-DISCLOSURE",), ("PAIR-0032-CLASSICAL-DISCLOSURE",))),
    Contract("OLP0033_NONENUMERABILITY_CONSTRUCTIONS_20260907", "13aa46d70ae164ca7b2be107503238027c2fadc3d0204a3bc0c68d9feb26aecc", 71615,
        "arabic-bounded-source-repairs.v1", tuple("AR-OLP0033-REPAIR-" + suffix + "-20260907" for suffix in ("G03", "G06", "G13", "NFC1", "NFC2", "NFC3")),
        (("OLP0033-G13",), ("OLP0033-G03", "OLP0033-G06", "OLP0033-NFC1", "OLP0033-NFC2", "OLP0033-NFC3"))),
    Contract("OLP0034_REDUCTION_CONSTRUCTIONS_20260907", "8addb4be1b7b8cc92f7044ab4ef357de6ea8105e134ac4ad921d9e5348580631", 19497,
        "openlogic-reduction-construction-repairs-v1", REDUCTION_IDS,
        (("RED-0034-CODOMAIN-MSA",), ("RED-0034-CODOMAIN-CLASSICAL", "RED-0034-INSTRUMENTAL-ANTECEDENT", "RED-0034-DIRECT-CONDITIONAL"))),
    Contract("OLP0035_EQUINUMEROSITY_CONSTRUCTIONS_20260907", "4615dbc5636212dc0c9ca3c2244afef44f13a49d8a330ffd5dd6ce51415f68ed", 78958,
        "openlogic-equinumerosity-construction-repairs-v1",
        ("AR-OLP0035-ar-G09",) + tuple("AR-OLP0035-ar-classical-" + suffix for suffix in ("G09", "G10", "G14", "G15", "NFC01")),
        (("OLP0035-msa-P1",), tuple("OLP0035-classical-P" + str(n) for n in range(1, 7)))),
)


@dataclass(frozen=True)
class Identity:
    path: str
    bytes: int
    sha256: str


@dataclass(frozen=True)
class Location:
    source: Identity
    byte_start: int
    byte_end: int
    line_start: int
    line_end: int
    literal: str
    excerpt: str


@dataclass(frozen=True)
class Patch:
    patch_id: str
    decision_ids: tuple[str, ...]
    application_index: int
    before: Location
    after: Location
    ownership_basis: str
    raw_json: str


@dataclass(frozen=True)
class SourceTransition:
    ledger_path: str
    unit_id: str
    edition: Edition
    before: Identity
    after: Identity
    before_bytes: bytes
    after_bytes: bytes
    patches: tuple[Patch, ...]
    source_order_patch_ids: tuple[str, ...]


@dataclass(frozen=True)
class Witness:
    location: Location
    recorded_phase: str
    verified_phase: str
    raw_json: str


@dataclass(frozen=True)
class Decision:
    decision_id: str
    unit_id: str
    edition: Edition
    ledger_path: str
    ledger_index: int
    status: str
    recording_mode: str
    rationale: str
    patches: tuple[Patch, ...]
    witnesses: tuple[Witness, ...]
    raw_json: str


@dataclass(frozen=True)
class Supersession:
    decision_id: str
    previous_status: str
    current_status: str
    previous_decision_json: str
    current_decision_json: str
    history_source: Identity
    changed_fields: tuple[str, ...]


@dataclass(frozen=True)
class Ledger:
    identity: Identity
    raw_bytes: bytes
    status: str
    decisions: tuple[Decision, ...]


@dataclass(frozen=True)
class Batch:
    ledgers: tuple[Ledger, ...]
    decisions: tuple[Decision, ...]
    sources: tuple[SourceTransition, ...]
    supersessions: tuple[Supersession, ...]
    input_identities: tuple[Identity, ...]
    scope: str = "Exact finite source/patch/location admission only; no semantic, authority-attestation, full-review, PDF or publication certification."


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def json_text(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def parse(raw):
    def pairs(rows):
        result = {}
        for key, value in rows:
            require(key not in result, "Duplicate JSON key")
            result[key] = value
        return result
    return json.loads(raw.decode("utf-8-sig"), object_pairs_hook=pairs)


def check_identity(raw, expected, prefix=""):
    require((len(raw), sha(raw)) == (expected[prefix + "bytes"], expected[prefix + "sha256"]), "Source hash/byte identity differs")


def exact_location(raw, source, literal, recorded=None, *, witness_newline_endpoint=False):
    """Zero-based half-open bytes; one-based inclusive nonempty source lines."""
    needle = literal.encode("utf-8")
    require(bool(needle) and raw.count(needle) == 1, "Literal missing or ambiguous")
    start = raw.index(needle)
    end = start + len(needle)
    # UTF-8 decode confirms the boundaries do not split a code point.
    raw[:start].decode("utf-8")
    raw[:end].decode("utf-8")
    first = raw[:start].count(b"\n") + 1
    last = raw[:end - 1].count(b"\n") + 1
    excerpt = "\n".join(raw.decode("utf-8").splitlines()[first - 1:last])
    location = Location(source, start, end, first, last, literal, excerpt)
    if recorded is not None:
        for key, actual in (("byte_start", start), ("byte_end", end), ("line_start", first), ("line_end", last)):
            # Some complete legacy quotations include the final newline and
            # record its endpoint on the next line. This is not a patch waiver:
            # exact bytes prove that sole alternative; normalized lines remain
            # inclusive occupied lines and the original declaration is retained.
            endpoint = (witness_newline_endpoint and key == "line_end" and needle.endswith(b"\n")
                        and recorded.get(key) == raw[:end].count(b"\n") + 1)
            require(type(recorded.get(key)) is int and (recorded[key] == actual or endpoint), "Wrong exact location boundary: " + key)
        for key in ("literal", "text"):
            if key in recorded:
                require(recorded[key] == literal, "Recorded location literal differs")
        if "excerpt" in recorded:
            recorded_excerpt = "\n".join(raw.decode("utf-8").splitlines()[first - 1:recorded["line_end"]])
            require(recorded["excerpt"] in (recorded_excerpt, recorded_excerpt + "\n"), "Recorded line excerpt differs at " + source.path + ":" + str(first))
    return location


def patch_owners(transaction, patch, choices):
    """Three schemas declare IDs; reduction uses exact occurrence+wording join."""
    by_id = {d["decision_id"]: d for d in choices}
    if "decision_ids" in patch:
        owners = tuple(patch["decision_ids"])
        require(owners and len(owners) == len(set(owners)), "Missing or duplicate patch owners")
        basis = "explicit decision_ids"
    else:
        owners = tuple(d["decision_id"] for d in choices
            if d["unit_id"] == transaction["unit_id"] and d["edition"] == transaction["edition"]
            and d.get("before_arabic") == patch["before"] and d.get("chosen_arabic") == patch["after"]
            and len(d.get("occurrences", [])) == 1
            and d["occurrences"][0].get("target_path") == transaction["path"]
            and d["occurrences"][0].get("literal") == patch["after"])
        require(len(owners) == 1, "Missing or ambiguous exact reduction ownership")
        basis = "unique exact unit/edition/path/before/after/occurrence join"
    for owner in owners:
        require(owner in by_id, "Unknown patch decision ID")
        row = by_id[owner]
        require((row["unit_id"], row["edition"]) == (transaction["unit_id"], transaction["edition"]), "Wrong decision unit/edition ownership")
    return owners, basis


def check_choice_ownership(choice, patches):
    """Corroborate declared IDs against each schema's independent wording link."""
    actual = tuple((p.before.literal, p.after.literal) for p in patches)
    if "raw_before" in choice:
        require(actual == ((choice["raw_before"], choice["raw_after"]),), "Decision raw wording does not own its patch")
    elif isinstance(choice.get("grammatical_realization"), list):
        require(actual == tuple((r["before"], r["after"]) for r in choice["grammatical_realization"]), "Decision realizations do not own exact patches")
    elif "occurrence_bindings" in choice:
        bound = [(row["path"], row["sha256"], location["byte_start"], location["byte_end"], location["literal"])
                 for row in choice["occurrence_bindings"] for location in row["locations"]]
        expected = [(p.after.source.path, p.after.source.sha256, p.after.byte_start, p.after.byte_end, p.after.literal) for p in patches]
        require(bound == expected, "Pairing occurrence bindings do not own exact patches")
    else:
        require(choice["decision_id"] in REDUCTION_IDS and actual == ((choice["before_arabic"], choice["chosen_arabic"]),), "Unknown or mismatched ownership schema")


def normalize(repo=REPO, english_root=ENGLISH, *, read: Callable[[Path], bytes] | None = None) -> Batch:
    """Consume only the four pinned ledgers and their named finite source inputs."""
    repo, english_root = Path(repo).resolve(), Path(english_root).resolve()
    reader = read or Path.read_bytes
    inputs: dict[Path, Identity] = {}
    cached: dict[Path, bytes] = {}

    def load(path):
        path = path.resolve()
        if path not in cached:
            raw = reader(path)
            require(len(raw) < 2 * 1024 * 1024, "Oversized finite input")
            cached[path] = raw
            inputs[path] = Identity(path.as_posix(), len(raw), sha(raw))
        return cached[path]

    def local(relative):
        path = (repo / relative).resolve()
        require(path.is_relative_to(repo), "Input escaped repository")
        return path

    def identify(path_value):
        path = Path(path_value)
        path = path.resolve() if path.is_absolute() else local(path_value)
        for unit, filename in UNIT_FILES.items():
            if path == (english_root / CONTENT / filename).resolve():
                return path, unit, "english"
            for edition, prefix in (("msa", "ar"), ("classical", "ar-classical")):
                if path == (repo / "source/locale" / prefix / CONTENT / filename).resolve():
                    return path, unit, edition
        if path == local("source/locale/ar/open-logic-config.sty"):
            return path, "shared", "shared"
        raise ValueError("Unadmitted source path")

    def public_identity(path, raw):
        logical = path.relative_to(repo).as_posix() if path.is_relative_to(repo) else path.as_posix()
        return Identity(logical, len(raw), sha(raw))

    ledgers, transitions, decisions = [], [], []
    all_patch_ids, all_ids = set(), set()
    pairing_payload = None
    for contract in CONTRACTS:
        ledger_path = REPAIRS + contract.stem + ".json"
        raw = load(local(ledger_path))
        require((sha(raw), len(raw)) == (contract.sha256, contract.bytes), "Pinned ledger identity differs: " + contract.stem)
        payload = parse(raw)
        require(payload["schema"] == contract.schema, "Ledger schema differs")
        choices, transactions = payload["decisions"], payload["transactions"]
        require(tuple(d["decision_id"] for d in choices) == contract.decision_ids, "Decision inventory/order differs")
        require(tuple(tuple(p["patch_id"] for p in t["patches"]) for t in transactions) == contract.transaction_patches, "Transaction/patch order differs")
        require(not all_ids.intersection(contract.decision_ids), "Duplicate batch decision")
        all_ids.update(contract.decision_ids)
        if contract.decision_ids == PAIRING_IDS:
            pairing_payload = payload
        # (resolved path, sha) -> exact before/current source, plus phase proof.
        versions = {}
        local_transitions = []
        for transaction in transactions:
            path, unit, edition = identify(transaction["path"])
            require((unit, edition) == (transaction["unit_id"], transaction["edition"]) and edition in ("msa", "classical"), "Transaction ownership differs")
            after = load(path)
            check_identity(after, transaction, "after_")
            before = after
            for patch in reversed(transaction["patches"]):
                require(patch["before"] != patch["after"] and patch.get("occurrences", 1) == 1, "Unchanged or repeated patch")
                old, new = patch["before"].encode(), patch["after"].encode()
                require(before.count(new) == 1, "Inverse replacement is not unique")
                before = before.replace(new, old, 1)
            check_identity(before, transaction, "before_")
            if "before_path" in transaction:
                require(load(local(transaction["before_path"])) == before, "Stored predecessor differs from inverse")
            bid, aid = public_identity(path, before), public_identity(path, after)
            versions[(path, bid.sha256)] = (before, bid, "historical-before")
            versions[(path, aid.sha256)] = (after, aid, "applied-current-source")
            replay, patches = before, []
            for index, patch in enumerate(transaction["patches"]):
                pid = patch["patch_id"]
                require(pid not in all_patch_ids, "Duplicate patch ID")
                all_patch_ids.add(pid)
                owners, basis = patch_owners(transaction, patch, choices)
                bp = exact_location(before, bid, patch["before"], patch["before_location"])
                ap = exact_location(after, aid, patch["after"], patch["after_location"])
                require(replay.count(patch["before"].encode()) == 1, "Forward replacement is not unique")
                replay = replay.replace(patch["before"].encode(), patch["after"].encode(), 1)
                patches.append(Patch(pid, owners, index, bp, ap, basis, json_text(patch)))
            require(replay == after, "Forward replay differs")
            physical = sorted(patches, key=lambda p: p.before.byte_start)
            require(all(a.before.byte_end <= b.before.byte_start and a.after.byte_end <= b.after.byte_start for a, b in zip(physical, physical[1:])), "Patches overlap or physical order changed")
            transition = SourceTransition(ledger_path, unit, edition, bid, aid, before, after, tuple(patches), tuple(p.patch_id for p in physical))
            local_transitions.append(transition)
            transitions.append(transition)
        inventory = payload.get("primary_source_inventory")
        if inventory is None:
            require(contract.decision_ids == REDUCTION_IDS, "Missing primary source inventory")
            english = payload["english_source"]
            inventory = [{"path": english["path"], "edition": "english", "before_bytes": english["bytes"], "after_bytes": english["bytes"],
                          "before_sha256": english["sha256"], "after_sha256": english["sha256"]}] + list(transactions)
        inventoried = set()
        for item in inventory:
            path, unit, edition = identify(item["path"])
            require(path not in inventoried and item["edition"] == edition and item.get("unit_id", unit) == unit, "Duplicate or mismatched primary inventory")
            inventoried.add(path)
            current = load(path)
            check_identity(current, item, "after_")
            if edition in ("english", "shared"):
                check_identity(current, item, "before_")
                if edition == "english":
                    require(sha(current) == ENGLISH_HASHES[unit], "Frozen English differs")
                sid = public_identity(path, current)
                versions[(path, sid.sha256)] = (current, sid, "unchanged")
            else:
                require((path, item["before_sha256"]) in versions and (path, item["after_sha256"]) in versions, "Inventory not bound to exact transaction")
                check_identity(versions[(path, item["before_sha256"])][0], item, "before_")
        require(all(local(t.after.path) in inventoried for t in local_transitions), "Transaction omitted from source inventory")

        def witness(value, inherited_path=None, inherited_hash=None):
            path, _, _ = identify(value.get("path", inherited_path))
            wanted = value.get("sha256", inherited_hash)
            require((path, wanted) in versions, "Witness names an unproved source phase")
            body, sid, phase = versions[(path, wanted)]
            if "bytes" in value:
                require(value["bytes"] == len(body), "Witness byte count differs")
            literal = value.get("literal", value.get("text"))
            require(isinstance(literal, str), "Witness lacks exact literal")
            loc = exact_location(body, sid, literal, value, witness_newline_endpoint=True)
            return Witness(loc, value.get("phase", "unspecified"), phase, json_text(value))

        normalized = []
        for index, choice in enumerate(choices):
            owned = tuple(p for t in local_transitions for p in t.patches if choice["decision_id"] in p.decision_ids)
            require(owned and choice.get("open_to_correction") is True, "Choice has no patch or provisional evidence flag")
            check_choice_ownership(choice, owned)
            require(isinstance(choice.get("rationale"), str) and choice["rationale"], "Choice rationale missing")
            witnesses = [witness(w) for w in choice.get("source_witnesses", [])]
            witnesses += [witness(w) for w in choice.get("literal_review_occurrences", [])]
            for binding in choice.get("occurrence_bindings", []):
                witnesses += [witness(loc, binding["path"], binding["sha256"]) for loc in binding["locations"]]
            for occurrence in choice.get("occurrences", []):
                require(occurrence["unit_id"] == choice["unit_id"], "Occurrence unit differs")
                witnesses.append(witness(occurrence["english"], occurrence["source_path"], occurrence["source_sha256"]))
                witnesses.append(witness(occurrence, occurrence["target_path"], occurrence["target_sha256"]))
            require(any(w.verified_phase == "unchanged" and Path(w.location.source.path).is_relative_to(english_root)
                        for w in witnesses), "Choice lacks proved English witness")
            row = Decision(choice["decision_id"], choice["unit_id"], choice["edition"], ledger_path, index,
                choice["status"], choice.get("recording_mode", payload.get("recording_mode", "")), choice["rationale"], owned, tuple(witnesses), json_text(choice))
            normalized.append(row)
            decisions.append(row)
        ledgers.append(Ledger(Identity(ledger_path, len(raw), sha(raw)), raw, payload["status"], tuple(normalized)))
    require((len(decisions), len(transitions), len(all_patch_ids)) == (23, 10, 25), "Finite batch inventory differs")
    require(len({s.after.path for s in transitions}) == 10, "Changed source repeated across batch")
    application = pairing_payload["application"]
    require(REPAIRS + application["prepared_ledger_history"] == PROPOSAL_HISTORY and application["prepared_ledger_sha256"] == PROPOSAL_SHA, "Proposal predecessor identity differs")
    prior_raw = load(local(PROPOSAL_HISTORY))
    require(sha(prior_raw) == PROPOSAL_SHA, "Proposal predecessor bytes differ")
    prior = parse(prior_raw)
    require(tuple(d["decision_id"] for d in prior["decisions"]) == PAIRING_IDS, "Proposal history IDs/order differ")
    supersessions = []
    for old, current in zip(prior["decisions"], pairing_payload["decisions"]):
        changed = tuple(k for k in current if current[k] != old.get(k))
        require(set(old) == set(current) and set(changed) == {"status", "page_status", "occurrence_bindings"}, "Proposal history altered beyond exact application transition")
        require(old["status"] == "proposed-unapplied" and current["status"] == "provisional-in-use", "Unexpected proposal status transition")
        supersessions.append(Supersession(current["decision_id"], old["status"], current["status"], json_text(old), json_text(current),
            Identity(PROPOSAL_HISTORY, len(prior_raw), sha(prior_raw)), changed))
    # Detect concurrent edits after every proof, without any directory scan.
    for path, expected in inputs.items():
        require((len(raw := reader(path)), sha(raw)) == (expected.bytes, expected.sha256), "Input changed during finite admission")
    return Batch(tuple(ledgers), tuple(decisions), tuple(transitions), tuple(supersessions), tuple(inputs.values()))


if __name__ == "__main__":
    result = normalize()
    print(json.dumps({"status": "PASS_FINITE_CARDINALITY_ADMISSION", "ledgers": len(result.ledgers),
        "decisions": len(result.decisions), "patches": sum(len(s.patches) for s in result.sources),
        "changed_sources": len(result.sources), "explicit_proposal_supersessions": len(result.supersessions),
        "inputs": len(result.input_identities), "scope": result.scope}))
