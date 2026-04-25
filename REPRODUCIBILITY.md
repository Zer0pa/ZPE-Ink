# Reproducibility

## Canonical Inputs

- `docs/family/ZPINK_COMPATIBILITY_VECTOR.json` — packet/header compatibility vector used by the binding contract checks.
- `proofs/artifacts/public_benchmarks/dataset_matrix.json` — public benchmark dataset status and measured ratios.
- `proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json` — committed public-benchmark evidence bundle.
- `proofs/logs/20260321_technical_alignment_cross_runtime.json` — cross-runtime technical-alignment status for the shipped bindings.

## Golden-Bundle Hash

Will be populated by the `receipt-bundle.yml` workflow in Wave 3.

## Verification Command

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e './code[dev]'
python -m pytest code/tests -q
python -m zpe_ink demo
python -m zpe_ink verify-roundtrip
```

## Supported Runtimes

- Python package (`code/zpe_ink`)
- PyO3 native binding (`code/bindings/python_native`)
- WASM binding (`code/bindings/wasm`)
- Swift binding (`code/bindings/swift`)
- C# binding (`code/bindings/csharp`)
