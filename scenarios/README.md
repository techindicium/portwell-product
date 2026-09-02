# Scenarios

A scenario is one case the track's system is expected to handle, written so that it can be run
and its outcome compared against a stated expectation. Scenarios are the unit the Module 4
evaluation set is built from, but they are useful from Module 1 because a lifecycle nothing can
run a case through is a diagram.

```text
scenarios/
  visible/    cases the track can see, run, and add to
  heldout/    supplied by the teaching team in Module 4, never present before then
```

`scenarios/heldout/` is refused by `scripts/hooks/guard_paths.py` and denied in
`.claude/settings.json`. Both are deliberate: the directory is protected before it exists so
that the protection is not something the teaching team has to remember to add later.

## Families

Every scenario declares one family. A useful evaluation set has all five.

| Family | Asks |
| :- | :- |
| `normal` | Does the ordinary case complete with its evidence intact? |
| `boundary` | What happens at the threshold, the empty set, the first record, the tier edge? |
| `adversarial` | What happens when the input is shaped to produce a wrong confident answer? |
| `stale-context` | What happens when a superseded or expired artifact is reachable? |
| `recovery` | When it fails, does it stop, escalate, and leave the state readable? |

## Format

```yaml
id: SC-PDLC-01
family: normal
title: One line, in the imperative, naming the case
item: ACC-1001
given:
  - Facts that hold before the run, each independently checkable
when: The single action taken
expect:
  states: [intake, context, route, act, verify, approve, handoff]
  evidence: [request, context-manifest, routing-decision, verification-report, approval, handoff-note]
  refusals: []
  escalates: false
detects: What failure this case would catch that the others would not
```

`expect.refusals` lists the invariant strings a run is expected to hit. A `recovery` scenario
with an empty `refusals` list and `escalates: false` is not testing recovery.

Run them with `make scenarios`. The runner checks the scenario file's shape, not the track's
behaviour; wiring a scenario to the track's own system is group work.
