from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .primitivetoken import Point, encode_stroke_to_tokens, stroke_to_points

TOKEN_MAP = {
    0: "N",
    1: "NE",
    2: "E",
    3: "SE",
    4: "S",
    5: "SW",
    6: "W",
    7: "NW",
}


def _coerce_stroke(stroke: list[Point] | dict[str, list[int]]) -> list[Point]:
    if isinstance(stroke, dict):
        return stroke_to_points(stroke)
    return list(stroke)


class InkTokenizer:
    VOCAB_VERSION = 1
    VOCAB_SIZE = 8

    def __init__(self) -> None:
        self.token_map = TOKEN_MAP.copy()

    def encode_stroke(self, stroke: list[Point] | dict[str, list[int]]) -> list[int]:
        points = _coerce_stroke(stroke)
        tokens, _, _, _ = encode_stroke_to_tokens(points)
        return tokens

    def encode_corpus(self, strokes_list: Iterable[list[Point] | dict[str, list[int]]]) -> list[list[int]]:
        return [self.encode_stroke(stroke) for stroke in strokes_list]

    def token_distribution(self, encoded_corpus: Iterable[list[int]]) -> dict[str, int]:
        counts = {str(token_id): 0 for token_id in self.token_map}
        for encoded_stroke in encoded_corpus:
            for token in encoded_stroke:
                if token >= 0:
                    counts[str(token)] += 1
        return counts

    def vocab_payload(self) -> dict[str, object]:
        return {
            "version": self.VOCAB_VERSION,
            "directions": self.VOCAB_SIZE,
            "token_map": self.token_map,
            "schema": "zpeink-tokenizer-v1",
        }

    def save_vocab(self, path: str) -> None:
        output_path = Path(path)
        output_path.write_text(json.dumps(self.vocab_payload(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
