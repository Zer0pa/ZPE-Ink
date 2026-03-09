# Governance

This repo is governed by evidence discipline.

## Rules

- runtime and artifact truth outrank prose
- mixed evidence is not a pass
- unresolved contradictions must stay explicit
- package or contract changes that break `.zpink` compatibility require a compatibility-vector update

## Status Terms

- `VERIFIED`: directly supported by current artifacts
- `INFERRED`: coherent synthesis across verified artifacts
- `INCONCLUSIVE`: contradictory or incomplete evidence
- `DEFERRED`: intentionally not executed in the current phase

## Current Governance Reality

- package boundary: normalized
- private staging: allowed
- public release: not allowed
- current repo truth: `INCONCLUSIVE`
