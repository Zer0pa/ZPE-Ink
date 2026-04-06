from __future__ import annotations

import argparse
import json
import statistics
import tarfile
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT))

from zpe_ink.codec import encode_zpink
from zpe_ink.public_benchmarking import fetch_url, parse_inkml_corpus


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def ratio_rows(samples: list[list[dict[str, list[int]]]], *, optimized: bool) -> list[dict[str, float | int]]:
    rows: list[dict[str, float | int]] = []
    for index, sample in enumerate(samples):
        raw = sum(len(stroke["x"]) * 2 * 4 for stroke in sample)
        if optimized:
            encoded = encode_zpink(sample, mode="lossless")
        else:
            encoded = encode_zpink(sample, mode="lossless", include_tilt=True, include_azimuth=True)
        strokes = len(sample)
        points = sum(len(stroke["x"]) for stroke in sample)
        rows.append(
            {
                "sample_index": index,
                "compression_ratio": raw / len(encoded),
                "encoded_bytes": len(encoded),
                "raw_bytes": raw,
                "stroke_count": strokes,
                "point_count": points,
                "points_per_stroke": points / strokes if strokes else 0.0,
            }
        )
    return rows


def summarize(rows: list[dict[str, float | int]]) -> dict[str, float | int]:
    ratios = [float(row["compression_ratio"]) for row in rows]
    strokes = [int(row["stroke_count"]) for row in rows]
    points_per_stroke = [float(row["points_per_stroke"]) for row in rows]
    ordered = sorted(rows, key=lambda row: float(row["compression_ratio"]))
    return {
        "sample_count": len(rows),
        "mean_ratio": statistics.mean(ratios),
        "median_ratio": statistics.median(ratios),
        "min_ratio": min(ratios),
        "max_ratio": max(ratios),
        "mean_stroke_count": statistics.mean(strokes),
        "mean_points_per_stroke": statistics.mean(points_per_stroke),
        "worst_samples": ordered[:10],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", required=True)
    args = parser.parse_args()

    artifact_root = Path(args.artifact_root)
    artifact_root.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="zpe-ink-mathwriting-analysis-") as temp_dir:
        temp_root = Path(temp_dir)

        math_archive = fetch_url(
            "https://storage.googleapis.com/mathwriting_data/mathwriting-2024-excerpt.tgz",
            temp_root / "mathwriting.tgz",
        )
        math_extract = temp_root / "mathwriting"
        with tarfile.open(math_archive, "r:gz") as handle:
            handle.extractall(math_extract)
        _, math_samples, _ = parse_inkml_corpus(math_extract, limit=70)

        crohme_archive = fetch_url(
            "https://oldweb.isical.ac.in/~crohme/ICFHR_package.zip",
            temp_root / "crohme.zip",
        )
        crohme_extract = temp_root / "crohme"
        with zipfile.ZipFile(crohme_archive) as handle:
            handle.extractall(crohme_extract)
        _, crohme_samples, _ = parse_inkml_corpus(crohme_extract, limit=90)

        math_before = ratio_rows(math_samples, optimized=False)
        math_after = ratio_rows(math_samples, optimized=True)
        crohme_before = ratio_rows(crohme_samples, optimized=False)
        crohme_after = ratio_rows(crohme_samples, optimized=True)

        payload = {
            "generated_on": "2026-04-06",
            "codec_change": "auto-suppress zero tilt/azimuth channels unless explicitly requested",
            "mathwriting": {
                "before": summarize(math_before),
                "after": summarize(math_after),
                "mean_ratio_delta": statistics.mean(float(row["compression_ratio"]) for row in math_after)
                - statistics.mean(float(row["compression_ratio"]) for row in math_before),
            },
            "crohme": {
                "before": summarize(crohme_before),
                "after": summarize(crohme_after),
                "mean_ratio_delta": statistics.mean(float(row["compression_ratio"]) for row in crohme_after)
                - statistics.mean(float(row["compression_ratio"]) for row in crohme_before),
            },
            "finding": {
                "primary_driver": "short multi-stroke samples pay disproportionate per-stroke optional-channel overhead",
                "evidence": "The lowest-ratio MathWriting samples have low points-per-stroke and improve when zero tilt/azimuth streams are omitted.",
                "implemented_fix": "encode_zpink now auto-disables zero-valued tilt and azimuth channels while preserving lossless reconstruction.",
            },
        }
        write_json(artifact_root / "comparison.json", payload)

        readme_lines = [
            "# MathWriting Gap Analysis",
            "",
            "| Corpus | Before | After | Delta |",
            "|---|---:|---:|---:|",
            f"| MathWriting mean ratio | {payload['mathwriting']['before']['mean_ratio']:.4f}x | {payload['mathwriting']['after']['mean_ratio']:.4f}x | {payload['mathwriting']['mean_ratio_delta']:+.4f}x |",
            f"| CROHME mean ratio | {payload['crohme']['before']['mean_ratio']:.4f}x | {payload['crohme']['after']['mean_ratio']:.4f}x | {payload['crohme']['mean_ratio_delta']:+.4f}x |",
            "",
            "Finding: the hardest MathWriting cases are short, multi-stroke samples where zero tilt/azimuth streams add fixed overhead.",
            "Action: auto-suppress zero optional channels by default, while raising on explicit lossy suppression of non-zero data.",
        ]
        (artifact_root / "README.md").write_text("\n".join(readme_lines) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
