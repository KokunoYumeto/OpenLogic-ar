"""Independent readback of the six OLP-0014 additive-note review choices.

No producer import or generated PASS flag establishes admission. The immutable
record, reversible source insertion, English passages and consulted canon files
are checked directly before generated JSON and human surfaces are compared.
"""
import base64
import hashlib
import html
import json
from pathlib import Path
import re
from urllib.parse import unquote


PREFIX = "olp0014-domain-size-20260909:"
LEDGER_PATH = "evidence/classical/repairs/olp0014-domain-size-20260909/REPAIR_RECORD.json"
LEDGER_SHA = "48c352e665b1dcf7f7ebfe1900e0ea625b794408d2e18aad81e563d3e4602ea1"
BEFORE_PATH = "evidence/classical/repairs/olp0014-domain-size-20260909/BEFORE_SOURCES.json"
BEFORE_SHA = "e31555b2577a75b86d52022736f655f2c59569325db296c98a50582cf1514f40"
LOCATOR_STATUS = "source-clarification-exact-note-verified"
RELATIVE_SOURCE = "content/sets-functions-relations/relations/special-properties.tex"
SOURCE_PATHS = {"msa": "source/locale/ar/" + RELATIVE_SOURCE,
                "classical": "source/locale/ar-classical/" + RELATIVE_SOURCE}
DECISION_IDS = tuple(PREFIX + kind + ":" + family for kind in SOURCE_PATHS for family in
                     ("fixed-domain-scope", "two-elements-iff", "separate-antisymmetry-condition"))


def require(value, reason):
    if not value:
        raise ValueError("independent OLP-0014 note: " + reason)


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def byte_sha(data):
    return hashlib.sha256(data).hexdigest()


def read_small(path, inputs, expected=None):
    require(path.stat().st_size <= 2 * 1024 * 1024, "oversized source/record: " + str(path))
    data = path.read_bytes()
    digest = byte_sha(data)
    require(expected is None or digest == expected.lower(), "pinned bytes differ: " + str(path))
    inputs[str(path.resolve())] = digest
    return data


def excerpt(data, declaration):
    lines = data.decode("utf-8").splitlines()
    first, last = declaration["line_start"], declaration["line_end"]
    require(type(first) is int and type(last) is int and 1 <= first <= last <= len(lines),
            "invalid source line interval")
    text = "\n".join(lines[first - 1:last])
    require(text == declaration["excerpt"], "exact source excerpt differs")
    if "excerpt_sha256" in declaration:
        require(byte_sha(text.encode()) == declaration["excerpt_sha256"].lower(), "excerpt hash differs")
    return text


def file_identity(path, declaration, inputs):
    require(path.stat().st_size == declaration["bytes"], "canon byte count differs: " + str(path))
    digest = inputs.get(str(path.resolve()))
    if digest is None:
        digest = sha(path)
        inputs[str(path.resolve())] = digest
    require(digest == declaration["sha256"].lower(), "canon hash differs: " + str(path))


