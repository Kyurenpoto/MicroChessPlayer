# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import NamedTuple, Union


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


class NextFENResponseModel(NamedTuple):
    next_fens: list[str]


class NextSANResponseModel(NamedTuple):
    next_sans: list[str]


class FENStatusResponseModel(NamedTuple):
    statuses: list[int]
    legal_moves: list[list[str]]


class ErrorResponseModel(NamedTuple):
    message: str
    error: str


class RequestErrorResponseModel(ErrorResponseModel):
    @classmethod
    def from_message(cls, message: str) -> RequestErrorResponseModel:
        return RequestErrorResponseModel(message, "request.RequestError")


class HTTPStatusErrorResponseModel(ErrorResponseModel):
    @classmethod
    def from_message(cls, message: str) -> HTTPStatusErrorResponseModel:
        return HTTPStatusErrorResponseModel(message, "request.HTTPStatusError")


TrajectoryResponsableModel = Union[TrajectoryResponseModel, RequestErrorResponseModel, HTTPStatusErrorResponseModel]
GameResponsableModel = Union[GameResponseModel, RequestErrorResponseModel, HTTPStatusErrorResponseModel]
MeasurementResponsableModel = Union[MeasurementResponseModel, RequestErrorResponseModel, HTTPStatusErrorResponseModel]
