# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only


from typing import List

from infra.apiclient import APIClient


class RequestedNextFEN:
    __slots__ = ["__url", "__fens", "__sans"]

    __url: str
    __fens: List[str]
    __sans: List[str]

    def __init__(self, url: str, fens: List[str], sans: List[str]):
        self.__url = url
        self.__fens = fens
        self.__sans = sans

    async def value(self) -> List[str]:
        return (await APIClient(self.__url).post({"fens": self.__fens, "sans": self.__sans}))["next_fens"]
