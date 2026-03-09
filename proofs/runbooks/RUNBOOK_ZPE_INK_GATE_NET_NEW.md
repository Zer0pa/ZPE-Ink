# RUNBOOK_ZPE_INK_GATE_NET_NEW

## Objective
Execute Appendix E NET-NEW ingestion gates (`E-G1..E-G5`) with attempt-all evidence, impracticality adjudication, and RunPod readiness outputs when needed.

## Commands
1. `python3 scripts/gate_e_net_new_ingestion.py --artifact-root artifacts/2026-02-20_zpe_ink_wave1`
2. `python3 scripts/generate_handoff.py --artifact-root artifacts/2026-02-20_zpe_ink_wave1 --max-wave`

## Expected Artifacts
- `artifacts/2026-02-20_zpe_ink_wave1/max_resource_lock.json`
- `artifacts/2026-02-20_zpe_ink_wave1/max_resource_validation_log.md`
- `artifacts/2026-02-20_zpe_ink_wave1/max_claim_resource_map.json`
- `artifacts/2026-02-20_zpe_ink_wave1/impracticality_decisions.json`
- `artifacts/2026-02-20_zpe_ink_wave1/inkml_converter_validation.json`
- `artifacts/2026-02-20_zpe_ink_wave1/cross_script_generalization_report.json`
- `artifacts/2026-02-20_zpe_ink_wave1/net_new_gap_closure_matrix.json`
- `artifacts/2026-02-20_zpe_ink_wave1/runpod_readiness_manifest.json` (only when `IMP-COMPUTE`)

## Fail Signatures
- Any E3 resource not attempted with command evidence.
- Any skipped resource missing valid `IMP-*` code + fallback + claim-impact note.
- Core claims close on synthetic-only traces despite available real-corpus ingestion.
- Compute deferment occurs but RunPod readiness artifact is missing.

## Rollback
- Patch ingestion connectors and parser normalization in minimal scope.
- Re-run NET-NEW ingestion gate and final packaging.
