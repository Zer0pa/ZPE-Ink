from __future__ import annotations

import json
import math
import statistics
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from .codec import decode_zpink, encode_zpink
from .inkml import collect_inkml_files, inkml_to_strokes


def fetch_url(url: str, destination: Path, *, timeout: int = 60) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=timeout) as response, destination.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)
    return destination


def probe_url(url: str, *, timeout: int = 30) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            head = response.read(2048).decode("utf-8", errors="ignore")
            return {
                "url": url,
                "status": "reachable",
                "http_status": getattr(response, "status", 200),
                "snippet": head[:512],
            }
    except urllib.error.URLError as exc:
        return {
            "url": url,
            "status": "failed",
            "error": str(exc),
        }


def parse_inkml_corpus(root: Path, *, limit: int) -> tuple[list[Path], list[list[dict[str, list[int]]]], int]:
    files = collect_inkml_files(root, limit=limit)
    samples: list[list[dict[str, list[int]]]] = []
    parse_failures = 0
    for path in files:
        try:
            strokes = inkml_to_strokes(path)
        except Exception:
            parse_failures += 1
            continue
        if strokes:
            samples.append(strokes)
    return files, samples, parse_failures


def parse_quickdraw_ndjson(path: Path, *, limit: int) -> list[list[dict[str, list[int]]]]:
    samples: list[list[dict[str, list[int]]]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            if len(samples) >= limit:
                break
            line = raw_line.strip()
            if not line:
                continue
            payload = json.loads(line)
            drawing = payload.get("drawing", [])
            sample: list[dict[str, list[int]]] = []
            for stroke in drawing:
                if len(stroke) < 2:
                    continue
                x_vals = [int(round(value)) for value in stroke[0]]
                y_vals = [int(round(value)) for value in stroke[1]]
                point_count = min(len(x_vals), len(y_vals))
                if point_count < 2:
                    continue
                x_vals = x_vals[:point_count]
                y_vals = y_vals[:point_count]
                sample.append(
                    {
                        "x": x_vals,
                        "y": y_vals,
                        "pressure": [512] * point_count,
                        "tilt": [0] * point_count,
                        "azimuth": [0] * point_count,
                    }
                )
            if sample:
                samples.append(sample)
    return samples


def parse_digilets_raw(root: Path, *, limit: int) -> list[list[dict[str, list[int]]]]:
    samples: list[list[dict[str, list[int]]]] = []
    for path in sorted(root.glob("*")):
        if len(samples) >= limit:
            break
        if not path.is_file() or path.name.endswith("_info"):
            continue
        lines = [line.strip() for line in path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]
        for index in range(0, len(lines), 2):
            if len(samples) >= limit:
                break
            point_line = lines[index]
            fields = point_line.split()
            if len(fields) < 10 or len(fields) % 5 != 0:
                continue

            strokes: list[dict[str, list[int]]] = []
            current_x: list[int] = []
            current_y: list[int] = []
            current_pressure: list[int] = []

            def finalize_stroke() -> None:
                if len(current_x) < 2:
                    return
                point_count = len(current_x)
                strokes.append(
                    {
                        "x": current_x.copy(),
                        "y": current_y.copy(),
                        "pressure": current_pressure.copy(),
                        "tilt": [0] * point_count,
                        "azimuth": [0] * point_count,
                    }
                )

            for offset in range(0, len(fields), 5):
                try:
                    x_val = int(round(float(fields[offset]) * 2000.0))
                    y_val = int(round(float(fields[offset + 1]) * 2000.0))
                    pressure = int(round(float(fields[offset + 2]) * 1023.0))
                    pen_down = int(round(float(fields[offset + 3])))
                except ValueError:
                    current_x = []
                    current_y = []
                    current_pressure = []
                    strokes = []
                    break

                pressure = max(0, min(1023, pressure))
                if pen_down == 1 and current_x:
                    finalize_stroke()
                    current_x = []
                    current_y = []
                    current_pressure = []

                current_x.append(x_val)
                current_y.append(y_val)
                current_pressure.append(pressure)

            if current_x:
                finalize_stroke()
            if strokes:
                samples.append(strokes)
    return samples


def evaluate_samples(name: str, samples: list[list[dict[str, list[int]]]]) -> dict[str, Any]:
    total_raw = 0
    total_encoded = 0
    max_hausdorff = 0.0
    sq_err = 0.0
    sq_count = 0
    latencies: list[float] = []
    sample_count = 0
    stroke_count = 0
    point_count = 0
    roundtrip_pass = True

    for sample in samples:
        if not sample:
            continue

        start = time.perf_counter_ns()
        encoded = encode_zpink(sample, mode="lossless")
        elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000.0
        decoded = decode_zpink(encoded)["strokes"]
        roundtrip_pass = roundtrip_pass and decoded == sample

        total_raw += sum(len(stroke["x"]) * 2 * 4 for stroke in sample)
        total_encoded += len(encoded)
        max_hausdorff = max(max_hausdorff, corpus_hausdorff(sample, decoded))

        for src, rec in zip(sample, decoded):
            for source_pressure, replay_pressure in zip(src["pressure"], rec["pressure"]):
                sq_err += float((source_pressure - replay_pressure) ** 2)
                sq_count += 1

        latencies.append(elapsed_ms / max(1, len(sample)))
        sample_count += 1
        stroke_count += len(sample)
        point_count += sum(len(stroke["x"]) for stroke in sample)

    compression = (total_raw / total_encoded) if total_encoded > 0 else 0.0
    rmse = math.sqrt(sq_err / sq_count) if sq_count else 0.0
    return {
        "name": name,
        "sample_count": sample_count,
        "stroke_count": stroke_count,
        "point_count": point_count,
        "compression_ratio": compression,
        "max_hausdorff_px": max_hausdorff,
        "pressure_rmse_percent": (rmse / 1023.0) * 100.0,
        "median_ms_per_stroke": statistics.median(latencies) if latencies else None,
        "roundtrip_pass": roundtrip_pass,
    }


def corpus_hausdorff(original: list[dict[str, list[int]]], reconstructed: list[dict[str, list[int]]]) -> float:
    if len(original) != len(reconstructed):
        raise ValueError("stroke corpus length mismatch")

    def points(stroke: dict[str, list[int]]) -> list[tuple[int, int]]:
        coords = list(zip(stroke["x"], stroke["y"]))
        if len(coords) > 160:
            step = max(1, len(coords) // 160)
            coords = coords[::step]
        return coords

    def directed(source: list[tuple[int, int]], target: list[tuple[int, int]]) -> float:
        best = 0.0
        for sx, sy in source:
            nearest = min(math.hypot(sx - tx, sy - ty) for tx, ty in target)
            best = max(best, nearest)
        return best

    max_distance = 0.0
    for source, replay in zip(original, reconstructed):
        src_points = points(source)
        replay_points = points(replay)
        if not src_points or not replay_points:
            continue
        max_distance = max(max_distance, directed(src_points, replay_points), directed(replay_points, src_points))
    return max_distance
