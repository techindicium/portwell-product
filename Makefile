# Product at Portwell Software.
#
# PYTEST_PATHS is where this repository's tests live. Set it in Makefile.local, which is not
# overwritten when the shared repository template is refreshed.
PYTEST_PATHS ?=
PYTHON       ?= python3

-include Makefile.local

.PHONY: help setup test clean

help:
	@echo "setup       create .venv and install what this repository needs"
	@echo "test        run this repository's tests ($(if $(PYTEST_PATHS),$(PYTEST_PATHS),none yet))"
	@echo ""
	@echo "Anything else this repository needs belongs in Makefile.local."

# Run once per clone. Creates .venv, installs dependencies, and builds any local database.
setup:
	@./scripts/setup.sh

test:
ifeq ($(strip $(PYTEST_PATHS)),)
	@echo "No tests here yet."
else
	@$(PYTHON) -m pytest $(PYTEST_PATHS) -q
endif

clean:
	@rm -rf .venv .pytest_cache
	@find . -name __pycache__ -type d -prune -exec rm -rf {} +
