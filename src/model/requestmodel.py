# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import NamedTuple

from src.usecase.typemodel import URLString


class TrajectoryRequestModel(NamedTuple):
    env: URLString
    fens: list[str]
    ai_white: URLString
    ai_black: URLString
    step: int


class GameRequestModel(NamedTuple):
    env: URLString
    ai_white: URLString
    ai_black: URLString


class MeasurementRequestModel(NamedTuple):
    env: URLString
    ai_white: URLString
    ai_black: URLString
    playtime: int


class NextFENRequestModel(NamedTuple):
    next_fen: URLString
    fens: list[str]
    sans: list[str]


class NextSANRequestModel(NamedTuple):
    next_san: URLString
    fens: list[str]
    legal_moves: list[list[str]]


class FENStatusRequestModel(NamedTuple):
    fen_status: URLString
    fens: list[str]
