#!/usr/bin/env python3
"""PostToolUse check: warn when the lifecycle log points at evidence that is not readable.

This is the cheap half of the verification story. It does not decide whether the evidence is
good, only whether the claim that evidence exists survives contact with the filesystem.
Exits 0 with a warning on stderr rather than blocking, because a missing evidence file is a
finding for the reviewer and not a reason to stop the run.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def main() -> int:
    try:
        json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
    log = project / "state" / "lifecycle.jsonl"
    if not log.exists():
        return 0

    missing: list[str] = []
    for lineno, line in enumerate(log.read_text().splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        evidence = record.get("evidence")
        if not evidence:
            continue
        if not (project / evidence).exists():
            missing.append(f"line {lineno}: {record.get('item')} -> {record.get('to')} cites {evidence}")

    if missing:
        print("WARNING: lifecycle evidence is not readable", file=sys.stderr)
        for entry in missing:
            print(f"  {entry}", file=sys.stderr)
        print("  to recover: restore the evidence file, or re-record the transition with a path that exists.", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
