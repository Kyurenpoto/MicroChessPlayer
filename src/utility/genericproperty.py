# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod
from typing import Any, Callable, Coroutine, Generic, NamedTuple, TypeVar

T1 = TypeVar("T1")
T2 = TypeVar("T2")


class GenericProperty(ABC):
    @abstractmethod
    def verify(self, target: Any) -> None:
        pass


class Symmetry(GenericProperty, ABC, Generic[T1, T2]):
    def verify(self, x: Any) -> None:
        assert x == self.function(self.inverse(x))

    @abstractmethod
    def function(self, x: T1) -> T2:
        pass

    @abstractmethod
    def inverse(self, x: T2) -> T1:
        pass


class Commutativity(GenericProperty, ABC, Generic[T1]):
    def verify(self, x: Any) -> None:
        assert self.function1(self.function2(x)) == self.function2(self.function1(x))

    @abstractmethod
    def function1(self, x: T1) -> T1:
        pass

    @abstractmethod
    def function2(self, x: T1) -> T1:
        pass


class Invariant(GenericProperty, ABC, Generic[T1, T2]):
    def verify(self, x: Any) -> None:
        assert self.invariant(x) == self.invariant(self.function(x))

    @abstractmethod
    def function(self, x: T1) -> T1:
        pass

    @abstractmethod
    def invariant(self, x: T1) -> T2:
        pass


class Idempotence(GenericProperty, ABC, Generic[T1]):
    def verify(self, x: Any) -> None:
        assert self.function(x) == self.function(self.function(x))

    @abstractmethod
    def function(self, x: T1) -> T1:
        pass


class Indunction(GenericProperty, ABC, Generic[T1, T2]):
    def verify(self, x: Any) -> None:
        assert self.function(x) == self.function(self.composer([self.function(piece) for piece in self.separator(x)]))

    @abstractmethod
    def function(self, x: T1) -> T2:
        pass

    @abstractmethod
    def separator(self, x: T1) -> list[T1]:
        pass

    @abstractmethod
    def composer(self, x: list[T2]) -> T1:
        pass


class Blackbox(GenericProperty, ABC, Generic[T1, T2]):
    def verify(self, x: Any) -> None:
        assert self.verifier(self.function(x))

    @abstractmethod
    def function(self, x: T1) -> T2:
        pass

    @abstractmethod
    def verifier(self, x: T2) -> bool:
        pass


class Oracle(GenericProperty, ABC, Generic[T1, T2]):
    def verify(self, x: Any) -> None:
        assert self.function1(x) == self.function2(x)

    @abstractmethod
    def function1(self, x: T1) -> T2:
        pass

    @abstractmethod
    def function2(self, x: T1) -> T2:
        pass


class AsyncGenericProperty(ABC):
    @abstractmethod
    async def verify(self, target: Any) -> None:
        pass


class AsyncSymmetry(AsyncGenericProperty, ABC, Generic[T1, T2]):
    async def verify(self, x: Any) -> None:
        assert x == await self.function(await self.inverse(x))

    @abstractmethod
    async def function(self, x: T1) -> T2:
        pass

    @abstractmethod
    async def inverse(self, x: T2) -> T1:
        pass


class AsyncCommutativity(AsyncGenericProperty, ABC, Generic[T1]):
    async def verify(self, x: Any) -> None:
        assert await self.function1(await self.function2(x)) == await self.function2(await self.function1(x))

    @abstractmethod
    async def function1(self, x: T1) -> T1:
        pass

    @abstractmethod
    async def function2(self, x: T1) -> T1:
        pass


class AsyncInvariant(AsyncGenericProperty, ABC, Generic[T1, T2]):
    async def verify(self, x: Any) -> None:
        assert await self.invariant(x) == await self.invariant(await self.function(x))

    @abstractmethod
    async def function(self, x: T1) -> T1:
        pass

    @abstractmethod
    async def invariant(self, x: T1) -> T2:
        pass


class AsyncIdempotence(AsyncGenericProperty, ABC, Generic[T1]):
    async def verify(self, x: Any) -> None:
        assert await self.function(x) == await self.function(await self.function(x))

    @abstractmethod
    async def function(self, x: T1) -> T1:
        pass


class AsyncIndunction(AsyncGenericProperty, ABC, Generic[T1, T2]):
    async def verify(self, x: Any) -> None:
        assert await self.function(x) == await self.function(
            await self.composer([await self.function(piece) for piece in await self.separator(x)])
        )

    @abstractmethod
    async def function(self, x: T1) -> T2:
        pass

    @abstractmethod
    async def separator(self, x: T1) -> list[T1]:
        pass

    @abstractmethod
    async def composer(self, x: list[T2]) -> T1:
        pass


class AsyncBlackbox(AsyncGenericProperty, ABC, Generic[T1, T2]):
    async def verify(self, x: Any) -> None:
        assert await self.verifier(await self.function(x))

    @abstractmethod
    async def function(self, x: T1) -> T2:
        pass

    @abstractmethod
    async def verifier(self, x: T2) -> bool:
        pass


class AsyncOracle(AsyncGenericProperty, ABC, Generic[T1, T2]):
    async def verify(self, x: Any) -> None:
        assert await self.function1(x) == await self.function2(x)

    @abstractmethod
    async def function1(self, x: T1) -> T2:
        pass

    @abstractmethod
    async def function2(self, x: T1) -> T2:
        pass
