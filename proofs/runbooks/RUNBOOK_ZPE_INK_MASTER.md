# RUNBOOK_ZPE_INK_MASTER

## Scope Lock
- Lane root: repo root (`ZPE-Ink/`)
- Hard boundary: no edits outside lane; never touch sibling lanes.
- Historical PRD and startup prompt remain in the outer workspace shell.

## Environment Bootstrap
- Mandatory first step before any gate command:
  - `bash code/scripts/load_env.sh`
- Secrets policy:
  - never print token values in logs;
  - log only presence/absence and key names.

## Deterministic Seed Policy
- Global seed: `20260220`
- Replay seeds for determinism gate: `[20260220, 20260221, 20260222, 20260223, 20260224]`
- All synthetic fixtures generated from seeded RNG; fixture manifest stores seed and hashes.

## Master Gate Order (No Skips)
1. Gate A: runbook + resource lock + baseline inventory
2. Gate B: `.zpink` encode/decode + lossless synthetic roundtrip
3. Gate C: compression/fidelity/pressure/latency matrix
4. Gate D: malformed/adversarial/determinism campaigns
5. Gate E: cross-runtime parity + packaging contract
6. Gate N (Appendix E): NET-NEW resource ingestion, impracticality adjudication, gap closure matrix, RunPod readiness
7. Gate M (Appendix D): maximalization closure on real-corpus validity and long-sequence stress (uses Gate N outputs)
8. Gate F (Appendix F): commercialization-safe closure and `PAUSED_EXTERNAL` adjudication

## Command Ledger (Planned)
1. `python3 code/scripts/gate_a_setup.py --artifact-root proofs/reruns/INK-Canonical-<UTC timestamp>`
2. `python3 -m pytest code/tests/test_codec_roundtrip.py -q`
3. `python3 code/scripts/gate_b_roundtrip.py --artifact-root proofs/reruns/INK-Canonical-<UTC timestamp>`
4. `python3 code/scripts/gate_c_benchmarks.py --artifact-root proofs/reruns/INK-Canonical-<UTC timestamp>`
5. `python3 code/scripts/gate_d_falsification.py --artifact-root proofs/reruns/INK-Canonical-<UTC timestamp>`
6. `bash code/scripts/gate_e_cross_runtime.sh proofs/reruns/INK-Canonical-<UTC timestamp>`
7. `python3 code/scripts/generate_handoff.py --artifact-root proofs/reruns/INK-Canonical-<UTC timestamp>`
8. `python3 code/scripts/gate_e_net_new_ingestion.py --artifact-root proofs/reruns/INK-Canonical-<UTC timestamp>`
9. `python3 code/scripts/gate_m_maximalization.py --artifact-root proofs/reruns/INK-Canonical-<UTC timestamp>`
10. `python3 code/scripts/gate_f_commercial_closure.py --artifact-root proofs/reruns/INK-Canonical-<UTC timestamp>`
11. `python3 code/scripts/generate_handoff.py --artifact-root proofs/reruns/INK-Canonical-<UTC timestamp> --max-wave`

## Expected Outputs
- Legacy curated Wave-1 outputs were removed during cleanup.
- Future rerun outputs should land under:
  - `proofs/reruns/INK-Canonical-<UTC timestamp>/`
- Appendix E artifacts under:
  - `max_resource_lock.json`
  - `max_resource_validation_log.md`
  - `max_claim_resource_map.json`
  - `impracticality_decisions.json`
  - `inkml_converter_validation.json`
  - `cross_script_generalization_report.json`
  - `net_new_gap_closure_matrix.json`
  - `runpod_readiness_manifest.json` (conditional on `IMP-COMPUTE`)
- Appendix F artifacts under:
  - `commercialization_risk_register.md`
  - `commercial_corpus_parity.json`

## Fail Signatures (Global)
- Any uncaught exception process-exit in falsification commands.
- Determinism hashes mismatch across fixed-seed replays.
- Claim threshold miss for C001-C006.
- Missing artifact file listed in PRD section 7 and Appendix C.
- Missing Appendix E mandatory artifacts.
- Any skipped resource without valid impracticality code and evidence.
- Any core claim closed on synthetic-only traces when real traces were available.
- Any claim that remains `INCONCLUSIVE` after Gate F without explicit `FAIL` or `PAUSED_EXTERNAL` evidence.

## Rollback Policy
- Maintain gate checkpoint tags in command log (`GATE_A_PASS`, etc.).
- On failure:
  1. Patch minimal surface.
  2. Rerun failed gate.
  3. Rerun all downstream gates.
  4. Update claim status delta only after reruns.

## Falsification-First Claim Plan
- INK-C001: Attempt byte tamper and point-order corruption before claiming roundtrip PASS.
- INK-C002: Attempt high-entropy strokes to push compression ratio below threshold.
- INK-C003: Attempt adversarial zig-zag curvature to inflate Hausdorff distance.
- INK-C004: Attempt pressure spikes and saturation overflow.
- INK-C005: Attempt long high-velocity traces and batch load latency.
- INK-C006: Attempt parity mismatch across Python/WASM/native with randomized corpus.

## Comparator Plan (Predeclared)
- Incumbent baseline comparator: raw float32 coordinate storage (no compression).
- Modern comparator target: Google ink-stroke-modeler smoothing pipeline.
- If Google modeler unavailable: fallback to deterministic Chaikin smoothing + explicit comparability impact logging.

## Concept-Resource Traceability Plan (Appendix B)
1. Google ink-stroke-modeler: validate availability and smoothing comparator evidence.
2. Wacom Universal Ink Library: adapter smoke test and conversion trace.
3. Microsoft InkML.js (or equivalent): web-format adapter parity evidence.
4. IAM dataset: validation matrix entry with provenance lock.
5. UNIPEN dataset: validation matrix entry with provenance lock.
6. wasm-bindgen: build/test evidence for WASM adapter.
7. PyO3: build/import evidence for Python native binding path.

## Fallback Plan (Resource Failures)
- Record failed command + stderr in `falsification_results.md` and `command_log.txt`.
- Use nearest open equivalent:
  - Google modeler -> Chaikin smoothing baseline.
  - InkML.js -> local InkML XML parser subset.
  - IAM/UNIPEN download failure -> deterministic proxy fixtures with equivalent stroke statistics.
- Mark impacted traceability entries `INCONCLUSIVE` unless equivalence proof exists.
- Impracticality codes allowed only:
  - `IMP-LICENSE`
  - `IMP-ACCESS`
  - `IMP-COMPUTE`
  - `IMP-STORAGE`
  - `IMP-NOCODE`

## Commercialization Closure Rules (Appendix F)
- Preferred commercial-safe corpora for closure:
  - MathWriting (`CC-BY-4.0`)
  - UCI Pen Digits (as UNIPEN substitute in this lane)
- Non-commercial/restricted resources (e.g., IAM/UNIPEN direct, Muharaf if license uncertain) must be:
  1. tagged in `commercialization_risk_register.md`,
  2. mapped to commercial-safe alternatives where possible,
  3. set to `PAUSED_EXTERNAL` when no equivalent commercial-safe alternative is proven.
- Claims must end Gate F as `PASS`, `FAIL`, or `PAUSED_EXTERNAL` only.
