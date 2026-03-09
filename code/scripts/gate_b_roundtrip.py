from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from zpe_ink.codec import canonical_json, decode_zpink, encode_zpink
from zpe_ink.fixtures import generate_synthetic_lossless
from zpe_ink.io import append_log, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", required=True)
    args = parser.parse_args()

    root = Path(args.artifact_root)
    root.mkdir(parents=True, exist_ok=True)

    strokes = generate_synthetic_lossless()
    encoded = encode_zpink(strokes, mode="lossless", seed=20260220)
    decoded = decode_zpink(encoded)

    exact = decoded["strokes"] == strokes
    digest = hashlib.sha256(canonical_json(decoded).encode("utf-8")).hexdigest()

    sample_dir = root / "samples"
    sample_dir.mkdir(parents=True, exist_ok=True)
    sample_file = sample_dir / "synthetic_lossless.zpink"
    sample_file.write_bytes(encoded)

    output = {
        "claim_id": "INK-C001",
        "pass": exact,
        "stroke_count": len(strokes),
        "point_count_total": sum(len(stroke["x"]) for stroke in strokes),
        "canonical_hash": digest,
        "sample_file": str(sample_file),
    }
    write_json(root / "ink_roundtrip_results.json", output)

    append_log(root / "regression_results.txt", f"[GATE_B] lossless_roundtrip_pass={exact}")
    if not exact:
        raise SystemExit("roundtrip mismatch")

    print("GATE_B_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
