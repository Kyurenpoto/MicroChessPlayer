# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import Final, Type, cast

import pytest
import respx
from fastapi import status
from httpx import RequestError, Response
from src.apiproxy.fenstatus import FENStatus
from src.core.boundary import FakeMultipleProxyResponseBoundary
from src.model.httperrormodel import NamedHTTPRequestErrorTypeName, NamedHTTPStatusCode
from src.model.requestmodel import FENStatusRequestModel
from src.model.responsemodel import ClearErrorResponseModel, FENStatusResponsableModel, FENStatusResponseModel
from src.utility.fakedatafactory import IntegerMetaFactory, ListMetaFactory, NestedListFactory, TableFactory
from src.utility.genericproperty import AsyncBlackbox

FEN_STATUS_URL: Final[str] = "http://fake-env/model/fen-status"


async def target_to_test(request: FENStatusRequestModel = FENStatusRequestModel(fens=[])) -> FENStatusResponsableModel:
    return await FENStatus(FEN_STATUS_URL, FakeMultipleProxyResponseBoundary()).request_to_response(request)


@pytest.mark.parametrize(
    "statuses, legal_moves",
    TableFactory(
        [
            ListMetaFactory(int).factory(),
            NestedListFactory(ListMetaFactory(str).factory(), IntegerMetaFactory(0, 10).factory(False)),
        ],
        100,
    ).created(),
)
@pytest.mark.asyncio
@respx.mock
async def test_given_random_response_when_call_request_to_response_then_return_normal_response(
    statuses: list[int], legal_moves: list[list[str]]
) -> None:
    async def target_function(json: dict) -> FENStatusResponsableModel:
        respx.post(FEN_STATUS_URL).mock(side_effect=[Response(status.HTTP_200_OK, json=json)])

        return await target_to_test()

    async def verifier(response: FENStatusResponsableModel) -> bool:
        return (
            cast(FENStatusResponseModel, response).statuses == statuses
            and cast(FENStatusResponseModel, response).legal_moves == legal_moves
        )

    await AsyncBlackbox(target_function, verifier).property().verify(
        {"statuses": statuses, "legal_moves": legal_moves, "links": {}}
    )


@pytest.mark.parametrize(
    "error_type",
    list(NamedHTTPRequestErrorTypeName.type_list()),
)
@pytest.mark.asyncio
@respx.mock
async def test_given_request_exception_when_call_request_to_response_then_return_request_error(
    error_type: Type[RequestError],
) -> None:
    async def target_function(error_type: Type[RequestError]) -> FENStatusResponsableModel:
        respx.post(FEN_STATUS_URL).mock(side_effect=[error_type("")])

        return await target_to_test()

    async def verifier(response: FENStatusResponsableModel) -> bool:
        return (
            cast(ClearErrorResponseModel, response).error.category == "HTTP-Request"
            and cast(ClearErrorResponseModel, response).message.response_detail
            == NamedHTTPRequestErrorTypeName(error_type.__name__).name()
        )

    await AsyncBlackbox(target_function, verifier).property().verify(error_type)


@pytest.mark.parametrize(
    "status_code",
    list(NamedHTTPStatusCode.name_map().keys()),
)
@pytest.mark.asyncio
@respx.mock
async def test_given_http_error_response_seted_when_call_request_to_response_then_return_response_error(
    status_code: int,
) -> None:
    async def target_function(status_code: int) -> FENStatusResponsableModel:
        respx.post(FEN_STATUS_URL).mock(side_effect=[Response(status_code, json={})])

        return await target_to_test()

    async def verifier(response: FENStatusResponsableModel) -> bool:
        return (
            cast(ClearErrorResponseModel, response).error.category == "HTTP-Response"
            and cast(ClearErrorResponseModel, response).error.code == status_code
        )

    await AsyncBlackbox(target_function, verifier).property().verify(status_code)
