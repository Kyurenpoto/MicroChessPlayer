# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from src.config import Container
from src.framework.dto.playerdto import (
    PlayerGameRequest,
    PlayerInternal,
    PlayerMeasurementRequest,
    PlayerTrajectoryRequest,
)
from src.model.requestmodel import (
    GameRequestModel,
    MeasurementRequestModel,
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
