# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import Any

from src.converter.requestconverter import NextSANRequestToDTO
from src.converter.responseconverter import AINextSANResponseToModel
from src.core.apiproxy import PostAPIProxy, post_api_proxy_handle_exception
from src.framework.dto.aidto import AINextSANRequest, AINextSANResponse
from src.model.requestmodel import NextSANRequestModel
from src.model.responsemodel import NextSANResponsableModel

NextSANProxy = PostAPIProxy[AINextSANRequest, AINextSANResponse, NextSANRequestModel, NextSANResponsableModel]


class NextSAN(NextSANProxy):
    async def jsondict_to_response(self, jsondict: dict[str, Any]) -> AINextSANResponse:
        return AINextSANResponse.parse_obj(jsondict)

    @post_api_proxy_handle_exception("next-san")
    async def request_to_response(self, request: NextSANRequestModel) -> NextSANResponsableModel:
        return AINextSANResponseToModel.from_dto(
            await self.fetch(NextSANRequestToDTO.from_model(request).convert())
        ).convert()
