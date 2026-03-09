# RUNBOOK_ZPE_INK_GATE_A

## Objective
Runbook completeness, dataset/resource lock, baseline inventory, provenance capture, and NET-NEW input lock.

## Commands
1. `python3 scripts/gate_a_setup.py --artifact-root artifacts/2026-02-20_zpe_ink_wave1`

## Expected Artifacts
- `artifacts/2026-02-20_zpe_ink_wave1/before_after_metrics.json` (baseline side populated)
- `artifacts/2026-02-20_zpe_ink_wave1/concept_resource_traceability.json` (initial mapping)
- `artifacts/2026-02-20_zpe_ink_wave1/command_log.txt` (resource lock attempts)
- `artifacts/2026-02-20_zpe_ink_wave1/max_resource_lock.json` (E1 pack lock)

## Fail Signatures
- Missing runbook files.
- Missing provenance lock metadata (version/date/hash or snapshot note).
- Traceability map missing any Appendix B item.
- Missing E1 evidence-input lock entries for NET-NEW pack md/pdf.

## Rollback
- Recreate malformed/missing baseline files from gate script templates.
- Re-run Gate A before proceeding.
