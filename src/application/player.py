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
from src.usecase.game import Game, GameUsecase
from src.usecase.measurement import Measurement, MeasurementUsecase
from src.usecase.trajectory import Trajectory, TrajectoryUsecase
from submodules.fastapi_haljson.src.halconverter import ResponseToJSONBody
from submodules.fastapi_haljson.src.halresponse import HALJSONResponse


class TrajectoryPlayer(NamedTuple):
    intent: TrajectoryIntent
    usecase: TrajectoryUsecase

    @classmethod
    def from_usecase(cls, usecase: TrajectoryUsecase) -> TrajectoryPlayer:
        intent = TrajectoryIntent(usecase)
        usecase.register_framework(intent)

        return TrajectoryPlayer(intent, usecase)


class GamePlayer(NamedTuple):
    intent: GameIntent
    usecase: GameUsecase

    @classmethod
    def from_usecase(cls, usecase: GameUsecase) -> GamePlayer:
        intent = GameIntent(usecase)
        usecase.register_framework(intent)

        return GamePlayer(intent, usecase)


class MeasurementPlayer(NamedTuple):
    intent: MeasurementIntent
    usecase: MeasurementUsecase

    @classmethod
    def from_usecase(cls, usecase: MeasurementUsecase) -> MeasurementPlayer:
        intent = MeasurementIntent(usecase)
        usecase.register_framework(intent)

        return MeasurementPlayer(intent, usecase)


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
            await TrajectoryPlayer.from_usecase(Trajectory.default()).intent.dispatch(request)
        )

    async def game(self, request: PlayerGameRequest) -> HALJSONResponse:
        container.api_info.override(providers.Factory(PlayerAPIInfo, name="game", method="post"))

        return self.response_converter.convert(await GamePlayer.from_usecase(Game.default()).intent.dispatch(request))

    async def measurement(self, request: PlayerMeasurementRequest) -> HALJSONResponse:
        container.api_info.override(providers.Factory(PlayerAPIInfo, name="measurement", method="post"))

        return self.response_converter.convert(
            await MeasurementPlayer.from_usecase(Measurement.default()).intent.dispatch(request)
        )
