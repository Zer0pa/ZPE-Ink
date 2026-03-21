from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
import tempfile
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
from zpe_ink.inkml import collect_inkml_files, inkml_to_strokes
from zpe_ink.phase2_authority import (
    build_claim_scope_map,
    build_contradiction_manifest,
    raw_float32_xy_payload,
)
from zpe_ink.unipen import load_uji_pen_characters


COMPARATOR_SPECS = {
    "zstd": {"command": ["zstd", "-19", "-q", "-c"], "version_args": ["--version"]},
    "brotli": {"command": ["brotli", "-q", "11", "-c"], "version_args": ["--version"]},
    "lz4": {"command": ["lz4", "-9", "-z", "-c"], "version_args": ["-V"]},
}


def _timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_release_report_verdict(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Verdict:"):
            return line.split("`")[1]
    return "INCONCLUSIVE"


def _read_license_text(pyproject_path: Path) -> str:
    for line in pyproject_path.read_text(encoding="utf-8").splitlines():
        if "LicenseRef-Zer0pa-SAL-6.0" in line:
            return "LicenseRef-Zer0pa-SAL-6.0"
    return "UNKNOWN"


def _run_text_command(command: list[str], log_path: Path, label: str, *, cwd: Path | None = None) -> dict[str, Any]:
    proc = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    append_command_log(log_path, label, " ".join(command), proc.returncode, proc.stdout, proc.stderr)
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def _run_binary_command(
    command: list[str],
    data: bytes,
    log_path: Path,
    label: str,
    *,
    cwd: Path | None = None,
) -> dict[str, Any]:
    proc = subprocess.run(command, cwd=cwd, input=data, capture_output=True)
    stderr_text = proc.stderr.decode("utf-8", errors="ignore")
    append_command_log(
        log_path,
        label,
        " ".join(command),
        proc.returncode,
        f"stdout_bytes={len(proc.stdout)}",
        stderr_text,
    )
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout_bytes": len(proc.stdout),
        "stderr": stderr_text,
    }


def _detect_comparators(log_path: Path) -> dict[str, dict[str, Any]]:
    comparators: dict[str, dict[str, Any]] = {}
    for name, spec in COMPARATOR_SPECS.items():
        binary = shutil.which(spec["command"][0])
        if binary is None:
            raise RuntimeError(f"required comparator binary not found: {name}")
        version_result = _run_text_command(
            [binary, *spec["version_args"]],
            log_path,
            f"phase2_{name}_version",
        )
        version = version_result["stdout"].strip() or version_result["stderr"].strip()
        comparators[name] = {
            "path": binary,
            "command": [binary, *spec["command"][1:]],
            "version": version,
        }
    return comparators


def _parse_inkml_dataset(root: Path, *, limit: int) -> dict[str, Any]:
    files = collect_inkml_files(root, limit=limit)
    samples: list[list[dict[str, list[int]]]] = []
    parse_failures = 0
    for path in files:
        try:
            strokes = inkml_to_strokes(path)
        except Exception:
            parse_failures += 1
            continue
        if strokes:
            samples.append(strokes)
    return {
        "samples": samples,
        "files_detected": len(files),
        "parse_failures": parse_failures,
        "source": str(root),
    }


def _load_public_corpora(phase1_root: Path) -> dict[str, dict[str, Any]]:
    cache_root = phase1_root / "net_new_cache"
    return {
        "mathwriting": _parse_inkml_dataset(
            cache_root / "mathwriting" / "mathwriting-2024-excerpt",
            limit=70,
        ),
        "crohme": _parse_inkml_dataset(
            cache_root / "crohme" / "ICFHR_package",
            limit=90,
        ),
        "uji_pen_characters": {
            "samples": load_uji_pen_characters(cache_root / "uji_pen_characters", limit=140),
            "source": str(cache_root / "uji_pen_characters"),
        },
    }


def _ratio(raw_size: int, encoded_size: int) -> float:
    if encoded_size <= 0:
        raise ValueError("encoded size must be positive")
    return raw_size / encoded_size


