# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from application.createdresponse import CreatedGameResponse, CreatedMeasurementResponse, CreatedTrajectoryResponse
from config import Container
from dependency_injector.wiring import Provide, inject
from domain.dto.playerdto import (
    PlayerErrorResponse,
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerInternalModel,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from fastapi import APIRouter, status
from fastapi.params import Depends
from presentation.response import ExceptionHandledResponse, HALJSONResponse

router: APIRouter = APIRouter(prefix="/player")


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
@inject
async def trajectory(
    request: PlayerTrajectoryRequest, internal_model: PlayerInternalModel = Depends(Provide[Container.internal_model])
) -> HALJSONResponse:
    return await ExceptionHandledResponse(internal_model, CreatedTrajectoryResponse(request)).handled()


@router.post(
    "/game",
    name="game",
    description="Trajactory from starting FEN to end",
    status_code=status.HTTP_200_OK,
    response_model=PlayerGameResponse,
    responses={**responses},
)
@inject
async def game(
    request: PlayerGameRequest, internal_model: PlayerInternalModel = Depends(Provide[Container.internal_model])
) -> HALJSONResponse:
    return await ExceptionHandledResponse(internal_model, CreatedGameResponse(request)).handled()


@router.post(
    "/measurement",
    name="measurement",
    description="Measurement of win/lose/draw when playing white",
    status_code=status.HTTP_200_OK,
    response_model=PlayerMeasurementResponse,
    responses={**responses},
)
@inject
async def measurement(
    request: PlayerMeasurementRequest, internal_model: PlayerInternalModel = Depends(Provide[Container.internal_model])
) -> HALJSONResponse:
    return await ExceptionHandledResponse(internal_model, CreatedMeasurementResponse(request)).handled()
