from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_command_log(log_path: Path, label: str, command: str, rc: int, stdout: str, stderr: str) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"[{ts()}] {label}\n")
        handle.write(f"CMD: {command}\n")
        handle.write(f"RC: {rc}\n")
        if stdout:
            handle.write("STDOUT:\n")
            handle.write(stdout.rstrip("\n") + "\n")
        if stderr:
            handle.write("STDERR:\n")
            handle.write(stderr.rstrip("\n") + "\n")
        handle.write("---\n")


def run_command(command: list[str], log_path: Path, label: str) -> dict[str, Any]:
    proc = subprocess.run(command, capture_output=True, text=True)
    append_command_log(
        log_path,
        label=label,
        command=" ".join(command),
        rc=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)
        if not text.endswith("\n"):
            handle.write("\n")


def resolve_net_new_pack_inputs(repo_root: Path) -> list[Path]:
    """Resolve the external NET-NEW pack without hardcoding one machine path."""

    pack_names = [
        "ZPE 10-Lane NET-NEW Resource Maximization Pack.md",
        "ZPE 10-Lane NET-NEW Resource Maximization Pack.pdf",
    ]
    search_roots: list[Path] = []
    env_root = os.environ.get("ZPE_NET_NEW_PACK_ROOT")
    if env_root:
        search_roots.append(Path(env_root).expanduser())

    search_roots.extend([repo_root, *list(repo_root.parents[:3])])

    seen: set[Path] = set()
    for base in search_roots:
        base = base.resolve()
        if base in seen:
            continue
        seen.add(base)
        candidates = [base / name for name in pack_names]
        if all(candidate.exists() for candidate in candidates):
            return candidates

    fallback_root = search_roots[0] if search_roots else repo_root
    return [fallback_root / name for name in pack_names]
