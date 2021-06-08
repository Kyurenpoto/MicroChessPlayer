# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

import pytest
from httpx import AsyncClient
from main import app


@pytest.fixture
async def async_client() -> AsyncClient:
    client = AsyncClient(app=app, base_url="http://test")
    yield client
    await client.aclose()
