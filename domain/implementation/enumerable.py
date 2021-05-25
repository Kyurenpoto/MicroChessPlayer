# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from itertools import chain
from typing import Callable, Iterable


class Enumerable(list):
    @classmethod
    def filled(cls, value, length: int) -> Enumerable:
        return Enumerable([value] * length)

    @classmethod
    def indice(cls, length: int) -> Enumerable:
        return Enumerable(range(length))

    @classmethod
    def mapped_with_others(cls, target: Iterable[Iterable], mapper: Callable) -> Enumerable:
        return Enumerable(zip(*target)).mapped(lambda x: mapper(*x))

    @classmethod
    def disjoint_unioned(
        cls, value, length: int, indice_with_disjoint: Iterable[tuple[Iterable[int], Iterable]]
    ) -> Enumerable:
        return Enumerable.filled(value, length).replaced(
            dict(chain(*[zip(indice, disjoint) for indice, disjoint in indice_with_disjoint]))
        )

    def to_indice(self) -> Enumerable:
        return Enumerable.indice(len(self))

    def to_odd_indice(self) -> Enumerable:
        return Enumerable(range(1, len(self), 2))

    def to_even_indice(self) -> Enumerable:
        return Enumerable(range(0, len(self), 2))

    def to_conditional_indice(self, condition: Callable) -> Enumerable:
        return Enumerable(filter(lambda i: condition(self[i]), self.to_indice()))

    def mapped(self, mapper: Callable) -> Enumerable:
        return Enumerable(map(mapper, self))

    def indexed(self, indice: Iterable[int]) -> Enumerable:
        return Enumerable(filter(lambda x: x < len(self), indice)).mapped(lambda i: self[i])

    def odd_indexed(self) -> Enumerable:
        return self.indexed(self.to_odd_indice())

    def even_indexed(self) -> Enumerable:
        return self.indexed(self.to_even_indice())

    def conditioned(self, condition: Callable) -> Enumerable:
        return self.indexed(self.to_conditional_indice(condition))

    def wrapped(self) -> Enumerable:
        return Enumerable(self).mapped(lambda x: [x])

    def replaced(self, replace_map: dict) -> Enumerable:
        indice: set[int] = set(replace_map.keys())

        return self.to_indice().mapped(lambda i: replace_map[i] if i in indice else self[i])
