# FORMALISM

## Scope
This repository's governing formalism is the `.zpink` packet spec and the artifact chain that proves it. The current package is a deterministic codec and falsification harness for stroke telemetry, not an abstract model layer.

## Governing Artifact Chain
1. Mission and acceptance claims originate in `PRD_ZPE_INK_SECTOR_EXPANSION_WAVE1_2026-02-20.md`.
2. Gate sequencing and fail signatures are predeclared in `runbooks/RUNBOOK_ZPE_INK_MASTER.md` and `runbooks/RUNBOOK_ZPE_INK_GATE_*.md`.
3. Implementation lives in `zpe_ink/codec.py`, `zpe_ink/metrics.py`, `zpe_ink/fixtures.py`, `zpe_ink/inkml.py`, and `bindings/*`.
4. Evidence is recorded in `artifacts/2026-02-20_zpe_ink_wave1/*`.
5. Final packaging is summarized by `artifacts/2026-02-20_zpe_ink_wave1/handoff_manifest.json`.

## `.zpink` Packet Spec
The canonical framing spec is documented in `format/ZPINK_SPEC.md` and implemented in `zpe_ink/codec.py`.

### Header
- Total header size: 22 bytes, little-endian.
- Layout: `magic[5]`, `version[u8]`, `mode[u8]`, `flags[u8]`, `stroke_count[u16]`, `seed[u32]`, `payload_len[u32]`, `payload_crc32[u32]`.
- Magic value: `ZPINK`.
- Version: `1`.
- Mode codes: `0=lossless`, `1=high`, `2=medium`, `3=sketch`.
- Flags: `0x1 pressure`, `0x2 tilt`, `0x4 azimuth`.

### Per-Stroke Payload
- `point_count[u16]`.
- `x0[i32]`, `y0[i32]`.
- `x_delta_stream_len[u32]` followed by RLE-varint delta stream.
- `y_delta_stream_len[u32]` followed by RLE-varint delta stream.
- `pressure0[u16]`.
- `pressure_delta_stream_len[u32]` followed by RLE-varint delta stream.
- If `flags & 0x2`, the stream also contains `tilt0[i16]` and a tilt delta stream.
- If `flags & 0x4`, the stream also contains `azimuth0[i16]` and an azimuth delta stream.

### Delta Stream Encoding
- Deltas are encoded as repeated `(zigzag-varuint delta, varuint run_len)` pairs.
- The decoder rejects zero-length runs, overflow, truncated streams, and trailing bytes.
- The CRC covers the payload only, not the header.

## Channel Semantics
The codec operates on stroke dictionaries with `x`, `y`, `pressure`, `tilt`, and `azimuth` integer arrays.

- `x` and `y` are spatial coordinates stored as signed 32-bit integers.
- `pressure` is a mandatory 0..1023 channel stored as unsigned 16-bit integers at the first sample and deltas afterward.
- `tilt` is a signed channel constrained to -900..900.
- `azimuth` is a signed channel constrained to 0..3600.
- `seed` is a provenance field in the header; the current decoder returns it unchanged and the deterministic harness uses fixed seeds for fixture generation.

## Codec Invariants
The implementation in `zpe_ink/codec.py` and the tests in `tests/test_codec_roundtrip.py` enforce the following invariants:

- `magic` must equal `ZPINK`.
- `version` must equal `1`.
- `mode_code` must map to one of the four declared modes.
- `pressure` is mandatory; streams with the pressure flag cleared fail decode.
- Each stroke must have at least one point.
- Array lengths must match within a stroke.
- Quantized coordinates must remain in signed 32-bit range.
- Pressure, tilt, and azimuth values must remain inside the declared bounds after reconstruction.
- Decoded payloads must consume the full payload with no trailing bytes.
- CRC mismatch, truncation, and malformed delta streams are hard failures.

## Compression Modes
The current encoder applies quantization only to `x` and `y`.

| Mode | Step | Effect |
|---|---:|---|
| `lossless` | 1 | No coordinate quantization. |
| `high` | 2 | Sub-pixel repeatability improvement for delta runs. |
| `medium` | 4 | Coarser coordinate quantization. |
| `sketch` | 8 | Most aggressive coordinate quantization in the current build. |

Pressure, tilt, and azimuth are not quantized by the current encoder path.

## Metric Formalism
The authoritative metric definitions live in `zpe_ink/metrics.py` and are reused by the gate scripts.

