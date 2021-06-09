# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from typing import NamedTuple

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from httpx import HTTPStatusError, RequestError
from src.application.createdresponse import ICreatedResponse
from src.domain.dto.playerdto import PlayerInternalModel


class HALJSONResponse(JSONResponse):
    media_type = "application/hal+json"


class OkResponse(HALJSONResponse):
    @classmethod
    def from_response_data(cls, data) -> OkResponse:
        return OkResponse(content=jsonable_encoder(data))


class NotFoundResponse(HALJSONResponse):
    @classmethod
    def from_response_data(cls, data) -> NotFoundResponse:
        return NotFoundResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(data))


class UnprocessableEntityResponse(HALJSONResponse):
    @classmethod
    def from_response_data(cls, data) -> UnprocessableEntityResponse:
        return UnprocessableEntityResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(data)
        )


class ExceptionHandledResponse(NamedTuple):
    internal_model: PlayerInternalModel
    created: ICreatedResponse

    async def handled(self) -> HALJSONResponse:
        try:
            return OkResponse.from_response_data(await self.created.created(self.internal_model))
        except RequestError as ex:
            return NotFoundResponse.from_response_data(
                self.created.error(
                    self.internal_model,
                    f"An error occurred while requesting {ex.request.url!r}: {ex.args[0]!r}",
                    "request.RequestError",
                )
            )
        except HTTPStatusError as ex:
            return UnprocessableEntityResponse.from_response_data(
                self.created.error(
                    self.internal_model,
                    f"Error response {ex.response.status_code} "
                    + f"while requesting {ex.request.url!r}: {ex.response.json()!r}",
                    "request.HTTPStatusError",
                )
            )
