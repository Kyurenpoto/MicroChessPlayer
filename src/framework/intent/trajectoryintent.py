# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, Callable, NamedTuple, Union

from src.converter.requestconverter import TrajectoryRequestToModel
from src.converter.responseconverter import (
    HTTPStatusErrorResponseToDTO,
    RequestErrorResponseToDTO,
    TrajectoryResponseToDTO,
)
from src.core.event import EventAGen, PopEvent
from src.core.intent import Intent, IntentData
from src.framework.dto.playerdto import (
    PlayerHTTPStatusErrorResponse,
    PlayerRequestErrorResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from src.model.requestmodel import TrajectoryRequestModel
from src.model.responsemodel import TrajectoryResponsableModel

ResponseType = Union[PlayerTrajectoryResponse, PlayerRequestErrorResponse, PlayerHTTPStatusErrorResponse]


class TrajectoryResponsableToDTO(NamedTuple):
    converters: dict[
        str,
        Union[
            Callable[[Any], TrajectoryResponseToDTO],
            Callable[[Any], RequestErrorResponseToDTO],
            Callable[[Any], HTTPStatusErrorResponseToDTO],
        ],
    ]

    @classmethod
    def from_request_dto(cls, request_dto: PlayerTrajectoryRequest) -> TrajectoryResponsableToDTO:
        return TrajectoryResponsableToDTO(
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


class TrajectoryIntent(
    IntentData,
    Intent[PlayerTrajectoryRequest, ResponseType, TrajectoryRequestModel, TrajectoryResponsableModel],
):
    async def executed(self, request: PlayerTrajectoryRequest) -> EventAGen:
        yield PopEvent(
            TrajectoryResponsableToDTO.from_request_dto(request).convert(
                (yield await self.usecase.request(TrajectoryRequestToModel.from_dto(request).convert()))
            )
        )
