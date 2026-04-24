"""ZPE Ink codec package."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import tomllib

from .codec import ZPInkDecodeError, ZPInkEncodeError, decode_zpink, encode_zpink
from .cli import demo_payload, roundtrip_check
from .token_sidecar import build_token_sidecar, build_token_sidecar_from_zpink, reconstruct_token_sidecar


def _fallback_version() -> str:
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    with pyproject_path.open("rb") as handle:
        payload = tomllib.load(handle)
    return payload["project"]["version"]


try:
    __version__ = version("zpe-ink")
except PackageNotFoundError:
    __version__ = _fallback_version()


__all__ = [
    "ZPInkDecodeError",
    "ZPInkEncodeError",
    "__version__",
    "build_token_sidecar",
    "build_token_sidecar_from_zpink",
    "decode_zpink",
    "demo_payload",
    "encode_zpink",
    "reconstruct_token_sidecar",
    "roundtrip_check",
]
