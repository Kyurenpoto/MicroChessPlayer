# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

import pytest
from domain.implementation.movement import FEN, SAN, FakeBlackMovement, FakeWhiteMovement, IMovement
from domain.implementation.status import FakeCheckmateStatus, FakeStalemateStatus, FakeStatus, IStatus
from domain.implementation.trace import (
    IndexableTrace,
    MappableTrace,
    MovableTrace,
    OneStepTrace,
    ProducableTrace,
    SplitableTrace,
    Trace,
)


class TestTrace:
    @pytest.mark.parametrize(
        "color, indice",
        [
            ("w", [0]),
            ("b", [1]),
        ],
    )
    def test_to_color_indice(self, color: str, indice: list[int]) -> None:
        assert Trace.from_FENs([FEN.starting(), FEN.first()]).to_color_indice(color) == indice

    def test_to_not_empty_indice(self) -> None:
        assert Trace([[], [FEN.starting()], []], [[], [], []], [[], [], []]).to_not_empty_indice() == [1]

    def test_SAN_normalized(self) -> None:
        assert Trace(
            [[FEN.starting(), FEN.starting()], [FEN.starting(), FEN.starting()]],
            [[SAN.first(), SAN.first()], [SAN.first()]],
            [[0, 0], [0, 0]],
        ).SAN_normalized() == Trace(
            [[FEN.starting(), FEN.starting()], [FEN.starting(), FEN.starting()]],
            [[SAN.first()], [SAN.first()]],
            [[0, 0], [0, 0]],
        )

    @pytest.mark.parametrize(
        "trace, corrected",
        [
            (
                Trace(
                    [[FEN.starting()], [FEN.first()], [FEN.starting()], [FEN.first()]],
                    [[], [], [], []],
                    [[1], [1], [0.5], [0.5]],
                ),
                Trace(
                    [[FEN.starting()], [FEN.first()], [FEN.starting()], [FEN.first()]],
                    [[], [], [], []],
                    [[1], [1], [0.5], [0.5]],
                ),
            ),
            (
                Trace(
                    [
                        [FEN.starting(), FEN.first()],
                        [FEN.first(), FEN.starting()],
                        [FEN.starting(), FEN.first()],
                        [FEN.first(), FEN.starting()],
                    ],
                    [[SAN.first()], [SAN.first()], [SAN.first()], [SAN.first()]],
                    [[0, 1], [0, 1], [0, 0.5], [0, 0.5]],
                ),
                Trace(
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
                Trace(
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
                Trace(
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
    def test_end_corrected(self, trace: Trace, corrected: Trace) -> None:
        assert trace.end_corrected() == corrected


class TestMappableTrace:
    def test_concatenated(self) -> None:
        assert MappableTrace([[]], [[]], [[]]).concatenated(MappableTrace([[]], [[]], [[]])) == MappableTrace(
            [[], []], [[], []], [[], []]
        )

    def test_inner_concatenated(self) -> None:
        assert MappableTrace._make(Trace.from_FENs([FEN.starting()])).inner_concatenated(
            Trace([[FEN.first()]], [[SAN.first()]], [[0]])
        ) == Trace([[FEN.starting(), FEN.first()]], [[SAN.first()]], [[0]])


class TestIndexableTrace:
    def test_inner_odd_indexed(self) -> None:
        assert IndexableTrace([[FEN.starting(), FEN.first()]], [[SAN.first()]], [[0]]).inner_odd_indexed() == Trace(
            [[FEN.first()]], [[]], [[]]
        )

    def test_inner_even_indexed(self) -> None:
        assert IndexableTrace([[FEN.starting(), FEN.first()]], [[SAN.first()]], [[0]]).inner_even_indexed() == Trace(
            [[FEN.starting()]], [[SAN.first()]], [[0]]
        )


class TestSplitableTrace:
    def test_color_splited(self) -> None:
        SplitableTrace([[FEN.starting()], [FEN.first()]], [[SAN.first()], []], [[0], [0]]).color_splited() == (
            Trace([[FEN.starting()]], [[SAN.first()]], [[0]]),
            Trace([[FEN.first()]], [[]], [[]]),
        )

    def test_inner_parity_splited(self) -> None:
        SplitableTrace([[FEN.starting(), FEN.first()]], [[SAN.first()]], [[0]]).inner_parity_splited() == (
            Trace([[FEN.starting()]], [[SAN.first()]], [[0]]),
            Trace([[FEN.first()]], [[]], [[]]),
        )

    @pytest.mark.parametrize(
        "target, white, black",
        [
            (
                SplitableTrace([[FEN.starting(), FEN.first(), FEN.starting()]], [[SAN.first(), SAN.first()]], [[0, 0]]),
                Trace([[FEN.starting(), FEN.starting()]], [[SAN.first()]], [[0]]),
                Trace([[FEN.first()]], [[]], [[0]]),
            ),
            (
                SplitableTrace([[FEN.starting(), FEN.first()]], [[SAN.first()]], [[0]]),
                Trace([[FEN.starting()]], [[]], [[0]]),
                Trace([[FEN.first()]], [[]], [[]]),
            ),
            (
                SplitableTrace([[FEN.starting()]], [[]], [[]]),
                Trace([[FEN.starting()]], [[]], [[]]),
                Trace([], [], []),
            ),
        ],
    )
    def test_split_with_color_turn(self, target: SplitableTrace, white: Trace, black: Trace) -> None:
        assert target.splited_with_color_turn() == (white, black)

    def test_color_unioned(self) -> None:
        assert SplitableTrace.color_unioned(
            5,
            OneStepTrace(Trace([[FEN.starting()]], [[SAN.first()]], [[0], [0.5]]), [0, 1], [0]),
            OneStepTrace(Trace([[FEN.first()]], [[SAN.first()]], [[0], [0.5]]), [2, 3], [2]),
        ) == SplitableTrace(
            [[FEN.starting()], [], [FEN.first()], [], []],
            [[SAN.first()], [], [SAN.first()], [], []],
            [[0], [0.5], [0], [0.5], []],
        )


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
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "fens, status, white, black",
        [
            (
                [FEN.starting(), FEN.first()],
                FakeStatus(),
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
            (
                [FEN.starting(), FEN.first()],
                FakeCheckmateStatus(),
                Trace([[FEN.starting()]], [[]], [[1]]),
                Trace([[FEN.first()]], [[]], [[1]]),
            ),
            (
                [FEN.starting(), FEN.first()],
                FakeStalemateStatus(),
                Trace([[FEN.starting()]], [[]], [[0.5]]),
                Trace([[FEN.first()]], [[]], [[0.5]]),
            ),
            (
                [FEN.starting(), FEN.first()],
                FakeCheckmateStatus(2),
                Trace([[FEN.starting(), FEN.white_end()], [FEN.starting()]], [[SAN.first()], []], [[0, 1], [0]]),
                Trace([[FEN.first(), FEN.black_end()], [FEN.first()]], [[SAN.first()], []], [[0, 1], [0]]),
            ),
            (
                [FEN.starting(), FEN.first()],
                FakeStalemateStatus(2),
                Trace([[FEN.starting(), FEN.white_end()], [FEN.starting()]], [[SAN.first()], []], [[0, 0.5], [0.5]]),
                Trace([[FEN.first(), FEN.black_end()], [FEN.first()]], [[SAN.first()], []], [[0, 0.5], [0.5]]),
            ),
            (
                [FEN.starting(), FEN.first()],
                FakeCheckmateStatus(4),
                Trace(
                    [[FEN.starting(), FEN.starting()], [FEN.starting(), FEN.white_end()]],
                    [[SAN.first()], [SAN.first()]],
                    [[0, 0], [0, 1]],
                ),
                Trace(
                    [[FEN.first(), FEN.first()], [FEN.first(), FEN.black_end()]],
                    [[SAN.first()], [SAN.first()]],
                    [[0, 0], [0, 1]],
                ),
            ),
            (
                [FEN.starting(), FEN.first()],
                FakeStalemateStatus(4),
                Trace(
                    [[FEN.starting(), FEN.starting()], [FEN.starting(), FEN.white_end()]],
                    [[SAN.first()], [SAN.first()]],
                    [[0, 0.5], [0, 0.5]],
                ),
                Trace(
                    [[FEN.first(), FEN.first()], [FEN.first(), FEN.black_end()]],
                    [[SAN.first()], [SAN.first()]],
                    [[0, 0.5], [0, 0.5]],
                ),
            ),
            (
                [FEN.starting(), FEN.first()],
                FakeCheckmateStatus(6),
                Trace(
                    [[FEN.starting(), FEN.starting(), FEN.white_end()], [FEN.starting(), FEN.starting()]],
                    [[SAN.first(), SAN.first()], [SAN.first()]],
                    [[0, 0, 1], [0, 0]],
                ),
                Trace(
                    [[FEN.first(), FEN.first(), FEN.black_end()], [FEN.first(), FEN.first()]],
                    [[SAN.first(), SAN.first()], [SAN.first()]],
                    [[0, 0, 1], [0, 0]],
                ),
            ),
            (
                [FEN.starting(), FEN.first()],
                FakeStalemateStatus(6),
                Trace(
                    [[FEN.starting(), FEN.starting(), FEN.white_end()], [FEN.starting(), FEN.starting()]],
                    [[SAN.first(), SAN.first()], [SAN.first()]],
                    [[0, 0, 0.5], [0, 0.5]],
                ),
                Trace(
                    [[FEN.first(), FEN.first(), FEN.black_end()], [FEN.first(), FEN.first()]],
                    [[SAN.first(), SAN.first()], [SAN.first()]],
                    [[0, 0, 0.5], [0, 0.5]],
                ),
            ),
        ],
    )
    async def test_produced(self, fens: list[str], status: IStatus, white: Trace, black: Trace) -> None:
        assert await ProducableTrace(3, fens, status, FakeWhiteMovement(), FakeBlackMovement()).produced() == (
            white,
            black,
        )
