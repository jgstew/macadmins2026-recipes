#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
WORKSHOP_DIR="$(cd "$SCRIPT_DIR"/.. >/dev/null 2>&1 && pwd)"

echo -e "RUNNING: echo -n \"\" | PYTHONPATH=/Library/AutoPkg /usr/local/autopkg/python HelloWorld.py greeting_name=MacAdmins verbose=1\nRESULT:"
echo -n "" | PYTHONPATH=/Library/AutoPkg /usr/local/autopkg/python "$WORKSHOP_DIR"/HelloWorld.py greeting_name=MacAdmins verbose=1
