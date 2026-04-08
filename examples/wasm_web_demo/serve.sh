#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
port="${PORT:-8000}"
exec python3 -m http.server "$port" --bind 127.0.0.1 --directory "$script_dir"
