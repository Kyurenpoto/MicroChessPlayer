# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import Any

from src.converter.requestconverter import NextFENRequestToDTO
from src.converter.responseconverter import EnvironmentNextFENResponseToModel
from src.core.apiproxy import PostAPIProxy, post_api_proxy_handle_exception
from src.framework.dto.environmentdto import EnvironmentNextFENRequest, EnvironmentNextFENResponse
from src.model.requestmodel import NextFENRequestModel
from src.model.responsemodel import NextFENResponsableModel

NextFENProxy = PostAPIProxy[
    EnvironmentNextFENRequest, EnvironmentNextFENResponse, NextFENRequestModel, NextFENResponsableModel
]


class NextFEN(NextFENProxy):
    async def jsondict_to_response(self, jsondict: dict[str, Any]) -> EnvironmentNextFENResponse:
        return EnvironmentNextFENResponse.parse_obj(jsondict)

    @post_api_proxy_handle_exception("next-fen")
    async def request_to_response(self, request: NextFENRequestModel) -> NextFENResponsableModel:
        return EnvironmentNextFENResponseToModel.from_dto(
            await self.fetch(NextFENRequestToDTO.from_model(request).convert())
        ).convert()
