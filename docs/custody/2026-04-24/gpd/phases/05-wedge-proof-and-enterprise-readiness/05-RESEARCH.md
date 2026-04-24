# Phase 05 Research

## Objective

Determine whether any narrow commercial wedge survives after Phase 03 external closure and Phase 04 candidate-branch execution, while preserving the contradiction-first contract and the active `LicenseRef-Zer0pa-SAL-6.0` posture.

## Evidence Baseline

### Authority and contradiction anchors

- `ZPE-Ink/proofs/reruns/benchmark_freeze_local/baseline_results.json`
  - structured tier: sovereign `zpe_ink=5.590209480060199x`
  - structured engineering comparator: `brotli=6.825565026256283x`
  - hard corpus: `MathWriting=1.0944074088858728x`, `CROHME=1.301456280301924x`
- `ZPE-Ink/proofs/reruns/benchmark_freeze_local/claim_scope_map.json`
  - broad claim verdict: `FAIL`
  - structured-tier-only qualifier remains mandatory
  - release-ready or enterprise-ready language is explicitly blocked
- `ZPE-Ink/proofs/reruns/contradiction_resolution_local/contradiction_resolution_manifest.json`
  - overall current verdict: `INCONCLUSIVE`
  - release surface verdict: `FAIL`
  - sovereign `GO/NO-GO`: `NO-GO`

### External closure anchors

- `ZPE-Ink/proofs/reruns/phase3_external/blind_clone_verdict.json`
  - blind clone is partially closed but still `INCONCLUSIVE`
  - remaining failure: `gate_a_setup.py` aborts on missing optional `npm`
- `ZPE-Ink/proofs/reruns/phase3_external/calliar_benchmark.json`
  - real non-Latin evidence exists, but only at `2.774608127006351x`

### Candidate-branch anchors

- `.gpd/phases/04-runtime-challenger-and-token-branches/04-01-SUMMARY.md`
  - primitive-token candidate beats `brotli` on the structured tier
  - bounded Calliar fidelity is disqualifying
- `.gpd/phases/04-runtime-challenger-and-token-branches/04-02-SUMMARY.md`
  - tokenizer scaffold exists
  - tokenizer remains scaffold evidence, not wedge closure

## Action Brief Reconciliation

The 2026-04-05 action brief contributes useful candidate work, but it is not contract-sovereign. It contains three classes of input:

1. **Potential interoperability work**
   - Swift decoder
   - C# decoder
   - cross-runtime parity harness
2. **Potential benchmark/diagnostic work**
   - public handwriting datasets
   - MathWriting gap analysis
3. **Packaging / surface hygiene**
   - README cross-link

### Stale or conflicting assumptions in the brief

- The brief points to commit `0353ec2`, but the live repo `HEAD` is `98b5ed73473540667b65d7bd519c2980ff2c188d`.
- The current local worktree has uncommitted deletions for:
  - `ZPE-Ink/code/bindings/swift/ZPEInk.swift`
  - `ZPE-Ink/code/bindings/csharp/ZpeInk.cs`
  - `ZPE-Ink/code/zpe_ink/codec.py`
  - additional WASM/python-native/core files
- `git ls-tree -r HEAD` confirms those files still exist in `HEAD`, so the brief is partially aligned to repository history, but not to the active working tree.
- The repo PRD has been reduced to a legacy stub; the real truth surface now lives in `README.md`, `docs/DOC_REGISTRY.md`, and `proofs/README.md`.

## Wedge Lane Assessment

### 1. Transport wedge

**Current status:** narrow transport truth only, not a surviving commercial wedge.

Why it fails Phase 05 as a wedge:
- hard-corpus evidence remains weak
- frozen `brotli` still beats the sovereign runtime on the structured tier
- contradiction and release surfaces remain open / fail

What survives:
- a truthful statement that the kernel remains above `5x` on the structured tier and preserves transport gates

### 2. Tokenizer wedge

**Current status:** not viable as a current wedge.

Why it fails:
- only a bounded QuickDraw scaffold proof exists
- no authority carry-over to harder corpora or revenue-bearing posture
- explicit Phase 04 summary already blocks promotion

### 3. Interoperability wedge

**Current status:** narrowest plausible future wedge, but not yet proven.

Why it is the strongest candidate:
- the action brief's A1-A3 items point directly at a concrete product family: a cross-runtime ink interchange kit
- the contract explicitly asks Phase 05 to decide whether the wedge belongs to transport, tokenizer, or interoperability
- an interoperability wedge can stay narrow and license-correct under SAL-v6

Why it still fails today:
- current local worktree deletes the very binding files the brief wants to extend
- Swift and C# in `HEAD` are still header-level probes rather than full parity implementations
- enterprise-readiness language would outrun the actual proof surface

### 4. Dataset-expansion lane

**Current status:** diagnostic only, not a wedge by itself.

Why it matters:
- CROHME-like work and MathWriting gap analysis can sharpen blocker intelligence

Why it is not Phase 05 closure:
- additional benchmark breadth does not itself create a surviving commercial wedge
- it mainly informs follow-on research after a `NO-GO` or a narrowed candidate decision

## Recommended Phase 05 Split

### 05-01: Prove or narrow the first commercial wedge

Do not implement the brief blindly. Instead:
- audit the action brief against repo truth
- evaluate transport, tokenizer, and interoperability lanes against the actual contract
- decide whether any lane survives now or only as a future candidate

Primary expected result:
- `NO_CURRENT_WEDGE_PROVEN`
- `INTEROPERABILITY` identified as the narrowest future candidate, but blocked by repo-state divergence and missing decoder parity work

### 05-02: Publish final enterprise-readiness and go/no-go decision

Use 05-01 outputs plus the phase 1-4 evidence bundle to publish:
- wedge proof memo
- enterprise boundary note
- final go/no-go surface

Primary expected result:
- final enterprise verdict remains `NO-GO`
- final enterprise-readiness status remains `NOT_READY`
- next honest follow-on is a candidate interoperability rehabilitation branch, not a release surface upgrade

## Acceptance Tests to Carry Into Planning

- the phase must name one surviving wedge or explicitly reject all current wedges
- the final verdict must be singular and machine-readable
- the final memo must preserve SAL-v6, structured-tier-only qualifier discipline, and contradiction visibility
- the action brief must be downgraded from “execution checklist” to “candidate input” wherever it conflicts with live repo truth

## Forbidden Proxies

- “full cross-runtime parity” claimed from header stubs or deleted local files
- “enterprise readiness” inferred from docs cleanup, package availability, or private-repo hygiene
- “wedge proved” inferred from candidate-branch benchmarks that already failed promotion
- “brief says implement” treated as sufficient reason to override the live contract
