# ZPE-Ink

ZPE-Ink is an always-in-beta `.zpink` digital-ink codec — one of 17 independent encoding products in the Zer0pa portfolio. Every claim in this README is anchored to a committed proof artifact or CI test in this repository.

License: see `LICENSE`.

## What This Is

Deterministic stroke-packet codec. Bit-exact .zpink roundtrip with 0.0 Hausdorff error on measured datasets. Install from PyPI: `pip install zpe-ink`

- lossless encode/decode roundtrip for generated stroke fixtures - CRC and truncated-payload rejection - optional pressure, tilt, and azimuth channel handling - static binding-contract consistency across the Python, PyO3, WASM, Swift, and C# surfaces

The committed public benchmark artifacts are in `proofs/` and their compression-ratio results are surfaced below. CI does not rerun those external corpora; the benchmark rows are static committed artifacts.

## Codec Mechanics

<p>
  <img src=".github/assets/readme/lane-mechanics/INK.gif" alt="ZPE-Ink Codec Mechanics animation" width="100%">
</p>

| Field | Value |
| ------- | ------- |
| Architecture | STROKE_MANIFOLD |
| Encoding | INK_DELTA_V1 |
| Mechanics Asset | `.github/assets/readme/lane-mechanics/INK.gif` |

## Key Metrics

| Metric | Value | Baseline |
| -------- | ------- | ---------- |
| UJI Pen Characters compression ratio | 1.6111× | proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json |
| Max Hausdorff error (all measured corpora) | 0.0 px | proofs/artifacts/public_benchmarks/dataset_matrix.json |
| Measured samples (UJI corpus) | 1,364 | proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json |
| Encode latency | 0.02–0.10 ms/stroke | proofs/artifacts/public_benchmarks/dataset_matrix.json (median_ms_per_stroke) |

> Source: committed static benchmark artifacts at `proofs/artifacts/public_benchmarks/` and `proofs/reruns/phase3_public_benchmarks/`. CI does not rerun external corpora; results are bounded to the sample sizes shown.

## Repo Identity

| Field | Value |
| ------- | ------- |
| Identifier | ZPE-Ink |
| Repository | https://github.com/Zer0pa/ZPE-Ink |
| Section | encoding |
| Visibility | PUBLIC |
| Architecture | STROKE_MANIFOLD |
| Encoding | INK_DELTA_V1 |
| Commit SHA | 98b5ed734735 |
| License | SAL-7.0 |
| Authority Source | proofs/reruns/phase5_wedge/final_go_no_go_surface.json |

## Readiness

| Field | Value |
| ------- | ------- |
| Verdict | STAGED |
| Checks | 6/6 |
| Anchors | 6 display anchors |
| Commit | 98b5ed734735 |
| Authority | proofs/reruns/phase5_wedge/final_go_no_go_surface.json |

### Honest Blocker

No claim of release readiness (release surface FAIL); No claim of blind-clone closure (INCONCLUSIVE); No claim of hard-corpus pass

## What We Prove

- `.zpink` lossless roundtrip is bit-exact for all generated stroke fixtures — CRC-framed, structured-channel, not byte-opaque. Proof: `proofs/logs/20260321_technical_alignment_pytest.txt`
- Corrupted or truncated payloads are rejected by the codec before decoded data is returned. Proof: `proofs/logs/20260321_technical_alignment_pytest.txt`
- Zero-valued optional channels (tilt, azimuth) are suppressed by default without altering decoded strokes; zero-channel suppression raised CROHME mean compression from 1.52× to 1.76×. Proof: `proofs/artifacts/mathwriting_analysis/comparison.json`
- Binding headers and package version are contract-consistent across the Python, PyO3, WASM, Swift, and C# surfaces. Proof: `proofs/logs/20260321_technical_alignment_binding_contracts.json`
- Hausdorff error = 0.0 px on all five measured public corpora (UJI, CROHME, DigiLeTs, MathWriting, QuickDraw). Proof: `proofs/artifacts/public_benchmarks/dataset_matrix.json`

## What We Don't Claim

- No claim of release readiness
- No claim of blind-clone closure
- No claim of hard-corpus pass
- No claim of general digital-ink dominance
- No claim that the public benchmark rows close release readiness or hard-corpus authority
- No claim that local binding-contract checks prove full runtime parity for every downstream environment
- No claim that committed compression ratios on the above datasets constitute superiority over general-purpose codecs on those corpora

