use crc32fast::Hasher;
use serde::Serialize;
use wasm_bindgen::prelude::*;

const MAGIC: &[u8; 5] = b"ZPINK";
const VERSION: u8 = 1;
const FLAG_PRESSURE: u8 = 0b001;
const FLAG_TILT: u8 = 0b010;
const FLAG_AZIMUTH: u8 = 0b100;

#[derive(Serialize)]
struct Decoded {
    magic: String,
    version: u8,
    mode: String,
    flags: u8,
    seed: u32,
    strokes: Vec<Stroke>,
}

#[derive(Serialize)]
struct Stroke {
    x: Vec<i32>,
    y: Vec<i32>,
    pressure: Vec<i32>,
    tilt: Vec<i32>,
    azimuth: Vec<i32>,
}

#[wasm_bindgen]
pub fn decode_to_json(input: &[u8]) -> Result<String, JsValue> {
    match decode_impl(input) {
        Ok(decoded) => serde_json::to_string(&decoded)
            .map_err(|err| JsValue::from_str(&format!("json serialization failed: {err}"))),
        Err(err) => Err(JsValue::from_str(&err)),
    }
}

fn decode_impl(input: &[u8]) -> Result<Decoded, String> {
    if input.len() < 22 {
        return Err("stream too short for header".to_string());
    }

    if &input[0..5] != MAGIC {
        return Err("invalid magic".to_string());
    }
    let version = input[5];
    if version != VERSION {
        return Err(format!("unsupported version: {version}"));
    }

    let mode_code = input[6];
    let mode = match mode_code {
        0 => "lossless",
        1 => "high",
        2 => "medium",
        3 => "sketch",
        _ => return Err(format!("invalid mode code: {mode_code}")),
    }
    .to_string();

    let flags = input[7];
    if (flags & FLAG_PRESSURE) == 0 {
        return Err("pressure channel is mandatory".to_string());
    }

    let stroke_count = u16::from_le_bytes([input[8], input[9]]) as usize;
    let seed = u32::from_le_bytes([input[10], input[11], input[12], input[13]]);
    let payload_len = u32::from_le_bytes([input[14], input[15], input[16], input[17]]) as usize;
    let payload_crc = u32::from_le_bytes([input[18], input[19], input[20], input[21]]);

    let payload = &input[22..];
    if payload.len() != payload_len {
        return Err("payload length mismatch".to_string());
    }

    let mut hasher = Hasher::new();
    hasher.update(payload);
    let computed = hasher.finalize();
    if computed != payload_crc {
        return Err("payload CRC mismatch".to_string());
    }

    let mut offset = 0usize;
    let has_tilt = (flags & FLAG_TILT) != 0;
    let has_azimuth = (flags & FLAG_AZIMUTH) != 0;

    let mut strokes = Vec::with_capacity(stroke_count);
    for _ in 0..stroke_count {
        let point_count = read_u16(payload, &mut offset)? as usize;
        if point_count == 0 {
            return Err("stroke has zero points".to_string());
        }

        let x0 = read_i32(payload, &mut offset)?;
        let y0 = read_i32(payload, &mut offset)?;

        let x_len = read_u32(payload, &mut offset)? as usize;
        let x_end = checked_end(offset, x_len, payload.len(), "x stream")?;
        let x_deltas = decode_delta_rle(&payload[offset..x_end], point_count.saturating_sub(1))?;
        offset = x_end;

        let y_len = read_u32(payload, &mut offset)? as usize;
        let y_end = checked_end(offset, y_len, payload.len(), "y stream")?;
        let y_deltas = decode_delta_rle(&payload[offset..y_end], point_count.saturating_sub(1))?;
        offset = y_end;

        let mut x = Vec::with_capacity(point_count);
        let mut y = Vec::with_capacity(point_count);
        x.push(x0);
        y.push(y0);
        for delta in x_deltas {
            let next = x.last().copied().unwrap_or(0).wrapping_add(delta);
            x.push(next);
        }
        for delta in y_deltas {
            let next = y.last().copied().unwrap_or(0).wrapping_add(delta);
            y.push(next);
        }

        let p0 = read_u16(payload, &mut offset)? as i32;
        let p_len = read_u32(payload, &mut offset)? as usize;
        let p_end = checked_end(offset, p_len, payload.len(), "pressure stream")?;
        let p_deltas = decode_delta_rle(&payload[offset..p_end], point_count.saturating_sub(1))?;
        offset = p_end;

        let mut pressure = Vec::with_capacity(point_count);
        pressure.push(p0);
        for delta in p_deltas {
            let next = pressure.last().copied().unwrap_or(0) + delta;
            if !(0..=1023).contains(&next) {
                return Err("pressure out of range".to_string());
            }
            pressure.push(next);
        }

        let mut tilt = vec![0; point_count];
        if has_tilt {
            let t0 = read_i16(payload, &mut offset)? as i32;
            let t_len = read_u32(payload, &mut offset)? as usize;
            let t_end = checked_end(offset, t_len, payload.len(), "tilt stream")?;
            let t_deltas = decode_delta_rle(&payload[offset..t_end], point_count.saturating_sub(1))?;
            offset = t_end;
            tilt = Vec::with_capacity(point_count);
            tilt.push(t0);
            for delta in t_deltas {
                let next = tilt.last().copied().unwrap_or(0) + delta;
                if !(-900..=900).contains(&next) {
                    return Err("tilt out of range".to_string());
                }
                tilt.push(next);
            }
        }

        let mut azimuth = vec![0; point_count];
        if has_azimuth {
            let a0 = read_i16(payload, &mut offset)? as i32;
            let a_len = read_u32(payload, &mut offset)? as usize;
            let a_end = checked_end(offset, a_len, payload.len(), "azimuth stream")?;
            let a_deltas = decode_delta_rle(&payload[offset..a_end], point_count.saturating_sub(1))?;
            offset = a_end;
            azimuth = Vec::with_capacity(point_count);
            azimuth.push(a0);
            for delta in a_deltas {
                let next = azimuth.last().copied().unwrap_or(0) + delta;
                if !(0..=3600).contains(&next) {
                    return Err("azimuth out of range".to_string());
                }
                azimuth.push(next);
            }
        }

        strokes.push(Stroke {
            x,
            y,
            pressure,
            tilt,
            azimuth,
        });
    }

    if offset != payload.len() {
        return Err("payload contains trailing bytes".to_string());
    }

    Ok(Decoded {
        magic: "ZPINK".to_string(),
        version,
        mode,
        flags,
        seed,
        strokes,
    })
}

