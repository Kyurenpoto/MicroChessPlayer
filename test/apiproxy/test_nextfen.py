# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from test.apiproxy.apiproxytestbase import ErrorTestable, NormalBlackBox, TargetToTest
from typing import Final, Union

import pytest
import respx
from httpx import RequestError, Response
from src.apiproxy.nextfen import NextFEN
from src.core.boundary import FakeMultipleProxyResponseBoundary
from src.model.requestmodel import NextFENRequestModel
from src.model.responsemodel import NextFENResponsableModel, NextFENResponseModel
from src.utility.fakedatafactory import ListedFactory, ListMetaFactory

Next_FEN_URL: Final[str] = "http://fake-env/model/next-san"


class NextFENTargetToTest(TargetToTest[NextFENResponsableModel]):
    @respx.mock
    async def target(self, given: Union[RequestError, Response]) -> NextFENResponsableModel:
        respx.post(Next_FEN_URL).mock(side_effect=[given])

        return await NextFEN(Next_FEN_URL, FakeMultipleProxyResponseBoundary()).request_to_response(
            NextFENRequestModel(fens=[], sans=[])
        )


class TestNextFEN(ErrorTestable[NextFENResponsableModel]):
    @pytest.mark.parametrize(
        "next_fens",
        ListedFactory(
            ListMetaFactory(str).factory(),
            100,
        ).created(),
    )
    @pytest.mark.asyncio
    async def test_given_random_response_when_call_request_to_response_then_return_normal_response(
        self,
        next_fens: list[str],
    ) -> None:
        await NormalBlackBox[NextFENResponsableModel](self.target_to_test(), NextFENResponseModel(next_fens)).verify(
            {"next_fens": next_fens, "links": {}}
        )

    def target_to_test(self) -> TargetToTest:
        return NextFENTargetToTest()

    def service_name(self) -> str:
        return "next-fen"
