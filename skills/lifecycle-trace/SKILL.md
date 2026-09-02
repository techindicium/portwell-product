---
name: lifecycle-trace
description: Trace one PDLC work item through the common delivery path, recording state and evidence at each stage. Use when an item enters the track, when it needs to advance, or when a reviewer asks where an item stands and why.
---

# Lifecycle trace

This is the one skill the shell ships with. It exists as a worked example of the shape a
lifecycle procedure takes in this repository: a named procedure, a bounded context contract, a
deterministic helper doing the state mutation, and a refusal path. Groups add their own skills
alongside it and are free to replace this one once theirs is better.

## Context contract

| Class | Content |
| :- | :- |
| Required | `state/state-model.json`, the item's own request or source artifact, `docs/architecture-rules.md` |
| Optional | Sibling items in the same product area, the relevant entry in `docs/policies.md` |
| Prohibited | `scenarios/heldout/` in any form, credentials, raw customer data outside `fixtures/` |
| Refreshable | The lifecycle log, which changes during the run and is re-read rather than remembered |

Load the required set. Do not load the whole repository: the routing decision below depends on
a small number of facts, and a large context makes it harder to see which fact drove it.

## Procedure

1. **Intake.** Confirm the item has an identifier that matches the scheme in
   `docs/identifiers.md`. Write the request to `evidence/<item>/request.md`, stating the asked-for
   outcome, the constraints, and what is explicitly out of scope. Advance to `intake`.

2. **Context.** Assemble only the context the item needs. Write
   `evidence/<item>/context-manifest.md` listing every artifact loaded, where it came from, and
   how old it is. An artifact whose age matters and whose age is unknown is recorded as unknown,
   not estimated. Advance to `context`.

3. **Route.** Decide the autonomy level from four inputs: how complete the specification is,
   whether a comparable case already exists in the repository, the blast radius if the result is
   wrong, and how novel the work is. Write `evidence/<item>/routing-decision.md` with the four
   inputs, the chosen path, and the condition that would have chosen differently. Advance to
   `route`.

4. **Act.** Attempt the change. Record what was attempted, not only what succeeded, in
   `evidence/<item>/attempt-trace.md`. Advance to `act`.

5. **Verify.** Run the deterministic checks first: `make verify`. Record the result in
   `evidence/<item>/verification-report.md` whether it passed or failed. A failure returns the item
   to `act`, and the correction loop is bounded by `max_correction_attempts` in the state model.
   When that budget is exhausted, advance to `escalated` rather than trying again.

6. **Approve.** A named human or a gate accepts the result against the acceptance conditions
   written at intake. Record who and against what in `evidence/<item>/approval.md`.

7. **Handoff.** Publish the artifact with its contract. Record what a consumer needs to know,
   including anything that is now their problem, in `evidence/<item>/handoff-note.md`.

8. **Observe.** After handoff, record what was measured in `evidence/<item>/observation.md`,
   including the case where nothing was measured yet and when it will be.

## Recording a transition

State is never edited by hand. The guard in `scripts/hooks/guard_paths.py` refuses it.

```bash
python3 scripts/lifecycle.py advance \
  --item <ITEM-ID> \
  --to context \
  --evidence evidence/<ITEM-ID>/context-manifest.md \
  --actor agent \
  --note "why this advance is justified"
```

Read where an item stands with `python3 scripts/lifecycle.py show --item <ITEM-ID>`, and check
the whole log with `python3 scripts/lifecycle.py validate`.

## Stop conditions

Stop and escalate rather than continuing when any of these holds:

- The correction budget in `state/state-model.json` is exhausted.
- The item has been blocked twice.
- The work would require a write the guard refuses.
- An input the routing decision depended on turns out to be stale, superseded, or unsourced.
- The acceptance conditions cannot be evaluated with the evidence available.

## What this skill does not do

It does not decide the track's domain questions, and it does not review its own output. Those
belong to the skills and agents the groups add.
