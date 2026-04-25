# ZPE-Ink

ZPE-Ink is an always-in-beta `.zpink` digital-ink codec surface. This README only states claims that are backed by committed proof artifacts and CI tests in this repository.

License: see `LICENSE`.

## What This Is

ZPE-Ink provides Python encode/decode commands for deterministic `.zpink` stroke packets. The tested claim surface is intentionally narrow:

- lossless encode/decode roundtrip for generated stroke fixtures
- CRC and truncated-payload rejection
- optional pressure, tilt, and azimuth channel handling
- static binding-contract consistency across the Python, PyO3, WASM, Swift, and C# surfaces

The committed public benchmark artifacts are in `proofs/` and their compression-ratio results are surfaced below. CI does not rerun those external corpora; the benchmark rows are static committed artifacts.

## Encoding Contract

| Claim | Proof artifact | CI test |
|---|---|---|
| `.zpink` lossless roundtrip is bit-exact for generated fixtures | `proofs/logs/20260321_technical_alignment_pytest.txt` | `code/tests/test_codec_roundtrip.py::test_lossless_roundtrip_bit_exact` |
| Corrupted or truncated payloads are rejected | `proofs/logs/20260321_technical_alignment_pytest.txt` | `code/tests/test_codec_roundtrip.py::test_crc_tamper_detection`, `code/tests/test_codec_roundtrip.py::test_reject_truncated_payload` |
| zero-valued optional channels can be omitted without changing decoded strokes | `proofs/logs/20260321_technical_alignment_pytest.txt` | `code/tests/test_codec_roundtrip.py::test_zero_optional_channels_are_omitted_by_default` |
| binding headers and package version are contract-consistent | `proofs/logs/20260321_technical_alignment_binding_contracts.json` | `code/tests/test_binding_contracts.py::test_repo_binding_contracts_pass` |
| CLI demo and roundtrip entry points execute | `proofs/logs/20260321_technical_alignment_wheel_install.txt` | `code/tests/test_cli.py` |

## Public Benchmark Results

These rows are committed static artifacts. The codec ran `encode → decode → verify` on each dataset using the repo-local lossless path. CI does not rerun these external corpora; results are bounded to the sample sizes shown.

| Dataset | Samples | Compression ratio | Max Hausdorff (px) | Roundtrip fidelity | Proof artifact |
|---|---:|---:|---:|---|---|
| UJI Pen Characters | 1,364 | **1.6111×** | 0.0 | exact | `proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json` |
| CROHME (ICFHR package) | 90 | **1.4360×** | 0.0 | exact | `proofs/artifacts/public_benchmarks/dataset_matrix.json` |
| DigiLeTs | 180 | **1.0891×** | 0.0 | exact | `proofs/artifacts/public_benchmarks/dataset_matrix.json` |
| MathWriting excerpt | 70 | **1.1870×** | 0.0 | exact | `proofs/artifacts/public_benchmarks/dataset_matrix.json` |
| QuickDraw (cat) | 256 | **1.0181×** | 0.0 | exact | `proofs/artifacts/public_benchmarks/dataset_matrix.json` |
| IAM On-Line | — | — | — | skipped: registration-gated | `proofs/artifacts/public_benchmarks/dataset_matrix.json` |
| UNIPEN | — | — | — | skipped: host unavailable | `proofs/artifacts/public_benchmarks/dataset_matrix.json` |

Baseline: raw little-endian float32 x/y pairs per point. Hausdorff = 0.0 on all measured datasets means decoded coordinates match the source integers exactly.

**Zero-channel suppression improvement (committed):** auto-suppressing zero tilt/azimuth streams raised CROHME mean compression from 1.52× to 1.76× (max 3.34×) and MathWriting mean from 1.06× to 1.15×. This change is captured in `proofs/artifacts/mathwriting_analysis/comparison.json` and exercised by `code/tests/test_codec_roundtrip.py::test_zero_optional_channels_are_omitted_by_default`.

Encode latency on the measured corpora: median 0.02–0.10 ms/stroke (single-core Python, macOS; QuickDraw low end 0.026 ms/stroke, MathWriting high end 0.099 ms/stroke). Source: `proofs/artifacts/public_benchmarks/dataset_matrix.json` (`median_ms_per_stroke` field).

These results do not constitute a hard-corpus pass, release-readiness claim, or competitive superiority claim. See `proofs/artifacts/public_benchmarks/README.md` for full methodology notes.

## Commercial Readiness

No commercial-readiness or release-readiness claim is made from this README. Release validation remains bounded by `proofs/release_validation/README.md`.

## What We Do Not Claim

- No claim of release readiness
- No claim of blind-clone closure
- No claim of hard-corpus pass
- No claim of general digital-ink dominance
- No claim that the public benchmark rows close release readiness or hard-corpus authority
- No claim that local binding-contract checks prove full runtime parity for every downstream environment
- No claim that committed compression ratios on the above datasets constitute superiority over general-purpose codecs on those corpora

## Quick Start

Development install:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e './code[dev]'
python -m pytest code/tests -q
python -m zpe_ink demo
python -m zpe_ink verify-roundtrip
```

Package build:

```bash
python -m build
```

## Repository Links

| Field | Value |
|---|---|
| Repository | `https://github.com/Zer0pa/ZPE-Ink` |
| Issues | `https://github.com/Zer0pa/ZPE-Ink/issues` |
| Contact | `architects@zer0pa.ai` |
