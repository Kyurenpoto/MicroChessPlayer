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
    def from_message_with_service(cls, message: str, service: str) -> RequestErrorResponseModel:
        return RequestErrorResponseModel(message, f"{service}.RequestError")


class HTTPStatusErrorResponseModel(ErrorResponseModel):
    @classmethod
    def from_message(cls, message: str) -> HTTPStatusErrorResponseModel:
        return HTTPStatusErrorResponseModel(message, "request.HTTPStatusError")


class BadRequestResponseModel(ErrorResponseModel):
    @classmethod
    def from_message_with_service(cls, message: str, service: str) -> BadRequestResponseModel:
        return BadRequestResponseModel(message, f"{service}.BadRequest")

    def status_code(self) -> int:
        return status.HTTP_400_BAD_REQUEST


class PayloadTooLargeResponseModel(ErrorResponseModel):
    @classmethod
    def from_message_with_service(cls, message: str, service: str) -> PayloadTooLargeResponseModel:
        return PayloadTooLargeResponseModel(message, f"{service}.PayloadTooLarge")

    def status_code(self) -> int:
        return status.HTTP_413_REQUEST_ENTITY_TOO_LARGE


class UnsupportedMediaTypeResponseModel(ErrorResponseModel):
    @classmethod
    def from_message_with_service(cls, message: str, service: str) -> UnsupportedMediaTypeResponseModel:
        return UnsupportedMediaTypeResponseModel(message, f"{service}.UnsupportedMediaType")

    def status_code(self) -> int:
        return status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


class UnprocessableEntityResponseModel(ErrorResponseModel):
    @classmethod
    def from_message_with_service(cls, message: str, service: str) -> UnprocessableEntityResponseModel:
        return UnprocessableEntityResponseModel(message, f"{service}.UnprocessableEntity")

    def status_code(self) -> int:
        return status.HTTP_422_UNPROCESSABLE_ENTITY


class InternalServerErrorResponseModel(ErrorResponseModel):
    @classmethod
    def from_message_with_service(cls, message: str, service: str) -> InternalServerErrorResponseModel:
        return InternalServerErrorResponseModel(message, f"{service}.InternalServerError")

    def status_code(self) -> int:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


class BadGatewayResponseModel(ErrorResponseModel):
    @classmethod
    def from_message_with_service(cls, message: str, service: str) -> BadGatewayResponseModel:
        return BadGatewayResponseModel(message, f"{service}.BadGateway")

    def status_code(self) -> int:
        return status.HTTP_502_BAD_GATEWAY


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
