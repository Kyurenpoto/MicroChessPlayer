# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from domain.dto.playerdto import (
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerRateRequest,
    PlayerRateResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router: APIRouter = APIRouter(prefix="/player")


@router.post("/trajectory", status_code=status.HTTP_200_OK, description="Trajactory starting with the requested FEN")
async def trajectory(request: PlayerTrajectoryRequest) -> JSONResponse:
    try:
        return JSONResponse(content=jsonable_encoder(PlayerTrajectoryResponse()))
    except RuntimeError as ex:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(ex.args[0]))


@router.post(
    "/game",
    status_code=status.HTTP_200_OK,
    description="Trajactory from starting FEN to end",
)
async def game(request: PlayerGameRequest) -> JSONResponse:
    try:
        return JSONResponse(content=jsonable_encoder(PlayerGameResponse()))
    except RuntimeError as ex:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(ex.args[0]))


@router.post(
    "/rate",
    status_code=status.HTTP_200_OK,
    description="Win rate when playing black and white respectively",
)
async def rate(request: PlayerRateRequest) -> JSONResponse:
    try:
        return JSONResponse(content=jsonable_encoder(PlayerRateResponse()))
    except RuntimeError as ex:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(ex.args[0]))
