# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations


class GeneratedLinks(dict[str, dict[str, str]]):
    @classmethod
    def from_host_with_apis(cls, host: str, apis: dict[str, str]) -> GeneratedLinks:
        return GeneratedLinks({rel: {"href": ("http://" + host + api)} for rel, api in apis.items()})

    @classmethod
    def from_host_with_apis_requested(cls, host: str, apis: dict[str, str], requested: str) -> GeneratedLinks:
        return GeneratedLinks(
            {
                "self": {"href": ("http://" + host + apis[requested])},
                "profile": {"href": ("http://" + host + "/docs")},
                "profile2": {"href": ("http://" + host + "/redoc")},
                **GeneratedLinks.from_host_with_apis(host, apis),
            }
        )
