# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

import pytest

from domain.dto.playerdto import (
    PlayerAIInfo,
    PlayerAIMeasurement,
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerLink,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from domain.implementation.movement import FEN, SAN
from domain.player import FakeService, MicroChessPlayer


@pytest.mark.asyncio
async def test_trajectory() -> None:
    assert await MicroChessPlayer("http://test", {"trajectory": ""}, FakeService()).trajectory(
        PlayerTrajectoryRequest(
            fens=[FEN.starting(), FEN.first()],
            white=PlayerAIInfo(url="http://test"),
            black=PlayerAIInfo(url="http://test"),
            step=3,
        ),
        "test",
    ) == PlayerTrajectoryResponse(
        fens=(([[FEN.starting()] * 2] * 2) + ([[FEN.first()] * 2] * 2)),
        sans=[[SAN.first()]] * 4,
        results=[[0, 0]] * 4,
        links=[PlayerLink(rel="self", href="http://test"), PlayerLink(rel="trajectory", href="http://test")],
    )


@pytest.mark.asyncio
async def test_game() -> None:
    assert await MicroChessPlayer("http://test", {"game": ""}, FakeService()).game(
        PlayerGameRequest(white=PlayerAIInfo(url="http://test"), black=PlayerAIInfo(url="http://test")), "test"
    ) == PlayerGameResponse(
        fens=[FEN.starting()],
        sans=[],
        result="1-0",
        links=[PlayerLink(rel="self", href="http://test"), PlayerLink(rel="game", href="http://test")],
    )


@pytest.mark.asyncio
async def test_measurement() -> None:
    assert await MicroChessPlayer("http://test", {"measurement": ""}, FakeService()).measurement(
        PlayerMeasurementRequest(
            white=PlayerAIInfo(url="http://test"), black=PlayerAIInfo(url="http://test"), playtime=3
        ),
        "test",
    ) == PlayerMeasurementResponse(
        white=PlayerAIMeasurement(score=1.5, win=1, draw=1, lose=1),
        black=PlayerAIMeasurement(score=1.5, win=1, draw=1, lose=1),
        links=[PlayerLink(rel="self", href="http://test"), PlayerLink(rel="measurement", href="http://test")],
    )
