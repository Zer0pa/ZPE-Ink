from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path


INKML_NS = "{http://www.w3.org/2003/InkML}"
NUMBER_RE = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")


def _parse_trace_points(text: str, *, scale: int = 100) -> list[tuple[int, int, int]]:
    points: list[tuple[int, int, int]] = []
    chunks = [chunk.strip() for chunk in text.split(",") if chunk.strip()]
    for chunk in chunks:
        nums = [float(token) for token in NUMBER_RE.findall(chunk)]
        if len(nums) < 2:
            continue
        x = int(round(nums[0] * scale))
        y = int(round(nums[1] * scale))
        p = 512
        if len(nums) >= 3:
            candidate = int(round(nums[2]))
            if 0 <= candidate <= 1023:
                p = candidate
            elif 0.0 <= nums[2] <= 1.0:
                p = int(round(nums[2] * 1023.0))
        points.append((x, y, p))
    return points


def inkml_to_strokes(path: Path, *, scale: int = 100) -> list[dict[str, list[int]]]:
    tree = ET.parse(path)
    root = tree.getroot()

    traces = root.findall(f".//{INKML_NS}trace")
    if not traces:
        traces = root.findall(".//trace")

    strokes: list[dict[str, list[int]]] = []
    for trace in traces:
        if trace.text is None:
            continue
        pts = _parse_trace_points(trace.text, scale=scale)
        if len(pts) < 2:
            continue
        x = [p[0] for p in pts]
        y = [p[1] for p in pts]
        pressure = [p[2] for p in pts]
        strokes.append(
            {
                "x": x,
                "y": y,
                "pressure": pressure,
                "tilt": [0] * len(x),
                "azimuth": [0] * len(x),
            }
        )
    return strokes


def collect_inkml_files(root: Path, limit: int = 200) -> list[Path]:
    files = sorted(root.rglob("*.inkml"))
    return files[:limit]
