from __future__ import annotations

import json
from pathlib import Path
import tomllib

from zpe_ink import __version__
from zpe_ink.cli import demo_payload, main, roundtrip_check


def test_demo_payload_shape() -> None:
    payload = demo_payload()
    assert payload["mode"] == "lossless"
    assert payload["seed"] == 20260220
    assert payload["stroke_count"] == 3
    assert payload["encoded_bytes"] > 0


def test_roundtrip_check_passes() -> None:
    assert roundtrip_check() is True


def test_main_demo(capsys) -> None:
    assert main(["demo"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["mode"] == "lossless"


def test_main_verify_roundtrip(capsys) -> None:
    assert main(["verify-roundtrip"]) == 0
    assert capsys.readouterr().out.strip() == "roundtrip_ok"


def test_package_version_matches_pyproject() -> None:
    with (Path(__file__).resolve().parents[1] / "pyproject.toml").open("rb") as handle:
        payload = tomllib.load(handle)
    assert __version__ == payload["project"]["version"]
