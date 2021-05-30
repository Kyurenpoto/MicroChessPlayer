# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from domain.implementation.enumerable import Enumerable, Indexable, Mappable


class TestEnumerable:
    def test_filled(self) -> None:
        assert Enumerable.filled([], 5) == Enumerable([[]] * 5)

    def test_indice(self) -> None:
        assert Enumerable.indice(5) == Enumerable(list(range(5)))

    def test_to_indice(self) -> None:
        assert Enumerable(["a", "b", "c", "d", "e"]).to_indice() == Enumerable.indice(5)

    def test_to_odd_indice(self) -> None:
        assert Enumerable(["a", "b", "c", "d", "e"]).to_odd_indice() == Enumerable([1, 3])

    def test_to_even_indice(self) -> None:
        assert Enumerable(["a", "b", "c", "d", "e"]).to_even_indice() == Enumerable([0, 2, 4])

    def test_to_conditional_indice(self) -> None:
        assert Enumerable([0, 1, 2, 3, 4]).to_conditional_indice(lambda x: x % 2 == 1) == Enumerable([1, 3])


class TestMappable:
    def test_mapped(self) -> None:
        assert Mappable([0, 1, 2, 3, 4]).mapped(lambda x: x * 2) == Mappable([0, 2, 4, 6, 8])

    def test_wrapped(self) -> None:
        assert Mappable([0, 1, 2, 3, 4]).wrapped() == Mappable([[0], [1], [2], [3], [4]])

    def test_replaced(self) -> None:
        assert Mappable([0, 1, 2, 3, 4]).replaced({2: 6, 1: 5}) == Mappable([0, 5, 6, 3, 4])

    def test_replaced_with_disjoint(self) -> None:
        assert Mappable(Enumerable.filled(0, 5)).replaced_with_disjoint(
            [([1, 2], [1, 2]), ([3, 4], [3, 4])]
        ) == Mappable([0, 1, 2, 3, 4])

    def test_concatenated(self) -> None:
        assert Mappable.concatenated([[2, 3], [0, 1]]) == Mappable([2, 3, 0, 1])

    def test_indice_to_disjoint(self) -> None:
        assert list(Mappable.indice_to_disjoint([([1, 2], lambda x: x), ([3, 4], lambda x: x)])) == [
            ([1, 2], [1, 2]),
            ([3, 4], [3, 4]),
        ]

    def test_disjoint_to_replace_map(self) -> None:
        assert Mappable.disjoint_to_replace_map([([1, 2], [1, 2]), ([3, 4], [3, 4])]) == {1: 1, 2: 2, 3: 3, 4: 4}

    def test_disjoint_unioned(self) -> None:
        assert Mappable.disjoint_unioned(0, 5, [([1, 2], [1, 2]), ([3, 4], [3, 4])]) == Mappable([0, 1, 2, 3, 4])

    def test_mapped_with_others(self) -> None:
        assert Mappable.mapped_with_others(([0, 1], [0, 1], [0, 1]), lambda x, y, z: x + y + z) == Mappable([0, 3])


class TestIndexable:
    def test_indexed(self) -> None:
        assert Indexable([0, 1, 2, 3, 4]).indexed([1, 3, 5, -1]) == Indexable([1, 3])

    def test_odd_indexed(self) -> None:
        assert Indexable([0, 1, 2, 3, 4]).odd_indexed() == Indexable([1, 3])

    def test_even_indexed(self) -> None:
        assert Indexable([0, 1, 2, 3, 4]).even_indexed() == Indexable([0, 2, 4])

    def test_conditional_indexed(self) -> None:
        assert Indexable([0, 1, 2, 3, 4]).conditional_indexed(lambda x: x % 2 == 1) == Indexable([1, 3])
