"""Four independent A4-landscape tutoring sheets with enlarged tables."""

from __future__ import annotations

from manim import WHITE, Line, Scene

from tutor_english_a4 import (
    GRID,
    NAVY,
    label,
    table,
)


class TutorPage(Scene):
    """Shared A4 landscape page furniture."""

    page_number = ""

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = WHITE

    def add_heading(self, title: str) -> None:
        """ページ上部にメインタイトルだけを配置する。"""
        heading = label(
            title,
            44,
            color=NAVY,
            weight="BOLD",
        )
        heading.move_to([0, 4.4, 0])
        self.add(heading)

    def add_page_number(self) -> None:
        page = label(
            self.page_number,
            16,
            color=NAVY,
        )
        page.move_to([6.45, -4.72, 0])
        self.add(page)

    def add_cell_lines(
        self,
        *,
        center_y: float,
        header_height: float,
        row_height: float,
        row_count: int,
        column_widths: list[float],
        writable_columns: list[int],
        line_ratio: float = 0.76,
        y_offset: float = -0.1,
    ) -> None:
        """指定した表のセル内に記入用の横線を配置する。"""
        total_height = header_height + row_count * row_height
        top = center_y + total_height / 2
        left = -sum(column_widths) / 2

        column_centers: list[float] = []
        current_x = left

        for width in column_widths:
            column_centers.append(current_x + width / 2)
            current_x += width

        for row_index in range(row_count):
            y = top - header_height - row_height * (row_index + 0.5) + y_offset

            for column_index in writable_columns:
                width = column_widths[column_index]
                center_x = column_centers[column_index]
                half_length = width * line_ratio / 2

                writing_line = Line(
                    [center_x - half_length, y, 0],
                    [center_x + half_length, y, 0],
                    color=GRID,
                    stroke_width=1.4,
                )
                self.add(writing_line)


class PronounReferenceA4(TutorPage):
    """Reference chart for personal pronoun forms."""

    page_number = "1 / 4"

    def construct(self) -> None:
        self.add_heading("代名詞の活用形")

        rows = [
            ["わたし", "I", "my", "me", "mine"],
            ["あなた／あなたたち", "you", "your", "you", "yours"],
            ["彼", "he", "his", "him", "his"],
            ["彼女", "she", "her", "her", "hers"],
            ["わたしたち", "we", "our", "us", "ours"],
            ["彼ら／彼女ら", "they", "their", "them", "theirs"],
        ]

        column_widths = [2.9, 2.35, 2.35, 2.35, 2.75]
        row_height = 1.18
        header_height = 0.84

        chart = table(
            ["意味", "主格", "所有格", "目的格", "所有代名詞"],
            rows,
            column_widths,
            row_height,
            header_height,
            24,
        )
        chart.move_to([0, -0.32, 0])

        self.add(chart)
        self.add_page_number()


class PastTenseReferenceA4(TutorPage):
    """Reference chart for common irregular past-tense verbs."""

    page_number = "2 / 4"

    def construct(self) -> None:
        self.add_heading("不規則動詞の過去形")

        rows = [
            ["～である／いる", "be", "was / were"],
            ["する", "do", "did"],
            ["得る／着く", "get", "got"],
            ["与える", "give", "gave"],
            ["持っている", "have", "had"],
            ["行く", "go", "went"],
            ["来る", "come", "came"],
            ["見る", "see", "saw"],
            ["食べる", "eat", "ate"],
            ["作る", "make", "made"],
            ["買う", "buy", "bought"],
            ["取る／持っていく", "take", "took"],
            ["書く", "write", "wrote"],
            ["読む", "read", "read"],
            ["話す", "speak", "spoke"],
            ["知っている", "know", "knew"],
            ["思う", "think", "thought"],
            ["見つける", "find", "found"],
            ["会う", "meet", "met"],
            ["走る", "run", "ran"],
        ]

        column_widths = [4.4, 4.0, 4.4]
        row_height = 0.38
        header_height = 0.72

        chart = table(
            ["意味", "原形", "過去形"],
            rows,
            column_widths,
            row_height,
            header_height,
            18,
        )
        chart.move_to([0, -0.35, 0])

        self.add(chart)
        self.add_page_number()


class PronounPracticeA4(TutorPage):
    """Writing exercise for personal pronoun forms."""

    page_number = "3 / 4"

    def construct(self) -> None:
        self.add_heading("代名詞の活用形　練習")

        meanings = [
            "わたし",
            "あなた／あなたたち",
            "彼",
            "彼女",
            "わたしたち",
            "彼ら／彼女ら",
        ]

        rows = [[meaning, "", "", "", ""] for meaning in meanings]

        column_widths = [2.9, 2.35, 2.35, 2.35, 2.75]
        row_height = 1.18
        header_height = 0.84
        center_y = -0.32

        chart = table(
            ["意味", "主格", "所有格", "目的格", "所有代名詞"],
            rows,
            column_widths,
            row_height,
            header_height,
            23,
        )
        chart.move_to([0, center_y, 0])

        self.add(chart)

        self.add_cell_lines(
            center_y=center_y,
            header_height=header_height,
            row_height=row_height,
            row_count=len(rows),
            column_widths=column_widths,
            writable_columns=[1, 2, 3, 4],
            line_ratio=0.76,
            y_offset=-0.12,
        )

        self.add_page_number()


class PastTensePracticeA4(TutorPage):
    """Writing exercise for common irregular past-tense verbs."""

    page_number = "4 / 4"

    def construct(self) -> None:
        self.add_heading("不規則動詞の過去形　練習")

        rows = [
            ["1", "～である／いる", "", ""],
            ["2", "する", "", ""],
            ["3", "得る／着く", "", ""],
            ["4", "与える", "", ""],
            ["5", "持っている", "", ""],
            ["6", "行く", "", ""],
            ["7", "来る", "", ""],
            ["8", "見る", "", ""],
            ["9", "食べる", "", ""],
            ["10", "作る", "", ""],
            ["11", "買う", "", ""],
            ["12", "取る／持っていく", "", ""],
            ["13", "書く", "", ""],
            ["14", "読む", "", ""],
            ["15", "話す", "", ""],
            ["16", "知っている", "", ""],
            ["17", "思う", "", ""],
            ["18", "見つける", "", ""],
            ["19", "会う", "", ""],
            ["20", "走る", "", ""],
        ]

        column_widths = [1.0, 4.0, 3.8, 4.0]
        row_height = 0.38
        header_height = 0.72
        center_y = -0.35

        chart = table(
            ["番号", "意味", "原形", "過去形"],
            rows,
            column_widths,
            row_height,
            header_height,
            17,
        )
        chart.move_to([0, center_y, 0])

        self.add(chart)

        self.add_cell_lines(
            center_y=center_y,
            header_height=header_height,
            row_height=row_height,
            row_count=len(rows),
            column_widths=column_widths,
            writable_columns=[2, 3],
            line_ratio=0.76,
            y_offset=-0.07,
        )

        self.add_page_number()
