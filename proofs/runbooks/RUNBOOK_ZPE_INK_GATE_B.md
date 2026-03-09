# RUNBOOK_ZPE_INK_GATE_B

## Objective
Implement `.zpink` codec and prove synthetic lossless roundtrip.

## Commands
1. `python3 -m pytest tests/test_codec_roundtrip.py -q`
2. `python3 scripts/gate_b_roundtrip.py --artifact-root artifacts/2026-02-20_zpe_ink_wave1`

## Expected Artifacts
- `artifacts/2026-02-20_zpe_ink_wave1/ink_roundtrip_results.json`
- `artifacts/2026-02-20_zpe_ink_wave1/regression_results.txt` (updated)

## Fail Signatures
- Roundtrip mismatch in coordinates/pressure channels.
- Decode accepts malformed headers without explicit error.

## Rollback
- Revert codec framing changes to last passing fixture hash set.
- Re-run unit test + Gate B script.
