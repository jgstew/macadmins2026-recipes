#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
WORKSHOP_DIR="$(cd "$SCRIPT_DIR"/.. >/dev/null 2>&1 && pwd)"

echo -e "RUNNING: autopkg run -v HelloWorld.recipe.yaml --search-dir .\nRESULT:"
autopkg run -v "$WORKSHOP_DIR"/HelloWorld.recipe.yaml --search-dir "$WORKSHOP_DIR"

echo -e "\nRUNNING: echo -n \"\" | PYTHONPATH=/Library/AutoPkg /usr/local/autopkg/python HelloWorld.py greeting_name=MacAdmins verbose=1\nRESULT:"
echo -n "" | PYTHONPATH=/Library/AutoPkg /usr/local/autopkg/python "$WORKSHOP_DIR"/HelloWorld.py greeting_name=MacAdmins verbose=1
