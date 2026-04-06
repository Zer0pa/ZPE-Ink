# Public Benchmark Summary

| Dataset | Status | Samples | Compression Ratio | Notes |
|---|---|---:|---:|---|
| MathWriting | benchmarked | 70 | 1.0944x | excerpt InkML |
| CROHME | benchmarked_fallback | 90 | 1.3015x | ICFHR package |
| QuickDraw (cat) | benchmarked | 256 | 0.7672x | simplified NDJSON |
| DigiLeTs | benchmarked | 180 | 1.0014x | raw complete set |
| IAM On-Line | skipped_access | 0 | n/a | registration-gated |
| UNIPEN | skipped_access | 0 | n/a | host unavailable |

All benchmarked datasets ran `encode -> decode -> verify` using the repo-local lossless codec path.
