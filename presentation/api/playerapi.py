# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from typing import Optional

from application.playground import MicroChessPlayGround
from domain.dto.playerdto import PlayerGameRequest, PlayerRateRequest, PlayerTrajectoryRequest
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from presentation.response import (
    CreatedGameResponse,
    CreatedRateResponse,
    CreatedTrajectoryResponse,
    ExceptionHandledResponse,
)

router: APIRouter = APIRouter(prefix="/player")
playground: Optional[MicroChessPlayGround] = None


def setting(url_env: str) -> None:
    global playground

    playground = MicroChessPlayGround.from_url(url_env)


@router.post(
    "/trajectory",
    status_code=status.HTTP_200_OK,
    description="Trajactory starting with the requested FEN",
)
async def trajectory(request: PlayerTrajectoryRequest) -> JSONResponse:
    return await ExceptionHandledResponse(CreatedTrajectoryResponse(request)).handled(playground)


@router.post(
    "/game",
    status_code=status.HTTP_200_OK,
    description="Trajactory from starting FEN to end",
)
async def game(request: PlayerGameRequest) -> JSONResponse:
    return await ExceptionHandledResponse(CreatedGameResponse(request)).handled(playground)


@router.post(
    "/rate",
    status_code=status.HTTP_200_OK,
    description="Win rate when playing black and white respectively",
)
async def rate(request: PlayerRateRequest) -> JSONResponse:
    return await ExceptionHandledResponse(CreatedRateResponse(request)).handled(playground)
