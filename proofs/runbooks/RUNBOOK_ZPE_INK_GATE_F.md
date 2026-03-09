# RUNBOOK_ZPE_INK_GATE_F

## Objective
Execute Appendix F commercial-safe closure (`F-G1..F-G3`) and force all open claim/resource statuses to `PASS`, `FAIL`, or `PAUSED_EXTERNAL` with evidence.

## Commands
1. `python3 scripts/gate_f_commercial_closure.py --artifact-root artifacts/2026-02-20_zpe_ink_wave1`
2. `python3 scripts/generate_handoff.py --artifact-root artifacts/2026-02-20_zpe_ink_wave1 --max-wave`

## Expected Artifacts
- `artifacts/2026-02-20_zpe_ink_wave1/commercialization_risk_register.md`
- `artifacts/2026-02-20_zpe_ink_wave1/commercial_corpus_parity.json`
- `artifacts/2026-02-20_zpe_ink_wave1/net_new_gap_closure_matrix.json` (with `F-G1..F-G3`)
- `artifacts/2026-02-20_zpe_ink_wave1/max_claim_resource_map.json` (no `INCONCLUSIVE`)
- `artifacts/2026-02-20_zpe_ink_wave1/claim_status_delta.md`

## Fail Signatures
- Commercial-safe corpus parity not executed (MathWriting + UCI Pen Digits).
- Any NC-only/restricted resource used for claim promotion without explicit `PAUSED_EXTERNAL`.
- Any `INCONCLUSIVE` status remaining after Gate F.
- Any claim promoted despite IAM-dependent path violation.

## Rollback
- Patch minimal corpus adapter or status-adjudication logic.
- Re-run Gate F and downstream packaging only.
