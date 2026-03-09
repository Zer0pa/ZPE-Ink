"""ZPE Ink codec package."""

from .codec import ZPInkDecodeError, ZPInkEncodeError, decode_zpink, encode_zpink

__all__ = [
    "ZPInkDecodeError",
    "ZPInkEncodeError",
    "decode_zpink",
    "encode_zpink",
]
