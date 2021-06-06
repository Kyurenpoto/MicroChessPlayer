# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from typing import NamedTuple

from domain.dto.playerdto import (
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerMeasurementRequest,
    PlayerMeasurementResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from domain.player import MicroChessPlayer


class MicroChessPlayGround(NamedTuple):
    player: MicroChessPlayer

    @classmethod
    def from_url(cls, url_env: str) -> MicroChessPlayGround:
        return MicroChessPlayGround(MicroChessPlayer.from_url(url_env))

    async def trajectory(self, request: PlayerTrajectoryRequest) -> PlayerTrajectoryResponse:
        return await self.player.trajectory(request)

    async def game(self, request: PlayerGameRequest) -> PlayerGameResponse:
        return await self.player.game(request)

    async def measurement(self, request: PlayerMeasurementRequest) -> PlayerMeasurementResponse:
        return await self.player.measurement(request)
