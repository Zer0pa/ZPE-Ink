from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.shared import append_command_log, write_json
from zpe_ink.codec import encode_zpink
from zpe_ink.fixtures import generate_iam_proxy, generate_synthetic_lossless, generate_unipen_proxy
from zpe_ink.metrics import corpus_hausdorff
from zpe_ink.phase2_authority import raw_float32_xy_payload
from zpe_ink.primitivetoken import decode_primitive_strokes, encode_primitive_strokes

CALLIAR_URL = "https://raw.githubusercontent.com/ARBML/Calliar/main/calliar_dataset/dataset.npz"
DISK_FLOOR_BYTES = 5 * 1024**3
CANONICAL_COMET_WORKSPACE = "zer0pa"
CANONICAL_COMET_PROJECT = "zpe-ink"


def _timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _check_disk() -> int:
    free_bytes = shutil.disk_usage("/").free
    if free_bytes < DISK_FLOOR_BYTES:
        raise RuntimeError(f"disk safety floor breached: {free_bytes} bytes free")
    return free_bytes


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _ratio(raw_size: int, encoded_size: int) -> float:
    if encoded_size <= 0:
        raise ValueError("encoded size must be positive")
    return raw_size / encoded_size


def _run_binary_command(command: list[str], data: bytes, log_path: Path, label: str) -> dict[str, Any]:
    proc = subprocess.run(command, input=data, capture_output=True)
    append_command_log(
        log_path,
        label,
        " ".join(command),
        proc.returncode,
        f"stdout_bytes={len(proc.stdout)}",
        proc.stderr.decode("utf-8", errors="ignore"),
    )
    return {
        "returncode": proc.returncode,
        "stdout_bytes": len(proc.stdout),
        "stderr": proc.stderr.decode("utf-8", errors="ignore"),
    }


