---
phase: draft-follow-on-interoperability-truth-reconciliation
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - .gpd/drafts/2026-04-23-zpe-ink-reality-reconciliation.md
  - ZPE-Ink/proofs/reruns/follow_on_reassessment_2026-04-23/repo_truth_matrix.json
  - ZPE-Ink/proofs/reruns/follow_on_reassessment_2026-04-23/local_cpu_rerun_manifest.json
  - ZPE-Ink/proofs/reruns/follow_on_reassessment_2026-04-23/interoperability_candidate_verdict.json
  - .gpd/drafts/2026-04-23-next-milestone-note.md
interactive: false

conventions:
  units: "verdict classes, seconds, ratios, and explicit pass/fail gate states"
  metric: "truth-surface consistency before reopening any commercial or interoperability lane"
  coordinates: "screen Cartesian"

contract:
  schema_version: 1
  scope:
    question: Does the current April 23 repo state justify reopening a narrow interoperability candidate lane, or does the honest verdict remain NO-GO after truth-surface reconciliation and a fresh local CPU rerun?
  claims:
    - id: claim-truth-reconciliation
      statement: The current repo, proof, and market surfaces can be reconciled into one bounded truth surface that names exactly which archived assumptions are stale and which remain governing.
      deliverables: [deliv-reality-note, deliv-truth-matrix]
      acceptance_tests: [test-truth-matrix, test-reality-note]
      references: [ref-state, ref-final-go-no-go, ref-readme, ref-market-surface, ref-license, ref-action-brief]
    - id: claim-local-rerun
      statement: The current local M1 lane is sufficient to rerun the decisive interoperability-facing proof surface, and any remaining blocker can be expressed as a local storage/build issue rather than a GPU or pod dependency.
      deliverables: [deliv-rerun-manifest]
      acceptance_tests: [test-local-rerun]
      references: [ref-architecture, ref-parity-test, ref-cross-runtime-log, ref-binding-log]
    - id: claim-follow-on-decision
      statement: A new milestone should be opened only if the reconciled truth surface and fresh local rerun both support a narrower interoperability candidate without overriding the sovereign NO-GO and hard-corpus constraints.
      deliverables: [deliv-interoperability-verdict, deliv-milestone-note]
      acceptance_tests: [test-follow-on-decision]
      references: [ref-final-go-no-go, ref-market-surface, ref-cross-runtime-log, ref-blind-clone]
  deliverables:
    - id: deliv-reality-note
      kind: report
      path: .gpd/drafts/2026-04-23-zpe-ink-reality-reconciliation.md
      description: Human-readable note reconciling current repo truth with the frozen Phase 05 closeout assumptions.
    - id: deliv-truth-matrix
      kind: report
      path: ZPE-Ink/proofs/reruns/follow_on_reassessment_2026-04-23/repo_truth_matrix.json
      description: Machine-readable matrix of every contradiction across README, market surface, license metadata, GPD state, and proof artifacts.
    - id: deliv-rerun-manifest
      kind: report
      path: ZPE-Ink/proofs/reruns/follow_on_reassessment_2026-04-23/local_cpu_rerun_manifest.json
      description: Local CPU rerun status for pytest, cross-runtime parity, binding contracts, package build, and any blocking storage facts.
    - id: deliv-interoperability-verdict
      kind: report
      path: ZPE-Ink/proofs/reruns/follow_on_reassessment_2026-04-23/interoperability_candidate_verdict.json
      description: Decision artifact naming whether interoperability is still only a future candidate, a reopened bounded lane, or still blocked.
    - id: deliv-milestone-note
      kind: report
      path: .gpd/drafts/2026-04-23-next-milestone-note.md
      description: Recommendation on whether to open a new milestone or keep the workstream closed.
  references:
    - id: ref-state
      kind: prior_artifact
      locator: .gpd/STATE.md
      role: definition
      why_it_matters: Carries the archived Phase 05 final decision and open questions.
      applies_to: [claim-truth-reconciliation]
      must_surface: true
      required_actions: [read, compare, cite]
    - id: ref-final-go-no-go
      kind: prior_artifact
      locator: ZPE-Ink/proofs/reruns/phase5_wedge/final_go_no_go_surface.json
      role: benchmark
      why_it_matters: Remains the sovereign final verdict until a new decision artifact replaces it honestly.
      applies_to: [claim-truth-reconciliation, claim-follow-on-decision]
      must_surface: true
      required_actions: [read, compare, cite]
    - id: ref-readme
      kind: prior_artifact
      locator: ZPE-Ink/README.md
      role: benchmark
      why_it_matters: Current public-facing surface contains live wording that may contradict the final go/no-go artifact.
      applies_to: [claim-truth-reconciliation]
      must_surface: true
      required_actions: [read, compare, classify]
    - id: ref-market-surface
      kind: prior_artifact
      locator: ZPE-Ink/docs/market_surface.json
      role: benchmark
      why_it_matters: Encodes the repo's explicit commercial wedge language and license metadata.
      applies_to: [claim-truth-reconciliation, claim-follow-on-decision]
      must_surface: true
      required_actions: [read, compare, classify]
    - id: ref-license
      kind: prior_artifact
      locator: ZPE-Ink/LICENSE
      role: definition
      why_it_matters: The legal surface is authoritative and currently diverges from README badge text.
      applies_to: [claim-truth-reconciliation]
      must_surface: true
      required_actions: [read, compare, cite]
    - id: ref-action-brief
      kind: prior_artifact
      locator: /Users/Zer0pa/ZPE/ZPE Ink/ZPE-Ink_ACTION_BRIEF.md
      role: candidate_input
      why_it_matters: The brief contains stale assumptions that must be classified rather than executed blindly.
      applies_to: [claim-truth-reconciliation]
      must_surface: true
      required_actions: [read, compare, classify]
    - id: ref-architecture
      kind: prior_artifact
      locator: ZPE-Ink/docs/ARCHITECTURE.md
      role: benchmark
      why_it_matters: Documents the officially claimed runtime surfaces and currently understates live parity evidence.
      applies_to: [claim-local-rerun]
      must_surface: true
      required_actions: [read, compare, cite]
    - id: ref-parity-test
      kind: prior_artifact
      locator: ZPE-Ink/code/tests/test_cross_runtime_parity.py
      role: definition
      why_it_matters: Shows that Swift and C# decode parity can be exercised locally on this machine.
      applies_to: [claim-local-rerun]
      must_surface: true
      required_actions: [read, run, cite]
    - id: ref-cross-runtime-log
      kind: prior_artifact
      locator: ZPE-Ink/proofs/logs/20260321_technical_alignment_cross_runtime.json
      role: benchmark
      why_it_matters: Supplies the prior parity-ready evidence surface that the rerun must confirm or narrow.
      applies_to: [claim-local-rerun, claim-follow-on-decision]
      must_surface: true
      required_actions: [read, compare, cite]
    - id: ref-binding-log
      kind: prior_artifact
      locator: ZPE-Ink/proofs/logs/20260321_technical_alignment_binding_contracts.json
      role: benchmark
      why_it_matters: Anchors binding consistency expectations before any new interoperability conclusion.
      applies_to: [claim-local-rerun]
      must_surface: true
      required_actions: [read, compare, cite]
    - id: ref-blind-clone
      kind: prior_artifact
      locator: ZPE-Ink/proofs/reruns/phase3_external/blind_clone_verdict.json
      role: benchmark
      why_it_matters: Any reopened wedge still remains subordinate to the external blind-clone incompleteness.
      applies_to: [claim-follow-on-decision]
      must_surface: true
      required_actions: [read, compare, cite]
  acceptance_tests:
    - id: test-truth-matrix
      subject: claim-truth-reconciliation
      kind: consistency
      procedure: Compare README, market surface, architecture doc, license metadata, action brief, and Phase 05 artifacts line-by-line.
      pass_condition: Every contradiction is classified as stale artifact, stale doc claim, live repo truth, or unresolved blocker with no silent smoothing.
      evidence_required: [deliv-truth-matrix, ref-readme, ref-market-surface, ref-license, ref-final-go-no-go]
      automation: hybrid
    - id: test-reality-note
      subject: claim-truth-reconciliation
      kind: human_review
      procedure: Read the truth matrix and write one bounded narrative note.
      pass_condition: The note names what changed since Phase 05 and what still governs the workstream.
      evidence_required: [deliv-reality-note, deliv-truth-matrix, ref-state]
      automation: hybrid
    - id: test-local-rerun
      subject: claim-local-rerun
      kind: benchmark
      procedure: Rerun local pytest, cross-runtime parity, binding contracts, and package build after clearing sufficient temp space; record exact timings and blockers.
      pass_condition: CPU-only local verification either passes end-to-end or fails on an explicit local storage/build blocker, with no GPU or pod dependency introduced.
      evidence_required: [deliv-rerun-manifest, ref-parity-test, ref-cross-runtime-log, ref-binding-log]
      automation: hybrid
    - id: test-follow-on-decision
      subject: claim-follow-on-decision
      kind: human_review
      procedure: Read the truth matrix and rerun manifest, then decide whether a new milestone is justified.
      pass_condition: The verdict stays narrower than current market-surface wording and never upgrades enterprise or broad commercial posture by implication.
      evidence_required: [deliv-interoperability-verdict, deliv-milestone-note, deliv-rerun-manifest, ref-final-go-no-go, ref-blind-clone]
      automation: hybrid
  forbidden_proxies:
    - id: fp-doc-polish
      subject: claim-truth-reconciliation
      proxy: Treating README or badge cleanup as resolution of the underlying truth-surface contradiction.
      reason: Surface polish is not evidence.
    - id: fp-pod-escalation
      subject: claim-local-rerun
      proxy: Escalating to GPU, RunPod, or other external compute before exhausting the local CPU rerun and storage fix.
      reason: The verified code path is CPU-only and current blockers are local.
    - id: fp-commercial-upgrade
      subject: claim-follow-on-decision
      proxy: Treating cross-runtime parity or a narrow interoperability candidate as proof of current commercial readiness.
      reason: Phase 05 sovereign verdict remains NO-GO until replaced by a new coherent decision artifact.
  links:
    - id: link-truth-matrix
      source: claim-truth-reconciliation
      target: deliv-truth-matrix
      relation: supports
      verified_by: [test-truth-matrix]
    - id: link-rerun-manifest
      source: claim-local-rerun
      target: deliv-rerun-manifest
      relation: supports
      verified_by: [test-local-rerun]
    - id: link-follow-on-verdict
      source: claim-follow-on-decision
      target: deliv-interoperability-verdict
      relation: supports
      verified_by: [test-follow-on-decision]
  uncertainty_markers:
    weakest_anchors: ["Package build/install is currently blocked by a near-full local disk, so installable-surface confirmation is not fresh yet."]
    disconfirming_observations: ["The fresh local rerun fails on a functional parity or build defect that is not explained by storage alone.", "The reconciled truth surface still supports only NO-GO with no bounded interoperability reopening."]
