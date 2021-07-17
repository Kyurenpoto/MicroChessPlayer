# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, Callable, NamedTuple, Union

from src.adapter.requestboundary import GameRequestBoundary
from src.adapter.responseboundary import GameResponseBoundary
from src.converter.requestconverter import GameRequestToModel
from src.converter.responseconverter import GameResponseToDTO, HTTPStatusErrorResponseToDTO, RequestErrorResponseToDTO
from src.framework.dto.playerdto import (
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerHTTPStatusErrorResponse,
    PlayerRequestErrorResponse,
)
from src.model.requestmodel import GameRequestModel
from src.model.responsemodel import GameResponsableModel
from src.usecase.game import GameFactory, IGame


class GameRequestIntentData(NamedTuple):
    usecase: IGame


class GameRequestIntent(GameRequestIntentData, GameRequestBoundary):
    async def request(self, request_model: GameRequestModel) -> None:
        await self.usecase.executed(request_model)


class GameResponseIntentData(NamedTuple):
    response_model: list[GameResponsableModel]


class GameResponseIntent(GameResponseIntentData, GameResponseBoundary):
    async def response(self, response_model: GameResponsableModel) -> None:
        self.response_model.append(response_model)

    async def pull(self) -> GameResponsableModel:
        return self.response_model[0]


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


class GameIntent(NamedTuple):
    request_intent: GameRequestIntent
    response_intent: GameResponseIntent

    @classmethod
    def from_usecase_factory(cls, factory: GameFactory) -> GameIntent:
        response_intent: GameResponseIntent = GameResponseIntent([])

        return GameIntent(GameRequestIntent(factory.createdGame(response_intent)), response_intent)

    async def executed(self, request: PlayerGameRequest) -> ResponseType:
        await self.request_intent.request(GameRequestToModel.from_dto(request).convert())

        return GameResponsableToDTO.from_request_dto(request).convert(await self.response_intent.pull())
