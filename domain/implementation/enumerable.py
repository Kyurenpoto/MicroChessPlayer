# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from typing import List


class IndexedList:
    __slots__ = ["__target", "__indice"]

    __target: List
    __indice: List[int]

    def __init__(self, target: List, indice: List[int]):
        self.__target = target
        self.__indice = list(filter(lambda x: x < len(target), indice))

    def value(self) -> List:
        return [self.__target[i] for i in self.__indice]
