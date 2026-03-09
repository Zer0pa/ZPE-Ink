# ZPINK Spec v1

## Header (22 bytes, little-endian)
- `magic[5]`: ASCII `ZPINK`
- `version[u8]`: `1`
- `mode[u8]`: `0=lossless`, `1=high`, `2=medium`, `3=sketch`
- `flags[u8]`: bitmask (`0x1 pressure`, `0x2 tilt`, `0x4 azimuth`)
- `stroke_count[u16]`
- `seed[u32]`
- `payload_len[u32]`
- `payload_crc32[u32]`

## Per-stroke Payload
- `point_count[u16]`
- `x0[i32]`
- `y0[i32]`
- `x_delta_stream_len[u32]` + RLE-varint stream
- `y_delta_stream_len[u32]` + RLE-varint stream
- `pressure0[u16]`
- `pressure_delta_stream_len[u32]` + RLE-varint stream
- If `flags & 0x2`:
  - `tilt0[i16]`
  - `tilt_delta_stream_len[u32]` + RLE-varint stream
- If `flags & 0x4`:
  - `azimuth0[i16]`
  - `azimuth_delta_stream_len[u32]` + RLE-varint stream

## Delta Stream Encoding
- Deltas are run-length encoded as repeated segments:
  - `delta[zigzag-varuint]`
  - `run_len[varuint]`
- Decoders must fail on zero-length runs, overflow, and trailing bytes.
