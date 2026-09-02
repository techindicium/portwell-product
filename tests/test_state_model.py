"""The state model is a reviewed artifact, so it has tests of its own.

These fail loudly when a group edits state/state-model.json in a way that breaks the
guarantees the rest of the repository depends on.
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MODEL = json.loads((ROOT / "state" / "state-model.json").read_text())


def test_every_path_state_is_declared():
    for state in MODEL["path"]:
        assert state in MODEL["states"], f"path state '{state}' is not declared"


def test_every_transition_endpoint_is_declared():
    for frm, targets in MODEL["transitions"].items():
        assert frm in MODEL["states"], f"transition source '{frm}' is not a declared state"
        for to in targets:
            assert to in MODEL["states"], f"'{frm}' -> '{to}' targets an undeclared state"


def test_every_state_has_a_transition_entry():
    for state in MODEL["states"]:
        assert state in MODEL["transitions"], f"state '{state}' has no transition entry"


def test_terminal_states_have_no_outgoing_transitions():
    for state, spec in MODEL["states"].items():
        if spec["kind"] == "terminal":
            assert MODEL["transitions"][state] == [], f"terminal state '{state}' has outgoing transitions"


def test_failure_states_survive():
    """A lifecycle with only a happy path is the failure this course is about."""
    kinds = {spec["kind"] for spec in MODEL["states"].values()}
    assert "failure" in kinds, "the state model has no failure states left"
    assert any(
        spec["kind"] == "failure" for name, spec in MODEL["states"].items() if name == "escalated"
    ), "'escalated' must remain a failure state; stop conditions depend on it"


def test_every_state_declares_evidence():
    for state, spec in MODEL["states"].items():
        assert spec.get("evidence"), f"state '{state}' requires no evidence, so advancing to it proves nothing"


def test_correction_loop_is_bounded():
    limits = MODEL["limits"]
    assert limits["max_correction_attempts"] >= 1
    assert limits["max_correction_attempts"] <= 10, "an effectively unbounded correction loop is not a budget"
    assert "act" in MODEL["transitions"]["verify"], "verify must be able to return to act for corrections"


def test_every_state_is_reachable_from_the_entry_state():
    entry = MODEL["path"][0]
    seen = {entry}
    frontier = [entry]
    while frontier:
        for target in MODEL["transitions"][frontier.pop()]:
            if target not in seen:
                seen.add(target)
                frontier.append(target)
    unreachable = set(MODEL["states"]) - seen
    assert not unreachable, f"unreachable states: {sorted(unreachable)}"


@pytest.mark.parametrize("state", ["blocked", "escalated"])
def test_failure_states_have_a_way_out(state):
    assert MODEL["transitions"][state], f"'{state}' is a dead end, so a run entering it cannot recover"


def test_the_end_of_the_happy_path_can_reach_a_terminal_state():
    """Handing off is not the end. An artifact that can never be retired is a liability."""
    last = MODEL["path"][-1]
    reachable = MODEL["transitions"][last]
    terminals = {n for n, s in MODEL["states"].items() if s["kind"] == "terminal"}
    assert terminals & set(reachable), f"'{last}' cannot reach any terminal state"
