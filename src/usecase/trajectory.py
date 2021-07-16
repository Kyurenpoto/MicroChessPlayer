# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import NamedTuple

from httpx import HTTPStatusError, RequestError
from src.adapter.responseboundary import TrajectoryResponseBoundary
from src.entity.movement import FEN, SAN, Movement
from src.entity.status import Status
from src.entity.trace import ColoredTrace, FiniteTraceProducable, ProducableTrace, Trace
from src.model.requestmodel import TrajectoryRequestModel
from src.model.responsemodel import HTTPStatusErrorResponseModel, RequestErrorResponseModel, TrajectoryResponseModel


class ITrajectory(ABC):
    @abstractmethod
    async def executed(self, request_model: TrajectoryRequestModel) -> None:
        pass


class TrajectoryData(NamedTuple):
    response_boundary: TrajectoryResponseBoundary


class Trajectory(TrajectoryData, ITrajectory):
    async def executed(self, request_model: TrajectoryRequestModel) -> None:
        try:
            await self.response_boundary.response(
                TrajectoryResponseModel._make(
                    (
                        await ProducableTrace(
                            Status(request_model.env),
                            Movement(request_model.env, request_model.ai_white),
                            Movement(request_model.env, request_model.ai_black),
                            FiniteTraceProducable(request_model.step),
                        ).produced_with_spliting(request_model.fens)
                    ).concatenated()
                )
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


class FakeTrajectory(TrajectoryData, ITrajectory):
    async def executed(self, request_model: TrajectoryRequestModel) -> None:
        await self.response_boundary.response(
            TrajectoryResponseModel._make(
                ColoredTrace(
                    Trace(
                        [[FEN.starting(), FEN.starting()], [FEN.starting(), FEN.starting()]],
                        [[SAN.first()], [SAN.first()]],
                        [[0, 0], [0, 0]],
                    ),
                    Trace(
                        [[FEN.first(), FEN.first()], [FEN.first(), FEN.first()]],
                        [[SAN.first()], [SAN.first()]],
                        [[0, 0], [0, 0]],
                    ),
                ).concatenated()
            )
        )


class TrajectoryFactory(ABC):
    @abstractmethod
    def createdTrajectory(self, response_boundary: TrajectoryResponseBoundary) -> ITrajectory:
        pass


class NormalTrajectoryFactory(TrajectoryFactory):
    def createdTrajectory(self, response_boundary: TrajectoryResponseBoundary) -> ITrajectory:
        return Trajectory(response_boundary)


class FakeTrajectoryFactory(TrajectoryFactory):
    def createdTrajectory(self, response_boundary: TrajectoryResponseBoundary) -> ITrajectory:
        return FakeTrajectory(response_boundary)
