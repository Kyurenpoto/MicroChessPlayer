# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from typing import NamedTuple

from domain.implementation.movement import Movement
from domain.implementation.status import Status

from .trace import ColoredTrace, FiniteTraceProducable, ProducableTrace


class Trajectory(NamedTuple):
    producable: ProducableTrace

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
