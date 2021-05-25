# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations, unicode_literals

from typing import Callable, Iterable, List, NamedTuple, Tuple

from .enumerable import Enumerable, Indexable, Mappable
from .movement import GeneratedMovementBase
from .status import GeneratedStatusBase


class Trace(NamedTuple):
    fens: List[List[str]]
    sans: List[List[str]]
    results: List[List[float]]

    @classmethod
    def from_fens(cls, fens: List[str]) -> Trace:
        return Trace(
            Mappable(fens).wrapped(),
            Enumerable.filled([], len(fens)),
            Enumerable.filled([], len(fens)),
        )

    @classmethod
    def cross_concatenated(cls, traces: list[tuple[Trace, Trace]]) -> tuple[Trace, Trace]:
        return (
            traces[0][0].concatenated(traces[1][1]),
            traces[1][0].concatenated(traces[0][1]),
        )

    def mapped(self, mapper: Callable) -> Trace:
        return Trace(*map(mapper, self))

    def inner_mapped(self, mapper: Callable) -> Trace:
        return self.mapped(lambda y: Mappable(y).mapped(mapper))

    def indexed(self, indice: Iterable[int]) -> Trace:
        return self.mapped(lambda x: Indexable(x).indexed(indice))

    def inner_odd_indexed(self) -> Trace:
        return self.inner_mapped(lambda x: Indexable(x).odd_indexed())

    def inner_even_indexed(self) -> Trace:
        return self.inner_mapped(lambda x: Indexable(x).even_indexed())

    def to_color_indice(self, color: str) -> Iterable[int]:
        return Enumerable(self.fens).to_conditional_indice(lambda x: x[0].split(" ")[1] == color)

    def colored(self, color: str) -> Trace:
        return self.indexed(Enumerable(self.fens).to_conditional_indice(lambda x: x[0].split(" ")[1] == color))

    def mapped_with(self, other: Trace, mapper: Callable) -> Trace:
        return Trace(*map(mapper, zip(self, other)))

    def moved(self, next_trace: Trace) -> Trace:
        return self.mapped_with(next_trace, lambda z: Mappable.mapped_with_others(z, lambda x, y: x + y))

    def concatenated(self, other: Trace) -> Trace:
        return self.mapped_with(other, lambda z: z[0] + z[1])

    def color_splited(self) -> tuple[Trace, Trace]:
        return self.colored("w"), self.colored("b")

    def inner_parity_splited(self) -> tuple[Trace, Trace]:
        return self.inner_even_indexed(), self.inner_odd_indexed()

    def splited_with_color_turn(self) -> tuple[Trace, Trace]:
        return Trace.cross_concatenated(list(map(lambda x: x.inner_parity_splited(), self.color_splited())))


class UnionedTrace:
    __slots__ = ["__trace1", "__trace2", "__indice1", "__indice2", "__next_indice1", "__next_indice2", "__length"]

    __trace1: Trace
    __trace2: Trace
    __indice1: List[int]
    __indice2: List[int]
    __next_indice1: List[int]
    __next_indice2: List[int]
    __length: int

    def __init__(
        self,
        trace1: Trace,
        trace2: Trace,
        indice1: List[int],
        indice2: List[int],
        next_indice1: List[int],
        next_indice2: List[int],
        length: int,
    ):
        self.__trace1 = trace1
        self.__trace2 = trace2
        self.__indice1 = indice1
        self.__indice2 = indice2
        self.__next_indice1 = next_indice1
        self.__next_indice2 = next_indice2
        self.__length = length

    def value(self) -> Trace:
        fens1, sans1, results1 = self.__trace1
        fens2, sans2, results2 = self.__trace2
        return Trace(
            Mappable.disjoint_unioned([], self.__length, [(self.__next_indice1, fens1), (self.__next_indice2, fens2)]),
            Mappable.disjoint_unioned([], self.__length, [(self.__next_indice1, sans1), (self.__next_indice2, sans2)]),
            Mappable.disjoint_unioned([], self.__length, [(self.__indice1, results1), (self.__indice2, results2)]),
        )


