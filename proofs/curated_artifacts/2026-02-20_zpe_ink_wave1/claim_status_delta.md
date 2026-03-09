# Claim Status Delta

| Claim | Description | Pre | Post | Evidence | Max-Wave Resource Evidence |
|---|---|---|---|---|---|
| INK-C001 | Lossless synthetic roundtrip | UNTESTED | PASS | `artifacts/2026-02-20_zpe_ink_wave1/ink_roundtrip_results.json` | MathWriting:RESOLVED; CROHME:RESOLVED; UCI Pen Digits:RESOLVED; IAM/UNIPEN:PAUSED_EXTERNAL; Muharaf:PAUSED_EXTERNAL |
| INK-C002 | CR >= 5x vs raw | UNTESTED | PASS | `artifacts/2026-02-20_zpe_ink_wave1/ink_compression_benchmark.json` | MathWriting:RESOLVED; CROHME:RESOLVED; UCI Pen Digits:RESOLVED; IAM/UNIPEN:PAUSED_EXTERNAL; Muharaf:PAUSED_EXTERNAL |
| INK-C003 | Hausdorff <= 1 px | UNTESTED | PASS | `artifacts/2026-02-20_zpe_ink_wave1/ink_fidelity_metrics.json` | MathWriting:RESOLVED; OpenRing:PAUSED_EXTERNAL |
| INK-C004 | Pressure RMSE <= 2% | UNTESTED | PASS | `artifacts/2026-02-20_zpe_ink_wave1/ink_pressure_metrics.json` | OpenRing:PAUSED_EXTERNAL |
| INK-C005 | Encode latency <= 2 ms/stroke | UNTESTED | PASS | `artifacts/2026-02-20_zpe_ink_wave1/ink_latency_benchmark.json` | UCI Pen Digits:RESOLVED; Muharaf:PAUSED_EXTERNAL |
| INK-C006 | Cross-runtime decode parity | UNTESTED | PASS | `artifacts/2026-02-20_zpe_ink_wave1/ink_cross_runtime_parity.json` | UCI Pen Digits:RESOLVED; IAM/UNIPEN:PAUSED_EXTERNAL |
