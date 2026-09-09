# Seed manifest

**Delete this file before handover.** It describes what was placed in this repository and why,
which is teaching-team information. A group that reads it has been told where to look.

## What this repository is

Product decisions and the documents behind them. Discovery notes, decision records, experiment designs and results, and the launch material. Documents and spreadsheets, because that is what this work produces.

## What was placed here

| Path | What it is |
| :- | :- |
| `data/discovery/` | Opportunities, the expansion design, and last year's sales deck |
| `data/decisions/` | Decision records |
| `data/experiments/` | Experiment design and results |
| `data/launch/` | Readiness checklist and adoption measures |
| `data/onboarding/, data/pricing/, data/people/` | Company documents other tracks cite |
| `docs/interviews/` | How decisions happen, and what the pilot showed |

## Where the data comes from

Every seeded fixture in the mock systems is generated from `course-shared/canon/data/` by
`course-shared/tools/seed_mocks.py`. The files in this repository are authored rather than
generated, but they are reconciled against the same canon: account identifiers, people, product
areas and policy numbers all resolve there.

Changing a value here without changing the canon puts this repository out of step with the four
mock systems. `seed_mocks.py --check` does not cover authored files, so nothing will tell you.

## What is deliberately wrong

The opportunity document was written before both June incidents, was never revised, and is still the document people read. Nothing carries a review date.

The full register is `course-shared/heldout/seeded-defects.md`, and the contradictions this
repository takes part in are in `course-shared/canon/conflicts.md`. Both are held out.

## Identifier ranges

This repository's reserved ranges are in `course-shared/canon/identifiers.md`. Identifiers
outside its own range are references to another track's material and must resolve.
