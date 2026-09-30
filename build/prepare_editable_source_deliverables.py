#!/usr/bin/env python3
"""Prepare the three direct TeX/source-ZIP deliverables without running TeX.

The direct ``.tex`` files are truthful archival aggregates made by
``assemble_complete_722_tex.py``.  Each source ZIP preserves the real two-job
source layout, the exact 722 compiled bodies, the necessary local styles,
figures, bibliography, fonts and reconstruction programs, and Arabic build
instructions.  No network or publication operation is performed here.

The command writes two independent staging passes and refuses success unless
all six release-facing files are byte-identical between the primary and cold
replay passes.

Generated graph files are immutable.  The six-file current namespace is
created transactionally only when it is wholly absent; an existing namespace
must already be complete and byte-identical to the graph recomputed from the
current source snapshot.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import shutil
import stat
import sys
import tempfile
from typing import Any, Iterable, Mapping, Sequence
import zipfile


sys.path.insert(0, str(Path(__file__).resolve().parent))
import assemble_complete_722_tex as aggregate


SCHEMA = "openlogic-arabic-editable-source-deliverables-v1"
BUNDLE_SCHEMA = "openlogic-arabic-complete-source-bundle-v1"
REPLAY_SCHEMA = "openlogic-arabic-editable-source-cold-replay-v1"
AI_DISCLOSURE = "OpenAI Codex — GPT-6.1 Sol, Ultra effort"
AI_REPAIR_DISCLOSURE = "OpenAI Codex — GPT-6 Astra, Ultra effort"
AI_PREVIOUS_LAYOUT_DISCLOSURE = "OpenAI Codex — GPT-6 Sol, Ultra effort"
AI_PREVIOUS_NAMED_DISCLOSURE = "OpenAI Codex — GPT-6 Sol, Ultra effort"
AI_INHERITED_DISCLOSURE = "OpenAI Codex — GPT-5.6 Sol, Ultra effort"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
ZIP_MODE = 0o100644
INHERITED_ZENODO_FILES = 71
ZENODO_FILE_CAP = 100
MAX_NEW_FILES = ZENODO_FILE_CAP - INHERITED_ZENODO_FILES
NEW_RELEASE_FILES = 6
CURRENT_MSA_MODE = False
CURRENT_MSA_GRAPH_ROOT = "evidence/editable-source-deliverables-20260930-v13-msa-quantifier-reference-items"
CURRENT_MSA_MANIFEST = "evidence/msa-source-successor-20260930/EFFECTIVE_BUILD_MANIFEST.json"
CURRENT_MSA_REBIND = "evidence/provenance/openlogic-control/MSA_CLOSURE_MANIFEST_REBIND_20260930_FORMULA_ANNOTATED.json"
CURRENT_REFERENCE_LEDGER = "evidence/classical/terminology/SOL6_ARABIC_REFERENCE_LOCALIZATION_20260930.json"

RECONCILIATION = (
    "evidence/classical/SOURCE_RECONCILIATION_CLOSURE_MANIFEST_20260905.json"
)
ACCEPTANCE = "evidence/classical/FULL_TRANSLATION_ACCEPTANCE_AUDIT.json"
PRESENTATION = "evidence/classical/NOTATION_MATERIALIZATION_RECEIPT.json"
DECISIONS = "evidence/classical/NOTATION_MATERIALIZATION_DECISIONS.json"
MSA_REBIND = (
    "evidence/provenance/openlogic-control/"
    "MSA_CLOSURE_MANIFEST_REBIND_20260905.json"
)
# Previous graph namespaces are immutable.  The current source successor
# receives a fresh namespace, never an overwrite of the published v3 graph.
HISTORICAL_GRAPH_ROOTS = (
    "evidence/editable-source-deliverables-20260922",
    "evidence/editable-source-deliverables-20260924",
    "evidence/editable-source-deliverables-20260924-v2",
    "evidence/editable-source-deliverables-20260924-v3",
    "evidence/editable-source-deliverables-20260925-v4",
    "evidence/editable-source-deliverables-20260926-v5",
    "evidence/editable-source-deliverables-20260926-v6-bibltr-meta",
    "evidence/editable-source-deliverables-20260926-v7-bibltr-mathdir",
    "evidence/editable-source-deliverables-20260928-v8-fn-ltr",
    "evidence/editable-source-deliverables-20260928-v9-fn-unicode",
    "evidence/editable-source-deliverables-20260928-v10-fn-unicode-attributed",
)
GRAPH_ROOT = "evidence/editable-source-deliverables-20260928-v11-fixed-names"
EXPECTED_RECONCILIATION_SHA256 = (
    "7efe0a46648cff60f0f179c98ab01d948630bfe4b7dd944f0f8061b728c18ef1"
)
EXPECTED_PRESENTATION_SHA256 = (
    "a3817d79ed98a104594c9db428f72a0c590162dfed02c59a3d2c47bf69a7a5a4"
)
EXPECTED_CLASSICAL_SOURCE_TREE_SHA256 = (
    "F6590340CFD3B0FC291A535BCF124849AEA8DF08F45FA6DAE59FE7FF061DCA4F"
)
EXPECTED_CLASSICAL_PRESENTATION_TREE_SHA256 = (
    "B6D83898A2F648C149E15BC485F52A047F8302ABB390A28A1187FC79BB85FB37"
)

ROLE_ORDER = (
    "msa-international",
    "msa-machrek",
    "classical-eastern-rtl",
)
ROLE_STEMS = {
    "msa-international": "OPENLOGIC_ar_R3_MSA_INTERNATIONAL",
    "msa-machrek": "OPENLOGIC_ar_R3_MSA_MACHREK",
    "classical-eastern-rtl": "OPENLOGIC_ar_R3_CLASSICAL_EASTERN_RTL",
}

COMMON_SOURCE_FILES = (
    "source/open-logic-config.sty",
    "source/open-logic-envs.sty",
    "source/open-logic-locale.sty",
    "source/sty/bussproofs-extra.sty",
    "source/sty/open-logic-defer.sty",
    "source/sty/open-logic-formulas.sty",
    "source/sty/open-logic-referencing.sty",
    "source/sty/open-logic-selective.sty",
    "source/sty/open-logic-tokenize.sty",
    "source/sty/open-logic.sty",
    "source/sty/ptolemaicastronomy.sty",
    "source/assets/diagrams/bijective.tikz",
    "source/assets/diagrams/composition.tikz",
    "source/assets/diagrams/difference.tikz",
    "source/assets/diagrams/function.tikz",
    "source/assets/diagrams/injective.tikz",
    "source/assets/diagrams/intersection.tikz",
    "source/assets/diagrams/surjective.tikz",
    "source/assets/diagrams/turing-machine.tikz",
    "source/assets/diagrams/union.tikz",
    "source/bib/natbib-oup.bst",
    "source/bib/open-logic.bib",
)
SCHEHERAZADE_RUNTIME = (
    "00_control/fonts/scheherazade-2.100/Scheherazade-Bold.ttf",
    "00_control/fonts/scheherazade-2.100/Scheherazade-Regular.ttf",
)
SCHEHERAZADE_AUXILIARY = (
    "00_control/fonts/scheherazade-2.100/FONT_RECEIPT.md",
    "00_control/fonts/scheherazade-2.100/OFL.txt",
)
XITS_RUNTIME = (
    "source/locale/ar/fonts/vendor/xits-1.302/XITSMath-Regular.otf",
)
XITS_AUXILIARY = (
    "source/locale/ar/fonts/vendor/xits-1.302/OFL.txt",
)

MSA_SOURCE_SUPPORT = (
    "source/locale/ar/open-logic-complete-ar.tex",
    "source/locale/ar/open-logic-closure-supplement-ar.tex",
    "source/locale/ar/open-logic-complete-ar-readable-letter-international.tex",
    "source/locale/ar/open-logic-closure-supplement-ar-readable-letter-international.tex",
    "source/locale/ar/open-logic-complete-ar-readable-letter-machrek.tex",
    "source/locale/ar/open-logic-closure-supplement-ar-readable-letter-machrek.tex",
    "source/locale/ar/open-logic-readable-letter-r2-layout-ar.tex",
    "source/locale/ar/open-logic-notation-profile-ar.tex",
    "source/locale/ar/open-logic-config.sty",
    "source/locale/ar/open-logic-locale.sty",
    "source/locale/ar/fonts/OpenLogicMachrekDigits-Regular.otf",
    *XITS_RUNTIME,
    *XITS_AUXILIARY,
)
CLASSICAL_SOURCE_SUPPORT = (
    "source/locale/ar-classical/open-logic-complete-ar-classical-eastern-rtl.tex",
    "source/locale/ar-classical/open-logic-closure-supplement-ar-classical-eastern-rtl.tex",
    "source/locale/ar-classical/open-logic-ar-classical-eastern-rtl-preamble.tex",
    "source/locale/ar-classical/open-logic-letters-ar-classical.tex",
    "source/locale/ar-classical/open-logic-named-atoms-ar-classical.tex",
    "source/locale/ar-classical/open-logic-numerals-ar-classical.tex",
    "source/locale/ar-classical/open-logic-rtl-math.tex",
    "source/locale/ar-classical/open-logic-sets-ar-classical.tex",
    "source/locale/ar-classical-presentation/open-logic-materialization-contract.tex",
    "source/locale/ar/open-logic-readable-letter-r2-layout-ar.tex",
    "source/locale/ar/open-logic-config.sty",
    "source/locale/ar/open-logic-locale.sty",
    *XITS_RUNTIME,
    *XITS_AUXILIARY,
)

COMMON_BUILD_FILES = (
    "build/assemble_complete_722_tex.py",
    "build/Invoke-WithInterlanguageTeXMutex.ps1",
    "build/repair_rtl_link_rects_letter_ar.py",
    "build/repair_rtl_link_rects_ar.py",
)
MSA_BUILD_FILES = (
    *COMMON_BUILD_FILES,
    "build/BUILD_DUAL_NOTATION.ps1",
    "build/BUILD_DUAL_NOTATION_INNER.ps1",
    "build/BUILD_COMPLETE_DUAL_NOTATION_REQUIREMENTS.md",
    "build/assemble_complete_722_reader.py",
    "build/audit_arabic_notation_profiles.py",
    "build/make_machrek_digit_font.py",
    "build/profile_checkpoint.py",
    "build/qa_dual_notation_pdfs.py",
    "build/rebind_msa_closure_manifest.py",
)
CLASSICAL_BUILD_FILES = (
    *COMMON_BUILD_FILES,
    "build/BUILD_CLASSICAL_ARABIC_EASTERN_RTL.ps1",
    "build/BUILD_CLASSICAL_ARABIC_EASTERN_RTL_INNER.ps1",
    "build/assemble_classical_722_reader.py",
    "build/assemble_complete_722_reader.py",
    "build/classical_closure_successor_adapter_20260913.py",
    "build/classical_implicit_carrier_successor_20260910.py",
    "build/classical_reader_build_contract.py",
    "build/materialize_classical_notation.py",
    "build/tests/verify_classical_layout_u14_u16_static.py",
    "build/validate_classical_overlay.py",
    "build/validate_classical_rtl_closure_receipt.py",
    "build/verify_classical_reader_routing.py",
)

MSA_EVIDENCE_FILES = (
    RECONCILIATION,
    ACCEPTANCE,
    MSA_REBIND,
    "evidence/provenance/openlogic-control/CLOSURE_MANIFEST.csv",
    "evidence/notation/PROFILE_MAPPING.json",
    "evidence/notation/MACHREK_DIGIT_FONT_PROVENANCE.json",
    "evidence/notation/DUAL_NOTATION_REPRODUCIBILITY.json",
)
CLASSICAL_EVIDENCE_FILES = (
    RECONCILIATION,
    ACCEPTANCE,
    PRESENTATION,
    DECISIONS,
    "evidence/classical/NOTATION_MATERIALIZATION_POLICY.json",
    "evidence/classical/NOTATION_MATERIALIZATION_SUMMARY.md",
    "evidence/classical/BASELINE.json",
    "evidence/classical/LETTER_PRESENTATION_REGISTRY.json",
    "evidence/classical/SET_SYMBOL_MAPPING.json",
    "evidence/classical/SOURCE_RECONCILIATION_AUDIT_20260905.json",
    "evidence/classical/SOURCE_RECONCILIATION_METADATA_20260905.json",
    "evidence/classical/SOURCE_RECONCILIATION_STATIC_VALIDATION_20260905.json",
    "evidence/classical/BASELINE_CORRECTION_OVERLAY_FULL_20260905.json",
    "evidence/classical/MATH_TEXT_DECLARATIONS_FULL_20260905.json",
    "evidence/classical/STRUCTURAL_REVIEW_DECLARATIONS_FULL_20260905.json",
    "evidence/classical/FORMAL_REPAIR_DECLARATIONS_FULL_20260905.json",
    "evidence/classical/GENERAL_REVIEW_DECLARATIONS_FULL_20260905.json",
    "evidence/classical/RTL_RUNTIME_CLOSURE_20260905.json",
    "evidence/classical/repairs/CLASSICAL_LAYOUT_U14_U16_STATIC_RECEIPT_20260924.json",
)


class PreparationError(RuntimeError):
    """A source identity, staging, archive, or replay invariant failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PreparationError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def canonical_value_sha256(value: Any) -> str:
    data = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(data)


