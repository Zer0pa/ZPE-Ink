# Methodology Conventions

## Scope
- This report covers the conventions observed in `format/ZPINK_SPEC.md`, `zpe_ink/`, `bindings/`, `scripts/`, `tests/test_codec_roundtrip.py`, `runbooks/`, and `artifacts/2026-02-20_zpe_ink_wave1/`.
- The active packet contract anchor is `ZPE-Ink/docs/family/ZPINK_INTERFACE_CONTRACT.md`, with the machine-readable version in `ZPE-Ink/docs/family/ZPINK_COMPATIBILITY_VECTOR.json`.

## Binary Format
- The `.zpink` header is 22 bytes and little-endian.
- `magic[5]` is ASCII `ZPINK`.
- `version[u8]` is `1`.
- `mode[u8]` maps `0=lossless`, `1=high`, `2=medium`, `3=sketch`.
- `flags[u8]` is a bitmask with `0x1 pressure`, `0x2 tilt`, `0x4 azimuth`.
- `stroke_count[u16]`, `seed[u32]`, `payload_len[u32]`, and `payload_crc32[u32]` are stored in the header.
- The payload CRC is computed over the payload only in `zpe_ink/codec.py`.

## Stroke Schema
- The encoder and decoder use the stroke dict keys `x`, `y`, `pressure`, `tilt`, and `azimuth`.
- `point_count[u16]` precedes each stroke payload.
- `x0` and `y0` are stored as signed 32-bit little-endian integers.
- `pressure0` is stored as `u16`; `tilt0` and `azimuth0` are stored as signed 16-bit integers when their flags are present.
- Delta streams are length-prefixed with `u32` byte lengths and encoded as RLE segments of `zigzag-varuint delta` plus `varuint run_len`.
- Decoders reject zero-length runs, overflow, and trailing bytes.

## Value Ranges
- `x` and `y` are validated against signed 32-bit range bounds in `zpe_ink/codec.py`.
- `pressure` is constrained to `0..1023`.
- `tilt` is constrained to `-900..900`.
- `azimuth` is constrained to `0..3600`.
- Empty strokes are rejected; `point_count` must be at least 1 and no more than `65535`.

## Mode Semantics
- `lossless` leaves `x` and `y` unchanged.
- `high` quantizes `x` and `y` to step `2`.
- `medium` quantizes `x` and `y` to step `4`.
- `sketch` quantizes `x` and `y` to step `8`.
- Quantization is applied only to `x` and `y`; pressure, tilt, and azimuth are not quantized by `encode_zpink`.

## Optional Channel Semantics
- `pressure` is mandatory in both encoder and decoder paths.
- `tilt` and `azimuth` are optional by flag, but `decode_zpink` still returns arrays for both keys.
- When a flag is absent, the decoder fills that channel with zeroes for each point.

## Determinism
- The observed fixture seeds are `20260220`, `20260221`, `20260223`, and `20260224` in `zpe_ink/fixtures.py`.
- `encode_zpink(..., seed=20260220)` stores the seed in the header; the current encoder does not derive randomness from it.
- Deterministic parity hashing uses `zpe_ink.codec.canonical_json`, which serializes with sorted keys and compact separators.
- Artifact writers in `zpe_ink/io.py` emit JSON with sorted keys, two-space indentation, and a trailing newline.

## Naming Conventions
- Python API names are `encode_zpink`, `decode_zpink`, `canonical_json`, `ZPInkEncodeError`, and `ZPInkDecodeError`.
- The C# mirror exposes `ZpeInk.DecodeHeader` in `bindings/csharp/ZpeInk.cs`.
- The Rust/WASM surface exposes `decode_to_json` in `bindings/wasm/src/lib.rs`.
- The Swift mirror exposes `decode(_:)` in `scripts/swift_decode.swift`.
- The package version anchor is `0.1.0` in `ZPE-Ink/docs/family/ZPINK_COMPATIBILITY_VECTOR.json`.

## Metric Naming
- The core benchmark names are `compression_ratio`, `max_hausdorff_px`, `pressure_rmse_percent`, `median_ms_per_stroke`, `p95_ms_per_stroke`, and `min_ms_per_stroke`.
- Claim IDs use the `INK-C001` through `INK-C006` prefix in `scripts/generate_handoff.py` and the artifact JSON files.
- Falsification campaign IDs use the `DT-INK-1` through `DT-INK-5` prefix in `scripts/gate_d_falsification.py`.
- Impracticality codes observed in artifacts are `IMP-ACCESS`, `IMP-COMPUTE`, `IMP-NOCODE`, and the policy-listed `IMP-LICENSE` and `IMP-STORAGE`.

## Artifact Naming
- Gate outputs are written under `artifacts/2026-02-20_zpe_ink_wave1/`.
- Core files are `ink_roundtrip_results.json`, `ink_compression_benchmark.json`, `ink_fidelity_metrics.json`, `ink_pressure_metrics.json`, `ink_latency_benchmark.json`, `ink_cross_runtime_parity.json`, `determinism_replay_results.json`, and `falsification_results.md`.
- Handoff and closure files include `artifacts/2026-02-20_zpe_ink_wave1/handoff_manifest.json`, `artifacts/2026-02-20_zpe_ink_wave1/quality_gate_scorecard.json`, `artifacts/2026-02-20_zpe_ink_wave1/claim_status_delta.md`, `artifacts/2026-02-20_zpe_ink_wave1/integration_readiness_contract.json`, `artifacts/2026-02-20_zpe_ink_wave1/maximalization_gate_results.json`, `artifacts/2026-02-20_zpe_ink_wave1/commercial_corpus_parity.json`, and `artifacts/2026-02-20_zpe_ink_wave1/inkml_converter_validation.json`.
- The roundtrip gate writes a sample payload to `artifacts/2026-02-20_zpe_ink_wave1/samples/synthetic_lossless.zpink`.

## Cross-File Terminology Contract
- `magic`, `version`, `mode`, `flags`, `seed`, and `strokes` are stable field names across Python, WASM, Swift, and the generated artifact JSON.
- `lossless`, `high`, `medium`, and `sketch` are the canonical mode strings; the header stores numeric codes.
- `pressure` is always treated as mandatory claim surface, while `tilt` and `azimuth` are channel-gated optional surfaces.
- `canonical_hash` in `ink_roundtrip_results.json` is the SHA-256 of the canonical JSON decode output.
- `compression_ratio` in the benchmark artifacts is computed against raw float32 `x/y` storage only, not against a full multi-channel raw baseline.

## Observed Path Drift
- `ZPE-Ink/docs/ARCHITECTURE.md` still describes source layout under `code/`, while the executable source tree used by the gates is `zpe_ink/`, `bindings/`, and `scripts/`.
- The validation and runbook surfaces use the actual repo paths from the current tree, not the older `code/` path naming.
