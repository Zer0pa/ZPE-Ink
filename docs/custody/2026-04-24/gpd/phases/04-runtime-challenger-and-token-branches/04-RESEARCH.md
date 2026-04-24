# Phase 04 Research

Date: 2026-03-21
Phase: `04-runtime-challenger-and-token-branches`

## Question

What is the strongest honest Phase 04 engineering lane now that Phase 03 is complete: a candidate primitive-token runtime branch, a tokenizer scaffold, or a cross-repo GPD integration push?

## Live Facts

- The authoritative lane is still the current ZPE Ink workspace and inner repo:
  - workspace: `/Users/Zer0pa/ZPE/ZPE Ink`
  - repo: `/Users/Zer0pa/ZPE/ZPE Ink/ZPE-Ink`
- The current sovereign gate is still narrow:
  - structured-tier `zpe_ink`: `5.590209480060199x`
  - structured-tier `brotli`: `6.825565026256283x`
  - MathWriting: `1.0944074088858728x`
  - CROHME: `1.301456280301924x`
  - Calliar: `2.774608127006351x`
- The blind-clone npm crash is no longer a live code blocker in this repo:
  - `code/scripts/shared.py` already catches `FileNotFoundError`
  - `code/scripts/gate_a_setup.py` exits `0` even when `npm` is absent from `PATH`
- The only canonical telemetry constants found in this workstream are Comet constants:
  - workspace: `zer0pa`
  - project: `zpe-ink`
  - source: `ZPE-Ink/code/scripts/log_current_state_to_comet.py`
- There is no Opik surface anywhere in the current workstream.
- Local disk is healthy for bounded Phase 04 branch work:
  - `/` free space is roughly `21.28 GiB`
- External execution is only partially live:
  - RunPod direct TCP is reachable at `38.80.152.72:30709`
  - the current pod has only `1.8 GiB` free and therefore fails the brief's `5 GiB` floor
  - `COMET_API_KEY` is not exported in this shell
  - `RUNPOD_API_KEY` is not exported in this shell

## Research Conclusions

- The current lane can and should execute the candidate runtime and tokenizer branch work locally now.
- The current lane should not treat the user-supplied `psi-oss/get-physics-done` integration brief as the authoritative Phase 04 closure surface:
  - it points at a different repo and branch,
  - it is useful as engineering intent,
  - but the authoritative phase gate for this lane still lives in `ZPE-Ink/` and `.gpd/`.
- The honest Phase 04 job is therefore:
  - implement a candidate primitive-token branch inside `ZPE-Ink/code/zpe_ink/`
  - benchmark it against the frozen sovereign runtime and `brotli`
  - scaffold a tokenizer artifact with a real corpus proof
  - record the telemetry constants and external-credential reality without fabricating Comet or Opik closure
- Frozen Phase 02 artifacts should stay frozen. Phase 04 should write sidecar artifacts rather than mutating the historical claim-scope surface in place.

## What Phase 04 Must Produce

- A candidate-only primitive-token runtime module, tests, and benchmark artifact.
- A candidate-only tokenizer module, tests, and corpus proof artifact.
- A phase-local telemetry and state sidecar that records:
  - canonical Comet constants,
  - Opik absence,
  - credential presence or absence,
  - candidate-branch result interpretation.
- Honest plan summaries that do not promote candidate work into sovereign runtime truth.

## What Phase 04 Must Not Pretend

- It must not rewrite the sovereign runtime identity based on a candidate branch.
- It must not treat missing Comet or RunPod credentials as if telemetry or fresh-pod closure happened.
- It must not mutate the frozen Phase 02 claim-scope artifact just to make the branch look integrated.
- It must not blur the current lane with the external `psi-oss/get-physics-done` repo.

## Carry-Forward Implication

- Phase 04 can advance honestly on the local Mac lane even if external telemetry and fresh RunPod pod provisioning remain unavailable in this shell.
- If the primitive-token candidate fails to beat `brotli`, that is still a valid engineering result and must be published as such.
- If the tokenizer scaffold ships cleanly, that supports the branch program, not the sovereign authority claim.
