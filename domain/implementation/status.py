# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from abc import ABCMeta, abstractmethod
from enum import Enum, auto

from .enumerable import Mappable
from .fenstatus import RequestedFENStatus


class IStatus(metaclass=ABCMeta):
    @abstractmethod
    async def status(self, fens: list[str]) -> tuple[list[float], list[list[str]]]:
        pass


class MicroBoardStatus(Enum):
    NONE = auto()
    CHECKMATE = auto()
    STALEMATE = auto()
    INSUFFICIENT_MATERIAL = auto()
    FIFTY_MOVES = auto()

    def to_result(self) -> float:
        if self == MicroBoardStatus.NONE:
            return 0
        if self == MicroBoardStatus.CHECKMATE:
            return 1

        return 0.5


class Status(str, IStatus):
    async def status(self, fens: list[str]) -> tuple[list[float], list[list[str]]]:
        statuses, legal_moves = await RequestedFENStatus.from_url_with_FENs(self, fens)

        return Mappable(statuses).mapped(lambda x: MicroBoardStatus(x).to_result()), legal_moves


class Fake(IStatus):
    async def status(self, fens: list[str]) -> tuple[list[float], list[list[str]]]:
        return [0], [
            [
                "e4e5",
                "e4e6",
                "e4e7",
                "f4e5",
                "f4g5",
                "f4h6",
                "g4e5",
                "g4f6",
                "g4h6",
                "h4g5",
                "h5h6",
            ]
        ]
