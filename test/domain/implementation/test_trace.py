# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from typing import NamedTuple

import pytest
from domain.implementation.enumerable import Mappable
from domain.implementation.movement import FEN, SAN, FakeBlackMovement, FakeWhiteMovement, IMovement
from domain.implementation.status import FakeCheckmateStatus, FakeStalemateStatus, FakeStatus, IStatus
from domain.implementation.trace import (
    ColoredTrace,
    CorrectableTrace,
    FiniteTraceProducable,
    InfiniteTraceProducable,
    ITraceProducable,
    MovableTrace,
    OneStepTrace,
    ProducableTrace,
    SplitableTrace,
    Trace,
)


class TestCorrectableTrace:
    @pytest.mark.parametrize(
        "trace, corrected",
        [
            (
                CorrectableTrace(
                    [[FEN.starting()], [FEN.first()], [FEN.starting()], [FEN.first()]],
                    [[], [], [], []],
                    [[1], [1], [0.5], [0.5]],
                ),
                CorrectableTrace(
                    [[FEN.starting()], [FEN.first()], [FEN.starting()], [FEN.first()]],
                    [[], [], [], []],
                    [[1], [1], [0.5], [0.5]],
                ),
            ),
            (
                CorrectableTrace(
                    [
                        [FEN.starting(), FEN.first()],
                        [FEN.first(), FEN.starting()],
                        [FEN.starting(), FEN.first()],
                        [FEN.first(), FEN.starting()],
                    ],
                    [[SAN.first()], [SAN.first()], [SAN.first()], [SAN.first()]],
                    [[0, 1], [0, 1], [0, 0.5], [0, 0.5]],
                ),
                CorrectableTrace(
                    [
                        [FEN.starting(), FEN.first(), FEN.white_end()],
                        [FEN.first(), FEN.starting(), FEN.black_end()],
                        [FEN.starting(), FEN.first(), FEN.white_end()],
                        [FEN.first(), FEN.starting(), FEN.black_end()],
                    ],
                    [[SAN.first()], [SAN.first()], [SAN.first()], [SAN.first()]],
                    [[0, 0, 1], [0, 0, 1], [0, 0.5, 0.5], [0, 0.5, 0.5]],
                ),
            ),
            (
                CorrectableTrace(
                    [
                        [FEN.starting(), FEN.first(), FEN.starting()],
                        [FEN.first(), FEN.starting(), FEN.first()],
                        [FEN.starting(), FEN.first(), FEN.starting()],
                        [FEN.first(), FEN.starting(), FEN.first()],
                    ],
                    [
                        [SAN.first(), SAN.first()],
                        [SAN.first(), SAN.first()],
                        [SAN.first(), SAN.first()],
                        [SAN.first(), SAN.first()],
                    ],
                    [[0, 0, 1], [0, 0, 1], [0, 0, 0.5], [0, 0, 0.5]],
                ),
                CorrectableTrace(
                    [
                        [FEN.starting(), FEN.first(), FEN.starting(), FEN.black_end()],
                        [FEN.first(), FEN.starting(), FEN.first(), FEN.white_end()],
                        [FEN.starting(), FEN.first(), FEN.starting(), FEN.black_end()],
                        [FEN.first(), FEN.starting(), FEN.first(), FEN.white_end()],
                    ],
                    [
                        [SAN.first(), SAN.first()],
                        [SAN.first(), SAN.first()],
                        [SAN.first(), SAN.first()],
                        [SAN.first(), SAN.first()],
                    ],
                    [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0.5, 0.5], [0, 0, 0.5, 0.5]],
                ),
            ),
        ],
    )
    def test_end_corrected(self, trace: CorrectableTrace, corrected: CorrectableTrace) -> None:
        assert trace.end_corrected() == corrected


class TestSplitableTrace:
    @pytest.mark.parametrize(
        "target, colored",
        [
            (
                SplitableTrace([[FEN.starting(), FEN.first(), FEN.starting()]], [[SAN.first(), SAN.first()]], [[0, 0]]),
                ColoredTrace(
                    Trace([[FEN.starting(), FEN.starting()]], [[SAN.first()]], [[0]]),
                    Trace([[FEN.first()]], [[]], [[0]]),
                ),
            ),
            (
                SplitableTrace([[FEN.starting(), FEN.first()]], [[SAN.first()]], [[0]]),
                ColoredTrace(
                    Trace([[FEN.starting()]], [[]], [[0]]),
                    Trace([[FEN.first()]], [[]], [[]]),
                ),
            ),
            (
                SplitableTrace([[FEN.starting()]], [[]], [[]]),
                ColoredTrace(
                    Trace([[FEN.starting()]], [[]], [[]]),
                    Trace([], [], []),
                ),
            ),
        ],
    )
    def test_split_with_color_turn(self, target: SplitableTrace, colored: ColoredTrace) -> None:
        assert target.splited_with_color_turn() == colored


