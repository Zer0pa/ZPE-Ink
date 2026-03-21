from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.shared import write_json


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _normalize_git_url(url: str | None) -> str:
    if not url:
        return ""
    cleaned = url.strip().rstrip("/")
    if cleaned.endswith(".git"):
        cleaned = cleaned[:-4]
    return cleaned


def _git_output(repo: Path, *args: str) -> str | None:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def _git_probe_origin(repo: Path) -> dict[str, Any]:
    proc = subprocess.run(
        ["git", "-C", str(repo), "ls-remote", "--symref", "origin", "HEAD"],
        capture_output=True,
        text=True,
    )
    head_ref = None
    for line in proc.stdout.splitlines():
        if line.startswith("ref: ") and "\tHEAD" in line:
            head_ref = line.split()[1]
            break
    return {
        "returncode": proc.returncode,
        "head_ref": head_ref,
        "stdout_preview": proc.stdout.splitlines()[:2],
        "stderr_preview": proc.stderr.splitlines()[:2],
    }


def _bool_metric(value: bool) -> int:
    return 1 if value else 0


def _collect_assets(review_pack_dir: Path, artifact_root: Path) -> list[Path]:
    assets: list[Path] = []
    seen: set[Path] = set()

    def add(path: Path) -> None:
        resolved = path.resolve()
        if resolved.exists() and resolved not in seen:
            seen.add(resolved)
            assets.append(resolved)

    for path in sorted(review_pack_dir.glob("*")):
        if path.is_file():
            add(path)

    key_artifacts = [
        artifact_root / "ink_compression_benchmark.json",
        artifact_root / "ink_cross_runtime_parity.json",
        artifact_root / "inkml_converter_validation.json",
        artifact_root / "unipen_like_converter_validation.json",
        artifact_root / "commercial_corpus_parity.json",
        artifact_root / "maximalization_gate_results.json",
        artifact_root / "command_log.txt",
    ]
    for path in key_artifacts:
        add(path)

    return assets


def _build_manifest(
    *,
    outer_workspace: Path,
    repo: Path,
    artifact_root: Path,
    review_pack_dir: Path,
    expected_origin: str,
    active_gate: str,
) -> dict[str, Any]:
    quality = _read_json(artifact_root / "quality_gate_scorecard.json")
    handoff = _read_json(artifact_root / "handoff_manifest.json")
    gap = _read_json(artifact_root / "net_new_gap_closure_matrix.json")
    compression = _read_json(artifact_root / "ink_compression_benchmark.json")
    parity = _read_json(artifact_root / "ink_cross_runtime_parity.json")
    inkml = _read_json(artifact_root / "inkml_converter_validation.json")
    uji = _read_json(artifact_root / "unipen_like_converter_validation.json")
    commercial = _read_json(artifact_root / "commercial_corpus_parity.json")
    maximalization = _read_json(artifact_root / "maximalization_gate_results.json")

    actual_origin = _git_output(repo, "remote", "get-url", "origin")
    branch = _git_output(repo, "branch", "--show-current") or "UNKNOWN"
    outer_branch = _git_output(outer_workspace, "branch", "--show-current") or "UNKNOWN"
    origin_probe = _git_probe_origin(repo)

    failing_gates = [
        gate_name
        for gate_name, gate_data in gap.get("appendix_d_and_e_gates", {}).items()
        if not gate_data.get("pass", False)
    ]
    cross_script = maximalization.get("cross_script_summary", {})
    math_metrics = inkml.get("mathwriting", {}).get("metrics", {})
    crohme_metrics = inkml.get("crohme", {}).get("metrics", {})
    uji_metrics = uji.get("uji_pen_characters", {}).get("metrics", {})
    commercial_datasets = commercial.get("datasets", {})
    pen_digits_ratio = commercial_datasets.get("uci_pendigits", {}).get("compression_ratio")

    manifest = {
        "timestamp_utc": _utc_timestamp(),
        "lane": "ZPE Ink",
        "workspace": str(outer_workspace.resolve()),
        "repo": str(repo.resolve()),
        "branch": branch,
        "active_gate": active_gate,
        "authority_state": {
            "go_no_go": handoff.get("go_no_go", "UNKNOWN"),
            "current_verdict": "INCONCLUSIVE",
            "failing_gates": failing_gates,
            "resource_status": gap.get("resource_status", {}),
        },
        "lane_boundary": {
            "outer_workspace_is_git_repo": (outer_workspace / ".git").exists(),
            "outer_workspace_branch": outer_branch,
            "inner_repo_is_git_repo": (repo / ".git").exists(),
        },
        "github_linkage": {
            "expected_origin": expected_origin,
            "actual_origin": actual_origin,
            "matches_expected": _normalize_git_url(actual_origin) == _normalize_git_url(expected_origin),
            "origin_probe": origin_probe,
        },
        "metrics": {
            "quality_total_score": quality.get("total_score"),
            "quality_minimum_required": quality.get("minimum_required"),
            "core_claims_pass": _bool_metric(bool(quality.get("core_claims_pass"))),
            "appendix_d_e_all_pass": _bool_metric(bool(quality.get("appendix_d_e_all_pass"))),
            "compression_ratio_structured": compression.get("overall_ratio"),
            "cross_runtime_pass": _bool_metric(bool(parity.get("pass"))),
            "mathwriting_compression_ratio": math_metrics.get("compression_ratio"),
            "crohme_compression_ratio": crohme_metrics.get("compression_ratio"),
            "uji_pen_characters_compression_ratio": uji_metrics.get("compression_ratio"),
            "uci_pen_digits_compression_ratio": pen_digits_ratio,
            "cross_script_executed": _bool_metric(bool(cross_script.get("cross_script_executed"))),
            "cross_script_required": _bool_metric(bool(cross_script.get("cross_script_required"))),
            "failing_gate_count": len(failing_gates),
            "handoff_file_count": len(handoff.get("files", [])),
        },
        "asset_paths": [str(path) for path in _collect_assets(review_pack_dir, artifact_root)],
    }
    return manifest


