# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, status
from fastapi.params import Depends
from src.application.createdresponse import CreatedGameResponse, CreatedMeasurementResponse, CreatedTrajectoryResponse
from src.config import Container
from src.domain.dto.playerdto import (
    PlayerErrorResponse,
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerInternalModel,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from src.presentation.response import ExceptionHandledResponse
from submodules.fastapi_haljson.src.halresponse import HALJSONResponse

router: APIRouter = APIRouter(prefix="/player")


responses: dict[int, dict] = {
    status.HTTP_400_BAD_REQUEST: {
        "model": PlayerErrorResponse,
        "description": "Requested with invalid url",
        "content": {"application/hal+json": {"schema": {"$ref": "#/components/schemas/PlayerErrorResponse"}}},
    },
    status.HTTP_404_NOT_FOUND: {
        "model": PlayerErrorResponse,
        "description": "An error occured while requesting",
        "content": {"application/hal+json": {"schema": {"$ref": "#/components/schemas/PlayerErrorResponse"}}},
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": PlayerErrorResponse,
        "description": "Received a response with a failed status",
        "content": {"application/hal+json": {"schema": {"$ref": "#/components/schemas/PlayerErrorResponse"}}},
    },
}


@router.post(
    "/trajectory",
    name="trajectory",
    description="Trajactory starting with the requested FEN",
    status_code=status.HTTP_200_OK,
    response_model=PlayerTrajectoryResponse,
    responses={
        status.HTTP_200_OK: {
            "model": PlayerTrajectoryResponse,
            "content": {"application/hal+json": {"schema": {"$ref": "#/components/schemas/PlayerTrajectoryResponse"}}},
        },
        **responses,
    },
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
    responses={
        status.HTTP_200_OK: {
            "model": PlayerGameResponse,
            "content": {"application/hal+json": {"schema": {"$ref": "#/components/schemas/PlayerGameResponse"}}},
        },
        **responses,
    },
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
    responses={
        status.HTTP_200_OK: {
            "model": PlayerMeasurementResponse,
            "content": {"application/hal+json": {"schema": {"$ref": "#/components/schemas/PlayerMeasurementResponse"}}},
        },
        **responses,
    },
)
@inject
async def measurement(
    request: PlayerMeasurementRequest, internal_model: PlayerInternalModel = Depends(Provide[Container.internal_model])
) -> HALJSONResponse:
    return await ExceptionHandledResponse(internal_model, CreatedMeasurementResponse(request)).handled()
