from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any

from .codec import FLAG_AZIMUTH, FLAG_PRESSURE, FLAG_TILT, HEADER_STRUCT, MAGIC, VERSION


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _expect_contains(path: Path, needle: str, label: str) -> dict[str, Any]:
    haystack = _read_text(path)
    passed = needle in haystack
    return {
        "id": label,
        "path": str(path),
        "status": "PASS" if passed else "FAIL",
        "needle": needle,
    }


def _load_pyproject_version(repo_root: Path) -> str:
    payload = _load_toml(repo_root / "code" / "pyproject.toml")
    return payload["project"]["version"]


def verify_repo_binding_contracts(repo_root: Path) -> dict[str, Any]:
    root = repo_root.resolve()
    vector_path = root / "docs" / "family" / "ZPINK_COMPATIBILITY_VECTOR.json"
    vector = json.loads(vector_path.read_text(encoding="utf-8"))
    package_version = _load_pyproject_version(root)
    python_native_cargo_path = root / "code" / "bindings" / "python_native" / "Cargo.toml"
    python_native_cargo = _load_toml(python_native_cargo_path)
    pyo3_features = python_native_cargo["dependencies"]["pyo3"]["features"]

    checks = [
        {
            "id": "python_magic",
            "path": str(root / "code" / "zpe_ink" / "codec.py"),
            "status": "PASS" if MAGIC.decode("ascii") == vector["header"]["magic"] else "FAIL",
            "expected": vector["header"]["magic"],
            "observed": MAGIC.decode("ascii"),
        },
        {
            "id": "python_version",
            "path": str(root / "code" / "zpe_ink" / "codec.py"),
            "status": "PASS" if VERSION == vector["header"]["version"] else "FAIL",
            "expected": vector["header"]["version"],
            "observed": VERSION,
        },
        {
            "id": "python_header_bytes",
            "path": str(root / "code" / "zpe_ink" / "codec.py"),
            "status": "PASS" if HEADER_STRUCT.size == vector["header"]["header_bytes"] else "FAIL",
            "expected": vector["header"]["header_bytes"],
            "observed": HEADER_STRUCT.size,
        },
        {
            "id": "python_flags",
            "path": str(root / "code" / "zpe_ink" / "codec.py"),
            "status": "PASS"
            if {
                "pressure": FLAG_PRESSURE,
                "tilt": FLAG_TILT,
                "azimuth": FLAG_AZIMUTH,
            }
            == vector["flags"]
            else "FAIL",
            "expected": vector["flags"],
            "observed": {
                "pressure": FLAG_PRESSURE,
                "tilt": FLAG_TILT,
                "azimuth": FLAG_AZIMUTH,
            },
        },
        {
            "id": "package_version",
            "path": str(root / "code" / "pyproject.toml"),
            "status": "PASS" if package_version == vector["package_version"] else "FAIL",
            "expected": vector["package_version"],
            "observed": package_version,
        },
        {
            "id": "python_native_abi3_baseline",
            "path": str(python_native_cargo_path),
            "status": "PASS" if "abi3-py311" in pyo3_features else "FAIL",
            "expected": "abi3-py311",
            "observed": sorted(pyo3_features),
        },
        {
            "id": "python_native_extension_module",
            "path": str(python_native_cargo_path),
            "status": "PASS" if "extension-module" in pyo3_features else "FAIL",
            "expected": "extension-module",
            "observed": sorted(pyo3_features),
        },
        _expect_contains(root / "code" / "bindings" / "python_native" / "src" / "lib.rs", 'b"ZPINK"', "python_native_magic"),
        _expect_contains(root / "code" / "bindings" / "python_native" / "src" / "lib.rs", f'"{package_version}"', "python_native_version"),
        _expect_contains(root / "code" / "bindings" / "python_native" / "src" / "lib.rs", "input.len() < 22", "python_native_header_bytes"),
        _expect_contains(root / "code" / "bindings" / "wasm" / "src" / "lib.rs", 'b"ZPINK"', "wasm_magic"),
        _expect_contains(root / "code" / "bindings" / "wasm" / "src" / "lib.rs", f"const VERSION: u8 = {VERSION};", "wasm_version"),
        _expect_contains(root / "code" / "bindings" / "wasm" / "src" / "lib.rs", "input.len() < 22", "wasm_header_bytes"),
        _expect_contains(root / "code" / "bindings" / "swift" / "ZPEInk.swift", '"ZPINK"', "swift_magic"),
        _expect_contains(root / "code" / "bindings" / "swift" / "ZPEInk.swift", f'"{package_version}"', "swift_version"),
        _expect_contains(root / "code" / "bindings" / "swift" / "ZPEInk.swift", "bytes.count >= 22", "swift_header_bytes"),
        _expect_contains(root / "code" / "bindings" / "csharp" / "ZpeInk.cs", "'Z'", "csharp_magic"),
        _expect_contains(root / "code" / "bindings" / "csharp" / "ZpeInk.cs", f'"{package_version}"', "csharp_version"),
        _expect_contains(root / "code" / "bindings" / "csharp" / "ZpeInk.cs", "bytes.Length < 22", "csharp_header_bytes"),
    ]

    failures = [check for check in checks if check["status"] != "PASS"]
    return {
        "status": "PASS" if not failures else "FAIL",
        "repo_root": str(root),
        "vector_path": str(vector_path),
        "contract_version": vector["contract_version"],
        "package_version": package_version,
        "checks": checks,
        "failure_count": len(failures),
    }
