# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Optional

from application.playground import MicroChessPlayGround
from domain.dto.playerdto import (
    PlayerErrorResponse,
    PlayerGameRequest,
    PlayerHAL,
    PlayerMeasurementRequest,
    PlayerTrajectoryRequest,
)
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from httpx import HTTPStatusError, InvalidURL, RequestError


class OkResponse(JSONResponse):
    @classmethod
    def from_response_data(cls, data) -> OkResponse:
        return OkResponse(content=jsonable_encoder(data))


class BadRequestResponse(JSONResponse):
    @classmethod
    def from_response_data(cls, data) -> BadRequestResponse:
        return BadRequestResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(data))


class NotFoundResponse(JSONResponse):
    @classmethod
    def from_response_data(cls, data) -> NotFoundResponse:
        return NotFoundResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(data))


class UnprocessableEntityResponse(JSONResponse):
    @classmethod
    def from_response_data(cls, data) -> UnprocessableEntityResponse:
        return UnprocessableEntityResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(data)
        )


class TrajectoryRequestData(NamedTuple):
    request: PlayerTrajectoryRequest


class GameRequestData(NamedTuple):
    request: PlayerGameRequest


class RateRequestData(NamedTuple):
    request: PlayerMeasurementRequest


class ICreatedResponse(metaclass=ABCMeta):
    @abstractmethod
    async def created(self, playground: Optional[MicroChessPlayGround]) -> OkResponse:
        pass

    @abstractmethod
    def error(self, playground: Optional[MicroChessPlayGround], message: str, error_type: str) -> PlayerErrorResponse:
        pass


class CreatedTrajectoryResponse(TrajectoryRequestData, ICreatedResponse):
    async def created(self, playground: Optional[MicroChessPlayGround]) -> OkResponse:
        return OkResponse.from_response_data(await playground.trajectory(self.request))

    def error(self, playground: Optional[MicroChessPlayGround], message: str, error_type: str) -> PlayerErrorResponse:
        return PlayerErrorResponse(
            links=PlayerHAL.from_apis_with_requested(playground.player.apis, "trajectory", "post").links,
            message=message,
            location="body",
            param="fens, white, black, step",
            value=(self.request.fens, self.request.white, self.request.black, self.request.step),
            error=error_type,
        )


class CreatedGameResponse(GameRequestData, ICreatedResponse):
    async def created(self, playground: Optional[MicroChessPlayGround]) -> OkResponse:
        return OkResponse.from_response_data(await playground.game(self.request))

    def error(self, playground: Optional[MicroChessPlayGround], message: str, error_type: str) -> PlayerErrorResponse:
        return PlayerErrorResponse(
            links=PlayerHAL.from_apis_with_requested(playground.player.apis, "game", "post").links,
            message=message,
            location="body",
            param="white, black",
            value=(self.request.white, self.request.black),
            error=error_type,
        )


class CreatedMeasurementResponse(RateRequestData, ICreatedResponse):
    async def created(self, playground: Optional[MicroChessPlayGround]) -> OkResponse:
        return OkResponse.from_response_data(await playground.measurement(self.request))

    def error(self, playground: Optional[MicroChessPlayGround], message: str, error_type: str) -> PlayerErrorResponse:
        return PlayerErrorResponse(
            links=PlayerHAL.from_apis_with_requested(playground.player.apis, "measurement", "post").links,
            message=message,
            location="body",
            param="white, black, playtime",
            value=(self.request.white, self.request.black, self.request.playtime),
            error=error_type,
        )


class ExceptionHandledResponse(NamedTuple):
    created: ICreatedResponse

    async def handled(self, playground: Optional[MicroChessPlayGround]) -> JSONResponse:
        try:
            return await self.created.created(playground)
        except InvalidURL as ex:
            return BadRequestResponse.from_response_data(
                self.created.error(playground, f"Requested with invalid url: {ex.args[0]!r}", "request.InvalidURL")
            )
        except RequestError as ex:
            return NotFoundResponse.from_response_data(
                self.created.error(
                    playground,
                    f"An error occurred while requesting {ex.request.url!r}: {ex.args[0]!r}",
                    "request.RequestError",
                )
            )
        except HTTPStatusError as ex:
            return UnprocessableEntityResponse.from_response_data(
                self.created.error(
                    playground,
                    f"Error response {ex.response.status_code} "
                    + f"while requesting {ex.request.url!r}: {ex.response.json()!r}",
                    "request.HTTPStatusError",
                )
            )
