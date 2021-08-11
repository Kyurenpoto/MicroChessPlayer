# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from enum import Enum, auto


class Color(Enum):
    WHITE = auto()
    BLACK = auto()

    def opposite(self) -> Color:
        return {Color.WHITE: Color.BLACK, Color.BLACK: Color.WHITE}[self]


class FEN(str):
    @classmethod
    def end(cls, color: Color) -> FEN:
        return FEN("8/8/8/8/8/8/8/8 " + {Color.WHITE: "w", Color.BLACK: "b"}[color] + " - - 0 1")

    def color(self) -> Color:
        return {"w": Color.WHITE, "b": Color.BLACK}[self.split(" ")[1]]


class SAN(str):
    pass


class Status(Enum):
    NONE = auto()
    CHECKMATED = auto()
    STALEMATED = auto()
    INSUFFICIENT_MATERIAL = auto()
    FIFTY_MOVES = auto()


class Reward(float):
    @classmethod
    def from_status(cls, status: Status) -> Reward:
        if status == Status.NONE:
            return Reward(0)
        if status == Status.CHECKMATED:
            return Reward(1)

        return Reward(0.5)

    def opposite(self) -> Reward:
        return Reward(1 - self)

    def with_opposite(self) -> list[Reward]:
        return [self.opposite(), self]
