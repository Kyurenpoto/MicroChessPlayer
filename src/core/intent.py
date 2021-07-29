# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import abstractmethod
from typing import Any, TypeVar, cast

from src.core.adapter import ToUsecaseAdapter
from src.core.boundary import FrameworkResponseBoundary
from src.core.event import Event, EventAGen, EventOperator, PopEvent

IntentReq = TypeVar("IntentReq")
IntentRes = TypeVar("IntentRes")
UsecaseReq = TypeVar("UsecaseReq")
UsecaseRes = TypeVar("UsecaseRes")


class Intent(ToUsecaseAdapter[IntentReq, IntentRes], FrameworkResponseBoundary[UsecaseReq, UsecaseRes]):
    async def dispatch(self, req: IntentReq) -> IntentRes:
        callstack: list[EventAGen] = list[EventAGen]([self.executed(req)])
        op: EventOperator = lambda agen: agen.__anext__()
        event: Event = PopEvent(None)

        while len(callstack) > 0:
            event = await op(callstack[-1])
            op = await event.execute(callstack)

        return cast(PopEvent, event).value

    async def response(self, res: UsecaseRes) -> PopEvent:
        return PopEvent(res)

    @abstractmethod
    async def executed(self, req: Any) -> EventAGen:
        yield PopEvent(None)
