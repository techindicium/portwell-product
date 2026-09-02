# Architecture rules, PDLC track

Rules the track's system holds itself to. Each one says how it is enforced. A rule enforced
only by this document being read is marked `prose`, and turning one of those into an executable
control is the Module 3 exercise.

| # | Rule | Enforced by |
| -: | :- | :- |
| 1 | State transitions go through `scripts/lifecycle.py`. | `scripts/hooks/guard_paths.py`, `tests/test_guard_paths.py` |
| 2 | Every recorded transition cites evidence that exists and is non-empty. | `scripts/lifecycle.py`, `scripts/hooks/check_evidence.py` |
| 3 | The correction loop is bounded and exhaustion escalates. | `state/state-model.json` limits, `tests/test_lifecycle_cli.py` |
| 4 | Held-out scenarios are never readable or writable from the track. | `.claude/settings.json` deny, guard hook, `tests/test_scenarios.py` |
| 5 | Deterministic checks run before any specialist agent review. | `prose` |
| 6 | A tool refuses invalid input rather than guessing. | `prose` |
| 7 | An artifact handed to another track carries its contract version. | `prose` |
| 8 | No fixture data leaves the repository and no tool reaches a real endpoint. | `.claude/settings.json` deny on network commands |

## Blast radius

Where a wrong result has effects, which is what routing decisions weigh.

| Change touches | Blast radius | Routing consequence |
| :- | :- | :- |
| `state/state-model.json` | Every item in the track | Human approval, and a test change in the same pull request |
| `scripts/` or `hooks/` | Every future run | Human approval, regression case required |
| `skills/` or `agents/` | Future runs that route to them | Reviewed, fast path allowed |
| `scenarios/visible/` | The evaluation set only | Fast path |
| `evidence/` | One item | Fast path |
| `fixtures/` | Every scenario reading them | Human approval, because tests key on fixture identifiers |

## Additions

Groups add rules. A useful addition names the failure it prevents and how it is enforced. A rule
with no enforcement column entry and no incident behind it is a preference, and preferences go
in `CLAUDE.md`.
