"""Exact, read-only admission of the already repaired shared configuration.

There are four executable Lang-argument edits and one explanatory comment
edit.  Newline changes are part of the five exact byte spans, not normalized
away.  The three implicit math carriers are not modified by this successor.
"""

from __future__ import annotations

import hashlib
from typing import Any


HISTORICAL_SHA256 = "ab19be71b50b415738603290317b504d9fa6b82850fe640d585c62db1540ced3"
CURRENT_SHA256 = "c20b63c3dc3aa97e56ce0e87dc6b3fbd303390449ab7ee8f93c7b922a35efa6b"
HISTORICAL_BYTES = 52113
CURRENT_BYTES = 52261

# (label, historical line, current line, historical offset, current offset,
#  exact historical bytes, exact current bytes). Offsets are zero based.
EXACT_EDITS = (
    ("explanatory-comment", 1167, 1167, 35086, 35086,
     b"% - `\\Trm[L]`: the set of terms (of a language)\r\n",
     b"% - `\\Trm[L]`: the set of terms (of a language)\n"
     b"% Pass the whole optional value to Lang. It may contain a compound identifier\n"
     b"% (including a typed Arabic label), not just one unexpanded TeX token.\n"),
    ("Trm-optional-language", 1172, 1174, 35225, 35373,
     b"        { \\mathrm{Trm}({\\Lang #1}) }\r\n",
     b"        { \\mathrm{Trm}({\\Lang{#1}}) }\n"),
    ("Frm-optional-language", 1179, 1181, 35408, 35556,
     b"        { \\mathrm{Frm}({\\Lang #1}) }\r\n",
     b"        { \\mathrm{Frm}({\\Lang{#1}}) }\n"),
    ("TrmSOL-optional-language", 1187, 1189, 35609, 35757,
     b"        { \\mathrm{Trm}^2({\\Lang #1}) }\r\n",
     b"        { \\mathrm{Trm}^2({\\Lang{#1}}) }\n"),
    ("FrmSOL-optional-language", 1194, 1196, 35813, 35961,
     b"        { \\mathrm{Frm}^2({\\Lang #1}) }\r\n",
     b"        { \\mathrm{Frm}^2({\\Lang{#1}}) }\n"),
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _replace_exact(raw: bytes, *, inverse: bool) -> bytes:
    """Replace only declared, uniquely attested spans at fixed byte offsets."""
    parts: list[bytes] = []
    cursor = 0
    for label, old_line, new_line, old_start, new_start, before, after in EXACT_EDITS:
        start, old, new, line = ((new_start, after, before, new_line) if inverse
                                 else (old_start, before, after, old_line))
        _require(start >= cursor and raw[start:start + len(old)] == old,
                 f"configuration successor exact span changed: {label}")
        _require(raw.count(old) == 1 and raw[:start].count(b"\n") + 1 == line,
                 f"configuration successor span is ambiguous or relocated: {label}")
        parts.extend((raw[cursor:start], new))
        cursor = start + len(old)
    parts.append(raw[cursor:])
    return b"".join(parts)


def validate_successor(raw: bytes) -> tuple[bytes, dict[str, Any]]:
    """Require current bytes and independently prove their exact predecessor.

    A historical configuration alone is not the current production profile.
    Returning reconstructed historical bytes lets the consumer check its three
    consulted definitions and line numbers in *both* identities.
    """
    _require(len(raw) == CURRENT_BYTES and hashlib.sha256(raw).hexdigest() == CURRENT_SHA256,
             "implicit math-carrier configuration identity changed")
    historical = _replace_exact(raw, inverse=True)
    _require(len(historical) == HISTORICAL_BYTES and
             hashlib.sha256(historical).hexdigest() == HISTORICAL_SHA256,
             "configuration successor does not reconstruct the pinned historical identity")
    _require(_replace_exact(historical, inverse=False) == raw,
             "configuration successor exact forward replay failed")
    return historical, {
        "schema": "openlogic-implicit-carrier-configuration-successor-v1",
        "status": "PASS_EXACT_SUCCESSOR",
        "historical": {"bytes": HISTORICAL_BYTES, "sha256": HISTORICAL_SHA256},
        "current": {"bytes": CURRENT_BYTES, "sha256": CURRENT_SHA256},
        "executable_body_edits": 4,
        "comment_block_edits": 1,
        "exact_inverse_and_forward_replay": True,
        "other_bytes_unchanged": True,
        "edits": [
            {
                "id": label,
                "historical_line_start": old_line,
                "current_line_start": new_line,
                "historical_byte_start": old_start,
                "current_byte_start": new_start,
                "historical_utf8": before.decode("utf-8"),
                "current_utf8": after.decode("utf-8"),
            }
            for label, old_line, new_line, old_start, new_start, before, after in EXACT_EDITS
        ],
    }
