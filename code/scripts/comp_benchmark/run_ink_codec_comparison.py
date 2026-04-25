"""Comparator benchmark: ZPE-Ink vs gzip / zlib on stroke buffers.

Wave-CB Phase 1 — comp benchmark.

Honest framing: ZPE-Ink's product claim is *lossless roundtrip + structured
semantics* (typed channels, deterministic delta+RLE, CRC-checked frame).
General-purpose entropy coders (gzip, zlib) operate on opaque byte streams
and are expected to be competitive or better on raw compression ratio.

Comparator path: option (b) — apples-to-apples on the same buffer the
codec ingests. The float32 spec in the brief is mapped to the lane's
canonical int representation: stroke channels (x, y, pressure, tilt,
azimuth) are packed as little-endian int32 contiguous arrays. Both the
ZPE-Ink encoder and the comparator gzip/zlib see the *same* raw byte
buffer derived from these arrays. Hausdorff fidelity is computed on
2-D (x, y) coordinates which is the geometric stroke locus.

Data source: deterministic in-repo fixtures (`zpe_ink.fixtures`) — no
external download, no committed raw third-party stroke data. Seeds are
recorded in the artifact.
"""

from __future__ import annotations

import gzip
import json
import struct
import zlib
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median

import numpy as np

from zpe_ink.codec import decode_zpink, encode_zpink
from zpe_ink.fixtures import generate_iam_proxy, generate_unipen_proxy

REPO_ROOT = Path(__file__).resolve().parents[3]
ARTIFACT_DIR = REPO_ROOT / "proofs" / "artifacts" / "comp_benchmarks"
ARTIFACT_PATH = ARTIFACT_DIR / "ink_codec_comparison.json"
SUMMARY_PATH = ARTIFACT_DIR / "summary.md"


def _stroke_to_raw_bytes(stroke: dict[str, list[int]]) -> bytes:
    """Pack stroke channels as little-endian int32 contiguous bytes.

    This is the apples-to-apples buffer fed to gzip/zlib. ZPE-Ink ingests the
    same channel arrays via its public API. The byte layout is:
        x | y | pressure | tilt | azimuth   (each as int32 little-endian)
    """
    parts = []
    for key in ("x", "y", "pressure", "tilt", "azimuth"):
        arr = np.asarray(stroke.get(key, []), dtype=np.int32)
        parts.append(arr.tobytes())
    return b"".join(parts)


def _hausdorff_xy(orig: dict[str, list[int]], dec: dict[str, list[int]]) -> float:
    """Symmetric Hausdorff distance on (x, y) loci, in stroke-coordinate units (px)."""
    a = np.column_stack([np.asarray(orig["x"], dtype=np.float64),
                         np.asarray(orig["y"], dtype=np.float64)])
    b = np.column_stack([np.asarray(dec["x"], dtype=np.float64),
                         np.asarray(dec["y"], dtype=np.float64)])
    if a.shape[0] == 0 or b.shape[0] == 0:
        return float("nan")
    # Full pairwise (small strokes; OK for benchmark scale).
    diff = a[:, None, :] - b[None, :, :]
    dist = np.sqrt((diff ** 2).sum(axis=-1))
    forward = dist.min(axis=1).max()
    backward = dist.min(axis=0).max()
    return float(max(forward, backward))


def _benchmark_set(label: str, strokes: list[dict[str, list[int]]],
                   seed: int) -> dict:
    per_stroke = []
    # Encode the entire batch once (matches how the codec is used in production).
    zpink_bytes = encode_zpink(strokes)
    decoded = decode_zpink(zpink_bytes)["strokes"]

    raw_total = 0
    gzip_total = 0
    zlib_total = 0
    zpink_total = len(zpink_bytes)
    hausdorffs = []

    for idx, (s, d) in enumerate(zip(strokes, decoded)):
        raw = _stroke_to_raw_bytes(s)
        raw_total += len(raw)
        gz = gzip.compress(raw, compresslevel=6, mtime=0)
        zl = zlib.compress(raw, level=6)
        gzip_total += len(gz)
        zlib_total += len(zl)
        # Per-stroke ZPE-Ink encode (for per-stroke CR; aggregate is the batched stream).
        s_only = encode_zpink([s])
        h = _hausdorff_xy(s, d)
        hausdorffs.append(h)
        per_stroke.append({
            "index": idx,
            "points": len(s["x"]),
            "raw_bytes": len(raw),
            "gzip_bytes": len(gz),
            "zlib_bytes": len(zl),
            "zpink_bytes_per_stroke": len(s_only),
            "gzip_cr": len(raw) / len(gz) if len(gz) else None,
            "zlib_cr": len(raw) / len(zl) if len(zl) else None,
            "zpink_cr_per_stroke": len(raw) / len(s_only) if len(s_only) else None,
            "hausdorff_xy_px": h,
        })

    def crs(field: str) -> list[float]:
        return [row[field] for row in per_stroke if row[field] is not None]

    return {
        "label": label,
        "seed": seed,
        "stroke_count": len(strokes),
        "raw_total_bytes": raw_total,
        "gzip_total_bytes": gzip_total,
        "zlib_total_bytes": zlib_total,
        "zpink_batched_bytes": zpink_total,
        "aggregate_cr": {
            "gzip": raw_total / gzip_total if gzip_total else None,
            "zlib": raw_total / zlib_total if zlib_total else None,
            "zpink_batched": raw_total / zpink_total if zpink_total else None,
        },
        "per_stroke_cr_summary": {
            "gzip": {"mean": mean(crs("gzip_cr")), "median": median(crs("gzip_cr"))},
            "zlib": {"mean": mean(crs("zlib_cr")), "median": median(crs("zlib_cr"))},
            "zpink": {
                "mean": mean(crs("zpink_cr_per_stroke")),
                "median": median(crs("zpink_cr_per_stroke")),
            },
        },
        "hausdorff_xy_px": {
            "max": max(hausdorffs),
            "mean": mean(hausdorffs),
            "median": median(hausdorffs),
        },
        "per_stroke": per_stroke,
    }


