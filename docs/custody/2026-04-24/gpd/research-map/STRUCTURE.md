# Structure

This repo has two visible surfaces: the current workspace root and a packaged mirror under `ZPE-Ink/`. The root tree holds the active codec, gates, artifacts, and runbooks; the mirror holds the installable package boundary, proof bundle, and smoke/demo helpers used by the nested release-readiness workflow.

## Directory Layout

- `zpe_ink/` is the active Python codec package.
- `bindings/` contains source bindings for `csharp`, `swift`, `wasm`, and `python_native`.
- `scripts/` contains the gate runners, orchestration wrappers, shared logging helpers, and the Swift/WASM decoder runners.
- `tests/` contains the root regression test surface, currently `tests/test_codec_roundtrip.py`.
- `format/` contains the wire-format contract in `format/ZPINK_SPEC.md`.
- `runbooks/` contains the root wave-1 gate runbooks.
- `artifacts/2026-02-20_zpe_ink_wave1/` is the live gate output bundle and evidence warehouse.
- `ZPE-Ink/code/` mirrors the package source, bindings, scripts, tests, and package metadata for the nested installable boundary.
- `ZPE-Ink/proofs/` contains curated proof anchors, runbook copies, logs, and release-readiness docs.
- `ZPE-Ink/executable/` contains local smoke helpers: `demo.py`, `verify_roundtrip.py`, and `verify_cross_runtime.py`.
- `ZPE-Ink/Makefile` drives the nested package install, test, build, demo, and smoke commands.

## Naming And File Patterns

- Gate scripts follow `scripts/gate_[a-f,m].py` and `scripts/gate_e_cross_runtime.sh`.
- Orchestration wrappers are `scripts/run_all_gates.sh` and `scripts/run_max_wave.sh`.
- Runbooks use `runbooks/RUNBOOK_ZPE_INK_GATE_*.md` plus `RUNBOOK_ZPE_INK_MASTER.md`.
- Artifact files are named by function, not by implementation detail: `artifacts/2026-02-20_zpe_ink_wave1/ink_roundtrip_results.json`, `artifacts/2026-02-20_zpe_ink_wave1/ink_compression_benchmark.json`, `artifacts/2026-02-20_zpe_ink_wave1/ink_fidelity_metrics.json`, `artifacts/2026-02-20_zpe_ink_wave1/ink_pressure_metrics.json`, `artifacts/2026-02-20_zpe_ink_wave1/ink_latency_benchmark.json`, `artifacts/2026-02-20_zpe_ink_wave1/ink_cross_runtime_parity.json`, `artifacts/2026-02-20_zpe_ink_wave1/determinism_replay_results.json`, and related reports.
- Logs use `artifacts/2026-02-20_zpe_ink_wave1/command_log.txt` for command traces and `artifacts/2026-02-20_zpe_ink_wave1/regression_results.txt` for test/gate summaries.
- Binary payloads use the `.zpink` extension; generated runtime bundles live under `artifacts/2026-02-20_zpe_ink_wave1/parity/`; downloaded inputs live under `artifacts/2026-02-20_zpe_ink_wave1/net_new_cache/` and `artifacts/2026-02-20_zpe_ink_wave1/resource_cache/`.

## Input And Output Shapes

- The canonical codec input is a list of stroke dictionaries with `x`, `y`, `pressure`, `tilt`, and `azimuth` integer arrays.
- InkML ingestion accepts `.inkml` files and produces the same stroke dictionary schema through `zpe_ink/inkml.py`.
- The UCI Pen Digits path in `scripts/gate_f_commercial_closure.py` parses `.tra` and `.tes` CSV rows into one-stroke samples.
- The Muharaf path in `scripts/gate_e_net_new_ingestion.py` reads a Parquet image column and rasterizes it into synthetic stroke traces when online strokes are not present.
- The `parity/` outputs are JSON-text decodes of the same `.zpink` input, plus the compiled Swift binary and the generated C# probe source.
- `zpe_ink/io.py` and `scripts/shared.py` normalize writes to JSON, logs, and append-only text files so downstream gates can consume stable filenames.

## Dependency Relationships

- `zpe_ink/codec.py` is the dependency root for all encode/decode work.
- `zpe_ink/fixtures.py` feeds the tests and every benchmark/falsification gate.
- `zpe_ink/metrics.py` is consumed by `scripts/gate_c_benchmarks.py`, `scripts/gate_e_net_new_ingestion.py`, and `scripts/gate_f_commercial_closure.py`.
- `zpe_ink/inkml.py` is consumed by Gate N for MathWriting and CROHME ingestion.
- `scripts/shared.py` is the shared orchestration helper for subprocess execution and file emission.
- `scripts/generate_handoff.py` is a reducer: it reads gate outputs and writes the summary contract files without recomputing codec metrics.
- `bindings/wasm/` and `bindings/python_native/` each have their own `Cargo.toml` and Rust source tree, while `bindings/swift/` and `bindings/csharp/` are single-file adapters.

## Build And Test Entry Points

- Root package regression: `python3 -m pytest tests/test_codec_roundtrip.py -q`.
- Root gate chain: `bash scripts/run_all_gates.sh`.
- Full wave chain: `bash scripts/run_max_wave.sh`.
- Individual gates: `python3 scripts/gate_a_setup.py --artifact-root artifacts/2026-02-20_zpe_ink_wave1`, `python3 scripts/gate_b_roundtrip.py --artifact-root ...`, `python3 scripts/gate_c_benchmarks.py --artifact-root ...`, `python3 scripts/gate_d_falsification.py --artifact-root ...`, `bash scripts/gate_e_cross_runtime.sh ...`, `python3 scripts/gate_e_net_new_ingestion.py --artifact-root ...`, `python3 scripts/gate_m_maximalization.py --artifact-root ...`, and `python3 scripts/gate_f_commercial_closure.py --artifact-root ...`.
- Nested package commands: `cd ZPE-Ink && make install`, `make test`, `make build`, `make demo`, and `make smoke`.
- Cross-runtime helpers are `scripts/wasm_decode_runner.mjs` and `scripts/swift_decode.swift`.
- Environment bootstrap is `bash scripts/load_env.sh`; it requires a `.env` file and exports keys before any gate run that depends on local secrets or tool settings.

## Where Future Work Belongs

- Wire-format changes belong in `zpe_ink/codec.py` first, then `format/ZPINK_SPEC.md`, then the runtime adapters under `bindings/`.
- New metrics or benchmark claims belong in `zpe_ink/metrics.py` and the relevant `scripts/gate_*.py` consumer.
- New corpora or ingestion paths belong in `zpe_ink/inkml.py`, `zpe_ink/fixtures.py`, or a new helper beside `scripts/gate_e_net_new_ingestion.py`, depending on whether the input is real, synthetic, or fallback-derived.
- New validation behavior belongs in `tests/` for root regression coverage and in the relevant gate script for artifact-level evidence.
- New summary or handoff fields belong in `scripts/generate_handoff.py` and the downstream proof mirror, not in the generated artifacts by hand.
- Changes intended for the nested release boundary should be reflected in `ZPE-Ink/code/` and its `Makefile` flow; changes intended for the active workspace harness should be made in the root tree.
