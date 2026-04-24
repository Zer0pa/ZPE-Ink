# Ink Token Augmentation Runbook

## Purpose

Design and, when explicitly authorized, execute the narrow candidate augmentation path for ZPE-Ink that adds an integer-canvas or binary/discrete codebook interchange layer without displacing the sovereign `.zpink` surface.

## Owner / Agent Type

Research-implementation hybrid agent.

## Input Artifacts

- approved follow-on decision artifact
- approved augmented PRD
- proof/validation rerun packet
- candidate corpus plan
- current packet-contract docs

## Output Artifacts

- candidate design note
- corpus/benchmark manifest
- compatibility spec
- candidate proof bundle
- kill-condition review

## Acceptance Gate

- Candidate layer is explicitly branch-only or candidate-only.
- Candidate layer preserves current `.zpink` round-trip and parity guarantees.
- Candidate benchmark packet names exact corpora and retrieval/comparison protocol.
- Candidate value is measured against a bounded audience/use case, not against a broad product story.

## Failure Mode

- candidate layer replaces `.zpink` authority by implication
- corpus plan relies on unavailable or unlicensed datasets
- integer-canvas or codebook design cannot preserve runtime-stable semantics
- retrieval/token claims outrun measured evidence

## Execution Surface

- Mac required: yes for initial prototyping and bounded benchmarks
- RunPod required: only if later pretraining/corpus volume exceeds local lane
- Hugging Face required: yes for large corpora, checkpoints, and benchmark bundles

## Procedure

1. Choose one candidate path after the follow-on decision:
   - integer-canvas tokenization
   - binary/discrete codebook tokenization
   - hybrid token layer alongside `.zpink`
2. Freeze the baseline:
   - current `.zpink` packet contract
   - current parity surface
   - current truth matrix
3. Define corpus scope:
   - in-lane public corpora only at first
   - future external/private corpora only after approval
4. Define one benchmark family:
   - interchange determinism
   - retrieval/search utility
   - compatibility with trajectory/ink-token literature
5. Write explicit kill conditions before implementation begins.

## ZPE-Ink Specific Gates

- Candidate branch must not weaken the existing narrow interchange wedge.
- Any claim of InkML successor, InkSight compatibility, or foundation-model readiness must remain future-facing until proven.
- Candidate corpora and outputs must have HF custody destinations before large execution starts.

## Kill Conditions

- If a candidate token surface cannot maintain deterministic runtime parity, stop.
- If local corpora are insufficient to test the candidate honestly and no approved external path exists, stop.
- If the candidate path depends on remote compute before the local CPU lane is exhausted, stop.
