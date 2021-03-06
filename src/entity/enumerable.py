# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

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

    def to_indice(self) -> Enumerable:
        return Enumerable.indice(len(self))

    def to_odd_indice(self) -> Enumerable:
        return Enumerable(range(1, len(self), 2))

    def to_even_indice(self) -> Enumerable:
        return Enumerable(range(0, len(self), 2))

    def to_conditional_indice(self, condition: Callable) -> Enumerable:
        return Enumerable(filter(lambda i: condition(self[i]), self.to_indice()))


class Mappable(list):
    @classmethod
    def concatenated(cls, target: Iterable[Iterable]) -> Mappable:
        return Mappable(chain(*target))

    @classmethod
    def indice_to_disjoint(
        cls, indice_with_mapper: Iterable[tuple[Iterable[int], Callable]]
    ) -> Iterable[tuple[Iterable[int], Iterable]]:
        return map(lambda x: (x[0], list(map(x[1], x[0]))), indice_with_mapper)

    @classmethod
    def disjoint_to_replace_map(cls, indice_with_disjoint: Iterable[tuple[Iterable[int], Iterable]]) -> dict:
        return dict(Mappable.concatenated(Mappable(indice_with_disjoint).mapped(lambda x: zip(*x))))

    @classmethod
    def disjoint_unioned(
        cls, value, length: int, indice_with_disjoint: Iterable[tuple[Iterable[int], Iterable]]
    ) -> Mappable:
        return Mappable(Enumerable.filled(value, length)).replaced_with_disjoint(indice_with_disjoint)

    @classmethod
    def mapped_with_others(cls, target: Iterable[Iterable], mapper: Callable) -> Mappable:
        return Mappable(zip(*target)).mapped(lambda x: mapper(*x))

    def mapped(self, mapper: Callable) -> Mappable:
        return Mappable(map(mapper, self))

    def wrapped(self) -> Mappable:
        return self.mapped(lambda x: [x])

    def replaced(self, replace_map: dict) -> Mappable:
        indice: set[int] = set(replace_map.keys())

        return Mappable(Enumerable(self).to_indice()).mapped(lambda i: replace_map[i] if i in indice else self[i])

    def replaced_with_disjoint(self, indice_with_disjoint: Iterable[tuple[Iterable[int], Iterable]]) -> Mappable:
        return self.replaced(Mappable.disjoint_to_replace_map(indice_with_disjoint))


class Indexable(list):
    def indexed(self, indice: Iterable[int]) -> Indexable:
        return Indexable(Mappable(filter(lambda x: 0 <= x < len(self), indice)).mapped(lambda i: self[i]))

    def odd_indexed(self) -> Indexable:
        return self.indexed(Enumerable(self).to_odd_indice())

    def even_indexed(self) -> Indexable:
        return self.indexed(Enumerable(self).to_even_indice())

    def conditional_indexed(self, condition: Callable) -> Indexable:
        return self.indexed(Enumerable(self).to_conditional_indice(condition))
