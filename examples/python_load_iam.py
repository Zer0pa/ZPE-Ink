#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = REPO_ROOT / "code"
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from zpe_ink.codec import decode_zpink, encode_zpink  # noqa: E402
from zpe_ink.fixtures import generate_iam_proxy  # noqa: E402
from zpe_ink.inkml import collect_inkml_files, inkml_to_strokes  # noqa: E402
from zpe_ink.unipen import parse_unipen_like_file  # noqa: E402


def _load_samples_from_path(path: Path, *, limit: int) -> list[list[dict[str, list[int]]]]:
    if path.is_dir():
        samples: list[list[dict[str, list[int]]]] = []
        for inkml_path in collect_inkml_files(path, limit=limit):
            strokes = inkml_to_strokes(inkml_path)
            if strokes:
                samples.append(strokes)
            if len(samples) >= limit:
                break
        return samples

    if path.suffix.lower() in {".inkml", ".xml"}:
        strokes = inkml_to_strokes(path)
        return [strokes] if strokes else []

    parsed = parse_unipen_like_file(path, limit=limit)
    return [sample["strokes"] for sample in parsed if sample.get("strokes")]


def _summarize_samples(samples: list[list[dict[str, list[int]]]]) -> dict[str, Any]:
    total_encoded = 0
    total_strokes = 0
    roundtrip_pass = True
    for sample in samples:
        encoded = encode_zpink(sample, mode="lossless", seed=20260408)
        decoded = decode_zpink(encoded)["strokes"]
        total_encoded += len(encoded)
        total_strokes += len(sample)
        roundtrip_pass = roundtrip_pass and decoded == sample
    return {
        "sample_count": len(samples),
        "stroke_count": total_strokes,
        "encoded_bytes": total_encoded,
        "roundtrip_pass": roundtrip_pass,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Load IAM-style input and round-trip it with the repo codec.")
    parser.add_argument("--input", type=Path, help="InkML or UNIPEN-like sample path")
    parser.add_argument("--limit", type=int, default=12, help="Maximum samples to load from a directory")
    parser.add_argument(
        "--proxy-demo",
        action="store_true",
        help="Use the synthetic IAM-shaped proxy corpus and do not claim real IAM data",
    )
    args = parser.parse_args()

    if args.input is None:
        args.proxy_demo = True

    if args.proxy_demo:
        samples = [generate_iam_proxy()]
        summary = {
            "mode": "proxy-demo",
            "source": "synthetic IAM-shaped strokes",
            "note": "Proxy mode only. No real IAM corpus is claimed.",
        }
    else:
        samples = _load_samples_from_path(args.input, limit=args.limit)
        summary = {
            "mode": "provided-input",
            "source": str(args.input),
            "note": "Input path may be InkML or UNIPEN-like. No proxy claims are mixed into this run.",
        }

    stats = _summarize_samples(samples)
    stats.update(summary)
    stats["preview"] = "real input" if not args.proxy_demo else "proxy demo"
    print(json.dumps(stats, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
