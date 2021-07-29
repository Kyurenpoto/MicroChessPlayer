# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import abstractmethod
from typing import NamedTuple, TypeVar, Union, cast

from src.core.boundary import DataStoreRequestBoundary, FrameworkRequestBoundary, FrameworkResponseBoundary
from src.core.event import EventAGen, PopEvent, PushEvent

UsecaseReq = TypeVar("UsecaseReq")
UsecaseRes = TypeVar("UsecaseRes")


class Usecase(FrameworkRequestBoundary[UsecaseReq, UsecaseRes]):
    async def request(self, req: UsecaseReq) -> PushEvent:
        return PushEvent(self.executed(req))

    @abstractmethod
    async def executed(self, req: UsecaseReq) -> EventAGen:
        yield PopEvent(None)


class UsecaseData(NamedTuple):
    boundaries: dict[str, Union[FrameworkResponseBoundary, DataStoreRequestBoundary]]

    def datastore(self) -> DataStoreRequestBoundary:
        return cast(DataStoreRequestBoundary, self.boundaries["datastore"])

    def framework(self) -> FrameworkResponseBoundary:
        return cast(FrameworkResponseBoundary, self.boundaries["framework"])
