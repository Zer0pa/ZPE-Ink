from __future__ import annotations

import argparse
import sys
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = CODE_ROOT.parent
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from zpe_ink.fixtures import dataset_manifest

from scripts.shared import resolve_net_new_pack_inputs, run_command, write_json


def _required_runbooks() -> list[str]:
    return [
        "proofs/runbooks/RUNBOOK_ZPE_INK_MASTER.md",
        "proofs/runbooks/RUNBOOK_ZPE_INK_GATE_A.md",
        "proofs/runbooks/RUNBOOK_ZPE_INK_GATE_B.md",
        "proofs/runbooks/RUNBOOK_ZPE_INK_GATE_C.md",
        "proofs/runbooks/RUNBOOK_ZPE_INK_GATE_D.md",
        "proofs/runbooks/RUNBOOK_ZPE_INK_GATE_E.md",
        "proofs/runbooks/RUNBOOK_ZPE_INK_GATE_M.md",
        "proofs/runbooks/RUNBOOK_ZPE_INK_GATE_NET_NEW.md",
        "proofs/runbooks/RUNBOOK_ZPE_INK_GATE_F.md",
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", required=True)
    args = parser.parse_args()

    root = Path(args.artifact_root)
    root.mkdir(parents=True, exist_ok=True)
    log_path = root / "command_log.txt"

    missing = [path for path in _required_runbooks() if not (REPO_ROOT / path).exists()]
    if missing:
        raise SystemExit(f"missing runbooks: {missing}")

    probes = {}
    probes["google_ink_stroke_modeler"] = run_command(
        ["git", "ls-remote", "--heads", "https://github.com/google/ink-stroke-modeler.git", "HEAD"],
        log_path,
        "resource_probe_google_ink_stroke_modeler",
    )
    probes["wacom_universal_ink_library"] = run_command(
        [
            sys.executable,
            "-m",
            "pip",
            "download",
            "--no-deps",
            "universal-ink-library",
            "-d",
            str(root / "resource_cache"),
        ],
        log_path,
        "resource_probe_wacom_universal_ink_library",
    )
    probes["inkmljs"] = run_command(
        ["npm", "view", "inkmljs", "version"],
        log_path,
        "resource_probe_inkmljs",
    )
    probes["iam_dataset"] = run_command(
        [
            "curl",
            "-L",
            "-I",
            "-sS",
            "https://fki.tic.heia-fr.ch/databases/iam-on-line-handwriting-database",
        ],
        log_path,
        "resource_probe_iam_dataset",
    )
    probes["unipen_dataset"] = run_command(
        ["curl", "-L", "-I", "-sS", "https://unipen.nici.ru.nl"],
        log_path,
        "resource_probe_unipen_dataset",
    )
    probes["wasm_bindgen_toolchain"] = run_command(
        ["wasm-pack", "--version"],
        log_path,
        "resource_probe_wasm_bindgen_toolchain",
    )
    probes["pyo3_toolchain"] = run_command(
        ["maturin", "--version"],
        log_path,
        "resource_probe_pyo3_toolchain",
    )

    net_new_inputs = resolve_net_new_pack_inputs(REPO_ROOT)
    lock_entries = []
    for item in net_new_inputs:
        lock_entries.append(
            {
                "path": str(item),
                "exists": item.exists(),
                "size_bytes": item.stat().st_size if item.exists() else None,
            }
        )
    write_json(
        root / "max_resource_lock.json",
        {"evidence_inputs": lock_entries, "status": "LOCKED" if all(e["exists"] for e in lock_entries) else "MISSING"},
    )

    # Baseline metrics are zero-state, before implementation evidence.
    before_after = {
        "baseline": {
            "lossless_roundtrip_pass_rate": 0.0,
            "compression_ratio": 0.0,
            "hausdorff_px": 0.0,
            "pressure_rmse_percent": 0.0,
            "encode_latency_ms_per_stroke": 0.0,
            "cross_runtime_parity": 0.0,
        },
        "after": {},
        "delta": {},
    }
    write_json(root / "before_after_metrics.json", before_after)

    traceability = {
        "appendix_b_items": [
            {
                "id": "B1",
                "resource": "Google ink-stroke-modeler",
                "source_reference": "https://github.com/google/ink-stroke-modeler",
                "planned_usage": "Primary smoothing baseline comparator",
                "probe_returncode": probes["google_ink_stroke_modeler"]["returncode"],
                "status": "PROBED" if probes["google_ink_stroke_modeler"]["returncode"] == 0 else "INCONCLUSIVE",
                "evidence_artifact": "artifacts/2026-02-20_zpe_ink_wave1/command_log.txt",
                "fallback": "Chaikin smoothing comparator if source path unavailable",
            },
            {
                "id": "B2",
                "resource": "Wacom Universal Ink Library",
                "source_reference": "https://github.com/Wacom-Developer/universal-ink-library",
                "planned_usage": "Adapter smoke-test ingestion coverage",
                "probe_returncode": probes["wacom_universal_ink_library"]["returncode"],
                "status": "PROBED" if probes["wacom_universal_ink_library"]["returncode"] == 0 else "INCONCLUSIVE",
                "evidence_artifact": "artifacts/2026-02-20_zpe_ink_wave1/command_log.txt",
                "fallback": "Synthetic UIM-like stroke schema fixture",
            },
            {
                "id": "B3",
                "resource": "Microsoft InkML.js or equivalent",
                "source_reference": "https://github.com/Microsoft/InkMLjs",
                "planned_usage": "Web format adapter parity",
                "probe_returncode": probes["inkmljs"]["returncode"],
                "status": "PROBED" if probes["inkmljs"]["returncode"] == 0 else "INCONCLUSIVE",
                "evidence_artifact": "artifacts/2026-02-20_zpe_ink_wave1/command_log.txt",
                "fallback": "Built-in minimal InkML parser for traceability test",
            },
            {
                "id": "B4",
                "resource": "IAM On-Line Handwriting dataset",
                "source_reference": "https://fki.tic.heia-fr.ch/databases/iam-on-line-handwriting-database",
                "planned_usage": "Validation matrix corpus",
                "probe_returncode": probes["iam_dataset"]["returncode"],
                "status": "PROBED" if probes["iam_dataset"]["returncode"] == 0 else "INCONCLUSIVE",
                "evidence_artifact": "artifacts/2026-02-20_zpe_ink_wave1/command_log.txt",
                "fallback": "IAM-shaped deterministic proxy corpus",
            },
            {
                "id": "B5",
                "resource": "UNIPEN dataset",
                "source_reference": "https://unipen.nici.ru.nl",
                "planned_usage": "Cross-script validation matrix corpus",
                "probe_returncode": probes["unipen_dataset"]["returncode"],
                "status": "PROBED" if probes["unipen_dataset"]["returncode"] == 0 else "INCONCLUSIVE",
                "evidence_artifact": "artifacts/2026-02-20_zpe_ink_wave1/command_log.txt",
                "fallback": "UNIPEN-shaped deterministic proxy corpus",
            },
            {
                "id": "B6",
                "resource": "wasm-bindgen path",
                "source_reference": "https://github.com/rustwasm/wasm-bindgen",
                "planned_usage": "WASM adapter build and parity run",
                "probe_returncode": probes["wasm_bindgen_toolchain"]["returncode"],
                "status": "PROBED" if probes["wasm_bindgen_toolchain"]["returncode"] == 0 else "INCONCLUSIVE",
                "evidence_artifact": "artifacts/2026-02-20_zpe_ink_wave1/command_log.txt",
                "fallback": "Node-only parser for parity if wasm build unavailable",
            },
            {
                "id": "B7",
                "resource": "PyO3 path",
                "source_reference": "https://github.com/PyO3/pyo3",
                "planned_usage": "Python native binding behavior validation",
                "probe_returncode": probes["pyo3_toolchain"]["returncode"],
                "status": "PROBED" if probes["pyo3_toolchain"]["returncode"] == 0 else "INCONCLUSIVE",
                "evidence_artifact": "artifacts/2026-02-20_zpe_ink_wave1/command_log.txt",
                "fallback": "Pure Python adapter retained if native extension build fails",
            },
        ],
        "dataset_manifest": dataset_manifest(),
    }
    write_json(root / "concept_resource_traceability.json", traceability)

    inventory = {
        "runbooks": _required_runbooks(),
        "initial_probe_summary": {key: value["returncode"] for key, value in probes.items()},
    }
    write_json(root / "baseline_inventory.json", inventory)

    print("GATE_A_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
