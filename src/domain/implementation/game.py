# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import NamedTuple

from src.domain.implementation.movement import FEN, SAN, Movement
from src.domain.implementation.status import Status

from .trace import InfiniteTraceProducable, ProducableTrace, Trace


class IGame(metaclass=ABCMeta):
    @abstractmethod
    async def produced(self) -> Trace:
        pass


class GameData(NamedTuple):
    producable: ProducableTrace


class Game(GameData, IGame):
    @classmethod
    def from_urls(cls, url_env: str, url_ai_white: str, url_ai_black: str) -> Game:
        return Game(
            ProducableTrace(
                Status(url_env),
                Movement(url_env, url_ai_white),
                Movement(url_env, url_ai_black),
                InfiniteTraceProducable(),
            )
        )

    async def produced(self) -> Trace:
        return await self.producable.produced([FEN.starting()])


class FakeGame(IGame):
    async def produced(self) -> Trace:
        return Trace([[FEN.starting()]], [[]], [[1]])
