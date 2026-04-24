# Implementation Runbook

## Purpose

Execute the approved bounded engineering slice for ZPE-Ink after the follow-on decision gate, without widening beyond the evidence-backed lane.

## Owner / Agent Type

Implementation agent with verifier support.

## Input Artifacts

- approved augmented PRD
- approved GPD execution plan
- truth matrix
- local CPU rerun manifest
- interoperability decision artifact
- repo playbook / governance constraints

## Output Artifacts

- scoped code changes
- scoped docs updates
- new proof artifacts for the approved slice
- execution summary

## Acceptance Gate

- Implementation stays inside the approved lane:
  - truth reconciliation and rerun closure first
  - augmentation branch second only if approved
- No broad README or market-surface upgrade is allowed unless directly backed by the new decision artifact.
- Existing `.zpink` authority guarantees remain intact.

## Failure Mode

- candidate-branch work is treated as sovereign runtime truth
- docs are promoted before proof artifacts exist
- augmentation claims outrun hard-corpus or blind-clone boundaries
- GitHub mutation begins before the user authorizes execution or publish steps

## Execution Surface

- Mac required: yes
- RunPod required: conditional only for later large-corpus or remote-only evidence
- Hugging Face required: conditional for large corpora, bundles, or checkpoints

## Procedure

1. Execute repo-truth and proof runbooks first.
2. Read the resulting decision artifact.
3. If the decision says `keep closed`, stop.
4. If the decision says `branch only`, create implementation tasks only for that branch scope after user authorization.
5. If the decision says `bounded reopen`, implement only the approved slice:
   - truth-surface fixes
   - proof refresh
   - and optionally the approved candidate augmentation layer
6. Keep docs changes tightly subordinate to proof changes.

## ZPE-Ink Specific Gates

- No change may erase or weaken the Phase 05 negative artifacts.
- No change may relabel the current market wedge beyond deterministic multi-runtime interchange unless a fresh artifact says so.
- Any candidate token/codebook layer must be explicitly marked candidate-only until it earns its own acceptance gate.

## Kill Conditions

- If implementation requires broad repo restructuring to make progress, stop and split the work into a narrower branch or phase.
- If the candidate augmentation starts to compete with `.zpink` authority before the branch proves itself, stop and isolate it.
