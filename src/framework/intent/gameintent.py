# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import NamedTuple

from src.adapter.requestboundary import GameRequestBoundary
from src.adapter.responseboundary import GameResponseBoundary
from src.converter.requestconverter import GameRequestToModel
from src.converter.responseconverter import GameResponseToDTO
from src.domain.dto.playerdto import PlayerGameRequest, PlayerGameResponse
from src.usecase.game import FakeGame, Game, GameFactory, IGame
from src.usecase.requestmodel import GameRequestModel
from src.usecase.responsemodel import GameResponseModel


class GameRequestIntentData(NamedTuple):
    usecase: IGame


class GameRequestIntent(GameRequestIntentData, GameRequestBoundary):
    async def request(self, request_model: GameRequestModel) -> None:
        await self.usecase.executed(request_model)


class GameResponseIntentData(NamedTuple):
    response_model: list[GameResponseModel] = []


class GameResponseIntent(GameResponseIntentData, GameResponseBoundary):
    async def response(self, response_model: GameResponseModel) -> None:
        self.response_model.append(response_model)

    async def pull(self) -> GameResponseModel:
        return self.response_model[0]


class GameIntent(NamedTuple):
    request_intent: GameRequestIntent
    response_intent: GameResponseIntent

    @classmethod
    def from_usecase_factory(cls, factory: GameFactory) -> GameIntent:
        response_intent: GameResponseIntent = GameResponseIntent()

        return GameIntent(GameRequestIntent(factory.createdGame(response_intent)), response_intent)

    async def push(self, request: PlayerGameRequest) -> None:
        await self.request_intent.request(GameRequestToModel.from_dto(request).convert())

    async def pull(self) -> PlayerGameResponse:
        return GameResponseToDTO.from_model(await self.response_intent.pull()).convert()

    async def executed(self, request: PlayerGameRequest) -> PlayerGameResponse:
        await self.push(request)

        return await self.pull()
