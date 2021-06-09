# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from typing import Union

from pydantic import AnyHttpUrl, BaseModel
from pydantic.fields import Field


class PlayerURL(BaseModel):
    url: AnyHttpUrl


class PlayerInternalModel(BaseModel):
    url_env: PlayerURL
    routes: dict[str, str]


class PlayerHALLink(BaseModel):
    href: str = Field(
        ...,
        description="HATEOAS link",
    )

    @classmethod
    def doc_link(cls, rel: str, api: str, http_method: str, profile_location: str) -> PlayerHALLink:
        return PlayerHALLink(href=profile_location + "_".join([rel] + api.split("/")[1:] + [http_method]))


class PlayerHAL(BaseModel):
    links: dict[str, PlayerHALLink] = Field(
        ...,
        description="HATEOAS links",
    )

    @classmethod
    def from_apis(cls, routes: dict[str, str]) -> PlayerHAL:
        return PlayerHAL(links={rel: PlayerHALLink(href=api) for rel, api in routes.items()})

    @classmethod
    def from_apis_with_requested(cls, routes: dict[str, str], requested: str, http_method) -> PlayerHAL:
        return PlayerHAL(
            links={
                "self": PlayerHALLink(href=routes[requested]),
                "profile": PlayerHALLink.doc_link(requested, routes[requested], http_method, "/docs#default/"),
                "profile2": PlayerHALLink.doc_link(requested, routes[requested], http_method, "/redoc#operation/"),
                **PlayerHAL.from_apis(routes).links,
            }
        )


class PlayerAIInfo(BaseModel):
    url: AnyHttpUrl = Field(
        ...,
        description="URL of AI server to get next SANs",
        example="http://localhost:6011/ai",
    )


class PlayerTrajectoryRequest(BaseModel):
    fens: list[str] = Field(
        ...,
        description="List of FENs starting trajectories",
        example=["4knbr/4p3/8/7P/4RBNK/8/8/8 w Kk - 0 1", "4k3/6B1/4R1K1/4p3/8/8/8/8 b Kk - 0 1"],
        min_items=1,
    )
    white: PlayerAIInfo = Field(
        ...,
        description="Information of white-side AI",
    )
    black: PlayerAIInfo = Field(
        ...,
        description="Information of black-side AI",
    )
    step: int = Field(
        ...,
        description="Maximum steps of trajectories",
        example=1,
        ge=0,
    )


class PlayerTrajectoryResponse(PlayerHAL):
    fens: list[list[str]] = Field(
        ...,
        description="List of FENs in trajectories",
        example=[
            ["4knbr/4p3/8/7P/4RBNK/8/8/8 w Kk - 0 1", "4knbr/4p3/7P/8/4RBNK/8/8/8 b Kk - 0 1"],
            ["4k3/6B1/4R1K1/4p3/8/8/8/8 b Kk - 0 1", "8/8/8/8/8/8/8/8 w Kk - 0 1"],
        ],
    )
    sans: list[list[str]] = Field(
        ...,
        description="List of SANs in trajectories",
        example=[["h5h6"], []],
    )
    results: list[list[float]] = Field(
        ...,
        description="List of results in trajectories",
        example=[[0, 0], [0, 1]],
    )


class PlayerGameRequest(BaseModel):
    white: PlayerAIInfo = Field(
        ...,
        description="Information of white-side AI",
    )
    black: PlayerAIInfo = Field(
        ...,
        description="Information of black-side AI",
    )


class PlayerGameResponse(PlayerHAL):
    fens: list[str] = Field(
        ...,
        description="List of FENs in episode",
        example=[
            "4knbr/4p3/8/7P/4RBNK/8/8/8 w Kk - 0 1",
            "4knbr/4p3/7B/7P/4RNK/8/8/8 b k - 1 1",
            "4knb1/4p3/7r/7P/4RNK/8/8/8 w - - 0 2",
            "4knb1/4p3/7N/7P/4R1K/8/8/8 b - - 0 2",
            "4kn2/4p2b/7N/7P/4R1K/8/8/8 w - - 1 3",
            "4kn2/4R2b/7N/7P/7K/8/8/8 b - - 0 4",
            "5n2/4k2b/7N/7P/7K/8/8/8 w - - 0 5",
            "5nN1/4k2b/8/7P/7K/8/8/8 b - - 1 5",
            "5nb1/4k3/8/7P/7K/8/8/8 w - - 0 6",
            "5nb1/4k3/8/6KP/8/8/8/8 b - - 1 6",
            "6b1/4k2n/8/6KP/8/8/8/8 w - - 2 7",
            "6b1/4k2n/7K/7P/8/8/8/8 b - - 3 7",
            "6b1/52n/5k1K/7P/8/8/8/8 w - - 4 8",
            "8/8/8/8/8/8/8/8 b - - 4 8",
        ],
    )
    sans: list[str] = Field(
        ...,
        description="List of SANs in episode",
        example=[
            "e4e5",
            "h8h6",
            "g4h6",
            "g8h7",
            "e4e7",
            "e8e7",
            "h6g8",
            "h7g8",
            "h4g5",
            "f8h7",
            "g5h6",
            "e7f6",
        ],
    )
    result: str = Field(
        ...,
        description="Result of episode",
        example="1/2-1/2",
    )


class PlayerMeasurementRequest(BaseModel):
    white: PlayerAIInfo = Field(
        ...,
        description="Information of white-side AI",
    )
    black: PlayerAIInfo = Field(
        ...,
        description="Information of black-side AI",
    )
    playtime: int = Field(
        ...,
        description="Number of plays to measure win rate ",
        example=4,
        ge=1,
    )


class PlayerAIMeasurement(BaseModel):
    score: float = Field(
        ...,
        description="Measured score",
        example="2",
    )
    win: int = Field(
        ...,
        description="Measured number of win",
        example="1",
    )
    lose: int = Field(
        ...,
        description="Measured number of lose",
        example="1",
    )
    draw: int = Field(
        ...,
        description="Measured number of draw",
        example="2",
    )


class PlayerMeasurementResponse(PlayerHAL):
    white: PlayerAIMeasurement = Field(
        ...,
        description="Measurement of white-side AI",
    )
    black: PlayerAIMeasurement = Field(
        ...,
        description="Measurement of black-side AI",
    )


class PlayerErrorResponse(PlayerHAL):
    message: str = Field(
        ...,
        description="Error message",
    )
    location: str = Field(
        ...,
        description="Error location",
    )
    param: str = Field(
        ...,
        description="Parameters of request",
    )
    value: Union[
        tuple[list[str], PlayerAIInfo, PlayerAIInfo, int],
        tuple[PlayerAIInfo, PlayerAIInfo],
        tuple[PlayerAIInfo, PlayerAIInfo, int],
    ] = Field(
        ...,
        description="Values of request",
    )
    error: str = Field(
        ...,
        description="Error type",
    )
