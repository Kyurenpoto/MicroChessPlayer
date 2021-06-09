# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from application.createdresponse import CreatedGameResponse, CreatedMeasurementResponse, CreatedTrajectoryResponse
from domain.dto.playerdto import (
    PlayerErrorResponse,
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerInternalModel,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
    PlayerURL,
)
from fastapi import APIRouter, status
from presentation.response import ExceptionHandledResponse, HALJSONResponse

router: APIRouter = APIRouter(prefix="/player")
internal_model: PlayerInternalModel


def setting(url_env: PlayerURL) -> None:
    global internal_model

    internal_model = PlayerInternalModel(url_env=url_env, routes={route.name: route.path for route in router.routes})


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
    return await ExceptionHandledResponse(internal_model, CreatedTrajectoryResponse(request)).handled()


@router.post(
    "/game",
    name="game",
    description="Trajactory from starting FEN to end",
    status_code=status.HTTP_200_OK,
    response_model=PlayerGameResponse,
    responses={**responses},
)
async def game(request: PlayerGameRequest) -> HALJSONResponse:
    return await ExceptionHandledResponse(internal_model, CreatedGameResponse(request)).handled()


@router.post(
    "/measurement",
    name="measurement",
    description="Measurement of win/lose/draw when playing white",
    status_code=status.HTTP_200_OK,
    response_model=PlayerMeasurementResponse,
    responses={**responses},
)
async def measurement(request: PlayerMeasurementRequest) -> HALJSONResponse:
    return await ExceptionHandledResponse(internal_model, CreatedMeasurementResponse(request)).handled()
