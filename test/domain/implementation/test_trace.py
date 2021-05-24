# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from typing import List

import pytest
from domain.implementation.trace import ColoredTrace, IndexedTrace, SplitedTrace, Trace

STARTING_FEN = "4knbr/4p3/8/7P/4RBNK/8/8/8 w Kk - 0 1"
FIRST_FEN = "4knbr/4p3/7P/8/4RBNK/8/8/8 b Kk - 0 1"
FIRST_SAN = "h5h6"


def test_move() -> None:
    assert Trace.from_fens([STARTING_FEN]).moved(Trace([[FIRST_FEN]], [[FIRST_SAN]], [[0]])) == Trace(
        [[STARTING_FEN, FIRST_FEN]], [[FIRST_SAN]], [[0]]
    )


def test_index() -> None:
    fens, sans, results = IndexedTrace(Trace([[STARTING_FEN], [FIRST_FEN]], [[FIRST_SAN]], [[0], [0]]), [0]).value()

    assert fens == [[STARTING_FEN]]
    assert sans == [[FIRST_SAN]]
    assert results == [[0]]


@pytest.mark.parametrize("color, fen, sanlist", [("w", STARTING_FEN, [FIRST_SAN]), ("b", FIRST_FEN, [])])
def test_color(color: str, fen: str, sanlist: List[str]) -> None:
    fens, sans, results = ColoredTrace(Trace([[STARTING_FEN], [FIRST_FEN]], [[FIRST_SAN]], [[0], [0]]), color).value()

    assert fens == [[fen]]
    assert sans == [sanlist]
    assert results == [[0]]


def test_split() -> None:
    white, black = SplitedTrace(
        Trace([[STARTING_FEN, FIRST_FEN, STARTING_FEN]], [[FIRST_SAN, FIRST_SAN]], [[0, 0, 0]])
    ).value()
    fens_white, sans_white, results_white = white
    fens_black, sans_black, results_black = black

    assert fens_white == [[STARTING_FEN, STARTING_FEN]]
    assert sans_white == [[FIRST_SAN]]
    assert results_white == [[0, 0]]

    assert fens_black == [[FIRST_FEN]]
    assert sans_black == [[FIRST_SAN]]
    assert results_black == [[0]]
