# ZPE Ink Team Review Pack

Date: 2026-03-20
Audience: science + engineering
Scope: current product status, decisive evidence, and the next valid path

## Current Status In One Page

ZPE Ink is in a stronger local state than before, but it is not ready for a pass narrative. The deterministic transport lane is real and locally executable on the MacBook M1 Air. The structured-tier sovereign metric still passes at `5.5902x`, cross-runtime parity now passes locally across Python, WASM, Swift, and PyO3, and the proof harness now runs end-to-end from repo root. A real lightweight public online-stroke lane was added using UJI Pen Characters alongside MathWriting and CROHME.

The hard truth is still the hard truth:

- hard-corpus compression remains weak:
  - MathWriting `1.0944x`
  - CROHME `1.3015x`
  - UJI Pen Characters `1.5110x`
  - UCI Pen Digits `0.6173x`
- `M1_real_iam_unipen_non_inferior` still fails
- `E-G3_cross_script_required` still fails
- the handoff verdict is still `NO-GO`

My view: the project now has a credible local kernel and measurement harness, but it does not yet have the hard-corpus authority or enterprise interoperability proof needed to claim a breakout product. The next phase should be narrow and brutal: direct IAM/UNIPEN closure, non-Latin online-stroke closure, and only then any broader productization language.

## The 10-Document Pack

Read these in order:

1. `docs/team_review/ZPE_INK_TEAM_REVIEW_PACK_2026-03-20.md`
   - This document. Start here for the status read and recommended interpretation.

2. `PRD_ZPE_DIGITAL_INK.md`
   - Canonical product and authority-metric charter.
   - Use this to understand what counts as success and what is still explicitly blocked.

3. `../.gpd/ROADMAP.md`
   - Current phase structure and what Phase 01 was supposed to do.
   - Use this to see how the local execution fits into the longer program.

4. `../.gpd/phases/01-local-authority-rerun-and-kernel-uplift/01-03-SUMMARY.md`
   - Honest closeout of the executed local phase.
   - This is the best short read on what changed and what remains open.

5. `proofs/reruns/phase1_m1_local/claim_status_delta.md`
   - Claim-by-claim status with resource posture.
   - Use this to connect technical claims to current evidence and paused external dependencies.

6. `proofs/reruns/phase1_m1_local/net_new_gap_closure_matrix.json`
   - Appendix D/E/F/M gate matrix.
   - This is the fastest way to see which gates now pass locally and which still fail.

7. `proofs/reruns/phase1_m1_local/blockers_before_after.json`
   - Before/after blocker set.
   - This shows what the local phase genuinely closed and what remains sovereign.

8. `proofs/reruns/phase1_m1_local/commercialization_risk_register.md`
   - External dependency map for commercialization and platform validation.
   - This is where the science team and engineering team should align on what is external vs fixable.

9. `proofs/reruns/phase1_m1_local/quality_gate_scorecard.json`
   - Dimension scores and non-negotiable local execution checks.
   - Read this with the next document, not in isolation.

10. `proofs/reruns/phase1_m1_local/handoff_manifest.json`
    - Final handoff verdict.
    - This document is the stop-sign. It remains `NO-GO`, which is why the project is not ready for a pass story.

## How To Interpret The Pack

- Do not let the local `PASS` surfaces erase the `NO-GO` handoff.
- Do not let the structured-tier `5.5902x` result masquerade as hard-corpus authority.
- Do not let the local cross-runtime pass masquerade as device- or ecosystem-level interoperability closure.
- Do treat the current repo as a credible drop-in deterministic transport substrate with better execution hygiene than before.

## Key Data To Carry Forward

- Structured/proxy sovereign metric: `5.5902x`
- Hard-corpus real online-stroke results:
  - MathWriting `1.0944x`
  - CROHME `1.3015x`
  - UJI Pen Characters `1.5110x`
- Commercial-safe substitute:
  - UCI Pen Digits `0.6173x`
- Cross-runtime parity:
  - Python/WASM/Swift hash parity `PASS`
  - PyO3 build/import `PASS`
  - C# managed-runtime header probe `PASS`
- Remaining open blockers:
  - direct UNIPEN access
  - direct IAM online-stroke closure
  - non-Latin online-stroke closure
  - PencilKit device-level validation

## My Recommendation

Run the next phase as a hard-authority closure phase, not as a product-polish phase.

Priority order:

1. Close direct IAM and UNIPEN access or prove decisively that those rows are structurally unreachable.
2. Add one real non-Latin online-stroke corpus and rerun the same-corpus pack.
3. Only after that decide whether the best wedge is:
   - enterprise transport kernel
   - tokenizer/data substrate
   - selected interoperability surface

What I would not do next:

- broaden adapter work before the hard-corpus blocker moves
- market the current lane as a primitive-token kernel
- spend time on cosmetic docs or release framing while `handoff_manifest.json` still says `NO-GO`
