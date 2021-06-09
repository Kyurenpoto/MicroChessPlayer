# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Iterable, NamedTuple

from domain.dto.playerdto import (
    PlayerAIMeasurement,
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerHAL,
    PlayerInternalModel,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from domain.implementation.game import FakeGame, Game, IGame
from domain.implementation.measurement import FakeMeasurement, IMeasurement, Measurement
from domain.implementation.trace import Trace
from domain.implementation.trajectory import FakeTrajectory, ITrajectory, Trajectory


class IService(metaclass=ABCMeta):
    @abstractmethod
    def trajectory(self, url_env: str, url_ai_white: str, url_ai_black: str, step: int) -> ITrajectory:
        pass

    @abstractmethod
    def game(self, url_env: str, url_ai_white: str, url_ai_black: str) -> IGame:
        pass

    @abstractmethod
    def rate(self, url_env: str, url_ai_white: str, url_ai_black: str) -> IMeasurement:
        pass


class Service(IService):
    def trajectory(self, url_env: str, url_ai_white: str, url_ai_black: str, step: int) -> ITrajectory:
        return Trajectory.from_urls_with_step(url_env, url_ai_white, url_ai_black, step)

    def game(self, url_env: str, url_ai_white: str, url_ai_black: str) -> IGame:
        return Game.from_urls(url_env, url_ai_white, url_ai_black)

    def rate(self, url_env: str, url_ai_white: str, url_ai_black: str) -> IMeasurement:
        return Measurement.from_urls(url_env, url_ai_white, url_ai_black)


class FakeService(IService):
    def trajectory(self, url_env: str, url_ai_white: str, url_ai_black: str, step: int) -> ITrajectory:
        return FakeTrajectory()

    def game(self, url_env: str, url_ai_white: str, url_ai_black: str) -> IGame:
        return FakeGame()

    def rate(self, url_env: str, url_ai_white: str, url_ai_black: str) -> IMeasurement:
        return FakeMeasurement()


class Score(str):
    @classmethod
    def from_results(cls, results: list[float]) -> Score:
        if results[-1] == 0.5:
            return Score.draw()

        return Score.white_win() if len(results) % 2 == 1 else Score.black_win()

    @classmethod
    def white_win(cls) -> Score:
        return Score("1-0")

    @classmethod
    def black_win(cls) -> Score:
        return Score("0-1")

    @classmethod
    def draw(cls) -> Score:
        return Score("1/2-1/2")


class Statistics(dict[Score, int]):
    @classmethod
    def from_traces(cls, traces: Iterable[Trace]) -> Statistics:
        results: list[Score] = [Score.from_results(trace.results[0]) for trace in traces]

        return Statistics(
            {
                Score.white_win(): results.count(Score.white_win()),
                Score.black_win(): results.count(Score.black_win()),
                Score.draw(): results.count(Score.draw()),
            }
        )

    def white(self) -> PlayerAIMeasurement:
        return PlayerAIMeasurement(
            score=(self[Score.white_win()] + (self[Score.draw()] * 0.5)),
            win=self[Score.white_win()],
            draw=self[Score.draw()],
            lose=self[Score.black_win()],
        )

    def black(self) -> PlayerAIMeasurement:
        return PlayerAIMeasurement(
            score=(self[Score.black_win()] + (self[Score.draw()] * 0.5)),
            win=self[Score.black_win()],
            draw=self[Score.draw()],
            lose=self[Score.white_win()],
        )


class MicroChessPlayer(NamedTuple):
    service: IService

    @classmethod
    def from_url(cls) -> MicroChessPlayer:
        return MicroChessPlayer(Service())

    async def trajectory(
        self, request: PlayerTrajectoryRequest, internal_model: PlayerInternalModel, name: str, method: str
    ) -> PlayerTrajectoryResponse:
        produced: Trace = (
            await self.service.trajectory(
                internal_model.url_env, request.white.url, request.black.url, request.step
            ).produced(request.fens)
        ).concatenated()

        return PlayerTrajectoryResponse(
            links=PlayerHAL.from_apis_with_requested(internal_model.routes, name, method).links,
            fens=produced.fens,
            sans=produced.sans,
            results=produced.results,
        )

    async def game(
        self, request: PlayerGameRequest, internal_model: PlayerInternalModel, name: str, method: str
    ) -> PlayerGameResponse:
        produced: Trace = await self.service.game(
            internal_model.url_env, request.white.url, request.black.url
        ).produced()

        return PlayerGameResponse(
            links=PlayerHAL.from_apis_with_requested(internal_model.routes, name, method).links,
            fens=produced.fens[0],
            sans=produced.sans[0],
            result=Score.from_results(produced.results[0]),
        )

    async def measurement(
        self, request: PlayerMeasurementRequest, internal_model: PlayerInternalModel, name: str, method: str
    ) -> PlayerMeasurementResponse:
        statistics: Statistics = Statistics.from_traces(
            await self.service.rate(internal_model.url_env, request.white.url, request.black.url).produced(
                request.playtime
            )
        )

        return PlayerMeasurementResponse(
            links=PlayerHAL.from_apis_with_requested(internal_model.routes, name, method).links,
            white=statistics.white(),
            black=statistics.black(),
        )
