from __future__ import annotations

from zpe_ink.unipen import load_uji_pen_characters, parse_unipen_like_file


def test_parse_unipen_like_file_preserves_multistroke_segments(tmp_path) -> None:
    sample = tmp_path / "UJIpenchars-w99"
    sample.write_text(
        "\n".join(
            [
                '.SEGMENT CHARACTER 0 ? "a"',
                ".PEN_DOWN",
                "10 20",
                "15 25",
                ".PEN_UP",
                ".PEN_DOWN",
                "30 40",
                "35 45",
                ".PEN_UP",
                ".DT 100",
                '.SEGMENT CHARACTER 1 ? "7"',
                ".PEN_DOWN",
                "50 60",
                "55 65",
                ".PEN_UP",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    parsed = parse_unipen_like_file(sample)

    assert len(parsed) == 2
    assert parsed[0]["label"] == "a"
    assert len(parsed[0]["strokes"]) == 2
    assert parsed[0]["strokes"][0]["x"] == [10, 15]
    assert parsed[0]["strokes"][1]["y"] == [40, 45]
    assert parsed[1]["label"] == "7"
    assert len(parsed[1]["strokes"]) == 1


def test_load_uji_pen_characters_respects_limit(tmp_path) -> None:
    for index in range(2):
        sample = tmp_path / f"UJIpenchars-w{index + 1:02d}"
        sample.write_text(
            "\n".join(
                [
                    f'.SEGMENT CHARACTER {index} ? "x"',
                    ".PEN_DOWN",
                    "0 0",
                    "1 1",
                    ".PEN_UP",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

    loaded = load_uji_pen_characters(tmp_path, limit=1)

    assert len(loaded) == 1
    assert loaded[0][0]["x"] == [0, 1]
