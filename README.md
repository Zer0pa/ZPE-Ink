<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>

# ZPE-Ink

Deterministic digital-ink codec centered on the `.zpink` packet format. Always-in-beta: current proof subset and rerun surface are live and auditable.

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-SAL%20v7.0-e5e7eb?labelColor=111111" alt="License: SAL v7.0"></a>
</p>

<p>
  <img src=".github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>

## What This Is

Cross-runtime deterministic ink codec. The committed public benchmark surface spans 1.02–1.61× compression across five public datasets, with UJI Pen Characters at 1.6111× exact roundtrip. The `.zpink` packet format encodes stroke streams — pressure, tilt, timing — across Python, Rust, WASM, Swift, and C# bindings using 8-direction Freeman chain codes packed as 4-bit nibbles.

ZPE-Ink targets annotation-runtime teams and cross-platform pen-input infrastructure where ink fidelity matters and generic codecs destroy structural detail. The public proof surface in this repo is bounded to committed public-benchmark and technical-alignment artifacts.

**Readiness: always-in-beta.** Structured-tier transport proved. Sovereign release surface remains FAIL.

| Field | Value |
|-------|-------|
| Architecture | STROKE_MANIFOLD |
| Encoding | INK_DELTA_V1 |

## Key Metrics

| Metric | Value | Baseline |
|--------|-------|----------|
| PUBLIC_CR | 1.02–1.61× | 5 public datasets |
| UJI_PUBLIC | 1.6111× | exact roundtrip on bounded UJI Pen Characters public row |
| PARITY | 5/5 | Python, Rust, WASM, Swift, C# |
| CONTRACTS | 0 failures | binding contract checks |

> Source: `proofs/artifacts/public_benchmarks/README.md`, `proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json`, `proofs/logs/20260321_technical_alignment_cross_runtime.json`, `proofs/logs/20260321_technical_alignment_binding_contracts.json`

## What We Prove

> Auditable guarantees backed by committed public-benchmark and technical-alignment artifacts.

- Public benchmark corpus replay remains lossless across committed benchmarked datasets
- Python/Rust/WASM parity passes locally
- Swift/C# header contracts pass (magic, version, header size)
- UJI Pen Characters public row: 1.6111× with exact roundtrip on `1,364` samples / `74,592` points

<p>
  <img src=".github/assets/readme/section-bars/open-risks-non-blocking.svg" alt="OPEN RISKS (NON-BLOCKING)" width="100%">
</p>

## What We Don't Claim

- No claim of release readiness (release surface FAIL)
- No claim of blind-clone closure (INCONCLUSIVE)
- No claim of hard-corpus pass
- No claim of general digital-ink dominance
- No claim that the current public-benchmark surface closes release readiness or hard-corpus authority
- No claim that the UJI Pen Characters row closes release readiness, hard-corpus authority, or the sovereign gate

<p>
  <img src=".github/assets/readme/section-bars/quickstart-and-authority-point.svg" alt="QUICKSTART AND AUTHORITY POINT" width="100%">
</p>

## Commercial Readiness

| Field | Value |
|-------|-------|
| Verdict | INCONCLUSIVE |
| Commit SHA | 8cec1bcdcaef |
| Confidence | 67% |
| Source | proofs/release_validation/README.md |

## Tests and Verification

| Code | Check | Verdict |
|------|-------|---------|
| V_01 | Public benchmark roundtrip surface | PASS |
| V_02 | Python/Rust/WASM parity | PASS |
| V_03 | Swift/C# header contracts | PASS |
| V_04 | Pytest regression surface | PASS |
| V_05 | Release-validation surface | INC |
| V_06 | Blind-clone closure | INC |

## Proof Anchors

| Path | State |
|------|-------|
| proofs/release_validation/README.md | CURRENT |
| proofs/artifacts/public_benchmarks/README.md | CURRENT |
| proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json | CURRENT |
| proofs/logs/20260321_technical_alignment_cross_runtime.json | VERIFIED |
| proofs/logs/20260321_technical_alignment_binding_contracts.json | VERIFIED |
| proofs/logs/20260321_technical_alignment_pytest.txt | VERIFIED |
| proofs/logs/20260321_technical_alignment_wheel_install.txt | VERIFIED |

Any contradiction across these anchors keeps the repo `INCONCLUSIVE`.

<p>
  <img src=".github/assets/readme/section-bars/repo-shape.svg" alt="REPO SHAPE" width="100%">
</p>

## Repo Shape

| Field | Value |
|-------|-------|
| Proof Anchors | 7 |
| Modality Lanes | 6 |
| Authority Source | proofs/release_validation/README.md |

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
| Auditor path | `proofs/release_validation/README.md` |
| Security policy | `SECURITY.md` |
| Support routing | `docs/LEGAL_BOUNDARIES.md` |

## Who This Is For

| | |
|---|---|
| **Ideal first buyer** | Stylus/annotation runtime team or cross-platform pen-input infrastructure team |
| **Pain** | Ink streams vary across runtimes — iOS, Web, Android — requiring per-platform codecs with no determinism guarantee |
| **Deployment** | SDK — Python package with repo-local Rust/WASM/Swift/C# bindings |
| **Family position** | Secondary product candidate in the Zer0pa deterministic encoding family. Not the lead commercial front door |
