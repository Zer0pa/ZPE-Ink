from __future__ import annotations

import binascii
import json
import struct
from typing import Any

MAGIC = b"ZPINK"
VERSION = 1
MODE_TO_CODE = {"lossless": 0, "high": 1, "medium": 2, "sketch": 3}
CODE_TO_MODE = {value: key for key, value in MODE_TO_CODE.items()}
HEADER_STRUCT = struct.Struct("<5sBBBHIII")

FLAG_PRESSURE = 0b001
FLAG_TILT = 0b010
FLAG_AZIMUTH = 0b100


class ZPInkEncodeError(ValueError):
    """Raised when input cannot be encoded as .zpink."""


class ZPInkDecodeError(ValueError):
    """Raised when input is not a valid .zpink stream."""


def _zigzag_encode(value: int) -> int:
    return (value << 1) ^ (value >> 31)


def _zigzag_decode(value: int) -> int:
    return (value >> 1) ^ -(value & 1)


def _encode_varuint(value: int) -> bytes:
    if value < 0:
        raise ZPInkEncodeError(f"varuint cannot encode negative value: {value}")
    out = bytearray()
    v = value
    while True:
        chunk = v & 0x7F
        v >>= 7
        if v:
            out.append(chunk | 0x80)
        else:
            out.append(chunk)
            return bytes(out)


def _append_varuint(out: bytearray, value: int) -> None:
    if value < 0:
        raise ZPInkEncodeError(f"varuint cannot encode negative value: {value}")
    v = value
    while v >= 0x80:
        out.append((v & 0x7F) | 0x80)
        v >>= 7
    out.append(v)


def _decode_varuint(data: bytes, offset: int) -> tuple[int, int]:
    value = 0
    shift = 0
    idx = offset
    while idx < len(data):
        byte = data[idx]
        idx += 1
        value |= (byte & 0x7F) << shift
        if (byte & 0x80) == 0:
            return value, idx
        shift += 7
        if shift > 35:
            raise ZPInkDecodeError("varuint overflow")
    raise ZPInkDecodeError("unexpected end of stream while decoding varuint")


def _encode_delta_rle(deltas: list[int]) -> bytes:
    if not deltas:
        return b""
    out = bytearray()
    idx = 0
    total = len(deltas)
    while idx < total:
        current = deltas[idx]
        run = 1
        while idx + run < total and deltas[idx + run] == current:
            run += 1
        _append_varuint(out, _zigzag_encode(current))
        _append_varuint(out, run)
        idx += run
    return bytes(out)


def _decode_delta_rle(encoded: bytes, count: int) -> list[int]:
    if count == 0:
        return []
    out: list[int] = []
    idx = 0
    while len(out) < count:
        if idx >= len(encoded):
            raise ZPInkDecodeError("delta stream ended before expected count")
        encoded_delta, idx = _decode_varuint(encoded, idx)
        run, idx = _decode_varuint(encoded, idx)
        if run == 0:
            raise ZPInkDecodeError("delta stream contains zero-length run")
        out.extend([_zigzag_decode(encoded_delta)] * run)
    if len(out) != count:
        raise ZPInkDecodeError("delta stream run lengths overflow point count")
    if idx != len(encoded):
        raise ZPInkDecodeError("delta stream has trailing bytes")
    return out


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ZPInkEncodeError(message)


def _validate_int_range(name: str, value: int, lo: int, hi: int) -> None:
    if not (lo <= value <= hi):
        raise ZPInkEncodeError(f"{name}={value} outside [{lo}, {hi}]")


def _validate_series_range(name: str, values: list[int], lo: int, hi: int) -> None:
    if not values:
        return
    vmin = min(values)
    vmax = max(values)
    if vmin < lo or vmax > hi:
        raise ZPInkEncodeError(f"{name} outside [{lo}, {hi}]")


def _read_u32(data: bytes, offset: int) -> tuple[int, int]:
    end = offset + 4
    if end > len(data):
        raise ZPInkDecodeError("unexpected end of payload (u32)")
    return struct.unpack_from("<I", data, offset)[0], end


def _read_u16(data: bytes, offset: int) -> tuple[int, int]:
    end = offset + 2
    if end > len(data):
        raise ZPInkDecodeError("unexpected end of payload (u16)")
    return struct.unpack_from("<H", data, offset)[0], end


def _read_i16(data: bytes, offset: int) -> tuple[int, int]:
    end = offset + 2
    if end > len(data):
        raise ZPInkDecodeError("unexpected end of payload (i16)")
    return struct.unpack_from("<h", data, offset)[0], end


def _read_i32(data: bytes, offset: int) -> tuple[int, int]:
    end = offset + 4
    if end > len(data):
        raise ZPInkDecodeError("unexpected end of payload (i32)")
    return struct.unpack_from("<i", data, offset)[0], end


