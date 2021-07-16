# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT


from abc import ABC, abstractmethod

from src.model.responsemodel import GameResponsableModel, MeasurementResponsableModel, TrajectoryResponsableModel


class TrajectoryResponseBoundary(ABC):
    @abstractmethod
    async def response(self, response_model: TrajectoryResponsableModel) -> None:
        pass


class GameResponseBoundary(ABC):
    @abstractmethod
    async def response(self, response_model: GameResponsableModel) -> None:
        pass


class MeasurementResponseBoundary(ABC):
    @abstractmethod
    async def response(self, response_model: MeasurementResponsableModel) -> None:
        pass
