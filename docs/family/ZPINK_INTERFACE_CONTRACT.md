# ZPINK Spec v1

This document is the canonical `.zpink` packet contract. Any compatibility changes must update `docs/family/ZPINK_COMPATIBILITY_VECTOR.json`.

Reader orientation: a `.zpink` packet represents a stroke stream with deterministic deltas. `mode` selects fidelity tier, `flags` gate optional channels, and pressure is mandatory in v1 (the codec enforces it for every stroke).

## Header (22 bytes, little-endian)

| section | field | encoding | value_or_rule | required_when |
|---|---|---|---|---|
| header | `magic` | `ASCII[5]` | `ZPINK` | always |
| header | `version` | `u8` | `1` | always |
| header | `mode` | `u8` | `0=lossless`, `1=high`, `2=medium`, `3=sketch` | always |
| header | `flags` | `u8 bitmask` | `0x1 pressure`, `0x2 tilt`, `0x4 azimuth` | always |
| header | `stroke_count` | `u16` | number of strokes | always |
| header | `seed` | `u32` | determinism seed | always |
| header | `payload_len` | `u32` | bytes after header | always |
| header | `payload_crc32` | `u32` | CRC32 of payload | always |

## Per-stroke payload

| section | field | encoding | value_or_rule | required_when |
|---|---|---|---|---|
| stroke | `point_count` | `u16` | must be &gt; 0 | always |
| stroke | `x0` | `i32` | first x | always |
| stroke | `y0` | `i32` | first y | always |
| stroke | `x_delta_stream_len` | `u32` | bytes | always |
| stroke | `x_delta_stream` | RLE varint | deltas for remaining points | always |
| stroke | `y_delta_stream_len` | `u32` | bytes | always |
| stroke | `y_delta_stream` | RLE varint | deltas for remaining points | always |
| stroke | `pressure0` | `u16` | first pressure | always |
| stroke | `pressure_delta_stream_len` | `u32` | bytes | always |
| stroke | `pressure_delta_stream` | RLE varint | deltas | always |
| stroke | `tilt0` | `i16` | first tilt | `flags & 0x2` |
| stroke | `tilt_delta_stream_len` | `u32` | bytes | `flags & 0x2` |
| stroke | `tilt_delta_stream` | RLE varint | deltas | `flags & 0x2` |
| stroke | `azimuth0` | `i16` | first azimuth | `flags & 0x4` |
| stroke | `azimuth_delta_stream_len` | `u32` | bytes | `flags & 0x4` |
| stroke | `azimuth_delta_stream` | RLE varint | deltas | `flags & 0x4` |

## Delta stream encoding rules

- Deltas are run-length encoded as repeated segments: `delta[zigzag-varuint]` then `run_len[varuint]`.
- Decoders must fail on zero-length runs, overflow, and trailing bytes.
