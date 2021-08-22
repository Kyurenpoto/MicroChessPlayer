# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import Type

from fastapi import status
from httpx import (
    CloseError,
    ConnectError,
    ConnectTimeout,
    DecodingError,
    LocalProtocolError,
    PoolTimeout,
    ProxyError,
    ReadError,
    ReadTimeout,
    RemoteProtocolError,
    RequestError,
    TooManyRedirects,
    UnsupportedProtocol,
    WriteError,
    WriteTimeout,
)


class NamedHTTPRequestErrorTypeName(str):
    @classmethod
    def type_list(cls) -> list[Type[RequestError]]:
        return [
            CloseError,
            ConnectError,
            ConnectTimeout,
            DecodingError,
            LocalProtocolError,
            PoolTimeout,
            ProxyError,
            ReadError,
            ReadTimeout,
            RemoteProtocolError,
            TooManyRedirects,
            UnsupportedProtocol,
            WriteError,
            WriteTimeout,
        ]

    @classmethod
    def name_map(cls) -> dict[str, str]:
        return {
            CloseError.__name__: "Close Error",
            ConnectError.__name__: "Connect Error",
            ConnectTimeout.__name__: "Connect Timeout",
            DecodingError.__name__: "Decoding Error",
            LocalProtocolError.__name__: "Local Protocol Error",
            PoolTimeout.__name__: "Pool Timeout",
            ProxyError.__name__: "Proxy Error",
            ReadError.__name__: "Read Error",
            ReadTimeout.__name__: "Read Timeout",
            RemoteProtocolError.__name__: "Remote Protocol Error",
            TooManyRedirects.__name__: "Too Many Redirects",
            UnsupportedProtocol.__name__: "Unsupported Protocol",
            WriteError.__name__: "Write Error",
            WriteTimeout.__name__: "Write Timeout",
        }

    def name(self) -> str:
        try:
            return self.name_map()[self]
        except:
            return self.name_map()[ConnectTimeout.__name__]


class NamedHTTPStatusCode(int):
    @classmethod
    def name_map(cls) -> dict[int, str]:
        return {
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
            status.HTTP_402_PAYMENT_REQUIRED: "Payment Required",
            status.HTTP_403_FORBIDDEN: "Forbidden",
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_405_METHOD_NOT_ALLOWED: "Method Not Allowed",
            status.HTTP_406_NOT_ACCEPTABLE: "Not Acceptable",
            status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED: "Proxy Authentication Aequired",
            status.HTTP_408_REQUEST_TIMEOUT: "Request Timeout",
            status.HTTP_409_CONFLICT: "Conflict",
            status.HTTP_410_GONE: "Gone",
            status.HTTP_411_LENGTH_REQUIRED: "Length Required",
            status.HTTP_412_PRECONDITION_FAILED: "Precondition Failed",
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: "Request Entity Too Large",
            status.HTTP_414_REQUEST_URI_TOO_LONG: "Request Uri Too Long",
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: "Unsupported Media Type",
            status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE: "Requested Range Not Satisfiable",
            status.HTTP_417_EXPECTATION_FAILED: "Expectation Failed",
            status.HTTP_418_IM_A_TEAPOT: "Im A Teapot",
            status.HTTP_421_MISDIRECTED_REQUEST: "Misdirected Request",
            status.HTTP_422_UNPROCESSABLE_ENTITY: "Unprocessable Entity",
            status.HTTP_423_LOCKED: "Locked",
            status.HTTP_424_FAILED_DEPENDENCY: "Failed Dependency",
            status.HTTP_425_TOO_EARLY: "Too Early",
            status.HTTP_426_UPGRADE_REQUIRED: "Upgrade Required",
            status.HTTP_428_PRECONDITION_REQUIRED: "Precondition Required",
            status.HTTP_429_TOO_MANY_REQUESTS: "Too Many Requests",
            status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE: "Request Header Fields Too Large",
            status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS: "Unavailable For Legal Reasons",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
            status.HTTP_501_NOT_IMPLEMENTED: "Not Implemented",
            status.HTTP_502_BAD_GATEWAY: "Bad Gateway",
            status.HTTP_503_SERVICE_UNAVAILABLE: "Service Unavailable",
            status.HTTP_504_GATEWAY_TIMEOUT: "Gateway Timeout",
            status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED: "Http Version Not Supported",
            status.HTTP_506_VARIANT_ALSO_NEGOTIATES: "Variant Also Negotiates",
            status.HTTP_507_INSUFFICIENT_STORAGE: "Insufficient Storage",
            status.HTTP_508_LOOP_DETECTED: "Loop Detected",
            status.HTTP_510_NOT_EXTENDED: "Not Extended",
            status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED: "Network Authentication Required",
        }

    def name(self) -> str:
        try:
            return self.name_map()[self]
        except:
            return self.name_map()[status.HTTP_500_INTERNAL_SERVER_ERROR]
