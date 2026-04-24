<p>
  <img src="../../.github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>

# ZPINK Token Sidecar Contract v1

Candidate-only contract for a deterministic token sidecar derived from sovereign `.zpink` payloads.

## Status

- `candidate_status`: `CANDIDATE_ONLY`
- `.zpink` remains the transport authority
- this surface is allowed only for bounded interchange indexing and token-research follow-on work

## Purpose

The token sidecar exposes a deterministic 8-direction token view of `.zpink` stroke streams without replacing the `.zpink` payload. It exists to support bounded interoperability and token-surface experiments after the April 2026 truth-reconciliation rerun.

## Required Fields

| field | rule |
|---|---|
| `schema` | `zpeink-token-sidecar-v1` |
| `candidate_status` | must be `CANDIDATE_ONLY` |
| `runtime_authority` | must explicitly preserve `.zpink` as sovereign |
| `source_format` | source payload type; current allowed source is `.zpink` |
| `source_sha256` | SHA-256 of the source payload when derived from bytes |
| `stroke_count` | number of strokes represented |
| `token_count` | total directional tokens across all strokes |
| `token_distribution` | counts for tokens `0..7` |
| `strokes[]` | per-stroke token records |
| `sidecar_sha256` | SHA-256 of the canonicalized sidecar document |

## Per-Stroke Record

| field | rule |
|---|---|
| `point_count` | source point count |
| `origin` | first `x,y` point |
| `step_size` | median directional step used by the primitive-token reconstruction |
| `tokens` | directional token list |
| `pressure` | full pressure channel |
| `tilt` | full tilt channel |
| `azimuth` | full azimuth channel |

## Failure Boundary

This sidecar is not a general-fidelity runtime. High-velocity or non-directional corpora may degrade under primitive-token reconstruction. Any such degradation keeps the sidecar branch-only and blocks promotion to sovereign runtime status.
