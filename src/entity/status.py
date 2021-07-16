# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto

from src.entity.enumerable import Mappable
from src.entity.fenstatus import RequestedFENStatus


class IStatus(ABC):
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
        if len(fens) == 0:
            return [], []

        statuses, legal_moves = await RequestedFENStatus.from_url_with_FENs(self, fens)

        return Mappable(statuses).mapped(lambda x: MicroBoardStatus(x).to_result()), legal_moves


class FakeStatus(IStatus):
    async def status(self, fens: list[str]) -> tuple[list[float], list[list[str]]]:
        return [0] * len(fens), [
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
        ] * len(fens)


@dataclass
class FakeFinitePrefixStatus(IStatus):
    rest_prefix: int = 0

    async def status(self, fens: list[str]) -> tuple[list[float], list[list[str]]]:
        if self.rest_prefix != 0:
            self.rest_prefix -= 1
            return await FakeStatus().status(fens)

        return self.after_prefix(fens)

    @abstractmethod
    def after_prefix(self, fens: list[str]) -> tuple[list[float], list[list[str]]]:
        pass


class FakeCheckmateStatus(FakeFinitePrefixStatus):
    def after_prefix(self, fens: list[str]) -> tuple[list[float], list[list[str]]]:
        return [1] * len(fens), [[]] * len(fens)


class FakeStalemateStatus(FakeFinitePrefixStatus):
    def after_prefix(self, fens: list[str]) -> tuple[list[float], list[list[str]]]:
        return [0.5] * len(fens), [[]] * len(fens)
