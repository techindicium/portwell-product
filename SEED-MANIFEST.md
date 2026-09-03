# Seed manifest, PDLC track

**Status:** the shell is in place. The track ships the legacy starting condition only, with no
lifecycle, no controls, and no process verification, because building those is the four modules'
work. The track's domain material is not seeded yet. This file is the specification for that work.

**Audience:** teaching team. Delete this file before handing the repository to participants.

Follow `track-sdlc/` as the worked reference.

## What the track builds

An agentic product-development system that turns evidence into governed decisions,
specifications, experiments, launch readiness, and outcome review. Its primary artifact is a
governed product-development process and the decisions that come out of it.

This is the track most likely to drift into documents about documents. Its fixture material has
to make decisions hard: four stakeholders who disagree, one policy that is not signed off, and
evidence that genuinely does not settle the question.

## Files to seed

| Path | Content | Notes |
| :- | :- | :- |
| `fixtures/discovery/interviews/*.md` | Six to eight interview notes with support engineers and two customers | Two must disagree about whether review capacity or answer quality is the bottleneck |
| `fixtures/discovery/opportunity-OPP-04.md` | The opportunity brief for expanding the Assist pilot | Written before the two incidents, and not updated after them |
| `fixtures/stakeholder-requests/` | Four requests, one per stakeholder, that cannot all be satisfied | `P-ANA` expand, `P-RUI` fix review capacity first, `P-GAB` use it in renewals now, `P-TOM` `POL-03` unsigned for LATAM |
| `fixtures/experiments/EXP-02.md` | The pilot's design, its pre-registered threshold, and its result | The result misses the threshold on one measure and beats it on another |
| `fixtures/experiments/EXP-02-results.csv` | Per-account pilot numbers | Must reconcile with the DDLC track's warehouse figures |
| `fixtures/launch/readiness-checklist.md` | The checklist as the team keeps it, with two items ticked that have no evidence behind them | |
| `fixtures/launch/adoption-measures.md` | Draft adoption measures, two of which are activity counts presented as outcomes | The Module 4 discussion depends on this |
| `fixtures/incidents/INC-01.md`, `INC-02.md` | The two pilot incident write-ups | Canon text in `course-shared/canon/company.md` |
| `project/decisions/` | Where governed decisions land, with a schema | This track owns the `launch-decision` contract |
| `project/schema/launch-decision.schema.json` | Fields: opportunity, decision, scope, evidence, constraints, approver, decided_at, review_at | Contract shape in `course-shared/canon/identifiers.md` |
| `docs/policies.md` | `POL-08`, `POL-03`, `POL-01`, `POL-10` and `POL-11` as the superseded pair | Copy verbatim from canon |
| `docs/identifiers.md` | Owned: opportunity, experiment. Consumed: everything | Reserved range `OPP-`, `EXP-` |
| `docs/dependencies.md` | The evidence this track consumes from DDLC and KDLC, and what it verifies | |
| `docs/backlog.md` | Eight to twelve items, one of which does not apply here | |
| `docs/architecture-rules.md` | Append PDLC rules and the blast-radius table | High-radius: a launch decision, and a change to an adoption measure |
| `legacy/tracker.csv` | What is in flight, with inconsistent statuses and missing owners | The Module 1 trace starts here |
| `legacy/incidents/` | `INC-01` and `INC-02` as this track saw them | Each traceable to a control that does not exist |

## Seeded problems, one per family

| Family | Seed | Why it survives a green suite |
| :- | :- | :- |
| Stale context | `POL-10` cited in the readiness checklist after `POL-11` superseded it on 2026-07-01 | Nothing checks a policy citation against the policy's status |
| Missing provenance | The opportunity brief cites a market size figure with no attribution | Nothing requires an evidence reference to resolve |
| Specification gaming | `EXP-02`'s success threshold lowered after the result came in, with no decision record | The experiment file is the only record of its own threshold |
| Weak routing | A pilot expansion past 25 accounts recorded as a routine scope change, which `POL-08` says needs a launch-readiness decision | Scope is a free-text field |
| Recovery failure | A decision blocked on `P-TOM`'s `POL-03` sign-off that retries the same request three times without escalating | The blocker has no owner field |

## Cross-track consistency

`EXP-02-results.csv` must reconcile with the DDLC warehouse on the ten canon accounts. The four
stakeholder positions in `course-shared/canon/company.md` are fixed and must not be resolved in
the fixture material: an agentic system that inherits a settled disagreement has nothing to
govern.

## Acceptance

- `make test` passes on a clean clone, or reports that the track has no tests yet.
- The four stakeholder positions remain unresolved in the seed material.
- Every visible scenario names a real decision, experiment, or checklist item.
- The five seeded problems are recorded in `course-shared/heldout/seeded-defects.md`.
