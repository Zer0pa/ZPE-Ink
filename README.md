<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>

# ZPE-Ink

Deterministic digital-ink codec centered on the `.zpink` packet format. ZPE-Ink is a live beta proof surface: useful now for bounded transport and proof inspection, still under active authority tightening before any broader release claim.

<p>
  <img src=".github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>

## What This Is

Cross-runtime deterministic ink codec. Current authority preserves a structured-tier transport pass at `5.5902x` versus the raw float32 `x/y` baseline, plus a bounded UJI Pen Characters public row at `1.6111x` exact roundtrip. The core `.zpink` packet format carries `x`, `y`, `pressure`, optional `tilt`, and optional `azimuth` through a deterministic header and delta-RLE payload contract.

ZPE-Ink targets annotation-runtime teams and cross-platform pen-input infrastructure where ink fidelity and deterministic interchange matter. The installable release unit is the Python package under `code/`. Rust, WASM, Swift, and C# remain repo-local verification and contract surfaces. A separate tokenizer lane maps stroke motion into 8-direction primitives packed as 4-bit nibbles; that lane is real, but it is not the sovereign transport claim.

**Public posture: always in beta.** Useful now for bounded transport and inspection. Current sovereign authority remains `NO-GO`, so the repo does not claim release-ready or enterprise-ready status.

| Field | Value |
|-------|-------|
| Architecture | STROKE_MANIFOLD |
| Encoding | INK_DELTA_V1 |
| Primitive scope | 8-direction tokenizer lane in `code/zpe_ink/primitivetoken.py`; core transport lives in `code/zpe_ink/codec.py` |
| Current authority scope | structured-tier transport plus bounded public UJI row |

## Key Metrics

| Metric | Value | Baseline |
|--------|-------|----------|
| STRUCT_CR | 5.5902x | structured tier, synthetic data, versus raw float32 `x/y` baseline |
| RUNTIME_PARITY | 3/3 | Python/Rust/WASM byte-identical parity surface |
| HARD_CORPUS | 1.0944x-1.3015x | MathWriting and CROHME rows in `claim_scope_map.json` |
| UJI_PUBLIC | 1.6111x | exact roundtrip on `1,364` UJI samples / `74,592` points |

## Competitive Benchmarks

> Structured tier; version-locked tools. Source: [`proofs/reruns/benchmark_freeze_local/`](proofs/reruns/benchmark_freeze_local/)

| Tool | Ratio | Notes |
|------|-------|-------|
| Brotli (q11) | **6.83×** | wins structured tier |
| **ZPE-Ink** | **5.59×** | 5 runtimes; deterministic |
| zstd (l19) | 4.92× | — |
| LZ4 (l9) | 1.99× | — |

Brotli wins on ratio. ZPE-Ink's distinct surface is deterministic multi-channel transport and runtime contract design, not structured-tier ratio leadership.

## What We Prove

> Auditable guarantees backed by committed proof artifacts. Start at `proofs/reruns/phase5_wedge/final_go_no_go_surface.json`.

- Structured-tier transport above `5x` versus raw float32 `x/y`
- Bounded UJI Pen Characters row at `1.6111x` exact roundtrip
- Binding contract alignment across Python, PyO3, WASM, Swift, and C#
- Blind-clone install, roundtrip, and `pytest` execution on an untouched host
- 8-direction tokenizer lane with retained pressure, tilt, and azimuth side channels

<p>
  <img src=".github/assets/readme/section-bars/open-risks-non-blocking.svg" alt="OPEN RISKS (NON-BLOCKING)" width="100%">
</p>

## What We Don't Claim

- Release-ready or enterprise-ready posture
- Hard-corpus superiority
- Structured-tier ratio leadership over Brotli
- Blind-clone closure
- Cross-script authority closure
- Tokenizer scaffold as a current commercial wedge

