# Plan 03 Summary

Status: complete
Artifact root: `ZPE-Ink/proofs/reruns/phase1_m1_local`

## Core Results

- Full local `run_max_wave.sh` completed on the M1 host with `PYTHON_BIN=/opt/homebrew/bin/python3`.
- Cross-runtime parity is now a real local pass:
  - Python / WASM / Swift hashes match
  - PyO3 build and import pass
  - C# managed-runtime header probe compiles and executes
- Structured-tier sovereign metric remains locally satisfied:
  - `5.5902x` overall on the frozen structured/proxy pack

## Public-Corpus Results

- MathWriting: `1.0944x`
- CROHME: `1.3015x`
- UJI Pen Characters: `1.5110x`
- UCI Pen Digits commercial-safe substitute: `0.6173x`

Interpretation:

- The lane is strong on deterministic transport, fidelity, latency, and local execution.
- The lane is not strong on broad hard-corpus compression.
- UJI improves the real online-stroke evidence surface, but it does not close direct UNIPEN.

## Gate State After Rerun

Passed locally:

- setup
- roundtrip
- benchmark
- falsification
- cross-runtime parity
- NET-NEW attempt-all
- maximalization `M2`, `M3`, `M4`
- commercial closure `F-G1`, `F-G2`, `F-G3`

Still open or failing:

- `E-G3_cross_script_required`: `FAIL`
- `M1_real_iam_unipen_non_inferior`: `FAIL`
- handoff manifest verdict: `NO-GO`

## Remaining Sovereign Blockers

- Direct UNIPEN access is still unavailable after repeated local and containerized attempts.
- Direct IAM online-stroke closure was not established inside the local-only phase.
- A real non-Latin online-stroke corpus remains open.
- Device-level PencilKit validation remains `PAUSED_EXTERNAL`.

## Next Valid Phase

Phase 02 should target direct IAM/UNIPEN acquisition and non-Latin online-stroke closure. It should not spend time re-explaining the local codec unless the sovereign hard-corpus blocker moves.
