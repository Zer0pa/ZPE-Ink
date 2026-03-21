from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.shared import append_command_log, run_command, write_json
from zpe_ink.codec import decode_zpink, encode_zpink
from zpe_ink.fixtures import generate_adversarial_spike_set


def _make_long_stress_samples(seed: int = 20260301, stroke_count: int = 12000) -> list[dict[str, list[int]]]:
    rng = random.Random(seed)
    samples: list[dict[str, list[int]]] = []
    for _ in range(stroke_count):
        x = [rng.randint(0, 2048)]
        y = [rng.randint(0, 2048)]
        pressure = [rng.randint(350, 650)]
        tilt = [rng.randint(-120, 120)]
        azimuth = [rng.randint(0, 3599)]
        # Keep each stroke compact to maintain memory realism while meeting >10k stress requirement.
        for _step in range(9):
            x.append(x[-1] + rng.randint(-2, 2))
            y.append(y[-1] + rng.randint(-2, 2))
            pressure.append(max(0, min(1023, pressure[-1] + rng.randint(-4, 4))))
            tilt.append(max(-900, min(900, tilt[-1] + rng.randint(-2, 2))))
            azimuth.append((azimuth[-1] + rng.randint(-6, 6)) % 3600)
        samples.append({"x": x, "y": y, "pressure": pressure, "tilt": tilt, "azimuth": azimuth})
    return samples


