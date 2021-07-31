# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import abstractmethod
from typing import NamedTuple, TypeVar, Union, cast

from src.core.boundary import DataStoreRequestBoundary, FrameworkRequestBoundary, FrameworkResponseBoundary
from src.core.event import EventAGen, PushEvent

UsecaseReq = TypeVar("UsecaseReq")
UsecaseRes = TypeVar("UsecaseRes")


class UsecaseData(NamedTuple):
    boundaries: dict[str, Union[FrameworkResponseBoundary, DataStoreRequestBoundary]]

    def datastore(self) -> DataStoreRequestBoundary:
        return cast(DataStoreRequestBoundary, self.boundaries["datastore"])

    def framework(self) -> FrameworkResponseBoundary:
        return cast(FrameworkResponseBoundary, self.boundaries["framework"])


class Usecase(UsecaseData, FrameworkRequestBoundary[UsecaseReq, UsecaseRes]):
    async def request(self, request: UsecaseReq) -> PushEvent:
        return PushEvent(self.executed(request))

    async def executed(self, request: UsecaseReq) -> EventAGen:
        yield await self.framework().response(await self.request_to_responsable(request))

    @abstractmethod
    async def request_to_responsable(self, request: UsecaseReq) -> UsecaseRes:
        pass
