# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from typing import List

import pytest
from domain.implementation.trace import IndexableTrace, MappableTrace, SplitableTrace, Trace

STARTING_FEN = "4knbr/4p3/8/7P/4RBNK/8/8/8 w Kk - 0 1"
FIRST_FEN = "4knbr/4p3/7P/8/4RBNK/8/8/8 b Kk - 0 1"
FIRST_SAN = "h5h6"


def test_move() -> None:
    assert MappableTrace.from_fens([STARTING_FEN]).moved(Trace([[FIRST_FEN]], [[FIRST_SAN]], [[0]])) == Trace(
        [[STARTING_FEN, FIRST_FEN]], [[FIRST_SAN]], [[0]]
    )


def test_index() -> None:
    assert IndexableTrace([[STARTING_FEN], [FIRST_FEN]], [[FIRST_SAN], []], [[0], [0]]).indexed([0]) == Trace(
        [[STARTING_FEN]], [[FIRST_SAN]], [[0]]
    )


@pytest.mark.parametrize(
    "color, fen, sanlist",
    [
        ("w", STARTING_FEN, [FIRST_SAN]),
        ("b", FIRST_FEN, []),
    ],
)
def test_color(color: str, fen: str, sanlist: List[str]) -> None:
    assert IndexableTrace([[STARTING_FEN], [FIRST_FEN]], [[FIRST_SAN], []], [[0], [0]]).colored(color) == Trace(
        [[fen]], [sanlist], [[0]]
    )


@pytest.mark.parametrize(
    "target, white, black",
    [
        (
            SplitableTrace([[STARTING_FEN, FIRST_FEN, STARTING_FEN]], [[FIRST_SAN, FIRST_SAN]], [[0, 0]]),
            Trace([[STARTING_FEN, STARTING_FEN]], [[FIRST_SAN]], [[0]]),
            Trace([[FIRST_FEN]], [[FIRST_SAN]], [[0]]),
        ),
        (
            SplitableTrace([[STARTING_FEN, FIRST_FEN]], [[FIRST_SAN]], [[0]]),
            Trace([[STARTING_FEN]], [[FIRST_SAN]], [[0]]),
            Trace([[FIRST_FEN]], [[]], [[]]),
        ),
        (
            SplitableTrace([[STARTING_FEN]], [[]], [[]]),
            Trace([[STARTING_FEN]], [[]], [[]]),
            Trace([[]], [[]], [[]]),
        ),
    ],
)
def test_split_with_color_turn(target: SplitableTrace, white: Trace, black: Trace) -> None:
    assert target.splited_with_color_turn() == (white, black)
