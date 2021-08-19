# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

import pytest
from fastapi import status
from src.converter.responseconverter import ConvertedHTTPStatusErrorResponseModel
from src.utility.fakedatafactory import ConditionalFactory, IntegerMetaFactory, ListFactory
from src.utility.genericproperty import Blackbox


@pytest.mark.parametrize(
    "status_code",
    ListFactory(
        ConditionalFactory(IntegerMetaFactory(400, 599).factory(), lambda x: x not in [400, 413, 415, 422, 500, 502]),
        100,
    ).created(),
)
@pytest.mark.asyncio
async def test_unknown_statuses_such_that_constant(status_code: int) -> None:
    assert (
        ConvertedHTTPStatusErrorResponseModel(status_code, "", {}, "").convert()
        == ConvertedHTTPStatusErrorResponseModel(status.HTTP_500_INTERNAL_SERVER_ERROR, "", {}, "").convert()
    )


@pytest.mark.parametrize(
    "status_code",
    [
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        status.HTTP_502_BAD_GATEWAY,
    ],
)
@pytest.mark.asyncio
async def test_known_statuses_such_that_blackbox(status_code: int) -> None:
    Blackbox(
        lambda x: ConvertedHTTPStatusErrorResponseModel(x, "", {}, "").convert(), lambda x, y: x == y.status_code()
    ).property().verify(status_code)
