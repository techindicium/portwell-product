# State

`state-model.json` declares the states, transitions, evidence requirements, and budgets.
`lifecycle.jsonl` is the append-only record of what actually happened.

The log is JSONL rather than a table because four groups mutate it concurrently during a week.
An append-only line-oriented file merges; a markdown table does not.

One line per transition:

```json
{"at":"2026-09-11T14:02:11Z","item":"TCK-004417","from":"context","to":"route","actor":"agent","evidence":"evidence/TCK-004417/routing-decision.md","note":"billing area, Enterprise tier, human review required by POL-01"}
```

`from` is `null` on the first transition. `evidence` is a repository-relative path that existed
and was non-empty when the transition was recorded. `note` is optional and should carry the
reason, not restate the transition.

Extending the model is expected. Adding a state means adding it to `states`, giving it an
evidence requirement, wiring it into `transitions`, and keeping `tests/test_state_model.py`
green. Removing a failure state is not an extension.
