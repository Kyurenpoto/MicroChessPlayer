# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import Final, Type, cast

import pytest
import respx
from fastapi import status
from httpx import RequestError, Response
from src.apiproxy.nextsan import NextSAN
from src.core.boundary import FakeMultipleProxyResponseBoundary
from src.model.httperrormodel import NamedHTTPRequestErrorTypeName, NamedHTTPStatusCode
from src.model.requestmodel import NextSANRequestModel
from src.model.responsemodel import ClearErrorResponseModel, NextSANResponsableModel, NextSANResponseModel
from src.utility.fakedatafactory import ListedFactory, ListMetaFactory
from src.utility.genericproperty import AsyncBlackbox

Next_SAN_URL: Final[str] = "http://fake-env/model/fen-status"


async def target_to_test(
    request: NextSANRequestModel = NextSANRequestModel(fens=[], legal_sans=[])
) -> NextSANResponsableModel:
    return await NextSAN(Next_SAN_URL, FakeMultipleProxyResponseBoundary()).request_to_response(request)


@pytest.mark.parametrize(
    "next_sans",
    ListedFactory(
        ListMetaFactory(str).factory(),
        100,
    ).created(),
)
@pytest.mark.asyncio
@respx.mock
async def test_given_random_response_when_call_request_to_response_then_return_normal_response(
    next_sans: list[str],
) -> None:
    print(next_sans)

    async def target_function(json: dict) -> NextSANResponsableModel:
        respx.post(Next_SAN_URL).mock(side_effect=[Response(status.HTTP_200_OK, json=json)])

        return await target_to_test()

    async def verifier(response: NextSANResponsableModel) -> bool:
        return cast(NextSANResponseModel, response).next_sans == next_sans

    await AsyncBlackbox(target_function, verifier).property().verify({"next_sans": next_sans, "links": {}})


@pytest.mark.parametrize(
    "error_type",
    list(NamedHTTPRequestErrorTypeName.type_list()),
)
@pytest.mark.asyncio
@respx.mock
async def test_given_request_exception_when_call_request_to_response_then_return_request_error(
    error_type: Type[RequestError],
) -> None:
    async def target_function(error_type: Type[RequestError]) -> NextSANResponsableModel:
        respx.post(Next_SAN_URL).mock(side_effect=[error_type("")])

        return await target_to_test()

    async def verifier(response: NextSANResponsableModel) -> bool:
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
    async def target_function(status_code: int) -> NextSANResponsableModel:
        respx.post(Next_SAN_URL).mock(side_effect=[Response(status_code, json={})])

        return await target_to_test()

    async def verifier(response: NextSANResponsableModel) -> bool:
        return (
            cast(ClearErrorResponseModel, response).error.category == "HTTP-Response"
            and cast(ClearErrorResponseModel, response).error.code == status_code
        )

    await AsyncBlackbox(target_function, verifier).property().verify(status_code)