def _apply_quantization(values: list[int], mode: str) -> list[int]:
    if mode == "lossless":
        return values
    # "high" mode keeps sub-pixel fidelity while increasing repeatability in delta runs.
    step = 2 if mode == "high" else 4 if mode == "medium" else 8
    return [int(round(value / step) * step) for value in values]


def encode_zpink(
    strokes: list[dict[str, list[int]]],
    *,
    mode: str = "lossless",
    include_tilt: bool = True,
    include_azimuth: bool = True,
    seed: int = 20260220,
) -> bytes:
    """Encode stroke arrays into .zpink bytes.

    Stroke schema per entry:
    {
      "x": [int...],
      "y": [int...],
      "pressure": [int...],
      "tilt": [int...],
      "azimuth": [int...],
    }
    """

    if mode not in MODE_TO_CODE:
        raise ZPInkEncodeError(f"unsupported mode: {mode}")

    flags = FLAG_PRESSURE
    if include_tilt:
        flags |= FLAG_TILT
    if include_azimuth:
        flags |= FLAG_AZIMUTH

    payload = bytearray()

    for stroke_index, stroke in enumerate(strokes):
        x = [int(v) for v in stroke.get("x", [])]
        y = [int(v) for v in stroke.get("y", [])]
        pressure = [int(v) for v in stroke.get("pressure", [])]
        tilt = [int(v) for v in stroke.get("tilt", [0] * len(x))]
        azimuth = [int(v) for v in stroke.get("azimuth", [0] * len(x))]

        x = _apply_quantization(x, mode)
        y = _apply_quantization(y, mode)

        point_count = len(x)
        _require(point_count > 0, f"stroke[{stroke_index}] must contain at least one point")
        _require(point_count <= 65535, f"stroke[{stroke_index}] point_count exceeds u16")
        _require(len(y) == point_count, f"stroke[{stroke_index}] y length mismatch")
        _require(len(pressure) == point_count, f"stroke[{stroke_index}] pressure length mismatch")
        _require(len(tilt) == point_count, f"stroke[{stroke_index}] tilt length mismatch")
        _require(len(azimuth) == point_count, f"stroke[{stroke_index}] azimuth length mismatch")

        _validate_series_range("x", x, -(2**31), 2**31 - 1)
        _validate_series_range("y", y, -(2**31), 2**31 - 1)
        _validate_series_range("pressure", pressure, 0, 1023)
        _validate_series_range("tilt", tilt, -900, 900)
        _validate_series_range("azimuth", azimuth, 0, 3600)

        dx = [x[i] - x[i - 1] for i in range(1, point_count)]
        dy = [y[i] - y[i - 1] for i in range(1, point_count)]
        dp = [pressure[i] - pressure[i - 1] for i in range(1, point_count)]
        dt = [tilt[i] - tilt[i - 1] for i in range(1, point_count)]
        da = [azimuth[i] - azimuth[i - 1] for i in range(1, point_count)]

        x_stream = _encode_delta_rle(dx)
        y_stream = _encode_delta_rle(dy)
        p_stream = _encode_delta_rle(dp)
        t_stream = _encode_delta_rle(dt)
        a_stream = _encode_delta_rle(da)

        payload.extend(struct.pack("<H", point_count))
        payload.extend(struct.pack("<i", x[0]))
        payload.extend(struct.pack("<i", y[0]))

        payload.extend(struct.pack("<I", len(x_stream)))
        payload.extend(x_stream)
        payload.extend(struct.pack("<I", len(y_stream)))
        payload.extend(y_stream)

        payload.extend(struct.pack("<H", pressure[0]))
        payload.extend(struct.pack("<I", len(p_stream)))
        payload.extend(p_stream)

        if include_tilt:
            payload.extend(struct.pack("<h", tilt[0]))
            payload.extend(struct.pack("<I", len(t_stream)))
            payload.extend(t_stream)

        if include_azimuth:
            payload.extend(struct.pack("<h", azimuth[0]))
            payload.extend(struct.pack("<I", len(a_stream)))
            payload.extend(a_stream)

    payload_bytes = bytes(payload)
    payload_crc = binascii.crc32(payload_bytes) & 0xFFFFFFFF
    header = HEADER_STRUCT.pack(
        MAGIC,
        VERSION,
        MODE_TO_CODE[mode],
        flags,
        len(strokes),
        seed,
        len(payload_bytes),
        payload_crc,
    )
    return header + payload_bytes


