# Context contract, PDLC track

Module 2 asks for a context contract separating required, optional, prohibited, and refreshable
context. This file is where the track's version lives. The worked example in
`skills/lifecycle-trace/SKILL.md` shows the shape for one procedure; this file is the
repository-wide default.

| Class | Means | Consequence of getting it wrong |
| :- | :- | :- |
| Required | The run cannot make a correct decision without it | Wrong decision, confidently made |
| Optional | Improves the result where cheap, safe to omit | Cost with no benefit |
| Prohibited | Must never enter the context | Leak, or an evaluation invalidated |
| Refreshable | Changes during the run, so it is re-read rather than remembered | Decisions made against a state that has moved |

## Repository default

| Class | Content |
| :- | :- |
| Required | `README.md` invariants, `docs/architecture-rules.md`, the item's own request |
| Optional | Comparable prior items, `docs/policies.md` entries for the item's area |
| Prohibited | `scenarios/heldout/`, anything under `.env`, real customer data |
| Refreshable | `state/lifecycle.jsonl`, the working tree, check results |

<!-- TRACK SEED: groups extend this table with the track's domain context and state, for each
     class, and record what happens when a class is violated. -->

## The test that matters

For each row in Prohibited, name how it is prevented, not how it is discouraged. Two of the
four in the default table are prevented by `.claude/settings.json` and the guard hook. The
others are currently prose, and that gap is a legitimate Module 3 target.