class TestMovableTrace:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "fen, movement, next_fen",
        [
            (
                FEN.starting(),
                FakeWhiteMovement(),
                FEN.first(),
            ),
            (
                FEN.first(),
                FakeBlackMovement(),
                FEN.starting(),
            ),
        ],
    )
    async def test_to_move(self, fen: str, movement: IMovement, next_fen: str) -> None:
        assert await MovableTrace.from_FENs([fen]).to_move(FakeStatus(), movement) == (
            Trace([[next_fen]], [[SAN.first()]], [[0]]),
            [0],
        )

    def test_moved(self) -> None:
        assert MovableTrace.from_FENs([FEN.starting(), FEN.starting(), FEN.first(), FEN.first()]).moved(
            OneStepTrace(Trace([[FEN.first()]], [[SAN.first()]], [[0], [0.5]]), [0, 1], [0]),
            OneStepTrace(Trace([[FEN.starting()]], [[SAN.first()]], [[0], [0.5]]), [2, 3], [2]),
        ) == MovableTrace(
            [[FEN.starting(), FEN.first()], [FEN.starting()], [FEN.first(), FEN.starting()], [FEN.first()]],
            [[SAN.first()], [], [SAN.first()], []],
            [[0], [0.5], [0], [0.5]],
        )


class TestProducableTrace:
    class GeneratableParam(NamedTuple):
        rest_prefix: int
        common_white: Trace
        common_black: Trace
        additional_results: list[list[list[float]]]

        def generated(self) -> list[tuple]:
            return [
                (
                    [FEN.starting(), FEN.first()],
                    status_type(self.rest_prefix),
                    ColoredTrace(
                        Trace(self.common_white.fens, self.common_white.sans, self.additional_results[i]),
                        Trace(self.common_black.fens, self.common_black.sans, self.additional_results[i]),
                    ),
                    producable,
                )
                for status_type, i in [(FakeCheckmateStatus, 0), (FakeStalemateStatus, 1)]
                for producable in [FiniteTraceProducable(3), InfiniteTraceProducable()]
            ]

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "fens, status, colored, producable",
        [
            (
                [FEN.starting(), FEN.first()],
                FakeStatus(),
                ColoredTrace(
                    Trace(
                        [[FEN.starting(), FEN.starting()], [FEN.starting(), FEN.starting()]],
                        [[SAN.first()], [SAN.first()]],
                        [[0, 0], [0, 0]],
                    ),
                    Trace(
                        [[FEN.first(), FEN.first()], [FEN.first(), FEN.first()]],
                        [[SAN.first()], [SAN.first()]],
                        [[0, 0], [0, 0]],
                    ),
                ),
                FiniteTraceProducable(3),
            ),
        ]
        + Mappable.concatenated(
            Mappable(
                [
                    GeneratableParam(
                        0, Trace([[FEN.starting()]], [[]], []), Trace([[FEN.first()]], [[]], []), [[[1]], [[0.5]]]
                    ),
                    GeneratableParam(
                        2,
                        Trace([[FEN.starting(), FEN.white_end()], [FEN.starting()]], [[SAN.first()], []], []),
                        Trace([[FEN.first(), FEN.black_end()], [FEN.first()]], [[SAN.first()], []], []),
                        [[[0, 1], [0]], [[0, 0.5], [0.5]]],
                    ),
                    GeneratableParam(
                        4,
                        Trace(
                            [[FEN.starting(), FEN.starting()], [FEN.starting(), FEN.white_end()]],
                            [[SAN.first()], [SAN.first()]],
                            [],
                        ),
                        Trace(
                            [[FEN.first(), FEN.first()], [FEN.first(), FEN.black_end()]],
                            [[SAN.first()], [SAN.first()]],
                            [],
                        ),
                        [[[0, 0], [0, 1]], [[0, 0.5], [0, 0.5]]],
                    ),
                    GeneratableParam(
                        6,
                        Trace(
                            [[FEN.starting(), FEN.starting(), FEN.white_end()], [FEN.starting(), FEN.starting()]],
                            [[SAN.first(), SAN.first()], [SAN.first()]],
                            [],
                        ),
                        Trace(
                            [[FEN.first(), FEN.first(), FEN.black_end()], [FEN.first(), FEN.first()]],
                            [[SAN.first(), SAN.first()], [SAN.first()]],
                            [],
                        ),
                        [[[0, 0, 1], [0, 0]], [[0, 0, 0.5], [0, 0.5]]],
                    ),
                ]
            ).mapped(lambda x: x.generated()),
        ),
    )
    async def test_produced(
        self, fens: list[str], status: IStatus, colored: ColoredTrace, producable: ITraceProducable
    ) -> None:
        assert (
            await ProducableTrace(status, FakeWhiteMovement(), FakeBlackMovement(), producable).produced_with_spliting(
                fens
            )
            == colored
        )
