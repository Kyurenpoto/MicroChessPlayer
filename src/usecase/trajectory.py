# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import NamedTuple

from src.adapter.responseboundary import TrajectoryResponseBoundary
from src.domain.implementation.movement import FEN, SAN, Movement
from src.domain.implementation.status import Status
from src.domain.implementation.trace import ColoredTrace, FiniteTraceProducable, ProducableTrace, Trace
from src.usecase.requestmodel import TrajectoryRequestModel
from src.usecase.responsemodel import TrajectoryResponseModel


class ITrajectory(metaclass=ABCMeta):
    @abstractmethod
    async def executed(self, request_model: TrajectoryRequestModel) -> None:
        pass


class TrajectoryData(NamedTuple):
    response_boundary: TrajectoryResponseBoundary


class Trajectory(TrajectoryData, ITrajectory):
    async def executed(self, request_model: TrajectoryRequestModel) -> None:
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


class TrajectoryFactory(metaclass=ABCMeta):
    @abstractmethod
    def createdTrajectory(self, response_boundary: TrajectoryResponseBoundary) -> ITrajectory:
        pass


class NormalTrajectoryFactory(TrajectoryFactory):
    def createdTrajectory(self, response_boundary: TrajectoryResponseBoundary) -> ITrajectory:
        return Trajectory(response_boundary)


class FakeTrajectoryFactory(TrajectoryFactory):
    def createdTrajectory(self, response_boundary: TrajectoryResponseBoundary) -> ITrajectory:
        return FakeTrajectory(response_boundary)
