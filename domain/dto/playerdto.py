# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from typing import Union

from pydantic import AnyHttpUrl, BaseModel
from pydantic.fields import Field


class PlayerLink(BaseModel):
    rel: str = Field(
        ...,
        description="Relationship with current API",
    )
    href: str = Field(
        ...,
        description="URL of API",
    )


class PlayerAIInfo(BaseModel):
    url: AnyHttpUrl = Field(
        ...,
        description="URL of AI server",
        example="http://localhost:6011/ai",
    )


class PlayerTrajectoryRequest(BaseModel):
    fens: list[str] = Field(
        ...,
        description="List of FENs starting trajectories",
        example=["4knbr/4p3/8/7P/4RBNK/8/8/8 w Kk - 0 1", "4k3/6B1/4R1K1/4p3/8/8/8/8 b Kk - 0 1"],
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


class PlayerTrajectoryResponse(BaseModel):
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
    links: list[PlayerLink] = Field(
        ...,
        description="HATEOAS information",
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


class PlayerGameResponse(BaseModel):
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
    links: list[PlayerLink] = Field(
        ...,
        description="HATEOAS information",
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
    score: int = Field(
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


class PlayerMeasurementResponse(BaseModel):
    white: PlayerAIMeasurement = Field(
        ...,
        description="Measurement of white-side AI",
    )
    black: PlayerAIMeasurement = Field(
        ...,
        description="Measurement of black-side AI",
    )
    links: list[PlayerLink] = Field(
        ...,
        description="HATEOAS information",
    )


class PlayerErrorResponse(BaseModel):
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
    links: list[PlayerLink] = Field(
        ...,
        description="HATEOAS information",
    )
