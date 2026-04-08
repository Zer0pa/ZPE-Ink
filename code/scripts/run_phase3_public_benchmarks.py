from __future__ import annotations

import argparse
import json
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.shared import append_command_log, run_command, write_json
from zpe_ink.benchmarks import measure_dataset
from zpe_ink.io import sha256_file
from zpe_ink.unipen import load_uji_pen_characters


IAM_URL = "https://fki.tic.heia-fr.ch/databases/iam-on-line-handwriting-database"
CASIA_URL = "https://nlpr.ia.ac.cn/databases/handwriting/home.html"
UJI_PAGE_URL = "https://archive.ics.uci.edu/dataset/160/uji+pen+characters"
UJI_ZIP_URL = "https://archive.ics.uci.edu/static/public/160/uji+pen+characters.zip"


def _safe_extract_zip(archive_path: Path, destination: Path) -> list[str]:
    extracted: list[str] = []
    destination = destination.resolve()
    with zipfile.ZipFile(archive_path) as handle:
        for member in handle.infolist():
            target = (destination / member.filename).resolve()
            if not str(target).startswith(str(destination)):
                raise ValueError(f"unsafe zip path: {member.filename}")
            handle.extract(member, destination)
            extracted.append(member.filename)
    return extracted


def _probe_url(url: str, log_path: Path, label: str) -> dict[str, Any]:
    result = run_command(
        [
            "curl",
            "-L",
            "-sS",
            "--max-time",
            "20",
            "-o",
            "/dev/null",
            "-w",
            "%{http_code} %{url_effective}",
            url,
        ],
        log_path,
        label,
    )
    status_code = "000"
    final_url = url
    parts = result["stdout"].strip().split(maxsplit=1)
    if parts:
        status_code = parts[0]
    if len(parts) == 2:
        final_url = parts[1]
    return {
        "url": url,
        "returncode": result["returncode"],
        "status_code": status_code,
        "final_url": final_url,
    }


def _blocked_row(name: str, url: str, probe: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "dataset": name,
        "source_url": url,
        "status": "blocked",
        "strokes": None,
        "points_per_stroke": None,
        "raw_size_bytes": None,
        "compressed_size_bytes": None,
        "compression_ratio": None,
        "roundtrip_fidelity": None,
        "note": reason,
        "probe": probe,
    }


def _blocked_note(probe: dict[str, Any]) -> str:
    if probe["returncode"] == 0 and probe["status_code"].startswith("2"):
        return f"Official page reachable via HTTP {probe['status_code']}, but no direct public corpus download was established for this phase."
    return (
        "Official access probe failed or timed out from this environment, "
        f"with rc={probe['returncode']} and status={probe['status_code']}."
    )


def _benchmark_uji(log_path: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="zpe-ink-phase3-uji-") as temp_root_str:
        temp_root = Path(temp_root_str)
        archive_path = temp_root / "uji_pen_characters.zip"
        extract_root = temp_root / "uji_pen_characters"

        download = run_command(
            ["curl", "-L", "-sS", "--max-time", "60", UJI_ZIP_URL, "-o", str(archive_path)],
            log_path,
            "phase3_uji_download",
        )
        if download["returncode"] != 0 or not archive_path.exists():
            raise RuntimeError("failed to download UJI Pen Characters archive")

        extracted = _safe_extract_zip(archive_path, extract_root)
        append_command_log(
            log_path,
            "phase3_uji_extract",
            f"safe-unzip {archive_path}",
            0,
            f"members={len(extracted)}",
            "",
        )

        samples = load_uji_pen_characters(extract_root, limit=100000)
        metrics = measure_dataset(samples)
        return {
            "dataset": "UJI Pen Characters",
            "source_url": UJI_PAGE_URL,
            "download_url": UJI_ZIP_URL,
            "status": "measured",
            "strokes": metrics["stroke_count"],
            "points_per_stroke": metrics["average_points_per_stroke"],
            "raw_size_bytes": metrics["raw_size_bytes"],
            "compressed_size_bytes": metrics["compressed_size_bytes"],
            "compression_ratio": metrics["compression_ratio"],
            "roundtrip_fidelity": metrics["roundtrip_fidelity"],
            "sample_count": metrics["sample_count"],
            "point_count": metrics["point_count"],
            "mode": metrics["mode"],
            "seed": metrics["seed"],
            "archive_sha256": sha256_file(archive_path),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run public Phase 3 dataset benchmarks for ZPE-Ink.")
    parser.add_argument(
        "--artifact-root",
        default=str(REPO_ROOT / "proofs" / "reruns" / "phase3_public_benchmarks"),
        help="Directory for JSON artifacts and command logs",
    )
    args = parser.parse_args()

    artifact_root = Path(args.artifact_root)
    artifact_root.mkdir(parents=True, exist_ok=True)
    log_path = artifact_root / "command_log.txt"

    iam_probe = _probe_url(IAM_URL, log_path, "phase3_iam_probe")
    casia_probe = _probe_url(CASIA_URL, log_path, "phase3_casia_probe")
    uji_probe = _probe_url(UJI_PAGE_URL, log_path, "phase3_uji_page_probe")

    uji_row = _benchmark_uji(log_path)
    rows = [
        _blocked_row(
            "IAM On-Line Handwriting",
            IAM_URL,
            iam_probe,
            f"Registration-gated dataset. {_blocked_note(iam_probe)}",
        ),
        _blocked_row(
            "CASIA Online Handwriting",
            CASIA_URL,
            casia_probe,
            f"Registration-gated dataset. {_blocked_note(casia_probe)}",
        ),
        uji_row,
    ]

    payload = {
        "generated_from": "code/scripts/run_phase3_public_benchmarks.py",
        "baseline": "raw float32 xy payload",
        "rows": rows,
        "probes": {
            "iam": iam_probe,
            "casia": casia_probe,
            "uji_page": uji_probe,
        },
    }
    write_json(artifact_root / "phase3_public_benchmarks.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
