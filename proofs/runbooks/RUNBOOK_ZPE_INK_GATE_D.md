# RUNBOOK_ZPE_INK_GATE_D

## Objective
Execute malformed/adversarial campaigns and determinism replay.

## Commands
1. `python3 scripts/gate_d_falsification.py --artifact-root artifacts/2026-02-20_zpe_ink_wave1`

## Expected Artifacts
- `artifacts/2026-02-20_zpe_ink_wave1/determinism_replay_results.json`
- `artifacts/2026-02-20_zpe_ink_wave1/falsification_results.md`

## Fail Signatures
- Any uncaught crash > 0%.
- Determinism replay not 5/5 hash-identical.
- Memory ceiling breach in long-page stress test.
- Long-sequence (>10k stroke) maximalization stress is not executed.

## Rollback
- Isolate failing corpus sample and patch decoder guardrails.
- Re-run Gate D and Gate E.
