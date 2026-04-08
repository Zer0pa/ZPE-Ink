#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"

wasm_pack="${WASM_PACK:-wasm-pack}"

cd "$script_dir"
"$wasm_pack" build "$repo_root/code/bindings/wasm" --target web --release --out-dir "$script_dir/pkg"

