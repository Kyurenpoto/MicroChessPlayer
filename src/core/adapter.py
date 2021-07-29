# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ReqType = TypeVar("ReqType")
ResType = TypeVar("ResType")


class ToUsecaseAdapter(ABC, Generic[ReqType, ResType]):
    @abstractmethod
    async def dispatch(self, req: ReqType) -> ResType:
        pass
