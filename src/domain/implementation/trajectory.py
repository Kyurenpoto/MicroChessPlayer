# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import NamedTuple

from src.domain.implementation.movement import FEN, SAN, Movement
from src.domain.implementation.status import Status
from src.domain.implementation.trace import ColoredTrace, FiniteTraceProducable, ProducableTrace, Trace


class ITrajectory(metaclass=ABCMeta):
    @abstractmethod
    async def produced(self, fens: list[str]) -> ColoredTrace:
        pass


class TrajectoryData(NamedTuple):
    producable: ProducableTrace


class Trajectory(TrajectoryData, ITrajectory):
    @classmethod
    def from_urls_with_step(cls, url_env: str, url_ai_white: str, url_ai_black: str, step: int) -> Trajectory:
        return Trajectory(
            ProducableTrace(
                Status(url_env),
                Movement(url_env, url_ai_white),
                Movement(url_env, url_ai_black),
                FiniteTraceProducable(step),
            )
        )

    async def produced(self, fens: list[str]) -> ColoredTrace:
        return await self.producable.produced_with_spliting(fens)


class FakeTrajectory(ITrajectory):
    async def produced(self, fens: list[str]) -> ColoredTrace:
        return ColoredTrace(
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
        )
