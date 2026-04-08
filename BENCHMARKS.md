# ZPE-Ink Benchmarks

Public rows only. No proxy data is promoted here.

## Methodology

1. Run from the repo root: `python code/scripts/run_phase3_public_benchmarks.py`
2. Artifact path: `proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json`
3. Baseline: raw float32 `x/y` payload, matching the repo's current authority surface.
4. Fidelity rule: `exact` means decode output matched the source stroke arrays byte-for-byte at the integer channel level.
5. Registration-gated datasets stay blocked until the real corpus is acquired in-lane. No proxy values are substituted into this table.

## Dataset Table

| dataset | strokes | points_per_stroke | raw_size | compressed | ratio | roundtrip_fidelity |
|---|---:|---:|---:|---:|---:|---|
| IAM On-Line Handwriting | blocked | blocked | blocked | blocked | blocked | blocked |
| CASIA Online Handwriting | blocked | blocked | blocked | blocked | blocked | blocked |
| UJI Pen Characters | 1,854 | 40.23 | 596,736 B | 370,379 B | 1.6111x | exact |

## Sources

- IAM On-Line Handwriting: `https://fki.tic.heia-fr.ch/databases/iam-on-line-handwriting-database`
  Probe result on 2026-04-08: `HTTP/1.1 200 OK`. No direct public corpus download was established for this phase.
- CASIA Online Handwriting: `https://nlpr.ia.ac.cn/databases/handwriting/home.html`
  Probe result on 2026-04-08: `rc=28`, `status=000` after the bounded 20-second probe. No direct public corpus download was established for this phase.
- UJI Pen Characters: `https://archive.ics.uci.edu/dataset/160/uji+pen+characters`
  Download URL used: `https://archive.ics.uci.edu/static/public/160/uji+pen+characters.zip`
  Archive SHA-256: `06e484103d21ead80ec7675059d3ffe66f39f51bfcb9c77a00fbbfb1c85546dc`

## Notes

- UJI metrics were measured over `1,364` isolated-character samples and `74,592` total points.
- This file does not widen the repo claim surface beyond the current structured-tier authority boundary.
