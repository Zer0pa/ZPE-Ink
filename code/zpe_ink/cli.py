from __future__ import annotations

import argparse
import json
import random
from typing import Sequence

from .codec import decode_zpink, encode_zpink
from .fixtures import generate_directional_stroke


def demo_payload() -> dict[str, int | str]:
    rng = random.Random(20260220)
    strokes = [generate_directional_stroke(rng, segments=8) for _ in range(3)]
    encoded = encode_zpink(strokes, mode="lossless", seed=20260220)
    decoded = decode_zpink(encoded)
    return {
        "encoded_bytes": len(encoded),
        "mode": decoded["mode"],
        "seed": decoded["seed"],
        "stroke_count": len(decoded["strokes"]),
    }


def roundtrip_check() -> bool:
    rng = random.Random(20260220)
    strokes = [generate_directional_stroke(rng, segments=10) for _ in range(4)]
    encoded = encode_zpink(strokes, mode="lossless", seed=20260220)
    decoded = decode_zpink(encoded)
    return decoded["strokes"] == strokes


def _run_demo() -> int:
    print(json.dumps(demo_payload(), indent=2, sort_keys=True))
    return 0


def _run_verify_roundtrip() -> int:
    if not roundtrip_check():
        raise SystemExit("roundtrip mismatch")
    print("roundtrip_ok")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="zpe-ink")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("demo", help="print a deterministic demo payload")
    subparsers.add_parser("verify-roundtrip", help="run the lossless roundtrip smoke test")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "demo":
        return _run_demo()
    if args.command == "verify-roundtrip":
        return _run_verify_roundtrip()
    raise SystemExit(f"unsupported command: {args.command}")


def entrypoint() -> None:
    raise SystemExit(main())


def demo_entry() -> None:
    raise SystemExit(_run_demo())


def verify_roundtrip_entry() -> None:
    raise SystemExit(_run_verify_roundtrip())
