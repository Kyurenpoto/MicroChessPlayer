# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from typing import Iterable, NamedTuple

from src.entity.producable import RawTrace
from src.model.repositoryrequestmodel import (
    RawTraceRepositoryCreateRequestModel,
    RawTraceRepositoryDeleteRequestModel,
    RawTraceRepositoryReadRequestModel,
    RawTraceRepositoryUpdateRequestModel,
    RawTraceSpecification,
)
from src.model.repositoryresponsemodel import RawTraceRepositoryReadResponseModel
from vo.basic import Status


class AllRawTraceSpecification(RawTraceSpecification):
    def refine(self, raw_traces: Iterable[RawTrace]) -> Iterable[RawTrace]:
        return raw_traces


class ExtendableRawTraceSpecification(RawTraceSpecification):
    def refine(self, raw_traces: Iterable[RawTrace]) -> Iterable[RawTrace]:
        return filter(lambda x: x.last_status() == Status.NONE, raw_traces)


class RawTraceRepository(NamedTuple):
    raw_traces: dict[int, RawTrace]
    last_id: int

    async def create(self, request: RawTraceRepositoryCreateRequestModel) -> None:
        if len(request.raw_traces) == 0:
            return

        for i, raw_trace in enumerate(request.raw_traces):
            raw_trace.id = self.last_id + i
        self.last_id += len(request.raw_traces)

        self.raw_traces.update({raw_trace.id: raw_trace for raw_trace in request.raw_traces})

    async def update(self, request: RawTraceRepositoryUpdateRequestModel) -> None:
        await self.create(
            RawTraceRepositoryCreateRequestModel(
                list(filter(lambda x: x.id not in self.raw_traces, request.raw_traces))
            )
        )

        self.raw_traces.update(
            {raw_trace.id: raw_trace for raw_trace in filter(lambda x: x.id in self.raw_traces, request.raw_traces)}
        )

    async def delete(self, request: RawTraceRepositoryDeleteRequestModel) -> None:
        for raw_trace in request.raw_traces:
            self.raw_traces.pop(raw_trace.id)

    async def read(self, request: RawTraceRepositoryReadRequestModel) -> RawTraceRepositoryReadResponseModel:
        return RawTraceRepositoryReadResponseModel(list(request.spec.refine(self.raw_traces.values())))
