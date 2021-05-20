# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from typing import Callable, List, Tuple

from .enumerable import IndexedList


class Trace:
    __slots__ = ["__fens", "__sans", "__results"]

    __fens: List[List[str]]
    __sans: List[List[str]]
    __results: List[List[float]]

    def __init__(self, fens: List[List[str]], sans: List[List[str]], results: List[List[float]]):
        self.__fens = fens
        self.__sans = sans
        self.__results = results

    @classmethod
    def from_fens(cls, fens: List[str]) -> Trace:
        return cls(fens=[[x] for x in fens], sans=([[]] * len(fens)), results=([[]] * len(fens)))

    def value(self) -> Tuple[List[List[str]], List[List[str]], List[List[float]]]:
        return self.__fens, self.__sans, self.__results

    def move(self, next_fens: List[List[str]], next_sans: List[List[str]], next_results: List[List[float]]) -> Trace:
        return Trace(
            self.__append(self.__fens, next_fens),
            self.__append(self.__sans, next_sans),
            self.__append(self.__results, next_results),
        )

    def __append(self, oldlist: List[List], newlist: List[List]) -> List[List]:
        return [old_x + new_x for old_x, new_x in zip(oldlist, newlist)]


class IndexedTrace:
    __slots__ = ["__trace", "__indice"]

    __trace: Trace
    __indice: List[int]

    def __init__(self, trace: Trace, indice: List[int]):
        self.__trace = trace
        self.__indice = indice

    def value(self) -> Trace:
        fens, sans, results = self.__trace.value()

        return Trace(*map(lambda x: IndexedList(x, self.__indice).value(), [fens, sans + [[]], results]))


class ColoredTrace:
    __slots__ = ["__trace", "__color"]

    __trace: Trace
    __color: str

    def __init__(self, trace: Trace, color: str):
        self.__trace = trace
        self.__color = color

    def value(self) -> Trace:
        fens, _, _ = self.__trace.value()
        indice = list(filter(lambda x: fens[x][0].split(" ")[1] == self.__color, range(len(fens))))

        return IndexedTrace(self.__trace, indice).value()


class SplitedTrace:
    __slots__ = ["__trace"]

    __trace: Trace

    def __init__(self, trace: Trace):
        self.__trace = trace

    def value(self) -> Tuple[Trace, Trace]:
        splited = Trace(*map(lambda x: self.__split(x), self.__trace.value()))

        return (
            ColoredTrace(splited, "w").value(),
            ColoredTrace(splited, "b").value(),
        )

    def __split(self, target: List[List]) -> List[List]:
        return self.__selected(target, lambda x: range(0, len(x), 2)) + self.__selected(
            target, lambda x: range(1, len(x), 2)
        )

    def __selected(self, target: List[List], where: Callable[[List], range]) -> List[List]:
        return list(filter(lambda x: x != [], [IndexedList(x, list(where(x))).value() for x in target]))


def next_indice(indice: List[int], results: List[float]) -> List[int]:
    return [indice[x] for x in filter(lambda x: results[x] == 0, range(len(results)))]


class GeneratedTrace:
    __slots__ = ["__step", "__fens", "__env", "__white", "__black"]

    __step: int
    __fens: List[str]
    __url_env: str
    __url_white: str
    __url_black: str

    def __init__(self, step: int, fens: List[str], url_env: str, url_white: str, url_black: str):
        self.__step = step
        self.__fens = fens
        self.__url_env = url_env
        self.__url_white = url_white
        self.__url_black = url_black

    def value(self) -> Trace:
        indice = range(len(self.__fens))
        trace = Trace.from_fens(self.__fens)

        return trace
