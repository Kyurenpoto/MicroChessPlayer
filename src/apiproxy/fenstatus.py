# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import Any

from httpx import HTTPStatusError, RequestError
from src.converter.requestconverter import FENStatusRequestToDTO
from src.converter.responseconverter import (
    ConvertedHTTPStatusErrorResponseModel,
    ConvertedRequestErrorResponseModel,
    EnvironmentFENStatusResponseToModel,
)
from src.core.apiproxy import PostAPIProxy
from src.core.event import EventAGen
from src.framework.dto.environmentdto import EnvironmentFENStatusRequest, EnvironmentFENStatusResponse
from src.model.requestmodel import FENStatusRequestModel
from src.model.responsemodel import FENStatusResponsableModel

FENStatusProxy = PostAPIProxy[
    EnvironmentFENStatusRequest, EnvironmentFENStatusResponse, FENStatusRequestModel, FENStatusResponsableModel
]


class FENStatus(FENStatusProxy):
    async def jsondict_to_response(self, jsondict: dict[str, Any]) -> EnvironmentFENStatusResponse:
        return EnvironmentFENStatusResponse.parse_obj(jsondict)

    async def executed(self, request: FENStatusRequestModel) -> EventAGen:
        try:
            yield await self.usecase.response(
                EnvironmentFENStatusResponseToModel.from_dto(
                    await self.fetch(FENStatusRequestToDTO.from_model(request).convert())
                ).convert()
            )
        except RequestError as ex:
            yield await self.usecase.response(
                ConvertedRequestErrorResponseModel(ex.request.url, ex.args[0], "fen-status").convert()
            )
        except HTTPStatusError as ex:
            yield await self.usecase.response(
                ConvertedHTTPStatusErrorResponseModel(
                    ex.response.status_code, ex.request.url, ex.response.json(), "fen-status"
                ).convert()
            )
