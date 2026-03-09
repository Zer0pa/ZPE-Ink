from __future__ import annotations

import random
import sys
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1] / "code"
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from zpe_ink.codec import decode_zpink, encode_zpink
from zpe_ink.fixtures import generate_directional_stroke


def main() -> int:
    rng = random.Random(20260220)
    strokes = [generate_directional_stroke(rng, segments=10) for _ in range(4)]
    encoded = encode_zpink(strokes, mode="lossless", seed=20260220)
    decoded = decode_zpink(encoded)
    if decoded["strokes"] != strokes:
        raise SystemExit("roundtrip mismatch")
    print("roundtrip_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
