# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT


from abc import ABC, abstractmethod

from src.model.requestmodel import (
    FENStatusRequestModel,
    GameRequestModel,
    MeasurementRequestModel,
    NextFENRequestModel,
    NextSANRequestModel,
    TrajectoryRequestModel,
)


class TrajectoryRequestBoundary(ABC):
    @abstractmethod
    async def request(self, request_model: TrajectoryRequestModel) -> None:
        pass


class GameRequestBoundary(ABC):
    @abstractmethod
    async def request(self, request_model: GameRequestModel) -> None:
        pass


class MeasurementRequestBoundary(ABC):
    @abstractmethod
    async def request(self, request_model: MeasurementRequestModel) -> None:
        pass


class NextFENRequestBoundary(ABC):
    @abstractmethod
    def request(self, request_model: NextFENRequestModel) -> None:
        pass


class NextSANRequestBoundary(ABC):
    @abstractmethod
    def request(self, request_model: NextSANRequestModel) -> None:
        pass


class FENStatusRequestBoundary(ABC):
    @abstractmethod
    def request(self, request_model: FENStatusRequestModel) -> None:
        pass
