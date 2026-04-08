from __future__ import annotations

import random

from zpe_ink.benchmarks import measure_dataset
from zpe_ink.fixtures import generate_directional_stroke


def test_measure_dataset_reports_exact_roundtrip() -> None:
    rng = random.Random(20260408)
    samples = [[generate_directional_stroke(rng, segments=8)] for _ in range(4)]

    metrics = measure_dataset(samples, seed=20260408)

    assert metrics["sample_count"] == 4
    assert metrics["stroke_count"] == 4
    assert metrics["point_count"] > 0
    assert metrics["raw_size_bytes"] > metrics["compressed_size_bytes"]
    assert metrics["compression_ratio"] > 1.0
    assert metrics["roundtrip_fidelity"] == "exact"


def test_measure_dataset_handles_empty_input() -> None:
    metrics = measure_dataset([])

    assert metrics["sample_count"] == 0
    assert metrics["stroke_count"] == 0
    assert metrics["point_count"] == 0
    assert metrics["average_points_per_stroke"] == 0.0
    assert metrics["raw_size_bytes"] == 0
    assert metrics["compressed_size_bytes"] == 0
    assert metrics["compression_ratio"] == 0.0
    assert metrics["roundtrip_fidelity"] == "exact"
