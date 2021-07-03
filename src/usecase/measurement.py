# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import NamedTuple

from src.domain.implementation.enumerable import Mappable
from src.domain.implementation.movement import FEN, Movement
from src.domain.implementation.score import Score
from src.domain.implementation.status import Status
from src.domain.implementation.trace import InfiniteTraceProducable, ProducableTrace, Trace
from src.usecase.requestmodel import MeasurementRequestModel
from src.usecase.responsemodel import MeasurementInfo, MeasurementResponseModel


class Statistics(dict[Score, int]):
    @classmethod
    def from_traces(cls, trace: Trace) -> Statistics:
        results: list[Score] = Mappable(trace.results).mapped(lambda x: Score.from_results(x))

        return Statistics(
            {
                Score.white_win(): results.count(Score.white_win()),
                Score.black_win(): results.count(Score.black_win()),
                Score.draw(): results.count(Score.draw()),
            }
        )

    def white(self) -> MeasurementInfo:
        return MeasurementInfo(
            score=(self[Score.white_win()] + (self[Score.draw()] * 0.5)),
            win=self[Score.white_win()],
            draw=self[Score.draw()],
            lose=self[Score.black_win()],
        )

    def black(self) -> MeasurementInfo:
        return MeasurementInfo(
            score=(self[Score.black_win()] + (self[Score.draw()] * 0.5)),
            win=self[Score.black_win()],
            draw=self[Score.draw()],
            lose=self[Score.white_win()],
        )

    def to_response(self) -> MeasurementResponseModel:
        return MeasurementResponseModel(self.white(), self.black())


class IMeasurement(metaclass=ABCMeta):
    @abstractmethod
    async def executed(self) -> MeasurementResponseModel:
        pass


class MeasurementData(NamedTuple):
    request_model: MeasurementRequestModel


class Measurement(MeasurementData, IMeasurement):
    async def executed(self) -> MeasurementResponseModel:
        return Statistics.from_traces(
            await ProducableTrace(
                Status(self.request_model.env),
                Movement(self.request_model.env, self.request_model.ai_white),
                Movement(self.request_model.env, self.request_model.ai_black),
                InfiniteTraceProducable(),
            ).produced([FEN.starting()] * self.request_model.playtime)
        ).to_response()


class FakeMeasurement(IMeasurement):
    async def executed(self) -> MeasurementResponseModel:
        return MeasurementResponseModel(MeasurementInfo(1.5, 1, 1, 1), MeasurementInfo(1.5, 1, 1, 1))
