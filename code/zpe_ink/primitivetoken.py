from __future__ import annotations

import math
import struct
from dataclasses import dataclass
from typing import Iterable

from .codec import ZPInkDecodeError, ZPInkEncodeError, _decode_delta_rle, _encode_delta_rle

MAGIC = b"ZPTK"
VERSION = 1
HEADER_STRUCT = struct.Struct("<4sBI")
STROKE_HEADER_STRUCT = struct.Struct("<IiihI")

DIRECTION_NAMES = {
    0: "N",
    1: "NE",
    2: "E",
    3: "SE",
    4: "S",
    5: "SW",
    6: "W",
    7: "NW",
}
DIRECTION_VECTORS = {
    0: (0, -1),
    1: (1, -1),
    2: (1, 0),
    3: (1, 1),
    4: (0, 1),
    5: (-1, 1),
    6: (-1, 0),
    7: (-1, -1),
}


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    pressure: int = 512
    tilt: int = 0
    azimuth: int = 0


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ZPInkEncodeError(message)


def _read_struct(data: bytes, offset: int, fmt: struct.Struct) -> tuple[tuple[int, ...], int]:
    end = offset + fmt.size
    if end > len(data):
        raise ZPInkDecodeError("primitive-token payload truncated")
    return fmt.unpack_from(data, offset), end


def _read_u32(data: bytes, offset: int) -> tuple[int, int]:
    (value,), next_offset = _read_struct(data, offset, struct.Struct("<I"))
    return value, next_offset


def _read_u16(data: bytes, offset: int) -> tuple[int, int]:
    (value,), next_offset = _read_struct(data, offset, struct.Struct("<H"))
    return value, next_offset


def _read_i16(data: bytes, offset: int) -> tuple[int, int]:
    (value,), next_offset = _read_struct(data, offset, struct.Struct("<h"))
    return value, next_offset


def _read_bytes(data: bytes, offset: int, size: int) -> tuple[bytes, int]:
    end = offset + size
    if end > len(data):
        raise ZPInkDecodeError("primitive-token stream overflows payload")
    return data[offset:end], end


def _coerce_points(points: Iterable[Point]) -> list[Point]:
    out = list(points)
    _require(bool(out), "stroke must contain at least one point")
    return out


def stroke_to_points(stroke: dict[str, list[int]]) -> list[Point]:
    x_vals = stroke.get("x", [])
    y_vals = stroke.get("y", [])
    pressure_vals = stroke.get("pressure", [])
    tilt_vals = stroke.get("tilt", [0] * len(x_vals))
    azimuth_vals = stroke.get("azimuth", [0] * len(x_vals))
    _require(len(x_vals) == len(y_vals), "stroke x/y channel length mismatch")
    _require(len(x_vals) == len(pressure_vals), "stroke pressure channel length mismatch")
    _require(len(x_vals) == len(tilt_vals), "stroke tilt channel length mismatch")
    _require(len(x_vals) == len(azimuth_vals), "stroke azimuth channel length mismatch")
    _require(bool(x_vals), "stroke must contain at least one point")
    return [
        Point(
            x=int(x_val),
            y=int(y_val),
            pressure=int(pressure_val),
            tilt=int(tilt_val),
            azimuth=int(azimuth_val),
        )
        for x_val, y_val, pressure_val, tilt_val, azimuth_val in zip(
            x_vals,
            y_vals,
            pressure_vals,
            tilt_vals,
            azimuth_vals,
        )
    ]


def points_to_stroke(points: Iterable[Point]) -> dict[str, list[int]]:
    pts = _coerce_points(points)
    return {
        "x": [point.x for point in pts],
        "y": [point.y for point in pts],
        "pressure": [point.pressure for point in pts],
        "tilt": [point.tilt for point in pts],
        "azimuth": [point.azimuth for point in pts],
    }


def _step_magnitude(dx: int, dy: int) -> int:
    return max(abs(dx), abs(dy))


