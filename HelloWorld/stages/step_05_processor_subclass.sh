#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

echo -e "RUNNING: PYTHONPATH=/Library/AutoPkg /usr/local/autopkg/python step_05_processor_subclass.py\nRESULT:"
PYTHONPATH=/Library/AutoPkg /usr/local/autopkg/python "$SCRIPT_DIR"/step_05_processor_subclass.py
