# Proof And Validation Runbook

## Purpose

Refresh the decisive local CPU proof surface for ZPE-Ink and produce the evidence required to classify the interoperability lane honestly.

## Owner / Agent Type

Execution agent or verifier.

## Input Artifacts

- [test_cross_runtime_parity.py](/Users/Zer0pa/ZPE/ZPE%20Ink/ZPE-Ink/code/tests/test_cross_runtime_parity.py)
- [20260321_technical_alignment_cross_runtime.json](/Users/Zer0pa/ZPE/ZPE%20Ink/ZPE-Ink/proofs/logs/20260321_technical_alignment_cross_runtime.json)
- [20260321_technical_alignment_binding_contracts.json](/Users/Zer0pa/ZPE/ZPE%20Ink/ZPE-Ink/proofs/logs/20260321_technical_alignment_binding_contracts.json)
- [README.md](/Users/Zer0pa/ZPE/ZPE%20Ink/ZPE-Ink/README.md)
- [ARCHITECTURE.md](/Users/Zer0pa/ZPE/ZPE%20Ink/ZPE-Ink/docs/ARCHITECTURE.md)
- current packaging metadata and build scripts

## Output Artifacts

- local CPU rerun manifest
- parity result packet
- build/install smoke result
- discrepancy list against prior proof logs

## Acceptance Gate

The rerun packet must classify each check as pass, fail, or skipped with explicit reason:

- `pytest code/tests -q`
- Swift/C# parity execution
- WASM parity execution when toolchain is present
- binding-contract verification
- supported build path
- install smoke

No check is allowed to disappear into narrative or implicit fallback.

## Failure Mode

- parity test silently skipped
- build path not exercised
- stale proof log cited as fresh evidence
- ambiguity between toolchain absence, storage failure, and functional defect

## Execution Surface

- Mac required: yes
- RunPod required: no for first pass
- Hugging Face required: yes for large resulting proof bundles

## Procedure

1. Verify local disk and toolchain state.
2. Run the bounded local CPU verification packet in this order:
   - `pytest code/tests -q`
   - cross-runtime parity test
   - binding-contract verification
   - wheel or sdist build
   - install smoke in a clean venv
3. Record exact timings, toolchains detected, and whether Swift/C#/WASM ran or skipped.
4. Compare outcomes to the March 21 technical-alignment logs.
5. Emit a rerun manifest that states one of:
   - full local CPU pass
   - partial pass with classified blocker
   - fail with functional defect

## ZPE-Ink Specific Gates

- Swift and C# must be treated as decode-parity surfaces, not just header-contract surfaces, if the fresh rerun confirms that path.
- The install/build gate must be fresh before any new integer-canvas or codebook layer is entertained.
- The current `.zpink` packet contract remains the baseline; candidate augmentation work cannot rewrite the acceptance gate around a new surface prematurely.

## Kill Conditions

- If the rerun reveals a real functional regression in parity or build/install, stop augmentation execution and reopen only a repair lane.
- If the rerun cannot distinguish toolchain/environment failure from product failure, stop and repair the verification harness first.
