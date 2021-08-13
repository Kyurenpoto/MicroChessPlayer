# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import abstractmethod
from typing import Any, NamedTuple, Type, TypeVar, get_args

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
    datastores: dict[tuple[Type, Type], DataStoreRequestBoundary]
    proxies: dict[tuple[Type, Type], ProxyRequestBoundary]

    def register_framework(self, framework: FrameworkResponseBoundary) -> None:
        self.frameworks.append(framework)

    def register_datastore(self, datastore: DataStoreRequestBoundary) -> None:
        req_type, res_type = get_args(datastore)
        self.datastores[(req_type, res_type)] = datastore

    def register_proxy(self, proxy: ProxyRequestBoundary) -> None:
        req_type, res_type = get_args(proxy)
        self.proxies[(req_type, res_type)] = proxy


UsecaseReq = TypeVar("UsecaseReq")
UsecaseRes = TypeVar("UsecaseRes")


class Usecase(UsecaseData, FrameworkRequestBoundary[UsecaseReq, UsecaseRes], MultipleProxyResponseBoundary):
    async def request(self, request: UsecaseReq) -> PushEvent:
        return PushEvent(self.executed(request))

    async def response(self, response: Any) -> PopEvent:
        if type(response) not in self.datastores and type(response) not in self.proxies:
            raise KeyError

        return PopEvent(response)

    @abstractmethod
    async def executed(self, request: UsecaseReq) -> EventAGen:
        yield PopEvent(None)
