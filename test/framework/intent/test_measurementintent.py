# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

import pytest
from dependency_injector import providers
from src.config import Container
from src.converter.responseconverter import MeasurementResponseToDTO
from src.domain.dto.playerdto import PlayerAIInfo, PlayerAPIInfo, PlayerMeasurementRequest
from src.framework.intent.measurementintent import MeasurementIntent
from src.usecase.measurement import FakeMeasurementFactory
from src.usecase.responsemodel import MeasurementInfo


@pytest.mark.asyncio
async def test_measurement_intent(container: Container) -> None:
    container.api_info.override(providers.Factory(PlayerAPIInfo, name="measurement", method="post"))

    assert (
        await MeasurementIntent.from_usecase_factory(FakeMeasurementFactory()).executed(
            PlayerMeasurementRequest(
                white=PlayerAIInfo(url="http://test"), black=PlayerAIInfo(url="http://test"), playtime=3
            )
        )
        == MeasurementResponseToDTO(MeasurementInfo(1.5, 1, 1, 1), MeasurementInfo(1.5, 1, 1, 1)).convert()
    )
