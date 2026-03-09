from __future__ import annotations

import hashlib
import math
import statistics
import time
import gc
from typing import Callable

from .codec import canonical_json, decode_zpink, encode_zpink


def compression_ratio(strokes: list[dict[str, list[int]]], encoded: bytes) -> float:
    raw_bytes = sum(len(stroke["x"]) * 2 * 4 for stroke in strokes)
    if len(encoded) == 0:
        raise ValueError("encoded stream is empty")
    return raw_bytes / len(encoded)


def _points(stroke: dict[str, list[int]]) -> list[tuple[int, int]]:
    return list(zip(stroke["x"], stroke["y"]))


def hausdorff_distance(a: list[tuple[int, int]], b: list[tuple[int, int]]) -> float:
    if not a or not b:
        return float("inf")

    def directed(u: list[tuple[int, int]], v: list[tuple[int, int]]) -> float:
        best = 0.0
        for ux, uy in u:
            nearest = min(math.hypot(ux - vx, uy - vy) for vx, vy in v)
            best = max(best, nearest)
        return best

    return max(directed(a, b), directed(b, a))


def corpus_hausdorff(original: list[dict[str, list[int]]], reconstructed: list[dict[str, list[int]]]) -> float:
    if len(original) != len(reconstructed):
        raise ValueError("stroke corpus lengths mismatch")
    distances = [hausdorff_distance(_points(o), _points(r)) for o, r in zip(original, reconstructed)]
    return max(distances)


def pressure_rmse_percent(original: list[dict[str, list[int]]], reconstructed: list[dict[str, list[int]]]) -> float:
    if len(original) != len(reconstructed):
        raise ValueError("stroke corpus lengths mismatch")
    sq_err = []
    for o, r in zip(original, reconstructed):
        if len(o["pressure"]) != len(r["pressure"]):
            raise ValueError("pressure channel length mismatch")
        for op, rp in zip(o["pressure"], r["pressure"]):
            sq_err.append((op - rp) ** 2)
    rmse = math.sqrt(sum(sq_err) / max(1, len(sq_err)))
    return (rmse / 1023.0) * 100.0


def encode_latency_ms(
    strokes: list[dict[str, list[int]]], repeats: int = 30, mode: str = "lossless", warmup: int = 5
) -> dict[str, float]:
    for _ in range(max(0, warmup)):
        encode_zpink(strokes, mode=mode)

    gc_enabled = gc.isenabled()
    if gc_enabled:
        gc.disable()
    timings = []
    try:
        for _ in range(repeats):
            start = time.perf_counter_ns()
            encode_zpink(strokes, mode=mode)
            elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000.0
            timings.append(elapsed_ms / max(1, len(strokes)))
    finally:
        if gc_enabled:
            gc.enable()
    return {
        "median_ms_per_stroke": statistics.median(timings),
        "p95_ms_per_stroke": statistics.quantiles(timings, n=20)[18],
        "min_ms_per_stroke": min(timings),
    }


def determinism_hash(strokes: list[dict[str, list[int]]], seed: int, mode: str = "lossless") -> str:
    encoded = encode_zpink(strokes, seed=seed, mode=mode)
    decoded = decode_zpink(encoded)
    digest = hashlib.sha256(canonical_json(decoded).encode("utf-8")).hexdigest()
    return digest


def throughput_hash(func: Callable[[], bytes]) -> str:
    data = func()
    return hashlib.sha256(data).hexdigest()
