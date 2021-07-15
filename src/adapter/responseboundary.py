# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT


from abc import ABCMeta, abstractmethod

from src.model.responsemodel import GameResponsableModel, MeasurementResponsableModel, TrajectoryResponsableModel


class TrajectoryResponseBoundary(metaclass=ABCMeta):
    @abstractmethod
    async def response(self, response_model: TrajectoryResponsableModel) -> None:
        pass


class GameResponseBoundary(metaclass=ABCMeta):
    @abstractmethod
    async def response(self, response_model: GameResponsableModel) -> None:
        pass


class MeasurementResponseBoundary(metaclass=ABCMeta):
    @abstractmethod
    async def response(self, response_model: MeasurementResponsableModel) -> None:
        pass
