# ZPE-Ink Runbook Index

## 1. Repo Truth And Governance Runbook

- Purpose: reconcile live repo truth against archived authority artifacts and enforce repo/governance discipline before any reopening.
- Owner/agent type: senior execution agent or planner with repo/governance authority.
- Input artifacts: archived `NO-GO` packet, README, market surface, architecture doc, license/package metadata, GPD state, repo playbook, ethos, mechanics audit brief.
- Output artifacts: truth matrix, reconciliation note, contradiction ledger, governance compliance notes.
- Acceptance gate: every contradiction is classified and no public-facing surface outruns the sovereign decision.
- Failure mode: unresolved contradiction, claim inflation, or parser-breaking front-door edits.
- Requires: Mac yes, RunPod no, HF only for large output bundles.

## 2. Artifact And HF Custody Runbook

- Purpose: ensure all large proofs, corpora, rerun bundles, and future augmentation artifacts have live HF custody under `Zer0pa`.
- Owner/agent type: execution agent with HF operational access.
- Input artifacts: current HF custody report, local proof tree, future large outputs, corpus manifests.
- Output artifacts: HF custody manifest, live target verification, upload receipts, residual-risk note.
- Acceptance gate: no valuable large artifact remains only on Mac or remote scratch without live HF verification.
- Failure mode: wrong namespace, incomplete upload, unverified target, or GitHub-class material incorrectly diverted to HF.
- Requires: Mac yes, RunPod only if remote salvage exists, HF yes.

## 3. Proof And Validation Runbook

- Purpose: refresh the local CPU proof surface and measure whether the interchange lane is actually still viable.
- Owner/agent type: execution or verification agent.
- Input artifacts: test suite, parity test, binding-contract script, package build/install workflow, prior proof logs.
- Output artifacts: rerun manifest, timing/results packet, discrepancy list, updated evidence bundle.
- Acceptance gate: tests/build/parity either pass cleanly or fail in a precisely classified way.
- Failure mode: ambiguous failure classification, skipped parity without explanation, or silent downgrade of the authority metric.
- Requires: Mac yes, RunPod no for first pass, HF for large proof bundles.

## 4. Implementation Runbook

- Purpose: carry out the bounded engineering slice approved after the follow-on decision.
- Owner/agent type: implementation agent with verification support.
- Input artifacts: approved PRD, GPD execution plan, truth matrix, rerun manifest, decision artifact.
- Output artifacts: scoped code/docs/proof changes for the approved slice only.
- Acceptance gate: implementation stays inside the approved lane and preserves current sovereign guarantees.
- Failure mode: widening into commercialization, branch confusion, or regressions against existing `.zpink` authority.
- Requires: Mac yes, RunPod conditional, HF conditional.

## 5. Verification And Release-Readiness Runbook

- Purpose: verify whether the bounded execution wave justifies reopening, continued closure, or a narrower branch-only outcome.
- Owner/agent type: verifier or senior review agent.
- Input artifacts: truth matrix, rerun manifest, implementation outputs, prior Phase 05 artifacts.
- Output artifacts: decision packet, updated readiness note, release/readme guidance.
- Acceptance gate: new verdict is explicitly narrower than current public surfaces and evidence-backed.
- Failure mode: narrative upgrade without decisive evidence or confusion between local technical success and market readiness.
- Requires: Mac yes, RunPod conditional, HF for final large bundles.

## 6. Ink Token Augmentation Runbook

- Purpose: design and, when authorized, execute the candidate augmentation path for integer-canvas or binary/discrete codebook interchange without disturbing the sovereign runtime surface.
- Owner/agent type: implementation/research hybrid agent.
- Input artifacts: approved augmentation decision, corpus plan, token/codebook design note, parity constraints.
- Output artifacts: candidate branch design, benchmark packet, compatibility note, kill-condition check.
- Acceptance gate: candidate layer coexists with `.zpink` authority and proves bounded value without widening claims.
- Failure mode: parity regression, codebook/token layer drift, or inability to justify the candidate over current interchange truth.
- Requires: Mac yes for initial work, RunPod conditional for large-scale corpus or pretraining, HF yes for corpora/checkpoints/proof bundles.
