# Requirements: ZPE-Digital-Ink

**Defined:** 2026-03-20
**Core Research Question:** Can ZPE-Digital-Ink become a contradiction-free, same-corpus-honest, commercially disruptive ink utility kernel, or must the claim stay narrowly scoped to structured-tier transport plus explicit candidate branches?

## Primary Requirements

### Authority Surface

- [ ] **AUTH-01**: Preserve `AM-INK-01 >= 5.0x` on the structured tier against the frozen raw float32 baseline.
- [ ] **AUTH-02**: Preserve exact roundtrip, fidelity, pressure, latency, and declared cross-runtime parity while running any new benchmark or kernel change.
- [ ] **AUTH-03**: Keep the `5x` figure permanently qualified as `structured-ink tier only` unless hard-corpus evidence independently earns a broader claim.

### Contradiction Resolution

- [ ] **FZ09-01**: Parse the current PASS and `NO-GO` surfaces into an explicit blocker ledger with one status per blocker.
- [ ] **FZ09-02**: Classify each unresolved blocker as code bug, missing artifact, claim-scope issue, external-access dependency, or not-viable path.
- [ ] **FZ09-03**: Produce a replacement contradiction-resolution handoff artifact that removes ambiguous `FAIL`/`PASS` coexistence for the same gate.

### Environment and Reproducibility

- [ ] **ENV-01**: Verify the M1-local toolchain with tests, package metadata check, and wheel build using a repo-scoped workflow or an explicitly justified equivalent.
- [ ] **ENV-02**: Track storage usage and delete non-essential large outputs during execution.
- [ ] **ENV-03**: Keep GitHub linkage and Comet logging current for the live evidence surface.

### Comparator Freeze

- [ ] **COMP-01**: Freeze the comparator stack for same-corpus accounting: raw float32 baseline, `zstd`, `brotli`, and `lz4`.
- [ ] **COMP-02**: Record comparator versions and rerun structured-tier comparisons under the frozen stack.
- [ ] **COMP-03**: Ensure comparator-freeze results preserve `AUTH-01` without hidden byte-accounting drift.

### Hard-Corpus Honesty

- [ ] **HCOR-01**: Rerun MathWriting and CROHME under the frozen comparator stack with exact byte accounting.
- [ ] **HCOR-02**: Write a claim-scope artifact that blocks broad handwriting-compression claims when hard-corpus evidence stays weak.
- [ ] **HCOR-03**: Keep structured-tier and hard-corpus surfaces separate in every summary, review pack, and handoff.

### External Boundary Control

- [ ] **EXTB-01**: Treat Red Magic, broader corpora, Apple-device checks, and RunPod as later-boundary work unless they are actually available in-lane.
- [ ] **EXTB-02**: Prompt the user before any RunPod usage or any action that crosses the current local boundary.

## Follow-up Requirements

### Runtime and Token Branches

- **BRCH-01**: Implement a primitive-token or hybrid runtime challenger without mislabeling it as the sovereign runtime.
- **BRCH-02**: Scaffold a tokenizer branch only after authority truth and contradiction status are stable.

### External Closure

- **BLND-01**: Execute blind-clone verification on an untouched external host before any `GO` verdict.
- **BLND-02**: Extend hard-corpus closure to user-approved external datasets and non-Latin online-stroke surfaces.

### Commercial Wedge

- **WEDG-01**: Prove one narrow commercial wedge with honest license and standards posture.
- **WEDG-02**: Decide whether the wedge belongs to transport, tokenizer, or interoperability rather than assuming all three.

## Out of Scope

| Topic | Reason |
| ----- | ------ |
| Public release language | Blocked by FZ-09 and missing blind-clone verification |
| Silent relicensing or permissive-open assumptions | Current repo truth is SAL-v6 |
| RunPod-first execution | Violates the current local-first compute boundary |
| Blending structured-tier and hard-corpus ratios into one marketing number | Forbidden proxy |
| Treating the current runtime as already primitive-token | Runtime identity remains open |

## Accuracy and Validation Criteria

| Requirement | Accuracy Target | Validation Method |
| ----------- | --------------- | ----------------- |
| AUTH-01 | `>= 5.0x` structured-tier ratio | Frozen benchmark rerun against raw float32 baseline |
| AUTH-02 | Zero transport regressions | Pytest, parity checks, and benchmark gate outputs |
| FZ09-01 | No ambiguous blocker state | Parsed blocker ledger and contradiction-resolution manifest |
| COMP-01 | Comparator versions pinned exactly | Manifest file with versions and rerunnable harness |
| HCOR-01 | Exact same-corpus byte accounting | Per-file and aggregate benchmark artifacts |
| HCOR-02 | Broad claims explicitly blocked when needed | `claim_scope_map` or equivalent artifact |
| ENV-02 | Storage stays within the live lane envelope | `df`, `du`, cleanup log, and artifact inventory |

