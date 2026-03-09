#!/usr/bin/env bash
set -euo pipefail

ART_ROOT="${1:-proofs/reruns/INK-Canonical-local}"
mkdir -p "$ART_ROOT"
export PYTHONPATH="${PYTHONPATH:-}:code"
PYTHON_BIN="${PYTHON_BIN:-python3}"

"$PYTHON_BIN" code/scripts/gate_a_setup.py --artifact-root "$ART_ROOT"
"$PYTHON_BIN" -m pytest code/tests/test_codec_roundtrip.py > "$ART_ROOT/regression_results.txt"
"$PYTHON_BIN" code/scripts/gate_b_roundtrip.py --artifact-root "$ART_ROOT"
"$PYTHON_BIN" code/scripts/gate_c_benchmarks.py --artifact-root "$ART_ROOT"
"$PYTHON_BIN" code/scripts/gate_d_falsification.py --artifact-root "$ART_ROOT"
bash code/scripts/gate_e_cross_runtime.sh "$ART_ROOT"
"$PYTHON_BIN" code/scripts/generate_handoff.py --artifact-root "$ART_ROOT"

echo "ALL_GATES_PASS"
