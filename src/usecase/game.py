# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import abstractmethod

from httpx import HTTPStatusError, RequestError
from src.core.event import EventAGen
from src.core.usecase import Usecase
from src.entity.movement import FEN, Movement
from src.entity.score import Score
from src.entity.status import Status
from src.entity.trace import InfiniteTraceProducable, ProducableTrace, Trace
from src.model.requestmodel import GameRequestModel
from src.model.responsemodel import (
    GameResponsableModel,
    GameResponseModel,
    HTTPStatusErrorResponseModel,
    RequestErrorResponseModel,
)


class ResultTrace(Trace):
    def to_response(self) -> GameResponseModel:
        return GameResponseModel(self.fens[0], self.sans[0], Score.from_results(self.results[0]))


class GameUsecase(Usecase[GameRequestModel, GameResponsableModel]):
    @classmethod
    def default(cls) -> GameUsecase:
        return cls([], {}, {})


class Game(GameUsecase):
    async def executed(self, request: GameRequestModel) -> EventAGen:
        try:
            yield await self.frameworks[0].response(
                ResultTrace._make(
                    await ProducableTrace(
                        Status(request.env),
                        Movement(request.env, request.ai_white),
                        Movement(request.env, request.ai_black),
                        InfiniteTraceProducable(),
                    ).produced([FEN.starting()])
                ).to_response()
            )
        except RequestError as ex:
            yield await self.frameworks[0].response(
                RequestErrorResponseModel(
                    f"An error occurred while requesting {ex.request.url!r}: {ex.args[0]!r}",
                    "request.RequestError",
                )
            )
        except HTTPStatusError as ex:
            yield await self.frameworks[0].response(
                HTTPStatusErrorResponseModel(
                    f"Error response {ex.response.status_code} "
                    + f"while requesting {ex.request.url!r}: {ex.response.json()!r}",
                    "request.HTTPStatusError",
                )
            )


class FakeGame(GameUsecase):
    async def executed(self, request: GameRequestModel) -> EventAGen:
        try:
            yield await self.frameworks[0].response(GameResponseModel([FEN.starting()], [], "1-0"))
        except RequestError as ex:
            yield await self.frameworks[0].response(
                RequestErrorResponseModel(
                    f"An error occurred while requesting {ex.request.url!r}: {ex.args[0]!r}",
                    "request.RequestError",
                )
            )
        except HTTPStatusError as ex:
            yield await self.frameworks[0].response(
                HTTPStatusErrorResponseModel(
                    f"Error response {ex.response.status_code} "
                    + f"while requesting {ex.request.url!r}: {ex.response.json()!r}",
                    "request.HTTPStatusError",
                )
            )
