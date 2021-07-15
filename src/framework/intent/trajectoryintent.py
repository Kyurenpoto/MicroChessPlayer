# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, Callable, NamedTuple, Union, cast

from src.adapter.requestboundary import TrajectoryRequestBoundary
from src.adapter.responseboundary import TrajectoryResponseBoundary
from src.converter.requestconverter import TrajectoryRequestToModel
from src.converter.responseconverter import (
    HTTPStatusErrorResponseToDTO,
    RequestErrorResponseToDTO,
    TrajectoryResponseToDTO,
)
from src.framework.dto.playerdto import (
    PlayerHTTPStatusErrorResponse,
    PlayerRequestErrorResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from src.model.requestmodel import TrajectoryRequestModel
from src.model.responsemodel import TrajectoryResponsableModel
from src.usecase.trajectory import ITrajectory, TrajectoryFactory


class TrajectoryRequestIntentData(NamedTuple):
    usecase: ITrajectory


class TrajectoryRequestIntent(TrajectoryRequestIntentData, TrajectoryRequestBoundary):
    async def request(self, request_model: TrajectoryRequestModel) -> None:
        await self.usecase.executed(request_model)


class TrajectoryResponseIntentData(NamedTuple):
    response_model: list[TrajectoryResponsableModel] = []


class TrajectoryResponseIntent(TrajectoryResponseIntentData, TrajectoryResponseBoundary):
    async def response(self, response_model: TrajectoryResponsableModel) -> None:
        self.response_model.append(response_model)

    async def pull(self) -> TrajectoryResponsableModel:
        return self.response_model[0]


ResponseType = Union[PlayerTrajectoryResponse, PlayerRequestErrorResponse, PlayerHTTPStatusErrorResponse]


class TrajectoryResonsableConverter(NamedTuple):
    converters: dict[
        str,
        Union[
            Callable[[Any], TrajectoryResponseToDTO],
            Callable[[Any], RequestErrorResponseToDTO],
            Callable[[Any], HTTPStatusErrorResponseToDTO],
        ],
    ]

    @classmethod
    def from_request_dto(cls, request_dto: PlayerTrajectoryRequest) -> TrajectoryResonsableConverter:
        return TrajectoryResonsableConverter(
            {
                "TrajectoryResponseModel": (lambda model: TrajectoryResponseToDTO.from_model(model)),
                "RequestErrorResponseModel": (
                    lambda model: RequestErrorResponseToDTO.from_model_with_request_dto(model, request_dto)
                ),
                "HTTPStatusErrorResponseModel": (
                    lambda model: HTTPStatusErrorResponseToDTO.from_model_with_request_dto(model, request_dto)
                ),
            }
        )

    def convert(self, model: TrajectoryResponsableModel) -> ResponseType:
        return self.converters[type(model).__name__](model).convert()


class TrajectoryIntent(NamedTuple):
    request_intent: TrajectoryRequestIntent
    response_intent: TrajectoryResponseIntent

    @classmethod
    def from_usecase_factory(cls, factory: TrajectoryFactory) -> TrajectoryIntent:
        response_intent: TrajectoryResponseIntent = TrajectoryResponseIntent()

        return TrajectoryIntent(TrajectoryRequestIntent(factory.createdTrajectory(response_intent)), response_intent)

    async def push(self, request: PlayerTrajectoryRequest) -> None:
        await self.request_intent.request(TrajectoryRequestToModel.from_dto(request).convert())

    async def pull(self, request: PlayerTrajectoryRequest) -> ResponseType:
        return TrajectoryResonsableConverter.from_request_dto(request).convert(await self.response_intent.pull())

    async def executed(self, request: PlayerTrajectoryRequest) -> ResponseType:
        await self.push(request)

        return await self.pull(request)
