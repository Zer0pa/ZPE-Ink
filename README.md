# ZPE-Ink

Private staging repo for the ZPE Ink Wave-1 codec surface.

Current state on 2026-03-09:

- the repo boundary is now isolated from the outer workspace shell
- the Python codec package and curated Wave-1 proof anchors are present
- the package build surface has been normalized under `code/`
- the sector is not greenlit for release
- the current readiness verdict remains `INCONCLUSIVE` because `proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/quality_gate_scorecard.json` reports `pass=true` while `proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/handoff_manifest.json` reports `go_no_go=NO-GO`

## What This Repo Is

ZPE-Ink is a deterministic digital-ink codec centered on the `.zpink` packet format. The current implementation includes:

- Python encode/decode for stroke streams
- a small pytest regression surface
- source bindings for WASM, Python-native, Swift, and C#
- imported gate runbooks from the original sector workspace
- a curated subset of the 2026-02-20 Wave-1 proof bundle

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ./code
python -m pytest code/tests -q
python executable/demo.py
python -m pip wheel ./code --no-deps -w dist
```

## Repo Map

- `code/`: package source, tests, bindings, and gate scripts
- `docs/`: architecture, support, legal boundaries, and the `.zpink` contract surface
- `proofs/`: curated Wave-1 proof anchors, imported runbooks, and future rerun locations
- `executable/`: low-cost local demo and verification entry points

## Proof Anchors

Start here:

- `proofs/INK_WAVE1_RELEASE_READINESS_REPORT.md`
- `proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/quality_gate_scorecard.json`
- `proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/handoff_manifest.json`
- `proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/claim_status_delta.md`
- `proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/ink_cross_runtime_parity.json`

## Boundary Note

This repo is the only GitHub repo candidate for ZPE Ink. The outer workspace still contains operator-only materials, raw artifact warehouses, and historical planning files. Those do not belong in the staged repo boundary.
