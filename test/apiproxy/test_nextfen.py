# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import Final, Type, cast

import pytest
import respx
from fastapi import status
from httpx import RequestError, Response
from src.apiproxy.nextfen import NextFEN
from src.core.boundary import FakeMultipleProxyResponseBoundary
from src.model.httperrormodel import NamedHTTPRequestErrorTypeName, NamedHTTPStatusCode
from src.model.requestmodel import NextFENRequestModel
from src.model.responsemodel import ClearErrorResponseModel, NextFENResponsableModel, NextFENResponseModel
from src.utility.fakedatafactory import ListedFactory, ListMetaFactory
from src.utility.genericproperty import AsyncBlackbox

Next_FEN_URL: Final[str] = "http://fake-env/model/fen-status"


async def target_to_test(
    request: NextFENRequestModel = NextFENRequestModel(fens=[], sans=[])
) -> NextFENResponsableModel:
    return await NextFEN(Next_FEN_URL, FakeMultipleProxyResponseBoundary()).request_to_response(request)


@pytest.mark.parametrize(
    "next_fens",
    ListedFactory(
        ListMetaFactory(str).factory(),
        100,
    ).created(),
)
@pytest.mark.asyncio
@respx.mock
async def test_request_to_response(next_fens: list[str]) -> None:
    print(next_fens)

    async def target_function(json: dict) -> NextFENResponsableModel:
        respx.post(Next_FEN_URL).mock(side_effect=[Response(status.HTTP_200_OK, json=json)])

        return await target_to_test()

    async def verifier(response: NextFENResponsableModel) -> bool:
        return cast(NextFENResponseModel, response).next_fens == next_fens

    await AsyncBlackbox(target_function, verifier).property().verify({"next_fens": next_fens, "links": {}})


@pytest.mark.parametrize(
    "error_type",
    list(NamedHTTPRequestErrorTypeName.type_list()),
)
@pytest.mark.asyncio
@respx.mock
async def test_request_to_response_with_request_error(error_type: Type[RequestError]) -> None:
    async def target_function(error_type: Type[RequestError]) -> NextFENResponsableModel:
        respx.post(Next_FEN_URL).mock(side_effect=[error_type("")])

        return await target_to_test()

    async def verifier(response: NextFENResponsableModel) -> bool:
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
async def test_request_to_response_with_error_response(status_code: int) -> None:
    async def target_function(status_code: int) -> NextFENResponsableModel:
        respx.post(Next_FEN_URL).mock(side_effect=[Response(status_code, json={})])

        return await target_to_test()

    async def verifier(response: NextFENResponsableModel) -> bool:
        return (
            cast(ClearErrorResponseModel, response).error.category == "HTTP-Response"
            and cast(ClearErrorResponseModel, response).error.code == status_code
        )

    await AsyncBlackbox(target_function, verifier).property().verify(status_code)
