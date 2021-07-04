# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT


from abc import ABCMeta, abstractmethod

from src.usecase.requestmodel import GameRequestModel, MeasurementRequestModel, TrajectoryRequestModel


class TrajectoryRequestBoundary(metaclass=ABCMeta):
    @abstractmethod
    async def request(self, request_model: TrajectoryRequestModel) -> None:
        pass


class GameRequestBoundary(metaclass=ABCMeta):
    @abstractmethod
    async def request(self, request_model: GameRequestModel) -> None:
        pass


class MeasurementRequestBoundary(metaclass=ABCMeta):
    @abstractmethod
    async def request(self, request_model: MeasurementRequestModel) -> None:
        pass
