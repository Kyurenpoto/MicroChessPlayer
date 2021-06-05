# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from pydantic import BaseModel


class PlayerAIInfo(BaseModel):
    url: str


class PlayerTrajectoryRequest(BaseModel):
    fens: list[str]
    white: PlayerAIInfo
    black: PlayerAIInfo
    step: int


class PlayerTrajectoryResponse(BaseModel):
    fens: list[list[str]]
    sans: list[list[str]]
    results: list[list[float]]


class PlayerGameRequest(BaseModel):
    white: PlayerAIInfo
    black: PlayerAIInfo


class PlayerGameResponse(BaseModel):
    fens: list[str]
    sans: list[str]
    result: str


class PlayerMeasurementRequest(BaseModel):
    white: PlayerAIInfo
    black: PlayerAIInfo
    playtime: int


class PlayerAIMesurement(BaseModel):
    score: int
    win: int
    lose: int
    draw: int


class PlayerMeasurementResponse(BaseModel):
    white: PlayerAIResult
    black: PlayerAIResult
