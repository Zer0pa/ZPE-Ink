# V6 Authority Surface — Completion Report

**Repo:** ZPE-Ink
**Agent:** Codex
**Date:** 2026-04-14
**Branch:** campaign/v6-authority-surface

## Dimensions Executed

- [x] **A: Key Metrics** — rewritten
- [x] **B: Competitive Benchmarks** — added
- [x] **C: pip Install Fix** — fixed with root-level wrapper
- [x] **D: Publish Workflow** — added
- [x] **E: Proof Sync** — synced 3 files

## Verification

- pip install from root: PASS
- import test: PASS
- Proof anchors verified: 3/3 exist
- Competitive claims honest: YES

## Key Metrics Written

| Metric | Value | Baseline | Proof File |
|--------|-------|----------|------------|
| STRUCTURED_TIER | 5.5902× | vs Brotli 6.8256× | `proofs/reruns/benchmark_freeze_local/baseline_results.json` |
| CALLIAR | 2.7746× | 2500-sample corpus | `proofs/reruns/phase3_external/calliar_benchmark.json` |
| CROHME | 1.3015× | vs Brotli 2.1571× | `proofs/reruns/benchmark_freeze_local/baseline_results.json` |
| MATHWRITING | 1.0944× | vs Brotli 1.6256× | `proofs/reruns/benchmark_freeze_local/baseline_results.json` |

## Issues / Blockers

- The brief asked for `CALLIAR | 2.7746× | vs Brotli (external corpus)`, but no retained public proof artifact contains a Calliar-vs-Brotli comparator. The README therefore uses corpus context instead of fabricating a competitor baseline.
- `proofs/reruns/benchmark_freeze_local/claim_scope_map.json` still records `license_surface = LicenseRef-Zer0pa-SAL-6.0`. This retained proof artifact was left untouched per provenance rules. The new root `pyproject.toml` uses `LicenseRef-Zer0pa-SAL-6.2`.
