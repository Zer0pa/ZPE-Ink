# ZPE-Ink Comp Benchmark Summary (Wave-CB Phase 1)

Generated: 2026-04-25T21:30:20.916745+00:00
Comparators: gzip(level=6), zlib(level=6)
Data source: in-repo deterministic fixtures (seeds 20260220, 20260221)
Buffer layout: int32_le concat(x, y, pressure, tilt, azimuth)

## Aggregate compression ratio (raw_bytes / encoded_bytes)
- gzip:  7.336
- zlib:  7.441
- zpink: 12.735

## Hausdorff fidelity (xy locus, px)
- ZPE-Ink max across 128 strokes: 0.000000

## Honest framing
ZPE-Ink does not claim raw CR dominance over gzip/zlib. It claims
lossless roundtrip with structured semantics (Hausdorff = 0.0 px
on x,y). Comparator numbers are reported as-found.
