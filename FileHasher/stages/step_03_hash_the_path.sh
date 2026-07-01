#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

echo -e "RUNNING: /usr/local/autopkg/python step_03_hash_the_path.py pathname=sample.txt verbose=1\nRESULT:"
/usr/local/autopkg/python "$SCRIPT_DIR"/step_03_hash_the_path.py pathname="$SCRIPT_DIR"/sample.txt verbose=1
