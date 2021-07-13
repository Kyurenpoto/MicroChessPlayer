# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT


from abc import ABCMeta, abstractmethod

from src.model.responsemodel import GameResponseModel, MeasurementResponseModel, TrajectoryResponseModel


class TrajectoryResponseBoundary(metaclass=ABCMeta):
    @abstractmethod
    async def response(self, response_model: TrajectoryResponseModel) -> None:
        pass


class GameResponseBoundary(metaclass=ABCMeta):
    @abstractmethod
    async def response(self, response_model: GameResponseModel) -> None:
        pass


class MeasurementResponseBoundary(metaclass=ABCMeta):
    @abstractmethod
    async def response(self, response_model: MeasurementResponseModel) -> None:
        pass
