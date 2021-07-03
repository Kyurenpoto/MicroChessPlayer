# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import NamedTuple

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
    async def executed(self) -> GameResponseModel:
        pass


class GameData(NamedTuple):
    request_model: GameRequestModel


class Game(GameData, IGame):
    async def executed(self) -> GameResponseModel:
        return ResultTrace._make(
            await ProducableTrace(
                Status(self.request_model.env),
                Movement(self.request_model.env, self.request_model.ai_white),
                Movement(self.request_model.env, self.request_model.ai_black),
                InfiniteTraceProducable(),
            ).produced([FEN.starting()])
        ).to_response()


class FakeGame(IGame):
    async def executed(self) -> GameResponseModel:
        return GameResponseModel([FEN.starting()], [], "1-0")
