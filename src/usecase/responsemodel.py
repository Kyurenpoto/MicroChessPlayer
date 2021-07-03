# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT


from typing import NamedTuple, Union

from src.usecase.typemodel import URLString


class TrajectoryResponseModel(NamedTuple):
    fens: list[list[str]]
    sans: list[list[str]]
    results: list[list[float]]


class GameResponseModel(NamedTuple):
    fens: list[str]
    sans: list[str]
    result: str


class MeasurementInfo(NamedTuple):
    score: float
    win: int
    lose: int
    draw: int


class MeasurementResponseModel(NamedTuple):
    white_info: MeasurementInfo
    black_info: MeasurementInfo


class ErrorResponseModel(NamedTuple):
    message: str
    location: str
    param: str
    value: Union[
        tuple[URLString, list[str], URLString, URLString, int],
        tuple[URLString, URLString, URLString],
        tuple[URLString, URLString, URLString, int],
    ]
    error: str
