from __future__ import annotations

import argparse
import gc
import hashlib
import json
import sys
import tracemalloc
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from zpe_ink.codec import ZPInkDecodeError, canonical_json, decode_zpink, encode_zpink
from zpe_ink.fixtures import (
    generate_adversarial_spike_set,
    generate_high_velocity_stroke,
    generate_long_page,
    generate_synthetic_lossless,
)
from zpe_ink.io import append_log, write_json


def _campaign_malformed() -> dict[str, object]:
    source = encode_zpink(generate_synthetic_lossless()[:4])
    corpus = {
        "truncated": source[:-7],
        "bad_magic": b"BROKE" + source[5:],
        "crc_tamper": source[:-1] + bytes([source[-1] ^ 0xAA]),
        "payload_len_tamper": source[:15] + b"\x01\x00\x00\x00" + source[19:],
    }
    total = len(corpus)
    caught = 0
    uncaught = []
    for name, sample in corpus.items():
        try:
            decode_zpink(sample)
            uncaught.append(name)
        except ZPInkDecodeError:
            caught += 1

    return {
        "campaign": "DT-INK-1",
        "total_cases": total,
        "caught_cases": caught,
        "uncaught_cases": uncaught,
        "uncaught_crash_rate_percent": 0.0 if not uncaught else 100.0 * len(uncaught) / total,
        "pass": len(uncaught) == 0,
    }


def _campaign_adversarial() -> dict[str, object]:
    spikes = generate_adversarial_spike_set()
    encoded = encode_zpink(spikes, mode="lossless")
    decoded = decode_zpink(encoded)["strokes"]
    max_pressure_diff = 0
    max_tilt_diff = 0
    for src, got in zip(spikes, decoded):
        max_pressure_diff = max(
            max_pressure_diff,
            max(abs(a - b) for a, b in zip(src["pressure"], got["pressure"])),
        )
        max_tilt_diff = max(max_tilt_diff, max(abs(a - b) for a, b in zip(src["tilt"], got["tilt"])))

    return {
        "campaign": "DT-INK-2",
        "stroke_count": len(spikes),
        "max_pressure_diff": max_pressure_diff,
        "max_tilt_diff": max_tilt_diff,
        "pass": max_pressure_diff == 0 and max_tilt_diff == 0,
    }


def _campaign_determinism() -> dict[str, object]:
    strokes = generate_synthetic_lossless(seed=20260220)
    hashes: list[str] = []
    for _ in range(5):
        encoded = encode_zpink(strokes, mode="lossless", seed=20260220)
        decoded = decode_zpink(encoded)
        payload = canonical_json(decoded).encode("utf-8")
        hashes.append(hashlib.sha256(payload).hexdigest())

    unique_count = len(set(hashes))
    return {
        "campaign": "DT-INK-3",
        "runs": 5,
        "unique_hashes": unique_count,
        "hashes": hashes,
        "pass": unique_count == 1,
    }


def _campaign_high_velocity() -> dict[str, object]:
    stroke = generate_high_velocity_stroke(__import__("random").Random(20260225), points=1800)
    encoded = encode_zpink([stroke], mode="lossless")
    decoded = decode_zpink(encoded)["strokes"][0]
    max_xy_diff = max(
        max(abs(a - b) for a, b in zip(stroke["x"], decoded["x"])),
        max(abs(a - b) for a, b in zip(stroke["y"], decoded["y"])),
    )
    return {
        "campaign": "DT-INK-4",
        "points": len(stroke["x"]),
        "max_xy_diff": max_xy_diff,
        "pass": max_xy_diff == 0,
    }


def _campaign_long_page() -> dict[str, object]:
    corpus = generate_long_page()
    tracemalloc.start()
    encoded = encode_zpink(corpus, mode="lossless")
    decoded = decode_zpink(encoded)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    gc.collect()
    peak_mb = peak / (1024 * 1024)
    return {
        "campaign": "DT-INK-5",
        "stroke_count": len(corpus),
        "decoded_stroke_count": len(decoded["strokes"]),
        "peak_memory_mb": peak_mb,
        "memory_ceiling_mb": 256.0,
        "pass": len(decoded["strokes"]) == len(corpus) and peak_mb <= 256.0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", required=True)
    args = parser.parse_args()

    root = Path(args.artifact_root)
    root.mkdir(parents=True, exist_ok=True)

    campaigns = [
        _campaign_malformed(),
        _campaign_adversarial(),
        _campaign_determinism(),
        _campaign_high_velocity(),
        _campaign_long_page(),
    ]

    determinism = next(item for item in campaigns if item["campaign"] == "DT-INK-3")
    write_json(
        root / "determinism_replay_results.json",
        {
            "runs": determinism["runs"],
            "unique_hashes": determinism["unique_hashes"],
            "pass": determinism["pass"],
        },
    )

    lines = ["# Falsification Results", ""]
    for campaign in campaigns:
        lines.append(f"## {campaign['campaign']}")
        lines.append(f"- PASS: {campaign['pass']}")
        for key, value in campaign.items():
            if key in {"campaign", "pass"}:
                continue
            lines.append(f"- {key}: {json.dumps(value)}")
        lines.append("")

    # Resource substitution notes from command probe results if needed.
    lines.extend(
        [
            "## Substitution Notes",
            "- If IAM/UNIPEN direct downloads were unavailable, deterministic proxy corpora were used.",
            "- If InkML.js package resolution failed, equivalent local XML parser path remained as fallback.",
            "- Claims impacted by non-equivalent substitutions remain PAUSED_EXTERNAL or FAIL in traceability outputs.",
        ]
    )
    (root / "falsification_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    uncaught_crash_rate = next(item for item in campaigns if item["campaign"] == "DT-INK-1")[
        "uncaught_crash_rate_percent"
    ]
    append_log(root / "regression_results.txt", f"[GATE_D] uncaught_crash_rate={uncaught_crash_rate}")
    append_log(root / "regression_results.txt", f"[GATE_D] determinism_unique_hashes={determinism['unique_hashes']}")

    if uncaught_crash_rate > 0:
        raise SystemExit("uncaught crash detected in malformed corpus")
    if not determinism["pass"]:
        raise SystemExit("determinism replay failed")
    for campaign in campaigns:
        if not campaign["pass"]:
            raise SystemExit(f"{campaign['campaign']} failed")

    print("GATE_D_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
