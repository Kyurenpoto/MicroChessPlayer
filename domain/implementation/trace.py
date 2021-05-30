# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations, unicode_literals

from typing import Callable, Iterable, NamedTuple

from .enumerable import Enumerable, Indexable, Mappable
from .movement import FEN, IMovement
from .status import IStatus


class CorrectionMappable(Indexable):
    @classmethod
    def from_target_results(cls, results: list[list[float]]) -> CorrectionMappable:
        return CorrectionMappable(Enumerable(results).to_conditional_indice(lambda x: len(x) > 1 and x[-1] != 0))

    def corrected_fens(self, fens: list[list[str]]) -> list[list[str]]:
        return Mappable(fens).replaced_with_disjoint(
            Mappable.indice_to_disjoint(
                [
                    (
                        self.conditional_indexed(lambda i: fens[i][-1].split(" ")[1] == "w"),
                        lambda i: fens[i] + [FEN.black_end()],
                    ),
                    (
                        self.conditional_indexed(lambda i: fens[i][-1].split(" ")[1] == "b"),
                        lambda i: fens[i] + [FEN.white_end()],
                    ),
                ]
            )
        )

    def corrected_results(self, results: list[list[float]]) -> list[list[float]]:
        return Mappable(results).replaced_with_disjoint(
            Mappable.indice_to_disjoint(
                [
                    (self.conditional_indexed(lambda i: results[i][-1] == 1), lambda i: results[i][:-1] + [0.0, 1]),
                    (self.conditional_indexed(lambda i: results[i][-1] == 0.5), lambda i: results[i] + [0.5]),
                ]
            )
        )


class Trace(NamedTuple):
    fens: list[list[str]]
    sans: list[list[str]]
    results: list[list[float]]

    @classmethod
    def from_FENs(cls, fens: list[str]) -> Trace:
        return Trace(
            Mappable(fens).wrapped(),
            Enumerable.filled([], len(fens)),
            Enumerable.filled([], len(fens)),
        )

    @classmethod
    def from_unwrapped(cls, fens: list[str], sans: list[str], results: list[float]) -> Trace:
        return Trace(*map(lambda x: Mappable(x).wrapped(), [fens, sans, results]))

    def to_color_indice(self, color: str) -> Iterable[int]:
        return Enumerable(self.fens).to_conditional_indice(lambda x: x[0].split(" ")[1] == color)

    def to_not_empty_indice(self) -> Iterable[int]:
        return Enumerable(self.fens).to_conditional_indice(lambda x: len(x) != 0)

    def SAN_normalized(self) -> Trace:
        return Trace(
            self.fens,
            Mappable(Enumerable(self.fens).to_indice()).mapped(
                lambda i: self.sans[i][:-1] if len(self.fens[i]) != len(self.sans[i]) + 1 else self.sans[i]
            ),
            self.results,
        )

    def end_corrected(self) -> Trace:
        correctable: CorrectionMappable = CorrectionMappable.from_target_results(self.results)

        return Trace(
            correctable.corrected_fens(self.fens),
            self.sans,
            correctable.corrected_results(self.results),
        )


class MappableTrace(Trace):
    def mapped(self, mapper: Callable) -> MappableTrace:
        return MappableTrace(*map(mapper, self))

    def inner_mapped(self, mapper: Callable) -> MappableTrace:
        return self.mapped(lambda y: Mappable(y).mapped(mapper))

    def mapped_with(self, other: Trace, mapper: Callable) -> MappableTrace:
        return MappableTrace(*map(mapper, zip(self, other)))

    def concatenated(self, other: Trace) -> MappableTrace:
        return self.mapped_with(other, lambda z: z[0] + z[1])

    def inner_concatenated(self, other: Trace) -> MappableTrace:
        return self.mapped_with(other, lambda z: Mappable.mapped_with_others(z, lambda x, y: x + y))