---

<!-- Review-only draft. Not yet part of ROADMAP.md and does not revise the closed milestone. -->

<objective>
Reconcile the live ZPE-Ink repo truth with the frozen Phase 05 closeout, then decide whether a new bounded interoperability follow-on is justified.

Purpose: prevent stale artifacts, outdated wedge language, or storage noise from driving the next milestone.
Output: one truth-reconciliation packet, one fresh local CPU rerun manifest, and one follow-on decision note.
</objective>

<execution_context>
@/Users/prinivenpillay/.codex/get-physics-done/workflows/execute-plan.md
@/Users/prinivenpillay/.codex/get-physics-done/templates/summary.md
</execution_context>

<context>
@.gpd/PROJECT.md
@.gpd/STATE.md
@.gpd/phases/05-wedge-proof-and-enterprise-readiness/05-02-SUMMARY.md
@ZPE-Ink/README.md
@ZPE-Ink/docs/ARCHITECTURE.md
@ZPE-Ink/docs/market_surface.json
@ZPE-Ink/LICENSE
@ZPE-Ink/code/tests/test_cross_runtime_parity.py
@ZPE-Ink/proofs/logs/20260321_technical_alignment_cross_runtime.json
@ZPE-Ink/proofs/reruns/phase5_wedge/final_go_no_go_surface.json
@ZPE-Ink/proofs/reruns/phase3_external/blind_clone_verdict.json
@/Users/Zer0pa/ZPE/ZPE Ink/ZPE-Ink_ACTION_BRIEF.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Build the repo-truth reconciliation matrix</name>
  <files>.gpd/drafts/2026-04-23-zpe-ink-reality-reconciliation.md, ZPE-Ink/proofs/reruns/follow_on_reassessment_2026-04-23/repo_truth_matrix.json</files>
  <action>Compare the current repo branch, README, architecture doc, market surface, license metadata, action brief, and Phase 05 decision artifacts. Record every contradiction across verdicts, license versions, runtime-surface claims, and buyer/wedge language.</action>
  <verify>Keep the final go/no-go artifact sovereign unless a newer evidence-backed artifact explicitly supersedes it. Mark each mismatch as stale closeout assumption, stale live doc, or unresolved blocker.</verify>
  <done>The project has one auditable matrix showing what is current truth, what is stale, and what must be fixed before any new commercial or interoperability claim is allowed.</done>
