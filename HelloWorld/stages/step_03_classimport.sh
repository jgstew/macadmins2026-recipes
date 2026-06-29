#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

echo -e "RUNNING: PYTHONPATH=stages /usr/local/autopkg/python -c \"import step_03_class\"\nRESULT:"
PYTHONPATH="$SCRIPT_DIR" /usr/local/autopkg/python -c "import step_03_class"
