# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import abstractmethod
from typing import Any, NamedTuple, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from src.core.adapter import APIProxyAdapter
from src.core.boundary import MultipleProxyResponseBoundary, ProxyRequestBoundary
from src.core.event import EventAGen, PopEvent, PushEvent
from src.infra.postclient import PostClient

ProxyReq = TypeVar("ProxyReq")
ProxyRes = TypeVar("ProxyRes")


class APIProxyData(NamedTuple):
    url: str
    usecase: MultipleProxyResponseBoundary


PostAPIReq = TypeVar("PostAPIReq", bound=BaseModel)
PostAPIRes = TypeVar("PostAPIRes", bound=BaseModel)


class PostAPIProxy(APIProxyData, APIProxyAdapter[PostAPIReq, PostAPIRes], ProxyRequestBoundary[ProxyReq, ProxyRes]):
    async def fetch(self, request: PostAPIReq) -> PostAPIRes:
        return await self.jsondict_to_response(await PostClient(self.url).post(jsonable_encoder(request)))

    @abstractmethod
    async def jsondict_to_response(self, jsondict: dict[str, Any]) -> PostAPIRes:
        pass

    async def request(self, request: ProxyReq) -> PushEvent:
        return PushEvent(self.executed(request))

    @abstractmethod
    async def executed(self, request: ProxyReq) -> EventAGen:
        yield PopEvent(None)
