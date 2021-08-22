# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod
from typing import Any, Callable, Coroutine, NamedTuple


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
    verifier: Callable[[Any], bool]


class Blackbox(BlackboxData, GenericProperty):
    def property(self) -> Property:
        return Property(lambda x: self.verifier(self.function(x)))


class OracleData(NamedTuple):
    function1: Callable[[Any], Any]
    function2: Callable[[Any], Any]


class Oracle(OracleData, GenericProperty):
    def property(self) -> Property:
        return Property(lambda x: self.function1(x) == self.function2(x))


class AsyncProperty(NamedTuple):
    property: Callable[[Any], Coroutine[Any, Any, bool]]

    async def verify(self, target: Any) -> None:
        assert await self.property(target)


class AsyncGenericProperty(ABC):
    @abstractmethod
    async def property(self) -> AsyncProperty:
        pass


class AsyncSymmetryData(NamedTuple):
    function: Callable[[Any], Coroutine[Any, Any, Any]]
    inverse: Callable[[Any], Coroutine[Any, Any, Any]]


class AsyncSymmetry(AsyncSymmetryData, AsyncGenericProperty):
    async def property(self) -> AsyncProperty:
        async def async_lambda(x) -> bool:
            return x == await self.function(await self.inverse(x))

        return AsyncProperty(async_lambda)


class AsyncCommutativityData(NamedTuple):
    function1: Callable[[Any], Coroutine[Any, Any, Any]]
    function2: Callable[[Any], Coroutine[Any, Any, Any]]


class AsyncCommutativity(AsyncCommutativityData, AsyncGenericProperty):
    def property(self) -> AsyncProperty:
        async def async_lambda(x) -> bool:
            return await self.function1(await self.function2(x)) == await self.function2(await self.function1(x))

        return AsyncProperty(async_lambda)


class AsyncInvariantData(NamedTuple):
    function: Callable[[Any], Coroutine[Any, Any, Any]]
    invariant: Callable[[Any], Coroutine[Any, Any, Any]]


class AsyncInvariant(AsyncInvariantData, AsyncGenericProperty):
    def property(self) -> AsyncProperty:
        async def async_lambda(x) -> bool:
            return await self.invariant(x) == await self.invariant(await self.function(x))

        return AsyncProperty(async_lambda)


class AsyncIdempotenceData(NamedTuple):
    function: Callable[[Any], Coroutine[Any, Any, Any]]


class AsyncIdempotence(AsyncIdempotenceData, AsyncGenericProperty):
    def property(self) -> AsyncProperty:
        async def async_lambda(x) -> bool:
            return await self.function(x) == await self.function(await self.function(x))

        return AsyncProperty(async_lambda)


class AsyncIndunctionData(NamedTuple):
    function: Callable[[Any], Coroutine[Any, Any, Any]]
    separator: Callable[[Any], Coroutine[Any, Any, list]]
    composer: Callable[[list], Coroutine[Any, Any, Any]]


class AsyncIndunction(AsyncIndunctionData, AsyncGenericProperty):
    def property(self) -> AsyncProperty:
        async def async_lambda(x) -> bool:
            return await self.function(x) == await self.function(
                await self.composer([await self.function(piece) for piece in await self.separator(x)])
            )

        return AsyncProperty(async_lambda)


class AsyncBlackboxData(NamedTuple):
    function: Callable[[Any], Coroutine[Any, Any, Any]]
    verifier: Callable[[Any], Coroutine[Any, Any, bool]]


class AsyncBlackbox(AsyncBlackboxData, AsyncGenericProperty):
    def property(self) -> AsyncProperty:
        async def async_lambda(x) -> bool:
            return await self.verifier(await self.function(x))

        return AsyncProperty(async_lambda)


class AsyncOracleData(NamedTuple):
    function1: Callable[[Any], Coroutine[Any, Any, Any]]
    function2: Callable[[Any], Coroutine[Any, Any, Any]]


class AsyncOracle(AsyncOracleData, AsyncGenericProperty):
    def property(self) -> AsyncProperty:
        async def async_lambda(x) -> bool:
            return await self.function1(x) == await self.function2(x)

        return AsyncProperty(async_lambda)
