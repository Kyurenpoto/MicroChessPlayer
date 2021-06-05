# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Optional

from application.playground import MicroChessPlayGround
from domain.dto.playerdto import PlayerGameRequest, PlayerMeasurementRequest, PlayerTrajectoryRequest
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from httpx import HTTPStatusError, InvalidURL, RequestError


class TrajectoryRequestData(NamedTuple):
    request: PlayerTrajectoryRequest


class GameRequestData(NamedTuple):
    request: PlayerGameRequest


class RateRequestData(NamedTuple):
    request: PlayerMeasurementRequest


class ICreatedResponse(metaclass=ABCMeta):
    @abstractmethod
    async def created(self, playground: Optional[MicroChessPlayGround]) -> JSONResponse:
        pass


class CreatedTrajectoryResponse(TrajectoryRequestData, ICreatedResponse):
    async def created(self, playground: Optional[MicroChessPlayGround]) -> JSONResponse:
        return JSONResponse(content=jsonable_encoder(await playground.trajectory(self.request)))


class CreatedGameResponse(GameRequestData, ICreatedResponse):
    async def created(self, playground: Optional[MicroChessPlayGround]) -> JSONResponse:
        return JSONResponse(content=jsonable_encoder(await playground.game(self.request)))


class CreatedMesurementResponse(RateRequestData, ICreatedResponse):
    async def created(self, playground: Optional[MicroChessPlayGround]) -> JSONResponse:
        return JSONResponse(content=jsonable_encoder(await playground.mesurement(self.request)))


class ExceptionHandledResponse(NamedTuple):
    created: ICreatedResponse

    async def handled(self, playground: Optional[MicroChessPlayGround]) -> JSONResponse:
        try:
            return await self.created.created(playground)
        except InvalidURL as ex:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=jsonable_encoder(f"Requested with invalid url: {ex.args[0]!r}"),
            )
        except RequestError as ex:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=jsonable_encoder(f"An error occurred while requesting {ex.request.url!r}: {ex.args[0]!r}"),
            )
        except HTTPStatusError as ex:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content=jsonable_encoder(
                    f"Error response {ex.response.status_code} "
                    + f"while requesting {ex.request.url!r}: {ex.response.json()!r}"
                ),
            )
