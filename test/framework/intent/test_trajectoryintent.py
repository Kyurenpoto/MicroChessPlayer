# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

import pytest
from dependency_injector import providers
from src.config import Container
from src.converter.responseconverter import TrajectoryResponseToDTO
from src.domain.dto.playerdto import PlayerAIInfo, PlayerAPIInfo, PlayerTrajectoryRequest
from src.entity.movement import FEN, SAN
from src.framework.intent.trajectoryintent import TrajectoryIntent
from src.usecase.trajectory import FakeTrajectoryFactory


@pytest.mark.asyncio
async def test_trajectory_intent(container: Container) -> None:
    container.api_info.override(providers.Factory(PlayerAPIInfo, name="trajectory", method="post"))

    assert (
        await TrajectoryIntent.from_usecase_factory(FakeTrajectoryFactory()).executed(
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
