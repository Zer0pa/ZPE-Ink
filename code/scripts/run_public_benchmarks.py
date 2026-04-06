from __future__ import annotations

import argparse
import json
import tarfile
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT))

from zpe_ink.public_benchmarking import (
    evaluate_samples,
    fetch_url,
    parse_digilets_raw,
    parse_inkml_corpus,
    parse_quickdraw_ndjson,
    probe_url,
)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", required=True)
    args = parser.parse_args()

    artifact_root = Path(args.artifact_root)
    artifact_root.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="zpe-ink-public-benchmarks-") as temp_dir:
        temp_root = Path(temp_dir)

        math_archive = fetch_url(
            "https://storage.googleapis.com/mathwriting_data/mathwriting-2024-excerpt.tgz",
            temp_root / "mathwriting.tgz",
        )
        math_extract = temp_root / "mathwriting"
        with tarfile.open(math_archive, "r:gz") as handle:
            handle.extractall(math_extract)
        math_files, math_samples, math_parse_failures = parse_inkml_corpus(math_extract, limit=70)
        math_metrics = evaluate_samples("mathwriting_excerpt", math_samples)

        crohme_archive = fetch_url(
            "https://oldweb.isical.ac.in/~crohme/ICFHR_package.zip",
            temp_root / "crohme.zip",
        )
        crohme_extract = temp_root / "crohme"
        with zipfile.ZipFile(crohme_archive) as handle:
            handle.extractall(crohme_extract)
        crohme_files, crohme_samples, crohme_parse_failures = parse_inkml_corpus(crohme_extract, limit=90)
        crohme_metrics = evaluate_samples("crohme_icfhr_package", crohme_samples)

        quickdraw_file = fetch_url(
            "https://storage.googleapis.com/quickdraw_dataset/full/simplified/cat.ndjson",
            temp_root / "quickdraw-cat.ndjson",
        )
        quickdraw_samples = parse_quickdraw_ndjson(quickdraw_file, limit=256)
        quickdraw_metrics = evaluate_samples("quickdraw_cat_simplified", quickdraw_samples)

        digilets_dir = temp_root / "DigiLeTs"
        __import__("subprocess").run(
            ["git", "clone", "--depth", "1", "https://github.com/CognitiveModeling/DigiLeTs.git", str(digilets_dir)],
            check=True,
            capture_output=True,
            text=True,
        )
        digilets_samples = parse_digilets_raw(digilets_dir / "data" / "raw" / "complete", limit=180)
        digilets_metrics = evaluate_samples("digilets_raw_complete", digilets_samples)

        iam_probe = probe_url("https://fki.tic.heia-fr.ch/databases/iam-on-line-handwriting-database")
        unipen_probe = probe_url("https://unipen.nici.ru.nl")

        dataset_matrix = {
            "generated_on": "2026-04-06",
            "datasets": [
                {
                    "name": "MathWriting",
                    "status": "benchmarked",
                    "source_url": "https://storage.googleapis.com/mathwriting_data/mathwriting-2024-excerpt.tgz",
                    "inkml_files": len(math_files),
                    "parse_failures": math_parse_failures,
                    "metrics": math_metrics,
                },
                {
                    "name": "CROHME",
                    "status": "benchmarked_fallback",
                    "source_url": "https://oldweb.isical.ac.in/~crohme/ICFHR_package.zip",
                    "inkml_files": len(crohme_files),
                    "parse_failures": crohme_parse_failures,
                    "metrics": crohme_metrics,
                    "note": "The revised 2019 landing path was not used; the public ICFHR package remained available.",
                },
                {
                    "name": "QuickDraw",
                    "status": "benchmarked",
                    "source_url": "https://storage.googleapis.com/quickdraw_dataset/full/simplified/cat.ndjson",
                    "category": "cat",
                    "metrics": quickdraw_metrics,
                    "note": "Simplified NDJSON category sample with synthesized pressure/tilt/azimuth channels.",
                },
                {
                    "name": "DigiLeTs",
                    "status": "benchmarked",
                    "source_url": "https://github.com/CognitiveModeling/DigiLeTs",
                    "metrics": digilets_metrics,
                    "note": "Parsed from raw complete participant files with pen-down stroke segmentation.",
                },
                {
                    "name": "IAM On-Line",
                    "status": "skipped_access",
                    "source_url": "https://fki.tic.heia-fr.ch/databases/iam-on-line-handwriting-database",
                    "probe": iam_probe,
                    "note": "Landing page reachable, but direct agent-only dataset acquisition remains registration-gated.",
                },
                {
                    "name": "UNIPEN",
                    "status": "skipped_access",
                    "source_url": "https://unipen.nici.ru.nl",
                    "probe": unipen_probe,
                    "note": "Direct host probe failed in-lane.",
                },
            ],
        }
        write_json(artifact_root / "dataset_matrix.json", dataset_matrix)

        summary_lines = [
            "# Public Benchmark Summary",
            "",
            "| Dataset | Status | Samples | Compression Ratio | Notes |",
            "|---|---|---:|---:|---|",
            f"| MathWriting | benchmarked | {math_metrics['sample_count']} | {math_metrics['compression_ratio']:.4f}x | excerpt InkML |",
            f"| CROHME | benchmarked_fallback | {crohme_metrics['sample_count']} | {crohme_metrics['compression_ratio']:.4f}x | ICFHR package |",
            f"| QuickDraw (cat) | benchmarked | {quickdraw_metrics['sample_count']} | {quickdraw_metrics['compression_ratio']:.4f}x | simplified NDJSON |",
            f"| DigiLeTs | benchmarked | {digilets_metrics['sample_count']} | {digilets_metrics['compression_ratio']:.4f}x | raw complete set |",
            "| IAM On-Line | skipped_access | 0 | n/a | registration-gated |",
            "| UNIPEN | skipped_access | 0 | n/a | host unavailable |",
            "",
            "All benchmarked datasets ran `encode -> decode -> verify` using the repo-local lossless codec path.",
        ]
        (artifact_root / "README.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
