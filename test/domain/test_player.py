# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

import pytest

from domain.dto.playerdto import (
    PlayerAIInfo,
    PlayerAIMeasurement,
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from domain.implementation.movement import FEN, SAN
from domain.player import FakeService, MicroChessPlayer


@pytest.mark.asyncio
async def test_trajectory() -> None:
    assert await MicroChessPlayer("http://test", FakeService()).trajectory(
        PlayerTrajectoryRequest(
            fens=[FEN.starting(), FEN.first()],
            white=PlayerAIInfo(url="http://test"),
            black=PlayerAIInfo(url="http://test"),
            step=3,
        )
    ) == PlayerTrajectoryResponse(
        fens=(([[FEN.starting()] * 2] * 2) + ([[FEN.first()] * 2] * 2)), sans=[[SAN.first()]] * 4, results=[[0, 0]] * 4
    )


@pytest.mark.asyncio
async def test_game() -> None:
    assert await MicroChessPlayer("http://test", FakeService()).game(
        PlayerGameRequest(white=PlayerAIInfo(url="http://test"), black=PlayerAIInfo(url="http://test"))
    ) == PlayerGameResponse(fens=[FEN.starting()], sans=[], result="1-0")


@pytest.mark.asyncio
async def test_measurement() -> None:
    assert await MicroChessPlayer("http://test", FakeService()).measurement(
        PlayerMeasurementRequest(
            white=PlayerAIInfo(url="http://test"), black=PlayerAIInfo(url="http://test"), playtime=3
        )
    ) == PlayerMeasurementResponse(
        white=PlayerAIMeasurement(score=1.5, win=1, draw=1, lose=1),
        black=PlayerAIMeasurement(score=1.5, win=1, draw=1, lose=1),
    )
