# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

import pytest
from src.domain.dto.playerdto import (
    PlayerAIInfo,
    PlayerAIMeasurement,
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerHAL,
    PlayerInternalModel,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from src.domain.implementation.movement import FEN, SAN
from src.domain.player import FakeService, MicroChessPlayer


@pytest.mark.asyncio
async def test_trajectory() -> None:
    assert await MicroChessPlayer(FakeService()).trajectory(
        PlayerTrajectoryRequest(
            fens=[FEN.starting(), FEN.first()],
            white=PlayerAIInfo(url="http://test"),
            black=PlayerAIInfo(url="http://test"),
            step=3,
        ),
        PlayerInternalModel(url_env="http://test", routes={"trajectory": ""}),
        "trajectory",
        "post",
    ) == PlayerTrajectoryResponse(
        links=PlayerHAL.from_apis_with_requested({"trajectory": ""}, "trajectory", "post").links,
        fens=(([[FEN.starting()] * 2] * 2) + ([[FEN.first()] * 2] * 2)),
        sans=[[SAN.first()]] * 4,
        results=[[0, 0]] * 4,
    )


@pytest.mark.asyncio
async def test_game() -> None:
    assert await MicroChessPlayer(FakeService()).game(
        PlayerGameRequest(white=PlayerAIInfo(url="http://test"), black=PlayerAIInfo(url="http://test")),
        PlayerInternalModel(url_env="http://test", routes={"game": ""}),
        "game",
        "post",
    ) == PlayerGameResponse(
        links=PlayerHAL.from_apis_with_requested({"game": ""}, "game", "post").links,
        fens=[FEN.starting()],
        sans=[],
        result="1-0",
    )


@pytest.mark.asyncio
async def test_measurement() -> None:
    assert await MicroChessPlayer(FakeService()).measurement(
        PlayerMeasurementRequest(
            white=PlayerAIInfo(url="http://test"), black=PlayerAIInfo(url="http://test"), playtime=3
        ),
        PlayerInternalModel(url_env="http://test", routes={"measurement": ""}),
        "measurement",
        "post",
    ) == PlayerMeasurementResponse(
        links=PlayerHAL.from_apis_with_requested({"measurement": ""}, "measurement", "post").links,
        white=PlayerAIMeasurement(score=1.5, win=1, draw=1, lose=1),
        black=PlayerAIMeasurement(score=1.5, win=1, draw=1, lose=1),
    )
