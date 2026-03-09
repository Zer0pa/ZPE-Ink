#!/usr/bin/env bash
set -euo pipefail

ARTIFACT_ROOT="${1:?artifact root required}"
python3 scripts/gate_e_cross_runtime.py "$ARTIFACT_ROOT"