## Verification Status

| Code | Check | Verdict |
| ------ | ------- | --------- |
| V_01 | Bit-exact encode→decode roundtrip on generated fixtures | PASS |
| V_02 | Corrupted payloads are rejected before decode | PASS |
| V_03 | Truncated payloads are rejected | PASS |
| V_04 | Zero tilt/azimuth channels suppressed without altering decoded strokes | PASS |
| V_05 | Binding headers + package version are contract-consistent | PASS |
| V_06 | CLI demo and verify-roundtrip entry points execute | PASS |

## Proof Anchors

| Path | State |
| ------ | ------- |
| `proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json` | VERIFIED |
| `proofs/artifacts/public_benchmarks/dataset_matrix.json` | VERIFIED |
| `proofs/artifacts/public_benchmarks/README.md` | VERIFIED |
| `proofs/artifacts/comp_benchmarks/ink_codec_comparison.json` | VERIFIED |
| `proofs/artifacts/comp_benchmarks/ink_codec_comparison_real_corpora.json` | VERIFIED |
| `proofs/artifacts/comp_benchmarks/summary.md` | VERIFIED |

## Repo Shape

| Field | Value |
| ------- | ------- |
| Proof Anchors | 6 display anchors |
| Modality Lanes | 6 |
| Architecture | STROKE_MANIFOLD |
| Encoding | INK_DELTA_V1 |
| Verification | 6/6 checks |
| Authority Source | proofs/reruns/phase5_wedge/final_go_no_go_surface.json |

## Competitive Benchmarks

ZPE-Ink is a lossless CRC-framed structured-channel stroke codec — Hausdorff = 0.0 px on all measured corpora. Compression ratio is reported below for reference, but the product claim is structural fidelity + tamper detection, not CR dominance. The representative reference for non-fixture inputs is the real-public-corpora row block; the synthetic fixtures that follow are an RLE-friendly ceiling and are retained only as an upper-bound reference.

### Real public corpora (representative)

Same comparator path applied to two real public handwriting corpora. Real IAM remains registration-gated and real UNIPEN remains host-blocked (per the Public Benchmark Results table); QuickDraw and CROHME are downloadable.

| Corpus | Source | Samples | gzip CR | zlib CR | ZPE-Ink CR | Hausdorff (px) |
|---|---|---:|---:|---:|---:|---:|
| QuickDraw `cat` (simplified) | `storage.googleapis.com/quickdraw_dataset` | 50 | 2.248 | 2.872 | 2.535 | 0.0 |
| CROHME (ICFHR package) | `oldweb.isical.ac.in/~crohme/ICFHR_package.zip` | 50 | 3.541 | 3.878 | 4.077 | 0.0 |
| **Aggregate (bytes-weighted)** | — | 100 | **3.328** | **3.732** | **3.818** | **0.0** |

Methodology: same int32 little-endian buffer layout fed to all three codecs; per-sample `encode_zpink` for ZPE-Ink. QuickDraw simplified ndjson supplies (x, y) only — `pressure=512`, `tilt=0`, `azimuth=0` are stuffed into the buffer slots so shape matches; this advantages RLE on the constant channels and is reported as-found. Full byte-level table at `proofs/artifacts/comp_benchmarks/ink_codec_comparison_real_corpora.json`.

**Read this honestly.** On real handwriting the gap between ZPE-Ink and gzip/zlib is narrow — zlib is competitive on QuickDraw, ZPE-Ink leads on CROHME. These real-corpus numbers are the representative reference for non-fixture inputs. Lossless roundtrip (Hausdorff = 0.0) holds on both real corpora; that structural-fidelity property, not the CR delta, is the product claim.

### Synthetic ceiling fixtures (RLE-friendly by construction)

These ratios are measured on **in-repo synthetic stroke fixtures** designed to exercise the codec's integer-native delta+RLE path. They are NOT measured on real IAM, UNIPEN, CROHME, UJI, or QuickDraw corpora — note that real IAM and real UNIPEN are marked "skipped" in the Public Benchmark Results section above. Synthetic fixtures favor RLE-friendly inputs by design and should be read as a ceiling, not a representative ratio.

