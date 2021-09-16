# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod
from typing import Any, Generic, NamedTuple, Type, TypeVar, Union, cast

import pytest
from fastapi import status
from httpx import RequestError, Response
from src.converter.responseconverter import RequestErrorTypeModelFactory, ResponseErrorTypeModelFactory
from src.model.httperrormodel import NamedHTTPRequestErrorTypeName, NamedHTTPStatusCode
from src.model.responsemodel import ClearErrorResponseModel, ErrorTypeModel
from src.utility.genericproperty import AsyncBlackbox

ResModel = TypeVar("ResModel")


class TargetToTest(ABC, Generic[ResModel]):
    @abstractmethod
    async def target(self, given: Union[RequestError, Response]) -> ResModel:
        pass


class NormalBlackBoxData(NamedTuple):
    target_to_test: TargetToTest
    expected_response: Any


class NormalBlackBox(NormalBlackBoxData, AsyncBlackbox[dict, ResModel]):
    async def function(self, json: dict) -> ResModel:
        return await self.target_to_test.target(Response(status.HTTP_200_OK, json=json))

    async def verifier(self, response: ResModel) -> bool:
        return response == self.expected_response


class ErrorBlackBoxData(NamedTuple):
    target_to_test: TargetToTest
    expected_type: ErrorTypeModel


T = TypeVar("T")


class ErrorBlackBox(ErrorBlackBoxData, AsyncBlackbox[T, ResModel]):
    async def verifier(self, response: ResModel) -> bool:
        return cast(ClearErrorResponseModel, response).error == self.expected_type


class RequestErrorBlackBox(ErrorBlackBox[Type[RequestError], ResModel]):
    async def function(self, error_type: Type[RequestError]) -> ResModel:
        return await self.target_to_test.target(error_type(""))


class ResponseErrorBlackBox(ErrorBlackBox[int, ResModel]):
    async def function(self, status_code: int) -> ResModel:
        return await self.target_to_test.target(Response(status_code, json={}))


class APIProxyTestable(ABC):
    @abstractmethod
    def target_to_test(self) -> TargetToTest:
        pass


class NormalTestable(Generic[ResModel], APIProxyTestable):
    pass


class ErrorTestable(Generic[ResModel], APIProxyTestable):
    @pytest.mark.parametrize(
        "error_type",
        list(NamedHTTPRequestErrorTypeName.type_list()),
    )
    @pytest.mark.asyncio
    async def test_given_request_exception_when_call_request_to_response_then_return_request_error(
        self,
        error_type: Type[RequestError],
    ) -> None:
        await RequestErrorBlackBox[ResModel](
            self.target_to_test(), RequestErrorTypeModelFactory(self.service_name(), error_type.__name__).created()
        ).verify(error_type)

    @pytest.mark.parametrize(
        "status_code",
        list(NamedHTTPStatusCode.name_map().keys()),
    )
    @pytest.mark.asyncio
    async def test_given_http_error_response_seted_when_call_request_to_response_then_return_response_error(
        self,
        status_code: int,
    ) -> None:
        await ResponseErrorBlackBox[ResModel](
            self.target_to_test(), ResponseErrorTypeModelFactory(self.service_name(), status_code).created()
        ).verify(status_code)

    @abstractmethod
    def service_name(self) -> str:
        pass
