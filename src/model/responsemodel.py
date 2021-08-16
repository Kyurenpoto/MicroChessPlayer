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

    @classmethod
    def from_message_with_service(cls, message: str, service: str) -> BadRequestResponseModel:
        return BadRequestResponseModel(message, f"{service}.RequestError")


class HTTPStatusErrorResponseModel(ErrorResponseModel):
    @classmethod
    def from_message(cls, message: str) -> HTTPStatusErrorResponseModel:
        return HTTPStatusErrorResponseModel(message, "request.HTTPStatusError")


class BadRequestResponseModel(ErrorResponseModel):
    @classmethod
    def from_message_with_service(cls, message: str, service: str) -> BadRequestResponseModel:
        return BadRequestResponseModel(message, f"{service}.BadRequest")


class PayloadTooLargeResponseModel(ErrorResponseModel):
    @classmethod
    def from_message_with_service(cls, message: str, service: str) -> PayloadTooLargeResponseModel:
        return PayloadTooLargeResponseModel(message, f"{service}.PayloadTooLarge")


class UnsupportedMediaTypeResponseModel(ErrorResponseModel):
    @classmethod
    def from_message_with_service(cls, message: str, service: str) -> UnsupportedMediaTypeResponseModel:
        return UnsupportedMediaTypeResponseModel(message, f"{service}.UnsupportedMediaType")


class UnprocessableEntityResponseModel(ErrorResponseModel):
    @classmethod
    def from_message_with_service(cls, message: str, service: str) -> UnprocessableEntityResponseModel:
        return UnprocessableEntityResponseModel(message, f"{service}.UnprocessableEntity")


class InternalServerErrorResponseModel(ErrorResponseModel):
    @classmethod
    def from_message_with_service(cls, message: str, service: str) -> InternalServerErrorResponseModel:
        return InternalServerErrorResponseModel(message, f"{service}.InternalServerError")


class BadGatewayResponseModel(ErrorResponseModel):
    @classmethod
    def from_message_with_service(cls, message: str, service: str) -> BadGatewayResponseModel:
        return BadGatewayResponseModel(message, f"{service}.BadGateway")


ResponseErrorResponseModel = Union[
    BadRequestResponseModel,
    PayloadTooLargeResponseModel,
    UnsupportedMediaTypeResponseModel,
    UnprocessableEntityResponseModel,
    InternalServerErrorResponseModel,
    BadGatewayResponseModel,
]


TrajectoryResponsableModel = Union[TrajectoryResponseModel, RequestErrorResponseModel, HTTPStatusErrorResponseModel]
GameResponsableModel = Union[GameResponseModel, RequestErrorResponseModel, HTTPStatusErrorResponseModel]
MeasurementResponsableModel = Union[MeasurementResponseModel, RequestErrorResponseModel, HTTPStatusErrorResponseModel]
NextFENResponsableModel = Union[NextFENResponseModel, RequestErrorResponseModel, HTTPStatusErrorResponseModel]
NextSANResponsableModel = Union[NextSANResponseModel, RequestErrorResponseModel, HTTPStatusErrorResponseModel]
FENStatusResponsableModel = Union[FENStatusResponseModel, ErrorResponseModel]
