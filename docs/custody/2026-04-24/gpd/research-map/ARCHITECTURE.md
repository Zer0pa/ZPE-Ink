# Architecture

This repo centers on a deterministic `.zpink` codec implemented in Python, with parity adapters in WASM, Swift, C#, and PyO3. The current pipeline is encode-first: Python produces the reference wire format, the other runtimes mirror the decoder contract, and the gate scripts turn codec behavior into benchmark and falsification artifacts.

## Computational Pipeline

- Inputs are stroke corpora shaped as `list[dict[str, list[int]]]` with `x`, `y`, `pressure`, `tilt`, and `azimuth` channels.
- Synthetic corpora are generated in `zpe_ink/fixtures.py` with fixed seeds, including `generate_synthetic_lossless()`, `generate_iam_proxy()`, `generate_unipen_proxy()`, `generate_adversarial_spike_set()`, and `generate_long_page()`.
- Real or quasi-real corpora are normalized in `zpe_ink/inkml.py` through `inkml_to_strokes()` and `collect_inkml_files()`.
- Metrics and verification live in `zpe_ink/metrics.py`, while JSON/log helpers live in `zpe_ink/io.py` and `scripts/shared.py`.

## Encode/Decode Flow

- `zpe_ink/codec.py` defines the wire format contract.
- `encode_zpink()` validates stroke lengths and value ranges, optionally quantizes `x` and `y` by mode, computes delta arrays, compresses them with zigzag varuint run-length encoding, and emits a CRC32-framed payload.
- The header uses `MAGIC = b"ZPINK"`, `VERSION = 1`, a mode byte, flags, stroke count, seed, payload length, and payload CRC.
- `pressure` is mandatory; `tilt` and `azimuth` are gated by flags.
- `decode_zpink()` reverses the frame, validates CRC and lengths, reconstructs absolute coordinates and channel values, and rejects truncated, overflowed, or trailing-byte streams.
- `canonical_json()` is the parity hash canonicalizer used by the cross-runtime checks.

## Runtime Boundaries

- Python is the reference implementation and the only full encode path.
- `bindings/wasm/src/lib.rs` exposes `decode_to_json()` through `wasm-bindgen`; `scripts/wasm_decode_runner.mjs` loads the built package and prints the decoded JSON.
- `scripts/swift_decode.swift` is a standalone Swift decoder that mirrors the Python framing and returns JSON on stdout.
- `bindings/python_native/src/lib.rs` exposes the same decoder contract as `zpe_ink_native.decode_to_json()` and `version()` for the PyO3 path.
- `bindings/csharp/ZpeInk.cs` currently only exposes `DecodeHeader()` and is used as a managed-runtime header probe, not as the full parity decoder.

## Benchmark And Falsification Orchestration

- `scripts/gate_a_setup.py` probes external resources, validates required runbooks, writes the initial traceability and baseline inventory, and locks the wave-1 evidence inputs.
- `scripts/gate_b_roundtrip.py` runs the synthetic lossless roundtrip and writes `ink_roundtrip_results.json` plus the sample `.zpink` payload.
- `scripts/gate_c_benchmarks.py` computes compression ratio, Hausdorff fidelity, pressure RMSE, and encode latency over synthetic, IAM-proxy, and UNIPEN-proxy corpora.
- `scripts/gate_d_falsification.py` runs malformed-input, adversarial-spike, determinism-replay, high-velocity, and long-page stress campaigns.
- `scripts/gate_e_cross_runtime.py` builds WASM, compiles and runs Swift, builds and imports the PyO3 wheel, and compares parity hashes against Python.
- `scripts/gate_e_net_new_ingestion.py` attempts real-corpus ingestion and fallback acquisition for MathWriting, CROHME, OpenRing, Muharaf, and IAM/UNIPEN.
- `scripts/gate_m_maximalization.py` consumes Gate N outputs, adds Appendix D kill tests, and records long-sequence stress plus managed-runtime probing.
- `scripts/gate_f_commercial_closure.py` consumes Gate N and M outputs, reruns commercial-safe corpora, and forces claim/resource statuses into `PASS`, `FAIL`, or `PAUSED_EXTERNAL`.

## Artifact Generation Flow

- `scripts/run_all_gates.sh` is the shorter orchestration path: load the workspace, run Gates A through E, then `scripts/generate_handoff.py`.
- `scripts/run_max_wave.sh` is the full wave driver: it loads `.env`, runs Gates A, B, C, D, E, N, M, F, and then the max-wave handoff.
- `scripts/generate_handoff.py` consumes the gate outputs and rewrites `before_after_metrics.json`, `claim_status_delta.md`, `integration_readiness_contract.json`, `quality_gate_scorecard.json`, `innovation_delta_report.md`, `residual_risk_register.md`, and the final `handoff_manifest.json`.
- The main output bundle is `artifacts/2026-02-20_zpe_ink_wave1/`, which contains the sample payload, parity artifacts, benchmark JSON, falsification reports, resource caches, and command logs.
- Cross-runtime outputs land under `artifacts/2026-02-20_zpe_ink_wave1/parity/`, including the WASM/Swift decoded JSON, the compiled Swift binary, the generated C# probe source, and the PyO3 wheel.
- The curated release mirror lives under `ZPE-Ink/proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/`.

## Dependencies And Likely Bottlenecks

- Core runtime code uses only the Python standard library.
- Test execution depends on `pytest`.
- Gate E depends on external toolchains: `wasm-pack`, `node`, `swiftc`, `maturin`, Rust, and a Python virtual environment for wheel import validation.
- Gate N depends on `huggingface_hub`, `pyarrow`, `PIL`, `tarfile`, `zipfile`, network access, and multiple remote dataset or repository probes.
- Gate F depends on UCI download access, repeated host/container probes, and the commercial-safe substitution path.
- Likely bottlenecks, inferred from the current implementation: full-corpus Python loops in `encode_zpink()`, O(n*m) Hausdorff distance evaluation in `zpe_ink/metrics.py`, repeated JSON serialization for parity hashing, external downloads, and cross-runtime build startup overhead.

