# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import NamedTuple

from src.adapter.responseboundary import GameResponseBoundary
from src.domain.implementation.movement import FEN, Movement
from src.domain.implementation.score import Score
from src.domain.implementation.status import Status
from src.domain.implementation.trace import InfiniteTraceProducable, ProducableTrace, Trace
from src.usecase.requestmodel import GameRequestModel
from src.usecase.responsemodel import GameResponseModel


class ResultTrace(Trace):
    def to_response(self) -> GameResponseModel:
        return GameResponseModel(self.fens[0], self.sans[0], Score.from_results(self.results[0]))


class IGame(metaclass=ABCMeta):
    @abstractmethod
    async def executed(self, request_model: GameRequestModel) -> None:
        pass


class GameData(NamedTuple):
    response_boundary: GameResponseBoundary


class Game(GameData, IGame):
    async def executed(self, request_model: GameRequestModel) -> None:
        await self.response_boundary.response(
            ResultTrace._make(
                await ProducableTrace(
                    Status(request_model.env),
                    Movement(request_model.env, request_model.ai_white),
                    Movement(request_model.env, request_model.ai_black),
                    InfiniteTraceProducable(),
                ).produced([FEN.starting()])
            ).to_response()
        )


class FakeGame(GameData, IGame):
    async def executed(self, request_model: GameRequestModel) -> None:
        await self.response_boundary.response(GameResponseModel([FEN.starting()], [], "1-0"))
