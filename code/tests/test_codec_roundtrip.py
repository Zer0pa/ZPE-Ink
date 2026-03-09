from __future__ import annotations

import random

import pytest

from zpe_ink.codec import ZPInkDecodeError, decode_zpink, encode_zpink
from zpe_ink.fixtures import generate_directional_stroke


def _sample_strokes() -> list[dict[str, list[int]]]:
    rng = random.Random(20260220)
    return [generate_directional_stroke(rng, segments=10) for _ in range(6)]


def test_lossless_roundtrip_bit_exact() -> None:
    strokes = _sample_strokes()
    encoded = encode_zpink(strokes, mode="lossless", seed=20260220)
    decoded = decode_zpink(encoded)
    assert decoded["mode"] == "lossless"
    assert decoded["seed"] == 20260220
    assert decoded["strokes"] == strokes


def test_crc_tamper_detection() -> None:
    strokes = _sample_strokes()
    encoded = bytearray(encode_zpink(strokes))
    encoded[-1] ^= 0x01
    with pytest.raises(ZPInkDecodeError, match="CRC"):
        decode_zpink(bytes(encoded))


def test_reject_truncated_payload() -> None:
    strokes = _sample_strokes()
    encoded = encode_zpink(strokes)
    with pytest.raises(ZPInkDecodeError):
        decode_zpink(encoded[:-5])


def test_quantized_high_mode_stays_finite() -> None:
    strokes = _sample_strokes()
    encoded = encode_zpink(strokes, mode="high")
    decoded = decode_zpink(encoded)
    assert len(decoded["strokes"]) == len(strokes)
    for stroke in decoded["strokes"]:
        assert len(stroke["x"]) > 0
