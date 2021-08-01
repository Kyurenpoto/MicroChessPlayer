# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from pydantic import BaseModel
from submodules.fastapi_haljson.src.halmodel import HALBase


class AINextSANRequest(BaseModel):
    fens: list[str]


class AINextSANResponse(HALBase):
    next_sans: list[str]


class AIErrorResponse(HALBase):
    message: str
    location: str
    param: str
    value: list[str]
    error: str
