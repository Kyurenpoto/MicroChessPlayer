# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from typing import List, Union

from pydantic import BaseModel


class PlayerAIInfo(BaseModel):
    url: str
    port: int


class PlayerTrajactoryRequest(BaseModel):
    fens: List[str]
    white: PlayerAIInfo
    black: PlayerAIInfo


class PlayerTrajactoryResponse(BaseModel):
    fens: List[List[str]]
    sans: List[List[str]]
    results: List[int]


class PlayerGameRequest(BaseModel):
    white: PlayerAIInfo
    black: PlayerAIInfo


class PlayerGameResponse(BaseModel):
    fens: List[str]
    sans: List[str]
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
    value: Union[List[str], PlayerAIInfo, int]
    error: str
