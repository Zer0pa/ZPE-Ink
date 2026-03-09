from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from zpe_ink.codec import decode_zpink, encode_zpink
from zpe_ink.fixtures import generate_iam_proxy, generate_synthetic_lossless, generate_unipen_proxy
from zpe_ink.io import append_log, write_json
from zpe_ink.metrics import compression_ratio, corpus_hausdorff, encode_latency_ms, pressure_rmse_percent


THRESHOLDS = {
    "compression_ratio_min": 5.0,
    "hausdorff_px_max": 1.0,
    "pressure_rmse_percent_max": 2.0,
    "encode_latency_ms_per_stroke_max": 2.0,
}


def _eval_corpus(name: str, strokes: list[dict[str, list[int]]]) -> dict[str, float | str | int]:
    encoded = encode_zpink(strokes, mode="lossless")
    decoded = decode_zpink(encoded)["strokes"]
    return {
        "name": name,
        "stroke_count": len(strokes),
        "point_count": sum(len(stroke["x"]) for stroke in strokes),
        "compression_ratio": compression_ratio(strokes, encoded),
        "hausdorff_px": corpus_hausdorff(strokes, decoded),
        "pressure_rmse_percent": pressure_rmse_percent(strokes, decoded),
        "encoded_bytes": len(encoded),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", required=True)
    args = parser.parse_args()
    root = Path(args.artifact_root)
    root.mkdir(parents=True, exist_ok=True)

    corpora = {
        "synthetic_lossless": generate_synthetic_lossless(),
        "iam_proxy": generate_iam_proxy(),
        "unipen_proxy": generate_unipen_proxy(),
    }

    # Measure encoder latency before heavier fidelity workloads to reduce thermal/scheduler distortion.
    latency = encode_latency_ms(corpora["iam_proxy"], repeats=40, warmup=8)

    per_corpus = [_eval_corpus(name, strokes) for name, strokes in corpora.items()]

    overall_ratio = sum(item["compression_ratio"] for item in per_corpus) / len(per_corpus)
    max_hausdorff = max(item["hausdorff_px"] for item in per_corpus)
    max_rmse = max(item["pressure_rmse_percent"] for item in per_corpus)

    compression_payload = {
        "claim_id": "INK-C002",
        "threshold": THRESHOLDS["compression_ratio_min"],
        "overall_ratio": overall_ratio,
        "pass": overall_ratio >= THRESHOLDS["compression_ratio_min"],
        "per_corpus": per_corpus,
        "comparator": {
            "incumbent": "raw float32 coordinate storage",
            "modern": "ink-stroke-modeler (or deterministic fallback)",
        },
    }
    fidelity_payload = {
        "claim_id": "INK-C003",
        "threshold_px": THRESHOLDS["hausdorff_px_max"],
        "max_hausdorff_px": max_hausdorff,
        "pass": max_hausdorff <= THRESHOLDS["hausdorff_px_max"],
        "per_corpus": [{"name": c["name"], "hausdorff_px": c["hausdorff_px"]} for c in per_corpus],
    }
    pressure_payload = {
        "claim_id": "INK-C004",
        "threshold_percent": THRESHOLDS["pressure_rmse_percent_max"],
        "max_rmse_percent": max_rmse,
        "pass": max_rmse <= THRESHOLDS["pressure_rmse_percent_max"],
        "per_corpus": [{"name": c["name"], "rmse_percent": c["pressure_rmse_percent"]} for c in per_corpus],
    }
    latency_payload = {
        "claim_id": "INK-C005",
        "threshold_ms_per_stroke": THRESHOLDS["encode_latency_ms_per_stroke_max"],
        **latency,
        "pass": latency["median_ms_per_stroke"] <= THRESHOLDS["encode_latency_ms_per_stroke_max"],
    }

    write_json(root / "ink_compression_benchmark.json", compression_payload)
    write_json(root / "ink_fidelity_metrics.json", fidelity_payload)
    write_json(root / "ink_pressure_metrics.json", pressure_payload)
    write_json(root / "ink_latency_benchmark.json", latency_payload)

    append_log(root / "regression_results.txt", f"[GATE_C] compression_pass={compression_payload['pass']}")
    append_log(root / "regression_results.txt", f"[GATE_C] fidelity_pass={fidelity_payload['pass']}")
    append_log(root / "regression_results.txt", f"[GATE_C] pressure_pass={pressure_payload['pass']}")
    append_log(root / "regression_results.txt", f"[GATE_C] latency_pass={latency_payload['pass']}")

    for payload, claim in [
        (compression_payload, "INK-C002"),
        (fidelity_payload, "INK-C003"),
        (pressure_payload, "INK-C004"),
        (latency_payload, "INK-C005"),
    ]:
        if not payload["pass"]:
            raise SystemExit(f"{claim} threshold failed")

    print("GATE_C_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
