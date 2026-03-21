from __future__ import annotations

import shlex
from pathlib import Path
from typing import Any


def _build_stroke(points: list[tuple[int, int]], pressure: int) -> dict[str, list[int]] | None:
    if len(points) < 2:
        return None
    x_vals = [x for x, _ in points]
    y_vals = [y for _, y in points]
    point_count = len(points)
    return {
        "x": x_vals,
        "y": y_vals,
        "pressure": [pressure] * point_count,
        "tilt": [0] * point_count,
        "azimuth": [0] * point_count,
    }


def parse_unipen_like_file(
    path: Path,
    *,
    scale: int = 1,
    pressure: int = 512,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    samples: list[dict[str, Any]] = []
    current_label: str | None = None
    current_sample_id: str | None = None
    current_strokes: list[dict[str, list[int]]] = []
    current_points: list[tuple[int, int]] | None = None

    def finalize_stroke() -> None:
        nonlocal current_points
        if current_points is None:
            return
        stroke = _build_stroke(current_points, pressure)
        if stroke is not None:
            current_strokes.append(stroke)
        current_points = None

    def finalize_sample() -> None:
        nonlocal current_label, current_sample_id, current_strokes, current_points
        finalize_stroke()
        if current_strokes:
            sample_key = current_sample_id or str(len(samples))
            sample_label = current_label or "?"
            samples.append(
                {
                    "sample_id": f"{path.name}:{sample_key}",
                    "label": sample_label,
                    "strokes": current_strokes,
                }
            )
        current_label = None
        current_sample_id = None
        current_strokes = []
        current_points = None

    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith(".SEGMENT"):
            finalize_sample()
            parts = shlex.split(line)
            current_sample_id = parts[2] if len(parts) >= 3 else str(len(samples))
            current_label = parts[-1] if parts else "?"
            continue

        if line == ".PEN_DOWN":
            finalize_stroke()
            current_points = []
            continue

        if line == ".PEN_UP":
            finalize_stroke()
            continue

        if line.startswith("."):
            continue

        if current_points is None:
            continue

        fields = line.split()
        if len(fields) < 2:
            continue

        try:
            x_val = int(round(float(fields[0]) * scale))
            y_val = int(round(float(fields[1]) * scale))
        except ValueError:
            continue

        current_points.append((x_val, y_val))

    finalize_sample()
    if limit is not None:
        return samples[:limit]
    return samples


def load_uji_pen_characters(root: Path, *, limit: int = 160) -> list[list[dict[str, list[int]]]]:
    samples: list[list[dict[str, list[int]]]] = []
    for path in sorted(root.glob("UJIpenchars-w*")):
        for sample in parse_unipen_like_file(path):
            samples.append(sample["strokes"])
            if len(samples) >= limit:
                return samples
    return samples
