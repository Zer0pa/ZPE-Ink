from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from zpe_ink.codec import canonical_json, decode_zpink, encode_zpink
from zpe_ink.fixtures import generate_synthetic_lossless

REPO_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = REPO_ROOT / "code"


def _run(command: list[str], *, timeout: int = 45) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False, timeout=timeout)


def _build_fixture(tmp_path: Path) -> tuple[Path, Path, str]:
    strokes = generate_synthetic_lossless(seed=20260406)[:16]
    payload = encode_zpink(strokes, mode="lossless", seed=20260406)
    expected = canonical_json(decode_zpink(payload))
    payload_path = tmp_path / "swift_fixture.zpink"
    expected_path = tmp_path / "swift_expected.json"
    payload_path.write_bytes(payload)
    expected_path.write_text(expected, encoding="utf-8")
    return payload_path, expected_path, expected


def test_swift_binding_canonical_json_roundtrip(tmp_path: Path) -> None:
    swiftc = shutil.which("swiftc")
    if not swiftc:
        pytest.skip("swiftc is required for Swift binding verification")

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
