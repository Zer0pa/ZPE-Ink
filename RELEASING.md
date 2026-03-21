# Releasing

This repo follows a private-first release path.

Current technical release unit:

- installable Python package from `code/`
- wheel and sdist build from `code/pyproject.toml`
- installed smoke CLI surface:
  - `python -m zpe_ink demo`
  - `python -m zpe_ink verify-roundtrip`

Current source-verified but non-packaged surfaces:

- `code/bindings/python_native/`
- `code/bindings/wasm/`
- `code/bindings/swift/`
- `code/bindings/csharp/`

Those bindings are verified in CI as repo-local source surfaces. They are not part of the pip install unit.

Python-native binding rule:

- `code/bindings/python_native/` targets the stable PyO3 ABI baseline for Python 3.11+
- verify it against the same interpreter used for the Python package checks by setting `PYO3_PYTHON`

Current rule:

- no public release action until the sovereign release surface is `PASS` on the exact commit under consideration
- authoritative surfaces: `proofs/reruns/benchmark_freeze_local/claim_scope_map.json` and `proofs/reruns/contradiction_resolution_local/contradiction_resolution_manifest.json`

Minimum release sequence:

1. private staging push
2. inspector review on the pushed commit
3. contradiction reconciliation and required fixes
4. explicit operator approval
5. only then consider public release

Technical verification path before any release decision:

1. `python -m pip install -e './code[dev]'`
2. `python -m pytest code/tests -q`
3. `python code/scripts/verify_binding_contracts.py --repo-root .`
4. `python -m build --wheel --sdist ./code --outdir dist`
5. install the built wheel and rerun `zpe-ink-verify-roundtrip`
6. `PYO3_PYTHON="$(which python)" cargo check --manifest-path code/bindings/python_native/Cargo.toml`
7. `cargo check --manifest-path code/bindings/wasm/Cargo.toml --target wasm32-unknown-unknown`

Current blockers:

- sovereign release surface remains `FAIL` while the handoff manifest is `NO-GO`
- UNIPEN parity remains unresolved
- blind-clone verdict is still `INCONCLUSIVE` pending a rerun of gate-a resource probe
