# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from domain.implementation.enumerable import Enumerable, Indexable, Mappable


def test_enumerable_filled() -> None:
    assert Enumerable.filled([], 5) == Enumerable([[]] * 5)


def test_enumerable_indice() -> None:
    assert Enumerable.indice(5) == Enumerable(list(range(5)))


def test_enumerable_to_indice() -> None:
    assert Enumerable(["a", "b", "c", "d", "e"]).to_indice() == Enumerable.indice(5)


def test_enumerable_to_odd_indice() -> None:
    assert Enumerable(["a", "b", "c", "d", "e"]).to_odd_indice() == Enumerable([1, 3])


def test_enumerable_to_even_indice() -> None:
    assert Enumerable(["a", "b", "c", "d", "e"]).to_even_indice() == Enumerable([0, 2, 4])


def test_enumerable_to_conditional_indice() -> None:
    assert Enumerable([0, 1, 2, 3, 4]).to_conditional_indice(lambda x: x % 2 == 1) == Enumerable([1, 3])


def test_mappable_mapped() -> None:
    assert Mappable([0, 1, 2, 3, 4]).mapped(lambda x: x * 2) == Mappable([0, 2, 4, 6, 8])


def test_mappable_wrapped() -> None:
    assert Mappable([0, 1, 2, 3, 4]).wrapped() == Mappable([[0], [1], [2], [3], [4]])


def test_mappable_replaced() -> None:
    assert Mappable([0, 1, 2, 3, 4]).replaced({2: 6, 1: 5}) == Mappable([0, 5, 6, 3, 4])


def test_mappable_concatenated() -> None:
    assert Mappable.concatenated([[2, 3], [0, 1]]) == Mappable([2, 3, 0, 1])


def test_mappable_disjoint_unioned() -> None:
    assert Mappable.disjoint_unioned(0, 5, [([1, 2], [1, 2]), ([3, 4], [3, 4])]) == Mappable([0, 1, 2, 3, 4])


def test_mappable_mapped_with_others() -> None:
    assert Mappable.mapped_with_others(([0, 1], [0, 1], [0, 1]), lambda x, y, z: x + y + z) == Mappable([0, 3])


def test_indexable_indexed() -> None:
    assert Indexable([0, 1, 2, 3, 4]).indexed([1, 3, 5, -1]) == Indexable([1, 3])


def test_indexable_odd_indexed() -> None:
    assert Indexable([0, 1, 2, 3, 4]).odd_indexed() == Indexable([1, 3])


def test_indexable_even_indexed() -> None:
    assert Indexable([0, 1, 2, 3, 4]).even_indexed() == Indexable([0, 2, 4])


def test_indexable_conditioned() -> None:
    assert Indexable([0, 1, 2, 3, 4]).conditioned(lambda x: x % 2 == 1) == Indexable([1, 3])
