# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from src.infra.postclient import PostClient


class RequestedNextSAN(list[str]):
    @classmethod
    async def from_url_with_FENs_legal_moves(
        cls, url: str, fens: list[str], legal_moves: list[list[str]]
    ) -> RequestedNextSAN:
        return (await PostClient(url + "/ai/next-san").post({"fens": fens, "legal_moves": legal_moves}))["next_sans"]
