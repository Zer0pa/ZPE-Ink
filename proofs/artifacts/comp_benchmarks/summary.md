# ZPE-Ink Comp Benchmark Summary (Wave-CB Phase 1)

Generated: 2026-04-25T22:26:16.718407+00:00
Comparators: gzip(level=6), zlib(level=6)
Data source: in-repo deterministic synthetic fixtures (seeds 20260220 [synthetic_directional_64a], 20260221 [synthetic_directional_64b_sin_pressure])
Buffer layout: int32_le concat(x, y, pressure, tilt, azimuth)
Comparator path: c_apples_to_apples_same_buffer_int32_synthetic

## Aggregate compression ratio (bytes-weighted, raw_bytes / encoded_bytes)
- gzip:  7.336
- zlib:  7.441
- zpink: 12.735

## Hausdorff fidelity (xy locus, px)
- ZPE-Ink max across 128 strokes: 0.000000

## Verdict: PASS (property: lossless_roundtrip)

## Honest framing
These ratios are measured on in-repo synthetic stroke fixtures designed
to exercise the codec's integer-native delta+RLE path. They are NOT
measured on real IAM, UNIPEN, CROHME, UJI, or QuickDraw corpora.
Synthetic fixtures favor RLE-friendly inputs by design; ZPE-Ink does not
claim raw CR dominance over gzip/zlib on real handwriting. It claims
lossless roundtrip with structured semantics (Hausdorff = 0.0 px on x,y).
Comparator numbers are reported as-found.