def decode_zpink(data: bytes) -> dict[str, Any]:
    if len(data) < HEADER_STRUCT.size:
        raise ZPInkDecodeError("stream too short for header")

    magic, version, mode_code, flags, stroke_count, seed, payload_len, payload_crc = HEADER_STRUCT.unpack_from(
        data, 0
    )

    if magic != MAGIC:
        raise ZPInkDecodeError("invalid magic")
    if version != VERSION:
        raise ZPInkDecodeError(f"unsupported version: {version}")
    if mode_code not in CODE_TO_MODE:
        raise ZPInkDecodeError(f"invalid mode code: {mode_code}")

    payload = data[HEADER_STRUCT.size :]
    if len(payload) != payload_len:
        raise ZPInkDecodeError("payload length mismatch")
    if (binascii.crc32(payload) & 0xFFFFFFFF) != payload_crc:
        raise ZPInkDecodeError("payload CRC mismatch")

    offset = 0
    strokes: list[dict[str, list[int]]] = []
    has_tilt = (flags & FLAG_TILT) != 0
    has_azimuth = (flags & FLAG_AZIMUTH) != 0
    has_pressure = (flags & FLAG_PRESSURE) != 0
    if not has_pressure:
        raise ZPInkDecodeError("pressure channel is mandatory")

    for stroke_index in range(stroke_count):
        point_count, offset = _read_u16(payload, offset)
        if point_count == 0:
            raise ZPInkDecodeError(f"stroke[{stroke_index}] has zero points")

        x0, offset = _read_i32(payload, offset)
        y0, offset = _read_i32(payload, offset)

        x_stream_len, offset = _read_u32(payload, offset)
        x_stream_end = offset + x_stream_len
        if x_stream_end > len(payload):
            raise ZPInkDecodeError("x stream length overflows payload")
        x_deltas = _decode_delta_rle(payload[offset:x_stream_end], point_count - 1)
        offset = x_stream_end

        y_stream_len, offset = _read_u32(payload, offset)
        y_stream_end = offset + y_stream_len
        if y_stream_end > len(payload):
            raise ZPInkDecodeError("y stream length overflows payload")
        y_deltas = _decode_delta_rle(payload[offset:y_stream_end], point_count - 1)
        offset = y_stream_end

        x = [x0]
        y = [y0]
        for delta in x_deltas:
            x.append(x[-1] + delta)
        for delta in y_deltas:
            y.append(y[-1] + delta)

        p0, offset = _read_u16(payload, offset)
        p_stream_len, offset = _read_u32(payload, offset)
        p_stream_end = offset + p_stream_len
        if p_stream_end > len(payload):
            raise ZPInkDecodeError("pressure stream length overflows payload")
        p_deltas = _decode_delta_rle(payload[offset:p_stream_end], point_count - 1)
        offset = p_stream_end

        pressure = [int(p0)]
        for delta in p_deltas:
            pressure.append(pressure[-1] + delta)

        tilt = [0] * point_count
        if has_tilt:
            t0, offset = _read_i16(payload, offset)
            t_stream_len, offset = _read_u32(payload, offset)
            t_stream_end = offset + t_stream_len
            if t_stream_end > len(payload):
                raise ZPInkDecodeError("tilt stream length overflows payload")
            t_deltas = _decode_delta_rle(payload[offset:t_stream_end], point_count - 1)
            offset = t_stream_end
            tilt = [int(t0)]
            for delta in t_deltas:
                tilt.append(tilt[-1] + delta)

        azimuth = [0] * point_count
        if has_azimuth:
            a0, offset = _read_i16(payload, offset)
            a_stream_len, offset = _read_u32(payload, offset)
            a_stream_end = offset + a_stream_len
            if a_stream_end > len(payload):
                raise ZPInkDecodeError("azimuth stream length overflows payload")
            a_deltas = _decode_delta_rle(payload[offset:a_stream_end], point_count - 1)
            offset = a_stream_end
            azimuth = [int(a0)]
            for delta in a_deltas:
                azimuth.append(azimuth[-1] + delta)

        for idx in range(point_count):
            p = pressure[idx]
            if p < 0 or p > 1023:
                raise ZPInkDecodeError("pressure out of range")
            t = tilt[idx]
            if t < -900 or t > 900:
                raise ZPInkDecodeError("tilt out of range")
            a = azimuth[idx]
            if a < 0 or a > 3600:
                raise ZPInkDecodeError("azimuth out of range")

        strokes.append(
            {
                "x": x,
                "y": y,
                "pressure": pressure,
                "tilt": tilt,
                "azimuth": azimuth,
            }
        )

    if offset != len(payload):
        raise ZPInkDecodeError("payload contains trailing bytes")

    return {
        "magic": MAGIC.decode("ascii"),
        "version": version,
        "mode": CODE_TO_MODE[mode_code],
        "flags": flags,
        "seed": seed,
        "strokes": strokes,
    }


def canonical_json(decoded: dict[str, Any]) -> str:
    """Canonical JSON used for deterministic parity hashing across runtimes."""
    return json.dumps(decoded, sort_keys=True, separators=(",", ":"))
