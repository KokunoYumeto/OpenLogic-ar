#!/usr/bin/env python3
"""Create a truthful direct archival TeX aggregate for one 722-unit edition.

The complete readers are not produced by one TeX job. The canonical 642-unit
reader and the 80-unit closure supplement are compiled independently. Each PDF
then receives the hash-bound RTL link-rectangle repair before a hash-bound
Python/pypdf assembler joins the repaired PDFs. This module emits a direct
editable source aggregate, never a fictitious one-pass build master.

Membership and ordering come only from explicit passing graph inventories and
the ordered reconciliation authority. No directory enumeration or sort is
used to infer the 722 source bodies. All inputs are captured byte-for-byte,
then checked again immediately before an exclusive, no-replace pair commit.
"""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import sys
import tempfile
from typing import Any, Callable, Mapping, Sequence

if os.name == "nt":
    import ctypes
    import msvcrt
    from ctypes import wintypes


GRAPH_SCHEMA = "openlogic-complete-722-verified-graph-inventory-v1"
RECEIPT_SCHEMA = "openlogic-arabic-complete-722-tex-aggregate-v2"
RECONCILIATION_SCHEMA = "openlogic-classical-source-closure-manifest-v1"
PRESENTATION_SCHEMA = "openlogic-classical-notation-materialization-receipt-v1"
DECISION_SCHEMA = "openlogic-classical-notation-materialization-v2"
AGGREGATOR_RELATIVE = "build/assemble_complete_722_tex.py"
MARKER_TEXT = "%% OPENLOGIC-ARCHIVE-"
MARKER_TOKEN = MARKER_TEXT.encode("ascii")
BLOCK_MARKER = MARKER_TOKEN + b"BLOCK-"
SHA256_RE = re.compile(r"[0-9a-fA-F]{64}")
EXPECTED_IDS = tuple(f"OLP-{number:04d}" for number in range(1, 723))
READER_IDS = EXPECTED_IDS[:642]
CLOSURE_IDS = EXPECTED_IDS[642:]
TEX_OPTIONS = (
    "-interaction=nonstopmode",
    "-halt-on-error",
    "-file-line-error",
    "-recorder",
    "-synctex=1",
    "-output-directory=<isolated-work-directory>",
)
AI_AGENT = "OpenAI Codex"
AI_MODEL = "GPT-6.1 Sol"
AI_EFFORT = "Ultra"
AI_DISCLOSURE = "OpenAI Codex — GPT-6.1 Sol, Ultra effort"
AI_REPAIR_DISCLOSURE = "OpenAI Codex — GPT-6 Astra, Ultra effort"
AI_PREVIOUS_LAYOUT_DISCLOSURE = "OpenAI Codex — GPT-6 Sol, Ultra effort"
AI_PREVIOUS_NAMED_DISCLOSURE = "OpenAI Codex — GPT-6 Sol, Ultra effort"
AI_INHERITED_DISCLOSURE = "OpenAI Codex — GPT-5.6 Sol, Ultra effort"
RTL_LINK_REPAIR_RELATIVE = "build/repair_rtl_link_rects_letter_ar.py"
RTL_LINK_REPAIR_CORE_RELATIVE = "build/repair_rtl_link_rects_ar.py"
COMPLETE_ASSEMBLER_RELATIVE = "build/assemble_complete_722_reader.py"
RTL_LINK_REPAIR_BYTES = 42_964
RTL_LINK_REPAIR_SHA256 = (
    "d60f174cebc7479e486bfe76381220883bb21852fe314cb22b69ed3e62429a2f"
)
RTL_LINK_REPAIR_SUCCESSORS = frozenset({
    (49234, "21bd8385c0639c462287182d52a224d78e22158ad6d6fbfaaa467c2a8b97fd15"),
    (44601, "8eecc092e1109667c1b49bfa1543e4c130c8dfa15346787cc26e35357bebf86c"),
    (44900, "0da499b3f9d0c46138f4ed8f10bf2bd49683da84cf70f4f1652ad9c17dfc8609"),
})
FINAL_READBACK_HOOK_STAGES = (
    "before-open-output",
    "after-open-output",
    "after-open-receipt",
    "after-read-output",
    "after-read-receipt",
    "before-return",
)

# The Classical driver deliberately reuses only these three non-content
# Arabic-locale support files.  Its translated bodies must continue to come
# exclusively from ``ar-classical-presentation``; allowing the whole MSA tree
# here would make a stale or mixed-language graph inventory look valid.
CLASSICAL_SHARED_AR_SUPPORT = frozenset(
    {
        "source/locale/ar/open-logic-config.sty",
        "source/locale/ar/open-logic-locale.sty",
        "source/locale/ar/open-logic-readable-letter-r2-layout-ar.tex",
    }
)
CLASSICAL_SHARED_XITS_PREFIX = "source/locale/ar/fonts/vendor/xits-1.302/"
SCHEHERAZADE_FONT_PREFIX = "00_control/fonts/scheherazade-2.100/"


ROLE_CONFIG: dict[str, dict[str, Any]] = {
    "msa-international": {
        "profile": "international",
        "source_field": "msa",
        "compiled_prefix": "source/locale/ar/content/",
        "reader_master": "source/locale/ar/open-logic-complete-ar.tex",
        "closure_master": "source/locale/ar/open-logic-closure-supplement-ar.tex",
        "reader_wrapper": (
            "source/locale/ar/"
            "open-logic-complete-ar-readable-letter-international.tex"
        ),
        "closure_wrapper": (
            "source/locale/ar/"
            "open-logic-closure-supplement-ar-readable-letter-international.tex"
        ),
        "assembler": "build/assemble_complete_722_reader.py",
        "assembler_profile_argument": "international",
        "build_driver": "build/BUILD_DUAL_NOTATION.ps1",
        "build_inner": "build/BUILD_DUAL_NOTATION_INNER.ps1",
        "reader_passes": "initial LuaLaTeX, BibTeX, convergence passes 2..6",
        "closure_passes": "convergence passes 1..5",
        "arabic_label": "العربية المعيارية ذات الترميز الدولي",
        "presentation_required": False,
    },
    "msa-machrek": {
        "profile": "machrek",
        "source_field": "msa",
        "compiled_prefix": "source/locale/ar/content/",
        "reader_master": "source/locale/ar/open-logic-complete-ar.tex",
        "closure_master": "source/locale/ar/open-logic-closure-supplement-ar.tex",
        "reader_wrapper": (
            "source/locale/ar/"
            "open-logic-complete-ar-readable-letter-machrek.tex"
        ),
        "closure_wrapper": (
            "source/locale/ar/"
            "open-logic-closure-supplement-ar-readable-letter-machrek.tex"
        ),
        "assembler": "build/assemble_complete_722_reader.py",
        "assembler_profile_argument": "machrek",
        "build_driver": "build/BUILD_DUAL_NOTATION.ps1",
        "build_inner": "build/BUILD_DUAL_NOTATION_INNER.ps1",
        "reader_passes": "initial LuaLaTeX, BibTeX, convergence passes 2..6",
        "closure_passes": "convergence passes 1..5",
        "arabic_label": "العربية المعيارية ذات ترميز المشرق",
        "presentation_required": False,
    },
    "classical-eastern-rtl": {
        "profile": "classical",
        "source_field": "classical",
        "compiled_prefix": "source/locale/ar-classical-presentation/content/",
        "authoritative_prefix": "source/locale/ar-classical/content/",
        "reader_master": (
            "source/locale/ar-classical/"
            "open-logic-complete-ar-classical-eastern-rtl.tex"
        ),
        "reader_wrapper": (
            "source/locale/ar-classical/"
            "open-logic-complete-ar-classical-eastern-rtl.tex"
        ),
        "closure_master": (
            "source/locale/ar-classical/"
            "open-logic-closure-supplement-ar-classical-eastern-rtl.tex"
        ),
        "closure_wrapper": (
            "source/locale/ar-classical/"
            "open-logic-closure-supplement-ar-classical-eastern-rtl.tex"
        ),
        "assembler": "build/assemble_classical_722_reader.py",
        "assembler_profile_argument": None,
        "build_driver": "build/BUILD_CLASSICAL_ARABIC_EASTERN_RTL.ps1",
        "build_inner": "build/BUILD_CLASSICAL_ARABIC_EASTERN_RTL_INNER.ps1",
        "reader_passes": "initial LuaLaTeX, BibTeX, convergence passes 2..7",
        "closure_passes": "convergence passes 1..6",
        "arabic_label": "الصياغة العربية التراثية بالترميز الشرقي والعرض اليميني",
        "presentation_required": True,
    },
}


