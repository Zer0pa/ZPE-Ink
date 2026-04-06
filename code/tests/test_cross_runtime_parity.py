from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from zpe_ink.codec import canonical_json, decode_zpink, encode_zpink
from zpe_ink.fixtures import generate_synthetic_lossless

REPO_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = REPO_ROOT / "code"


def _canonicalize(text: str) -> str:
    return json.dumps(json.loads(text), sort_keys=True, separators=(",", ":"))


def _run(command: list[str], *, timeout: int = 45) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False, timeout=timeout)


def _build_fixture(tmp_path: Path) -> tuple[Path, Path, str]:
    strokes = generate_synthetic_lossless(seed=20260406)[:16]
    payload = encode_zpink(strokes, mode="lossless", seed=20260406)
    expected = canonical_json(decode_zpink(payload))
    payload_path = tmp_path / "cross_runtime_input.zpink"
    expected_path = tmp_path / "expected_decoded.json"
    payload_path.write_bytes(payload)
    expected_path.write_text(expected, encoding="utf-8")
    return payload_path, expected_path, expected


def test_cross_runtime_parity_python_swift_csharp(tmp_path: Path) -> None:
    swiftc = shutil.which("swiftc")
    mcs = shutil.which("mcs")
    mono = shutil.which("mono")
    if not swiftc or not mcs or not mono:
        pytest.skip("swiftc, mcs, and mono are required for cross-runtime parity")

    payload_path, expected_path, expected = _build_fixture(tmp_path)

    swift_bin = tmp_path / "swift_decode_bin"
    swift_build = _run(
        [
            swiftc,
            str(CODE_ROOT / "bindings" / "swift" / "ZPEInk.swift"),
            str(CODE_ROOT / "bindings" / "swift" / "Tests" / "ZPEInkParity.swift"),
            "-o",
            str(swift_bin),
        ]
    )
    assert swift_build.returncode == 0, swift_build.stderr

    swift_run = _run([str(swift_bin), str(payload_path), str(expected_path)])
    assert swift_run.returncode == 0, swift_run.stderr
    assert swift_run.stdout == expected

    csharp_bin = tmp_path / "csharp_decode.exe"
    csharp_build = _run(
        [
            mcs,
            "-out:" + str(csharp_bin),
            str(CODE_ROOT / "bindings" / "csharp" / "Tests" / "ZpeInkParity.cs"),
            str(CODE_ROOT / "bindings" / "csharp" / "ZpeInk.cs"),
        ]
    )
    assert csharp_build.returncode == 0, csharp_build.stderr

    csharp_run = _run([mono, str(csharp_bin), str(payload_path), str(expected_path)])
    assert csharp_run.returncode == 0, csharp_run.stderr
    assert csharp_run.stdout == expected


def test_cross_runtime_parity_wasm(tmp_path: Path) -> None:
    wasm_pack = shutil.which("wasm-pack")
    node = shutil.which("node")
    if not wasm_pack or not node:
        pytest.skip("wasm-pack and node are required for wasm parity")

    payload_path, _, expected = _build_fixture(tmp_path)
    build = _run(
        [
            wasm_pack,
            "build",
            str(CODE_ROOT / "bindings" / "wasm"),
            "--target",
            "nodejs",
            "--release",
            "--out-dir",
            "pkg",
        ]
    )
    assert build.returncode == 0, build.stderr

    node_run = _run([node, str(CODE_ROOT / "scripts" / "wasm_decode_runner.mjs"), str(payload_path)])
    assert node_run.returncode == 0, node_run.stderr
    assert _canonicalize(node_run.stdout) == expected