class NextIndice:
    __slots__ = ["__indice", "__results"]

    __indice: List[int]
    __results: List[float]

    def __init__(self, indice: List[int], results: List[float]):
        self.__indice = indice
        self.__results = results

    def value(self) -> List[int]:
        return Indexable(self.__indice).indexed(filter(lambda x: self.__results[x] == 0, range(len(self.__results))))


class NextTrace:
    __slots__ = ["__fens", "__indice", "__status", "__movement"]

    __fens: List[str]
    __indice: List[int]
    __status: GeneratedStatusBase
    __movement: GeneratedMovementBase

    def __init__(
        self, fens: List[str], indice: List[int], status: GeneratedStatusBase, movement: GeneratedMovementBase
    ):
        self.__fens = fens
        self.__indice = indice
        self.__status = status
        self.__movement = movement

    async def value(self) -> Tuple[Trace, List[int]]:
        if self.__indice == []:
            return Trace.from_fens([]), []

        results, legal_moves = await self.__status.value(self.__fens)
        next_indice: List[int] = NextIndice(list(range(len(self.__fens))), results).value()
        next_fens, next_sans = await self.__movement.value(Indexable(self.__fens).indexed(next_indice), legal_moves)

        return (
            Trace(Mappable(next_fens).wrapped(), Mappable(next_sans).wrapped(), Mappable(results).wrapped()),
            next_indice,
        )


class TwoColorMovedTrace:
    __slots__ = [
        "__trace",
        "__next_trace_white",
        "__next_trace_black",
        "__indice_white",
        "__indice_black",
        "__next_indice_white",
        "__next_indice_black",
        "__length",
    ]
    __trace: Trace
    __next_trace_white: Trace
    __next_trace_black: Trace
    __indice_white: List[int]
    __indice_black: List[int]
    __next_indice_white: List[int]
    __next_indice_black: List[int]
    __length: int

    def __init__(
        self,
        trace: Trace,
        next_trace_white: Trace,
        next_trace_black: Trace,
        indice_white: List[int],
        indice_black: List[int],
        next_indice_white: List[int],
        next_indice_black: List[int],
        length: int,
    ):
        self.__trace = trace
        self.__next_trace_white = next_trace_white
        self.__next_trace_black = next_trace_black
        self.__indice_white = indice_white
        self.__indice_black = indice_black
        self.__next_indice_white = next_indice_white
        self.__next_indice_black = next_indice_black
        self.__length = length

    def value(self) -> Trace:
        pass


class ProducedTrace:
    __slots__ = ["__step", "__fens", "__status", "__white", "__black"]

    __step: int
    __fens: List[str]
    __status: GeneratedStatusBase
    __white: GeneratedMovementBase
    __black: GeneratedMovementBase

    def __init__(
        self,
        step: int,
        fens: List[str],
        status: GeneratedStatusBase,
        white: GeneratedMovementBase,
        black: GeneratedMovementBase,
    ):
        self.__step = step
        self.__fens = fens
        self.__status = status
        self.__white = white
        self.__black = black

    async def value(self) -> Trace:
        length: int = len(self.__fens)
        trace: Trace = Trace.from_fens(self.__fens)
        indice_white: List[int] = list(trace.to_color_indice("w"))
        indice_black: List[int] = list(trace.to_color_indice("b"))
        fens_white: List[str] = Indexable(self.__fens).indexed(indice_white)
        fens_black: List[str] = Indexable(self.__fens).indexed(indice_black)

        for _ in range(self.__step):
            if indice_white == [] and indice_black == []:
                break

            next_trace_white, next_indice_white = await NextTrace(
                fens_white, indice_white, self.__status, self.__white
            ).value()
            next_trace_black, next_indice_black = await NextTrace(
                fens_black, indice_black, self.__status, self.__black
            ).value()

            # trace.move(
            #    *UnionedTrace(
            #        next_trace_white,
            #        next_trace_black,
            #        indice_white,
            #        indice_black,
            #        next_indice_white,
            #        next_indice_black,
            #        length,
            #    ).value()
            # )

            indice_white = next_indice_black
            indice_black = next_indice_white
            fens_white = Mappable(next_trace_black.fens).mapped(lambda x: x[0])
            fens_black = Mappable(next_trace_white.fens).mapped(lambda x: x[0])

        return trace
