# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.core.event import PopEvent, PushEvent

ReqType = TypeVar("ReqType")
ResType = TypeVar("ResType")


class RequestBoundary(ABC, Generic[ReqType, ResType]):
    @abstractmethod
    async def request(self, req: ReqType) -> PushEvent:
        pass


class ResponseBoundary(ABC, Generic[ReqType, ResType]):
    @abstractmethod
    async def response(self, res: ResType) -> PopEvent:
        pass


FrameworkRequestBoundary = RequestBoundary
FrameworkResponseBoundary = ResponseBoundary
DataStoreRequestBoundary = RequestBoundary
DataStoreResponseBoundary = ResponseBoundary