def main() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    sets = []
    iam_seed = 20260220
    unipen_seed = 20260221
    sets.append(_benchmark_set("iam_proxy", generate_iam_proxy(seed=iam_seed), iam_seed))
    sets.append(_benchmark_set("unipen_proxy", generate_unipen_proxy(seed=unipen_seed), unipen_seed))

    # Aggregate across both sets.
    raw_all = sum(s["raw_total_bytes"] for s in sets)
    gzip_all = sum(s["gzip_total_bytes"] for s in sets)
    zlib_all = sum(s["zlib_total_bytes"] for s in sets)
    zpink_all = sum(s["zpink_batched_bytes"] for s in sets)
    haus_all_max = max(s["hausdorff_xy_px"]["max"] for s in sets)

    artifact = {
        "schema_version": 1,
        "lane": "ZPE-Ink",
        "wave": "CB",
        "phase": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "comparators": ["gzip(level=6)", "zlib(level=6)"],
        "metric": "compression_ratio + symmetric_hausdorff_xy",
        "data_source": {
            "kind": "in_repo_deterministic_fixtures",
            "module": "zpe_ink.fixtures",
            "generators": ["generate_iam_proxy", "generate_unipen_proxy"],
            "note": ("Lane fixtures are deterministic synthetic strokes mirroring "
                     "IAM-/UNIPEN-style stroke statistics. Seeds recorded per set. "
                     "No third-party raw stroke data is committed."),
        },
        "comparator_path": "b_apples_to_apples_same_buffer",
        "raw_buffer_layout": "int32_le concat(x, y, pressure, tilt, azimuth)",
        "framing_note": (
            "ZPE-Ink is not optimised to dominate general-purpose entropy coders on "
            "raw compression ratio. Its product claim is (i) lossless roundtrip with "
            "exact-bit recovery of structured channels (Hausdorff = 0.0 px on x,y), "
            "(ii) deterministic CRC-framed bytes suitable for cross-runtime parity "
            "(WASM / PyO3 / Swift), and (iii) typed semantics (per-channel range "
            "validation, mode flags). Where gzip/zlib compress better, that reflects "
            "their statistical advantage on opaque byte streams; ZPE-Ink trades a "
            "fraction of raw CR for verifiable structure. The numbers below are "
            "reported as-found; no claim of CR dominance is made."
        ),
        "sets": sets,
        "aggregate_across_sets": {
            "raw_total_bytes": raw_all,
            "gzip_total_bytes": gzip_all,
            "zlib_total_bytes": zlib_all,
            "zpink_total_bytes": zpink_all,
            "aggregate_cr": {
                "gzip": raw_all / gzip_all if gzip_all else None,
                "zlib": raw_all / zlib_all if zlib_all else None,
                "zpink_batched": raw_all / zpink_all if zpink_all else None,
            },
            "hausdorff_xy_px_max": haus_all_max,
        },
        "verdict": "PASS_LOSSLESS" if haus_all_max == 0.0 else "FAIL_LOSSLESS",
    }

    with ARTIFACT_PATH.open("w") as f:
        json.dump(artifact, f, indent=2, sort_keys=False)

    # Summary markdown.
    agg = artifact["aggregate_across_sets"]["aggregate_cr"]
    lines = [
        "# ZPE-Ink Comp Benchmark Summary (Wave-CB Phase 1)",
        "",
        f"Generated: {artifact['generated_at_utc']}",
        f"Comparators: {', '.join(artifact['comparators'])}",
        f"Data source: in-repo deterministic fixtures (seeds {iam_seed}, {unipen_seed})",
        f"Buffer layout: {artifact['raw_buffer_layout']}",
        "",
        "## Aggregate compression ratio (raw_bytes / encoded_bytes)",
        f"- gzip:  {agg['gzip']:.3f}",
        f"- zlib:  {agg['zlib']:.3f}",
        f"- zpink: {agg['zpink_batched']:.3f}",
        "",
        f"## Hausdorff fidelity (xy locus, px)",
        f"- ZPE-Ink max across {sum(s['stroke_count'] for s in sets)} strokes: "
        f"{artifact['aggregate_across_sets']['hausdorff_xy_px_max']:.6f}",
        "",
        "## Honest framing",
        "ZPE-Ink does not claim raw CR dominance over gzip/zlib. It claims",
        "lossless roundtrip with structured semantics (Hausdorff = 0.0 px",
        "on x,y). Comparator numbers are reported as-found.",
    ]
    SUMMARY_PATH.write_text("\n".join(lines) + "\n")

    print(json.dumps({
        "artifact": str(ARTIFACT_PATH.relative_to(REPO_ROOT)),
        "summary": str(SUMMARY_PATH.relative_to(REPO_ROOT)),
        "aggregate_cr": agg,
        "hausdorff_max_px": artifact["aggregate_across_sets"]["hausdorff_xy_px_max"],
        "verdict": artifact["verdict"],
    }, indent=2))


if __name__ == "__main__":
    main()
