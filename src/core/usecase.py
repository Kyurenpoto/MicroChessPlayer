# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import abstractmethod
from typing import NamedTuple, TypeVar

from src.core.boundary import (
    DataStoreRequestBoundary,
    FrameworkRequestBoundary,
    FrameworkResponseBoundary,
    ProxyRequestBoundary,
)
from src.core.event import EventAGen, PopEvent, PushEvent

UsecaseReq = TypeVar("UsecaseReq")
UsecaseRes = TypeVar("UsecaseRes")


class UsecaseData(NamedTuple):
    frameworks: list[FrameworkResponseBoundary]
    datastores: dict[str, DataStoreRequestBoundary]
    proxies: dict[str, ProxyRequestBoundary]

    def register_framework(self, framework: FrameworkResponseBoundary) -> None:
        self.frameworks.append(framework)

    def register_datastore(self, id: str, datastore: DataStoreRequestBoundary) -> None:
        self.datastores[id] = datastore

    def register_proxy(self, id: str, proxy: ProxyRequestBoundary) -> None:
        self.proxies[id] = proxy


class Usecase(UsecaseData, FrameworkRequestBoundary[UsecaseReq, UsecaseRes]):
    async def request(self, request: UsecaseReq) -> PushEvent:
        return PushEvent(self.executed(request))

    @abstractmethod
    async def executed(self, request: UsecaseReq) -> EventAGen:
        yield PopEvent(None)
