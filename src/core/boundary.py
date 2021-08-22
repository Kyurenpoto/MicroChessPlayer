# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

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


class MultipleResponseBoundary(ResponseBoundary[Any, Any]):
    pass


FrameworkRequestBoundary = RequestBoundary
FrameworkResponseBoundary = ResponseBoundary
DataStoreRequestBoundary = RequestBoundary
MultipleDataStoreResponseBoundary = MultipleResponseBoundary
ProxyRequestBoundary = RequestBoundary
MultipleProxyResponseBoundary = MultipleResponseBoundary


class FakeMultipleProxyResponseBoundary(MultipleResponseBoundary):
    async def response(self, res) -> PopEvent:
        return PopEvent(None)
