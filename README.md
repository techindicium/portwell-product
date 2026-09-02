# Product Development Lifecycle agentic delivery system

The PDLC track repository for **Advanced SDLC and harness engineering**. Four groups
build one system here across four weekly modules, and the track submits one integrated group
pull request per group per week.

This repository is not the Portwell Assist product. It is the delivery system that produces the
PDLC lifecycle artifact for Assist.

## Setup

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
make verify
```

`make verify` must pass on a clean clone. If it does not, that is a bug in the track baseline
and belongs to the teaching team, not to your group.

## Layout

```text
.claude/settings.json        project-scoped permissions
.claude-plugin/plugin.json   plugin manifest
skills/                      named lifecycle procedures
agents/                      specialist reviewers
hooks/hooks.json             where deterministic interception is wired
scripts/                     deterministic helpers, standard library only
scripts/hooks/               hook implementations
mcp/                         tool servers, and the simulated external services
state/                       the state model and the append-only lifecycle log
scenarios/visible/           cases the track can run
scenarios/heldout/           supplied in Module 4, refused by the guard until then
tests/                       the repository's own checks
docs/                        the track's rules, policies, and identifier schemes
fixtures/                    the track's seed material
evidence/<item>/             what each state transition recorded
```

## The rules that are not yours to change

Three, and each has a test that fails if it is removed.

1. **State moves through the CLI.** `scripts/lifecycle.py` is the only writer of
   `state/lifecycle.jsonl`. `scripts/hooks/guard_paths.py` refuses anything else.
   Regression: `tests/test_guard_paths.py`.
2. **The state model keeps its failure states.** A lifecycle with only a happy path is the
   failure this course studies. Regression: `tests/test_state_model.py`.
3. **Held-out cases stay held out.** `scenarios/heldout/` is denied in settings and refused by
   the guard, before it exists. Regression: `tests/test_scenarios.py`.

Everything else is yours: skills, agents, tools, additional hooks, additional states, the
track's domain checks, and the scenarios you add.

## Working rhythm

| Module | Shared capability | What lands here |
| :- | :- | :- |
| 1 | Lifecycle and state | The track's real lifecycle, its artifacts, transitions, and failure states |
| 2 | Harness architecture | A context contract, two safe tools, permissions, one interception point, one induced failure |
| 3 | Meta-harness controls | One prose rule turned into an executable control with a regression case |
| 4 | Verification and operation | An evaluation set, ordered checks, held-out failure analysis, operating measures |

Before implementing your group's lens, model the whole capability. The lens is the part you go
deeper on, not the part you do instead.

## Recording work

```bash
python3 scripts/lifecycle.py advance --item <ID> --to context \
  --evidence evidence/<ID>/context-manifest.md --actor agent --note "why"
python3 scripts/lifecycle.py show --item <ID>
make verify
```

A pull request that claims a transition the log does not contain will be returned.
