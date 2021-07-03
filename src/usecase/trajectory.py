# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import NamedTuple

from src.domain.implementation.movement import FEN, SAN, Movement
from src.domain.implementation.status import Status
from src.domain.implementation.trace import ColoredTrace, FiniteTraceProducable, ProducableTrace, Trace
from src.usecase.requestmodel import TrajectoryRequestModel
from src.usecase.responsemodel import TrajectoryResponseModel


class ITrajectory(metaclass=ABCMeta):
    @abstractmethod
    async def executed(self) -> TrajectoryResponseModel:
        pass


class TrajectoryData(NamedTuple):
    request_model: TrajectoryRequestModel


class Trajectory(TrajectoryData, ITrajectory):
    async def executed(self) -> TrajectoryResponseModel:
        return TrajectoryResponseModel._make(
            (
                await ProducableTrace(
                    Status(self.request_model.env),
                    Movement(self.request_model.env, self.request_model.ai_white),
                    Movement(self.request_model.env, self.request_model.ai_black),
                    FiniteTraceProducable(self.request_model.step),
                ).produced_with_spliting(self.request_model.fens)
            ).concatenated()
        )


class FakeTrajectory(ITrajectory):
    async def executed(self) -> TrajectoryResponseModel:
        return TrajectoryResponseModel._make(
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
