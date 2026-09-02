#!/usr/bin/env python3
"""Deterministic lifecycle state operations for a course track repository.

The point of this file is that state mutation is code, not prose an agent is asked to follow.
An agent advances an item by calling this CLI; the CLI refuses invalid transitions, missing
evidence, and exhausted budgets, and it appends rather than rewriting.

    python3 scripts/lifecycle.py advance --item TCK-004417 --to context \
        --evidence evidence/TCK-004417/context-manifest.md --actor agent
    python3 scripts/lifecycle.py show --item TCK-004417
    python3 scripts/lifecycle.py validate

Standard library only, deliberately: hooks run this without a virtual environment.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).resolve().parent.parent))
MODEL_PATH = ROOT / "state" / "state-model.json"
LOG_PATH = ROOT / "state" / "lifecycle.jsonl"

EXIT_OK = 0
EXIT_REFUSED = 1
EXIT_USAGE = 2


class Refused(Exception):
    """A refusal that names the invariant and the recovery action."""

    def __init__(self, invariant: str, detail: str, recover: str) -> None:
        super().__init__(detail)
        self.invariant = invariant
        self.detail = detail
        self.recover = recover

    def render(self) -> str:
        return (
            f"REFUSED: {self.invariant}\n"
            f"  what happened: {self.detail}\n"
            f"  to recover:    {self.recover}"
        )


def load_model() -> dict:
    if not MODEL_PATH.exists():
        raise Refused(
            "A track repository has a state model.",
            f"{MODEL_PATH.relative_to(ROOT)} is missing.",
            "Restore the file from the course shell before advancing any item.",
        )
    return json.loads(MODEL_PATH.read_text())


def load_log() -> list[dict]:
    if not LOG_PATH.exists():
        return []
    entries = []
    for lineno, line in enumerate(LOG_PATH.read_text().splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise Refused(
                "The lifecycle log is machine-readable at every line.",
                f"{LOG_PATH.name} line {lineno} is not valid JSON: {exc.msg}.",
                "Repair or remove that line. Never hand-edit this file; append through this CLI.",
            ) from exc
    return entries


def history(entries: list[dict], item: str) -> list[dict]:
    return [e for e in entries if e.get("item") == item]


def current_state(entries: list[dict], item: str) -> str | None:
    h = history(entries, item)
    return h[-1]["to"] if h else None


def check_transition(model: dict, frm: str | None, to: str) -> None:
    states = model["states"]
    if to not in states:
        raise Refused(
            "Every recorded state is declared in the state model.",
            f"'{to}' is not a declared state. Declared: {', '.join(sorted(states))}.",
            "Use a declared state, or add it to state/state-model.json with its evidence requirement first.",
        )
    if frm is None:
        entry = model["path"][0]
        if to != entry:
            raise Refused(
                "An item enters the lifecycle at its declared entry state.",
                f"The item has no history, so it can only enter at '{entry}', not '{to}'.",
                f"Advance the item to '{entry}' first.",
            )
        return
    allowed = model["transitions"].get(frm, [])
    if to not in allowed:
        allowed_text = ", ".join(allowed) if allowed else "nothing, it is terminal"
        raise Refused(
            "State transitions follow the declared state model.",
            f"'{frm}' -> '{to}' is not a declared transition. From '{frm}' the model allows: {allowed_text}.",
            "Either advance through a declared transition, or change state/state-model.json deliberately and say why in the pull request.",
        )


def check_budgets(model: dict, entries: list[dict], item: str, frm: str | None, to: str) -> None:
    limits = model.get("limits", {})
    h = history(entries, item)

    max_transitions = limits.get("max_transitions_per_item")
    if max_transitions and len(h) >= max_transitions:
        raise Refused(
            "An item has a bounded number of transitions.",
            f"{item} already has {len(h)} transitions, the limit is {max_transitions}.",
            "Stop autonomous work on this item and escalate to its human owner.",
        )

    max_corrections = limits.get("max_correction_attempts")
    if max_corrections and (frm, to) == ("verify", "act"):
        corrections = sum(1 for e in h if (e.get("from"), e.get("to")) == ("verify", "act"))
        if corrections >= max_corrections:
            raise Refused(
                "The correction loop is bounded, and exhaustion escalates rather than retries.",
                f"{item} has already returned from verify to act {corrections} times, the limit is {max_corrections}.",
                "Advance the item to 'escalated' with an escalation note instead of attempting another correction.",
            )

    blocked_limit = limits.get("escalate_after_blocked_transitions")
    if blocked_limit and to == "blocked":
        blocks = sum(1 for e in h if e.get("to") == "blocked")
        if blocks >= blocked_limit:
            raise Refused(
                "Repeated blocking escalates to a human.",
                f"{item} has been blocked {blocks} times, the limit is {blocked_limit}.",
                "Advance the item to 'escalated' and name the owner who has to unblock it.",
            )


def check_evidence(model: dict, to: str, evidence: str | None) -> Path | None:
    required = model["states"][to].get("evidence", [])
    if not required:
        return None
    if not evidence:
        raise Refused(
            "A state advance carries the evidence that state requires.",
            f"State '{to}' requires evidence of kind {', '.join(required)} and none was given.",
            "Write the evidence file, then pass it with --evidence <path>.",
        )
    path = (ROOT / evidence).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise Refused(
            "Evidence lives inside the repository so a reviewer can read it.",
            f"'{evidence}' resolves outside the project directory.",
            "Move the evidence file into the repository and pass a repository-relative path.",
        ) from exc
    if not path.exists():
        raise Refused(
            "Recorded evidence exists at the moment it is recorded.",
            f"'{evidence}' does not exist.",
            "Create the evidence file before advancing the item.",
        )
    if path.stat().st_size == 0:
        raise Refused(
            "Recorded evidence has content.",
            f"'{evidence}' exists but is empty.",
            "Write the evidence, then advance the item.",
        )
    return path


def cmd_advance(args: argparse.Namespace) -> int:
    model = load_model()
    entries = load_log()
    frm = current_state(entries, args.item)
    check_transition(model, frm, args.to)
    check_budgets(model, entries, args.item, frm, args.to)
    evidence = check_evidence(model, args.to, args.evidence)

    record = {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "item": args.item,
        "from": frm,
        "to": args.to,
        "actor": args.actor,
        "evidence": args.evidence,
        "note": args.note,
    }
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    where = f" evidence {evidence.relative_to(ROOT.resolve())}" if evidence else ""
    print(f"{args.item}: {frm or '(new)'} -> {args.to} by {args.actor}{where}")
    return EXIT_OK


def cmd_show(args: argparse.Namespace) -> int:
    entries = load_log()
    h = history(entries, args.item)
    if not h:
        print(f"{args.item}: no history")
        return EXIT_OK
    for e in h:
        note = f"  {e['note']}" if e.get("note") else ""
        print(f"{e['at']}  {e.get('from') or '(new)':>10} -> {e['to']:<10} {e.get('actor','?'):<8}{note}")
    print(f"{args.item}: currently {h[-1]['to']} after {len(h)} transitions")
    return EXIT_OK


def cmd_validate(args: argparse.Namespace) -> int:
    model = load_model()
    entries = load_log()
    problems: list[str] = []
    seen: dict[str, str | None] = {}
    for i, e in enumerate(entries, start=1):
        for field in ("at", "item", "to", "actor"):
            if not e.get(field):
                problems.append(f"line {i}: missing required field '{field}'")
        item = e.get("item")
        if not item:
            continue
        expected = seen.get(item)
        if e.get("from") != expected:
            problems.append(
                f"line {i}: {item} records from='{e.get('from')}' but the log leaves it at '{expected}'"
            )
        try:
            check_transition(model, expected, e.get("to", ""))
        except Refused as exc:
            problems.append(f"line {i}: {exc.detail}")
        seen[item] = e.get("to")

    if problems:
        if not args.quiet:
            print("Lifecycle log is invalid:", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        print(
            "  to recover: fix the log through this CLI, or reset the item and re-record its history.",
            file=sys.stderr,
        )
        return EXIT_REFUSED
    if not args.quiet:
        print(f"Lifecycle log is valid: {len(entries)} transitions across {len(seen)} items")
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="lifecycle.py", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_adv = sub.add_parser("advance", help="record a state transition for one item")
    p_adv.add_argument("--item", required=True)
    p_adv.add_argument("--to", required=True)
    p_adv.add_argument("--evidence")
    p_adv.add_argument("--actor", default="agent")
    p_adv.add_argument("--note")
    p_adv.set_defaults(func=cmd_advance)

    p_show = sub.add_parser("show", help="print the history of one item")
    p_show.add_argument("--item", required=True)
    p_show.set_defaults(func=cmd_show)

    p_val = sub.add_parser("validate", help="check the whole log against the state model")
    p_val.add_argument("--quiet", action="store_true")
    p_val.set_defaults(func=cmd_validate)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Refused as exc:
        print(exc.render(), file=sys.stderr)
        return EXIT_REFUSED


if __name__ == "__main__":
    sys.exit(main())
