# REFERENCES

## Registry Rules
- This file is an active anchor registry for the repo's current evidence chain.
- `Contract Subject IDs` use claim IDs when the anchor ties directly to a claim.
- `Carry Forward To` names workflow stages only.
- Status is current-state only.

| Anchor ID | Type | Source / Locator | Contract Subject IDs | Carry Forward To | Status | Notes |
|---|---|---|---|---|---|---|
| ZI-SPEC-001 | Spec | `format/ZPINK_SPEC.md` | `INK-C001`..`INK-C006` | Gate B, Gate C, Gate D, Gate E | ACTIVE | Canonical `.zpink` framing, modes, flags, and delta-stream rules. |
| ZI-PRD-001 | PRD | `PRD_ZPE_INK_SECTOR_EXPANSION_WAVE1_2026-02-20.md` | `INK-C001`..`INK-C006` | Gate A through Gate F | ACTIVE | Mission objective, claim matrix, mandatory artifacts, and appendix gates. |
| ZI-RB-MASTER-001 | Runbook | `runbooks/RUNBOOK_ZPE_INK_MASTER.md` | `INK-C001`..`INK-C006` | Gate A through Gate F | ACTIVE | Master gate order, deterministic seed policy, and fail signatures. |
| ZI-RB-B-001 | Runbook | `runbooks/RUNBOOK_ZPE_INK_GATE_B.md` | `INK-C001` | Gate B | ACTIVE | Roundtrip and malformed-header rejection contract. |
| ZI-RB-C-001 | Runbook | `runbooks/RUNBOOK_ZPE_INK_GATE_C.md` | `INK-C002`, `INK-C003`, `INK-C004`, `INK-C005` | Gate C | ACTIVE | Compression, fidelity, pressure, and latency threshold contract. |
| ZI-RB-D-001 | Runbook | `runbooks/RUNBOOK_ZPE_INK_GATE_D.md` | `INK-C001`..`INK-C005` | Gate D | ACTIVE | Malformed, adversarial, and determinism replay contract. |
| ZI-RB-E-001 | Runbook | `runbooks/RUNBOOK_ZPE_INK_GATE_E.md` | `INK-C006` | Gate E | ACTIVE | Cross-runtime parity and packaging contract. |
| ZI-RB-NETNEW-001 | Runbook | `runbooks/RUNBOOK_ZPE_INK_GATE_NET_NEW.md` | `INK-C001`..`INK-C006` | Gate N, Gate M, Gate F | ACTIVE | Appendix E intake and RunPod readiness contract. |
| ZI-RB-M-001 | Runbook | `runbooks/RUNBOOK_ZPE_INK_GATE_M.md` | `INK-C001`..`INK-C006` | Gate M | ACTIVE | Maximalization closure and long-sequence stress contract. |
| ZI-RB-F-001 | Runbook | `runbooks/RUNBOOK_ZPE_INK_GATE_F.md` | `INK-C001`..`INK-C006` | Gate F | ACTIVE | Commercial-safe closure and `PAUSED_EXTERNAL` adjudication. |
| ZI-CODEC-001 | Implementation | `zpe_ink/codec.py` | `INK-C001`..`INK-C006` | Gate B, Gate D, Gate E | ACTIVE | Header framing, RLE-varint encoding, range checks, canonical JSON. |
| ZI-METRICS-001 | Implementation | `zpe_ink/metrics.py` | `INK-C002`, `INK-C003`, `INK-C004`, `INK-C005` | Gate C, Gate F | ACTIVE | Compression ratio, Hausdorff, pressure RMSE, latency, determinism hash. |
| ZI-FIXTURES-001 | Implementation | `zpe_ink/fixtures.py` | `INK-C001`..`INK-C006` | Gate B through Gate M | ACTIVE | Deterministic synthetic, proxy, adversarial, and long-page corpora. |
| ZI-INKML-001 | Implementation | `zpe_ink/inkml.py` | `INK-C001`, `INK-C002`, `INK-C003`, `INK-C005` | Gate N, Gate F | ACTIVE | InkML trace extraction used for MathWriting and CROHME ingestion. |
| ZI-TEST-001 | Test | `tests/test_codec_roundtrip.py` | `INK-C001` | Gate B | ACTIVE | Bit-exact roundtrip, CRC tamper detection, truncated payload rejection, high-mode sanity. |
| ZI-ART-ROUNDTRIP-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/ink_roundtrip_results.json` | `INK-C001` | Handoff | ACTIVE | Wave-1 synthetic lossless roundtrip result. |
| ZI-ART-BENCH-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/ink_compression_benchmark.json` | `INK-C002` | Handoff | ACTIVE | Compression threshold result, overall ratio `5.590209480060199`. |
| ZI-ART-FIDELITY-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/ink_fidelity_metrics.json` | `INK-C003` | Handoff | ACTIVE | Max Hausdorff `0.0`. |
| ZI-ART-PRESSURE-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/ink_pressure_metrics.json` | `INK-C004` | Handoff | ACTIVE | Pressure RMSE `0.0`. |
| ZI-ART-LATENCY-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/ink_latency_benchmark.json` | `INK-C005` | Handoff | ACTIVE | Median latency `0.8174798203125` ms/stroke. |
| ZI-ART-PARITY-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/ink_cross_runtime_parity.json` | `INK-C006` | Handoff | ACTIVE | Python/WASM/Swift/PyO3 parity artifact. |
| ZI-ART-DET-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/determinism_replay_results.json` | `INK-C001`..`INK-C005` | Handoff | ACTIVE | Five-run replay with `unique_hashes: 1`. |
| ZI-ART-FALSE-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/falsification_results.md` | `INK-C001`..`INK-C005` | Gate D, Gate M | ACTIVE | Malformed, adversarial, determinism, and stress campaign log. |
| ZI-ART-SCORE-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/quality_gate_scorecard.json` | `INK-C001`..`INK-C006` | Handoff | ACTIVE | `pass: true`, `total_score: 47`, `appendix_d_e_all_pass: false`. |
| ZI-ART-HANDOFF-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/handoff_manifest.json` | `INK-C001`..`INK-C006` | Handoff | ACTIVE | Final package manifest, current `go_no_go: NO-GO`. |
| ZI-ART-GAP-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/net_new_gap_closure_matrix.json` | `INK-C001`..`INK-C006` | Gate M, Gate F | ACTIVE | Appendix D/E gate snapshot and resource-status matrix. |
| ZI-ART-IMP-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/impracticality_decisions.json` | `INK-C001`, `INK-C002`, `INK-C005`, `INK-C006` | Gate M, Gate F | ACTIVE | Recorded `IMP-ACCESS`, `IMP-NOCODE`, and `IMP-COMPUTE` decisions. |
| ZI-ART-CLAIM-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/claim_status_delta.md` | `INK-C001`..`INK-C006` | Handoff | ACTIVE | Claim matrix now records all six claims as `PASS`. |
| ZI-ART-TRACE-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/concept_resource_traceability.json` | Appendix B items B1..B7 | Gate A, Gate E, Gate F | ACTIVE | Registry for Google modeler, Wacom UIM, InkML.js, IAM, UNIPEN, wasm-bindgen, PyO3. |
| ZI-ART-COMM-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/commercial_corpus_parity.json` | `INK-C001`, `INK-C002`, `INK-C005`, `INK-C006` | Gate F | ACTIVE | Commercial-safe closure over MathWriting and UCI Pen Digits. |
| ZI-ART-RISK-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/commercialization_risk_register.md` | `INK-C001`..`INK-C006` | Gate F | ACTIVE | External-resource risk register with `PAUSED_EXTERNAL` closures. |
| ZI-ART-OPEN-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/concept_open_questions_resolution.md` | `INK-C001`..`INK-C006` | Gate E, Gate F | ACTIVE | Open question ledger for resolution and paused items. |
| ZI-ART-MAX-001 | Result | `artifacts/2026-02-20_zpe_ink_wave1/maximalization_gate_results.json` | `INK-C001`..`INK-C006` | Gate M | ACTIVE | Max-wave adjudication, including the `M1` failure. |
| ZI-ADAPT-WASM-001 | Runtime Adapter | `bindings/wasm/src/lib.rs`, `scripts/wasm_decode_runner.mjs` | `INK-C006` | Gate E | ACTIVE | WASM decoder and Node runner used for parity hash comparison. |
| ZI-ADAPT-SWIFT-001 | Runtime Adapter | `bindings/swift/ZPEInk.swift`, `scripts/swift_decode.swift` | `INK-C006` | Gate E | ACTIVE | Swift parity header/parser path and JSON emitter. |
| ZI-ADAPT-CSHARP-001 | Runtime Adapter | `bindings/csharp/ZpeInk.cs` | `INK-C006` | Gate M, Gate E | ACTIVE | C# header decoder used for managed-runtime closure. |
| ZI-ADAPT-PYO3-001 | Runtime Adapter | `bindings/python_native/src/lib.rs`, `bindings/python_native/Cargo.toml` | `INK-C006` | Gate E | ACTIVE | Python native binding path; current parity artifact records build/import evidence. |
| ZI-OPEN-001 | Open Question | `artifacts/2026-02-20_zpe_ink_wave1/net_new_gap_closure_matrix.json` and `artifacts/2026-02-20_zpe_ink_wave1/impracticality_decisions.json` | `INK-C001`, `INK-C002`, `INK-C006` | Gate M, Gate F | PAUSED_EXTERNAL | Direct IAM/UNIPEN closure remains unresolved; M1 stays false. |
| ZI-OPEN-002 | Open Question | `artifacts/2026-02-20_zpe_ink_wave1/impracticality_decisions.json` | `INK-C001`, `INK-C002`, `INK-C005` | Gate F | PAUSED_EXTERNAL | Muharaf is raster-only in the recorded lane evidence. |
| ZI-OPEN-003 | Open Question | `artifacts/2026-02-20_zpe_ink_wave1/impracticality_decisions.json` | Adapter validation track | Gate F | PAUSED_EXTERNAL | iOS PencilKit device-level path requires external device-lab access. |
