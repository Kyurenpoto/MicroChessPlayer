# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import Any

from httpx import AsyncClient, Response


class PostClient(str):
    async def post(self, data: dict[str, Any]) -> dict[str, Any]:
        async with AsyncClient() as client:
            response: Response = await client.post(url=self, json=data, timeout=1.0)

        response.raise_for_status()

        return response.json()
