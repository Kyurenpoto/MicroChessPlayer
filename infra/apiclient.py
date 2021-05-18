# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from typing import Any, Dict

from httpx import AsyncClient, Response
from starlette.status import HTTP_200_OK


class APIClient:
    __slots__ = ["__url"]

    __url: str

    def __init__(self, url: str):
        self.__url = url

    async def post(self, data: Dict[str, Any]) -> Dict[str, Any]:
        async with AsyncClient() as client:
            response: Response = await client.post(url=self.__url, data=data)

        if response.status_code == HTTP_200_OK:
            return response.json()

        raise RuntimeError(response.json())
