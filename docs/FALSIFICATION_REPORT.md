<p>
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>

# Falsification Report (Docs Pass)

Date: 2026-03-21
Scope: Documentation surface only. This report lists the claims adjusted during the docs pass and any remaining doc gaps.

## What Changed Since Last Report

- Removed legacy proof bundles and updated all doc references to current rerun and log surfaces.
- Rewrote proof anchors to reference current paths and downgraded candidate-only claims.

## Unsupported Claims Removed Or Downgraded

- Downgraded blind-clone status from implied "deferred" to explicit `INCONCLUSIVE` with evidence.
- Downgraded non-Latin status from "unexecuted" to "executed but not release-closing" based on Calliar evidence.
- Removed any implied claim of structured-tier superiority over all engineering comparators; Brotli remains higher on the structured tier.
- Marked public release language as blocked while the handoff manifest remains `NO-GO`.

## Path Or Render Issues Found

- Root README and docs index lacked the ZPE-IMC visual system and section bars; fixed by embedding repo-local assets.
- Docs index omitted proofs/runbooks and audit entry points; fixed by routing to `proofs/README.md` and `AUDITOR_PLAYBOOK.md`.
- `docs/ARCHITECTURE.md` and `code/README.md` were underspecified; expanded to include authority maps and verification references.

## Remaining Owner Inputs

- Decide whether to update or mark historical the gate runbooks under `proofs/runbooks/` that still reference pre-staging paths.
- Decide whether any removed legacy artifacts should be reintroduced in a separate archive repo (not this repo).
- Decide whether to publish a public package acquisition path beyond private staging.

## Live vs Local Drift

- Local repo now carries the ZPE-IMC asset set under `.github/assets/readme` and embeds it in key docs.
- Live GitHub render should be verified after push; no divergence is acceptable for the docs surfaces listed in `docs/DOC_REGISTRY.md`.

Key artifacts referenced:

- `proofs/reruns/benchmark_freeze_local/claim_scope_map.json`
- `proofs/reruns/contradiction_resolution_local/contradiction_resolution_manifest.json`

<p>
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>
