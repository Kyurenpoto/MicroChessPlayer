# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from typing import Union

from pydantic import BaseModel
from submodules.fastapi_haljson.src.halmodel import HALBase


class EnvironmentNextFENRequest(BaseModel):
    fens: list[str]
    sans: list[str]


class EnvironmentNextFENResponse(HALBase):
    next_fens: list[str]


class EnvironmentFENStatusRequest(BaseModel):
    fens: list[str]


class EnvironmentFENStatusResponse(HALBase):
    statuses: list[int]
    legal_moves: list[list[str]]


class EnvironmentErrorResponse(HALBase):
    message: str
    location: str
    param: str
    value: Union[list[str], list[list[str]]]
    error: str