def expectations(repo, english_root):
    """Return six independently source-checked specifications and input hashes."""
    repo, english_root = Path(repo).resolve(), Path(english_root).resolve()
    inputs = {}
    raw = read_small(repo / LEDGER_PATH, inputs, LEDGER_SHA)
    payload = json.loads(raw.decode("utf-8"))
    before_raw = read_small(repo / BEFORE_PATH, inputs, BEFORE_SHA)
    before = json.loads(before_raw.decode("utf-8"))
    require(payload["schema"] == "openlogic-ar-source-clarification-record-v1"
            and payload["repair_id"] == "olp0014-domain-size-20260909"
            and payload["unit_id"] == "OLP-0014" and payload["recorded_on"] == "2026-09-09"
            and payload["recording_mode"] == "contemporaneous" and payload["human_review_gate"] is False,
            "ledger identity/date/scope differs")
    require(before["schema"] == "openlogic-ar-exact-source-before-v1"
            and before["repair_id"] == payload["repair_id"]
            and payload["before_preservation"]["path"] == BEFORE_PATH,
            "preservation identity differs")
    prior = {entry["path"]: entry for entry in before["files"]}
    require(len(before["files"]) == len(prior) == 2 and set(prior) == set(SOURCE_PATHS.values()),
            "before-source inventory differs")
    changes = payload["source_changes"]
    require(len(changes) == 2 and {c["edition"] for c in changes} == set(SOURCE_PATHS),
            "two-edition source inventory differs")
    sources = {}
    for change in changes:
        kind, name = change["edition"], change["path"]
        require(name == SOURCE_PATHS[kind], "source edition/path differs")
        data = read_small(repo / name, inputs, change["sha256"])
        require(len(data) == change["bytes"], "current source byte count differs")
        saved = base64.b64decode(prior[name]["base64"], validate=True)
        require(len(saved) == prior[name]["bytes"] == change["before_bytes"]
                and byte_sha(saved) == prior[name]["sha256"] == change["before_sha256"],
                "preserved predecessor bytes differ")
        block = base64.b64decode(change["inserted_block_base64"], validate=True)
        require(block and data.count(block) == 1 and block == (change["note_text"] + "\n\n").encode(),
                "unique inserted note block differs")
        require(data.replace(block, b"", 1) == saved, "source changed beyond the additive note")
        note = excerpt(data, {**change, "excerpt": change["note_text"]})
        require(byte_sha(note.encode()) == change["note_sha256"] and re.findall(r"\$([^$]*)\$", note) == ["A", "A"],
                "note text/notation differs")
        excerpt(data, change["original_paragraph"])
        sources[kind] = data

    english = payload["authority"]["english"]
    require(english["source_relative"] == RELATIVE_SOURCE, "English source ownership differs")
    en_data = read_small(english_root / RELATIVE_SOURCE, inputs, english["sha256"])
    require(len(en_data) == english["bytes"] and len(english["passages"]) == 3,
            "English identity/passage inventory differs")
    for passage in english["passages"]:
        excerpt(en_data, passage)
    checks = payload["authority"]["canon_checks"]
    require(len(checks) == 3 and {c["physical_page"] for c in checks} == {42, 378, 602},
            "consulted canon inventory differs")
    for check in checks:
        source, page = check["source"], check["page_image"]
        source_path, page_path = (repo / source["path"]).resolve(), (repo / page["path"]).resolve()
        require(source_path.is_relative_to(repo.parent / "sources/DAM2018ENAR")
                and page_path.is_relative_to(repo / "tmp/pdfs")
                and check["consulted_before_choice"] is True and check["limits"], "canon scope/provenance differs")
        file_identity(source_path, source, inputs)
        file_identity(page_path, page, inputs)
    choices = payload["terminology_decisions"]
    require(tuple(c["decision_id"] for c in choices) == DECISION_IDS, "six-choice inventory differs")
    identity = {"path": LEDGER_PATH, "bytes": len(raw), "sha256": LEDGER_SHA.upper(),
                "adapter": {"kind": "source-clarification-olp0014-domain-size-v1", "terminology_rows_contributed": 6}}
    specs = {}
    for choice in choices:
        kind = choice["edition"]
        require(choice["open_to_correction"] is True and choice["expert_review_useful"] is True
                and choice["official_attestation_claimed"] is False and choice["recording_mode"] == "contemporaneous"
                and "new editorial inference" in choice["source_proposition_status"], "choice provenance differs")
        require(len(choice["occurrences"]) == 1, "choice occurrence inventory differs")
        loc = choice["occurrences"][0]
        require(loc["unit_id"] == "OLP-0014" and loc["source_kind"] == kind and loc["path"] == SOURCE_PATHS[kind]
                and loc["sha256"] == byte_sha(sources[kind]), "choice source ownership differs")
        text = excerpt(sources[kind], loc)
        require(choice["chosen_arabic"] in text and text.count(choice["chosen_arabic"]) == 1,
                "chosen literal absent or repeated in note")
        require(all(check in checks for check in choice["authority_checks"]), "choice canon provenance differs")
        occurrence = {"unit_id": "OLP-0014", kind: {"path": loc["path"], "sha256": loc["sha256"].upper(),
            "locator_status": LOCATOR_STATUS, "locators": [{"line_start": loc["line_start"], "line_end": loc["line_end"],
                "excerpt": loc["excerpt"], "ledger_locator_status": LOCATOR_STATUS}]}}
        specs[choice["decision_id"]] = {"choice": choice, "payload": payload, "before": before,
            "identity": identity, "occurrence": occurrence, "location": loc}
    return specs, inputs


def visible(value):
    return " ".join(html.unescape(re.sub(r"</?(?:span|a|br|em|strong)\b[^>]*>", "", str(value or ""))).split())


def literal(value):
    return visible(value).replace("$", "")


