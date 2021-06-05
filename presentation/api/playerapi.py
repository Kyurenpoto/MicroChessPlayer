# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from typing import Optional

from application.playground import MicroChessPlayGround
from domain.dto.playerdto import (
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse
from presentation.response import (
    CreatedGameResponse,
    CreatedMesurementResponse,
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
    description="Trajactory starting with the requested FEN",
    status_code=status.HTTP_200_OK,
    response_model=PlayerTrajectoryResponse,
)
async def trajectory(request: PlayerTrajectoryRequest) -> JSONResponse:
    return await ExceptionHandledResponse(CreatedTrajectoryResponse(request)).handled(playground)


@router.post(
    "/game",
    description="Trajactory from starting FEN to end",
    status_code=status.HTTP_200_OK,
    response_model=PlayerGameResponse,
)
async def game(request: PlayerGameRequest) -> JSONResponse:
    return await ExceptionHandledResponse(CreatedGameResponse(request)).handled(playground)


@router.post(
    "/mesurement",
    description="Mesurement of win/lose/draw when playing white",
    status_code=status.HTTP_200_OK,
    response_model=PlayerMeasurementResponse,
)
async def mesurement(request: PlayerMeasurementRequest) -> JSONResponse:
    return await ExceptionHandledResponse(CreatedMesurementResponse(request)).handled(playground)
