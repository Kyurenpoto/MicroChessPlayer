# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from enum import Enum
from typing import Any, NamedTuple, Type, Union

from dependency_injector.wiring import Provide, inject
from src.config import Container
from src.framework.dto.aidto import AINextSANResponse
from src.framework.dto.environmentdto import EnvironmentFENStatusResponse, EnvironmentNextFENResponse
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
    BadGatewayResponseModel,
    BadRequestResponseModel,
    FENStatusResponseModel,
    GameResponseModel,
    HTTPStatusErrorResponseModel,
    InternalServerErrorResponseModel,
    MeasurementInfo,
    MeasurementResponseModel,
    NextFENResponseModel,
    NextSANResponseModel,
    PayloadTooLargeResponseModel,
    RequestErrorResponseModel,
    ResponseErrorResponseModel,
    TrajectoryResponseModel,
    UnprocessableEntityResponseModel,
    UnsupportedMediaTypeResponseModel,
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


class EnvironmentNextFENResponseToModel(EnvironmentNextFENResponse):
    @classmethod
    def from_dto(cls, dto: EnvironmentNextFENResponse) -> EnvironmentNextFENResponseToModel:
        return EnvironmentNextFENResponseToModel(next_fens=dto.next_fens)

    def convert(self) -> NextFENResponseModel:
        return NextFENResponseModel(self.next_fens)


class EnvironmentFENStatusResponseToModel(EnvironmentFENStatusResponse):
    @classmethod
    def from_dto(cls, dto: EnvironmentFENStatusResponse) -> EnvironmentFENStatusResponseToModel:
        return EnvironmentFENStatusResponseToModel(statuses=dto.statuses, legal_moves=dto.legal_moves)

    def convert(self) -> FENStatusResponseModel:
        return FENStatusResponseModel(self.statuses, self.legal_moves)


class AINextSANResponseToModel(AINextSANResponse):
    @classmethod
    def from_dto(cls, dto: AINextSANResponse) -> AINextSANResponseToModel:
        return AINextSANResponseToModel(next_sans=dto.next_sans)

    def convert(self) -> NextSANResponseModel:
        return NextSANResponseModel(self.next_sans)


class ConvertedRequestErrorResponseModel(NamedTuple):
    request_url: str
    response_args: tuple
    service: str

    def convert(self) -> RequestErrorResponseModel:
        return RequestErrorResponseModel.from_message_with_service(
            f"Request Error occurred while requesting {self.request_url!r}: {self.response_args!r}",
            self.service,
        )


class HTTPStatusErrorCode(Enum):
    BAD_REQUEST = 400
    PAYLOAD_TOO_LARGE = 413
    UNSUPPORTED_MEDIA_TYPE = 415
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502


class ConvertedHTTPStatusErrorResponseModel(NamedTuple):
    status_code: int
    request_url: str
    response_json: dict[str, Any]
    service: str

    def convert(self) -> ResponseErrorResponseModel:
        type_convert_table: dict[HTTPStatusErrorCode, Type[ResponseErrorResponseModel]] = {
            HTTPStatusErrorCode.BAD_REQUEST: BadRequestResponseModel,
            HTTPStatusErrorCode.PAYLOAD_TOO_LARGE: PayloadTooLargeResponseModel,
            HTTPStatusErrorCode.UNSUPPORTED_MEDIA_TYPE: UnsupportedMediaTypeResponseModel,
            HTTPStatusErrorCode.UNPROCESSABLE_ENTITY: UnprocessableEntityResponseModel,
            HTTPStatusErrorCode.INTERNAL_SERVER_ERROR: InternalServerErrorResponseModel,
            HTTPStatusErrorCode.BAD_GATEWAY: BadGatewayResponseModel,
        }
        message_convert_table: dict[HTTPStatusErrorCode, str] = {
            HTTPStatusErrorCode.BAD_REQUEST: "Bad Request Error",
            HTTPStatusErrorCode.PAYLOAD_TOO_LARGE: "Payload Too Large Error",
            HTTPStatusErrorCode.UNSUPPORTED_MEDIA_TYPE: "Unsupported Media Type Error",
            HTTPStatusErrorCode.UNPROCESSABLE_ENTITY: "Unprocessable Entity Error",
            HTTPStatusErrorCode.INTERNAL_SERVER_ERROR: "Internal Server Error",
            HTTPStatusErrorCode.BAD_GATEWAY: "Bad Gateway Error",
        }

        try:
            return type_convert_table[HTTPStatusErrorCode(self.status_code)].from_message_with_service(
                message_convert_table[HTTPStatusErrorCode(self.status_code)]
                + f"occured while requesting {self.request_url!r}: {self.response_json!r}",
                self.service,
            )
        except KeyError:
            return type_convert_table[HTTPStatusErrorCode.INTERNAL_SERVER_ERROR].from_message_with_service(
                message_convert_table[HTTPStatusErrorCode.INTERNAL_SERVER_ERROR]
                + f"occured while requesting {self.request_url!r}: {self.response_json!r}",
                self.service,
            )
        except:
            return type_convert_table[HTTPStatusErrorCode.INTERNAL_SERVER_ERROR].from_message_with_service(
                message_convert_table[HTTPStatusErrorCode.INTERNAL_SERVER_ERROR]
                + f"occured while requesting {self.request_url!r}: {self.response_json!r}",
                self.service,
            )
