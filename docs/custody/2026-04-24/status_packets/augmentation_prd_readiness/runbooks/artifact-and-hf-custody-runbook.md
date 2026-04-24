# Artifact And HF Custody Runbook

## Purpose

Keep all ZPE-Ink large artifacts, proof bundles, corpora, checkpoints, and future rerun outputs recoverable under live Hugging Face storage while leaving GitHub as the authority for code/docs/small proof files.

## Owner / Agent Type

Execution agent with HF operational access and custody discipline.

## Input Artifacts

- [ZPE-Ink_HF_CUSTODY_REPORT.md](/Users/Zer0pa/Status_Packets/2026-04-24_HF_Custody_Central_Report/lane_reports/ZPE-Ink_HF_CUSTODY_REPORT.md)
- local `proofs/` tree
- local corpora or benchmark packs used in future augmentation work
- any future rerun manifests or checkpoint bundles

## Output Artifacts

- HF custody manifest
- live verification note
- upload receipts
- residual machine-loss risk note

## Acceptance Gate

- `Zer0pa/ZPE-Ink-artifacts` remains the verified dataset target for `proofs/`.
- Every large proof bundle, corpus, or rerun archive has:
  - a live HF target
  - a direct verification step
  - and a path recorded in the custody manifest
- GitHub-class material is reported, not silently uploaded to HF as a substitute.

## Failure Mode

- Wrong namespace
- unverified upload
- only-local rerun bundle
- model/checkpoint material without HF destination
- remote scratch or RunPod salvage not captured

## Execution Surface

- Mac required: yes
- RunPod required: only if future augmentation artifacts exist only on remote storage
- Hugging Face required: yes

## Procedure

1. Normalize auth before HF actions:
   `unset HF_TOKEN`
   `unset HUGGINGFACE_HUB_TOKEN`
   `unset HF_HOME`
   `hf auth whoami`
2. Verify expected identity:
   `user=Architect-Prime orgs=Zer0pa`
3. Reuse or create targets as needed:
   - dataset repo: `Zer0pa/ZPE-Ink-artifacts`
   - model repo: `Zer0pa/ZPE-Ink-models` only if actual model/checkpoint files appear
   - bucket: `Zer0pa/ZPE-Ink-scratch` only if mutable remote salvage appears
4. Upload only HF-class material:
   - `proofs/`
   - large corpora
   - benchmark packs
   - checkpoints
   - remote salvage bundles
5. Verify live targets directly after upload using `hf datasets info`, `hf models info`, or bucket inspection.
6. Record GitHub-required-later material separately and do not treat HF as a substitute.

## ZPE-Ink Specific Gates

- `proofs/` must remain live under `Zer0pa/ZPE-Ink-artifacts`.
- Future augmentation corpora like IAM-OnDB, CROHME, VNOn-DB, or large derived benchmark packs must be mirrored to HF before or during execution.
- Any future integer-canvas/codebook benchmark bundle must have HF custody if it grows beyond small proof-file scope.

## Kill Conditions

- If HF auth fails, stop and record `HF AUTH FAILED`.
- If a needed large artifact exists only on RunPod and is not locally recoverable, stop and record `RUNPOD ACCESS REQUIRED` with pod/path details.
