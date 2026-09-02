"""The guard hook is the repository's regression case for Module 3.

A control without a test that fails when the control is removed is an instruction, not a
control. These tests are that failing case.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
GUARD = ROOT / "scripts" / "hooks" / "guard_paths.py"


def guard(payload):
    return subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=ROOT,
        env={"CLAUDE_PROJECT_DIR": str(ROOT), "PATH": "/usr/bin:/bin"},
    )


def write(path):
    return {"tool_name": "Write", "tool_input": {"file_path": path}}


@pytest.mark.parametrize(
    "path",
    [
        "state/lifecycle.jsonl",
        "./state/lifecycle.jsonl",
        "state/state-model.json",
        "scenarios/heldout/HO-01.yaml",
        "scenarios/heldout/nested/deeper/HO-02.yaml",
    ],
)
def test_protected_paths_are_refused(path):
    result = guard(write(path))
    assert result.returncode == 2, f"{path} was allowed"
    assert "REFUSED:" in result.stderr
    assert "to recover:" in result.stderr


@pytest.mark.parametrize(
    "path",
    [
        "skills/new-skill/SKILL.md",
        "scenarios/visible/SC-01.yaml",
        "evidence/IT-1/request.md",
        "state/notes.md",
        "docs/policies.md",
    ],
)
def test_ordinary_paths_are_allowed(path):
    result = guard(write(path))
    assert result.returncode == 0, result.stderr


def test_an_absolute_path_into_a_protected_file_is_refused():
    result = guard(write(str(ROOT / "state" / "lifecycle.jsonl")))
    assert result.returncode == 2


def test_a_path_outside_the_project_is_not_the_guards_business():
    """Permissions handle that. This guard protects specific in-repository invariants."""
    result = guard(write("/etc/hosts"))
    assert result.returncode == 0


def test_multiedit_payloads_are_inspected():
    payload = {
        "tool_name": "MultiEdit",
        "tool_input": {
            "edits": [
                {"file_path": "docs/policies.md"},
                {"file_path": "state/lifecycle.jsonl"},
            ]
        },
    }
    result = guard(payload)
    assert result.returncode == 2, "a protected path hidden among allowed edits was let through"


def test_an_unparseable_payload_does_not_block_the_run():
    result = subprocess.run(
        [sys.executable, str(GUARD)],
        input="not json at all",
        capture_output=True,
        text=True,
        cwd=ROOT,
        env={"CLAUDE_PROJECT_DIR": str(ROOT), "PATH": "/usr/bin:/bin"},
    )
    assert result.returncode == 0


def test_the_refusal_message_names_the_replacement_action():
    result = guard(write("state/lifecycle.jsonl"))
    assert "scripts/lifecycle.py advance" in result.stderr
