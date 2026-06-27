#!/usr/bin/env bash
# Smoke-test every processor by importing it as a Python module.
# This is the FIRST thing to check: a processor that won't even import can
# never run in a recipe. It does NOT run main() or any recipe logic.
#
# Usage:
#   ./test_processors_load.sh          # import every processor + solution
#   ./test_processors_load.sh -v       # also print any output captured
#
# Exit codes:
#   0  all processors imported successfully
#   1  one or more processors failed to import

set -uo pipefail

VERBOSE=0
while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--verbose) VERBOSE=1; shift ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Pick a Python that can import autopkglib. Prefer a local .venv, then the
# interpreter bundled with a macOS AutoPkg install, then python3 on PATH.
# (autopkglib needs pyyaml etc.; a bare system python3 usually lacks them.)
PYTHON="${SCRIPT_DIR}/.venv/bin/python"
[[ ! -x "${PYTHON}" ]] && PYTHON="${SCRIPT_DIR}/.venv/Scripts/python"
[[ ! -x "${PYTHON}" ]] && PYTHON="/usr/local/autopkg/python"
[[ ! -x "${PYTHON}" ]] && PYTHON="$(command -v python3 || command -v python || true)"
if [[ -z "${PYTHON}" || ! -x "${PYTHON}" ]]; then
    echo "Python not found" >&2
    exit 1
fi

# autopkglib must be importable. Look for an autopkg checkout adjacent to this
# repo (../autopkg/Code) or inside it (./autopkg/Code).
AUTOPKG_PATH="${SCRIPT_DIR}/../autopkg/Code"
[[ ! -d "${AUTOPKG_PATH}" ]] && AUTOPKG_PATH="${SCRIPT_DIR}/autopkg/Code"
if [[ ! -d "${AUTOPKG_PATH}" ]]; then
    echo "autopkglib not found at ../autopkg/Code or ./autopkg/Code" >&2
    echo "See docs/00-setup.md for how to get an autopkg checkout." >&2
    exit 1
fi

PROCESSORS_DIR="${SCRIPT_DIR}/SharedProcessors"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

pass=0
fail=0
declare -a failures

TIMEOUT_CMD=""
command -v timeout &>/dev/null && TIMEOUT_CMD="timeout 60"

# Import each processor (top-level exercises + solutions) as a module.
for script in "${PROCESSORS_DIR}"/*.py "${PROCESSORS_DIR}"/solutions/*.py; do
    [[ -e "${script}" ]] || continue
    name="${script#"${SCRIPT_DIR}/"}"
    output=$(PYTHONPATH="${AUTOPKG_PATH}:${PROCESSORS_DIR}" ${TIMEOUT_CMD} "${PYTHON}" - "${script}" 2>&1 <<'EOF'
import importlib.util, sys, warnings
warnings.filterwarnings("ignore")
spec = importlib.util.spec_from_file_location("module", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
EOF
)
    if [[ $? -eq 0 ]]; then
        echo -e "  ${GREEN}PASS${NC}  ${name}"
        [[ ${VERBOSE} -eq 1 && -n "${output}" ]] && echo -e "${YELLOW}        ${output//$'\n'/$'\n'        }${NC}"
        (( pass++ ))
    else
        echo -e "  ${RED}FAIL${NC}  ${name}"
        echo -e "${YELLOW}        ${output//$'\n'/$'\n'        }${NC}"
        failures+=("${name}")
        (( fail++ ))
    fi
done

echo ""
echo -e "Results: ${GREEN}${pass} passed${NC}, ${RED}${fail} failed${NC}  ($(( pass + fail )) total)"

if [[ ${fail} -gt 0 ]]; then
    echo ""
    echo "Failed to import:"
    for f in "${failures[@]}"; do echo "  - ${f}"; done
    exit 1
fi