fn checked_end(offset: usize, len: usize, total: usize, label: &str) -> Result<usize, String> {
    offset
        .checked_add(len)
        .filter(|end| *end <= total)
        .ok_or_else(|| format!("{label} length overflows payload"))
}

fn read_u16(data: &[u8], offset: &mut usize) -> Result<u16, String> {
    if *offset + 2 > data.len() {
        return Err("unexpected end of payload (u16)".to_string());
    }
    let value = u16::from_le_bytes([data[*offset], data[*offset + 1]]);
    *offset += 2;
    Ok(value)
}

fn read_i16(data: &[u8], offset: &mut usize) -> Result<i16, String> {
    if *offset + 2 > data.len() {
        return Err("unexpected end of payload (i16)".to_string());
    }
    let value = i16::from_le_bytes([data[*offset], data[*offset + 1]]);
    *offset += 2;
    Ok(value)
}

fn read_u32(data: &[u8], offset: &mut usize) -> Result<u32, String> {
    if *offset + 4 > data.len() {
        return Err("unexpected end of payload (u32)".to_string());
    }
    let value = u32::from_le_bytes([
        data[*offset],
        data[*offset + 1],
        data[*offset + 2],
        data[*offset + 3],
    ]);
    *offset += 4;
    Ok(value)
}

fn read_i32(data: &[u8], offset: &mut usize) -> Result<i32, String> {
    if *offset + 4 > data.len() {
        return Err("unexpected end of payload (i32)".to_string());
    }
    let value = i32::from_le_bytes([
        data[*offset],
        data[*offset + 1],
        data[*offset + 2],
        data[*offset + 3],
    ]);
    *offset += 4;
    Ok(value)
}

fn zigzag_decode(value: u32) -> i32 {
    ((value >> 1) as i32) ^ (-((value & 1) as i32))
}

fn decode_varuint(data: &[u8], offset: &mut usize) -> Result<u32, String> {
    let mut value: u32 = 0;
    let mut shift = 0u32;

    while *offset < data.len() {
        let byte = data[*offset];
        *offset += 1;
        value |= ((byte & 0x7F) as u32) << shift;

        if (byte & 0x80) == 0 {
            return Ok(value);
        }

        shift += 7;
        if shift > 35 {
            return Err("varuint overflow".to_string());
        }
    }

    Err("unexpected end of stream while decoding varuint".to_string())
}

fn decode_delta_rle(encoded: &[u8], count: usize) -> Result<Vec<i32>, String> {
    if count == 0 {
        return Ok(Vec::new());
    }

    let mut out = Vec::with_capacity(count);
    let mut offset = 0usize;

    while out.len() < count {
        if offset >= encoded.len() {
            return Err("delta stream ended before expected count".to_string());
        }
        let encoded_delta = decode_varuint(encoded, &mut offset)?;
        let run = decode_varuint(encoded, &mut offset)? as usize;
        if run == 0 {
            return Err("delta stream contains zero-length run".to_string());
        }
        let delta = zigzag_decode(encoded_delta);
        for _ in 0..run {
            out.push(delta);
            if out.len() > count {
                return Err("delta stream run lengths overflow point count".to_string());
            }
        }
    }

    if offset != encoded.len() {
        return Err("delta stream has trailing bytes".to_string());
    }

    Ok(out)
}
