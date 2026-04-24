<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>

# ZPE-Ink

<p align="left">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-SAL%20v6.2-e5e7eb?labelColor=111111" alt="License: SAL v6.2"></a>
</p>

Deterministic digital-ink codec centered on the `.zpink` packet format. Always-in-beta: current proof subset and rerun surface are live and auditable, while the sovereign commercial verdict remains `NO-GO`.

<p>
  <img src=".github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>

## What This Is

Cross-runtime deterministic ink codec for stroke streams carrying xy geometry, pressure, tilt, and timing. The `.zpink` packet format serializes those fields identically across every runtime, with 8-direction Freeman chain codes packed as 4-bit nibbles on the stroke path.

The current public surface is bounded and mechanical: 1.0–2.8× compression on carried real public corpora, 1.6111× exact roundtrip on the UJI Pen Characters row, and 5.59× on the structured tier vs raw float32 xy-only baseline. It is aimed at annotation and pen-input infrastructure where stroke identity matters more than generic media compression. Bindings surface: Rust, WASM, Swift, C#.

**Readiness: always-in-beta.** Structured-tier transport proved. Sovereign release surface remains FAIL / NO-GO. The only reopened lane is a bounded interoperability follow-on with a candidate-only token sidecar.

| Field | Value |
|-------|-------|
| Architecture | STROKE_MANIFOLD |
| Encoding | INK_DELTA_V1 |

## Key Metrics

| Metric | Value | Baseline |
|--------|-------|----------|
| STRUCT_CR | 5.59× | structured tier, synthetic data, vs raw float32 xy-only baseline |
| REAL_CR | 1.02–2.77× | 5 public datasets (MathWriting, CROHME, QuickDraw, DigiLeTs, Calliar) |
| UJI_PUBLIC | 1.6111× | exact roundtrip on bounded UJI Pen Characters public row |
| PARITY | 4 runtimes | Py/WASM/Swift/C# decode parity on the 2026-04-24 local rerun |
| TOKEN_SIDECAR | candidate-only | exact on directional/proxy fixtures; degrades on adversarial spikes |

## Competitive Benchmarks

> Structured tier; version-locked tools. Source: [`proofs/reruns/benchmark_freeze_local/`](proofs/reruns/benchmark_freeze_local/)

| Tool | Ratio | Notes |
|------|-------|-------|
| Brotli (q11) | **6.83×** | wins structured tier |
| **ZPE-Ink** | **5.59×** | 5 runtimes; deterministic |
| zstd (l19) | 4.92× | — |
| LZ4 (l9) | 1.99× | — |

Brotli wins on ratio; ZPE-Ink wins on cross-runtime parity and deterministic encode.

## What We Prove

> Auditable guarantees backed by committed proof artifacts. Start at `proofs/reruns/follow_on_reassessment_2026-04-24/interoperability_candidate_verdict.json`.

- Structured-tier compression exceeds 5× vs raw float32
- Python/WASM/Swift/C# decode parity passes locally
- Binding contracts pass for Python native, WASM, Swift, and C#
- Structured tier ratio: 5.59×
- UJI Pen Characters public row: 1.6111× with exact roundtrip on `1,364` samples / `74,592` points
- Candidate token sidecar is deterministic and exact on directional/proxy fixtures, but not promotable as a general-fidelity runtime

<p>
  <img src=".github/assets/readme/section-bars/open-risks-non-blocking.svg" alt="OPEN RISKS (NON-BLOCKING)" width="100%">
</p>

## What We Don't Claim

- No claim of release readiness (release surface FAIL)
- No claim of blind-clone closure (INCONCLUSIVE)
- No claim of hard-corpus pass
- No claim of general digital-ink dominance
- 5× compression on real handwriting data — structured-tier 5.59× applies to synthetic data against a raw float32 xy-only baseline; real public corpora achieve 1.0–2.8×
- No claim that the UJI Pen Characters row closes release readiness, hard-corpus authority, or the sovereign gate

<p>
  <img src=".github/assets/readme/section-bars/quickstart-and-authority-point.svg" alt="QUICKSTART AND AUTHORITY POINT" width="100%">
</p>

## Commercial Readiness

| Field | Value |
|-------|-------|
| Sovereign Verdict | NO-GO |
| Enterprise Readiness | NOT_READY |
| Current Wedge | NONE_PROVEN |
| Follow-on Lane | OPEN_BOUNDED_CANDIDATE |
| Commit SHA | 8919e0d8df28 |
| Source | proofs/reruns/follow_on_reassessment_2026-04-24/interoperability_candidate_verdict.json |

## Tests and Verification

