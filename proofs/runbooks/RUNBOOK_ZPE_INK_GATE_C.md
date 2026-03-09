# RUNBOOK_ZPE_INK_GATE_C

## Objective
Benchmark compression, visual fidelity, pressure RMSE, and encode latency.

## Commands
1. `python3 scripts/gate_c_benchmarks.py --artifact-root artifacts/2026-02-20_zpe_ink_wave1`

## Expected Artifacts
- `artifacts/2026-02-20_zpe_ink_wave1/ink_compression_benchmark.json`
- `artifacts/2026-02-20_zpe_ink_wave1/ink_fidelity_metrics.json`
- `artifacts/2026-02-20_zpe_ink_wave1/ink_pressure_metrics.json`
- `artifacts/2026-02-20_zpe_ink_wave1/ink_latency_benchmark.json`

## Fail Signatures
- Compression ratio < 5.0.
- Hausdorff distance > 1.0 px @96 DPI.
- Pressure RMSE > 2%.
- Median encode latency > 2ms/stroke.

## Rollback
- Patch quantization/packet encoding minimal scope.
- Re-run Gate C and downstream gates.
