from __future__ import annotations

import random

from zpe_ink.codec import decode_zpink, encode_zpink
from zpe_ink.fixtures import generate_high_velocity_stroke


def test_high_frequency_strokes_roundtrip_lossless() -> None:
    rng = random.Random(20260408)
    strokes = [generate_high_velocity_stroke(rng, points=240) for _ in range(6)]

    encoded = encode_zpink(strokes, mode="lossless", seed=20260408)
    decoded = decode_zpink(encoded)

    assert decoded["mode"] == "lossless"
    assert decoded["seed"] == 20260408
    assert len(decoded["strokes"]) == len(strokes)
    assert decoded["strokes"] == strokes
