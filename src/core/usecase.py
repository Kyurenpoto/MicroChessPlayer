# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import abstractmethod
from typing import TypeVar

from src.core.boundary import FrameworkRequestBoundary
from src.core.event import EventAGen, PopEvent, PushEvent

UsecaseReq = TypeVar("UsecaseReq")
UsecaseRes = TypeVar("UsecaseRes")


class Usecase(FrameworkRequestBoundary[UsecaseReq, UsecaseRes]):
    async def request(self, req: UsecaseReq) -> PushEvent:
        return PushEvent(self.executed(req))

    @abstractmethod
    async def executed(self, req: UsecaseReq) -> EventAGen:
        yield PopEvent(None)
