# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from httpx import HTTPStatusError, RequestError
from src.core.event import EventAGen
from src.core.usecase import Usecase
from src.entity.movement import FEN, SAN, Movement
from src.entity.status import Status
from src.entity.trace import ColoredTrace, FiniteTraceProducable, ProducableTrace, Trace
from src.model.requestmodel import TrajectoryRequestModel
from src.model.responsemodel import (
    HTTPStatusErrorResponseModel,
    RequestErrorResponseModel,
    TrajectoryResponsableModel,
    TrajectoryResponseModel,
)

TrajectoryUsecase = Usecase[TrajectoryRequestModel, TrajectoryResponsableModel]


class Trajectory(TrajectoryUsecase):
    async def request_to_responsable(self, request: TrajectoryRequestModel) -> TrajectoryResponsableModel:
        try:
            return TrajectoryResponseModel._make(
                (
                    await ProducableTrace(
                        Status(request.env),
                        Movement(request.env, request.ai_white),
                        Movement(request.env, request.ai_black),
                        FiniteTraceProducable(request.step),
                    ).produced_with_spliting(request.fens)
                ).concatenated()
            )
        except RequestError as ex:
            return RequestErrorResponseModel(
                f"An error occurred while requesting {ex.request.url!r}: {ex.args[0]!r}",
                "request.RequestError",
            )
        except HTTPStatusError as ex:
            return HTTPStatusErrorResponseModel(
                f"Error response {ex.response.status_code} "
                + f"while requesting {ex.request.url!r}: {ex.response.json()!r}",
                "request.HTTPStatusError",
            )


class FakeTrajectory(TrajectoryUsecase):
    async def executed(self, request: TrajectoryRequestModel) -> EventAGen:
        yield await self.framework().response(
            TrajectoryResponseModel._make(
                ColoredTrace(
                    Trace(
                        [[FEN.starting(), FEN.starting()], [FEN.starting(), FEN.starting()]],
                        [[SAN.first()], [SAN.first()]],
                        [[0, 0], [0, 0]],
                    ),
                    Trace(
                        [[FEN.first(), FEN.first()], [FEN.first(), FEN.first()]],
                        [[SAN.first()], [SAN.first()]],
                        [[0, 0], [0, 0]],
                    ),
                ).concatenated()
            )
        )
