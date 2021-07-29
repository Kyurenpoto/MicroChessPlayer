# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Awaitable, Callable, NamedTuple

EventAGen = AsyncGenerator["Event", Any]
EventOperator = Callable[[EventAGen], Awaitable]


class Event(ABC):
    @abstractmethod
    async def execute(self, callstack: list[EventAGen]) -> EventOperator:
        pass


class PushEventData(NamedTuple):
    agen: AsyncGenerator


class PushEvent(PushEventData, Event):
    async def execute(self, callstack: list[EventAGen]) -> EventOperator:
        callstack.append(self.agen)

        return lambda agen: agen.__anext__()


class PopEventData(NamedTuple):
    value: Any


class PopEvent(PopEventData, Event):
    async def execute(self, callstack: list[EventAGen]) -> EventOperator:
        await callstack.pop(-1).aclose()

        return lambda agen: agen.asend(self.value)
