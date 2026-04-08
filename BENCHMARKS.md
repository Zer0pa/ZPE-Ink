# ZPE-Ink Benchmarks

This file is a scaffold for Phase 2.
Real public-dataset rows land in Phase 3 only.
Do not backfill synthetic or proxy data here.

## Reproducible Methodology

1. Record the repo commit, host, OS, Python version, Swift version, Rust toolchain, and browser/runtime version.
2. Record the exact dataset URL or local path, the command used, the sample count, and whether the source is public or proxy.
3. Run `encode -> decode -> verify` on the same sample set.
4. Capture raw bytes, encoded bytes, ratio, fidelity metric, and wall-clock timing.
5. Keep proxy/demo rows separate from public dataset rows.

## Phase 2 Scaffold

| dataset | source | baseline | zpe | ratio | fidelity | notes |
|---|---|---|---|---|---|---|
| Synthetic proxy | repo fixtures | raw float32 | n/a | n/a | roundtrip only | Proxy/demo surface only |
| Public datasets | reserved for Phase 3 | raw float32 | n/a | n/a | n/a | IAM, CASIA, and other real rows land in Phase 3 |

## Phase 3 Reservation

- Use only freely available public datasets.
- Replace proxy rows with measured rows from runnable scripts.
- Cite the dataset URL, the exact command, and the fidelity metric for each row.
