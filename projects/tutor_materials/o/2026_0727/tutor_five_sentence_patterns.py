"""A simple A4-landscape reference sheet for the five sentence patterns."""

from __future__ import annotations

from tutor_english_a4 import table
from tutor_english_four_pages import TutorPage


class FiveSentencePatternsA4(TutorPage):
    """Reference chart for the five basic English sentence patterns."""

    page_number = "1 / 1"

    def construct(self) -> None:
        self.add_heading("5つの文型")

        rows = [
            [
                "第1文型",
                "S + V",
                "S が ～ する",
                "Birds fly.",
                "動詞だけで意味が\nほぼ完結する。",
            ],
            [
                "第2文型",
                "S + V + C",
                "S ＝ C",
                "He is kind.",
                "補語 C は主語 S を\n説明する。",
            ],
            [
                "第3文型",
                "S + V + O",
                "S が O を ～ する",
                "I play tennis.",
                "目的語 O を1つとる。",
            ],
            [
                "第4文型",
                "S + V + O + O",
                "S が 人に 物を\n～ する",
                "She gave me\na book.",
                "目的語が2つある。",
            ],
            [
                "第5文型",
                "S + V + O + C",
                "O ＝ C",
                "We call him Ken.",
                "補語 C は目的語 O を\n説明する。",
            ],
        ]

        column_widths = [1.65, 2.35, 2.65, 2.75, 3.4]
        row_height = 1.42
        header_height = 0.84

        chart = table(
            ["文型", "形", "意味のイメージ", "例文", "ポイント"],
            rows,
            column_widths,
            row_height,
            header_height,
            22,
        )
        chart.move_to([0, -0.32, 0])

        self.add(chart)
        self.add_page_number()
