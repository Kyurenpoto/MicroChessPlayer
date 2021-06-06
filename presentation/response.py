# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Optional, Union

from application.playground import MicroChessPlayGround
from domain.dto.playerdto import (
    PlayerAIInfo,
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
    def name(self) -> str:
        pass

    @abstractmethod
    def param(self) -> str:
        pass

    @abstractmethod
    def value(
        self,
    ) -> Union[
        tuple[list[str], PlayerAIInfo, PlayerAIInfo, int],
        tuple[PlayerAIInfo, PlayerAIInfo],
        tuple[PlayerAIInfo, PlayerAIInfo, int],
    ]:
        pass


class CreatedTrajectoryResponse(TrajectoryRequestData, ICreatedResponse):
    async def created(self, playground: Optional[MicroChessPlayGround]) -> OkResponse:
        return OkResponse.from_response_data(await playground.trajectory(self.request))

    def name(self) -> str:
        return "trajectory"

    def param(self) -> str:
        return "fens, white, black, step"

    def value(
        self,
    ) -> Union[
        tuple[list[str], PlayerAIInfo, PlayerAIInfo, int],
        tuple[PlayerAIInfo, PlayerAIInfo],
        tuple[PlayerAIInfo, PlayerAIInfo, int],
    ]:
        return self.request.fens, self.request.white, self.request.black, self.request.step


class CreatedGameResponse(GameRequestData, ICreatedResponse):
    async def created(self, playground: Optional[MicroChessPlayGround]) -> OkResponse:
        return OkResponse.from_response_data(await playground.game(self.request))

    def name(self) -> str:
        return "game"

    def param(self) -> str:
        return "white, black"

    def value(
        self,
    ) -> Union[
        tuple[list[str], PlayerAIInfo, PlayerAIInfo, int],
        tuple[PlayerAIInfo, PlayerAIInfo],
        tuple[PlayerAIInfo, PlayerAIInfo, int],
    ]:
        return self.request.white, self.request.black


class CreatedMeasurementResponse(RateRequestData, ICreatedResponse):
    async def created(self, playground: Optional[MicroChessPlayGround]) -> OkResponse:
        return OkResponse.from_response_data(await playground.measurement(self.request))

    def name(self) -> str:
        return "measurement"

    def param(self) -> str:
        return "white, black, playtime"

    def value(
        self,
    ) -> Union[
        tuple[list[str], PlayerAIInfo, PlayerAIInfo, int],
        tuple[PlayerAIInfo, PlayerAIInfo],
        tuple[PlayerAIInfo, PlayerAIInfo, int],
    ]:
        return self.request.white, self.request.black


class ExceptionHandledResponse(NamedTuple):
    created: ICreatedResponse

    async def handled(self, playground: Optional[MicroChessPlayGround]) -> JSONResponse:
        try:
            return await self.created.created(playground)
        except InvalidURL as ex:
            return BadRequestResponse.from_response_data(
                PlayerErrorResponse(
                    links=PlayerHAL.from_with_apis_requested(playground.player.apis, self.created.name()).links,
                    message=f"Requested with invalid url: {ex.args[0]!r}",
                    location="body",
                    param=self.created.param(),
                    value=self.created.value(),
                    error="request.InvalidURL",
                ),
            )
        except RequestError as ex:
            return NotFoundResponse.from_response_data(
                PlayerErrorResponse(
                    links=PlayerHAL.from_with_apis_requested(playground.player.apis, self.created.name()).links,
                    message=f"An error occurred while requesting {ex.request.url!r}: {ex.args[0]!r}",
                    location="body",
                    param=self.created.param(),
                    value=self.created.value(),
                    error="request.RequestError",
                ),
            )
        except HTTPStatusError as ex:
            return UnprocessableEntityResponse.from_response_data(
                PlayerErrorResponse(
                    links=PlayerHAL.from_with_apis_requested(playground.player.apis, self.created.name()).links,
                    message=(
                        f"Error response {ex.response.status_code} "
                        + f"while requesting {ex.request.url!r}: {ex.response.json()!r}"
                    ),
                    location="body",
                    param=self.created.param(),
                    value=self.created.value(),
                    error="request.HTTPStatusError",
                ),
            )
