# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod
from typing import Any, Callable, NamedTuple

from faker import Faker


class FakeDataFactory(ABC):
    @abstractmethod
    def created(self) -> Any:
        pass


class ListFactoryData(NamedTuple):
    origin: FakeDataFactory
    cnt: int


class ListFactory(ListFactoryData, FakeDataFactory):
    def created(self) -> Any:
        return [self.origin.created() for _ in range(self.cnt)]


class TupleFactoryData(NamedTuple):
    origins: list[FakeDataFactory]


class TupleFactory(TupleFactoryData, FakeDataFactory):
    def created(self) -> Any:
        return tuple(origin.created() for origin in self.origins)


class TableFactoryData(NamedTuple):
    origins: list[FakeDataFactory]
    cnt: int


class TableFactory(TableFactoryData, FakeDataFactory):
    def created(self) -> Any:
        return ListFactory(TupleFactory(self.origins), self.cnt).created()


class ConditionalFactoryData(NamedTuple):
    origin: FakeDataFactory
    condition: Callable[[Any], bool]


class ConditionalFactory(ConditionalFactoryData, FakeDataFactory):
    def created(self) -> Any:
        while True:
            x = self.origin.created()
            if self.condition(x):
                return x


class FakeDataMetaFactory(ABC):
    @abstractmethod
    def factory(self) -> FakeDataFactory:
        pass


class IntegerFactoryData(NamedTuple):
    min: int
    max: int
    factory: Any


class IntegerFactory(IntegerFactoryData, FakeDataFactory):
    def created(self) -> Any:
        return self.factory.random_int(self.min, self.max)


class IntegerMetaFactoryData(NamedTuple):
    min: int
    max: int


class IntegerMetaFactory(IntegerMetaFactoryData, FakeDataMetaFactory):
    def factory(self) -> FakeDataFactory:
        return IntegerFactory(self.min, self.max, Faker().unique)
