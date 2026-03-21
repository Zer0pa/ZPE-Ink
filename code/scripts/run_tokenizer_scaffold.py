from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.shared import write_json
from zpe_ink.primitivetoken import Point
from zpe_ink.tokenizer import InkTokenizer

DISK_FLOOR_BYTES = 5 * 1024**3
QUICKDRAW_URL = "https://storage.googleapis.com/quickdraw_dataset/full/raw/cat.ndjson"
CANONICAL_COMET_WORKSPACE = "zer0pa"
CANONICAL_COMET_PROJECT = "zpe-ink"


def _timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _check_disk() -> int:
    free_bytes = shutil.disk_usage("/").free
    if free_bytes < DISK_FLOOR_BYTES:
        raise RuntimeError(f"disk safety floor breached: {free_bytes} bytes free")
    return free_bytes


def _quickdraw_stroke_to_points(stroke: list[list[float]]) -> list[Point]:
    if len(stroke) < 2:
        raise ValueError("quickdraw stroke must contain x and y channels")
    x_vals = stroke[0]
    y_vals = stroke[1]
    return [Point(int(round(x_val)), int(round(y_val)), 512, 0, 0) for x_val, y_val in zip(x_vals, y_vals)]


def _load_quickdraw_strokes_from_url(url: str, limit: int) -> tuple[list[list[Point]], int]:
    strokes: list[list[Point]] = []
    sample_count = 0
    with urllib.request.urlopen(url) as handle:
        for line in handle:
            payload = json.loads(line.decode("utf-8"))
            sample_count += 1
            for stroke in payload.get("drawing", []):
                strokes.append(_quickdraw_stroke_to_points(stroke))
            if sample_count >= limit:
                break
    return strokes, sample_count


def _comet_status(experiment_name: str, params: dict[str, Any]) -> dict[str, Any]:
    api_key = os.environ.get("COMET_API_KEY")
    if not api_key:
        return {
            "workspace": CANONICAL_COMET_WORKSPACE,
            "project": CANONICAL_COMET_PROJECT,
            "experiment_name": experiment_name,
            "logged": False,
            "reason": "COMET_API_KEY missing",
        }
    if importlib.util.find_spec("comet_ml") is None:
        return {
            "workspace": CANONICAL_COMET_WORKSPACE,
            "project": CANONICAL_COMET_PROJECT,
            "experiment_name": experiment_name,
            "logged": False,
            "reason": "comet_ml not installed",
        }
    from comet_ml import Experiment

    experiment = Experiment(
        api_key=api_key,
        workspace=CANONICAL_COMET_WORKSPACE,
        project_name=CANONICAL_COMET_PROJECT,
        log_code=False,
        auto_output_logging=False,
    )
    experiment.set_name(experiment_name)
    experiment.add_tag("phase04")
    experiment.add_tag("tokenizer-scaffold")
    for key, value in params.items():
        experiment.log_parameter(key, value)
    result = {
        "workspace": CANONICAL_COMET_WORKSPACE,
        "project": CANONICAL_COMET_PROJECT,
        "experiment_name": experiment_name,
        "logged": True,
        "url": experiment.url,
    }
    experiment.end()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default=str(REPO_ROOT / "proofs" / "reruns" / "tokenizer_scaffold" / "tokenizer_corpus_proof.json"),
    )
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    free_bytes_before = _check_disk()
    tokenizer = InkTokenizer()

    strokes, sample_count = _load_quickdraw_strokes_from_url(QUICKDRAW_URL, args.limit)
    encoded_once = tokenizer.encode_corpus(strokes)
    encoded_twice = tokenizer.encode_corpus(strokes)

    deterministic = encoded_once == encoded_twice
    distribution = tokenizer.token_distribution(encoded_once)
    telemetry = {
        "comet": _comet_status(
            "phase04-tokenizer-scaffold",
            {
                "vocab_size": tokenizer.VOCAB_SIZE,
                "corpus_size": sample_count,
                "deterministic": deterministic,
            },
        ),
        "opik": {
            "present": False,
            "reason": "no canonical Opik surface found in this workstream",
        },
    }

    payload = {
        "schema_version": 1,
        "generated_at": _timestamp(),
        "corpus": "quickdraw-cat-100",
        "source_url": QUICKDRAW_URL,
        "sample_count": sample_count,
        "strokes_encoded": len(strokes),
        "vocab_size": tokenizer.VOCAB_SIZE,
        "deterministic": deterministic,
        "token_distribution": distribution,
        "disk_free_gib_before": round(free_bytes_before / (1024**3), 3),
        "telemetry": telemetry,
    }
    write_json(output_path, payload)
    print("TOKENIZER_SCAFFOLD_COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
