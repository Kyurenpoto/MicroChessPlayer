# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import abstractmethod
from typing import Any, NamedTuple, TypeVar

from src.core.boundary import (
    DataStoreRequestBoundary,
    FrameworkRequestBoundary,
    FrameworkResponseBoundary,
    MultipleProxyResponseBoundary,
    ProxyRequestBoundary,
)
from src.core.event import EventAGen, PopEvent, PushEvent


class UsecaseData(NamedTuple):
    frameworks: list[FrameworkResponseBoundary]
    datastores: dict[str, DataStoreRequestBoundary]
    proxies: dict[str, ProxyRequestBoundary]

    def register_framework(self, framework: FrameworkResponseBoundary) -> None:
        self.frameworks.append(framework)

    def register_datastore(self, signature: str, datastore: DataStoreRequestBoundary) -> None:
        self.datastores[signature] = datastore

    def register_proxy(self, signature: str, proxy: ProxyRequestBoundary) -> None:
        self.proxies[signature] = proxy


UsecaseReq = TypeVar("UsecaseReq")
UsecaseRes = TypeVar("UsecaseRes")


class Usecase(UsecaseData, FrameworkRequestBoundary[UsecaseReq, UsecaseRes], MultipleProxyResponseBoundary):
    async def request(self, request: UsecaseReq) -> PushEvent:
        return PushEvent(self.executed(request))

    async def response(self, response: Any) -> PopEvent:
        return PopEvent(response)

    @abstractmethod
    async def executed(self, request: UsecaseReq) -> EventAGen:
        yield PopEvent(None)
