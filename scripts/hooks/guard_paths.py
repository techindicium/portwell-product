#!/usr/bin/env python3
"""PreToolUse guard: refuse writes that would bypass a deterministic control.

Reads the Claude Code hook payload on stdin and exits non-zero with a message when a write
would land somewhere the harness protects. Two invariants, both of which exist because prose
asking an agent not to touch a file is not a control:

  1. state/lifecycle.jsonl is append-only through scripts/lifecycle.py.
  2. scenarios/heldout/ is never writable from inside the repository.

Standard library only. Hooks run outside any virtual environment.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

PROTECTED = [
    (
        Path("state/lifecycle.jsonl"),
        "Lifecycle state is append-only through the CLI.",
        "Record the transition with: python3 scripts/lifecycle.py advance --item <id> --to <state> --evidence <path>",
    ),
    (
        Path("state/state-model.json"),
        "The state model is a reviewed artifact, not an incidental edit.",
        "Change it in its own commit, state the reason in the pull request, and update tests/test_state_model.py.",
    ),
    (
        Path("scenarios/heldout"),
        "Held-out scenarios are not visible or writable to the track.",
        "Work against scenarios/visible/. Held-out cases are supplied by the teaching team in Module 4.",
    ),
]


def target_paths(payload: dict) -> list[Path]:
    tool_input = payload.get("tool_input") or {}
    candidates: list[str] = []
    for key in ("file_path", "path", "notebook_path"):
        value = tool_input.get(key)
        if isinstance(value, str):
            candidates.append(value)
    for edit in tool_input.get("edits") or []:
        if isinstance(edit, dict) and isinstance(edit.get("file_path"), str):
            candidates.append(edit["file_path"])
    return [Path(c) for c in candidates]


def relative_to_project(path: Path, project: Path) -> Path | None:
    try:
        resolved = (project / path).resolve() if not path.is_absolute() else path.resolve()
        return resolved.relative_to(project.resolve())
    except (ValueError, OSError):
        return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        # A payload we cannot parse is not a reason to block the run.
        return 0

    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()

    for raw in target_paths(payload):
        rel = relative_to_project(raw, project)
        if rel is None:
            continue
        for protected, invariant, recover in PROTECTED:
            if rel == protected or protected in rel.parents:
                print(
                    f"REFUSED: {invariant}\n"
                    f"  what happened: a write to {rel} was blocked by scripts/hooks/guard_paths.py\n"
                    f"  to recover:    {recover}",
                    file=sys.stderr,
                )
                return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
