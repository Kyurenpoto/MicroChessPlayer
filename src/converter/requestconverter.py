# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from src.config import Container
from src.framework.dto.aidto import AINextSANRequest
from src.framework.dto.environmentdto import EnvironmentFENStatusRequest, EnvironmentNextFENRequest
from src.framework.dto.playerdto import (
    PlayerGameRequest,
    PlayerInternal,
    PlayerMeasurementRequest,
    PlayerTrajectoryRequest,
)
from src.model.requestmodel import (
    FENStatusRequestModel,
    GameRequestModel,
    MeasurementRequestModel,
    NextFENRequestModel,
    NextSANRequestModel,
    TrajectoryRequestModel,
    URLString,
)


class TrajectoryRequestToModel(PlayerTrajectoryRequest):
    @classmethod
    def from_dto(cls, dto: PlayerTrajectoryRequest) -> TrajectoryRequestToModel:
        return TrajectoryRequestToModel(fens=dto.fens, white=dto.white, black=dto.black, step=dto.step)

    @inject
    def convert(self, internal: PlayerInternal = Provide[Container.internal_model]) -> TrajectoryRequestModel:
        return TrajectoryRequestModel(
            URLString(internal.url_env), self.fens, URLString(self.white.url), URLString(self.black.url), self.step
        )


class GameRequestToModel(PlayerGameRequest):
    @classmethod
    def from_dto(cls, dto: PlayerGameRequest) -> GameRequestToModel:
        return GameRequestToModel(white=dto.white, black=dto.black)

    @inject
    def convert(self, internal: PlayerInternal = Provide[Container.internal_model]) -> GameRequestModel:
        return GameRequestModel(URLString(internal.url_env), URLString(self.white.url), URLString(self.black.url))


class MeasurementRequestToModel(PlayerMeasurementRequest):
    @classmethod
    def from_dto(cls, dto: PlayerMeasurementRequest) -> MeasurementRequestToModel:
        return MeasurementRequestToModel(white=dto.white, black=dto.black, playtime=dto.playtime)

    @inject
    def convert(self, internal: PlayerInternal = Provide[Container.internal_model]) -> MeasurementRequestModel:
        return MeasurementRequestModel(
            URLString(internal.url_env), URLString(self.white.url), URLString(self.black.url), self.playtime
        )


class NextFENRequestToDTO(NextFENRequestModel):
    @classmethod
    def from_model(cls, model: NextFENRequestModel) -> NextFENRequestToDTO:
        return NextFENRequestToDTO._make(model)

    def convert(self) -> EnvironmentNextFENRequest:
        return EnvironmentNextFENRequest(fens=self.fens, sans=self.sans)


class NextSANRequestToDTO(NextSANRequestModel):
    @classmethod
    def from_model(cls, model: NextSANRequestModel) -> NextSANRequestToDTO:
        return NextSANRequestToDTO._make(model)

    def convert(self) -> AINextSANRequest:
        return AINextSANRequest(fens=self.fens)


class FENStatusRequestToDTO(FENStatusRequestModel):
    @classmethod
    def from_model(cls, model: FENStatusRequestModel) -> FENStatusRequestToDTO:
        return FENStatusRequestToDTO._make(model)

    def convert(self) -> EnvironmentFENStatusRequest:
        return EnvironmentFENStatusRequest(fens=self.fens)
