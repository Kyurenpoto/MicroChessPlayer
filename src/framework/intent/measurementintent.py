# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, Callable, NamedTuple, Union

from src.converter.requestconverter import MeasurementRequestToModel
from src.converter.responseconverter import (
    HTTPStatusErrorResponseToDTO,
    MeasurementResponseToDTO,
    RequestErrorResponseToDTO,
)
from src.core.event import EventAGen, PopEvent
from src.core.intent import Intent, IntentData
from src.framework.dto.playerdto import (
    PlayerHTTPStatusErrorResponse,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerRequestErrorResponse,
)
from src.model.requestmodel import MeasurementRequestModel
from src.model.responsemodel import MeasurementResponsableModel

ResponseType = Union[PlayerMeasurementResponse, PlayerRequestErrorResponse, PlayerHTTPStatusErrorResponse]


class MeasurementResponsableToDTO(NamedTuple):
    converters: dict[
        str,
        Union[
            Callable[[Any], MeasurementResponseToDTO],
            Callable[[Any], RequestErrorResponseToDTO],
            Callable[[Any], HTTPStatusErrorResponseToDTO],
        ],
    ]

    @classmethod
    def from_request_dto(cls, request_dto: PlayerMeasurementRequest) -> MeasurementResponsableToDTO:
        return MeasurementResponsableToDTO(
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


class MeasurementIntent(
    IntentData, Intent[PlayerMeasurementRequest, ResponseType, MeasurementRequestModel, MeasurementResponsableModel]
):
    async def executed(self, request: PlayerMeasurementRequest) -> EventAGen:
        yield PopEvent(
            MeasurementResponsableToDTO.from_request_dto(request).convert(
                (yield await self.usecase.request(MeasurementRequestToModel.from_dto(request).convert()))
            )
        )
