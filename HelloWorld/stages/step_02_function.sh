#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

echo -e "RUNNING: /usr/local/autopkg/python step_02_function.py\nRESULT:"
/usr/local/autopkg/python "$SCRIPT_DIR"/step_02_function.py