</task>

<task type="auto">
  <name>Task 2: Clear the local storage blocker and rerun the CPU-only proof surface</name>
  <files>ZPE-Ink/proofs/reruns/follow_on_reassessment_2026-04-23/local_cpu_rerun_manifest.json</files>
  <action>Free enough local temp space to run the supported packaging path, then rerun pytest, cross-runtime parity, binding-contract verification, wheel or sdist build, and install smoke on the Mac M1 lane.</action>
  <verify>Record exact timings, whether Swift/C#/WASM parity executed rather than skipped, and whether any failure is a functional bug or only a storage/build-environment problem.</verify>
  <done>The compute boundary is explicit: either the local CPU lane is sufficient, or the remaining blocker is stated precisely without hand-waving toward GPU or pod usage.</done>
</task>

<task type="auto">
  <name>Task 3: Re-evaluate the interoperability candidate and decide on a new milestone</name>
  <files>ZPE-Ink/proofs/reruns/follow_on_reassessment_2026-04-23/interoperability_candidate_verdict.json, .gpd/drafts/2026-04-23-next-milestone-note.md</files>
  <action>Use the truth matrix and the fresh local rerun to classify interoperability as still blocked, reopened as a bounded candidate lane, or not worth reopening. Then decide whether the next honest move is a new milestone, a narrow branch, or continued closure.</action>
  <verify>Do not let docs language, parity success, or branch cleanliness stand in for commercial proof. Keep hard-corpus weakness, blind-clone incompleteness, and the sovereign NO-GO surface visible.</verify>
  <done>The workstream has one bounded decision on whether follow-on work exists and what exact shape it should take.</done>
</task>

</tasks>

<verification>
No external compute, GPU, or RunPod escalation is allowed unless Task 2 proves a real non-local blocker after storage cleanup. No reopened wedge or buyer language is allowed unless it stays narrower than the current market surface and remains consistent with the sovereign NO-GO and blind-clone constraints.
</verification>

<success_criteria>
The current repo truth is reconciled against archived Phase 05 assumptions, the local CPU verification surface is rerun on a cleaned machine, and the project ends with one explicit answer: open a new bounded interoperability milestone, open a narrower branch, or keep the workstream closed.
</success_criteria>

<output>
After completion, create `.gpd/drafts/2026-04-23-follow-on-interoperability-truth-reconciliation-SUMMARY.md`.
</output>
