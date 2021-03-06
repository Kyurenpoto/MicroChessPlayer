# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import abstractmethod
from typing import Any, NamedTuple, TypeVar, cast

from src.core.adapter import ToUsecaseAdapter
from src.core.boundary import FrameworkRequestBoundary, FrameworkResponseBoundary
from src.core.event import Event, EventAGen, EventOperator, PopEvent

IntentReq = TypeVar("IntentReq")
IntentRes = TypeVar("IntentRes")
UsecaseReq = TypeVar("UsecaseReq")
UsecaseRes = TypeVar("UsecaseRes")


class Intent(ToUsecaseAdapter[IntentReq, IntentRes], FrameworkResponseBoundary[UsecaseReq, UsecaseRes]):
    async def dispatch(self, request: IntentReq) -> IntentRes:
        callstack: list[EventAGen] = list[EventAGen]([self.executed(request)])
        op: EventOperator = lambda agen: agen.__anext__()
        event: Event = PopEvent(None)

        while len(callstack) > 0:
            event = await op(callstack[-1])
            op = await event.execute(callstack)

        return cast(PopEvent, event).value

    async def response(self, response: UsecaseRes) -> PopEvent:
        return PopEvent(response)

    @abstractmethod
    async def executed(self, request: Any) -> EventAGen:
        yield PopEvent(None)


class IntentData(NamedTuple):
    usecase: FrameworkRequestBoundary
