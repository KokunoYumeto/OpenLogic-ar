#!/usr/bin/env python3
"""Read one decision at a time from the frozen pretty-printed review index."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator


def iter_decisions(path: Path, max_record_bytes: int = 16_000_000) -> Iterator[dict]:
    """Yield records without loading the 154 MB enclosing JSON into memory.

    This index is produced with two-space JSON indentation: each top-level
    decision starts at four spaces, and no nested object can start there.
    Fail closed if that frozen layout or an individual-record cap changes.
    """
    with path.open("r", encoding="utf-8") as source:
        for line in source:
            if line == '  "decisions": [\n':
                break
        else:
            raise ValueError("Pretty-printed decisions array not found")
        block: list[str] = []
        size = 0
        count = 0
        for line in source:
            if not block:
                if line == '  ],\n':
                    if count != 1179:
                        raise ValueError(f"Unexpected frozen decision count: {count}")
                    return
                if line != '    {\n':
                    raise ValueError("Unexpected decision-object start")
            block.append(line)
            size += len(line.encode("utf-8"))
            if size > max_record_bytes:
                raise ValueError("A single decision exceeds the bounded parser limit")
            if line in ('    },\n', '    }\n'):
                payload = "".join(block).rstrip("\n")
                if payload.endswith(","):
                    payload = payload[:-1]
                record = json.loads(payload)
                if not isinstance(record, dict) or not isinstance(record.get("decision_id"), str):
                    raise ValueError("Malformed decision record")
                yield record
                count += 1
                block = []
                size = 0
        raise ValueError("Decisions array ended without its closing delimiter")