def _measure_dataset(
    name: str,
    samples: list[list[dict[str, list[int]]]],
    comparators: dict[str, dict[str, Any]],
    log_path: Path,
) -> dict[str, Any]:
    totals: dict[str, int] = {"raw_float32_xy": 0, "zpe_ink": 0}
    totals.update({name: 0 for name in comparators})

    sample_count = 0
    stroke_count = 0
    point_count = 0

    for index, sample in enumerate(samples):
        if not sample:
            continue
        raw_payload = raw_float32_xy_payload(sample)
        encoded = encode_zpink(sample, mode="lossless")

        totals["raw_float32_xy"] += len(raw_payload)
        totals["zpe_ink"] += len(encoded)
        sample_count += 1
        stroke_count += len(sample)
        point_count += sum(len(stroke["x"]) for stroke in sample)

        for comparator_name, comparator in comparators.items():
            result = _run_binary_command(
                comparator["command"],
                raw_payload,
                log_path,
                f"{name}_{comparator_name}_{index:03d}",
            )
            if result["returncode"] != 0:
                raise RuntimeError(f"{comparator_name} failed for {name}")
            totals[comparator_name] += result["stdout_bytes"]

    ratios = {
        "raw_float32_xy": 1.0,
        "zpe_ink": _ratio(totals["raw_float32_xy"], totals["zpe_ink"]),
    }
    for comparator_name in comparators:
        ratios[comparator_name] = _ratio(totals["raw_float32_xy"], totals[comparator_name])

    return {
        "name": name,
        "sample_count": sample_count,
        "stroke_count": stroke_count,
        "point_count": point_count,
        "sizes_bytes": totals,
        "ratios": ratios,
    }


def _summarize_structured(datasets: list[dict[str, Any]]) -> dict[str, Any]:
    comparator_names = list(datasets[0]["ratios"])
    overall_ratios = {}
    for comparator_name in comparator_names:
        overall_ratios[comparator_name] = sum(item["ratios"][comparator_name] for item in datasets) / len(datasets)
    return {
        "datasets": datasets,
        "overall_ratios": overall_ratios,
        "threshold": 5.0,
    }


