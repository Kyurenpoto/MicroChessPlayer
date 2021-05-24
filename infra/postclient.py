# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from typing import Any

from httpx import AsyncClient, Response
from starlette.status import HTTP_200_OK


class PostClient(str):
    async def post(self, data: dict[str, Any]) -> dict[str, Any]:
        async with AsyncClient() as client:
            response: Response = await client.post(url=self, data=data)

        if response.status_code == HTTP_200_OK:
            return response.json()

        raise RuntimeError(response.json())
