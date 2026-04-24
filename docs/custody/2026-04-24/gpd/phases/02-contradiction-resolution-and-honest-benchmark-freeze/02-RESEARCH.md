# Phase 02 Research

Date: 2026-03-20
Phase: `02-contradiction-resolution-and-honest-benchmark-freeze`

## Question

What can the current local M1 lane honestly resolve about the PASS-versus-NO-GO contradiction and the same-corpus authority surface before any external boundary is crossed?

## Decisive Facts Entering Phase 02

- The structured-tier anchor is still real: `/Users/Zer0pa/ZPE/ZPE Ink/ZPE-Ink/proofs/reruns/phase1_m1_local/ink_compression_benchmark.json` reports `5.590209480060199x`.
- The hard-corpus surface is still weak:
  - MathWriting: `1.0944074088858728x`
  - CROHME: `1.301456280301924x`
- The release surface is contradictory:
  - `/Users/Zer0pa/ZPE/ZPE Ink/ZPE-Ink/proofs/reruns/phase1_m1_local/quality_gate_scorecard.json` reports `pass=true`
  - `/Users/Zer0pa/ZPE/ZPE Ink/ZPE-Ink/proofs/reruns/phase1_m1_local/handoff_manifest.json` reports `go_no_go=NO-GO`
  - `/Users/Zer0pa/ZPE/ZPE Ink/ZPE-Ink/proofs/INK_WAVE1_RELEASE_READINESS_REPORT.md` records the current verdict as `INCONCLUSIVE`
- The contradiction is not arbitrary:
  - `generate_handoff.py` requires `core_pass && appendix_all_pass`
  - the current appendix failures include `E-G3_cross_script_required=false`
  - the current maximalization blocker includes `M1_real_iam_unipen_non_inferior=false`

## Local Phase-Research Conclusions

- `FZ-09` is locally decomposable. The current evidence points to a gate-surface mismatch, not to a random artifact corruption:
  - the scorecard is an internal quality surface
  - the handoff is a release-readiness surface
  - the release surface still fails because appendix and hard-corpus-related blockers remain open
- Comparator freeze can be executed locally now:
  - the repo already has cached MathWriting and CROHME corpora under `proofs/reruns/phase1_m1_local/net_new_cache/`
  - the machine already has CLI `zstd`, `brotli`, and `lz4`
  - the current disk budget is tight but sufficient for a no-redownload rerun
- Phase 02 does not need RunPod, Red Magic, or a new corpus download to update the honest local truth surface.

## What Phase 02 Must Produce

- A contradiction-resolution manifest with one current verdict per blocker and a clear distinction between:
  - internal quality pass
  - current sovereign release failure
  - overall contradiction status
- A frozen benchmark artifact that reports:
  - raw float32 baseline
  - explicit `zstd`, `brotli`, and `lz4` comparator surfaces
  - structured-tier ratios separately from MathWriting and CROHME ratios
- A claim-scope map that blocks broad authority language while the hard-corpus surface remains weak.

## What Phase 02 Must Not Pretend

- It must not pretend that local contradiction classification equals a release `PASS`.
- It must not blend structured-tier and hard-corpus numbers into one headline metric.
- It must not turn unattached device or unapproved external compute paths into evidence.

## Carry-Forward Boundary

- If the structured-tier rerun regresses below `5.0x`, the local authority surface weakens immediately.
- If the contradiction ledger still cannot reduce the conflict to explicit blocker classes, Phase 02 remains `INCONCLUSIVE`.
- If broader or non-Latin closure is still required after the honest local freeze, that work belongs to Phase 3 with an explicit boundary note.
