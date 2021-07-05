# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT


from __future__ import annotations


class Score(str):
    @classmethod
    def from_results(cls, results: list[float]) -> Score:
        if results[-1] == 0.5:
            return Score.draw()

        return Score.white_win() if len(results) % 2 == 1 else Score.black_win()

    @classmethod
    def white_win(cls) -> Score:
        return Score("1-0")

    @classmethod
    def black_win(cls) -> Score:
        return Score("0-1")

    @classmethod
    def draw(cls) -> Score:
        return Score("1/2-1/2")
