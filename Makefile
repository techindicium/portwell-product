# Deterministic checks for the PDLC track.
#
# PYTEST_PATHS is where the track's tests live. The shell ships with `tests`; a track that adds
# a service, a transformation project, or a publication pipeline extends it in Makefile.local,
# which is the track's own file and is never overwritten by a shell update.
PYTEST_PATHS ?= tests
PYTHON       ?= python3

-include Makefile.local

.PHONY: help setup verify check-state scenarios test hooks-test clean

help:
	@echo "setup       create .venv and install everything this track needs"
	@echo "verify      run every deterministic check, in the order they should run"
	@echo "check-state validate the lifecycle log against the state model"
	@echo "scenarios   check the shape of every visible scenario file"
	@echo "test        run the repository's tests ($(PYTEST_PATHS))"
	@echo "hooks-test  exercise the guard hook's refusal and allow paths"

# Run this once per clone. It creates .venv and installs the shell's dependencies plus any
# domain package the track carries, so `make verify` passes on a clean clone.
setup:
	@./scripts/setup.sh

# Order is the teaching point. Cheap structural checks first, then the shape of the evaluation
# set, then behaviour. Specialist-agent and human review come after this target, never instead.
verify: check-state scenarios test
	@echo "OK: deterministic checks passed"

check-state:
	@$(PYTHON) scripts/lifecycle.py validate

scenarios:
	@$(PYTHON) -m pytest tests/test_scenarios.py -q

test:
	@$(PYTHON) -m pytest $(PYTEST_PATHS) -q

hooks-test:
	@$(PYTHON) -m pytest tests/test_guard_paths.py -q

clean:
	@find . -name __pycache__ -type d -prune -exec rm -rf {} + ; \
	 rm -rf .pytest_cache
