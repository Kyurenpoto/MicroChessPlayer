# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from itertools import chain
from typing import Callable, Iterable


class Enumerable(list):
    def mapped(self, mapper: Callable) -> Enumerable:
        return Enumerable(map(mapper, self))

    def indexed(self, indice: Iterable[int]) -> Enumerable:
        return Enumerable(filter(lambda x: x < len(self), indice)).mapped(lambda i: self[i])

    def wrapped(self) -> Enumerable:
        return Enumerable(self).mapped(lambda x: [x])

    def replaced(self, replace_map: dict) -> Enumerable:
        indice: set[int] = set(replace_map.keys())

        return Enumerable(range(0, len(self))).mapped(lambda i: replace_map[i] if i in indice else self[i])

    @classmethod
    def single_value_filled(cls, value, length: int) -> Enumerable:
        return Enumerable([value] * length)

    @classmethod
    def mapped_with_others(cls, target: Iterable[Iterable], mapper: Callable) -> Enumerable:
        return Enumerable(zip(*target)).mapped(lambda x: mapper(*x))

    @classmethod
    def disjoint_unioned(
        cls, value, length: int, indice_with_disjoint: Iterable[tuple[Iterable[int], Iterable]]
    ) -> Enumerable:
        return Enumerable.single_value_filled(value, length).replaced(
            dict(chain(*[zip(indice, disjoint) for indice, disjoint in indice_with_disjoint]))
        )
