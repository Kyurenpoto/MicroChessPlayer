# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import NamedTuple

from httpx import HTTPStatusError, RequestError
from src.application.createdresponse import ICreatedResponse
from submodules.fastapi_haljson.src.halresponse import (
    HALJSONResponse,
    NotFoundResponse,
    OkResponse,
    UnprocessableEntityResponse,
)


class ExceptionHandledResponse(NamedTuple):
    created: ICreatedResponse

    async def handled(self) -> HALJSONResponse:
        try:
            return OkResponse.from_response_data(await self.created.normal())
        except RequestError as ex:
            return NotFoundResponse.from_response_data(
                self.created.error(
                    f"An error occurred while requesting {ex.request.url!r}: {ex.args[0]!r}",
                    "request.RequestError",
                )
            )
        except HTTPStatusError as ex:
            return UnprocessableEntityResponse.from_response_data(
                self.created.error(
                    f"Error response {ex.response.status_code} "
                    + f"while requesting {ex.request.url!r}: {ex.response.json()!r}",
                    "request.HTTPStatusError",
                )
            )