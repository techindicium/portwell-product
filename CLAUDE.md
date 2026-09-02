# Product Development Lifecycle delivery system

You are working inside the PDLC track repository for a course on harness
engineering. The subject of the work is the delivery system in this repository, not the
fictional product it serves.

## Read before acting

`README.md` for the layout and the three invariants. `docs/architecture-rules.md` for what the
track may and may not do. `docs/policies.md` for the fixture's prose rules, several of which
are deliberately not yet enforceable.

Do not read the whole repository. `skills/lifecycle-trace/SKILL.md` carries a context contract;
follow it. Loading more than the contract requires makes it harder for a reviewer to see which
fact drove a decision, and the pull request has to show that.

## How work is recorded

Every state change goes through `python3 scripts/lifecycle.py advance`. It refuses invalid
transitions, missing evidence, and exhausted budgets, and its refusals name the invariant and
the recovery action. Read the refusal rather than working around it.

Never write `state/lifecycle.jsonl` or `state/state-model.json` directly. A hook refuses it.

## Stop conditions

Stop and say so rather than continuing when:

- `scripts/lifecycle.py` refuses a transition and the refusal is correct.
- The correction budget in `state/state-model.json` is exhausted.
- A required input is stale, superseded, or has no source. Record that as a finding; do not
  substitute a plausible value.
- Work would need a permission this project does not grant. Ask; do not route around it.

An empty field is information. Leave it empty and say why.

## Verification order

Deterministic checks first, always: `make verify`. The `verifier` agent reads evidence after
those checks have run, not instead of them. Human approval comes last and is not yours to
record on someone's behalf.

## Writing

Plain declarative prose. No em dashes. State what is true, including what failed. A green run
that hides a correction is worth less to this course than a red one that is legible.
