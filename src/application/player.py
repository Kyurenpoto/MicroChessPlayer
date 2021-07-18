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
from src.framework.intent.gameintent import GameIntent, GameRequestIntent, GameResponseIntent
from src.framework.intent.measurementintent import (
    MeasurementIntent,
    MeasurementRequestIntent,
    MeasurementResponseIntent,
)
from src.framework.intent.trajectoryintent import TrajectoryIntent, TrajectoryRequestIntent, TrajectoryResponseIntent
from src.usecase.game import GameFactory, NormalGameFactory
from src.usecase.measurement import MeasurementFactory, NormalMeasurementFactory
from src.usecase.trajectory import NormalTrajectoryFactory, TrajectoryFactory
from submodules.fastapi_haljson.src.halconverter import ResponseToJSONBody
from submodules.fastapi_haljson.src.halresponse import HALJSONResponse


class TrajectoryPlayer(NamedTuple):
    intent: TrajectoryIntent

    @classmethod
    def from_usecase_factory(cls, usecase_factory: TrajectoryFactory) -> TrajectoryPlayer:
        response_intent: TrajectoryResponseIntent = TrajectoryResponseIntent([])
        usecase = usecase_factory.createdTrajectory(response_intent)

        return TrajectoryPlayer(TrajectoryIntent(TrajectoryRequestIntent(usecase), response_intent))


class GamePlayer(NamedTuple):
    intent: GameIntent

    @classmethod
    def from_usecase_factory(cls, usecase_factory: GameFactory) -> GamePlayer:
        response_intent: GameResponseIntent = GameResponseIntent([])
        usecase = usecase_factory.createdGame(response_intent)

        return GamePlayer(GameIntent(GameRequestIntent(usecase), response_intent))


class MeasurementPlayer(NamedTuple):
    intent: MeasurementIntent

    @classmethod
    def from_usecase_factory(cls, usecase_factory: MeasurementFactory) -> MeasurementPlayer:
        response_intent: MeasurementResponseIntent = MeasurementResponseIntent([])
        usecase = usecase_factory.createdMeasurement(response_intent)

        return MeasurementPlayer(MeasurementIntent(MeasurementRequestIntent(usecase), response_intent))


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
            await TrajectoryPlayer.from_usecase_factory(NormalTrajectoryFactory()).intent.executed(request)
        )

    async def game(self, request: PlayerGameRequest) -> HALJSONResponse:
        container.api_info.override(providers.Factory(PlayerAPIInfo, name="game", method="post"))

        return self.response_converter.convert(
            await GamePlayer.from_usecase_factory(NormalGameFactory()).intent.executed(request)
        )

    async def measurement(self, request: PlayerMeasurementRequest) -> HALJSONResponse:
        container.api_info.override(providers.Factory(PlayerAPIInfo, name="measurement", method="post"))

        return self.response_converter.convert(
            await MeasurementPlayer.from_usecase_factory(NormalMeasurementFactory()).intent.executed(request)
        )