def _detect_binary(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        raise RuntimeError(f"required comparator binary not found: {name}")
    return path


def _sample_measurement(
    name: str,
    samples: list[list[dict[str, list[int]]]],
    *,
    brotli_command: list[str],
    zstd_command: list[str],
    log_path: Path,
) -> dict[str, Any]:
    totals = {
        "raw_float32_xy": 0,
        "sovereign": 0,
        "primitive_raw": 0,
        "primitive_zstd": 0,
        "brotli": 0,
    }
    hausdorff_values: list[float] = []
    sample_count = 0
    stroke_count = 0
    point_count = 0

    for index, sample in enumerate(samples):
        raw_payload = raw_float32_xy_payload(sample)
        sovereign = encode_zpink(sample, mode="lossless")
        primitive = encode_primitive_strokes(sample)
        primitive_zstd = _run_binary_command(zstd_command, primitive, log_path, f"{name}_primitive_zstd_{index:03d}")
        brotli = _run_binary_command(brotli_command, raw_payload, log_path, f"{name}_brotli_{index:03d}")
        if primitive_zstd["returncode"] != 0:
            raise RuntimeError(f"zstd failed for {name} sample {index}")
        if brotli["returncode"] != 0:
            raise RuntimeError(f"brotli failed for {name} sample {index}")

        reconstructed = decode_primitive_strokes(primitive)
        totals["raw_float32_xy"] += len(raw_payload)
        totals["sovereign"] += len(sovereign)
        totals["primitive_raw"] += len(primitive)
        totals["primitive_zstd"] += primitive_zstd["stdout_bytes"]
        totals["brotli"] += brotli["stdout_bytes"]
        hausdorff_values.append(corpus_hausdorff(sample, reconstructed))
        sample_count += 1
        stroke_count += len(sample)
        point_count += sum(len(stroke["x"]) for stroke in sample)

    return {
        "name": name,
        "sample_count": sample_count,
        "stroke_count": stroke_count,
        "point_count": point_count,
        "sizes_bytes": totals,
        "ratios": {
            "raw_float32_xy": 1.0,
            "sovereign": _ratio(totals["raw_float32_xy"], totals["sovereign"]),
            "primitive_raw": _ratio(totals["raw_float32_xy"], totals["primitive_raw"]),
            "primitive_zstd": _ratio(totals["raw_float32_xy"], totals["primitive_zstd"]),
            "brotli": _ratio(totals["raw_float32_xy"], totals["brotli"]),
        },
        "hausdorff_max_px": max(hausdorff_values) if hausdorff_values else 0.0,
        "hausdorff_mean_px": sum(hausdorff_values) / len(hausdorff_values) if hausdorff_values else 0.0,
    }


def _average_ratios(datasets: list[dict[str, Any]]) -> dict[str, float]:
    keys = list(datasets[0]["ratios"])
    return {
        key: sum(dataset["ratios"][key] for dataset in datasets) / len(datasets)
        for key in keys
    }


def _calliar_row_to_sample(row: Any) -> list[dict[str, list[int]]]:
    sample: list[dict[str, list[int]]] = []
    current = {"x": [], "y": [], "pressure": [], "tilt": [], "azimuth": []}
    for x_val, y_val, stroke_end in row.tolist():
        current["x"].append(int(round(float(x_val))))
        current["y"].append(int(round(float(y_val))))
        current["pressure"].append(512)
        current["tilt"].append(0)
        current["azimuth"].append(0)
        if int(stroke_end) == 1:
            if current["x"]:
                sample.append(current)
            current = {"x": [], "y": [], "pressure": [], "tilt": [], "azimuth": []}
    if current["x"]:
        sample.append(current)
    return sample


def _load_calliar_samples(path: Path, limit: int) -> list[list[dict[str, list[int]]]]:
    if importlib.util.find_spec("numpy") is None:
        raise RuntimeError("numpy is required for the bounded Calliar benchmark")
    import numpy as np

    data = np.load(path, allow_pickle=True)
    samples: list[list[dict[str, list[int]]]] = []
    for split_name in ("train", "valid", "test"):
        for row in data[split_name]:
            sample = _calliar_row_to_sample(row)
            if sample:
                samples.append(sample)
            if len(samples) >= limit:
                return samples
    return samples


def _comet_status(experiment_name: str, metrics: dict[str, float]) -> dict[str, Any]:
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
    experiment.add_tag("primitive-token-branch")
    for key, value in metrics.items():
        experiment.log_metric(key, value)
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
        default=str(REPO_ROOT / "proofs" / "reruns" / "primitive_token_branch" / "primitivetoken_benchmark.json"),
    )
    parser.add_argument("--calliar-limit", type=int, default=100)
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command_log = output_path.parent / "command_log.txt"
    free_bytes_before = _check_disk()
    frozen_claim_scope = _read_json(REPO_ROOT / "proofs" / "reruns" / "benchmark_freeze_local" / "claim_scope_map.json")

    brotli_command = [_detect_binary("brotli"), "-q", "11", "-c"]
    zstd_command = [_detect_binary("zstd"), "-3", "-q", "-c"]

    structured_datasets = [
        _sample_measurement(
            "synthetic_lossless",
            [generate_synthetic_lossless()],
            brotli_command=brotli_command,
            zstd_command=zstd_command,
            log_path=command_log,
        ),
        _sample_measurement(
            "iam_proxy",
            [generate_iam_proxy()],
            brotli_command=brotli_command,
            zstd_command=zstd_command,
            log_path=command_log,
        ),
        _sample_measurement(
            "unipen_proxy",
            [generate_unipen_proxy()],
            brotli_command=brotli_command,
            zstd_command=zstd_command,
            log_path=command_log,
        ),
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        calliar_path = temp_root / "calliar_dataset.npz"
        urllib.request.urlretrieve(CALLIAR_URL, calliar_path)
        calliar_samples = _load_calliar_samples(calliar_path, args.calliar_limit)
        calliar_dataset = _sample_measurement(
            "calliar_bounded",
            calliar_samples,
            brotli_command=brotli_command,
            zstd_command=zstd_command,
            log_path=command_log,
        )

    structured_overall = _average_ratios(structured_datasets)
    structured_beats_brotli = structured_overall["primitive_zstd"] > structured_overall["brotli"]
    telemetry = {
        "comet": _comet_status(
            "phase04-primitive-token-branch",
            {
                "ratio_sovereign_structured": structured_overall["sovereign"],
                "ratio_primitive_raw_structured": structured_overall["primitive_raw"],
                "ratio_primitive_zstd_structured": structured_overall["primitive_zstd"],
                "ratio_brotli_structured": structured_overall["brotli"],
                "hausdorff_mean_primitive_structured": sum(
                    dataset["hausdorff_mean_px"] for dataset in structured_datasets
                )
                / len(structured_datasets),
                "ratio_primitive_zstd_calliar": calliar_dataset["ratios"]["primitive_zstd"],
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
        "command_log": str(command_log),
        "disk_free_gib_before": round(free_bytes_before / (1024**3), 3),
        "structured_tier": {
            "datasets": structured_datasets,
            "overall_ratios": structured_overall,
            "frozen_phase2_ratios": {
                "sovereign": frozen_claim_scope["ratios"]["structured_tier"],
                "brotli": frozen_claim_scope["ratios"]["structured_engineering_comparators"]["brotli"],
                "zstd": frozen_claim_scope["ratios"]["structured_engineering_comparators"]["zstd"],
            },
        },
        "calliar_bounded": {
            "source_url": CALLIAR_URL,
            "limit": args.calliar_limit,
            **calliar_dataset,
        },
        "candidate_branch_result": {
            "structured_beats_brotli": structured_beats_brotli,
            "status": "BEATS_BROTLI" if structured_beats_brotli else "DOES_NOT_BEAT_BROTLI",
            "candidate_only": True,
        },
        "telemetry": telemetry,
    }
    write_json(output_path, payload)
    print("PRIMITIVE_TOKEN_BENCHMARK_COMPLETE")
    return 0


if __name__ == "__main__":
    import os

    raise SystemExit(main())
