# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Union

from src.domain.dto.playerdto import (
    PlayerErrorResponse,
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerInternalModel,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from src.domain.player import MicroChessPlayer, Service
from submodules.fastapi_haljson.src.halmodel import HALBase


class TrajectoryRequestData(NamedTuple):
    request: PlayerTrajectoryRequest
    name: str = "trajectory"
    method: str = "post"


class GameRequestData(NamedTuple):
    request: PlayerGameRequest
    name: str = "game"
    method: str = "post"


class MeasurementRequestData(NamedTuple):
    request: PlayerMeasurementRequest
    name: str = "measurement"
    method: str = "post"


class ICreatedResponse(metaclass=ABCMeta):
    @abstractmethod
    async def created(
        self, internal_model: PlayerInternalModel
    ) -> Union[PlayerTrajectoryResponse, PlayerGameResponse, PlayerMeasurementResponse]:
        pass

    @abstractmethod
    def error(self, internal_model: PlayerInternalModel, message: str, error_type: str) -> PlayerErrorResponse:
        pass


class CreatedTrajectoryResponse(TrajectoryRequestData, ICreatedResponse):
    async def created(
        self, internal_model: PlayerInternalModel
    ) -> Union[PlayerTrajectoryResponse, PlayerGameResponse, PlayerMeasurementResponse]:
        return await MicroChessPlayer(Service()).trajectory(self.request, internal_model, self.name, self.method)

    def error(self, internal_model: PlayerInternalModel, message: str, error_type: str) -> PlayerErrorResponse:
        return PlayerErrorResponse(
            links=HALBase.from_routes_with_requested(internal_model.routes, self.name, self.method).links,
            message=message,
            location="body",
            param="fens, white, black, step",
            value=(self.request.fens, self.request.white, self.request.black, self.request.step),
            error=error_type,
        )


class CreatedGameResponse(GameRequestData, ICreatedResponse):
    async def created(
        self, internal_model: PlayerInternalModel
    ) -> Union[PlayerTrajectoryResponse, PlayerGameResponse, PlayerMeasurementResponse]:
        return await MicroChessPlayer(Service()).game(self.request, internal_model, self.name, self.method)

    def error(self, internal_model: PlayerInternalModel, message: str, error_type: str) -> PlayerErrorResponse:
        return PlayerErrorResponse(
            links=HALBase.from_routes_with_requested(internal_model.routes, self.name, self.method).links,
            message=message,
            location="body",
            param="white, black",
            value=(self.request.white, self.request.black),
            error=error_type,
        )


class CreatedMeasurementResponse(MeasurementRequestData, ICreatedResponse):
    async def created(
        self, internal_model: PlayerInternalModel
    ) -> Union[PlayerTrajectoryResponse, PlayerGameResponse, PlayerMeasurementResponse]:
        return await MicroChessPlayer(Service()).measurement(self.request, internal_model, self.name, self.method)

    def error(self, internal_model: PlayerInternalModel, message: str, error_type: str) -> PlayerErrorResponse:
        return PlayerErrorResponse(
            links=HALBase.from_routes_with_requested(internal_model.routes, self.name, self.method).links,
            message=message,
            location="body",
            param="white, black, playtime",
            value=(self.request.white, self.request.black, self.request.playtime),
            error=error_type,
        )
