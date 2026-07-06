#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

echo -e "RUNNING: /usr/local/autopkg/python step_04_read_the_file.py pathname=sample.txt verbose=1\nRESULT:"
/usr/local/autopkg/python "$SCRIPT_DIR"/step_04_read_the_file.py pathname="$SCRIPT_DIR"/sample.txt verbose=1
