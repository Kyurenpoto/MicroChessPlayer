# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import NamedTuple

from src.adapter.requestboundary import MeasurementRequestBoundary
from src.adapter.responseboundary import MeasurementResponseBoundary
from src.converter.requestconverter import MeasurementRequestToModel
from src.converter.responseconverter import MeasurementResponseToDTO
from src.domain.dto.playerdto import PlayerMeasurementRequest, PlayerMeasurementResponse
from src.usecase.measurement import IMeasurement, MeasurementFactory
from src.usecase.requestmodel import MeasurementRequestModel
from src.usecase.responsemodel import MeasurementResponseModel


class MeasurementRequestIntentData(NamedTuple):
    usecase: IMeasurement


class MeasurementRequestIntent(MeasurementRequestIntentData, MeasurementRequestBoundary):
    async def request(self, request_model: MeasurementRequestModel) -> None:
        await self.usecase.executed(request_model)


class MeasurementResponseIntentData(NamedTuple):
    response_model: list[MeasurementResponseModel] = []


class MeasurementResponseIntent(MeasurementResponseIntentData, MeasurementResponseBoundary):
    response_model: list[MeasurementResponseModel] = []

    async def response(self, response_model: MeasurementResponseModel) -> None:
        self.response_model.append(response_model)

    async def pull(self) -> MeasurementResponseModel:
        return self.response_model[0]


class MeasurementIntent(NamedTuple):
    request_intent: MeasurementRequestIntent
    response_intent: MeasurementResponseIntent

    @classmethod
    def from_usecase_factory(cls, factory: MeasurementFactory) -> MeasurementIntent:
        response_intent: MeasurementResponseIntent = MeasurementResponseIntent()

        return MeasurementIntent(MeasurementRequestIntent(factory.createdMeasurement(response_intent)), response_intent)

    async def push(self, request: PlayerMeasurementRequest) -> None:
        await self.request_intent.request(MeasurementRequestToModel.from_dto(request).convert())

    async def pull(self) -> PlayerMeasurementResponse:
        return MeasurementResponseToDTO.from_model(await self.response_intent.pull()).convert()

    async def executed(self, request: PlayerMeasurementRequest) -> PlayerMeasurementResponse:
        await self.push(request)

        return await self.pull()
