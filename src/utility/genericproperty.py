# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod
from typing import Any, Callable, NamedTuple


class Property(NamedTuple):
    property: Callable[[Any], bool]

    def verify(self, target: Any) -> None:
        assert self.property(target)


class GenericProperty(ABC):
    @abstractmethod
    def property(self) -> Property:
        pass


class SymmetryData(NamedTuple):
    function: Callable[[Any], Any]
    inverse: Callable[[Any], Any]


class Symmetry(SymmetryData, GenericProperty):
    def property(self) -> Property:
        return Property(lambda x: x == self.function(self.inverse(x)))


class CommutativityData(NamedTuple):
    function1: Callable[[Any], Any]
    function2: Callable[[Any], Any]


class Commutativity(CommutativityData, GenericProperty):
    def property(self) -> Property:
        return Property(lambda x: self.function1(self.function2(x)) == self.function2(self.function1(x)))


class InvariantData(NamedTuple):
    function: Callable[[Any], Any]
    invariant: Callable[[Any], Any]


class Invariant(InvariantData, GenericProperty):
    def property(self) -> Property:
        return Property(lambda x: self.invariant(x) == self.invariant(self.function(x)))


class IdempotenceData(NamedTuple):
    function: Callable[[Any], Any]


class Idempotence(IdempotenceData, GenericProperty):
    def property(self) -> Property:
        return Property(lambda x: self.function(x) == self.function(self.function(x)))


class IndunctionData(NamedTuple):
    function: Callable[[Any], Any]
    separator: Callable[[Any], list]
    composer: Callable[[list], Any]


class Indunction(IndunctionData, GenericProperty):
    def property(self) -> Property:
        return Property(
            lambda x: self.function(x)
            == self.function(self.composer([self.function(piece) for piece in self.separator(x)]))
        )


class BlackboxData(NamedTuple):
    function: Callable[[Any], Any]
    verifier: Callable[[Any, Any], bool]


class Blackbox(BlackboxData, GenericProperty):
    def property(self) -> Property:
        return Property(lambda x: self.verifier(x, self.function(x)))


class OracleData(NamedTuple):
    function1: Callable[[Any], Any]
    function2: Callable[[Any], Any]


class Oracle(OracleData, GenericProperty):
    def property(self) -> Property:
        return Property(lambda x: self.function1(x) == self.function2(x))
