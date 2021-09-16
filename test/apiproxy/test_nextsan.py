# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from test.apiproxy.apiproxytestbase import ErrorTestable, NormalBlackBox, TargetToTest
from typing import Final, Union

import pytest
import respx
from httpx import RequestError, Response
from src.apiproxy.nextsan import NextSAN
from src.core.boundary import FakeMultipleProxyResponseBoundary
from src.model.requestmodel import NextSANRequestModel
from src.model.responsemodel import NextSANResponsableModel, NextSANResponseModel
from src.utility.fakedatafactory import ListedFactory, ListMetaFactory

Next_SAN_URL: Final[str] = "http://fake-env/model/next-sans"


class NextSANTargetToTest(TargetToTest[NextSANResponsableModel]):
    @respx.mock
    async def target(self, given: Union[RequestError, Response]) -> NextSANResponsableModel:
        respx.post(Next_SAN_URL).mock(side_effect=[given])

        return await NextSAN(Next_SAN_URL, FakeMultipleProxyResponseBoundary()).request_to_response(
            NextSANRequestModel(fens=[], legal_sans=[])
        )


class TestNextSAN(ErrorTestable[NextSANResponsableModel]):
    @pytest.mark.parametrize(
        "next_sans",
        ListedFactory(
            ListMetaFactory(str).factory(),
            100,
        ).created(),
    )
    @pytest.mark.asyncio
    async def test_given_random_response_when_call_request_to_response_then_return_normal_response(
        self,
        next_sans: list[str],
    ) -> None:
        await NormalBlackBox[NextSANResponsableModel](self.target_to_test(), NextSANResponseModel(next_sans)).verify(
            {"next_sans": next_sans, "links": {}}
        )

    def target_to_test(self) -> TargetToTest:
        return NextSANTargetToTest()

    def service_name(self) -> str:
        return "next-san"
