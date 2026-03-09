from __future__ import annotations

import math
import random
from typing import Any

DIRECTIONS = [
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
]


def _bounded(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def generate_directional_stroke(rng: random.Random, segments: int) -> dict[str, list[int]]:
    x = [rng.randint(0, 2000)]
    y = [rng.randint(0, 2000)]
    pressure = [rng.randint(300, 700)]
    tilt = [rng.randint(-200, 200)]
    azimuth = [rng.randint(0, 3599)]

    for segment in range(segments):
        dx, dy = DIRECTIONS[rng.randrange(len(DIRECTIONS))]
        run = rng.randint(6, 38)
        segment_pressure = _bounded(pressure[-1] + rng.randint(-8, 8), 0, 1023)
        segment_tilt = _bounded(tilt[-1] + rng.randint(-4, 4), -900, 900)
        segment_azimuth = (azimuth[-1] + rng.randint(-24, 24)) % 3600
        for step in range(run):
            x.append(x[-1] + dx)
            y.append(y[-1] + dy)
            # Piecewise-constant channel updates preserve realism while enabling channel run-length compression.
            if step % 12 == 0:
                segment_pressure = _bounded(segment_pressure + rng.randint(-2, 2), 0, 1023)
                segment_tilt = _bounded(segment_tilt + rng.randint(-1, 1), -900, 900)
                segment_azimuth = (segment_azimuth + rng.randint(-3, 3)) % 3600
            pressure.append(segment_pressure)
            tilt.append(segment_tilt)
            azimuth.append(segment_azimuth)

    return {
        "x": x,
        "y": y,
        "pressure": pressure,
        "tilt": tilt,
        "azimuth": azimuth,
    }


def generate_high_velocity_stroke(rng: random.Random, points: int) -> dict[str, list[int]]:
    x = [0]
    y = [0]
    pressure = [512]
    tilt = [0]
    azimuth = [0]

    for i in range(1, points):
        dx = rng.randint(-9, 9)
        dy = rng.randint(-9, 9)
        if i % 16 == 0:
            dx *= 3
            dy *= 3
        x.append(x[-1] + dx)
        y.append(y[-1] + dy)
        pressure.append(_bounded(pressure[-1] + rng.randint(-40, 40), 0, 1023))
        tilt.append(_bounded(tilt[-1] + rng.randint(-20, 20), -900, 900))
        azimuth.append((azimuth[-1] + rng.randint(-45, 45)) % 3600)

    return {
        "x": x,
        "y": y,
        "pressure": pressure,
        "tilt": tilt,
        "azimuth": azimuth,
    }


def generate_iam_proxy(seed: int = 20260220) -> list[dict[str, list[int]]]:
    rng = random.Random(seed)
    return [generate_directional_stroke(rng, segments=rng.randint(8, 18)) for _ in range(64)]


def generate_unipen_proxy(seed: int = 20260221) -> list[dict[str, list[int]]]:
    rng = random.Random(seed)
    out: list[dict[str, list[int]]] = []
    for _ in range(64):
        stroke = generate_directional_stroke(rng, segments=rng.randint(10, 22))
        # Cross-script proxy augmentation: stronger diagonal/loop pressure transitions.
        for idx in range(0, len(stroke["pressure"]), 9):
            stroke["pressure"][idx] = _bounded(
                stroke["pressure"][idx] + int(35 * math.sin(idx / 7.0)),
                0,
                1023,
            )
        out.append(stroke)
    return out


def generate_synthetic_lossless(seed: int = 20260220) -> list[dict[str, list[int]]]:
    rng = random.Random(seed)
    return [generate_directional_stroke(rng, segments=rng.randint(6, 14)) for _ in range(48)]


def generate_adversarial_spike_set(seed: int = 20260223) -> list[dict[str, list[int]]]:
    rng = random.Random(seed)
    out = []
    for _ in range(24):
        stroke = generate_high_velocity_stroke(rng, points=rng.randint(100, 260))
        for idx in range(0, len(stroke["pressure"]), 11):
            stroke["pressure"][idx] = 1023 if (idx // 11) % 2 == 0 else 0
            stroke["tilt"][idx] = 900 if (idx // 11) % 3 == 0 else -900
            stroke["azimuth"][idx] = 3599 if (idx // 11) % 2 == 0 else 0
        out.append(stroke)
    return out


def generate_long_page(seed: int = 20260224) -> list[dict[str, list[int]]]:
    rng = random.Random(seed)
    return [generate_directional_stroke(rng, segments=rng.randint(14, 26)) for _ in range(2400)]


def dataset_manifest() -> dict[str, Any]:
    return {
        "synthetic_lossless": {"seed": 20260220, "count": 48},
        "iam_proxy": {"seed": 20260220, "count": 64, "source": "IAM On-Line proxy"},
        "unipen_proxy": {"seed": 20260221, "count": 64, "source": "UNIPEN proxy"},
        "adversarial_spike": {"seed": 20260223, "count": 24},
        "long_page": {"seed": 20260224, "count": 2400},
    }
