#!/bin/bash
# Installs the harness' Python dependencies so agents can run
# `python -m h5pharness build ...` (and the tests) as soon as a web session starts.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"
python3 -m pip install --quiet --disable-pip-version-check --root-user-action=ignore -r requirements-dev.txt
