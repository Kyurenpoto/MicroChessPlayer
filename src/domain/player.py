# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import NamedTuple

from src.domain.dto.playerdto import (
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from src.framework.intent.gameintent import GameIntent
from src.framework.intent.measurementintent import MeasurementIntent
from src.framework.intent.trajectoryintent import TrajectoryIntent
from src.usecase.game import FakeGameFactory, NormalGameFactory
from src.usecase.measurement import FakeMeasurementFactory, NormalMeasurementFactory
from src.usecase.trajectory import FakeTrajectoryFactory, NormalTrajectoryFactory


class Service(NamedTuple):
    trajectory: TrajectoryIntent = TrajectoryIntent.from_usecase_factory(NormalTrajectoryFactory())
    game: GameIntent = GameIntent.from_usecase_factory(NormalGameFactory())
    measurement: MeasurementIntent = MeasurementIntent.from_usecase_factory(NormalMeasurementFactory())


class FakeService(Service):
    trajectory: TrajectoryIntent = TrajectoryIntent.from_usecase_factory(FakeTrajectoryFactory())
    game: GameIntent = GameIntent.from_usecase_factory(FakeGameFactory())
    measurement: MeasurementIntent = MeasurementIntent.from_usecase_factory(FakeMeasurementFactory())


class MicroChessPlayer(NamedTuple):
    service: Service

    async def trajectory(self, request: PlayerTrajectoryRequest) -> PlayerTrajectoryResponse:
        return await self.service.trajectory.executed(request)

    async def game(self, request: PlayerGameRequest) -> PlayerGameResponse:
        return await self.service.game.executed(request)

    async def measurement(self, request: PlayerMeasurementRequest) -> PlayerMeasurementResponse:
        return await self.service.measurement.executed(request)
