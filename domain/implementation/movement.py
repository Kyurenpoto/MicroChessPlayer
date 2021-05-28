# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from abc import ABCMeta, abstractmethod
from typing import NamedTuple

from .nextfen import RequestedNextFEN
from .nextsan import RequestedNextSAN


class IMovement(metaclass=ABCMeta):
    @abstractmethod
    async def movement(self, fens: list[str], legal_moves: list[list[str]]) -> tuple[list[str], list[str]]:
        pass


class Movement(NamedTuple):
    url_env: str
    url_ai: str

    async def movement(self, fens: list[str], legal_moves: list[list[str]]) -> tuple[list[str], list[str]]:
        next_sans = await RequestedNextSAN.from_url_with_FENs_legal_moves(self.url_ai, fens, legal_moves)
        next_fens = await RequestedNextFEN.from_url_with_FENs_SANs(self.url_env, fens, next_sans)

        return next_fens, next_sans


class Fake(IMovement):
    async def movement(self, fens: list[str], legal_moves: list[list[str]]) -> tuple[list[str], list[str]]:
        return ["4knbr/4p3/7P/8/4RBNK/8/8/8 b Kk - 0 1"], ["h5h6"]
