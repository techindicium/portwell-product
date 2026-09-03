# Architecture rules

Rules this repository holds itself to. The `Enforced by` column is the honest one.

`prose` means exactly that. Nothing refuses a violation, nothing reports one, and a change that
breaks the rule merges.

| # | Rule | Enforced by |
| -: | :- | :- |
| 1 | No customer data leaves the repository, and no tool reaches a real endpoint. | `.claude/settings.json` deny on network commands |
| 2 | Identifiers owned by another team are referenced, never renumbered. | `prose`, and see `docs/identifiers.md` |
| 3 | An artifact published to another team carries its contract version. | `prose` |
| 4 | A rule that applies to a decision is stated even when nothing enforces it. | `prose` |
| 5 | Two sources that disagree are both reported, and the disagreement is left open. | `prose` |
| 6 | An artifact of unknown age is recorded as unknown rather than estimated. | `prose` |

Six rules, one enforced.

## Blast radius

Where a wrong result has effects. Nothing here weighs this automatically; the table exists so
that a person can.

| Change touches | Blast radius | Why |
| :- | :- | :- |
| `data/` | Every consumer, here and in other teams | Other teams key on these identifiers |
| A contract published to another team | That team's work and its own consumers | Breakage surfaces late, in someone else's repository |
| `docs/identifiers.md` | Every team | Renumbering is unrecoverable once another team has referenced it |
| `docs/policies.md` | Every future decision citing the policy | A policy edit silently changes what past decisions meant |
| This repository's own code | Whatever depends on it | Local, unless it sits on a published boundary |
| `docs/incidents/` | Nothing automated. It is the record of what happened. | Editing it rewrites history rather than correcting a system |

## Additions

A useful new rule names the failure it prevents and how it is enforced. A rule with no
enforcement and no incident behind it is a preference, and preferences belong in `CLAUDE.md`.

The more valuable move is the other direction: take a `prose` row above, find the incident or
near miss in `docs/incidents/`, and give the rule something that refuses.
