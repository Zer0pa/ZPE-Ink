from __future__ import annotations

from zpe_ink.metrics import corpus_hausdorff
from zpe_ink.primitivetoken import (
    Point,
    _angle_to_dir,
    decode_primitive_strokes,
    decode_tokens_to_stroke,
    encode_primitive_strokes,
    encode_stroke_to_tokens,
    pack_tokens,
    points_to_stroke,
    stroke_to_points,
    unpack_tokens,
)


def test_direction_mapping() -> None:
    assert _angle_to_dir(0, -3) == 0
    assert _angle_to_dir(4, -4) == 1
    assert _angle_to_dir(5, 0) == 2
    assert _angle_to_dir(4, 4) == 3
    assert _angle_to_dir(0, 6) == 4
    assert _angle_to_dir(-3, 3) == 5
    assert _angle_to_dir(-7, 0) == 6
    assert _angle_to_dir(-5, -5) == 7


def test_roundtrip_cardinal_reconstruction_within_tolerance() -> None:
    points = [
        Point(10, 10, 500, -10, 100),
        Point(10, 9, 501, -10, 100),
        Point(11, 9, 502, -10, 100),
        Point(11, 10, 503, -10, 100),
        Point(10, 10, 504, -10, 100),
    ]
    tokens, side_channels, origin, step_size = encode_stroke_to_tokens(points)
    reconstructed = decode_tokens_to_stroke(tokens, side_channels, origin, step_size)
    assert corpus_hausdorff([points_to_stroke(points)], [points_to_stroke(reconstructed)]) < 2.0


def test_side_channel_preservation() -> None:
    stroke = {
        "x": [1, 2, 3, 4],
        "y": [1, 1, 2, 2],
        "pressure": [111, 222, 333, 444],
        "tilt": [-3, -2, -1, 0],
        "azimuth": [10, 20, 30, 40],
    }
    encoded = encode_primitive_strokes([stroke])
    decoded = decode_primitive_strokes(encoded)
    assert decoded[0]["pressure"] == stroke["pressure"]
    assert decoded[0]["tilt"] == stroke["tilt"]
    assert decoded[0]["azimuth"] == stroke["azimuth"]


def test_pack_unpack() -> None:
    tokens = [0, 1, 2, 3, 4, 5, 6, 7, -1]
    packed = pack_tokens(tokens)
    assert unpack_tokens(packed, len(tokens)) == tokens


def test_deterministic_output() -> None:
    stroke = {
        "x": [0, 1, 2, 2, 1],
        "y": [0, 0, -1, -2, -2],
        "pressure": [500, 500, 505, 505, 510],
        "tilt": [0, 0, 1, 1, 1],
        "azimuth": [10, 10, 15, 15, 20],
    }
    first = encode_primitive_strokes([stroke])
    second = encode_primitive_strokes([stroke])
    assert first == second
    assert stroke_to_points(stroke)[0] == Point(0, 0, 500, 0, 10)
