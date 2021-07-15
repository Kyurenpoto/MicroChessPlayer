# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, NamedTuple, Union

from dependency_injector.wiring import Provide, inject
from src.config import Container
from src.framework.dto.playerdto import (
    PlayerAIMeasurement,
    PlayerAPIInfo,
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerHTTPStatusErrorResponse,
    PlayerInternal,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerRequestErrorResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from src.model.responsemodel import (
    GameResponseModel,
    HTTPStatusErrorResponseModel,
    MeasurementInfo,
    MeasurementResponseModel,
    RequestErrorResponseModel,
    TrajectoryResponseModel,
)
from submodules.fastapi_haljson.src.halmodel import HALBase


class TrajectoryResponseToDTO(TrajectoryResponseModel):
    @classmethod
    def from_model(cls, model: TrajectoryResponseModel) -> TrajectoryResponseToDTO:
        return TrajectoryResponseToDTO._make(model)

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
    def from_model(cls, model: GameResponseModel) -> GameResponseToDTO:
        return GameResponseToDTO._make(model)

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
    def from_model(cls, model: MeasurementInfo) -> MeasurementInfoToDTO:
        return MeasurementInfoToDTO._make(model)

    def convert(self) -> PlayerAIMeasurement:
        return PlayerAIMeasurement(score=self.score, win=self.win, lose=self.lose, draw=self.draw)


class MeasurementResponseToDTO(MeasurementResponseModel):
    @classmethod
    def from_model(cls, model: MeasurementResponseModel) -> MeasurementResponseToDTO:
        return MeasurementResponseToDTO._make(model)

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


class RequestErrorResponseToDTO(NamedTuple):
    model: RequestErrorResponseModel
    dto_dict: dict[str, Any]

    @classmethod
    def from_model_with_request_dto(
        cls,
        model: RequestErrorResponseModel,
        request_dto: Union[PlayerTrajectoryRequest, PlayerGameRequest, PlayerMeasurementRequest],
    ) -> RequestErrorResponseToDTO:
        return RequestErrorResponseToDTO(model, request_dto.dict())

    @inject
    def convert(
        self,
        internal_model: PlayerInternal = Provide[Container.internal_model],
        api_info: PlayerAPIInfo = Provide[Container.api_info],
    ) -> PlayerRequestErrorResponse:
        return PlayerRequestErrorResponse(
            links=HALBase.from_routes_with_requested(internal_model.routes, api_info.name, api_info.method).links,
            message=self.model.message,
            location="body",
            param=", ".join(self.dto_dict.keys()),
            value=list(self.dto_dict.values()),
            error=self.model.error,
        )


class HTTPStatusErrorResponseToDTO(NamedTuple):
    model: HTTPStatusErrorResponseModel
    dto_dict: dict[str, Any]

    @classmethod
    def from_model_with_request_dto(
        cls,
        model: HTTPStatusErrorResponseModel,
        request_dto: Union[PlayerTrajectoryRequest, PlayerGameRequest, PlayerMeasurementRequest],
    ) -> HTTPStatusErrorResponseToDTO:
        return HTTPStatusErrorResponseToDTO(model, request_dto.dict())

    @inject
    def convert(
        self,
        internal_model: PlayerInternal = Provide[Container.internal_model],
        api_info: PlayerAPIInfo = Provide[Container.api_info],
    ) -> PlayerHTTPStatusErrorResponse:
        return PlayerHTTPStatusErrorResponse(
            links=HALBase.from_routes_with_requested(internal_model.routes, api_info.name, api_info.method).links,
            message=self.model.message,
            location="body",
            param=", ".join(self.dto_dict.keys()),
            value=list(self.dto_dict.values()),
            error=self.model.error,
        )
