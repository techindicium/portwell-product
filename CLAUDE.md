# Product at Portwell Software

Portwell Software sells Portwell WMS, a warehouse management platform, to mid-market logistics
operators. This repository holds the Product work for the help portal, the AI-assisted
customer-support product currently in pilot.

## Read before acting

`docs/how-we-work-today.md` describes the process as it is actually practised. It is prose, it
is incomplete, and parts of it are contradicted by the records in `docs/incidents/`.

`docs/policies.md` holds the company's rules. Most are enforced by nothing except being read.

`docs/architecture-rules.md` and `docs/identifiers.md` hold the constraints that do apply.
Identifiers are shared with three other teams, so they may be referenced but never renumbered.

## What is not here

There is no defined delivery lifecycle, no recorded state, no approval gates, and no automated
verification of the process itself. Work is tracked in a spreadsheet and decisions live in
people's heads.

Do not silently build that layer. Proposing a lifecycle, a state file, a set of checks and a
hook to enforce them is the obvious reaction to reading this repository, and doing it unasked
replaces a decision the team has not made with one nobody agreed to.

When a task would be easier with a control that does not exist, name the missing control and
what it would protect, then continue without it.

## Working here

- Name the artifacts consulted, where each came from, and how old each is. Where the age is
  unknown, write unknown. Do not estimate it.
- Where two sources disagree, report both and say the disagreement is unresolved. Do not pick
  the more plausible one.
- Where a rule in `docs/policies.md` applies and nothing enforces it, say so.

## Stop conditions

Stop and say so rather than continuing when:

- A required input is stale, superseded, or has no identifiable source.
- Two artifacts contradict each other on a fact the task depends on.
- The task needs a permission this project does not grant. Ask; do not route around it.
- Finishing would mean writing down a fact nobody recorded.

An empty field is information. Leave it empty and say why.

## Writing

Plain declarative prose. No em dashes. State what is true, including what failed and what could
not be determined.
