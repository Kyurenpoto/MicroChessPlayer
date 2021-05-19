# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only


from typing import List

from infra.apiclient import APIClient


class RequestedNextSAN:
    __slots__ = ["__url", "__fens", "__legal_moves"]

    __url: str
    __fens: List[str]
    __legal_moves: List[List[str]]

    def __init__(self, url: str, fens: List[str], legal_moves: List[List[str]]):
        self.__url = url
        self.__fens = fens
        self.__legal_moves = legal_moves

    async def value(self) -> List[str]:
        return (await APIClient(self.__url).post({"fens": self.__fens, "legal_moves": self.__legal_moves}))["next_sans"]
