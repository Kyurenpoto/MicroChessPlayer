# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod

from src.usecase.requestmodel import FENStatusRequestModel, NextFENRequestModel, NextSANRequestModel


class NextFENRequestGateway(ABC):
    @abstractmethod
    def request(self, request_model: NextFENRequestModel) -> None:
        pass


class NextSANRequestGateway(ABC):
    @abstractmethod
    def request(self, request_model: NextSANRequestModel) -> None:
        pass


class FENStatusRequestGateway(ABC):
    @abstractmethod
    def request(self, request_model: FENStatusRequestModel) -> None:
        pass
