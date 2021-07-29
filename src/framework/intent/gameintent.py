# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, Callable, NamedTuple, Union

from src.converter.requestconverter import GameRequestToModel
from src.converter.responseconverter import GameResponseToDTO, HTTPStatusErrorResponseToDTO, RequestErrorResponseToDTO
from src.core.event import EventAGen, PopEvent
from src.core.intent import Intent, IntentData
from src.framework.dto.playerdto import (
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerHTTPStatusErrorResponse,
    PlayerRequestErrorResponse,
)
from src.model.requestmodel import GameRequestModel
from src.model.responsemodel import GameResponsableModel

ResponseType = Union[PlayerGameResponse, PlayerRequestErrorResponse, PlayerHTTPStatusErrorResponse]


class GameResponsableToDTO(NamedTuple):
    converters: dict[
        str,
        Union[
            Callable[[Any], GameResponseToDTO],
            Callable[[Any], RequestErrorResponseToDTO],
            Callable[[Any], HTTPStatusErrorResponseToDTO],
        ],
    ]

    @classmethod
    def from_request_dto(cls, request_dto: PlayerGameRequest) -> GameResponsableToDTO:
        return GameResponsableToDTO(
            {
                "GameResponseModel": (lambda model: GameResponseToDTO.from_model(model)),
                "RequestErrorResponseModel": (
                    lambda model: RequestErrorResponseToDTO.from_model_with_request_dto(model, request_dto)
                ),
                "HTTPStatusErrorResponseModel": (
                    lambda model: HTTPStatusErrorResponseToDTO.from_model_with_request_dto(model, request_dto)
                ),
            }
        )

    def convert(self, model: GameResponsableModel) -> ResponseType:
        return self.converters[type(model).__name__](model).convert()


class GameIntent(IntentData, Intent[PlayerGameRequest, ResponseType, GameRequestModel, GameResponsableModel]):
    async def executed(self, request: PlayerGameRequest) -> EventAGen:
        yield PopEvent(
            GameResponsableToDTO.from_request_dto(request).convert(
                (yield await self.usecase.request(GameRequestToModel.from_dto(request).convert()))
            )
        )