class IndexableTrace(Trace):
    def mapping_operated(self, mapper: Callable) -> IndexableTrace:
        return IndexableTrace._make(mapper(MappableTrace._make(self)))

    def indexed(self, indice: Iterable[int]) -> IndexableTrace:
        return self.mapping_operated(lambda y: y.mapped(lambda x: Indexable(x).indexed(indice)))

    def inner_odd_indexed(self) -> IndexableTrace:
        return self.mapping_operated(lambda y: y.inner_mapped(lambda x: Indexable(x).odd_indexed()))

    def inner_even_indexed(self) -> IndexableTrace:
        return self.mapping_operated(lambda y: y.inner_mapped(lambda x: Indexable(x).even_indexed()))

    def colored(self, color: str) -> IndexableTrace:
        return self.indexed(self.to_color_indice(color))

    def not_empty_indexed(self) -> IndexableTrace:
        return self.indexed(self.to_not_empty_indice())


class NoneStepTrace(NamedTuple):
    trace: Trace
    indice: Iterable[int]

    @classmethod
    def from_trace_with_color(cls, trace: Trace, color: str) -> NoneStepTrace:
        indice: Iterable[int] = IndexableTrace._make(trace).to_color_indice(color)

        return NoneStepTrace(Trace.from_FENs(Indexable(Mappable.concatenated(trace.fens)).indexed(indice)), indice)

    def only_FEN_leaved(self) -> NoneStepTrace:
        return NoneStepTrace(
            Trace(
                self.trace.fens,
                Enumerable.filled([], len(self.trace.fens)),
                Enumerable.filled([], len(self.trace.fens)),
            ),
            self.indice,
        )


class OneStepTrace(NamedTuple):
    next_trace: Trace
    indice: Iterable[int]
    next_indice: Iterable[int]

    @classmethod
    def from_none_step_with_prev_indice(cls, none_step: NoneStepTrace, prev_indice: Iterable[int]) -> OneStepTrace:
        return OneStepTrace(none_step.trace, prev_indice, none_step.indice)


class SplitableTrace(Trace):
    @classmethod
    def cross_concatenated(cls, traces: list[tuple[Trace, Trace]]) -> tuple[SplitableTrace, SplitableTrace]:
        return (
            SplitableTrace._make(MappableTrace._make(traces[0][0]).concatenated(traces[1][1])),
            SplitableTrace._make(MappableTrace._make(traces[1][0]).concatenated(traces[0][1])),
        )

    @classmethod
    def color_unioned(cls, length: int, white_trace: OneStepTrace, black_trace: OneStepTrace) -> SplitableTrace:
        return SplitableTrace(
            *map(
                lambda p: Mappable.disjoint_unioned([], length, p),
                zip(
                    zip([white_trace.next_indice, white_trace.next_indice, white_trace.indice], white_trace.next_trace),
                    zip([black_trace.next_indice, black_trace.next_indice, black_trace.indice], black_trace.next_trace),
                ),
            )
        )

    def mapping_operated(self, mapper: Callable) -> SplitableTrace:
        return SplitableTrace._make(mapper(IndexableTrace._make(self)))

    def color_splited(self) -> tuple[SplitableTrace, SplitableTrace]:
        return self.mapping_operated(lambda x: x.colored("w")), self.mapping_operated(lambda x: x.colored("b"))

    def inner_parity_splited(self) -> tuple[SplitableTrace, SplitableTrace]:
        return (
            self.mapping_operated(lambda x: x.inner_even_indexed().not_empty_indexed().SAN_normalized()),
            self.mapping_operated(lambda x: x.inner_odd_indexed().not_empty_indexed().SAN_normalized()),
        )

    def splited_with_color_turn(self) -> tuple[SplitableTrace, SplitableTrace]:
        return SplitableTrace.cross_concatenated(list(map(lambda x: x.inner_parity_splited(), self.color_splited())))


