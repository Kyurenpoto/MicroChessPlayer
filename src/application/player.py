# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import NamedTuple

from dependency_injector import providers
from src.config import container
from src.framework.dto.playerdto import (
    PlayerAPIInfo,
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerHTTPStatusErrorResponse,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerRequestErrorResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from src.framework.intent.gameintent import GameIntent
from src.framework.intent.measurementintent import MeasurementIntent
from src.framework.intent.trajectoryintent import TrajectoryIntent
from src.usecase.game import NormalGameFactory
from src.usecase.measurement import NormalMeasurementFactory
from src.usecase.trajectory import NormalTrajectoryFactory
from submodules.fastapi_haljson.src.halconverter import ResponseToJSONBody
from submodules.fastapi_haljson.src.halresponse import HALJSONResponse


class Player(NamedTuple):
    response_converter: ResponseToJSONBody

    @classmethod
    def from_type_map(
        cls,
        ok_responsable: list[str] = [
            PlayerTrajectoryResponse.__name__,
            PlayerGameResponse.__name__,
            PlayerMeasurementResponse.__name__,
        ],
        not_found_responsable: list[str] = [PlayerRequestErrorResponse.__name__],
        unprocessable_entity_responsable: list[str] = [PlayerHTTPStatusErrorResponse.__name__],
    ) -> Player:
        return Player(
            ResponseToJSONBody.from_response_names(
                to_ok=ok_responsable,
                to_not_found=not_found_responsable,
                to_unprocessable_entity=unprocessable_entity_responsable,
            )
        )

    async def trajectory(self, request: PlayerTrajectoryRequest) -> HALJSONResponse:
        container.api_info.override(providers.Factory(PlayerAPIInfo, name="trajectory", method="post"))

        return self.response_converter.convert(
            await TrajectoryIntent.from_usecase_factory(NormalTrajectoryFactory()).executed(request)
        )

    async def game(self, request: PlayerGameRequest) -> HALJSONResponse:
        container.api_info.override(providers.Factory(PlayerAPIInfo, name="game", method="post"))

        return self.response_converter.convert(
            await GameIntent.from_usecase_factory(NormalGameFactory()).executed(request)
        )

    async def measurement(self, request: PlayerMeasurementRequest) -> HALJSONResponse:
        container.api_info.override(providers.Factory(PlayerAPIInfo, name="measurement", method="post"))

        return self.response_converter.convert(
            await MeasurementIntent.from_usecase_factory(NormalMeasurementFactory()).executed(request)
        )
