# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from typing import Union

from pydantic import BaseModel


class PlayerAIInfo(BaseModel):
    url: str


class PlayerTrajactoryRequest(BaseModel):
    fens: list[str]
    white: PlayerAIInfo
    black: PlayerAIInfo


class PlayerTrajactoryResponse(BaseModel):
    fens: list[list[str]]
    sans: list[list[str]]
    results: list[int]


class PlayerGameRequest(BaseModel):
    white: PlayerAIInfo
    black: PlayerAIInfo


class PlayerGameResponse(BaseModel):
    fens: list[str]
    sans: list[str]
    result: int


class PlayerRateRequest(BaseModel):
    white: PlayerAIInfo
    black: PlayerAIInfo
    playtime: int


class PlayerAIResult(BaseModel):
    score: int
    win: int
    draw: int
    lose: int


class PlayerRateResponse(BaseModel):
    white: PlayerAIResult
    black: PlayerAIResult


class PlayerErrorResponse(BaseModel):
    message: str
    location: str
    param: str
    value: Union[list[str], PlayerAIInfo, int]
    error: str
