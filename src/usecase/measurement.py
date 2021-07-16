# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import NamedTuple

from httpx import HTTPStatusError, RequestError
from src.adapter.responseboundary import MeasurementResponseBoundary
from src.entity.enumerable import Mappable
from src.entity.movement import FEN, Movement
from src.entity.score import Score
from src.entity.status import Status
from src.entity.trace import InfiniteTraceProducable, ProducableTrace, Trace
from src.model.requestmodel import MeasurementRequestModel
from src.model.responsemodel import (
    HTTPStatusErrorResponseModel,
    MeasurementInfo,
    MeasurementResponseModel,
    RequestErrorResponseModel,
)


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


class IMeasurement(ABC):
    @abstractmethod
    async def executed(self, request_model: MeasurementRequestModel) -> None:
        pass


class MeasurementData(NamedTuple):
    response_boundary: MeasurementResponseBoundary


class Measurement(MeasurementData, IMeasurement):
    async def executed(self, request_model: MeasurementRequestModel) -> None:
        try:
            await self.response_boundary.response(
                Statistics.from_traces(
                    await ProducableTrace(
                        Status(request_model.env),
                        Movement(request_model.env, request_model.ai_white),
                        Movement(request_model.env, request_model.ai_black),
                        InfiniteTraceProducable(),
                    ).produced([FEN.starting()] * request_model.playtime)
                ).to_response()
            )
        except RequestError as ex:
            await self.response_boundary.response(
                RequestErrorResponseModel(
                    f"An error occurred while requesting {ex.request.url!r}: {ex.args[0]!r}",
                    "request.RequestError",
                )
            )
        except HTTPStatusError as ex:
            await self.response_boundary.response(
                HTTPStatusErrorResponseModel(
                    f"Error response {ex.response.status_code} "
                    + f"while requesting {ex.request.url!r}: {ex.response.json()!r}",
                    "request.HTTPStatusError",
                )
            )


class FakeMeasurement(MeasurementData, IMeasurement):
    async def executed(self, request_model: MeasurementRequestModel) -> None:
        await self.response_boundary.response(
            MeasurementResponseModel(MeasurementInfo(1.5, 1, 1, 1), MeasurementInfo(1.5, 1, 1, 1))
        )


class MeasurementFactory(ABC):
    @abstractmethod
    def createdMeasurement(self, response_boundary: MeasurementResponseBoundary) -> IMeasurement:
        pass


class NormalMeasurementFactory(MeasurementFactory):
    def createdMeasurement(self, response_boundary: MeasurementResponseBoundary) -> IMeasurement:
        return Measurement(response_boundary)


class FakeMeasurementFactory(MeasurementFactory):
    def createdMeasurement(self, response_boundary: MeasurementResponseBoundary) -> IMeasurement:
        return FakeMeasurement(response_boundary)
