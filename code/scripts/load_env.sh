#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f .env ]]; then
  echo "ENV_MISSING:.env"
  exit 1
fi

# Dotenv loader that preserves spaces in values without eval.
while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -z "$line" ]] && continue
  [[ "$line" =~ ^[[:space:]]*# ]] && continue
  key="${line%%=*}"
  value="${line#*=}"
  key="${key## }"
  key="${key%% }"
  export "$key=$value"
done < .env

echo "ENV_LOADED_KEYS:$(awk -F= 'NF && $1 !~ /^#/ {print $1}' .env | paste -sd ',' -)"
