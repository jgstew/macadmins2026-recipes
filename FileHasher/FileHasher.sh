#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

echo -e "RUNNING: autopkg run -v FileHasher.recipe.yaml --search-dir .\nRESULT:"
autopkg run -v "$SCRIPT_DIR"/FileHasher.recipe.yaml --search-dir "$SCRIPT_DIR"
