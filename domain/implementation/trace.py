# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations, unicode_literals

from typing import Callable, List, NamedTuple, Tuple

from .enumerable import Enumerable
from .movement import GeneratedMovementBase
from .status import GeneratedStatusBase


class Trace(NamedTuple):
    fens: List[List[str]]
    sans: List[List[str]]
    results: List[List[float]]

    @classmethod
    def from_fens(cls, fens: List[str]) -> Trace:
        return Trace(
            Enumerable(fens).wrapped(),
            Enumerable.single_value_filled([], len(fens)),
            Enumerable.single_value_filled([], len(fens)),
        )

    def mapped(self, mapper: Callable) -> Trace:
        return Trace(*map(mapper, self))

    def mapped_with(self, other: Trace, mapper: Callable) -> Trace:
        return Trace(*map(mapper, zip(self, other)))

    def moved(self, next_trace: Trace) -> Trace:
        return self.mapped_with(next_trace, lambda z: Enumerable.mapped_with_others(z, lambda x, y: x + y))


class IndexedTrace:
    __slots__ = ["__trace", "__indice"]

    __trace: Trace
    __indice: List[int]

    def __init__(self, trace: Trace, indice: List[int]):
        self.__trace = trace
        self.__indice = indice

    def value(self) -> Trace:
        return Trace(
            *map(
                lambda x: Enumerable(x).indexed(self.__indice),
                [self.__trace.fens, self.__trace.sans + [[]], self.__trace.results],
            )
        )


class ColoredIndice:
    __slots__ = ["__fens", "__color"]

    __fens: List[List[str]]
    __color: str

    def __init__(self, fens: List[List[str]], color: str):
        self.__fens = fens
        self.__color = color

    def value(self) -> List[int]:
        return list(filter(lambda x: self.__fens[x][0].split(" ")[1] == self.__color, range(len(self.__fens))))


class ColoredTrace:
    __slots__ = ["__trace", "__color"]

    __trace: Trace
    __color: str

    def __init__(self, trace: Trace, color: str):
        self.__trace = trace
        self.__color = color

    def value(self) -> Trace:
        return IndexedTrace(self.__trace, ColoredIndice(self.__trace.fens, self.__color).value()).value()


class SplitedTrace:
    __slots__ = ["__trace"]

    __trace: Trace

    def __init__(self, trace: Trace):
        self.__trace = trace

    def value(self) -> Tuple[Trace, Trace]:
        splited = Trace(*map(lambda x: self.__split(x), self.__trace))

        return (
            ColoredTrace(splited, "w").value(),
            ColoredTrace(splited, "b").value(),
        )

    def __split(self, target: List[List]) -> List[List]:
        return self.__selected(target, lambda x: range(0, len(x), 2)) + self.__selected(
            target, lambda x: range(1, len(x), 2)
        )

    def __selected(self, target: List[List], where: Callable[[List], range]) -> List[List]:
        return list(filter(lambda x: x != [], [Enumerable(x).indexed(where(x)) for x in target]))


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
        Enumerable.disjoint_unioned([], self.__length, [(self.__next_indice1, fens1), (self.__next_indice2, fens2)])
        return Trace(
            Enumerable.disjoint_unioned(
                [], self.__length, [(self.__next_indice1, fens1), (self.__next_indice2, fens2)]
            ),
            Enumerable.disjoint_unioned(
                [], self.__length, [(self.__next_indice1, sans1), (self.__next_indice2, sans2)]
            ),
            Enumerable.disjoint_unioned([], self.__length, [(self.__indice1, results1), (self.__indice2, results2)]),
        )


class NextIndice:
    __slots__ = ["__indice", "__results"]

    __indice: List[int]
    __results: List[float]

    def __init__(self, indice: List[int], results: List[float]):
        self.__indice = indice
        self.__results = results

    def value(self) -> List[int]:
        return Enumerable(self.__indice).indexed(filter(lambda x: self.__results[x] == 0, range(len(self.__results))))


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
        next_fens, next_sans = await self.__movement.value(Enumerable(self.__fens).indexed(next_indice), legal_moves)

        return (
            Trace(Enumerable(next_fens).wrapped(), Enumerable(next_sans).wrapped(), Enumerable(results).wrapped()),
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
        indice_white: List[int] = ColoredIndice(trace.fens, "w").value()
        indice_black: List[int] = ColoredIndice(trace.fens, "b").value()
        fens_white: List[str] = Enumerable(self.__fens).indexed(indice_white)
        fens_black: List[str] = Enumerable(self.__fens).indexed(indice_black)

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
            fens_white = Enumerable(next_trace_black.fens).mapped(lambda x: x[0])
            fens_black = Enumerable(next_trace_white.fens).mapped(lambda x: x[0])

        return trace
