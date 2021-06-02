# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from typing import NamedTuple

from domain.dto.playerdto import (
    PlayerAIResult,
    PlayerGameRequest,
    PlayerGameResponse,
    PlayerRateRequest,
    PlayerRateResponse,
    PlayerTrajectoryRequest,
    PlayerTrajectoryResponse,
)
from domain.implementation.game import Game
from domain.implementation.rate import Rate
from domain.implementation.trace import Trace
from domain.implementation.trajectory import Trajectory


class Results(list[float]):
    def __str__(self) -> str:
        if self[-1] == 0.5:
            return "1/2-1/2"

        return "1-0" if len(self) % 2 == 1 else "0-1"


class MicroChessPlayer(NamedTuple):
    url_env: str

    async def trajectory(self, request: PlayerTrajectoryRequest) -> PlayerTrajectoryResponse:
        produced: Trace = (
            await Trajectory.from_urls_with_step(
                self.url_env, request.white.url, request.black.url, request.step
            ).produced(request.fens)
        ).concatenated()

        return PlayerTrajectoryResponse(fens=produced.fens, sans=produced.sans, results=produced.results)

    async def game(self, request: PlayerGameRequest) -> PlayerGameResponse:
        produced: Trace = await Game.from_urls(self.url_env, request.white.url, request.black.url).produced()

        return PlayerGameResponse(
            fens=produced.fens[0], sans=produced.sans[0], result=str(Results(produced.results[0]))
        )

    async def rate(self, request: PlayerRateRequest) -> PlayerRateResponse:
        results: list[str] = [
            str(Results(trace.results[0]))
            for trace in await Rate.from_urls(self.url_env, request.white.url, request.black.url).produced(
                request.playtime
            )
        ]
        win = results.count("1-0")
        lose = results.count("0-1")
        draw = results.count("1/2-1/2")

        return PlayerRateResponse(
            white=PlayerAIResult(score=(win + (draw * 0.5)), win=win, lose=lose, draw=draw),
            black=PlayerAIResult(score=(lose + (draw * 0.5)), win=lose, lose=win, draw=draw),
        )