| Code | Check | Verdict |
|------|-------|---------|
| V_01 | Structured-tier compression boundary | PASS |
| V_02 | Python/WASM/Swift/C# parity | PASS |
| V_03 | Binding contracts | PASS |
| V_04 | Pytest regression surface | PASS |
| V_05 | Package build and install smoke | PASS |
| V_06 | Blind-clone closure | INC |
| V_07 | Sovereign release surface | FAIL / NO-GO |
| V_08 | Candidate token sidecar fit | CANDIDATE_ONLY |

## Proof Anchors

| Path | State |
|------|-------|
| proofs/reruns/follow_on_reassessment_2026-04-24/interoperability_candidate_verdict.json | CURRENT |
| proofs/reruns/follow_on_reassessment_2026-04-24/local_cpu_rerun_manifest.json | CURRENT |
| proofs/reruns/follow_on_reassessment_2026-04-24/repo_truth_matrix.json | CURRENT |
| proofs/reruns/follow_on_reassessment_2026-04-24/token_sidecar_candidate_verdict.json | CURRENT |
| proofs/reruns/phase5_wedge/final_go_no_go_surface.json | HISTORICAL_SOVEREIGN_CLOSEOUT |
| proofs/reruns/benchmark_freeze_local/claim_scope_map.json | CURRENT |
| proofs/reruns/contradiction_resolution_local/contradiction_resolution_manifest.json | CURRENT |
| proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json | CURRENT |
| proofs/logs/20260321_technical_alignment_cross_runtime.json | HISTORICAL_VERIFIED |
| proofs/logs/20260321_technical_alignment_binding_contracts.json | HISTORICAL_VERIFIED |

Any contradiction across these anchors keeps the repo `NO-GO` for a current wedge and blocks promotion of the bounded follow-on lane.

<p>
  <img src=".github/assets/readme/section-bars/repo-shape.svg" alt="REPO SHAPE" width="100%">
</p>

## Repo Shape

| Field | Value |
|-------|-------|
| Proof Anchors | 10 |
| Modality Lanes | 6 |
| Authority Source | proofs/reruns/follow_on_reassessment_2026-04-24/interoperability_candidate_verdict.json |

<p>
  <img src=".github/assets/readme/zpe-masthead-option-3-3.gif" alt="ZPE-Ink Masthead Option 3.3" width="100%">
</p>

## Quick Start

```bash
# Install from PyPI
pip install zpe-ink
```

Or install from source (development). Prereqs: Python 3.11+, Rust toolchain, and `wasm32-unknown-unknown` target for binding checks.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e './code[dev]'
python -m pytest code/tests -q
python -m zpe_ink demo
python -m zpe_ink verify-roundtrip
```

| Field | Value |
|-------|-------|
| Repository URL | `https://github.com/Zer0pa/ZPE-Ink` |
| Contact | `architects@zer0pa.ai` |

Verification anchors: `proofs/reruns/follow_on_reassessment_2026-04-24/local_cpu_rerun_manifest.json`, `proofs/reruns/follow_on_reassessment_2026-04-24/token_sidecar_candidate_verdict.json`.

<p>
  <img src=".github/assets/readme/section-bars/contributing-security-support.svg" alt="CONTRIBUTING, SECURITY, SUPPORT" width="100%">
</p>

## Ecosystem

- [ZPE-IMC](https://github.com/Zer0pa/ZPE-IMC) - reference repo for shared documentation layout and proof-surface conventions.
- [ZPE-Mocap](https://github.com/Zer0pa/ZPE-Mocap) - adjacent motion-stream codec in the ZPE transport family.
- [ZPE-XR](https://github.com/Zer0pa/ZPE-XR) - sibling XR motion compression surface with multi-runtime packaging work.

**Observability:** [Comet dashboard](https://www.comet.com/zer0pa/zpe-ink/view/new/panels) (public)

| Route | Target |
|-------|--------|
| Documentation index | `docs/ARCHITECTURE.md` |
| Auditor path | `proofs/reruns/follow_on_reassessment_2026-04-24/interoperability_candidate_verdict.json` |
| Governance rules | `GOVERNANCE.md` |
| Release gate rules | `RELEASING.md` |
| Contribution workflow | `CONTRIBUTING.md` |
| Security policy | `SECURITY.md` |
| Support routing | `docs/LEGAL_BOUNDARIES.md` |

## Who This Is For

| | |
|---|---|
| **Ideal first buyer** | Stylus/annotation runtime team or cross-platform pen-input infrastructure team |
| **Pain** | Ink streams vary across runtimes — iOS, Web, Android — requiring per-platform codecs with no determinism guarantee |
| **Deployment** | SDK — Python package with repo-local Rust/WASM/Swift/C# bindings |
| **Follow-on candidate** | Candidate-only token sidecar for bounded interchange indexing on directional/proxy corpora |
| **Family position** | Secondary product candidate in the Zer0pa deterministic encoding family. Not the lead commercial front door |
