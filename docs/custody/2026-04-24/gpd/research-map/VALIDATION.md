# Validation Surface

## Scope
- This report covers the validation and parity surfaces exercised by `tests/test_codec_roundtrip.py`, `scripts/run_all_gates.sh`, `scripts/gate_a_setup.py`, `scripts/gate_b_roundtrip.py`, `scripts/gate_c_benchmarks.py`, `scripts/gate_d_falsification.py`, `scripts/gate_e_cross_runtime.py`, `scripts/gate_e_net_new_ingestion.py`, `scripts/gate_m_maximalization.py`, `scripts/gate_f_commercial_closure.py`, and `scripts/generate_handoff.py`.
- Current evidence is stored under `artifacts/2026-02-20_zpe_ink_wave1/`.

## Unit and Roundtrip Checks
- `tests/test_codec_roundtrip.py` contains four checks: lossless bit-exact roundtrip, CRC tamper detection, truncated payload rejection, and finite high-mode decode.
- The test corpus is built from `generate_directional_stroke` in `zpe_ink/fixtures.py` with seed `20260220`.
- `gate_b_roundtrip.py` writes `ink_roundtrip_results.json` and the sample file `artifacts/2026-02-20_zpe_ink_wave1/samples/synthetic_lossless.zpink`.
- Current roundtrip evidence reports `claim_id=INK-C001`, `pass=true`, `stroke_count=48`, `point_count_total=9834`, and `canonical_hash=9533f8bc03681d8c73cb449cfa39a2dd985dedf071c612e00c56e304db5d8bef`.

## Benchmark Methodology
- `gate_c_benchmarks.py` evaluates three corpora: `synthetic_lossless`, `iam_proxy`, and `unipen_proxy`.
- Compression ratio is computed as raw coordinate bytes divided by encoded bytes, where raw bytes count only `x` and `y` as float32 pairs.
- Fidelity is measured with Hausdorff distance over `(x, y)` points.
- Pressure fidelity is measured as RMSE percent normalized by `1023.0`.
- Latency uses `encode_latency_ms` with warmup, GC disabled during measurement, 40 repeats for Gate C, and median/p95/min reporting per stroke.
- Gate C thresholds are `compression_ratio_min=5.0`, `hausdorff_px_max=1.0`, `pressure_rmse_percent_max=2.0`, and `encode_latency_ms_per_stroke_max=2.0`.
- Current Gate C evidence passes all four thresholds in `ink_compression_benchmark.json`, `ink_fidelity_metrics.json`, `ink_pressure_metrics.json`, and `ink_latency_benchmark.json`.

## Error Handling Assertions
- `decode_zpink` rejects streams that are too short for the header, have invalid magic, unsupported version, invalid mode code, payload length mismatch, CRC mismatch, missing pressure flag, zero-point strokes, overlong stream lengths, zero-length runs, varuint overflow, trailing bytes, or out-of-range channel values.
- The encoder rejects unsupported modes, empty strokes, length mismatches, and out-of-range value domains before framing is written.
- The malformed corpus in Gate D covers truncated payload, bad magic, CRC tamper, and payload-length tamper cases.

## Determinism and Falsification
- `gate_d_falsification.py` runs five campaigns: malformed corpus, adversarial spikes, determinism replay, high-velocity stroke, and long-page stress.
- The determinism replay reports `runs=5` and `unique_hashes=1` in `determinism_replay_results.json`.
- The long-page stress campaign uses `generate_long_page` and enforces a `256.0 MB` ceiling.
- Current Gate D evidence reports `uncaught_crash_rate=0.0` and passes all five campaigns.

## Cross-Runtime Parity
- `gate_e_cross_runtime.py` compares canonical JSON hashes for Python, WASM, and Swift decodes of the same `.zpink` payload.
- The parity artifact records matching hashes for Python, WASM, and Swift, with `pass=true`.
- The same gate also records `pyo3_build_returncode=0` and `pyo3_import_returncode=0`.
- The C# path in `scripts/gate_m_maximalization.py` is a header-only probe via `ZpeInk.DecodeHeader`, not a full decode parity check.

## Net-New Ingestion and Real-Corpus Validation
- `inkml_converter_validation.json` reports 70 MathWriting files and 90 CROHME files detected, with zero parse failures in both corpora.
- The same artifact reports `compression_ratio` below `5.0` for both corpora, while fidelity, pressure, and latency thresholds pass.
- `cross_script_generalization_report.json` includes a Muharaf vectorized fallback corpus with the same threshold pattern: compression below target, fidelity/pressure/latency passing.
- `iam_unipen_parity_table.json` records IAM and UNIPEN proxy evidence; IAM fails compression and latency thresholds, and UNIPEN fails compression.
- `maximalization_gate_results.json` reports `M1` as `FAIL`, `M2` as `PASS`, `M3` as `PASS`, and `M4` as `PASS`.

## Commercial-Safe Closure
- `commercial_corpus_parity.json` uses MathWriting and UCI Pen Digits as the commercial-safe parity corpora.
- The same artifact records `PAUSED_EXTERNAL` outcomes for IAM/UNIPEN, Muharaf, and iOS-PencilKit dependency paths.
- `quality_gate_scorecard.json` is `pass=true` with `total_score=47`, while `appendix_d_e_all_pass=false` because `M1` remains failing.
- `max_claim_resource_map.json` records claim-to-resource status binding for `INK-C001` through `INK-C006`.

## Gate Orchestration
- `scripts/run_all_gates.sh` runs Gate A, the roundtrip unit test, Gates B/C/D, Gate E parity, and `generate_handoff.py`.
- Full validation of the repository also depends on the separate runbook-driven commands for `gate_e_net_new_ingestion.py`, `gate_m_maximalization.py`, and `gate_f_commercial_closure.py`.
- `runbooks/RUNBOOK_ZPE_INK_MASTER.md` defines the intended gate order and the fail signatures for each gate.

## Observed Gaps
- There is no dedicated unit test for the malformed payload classes that are only exercised in Gate D, such as bad magic, bad version, bad mode code, zero-length runs, and trailing-byte rejection.
- There is no explicit automated test for the lossy quantization semantics of `high`, `medium`, and `sketch` modes beyond the `test_quantized_high_mode_stays_finite` smoke check.
- The full cross-runtime decode parity is Python/WASM/Swift/PyO3; the C# path is header-only.
- The single `scripts/run_all_gates.sh` entry point does not cover the later closure gates, so a complete validation run requires additional commands from the runbooks.
