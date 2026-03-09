# Auditor Playbook

This is the shortest honest local verification path for the private staging snapshot.

## What You Can Establish

- the repo has a clean inner boundary
- the `zpe_ink` package installs from `code/`
- the current pytest surface passes locally
- the curated Wave-1 proof anchors are present
- the current contradiction is explicit, not hidden

## Short Path

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ./code
python -m pytest code/tests -q
python executable/demo.py
python executable/verify_roundtrip.py
python executable/verify_cross_runtime.py
python -m pip wheel ./code --no-deps -w dist
```

## Inspect These Files Together

- `proofs/INK_WAVE1_RELEASE_READINESS_REPORT.md`
- `proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/quality_gate_scorecard.json`
- `proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/handoff_manifest.json`
- `proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/claim_status_delta.md`
- `proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/ink_cross_runtime_parity.json`

If those surfaces disagree, the repo state is still `INCONCLUSIVE`.