- Compression ratio: `raw_bytes / encoded_bytes`, where `raw_bytes = sum(len(stroke["x"]) * 2 * 4 for stroke in strokes)`.
- Hausdorff distance: symmetric max of the directed nearest-neighbor distance between `(x, y)` point sets.
- Corpus fidelity: max Hausdorff distance over paired strokes.
- Pressure RMSE percent: `sqrt(mean((p - p')^2)) / 1023 * 100`.
- Encode latency: median, p95, and min milliseconds per stroke measured over repeated encodes after warmup, with GC disabled during the timing loop.
- Determinism hash: SHA-256 over `canonical_json(decoded)` after encode-decode roundtrip.

The current metric baselines recorded in `artifacts/2026-02-20_zpe_ink_wave1/*` are:
- Compression ratio: `5.590209480060199` in `ink_compression_benchmark.json`.
- Max Hausdorff: `0.0` in `ink_fidelity_metrics.json`.
- Max pressure RMSE: `0.0` in `ink_pressure_metrics.json`.
- Median encode latency: `0.8174798203125` ms/stroke in `ink_latency_benchmark.json`.
- Determinism unique hashes: `1` in `determinism_replay_results.json`.

## Acceptance Logic
The repository uses layered acceptance gates rather than one monolithic pass condition.

- Gate B accepts only when synthetic lossless roundtrip is bit-exact and `tests/test_codec_roundtrip.py` passes.
- Gate C accepts only when compression, fidelity, pressure, and latency all satisfy the thresholds in `scripts/gate_c_benchmarks.py`.
- Gate D accepts only when malformed cases are rejected, adversarial cases roundtrip cleanly, and five fixed-seed replay hashes are identical.
- Gate E accepts only when Python, WASM, Swift, and PyO3 parity hashes match the Python canonical hash.
- Gate M accepts only when real-corpus maximalization closes the outstanding external-validity gaps.
- Gate F accepts only when commercial-safe closure removes `INCONCLUSIVE` from claim promotion paths.

The current wave-1 state is:
- Core claims `INK-C001`..`INK-C006` all pass in `artifacts/2026-02-20_zpe_ink_wave1/claim_status_delta.md`.
- `artifacts/2026-02-20_zpe_ink_wave1/quality_gate_scorecard.json` reports `pass: true`, `total_score: 47`, and `core_claims_pass: true`.
- `artifacts/2026-02-20_zpe_ink_wave1/maximalization_gate_results.json` leaves `M1_real_iam_unipen_non_inferior` as `false`.
- `artifacts/2026-02-20_zpe_ink_wave1/handoff_manifest.json` reports `go_no_go: NO-GO`.

## Runtime Parity Chain
The parity surface currently spans:
- Python codec in `zpe_ink/codec.py`.
- WASM decoder in `bindings/wasm/src/lib.rs` and `scripts/wasm_decode_runner.mjs`.
- Swift header decoder in `bindings/swift/ZPEInk.swift` and `scripts/swift_decode.swift`.
- C# header decoder in `bindings/csharp/ZpeInk.cs`.
- PyO3 native binding path in `bindings/python_native/src/lib.rs` and `bindings/python_native/Cargo.toml`.

`artifacts/2026-02-20_zpe_ink_wave1/ink_cross_runtime_parity.json` records parity success for the wave-1 input set.

## Deterministic Fixture Scheme
The test and benchmark corpora are generated from deterministic seeds in `zpe_ink/fixtures.py`.

- `generate_synthetic_lossless(seed=20260220)` drives the roundtrip and benchmark baseline.
- `generate_iam_proxy(seed=20260220)` and `generate_unipen_proxy(seed=20260221)` provide proxy corpora for current gate C and gate E comparisons.
- `generate_adversarial_spike_set(seed=20260223)` and `generate_long_page(seed=20260224)` drive the falsification campaigns.

## Current Open Boundaries
The following are not resolved in-lane and remain external or paused in the recorded artifact chain:

- Direct IAM/UNIPEN closure, per `artifacts/2026-02-20_zpe_ink_wave1/impracticality_decisions.json` and `artifacts/2026-02-20_zpe_ink_wave1/net_new_gap_closure_matrix.json`.
- Muharaf online-stroke equivalence, recorded as `IMP-NOCODE`.
- iOS PencilKit device-level validation, recorded as `IMP-COMPUTE`.
- OpenRing parity, retained as `PAUSED_EXTERNAL` in the commercialization closure artifacts.
