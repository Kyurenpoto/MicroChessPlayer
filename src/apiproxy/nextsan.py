# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import Any

from src.core.apiproxy import PostAPIProxy
from src.framework.dto.aidto import AINextSANRequest, AINextSANResponse

NextSANProxy = PostAPIProxy[AINextSANRequest, AINextSANResponse]


class NextSAN(NextSANProxy):
    async def jsondict_to_response(self, jsondict: dict[str, Any]) -> AINextSANResponse:
        return AINextSANResponse.parse_obj(jsondict)
