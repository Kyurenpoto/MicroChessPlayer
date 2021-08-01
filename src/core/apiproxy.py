# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import abstractmethod
from typing import Any, NamedTuple, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from src.core.adapter import APIProxyAdapter
from src.infra.postclient import PostClient

ProxyReq = TypeVar("ProxyReq", bound=BaseModel)
ProxyRes = TypeVar("ProxyRes", bound=BaseModel)


class APIProxyData(NamedTuple):
    url: str


class PostAPIProxy(APIProxyData, APIProxyAdapter[ProxyReq, ProxyRes]):
    async def fetch(self, request: ProxyReq) -> ProxyRes:
        return await self.jsondict_to_response(await PostClient(self.url).post(jsonable_encoder(request)))

    @abstractmethod
    async def jsondict_to_response(self, jsondict: dict[str, Any]) -> ProxyRes:
        pass
