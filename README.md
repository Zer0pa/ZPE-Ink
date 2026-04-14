<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>

# ZPE-Ink

Deterministic digital-ink codec centered on the `.zpink` packet format. This repo is a private staging snapshot with a current proof subset and rerun surface. It is not release-ready.

<p>
  <img src=".github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>

## What This Is

Cross-runtime deterministic ink codec. 1.0–2.8× compression on real public corpora; 5.59× on structured tier vs raw float32 xy-only baseline. The `.zpink` packet format encodes stroke streams — pressure, tilt, timing — identically across every runtime. Same input, same output, iOS to Web to Android. Strokes are tokenised using 8-direction Freeman chain codes packed as 4-bit nibbles.

ZPE-Ink targets annotation-runtime teams and cross-platform pen-input infrastructure where ink fidelity matters and generic codecs destroy structural detail. Validated through Calliar non-Latin corpus. Bindings surface: Rust, WASM, Swift, C#.

**Readiness: private-stage.** Structured-tier transport proved. Sovereign release surface remains FAIL.

| Field | Value |
|-------|-------|
| Architecture | STROKE_MANIFOLD |
| Encoding | INK_DELTA_V1 |

## Key Metrics

| Metric | Value | Baseline |
|--------|-------|----------|
| STRUCT_CR | 5.59× | structured tier, synthetic data, vs raw float32 xy-only baseline |
| REAL_CR | 1.02–2.77× | 5 public datasets (MathWriting, CROHME, QuickDraw, DigiLeTs, Calliar) |
| PARITY | 3/3 | Py/Rust/WASM decode |
| BINDINGS | 5 | Py/Rust/WASM/Swift/C# |
| GATES | 4/6 | sovereign surface FAIL |

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

> Auditable guarantees backed by committed proof artifacts. Start at `AUDITOR_PLAYBOOK.md`.

- Structured-tier compression exceeds 5× vs raw float32
- Python/Rust/WASM decode parity passes locally
- Swift/C# header contracts pass (magic, version, header size)
- Structured tier ratio: 5.59×

<p>
  <img src=".github/assets/readme/section-bars/open-risks-non-blocking.svg" alt="OPEN RISKS (NON-BLOCKING)" width="100%">
</p>

## What We Don't Claim

- No claim of release readiness (release surface FAIL)
- No claim of blind-clone closure (INCONCLUSIVE)
- No claim of hard-corpus pass
- No claim of general digital-ink dominance
- 5× compression on real handwriting data — structured-tier 5.59× applies to synthetic data against a raw float32 xy-only baseline; real public corpora achieve 1.0–2.8×

<p>
  <img src=".github/assets/readme/section-bars/quickstart-and-authority-point.svg" alt="QUICKSTART AND AUTHORITY POINT" width="100%">
</p>

## Commercial Readiness

| Field | Value |
|-------|-------|
| Verdict | INCONCLUSIVE |
| Commit SHA | 98b5ed734735 |
| Confidence | 67% |
| Source | proofs/INK_WAVE1_RELEASE_READINESS_REPORT.md |

> **Evaluators:** Proof surface available for inspection. Sovereign surface FAIL — see Open Risks. Contact hello@zer0pa.com.

Current authority reflects the latest committed verification surface. It does not imply release readiness.
Confidence basis: 4/6 verification checks currently PASS.

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
| V_02 | Python/Rust/WASM parity | PASS |
| V_03 | Swift/C# header contracts | PASS |
| V_04 | Pytest regression surface | PASS |
| V_05 | Sovereign release surface | FAIL |
| V_06 | Blind-clone closure | INC |

## Proof Anchors

| Path | State |
|------|-------|
| proofs/INK_WAVE1_RELEASE_READINESS_REPORT.md | VERIFIED |
| proofs/runbooks/20260321T005520Z_codex_receipt.md | VERIFIED |
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
| Proof Anchors | 6 |
| Modality Lanes | 6 |
| Authority Source | proofs/INK_WAVE1_RELEASE_READINESS_REPORT.md |

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
| Documentation index | `docs/README.md` |
| Auditor path | `AUDITOR_PLAYBOOK.md` |
| Governance rules | `GOVERNANCE.md` |
| Release gate rules | `RELEASING.md` |
| Contribution workflow | `CONTRIBUTING.md` |
| Security policy | `SECURITY.md` |
| Support routing | `docs/SUPPORT.md` |

## Who This Is For

| | |
|---|---|
| **Ideal first buyer** | Stylus/annotation runtime team or cross-platform pen-input infrastructure team |
| **Pain** | Ink streams vary across runtimes — iOS, Web, Android — requiring per-platform codecs with no determinism guarantee |
| **Deployment** | SDK — Python package with repo-local Rust/WASM/Swift/C# bindings |
| **Family position** | Secondary product candidate in the Zer0pa deterministic encoding family. Not the lead commercial front door |
