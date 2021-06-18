# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Union

from dependency_injector import providers
from dependency_injector.wiring import Provide, inject
from src.config import Container, container
from src.domain.dto.playerdto import (
    PlayerAIInfo,
    PlayerAPIInfo,
    PlayerErrorResponse,
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerInternal,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from src.domain.player import MicroChessPlayer, Service
from submodules.fastapi_haljson.src.halmodel import HALBase


class TrajectoryRequestData(NamedTuple):
    request: PlayerTrajectoryRequest


class GameRequestData(NamedTuple):
    request: PlayerGameRequest


class MeasurementRequestData(NamedTuple):
    request: PlayerMeasurementRequest


class ICreatedResponse(metaclass=ABCMeta):
    @abstractmethod
    async def normal(self) -> Union[PlayerTrajectoryResponse, PlayerGameResponse, PlayerMeasurementResponse]:
        pass

    @abstractmethod
    def error(self, message: str, error_type: str) -> PlayerErrorResponse:
        pass


class CreatedErrorResponse(NamedTuple):
    message: str
    param: str
    value: Union[
        tuple[list[str], PlayerAIInfo, PlayerAIInfo, int],
        tuple[PlayerAIInfo, PlayerAIInfo],
        tuple[PlayerAIInfo, PlayerAIInfo, int],
    ]
    error: str

    @inject
    def created(
        self,
        internal_model: PlayerInternal = Provide[Container.internal_model],
        api_info: PlayerAPIInfo = Provide[Container.api_info],
    ) -> PlayerErrorResponse:
        return PlayerErrorResponse(
            links=HALBase.from_routes_with_requested(internal_model.routes, api_info.name, api_info.method).links,
            message=self.message,
            location="body",
            param=self.param,
            value=self.value,
            error=self.error,
        )


class CreatedTrajectoryResponse(TrajectoryRequestData, ICreatedResponse):
    async def normal(self) -> Union[PlayerTrajectoryResponse, PlayerGameResponse, PlayerMeasurementResponse]:
        container.api_info.override(providers.Factory(PlayerAPIInfo, name="trajectory", method="post"))

        return await MicroChessPlayer(Service()).trajectory(self.request)

    def error(self, message: str, error_type: str) -> PlayerErrorResponse:
        return CreatedErrorResponse(
            message,
            "fens, white, black, step",
            (self.request.fens, self.request.white, self.request.black, self.request.step),
            error_type,
        ).created()


class CreatedGameResponse(GameRequestData, ICreatedResponse):
    async def normal(self) -> Union[PlayerTrajectoryResponse, PlayerGameResponse, PlayerMeasurementResponse]:
        container.api_info.override(providers.Factory(PlayerAPIInfo, name="game", method="post"))

        return await MicroChessPlayer(Service()).game(self.request)

    def error(self, message: str, error_type: str) -> PlayerErrorResponse:
        return CreatedErrorResponse(
            message,
            "white, black",
            (self.request.white, self.request.black),
            error_type,
        ).created()


class CreatedMeasurementResponse(MeasurementRequestData, ICreatedResponse):
    async def normal(self) -> Union[PlayerTrajectoryResponse, PlayerGameResponse, PlayerMeasurementResponse]:
        container.api_info.override(providers.Factory(PlayerAPIInfo, name="measurement", method="post"))

        return await MicroChessPlayer(Service()).measurement(self.request)

    def error(self, message: str, error_type: str) -> PlayerErrorResponse:
        return CreatedErrorResponse(
            message,
            "white, black, playtime",
            (self.request.white, self.request.black, self.request.playtime),
            error_type,
        ).created()
