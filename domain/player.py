# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Iterable, NamedTuple

from domain.dto.playerdto import (
    PlayerAIMesurement,
    PlayerGameRequest,
    PlayerGameResponse,
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


class Results(list[float]):
    def __str__(self) -> str:
        if self[-1] == 0.5:
            return "1/2-1/2"

        return "1-0" if len(self) % 2 == 1 else "0-1"


class Statistics(dict[str, int]):
    @classmethod
    def from_traces(cls, traces: Iterable[Trace]) -> Statistics:
        results: list[str] = [str(Results(trace.results[0])) for trace in traces]

        return Statistics(
            {"1-0": results.count("1-0"), "0-1": results.count("0-1"), "1/2-1/2": results.count("1/2-1/2")}
        )

    def white(self) -> PlayerAIMesurement:
        return PlayerAIMesurement(
            score=(self["1-0"] + (self["1/2-1/2"] * 0.5)), win=self["1-0"], draw=self["1/2-1/2"], lose=self["0-1"]
        )

    def black(self) -> PlayerAIMesurement:
        return PlayerAIMesurement(
            score=(self["0-1"] + (self["1/2-1/2"] * 0.5)), win=self["0-1"], draw=self["1/2-1/2"], lose=self["1-0"]
        )


class MicroChessPlayer(NamedTuple):
    url_env: str
    service: IService

    @classmethod
    def from_url(cls, url_env: str) -> MicroChessPlayer:
        return MicroChessPlayer(url_env, Service())

    async def trajectory(self, request: PlayerTrajectoryRequest) -> PlayerTrajectoryResponse:
        produced: Trace = (
            await self.service.trajectory(self.url_env, request.white.url, request.black.url, request.step).produced(
                request.fens
            )
        ).concatenated()

        return PlayerTrajectoryResponse(fens=produced.fens, sans=produced.sans, results=produced.results)

    async def game(self, request: PlayerGameRequest) -> PlayerGameResponse:
        produced: Trace = await self.service.game(self.url_env, request.white.url, request.black.url).produced()

        return PlayerGameResponse(
            fens=produced.fens[0], sans=produced.sans[0], result=str(Results(produced.results[0]))
        )

    async def measurement(self, request: PlayerMeasurementRequest) -> PlayerMeasurementResponse:
        statistics: Statistics = Statistics.from_traces(
            await self.service.rate(self.url_env, request.white.url, request.black.url).produced(request.playtime)
        )

        return PlayerMeasurementResponse(white=statistics.white(), black=statistics.black())