class AggregateError(ValueError):
    """A fail-closed validation or transactional-commit error."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def _object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AggregateError(f"JSON object contains duplicate key {key!r}")
        result[key] = value
    return result


def parse_json_bytes(data: bytes, label: str) -> dict[str, Any]:
    try:
        text = data.decode("utf-8")
        value = json.loads(text, object_pairs_hook=_object_without_duplicate_keys)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AggregateError(f"cannot parse {label}: {error}") from error
    if not isinstance(value, dict):
        raise AggregateError(f"{label} must be a JSON object")
    _reject_json_marker_strings(value, label)
    return value


def _reject_json_marker_strings(value: Any, label: str) -> None:
    """Keep the archive grammar out of every decoded JSON metadata string."""

    pending = [value]
    while pending:
        current = pending.pop()
        if isinstance(current, str):
            if MARKER_TEXT in current:
                raise AggregateError(f"{label} metadata contains an archive marker token")
        elif isinstance(current, dict):
            for key, child in current.items():
                if MARKER_TEXT in key:
                    raise AggregateError(
                        f"{label} metadata key contains an archive marker token"
                    )
                pending.append(child)
        elif isinstance(current, list):
            pending.extend(current)


def _reject_identity_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise AggregateError(f"{label} must be a nonempty string")
    if MARKER_TEXT in value:
        raise AggregateError(f"{label} contains an archive marker token")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise AggregateError(f"{label} contains a control character")
    return value


def normalize_relative(value: Any, label: str) -> str:
    value = _reject_identity_text(value, label)
    if "\\" in value or "\x00" in value:
        raise AggregateError(f"{label} is not a normalized POSIX path")
    posix = PurePosixPath(value)
    windows = PureWindowsPath(value)
    if (
        posix.is_absolute()
        or windows.is_absolute()
        or bool(windows.drive)
        or any(part in {"", ".", ".."} for part in posix.parts)
    ):
        raise AggregateError(f"{label} escapes or is not relative: {value!r}")
    if posix.as_posix() != value or any(":" in part for part in posix.parts):
        raise AggregateError(f"{label} is not canonical: {value!r}")
    return value


def _normalized_prefix(value: str, label: str) -> str:
    stripped = value[:-1] if value.endswith("/") else value
    return normalize_relative(stripped, label) + "/"


def _descriptor_equal(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    return (
        left.get("path") == right.get("path")
        and left.get("bytes") == right.get("bytes")
        and str(left.get("sha256", "")).lower()
        == str(right.get("sha256", "")).lower()
    )


def _byte_identity_equal(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    return (
        left.get("bytes") == right.get("bytes")
        and str(left.get("sha256", "")).lower()
        == str(right.get("sha256", "")).lower()
    )


def _dependency_scope(role: str, relative: str) -> str | None:
    """Return the exact profile/shared root class for one dependency path."""

    if relative.startswith(SCHEHERAZADE_FONT_PREFIX):
        return "shared-bundled-scheherazade-font"
    if role in {"msa-international", "msa-machrek"}:
        if relative.startswith("source/locale/ar/"):
            return "profile-msa"
    elif role == "classical-eastern-rtl":
        if relative.startswith("source/locale/ar-classical-presentation/"):
            return "profile-classical-presentation"
        if relative.startswith("source/locale/ar-classical/content/"):
            return None
        if relative.startswith("source/locale/ar-classical/"):
            return "profile-classical-entrypoint"
        if relative in CLASSICAL_SHARED_AR_SUPPORT:
            return "shared-ar-locale-support"
        if relative.startswith(CLASSICAL_SHARED_XITS_PREFIX):
            return "shared-classical-xits-font"
    if relative.startswith("source/") and not relative.startswith("source/locale/"):
        return "shared-source"
    return None


def _require_dependency_scope(
    role: str, lexical_relative: str, resolved_relative: str, label: str
) -> None:
    lexical_scope = _dependency_scope(role, lexical_relative)
    resolved_scope = _dependency_scope(role, resolved_relative)
    if lexical_scope is None:
        raise AggregateError(f"{label} is outside the role/shared dependency roots")
    if resolved_scope != lexical_scope:
        raise AggregateError(
            f"{label} crosses a role/shared real-path boundary: "
            f"{lexical_scope!r} -> {resolved_scope!r}"
        )


@dataclass(frozen=True)
class CapturedFile:
    relative: str
    resolved: Path
    native_identity: tuple[int, ...]
    link_count: int
    required_prefixes: tuple[str, ...]
    dependency_roles: tuple[str, ...]
    data: bytes
    descriptor: dict[str, Any]


@dataclass
class ExclusiveTemp:
    """An exclusively created temporary file kept open as an ownership anchor."""

    path: Path
    descriptor: int
    stat_identity: tuple[int, int]
    native_identity: tuple[int, ...]
    expected: bytes


class CaptureRegistry:
    """Capture each input once, then verify the same bytes before commit."""

    def __init__(self, repo: Path):
        self.repo = repo.resolve(strict=True)
        if not self.repo.is_dir():
            raise AggregateError(f"repository does not exist: {self.repo}")
        self._captured: dict[str, CapturedFile] = {}
        self._native_paths: dict[tuple[int, ...], str] = {}

    def _resolve_relative(
        self,
        relative: str,
        label: str,
        required_prefix: str | None,
        dependency_role: str | None,
    ) -> Path:
        relative = normalize_relative(relative, label)
        lexical = self.repo / Path(*PurePosixPath(relative).parts)
        try:
            resolved = lexical.resolve(strict=True)
        except (OSError, RuntimeError) as error:
            raise AggregateError(f"{label} does not resolve: {relative}") from error
        if not resolved.is_file():
            raise AggregateError(f"{label} is not a regular file: {relative}")
        try:
            resolved_relative = resolved.relative_to(self.repo).as_posix()
        except ValueError as error:
            raise AggregateError(f"{label} resolves outside the repository") from error
        if required_prefix is not None:
            prefix = _normalized_prefix(required_prefix, f"{label} role prefix")
            if not relative.startswith(prefix):
                raise AggregateError(
                    f"{label} is outside required role path {prefix!r}: {relative}"
                )
            prefix_relative = prefix[:-1]
            prefix_lexical = self.repo / Path(*PurePosixPath(prefix_relative).parts)
            try:
                prefix_resolved = prefix_lexical.resolve(strict=True)
            except (OSError, RuntimeError) as error:
                raise AggregateError(f"{label} role root does not resolve") from error
            if prefix_resolved != Path(os.path.abspath(prefix_lexical)):
                raise AggregateError(f"{label} role root is a symbolic-link alias")
            try:
                resolved.relative_to(prefix_resolved)
            except ValueError as error:
                raise AggregateError(
                    f"{label} resolves outside required real role tree {prefix!r}"
                ) from error
        if dependency_role is not None:
            _require_dependency_scope(
                dependency_role, relative, resolved_relative, label
            )
        return resolved

    def _capture_relative(
        self,
        relative: str,
        label: str,
        *,
        required_prefix: str | None = None,
        dependency_role: str | None = None,
        expected: Mapping[str, Any] | None = None,
    ) -> tuple[dict[str, Any], bytes]:
        relative = normalize_relative(relative, f"{label}.path")
        resolved = self._resolve_relative(
            relative, label, required_prefix, dependency_role
        )
        prior = self._captured.get(relative)
        if prior is None:
            with resolved.open("rb") as stream:
                status = os.fstat(stream.fileno())
                native_identity = _native_descriptor_identity(stream.fileno())
                data = stream.read()
            link_count = status.st_nlink
            if link_count != 1:
                raise AggregateError(
                    f"{label} is a hardlink alias ({link_count} native links)"
                )
            identity_path = self._native_paths.get(native_identity)
            if identity_path is not None and identity_path != relative:
                raise AggregateError(
                    f"{label} shares native identity with {identity_path}"
                )
            self._native_paths[native_identity] = relative
            descriptor = {
                "path": relative,
                "bytes": len(data),
                "sha256": sha256_bytes(data),
            }
            prior = CapturedFile(
                relative,
                resolved,
                native_identity,
                link_count,
                (required_prefix,) if required_prefix is not None else (),
                (dependency_role,) if dependency_role is not None else (),
                data,
                descriptor,
            )
            self._captured[relative] = prior
        else:
            if prior.resolved != resolved:
                raise AggregateError(f"{label} changed its resolved real path")
            if required_prefix is not None:
                self._resolve_relative(relative, label, required_prefix, None)
            if dependency_role is not None:
                self._resolve_relative(relative, label, None, dependency_role)
            required_prefixes = tuple(
                dict.fromkeys(
                    prior.required_prefixes
                    + ((required_prefix,) if required_prefix is not None else ())
                )
            )
            dependency_roles = tuple(
                dict.fromkeys(
                    prior.dependency_roles
                    + ((dependency_role,) if dependency_role is not None else ())
                )
            )
            if (
                required_prefixes != prior.required_prefixes
                or dependency_roles != prior.dependency_roles
            ):
                prior = CapturedFile(
                    prior.relative,
                    prior.resolved,
                    prior.native_identity,
                    prior.link_count,
                    required_prefixes,
                    dependency_roles,
                    prior.data,
                    prior.descriptor,
                )
                self._captured[relative] = prior
        if expected is not None and not _descriptor_equal(expected, prior.descriptor):
            raise AggregateError(f"{label} changed after its explicit inventory")
        return dict(prior.descriptor), prior.data

    def capture_recorded(
        self,
        value: Any,
        label: str,
        *,
        required_prefix: str | None = None,
        dependency_role: str | None = None,
    ) -> tuple[dict[str, Any], bytes]:
        if not isinstance(value, dict):
            raise AggregateError(f"{label} descriptor must be an object")
        relative = normalize_relative(value.get("path"), f"{label}.path")
        recorded_bytes = value.get("bytes")
        recorded_hash = str(value.get("sha256", ""))
        if type(recorded_bytes) is not int or recorded_bytes < 0:
            raise AggregateError(f"{label}.bytes must be a nonnegative integer")
        if not SHA256_RE.fullmatch(recorded_hash):
            raise AggregateError(f"{label}.sha256 is invalid")
        expected = {
            "path": relative,
            "bytes": recorded_bytes,
            "sha256": recorded_hash.lower(),
        }
        return self._capture_relative(
            relative,
            label,
            required_prefix=required_prefix,
            dependency_role=dependency_role,
            expected=expected,
        )

    def capture_canonical(
        self, relative: str, label: str, *, required_prefix: str
    ) -> tuple[dict[str, Any], bytes]:
        return self._capture_relative(relative, label, required_prefix=required_prefix)

    def capture_path(
        self,
        path: Path,
        label: str,
        *,
        required_prefix: str,
        expected_relative: str | None = None,
    ) -> tuple[dict[str, Any], bytes]:
        absolute = Path(os.path.abspath(path))
        try:
            relative = absolute.relative_to(self.repo).as_posix()
        except ValueError as error:
            raise AggregateError(f"{label} must be inside the repository") from error
        relative = normalize_relative(relative, f"{label}.path")
        if expected_relative is not None and relative != expected_relative:
            raise AggregateError(
                f"{label} is not canonical: {relative}; expected {expected_relative}"
            )
        return self._capture_relative(relative, label, required_prefix=required_prefix)

    def capture_json_path(
        self,
        path: Path,
        label: str,
        *,
        required_prefix: str = "evidence/",
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        descriptor, data = self.capture_path(
            path, label, required_prefix=required_prefix
        )
        return parse_json_bytes(data, label), descriptor

    def data_for(self, descriptor: Mapping[str, Any]) -> bytes:
        relative = normalize_relative(descriptor.get("path"), "captured descriptor path")
        try:
            captured = self._captured[relative]
        except KeyError as error:
            raise AggregateError(f"uncaptured input requested: {relative}") from error
        if not _descriptor_equal(descriptor, captured.descriptor):
            raise AggregateError(f"captured descriptor mismatch: {relative}")
        return captured.data

    def recheck_all(self) -> None:
        for captured in self._captured.values():
            label = f"pre-commit input {captured.relative}"
            current_resolved = self._resolve_relative(
                captured.relative, label, None, None
            )
            for required_prefix in captured.required_prefixes:
                self._resolve_relative(
                    captured.relative, label, required_prefix, None
                )
            for dependency_role in captured.dependency_roles:
                self._resolve_relative(
                    captured.relative, label, None, dependency_role
                )
            if current_resolved != captured.resolved:
                raise AggregateError(
                    f"input changed resolved path before commit: {captured.relative}"
                )
            with current_resolved.open("rb") as stream:
                status = os.fstat(stream.fileno())
                native_identity = _native_descriptor_identity(stream.fileno())
                current_data = stream.read()
            if native_identity != captured.native_identity:
                raise AggregateError(
                    f"input changed native identity before commit: {captured.relative}"
                )
            if status.st_nlink != captured.link_count or status.st_nlink != 1:
                raise AggregateError(
                    f"input changed native link count before commit: {captured.relative}"
                )
            if current_data != captured.data:
                raise AggregateError(f"input drift before commit: {captured.relative}")


def _existing_local_python_candidate(
    registry: CaptureRegistry, candidate: PurePosixPath
) -> str | None:
    """Return one explicit local Python candidate without enumerating a directory."""

    relative = normalize_relative(candidate.as_posix(), "local Python dependency")
    if not relative.startswith("build/") or not relative.endswith(".py"):
        return None
    lexical = registry.repo / Path(*PurePosixPath(relative).parts)
    try:
        return relative if lexical.is_file() else None
    except OSError as error:
        raise AggregateError(
            f"cannot inspect local Python dependency candidate: {relative}"
        ) from error


def _local_python_candidates(
    registry: CaptureRegistry, relative: str, data: bytes
) -> tuple[str, ...]:
    """Derive existing local imports/dynamic ``.py`` loads from captured bytes."""

    try:
        source = data.decode("utf-8")
        tree = ast.parse(source, filename=relative)
    except (UnicodeDecodeError, SyntaxError) as error:
        raise AggregateError(f"cannot parse local Python implementation {relative}") from error
    parent = PurePosixPath(relative).parent
    candidates: set[str] = set()

    def add_module(module: str, names: Sequence[str] = ()) -> None:
        if not module or module.startswith("."):
            return
        module_path = PurePosixPath(*module.split("."))
        paths = [parent / module_path.with_suffix(".py")]
        paths.append(parent / module_path / "__init__.py")
        for name in names:
            if name != "*":
                paths.append(parent / module_path / f"{name}.py")
        for path in paths:
            candidate = _existing_local_python_candidate(registry, path)
            if candidate is not None:
                candidates.add(candidate)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                add_module(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module is not None:
                add_module(node.module, [alias.name for alias in node.names])
        elif (
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and node.value.endswith(".py")
        ):
            value = node.value
            if "\\" in value or PureWindowsPath(value).is_absolute():
                continue
            value_path = PurePosixPath(value)
            if value_path.is_absolute() or any(part in {"", ".", ".."} for part in value_path.parts):
                continue
            candidate = _existing_local_python_candidate(registry, parent / value_path)
            if candidate is not None:
                candidates.add(candidate)
    candidates.discard(relative)
    return tuple(sorted(candidates))


def capture_local_python_closure(
    registry: CaptureRegistry, root_relative: str, label: str
) -> list[dict[str, Any]]:
    """Capture an explicit, recursive local implementation closure, root first."""

    root_relative = normalize_relative(root_relative, f"{label} root")
    if not root_relative.startswith("build/") or not root_relative.endswith(".py"):
        raise AggregateError(f"{label} root is not a canonical build Python file")
    pending = [root_relative]
    seen: set[str] = set()
    closure: list[dict[str, Any]] = []
    while pending:
        relative = pending.pop(0)
        if relative in seen:
            continue
        descriptor, data = registry.capture_canonical(
            relative, f"{label} implementation {relative}", required_prefix="build/"
        )
        closure.append(descriptor)
        seen.add(relative)
        for candidate in _local_python_candidates(registry, relative, data):
            if candidate not in seen and candidate not in pending:
                pending.append(candidate)
        if len(pending) > 1:
            pending.sort()
    return closure


def _exact_ids(rows: Any, expected: Sequence[str], label: str) -> list[dict[str, Any]]:
    if not isinstance(rows, list) or len(rows) != len(expected):
        raise AggregateError(f"{label} must contain exactly {len(expected)} rows")
    identifiers = [row.get("id") if isinstance(row, dict) else None for row in rows]
    if identifiers != list(expected):
        raise AggregateError(f"{label} has missing, extra, duplicate, or reordered IDs")
    return rows


def load_reconciliation(
    registry: CaptureRegistry, path: Path, role: str
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payload, manifest_descriptor = registry.capture_json_path(
        path, "source reconciliation manifest"
    )
    if payload.get("schema") != RECONCILIATION_SCHEMA:
        raise AggregateError("source reconciliation manifest schema is not accepted")
    if payload.get("status") != "PASS" or payload.get("total_units") != 722:
        raise AggregateError("source reconciliation manifest is not a passing 722-unit input")
    rows = _exact_ids(payload.get("units"), EXPECTED_IDS, "source reconciliation")
    config = ROLE_CONFIG[role]
    field = config["source_field"]
    prefix = config.get("authoritative_prefix", config["compiled_prefix"])
    locale_prefix = (
        "source/locale/ar-classical/" if field == "classical" else "source/locale/ar/"
    )
    results: list[dict[str, Any]] = []
    for identifier, row in zip(EXPECTED_IDS, rows, strict=True):
        source_path = normalize_relative(
            row.get("source_path"), f"reconciliation {identifier}.source_path"
        )
        if not source_path.startswith("content/"):
            raise AggregateError(f"reconciliation {identifier} source_path is not content")
        expected_path = locale_prefix + source_path
        descriptor, _ = registry.capture_recorded(
            row.get(field),
            f"reconciliation {identifier} {field}",
            required_prefix=prefix,
        )
        if descriptor["path"] != expected_path:
            raise AggregateError(
                f"reconciliation {identifier} descriptor/path binding is wrong"
            )
        results.append(
            {
                "id": identifier,
                "source_path": source_path,
                "authoritative": descriptor,
            }
        )
    if len({row["source_path"] for row in results}) != 722 or len(
        {row["authoritative"]["path"] for row in results}
    ) != 722:
        raise AggregateError("reconciliation must bind 722 distinct ID/path identities")
    return manifest_descriptor, results


def load_presentation_mapping(
    registry: CaptureRegistry,
    path: Path,
    reconciliation_rows: Sequence[Mapping[str, Any]],
) -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    Mapping[str, Any],
    Mapping[str, Any],
]:
    payload, mapping_descriptor = registry.capture_json_path(
        path, "Classical presentation mapping"
    )
    if payload.get("schema") != PRESENTATION_SCHEMA:
        raise AggregateError("Classical presentation mapping schema is not accepted")
    if (
        payload.get("status") != "PASS"
        or payload.get("release_eligible") is not True
        or payload.get("presentation_locale") != "ar-classical-presentation"
    ):
        raise AggregateError("Classical presentation mapping is not release-eligible")
    rows = _exact_ids(payload.get("units"), EXPECTED_IDS, "Classical mapping")
    results: list[dict[str, Any]] = []
    for identifier, row, reconciliation in zip(
        EXPECTED_IDS, rows, reconciliation_rows, strict=True
    ):
        source, _ = registry.capture_recorded(
            row.get("source"),
            f"Classical mapping {identifier} authoritative source",
            required_prefix="source/locale/ar-classical/content/",
        )
        if not _descriptor_equal(source, reconciliation["authoritative"]):
            raise AggregateError(
                f"Classical mapping {identifier} is not bound to reconciliation"
            )
        presentation, _ = registry.capture_recorded(
            row.get("presentation"),
            f"Classical mapping {identifier} compiled presentation",
            required_prefix="source/locale/ar-classical-presentation/content/",
        )
        expected_path = (
            "source/locale/ar-classical-presentation/"
            + reconciliation["source_path"]
        )
        if presentation["path"] != expected_path:
            raise AggregateError(
                f"Classical mapping {identifier} presentation path is wrong"
            )
        results.append(
            {
                "id": identifier,
                "source_path": reconciliation["source_path"],
                "authoritative": source,
                "compiled": presentation,
            }
        )
    if len({row["compiled"]["path"] for row in results}) != 722:
        raise AggregateError("Classical mapping must bind 722 distinct presentations")
    decision_ledger = payload.get("decision_ledger")
    authority = payload.get("authority")
    if not isinstance(decision_ledger, dict) or not isinstance(authority, dict):
        raise AggregateError("Classical mapping lacks decision-ledger/generator authority")
    generator = authority.get("generator")
    if not isinstance(generator, dict):
        raise AggregateError("Classical mapping lacks generator identity")
    return mapping_descriptor, results, decision_ledger, generator


def _decode_exact(data: bytes, label: str) -> tuple[str, bool]:
    bom = data.startswith(b"\xef\xbb\xbf")
    body = data[3:] if bom else data
    try:
        return body.decode("utf-8"), bom
    except UnicodeDecodeError as error:
        raise AggregateError(f"{label} is not strict UTF-8") from error


def _encode_exact(text: str, bom: bool) -> bytes:
    raw = text.encode("utf-8")
    return (b"\xef\xbb\xbf" + raw) if bom else raw


def _tree_hash(files: Mapping[str, bytes]) -> str:
    digest = hashlib.sha256()
    for relative, raw in sorted(files.items()):
        path_bytes = relative.encode("utf-8")
        digest.update(len(path_bytes).to_bytes(8, "big"))
        digest.update(path_bytes)
        digest.update(len(raw).to_bytes(8, "big"))
        digest.update(raw)
    return digest.hexdigest()


def _inverse_one(
    presented_raw: bytes,
    authoritative_raw: bytes,
    occurrences: Any,
    identifier: str,
) -> bytes:
    if not isinstance(occurrences, list):
        raise AggregateError(f"inverse ledger {identifier} occurrences must be a list")
    presented, presentation_bom = _decode_exact(presented_raw, f"{identifier} presentation")
    _, authority_bom = _decode_exact(authoritative_raw, f"{identifier} authority")
    if presentation_bom != authority_bom:
        raise AggregateError(f"inverse ledger {identifier} changed UTF-8 BOM state")
    replacements: list[tuple[int, int, str, str, str]] = []
    occurrence_ids: set[str] = set()
    fields = {
        "presented_char_start",
        "presented_char_end",
        "replacement",
        "source",
    }
    # Every notation-census occurrence may carry a ``source`` token even when
    # it is an explicit exemption and therefore has no presentation edit.
    # Only the three presentation-specific fields opt a row into inverse
    # replacement replay.  Once any of them is present, all four fields remain
    # mandatory and are validated below.
    presentation_fields = fields - {"source"}
    for index, occurrence in enumerate(occurrences):
        if not isinstance(occurrence, dict):
            raise AggregateError(f"inverse ledger {identifier} occurrence is not an object")
        present = fields.intersection(occurrence)
        if not presentation_fields.intersection(occurrence):
            continue
        if present != fields:
            raise AggregateError(f"inverse ledger {identifier} has a partial replacement")
        occurrence_id = _reject_identity_text(
            occurrence.get("occurrence_id"),
            f"inverse ledger {identifier} occurrence identity",
        )
        if occurrence_id in occurrence_ids:
            raise AggregateError(f"inverse ledger {identifier} duplicates an occurrence")
        occurrence_ids.add(occurrence_id)
        start = occurrence["presented_char_start"]
        end = occurrence["presented_char_end"]
        replacement = occurrence["replacement"]
        source = occurrence["source"]
        if (
            type(start) is not int
            or type(end) is not int
            or not isinstance(replacement, str)
            or not isinstance(source, str)
            or not (0 <= start <= end <= len(presented))
        ):
            raise AggregateError(f"inverse ledger {identifier} has invalid span {index}")
        replacements.append((start, end, replacement, source, occurrence_id))
    ordered = sorted(replacements)
    for left, right in zip(ordered, ordered[1:]):
        if left[1] > right[0]:
            raise AggregateError(f"inverse ledger {identifier} has overlapping spans")
    reconstructed = presented
    for start, end, replacement, source, occurrence_id in reversed(ordered):
        if reconstructed[start:end] != replacement:
            raise AggregateError(
                f"inverse replay {identifier} span drift: {occurrence_id}"
            )
        reconstructed = reconstructed[:start] + source + reconstructed[end:]
    reconstructed_raw = _encode_exact(reconstructed, authority_bom)
    if reconstructed_raw != authoritative_raw:
        raise AggregateError(f"inverse replay {identifier} is not byte-identical")
    return reconstructed_raw


def replay_classical_inverse(
    registry: CaptureRegistry,
    decision_path: Path,
    expected_decision: Mapping[str, Any],
    expected_generator: Mapping[str, Any],
    mapping_rows: Sequence[Mapping[str, Any]],
    aggregator_descriptor: Mapping[str, Any],
) -> dict[str, Any]:
    payload, decision_descriptor = registry.capture_json_path(
        decision_path, "Classical inverse decision ledger"
    )
    if not _descriptor_equal(decision_descriptor, expected_decision):
        raise AggregateError("Classical decision ledger is not the mapping-bound ledger")
    if (
        payload.get("schema") != DECISION_SCHEMA
        or payload.get("status") != "PASS"
        or payload.get("release_eligible") is not True
        or payload.get("presentation_locale") != "ar-classical-presentation"
    ):
        raise AggregateError("Classical inverse decision ledger is not release-eligible")
    authority = payload.get("authority")
    if not isinstance(authority, dict) or not _descriptor_equal(
        authority.get("generator", {}), expected_generator
    ):
        raise AggregateError("Classical decision ledger generator identity disagrees")
    rows = _exact_ids(payload.get("units"), EXPECTED_IDS, "Classical decision ledger")
    source_files: dict[str, bytes] = {}
    presentation_files: dict[str, bytes] = {}
    sequence = hashlib.sha256()
    for identifier, row, mapping in zip(EXPECTED_IDS, rows, mapping_rows, strict=True):
        if not _descriptor_equal(row.get("source", {}), mapping["authoritative"]):
            raise AggregateError(f"inverse ledger {identifier} source identity disagrees")
        if not _descriptor_equal(row.get("presentation", {}), mapping["compiled"]):
            raise AggregateError(
                f"inverse ledger {identifier} presentation identity disagrees"
            )
        authoritative_raw = registry.data_for(mapping["authoritative"])
        presented_raw = registry.data_for(mapping["compiled"])
        reconstructed = _inverse_one(
            presented_raw, authoritative_raw, row.get("occurrences"), identifier
        )
        source_files[mapping["authoritative"]["path"]] = authoritative_raw
        presentation_files[mapping["compiled"]["path"]] = presented_raw
        identifier_bytes = identifier.encode("ascii")
        sequence.update(len(identifier_bytes).to_bytes(8, "big"))
        sequence.update(identifier_bytes)
        sequence.update(len(reconstructed).to_bytes(8, "big"))
        sequence.update(reconstructed)
    source_tree = _tree_hash(source_files)
    presentation_tree = _tree_hash(presentation_files)
    for name, observed in (
        ("source_tree_sha256", source_tree),
        ("presentation_tree_sha256", presentation_tree),
    ):
        recorded = str(payload.get(name, ""))
        if not SHA256_RE.fullmatch(recorded) or recorded.lower() != observed:
            raise AggregateError(f"Classical decision ledger {name} does not replay")
    return {
        "status": "PASS_DETERMINISTIC_BYTE_REPLAY",
        "units_replayed": 722,
        "decision_ledger": decision_descriptor,
        "generator": dict(expected_generator),
        "verifier": dict(aggregator_descriptor),
        "source_tree_sha256": source_tree,
        "presentation_tree_sha256": presentation_tree,
        "ordered_reconstruction_sha256": sequence.hexdigest(),
        "self_asserted_inverse_fields_used_as_authority": False,
    }


def load_graph(
    registry: CaptureRegistry,
    path: Path,
    *,
    role: str,
    partition: str,
    expected_ids: Sequence[str],
    master: Mapping[str, Any],
    wrapper: Mapping[str, Any],
    reconciliation_descriptor: Mapping[str, Any],
    reconciliation_by_id: Mapping[str, Mapping[str, Any]],
    compiled_by_id: Mapping[str, Mapping[str, Any]],
    presentation_mapping: Mapping[str, Any] | None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    label = f"{partition} verified graph"
    payload, graph_descriptor = registry.capture_json_path(path, label)
    config = ROLE_CONFIG[role]
    if payload.get("schema") != GRAPH_SCHEMA:
        raise AggregateError(f"{label} schema is not accepted")
    if payload.get("status") != "PASS" or payload.get("failures") != []:
        raise AggregateError(f"{label} is not a passing verification input")
    graph_role = _reject_identity_text(payload.get("role"), f"{label}.role")
    graph_profile = _reject_identity_text(payload.get("profile"), f"{label}.profile")
    graph_partition = _reject_identity_text(
        payload.get("partition"), f"{label}.partition"
    )
    if graph_role != role or graph_profile != config["profile"]:
        raise AggregateError(f"{label} belongs to a different role or profile")
    if graph_partition != partition:
        raise AggregateError(f"{label} has the wrong partition")
    if not _descriptor_equal(payload.get("master", {}), master):
        raise AggregateError(f"{label} is not bound to its canonical master")
    if not _descriptor_equal(payload.get("wrapper", {}), wrapper):
        raise AggregateError(f"{label} is not bound to its canonical wrapper")
    if not _descriptor_equal(
        payload.get("reconciliation", {}), reconciliation_descriptor
    ):
        raise AggregateError(f"{label} is not bound to reconciliation")
    if config["presentation_required"]:
        if presentation_mapping is None or not _descriptor_equal(
            payload.get("presentation_mapping", {}), presentation_mapping
        ):
            raise AggregateError(f"{label} is not bound to presentation mapping")
    elif payload.get("presentation_mapping") is not None:
        raise AggregateError(f"{label} has unexpected Classical lineage")

    rows = _exact_ids(payload.get("units"), expected_ids, label)
    units: list[dict[str, Any]] = []
    for identifier, row in zip(expected_ids, rows, strict=True):
        expected_reconciliation = reconciliation_by_id[identifier]
        source_path = normalize_relative(
            row.get("source_path"), f"{label} {identifier}.source_path"
        )
        if source_path != expected_reconciliation["source_path"]:
            raise AggregateError(f"{label} {identifier} source_path binding is wrong")
        descriptor, _ = registry.capture_recorded(
            row,
            f"{label} {identifier} body",
            required_prefix=config["compiled_prefix"],
        )
        if not _descriptor_equal(descriptor, compiled_by_id[identifier]):
            raise AggregateError(f"{label} {identifier} descriptor binding is wrong")
        units.append(
            {
                "id": identifier,
                "source_path": source_path,
                "descriptor": descriptor,
            }
        )

    raw_dependencies = payload.get("dependencies")
    if not isinstance(raw_dependencies, list) or not raw_dependencies:
        raise AggregateError(f"{label} lacks an explicit dependency closure")
    dependencies: list[dict[str, Any]] = []
    for index, recorded in enumerate(raw_dependencies):
        dependency, _ = registry.capture_recorded(
            recorded,
            f"{label} dependency {index}",
            dependency_role=role,
        )
        dependencies.append(dependency)
    if len({item["path"] for item in dependencies}) != len(dependencies):
        raise AggregateError(f"{label} dependency closure contains duplicates")
    dependency_map = {item["path"]: item for item in dependencies}
    for required in [master, wrapper] + [row["descriptor"] for row in units]:
        if required["path"] not in dependency_map or not _descriptor_equal(
            dependency_map[required["path"]], required
        ):
            raise AggregateError(f"{label} dependency closure omits a required input")
    return graph_descriptor, units, dependencies


def _ensure_embed_safe(data: bytes, label: str) -> None:
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise AggregateError(f"{label} is not strict UTF-8") from error
    if MARKER_TOKEN in data:
        raise AggregateError(f"{label} contains an archive marker token")


def _append_block(
    output: bytearray,
    *,
    kind: str,
    identifier: str,
    descriptor: Mapping[str, Any],
    data: bytes,
) -> dict[str, int]:
    _ensure_embed_safe(data, f"embedded {identifier}")
    metadata = {
        "bytes": descriptor["bytes"],
        "id": identifier,
        "kind": kind,
        "path": descriptor["path"],
        "sha256": descriptor["sha256"],
    }
    encoded = json.dumps(metadata, sort_keys=True, separators=(",", ":"))
    output.extend(BLOCK_MARKER + b"BEGIN " + encoded.encode("ascii") + b"\n")
    start = len(output)
    output.extend(data)
    end = len(output)
    if not data.endswith(b"\n"):
        output.extend(b"\n")
    closing = {
        "id": identifier,
        "kind": kind,
        "sha256": descriptor["sha256"],
    }
    output.extend(
        BLOCK_MARKER
        + b"END "
        + json.dumps(closing, sort_keys=True, separators=(",", ":")).encode("ascii")
        + b"\n"
    )
    return {"start": start, "end_exclusive": end}


def _header(
    role: str,
    identity: Mapping[str, Any],
    assembler_path: str,
    rtl_link_repair_path: str,
) -> bytes:
    config = ROLE_CONFIG[role]
    identity_json = json.dumps(identity, sort_keys=True, separators=(",", ":"))
    lines = [
        "% !TeX encoding = UTF-8",
        "% ملف لاتخ تجميعي أرشيفي مباشر لمصادر طبعة المنطق المفتوح العربية الكاملة.",
        f"% الطبعة: {config['arabic_label']}؛ الوحدات: 722 (642 + 80).",
        "% يحفظ هذا الملف قائدي المكوّنين ومدخليهما وكل أجسام المصادر مرتبة وبايتاتها الأصلية بين فواصل ثابتة.",
        "% ليس هذا قائدا لبناء أحادي المرور، ولا يُدَّعى أنه يولد وحده بايتات PDF المطابقة.",
        "% تتطلب إعادة PDF الدقيقة مهمتي LuaLaTeX مستقلتين وفق الخيارات والتبعيات الموثقة في إيصال JSON،",
        f"% ثم إصلاح مستطيلات روابط كل مكوّن إلزاميا بالبرنامج المثبت: {rtl_link_repair_path}،",
        f"% ثم تجميع ملفي PDF المُصلحين ببرنامج Python/pypdf المثبت: {assembler_path}.",
        f"% الترجمة والتصحيحات السابقة الموثقة في المصدر الموروث: {AI_INHERITED_DISCLOSURE}.",
        *(
            [f"% تصحيحا تنسيق OLP-0310 وOLP-0658 في الطبعة التراثية: {AI_PREVIOUS_LAYOUT_DISCLOSURE}.",
             f"% تصحيح اتجاه أسماء الدوال اللاتينية وخرائط Unicode: {AI_REPAIR_DISCLOSURE}.",
             f"% تصحيح اتجاه أسماء النظريات والأنساق وقاعدة القطع ورمز القيمة: {AI_PREVIOUS_NAMED_DISCLOSURE}."]
            if role == "classical-eastern-rtl" else []
        ),
        f"% تجميع لاتخ الأرشيفي والتحقق الحتمي من الهوية والتغطية: {AI_DISCLOSURE}.",
        "% لا يعني هذا البيان مراجعة بشرية أو تأليفا بشريا غير موثق.",
        "% يحوي ملف JSON المصاحب الهويات والتجزئة والمديات البايتية وطريق إعادة الإنتاج الملزم.",
        "% OPENLOGIC-ARCHIVAL-IDENTITY " + identity_json,
        "",
    ]
    return "\n".join(lines).encode("utf-8")


def _file_identity(status: os.stat_result) -> tuple[int, int]:
    return status.st_dev, status.st_ino


if os.name == "nt":

    class _ByHandleFileInformation(ctypes.Structure):
        _fields_ = [
            ("file_attributes", wintypes.DWORD),
            ("creation_time", wintypes.FILETIME),
            ("last_access_time", wintypes.FILETIME),
            ("last_write_time", wintypes.FILETIME),
            ("volume_serial_number", wintypes.DWORD),
            ("file_size_high", wintypes.DWORD),
            ("file_size_low", wintypes.DWORD),
            ("number_of_links", wintypes.DWORD),
            ("file_index_high", wintypes.DWORD),
            ("file_index_low", wintypes.DWORD),
        ]

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _create_file = _kernel32.CreateFileW
    _create_file.argtypes = [
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.c_void_p,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    ]
    _create_file.restype = wintypes.HANDLE
    _get_file_information = _kernel32.GetFileInformationByHandle
    _get_file_information.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(_ByHandleFileInformation),
    ]
    _get_file_information.restype = wintypes.BOOL
    _get_file_size = _kernel32.GetFileSizeEx
    _get_file_size.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(ctypes.c_longlong),
    ]
    _get_file_size.restype = wintypes.BOOL
    _set_file_pointer = _kernel32.SetFilePointerEx
    _set_file_pointer.argtypes = [
        wintypes.HANDLE,
        ctypes.c_longlong,
        ctypes.POINTER(ctypes.c_longlong),
        wintypes.DWORD,
    ]
    _set_file_pointer.restype = wintypes.BOOL
    _read_file = _kernel32.ReadFile
    _read_file.argtypes = [
        wintypes.HANDLE,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        ctypes.c_void_p,
    ]
    _read_file.restype = wintypes.BOOL
    _set_file_information = _kernel32.SetFileInformationByHandle
    _set_file_information.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    ]
    _set_file_information.restype = wintypes.BOOL
    _close_handle = _kernel32.CloseHandle
    _close_handle.argtypes = [wintypes.HANDLE]
    _close_handle.restype = wintypes.BOOL
    _INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value


def _windows_handle_identity(handle: int) -> tuple[int, ...]:
    information = _ByHandleFileInformation()
    if not _get_file_information(handle, ctypes.byref(information)):
        raise ctypes.WinError(ctypes.get_last_error())
    file_index = (information.file_index_high << 32) | information.file_index_low
    creation = (
        information.creation_time.dwHighDateTime << 32
    ) | information.creation_time.dwLowDateTime
    return information.volume_serial_number, file_index, creation


def _native_descriptor_identity(descriptor: int) -> tuple[int, ...]:
    if os.name == "nt":
        return _windows_handle_identity(msvcrt.get_osfhandle(descriptor))
    status = os.fstat(descriptor)
    return status.st_dev, status.st_ino, status.st_ctime_ns


def _open_windows_delete_handle(path: Path) -> int | None:
    handle = _create_file(
        str(path),
        0x80000000 | 0x00010000 | 0x00000080,
        0x00000001 | 0x00000002 | 0x00000004,
        None,
        3,
        0x00200000,
        None,
    )
    if handle == _INVALID_HANDLE_VALUE:
        error = ctypes.get_last_error()
        if error in {2, 3}:
            return None
        raise AggregateError(
            f"cannot open ownership-pinned removal handle for {path.name}: "
            f"Windows error {error}"
        )
    return handle


def _open_windows_final_read_handle(path: Path, label: str) -> int:
    """Open a read handle that denies writers and deleters until final readback ends."""

    if os.name != "nt":
        raise AggregateError(
            "identity-pinned non-delete-share final readback is unavailable outside Windows"
        )
    handle = _create_file(
        str(path),
        0x80000000 | 0x00000080,
        0x00000001,
        None,
        3,
        0x00200000,
        None,
    )
    if handle == _INVALID_HANDLE_VALUE:
        error = ctypes.get_last_error()
        raise AggregateError(
            f"cannot open identity-pinned final {label} handle: Windows error {error}"
        )
    return handle


def _read_windows_handle(handle: int) -> bytes:
    size = ctypes.c_longlong()
    if not _get_file_size(handle, ctypes.byref(size)):
        raise ctypes.WinError(ctypes.get_last_error())
    if size.value < 0:
        raise AggregateError("ownership-pinned file has a negative size")
    if not _set_file_pointer(handle, 0, None, 0):
        raise ctypes.WinError(ctypes.get_last_error())
    remaining = size.value
    chunks: list[bytes] = []
    while remaining:
        requested = min(remaining, 1024 * 1024)
        buffer = ctypes.create_string_buffer(requested)
        count = wintypes.DWORD()
        if not _read_file(handle, buffer, requested, ctypes.byref(count), None):
            raise ctypes.WinError(ctypes.get_last_error())
        if count.value == 0:
            raise AggregateError("ownership-pinned read ended before the recorded size")
        chunks.append(buffer.raw[: count.value])
        remaining -= count.value
    return b"".join(chunks)


def _read_final_pair_locked(
    output: Path,
    output_temp: ExclusiveTemp,
    aggregate_bytes: bytes,
    receipt: Path,
    receipt_temp: ExclusiveTemp,
    receipt_bytes: bytes,
    hook: Callable[[str, Path, Path], None] | None,
) -> tuple[bytes, bytes]:
    """Read both finals through simultaneously held, identity-pinned handles."""

    output_handle: int | None = None
    receipt_handle: int | None = None

    def invoke(stage: str) -> None:
        if hook is not None:
            hook(stage, output, receipt)

    def require_identities() -> None:
        if output_handle is None or receipt_handle is None:
            raise AggregateError("final pair handles are not both pinned")
        if _windows_handle_identity(output_handle) != output_temp.native_identity:
            raise AggregateError("aggregate final handle lost its committed identity")
        if _windows_handle_identity(receipt_handle) != receipt_temp.native_identity:
            raise AggregateError("receipt final handle lost its committed identity")

    try:
        invoke("before-open-output")
        output_handle = _open_windows_final_read_handle(output, "aggregate")
        if _windows_handle_identity(output_handle) != output_temp.native_identity:
            raise AggregateError("aggregate final path was replaced before pinned readback")
        invoke("after-open-output")
        receipt_handle = _open_windows_final_read_handle(receipt, "receipt")
        require_identities()
        invoke("after-open-receipt")
        require_identities()
        final_aggregate = _read_windows_handle(output_handle)
        invoke("after-read-output")
        require_identities()
        final_receipt = _read_windows_handle(receipt_handle)
        invoke("after-read-receipt")
        require_identities()
        if final_aggregate != aggregate_bytes:
            raise AggregateError("aggregate final readback differs from generated bytes")
        if final_receipt != receipt_bytes:
            raise AggregateError("receipt final readback differs from generated bytes")
        invoke("before-return")
        require_identities()
        if _read_windows_handle(output_handle) != aggregate_bytes:
            raise AggregateError("aggregate changed before final handle release")
        if _read_windows_handle(receipt_handle) != receipt_bytes:
            raise AggregateError("receipt changed before final handle release")
        require_identities()
        return final_aggregate, final_receipt
    finally:
        if receipt_handle is not None:
            _close_handle(receipt_handle)
        if output_handle is not None:
            _close_handle(output_handle)


def _path_has_native_identity(path: Path, identity: tuple[int, ...]) -> bool:
    if os.name != "nt":
        try:
            status = os.stat(path, follow_symlinks=False)
        except OSError:
            return False
        return (status.st_dev, status.st_ino, status.st_ctime_ns) == identity
    handle = _open_windows_delete_handle(path)
    if handle is None:
        return False
    try:
        return _windows_handle_identity(handle) == identity
    finally:
        _close_handle(handle)


def _temp_owns_path(temporary: ExclusiveTemp, path: Path) -> bool:
    try:
        return (
            _file_identity(os.stat(path, follow_symlinks=False))
            == temporary.stat_identity
        )
    except OSError:
        return False


def _read_open_descriptor(descriptor: int) -> bytes:
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        chunk = os.read(descriptor, 1024 * 1024)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)


def _remove_owned_path_atomic(
    path: Path,
    temporary: ExclusiveTemp,
    expected: bytes | None,
    label: str,
    before_delete: Callable[[str, Path], None] | None,
) -> None:
    """Remove only the handle-pinned owned file; never unlink by checked name."""

    if os.name != "nt":
        raise AggregateError(
            "atomic ownership-pinned removal is unavailable outside Windows"
        )
    handle = _open_windows_delete_handle(path)
    if handle is None:
        return
    disposition_error: int | None = None
    try:
        if _windows_handle_identity(handle) != temporary.native_identity:
            return
        if expected is not None and _read_windows_handle(handle) != expected:
            raise AggregateError(f"{label} owned bytes changed; removal refused")
        if before_delete is not None:
            before_delete(label, path)
        disposition = ctypes.c_ubyte(1)
        if not _set_file_information(
            handle, 4, ctypes.byref(disposition), ctypes.sizeof(disposition)
        ):
            disposition_error = ctypes.get_last_error()
    finally:
        _close_handle(handle)
    if _path_has_native_identity(path, temporary.native_identity):
        detail = (
            f" (Windows error {disposition_error})"
            if disposition_error is not None
            else ""
        )
        raise AggregateError(f"{label} retained the owned path{detail}")


def _close_and_remove_owned_temp(
    temporary: ExclusiveTemp,
    label: str,
    before_delete: Callable[[str, Path], None] | None,
) -> None:
    if temporary.descriptor >= 0:
        os.close(temporary.descriptor)
        temporary.descriptor = -1
    _remove_owned_path_atomic(
        temporary.path,
        temporary,
        temporary.expected,
        label,
        before_delete,
    )


def _write_exclusive_temp(parent: Path, stem: str, data: bytes) -> ExclusiveTemp:
    descriptor, name = tempfile.mkstemp(
        prefix=f".{stem}.aggregate-", suffix=".tmp", dir=parent
    )
    path = Path(name)
    temporary = ExclusiveTemp(
        path=path,
        descriptor=descriptor,
        stat_identity=_file_identity(os.fstat(descriptor)),
        native_identity=_native_descriptor_identity(descriptor),
        expected=data,
    )
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if _read_open_descriptor(descriptor) != data:
            raise AggregateError(f"exclusive temporary readback changed: {path.name}")
        if not _temp_owns_path(temporary, path):
            raise AggregateError(f"exclusive temporary path changed: {path.name}")
        return temporary
    except Exception:
        if temporary.descriptor >= 0:
            os.close(temporary.descriptor)
            temporary.descriptor = -1
        _remove_owned_path_atomic(
            temporary.path,
            temporary,
            None,
            "failed temporary creation cleanup",
            None,
        )
        raise


def _rollback_owned_link(
    final: Path,
    temporary: ExclusiveTemp,
    expected: bytes,
    label: str,
    before_delete: Callable[[str, Path], None] | None,
) -> None:
    _remove_owned_path_atomic(final, temporary, expected, label, before_delete)


def _commit_pair_exclusive(
    output: Path,
    aggregate_bytes: bytes,
    receipt: Path,
    receipt_bytes: bytes,
    precommit: Callable[[], None],
    before_owned_delete: Callable[[str, Path], None] | None,
    final_readback_hook: Callable[[str, Path, Path], None] | None = None,
) -> dict[str, Any]:
    """Commit two files without replacing any path that appears concurrently."""

    output_temp = _write_exclusive_temp(output.parent, output.name, aggregate_bytes)
    receipt_temp: ExclusiveTemp | None = None
    output_linked = False
    receipt_linked = False
    output_temp_cleaned = False
    receipt_temp_cleaned = False

    def rollback_links() -> None:
        errors: list[BaseException] = []
        if receipt_linked and receipt_temp is not None:
            try:
                _rollback_owned_link(
                    receipt,
                    receipt_temp,
                    receipt_bytes,
                    "rollback-receipt",
                    before_owned_delete,
                )
            except Exception as error:  # preserve the other rollback attempt
                errors.append(error)
        if output_linked:
            try:
                _rollback_owned_link(
                    output,
                    output_temp,
                    aggregate_bytes,
                    "rollback-output",
                    before_owned_delete,
                )
            except Exception as error:  # preserve the other rollback attempt
                errors.append(error)
        if errors:
            raise AggregateError(
                f"exclusive pair rollback failed in {len(errors)} owned path(s)"
            ) from errors[0]

    try:
        receipt_temp = _write_exclusive_temp(receipt.parent, receipt.name, receipt_bytes)
        precommit()
        if not _temp_owns_path(output_temp, output_temp.path) or not _temp_owns_path(
            receipt_temp, receipt_temp.path
        ):
            raise AggregateError("exclusive temporary claim changed before commit")
        os.link(output_temp.path, output)
        output_linked = True
        os.link(receipt_temp.path, receipt)
        receipt_linked = True
        if not _temp_owns_path(output_temp, output):
            raise AggregateError("aggregate final path lost its exclusive claim")
        if not _temp_owns_path(receipt_temp, receipt):
            raise AggregateError("receipt final path lost its exclusive claim")
        # Release the writable temporary descriptors and remove only their
        # owned names before opening both finals with share-read-only handles.
        # The final hardlinks keep the same native file identities alive.
        _close_and_remove_owned_temp(
            output_temp, "cleanup-output-temp", before_owned_delete
        )
        output_temp_cleaned = True
        _close_and_remove_owned_temp(
            receipt_temp, "cleanup-receipt-temp", before_owned_delete
        )
        receipt_temp_cleaned = True
        final_aggregate, final_receipt = _read_final_pair_locked(
            output,
            output_temp,
            aggregate_bytes,
            receipt,
            receipt_temp,
            receipt_bytes,
            final_readback_hook,
        )
        return {
            "aggregate": {
                "file": output.name,
                "bytes": len(final_aggregate),
                "sha256": sha256_bytes(final_aggregate),
            },
            "receipt": {
                "file": receipt.name,
                "bytes": len(final_receipt),
                "sha256": sha256_bytes(final_receipt),
            },
        }
    except FileExistsError as error:
        try:
            rollback_links()
        except AggregateError as rollback_error:
            raise rollback_error from error
        raise AggregateError("release target appeared during exclusive pair commit") from error
    except Exception as error:
        try:
            rollback_links()
        except AggregateError as rollback_error:
            raise rollback_error from error
        raise
    finally:
        cleanup_errors: list[Exception] = []
        if not output_temp_cleaned:
            try:
                _close_and_remove_owned_temp(
                    output_temp, "cleanup-output-temp", before_owned_delete
                )
            except Exception as error:
                cleanup_errors.append(error)
        if receipt_temp is not None and not receipt_temp_cleaned:
            try:
                _close_and_remove_owned_temp(
                    receipt_temp, "cleanup-receipt-temp", before_owned_delete
                )
            except Exception as error:
                cleanup_errors.append(error)
        if cleanup_errors:
            raise AggregateError(
                f"exclusive temporary cleanup failed in {len(cleanup_errors)} path(s)"
            ) from cleanup_errors[0]


def _validate_output_identity(path: Path, label: str, suffix: str) -> None:
    if path.suffix.lower() != suffix:
        raise AggregateError(f"{label} must use the {suffix} suffix")
    _reject_identity_text(path.name, f"{label} filename")
    if not path.parent.is_dir():
        raise AggregateError(f"{label} parent does not exist: {path.parent}")


def assemble(
    *,
    repo: Path,
    role: str,
    reader_master: Path,
    closure_master: Path,
    reader_wrapper: Path,
    closure_wrapper: Path,
    reader_graph: Path,
    closure_graph: Path,
    reconciliation: Path,
    assembler: Path,
    output: Path,
    receipt: Path,
    presentation_mapping: Path | None = None,
    classical_decision_ledger: Path | None = None,
    _before_precommit_recheck: Callable[[], None] | None = None,
    _before_owned_handle_delete: Callable[[str, Path], None] | None = None,
    _final_readback_hook: Callable[[str, Path, Path], None] | None = None,
) -> dict[str, Any]:
    """Validate explicit authorities and transactionally write an aggregate pair."""

    if role not in ROLE_CONFIG:
        raise AggregateError(f"unsupported role: {role!r}")
    config = ROLE_CONFIG[role]
    required_classical = config["presentation_required"]
    if required_classical != (presentation_mapping is not None):
        raise AggregateError("Classical role requires exactly one presentation mapping")
    if required_classical != (classical_decision_ledger is not None):
        raise AggregateError("Classical role requires exactly one inverse decision ledger")
    _validate_output_identity(output, "aggregate output", ".tex")
    _validate_output_identity(receipt, "aggregate receipt", ".json")
    if Path(os.path.abspath(output)) == Path(os.path.abspath(receipt)):
        raise AggregateError("aggregate and receipt paths must be distinct")

    registry = CaptureRegistry(repo)
    canonical_inputs = {
        "reader_master": (reader_master, config["reader_master"]),
        "closure_master": (closure_master, config["closure_master"]),
        "reader_wrapper": (reader_wrapper, config["reader_wrapper"]),
        "closure_wrapper": (closure_wrapper, config["closure_wrapper"]),
        "assembler": (assembler, config["assembler"]),
    }
    descriptors: dict[str, dict[str, Any]] = {}
    for key, (path, expected) in canonical_inputs.items():
        prefix = "build/" if key == "assembler" else expected.rsplit("/", 1)[0] + "/"
        descriptors[key], _ = registry.capture_path(
            path,
            key.replace("_", " "),
            required_prefix=prefix,
            expected_relative=expected,
        )
    aggregator_descriptor, aggregator_bytes = registry.capture_canonical(
        AGGREGATOR_RELATIVE, "aggregate verifier", required_prefix="build/"
    )
    try:
        running_bytes = Path(__file__).resolve().read_bytes()
    except OSError as error:
        raise AggregateError("cannot capture running aggregate verifier") from error
    if aggregator_bytes != running_bytes:
        raise AggregateError("repository aggregate verifier differs from executing code")
    rtl_link_repair_closure = capture_local_python_closure(
        registry,
        RTL_LINK_REPAIR_RELATIVE,
        "mandatory RTL link-rectangle repair",
    )
    rtl_link_repair = rtl_link_repair_closure[0]
    if (rtl_link_repair["bytes"], rtl_link_repair["sha256"]) not in (
        {(RTL_LINK_REPAIR_BYTES, RTL_LINK_REPAIR_SHA256)} | RTL_LINK_REPAIR_SUCCESSORS
    ):
        raise AggregateError("mandatory RTL link repair identity is not accepted")
    if RTL_LINK_REPAIR_CORE_RELATIVE not in {
        item["path"] for item in rtl_link_repair_closure
    }:
        raise AggregateError("mandatory RTL link repair core is absent from its closure")
    assembly_implementation_closure = capture_local_python_closure(
        registry,
        config["assembler"],
        "complete reader PDF assembler",
    )
    if role == "classical-eastern-rtl" and COMPLETE_ASSEMBLER_RELATIVE not in {
        item["path"] for item in assembly_implementation_closure
    }:
        raise AggregateError("Classical assembler base implementation is absent")
    build_driver, _ = registry.capture_canonical(
        config["build_driver"], "guarded build driver", required_prefix="build/"
    )
    build_inner, _ = registry.capture_canonical(
        config["build_inner"], "guarded inner build", required_prefix="build/"
    )

    reconciliation_descriptor, reconciliation_rows = load_reconciliation(
        registry, reconciliation, role
    )
    reconciliation_by_id = {row["id"]: row for row in reconciliation_rows}
    presentation_descriptor: dict[str, Any] | None = None
    inverse_replay: dict[str, Any] | None = None
    if presentation_mapping is not None and classical_decision_ledger is not None:
        (
            presentation_descriptor,
            mapped_rows,
            expected_decision,
            expected_generator,
        ) = load_presentation_mapping(registry, presentation_mapping, reconciliation_rows)
        generator_descriptor, _ = registry.capture_canonical(
            "build/materialize_classical_notation.py",
            "Classical presentation generator",
            required_prefix="build/",
        )
        if not _descriptor_equal(generator_descriptor, expected_generator):
            raise AggregateError("Classical mapping generator identity changed")
        inverse_replay = replay_classical_inverse(
            registry,
            classical_decision_ledger,
            expected_decision,
            generator_descriptor,
            mapped_rows,
            aggregator_descriptor,
        )
        compiled_rows = mapped_rows
    else:
        compiled_rows = [
            {
                "id": row["id"],
                "source_path": row["source_path"],
                "authoritative": row["authoritative"],
                "compiled": row["authoritative"],
            }
            for row in reconciliation_rows
        ]
    compiled_by_id = {row["id"]: row["compiled"] for row in compiled_rows}

    reader_graph_descriptor, reader_units, reader_dependencies = load_graph(
        registry,
        reader_graph,
        role=role,
        partition="reader",
        expected_ids=READER_IDS,
        master=descriptors["reader_master"],
        wrapper=descriptors["reader_wrapper"],
        reconciliation_descriptor=reconciliation_descriptor,
        reconciliation_by_id=reconciliation_by_id,
        compiled_by_id=compiled_by_id,
        presentation_mapping=presentation_descriptor,
    )
    closure_graph_descriptor, closure_units, closure_dependencies = load_graph(
        registry,
        closure_graph,
        role=role,
        partition="closure",
        expected_ids=CLOSURE_IDS,
        master=descriptors["closure_master"],
        wrapper=descriptors["closure_wrapper"],
        reconciliation_descriptor=reconciliation_descriptor,
        reconciliation_by_id=reconciliation_by_id,
        compiled_by_id=compiled_by_id,
        presentation_mapping=presentation_descriptor,
    )
    graph_units = reader_units + closure_units
    if len({row["descriptor"]["path"] for row in graph_units}) != 722:
        raise AggregateError("verified graph union must contain 722 distinct body paths")

    identity = {
        "role": role,
        "profile": config["profile"],
        "aggregator": aggregator_descriptor,
        "assembler": descriptors["assembler"],
        "assembler_implementation_closure": assembly_implementation_closure,
        "rtl_link_repair": rtl_link_repair,
        "rtl_link_repair_implementation_closure": rtl_link_repair_closure,
        "reader_master": descriptors["reader_master"],
        "reader_wrapper": descriptors["reader_wrapper"],
        "closure_master": descriptors["closure_master"],
        "closure_wrapper": descriptors["closure_wrapper"],
        "reconciliation": reconciliation_descriptor,
        "reader_graph": reader_graph_descriptor,
        "closure_graph": closure_graph_descriptor,
        "presentation_mapping": presentation_descriptor,
    }
    aggregate = bytearray(
        _header(
            role,
            identity,
            descriptors["assembler"]["path"],
            rtl_link_repair["path"],
        )
    )
    component_ranges: dict[str, dict[str, int]] = {}

    def embed_component(
        descriptor: Mapping[str, Any], kind: str, identifier: str
    ) -> dict[str, int]:
        prior = component_ranges.get(descriptor["path"])
        if prior is not None:
            return prior
        span = _append_block(
            aggregate,
            kind=kind,
            identifier=identifier,
            descriptor=descriptor,
            data=registry.data_for(descriptor),
        )
        component_ranges[descriptor["path"]] = span
        return span

    reader_wrapper_range = embed_component(
        descriptors["reader_wrapper"], "reader-entrypoint-wrapper", "WRAPPER-READER-642"
    )
    reader_master_range = embed_component(
        descriptors["reader_master"], "reader-master-642", "MASTER-READER-642"
    )
    closure_wrapper_range = embed_component(
        descriptors["closure_wrapper"], "closure-entrypoint-wrapper", "WRAPPER-CLOSURE-80"
    )
    closure_master_range = embed_component(
        descriptors["closure_master"], "closure-master-80", "MASTER-CLOSURE-80"
    )

    bodies: list[dict[str, Any]] = []
    compiled_rows_by_id = {row["id"]: row for row in compiled_rows}
    for index, graph_row in enumerate(graph_units):
        identifier = graph_row["id"]
        partition = "reader" if index < 642 else "closure"
        mapping = compiled_rows_by_id[identifier]
        descriptor = graph_row["descriptor"]
        span = _append_block(
            aggregate,
            kind=f"{partition}-body",
            identifier=identifier,
            descriptor=descriptor,
            data=registry.data_for(descriptor),
        )
        bodies.append(
            {
                "id": identifier,
                "partition": partition,
                "reconciliation_source_path": mapping["source_path"],
                "graph_source_path": graph_row["source_path"],
                "compiled": descriptor,
                "authoritative": mapping["authoritative"],
                "compiled_bytes_equal_authoritative": (
                    _byte_identity_equal(descriptor, mapping["authoritative"])
                    and registry.data_for(descriptor)
                    == registry.data_for(mapping["authoritative"])
                ),
                "aggregate_byte_range": span,
            }
        )
    aggregate.extend(
        (
            MARKER_TEXT
            + "END "
            + json.dumps(
                {
                    "blocks": 722 + len(component_ranges),
                    "closure_units": 80,
                    "reader_units": 642,
                },
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        ).encode("ascii")
    )
    aggregate_bytes = bytes(aggregate)
    aggregate_descriptor = {
        "file": output.name,
        "bytes": len(aggregate_bytes),
        "sha256": sha256_bytes(aggregate_bytes),
        "encoding": "UTF-8",
        "format": "deterministic raw-byte archival TeX aggregate",
    }
    assembly_arguments = [
        "--reader",
        "<reader-component-rtl-links.pdf>",
        "--closure",
        "<closure-component-rtl-links.pdf>",
        "--output",
        "<complete-722.pdf>",
        "--receipt",
        "<pdf-assembly-receipt.json>",
    ]
    if config["assembler_profile_argument"] is not None:
        assembly_arguments += ["--profile", config["assembler_profile_argument"]]
    reader_repair_arguments = [
        "--input",
        "<reader-component-raw.pdf>",
        "--output",
        "<reader-component-rtl-links.pdf>",
        "--receipt",
        "<reader-rtl-link-repair-receipt.json>",
    ]
    closure_repair_arguments = [
        "--input",
        "<closure-component-raw.pdf>",
        "--output",
        "<closure-component-rtl-links.pdf>",
        "--receipt",
        "<closure-rtl-link-repair-receipt.json>",
    ]

    receipt_payload: dict[str, Any] = {
        "schema": RECEIPT_SCHEMA,
        "status": "PASS",
        "role": role,
        "profile": config["profile"],
        "ai_provenance": {
            "agent": AI_AGENT,
            "model": AI_MODEL,
            "effort": AI_EFFORT,
            "stable_disclosure": AI_DISCLOSURE,
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
                + f"أنشأ {AI_DISCLOSURE} هذا الملف التجميعي وإيصال التحقق "
                "وإعادة الإنتاج؛ والعمل المنجز هو تجميع مصادر لاتخ والتحقق "
                "الحتمي من الهوية والترتيب والتغطية والتجزئة، ولا يُدَّعى "
                "إجراء مراجعة بشرية."
            ),
        },
        "aggregate": aggregate_descriptor,
        "authorities": {
            "aggregator": aggregator_descriptor,
            "rtl_link_repair": rtl_link_repair,
            "rtl_link_repair_implementation_closure": rtl_link_repair_closure,
            "assembler_implementation_closure": assembly_implementation_closure,
            "reconciliation": reconciliation_descriptor,
            "reader_graph": reader_graph_descriptor,
            "closure_graph": closure_graph_descriptor,
            "classical_presentation_mapping": presentation_descriptor,
            "classical_inverse_replay": inverse_replay,
        },
        "masters": {
            "reader_642": {
                "master": {
                    **descriptors["reader_master"],
                    "aggregate_byte_range": reader_master_range,
                },
                "entrypoint_wrapper": {
                    **descriptors["reader_wrapper"],
                    "aggregate_byte_range": reader_wrapper_range,
                },
            },
            "closure_80": {
                "master": {
                    **descriptors["closure_master"],
                    "aggregate_byte_range": closure_master_range,
                },
                "entrypoint_wrapper": {
                    **descriptors["closure_wrapper"],
                    "aggregate_byte_range": closure_wrapper_range,
                },
            },
        },
        "coverage": {
            "expected_ids": {"first": "OLP-0001", "last": "OLP-0722"},
            "reader_units": 642,
            "closure_units": 80,
            "total_units": 722,
            "partition_overlap": 0,
            "compiled_body_paths": 722,
        },
        "bodies": bodies,
        "authoritative_lineage": {
            "field": config["source_field"],
            "compiled_tree": config["compiled_prefix"],
            "authoritative_tree": config.get(
                "authoritative_prefix", config["compiled_prefix"]
            ),
            "classical_mapping_separately_bound": presentation_descriptor is not None,
        },
        "reconstruction": {
            "route": (
                "two-independent-TeX-jobs-each-rtl-link-repaired-then-"
                "pypdf-assembly"
            ),
            "one_pass_tex_master_claimed": False,
            "aggregate_alone_claimed_byte_identical_to_pdf": False,
            "tex": {
                "engine": "LuaLaTeX",
                "executable": "lualatex",
                "options": list(TEX_OPTIONS),
                "bibliography_tool": "bibtex",
                "guarded_build_driver": build_driver,
                "guarded_inner_build": build_inner,
                "component_jobs": [
                    {
                        "order": 1,
                        "component": "canonical-reader",
                        "units": 642,
                        "master": descriptors["reader_master"],
                        "entrypoint_wrapper": descriptors["reader_wrapper"],
                        "pass_contract": config["reader_passes"],
                        "raw_pdf": "<reader-component-raw.pdf>",
                    },
                    {
                        "order": 3,
                        "component": "closure-supplement",
                        "units": 80,
                        "master": descriptors["closure_master"],
                        "entrypoint_wrapper": descriptors["closure_wrapper"],
                        "pass_contract": config["closure_passes"],
                        "raw_pdf": "<closure-component-raw.pdf>",
                    },
                ],
                "dependency_closures": {
                    "reader": {
                        "graph": reader_graph_descriptor,
                        "files": reader_dependencies,
                    },
                    "closure": {
                        "graph": closure_graph_descriptor,
                        "files": closure_dependencies,
                    },
                },
            },
            "rtl_link_repair": {
                "mandatory_per_component": True,
                "implementation": "Python/pypdf",
                "script": rtl_link_repair,
                "implementation_closure": rtl_link_repair_closure,
                "invocations": [
                    {
                        "order": 2,
                        "component": "canonical-reader",
                        "arguments": reader_repair_arguments,
                    },
                    {
                        "order": 4,
                        "component": "closure-supplement",
                        "arguments": closure_repair_arguments,
                    },
                ],
            },
            "assembly": {
                "order": 5,
                "implementation": "Python/pypdf",
                "script": descriptors["assembler"],
                "implementation_closure": assembly_implementation_closure,
                "arguments": assembly_arguments,
                "profile_argument": config["assembler_profile_argument"],
            },
            "execution_order": [
                {"order": 1, "stage": "LuaLaTeX/BibTeX", "component": "canonical-reader"},
                {"order": 2, "stage": "RTL-link-rectangle-repair", "component": "canonical-reader"},
                {"order": 3, "stage": "LuaLaTeX/BibTeX", "component": "closure-supplement"},
                {"order": 4, "stage": "RTL-link-rectangle-repair", "component": "closure-supplement"},
                {"order": 5, "stage": "Python/pypdf-assembly", "component": "complete-722"},
            ],
        },
        "checks": {
            "ordered_ids_exact": True,
            "id_reconciliation_graph_paths_exact": True,
            "reader_partition_exact": True,
            "closure_partition_exact": True,
            "partitions_disjoint": True,
            "partition_union_exact": True,
            "explicit_graph_order_used": True,
            "directory_sort_used": False,
            "captured_bytes_match_inventories": True,
            "native_file_identity_captured": True,
            "all_input_native_link_counts_one": True,
            "cross_path_native_identity_aliases": 0,
            "distinct_body_paths": True,
            "resolved_role_tree_enforced": True,
            "path_escape_count": 0,
            "role_leakage_count": 0,
            "marker_collision_count": 0,
            "missing_units": 0,
            "extra_units": 0,
            "duplicate_units": 0,
            "host_absolute_paths_recorded": False,
        },
        "pair_commit": {
            "method": (
                "exclusive temporary creation, no-replace hard-link pair, and "
                "ownership-pinned Windows handle disposition plus simultaneous "
                "non-write/non-delete-share final handles"
            ),
            "foreign_target_overwrite_allowed": False,
            "rollback_only_if_owned_file_id_and_expected_bytes": True,
            "path_check_then_unlink_used": False,
            "foreign_replacement_can_be_deleted": False,
            "final_pair_handles_held_simultaneously": True,
            "final_reads_use_identity_pinned_handles_only": True,
            "final_handles_share_read_only": True,
            "final_receipt_readback": (
                "The pair survives only after simultaneous identity-pinned final "
                "handles read the receipt and aggregate exactly as the generated "
                "canonical bytes while writes and deletion remain unshared."
            ),
        },
        "determinism": {
            "wall_clock_recorded": False,
            "path_order": "explicit reader graph followed by explicit closure graph",
            "json": "UTF-8, sorted keys, compact separators, LF terminator",
            "aggregate_delimiters": BLOCK_MARKER.decode("ascii"),
        },
        "failures": [],
    }
    receipt_core_hash = sha256_bytes(canonical_json_bytes(receipt_payload))
    receipt_payload["receipt_integrity"] = {
        "canonical_payload_without_this_field_sha256": receipt_core_hash,
        "final_readback_comparison": (
            "exact byte equality through simultaneous identity-pinned handles"
        ),
        "surviving_receipt_implies_pair_readback_passed": True,
    }
    receipt_bytes = canonical_json_bytes(receipt_payload)

    def precommit() -> None:
        if _before_precommit_recheck is not None:
            _before_precommit_recheck()
        registry.recheck_all()

    readback = _commit_pair_exclusive(
        output,
        aggregate_bytes,
        receipt,
        receipt_bytes,
        precommit,
        _before_owned_handle_delete,
        _final_readback_hook,
    )
    if readback["aggregate"]["sha256"] != aggregate_descriptor["sha256"]:
        raise AggregateError("committed aggregate identity changed after readback")
    return receipt_payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Create a truthful 722-unit archival TeX aggregate from explicit "
            "verified reader and closure graph inventories."
        )
    )
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--role", choices=tuple(ROLE_CONFIG), required=True)
    parser.add_argument("--reader-master", type=Path, required=True)
    parser.add_argument("--closure-master", type=Path, required=True)
    parser.add_argument("--reader-wrapper", type=Path, required=True)
    parser.add_argument("--closure-wrapper", type=Path, required=True)
    parser.add_argument("--reader-graph", type=Path, required=True)
    parser.add_argument("--closure-graph", type=Path, required=True)
    parser.add_argument("--reconciliation", type=Path, required=True)
    parser.add_argument("--presentation-mapping", type=Path)
    parser.add_argument("--classical-decision-ledger", type=Path)
    parser.add_argument("--assembler", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = assemble(
            repo=args.repo,
            role=args.role,
            reader_master=args.reader_master,
            closure_master=args.closure_master,
            reader_wrapper=args.reader_wrapper,
            closure_wrapper=args.closure_wrapper,
            reader_graph=args.reader_graph,
            closure_graph=args.closure_graph,
            reconciliation=args.reconciliation,
            presentation_mapping=args.presentation_mapping,
            classical_decision_ledger=args.classical_decision_ledger,
            assembler=args.assembler,
            output=args.output,
            receipt=args.receipt,
        )
    except (AggregateError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result["aggregate"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
