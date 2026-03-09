# Architecture

## Scope

ZPE-Ink is a deterministic stroke-stream codec built around the `.zpink` envelope.

## Packet Shape

The current contract is defined in `docs/family/ZPINK_INTERFACE_CONTRACT.md`.

High-level fields:

- magic: `ZPINK`
- version: `1`
- modes: `lossless`, `high`, `medium`, `sketch`
- channel flags: pressure, tilt, azimuth

## Code Layout

- `code/zpe_ink/codec.py`: encode/decode and validation
- `code/zpe_ink/fixtures.py`: deterministic sample generation
- `code/zpe_ink/inkml.py`: InkML parsing helpers
- `code/zpe_ink/metrics.py`: codec metric helpers

## Binding Layout

- `code/bindings/wasm/`: Rust/WASM source surface
- `code/bindings/python_native/`: PyO3-native surface
- `code/bindings/swift/`: Swift binding surface
- `code/bindings/csharp/`: C# binding surface

## Proof Boundary

This repo carries a curated proof subset under `proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/`.

The full historical warehouse remains outside the repo boundary in the outer workspace.