class MovableTrace(Trace):
    @classmethod
    def from_FENs(cls, fens: list[str]) -> MovableTrace:
        return MovableTrace._make(Trace.from_FENs(fens))

    async def to_move(self, status: IStatus, movement: IMovement) -> tuple[Trace, Iterable[int]]:
        fens = Mappable.concatenated(self.fens)
        results, legal_moves = await status.status(fens)
        secondary_indice: list[int] = Enumerable(results).to_conditional_indice(lambda x: x == 0)
        next_fens, next_sans = await movement.movement(Indexable(fens).indexed(secondary_indice), legal_moves)

        return Trace.from_unwrapped(next_fens, next_sans, results), secondary_indice

    async def to_last_update(self, status: IStatus) -> Trace:
        results, _ = await status.status(Mappable.concatenated(self.fens))

        return Trace.from_unwrapped([], [], results)

    def mapping_operated(self, mapper: Callable) -> MovableTrace:
        return MovableTrace._make(mapper(MappableTrace._make(self)))

    def moved(self, white_trace: OneStepTrace, black_trace: OneStepTrace) -> MovableTrace:
        return self.mapping_operated(
            lambda x: x.inner_concatenated(SplitableTrace.color_unioned(len(self.fens), white_trace, black_trace))
        )


class MovableNoneStepTrace(NoneStepTrace):
    async def moved(self, status: IStatus, movement: IMovement) -> MovableNoneStepTrace:
        trace, secondary_indice = await MovableTrace._make(self.trace).to_move(status, movement)

        return MovableNoneStepTrace(trace, Indexable(self.indice).indexed(secondary_indice))

    async def last_status_updated(self, status: IStatus) -> MovableNoneStepTrace:
        return MovableNoneStepTrace(await MovableTrace._make(self.trace).to_last_update(status), self.indice)


class OneStepProduct(NamedTuple):
    trace: MovableTrace
    white: NoneStepTrace
    black: NoneStepTrace

    @classmethod
    def from_FENs(cls, fens: list[str]) -> OneStepProduct:
        trace: MovableTrace = MovableTrace.from_FENs(fens)

        return OneStepProduct(
            trace,
            NoneStepTrace.from_trace_with_color(trace, "w"),
            NoneStepTrace.from_trace_with_color(trace, "b"),
        )

    async def one_step_produced(
        self, status: IStatus, movement_white: IMovement, movement_black: IMovement
    ) -> OneStepProduct:
        next_white: NoneStepTrace = await MovableNoneStepTrace._make(self.white).moved(status, movement_white)
        next_black: NoneStepTrace = await MovableNoneStepTrace._make(self.black).moved(status, movement_black)

        return OneStepProduct(
            self.trace.moved(
                OneStepTrace.from_none_step_with_prev_indice(next_white, self.white.indice),
                OneStepTrace.from_none_step_with_prev_indice(next_black, self.black.indice),
            ),
            next_black.only_FEN_leaved(),
            next_white.only_FEN_leaved(),
        )

    async def none_step_produced(self, status: IStatus) -> OneStepProduct:
        next_white: NoneStepTrace = await MovableNoneStepTrace._make(self.white).last_status_updated(status)
        next_black: NoneStepTrace = await MovableNoneStepTrace._make(self.black).last_status_updated(status)

        return OneStepProduct(
            self.trace.moved(
                OneStepTrace.from_none_step_with_prev_indice(next_white, self.white.indice),
                OneStepTrace.from_none_step_with_prev_indice(next_black, self.black.indice),
            ),
            next_black.only_FEN_leaved(),
            next_white.only_FEN_leaved(),
        )

    def empty(self) -> bool:
        return self.white.indice == [] and self.black.indice == []

    def splited(self) -> tuple[Trace, Trace]:
        return SplitableTrace._make(self.trace.end_corrected()).splited_with_color_turn()


class ProducableTrace(NamedTuple):
    step: int
    fens: list[str]
    status: IStatus
    movement_white: IMovement
    movement_black: IMovement

    async def produced(self) -> tuple[Trace, Trace]:
        product: OneStepProduct = OneStepProduct.from_FENs(self.fens)

        for _ in range(self.step):
            if product.empty():
                break

            product = await product.one_step_produced(self.status, self.movement_white, self.movement_black)

        if not product.empty():
            product = await product.none_step_produced(self.status)

        return product.splited()