def _csharp_header_probe(root: Path, log_path: Path) -> dict[str, Any]:
    parity_input = root / "parity" / "cross_runtime_input.zpink"
    runner_src = root / "parity" / "csharp_runner.cs"
    runner_bin = root / "parity" / "csharp_runner.exe"

    runner_src.write_text(
        """
using System;
using ZPE.Ink;

public static class Runner {
    public static int Main(string[] args) {
        if (args.Length < 1) return 2;
        var bytes = System.IO.File.ReadAllBytes(args[0]);
        var values = ZpeInk.DecodeHeader(bytes);
        Console.WriteLine($"version={values[0]},mode={values[1]},flags={values[2]},strokes={values[3]}");
        return 0;
    }
}
""".strip()
        + "\n",
        encoding="utf-8",
    )

    compile = run_command(
        [
            "mcs",
            "-out:" + str(runner_bin),
            str(runner_src),
            str(ROOT / "bindings" / "csharp" / "ZpeInk.cs"),
        ],
        log_path,
        "max_csharp_compile",
    )
    if compile["returncode"] != 0:
        return {
            "compiled": False,
            "executed": False,
            "stdout": "",
            "stderr": compile["stderr"],
        }

    run = run_command(["mono", str(runner_bin), str(parity_input)], log_path, "max_csharp_run")
    return {
        "compiled": True,
        "executed": run["returncode"] == 0,
        "stdout": run["stdout"].strip(),
        "stderr": run["stderr"].strip(),
        "returncode": run["returncode"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", required=True)
    args = parser.parse_args()

    root = Path(args.artifact_root)
    log_path = root / "command_log.txt"

    determinism = json.loads((root / "determinism_replay_results.json").read_text(encoding="utf-8"))
    parity = json.loads((root / "ink_cross_runtime_parity.json").read_text(encoding="utf-8"))
    impracticality = json.loads((root / "impracticality_decisions.json").read_text(encoding="utf-8"))
    gap = json.loads((root / "net_new_gap_closure_matrix.json").read_text(encoding="utf-8"))
    cross_script = json.loads((root / "cross_script_generalization_report.json").read_text(encoding="utf-8"))
    iam_unipen = json.loads((root / "iam_unipen_parity_table.json").read_text(encoding="utf-8"))

    # D5 kill test 1: pressure-noisy falsification subset.
    spikes = generate_adversarial_spike_set(seed=20260302)
    noisy_failures = 0
    for stroke in spikes:
        encoded = encode_zpink([stroke], mode="lossless")
        decoded = decode_zpink(encoded)["strokes"][0]
        if decoded != stroke:
            noisy_failures += 1

    # D5 kill test 3: sustained >10k stroke latency and stability.
    long_samples = _make_long_stress_samples()
    tracemalloc.start()
    start = time.perf_counter_ns()
    encoded = encode_zpink(long_samples, mode="lossless")
    decoded = decode_zpink(encoded)["strokes"]
    elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000.0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    long_uncaught_crash_rate = 0.0 if len(decoded) == len(long_samples) else 100.0
    long_latency_per_stroke = elapsed_ms / max(1, len(long_samples))

    # D5 kill test 2 + D2 managed runtime augmentation.
    csharp_probe = _csharp_header_probe(root, log_path)

    # Appendix D gate adjudication.
    iam_real_available = iam_unipen.get("iam") is not None and iam_unipen.get("iam", {}).get("sample_count", 0) > 0
    unipen_real_available = False  # UNIPEN host probe failed in this run; fallback proxy retained.
    m1_pass = iam_real_available and unipen_real_available

    m2_pass = parity.get("pass", False) and csharp_probe.get("compiled", False) and csharp_probe.get("executed", False)
    m3_pass = (
        noisy_failures == 0
        and long_uncaught_crash_rate == 0.0
        and determinism.get("pass", False)
        and determinism.get("runs", 0) == 5
        and determinism.get("unique_hashes", 99) == 1
    )
    decisions = impracticality.get("decisions", [])
    quantified_impacts = all(bool(item.get("claim_impact")) for item in decisions)
    m4_pass = quantified_impacts

    max_gates = {
        "M1_real_iam_unipen_non_inferior": {
            "pass": m1_pass,
            "status": "PASS" if m1_pass else "FAIL",
            "note": "Real IAM/UNIPEN non-inferiority not met; UNIPEN direct corpus unavailable and fallback parity under target",
            "evidence": "iam_unipen_parity_table.json",
        },
        "M2_cross_runtime_plus_inconclusive_runtime_closure": {
            "pass": m2_pass,
            "status": "PASS" if m2_pass else "FAIL",
            "note": "C# managed-runtime adapter executed header parity check",
            "evidence": "ink_cross_runtime_parity.json",
        },
        "M3_long_sequence_stress_and_determinism": {
            "pass": m3_pass,
            "status": "PASS" if m3_pass else "FAIL",
            "evidence": "falsification_results.md",
            "metrics": {
                "stress_stroke_count": len(long_samples),
                "stress_latency_ms_per_stroke": long_latency_per_stroke,
                "stress_peak_memory_mb": peak / (1024 * 1024),
                "uncaught_crash_rate_percent": long_uncaught_crash_rate,
            },
        },
        "M4_inconclusive_resolution_or_quantified_retention": {
            "pass": m4_pass,
            "status": "PASS" if m4_pass else "FAIL",
            "evidence": "impracticality_decisions.json",
        },
    }

    write_json(
        root / "maximalization_gate_results.json",
        {
            "gates": max_gates,
            "kill_tests": {
                "pressure_noisy_failures": noisy_failures,
                "long_sequence_stroke_count": len(long_samples),
                "long_sequence_latency_ms_per_stroke": long_latency_per_stroke,
                "long_sequence_uncaught_crash_rate_percent": long_uncaught_crash_rate,
            },
            "csharp_probe": csharp_probe,
            "cross_script_summary": cross_script,
        },
    )

    # Update gap closure matrix with maximalization gate outcomes.
    gap.setdefault("appendix_d_and_e_gates", {})
    gap["appendix_d_and_e_gates"].update(
        {
            "M1_real_iam_unipen_non_inferior": {
                "pass": m1_pass,
                "evidence": "maximalization_gate_results.json",
            },
            "M2_cross_runtime_inconclusive_runtime_closure": {
                "pass": m2_pass,
                "evidence": "maximalization_gate_results.json",
            },
            "M3_long_sequence_and_determinism": {
                "pass": m3_pass,
                "evidence": "maximalization_gate_results.json",
            },
            "M4_quantified_inconclusive_retention": {
                "pass": m4_pass,
                "evidence": "impracticality_decisions.json",
            },
        }
    )
    write_json(root / "net_new_gap_closure_matrix.json", gap)

    # Extend falsification report with Appendix D kill tests.
    falsification_path = root / "falsification_results.md"
    with falsification_path.open("a", encoding="utf-8") as handle:
        handle.write("\n## Appendix D Maximalization Kill Tests\n")
        handle.write(f"- pressure_noisy_failures: {noisy_failures}\n")
        handle.write(f"- long_sequence_stroke_count: {len(long_samples)}\n")
        handle.write(f"- long_sequence_latency_ms_per_stroke: {long_latency_per_stroke:.6f}\n")
        handle.write(f"- long_sequence_uncaught_crash_rate_percent: {long_uncaught_crash_rate}\n")
        handle.write(f"- csharp_managed_runtime_probe: {json.dumps(csharp_probe)}\n")

    with (root / "regression_results.txt").open("a", encoding="utf-8") as handle:
        handle.write(f"\n[GATE_M] m1_pass={m1_pass}")
        handle.write(f"\n[GATE_M] m2_pass={m2_pass}")
        handle.write(f"\n[GATE_M] m3_pass={m3_pass}")
        handle.write(f"\n[GATE_M] m4_pass={m4_pass}\n")

    append_command_log(log_path, "max_gate_complete", "gate_m_maximalization.py", 0, "M_APPENDIX_COMPLETE", "")

    print("GATE_M_COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
