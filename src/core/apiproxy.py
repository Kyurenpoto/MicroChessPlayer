# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import abstractmethod
from typing import Any, NamedTuple, TypeVar

from fastapi.encoders import jsonable_encoder
from httpx import HTTPStatusError, RequestError
from pydantic import BaseModel
from src.converter.responseconverter import ConvertedHTTPStatusErrorResponseModel, ConvertedRequestErrorResponseModel
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

    async def request(self, request: ProxyReq) -> PushEvent:
        return PushEvent(self.executed(request))

    async def executed(self, request: ProxyReq) -> EventAGen:
        yield await self.usecase.response(await self.request_to_response(request))

    @abstractmethod
    async def jsondict_to_response(self, jsondict: dict[str, Any]) -> PostAPIRes:
        pass

    @abstractmethod
    async def request_to_response(self, request: ProxyReq) -> ProxyRes:
        pass


def post_api_proxy_handle_exception(service_name: str):
    def handle_exception_with_service_name(request_to_response):
        async def handle_exception(*args, **kwargs):
            try:
                return request_to_response(*args, **kwargs)
            except RequestError as ex:
                return ConvertedRequestErrorResponseModel(ex.request.url, ex.args[0], service_name).convert()
            except HTTPStatusError as ex:
                return ConvertedHTTPStatusErrorResponseModel(
                    ex.response.status_code, ex.request.url, ex.response.json(), service_name
                ).convert()

        return handle_exception

    return handle_exception_with_service_name
