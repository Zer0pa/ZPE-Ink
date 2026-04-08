from __future__ import annotations

import subprocess
import sys
import venv
from pathlib import Path


def _run(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise AssertionError(
            "command failed",
            {
                "command": command,
                "cwd": str(cwd) if cwd is not None else None,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        )
    return result


def test_clean_install_from_built_wheel(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)

    _run(
        [
            sys.executable,
            "-m",
            "build",
            "--wheel",
            "--no-isolation",
            "--outdir",
            str(dist_dir),
            str(repo_root / "code"),
        ],
        cwd=repo_root,
    )

    wheels = sorted(dist_dir.glob("zpe_ink-*.whl"))
    assert len(wheels) == 1

    clean_env_dir = tmp_path / "clean-venv"
    venv.EnvBuilder(with_pip=True, clear=True).create(clean_env_dir)
    python_bin = clean_env_dir / ("Scripts" if sys.platform == "win32" else "bin") / "python"

    _run(
        [
            str(python_bin),
            "-m",
            "pip",
            "install",
            "--no-index",
            "--no-deps",
            str(wheels[0]),
        ]
    )

    smoke = _run([str(python_bin), "-m", "zpe_ink", "verify-roundtrip"])
    assert smoke.stdout.strip() == "roundtrip_ok"
