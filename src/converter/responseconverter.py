# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT


from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from src.config import Container
from src.framework.dto.playerdto import (
    PlayerAIMeasurement,
    PlayerAPIInfo,
    PlayerErrorResponse,
    PlayerGameResponse,
    PlayerInternal,
    PlayerMeasurementResponse,
    PlayerTrajectoryResponse,
)
from src.usecase.responsemodel import (
    ErrorResponseModel,
    GameResponseModel,
    MeasurementInfo,
    MeasurementResponseModel,
    TrajectoryResponseModel,
)
from submodules.fastapi_haljson.src.halmodel import HALBase


class TrajectoryResponseToDTO(TrajectoryResponseModel):
    @classmethod
    def from_model(cls, dto: TrajectoryResponseModel) -> TrajectoryResponseToDTO:
        return TrajectoryResponseToDTO._make(dto)

    @inject
    def convert(
        self,
        internal_model: PlayerInternal = Provide[Container.internal_model],
        api_info: PlayerAPIInfo = Provide[Container.api_info],
    ) -> PlayerTrajectoryResponse:
        return PlayerTrajectoryResponse(
            links=HALBase.from_routes_with_requested(internal_model.routes, api_info.name, api_info.method).links,
            fens=self.fens,
            sans=self.sans,
            results=self.results,
        )


class GameResponseToDTO(GameResponseModel):
    @classmethod
    def from_model(cls, dto: GameResponseModel) -> GameResponseToDTO:
        return GameResponseToDTO._make(dto)

    @inject
    def convert(
        self,
        internal_model: PlayerInternal = Provide[Container.internal_model],
        api_info: PlayerAPIInfo = Provide[Container.api_info],
    ) -> PlayerGameResponse:
        return PlayerGameResponse(
            links=HALBase.from_routes_with_requested(internal_model.routes, api_info.name, api_info.method).links,
            fens=self.fens,
            sans=self.sans,
            result=self.result,
        )


class MeasurementInfoToDTO(MeasurementInfo):
    @classmethod
    def from_model(cls, dto: MeasurementInfo) -> MeasurementInfoToDTO:
        return MeasurementInfoToDTO._make(dto)

    def convert(self) -> PlayerAIMeasurement:
        return PlayerAIMeasurement(score=self.score, win=self.win, lose=self.lose, draw=self.draw)


class MeasurementResponseToDTO(MeasurementResponseModel):
    @classmethod
    def from_model(cls, dto: MeasurementResponseModel) -> MeasurementResponseToDTO:
        return MeasurementResponseToDTO._make(dto)

    @inject
    def convert(
        self,
        internal_model: PlayerInternal = Provide[Container.internal_model],
        api_info: PlayerAPIInfo = Provide[Container.api_info],
    ) -> PlayerMeasurementResponse:
        return PlayerMeasurementResponse(
            links=HALBase.from_routes_with_requested(internal_model.routes, api_info.name, api_info.method).links,
            white=MeasurementInfoToDTO.from_model(self.white_info).convert(),
            black=MeasurementInfoToDTO.from_model(self.black_info).convert(),
        )


class ErrorResponseToDTO(ErrorResponseModel):
    @classmethod
    def from_model(cls, dto: ErrorResponseModel) -> ErrorResponseToDTO:
        return ErrorResponseToDTO._make(dto)

    @inject
    def convert(
        self,
        internal_model: PlayerInternal = Provide[Container.internal_model],
        api_info: PlayerAPIInfo = Provide[Container.api_info],
    ) -> PlayerErrorResponse:
        return PlayerErrorResponse(
            links=HALBase.from_routes_with_requested(internal_model.routes, api_info.name, api_info.method).links,
            message=self.message,
            location=self.location,
            param=self.param,
            value=self.value,
            error=self.error,
        )
