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
    def from_url(cls, url_env: str, apis: dict[str, str]) -> MicroChessPlayGround:
        return MicroChessPlayGround(MicroChessPlayer.from_url(url_env, apis))

    async def trajectory(self, request: PlayerTrajectoryRequest, host: str) -> PlayerTrajectoryResponse:
        return await self.player.trajectory(request, host)

    async def game(self, request: PlayerGameRequest, host: str) -> PlayerGameResponse:
        return await self.player.game(request, host)

    async def measurement(self, request: PlayerMeasurementRequest, host: str) -> PlayerMeasurementResponse:
        return await self.player.measurement(request, host)
