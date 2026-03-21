#!/usr/bin/env bash
set -euo pipefail

ART_ROOT="${1:-proofs/reruns/INK-Canonical-local}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
mkdir -p "$ART_ROOT"
export PYTHONPATH="${PYTHONPATH:-}:code"

if [[ -f .env ]]; then
  source code/scripts/load_env.sh > /dev/null
fi

"$PYTHON_BIN" code/scripts/gate_a_setup.py --artifact-root "$ART_ROOT"
"$PYTHON_BIN" -m pytest code/tests/test_codec_roundtrip.py > "$ART_ROOT/regression_results.txt"
"$PYTHON_BIN" code/scripts/gate_b_roundtrip.py --artifact-root "$ART_ROOT"
"$PYTHON_BIN" code/scripts/gate_c_benchmarks.py --artifact-root "$ART_ROOT"
"$PYTHON_BIN" code/scripts/gate_d_falsification.py --artifact-root "$ART_ROOT"
"$PYTHON_BIN" code/scripts/gate_e_cross_runtime.py "$ART_ROOT"
"$PYTHON_BIN" code/scripts/gate_e_net_new_ingestion.py --artifact-root "$ART_ROOT"
"$PYTHON_BIN" code/scripts/gate_m_maximalization.py --artifact-root "$ART_ROOT"
"$PYTHON_BIN" code/scripts/gate_f_commercial_closure.py --artifact-root "$ART_ROOT"
"$PYTHON_BIN" code/scripts/generate_handoff.py --artifact-root "$ART_ROOT" --max-wave

echo "MAX_WAVE_ALL_GATES_DONE"
