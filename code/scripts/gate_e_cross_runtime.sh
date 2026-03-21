#!/usr/bin/env bash
set -euo pipefail

ARTIFACT_ROOT="${1:?artifact root required}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

export PYTHONPATH="${PYTHONPATH:-}:$CODE_ROOT"
"$PYTHON_BIN" "$SCRIPT_DIR/gate_e_cross_runtime.py" "$ARTIFACT_ROOT"
