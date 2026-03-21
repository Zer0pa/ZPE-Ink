from __future__ import annotations

import json

from zpe_ink.primitivetoken import Point
from zpe_ink.tokenizer import InkTokenizer


def test_vocab_is_stable() -> None:
    tokenizer = InkTokenizer()
    assert tokenizer.VOCAB_SIZE == 8
    assert tokenizer.token_map[0] == "N"
    assert tokenizer.token_map[7] == "NW"


def test_encode_corpus_is_deterministic() -> None:
    tokenizer = InkTokenizer()
    strokes = [
        [Point(0, 0), Point(0, -1), Point(1, -2)],
        [Point(1, 1), Point(2, 1), Point(3, 1)],
    ]
    first = tokenizer.encode_corpus(strokes)
    second = tokenizer.encode_corpus(strokes)
    assert first == second
    assert first == [[0, 1], [2, 2]]


def test_token_distribution_counts_only_direction_tokens() -> None:
    tokenizer = InkTokenizer()
    distribution = tokenizer.token_distribution([[0, 1, 2], [2, 2, 7], [-1, 4]])
    assert distribution["2"] == 3
    assert distribution["7"] == 1
    assert distribution["0"] == 1


def test_save_vocab(tmp_path) -> None:
    tokenizer = InkTokenizer()
    path = tmp_path / "vocab.json"
    tokenizer.save_vocab(str(path))
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema"] == "zpeink-tokenizer-v1"
    assert payload["directions"] == 8
