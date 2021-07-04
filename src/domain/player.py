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
from src.framework.intent.gameintent import FakeGameIntent, GameIntent
from src.framework.intent.measurementintent import FakeMeasurementIntent, MeasurementIntent
from src.framework.intent.trajectoryintent import FakeTrajectoryIntent, TrajectoryIntent


class Service(NamedTuple):
    trajectory: TrajectoryIntent = TrajectoryIntent.from_usecase()
    game: GameIntent = GameIntent.from_usecase()
    measurement: MeasurementIntent = MeasurementIntent.from_usecase()


class FakeService(Service):
    trajectory: TrajectoryIntent = FakeTrajectoryIntent.from_usecase()
    game: GameIntent = FakeGameIntent.from_usecase()
    measurement: MeasurementIntent = FakeMeasurementIntent.from_usecase()


class MicroChessPlayer(NamedTuple):
    service: Service

    @classmethod
    def from_url(cls) -> MicroChessPlayer:
        return MicroChessPlayer(Service())

    async def trajectory(self, request: PlayerTrajectoryRequest) -> PlayerTrajectoryResponse:
        return await self.service.trajectory.executed(request)

    async def game(self, request: PlayerGameRequest) -> PlayerGameResponse:
        return await self.service.game.executed(request)

    async def measurement(self, request: PlayerMeasurementRequest) -> PlayerMeasurementResponse:
        return await self.service.measurement.executed(request)
