# Plan 02 Summary

Status: complete
Artifact root: `ZPE-Ink/proofs/reruns/benchmark_freeze_local`

## Structured Tier

- `zpe_ink`: `5.590209480060199x`
- `brotli`: `6.825565026256283x`
- `zstd`: `4.9199524605723175x`
- `lz4`: `1.990919682416212x`

Interpretation:

- The raw-baseline structured-tier claim survives.
- A broader engineering-comparator superiority claim does not survive.
- `brotli` currently beats `zpe_ink` on the frozen structured tier.

## Hard Corpora

- MathWriting:
  - `zpe_ink`: `1.0944074088858728x`
  - `brotli`: `1.62561517936555x`
  - `zstd`: `1.3205529598766919x`
- CROHME:
  - `zpe_ink`: `1.301456280301924x`
  - `brotli`: `2.157058753802995x`
  - `zstd`: `1.884287822177736x`

Interpretation:

- Hard-corpus authority remains weak.
- The frozen comparator stack makes the broad handwriting-compression story weaker, not stronger.

## Result

The honest claim surface is now narrower than it looked at the end of Phase 1:

- structured-tier-only against the raw float32 baseline is still allowed
- superiority over frozen engineering comparators is not supported
- broad hard-corpus authority is not supported
