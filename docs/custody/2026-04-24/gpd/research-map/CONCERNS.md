# Concerns

Analysis Date: 2026-03-19

## Authority Metric Conflict

- `ZPE-Ink/README.md` marks the repo verdict `INCONCLUSIVE` because `ZPE-Ink/proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/quality_gate_scorecard.json` reports `pass=true` while `ZPE-Ink/proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/handoff_manifest.json` reports `go_no_go=NO-GO`.
- `scripts/generate_handoff.py` computes `scorecard["pass"]` from total score, non-negotiables, and `core_pass`, while the handoff manifest uses `core_pass and appendix_all_pass`. That split creates a release-verdict divergence in the generated artifacts.

## Open P0 Blockers

- `artifacts/2026-02-20_zpe_ink_wave1/maximalization_gate_results.json` keeps `M1_real_iam_unipen_non_inferior` at `FAIL`.
- `artifacts/2026-02-20_zpe_ink_wave1/blockers_before_after.json` still lists `BLK-M1-REAL-IAM-UNIPEN` and `BLK-UNIPEN-ACCESS` as `OPEN` with `P0` severity.
- `artifacts/2026-02-20_zpe_ink_wave1/iam_unipen_parity_table.json` shows IAM and UNIPEN remain below the target compression threshold, so the real-corpus non-inferiority gate does not close on current evidence.

## Paused External Resources

- `artifacts/2026-02-20_zpe_ink_wave1/commercialization_risk_register.md` keeps IAM On-Line, UNIPEN, Muharaf, OpenRing traces, and the iOS PencilKit device-level path in `PAUSED_EXTERNAL`.
- `artifacts/2026-02-20_zpe_ink_wave1/impracticality_decisions.json` records failed acquisition probes for UNIPEN, Muharaf, and iOS device tooling, with fallbacks limited to UCI Pen Digits, raster-to-stroke comparison, and host-level parity.
- `artifacts/2026-02-20_zpe_ink_wave1/net_new_gap_closure_matrix.json` leaves `M1_real_iam_unipen_non_inferior` as the only Appendix D/E gate that fails.

## Validation Gaps

- `ZPE-Ink/proofs/release_validation/README.md` states that no full release-validation surface is claimed.
- `ZPE-Ink/proofs/release_validation/security/README.md` states that no fresh secret scan or security sweep was generated.
- `ZPE-Ink/proofs/INK_WAVE1_RELEASE_READINESS_REPORT.md` defers cold-clone verification, blind-clone testing, broad proof reruns, and performance augmentation.
- `ZPE-Ink/docs/LEGAL_BOUNDARIES.md` keeps the repo in private staging only and blocks broader product, medical, or legal claims.

## Binding Coverage Asymmetry

- `ZPE-Ink/code/bindings/swift/ZPEInk.swift` and `ZPE-Ink/code/bindings/csharp/ZpeInk.cs` expose header parsing only.
- `ZPE-Ink/code/scripts/gate_e_cross_runtime.py` treats Python/WASM/Swift hash parity as the parity gate; `pyo3_import_returncode` is reported but does not participate in `parity_pass`.
- `ZPE-Ink/code/scripts/gate_m_maximalization.py` validates C# through a header probe, not a full encode/decode roundtrip.
- The binding surfaces are therefore not symmetric with the parity claims implied by the repo front door.

## Runbook And Path Fragility

- `ZPE-Ink/proofs/runbooks/README.md` says some gate documents still use the historical `artifacts/2026-02-20_zpe_ink_wave1` artifact-root convention.
- `ZPE-Ink/code/scripts/run_all_gates.sh` and `ZPE-Ink/code/scripts/run_max_wave.sh` default to `proofs/reruns/INK-Canonical-local`, while the imported runbooks and gate scripts still hard-code the historical artifact-root.
- `scripts/gate_a_setup.py` and `scripts/gate_e_net_new_ingestion.py` still reference the outer-workspace resource pack paths under `/Users/prinivenpillay/ZPE Multimodality/`, which makes those entrypoints fragile outside this workspace shape.
- `ZPE-Ink/code/scripts/load_env.sh` hard-fails when `.env` is absent, so the shell bootstrap is environment-dependent.

## Narrow Regression Surface

- `ZPE-Ink/code/tests/test_codec_roundtrip.py` is the only visible pytest file in the lane code tree, so regression coverage is narrow relative to the number of gate scripts and adapter surfaces.
- `ZPE-Ink/proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/command_log.txt` and `ZPE-Ink/proofs/curated_artifacts/2026-02-20_zpe_ink_wave1/handoff_manifest.json` show a large generated evidence set, but the durable automated test surface remains small.

## Imported TODO Signal

- `artifacts/2026-02-20_zpe_ink_wave1/net_new_cache/openring_repo/app/models/inception-ring1-rr-all-ir/resp_rr/Fold-1/config.json` contains `pretrain_model: "TODO"`, and similar cached OpenRing model configs repeat that placeholder.
- This is an imported upstream artifact signal, not a lane-source stub in `ZPE-Ink/code/`, but it remains a verified placeholder inside the evidence warehouse.
