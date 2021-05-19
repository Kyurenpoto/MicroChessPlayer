# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only


from typing import Dict, List, Tuple, Union, cast

from infra.apiclient import APIClient


class RequestedFENStatus:
    __slots__ = ["__url", "__fens"]

    __url: str
    __fens: List[str]

    def __init__(self, url: str, fens: List[str]):
        self.__url = url
        self.__fens = fens

    async def value(self) -> Tuple[List[int], List[List[str]]]:
        result: Dict[str, Union[List[int], List[List[str]]]] = await APIClient(self.__url).post({"fens": self.__fens})

        return cast(List[int], result["statuses"]), cast(List[List[str]], result["legal_moves"])
