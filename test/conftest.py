# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

import pytest
from httpx import AsyncClient
from main import app, unwire, wire
from src.config import Container


@pytest.fixture
async def async_client() -> AsyncClient:
    wire("http://fake-env")
    client = AsyncClient(app=app, base_url="http://test")
    yield client
    await client.aclose()


@pytest.fixture
async def container() -> Container:
    wire("http://test")
    yield app.state.container
    unwire()
