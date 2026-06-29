#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

echo -e "RUNNING: /usr/local/autopkg/python step_04_main_guard.py\nRESULT:"
/usr/local/autopkg/python "$SCRIPT_DIR"/step_04_main_guard.py

echo -e "\nRUNNING: PYTHONPATH=stages /usr/local/autopkg/python -c \"import step_04_main_guard\"\nRESULT:"
PYTHONPATH="$SCRIPT_DIR" /usr/local/autopkg/python -c "import step_04_main_guard"