ZPE-Ink against general-purpose entropy coders on the lane's deterministic in-repo synthetic stroke fixtures (Wave-CB Phase 1). Apples-to-apples: every codec is fed the same byte buffer, an `int32` little-endian concatenation of `(x, y, pressure, tilt, azimuth)` per stroke. Hausdorff is the symmetric distance between original and decoded `(x, y)` loci in stroke-coordinate units (px).

| Codec | Aggregate CR (bytes-weighted) | Hausdorff Error (px) | Notes |
|---|---:|---:|---|
| gzip (level 6) | 7.336 | n/a (lossless byte stream, not stroke-aware) | Python `gzip.compress`, deterministic `mtime=0` |
| zlib (level 6) | 7.441 | n/a (lossless byte stream, not stroke-aware) | Python `zlib.compress` |
| ZPE-Ink (`.zpink`) | 12.735 | **0.0** on all 128 strokes | Lossless, CRC-framed, typed channels |

Headline values are the **bytes-weighted aggregate** ratio (`sum(raw_bytes) / sum(encoded_bytes)`) across both fixture sets — the industry-conventional aggregation for compression. The mean-of-per-set-means alternative (gzip 7.39 / zlib 7.51 / zpink 12.59) is also computable from the per-set entries in the committed artifact. Two fixture sets: `synthetic_directional_64a` (seed 20260220, 64 strokes) and `synthetic_directional_64b_sin_pressure` (seed 20260221, 64 strokes). Per-set per-stroke breakdowns and the full byte-level table are committed at `proofs/artifacts/comp_benchmarks/ink_codec_comparison.json`; the human-readable summary is at `proofs/artifacts/comp_benchmarks/summary.md`.

**Honest framing.** ZPE-Ink's product claim is *lossless roundtrip with structured semantics*, not raw CR dominance. The gzip/zlib comparators operate on opaque byte streams; ZPE-Ink operates on typed stroke channels with deterministic delta + RLE, CRC framing, and per-channel range validation. On these synthetic fixtures the typed approach happens to also dominate raw CR because the int32 channels are dense in small deltas — but no generalised CR-superiority claim is made and no claim is extended to real corpora outside this artifact. Where general-purpose coders compress better on a given corpus, that should be reported as-found.

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

## Upcoming Workstreams

This section captures the active lane priorities — what the next agent or contributor picks up, and what investors should expect. Cadence is continuous, not milestoned.

- **Real-corpus expansion (IAM unblock + UNIPEN mirror)** — Operations / External Dependency. IAM is registration-gated and UNIPEN host is unavailable; once unblocked, the existing comparator path runs as-is and produces the proper headline.

## License and Portfolio

License: SAL v7.1 — see `LICENSE`. ZPE-Ink is one of 17 codec lanes in the Zer0pa portfolio; repository index at `https://github.com/Zer0pa/ZPE-Ink`.

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

## Encoding Contract

| Claim | Proof artifact | CI test |
|---|---|---|
| `.zpink` lossless roundtrip is bit-exact for generated fixtures | `proofs/logs/20260321_technical_alignment_pytest.txt` | `code/tests/test_codec_roundtrip.py::test_lossless_roundtrip_bit_exact` |
| Corrupted or truncated payloads are rejected | `proofs/logs/20260321_technical_alignment_pytest.txt` | `code/tests/test_codec_roundtrip.py::test_crc_tamper_detection`, `code/tests/test_codec_roundtrip.py::test_reject_truncated_payload` |
| zero-valued optional channels can be omitted without changing decoded strokes | `proofs/logs/20260321_technical_alignment_pytest.txt` | `code/tests/test_codec_roundtrip.py::test_zero_optional_channels_are_omitted_by_default` |
| binding headers and package version are contract-consistent | `proofs/logs/20260321_technical_alignment_binding_contracts.json` | `code/tests/test_binding_contracts.py::test_repo_binding_contracts_pass` |
| CLI demo and roundtrip entry points execute | `proofs/logs/20260321_technical_alignment_wheel_install.txt` | `code/tests/test_cli.py` |

## Repository Links

| Field | Value |
|---|---|
| Repository | `https://github.com/Zer0pa/ZPE-Ink` |
| Issues | `https://github.com/Zer0pa/ZPE-Ink/issues` |
| License | SAL v7.1 — see `LICENSE` |
| Contact | `architects@zer0pa.ai` |
