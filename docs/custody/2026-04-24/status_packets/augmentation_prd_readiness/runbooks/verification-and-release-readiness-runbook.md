# Verification And Release-Readiness Runbook

## Purpose

Produce the bounded decision that says whether ZPE-Ink remains closed, reopens as a narrow interoperability lane, or needs only a branch-level follow-on.

## Owner / Agent Type

Verifier or senior review agent.

## Input Artifacts

- truth matrix
- reconciliation note
- local CPU rerun manifest
- implementation outputs, if any
- [final_go_no_go_surface.json](/Users/Zer0pa/ZPE/ZPE%20Ink/ZPE-Ink/proofs/reruns/phase5_wedge/final_go_no_go_surface.json)
- [blind_clone_verdict.json](/Users/Zer0pa/ZPE/ZPE%20Ink/ZPE-Ink/proofs/reruns/phase3_external/blind_clone_verdict.json)

## Output Artifacts

- updated decision packet
- milestone or branch recommendation
- release/readme guidance
- residual-risk note

## Acceptance Gate

The new verdict is valid only if:

- it is explicitly grounded in fresh evidence
- it remains narrower than current public wording
- it keeps hard-corpus weakness and blind-clone incompleteness visible
- it does not conflate local technical success with commercial readiness

## Failure Mode

- local parity success is treated as current market closure
- archived `NO-GO` is displaced without a replacement artifact
- readiness language broadens ahead of evidence

## Execution Surface

- Mac required: yes
- RunPod required: conditional only if the decision depends on remote-only evidence
- Hugging Face required: yes for final large proof bundles

## Procedure

1. Read the truth matrix and rerun manifest together.
2. Compare them to Phase 05 artifacts.
3. Decide one of:
   - continue closure
   - open a narrow branch only
   - open a bounded interoperability phase
4. If the result is not closure, write the exact boundary:
   - what is in scope
   - what is explicitly out of scope
   - what evidence is still missing
5. Produce front-door guidance, but do not publish it yet.

## ZPE-Ink Specific Gates

- `README` and `market_surface.json` cannot be upgraded ahead of the decision artifact.
- Enterprise-readiness remains blocked unless blind-clone and contradiction surfaces are explicitly closed.
- Hard-corpus compression claims remain bounded even if the interchange lane reopens.

## Kill Conditions

- If the fresh packet still supports only `NO-GO`, stop and keep closure.
- If the packet supports a branch but not a milestone, do not escalate to roadmap change.
