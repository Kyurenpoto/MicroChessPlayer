# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, Callable, NamedTuple, Union

from src.adapter.requestboundary import MeasurementRequestBoundary
from src.adapter.responseboundary import MeasurementResponseBoundary
from src.converter.requestconverter import MeasurementRequestToModel
from src.converter.responseconverter import (
    HTTPStatusErrorResponseToDTO,
    MeasurementResponseToDTO,
    RequestErrorResponseToDTO,
)
from src.framework.dto.playerdto import (
    PlayerHTTPStatusErrorResponse,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerRequestErrorResponse,
)
from src.model.requestmodel import MeasurementRequestModel
from src.model.responsemodel import MeasurementResponsableModel
from src.usecase.measurement import IMeasurement, MeasurementFactory


class MeasurementRequestIntentData(NamedTuple):
    usecase: IMeasurement


class MeasurementRequestIntent(MeasurementRequestIntentData, MeasurementRequestBoundary):
    async def request(self, request_model: MeasurementRequestModel) -> None:
        await self.usecase.executed(request_model)


class MeasurementResponseIntentData(NamedTuple):
    response_model: list[MeasurementResponsableModel]


class MeasurementResponseIntent(MeasurementResponseIntentData, MeasurementResponseBoundary):
    async def response(self, response_model: MeasurementResponsableModel) -> None:
        self.response_model.append(response_model)

    async def pull(self) -> MeasurementResponsableModel:
        return self.response_model[0]


ResponseType = Union[PlayerMeasurementResponse, PlayerRequestErrorResponse, PlayerHTTPStatusErrorResponse]


class MeasurementResonsableConverter(NamedTuple):
    converters: dict[
        str,
        Union[
            Callable[[Any], MeasurementResponseToDTO],
            Callable[[Any], RequestErrorResponseToDTO],
            Callable[[Any], HTTPStatusErrorResponseToDTO],
        ],
    ]

    @classmethod
    def from_request_dto(cls, request_dto: PlayerMeasurementRequest) -> MeasurementResonsableConverter:
        return MeasurementResonsableConverter(
            {
                "MeasurementResponseModel": (lambda model: MeasurementResponseToDTO.from_model(model)),
                "RequestErrorResponseModel": (
                    lambda model: RequestErrorResponseToDTO.from_model_with_request_dto(model, request_dto)
                ),
                "HTTPStatusErrorResponseModel": (
                    lambda model: HTTPStatusErrorResponseToDTO.from_model_with_request_dto(model, request_dto)
                ),
            }
        )

    def convert(self, model: MeasurementResponsableModel) -> ResponseType:
        return self.converters[type(model).__name__](model).convert()


class MeasurementIntent(NamedTuple):
    request_intent: MeasurementRequestIntent
    response_intent: MeasurementResponseIntent

    @classmethod
    def from_usecase_factory(cls, factory: MeasurementFactory) -> MeasurementIntent:
        response_intent: MeasurementResponseIntent = MeasurementResponseIntent([])

        return MeasurementIntent(MeasurementRequestIntent(factory.createdMeasurement(response_intent)), response_intent)

    async def push(self, request: PlayerMeasurementRequest) -> None:
        await self.request_intent.request(MeasurementRequestToModel.from_dto(request).convert())

    async def pull(self, request: PlayerMeasurementRequest) -> ResponseType:
        return MeasurementResonsableConverter.from_request_dto(request).convert(await self.response_intent.pull())

    async def executed(self, request: PlayerMeasurementRequest) -> ResponseType:
        await self.push(request)

        return await self.pull(request)
