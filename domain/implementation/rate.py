# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Iterable, NamedTuple

from domain.implementation.movement import FEN, SAN, Movement
from domain.implementation.status import Status

from .trace import InfiniteTraceProducable, ProducableTrace, Trace


class IRate(metaclass=ABCMeta):
    @abstractmethod
    async def produced(self, playtime: int) -> Iterable[Trace]:
        pass


class RateData(NamedTuple):
    producable: ProducableTrace


class Rate(RateData, IRate):
    @classmethod
    def from_urls(cls, url_env: str, url_ai_white: str, url_ai_black: str) -> Rate:
        return Rate(
            ProducableTrace(
                Status(url_env),
                Movement(url_env, url_ai_white),
                Movement(url_env, url_ai_black),
                InfiniteTraceProducable(),
            ),
        )

    async def produced(self, playtime: int) -> Iterable[Trace]:
        return (await self.producable.produced([FEN.starting()]) for _ in range(playtime))


class FakeRate(IRate):
    async def produced(self, playtime: int) -> Iterable[Trace]:
        return [
            Trace([[FEN.starting()]], [[]], [[1]]),
            Trace([[FEN.starting()]], [[]], [[0.5]]),
            Trace([[FEN.starting(), FEN.first()]], [[]], [[0, 1]]),
        ]
