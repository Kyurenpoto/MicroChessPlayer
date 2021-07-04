# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import NamedTuple

from src.adapter.requestboundary import TrajectoryRequestBoundary
from src.adapter.responseboundary import TrajectoryResponseBoundary
from src.converter.requestconverter import TrajectoryRequestToModel
from src.converter.responseconverter import TrajectoryResponseToDTO
from src.domain.dto.playerdto import PlayerTrajectoryRequest, PlayerTrajectoryResponse
from src.usecase.requestmodel import TrajectoryRequestModel
from src.usecase.responsemodel import TrajectoryResponseModel
from src.usecase.trajectory import FakeTrajectory, ITrajectory, Trajectory


class TrajectoryRequestIntentData(NamedTuple):
    usecase: ITrajectory


class TrajectoryRequestIntent(TrajectoryRequestIntentData, TrajectoryRequestBoundary):
    async def request(self, request_model: TrajectoryRequestModel) -> None:
        await self.usecase.executed(request_model)


class TrajectoryResponseIntentData(NamedTuple):
    response_model: list[TrajectoryResponseModel] = []


class TrajectoryResponseIntent(TrajectoryResponseIntentData, TrajectoryResponseBoundary):
    async def response(self, response_model: TrajectoryResponseModel) -> None:
        self.response_model.append(response_model)

    async def pull(self) -> TrajectoryResponseModel:
        return self.response_model[0]


class TrajectoryIntent(NamedTuple):
    request_intent: TrajectoryRequestIntent
    response_intent: TrajectoryResponseIntent

    @classmethod
    def from_usecase(cls) -> TrajectoryIntent:
        response_intent: TrajectoryResponseIntent = TrajectoryResponseIntent()

        return TrajectoryIntent(TrajectoryRequestIntent(Trajectory(response_intent)), response_intent)

    async def push(self, request: PlayerTrajectoryRequest) -> None:
        await self.request_intent.request(TrajectoryRequestToModel.from_dto(request).convert())

    async def pull(self) -> PlayerTrajectoryResponse:
        return TrajectoryResponseToDTO.from_model(await self.response_intent.pull()).convert()

    async def executed(self, request: PlayerTrajectoryRequest) -> PlayerTrajectoryResponse:
        await self.push(request)

        return await self.pull()


class FakeTrajectoryIntent(TrajectoryIntent):
    @classmethod
    def from_usecase(cls) -> FakeTrajectoryIntent:
        response_intent: TrajectoryResponseIntent = TrajectoryResponseIntent()

        return FakeTrajectoryIntent(TrajectoryRequestIntent(FakeTrajectory(response_intent)), response_intent)
