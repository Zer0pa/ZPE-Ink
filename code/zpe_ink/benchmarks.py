from __future__ import annotations

from typing import Any

from zpe_ink.codec import decode_zpink, encode_zpink
from zpe_ink.phase2_authority import raw_float32_xy_payload


Sample = list[dict[str, list[int]]]


def measure_dataset(samples: list[Sample], *, mode: str = "lossless", seed: int = 20260408) -> dict[str, Any]:
    total_raw_size = 0
    total_compressed_size = 0
    stroke_count = 0
    point_count = 0
    exact_roundtrip = True
    sample_count = 0

    for sample in samples:
        if not sample:
            continue

        encoded = encode_zpink(sample, mode=mode, seed=seed)
        decoded = decode_zpink(encoded)["strokes"]

        total_raw_size += len(raw_float32_xy_payload(sample))
        total_compressed_size += len(encoded)
        stroke_count += len(sample)
        point_count += sum(len(stroke["x"]) for stroke in sample)
        sample_count += 1
        exact_roundtrip = exact_roundtrip and decoded == sample

    average_points_per_stroke = (point_count / stroke_count) if stroke_count else 0.0
    compression_ratio = (total_raw_size / total_compressed_size) if total_compressed_size else 0.0

    return {
        "sample_count": sample_count,
        "stroke_count": stroke_count,
        "point_count": point_count,
        "average_points_per_stroke": round(average_points_per_stroke, 2),
        "raw_size_bytes": total_raw_size,
        "compressed_size_bytes": total_compressed_size,
        "compression_ratio": round(compression_ratio, 4),
        "roundtrip_fidelity": "exact" if exact_roundtrip else "mismatch",
        "mode": mode,
        "seed": seed,
    }
