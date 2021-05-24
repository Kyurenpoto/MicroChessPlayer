# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from infra.apiclient import APIClient


class RequestedNextFEN(list[str]):
    @classmethod
    async def from_url_with_FENs_SANs(cls, url: str, fens: list[str], sans: list[str]) -> RequestedNextFEN:
        return (await APIClient(url).post({"fens": fens, "sans": sans}))["next_fens"]