def _estimate_step_size(points: list[Point]) -> int:
    magnitudes = [
        _step_magnitude(current.x - previous.x, current.y - previous.y)
        for previous, current in zip(points, points[1:])
        if current.x != previous.x or current.y != previous.y
    ]
    if not magnitudes:
        return 1
    ordered = sorted(magnitudes)
    return max(1, ordered[len(ordered) // 2])


def _angle_to_dir(dx: int, dy: int) -> int:
    if dx == 0 and dy == 0:
        return -1
    angle = (math.degrees(math.atan2(dx, -dy)) + 360.0) % 360.0
    return int(round(angle / 45.0)) % 8


def encode_stroke_to_tokens(points: list[Point]) -> tuple[list[int], list[tuple[int, int, int]], Point, int]:
    pts = _coerce_points(points)
    tokens: list[int] = []
    for previous, current in zip(pts, pts[1:]):
        tokens.append(_angle_to_dir(current.x - previous.x, current.y - previous.y))
    side_channels = [(point.pressure, point.tilt, point.azimuth) for point in pts]
    return tokens, side_channels, pts[0], _estimate_step_size(pts)


def decode_tokens_to_stroke(
    tokens: list[int],
    side_channels: list[tuple[int, int, int]],
    origin: Point,
    step_size: int,
) -> list[Point]:
    _require(step_size > 0, "step_size must be positive")
    _require(len(side_channels) == len(tokens) + 1, "side channel count must match point count")
    x_pos = origin.x
    y_pos = origin.y
    points = [origin]
    for index, token in enumerate(tokens, start=1):
        if token != -1:
            try:
                dx, dy = DIRECTION_VECTORS[token]
            except KeyError as exc:
                raise ZPInkDecodeError(f"invalid primitive token: {token}") from exc
            x_pos += dx * step_size
            y_pos += dy * step_size
        pressure, tilt, azimuth = side_channels[index]
        points.append(
            Point(
                x=int(x_pos),
                y=int(y_pos),
                pressure=int(pressure),
                tilt=int(tilt),
                azimuth=int(azimuth),
            )
        )
    return points


def pack_tokens(tokens: list[int]) -> bytes:
    out = bytearray()
    for index in range(0, len(tokens), 2):
        first = tokens[index]
        second = tokens[index + 1] if index + 1 < len(tokens) else None
        if first < -1 or first > 7:
            raise ZPInkEncodeError(f"primitive token outside supported range: {first}")
        high = (first + 1) & 0x0F
        if second is None:
            low = 0x0F
        else:
            if second < -1 or second > 7:
                raise ZPInkEncodeError(f"primitive token outside supported range: {second}")
            low = (second + 1) & 0x0F
        out.append((high << 4) | low)
    return bytes(out)


def unpack_tokens(data: bytes, expected_count: int) -> list[int]:
    tokens: list[int] = []
    for byte in data:
        for nibble in ((byte >> 4) & 0x0F, byte & 0x0F):
            if len(tokens) >= expected_count:
                return tokens
            if nibble == 0x0F:
                continue
            if nibble > 8:
                raise ZPInkDecodeError(f"invalid packed primitive nibble: {nibble}")
            tokens.append(nibble - 1)
    if len(tokens) != expected_count:
        raise ZPInkDecodeError("packed primitive token count mismatch")
    return tokens


def _encode_side_channel(values: list[int]) -> tuple[int, bytes]:
    deltas = [current - previous for previous, current in zip(values, values[1:])]
    return values[0], _encode_delta_rle(deltas)


def _decode_side_channel(initial: int, encoded: bytes, count: int) -> list[int]:
    values = [int(initial)]
    for delta in _decode_delta_rle(encoded, count - 1):
        values.append(values[-1] + delta)
    return values


def _encode_stroke_record(stroke: dict[str, list[int]]) -> bytes:
    points = stroke_to_points(stroke)
    tokens, _, origin, step_size = encode_stroke_to_tokens(points)
    packed_tokens = pack_tokens(tokens)
    pressure = [point.pressure for point in points]
    tilt = [point.tilt for point in points]
    azimuth = [point.azimuth for point in points]
    pressure0, pressure_stream = _encode_side_channel(pressure)
    tilt0, tilt_stream = _encode_side_channel(tilt)
    azimuth0, azimuth_stream = _encode_side_channel(azimuth)
    out = bytearray()
    out.extend(STROKE_HEADER_STRUCT.pack(len(points), origin.x, origin.y, step_size, len(packed_tokens)))
    out.extend(packed_tokens)
    out.extend(struct.pack("<H", pressure0))
    out.extend(struct.pack("<I", len(pressure_stream)))
    out.extend(pressure_stream)
    out.extend(struct.pack("<h", tilt0))
    out.extend(struct.pack("<I", len(tilt_stream)))
    out.extend(tilt_stream)
    out.extend(struct.pack("<H", azimuth0))
    out.extend(struct.pack("<I", len(azimuth_stream)))
    out.extend(azimuth_stream)
    return bytes(out)


def encode_primitive_strokes(strokes: list[dict[str, list[int]]]) -> bytes:
    _require(bool(strokes), "sample must contain at least one stroke")
    payload = bytearray()
    for stroke in strokes:
        payload.extend(_encode_stroke_record(stroke))
    return HEADER_STRUCT.pack(MAGIC, VERSION, len(strokes)) + payload


def decode_primitive_strokes(data: bytes) -> list[dict[str, list[int]]]:
    if len(data) < HEADER_STRUCT.size:
        raise ZPInkDecodeError("primitive-token stream too short")
    magic, version, stroke_count = HEADER_STRUCT.unpack_from(data, 0)
    if magic != MAGIC:
        raise ZPInkDecodeError("invalid primitive-token magic")
    if version != VERSION:
        raise ZPInkDecodeError(f"unsupported primitive-token version: {version}")

    offset = HEADER_STRUCT.size
    strokes: list[dict[str, list[int]]] = []
    for _ in range(stroke_count):
        point_count, origin_x, origin_y, step_size, packed_len = STROKE_HEADER_STRUCT.unpack_from(data, offset)
        offset += STROKE_HEADER_STRUCT.size
        packed_tokens, offset = _read_bytes(data, offset, packed_len)
        tokens = unpack_tokens(packed_tokens, max(0, point_count - 1))

        pressure0, offset = _read_u16(data, offset)
        pressure_len, offset = _read_u32(data, offset)
        pressure_stream, offset = _read_bytes(data, offset, pressure_len)

        tilt0, offset = _read_i16(data, offset)
        tilt_len, offset = _read_u32(data, offset)
        tilt_stream, offset = _read_bytes(data, offset, tilt_len)

        azimuth0, offset = _read_u16(data, offset)
        azimuth_len, offset = _read_u32(data, offset)
        azimuth_stream, offset = _read_bytes(data, offset, azimuth_len)

        pressure = _decode_side_channel(pressure0, pressure_stream, point_count)
        tilt = _decode_side_channel(tilt0, tilt_stream, point_count)
        azimuth = _decode_side_channel(azimuth0, azimuth_stream, point_count)
        side_channels = list(zip(pressure, tilt, azimuth))
        points = decode_tokens_to_stroke(tokens, side_channels, Point(origin_x, origin_y, pressure0, tilt0, azimuth0), step_size)
        strokes.append(points_to_stroke(points))

    if offset != len(data):
        raise ZPInkDecodeError("primitive-token stream has trailing bytes")
    return strokes


__all__ = [
    "DIRECTION_NAMES",
    "DIRECTION_VECTORS",
    "Point",
    "decode_primitive_strokes",
    "decode_tokens_to_stroke",
    "encode_primitive_strokes",
    "encode_stroke_to_tokens",
    "pack_tokens",
    "points_to_stroke",
    "stroke_to_points",
    "unpack_tokens",
]
