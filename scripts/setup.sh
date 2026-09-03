#!/usr/bin/env bash
# Create the virtual environment and install what this repository needs.
#
# Installs the shared dependencies, then any package in this repository that
# carries its own pyproject.toml. A repository with no such package installs
# nothing extra and still ends cleanly.
#
# Prefers uv when present because it resolves an interpreter matching
# requires-python. Falls back to the stdlib venv module.
set -euo pipefail
cd "$(dirname "$0")/.."

VENV="${VENV:-.venv}"
PY="$VENV/bin/python"

say() { printf '%s\n' "$*"; }

if [ ! -x "$PY" ]; then
  if command -v uv >/dev/null 2>&1; then
    say "Creating $VENV with uv"
    uv venv "$VENV" -q
  else
    say "Creating $VENV with python3 -m venv"
    python3 -m venv "$VENV"
  fi
fi

install() {
  if command -v uv >/dev/null 2>&1; then
    VIRTUAL_ENV="$VENV" uv pip install -q "$@"
  else
    "$PY" -m pip install -q "$@"
  fi
}

say "Installing shared dependencies"
install -r requirements.txt

# Any directory holding a pyproject.toml is a package belonging to this repository.
found_pkg=0
for pj in */pyproject.toml; do
  [ -f "$pj" ] || continue
  pkg="$(dirname "$pj")"
  found_pkg=1
  if grep -q '^\[project.optional-dependencies\]' "$pj" && grep -q '^dev *=' "$pj"; then
    say "Installing $pkg with dev extras"
    install -e "$pkg[dev]"
  else
    say "Installing $pkg"
    install -e "$pkg"
  fi
done
[ "$found_pkg" -eq 0 ] && say "No local package here, shared dependencies only"

# Any local database is a build artifact, rebuilt from its committed SQL.
if [ -x scripts/build_db.py ]; then
  say ""
  say "Building the local database"
  "$PY" scripts/build_db.py
fi

say ""
say "Python:  $("$PY" -V)"
say "Ready.   Next: make test"
