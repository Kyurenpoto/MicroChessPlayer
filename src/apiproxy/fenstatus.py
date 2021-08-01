# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import Any

from src.core.apiproxy import PostAPIProxy
from src.framework.dto.environmentdto import EnvironmentFENStatusRequest, EnvironmentFENStatusResponse

FENStatusProxy = PostAPIProxy[EnvironmentFENStatusRequest, EnvironmentFENStatusResponse]


class FENStatus(FENStatusProxy):
    async def jsondict_to_response(self, jsondict: dict[str, Any]) -> EnvironmentFENStatusResponse:
        return EnvironmentFENStatusResponse.parse_obj(jsondict)
