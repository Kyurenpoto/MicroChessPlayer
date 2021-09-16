# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from test.apiproxy.apiproxytestbase import ErrorTestable, NormalBlackBox, TargetToTest
from typing import Final, Union

import pytest
import respx
from httpx import RequestError, Response
from src.apiproxy.fenstatus import FENStatus
from src.core.boundary import FakeMultipleProxyResponseBoundary
from src.model.requestmodel import FENStatusRequestModel
from src.model.responsemodel import FENStatusResponsableModel, FENStatusResponseModel
from src.utility.fakedatafactory import IntegerMetaFactory, ListMetaFactory, NestedListFactory, TableFactory

FEN_STATUS_URL: Final[str] = "http://fake-env/model/fen-status"


class FENStatusTargetToTest(TargetToTest[FENStatusResponsableModel]):
    @respx.mock
    async def target(self, given: Union[RequestError, Response]) -> FENStatusResponsableModel:
        respx.post(FEN_STATUS_URL).mock(side_effect=[given])

        return await FENStatus(FEN_STATUS_URL, FakeMultipleProxyResponseBoundary()).request_to_response(
            FENStatusRequestModel(fens=[])
        )


class TestFENStatus(ErrorTestable[FENStatusResponsableModel]):
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
    async def test_given_random_response_when_call_request_to_response_then_return_normal_response(
        self, statuses: list[int], legal_moves: list[list[str]]
    ) -> None:
        await NormalBlackBox[FENStatusResponsableModel](
            self.target_to_test(), FENStatusResponseModel(statuses, legal_moves)
        ).verify({"statuses": statuses, "legal_moves": legal_moves, "links": {}})

    def target_to_test(self) -> TargetToTest:
        return FENStatusTargetToTest()

    def service_name(self) -> str:
        return "fen-status"
