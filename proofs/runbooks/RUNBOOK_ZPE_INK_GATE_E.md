# RUNBOOK_ZPE_INK_GATE_E

## Objective
Validate cross-runtime decode parity (Python + WASM + native adapter) and package full handoff.

## Commands
1. `bash scripts/gate_e_cross_runtime.sh artifacts/2026-02-20_zpe_ink_wave1`
2. `python3 scripts/generate_handoff.py --artifact-root artifacts/2026-02-20_zpe_ink_wave1`

## Expected Artifacts
- `artifacts/2026-02-20_zpe_ink_wave1/ink_cross_runtime_parity.json`
- `artifacts/2026-02-20_zpe_ink_wave1/handoff_manifest.json`
- `artifacts/2026-02-20_zpe_ink_wave1/quality_gate_scorecard.json`
- `artifacts/2026-02-20_zpe_ink_wave1/integration_readiness_contract.json`

## Fail Signatures
- Runtime decode hash mismatch.
- Missing required artifact from PRD/Appendix C contract.

## Rollback
- Patch adapter parser parity differences.
- Rebuild adapter bundles and rerun Gate E.
