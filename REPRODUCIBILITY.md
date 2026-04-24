# Reproducibility

## Canonical Inputs

Use the committed source and proof artifacts on the checked-out commit:

- `code/zpe_ink/fixtures.py`
- `code/tests/test_cross_runtime_parity.py`
- `docs/family/ZPINK_INTERFACE_CONTRACT.md`
- `docs/family/ZPINK_COMPATIBILITY_VECTOR.json`
- `proofs/artifacts/public_benchmarks/dataset_matrix.json`
- `proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json`
- `proofs/logs/20260321_technical_alignment_cross_runtime.json`
- `proofs/logs/20260321_technical_alignment_binding_contracts.json`

## Golden-Bundle Hash

Pending. The golden-bundle hash must be populated by the later receipt-bundle workflow pass, not by this lane-hygiene PR.

## Verification Command

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e './code[dev]'
python -m pytest code/tests -q
python code/scripts/verify_binding_contracts.py --repo-root .
python -m zpe_ink verify-roundtrip
```

## Supported Runtimes

| Runtime | Current support surface | Verification |
|---|---|---|
| Python package | Installable package under `code/` | `proofs/logs/20260321_technical_alignment_wheel_install.txt` |
| Rust/PyO3 native binding | Repo-local source-verified binding; not a promoted packaged runtime | `proofs/logs/20260321_technical_alignment_cargo_python_native.txt` |
| WASM binding | Repo-local source-verified binding; not a promoted packaged runtime | `proofs/logs/20260321_technical_alignment_cargo_wasm.txt` |
| Swift binding | Header contract checked | `proofs/logs/20260321_technical_alignment_binding_contracts.json` |
| C# binding | Header contract checked | `proofs/logs/20260321_technical_alignment_binding_contracts.json` |

Apple Silicon note: the Python-native Rust binding must be rechecked with `cargo build --release` under `code/bindings/python_native` during the dedicated native-packaging pass. Until that pass lands, the supported claim remains source-verified only.
