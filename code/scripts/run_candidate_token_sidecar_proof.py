from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from zpe_ink.codec import encode_zpink
from zpe_ink.fixtures import (
    generate_adversarial_spike_set,
    generate_iam_proxy,
    generate_synthetic_lossless,
    generate_unipen_proxy,
)
from zpe_ink.metrics import corpus_hausdorff
from zpe_ink.token_sidecar import build_token_sidecar_from_zpink, reconstruct_token_sidecar


def _dataset_cases() -> list[tuple[str, list[dict[str, list[int]]], str]]:
    return [
        ("synthetic_lossless", generate_synthetic_lossless(seed=20260424), "directional synthetic fixture"),
        ("iam_proxy", generate_iam_proxy(seed=20260424), "IAM proxy fixture"),
        ("unipen_proxy", generate_unipen_proxy(seed=20260424), "UNIPEN proxy fixture"),
        ("adversarial_spike", generate_adversarial_spike_set(seed=20260424), "high-velocity adversarial fixture"),
    ]


def _dataset_result(name: str, strokes: list[dict[str, list[int]]], note: str) -> dict[str, object]:
    payload = encode_zpink(strokes, mode="lossless", seed=20260424)
    first = build_token_sidecar_from_zpink(payload)
    second = build_token_sidecar_from_zpink(payload)
    reconstructed = reconstruct_token_sidecar(first)
    hausdorff = corpus_hausdorff(strokes, reconstructed)
    return {
        "dataset": name,
        "note": note,
        "stroke_count": len(strokes),
        "zpink_bytes": len(payload),
        "sidecar_sha256": first["sidecar_sha256"],
        "deterministic": first == second,
        "hausdorff_px": hausdorff,
        "fit_class": "bounded_directional_exact" if hausdorff == 0.0 else "not_promotable_general_surface",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    datasets = [_dataset_result(name, strokes, note) for name, strokes, note in _dataset_cases()]
    exact_datasets = [entry["dataset"] for entry in datasets if entry["hausdorff_px"] == 0.0]
    degraded_datasets = [entry["dataset"] for entry in datasets if entry["hausdorff_px"] != 0.0]

    verdict = {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "candidate_surface": "hybrid_token_sidecar",
        "status": "CANDIDATE_ONLY",
        "authority_rule": ".zpink remains sovereign; token sidecar is a bounded follow-on layer",
        "bounded_fit_summary": {
            "exact_directional_or_proxy_datasets": exact_datasets,
            "degraded_datasets": degraded_datasets,
        },
        "datasets": datasets,
        "decision": {
            "lane_verdict": "OPEN_BOUNDED_CANDIDATE",
            "promotion_verdict": "DO_NOT_PROMOTE_AS_GENERAL_RUNTIME",
            "allowed_use": "directional/proxy interchange indexing and candidate retrieval experiments",
            "kill_condition": "If high-velocity or non-directional corpora become primary, stop using the token sidecar as a fidelity surface.",
        },
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(verdict, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
