# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

import pytest
import respx
from domain.dto.playerdto import PlayerHAL, PlayerURL
from domain.implementation.movement import FEN, SAN
from fastapi import status
from httpx import AsyncClient, Response
from presentation.api.playerapi import setting


@pytest.mark.asyncio
@respx.mock
async def test_trajectory(async_client: AsyncClient) -> None:
    respx.post("http://fake-env/model/fen-status").mock(
        side_effect=[
            Response(
                status.HTTP_200_OK,
                json={
                    "statuses": [1],
                    "legal_moves": [
                        [
                            "e4e5",
                            "e4e6",
                            "e4e7",
                            "f4e5",
                            "f4g5",
                            "f4h6",
                            "g4e5",
                            "g4f6",
                            "g4h6",
                            "h4g5",
                            "h5h6",
                        ]
                    ],
                },
            )
        ]
        * 8
    )

    respx.post("http://fake-env/model/next-fen").mock(
        side_effect=[
            Response(
                status.HTTP_200_OK,
                json={"next_fens": [FEN.first()]},
            ),
            Response(
                status.HTTP_200_OK,
                json={"next_fens": [FEN.starting()]},
            ),
        ]
        * 3
    )

    respx.post("http://fake-ai/ai/next-san").mock(
        side_effect=[
            Response(
                status.HTTP_200_OK,
                json={"next_sans": [SAN.first()]},
            ),
        ]
        * 6
    )

    setting(PlayerURL(url="http://fake-env"))

    response = await async_client.post(
        url="/player/trajectory",
        json={
            "fens": [FEN.starting(), FEN.first()],
            "white": {"url": "http://fake-ai"},
            "black": {"url": "http://fake-ai"},
            "step": 3,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "links": {
            rel: {"href": url.href}
            for rel, url in PlayerHAL.from_apis_with_requested(
                {
                    "trajectory": "/player/trajectory",
                    "game": "/player/game",
                    "measurement": "/player/measurement",
                },
                "trajectory",
                "post",
            ).links.items()
        },
        "fens": (([[FEN.starting()] * 2] * 2) + ([[FEN.first()] * 2] * 2)),
        "sans": [[SAN.first()]] * 4,
        "results": [[0, 0]] * 4,
    }


@pytest.mark.asyncio
async def test_trajectory_not_found(async_client: AsyncClient) -> None:
    setting(PlayerURL(url="http://fake-env"))

    response = await async_client.post(
        url="/player/trajectory",
        json={
            "fens": [FEN.starting(), FEN.first()],
            "white": {"url": "http://fake-ai"},
            "black": {"url": "http://fake-ai"},
            "step": 3,
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
@respx.mock
async def test_trajectory_unprocessable_entity(async_client: AsyncClient) -> None:
    respx.post("http://fake-env/model/fen-status").mock(
        side_effect=[Response(status.HTTP_422_UNPROCESSABLE_ENTITY, json={})]
    )

    setting(PlayerURL(url="http://fake-env"))

    response = await async_client.post(
        url="/player/trajectory",
        json={
            "fens": [FEN.starting(), FEN.first()],
            "white": {"url": "http://fake-ai"},
            "black": {"url": "http://fake-ai"},
            "step": 3,
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@respx.mock
async def test_game(async_client: AsyncClient) -> None:
    respx.post("http://fake-env/model/fen-status").mock(
        side_effect=[
            Response(
                status.HTTP_200_OK,
                json={
                    "statuses": [2],
                    "legal_moves": [[]],
                },
            )
        ]
    )

    setting(PlayerURL(url="http://fake-env"))

    response = await async_client.post(
        url="/player/game",
        json={
            "white": {"url": "http://fake-ai"},
            "black": {"url": "http://fake-ai"},
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "links": {
            rel: {"href": url.href}
            for rel, url in PlayerHAL.from_apis_with_requested(
                {
                    "trajectory": "/player/trajectory",
                    "game": "/player/game",
                    "measurement": "/player/measurement",
                },
                "game",
                "post",
            ).links.items()
        },
        "fens": [FEN.starting()],
        "sans": [],
        "result": "1-0",
    }


@pytest.mark.asyncio
async def test_game_not_found(async_client: AsyncClient) -> None:
    setting(PlayerURL(url="http://fake-env"))

    response = await async_client.post(
        url="/player/game",
        json={
            "white": {"url": "http://fake-ai"},
            "black": {"url": "http://fake-ai"},
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
@respx.mock
async def test_game_unprocessable_entity(async_client: AsyncClient) -> None:
    respx.post("http://fake-env/model/fen-status").mock(
        side_effect=[Response(status.HTTP_422_UNPROCESSABLE_ENTITY, json={})]
    )

    setting(PlayerURL(url="http://fake-env"))

    response = await async_client.post(
        url="/player/game",
        json={
            "white": {"url": "http://fake-ai"},
            "black": {"url": "http://fake-ai"},
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@respx.mock
async def test_measurement(async_client: AsyncClient) -> None:
    respx.post("http://fake-env/model/fen-status").mock(
        side_effect=[
            Response(
                status.HTTP_200_OK,
                json={
                    "statuses": [2],
                    "legal_moves": [[]],
                },
            ),
            Response(
                status.HTTP_200_OK,
                json={
                    "statuses": [3],
                    "legal_moves": [[]],
                },
            ),
            Response(
                status.HTTP_200_OK,
                json={
                    "statuses": [1],
                    "legal_moves": [
                        [
                            "e4e5",
                            "e4e6",
                            "e4e7",
                            "f4e5",
                            "f4g5",
                            "f4h6",
                            "g4e5",
                            "g4f6",
                            "g4h6",
                            "h4g5",
                            "h5h6",
                        ]
                    ],
                },
            ),
            Response(
                status.HTTP_200_OK,
                json={
                    "statuses": [2],
                    "legal_moves": [[]],
                },
            ),
        ]
    )

    respx.post("http://fake-env/model/next-fen").mock(
        side_effect=[
            Response(
                status.HTTP_200_OK,
                json={"next_fens": [FEN.first()]},
            )
        ]
    )

    respx.post("http://fake-ai/ai/next-san").mock(
        side_effect=[
            Response(
                status.HTTP_200_OK,
                json={"next_sans": [SAN.first()]},
            )
        ]
    )

    setting(PlayerURL(url="http://fake-env"))

    response = await async_client.post(
        url="/player/measurement",
        json={
            "white": {"url": "http://fake-ai"},
            "black": {"url": "http://fake-ai"},
            "playtime": 3,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "links": {
            rel: {"href": url.href}
            for rel, url in PlayerHAL.from_apis_with_requested(
                {
                    "trajectory": "/player/trajectory",
                    "game": "/player/game",
                    "measurement": "/player/measurement",
                },
                "measurement",
                "post",
            ).links.items()
        },
        "white": {"score": 1.5, "win": 1, "draw": 1, "lose": 1},
        "black": {"score": 1.5, "win": 1, "draw": 1, "lose": 1},
    }


@pytest.mark.asyncio
async def test_measurement_not_found(async_client: AsyncClient) -> None:
    setting(PlayerURL(url="http://fake-env"))

    response = await async_client.post(
        url="/player/measurement",
        json={
            "white": {"url": "http://fake-ai"},
            "black": {"url": "http://fake-ai"},
            "playtime": 3,
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
@respx.mock
async def test_measurement_unprocessable_entity(async_client: AsyncClient) -> None:
    respx.post("http://fake-env/model/fen-status").mock(
        side_effect=[Response(status.HTTP_422_UNPROCESSABLE_ENTITY, json={})]
    )

    setting(PlayerURL(url="http://fake-env"))

    response = await async_client.post(
        url="/player/measurement",
        json={
            "white": {"url": "http://fake-ai"},
            "black": {"url": "http://fake-ai"},
            "playtime": 3,
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
