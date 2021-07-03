# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import NamedTuple

from src.converter.requestconverter import GameRequestToModel, MeasurementRequestToModel, TrajectoryRequestToModel
from src.converter.responseconverter import GameResponseToDTO, MeasurementResponseToDTO, TrajectoryResponseToDTO
from src.domain.dto.playerdto import (
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from src.usecase.game import FakeGame, Game, IGame
from src.usecase.measurement import FakeMeasurement, IMeasurement, Measurement
from src.usecase.trajectory import FakeTrajectory, ITrajectory, Trajectory


class IService(metaclass=ABCMeta):
    @abstractmethod
    def trajectory(self, request: PlayerTrajectoryRequest) -> ITrajectory:
        pass

    @abstractmethod
    def game(self, request: PlayerGameRequest) -> IGame:
        pass

    @abstractmethod
    def rate(self, request: PlayerMeasurementRequest) -> IMeasurement:
        pass


class Service(IService):
    def trajectory(self, request: PlayerTrajectoryRequest) -> ITrajectory:
        return Trajectory(TrajectoryRequestToModel.from_dto(request).convert())

    def game(self, request: PlayerGameRequest) -> IGame:
        return Game(GameRequestToModel.from_dto(request).convert())

    def rate(self, request: PlayerMeasurementRequest) -> IMeasurement:
        return Measurement(MeasurementRequestToModel.from_dto(request).convert())


class FakeService(IService):
    def trajectory(self, request: PlayerTrajectoryRequest) -> ITrajectory:
        return FakeTrajectory()

    def game(self, request: PlayerGameRequest) -> IGame:
        return FakeGame()

    def rate(self, request: PlayerMeasurementRequest) -> IMeasurement:
        return FakeMeasurement()


class MicroChessPlayer(NamedTuple):
    service: IService

    @classmethod
    def from_url(cls) -> MicroChessPlayer:
        return MicroChessPlayer(Service())

    async def trajectory(self, request: PlayerTrajectoryRequest) -> PlayerTrajectoryResponse:
        return TrajectoryResponseToDTO.from_model(await self.service.trajectory(request).executed()).convert()

    async def game(self, request: PlayerGameRequest) -> PlayerGameResponse:
        return GameResponseToDTO.from_model(await self.service.game(request).executed()).convert()

    async def measurement(self, request: PlayerMeasurementRequest) -> PlayerMeasurementResponse:
        return MeasurementResponseToDTO.from_model(await self.service.rate(request).executed()).convert()