<p>
  <img src=".github/assets/readme/section-bars/quickstart-and-authority-point.svg" alt="QUICKSTART AND AUTHORITY POINT" width="100%">
</p>

## Commercial Readiness

| Field | Value |
|-------|-------|
| Verdict | STAGED |
| Commit SHA | d452733e8c74 |
| Confidence | 82% |
| Source | proofs/reruns/phase5_wedge/final_go_no_go_surface.json |

> **Evaluators:** Proof surface available for inspection. `STAGED` is the website enum for the bounded beta proof surface; the governing sovereign authority remains `NO-GO` / `FAIL`. Contact hello@zer0pa.com.

Commercial readiness reflects the bounded beta surface, not a closed release gate. Current authority still supports only structured-tier transport plus the bounded public UJI row, while the contradiction surface and blind-clone surface remain open.

<p>
  <img src=".github/assets/readme/zpe-masthead-option-3-2.gif" alt="ZPE-Ink Masthead Option 3.2" width="100%">
</p>

<p>
  <img src=".github/assets/readme/section-bars/lane-status-snapshot.svg" alt="LANE STATUS SNAPSHOT" width="100%">
</p>

## Tests and Verification

| Code | Check | Verdict |
|------|-------|---------|
| V_01 | Structured-tier compression boundary | PASS |
| V_02 | Bounded public UJI row with exact roundtrip | PASS |
| V_03 | Binding contract alignment (`zpink-v1`) | PASS |
| V_04 | Historical regression and cross-runtime baseline logs | PASS |
| V_05 | Blind-clone closure | INC |
| V_06 | Sovereign release gate | FAIL |

## Proof Anchors

| Path | State |
|------|-------|
| proofs/reruns/phase5_wedge/final_go_no_go_surface.json | CURRENT |
| proofs/reruns/benchmark_freeze_local/claim_scope_map.json | CURRENT |
| proofs/reruns/contradiction_resolution_local/contradiction_resolution_manifest.json | CURRENT |
| proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json | CURRENT |
| proofs/reruns/phase3_external/blind_clone_verdict.json | CURRENT |
| proofs/logs/20260321_technical_alignment_cross_runtime.json | HISTORICAL_VERIFIED |
| proofs/logs/20260321_technical_alignment_binding_contracts.json | HISTORICAL_VERIFIED |
| proofs/logs/20260321_technical_alignment_pytest.txt | HISTORICAL_VERIFIED |

Any contradiction across the current anchors keeps the release gate open.

<p>
  <img src=".github/assets/readme/section-bars/repo-shape.svg" alt="REPO SHAPE" width="100%">
</p>

## Repo Shape

| Field | Value |
|-------|-------|
| Proof Anchors | 8 |
| Runtime Surfaces | 5 |
| Authority Source | proofs/reruns/phase5_wedge/final_go_no_go_surface.json |

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

Verification anchors: `proofs/logs/20260321_technical_alignment_pytest.txt`, `proofs/logs/20260321_technical_alignment_wheel_install.txt`.

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
| Packet contract | `docs/family/ZPINK_INTERFACE_CONTRACT.md` |
| Auditor path | `proofs/reruns/phase5_wedge/final_go_no_go_surface.json` |
| Benchmark summary | `proofs/artifacts/public_benchmarks/README.md` |
| Historical release note | `docs/family/ZPINK_RELEASE_NOTE.md` |
| Support routing | `docs/LEGAL_BOUNDARIES.md` |

## Who This Is For

| | |
|---|---|
| **Ideal first buyer** | Stylus/annotation runtime team or cross-platform pen-input infrastructure team |
| **Pain** | Ink streams vary across runtimes — iOS, Web, Android — requiring per-platform codecs with no determinism guarantee |
| **Deployment** | SDK — Python package with repo-local Rust/WASM/Swift/C# bindings |
| **Portfolio position** | Independent encoding product in the ZPE portfolio; current authority supports bounded beta evaluation, not a closed commercial wedge |
