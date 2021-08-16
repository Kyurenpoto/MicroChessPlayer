# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import Any

from httpx import HTTPStatusError, RequestError
from src.converter.requestconverter import NextSANRequestToDTO
from src.converter.responseconverter import (
    AINextSANResponseToModel,
    ConvertedHTTPStatusErrorResponseModel,
    ConvertedRequestErrorResponseModel,
)
from src.core.apiproxy import PostAPIProxy
from src.core.event import EventAGen
from src.framework.dto.aidto import AINextSANRequest, AINextSANResponse
from src.model.requestmodel import NextSANRequestModel
from src.model.responsemodel import NextSANResponsableModel

NextSANProxy = PostAPIProxy[AINextSANRequest, AINextSANResponse, NextSANRequestModel, NextSANResponsableModel]


class NextSAN(NextSANProxy):
    async def jsondict_to_response(self, jsondict: dict[str, Any]) -> AINextSANResponse:
        return AINextSANResponse.parse_obj(jsondict)

    async def executed(self, request: NextSANRequestModel) -> EventAGen:
        try:
            yield await self.usecase.response(
                AINextSANResponseToModel.from_dto(
                    await self.fetch(NextSANRequestToDTO.from_model(request).convert())
                ).convert()
            )
        except RequestError as ex:
            yield await self.usecase.response(
                ConvertedRequestErrorResponseModel(ex.request.url, ex.args[0], "next-san").convert()
            )
        except HTTPStatusError as ex:
            yield await self.usecase.response(
                ConvertedHTTPStatusErrorResponseModel(
                    ex.response.status_code, ex.request.url, ex.response.json(), "next-san"
                ).convert()
            )
