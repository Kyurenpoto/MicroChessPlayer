# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod

from src.model.responsemodel import FENStatusResponseModel, NextFENResponseModel, NextSANResponseModel


class NextFENResponseGateway(ABC):
    @abstractmethod
    def request(self, response_model: NextFENResponseModel) -> None:
        pass


class NextSANResponseGateway(ABC):
    @abstractmethod
    def request(self, response_model: NextSANResponseModel) -> None:
        pass


class FENStatusResponseGateway(ABC):
    @abstractmethod
    def request(self, response_model: FENStatusResponseModel) -> None:
        pass
