# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import Any

from src.converter.requestconverter import FENStatusRequestToDTO
from src.converter.responseconverter import EnvironmentFENStatusResponseToModel
from src.core.apiproxy import PostAPIProxy, post_api_proxy_handle_exception
from src.framework.dto.environmentdto import EnvironmentFENStatusRequest, EnvironmentFENStatusResponse
from src.model.requestmodel import FENStatusRequestModel
from src.model.responsemodel import FENStatusResponsableModel

FENStatusProxy = PostAPIProxy[
    EnvironmentFENStatusRequest, EnvironmentFENStatusResponse, FENStatusRequestModel, FENStatusResponsableModel
]


class FENStatus(FENStatusProxy):
    async def jsondict_to_response(self, jsondict: dict[str, Any]) -> EnvironmentFENStatusResponse:
        return EnvironmentFENStatusResponse.parse_obj(jsondict)

    @post_api_proxy_handle_exception("fen-status")
    async def request_to_response(self, request: FENStatusRequestModel) -> FENStatusResponsableModel:
        return EnvironmentFENStatusResponseToModel.from_dto(
            await self.fetch(FENStatusRequestToDTO.from_model(request).convert())
        ).convert()
