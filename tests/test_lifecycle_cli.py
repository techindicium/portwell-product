"""Tests for the deterministic state helper.

The helper is the reason state mutation is reliable, so its refusals are tested as behaviour
rather than assumed from reading it.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def project(tmp_path):
    """A throwaway copy of the repository's state surface."""
    (tmp_path / "state").mkdir()
    shutil.copy(ROOT / "state" / "state-model.json", tmp_path / "state" / "state-model.json")
    (tmp_path / "scripts").mkdir()
    shutil.copy(ROOT / "scripts" / "lifecycle.py", tmp_path / "scripts" / "lifecycle.py")
    (tmp_path / "evidence").mkdir()
    return tmp_path


def run(project, *args):
    return subprocess.run(
        [sys.executable, str(project / "scripts" / "lifecycle.py"), *args],
        capture_output=True,
        text=True,
        cwd=project,
        env={"CLAUDE_PROJECT_DIR": str(project), "PATH": "/usr/bin:/bin"},
    )


def evidence(project, name, content="recorded for the test"):
    path = project / "evidence" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return f"evidence/{name}"


def advance(project, item, to, ev=None, actor="agent"):
    args = ["advance", "--item", item, "--to", to, "--actor", actor]
    if ev:
        args += ["--evidence", ev]
    return run(project, *args)


def test_an_item_enters_at_the_entry_state(project):
    result = advance(project, "IT-1", "intake", evidence(project, "IT-1/request.md"))
    assert result.returncode == 0, result.stderr
    assert "(new) -> intake" in result.stdout


def test_an_item_cannot_enter_mid_path(project):
    result = advance(project, "IT-1", "act", evidence(project, "IT-1/attempt-trace.md"))
    assert result.returncode == 1
    assert "can only enter at 'intake'" in result.stderr


def test_an_undeclared_transition_is_refused(project):
    advance(project, "IT-1", "intake", evidence(project, "IT-1/request.md"))
    result = advance(project, "IT-1", "handoff", evidence(project, "IT-1/handoff-note.md"))
    assert result.returncode == 1
    assert "is not a declared transition" in result.stderr
    assert "the model allows" in result.stderr


def test_a_refusal_names_the_invariant_and_the_recovery(project):
    result = advance(project, "IT-1", "verify", evidence(project, "IT-1/verification-report.md"))
    assert "REFUSED:" in result.stderr
    assert "what happened:" in result.stderr
    assert "to recover:" in result.stderr


def test_missing_evidence_is_refused(project):
    result = advance(project, "IT-1", "intake")
    assert result.returncode == 1
    assert "requires evidence" in result.stderr


def test_evidence_that_does_not_exist_is_refused(project):
    result = advance(project, "IT-1", "intake", "evidence/IT-1/request.md")
    assert result.returncode == 1
    assert "does not exist" in result.stderr


def test_empty_evidence_is_refused(project):
    path = project / "evidence" / "IT-1"
    path.mkdir(parents=True)
    (path / "request.md").write_text("")
    result = advance(project, "IT-1", "intake", "evidence/IT-1/request.md")
    assert result.returncode == 1
    assert "is empty" in result.stderr


def test_evidence_outside_the_repository_is_refused(project):
    result = advance(project, "IT-1", "intake", "../escaped.md")
    assert result.returncode == 1
    assert "outside the project directory" in result.stderr


def test_the_correction_budget_is_enforced(project):
    for state, name in [
        ("intake", "request.md"),
        ("context", "context-manifest.md"),
        ("route", "routing-decision.md"),
        ("act", "attempt-trace.md"),
    ]:
        assert advance(project, "IT-1", state, evidence(project, f"IT-1/{name}")).returncode == 0

    verify_ev = evidence(project, "IT-1/verification-report.md")
    act_ev = evidence(project, "IT-1/attempt-trace.md")
    for _ in range(3):
        assert advance(project, "IT-1", "verify", verify_ev).returncode == 0
        assert advance(project, "IT-1", "act", act_ev).returncode == 0

    assert advance(project, "IT-1", "verify", verify_ev).returncode == 0
    fourth = advance(project, "IT-1", "act", act_ev)
    assert fourth.returncode == 1
    assert "the limit is 3" in fourth.stderr
    assert "escalated" in fourth.stderr


def test_repeated_blocking_escalates(project):
    advance(project, "IT-1", "intake", evidence(project, "IT-1/request.md"))
    blocker = evidence(project, "IT-1/blocker.md")
    assert advance(project, "IT-1", "blocked", blocker).returncode == 0
    assert advance(project, "IT-1", "context", evidence(project, "IT-1/context-manifest.md")).returncode == 0
    assert advance(project, "IT-1", "blocked", blocker).returncode == 0
    assert advance(project, "IT-1", "context", evidence(project, "IT-1/context-manifest.md")).returncode == 0
    third = advance(project, "IT-1", "blocked", blocker)
    assert third.returncode == 1
    assert "escalates to a human" in third.stderr


def test_the_log_is_append_only_and_ordered(project):
    advance(project, "IT-1", "intake", evidence(project, "IT-1/request.md"))
    advance(project, "IT-1", "context", evidence(project, "IT-1/context-manifest.md"))
    lines = (project / "state" / "lifecycle.jsonl").read_text().strip().splitlines()
    assert len(lines) == 2
    first, second = (json.loads(line) for line in lines)
    assert first["from"] is None and first["to"] == "intake"
    assert second["from"] == "intake" and second["to"] == "context"


def test_validate_accepts_a_log_the_cli_wrote(project):
    advance(project, "IT-1", "intake", evidence(project, "IT-1/request.md"))
    advance(project, "IT-2", "intake", evidence(project, "IT-2/request.md"))
    result = run(project, "validate")
    assert result.returncode == 0, result.stderr
    assert "2 transitions across 2 items" in result.stdout


def test_validate_rejects_a_hand_edited_log(project):
    advance(project, "IT-1", "intake", evidence(project, "IT-1/request.md"))
    log = project / "state" / "lifecycle.jsonl"
    log.write_text(log.read_text() + json.dumps(
        {"at": "2026-09-02T10:00:00Z", "item": "IT-1", "from": "intake", "to": "handoff", "actor": "human"}
    ) + "\n")
    result = run(project, "validate")
    assert result.returncode == 1
    assert "is not a declared transition" in result.stderr


def test_validate_rejects_a_forged_from_field(project):
    advance(project, "IT-1", "intake", evidence(project, "IT-1/request.md"))
    log = project / "state" / "lifecycle.jsonl"
    log.write_text(log.read_text() + json.dumps(
        {"at": "2026-09-02T10:00:00Z", "item": "IT-1", "from": "approve", "to": "handoff", "actor": "human"}
    ) + "\n")
    result = run(project, "validate")
    assert result.returncode == 1
    assert "but the log leaves it at 'intake'" in result.stderr


def test_validate_rejects_unparseable_lines(project):
    log = project / "state" / "lifecycle.jsonl"
    log.write_text("this is not json\n")
    result = run(project, "validate")
    assert result.returncode == 1
    assert "is not valid JSON" in result.stderr


def test_show_reports_the_current_state(project):
    advance(project, "IT-1", "intake", evidence(project, "IT-1/request.md"))
    result = run(project, "show", "--item", "IT-1")
    assert result.returncode == 0
    assert "currently intake after 1 transitions" in result.stdout


def test_show_is_quiet_about_an_unknown_item(project):
    result = run(project, "show", "--item", "NOPE")
    assert result.returncode == 0
    assert "no history" in result.stdout
