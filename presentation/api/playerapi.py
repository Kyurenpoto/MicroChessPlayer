# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from typing import Optional

from application.playground import MicroChessPlayGround
from domain.dto.playerdto import (
    PlayerErrorResponse,
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from fastapi import APIRouter, status
from presentation.response import (
    CreatedGameResponse,
    CreatedMeasurementResponse,
    CreatedTrajectoryResponse,
    ExceptionHandledResponse,
    HALJSONResponse,
)
from pydantic.networks import AnyHttpUrl

router: APIRouter = APIRouter(prefix="/player")
playground: Optional[MicroChessPlayGround] = None


def setting(url_env: AnyHttpUrl) -> None:
    global playground

    playground = MicroChessPlayGround.from_url(url_env, {route.name: route.path for route in router.routes})


responses: dict[int, dict] = {
    status.HTTP_400_BAD_REQUEST: {
        "model": PlayerErrorResponse,
        "description": "Requested with invalid url",
    },
    status.HTTP_404_NOT_FOUND: {
        "model": PlayerErrorResponse,
        "description": "An error occured while requesting",
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": PlayerErrorResponse,
        "description": "Received a response with a failed status",
    },
}


@router.post(
    "/trajectory",
    name="trajectory",
    description="Trajactory starting with the requested FEN",
    status_code=status.HTTP_200_OK,
    response_model=PlayerTrajectoryResponse,
    responses={**responses},
)
async def trajectory(request: PlayerTrajectoryRequest) -> HALJSONResponse:
    return await ExceptionHandledResponse(CreatedTrajectoryResponse(request)).handled(playground)


@router.post(
    "/game",
    name="game",
    description="Trajactory from starting FEN to end",
    status_code=status.HTTP_200_OK,
    response_model=PlayerGameResponse,
    responses={**responses},
)
async def game(request: PlayerGameRequest) -> HALJSONResponse:
    return await ExceptionHandledResponse(CreatedGameResponse(request)).handled(playground)


@router.post(
    "/measurement",
    name="measurment",
    description="Measurement of win/lose/draw when playing white",
    status_code=status.HTTP_200_OK,
    response_model=PlayerMeasurementResponse,
    responses={**responses},
)
async def measurement(request: PlayerMeasurementRequest) -> HALJSONResponse:
    return await ExceptionHandledResponse(CreatedMeasurementResponse(request)).handled(playground)
