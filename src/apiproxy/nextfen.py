# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import Any

from src.core.apiproxy import PostAPIProxy
from src.framework.dto.environmentdto import EnvironmentNextFENRequest, EnvironmentNextFENResponse

NextFENProxy = PostAPIProxy[EnvironmentNextFENRequest, EnvironmentNextFENResponse]


class NextFEN(NextFENProxy):
    async def jsondict_to_response(self, jsondict: dict[str, Any]) -> EnvironmentNextFENResponse:
        return EnvironmentNextFENResponse.parse_obj(jsondict)
