# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from typing import NamedTuple

from infra.postclient import PostClient


class RequestedFENStatus(NamedTuple):
    statuses: list[int]
    legal_moves: list[list[str]]

    @classmethod
    async def from_url_with_FENs(cls, url: str, fens: list[str]) -> RequestedFENStatus:
        response = await PostClient(url).post({"fens": fens})

        return RequestedFENStatus(response["statuses"], response["legal_moves"])
