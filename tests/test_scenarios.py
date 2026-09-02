"""Scenario files are checked for shape so a broken case fails at check time, not run time."""

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
VISIBLE = sorted((ROOT / "scenarios" / "visible").glob("*.yaml"))
FAMILIES = {"normal", "boundary", "adversarial", "stale-context", "recovery"}
REQUIRED = {"id", "family", "title", "given", "when", "expect", "detects"}


def test_there_is_at_least_one_visible_scenario():
    assert VISIBLE, "scenarios/visible/ is empty, so the track has nothing it can run"


@pytest.mark.parametrize("path", VISIBLE, ids=lambda p: p.name)
def test_scenario_has_the_required_fields(path):
    data = yaml.safe_load(path.read_text())
    missing = REQUIRED - set(data)
    assert not missing, f"{path.name} is missing {sorted(missing)}"


@pytest.mark.parametrize("path", VISIBLE, ids=lambda p: p.name)
def test_family_is_declared_and_known(path):
    data = yaml.safe_load(path.read_text())
    assert data["family"] in FAMILIES, f"{path.name} declares unknown family '{data['family']}'"


@pytest.mark.parametrize("path", VISIBLE, ids=lambda p: p.name)
def test_expectation_block_is_complete(path):
    expect = yaml.safe_load(path.read_text())["expect"]
    for key in ("states", "evidence", "refusals", "escalates"):
        assert key in expect, f"{path.name} expect block is missing '{key}'"
    assert isinstance(expect["escalates"], bool), f"{path.name} expect.escalates must be a boolean"


@pytest.mark.parametrize("path", VISIBLE, ids=lambda p: p.name)
def test_recovery_scenarios_actually_test_recovery(path):
    data = yaml.safe_load(path.read_text())
    if data["family"] != "recovery":
        pytest.skip("not a recovery scenario")
    expect = data["expect"]
    assert expect["refusals"] or expect["escalates"], (
        f"{path.name} claims to be a recovery case but expects no refusal and no escalation"
    )


@pytest.mark.parametrize("path", VISIBLE, ids=lambda p: p.name)
def test_ids_match_filenames(path):
    data = yaml.safe_load(path.read_text())
    assert data["id"] == path.stem, f"{path.name} declares id '{data['id']}'"


def test_ids_are_unique():
    ids = [yaml.safe_load(p.read_text())["id"] for p in VISIBLE]
    assert len(ids) == len(set(ids)), "duplicate scenario ids"


def test_the_heldout_directory_is_not_present():
    """Held-out cases arrive in Module 4. Their presence before then is a leak."""
    heldout = ROOT / "scenarios" / "heldout"
    if heldout.exists():
        assert not any(heldout.iterdir()), "scenarios/heldout/ has content before Module 4"
