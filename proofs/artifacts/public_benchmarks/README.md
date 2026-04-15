# Public Benchmark Summary

| Dataset | Status | Samples | Compression Ratio | Notes |
|---|---|---:|---:|---|
| MathWriting | benchmarked | 70 | 1.1870x | excerpt InkML |
| CROHME | benchmarked_fallback | 90 | 1.4360x | ICFHR package |
| QuickDraw (cat) | benchmarked | 256 | 1.0181x | simplified NDJSON |
| DigiLeTs | benchmarked | 180 | 1.0891x | raw complete set |
| UJI Pen Characters | benchmarked_phase3 | 1,364 | 1.6111x | exact roundtrip; see `proofs/reruns/phase3_public_benchmarks/` |
| IAM On-Line | skipped_access | 0 | n/a | registration-gated |
| UNIPEN | skipped_access | 0 | n/a | host unavailable |

All benchmarked datasets ran `encode -> decode -> verify` using the repo-local lossless codec path.

The UJI row broadens the bounded public-handwriting surface only. It does not change release readiness, hard-corpus verdicts, or the sovereign `FAIL` / `NO-GO` gate.
