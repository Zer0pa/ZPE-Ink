# RUNBOOK_ZPE_INK_GATE_M

## Objective
Execute Appendix D maximalization gates (`M1..M4`) with falsification-first adjudication and quantified closure of prior `INCONCLUSIVE` gaps.

## Commands
1. `python3 scripts/gate_m_maximalization.py --artifact-root artifacts/2026-02-20_zpe_ink_wave1`

## Expected Artifacts
- `artifacts/2026-02-20_zpe_ink_wave1/cross_script_generalization_report.json`
- `artifacts/2026-02-20_zpe_ink_wave1/net_new_gap_closure_matrix.json`
- `artifacts/2026-02-20_zpe_ink_wave1/falsification_results.md` (max-wave updates)

## Fail Signatures
- Real-corpus runs are absent where resources were accessible.
- Parity matrix does not retain hash consistency across available runtimes.
- Long-sequence stress (`>10k` strokes) not executed or uncaught crash rate > 0%.
- Prior `INCONCLUSIVE` items lack quantified impact notes.

## Rollback
- Patch minimal parser/adapter scope.
- Re-run Gate M then Gate N and packaging.
