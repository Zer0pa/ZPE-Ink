from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from zpe_ink.codec import canonical_json, decode_zpink, encode_zpink
from zpe_ink.fixtures import generate_synthetic_lossless
from scripts.shared import append_command_log, run_command, write_json


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _canonicalize(text: str) -> str:
    payload = json.loads(text)
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _run_capture(command: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(command, capture_output=True, text=True, cwd=str(cwd) if cwd else None)
    return proc.returncode, proc.stdout, proc.stderr


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact_root")
    args = parser.parse_args()

    root = Path(args.artifact_root)
    root.mkdir(parents=True, exist_ok=True)
    log_path = root / "command_log.txt"

    parity_dir = root / "parity"
    parity_dir.mkdir(parents=True, exist_ok=True)

    strokes = generate_synthetic_lossless(seed=20260226)[:16]
    payload = encode_zpink(strokes, mode="lossless", seed=20260226)
    parity_file = parity_dir / "cross_runtime_input.zpink"
    parity_file.write_bytes(payload)

    py_decoded = decode_zpink(payload)
    py_json = canonical_json(py_decoded)
    py_hash = _sha(py_json)
    expected_json_file = parity_dir / "expected_decoded.json"
    expected_json_file.write_text(py_json, encoding="utf-8")

    wasm_build = run_command(
        [
            "wasm-pack",
            "build",
            str(ROOT / "bindings" / "wasm"),
            "--target",
            "nodejs",
            "--release",
            "--out-dir",
            "pkg",
        ],
        log_path,
        "gate_e_wasm_build",
    )

    node_rc, node_out, node_err = _run_capture(
        ["node", str(ROOT / "scripts" / "wasm_decode_runner.mjs"), str(parity_file)],
    )
    append_command_log(
        log_path,
        "gate_e_node_decode",
        f"node {ROOT / 'scripts' / 'wasm_decode_runner.mjs'}",
        node_rc,
        node_out,
        node_err,
    )

    swift_bin = parity_dir / "swift_decode_bin"
    swift_build_rc, swift_build_out, swift_build_err = _run_capture(
        [
            "swiftc",
            str(ROOT / "bindings" / "swift" / "ZPEInk.swift"),
            str(ROOT / "bindings" / "swift" / "Tests" / "ZPEInkParity.swift"),
            "-o",
            str(swift_bin),
        ]
    )
    append_command_log(
        log_path,
        "gate_e_swift_build",
        f"swiftc {ROOT / 'bindings' / 'swift' / 'ZPEInk.swift'} {ROOT / 'bindings' / 'swift' / 'Tests' / 'ZPEInkParity.swift'} -o <bin>",
        swift_build_rc,
        swift_build_out,
        swift_build_err,
    )
    if swift_build_rc == 0:
        swift_rc, swift_out, swift_err = _run_capture([str(swift_bin), str(parity_file), str(expected_json_file)])
    else:
        swift_rc, swift_out, swift_err = swift_build_rc, "", swift_build_err
    append_command_log(
        log_path,
        "gate_e_swift_decode",
        str(swift_bin),
        swift_rc,
        swift_out,
        swift_err,
    )

    csharp_bin = parity_dir / "csharp_decode.exe"
    csharp_build_rc, csharp_build_out, csharp_build_err = _run_capture(
        [
            "mcs",
            "-out:" + str(csharp_bin),
            str(ROOT / "bindings" / "csharp" / "Tests" / "ZpeInkParity.cs"),
            str(ROOT / "bindings" / "csharp" / "ZpeInk.cs"),
        ]
    )
    append_command_log(
        log_path,
        "gate_e_csharp_build",
        f"mcs -out:{csharp_bin} {ROOT / 'bindings' / 'csharp' / 'Tests' / 'ZpeInkParity.cs'} {ROOT / 'bindings' / 'csharp' / 'ZpeInk.cs'}",
        csharp_build_rc,
        csharp_build_out,
        csharp_build_err,
    )
    if csharp_build_rc == 0:
        csharp_rc, csharp_out, csharp_err = _run_capture(
            ["mono", str(csharp_bin), str(parity_file), str(expected_json_file)]
        )
    else:
        csharp_rc, csharp_out, csharp_err = csharp_build_rc, "", csharp_build_err
    append_command_log(
        log_path,
        "gate_e_csharp_decode",
        f"mono {csharp_bin}",
        csharp_rc,
        csharp_out,
        csharp_err,
    )

    wasm_hash = _sha(_canonicalize(node_out.strip())) if node_rc == 0 else None
    swift_hash = _sha(_canonicalize(swift_out.strip())) if swift_rc == 0 else None
    csharp_hash = _sha(_canonicalize(csharp_out.strip())) if csharp_rc == 0 else None

    parity_pass = (
        node_rc == 0
        and swift_rc == 0
        and csharp_rc == 0
        and wasm_hash == py_hash
        and swift_hash == py_hash
        and csharp_hash == py_hash
    )

    # PyO3 path validation.
    machine = platform.machine().lower()
    if machine in {"x86_64", "amd64"}:
        rust_target = "x86_64-apple-darwin"
    elif machine in {"arm64", "aarch64"}:
        rust_target = "aarch64-apple-darwin"
    else:
        rust_target = ""

    pyo3_cmd = [
        "env",
        "PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1",
        "maturin",
        "build",
        "--release",
        "--interpreter",
        sys.executable,
        "-m",
        str(ROOT / "bindings" / "python_native" / "Cargo.toml"),
        "-o",
        str(parity_dir / "wheels"),
    ]
    if rust_target:
        pyo3_cmd.extend(["--target", rust_target])

    pyo3_result = run_command(
        pyo3_cmd,
        log_path,
        "gate_e_pyo3_build",
    )

    pyo3_import_rc = 1
    pyo3_import_out = ""
    pyo3_import_err = ""
    if pyo3_result["returncode"] == 0:
        wheel_candidates = sorted((parity_dir / "wheels").glob("*.whl"))
        if wheel_candidates:
            with tempfile.TemporaryDirectory() as td:
                venv_path = Path(td) / "venv"
                rc, out, err = _run_capture([sys.executable, "-m", "venv", str(venv_path)])
                append_command_log(log_path, "gate_e_pyo3_venv", f"{sys.executable} -m venv {venv_path}", rc, out, err)
                if rc == 0:
                    pip_path = venv_path / "bin" / "pip"
                    py_path = venv_path / "bin" / "python"
                    rc, out, err = _run_capture([str(pip_path), "install", "--upgrade", "pip"])
                    append_command_log(log_path, "gate_e_pyo3_pip_upgrade", f"{pip_path} install --upgrade pip", rc, out, err)
                    rc, out, err = _run_capture([str(pip_path), "install", str(wheel_candidates[-1])])
                    append_command_log(log_path, "gate_e_pyo3_install", f"{pip_path} install wheel", rc, out, err)
                    if rc == 0:
                        rc, out, err = _run_capture(
                            [
                                str(py_path),
                                "-c",
                                (
                                    "import zpe_ink_native as m;"
                                    "print(m.version());"
                                    "print(m.decode_to_json(open('"
                                    + str(parity_file)
                                    + "','rb').read())[:16])"
                                ),
                            ]
                        )
                        pyo3_import_rc, pyo3_import_out, pyo3_import_err = rc, out, err
    append_command_log(
        log_path,
        "gate_e_pyo3_import",
        "python -c import zpe_ink_native",
        pyo3_import_rc,
        pyo3_import_out,
        pyo3_import_err,
    )

    payload_json = {
        "claim_id": "INK-C006",
        "python_hash": py_hash,
        "wasm_hash": wasm_hash,
        "swift_hash": swift_hash,
        "csharp_hash": csharp_hash,
        "node_decode_returncode": node_rc,
        "swift_decode_returncode": swift_rc,
        "csharp_decode_returncode": csharp_rc,
        "wasm_build_returncode": wasm_build["returncode"],
        "pyo3_build_returncode": pyo3_result["returncode"],
        "pyo3_import_returncode": pyo3_import_rc,
        "pass": parity_pass,
        "artifacts": {
            "parity_input": str(parity_file),
            "node_stdout": str(parity_dir / "node_decoded.json"),
            "swift_stdout": str(parity_dir / "swift_decoded.json"),
            "csharp_stdout": str(parity_dir / "csharp_decoded.json"),
        },
    }

    (parity_dir / "node_decoded.json").write_text(node_out, encoding="utf-8")
    (parity_dir / "swift_decoded.json").write_text(swift_out, encoding="utf-8")
    (parity_dir / "csharp_decoded.json").write_text(csharp_out, encoding="utf-8")
    write_json(root / "ink_cross_runtime_parity.json", payload_json)

    if not parity_pass:
        raise SystemExit("cross-runtime parity failed")

    print("GATE_E_PARITY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
