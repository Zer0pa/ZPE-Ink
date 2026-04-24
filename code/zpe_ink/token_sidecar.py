from __future__ import annotations

import hashlib
import json
from collections import Counter
from typing import Any

from .codec import decode_zpink
from .primitivetoken import Point, decode_tokens_to_stroke, encode_stroke_to_tokens, points_to_stroke, stroke_to_points

SCHEMA = "zpeink-token-sidecar-v1"


def _json_digest(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _build_sidecar_stroke(stroke: dict[str, list[int]]) -> dict[str, Any]:
    points = stroke_to_points(stroke)
    tokens, _, origin, step_size = encode_stroke_to_tokens(points)
    return {
        "point_count": len(points),
        "origin": {"x": origin.x, "y": origin.y},
        "step_size": step_size,
        "tokens": tokens,
        "pressure": stroke["pressure"],
        "tilt": stroke["tilt"],
        "azimuth": stroke["azimuth"],
    }


def _token_distribution(strokes: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for stroke in strokes:
        counts.update(str(token) for token in stroke["tokens"] if token >= 0)
    return {token: counts.get(token, 0) for token in map(str, range(8))}


def build_token_sidecar(
    strokes: list[dict[str, list[int]]],
    *,
    source_format: str,
    source_payload: bytes | None = None,
    source_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    sidecar_strokes = [_build_sidecar_stroke(stroke) for stroke in strokes]
    payload = {
        "schema": SCHEMA,
        "candidate_status": "CANDIDATE_ONLY",
        "runtime_authority": ".zpink remains sovereign; token sidecar is bounded follow-on only",
        "source_format": source_format,
        "source_sha256": hashlib.sha256(source_payload).hexdigest() if source_payload is not None else None,
        "source_metadata": source_metadata or {},
        "stroke_count": len(sidecar_strokes),
        "token_count": sum(len(stroke["tokens"]) for stroke in sidecar_strokes),
        "token_distribution": _token_distribution(sidecar_strokes),
        "strokes": sidecar_strokes,
    }
    payload["sidecar_sha256"] = _json_digest(payload)
    return payload


def build_token_sidecar_from_zpink(payload: bytes) -> dict[str, Any]:
    decoded = decode_zpink(payload)
    return build_token_sidecar(
        decoded["strokes"],
        source_format=".zpink",
        source_payload=payload,
        source_metadata={
            "mode": decoded["mode"],
            "seed": decoded["seed"],
            "version": decoded["version"],
        },
    )


def reconstruct_token_sidecar(sidecar: dict[str, Any]) -> list[dict[str, list[int]]]:
    if sidecar.get("schema") != SCHEMA:
        raise ValueError(f"unsupported token sidecar schema: {sidecar.get('schema')}")

    reconstructed: list[dict[str, list[int]]] = []
    for stroke in sidecar["strokes"]:
        pressure = [int(value) for value in stroke["pressure"]]
        tilt = [int(value) for value in stroke["tilt"]]
        azimuth = [int(value) for value in stroke["azimuth"]]
        side_channels = list(zip(pressure, tilt, azimuth))
        origin_xy = stroke["origin"]
        origin = Point(
            x=int(origin_xy["x"]),
            y=int(origin_xy["y"]),
            pressure=pressure[0],
            tilt=tilt[0],
            azimuth=azimuth[0],
        )
        points = decode_tokens_to_stroke(
            [int(token) for token in stroke["tokens"]],
            side_channels,
            origin,
            int(stroke["step_size"]),
        )
        reconstructed.append(points_to_stroke(points))
    return reconstructed


__all__ = [
    "SCHEMA",
    "build_token_sidecar",
    "build_token_sidecar_from_zpink",
    "reconstruct_token_sidecar",
]