def _environment_verification(log_path: Path, contradiction_root: Path) -> dict[str, Any]:
    free_disk_gib = shutil.disk_usage(REPO_ROOT).free / (1024 ** 3)
    pytest_result = _run_text_command(
        [sys.executable, "-m", "pytest", "tests", "-q"],
        log_path,
        "phase2_pytest",
        cwd=ROOT,
    )

    with tempfile.TemporaryDirectory(dir=contradiction_root) as wheel_dir:
        wheel_result = _run_text_command(
            [sys.executable, "-m", "pip", "wheel", ".", "--no-deps", "-w", wheel_dir],
            log_path,
            "phase2_wheel_build",
            cwd=ROOT,
        )
        wheel_files = [
            {
                "name": path.name,
                "size_bytes": path.stat().st_size,
            }
            for path in sorted(Path(wheel_dir).glob("*.whl"))
        ]

    adb_path = shutil.which("adb")
    adb_result = None
    adb_devices: list[str] = []
    if adb_path is not None:
        adb_result = _run_text_command([adb_path, "devices", "-l"], log_path, "phase2_adb_devices")
        adb_devices = [
            line.strip()
            for line in adb_result["stdout"].splitlines()
            if line.strip() and not line.startswith("List of devices attached")
        ]

    return {
        "schema_version": 1,
        "generated_at": _timestamp(),
        "platform": platform.platform(),
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
        "free_disk_gib": round(free_disk_gib, 3),
        "pytest": {
            "returncode": pytest_result["returncode"],
            "stdout_tail": pytest_result["stdout"].strip().splitlines()[-10:],
        },
        "wheel_build": {
            "returncode": wheel_result["returncode"],
            "wheel_files": wheel_files,
        },
        "adb": {
            "available": adb_path is not None,
            "attached_devices": adb_devices,
            "stdout_tail": [] if adb_result is None else adb_result["stdout"].strip().splitlines()[-10:],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase1-root",
        default=str(REPO_ROOT / "proofs" / "reruns" / "phase1_m1_local"),
    )
    parser.add_argument(
        "--contradiction-root",
        default=str(REPO_ROOT / "proofs" / "reruns" / "contradiction_resolution_local"),
    )
    parser.add_argument(
        "--benchmark-root",
        default=str(REPO_ROOT / "proofs" / "reruns" / "benchmark_freeze_local"),
    )
    args = parser.parse_args()

    phase1_root = Path(args.phase1_root)
    contradiction_root = Path(args.contradiction_root)
    benchmark_root = Path(args.benchmark_root)
    contradiction_root.mkdir(parents=True, exist_ok=True)
    benchmark_root.mkdir(parents=True, exist_ok=True)

    command_log = contradiction_root / "command_log.txt"
    environment = _environment_verification(command_log, contradiction_root)
    write_json(contradiction_root / "environment_verification.json", environment)

    scorecard = _read_json(phase1_root / "quality_gate_scorecard.json")
    handoff = _read_json(phase1_root / "handoff_manifest.json")
    gap_matrix = _read_json(phase1_root / "net_new_gap_closure_matrix.json")
    blockers_before_after = _read_json(phase1_root / "blockers_before_after.json")
    release_report_verdict = _read_release_report_verdict(REPO_ROOT / "proofs" / "INK_WAVE1_RELEASE_READINESS_REPORT.md")

    failing_gates = {
        gate_id: payload
        for gate_id, payload in gap_matrix["appendix_d_and_e_gates"].items()
        if not payload.get("pass", False)
    }

    contradiction_manifest = build_contradiction_manifest(
        scorecard_pass=bool(scorecard.get("pass", False)),
        appendix_all_pass=bool(scorecard.get("appendix_d_e_all_pass", False)),
        handoff_go_no_go=handoff.get("go_no_go", "NO-GO"),
        release_report_verdict=release_report_verdict,
        failing_gates=failing_gates,
        remaining_blockers=blockers_before_after.get("remaining_blockers", []),
        free_disk_gib=environment["free_disk_gib"],
        adb_available=bool(environment["adb"]["available"]),
        adb_devices=environment["adb"]["attached_devices"],
    )
    write_json(contradiction_root / "contradiction_resolution_manifest.json", contradiction_manifest)

    comparators = _detect_comparators(command_log)
    corpora = _load_public_corpora(phase1_root)

    structured_datasets = [
        _measure_dataset("synthetic_lossless", [generate_synthetic_lossless()], comparators, command_log),
        _measure_dataset("iam_proxy", [generate_iam_proxy()], comparators, command_log),
        _measure_dataset("unipen_proxy", [generate_unipen_proxy()], comparators, command_log),
    ]
    hard_datasets = [
        _measure_dataset("mathwriting", corpora["mathwriting"]["samples"], comparators, command_log),
        _measure_dataset("crohme", corpora["crohme"]["samples"], comparators, command_log),
    ]
    supporting_public = [
        _measure_dataset("uji_pen_characters", corpora["uji_pen_characters"]["samples"], comparators, command_log),
    ]

    baseline_results = {
        "schema_version": 1,
        "generated_at": _timestamp(),
        "source_artifact_root": str(phase1_root),
        "freeze_rules": {
            "raw_baseline": "little-endian float32 x/y pairs only, matching the existing raw float32 coordinate baseline",
            "compression_unit": "per-sample compression with encoded sizes summed across the corpus",
            "same_corpus_rule": "Each comparator sees the same raw x/y payload bytes before compression",
        },
        "comparators": {
            "raw_float32_xy": {"version": "baseline"},
            **{
                name: {
                    "path": comparator["path"],
                    "command": comparator["command"],
                    "version": comparator["version"],
                }
                for name, comparator in comparators.items()
            },
        },
        "structured_tier": _summarize_structured(structured_datasets),
        "hard_corpus": {
            "datasets": hard_datasets,
        },
        "supporting_public_corpora": {
            "datasets": supporting_public,
        },
        "transport_gate_snapshot": {
            "core_claims_pass": bool(scorecard.get("core_claims_pass", False)),
            "quality_scorecard_pass": bool(scorecard.get("pass", False)),
            "appendix_all_pass": bool(scorecard.get("appendix_d_e_all_pass", False)),
        },
    }
    write_json(benchmark_root / "baseline_results.json", baseline_results)

    claim_scope_map = build_claim_scope_map(
        structured_ratio=baseline_results["structured_tier"]["overall_ratios"]["zpe_ink"],
        structured_threshold=baseline_results["structured_tier"]["threshold"],
        structured_comparator_ratios={
            name: ratio
            for name, ratio in baseline_results["structured_tier"]["overall_ratios"].items()
            if name not in {"raw_float32_xy", "zpe_ink"}
        },
        hard_ratios={
            item["name"]: item["ratios"]["zpe_ink"]
            for item in baseline_results["hard_corpus"]["datasets"]
        },
        transport_gates_pass=bool(scorecard.get("core_claims_pass", False)),
        license_text=_read_license_text(ROOT / "pyproject.toml"),
        sovereign_release_verdict=contradiction_manifest["resolution_state"]["sovereign_release_verdict"],
        contradiction_status=contradiction_manifest["resolution_state"]["contradiction_status"],
    )
    write_json(benchmark_root / "claim_scope_map.json", claim_scope_map)

    print("PHASE2_TRUTH_SURFACE_COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
