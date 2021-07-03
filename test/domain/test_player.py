# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

import pytest
from dependency_injector import providers
from src.config import Container
from src.converter.responseconverter import GameResponseToDTO, MeasurementResponseToDTO, TrajectoryResponseToDTO
from src.domain.dto.playerdto import (
    PlayerAIInfo,
    PlayerAPIInfo,
    PlayerGameRequest,
    PlayerMeasurementRequest,
    PlayerTrajectoryRequest,
)
from src.domain.implementation.movement import FEN, SAN
from src.domain.player import FakeService, MicroChessPlayer
from src.usecase.responsemodel import MeasurementInfo


@pytest.mark.asyncio
async def test_trajectory(container: Container) -> None:
    container.api_info.override(providers.Factory(PlayerAPIInfo, name="trajectory", method="post"))

    assert (
        await MicroChessPlayer(FakeService()).trajectory(
            PlayerTrajectoryRequest(
                fens=[FEN.starting(), FEN.first()],
                white=PlayerAIInfo(url="http://test"),
                black=PlayerAIInfo(url="http://test"),
                step=3,
            )
        )
        == TrajectoryResponseToDTO(
            (([[FEN.starting()] * 2] * 2) + ([[FEN.first()] * 2] * 2)), [[SAN.first()]] * 4, [[0, 0]] * 4
        ).convert()
    )


@pytest.mark.asyncio
async def test_game(container: Container) -> None:
    container.api_info.override(providers.Factory(PlayerAPIInfo, name="game", method="post"))

    assert (
        await MicroChessPlayer(FakeService()).game(
            PlayerGameRequest(white=PlayerAIInfo(url="http://test"), black=PlayerAIInfo(url="http://test"))
        )
        == GameResponseToDTO([FEN.starting()], [], "1-0").convert()
    )


@pytest.mark.asyncio
async def test_measurement(container: Container) -> None:
    container.api_info.override(providers.Factory(PlayerAPIInfo, name="measurement", method="post"))

    assert (
        await MicroChessPlayer(FakeService()).measurement(
            PlayerMeasurementRequest(
                white=PlayerAIInfo(url="http://test"), black=PlayerAIInfo(url="http://test"), playtime=3
            )
        )
        == MeasurementResponseToDTO(MeasurementInfo(1.5, 1, 1, 1), MeasurementInfo(1.5, 1, 1, 1)).convert()
    )
