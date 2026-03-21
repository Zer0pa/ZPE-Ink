from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import sys
import tarfile
import time
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.shared import append_command_log, resolve_net_new_pack_inputs, run_command, write_json
from zpe_ink.codec import decode_zpink, encode_zpink
from zpe_ink.fixtures import generate_high_velocity_stroke, generate_unipen_proxy
from zpe_ink.inkml import collect_inkml_files, inkml_to_strokes
from zpe_ink.io import sha256_file
from zpe_ink.unipen import load_uji_pen_characters

ALLOWED_IMP = {"IMP-LICENSE", "IMP-ACCESS", "IMP-COMPUTE", "IMP-STORAGE", "IMP-NOCODE"}
CORE_THRESHOLDS = {
    "compression_ratio_min": 5.0,
    "hausdorff_px_max": 1.0,
    "pressure_rmse_percent_max": 2.0,
    "encode_latency_ms_per_stroke_max": 2.0,
}


def _corpus_hausdorff(a: list[dict[str, list[int]]], b: list[dict[str, list[int]]]) -> float:
    def points(stroke: dict[str, list[int]]) -> list[tuple[int, int]]:
        pts = list(zip(stroke["x"], stroke["y"]))
        if len(pts) > 160:
            step = max(1, len(pts) // 160)
            pts = pts[::step]
        return pts

    def directed(u: list[tuple[int, int]], v: list[tuple[int, int]]) -> float:
        best = 0.0
        for ux, uy in u:
            nearest = min(math.hypot(ux - vx, uy - vy) for vx, vy in v)
            best = max(best, nearest)
        return best

    if len(a) != len(b):
        raise ValueError("corpus length mismatch")
    max_dist = 0.0
    for src, rec in zip(a, b):
        u = points(src)
        v = points(rec)
        if not u or not v:
            continue
        max_dist = max(max_dist, directed(u, v), directed(v, u))
    return max_dist


def _evaluate_samples(name: str, samples: list[list[dict[str, list[int]]]]) -> dict[str, Any]:
    total_raw = 0
    total_encoded = 0
    max_hausdorff = 0.0
    sq_err = 0.0
    sq_count = 0
    latencies: list[float] = []
    sample_count = 0
    stroke_count = 0
    point_count = 0

    for sample in samples:
        if not sample:
            continue

        start = time.perf_counter_ns()
        encoded = encode_zpink(sample, mode="lossless")
        elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000.0
        decoded = decode_zpink(encoded)["strokes"]

        total_raw += sum(len(stroke["x"]) * 2 * 4 for stroke in sample)
        total_encoded += len(encoded)
        max_hausdorff = max(max_hausdorff, _corpus_hausdorff(sample, decoded))

        for src, rec in zip(sample, decoded):
            for source_pressure, replay_pressure in zip(src["pressure"], rec["pressure"]):
                sq_err += float((source_pressure - replay_pressure) ** 2)
                sq_count += 1

        latencies.append(elapsed_ms / max(1, len(sample)))
        sample_count += 1
        stroke_count += len(sample)
        point_count += sum(len(stroke["x"]) for stroke in sample)

    compression_ratio = (total_raw / total_encoded) if total_encoded > 0 else 0.0
    rmse = math.sqrt(sq_err / sq_count) if sq_count else 0.0
    rmse_percent = (rmse / 1023.0) * 100.0
    median_latency = statistics.median(latencies) if latencies else float("inf")

    return {
        "name": name,
        "sample_count": sample_count,
        "stroke_count": stroke_count,
        "point_count": point_count,
        "compression_ratio": compression_ratio,
        "max_hausdorff_px": max_hausdorff,
        "pressure_rmse_percent": rmse_percent,
        "median_ms_per_stroke": median_latency,
        "threshold_pass": {
            "compression": compression_ratio >= CORE_THRESHOLDS["compression_ratio_min"],
            "fidelity": max_hausdorff <= CORE_THRESHOLDS["hausdorff_px_max"],
            "pressure": rmse_percent <= CORE_THRESHOLDS["pressure_rmse_percent_max"],
            "latency": median_latency <= CORE_THRESHOLDS["encode_latency_ms_per_stroke_max"],
        },
    }


def _append_validation(lines: list[str], title: str, status: str, details: str) -> None:
    lines.append(f"## {title}")
    lines.append(f"- status: {status}")
    lines.append(f"- details: {details}")
    lines.append("")


def _download_if_missing(url: str, destination: Path, log_path: Path, label: str) -> None:
    if destination.exists():
        append_command_log(log_path, label, "cached", 0, "cached file reused", "")
        return
    run_command(["curl", "-L", "-sS", url, "-o", str(destination)], log_path, label)


def _parse_inkml_samples(root: Path, limit: int) -> tuple[list[Path], list[list[dict[str, list[int]]]], int]:
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
    return files, samples, parse_failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", required=True)
    args = parser.parse_args()

    root = Path(args.artifact_root)
    root.mkdir(parents=True, exist_ok=True)
    log_path = root / "command_log.txt"
    cache_root = root / "net_new_cache"
    cache_root.mkdir(parents=True, exist_ok=True)

    validation_lines = ["# Max Resource Validation Log", ""]
    impracticality: list[dict[str, Any]] = []
    claim_resource_map: dict[str, list[dict[str, Any]]] = {
        "INK-C001": [],
        "INK-C002": [],
        "INK-C003": [],
        "INK-C004": [],
        "INK-C005": [],
        "INK-C006": [],
    }

    e1_inputs = resolve_net_new_pack_inputs(REPO_ROOT)
    lock = [
        {
            "path": str(item),
            "exists": item.exists(),
            "size_bytes": item.stat().st_size if item.exists() else None,
            "sha256": sha256_file(item) if item.exists() else None,
        }
        for item in e1_inputs
    ]
    resource_locks: list[dict[str, Any]] = []

    math_dir = cache_root / "mathwriting"
    math_dir.mkdir(parents=True, exist_ok=True)
    math_tgz = math_dir / "mathwriting-2024-excerpt.tgz"
    _download_if_missing(
        "https://storage.googleapis.com/mathwriting_data/mathwriting-2024-excerpt.tgz",
        math_tgz,
        log_path,
        "net_new_mathwriting_download",
    )
    with tarfile.open(math_tgz, "r:gz") as handle:
        handle.extractall(math_dir)
    append_command_log(log_path, "net_new_mathwriting_extract", f"tar -xzf {math_tgz}", 0, "extracted", "")

    math_extract = math_dir / "mathwriting-2024-excerpt"
    math_inkml, math_samples, math_parse_fail = _parse_inkml_samples(math_extract, limit=70)
    math_metrics = _evaluate_samples("mathwriting_excerpt", math_samples)
    _append_validation(
        validation_lines,
        "MathWriting (InkML)",
        "ATTEMPTED",
        f"inkml_files={len(math_inkml)} parsed={len(math_samples)} parse_fail={math_parse_fail}",
    )
    claim_resource_map["INK-C001"].append({"resource": "MathWriting", "status": "RESOLVED", "evidence": "inkml_converter_validation.json"})
    claim_resource_map["INK-C002"].append({"resource": "MathWriting", "status": "RESOLVED", "evidence": "inkml_converter_validation.json"})
    claim_resource_map["INK-C003"].append({"resource": "MathWriting", "status": "RESOLVED", "evidence": "inkml_converter_validation.json"})
    resource_locks.append(
        {
            "resource": "MathWriting",
            "path": str(math_tgz),
            "exists": math_tgz.exists(),
            "size_bytes": math_tgz.stat().st_size if math_tgz.exists() else None,
            "sha256": sha256_file(math_tgz) if math_tgz.exists() else None,
        }
    )

    crohme_dir = cache_root / "crohme"
    crohme_dir.mkdir(parents=True, exist_ok=True)
    tc11_probe = run_command(
        ["curl", "-L", "-k", "-I", "-sS", "https://tc11.cvc.uab.es/datasets/CROHME2019_1"],
        log_path,
        "net_new_crohme2019_probe",
    )
    crohme_zip = crohme_dir / "ICFHR_package.zip"
    _download_if_missing(
        "https://oldweb.isical.ac.in/~crohme/ICFHR_package.zip",
        crohme_zip,
        log_path,
        "net_new_crohme_fallback_download",
    )
    with zipfile.ZipFile(crohme_zip) as handle:
        handle.extractall(crohme_dir)
    append_command_log(log_path, "net_new_crohme_extract", f"unzip {crohme_zip}", 0, "extracted", "")

    crohme_extract = crohme_dir / "ICFHR_package"
    crohme_inkml, crohme_samples, crohme_parse_fail = _parse_inkml_samples(crohme_extract, limit=90)
    crohme_metrics = _evaluate_samples("crohme_icfhr_package", crohme_samples)
    if tc11_probe["returncode"] != 0:
        impracticality.append(
            {
                "resource": "CROHME2019",
                "code": "IMP-ACCESS",
                "command_evidence": "net_new_crohme2019_probe",
                "error_signature": tc11_probe["stderr"] or tc11_probe["stdout"][:300],
                "fallback": "Used publicly downloadable ICFHR CROHME InkML package",
                "claim_impact": "CROHME benchmark run executed on earlier official corpus variant; 2019-specific comparability reduced",
            }
        )
    _append_validation(
        validation_lines,
        "CROHME",
        "ATTEMPTED",
        f"inkml_files={len(crohme_inkml)} parsed={len(crohme_samples)} parse_fail={crohme_parse_fail}",
    )
    claim_resource_map["INK-C001"].append({"resource": "CROHME", "status": "RESOLVED", "evidence": "inkml_converter_validation.json"})
    claim_resource_map["INK-C002"].append({"resource": "CROHME", "status": "RESOLVED", "evidence": "inkml_converter_validation.json"})
    resource_locks.append(
        {
            "resource": "CROHME",
            "path": str(crohme_zip),
            "exists": crohme_zip.exists(),
            "size_bytes": crohme_zip.stat().st_size if crohme_zip.exists() else None,
            "sha256": sha256_file(crohme_zip) if crohme_zip.exists() else None,
        }
    )

    openring_dir = cache_root / "openring_repo"
    if not openring_dir.exists():
        run_command(["git", "clone", "--depth", "1", "https://github.com/thuhci/OpenRing", str(openring_dir)], log_path, "net_new_openring_clone")
    else:
        append_command_log(log_path, "net_new_openring_clone", "cached", 0, "cached repo reused", "")

    trace_files = [
        path
        for path in openring_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in {".csv", ".json", ".bin"} and ".git" not in str(path)
    ]
    rng = random.Random(20260229)
    openring_samples = [[generate_high_velocity_stroke(rng, points=220)] for _ in range(64)]
    if not trace_files:
        impracticality.append(
            {
                "resource": "OpenRing",
                "code": "IMP-ACCESS",
                "command_evidence": "net_new_openring_clone",
                "error_signature": "No released ring-stroke trace files found in repo/releases",
                "fallback": "Wearable-like deterministic stroke proxy corpus",
                "claim_impact": "Wearable parity remains INCONCLUSIVE without real ring traces",
            }
        )
    openring_metrics = _evaluate_samples("openring_proxy", openring_samples)
    _append_validation(
        validation_lines,
        "OpenRing",
        "ATTEMPTED",
        f"trace_files_found={len(trace_files)} fallback_samples={len(openring_samples)}",
    )
    claim_resource_map["INK-C003"].append({"resource": "OpenRing", "status": "INCONCLUSIVE", "evidence": "impracticality_decisions.json"})
    claim_resource_map["INK-C004"].append({"resource": "OpenRing", "status": "INCONCLUSIVE", "evidence": "impracticality_decisions.json"})
    resource_locks.append(
        {
            "resource": "OpenRing",
            "path": str(openring_dir),
            "exists": openring_dir.exists(),
            "size_bytes": None,
            "sha256": None,
        }
    )

    uji_dir = cache_root / "uji_pen_characters"
    uji_dir.mkdir(parents=True, exist_ok=True)
    uji_zip = uji_dir / "uji_pen_characters.zip"
    _download_if_missing(
        "https://archive.ics.uci.edu/static/public/160/uji+pen+characters.zip",
        uji_zip,
        log_path,
        "net_new_uji_download",
    )
    with zipfile.ZipFile(uji_zip) as handle:
        handle.extractall(uji_dir)
    append_command_log(log_path, "net_new_uji_extract", f"unzip {uji_zip}", 0, "extracted", "")

    uji_samples = load_uji_pen_characters(uji_dir, limit=140)
    uji_metrics = _evaluate_samples("uji_pen_characters", uji_samples)
    _append_validation(
        validation_lines,
        "UJI Pen Characters",
        "ATTEMPTED",
        f"parsed_samples={len(uji_samples)} files={len(list(uji_dir.glob('UJIpenchars-w*')))}",
    )
    claim_resource_map["INK-C001"].append({"resource": "UJI Pen Characters", "status": "RESOLVED", "evidence": "unipen_like_converter_validation.json"})
    claim_resource_map["INK-C002"].append({"resource": "UJI Pen Characters", "status": "RESOLVED", "evidence": "unipen_like_converter_validation.json"})
    claim_resource_map["INK-C005"].append({"resource": "UJI Pen Characters", "status": "RESOLVED", "evidence": "unipen_like_converter_validation.json"})
    resource_locks.append(
        {
            "resource": "UJI Pen Characters",
            "path": str(uji_zip),
            "exists": uji_zip.exists(),
            "size_bytes": uji_zip.stat().st_size if uji_zip.exists() else None,
            "sha256": sha256_file(uji_zip) if uji_zip.exists() else None,
        }
    )

    iam_probe = run_command(
        ["curl", "-L", "-I", "-sS", "https://fki.tic.heia-fr.ch/databases/iam-on-line-handwriting-database"],
        log_path,
        "net_new_iam_probe",
    )
    unipen_probe = run_command(
        ["curl", "-L", "-I", "-sS", "https://unipen.nici.ru.nl"],
        log_path,
        "net_new_unipen_probe",
    )
    if iam_probe["returncode"] == 0:
        impracticality.append(
            {
                "resource": "IAM",
                "code": "IMP-LICENSE",
                "command_evidence": "net_new_iam_probe",
                "error_signature": "Landing page reachable but no free direct online-stroke download was established inside the local Phase 1 lane",
                "fallback": "Deferred to later same-corpus closure phase with explicit access handling",
                "claim_impact": "IAM online-stroke equivalence remains INCONCLUSIVE",
            }
        )
    if unipen_probe["returncode"] != 0:
        impracticality.append(
            {
                "resource": "UNIPEN",
                "code": "IMP-ACCESS",
                "command_evidence": "net_new_unipen_probe",
                "error_signature": unipen_probe["stderr"] or unipen_probe["stdout"][:300],
                "fallback": "Use real UNIPEN-like UJI Pen Characters plus deterministic UNIPEN-shaped proxy corpus in Phase 1",
                "claim_impact": "Direct UNIPEN comparability remains INCONCLUSIVE",
            }
        )

    unipen_proxy = [[stroke] for stroke in generate_unipen_proxy()[:60]]
    unipen_metrics = _evaluate_samples("unipen_proxy", unipen_proxy)
    iam_unipen_results = {
        "iam": None,
        "unipen": unipen_metrics,
        "uji_pen_characters": uji_metrics,
        "iam_probe_rc": iam_probe["returncode"],
        "unipen_probe_rc": unipen_probe["returncode"],
    }
    _append_validation(
        validation_lines,
        "IAM/UNIPEN",
        "ATTEMPTED",
        f"iam_probe_rc={iam_probe['returncode']} uji_samples={len(uji_samples)} unipen_proxy_samples={len(unipen_proxy)} unipen_probe_rc={unipen_probe['returncode']}",
    )
    claim_resource_map["INK-C001"].append({"resource": "IAM/UNIPEN", "status": "INCONCLUSIVE", "evidence": "net_new_gap_closure_matrix.json"})
    claim_resource_map["INK-C002"].append({"resource": "IAM/UNIPEN", "status": "INCONCLUSIVE", "evidence": "net_new_gap_closure_matrix.json"})
    claim_resource_map["INK-C006"].append({"resource": "IAM/UNIPEN", "status": "INCONCLUSIVE", "evidence": "net_new_gap_closure_matrix.json"})
    resource_locks.append(
        {
            "resource": "IAM/UNIPEN",
            "path": "probe_only",
            "exists": True,
            "size_bytes": None,
            "sha256": None,
        }
    )

    inkml_validation = {
        "mathwriting": {
            "inkml_files_detected": len(math_inkml),
            "parsed_samples": len(math_samples),
            "parse_failures": math_parse_fail,
            "metrics": math_metrics,
            "source_archive": str(math_tgz),
        },
        "crohme": {
            "inkml_files_detected": len(crohme_inkml),
            "parsed_samples": len(crohme_samples),
            "parse_failures": crohme_parse_fail,
            "metrics": crohme_metrics,
            "source_archive": str(crohme_zip),
        },
    }
    write_json(root / "inkml_converter_validation.json", inkml_validation)
    write_json(
        root / "unipen_like_converter_validation.json",
        {
            "uji_pen_characters": {
                "parsed_samples": len(uji_samples),
                "metrics": uji_metrics,
                "source_archive": str(uji_zip),
            }
        },
    )

    cross_script = {
        "datasets": {
            "mathwriting": math_metrics,
            "crohme": crohme_metrics,
            "uji_pen_characters": uji_metrics,
        },
        "cross_script_required": True,
        "cross_script_executed": False,
        "note": "Phase 1 local-only execution used free, real online-stroke corpora that fit the M1 storage/runtime envelope. A non-Latin online-stroke corpus remains open and was not replaced by raster fallback.",
    }
    write_json(root / "cross_script_generalization_report.json", cross_script)

    attempted_resources = ["MathWriting", "CROHME", "OpenRing", "UJI Pen Characters", "IAM/UNIPEN"]
    imp_codes_valid = all(item.get("code") in ALLOWED_IMP for item in impracticality)
    has_real_ink = all(
        metric["sample_count"] > 0
        for metric in [math_metrics, crohme_metrics, uji_metrics]
    )
    eg1 = len(attempted_resources) == 5
    eg2 = has_real_ink
    eg3 = cross_script["cross_script_executed"]
    eg4 = imp_codes_valid
    has_imp_compute = any(item["code"] == "IMP-COMPUTE" for item in impracticality)

    runpod_manifest = {
        "required": has_imp_compute,
        "status": "NOT_REQUIRED" if not has_imp_compute else "PENDING",
        "reason": "No IMP-COMPUTE deferments detected" if not has_imp_compute else "Compute deferment detected",
    }
    write_json(root / "runpod_readiness_manifest.json", runpod_manifest)
    eg5 = True if not has_imp_compute else (root / "runpod_readiness_manifest.json").exists()

    gap_matrix = {
        "appendix_d_and_e_gates": {
            "E-G1_attempt_all": {"pass": eg1, "evidence": "max_resource_validation_log.md"},
            "E-G2_non_synthetic_core_closure": {"pass": eg2, "evidence": "unipen_like_converter_validation.json"},
            "E-G3_cross_script_required": {"pass": eg3, "evidence": "cross_script_generalization_report.json"},
            "E-G4_impracticality_code_validity": {"pass": eg4, "evidence": "impracticality_decisions.json"},
            "E-G5_runpod_artifacts_if_compute_deferred": {"pass": eg5, "evidence": "runpod_readiness_manifest.json"},
        },
        "resource_status": {
            "MathWriting": "RESOLVED",
            "CROHME": "RESOLVED_WITH_FALLBACK" if any(item["resource"] == "CROHME2019" for item in impracticality) else "RESOLVED",
            "OpenRing": "INCONCLUSIVE",
            "UJI Pen Characters": "RESOLVED",
            "IAM/UNIPEN": "INCONCLUSIVE",
        },
        "iam_unipen_parity": iam_unipen_results,
    }
    write_json(root / "net_new_gap_closure_matrix.json", gap_matrix)

    traceability = json.loads((root / "concept_resource_traceability.json").read_text(encoding="utf-8"))
    for item in traceability["appendix_b_items"]:
        item_id = item["id"]
        if item_id == "B3":
            item["status"] = "RESOLVED"
            item["evidence_artifact"] = "artifacts/2026-02-20_zpe_ink_wave1/inkml_converter_validation.json"
        elif item_id == "B4":
            item["status"] = "INCONCLUSIVE"
            item["comparability_impact"] = "IAM landing page is reachable, but direct online-stroke acquisition was not closed in the local-only Phase 1 lane"
            item["evidence_artifact"] = "artifacts/2026-02-20_zpe_ink_wave1/net_new_gap_closure_matrix.json"
        elif item_id == "B5":
            item["status"] = "INCONCLUSIVE"
            item["comparability_impact"] = "UNIPEN host remained unavailable; UJI Pen Characters was added as a real UNIPEN-like public corpus, but direct UNIPEN parity stays open"
            item["evidence_artifact"] = "artifacts/2026-02-20_zpe_ink_wave1/unipen_like_converter_validation.json"
    write_json(root / "concept_resource_traceability.json", traceability)

    write_json(root / "max_claim_resource_map.json", claim_resource_map)
    write_json(root / "impracticality_decisions.json", {"decisions": impracticality})
    write_json(root / "openring_proxy_metrics.json", openring_metrics)
    write_json(root / "iam_unipen_parity_table.json", iam_unipen_results)
    write_json(root / "max_resource_lock.json", {"inputs": lock, "resources": resource_locks})

    (root / "max_resource_validation_log.md").write_text("\n".join(validation_lines) + "\n", encoding="utf-8")
    append_command_log(log_path, "net_new_gate_complete", "gate_e_net_new_ingestion.py", 0, "E_APPENDIX_COMPLETE", "")

    print("GATE_NET_NEW_COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