def _log_to_comet(
    *,
    manifest_path: Path,
    result_path: Path,
    manifest: dict[str, Any],
    asset_paths: list[str],
    api_key: str,
    workspace_name: str,
    project_name: str,
    experiment_name: str,
    agent_name: str,
) -> dict[str, Any]:
    try:
        from comet_ml import Experiment
    except ImportError as exc:
        raise RuntimeError("comet_ml is not installed in the active Python environment") from exc

    experiment = Experiment(
        api_key=api_key,
        workspace=workspace_name,
        project_name=project_name,
        log_code=False,
        auto_output_logging=False,
    )
    experiment.set_name(experiment_name)
    for tag in ["zpe-ink", "operational-realignment", "phase1_m1_local", agent_name.lower()]:
        experiment.add_tag(tag)

    experiment.log_parameter("lane", manifest["lane"])
    experiment.log_parameter("workspace", manifest["workspace"])
    experiment.log_parameter("repo", manifest["repo"])
    experiment.log_parameter("branch", manifest["branch"])
    experiment.log_parameter("active_gate", manifest["active_gate"])
    experiment.log_parameter("authority_go_no_go", manifest["authority_state"]["go_no_go"])
    experiment.log_parameter("authority_verdict", manifest["authority_state"]["current_verdict"])
    experiment.log_parameter("github_expected_origin", manifest["github_linkage"]["expected_origin"])
    experiment.log_parameter("github_actual_origin", manifest["github_linkage"]["actual_origin"] or "UNKNOWN")
    experiment.log_parameter("github_matches_expected", manifest["github_linkage"]["matches_expected"])
    experiment.log_parameter("outer_workspace_is_git_repo", manifest["lane_boundary"]["outer_workspace_is_git_repo"])
    experiment.log_parameter("inner_repo_is_git_repo", manifest["lane_boundary"]["inner_repo_is_git_repo"])
    experiment.log_parameter("agent_name", agent_name)

    for metric_name, metric_value in manifest["metrics"].items():
        if metric_value is None:
            continue
        experiment.log_metric(metric_name, metric_value)

    for gate_name in manifest["authority_state"]["failing_gates"]:
        experiment.log_other(f"failing_gate::{gate_name}", "FAIL")
    for resource_name, resource_state in manifest["authority_state"]["resource_status"].items():
        experiment.log_other(f"resource_status::{resource_name}", resource_state)

    experiment.log_asset(str(manifest_path), file_name=manifest_path.name)
    for asset_path in asset_paths:
        path = Path(asset_path)
        relative_name = path.name
        try:
            relative_name = str(path.relative_to(REPO_ROOT))
        except ValueError:
            pass
        experiment.log_asset(str(path), file_name=relative_name)

    result = {
        "timestamp_utc": _utc_timestamp(),
        "comet_workspace": workspace_name,
        "comet_project": project_name,
        "experiment_name": experiment_name,
        "experiment_key": experiment.get_key(),
        "experiment_url": getattr(experiment, "url", None),
        "logged_asset_count": len(asset_paths) + 1,
    }
    write_json(result_path, result)
    experiment.log_asset(str(result_path), file_name=result_path.name)
    experiment.end()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", required=True)
    parser.add_argument("--review-pack-dir", default=str(REPO_ROOT / "docs" / "team_review" / "2026-03-20_review_pack"))
    parser.add_argument("--outer-workspace", default=str(REPO_ROOT.parent))
    parser.add_argument("--expected-origin", default="https://github.com/Zer0pa/ZPE-Ink")
    parser.add_argument("--workspace-name", default="zer0pa")
    parser.add_argument("--project-name", default="zpe-ink")
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--agent-name", default="Codex")
    parser.add_argument(
        "--current-gate",
        default="operational realignment before GPD re-engagement",
    )
    parser.add_argument("--experiment-name")
    args = parser.parse_args()

    artifact_root = Path(args.artifact_root).resolve()
    review_pack_dir = Path(args.review_pack_dir).resolve()
    outer_workspace = Path(args.outer_workspace).resolve()

    if not artifact_root.exists():
        raise SystemExit(f"artifact root does not exist: {artifact_root}")
    if not review_pack_dir.exists():
        raise SystemExit(f"review pack does not exist: {review_pack_dir}")

    manifest = _build_manifest(
        outer_workspace=outer_workspace,
        repo=REPO_ROOT,
        artifact_root=artifact_root,
        review_pack_dir=review_pack_dir,
        expected_origin=args.expected_origin,
        active_gate=args.current_gate,
    )
    manifest_path = artifact_root / "comet_logging_manifest.json"
    write_json(manifest_path, manifest)

    experiment_name = args.experiment_name or f"zpe-ink-{artifact_root.name}-operational-realignment-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    result_path = artifact_root / "comet_logging_result.json"
    result = _log_to_comet(
        manifest_path=manifest_path,
        result_path=result_path,
        manifest=manifest,
        asset_paths=manifest["asset_paths"],
        api_key=args.api_key,
        workspace_name=args.workspace_name,
        project_name=args.project_name,
        experiment_name=experiment_name,
        agent_name=args.agent_name,
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
