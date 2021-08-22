# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod
from typing import Any, Callable, NamedTuple, Type

from faker import Faker


class FakeDataFactory(ABC):
    @abstractmethod
    def created(self) -> Any:
        pass


class ListedFactoryData(NamedTuple):
    origin: FakeDataFactory
    cnt: int


class ListedFactory(ListedFactoryData, FakeDataFactory):
    def created(self) -> Any:
        return [self.origin.created() for _ in range(self.cnt)]


class TupledFactoryData(NamedTuple):
    origins: list[FakeDataFactory]


class TupledFactory(TupledFactoryData, FakeDataFactory):
    def created(self) -> Any:
        return tuple(origin.created() for origin in self.origins)


class TableFactoryData(NamedTuple):
    origins: list[FakeDataFactory]
    cnt: int


class TableFactory(TableFactoryData, FakeDataFactory):
    def created(self) -> Any:
        return ListedFactory(TupledFactory(self.origins), self.cnt).created()


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
    def factory(self, unique: bool = True) -> FakeDataFactory:
        return IntegerFactory(self.min, self.max, (Faker().unique if unique else Faker()))


class ListFactoryData(NamedTuple):
    value_type: Type
    factory: Any


class ListFactory(ListFactoryData, FakeDataFactory):
    def created(self) -> Any:
        return self.factory.pylist(value_types=self.value_type)


class ListMetaFactoryData(NamedTuple):
    value_type: Type


class ListMetaFactory(ListMetaFactoryData, FakeDataMetaFactory):
    def factory(self) -> FakeDataFactory:
        return ListFactory(self.value_type, Faker())


class NestedListFactoryData(NamedTuple):
    inner_factory: FakeDataFactory
    outer_length_factory: FakeDataFactory


class NestedListFactory(NestedListFactoryData, FakeDataFactory):
    def created(self) -> Any:
        return [self.inner_factory.created() for _ in range(self.outer_length_factory.created())]
