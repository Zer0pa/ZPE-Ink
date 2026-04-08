from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def _run(command: list[str], *, cwd: Path | None = None, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False, timeout=timeout)


def test_python_iam_example_proxy_mode_runs() -> None:
    result = _run([sys.executable, "examples/python_load_iam.py", "--proxy-demo"], cwd=REPO_ROOT)
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["mode"] == "proxy-demo"
    assert payload["roundtrip_pass"] is True
    assert payload["sample_count"] == 1


def test_swift_pencilkit_example_runs_with_repo_binding(tmp_path: Path) -> None:
    swiftc = shutil.which("swiftc")
    if not swiftc:
        pytest.skip("swiftc is required for the Swift example")

    binary_path = tmp_path / "zpe_ink_swift_demo"
    build = _run(
        [
            swiftc,
            str(REPO_ROOT / "code" / "bindings" / "swift" / "ZPEInk.swift"),
            str(REPO_ROOT / "examples" / "swift_pencilkit.swift"),
            "-o",
            str(binary_path),
        ],
        cwd=REPO_ROOT,
    )
    assert build.returncode == 0, build.stderr

    run = _run([str(binary_path)], cwd=REPO_ROOT)
    assert run.returncode == 0, run.stderr
    payload = json.loads(run.stdout)
    assert payload["status"] == "PASS"
    assert payload["stroke_count"] == 2


def test_wasm_web_demo_build_runs(tmp_path: Path) -> None:
    wasm_pack = shutil.which("wasm-pack")
    cargo = shutil.which("cargo")
    if not wasm_pack or not cargo:
        pytest.skip("wasm-pack and cargo are required for the wasm web demo")

    demo_dir = REPO_ROOT / "examples" / "wasm_web_demo"
    pkg_dir = demo_dir / "pkg"
    if pkg_dir.exists():
        shutil.rmtree(pkg_dir)

    build = _run(["bash", "build.sh"], cwd=demo_dir, timeout=240)
    assert build.returncode == 0, build.stderr
    assert (pkg_dir / "zpe_ink_wasm.js").exists()
    assert (pkg_dir / "zpe_ink_wasm_bg.wasm").exists()

    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = str(sock.getsockname()[1])
    env = os.environ.copy()
    env["PORT"] = port
    server = subprocess.Popen(
        ["bash", "serve.sh"],
        cwd=demo_dir,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        deadline = time.time() + 10.0
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/index.html", timeout=1.0) as response:
                    html = response.read().decode("utf-8")
                    assert "ZPE-Ink WASM Demo" in html
                    break
            except Exception:
                if server.poll() is not None:
                    raise AssertionError("serve.sh exited before serving index.html")
                time.sleep(0.2)
        else:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=5)
            raise AssertionError("serve.sh did not start cleanly within 10 seconds")
    finally:
        if server.poll() is None:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=5)
