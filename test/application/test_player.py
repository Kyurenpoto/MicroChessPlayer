# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

import pytest
from dependency_injector import providers
from src.application.player import GamePlayer, MeasurementPlayer, TrajectoryPlayer
from src.config import Container
from src.converter.responseconverter import GameResponseToDTO, MeasurementResponseToDTO, TrajectoryResponseToDTO
from src.entity.movement import FEN, SAN
from src.framework.dto.playerdto import (
    PlayerAIInfo,
    PlayerAPIInfo,
    PlayerGameRequest,
    PlayerMeasurementRequest,
    PlayerTrajectoryRequest,
)
from src.model.responsemodel import MeasurementInfo
from src.usecase.game import FakeGame
from src.usecase.measurement import FakeMeasurement
from src.usecase.trajectory import FakeTrajectory


@pytest.mark.asyncio
async def test_trajectory_player(container: Container) -> None:
    container.api_info.override(providers.Factory(PlayerAPIInfo, name="trajectory", method="post"))

    assert (
        await TrajectoryPlayer.from_usecase(FakeTrajectory.default()).intent.dispatch(
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
async def test_game_intent(container: Container) -> None:
    container.api_info.override(providers.Factory(PlayerAPIInfo, name="game", method="post"))

    assert (
        await GamePlayer.from_usecase(FakeGame.default()).intent.dispatch(
            PlayerGameRequest(white=PlayerAIInfo(url="http://test"), black=PlayerAIInfo(url="http://test"))
        )
        == GameResponseToDTO([FEN.starting()], [], "1-0").convert()
    )


@pytest.mark.asyncio
async def test_measurement_intent(container: Container) -> None:
    container.api_info.override(providers.Factory(PlayerAPIInfo, name="measurement", method="post"))

    assert (
        await MeasurementPlayer.from_usecase(FakeMeasurement.default()).intent.dispatch(
            PlayerMeasurementRequest(
                white=PlayerAIInfo(url="http://test"), black=PlayerAIInfo(url="http://test"), playtime=3
            )
        )
        == MeasurementResponseToDTO(MeasurementInfo(1.5, 1, 1, 1), MeasurementInfo(1.5, 1, 1, 1)).convert()
    )