def normalize_relative(value: str, label: str) -> str:
    require(isinstance(value, str) and value, f"{label} is empty")
    require("\\" not in value and "\x00" not in value, f"{label} is not POSIX")
    posix = PurePosixPath(value)
    windows = PureWindowsPath(value)
    require(
        not posix.is_absolute()
        and not windows.is_absolute()
        and not windows.drive
        and posix.as_posix() == value
        and all(part not in {"", ".", ".."} and ":" not in part for part in posix.parts),
        f"{label} is unsafe: {value!r}",
    )
    return value


def descriptor(path: str, data: bytes) -> dict[str, Any]:
    return {"path": path, "bytes": len(data), "sha256": sha256_bytes(data)}


def descriptor_equal(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    return (
        left.get("path") == right.get("path")
        and left.get("bytes") == right.get("bytes")
        and str(left.get("sha256", "")).lower()
        == str(right.get("sha256", "")).lower()
    )


def _validated_descriptor(
    value: Any, label: str, *, expected_path: str | None = None
) -> dict[str, Any]:
    require(
        isinstance(value, dict) and set(value) == {"path", "bytes", "sha256"},
        f"{label} is not an exact file descriptor",
    )
    relative = normalize_relative(value.get("path"), f"{label}.path")
    if expected_path is not None:
        require(relative == expected_path, f"{label} has the wrong path")
    size = value.get("bytes")
    digest = value.get("sha256")
    require(type(size) is int and size >= 0, f"{label}.bytes is invalid")
    require(
        isinstance(digest, str)
        and len(digest) == 64
        and digest == digest.lower()
        and all(character in "0123456789abcdef" for character in digest),
        f"{label}.sha256 is invalid",
    )
    return {"path": relative, "bytes": size, "sha256": digest}


class Snapshot:
    """Capture repository files once and reject all later drift."""

    def __init__(self, repo: Path):
        self.repo = repo.resolve(strict=True)
        self.files: dict[str, bytes] = {}
        self.stats: dict[str, tuple[int, int, int, int]] = {}

    def capture(self, relative: str) -> bytes:
        relative = normalize_relative(relative, "snapshot path")
        if relative in self.files:
            return self.files[relative]
        lexical = self.repo / Path(*PurePosixPath(relative).parts)
        resolved = lexical.resolve(strict=True)
        require(resolved.is_file(), f"snapshot input is not a file: {relative}")
        require(resolved == Path(os.path.abspath(lexical)), f"symbolic path refused: {relative}")
        require(resolved.is_relative_to(self.repo), f"snapshot path escapes: {relative}")
        with resolved.open("rb") as stream:
            before = os.fstat(stream.fileno())
            data = stream.read()
            after = os.fstat(stream.fileno())
        require(before.st_nlink == 1 and after.st_nlink == 1, f"hardlink refused: {relative}")
        identity = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
        require(
            (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) == identity
            and len(data) == after.st_size,
            f"snapshot input changed while read: {relative}",
        )
        self.files[relative] = data
        self.stats[relative] = identity
        return data

    def describe(self, relative: str) -> dict[str, Any]:
        return descriptor(relative, self.capture(relative))

    def recorded(self, value: Mapping[str, Any], label: str) -> dict[str, Any]:
        require(isinstance(value, Mapping), f"{label} is not a descriptor")
        relative = normalize_relative(str(value.get("path", "")), f"{label}.path")
        observed = self.describe(relative)
        require(descriptor_equal(value, observed), f"{label} identity is stale")
        return observed

    def json(self, relative: str, label: str) -> dict[str, Any]:
        data = self.capture(relative)
        try:
            value = json.loads(data.decode("utf-8"), object_pairs_hook=_no_duplicates)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise PreparationError(f"{label} is not strict JSON") from error
        require(isinstance(value, dict), f"{label} root is not an object")
        return value

    def recheck(self) -> None:
        for relative, frozen in self.files.items():
            path = self.repo / Path(*PurePosixPath(relative).parts)
            resolved = path.resolve(strict=True)
            with resolved.open("rb") as stream:
                status = os.fstat(stream.fileno())
                data = stream.read()
            identity = (status.st_dev, status.st_ino, status.st_size, status.st_mtime_ns)
            require(identity == self.stats[relative], f"snapshot native identity drift: {relative}")
            require(status.st_nlink == 1, f"snapshot link-count drift: {relative}")
            require(data == frozen, f"snapshot byte drift: {relative}")


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise PreparationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def unique(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result


def _read_stable_regular(
    path: Path, label: str
) -> tuple[bytes, tuple[int, int, int, int], int]:
    resolved = path.resolve(strict=True)
    require(resolved.is_file(), f"{label} is not a file")
    require(resolved == Path(os.path.abspath(path)), f"{label} is symbolic")
    with resolved.open("rb") as stream:
        before = os.fstat(stream.fileno())
        data = stream.read()
        after = os.fstat(stream.fileno())
    identity = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    require(
        (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        == identity
        and len(data) == after.st_size,
        f"{label} changed while read",
    )
    require(before.st_nlink == 1 and after.st_nlink == 1, f"{label} is hardlinked")
    return data, identity, stat.S_IMODE(after.st_mode)


def _verify_acceptance_source_snapshot(
    snapshot: Snapshot,
    acceptance: Mapping[str, Any],
    reconciliation_rows: Sequence[Mapping[str, Any]],
    *,
    expected_ids: Sequence[str],
) -> dict[str, Any]:
    source_snapshot = acceptance.get("source_snapshot")
    expected_fields = {
        "schema",
        "status",
        "english_root",
        "unit_count",
        "live_source_bindings",
        "snapshot_sha256",
        "units",
    }
    require(
        isinstance(source_snapshot, dict) and set(source_snapshot) == expected_fields,
        "translation acceptance source_snapshot fields are not exact",
    )
    expected_count = len(expected_ids)
    require(
        source_snapshot.get("schema")
        == "openlogic-full-translation-source-snapshot-v1"
        and source_snapshot.get("status") == "PASS"
        and source_snapshot.get("unit_count") == expected_count
        and source_snapshot.get("live_source_bindings") == 3 * expected_count,
        "translation acceptance source_snapshot summary is not exact",
    )
    english_root_value = source_snapshot.get("english_root")
    require(
        isinstance(english_root_value, str)
        and english_root_value
        and Path(english_root_value).is_absolute(),
        "translation acceptance English root is not absolute",
    )
    english_root = Path(english_root_value).resolve(strict=True)
    require(english_root.is_dir(), "translation acceptance English root is not a directory")

    units = source_snapshot.get("units")
    require(
        isinstance(units, list)
        and len(units) == expected_count
        and len(reconciliation_rows) == expected_count,
        "translation acceptance source_snapshot is not unit-exact",
    )
    unit_fields = {"id", "english", "msa", "classical"}
    for identifier, item, reconciliation in zip(
        expected_ids, units, reconciliation_rows, strict=True
    ):
        require(
            isinstance(item, dict)
            and set(item) == unit_fields
            and item.get("id") == identifier
            and reconciliation.get("id") == identifier,
            f"translation acceptance source_snapshot order differs at {identifier}",
        )
        source_path = normalize_relative(
            str(reconciliation.get("source_path", "")),
            f"source reconciliation {identifier}.source_path",
        )

        for layer_name in ("msa", "classical"):
            recorded = _validated_descriptor(
                item.get(layer_name),
                f"translation acceptance {identifier}.{layer_name}",
            )
            reconciliation_descriptor = reconciliation.get(layer_name)
            require(
                isinstance(reconciliation_descriptor, Mapping)
                and descriptor_equal(recorded, reconciliation_descriptor),
                f"translation acceptance {identifier}.{layer_name} differs from reconciliation",
            )
            snapshot.recorded(
                recorded, f"translation acceptance {identifier}.{layer_name}"
            )

        english = _validated_descriptor(
            item.get("english"),
            f"translation acceptance {identifier}.english",
            expected_path=source_path,
        )
        require(
            english["sha256"] == reconciliation.get("english_sha256"),
            f"translation acceptance {identifier}.english differs from reconciliation",
        )
        english_lexical = english_root / Path(*PurePosixPath(source_path).parts)
        english_resolved = english_lexical.resolve(strict=True)
        require(
            english_resolved.is_relative_to(english_root),
            f"translation acceptance {identifier}.english escapes its root",
        )
        english_data, _, _ = _read_stable_regular(
            english_lexical, f"translation acceptance {identifier}.english"
        )
        require(
            descriptor_equal(english, descriptor(source_path, english_data)),
            f"translation acceptance {identifier}.english identity is stale",
        )

    require(
        isinstance(source_snapshot.get("snapshot_sha256"), str)
        and source_snapshot["snapshot_sha256"] == canonical_value_sha256(units),
        "translation acceptance source_snapshot fingerprint differs",
    )
    return {
        "status": "PASS_CURRENT_BYTES",
        "units_verified": expected_count,
        "bindings_verified": 3 * expected_count,
        "snapshot_sha256": source_snapshot["snapshot_sha256"],
    }


def _graph_paths(role: str) -> tuple[str, str]:
    return (
        f"{GRAPH_ROOT}/{role}-reader-642.graph.json",
        f"{GRAPH_ROOT}/{role}-closure-80.graph.json",
    )


def _role_graph_support(role: str) -> list[str]:
    config = aggregate.ROLE_CONFIG[role]
    result = [
        config["reader_master"],
        config["reader_wrapper"],
        config["closure_master"],
        config["closure_wrapper"],
        *COMMON_SOURCE_FILES,
        *SCHEHERAZADE_RUNTIME,
    ]
    if role in {"msa-international", "msa-machrek"}:
        result.extend(
            [
                "source/locale/ar/open-logic-readable-letter-r2-layout-ar.tex",
                "source/locale/ar/open-logic-notation-profile-ar.tex",
                "source/locale/ar/open-logic-config.sty",
                "source/locale/ar/open-logic-locale.sty",
            ]
        )
        if role == "msa-machrek":
            result.append("source/locale/ar/fonts/OpenLogicMachrekDigits-Regular.otf")
    else:
        result.extend(CLASSICAL_SOURCE_SUPPORT)
    return unique(result)


def _validate_generated_graph(
    graph: Any,
    *,
    role: str,
    partition: str,
    snapshot: Snapshot | None,
) -> None:
    require(role in ROLE_ORDER, f"unknown generated-graph role: {role}")
    require(partition in {"reader", "closure"}, f"unknown graph partition: {partition}")
    config = aggregate.ROLE_CONFIG[role]
    expected_ids = (
        aggregate.READER_IDS if partition == "reader" else aggregate.CLOSURE_IDS
    )
    expected_fields = {
        "schema",
        "status",
        "failures",
        "role",
        "profile",
        "partition",
        "master",
        "wrapper",
        "reconciliation",
        "presentation_mapping",
        "units",
        "dependencies",
    }
    require(
        isinstance(graph, dict) and set(graph) == expected_fields,
        f"generated graph {role}/{partition} fields are not exact",
    )
    require(
        graph.get("schema") == aggregate.GRAPH_SCHEMA
        and graph.get("status") == "PASS"
        and graph.get("failures") == []
        and graph.get("role") == role
        and graph.get("profile") == config["profile"]
        and graph.get("partition") == partition,
        f"generated graph {role}/{partition} identity is invalid",
    )

    master = _validated_descriptor(
        graph.get("master"),
        f"generated graph {role}/{partition}.master",
        expected_path=config[f"{partition}_master"],
    )
    wrapper = _validated_descriptor(
        graph.get("wrapper"),
        f"generated graph {role}/{partition}.wrapper",
        expected_path=config[f"{partition}_wrapper"],
    )
    reconciliation = _validated_descriptor(
        graph.get("reconciliation"),
        f"generated graph {role}/{partition}.reconciliation",
        expected_path=RECONCILIATION,
    )
    presentation_value = graph.get("presentation_mapping")
    if config["presentation_required"]:
        presentation = _validated_descriptor(
            presentation_value,
            f"generated graph {role}/{partition}.presentation_mapping",
            expected_path=PRESENTATION,
        )
    else:
        require(
            presentation_value is None,
            f"generated graph {role}/{partition} has unexpected presentation lineage",
        )
        presentation = None

    rows = graph.get("units")
    require(
        isinstance(rows, list)
        and len(rows) == len(expected_ids)
        and all(isinstance(row, dict) for row in rows)
        and [row.get("id") for row in rows] == list(expected_ids),
        f"generated graph {role}/{partition} unit IDs are not exact",
    )
    unit_descriptors: list[dict[str, Any]] = []
    for identifier, row in zip(expected_ids, rows, strict=True):
        require(
            isinstance(row, dict)
            and set(row) == {"id", "source_path", "path", "bytes", "sha256"},
            f"generated graph {role}/{partition} {identifier} fields are not exact",
        )
        normalize_relative(
            row.get("source_path"),
            f"generated graph {role}/{partition} {identifier}.source_path",
        )
        compiled = _validated_descriptor(
            {key: row[key] for key in ("path", "bytes", "sha256")},
            f"generated graph {role}/{partition} {identifier}.compiled",
        )
        require(
            compiled["path"].startswith(config["compiled_prefix"]),
            f"generated graph {role}/{partition} {identifier} is outside its compiled root",
        )
        unit_descriptors.append(compiled)

    raw_dependencies = graph.get("dependencies")
    require(
        isinstance(raw_dependencies, list) and raw_dependencies,
        f"generated graph {role}/{partition} lacks dependencies",
    )
    dependencies = [
        _validated_descriptor(
            item, f"generated graph {role}/{partition} dependency {index}"
        )
        for index, item in enumerate(raw_dependencies)
    ]
    expected_dependency_paths = unique(
        [
            master["path"],
            wrapper["path"],
            *[item["path"] for item in unit_descriptors],
            *_role_graph_support(role),
        ]
    )
    require(
        [item["path"] for item in dependencies] == expected_dependency_paths,
        f"generated graph {role}/{partition} dependency paths are not exact",
    )
    dependency_map = {item["path"]: item for item in dependencies}
    require(
        len(dependency_map) == len(dependencies),
        f"generated graph {role}/{partition} dependencies contain duplicates",
    )
    for required in [master, wrapper, *unit_descriptors]:
        require(
            required["path"] in dependency_map
            and descriptor_equal(required, dependency_map[required["path"]]),
            f"generated graph {role}/{partition} dependency binding differs",
        )

    if snapshot is not None:
        snapshot.recorded(master, f"generated graph {role}/{partition}.master")
        snapshot.recorded(wrapper, f"generated graph {role}/{partition}.wrapper")
        snapshot.recorded(
            reconciliation, f"generated graph {role}/{partition}.reconciliation"
        )
        if presentation is not None:
            snapshot.recorded(
                presentation,
                f"generated graph {role}/{partition}.presentation_mapping",
            )
        for identifier, compiled in zip(expected_ids, unit_descriptors, strict=True):
            snapshot.recorded(
                compiled, f"generated graph {role}/{partition} {identifier}.compiled"
            )
        for index, dependency in enumerate(dependencies):
            snapshot.recorded(
                dependency, f"generated graph {role}/{partition} dependency {index}"
            )


def _require_exact_readback(path: Path, data: bytes, label: str) -> None:
    observed, _, _ = _read_stable_regular(path, label)
    require(observed == data, f"{label} readback differs")


def _generated_graph_spec(relative: str) -> tuple[str, str]:
    relative = normalize_relative(relative, "generated graph path")
    specs = {
        path: (role, partition)
        for role in ROLE_ORDER
        for partition, path in zip(("reader", "closure"), _graph_paths(role), strict=True)
    }
    require(relative in specs, f"generated graph path is outside the six-file boundary: {relative}")
    return specs[relative]


def _expected_graph_paths() -> tuple[str, ...]:
    return tuple(path for role in ROLE_ORDER for path in _graph_paths(role))


def _commit_generated_graph_namespace(
    snapshot: Snapshot, payloads: Mapping[str, bytes]
) -> str:
    """Create the fresh six-file namespace once, or verify it without writes."""
    expected = _expected_graph_paths()
    require(
        tuple(payloads) == expected,
        "generated graph payload inventory or order is not the exact six-file boundary",
    )
    root_relative = normalize_relative(GRAPH_ROOT, "generated graph namespace")
    root = snapshot.repo / Path(*PurePosixPath(root_relative).parts)
    parent = root.parent
    require(parent.exists() and parent.is_dir(), "generated graph parent is absent")
    require(
        parent.resolve(strict=True) == Path(os.path.abspath(parent)),
        "generated graph parent crosses a symbolic path",
    )
    require(not root.is_symlink(), "generated graph namespace is symbolic")

    expected_names = {PurePosixPath(relative).name for relative in expected}
    if root.exists():
        require(root.is_dir(), "generated graph namespace is not a directory")
        require(
            root.resolve(strict=True) == Path(os.path.abspath(root)),
            "generated graph namespace crosses a symbolic path",
        )
        observed_names = {entry.name for entry in root.iterdir()}
        require(
            observed_names == expected_names,
            "existing generated graph namespace is not the exact six-file inventory",
        )
        for relative in expected:
            require(
                snapshot.capture(relative) == payloads[relative],
                f"immutable generated graph differs: {relative}",
            )
        return "verified-existing"

    staging = Path(
        tempfile.mkdtemp(prefix=f".{root.name}.staging-", dir=parent)
    )
    try:
        for relative in expected:
            target = staging / PurePosixPath(relative).name
            with target.open("xb") as stream:
                stream.write(payloads[relative])
                stream.flush()
                os.fsync(stream.fileno())
            _require_exact_readback(
                target, payloads[relative], f"staged generated graph {relative}"
            )
        require(
            {entry.name for entry in staging.iterdir()} == expected_names,
            "staged generated graph namespace is not the exact six-file inventory",
        )
        require(not root.exists(), "generated graph namespace appeared during creation")
        os.rename(staging, root)
        for relative in expected:
            require(
                snapshot.capture(relative) == payloads[relative],
                f"created generated graph differs: {relative}",
            )
        return "created"
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def prepare_graphs(
    snapshot: Snapshot,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any], dict[str, Any]]:
    if CURRENT_MSA_MODE:
        return _materialize_graphs(snapshot, _current_msa_manifest(snapshot), {})
    reconciliation = snapshot.json(RECONCILIATION, "source reconciliation")
    require(
        reconciliation.get("schema") == aggregate.RECONCILIATION_SCHEMA
        and reconciliation.get("status") == "PASS"
        and reconciliation.get("total_units") == 722,
        "source reconciliation is not a passing 722-unit closure",
    )
    rows = reconciliation.get("units")
    require(
        isinstance(rows, list)
        and [row.get("id") for row in rows if isinstance(row, dict)]
        == list(aggregate.EXPECTED_IDS),
        "source reconciliation IDs are not exact",
    )
    reconciliation_descriptor = snapshot.describe(RECONCILIATION)
    require(
        reconciliation_descriptor["sha256"] == EXPECTED_RECONCILIATION_SHA256,
        "source reconciliation is not the authority bound to this graph namespace",
    )

    acceptance = snapshot.json(ACCEPTANCE, "translation acceptance audit")
    require(
        acceptance.get("schema") == "openlogic-full-translation-acceptance-audit-v2"
        and acceptance.get("overall_status") == "PASS"
        and acceptance.get("summary", {}).get("unit_count") == 722
        and acceptance.get("summary", {}).get("live_source_bindings") == 2166
        and acceptance.get("summary", {}).get("blocking_finding_count") == 0,
        "translation acceptance audit is not a zero-blocker PASS",
    )
    _verify_acceptance_source_snapshot(
        snapshot,
        acceptance,
        rows,
        expected_ids=aggregate.EXPECTED_IDS,
    )

    presentation = snapshot.json(PRESENTATION, "Classical presentation mapping")
    require(
        presentation.get("schema") == aggregate.PRESENTATION_SCHEMA
        and presentation.get("status") == "PASS"
        and presentation.get("release_eligible") is True
        and presentation.get("presentation_locale") == "ar-classical-presentation",
        "Classical materialization is not a final release-eligible mapping",
    )
    presentation_rows = presentation.get("units")
    require(
        isinstance(presentation_rows, list)
        and [row.get("id") for row in presentation_rows if isinstance(row, dict)]
        == list(aggregate.EXPECTED_IDS),
        "Classical presentation IDs are not exact",
    )
    presentation_descriptor = snapshot.describe(PRESENTATION)
    require(
        presentation_descriptor["sha256"] == EXPECTED_PRESENTATION_SHA256,
        "Classical materialization receipt is not the authority bound to this graph namespace",
    )
    require(
        presentation.get("source_tree_sha256")
        == EXPECTED_CLASSICAL_SOURCE_TREE_SHA256,
        "Classical materialization source tree is not bound to this graph namespace",
    )
    require(
        presentation.get("presentation_tree_sha256")
        == EXPECTED_CLASSICAL_PRESENTATION_TREE_SHA256,
        "Classical materialization presentation tree is not bound to this graph namespace",
    )

    return _materialize_graphs(snapshot, reconciliation, presentation)


def _materialize_graphs(snapshot: Snapshot, reconciliation: dict, presentation: dict):
    rows = reconciliation["units"]
    reconciliation_descriptor = snapshot.describe(RECONCILIATION)
    presentation_rows = presentation.get("units", [])
    presentation_descriptor = snapshot.describe(PRESENTATION) if presentation else None
    graph_payloads: dict[str, bytes] = {}
    for role in ROLE_ORDER:
        config = aggregate.ROLE_CONFIG[role]
        if config["presentation_required"]:
            compiled = {
                row["id"]: snapshot.recorded(
                    row["presentation"], f"Classical presentation {row['id']}"
                )
                for row in presentation_rows
            }
        else:
            compiled = {
                row["id"]: snapshot.recorded(row["msa"], f"MSA source {row['id']}")
                for row in rows
            }
        by_id = {row["id"]: row for row in rows}
        support = [snapshot.describe(path) for path in _role_graph_support(role)]
        graph_paths = _graph_paths(role)
        for partition, ids, graph_relative in (
            ("reader", aggregate.READER_IDS, graph_paths[0]),
            ("closure", aggregate.CLOSURE_IDS, graph_paths[1]),
        ):
            master = snapshot.describe(config[f"{partition}_master"])
            wrapper = snapshot.describe(config[f"{partition}_wrapper"])
            units = [
                {
                    "id": identifier,
                    "source_path": by_id[identifier]["source_path"],
                    **compiled[identifier],
                }
                for identifier in ids
            ]
            dependencies: list[dict[str, Any]] = []
            dependency_paths: set[str] = set()
            for item in [master, wrapper, *[compiled[item] for item in ids], *support]:
                if item["path"] not in dependency_paths:
                    dependencies.append(item)
                    dependency_paths.add(item["path"])
            graph = {
                "schema": aggregate.GRAPH_SCHEMA,
                "status": "PASS",
                "failures": [],
                "role": role,
                "profile": config["profile"],
                "partition": partition,
                "master": master,
                "wrapper": wrapper,
                "reconciliation": reconciliation_descriptor,
                "presentation_mapping": (
                    presentation_descriptor if config["presentation_required"] else None
                ),
                "units": units,
                "dependencies": dependencies,
            }
            require(
                _generated_graph_spec(graph_relative) == (role, partition),
                f"generated graph path/role/partition mismatch: {graph_relative}",
            )
            _validate_generated_graph(
                graph, role=role, partition=partition, snapshot=snapshot
            )
            graph_payloads[graph_relative] = canonical_json_bytes(graph)

    # Validate all six graphs before the first write.  The namespace is then
    # created as one directory rename, or an existing immutable namespace is
    # accepted only after exact current-byte comparison.
    _commit_generated_graph_namespace(snapshot, graph_payloads)
    graph_descriptors = {
        relative: snapshot.describe(relative) for relative in graph_payloads
    }

    return graph_descriptors, reconciliation, presentation


def _authority_summary(snapshot: Snapshot, presentation: Mapping[str, Any]) -> dict[str, Any]:
    if CURRENT_MSA_MODE:
        return {
            "effective_current_msa_build_manifest": snapshot.describe(RECONCILIATION),
            "historical_source_reconciliation": snapshot.describe("evidence/classical/SOURCE_RECONCILIATION_CLOSURE_MANIFEST_20260905.json"),
            "msa_closure_rebind": snapshot.describe(MSA_REBIND),
            "source_correction_ledger": snapshot.describe("evidence/classical/terminology/SOL6_PROOF_QUANTIFICATION_RECHECK_20260930.json"),
            "reference_localization_ledger": snapshot.describe(CURRENT_REFERENCE_LEDGER),
            "scope_ar": "هوية مصادر البناء الحالي للقارئين المعياريين، مع تصحيح OLP-0087 المثبت وفواصل الإحالة العربية. لا يعاد تأريخ إقرار الترجمة السابق ولا تمنح شهادة مراجعة دلالية للكتاب كله؛ لم تعد الطبعة التراثية إلى البناء في هذه الدفعة."
        }
    reconciliation = snapshot.json(RECONCILIATION, "source reconciliation")
    return {
        "source_reconciliation": snapshot.describe(RECONCILIATION),
        "source_snapshot_sha256": reconciliation.get("source_snapshot_sha256"),
        "translation_acceptance": snapshot.describe(ACCEPTANCE),
        "classical_materialization": snapshot.describe(PRESENTATION),
        "classical_source_tree_sha256": presentation.get("source_tree_sha256"),
        "classical_presentation_tree_sha256": presentation.get(
            "presentation_tree_sha256"
        ),
        "classical_decision_ledger": snapshot.describe(DECISIONS),
        "msa_closure_rebind": snapshot.describe(MSA_REBIND),
    }


def _build_instructions(role: str, direct_tex_name: str) -> bytes:
    config = aggregate.ROLE_CONFIG[role]
    title = config["arabic_label"]
    if role in {"msa-international", "msa-machrek"}:
        build_block = """\
## البناء المحروس

يشغّل المدخل الآتي طبقتي العربية المعيارية ويُنتج مكوّن القارئ ذي ٦٤٢
وحدة وملحق الإغلاق ذي ٨٠ وحدة، ثم يصلح مستطيلات الروابط ويجمع المكوّنين:

```powershell
powershell -NoProfile -File build/BUILD_DUAL_NOTATION.ps1 `
  -FinalOutputDirectory C:\\build\\openlogic-final `
  -WorkDirectory C:\\build\\openlogic-work
```

يحصل هذا المدخل بنفسه على القفل المسمّى
`Global\\InterlanguageTeXSlotV1`. لا تُشغَّل أوامر TeX خارج هذا الحارس.
اختر من مجلد الناتج ملف الطبقة المسمّاة في رأس هذا الدليل.
"""
    else:
        build_block = """\
## البناء المحروس

تُبنى طبقة البيان التراثي بالمدخل الآتي، وهو يتحقق أولًا من إغلاق المصدر
ومن مادة العرض النهائية ثم يبني القارئ والملحق ويصلح الروابط ويجمعهما:

```powershell
powershell -NoProfile -File build/BUILD_CLASSICAL_ARABIC_EASTERN_RTL.ps1 `
  -BuildRole primary `
  -BuildRunId source-bundle-primary-0001 `
  -SourceClosureReceipt evidence/classical/SOURCE_RECONCILIATION_CLOSURE_MANIFEST_20260905.json `
  -RTLClosureReceipt evidence/classical/RTL_RUNTIME_CLOSURE_20260905.json `
  -MaterializationReceipt evidence/classical/NOTATION_MATERIALIZATION_RECEIPT.json `
  -FinalOutputDirectory C:\\build\\openlogic-classical-final `
  -WorkDirectory C:\\build\\openlogic-classical-work
```

يحصل هذا المدخل بنفسه على القفل المسمّى
`Global\\InterlanguageTeXSlotV1`. لا تُشغَّل أوامر TeX خارج هذا الحارس.
"""
    text = f"""\
# بناء مصدر نص المنطق المفتوح

الطبعة: **{title}**  
معرّف الطبقة التقني: `{role}`  
ملف لاتخ التجميعي المباشر: `{direct_tex_name}`  
عدد الوحدات: **٧٢٢ = ٦٤٢ + ٨٠**.

هذه الحزمة هي شجرة المصدر القابلة للتحرير الخاصة بالطبعة المذكورة. يحفظ
ملف لاتخ المباشر القائدين والمدخلين وأجسام الوحدات كلها بترتيبها وبايتاتها
المثبتة، لكنه ملف تجميعي أرشيفي وليس قائد بناء أحادي المرور. يعيد البناء
الصحيح مهمتي LuaLaTeX مستقلتين، ثم إصلاح روابط كل مكوّن، ثم تجميع ملفي PDF.

{build_block}

## المتطلبات

- Windows PowerShell، وLuaLaTeX، وBibTeX من TeX Live أو MiKTeX.
- أصناف وحزم لاتخ المستعملة في المصدر، ومنها `memoir` و`fontspec` و`babel`
  و`subfiles` و`hyperref` و`cleveref` وحزم الرياضيات والرسوم المبيّنة في السجل.
- Python 3 مع `pypdf`؛ ويتطلب مسار العربية المعيارية أيضًا `pdfplumber`
  و`fonttools` لفحوصه وبناء خط أرقام المشرق.
- الخطوط المضمّنة في `00_control/fonts` و`source/locale/ar/fonts` محفوظة
  مع نصوص رخصها. وتبقى خطوط TeX Gyre وLatin Modern وDejaVu من تثبيت النظام.

## التحقق من المصدر

يسرد `SOURCE_BUNDLE_MANIFEST.json` حجم كل عضو وSHA-256 له، ويثبت إغلاق
الوحدات وترتيبها وهويات مادة العرض. ينبغي التحقق من هذه القيم قبل البناء.
يحفظ `{GRAPH_ROOT}/` سجلي الرسم التجميعي
وإيصال ملف لاتخ لهذه الطبعة وحدها، ولا تضم الحزمة مخابئ TeX أو ملفات عمل.

## بيان المنشأ الآلي

الترجمة والتصحيحات السابقة الموثقة في المصدر الموروث: {AI_INHERITED_DISCLOSURE}.
{"تصحيحا تنسيق OLP-0310 وOLP-0658 في الطبعة التراثية: " + AI_PREVIOUS_LAYOUT_DISCLOSURE + ". تصحيح اتجاه أسماء الدوال اللاتينية وخرائط Unicode: " + AI_REPAIR_DISCLOSURE + ". تصحيح اتجاه أسماء النظريات والأنساق وقاعدة القطع ورمز القيمة: " + AI_PREVIOUS_NAMED_DISCLOSURE + "." if role == "classical-eastern-rtl" else ""}
{"تصحيح عبارتي شروط التكميم في OLP-0087، وفواصل الإحالات العربية المشتركة: " + AI_DISCLOSURE + ". الإقرار السابق محفوظ بوصفه سجلاً تاريخياً، وهذه الحزمة تثبت مصادر البناء الحالي لا مراجعة دلالية شاملة جديدة." if CURRENT_MSA_MODE else ""}
تجميع هذه المصادر والتحقق الحتمي منها: {AI_DISCLOSURE}. لا يدل ذلك على
مراجعة بشرية عربية غير موثقة.
"""
    return text.replace("\r\n", "\n").encode("utf-8")


def _source_body_paths(
    role: str, reconciliation: Mapping[str, Any], presentation: Mapping[str, Any]
) -> tuple[list[str], list[str]]:
    rows = reconciliation["units"]
    if role == "classical-eastern-rtl":
        presented = [row["presentation"]["path"] for row in presentation["units"]]
        authority = [row["classical"]["path"] for row in rows]
        return presented, authority
    return [row["msa"]["path"] for row in rows], []


def _role_repository_files(
    role: str,
    reconciliation: Mapping[str, Any],
    presentation: Mapping[str, Any],
    graph_paths: Sequence[str],
) -> list[str]:
    compiled, authority = _source_body_paths(role, reconciliation, presentation)
    common = [
        "LICENSE.md",
        *COMMON_SOURCE_FILES,
        *SCHEHERAZADE_RUNTIME,
        *SCHEHERAZADE_AUXILIARY,
        *graph_paths,
    ]
    if role in {"msa-international", "msa-machrek"}:
        return unique(
            [
                *common,
                *MSA_SOURCE_SUPPORT,
                *compiled,
                *MSA_BUILD_FILES,
                *MSA_EVIDENCE_FILES,
            ]
        )
    return unique(
        [
            *common,
            *CLASSICAL_SOURCE_SUPPORT,
            *compiled,
            *authority,
            *CLASSICAL_BUILD_FILES,
            *CLASSICAL_EVIDENCE_FILES,
        ]
    )


def _tree_hash(members: Mapping[str, bytes]) -> str:
    digest = hashlib.sha256()
    for name in sorted(members, key=lambda item: item.encode("utf-8")):
        name_bytes = name.encode("utf-8")
        data = members[name]
        digest.update(len(name_bytes).to_bytes(8, "big"))
        digest.update(name_bytes)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def _zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
    info.create_system = 3
    info.external_attr = ZIP_MODE << 16
    info.compress_type = zipfile.ZIP_STORED
    return info


def _write_new(path: Path, data: bytes, label: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    require(path.read_bytes() == data, f"{label} readback differs")


def _write_source_tree(root: Path, members: Mapping[str, bytes]) -> None:
    require(not root.exists(), f"source-tree destination already exists: {root}")
    root.mkdir(parents=True)
    for name in sorted(members, key=lambda item: item.encode("utf-8")):
        path = root / Path(*PurePosixPath(name).parts)
        _write_new(path, members[name], f"source-tree member {name}")


def _write_zip(path: Path, archive_root: str, members: Mapping[str, bytes]) -> None:
    ordered = sorted(members, key=lambda item: item.encode("utf-8"))
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "x", compression=zipfile.ZIP_STORED, allowZip64=True) as archive:
        for name in ordered:
            archive.writestr(_zip_info(f"{archive_root}/{name}"), members[name])
    with zipfile.ZipFile(path, "r") as archive:
        infos = archive.infolist()
        expected = [f"{archive_root}/{name}" for name in ordered]
        require([item.filename for item in infos] == expected, "ZIP order differs")
        require(archive.testzip() is None, "ZIP CRC verification failed")
        for info, name in zip(infos, ordered, strict=True):
            require(info.date_time == FIXED_ZIP_TIME, f"ZIP timestamp differs: {name}")
            require(info.compress_type == zipfile.ZIP_STORED, f"ZIP compression differs: {name}")
            require((info.external_attr >> 16) == ZIP_MODE, f"ZIP mode differs: {name}")
            require(archive.read(info) == members[name], f"ZIP bytes differ: {name}")


def _path_descriptor(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {"file": path.name, "bytes": len(data), "sha256": sha256_bytes(data)}


def _aggregate_kwargs(
    repo: Path,
    role: str,
    graph_paths: Sequence[str],
    output: Path,
    receipt: Path,
) -> dict[str, Any]:
    config = aggregate.ROLE_CONFIG[role]
    kwargs: dict[str, Any] = {
        "repo": repo,
        "role": role,
        "reader_master": repo / config["reader_master"],
        "closure_master": repo / config["closure_master"],
        "reader_wrapper": repo / config["reader_wrapper"],
        "closure_wrapper": repo / config["closure_wrapper"],
        "reader_graph": repo / graph_paths[0],
        "closure_graph": repo / graph_paths[1],
        "reconciliation": repo / RECONCILIATION,
        "assembler": repo / config["assembler"],
        "output": output,
        "receipt": receipt,
    }
    if config["presentation_required"]:
        kwargs["presentation_mapping"] = repo / PRESENTATION
        kwargs["classical_decision_ledger"] = repo / DECISIONS
    return kwargs


def build_stage(
    snapshot: Snapshot,
    stage: Path,
    graph_descriptors: Mapping[str, Mapping[str, Any]],
    reconciliation: Mapping[str, Any],
    presentation: Mapping[str, Any],
    authorities: Mapping[str, Any],
) -> dict[str, Any]:
    require(not stage.exists(), f"stage already exists: {stage}")
    files_dir = stage / "files"
    control_dir = stage / "control"
    trees_dir = stage / "source-trees"
    files_dir.mkdir(parents=True)
    control_dir.mkdir()
    trees_dir.mkdir()

    roles: list[dict[str, Any]] = []
    release_files: list[dict[str, Any]] = []
    for role in ROLE_ORDER:
        stem = ROLE_STEMS[role]
        direct_name = f"{stem}.tex"
        zip_name = f"{stem}_SOURCES.zip"
        direct_path = files_dir / direct_name
        aggregate_receipt = control_dir / f"{role}-aggregate-receipt.json"
        graph_paths = _graph_paths(role)
        result = aggregate.assemble(
            **_aggregate_kwargs(
                snapshot.repo, role, graph_paths, direct_path, aggregate_receipt
            )
        )
        require(
            result.get("status") == "PASS"
            and result.get("coverage", {}).get("total_units") == 722,
            f"aggregate did not pass: {role}",
        )
        direct_data = direct_path.read_bytes()
        receipt_data = aggregate_receipt.read_bytes()

        members: dict[str, bytes] = {
            direct_name: direct_data,
            "README_BUILD_AR.md": _build_instructions(role, direct_name),
        }
        for relative in _role_repository_files(
            role, reconciliation, presentation, graph_paths
        ):
            members[relative] = snapshot.capture(relative)
        receipt_member = f"{GRAPH_ROOT}/{role}-aggregate-receipt.json"
        members[receipt_member] = receipt_data

        listed = [
            descriptor(name, members[name])
            for name in sorted(members, key=lambda item: item.encode("utf-8"))
        ]
        compiled_paths, authority_paths = _source_body_paths(
            role, reconciliation, presentation
        )
        bundle_manifest = {
            "schema": BUNDLE_SCHEMA,
            "status": "PASS",
            "reader_id": role,
            "profile": aggregate.ROLE_CONFIG[role]["profile"],
            "arabic_label": aggregate.ROLE_CONFIG[role]["arabic_label"],
            "ai_provenance": {
                "disclosure": AI_DISCLOSURE,
                "inherited_translation_disclosure": AI_INHERITED_DISCLOSURE,
                "disclosure_ar": (
                    f"الترجمة والتصحيحات السابقة الموثقة في المصدر الموروث: "
                    f"{AI_INHERITED_DISCLOSURE}. "
                    + (
                        f"تصحيحا تنسيق OLP-0310 وOLP-0658 في الطبعة التراثية: "
                        f"{AI_PREVIOUS_LAYOUT_DISCLOSURE}. "
                        f"تصحيح اتجاه أسماء الدوال اللاتينية وخرائط Unicode: "
                        f"{AI_REPAIR_DISCLOSURE}. "
                        f"تصحيح اتجاه أسماء النظريات والأنساق وقاعدة القطع ورمز القيمة: {AI_PREVIOUS_NAMED_DISCLOSURE}. "
                        if role == "classical-eastern-rtl" else ""
                    )
                    + f"أُنجز تجميع المصدر والتحقق الحتمي بواسطة {AI_DISCLOSURE}؛ "
                    "ولا تُدَّعى مراجعة بشرية غير موثقة."
                ),
            },
            "coverage": {
                "first_id": "OLP-0001",
                "last_id": "OLP-0722",
                "reader_units": 642,
                "closure_units": 80,
                "total_units": 722,
                "compiled_body_files": len(compiled_paths),
                "separate_authoritative_body_files": len(authority_paths),
            },
            "direct_tex_member": descriptor(direct_name, direct_data),
            "aggregate_receipt_member": descriptor(receipt_member, receipt_data),
            "graph_inventories": [graph_descriptors[path] for path in graph_paths],
            "authorities": authorities,
            "build_instructions": "README_BUILD_AR.md",
            "member_manifest_excludes_only_itself": True,
            "members": listed,
            "members_without_manifest": len(listed),
            "tree_without_manifest_sha256": _tree_hash(members),
            "cache_members": 0,
            "evidence_policy": "only exact closure/build authorities; no evidence catch-all",
        }
        manifest_data = canonical_json_bytes(bundle_manifest)
        members["SOURCE_BUNDLE_MANIFEST.json"] = manifest_data

        source_tree = trees_dir / stem
        _write_source_tree(source_tree, members)
        archive_root = f"{stem}_SOURCE"
        zip_path = files_dir / zip_name
        _write_zip(zip_path, archive_root, members)
        with zipfile.ZipFile(zip_path, "r") as archive:
            archived_direct = archive.read(f"{archive_root}/{direct_name}")
        require(archived_direct == direct_data, f"ZIP/direct TeX mismatch: {role}")

        direct_descriptor = _path_descriptor(direct_path)
        zip_descriptor = _path_descriptor(zip_path)
        release_files.extend([direct_descriptor, zip_descriptor])
        roles.append(
            {
                "reader_id": role,
                "direct_tex": direct_descriptor,
                "source_zip": zip_descriptor,
                "source_tree_root": f"source-trees/{stem}",
                "source_bundle_manifest": descriptor(
                    "SOURCE_BUNDLE_MANIFEST.json", manifest_data
                ),
                "aggregate_receipt": descriptor(
                    f"control/{aggregate_receipt.name}", receipt_data
                ),
                "graph_inventories": [graph_descriptors[path] for path in graph_paths],
                "coverage": result["coverage"],
                "classical_inverse_replay": result["authorities"].get(
                    "classical_inverse_replay"
                ),
            }
        )

    require(len(release_files) == NEW_RELEASE_FILES, "release file count is not six")
    require(NEW_RELEASE_FILES <= MAX_NEW_FILES, "Zenodo new-file allowance exceeded")
    stage_manifest = {
        "schema": SCHEMA,
        "status": "PASS",
        "ai_disclosure": AI_DISCLOSURE,
        "authorities": authorities,
        "roles": roles,
        "release_files": release_files,
        "release_file_count": len(release_files),
        "zenodo_capacity": {
            "inherited_files": INHERITED_ZENODO_FILES,
            "new_files_in_this_deliverable": len(release_files),
            "maximum_new_files": MAX_NEW_FILES,
            "projected_files_for_these_additions_only": (
                INHERITED_ZENODO_FILES + len(release_files)
            ),
            "within_limit": (
                INHERITED_ZENODO_FILES + len(release_files) <= ZENODO_FILE_CAP
            ),
        },
        "determinism": {
            "timestamps_recorded": False,
            "zip_timestamp": "1980-01-01T00:00:00",
            "zip_compression": "stored",
            "zip_member_mode": "0100644",
            "zip_member_order": "UTF-8 byte order",
        },
        "tex_invoked": False,
        "network_invoked": False,
        "published": False,
    }
    manifest_data = canonical_json_bytes(stage_manifest)
    if CURRENT_MSA_MODE:
        stage_manifest["zenodo_capacity"] = {
            "local_new_files": len(release_files), "maximum_public_files": ZENODO_FILE_CAP,
            "public_inventory_not_evaluated": True,
            "scope_ar": "يُفحص العدد الفعلي للملفات المنشورة في معاملة النشر؛ هذا الإعداد المحلي لا يفترض أن السجل العام فارغ."
        }
        manifest_data = canonical_json_bytes(stage_manifest)
    _write_new(stage / "STAGE_MANIFEST.json", manifest_data, "stage manifest")
    return stage_manifest


def _compare_stage_files(primary: Path, replay: Path) -> list[dict[str, Any]]:
    primary_files = sorted(
        (path.name for path in (primary / "files").iterdir() if path.is_file()),
        key=lambda item: item.encode("utf-8"),
    )
    replay_files = sorted(
        (path.name for path in (replay / "files").iterdir() if path.is_file()),
        key=lambda item: item.encode("utf-8"),
    )
    require(primary_files == replay_files, "cold replay filename inventory differs")
    require(len(primary_files) == NEW_RELEASE_FILES, "cold replay inventory is not six")
    comparison: list[dict[str, Any]] = []
    for name in primary_files:
        left = (primary / "files" / name).read_bytes()
        right = (replay / "files" / name).read_bytes()
        require(left == right, f"cold replay byte mismatch: {name}")
        comparison.append({"file": name, "bytes": len(left), "sha256": sha256_bytes(left)})
    require(
        (primary / "STAGE_MANIFEST.json").read_bytes()
        == (replay / "STAGE_MANIFEST.json").read_bytes(),
        "cold replay stage manifests differ",
    )
    return comparison


def _current_msa_manifest(snapshot: Snapshot) -> dict:
    import rebind_msa_closure_manifest as rebind
    historical = rebind.DEFAULT_AUTHORITY
    require(snapshot.describe(historical)["sha256"] ==
            "7efe0a46648cff60f0f179c98ab01d948630bfe4b7dd944f0f8061b728c18ef1",
            "historical MSA authority changed")
    repo = snapshot.repo
    rebind.verify_receipt(repo, repo / rebind.DEFAULT_MANIFEST, repo / historical,
                          repo / CURRENT_MSA_REBIND, repo / rebind.PROOF_LEDGER)
    _, units, successor = rebind.authority_units(repo, repo / historical, repo / rebind.PROOF_LEDGER)
    require(successor is not None, "exact MSA successor absent")
    reference = snapshot.json(CURRENT_REFERENCE_LEDGER, "reference localization choices")
    transition = reference.get("source_transition", {})
    require(transition.get("path") == "source/locale/ar/open-logic-locale.sty"
            and transition.get("before_sha256") == "e635bdac43c8e682f64df8a94c94d360abed755917eb06ccd16e446f7e674b16"
            and transition.get("after_sha256") == "21b6507c077673d282fcb21483af8c9eac76c5da792843cf1ec057b43c45b816"
            and snapshot.describe(transition["path"])["sha256"] == transition["after_sha256"],
            "reference-localization endpoint changed")
    payload = {"schema": aggregate.RECONCILIATION_SCHEMA, "status": "PASS",
               "release_id": "openlogic-current-msa-build-20260930", "total_units": 722,
               "source_snapshot_sha256": canonical_value_sha256(units), "units": units,
               "historical_authority": snapshot.describe(historical),
               "msa_source_successor": successor,
               "scope_ar": "هوية بناء حالي للمعيارية فقط؛ جميع الوحدات السابقة محفوظة ما عدا تصحيح OLP-0087 المثبت بعكس تعديلين. ليس إقرار مراجعة دلالية جديدة ولا تغييراً في الإقرار التاريخي أو في التراثية."}
    data = canonical_json_bytes(payload)
    destination = repo / CURRENT_MSA_MANIFEST
    if destination.exists():
        require(snapshot.capture(CURRENT_MSA_MANIFEST) == data, "immutable current MSA manifest differs")
    else:
        _write_new(destination, data, "effective current MSA manifest")
        snapshot.capture(CURRENT_MSA_MANIFEST)
    return payload


@contextmanager
def current_msa_scope():
    """Explicit CLI scope; restore historical three-edition defaults on exit."""
    names = ("CURRENT_MSA_MODE", "ROLE_ORDER", "ROLE_STEMS", "GRAPH_ROOT", "RECONCILIATION",
             "MSA_REBIND", "MSA_BUILD_FILES", "MSA_EVIDENCE_FILES", "NEW_RELEASE_FILES",
             "INHERITED_ZENODO_FILES", "MAX_NEW_FILES")
    saved = {name: globals()[name] for name in names}
    try:
        globals().update(CURRENT_MSA_MODE=True, ROLE_ORDER=("msa-international", "msa-machrek"),
                         ROLE_STEMS={key: saved["ROLE_STEMS"][key] for key in ("msa-international", "msa-machrek")},
                         GRAPH_ROOT=CURRENT_MSA_GRAPH_ROOT, RECONCILIATION=CURRENT_MSA_MANIFEST,
                         MSA_REBIND=CURRENT_MSA_REBIND, NEW_RELEASE_FILES=4,
                         INHERITED_ZENODO_FILES=0, MAX_NEW_FILES=100)
        # Capacity is checked against the actual public inventory by the release
        # transaction, not this offline producer's obsolete 71-file assumption.
        globals()["MSA_BUILD_FILES"] = (*saved["MSA_BUILD_FILES"], "build/validate_classical_overlay.py")
        globals()["MSA_EVIDENCE_FILES"] = unique([
            saved["RECONCILIATION"], CURRENT_MSA_MANIFEST, CURRENT_MSA_REBIND,
            "evidence/classical/terminology/SOL6_PROOF_QUANTIFICATION_RECHECK_20260930.json",
            CURRENT_REFERENCE_LEDGER,
            "source/locale/ar-classical/content/first-order-logic/natural-deduction/quantifier-rules.tex",
            *[p for p in saved["MSA_EVIDENCE_FILES"] if p not in (saved["RECONCILIATION"], ACCEPTANCE, saved["MSA_REBIND"])],
        ])
        yield
    finally:
        globals().update(saved)


def prepare(
    repo: Path,
    output_root: Path,
) -> dict[str, Any]:
    repo = repo.resolve(strict=True)
    output_root = Path(os.path.abspath(output_root))
    require(output_root.is_relative_to(repo / "tmp"), "output root must be under repo/tmp")
    require(not output_root.exists(), f"output root already exists: {output_root}")
    require(NEW_RELEASE_FILES <= MAX_NEW_FILES, "new-file allowance is impossible")

    snapshot = Snapshot(repo)
    graph_descriptors, reconciliation, presentation = prepare_graphs(snapshot)
    authorities = _authority_summary(snapshot, presentation)
    output_root.mkdir(parents=True)
    try:
        primary_manifest = build_stage(
            snapshot,
            output_root / "primary",
            graph_descriptors,
            reconciliation,
            presentation,
            authorities,
        )
        replay_manifest = build_stage(
            snapshot,
            output_root / "cold-replay",
            graph_descriptors,
            reconciliation,
            presentation,
            authorities,
        )
        require(primary_manifest == replay_manifest, "stage manifest values differ")
        compared = _compare_stage_files(
            output_root / "primary", output_root / "cold-replay"
        )
        snapshot.recheck()
        receipt = {
            "schema": REPLAY_SCHEMA,
            "status": "PASS_BYTE_IDENTICAL_COLD_REPLAY",
            "files_compared": len(compared),
            "files": compared,
            "primary_stage_manifest": descriptor(
                "primary/STAGE_MANIFEST.json",
                (output_root / "primary" / "STAGE_MANIFEST.json").read_bytes(),
            ),
            "replay_stage_manifest": descriptor(
                "cold-replay/STAGE_MANIFEST.json",
                (output_root / "cold-replay" / "STAGE_MANIFEST.json").read_bytes(),
            ),
            "authorities": authorities,
            "checks": {
                "all_six_release_files_byte_identical": True,
                "stage_manifests_byte_identical": True,
                "source_inputs_rechecked_after_replay": True,
                "tex_invoked": False,
                "network_invoked": False,
                "publication_performed": False,
            },
        }
        data = canonical_json_bytes(receipt)
        if CURRENT_MSA_MODE:
            receipt["checks"]["all_release_files_byte_identical"] = receipt["checks"].pop("all_six_release_files_byte_identical")
            data = canonical_json_bytes(receipt)
        _write_new(
            output_root / "COLD_REPLAY_COMPARISON.json", data, "cold replay receipt"
        )
        return receipt
    except Exception:
        # Preserve a partially produced explicit staging root for diagnosis;
        # never silently replace or reuse it on a retry.
        raise


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare three direct 722-unit TeX aggregates and deterministic "
            "complete source ZIPs, then cold-replay them without invoking TeX."
        )
    )
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--current-msa-successor", action="store_true",
                        help="Package only the two current MSA editions using the one exact OLP-0087 successor; preserve historical Classical authorities.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.current_msa_successor:
            with current_msa_scope():
                result = prepare(args.repo, args.output_root)
        else:
            result = prepare(args.repo, args.output_root)
    except (OSError, PreparationError, aggregate.AggregateError, zipfile.BadZipFile) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