def validate_row(row, specs, surfaces, csv_rows, errors):
    """Validate one admitted note row and all its rendered surfaces; return success."""
    key = row["decision_id"]
    if key not in specs:
        if key.startswith(PREFIX) or row.get("source_clarification"):
            errors.append(key + ": uncommissioned/unverified source clarification")
        return False
    previous_errors = len(errors)
    def check(condition, message):
        if not condition:
            errors.append(key + ": " + message)
    spec = specs[key]
    choice, loc = spec["choice"], spec["location"]
    for field, value in choice.items():
        if field != "occurrences":
            check(field in row and row[field] == value, "canonical clarification field differs: " + field)
    check(row.get("source_record") == spec["identity"], "clarification source ledger identity/adapter differs")
    check(row.get("source_clarification") == {"ledger_path": LEDGER_PATH, "ledger_sha256": LEDGER_SHA.upper(),
        "source_ledger": spec["payload"], "choice_record": choice, "historical_before_sources": spec["before"]},
        "full clarification provenance differs")
    check(row.get("occurrences") == [spec["occurrence"]], "normalized clarification occurrence differs")
    check(not row.get("semantic_propagation_repair") and not row.get("expert_review_assessment"),
          "clarification misclassified as a different repair/assessment")
    check(row.get("printed_page") is None, "source-only clarification invents a printed page")
    metadata = row.get("index_metadata", {})
    check(metadata.get("human_index_included") is True, "clarification excluded from human index")
    groups = metadata.get("occurrences", [])
    check(len(groups) == 1, "clarification human occurrence inventory differs")
    first, last = loc["line_start"], loc["line_end"]
    suffix = f"#L{first}-L{last}"
    wanted = loc["path"] + suffix
    if len(groups) == 1:
        group = groups[0]
        check(group.get("unit", {}).get("unit_id") == "OLP-0014" and group.get("human_review_included") is True,
              "clarification human occurrence unit/inclusion differs")
        check(group.get("raw_occurrence") == spec["occurrence"]
              and group.get("human_review_location_count") == 1 and group.get("machine_location_count") == 1,
              "clarification human occurrence provenance/count differs")
        locations = group.get("locations", [])
        check(len(locations) == 1, "clarification requires exactly one human note location")
        if len(locations) == 1:
            location = locations[0]
            rec = location.get("line_reconciliation", {})
            check(location.get("source_kind") == choice["edition"] and location.get("logical_path") == loc["path"]
                  and location.get("recorded_path") == loc["path"] and location.get("current_excerpt") == loc["excerpt"]
                  and location.get("excerpt") == loc["excerpt"]
                  and location.get("current_sha256", "").lower() == loc["sha256"]
                  and location.get("recorded_sha256", "").lower() == loc["sha256"], "human note source identity/excerpt differs")
            check(location.get("location_id") == key + ":occ001:" + choice["edition"] + ":loc001"
                  and location.get("ledger_locator_status") == LOCATOR_STATUS,
                  "human note locator identity/provenance differs")
            check(rec.get("resolved") is True and rec.get("recorded_hash_matches_current") is True
                  and (rec.get("current_line_start"), rec.get("current_line_end")) == (first, last)
                  and (location.get("line_start"), location.get("line_end")) == (first, last)
                  and location.get("human_review_included") is True, "human note source reconciliation differs")
            check(not location.get("page_evidence"), "source-only clarification invents PDF page evidence")
            check(unquote(location.get("source_url") or "").endswith(wanted)
                  and location.get("source_url") == (location.get("file_url") or "") + suffix,
                  "human note source URL differs")
    reason, question = visible(choice["rationale"]), visible(choice["expert_question"])
    for name in ("complete", "priority"):
        check(bool(surfaces.get(name, {}).get(key)), "missing clarification section: " + name)
    for prefix in ("complete-", "priority-"):
        check(any(key in mapping for name, mapping in surfaces.items() if name.startswith(prefix)),
              "missing detailed clarification shard: " + prefix)
    for name, mapping in surfaces.items():
        for section in mapping.get(key, []):
            why = " ".join(line for line in section.splitlines() if "**Why this choice / سبب الاختيار:**" in line)
            questions = " ".join(line for line in section.splitlines() if "**Please double-check / يُرجى التحقق:**" in line
                                 or "PLEASE DOUBLE-CHECK THIS CHOICE" in line)
            check(reason in visible(why), "missing/truncated clarification reason: " + name)
            check(question in visible(questions), "missing/truncated clarification question: " + name)
            check(re.search(re.escape(wanted) + r"(?=$|[\s)>])", unquote(section)) is not None,
                  "missing exact clarification source link: " + name)
    rows = csv_rows.get(key, [])
    check(len(rows) == 1, "clarification CSV occurrence inventory differs")
    for values in rows:
        check(len(values) == 13, "clarification CSV column count differs")
        if len(values) != 13:
            continue
        check(reason in visible(values[5]) and question in visible(values[12]), "CSV clarification explanation/question differs")
        check(literal(choice["chosen_arabic"]) == literal(values[3]) and choice["english_term"] in visible(values[2]),
              "CSV clarification source/chosen wording differs")
        check(re.match(r"OLP-0014(?=$|\s)", values[7]) is not None, "CSV clarification unit differs")
        parsed = re.findall(r"([^\s|]+):L(\d+)(?:–L(\d+))?(?=$|[\s|])", values[8])
        check(parsed == [(loc["path"], str(first), str(last))]
              and re.search(re.escape(wanted) + r"(?=$|[\s)>])", unquote(values[8])) is not None,
              "CSV exact clarification source locator/link differs")
        check(not values[9].strip() and not values[10].strip(), "CSV clarification invents PDF page evidence")
    return len(errors) == previous_errors