## Contract Coverage

| Requirement | Decisive Output / Deliverable | Anchor / Benchmark / Reference | Prior Inputs / Baselines | False Progress To Reject |
| ----------- | ----------------------------- | ------------------------------ | ------------------------ | ------------------------ |
| AUTH-01 | Structured-tier freeze benchmark | `ink_compression_benchmark.json`, PRD | Phase 1 local proof bundle | Moving the baseline or counting bytes differently |
| AUTH-03 | Claim-scope artifact | PRD, review pack, release report | Phase 1 summaries | Using `5x` without the structured-tier qualifier |
| FZ09-01 | Contradiction blocker ledger | `handoff_manifest.json`, `quality_gate_scorecard.json` | `claim_status_delta.md`, `blockers_before_after.json` | Hand-waving the contradiction as “just docs” |
| ENV-01 | Environment verification report | repo package metadata, tests, wheel output | current working tree | Treating the current shell as equivalent to a reproducible setup without proof |
| COMP-01 | Comparator manifest | raw float32, zstd, brotli, lz4 | Phase 1 transport artifacts | Freezing versions after the benchmark instead of before it |
| HCOR-01 | Hard-corpus benchmark artifact | MathWriting, CROHME | Phase 1 corpus caches | Reusing proxy metrics and renaming them hard-corpus truth |
| EXTB-02 | Boundary note or user prompt | current compute map | disk/device status, ADB state | Quietly crossing into RunPod or unattached hardware work |

## Traceability

| Requirement | Phase | Status |
| ----------- | ----- | ------ |
| AUTH-01 | Phase 2: Contradiction Resolution and Honest Benchmark Freeze | Pending |
| AUTH-02 | Phase 2: Contradiction Resolution and Honest Benchmark Freeze | Pending |
| AUTH-03 | Phase 2: Contradiction Resolution and Honest Benchmark Freeze | Pending |
| FZ09-01 | Phase 2: Contradiction Resolution and Honest Benchmark Freeze | Pending |
| FZ09-02 | Phase 2: Contradiction Resolution and Honest Benchmark Freeze | Pending |
| FZ09-03 | Phase 2: Contradiction Resolution and Honest Benchmark Freeze | Pending |
| ENV-01 | Phase 2: Contradiction Resolution and Honest Benchmark Freeze | Pending |
| ENV-02 | Phase 2: Contradiction Resolution and Honest Benchmark Freeze | Pending |
| ENV-03 | Phase 2: Contradiction Resolution and Honest Benchmark Freeze | Pending |
| COMP-01 | Phase 2: Contradiction Resolution and Honest Benchmark Freeze | Pending |
| COMP-02 | Phase 2: Contradiction Resolution and Honest Benchmark Freeze | Pending |
| COMP-03 | Phase 2: Contradiction Resolution and Honest Benchmark Freeze | Pending |
| HCOR-01 | Phase 2: Contradiction Resolution and Honest Benchmark Freeze | Pending |
| HCOR-02 | Phase 2: Contradiction Resolution and Honest Benchmark Freeze | Pending |
| HCOR-03 | Phase 2: Contradiction Resolution and Honest Benchmark Freeze | Pending |
| EXTB-01 | Phase 3: External Corpora and Blind-Clone Closure | Pending |
| EXTB-02 | Phase 3: External Corpora and Blind-Clone Closure | Pending |
| BRCH-01 | Phase 4: Runtime Challenger and Token Branches | Pending |
| BRCH-02 | Phase 4: Runtime Challenger and Token Branches | Pending |
| BLND-01 | Phase 3: External Corpora and Blind-Clone Closure | Pending |
| BLND-02 | Phase 3: External Corpora and Blind-Clone Closure | Pending |
| WEDG-01 | Phase 5: Wedge Proof and Enterprise Readiness | Complete |
| WEDG-02 | Phase 5: Wedge Proof and Enterprise Readiness | Complete |

**Coverage:**

- Primary requirements: 17 total
- Mapped to phases: 17
- Unmapped: 0

---

_Requirements defined: 2026-03-20_
_Last updated: 2026-03-20 after contradiction-first project realignment._
