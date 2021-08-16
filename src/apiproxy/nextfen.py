# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import Any

from httpx import HTTPStatusError, RequestError
from src.converter.requestconverter import NextFENRequestToDTO
from src.converter.responseconverter import (
    ConvertedHTTPStatusErrorResponseModel,
    ConvertedRequestErrorResponseModel,
    EnvironmentNextFENResponseToModel,
)
from src.core.apiproxy import PostAPIProxy
from src.core.event import EventAGen
from src.framework.dto.environmentdto import EnvironmentNextFENRequest, EnvironmentNextFENResponse
from src.model.requestmodel import NextFENRequestModel
from src.model.responsemodel import NextFENResponsableModel

NextFENProxy = PostAPIProxy[
    EnvironmentNextFENRequest, EnvironmentNextFENResponse, NextFENRequestModel, NextFENResponsableModel
]


class NextFEN(NextFENProxy):
    async def jsondict_to_response(self, jsondict: dict[str, Any]) -> EnvironmentNextFENResponse:
        return EnvironmentNextFENResponse.parse_obj(jsondict)

    async def executed(self, request: NextFENRequestModel) -> EventAGen:
        try:
            yield await self.usecase.response(
                EnvironmentNextFENResponseToModel.from_dto(
                    await self.fetch(NextFENRequestToDTO.from_model(request).convert())
                ).convert()
            )
        except RequestError as ex:
            yield await self.usecase.response(
                ConvertedRequestErrorResponseModel(ex.request.url, ex.args[0], "next-fen").convert()
            )
        except HTTPStatusError as ex:
            yield await self.usecase.response(
                ConvertedHTTPStatusErrorResponseModel(
                    ex.response.status_code, ex.request.url, ex.response.json(), "next-fen"
                ).convert()
            )
