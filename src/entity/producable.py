# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import NamedTuple

from src.vo.basic import FEN, SAN, Color, Reward, Status

FENSequence = list[FEN]
SANSequence = list[SAN]
StatusSequence = list[Status]
RewardSequence = list[Reward]


class RawTraceData(NamedTuple):
    id: int
    fen_seq: FENSequence
    san_seq: SANSequence
    status_seq: StatusSequence

    @classmethod
    def from_sequences(
        cls, id: int, fen_seq: FENSequence, san_seq: SANSequence, status_seq: StatusSequence
    ) -> RawTraceData:
        result: RawTraceData = RawTraceData(id, fen_seq, san_seq, status_seq)
        if not result.constrained():
            raise RuntimeError()

        return result

    def constrained(self) -> bool:
        return len(self.fen_seq) == len(self.status_seq) and len(self.fen_seq) == len(self.san_seq) + 1


class RawTrace(RawTraceData):
    @classmethod
    def from_sequences(
        cls, id: int, fen_seq: FENSequence, san_seq: SANSequence, status_seq: StatusSequence
    ) -> RawTrace:
        return RawTrace._make(RawTraceData.from_sequences(id, fen_seq, san_seq, status_seq))

    def last_fen(self) -> FEN:
        return self.fen_seq[-1]

    def last_status(self) -> Status:
        return self.status_seq[-1]

    def append(self, fen: FEN, san: SAN, status: Status) -> None:
        self.fen_seq.append(fen)
        self.san_seq.append(san)
        self.status_seq.append(status)


class TraceData(NamedTuple):
    id: int
    fen_seq: FENSequence
    san_seq: SANSequence
    reward_seq: RewardSequence


class IncompleteTraceData(TraceData):
    @classmethod
    def from_raw(cls, id: int, raw: RawTraceData) -> IncompleteTraceData:
        if raw.status_seq[-1] != Status.NONE:
            raise RuntimeError()

        return IncompleteTraceData(id, raw.fen_seq, raw.san_seq, [Reward(0.0)] * len(raw.status_seq))


class CompleteTraceData(TraceData):
    @classmethod
    def from_raw(cls, id: int, raw: RawTraceData) -> IncompleteTraceData:
        if raw.status_seq[-1] == Status.NONE:
            raise RuntimeError()

        return IncompleteTraceData(
            id,
            raw.fen_seq + [FEN.end(raw.fen_seq[-1].color().opposite())],
            raw.san_seq,
            [Reward(0.0)] * (len(raw.status_seq) - 1) + Reward.from_status(raw.status_seq[-1]).with_opposite(),
        )


class Trace(TraceData):
    @classmethod
    def from_raw(cls, id: int, raw: RawTraceData) -> Trace:
        if raw.status_seq[-1] == Status.NONE:
            return Trace._make(IncompleteTraceData.from_raw(id, raw))
        else:
            return Trace._make(CompleteTraceData.from_raw(id, raw))


class ColoredTrace(TraceData):
    @classmethod
    def from_trace(cls, id: int, trace: TraceData, color: Color) -> ColoredTrace:
        indice: slice = slice(0, None, 2) if trace.fen_seq[0].color() == color else slice(1, None, 2)

        return ColoredTrace(
            id,
            trace.fen_seq[indice],
            trace.san_seq[slice(None) if trace.reward_seq[-1] == Reward(0) else slice(None)][indice],
            trace.reward_seq[indice],
        )
