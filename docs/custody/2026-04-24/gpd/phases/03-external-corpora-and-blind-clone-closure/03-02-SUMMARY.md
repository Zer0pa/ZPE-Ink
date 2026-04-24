# Plan 02 Summary

Status: complete

## Blind-Clone Execution

- An untouched RunPod host cloned the private GitHub repo directly at commit `3d4efc2463e56077e4139b506c15a64bfd61fac5`.
- The blind clone established a real bounded external verdict:
  - editable package install: `PASS`
  - `executable/verify_roundtrip.py`: `PASS`
  - `pytest code/tests -q` inside the blind-clone venv: `PASS`
  - full resource-probe surface: `INCONCLUSIVE` because `gate_a_setup.py` hard-aborted when `npm` was absent instead of recording a probe miss

## What Phase 03 Closed

- The external boundary is now explicit and evidence-backed.
- Blind-clone verification is no longer `UNTESTED`.
- The workstream now carries a real broader non-Latin online-stroke result:
  - Calliar: `2.774608127006351x`

## What Phase 03 Did Not Change

- Sovereign release verdict remains `FAIL` / `NO-GO`.
- Overall contradiction surface remains `INCONCLUSIVE`, but it is narrower and better evidenced.
- `brotli` still beats `zpe_ink` on the structured tier.
- Direct UNIPEN closure remains unresolved.

## Phase 03 Verdict

- Phase 03 requirements are complete enough to advance the project honestly:
  - boundary crossing was explicit
  - blind clone was executed
  - broader corpus work stayed same-corpus and non-theatrical
- The result is not a release `PASS`. It is an honest external closeout that leaves the authority surface narrower, not broader.

## Next Valid Phase

Phase 04 should now plan candidate runtime and tokenizer branches against the updated external truth surface, while carrying forward:

- direct UNIPEN unresolved
- structured-tier comparator loss to `brotli`
- release still blocked
