# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations


class URLString(str):
    pass


class ApplicationState(str):
    pass


class EnvironmentState(ApplicationState):
    def FEN_status(self) -> EnvironmentState:
        return EnvironmentState("fen-status")

    def next_FEN(self) -> EnvironmentState:
        return EnvironmentState("next-fen")


class AIState(ApplicationState):
    def next_SAN(self) -> AIState:
        return AIState("next-san")


class ApplicationStateMap(dict[ApplicationState, URLString]):
    pass


class ExtendPolicy(int):
    pass


class FiniteExtendPolicy(ExtendPolicy):
    pass


class InfiniteExtendPolicy(ExtendPolicy):
    pass
