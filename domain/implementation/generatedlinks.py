# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

from domain.dto.playerdto import PlayerLink


class GeneratedLinks(list[PlayerLink]):
    @classmethod
    def from_host_with_apis(cls, host: str, apis: dict[str, str]) -> GeneratedLinks:
        return GeneratedLinks([PlayerLink(rel=rel, href=("http://" + host + api)) for rel, api in apis.items()])

    @classmethod
    def from_host_with_apis_requested(cls, host: str, apis: dict[str, str], requested: str) -> GeneratedLinks:
        return GeneratedLinks(
            [PlayerLink(rel="self", href=("http://" + host + apis[requested]))]
            + GeneratedLinks.from_host_with_apis(host, apis)
        )
