"""A4縦・家庭教師用の月次指導明細兼領収書."""

import json
import os
from pathlib import Path

from manim import (
    Line,
    Rectangle,
    RoundedRectangle,
    Text,
    VGroup,
    config,
)

from manim_research import LightScene


# ============================================================
# 用紙
# ============================================================

A4_WIDTH = 21.0
A4_HEIGHT = 29.7

PIXEL_WIDTH = 2480
PIXEL_HEIGHT = 3508

config.frame_width = A4_WIDTH
config.frame_height = A4_HEIGHT
config.pixel_width = PIXEL_WIDTH
config.pixel_height = PIXEL_HEIGHT
config.background_color = "#FFFFFF"


# ============================================================
# データ
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
JSON_DIR = BASE_DIR / "json"

DEFAULT_CONTENT_FILE_NAME = "receipt_2026_09.json"


def resolve_content_file() -> Path:
    requested = os.environ.get(
        "MANIM_CONTENT_FILE",
        DEFAULT_CONTENT_FILE_NAME,
    )

    requested_path = Path(requested).expanduser()

    if requested_path.is_absolute():
        return requested_path

    cwd_path = Path.cwd() / requested_path

    if cwd_path.is_file():
        return cwd_path.resolve()

    return JSON_DIR / requested_path


CONTENT_FILE = resolve_content_file()

config.output_file = f"tutoring_receipt_{CONTENT_FILE.stem}"


def load_content(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(
            f"JSONが見つかりません: {path}"
        )

    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    sessions = data.get("sessions", [])
    expenses = data.get("expenses", [])

    tuition_subtotal = 0

    for session in sessions:
        hours = session.get("hours")
        hourly_rate = session.get("hourly_rate")

        if hours is not None and hourly_rate is not None:
            session["amount"] = round(
                float(hours) * float(hourly_rate)
            )
        else:
            session["amount"] = None

        if session["amount"] is not None:
            tuition_subtotal += session["amount"]

    expense_total = 0

    for expense in expenses:
        amount = expense.get("amount")

        if amount is not None:
            expense_total += float(amount)

    data["tuition_subtotal"] = tuition_subtotal
    data["grand_total"] = tuition_subtotal + expense_total

    return data


CONTENT = load_content(CONTENT_FILE)


# ============================================================
# 表示用
# ============================================================

def format_yen(value) -> str:
    if value is None:
        return ""

    return f"{round(float(value)):,}円"


def recipient_text(value: str) -> str:
    value = value.strip()

    if not value:
        return "＿＿＿＿＿＿＿＿＿＿ 様"

    if value.endswith("様"):
        return value

    return f"{value} 様"


# ============================================================
# デザイン
# ============================================================

PAGE_LEFT = -9.1
PAGE_RIGHT = 9.1
PAGE_WIDTH = PAGE_RIGHT - PAGE_LEFT

TEXT_COLOR = "#263238"
MUTED_COLOR = "#667085"
LINE_COLOR = "#98A2B3"

ACCENT_COLOR = "#315C8C"
ACCENT_LIGHT = "#EAF1F8"
SURFACE_COLOR = "#F7F8FA"


# ============================================================
# Scene
# ============================================================

class TutoringReceipt(LightScene):

    def make_text(
        self,
        value: str,
        *,
        font_size: float = 30,
        color: str = TEXT_COLOR,
        weight: str = "NORMAL",
        max_width: float | None = None,
    ) -> Text:

        mob = Text(
            value if value else " ",
            font=self.theme.sans_font,
            font_size=font_size,
            color=color,
            weight=weight,
        )

        if (
            max_width is not None
            and mob.width > max_width
        ):
            mob.scale_to_fit_width(max_width)

        return mob


    @staticmethod
    def put_left(
        mob,
        x: float,
        y: float,
    ):
        mob.move_to(
            [
                x + mob.width / 2,
                y,
                0,
            ]
        )

        return mob


    @staticmethod
    def put_right(
        mob,
        x: float,
        y: float,
    ):
        mob.move_to(
            [
                x - mob.width / 2,
                y,
                0,
            ]
        )

        return mob


    # ========================================================
    # タイトル
    # ========================================================

    def add_header(self) -> None:

        title = self.make_text(
            CONTENT["title"],
            font_size=54,
            weight="BOLD",
        )

        title.move_to(
            [0, 13.25, 0]
        )

        rule = Line(
            [PAGE_LEFT, 12.55, 0],
            [PAGE_RIGHT, 12.55, 0],
            color=ACCENT_COLOR,
            stroke_width=2.0,
        )

        self.add(
            title,
            rule,
        )


    # ========================================================
    # 宛名
    # ========================================================

    def add_recipient(self) -> None:

        label = self.make_text(
            "宛名",
            font_size=22,
            color=MUTED_COLOR,
        )

        self.put_left(
            label,
            PAGE_LEFT,
            11.78,
        )

        recipient = self.make_text(
            recipient_text(
                CONTENT.get(
                    "recipient",
                    "",
                )
            ),
            font_size=39,
            weight="BOLD",
            max_width=13.5,
        )

        self.put_left(
            recipient,
            PAGE_LEFT,
            11.05,
        )

        line = Line(
            [PAGE_LEFT, 10.48, 0],
            [6.0, 10.48, 0],
            color=LINE_COLOR,
            stroke_width=1.1,
        )

        self.add(
            label,
            recipient,
            line,
        )


    # ========================================================
    # 対象月・領収日・但し書き
    #
    # 上部の「領収金額」欄は置かない
    # ========================================================

    def add_metadata(self) -> None:

        y1 = 9.45
        y2 = 8.55

        period_label = self.make_text(
            "対象月",
            font_size=22,
            color=MUTED_COLOR,
        )

        period = self.make_text(
            CONTENT.get(
                "period",
                "",
            ),
            font_size=29,
            weight="BOLD",
            max_width=5.5,
        )

        date_label = self.make_text(
            "領収日",
            font_size=22,
            color=MUTED_COLOR,
        )

        date = self.make_text(
            CONTENT.get(
                "received_date",
                "",
            ),
            font_size=29,
            max_width=6.5,
        )

        self.put_left(
            period_label,
            PAGE_LEFT,
            y1,
        )

        self.put_left(
            period,
            PAGE_LEFT + 1.7,
            y1,
        )

        self.put_left(
            date_label,
            1.1,
            y1,
        )

        self.put_left(
            date,
            2.85,
            y1,
        )

        description_label = self.make_text(
            "但し",
            font_size=22,
            color=MUTED_COLOR,
        )

        description = self.make_text(
            CONTENT.get(
                "description",
                "",
            ),
            font_size=28,
            max_width=14.8,
        )

        self.put_left(
            description_label,
            PAGE_LEFT,
            y2,
        )

        self.put_left(
            description,
            PAGE_LEFT + 1.7,
            y2,
        )

        self.add(
            period_label,
            period,
            date_label,
            date,
            description_label,
            description,
        )


    # ========================================================
    # 指導明細表
    # ========================================================

    def make_table(self):

        sessions = CONTENT.get(
            "sessions",
            [],
        )

        row_count = max(
            5,
            len(sessions),
        )

        table_top = 7.95
        header_height = 0.90
        row_height = 0.86

        # 合計 18.2 = PAGE_WIDTH
        #
        # 指導時間を最も広くする
        columns = [
            ("指導日", 3.75),
            ("指導時間", 6.15),
            ("時給", 3.65),
            ("金額", 4.65),
        ]

        total_height = (
            header_height
            + row_count * row_height
        )

        table_bottom = (
            table_top
            - total_height
        )

        table = VGroup()

        border = Rectangle(
            width=PAGE_WIDTH,
            height=total_height,
            stroke_color=LINE_COLOR,
            stroke_width=1.3,
        )

        border.move_to(
            [
                0,
                (
                    table_top
                    + table_bottom
                ) / 2,
                0,
            ]
        )

        table.add(border)

        header_bg = Rectangle(
            width=PAGE_WIDTH,
            height=header_height,
            stroke_width=0,
            fill_color=SURFACE_COLOR,
            fill_opacity=1.0,
        )

        header_bg.move_to(
            [
                0,
                table_top
                - header_height / 2,
                0,
            ]
        )

        table.add(header_bg)

        x_positions = [
            PAGE_LEFT
        ]

        x = PAGE_LEFT

        for _, width in columns:
            x += width
            x_positions.append(x)

        for x in x_positions[1:-1]:
            table.add(
                Line(
                    [x, table_top, 0],
                    [x, table_bottom, 0],
                    color=LINE_COLOR,
                    stroke_width=0.85,
                )
            )

        header_bottom = (
            table_top
            - header_height
        )

        table.add(
            Line(
                [PAGE_LEFT, header_bottom, 0],
                [PAGE_RIGHT, header_bottom, 0],
                color=LINE_COLOR,
                stroke_width=1.0,
            )
        )

        for row in range(
            1,
            row_count,
        ):
            y = (
                header_bottom
                - row * row_height
            )

            table.add(
                Line(
                    [PAGE_LEFT, y, 0],
                    [PAGE_RIGHT, y, 0],
                    color=LINE_COLOR,
                    stroke_width=0.7,
                )
            )

        # ヘッダー
        x = PAGE_LEFT

        for label, width in columns:

            text = self.make_text(
                label,
                font_size=25,
                weight="BOLD",
            )

            text.move_to(
                [
                    x + width / 2,
                    table_top
                    - header_height / 2,
                    0,
                ]
            )

            table.add(text)

            x += width

        # データ
        for row_index in range(
            row_count
        ):

            if row_index < len(
                sessions
            ):

                session = sessions[
                    row_index
                ]

                values = [
                    str(
                        session.get(
                            "date",
                            "",
                        )
                    ),
                    str(
                        session.get(
                            "time",
                            "",
                        )
                    ),
                    format_yen(
                        session.get(
                            "hourly_rate"
                        )
                    ),
                    format_yen(
                        session.get(
                            "amount"
                        )
                    ),
                ]

            else:

                values = [
                    "",
                    "",
                    "",
                    "",
                ]

            row_y = (
                header_bottom
                - (
                    row_index
                    + 0.5
                )
                * row_height
            )

            x = PAGE_LEFT

            for value, (_, width) in zip(
                values,
                columns,
                strict=True,
            ):

                text = self.make_text(
                    value,
                    font_size=24,
                    max_width=width - 0.4,
                )

                text.move_to(
                    [
                        x + width / 2,
                        row_y,
                        0,
                    ]
                )

                table.add(text)

                x += width

        return (
            table,
            table_bottom,
        )


    # ========================================================
    # 金額集計
    # ========================================================

    def add_summary(
        self,
        table_bottom: float,
    ) -> float:

        rows = [
            (
                "指導料小計",
                CONTENT.get(
                    "tuition_subtotal"
                ),
            )
        ]

        for expense in CONTENT.get(
            "expenses",
            [],
        ):
            rows.append(
                (
                    expense.get(
                        "label",
                        "",
                    ),
                    expense.get(
                        "amount"
                    ),
                )
            )

        start_y = (
            table_bottom
            - 0.55
        )

        label_x = 2.7
        amount_x = PAGE_RIGHT

        row_gap = 0.70

        for index, (
            label,
            amount,
        ) in enumerate(rows):

            y = (
                start_y
                - index * row_gap
            )

            label_mob = self.make_text(
                label,
                font_size=23,
                color=MUTED_COLOR,
            )

            amount_mob = self.make_text(
                format_yen(amount),
                font_size=28,
                max_width=4.1,
            )

            self.put_left(
                label_mob,
                label_x,
                y,
            )

            self.put_right(
                amount_mob,
                amount_x,
                y,
            )

            self.add(
                label_mob,
                amount_mob,
            )

        total_y = (
            start_y
            - len(rows) * row_gap
            - 0.35
        )

        total_box = RoundedRectangle(
            width=7.35,
            height=1.18,
            corner_radius=0.13,
            stroke_color=ACCENT_COLOR,
            stroke_width=1.7,
            fill_color=ACCENT_LIGHT,
            fill_opacity=1.0,
        )

        total_box.move_to(
            [
                5.42,
                total_y,
                0,
            ]
        )

        total_label = self.make_text(
            "合計",
            font_size=29,
            weight="BOLD",
        )

        total_amount = self.make_text(
            format_yen(
                CONTENT.get(
                    "grand_total"
                )
            ),
            font_size=36,
            color=ACCENT_COLOR,
            weight="BOLD",
        )

        self.put_left(
            total_label,
            2.15,
            total_y,
        )

        self.put_right(
            total_amount,
            PAGE_RIGHT - 0.30,
            total_y,
        )

        self.add(
            total_box,
            total_label,
            total_amount,
        )

        return total_y


    # ========================================================
    # 領収文・発行者
    # ========================================================

    def add_footer(
        self,
        summary_y: float,
    ) -> None:

        statement_y = (
            summary_y
            - 1.25
        )

        statement = self.make_text(
            "上記金額を、上記但し書きの内容として領収いたしました。",
            font_size=23,
            max_width=PAGE_WIDTH,
        )

        self.put_left(
            statement,
            PAGE_LEFT,
            statement_y,
        )

        panel_height = 3.15

        panel_center_y = (
            statement_y
            - 2.45
        )

        panel = RoundedRectangle(
            width=PAGE_WIDTH,
            height=panel_height,
            corner_radius=0.14,
            stroke_color=LINE_COLOR,
            stroke_width=1.1,
            fill_color=SURFACE_COLOR,
            fill_opacity=0.60,
        )

        panel.move_to(
            [
                0,
                panel_center_y,
                0,
            ]
        )

        issuer_label = self.make_text(
            "発行者",
            font_size=22,
            color=MUTED_COLOR,
        )

        issuer_name = self.make_text(
            CONTENT.get(
                "issuer",
                {},
            ).get(
                "name",
                "",
            ),
            font_size=30,
            weight="BOLD",
        )

        self.put_left(
            issuer_label,
            PAGE_LEFT + 0.5,
            panel_center_y + 0.60,
        )

        self.put_left(
            issuer_name,
            PAGE_LEFT + 0.5,
            panel_center_y - 0.08,
        )

        stamp_box = Rectangle(
            width=2.75,
            height=2.25,
            stroke_color=LINE_COLOR,
            stroke_width=1.0,
        )

        stamp_box.move_to(
            [
                7.05,
                panel_center_y - 0.05,
                0,
            ]
        )

        stamp_label = self.make_text(
            "署名・押印",
            font_size=20,
            color=MUTED_COLOR,
        )

        stamp_label.move_to(
            [
                7.05,
                panel_center_y + 1.30,
                0,
            ]
        )

        self.add(
            statement,
            panel,
            issuer_label,
            issuer_name,
            stamp_box,
            stamp_label,
        )


    # ========================================================
    # Scene
    # ========================================================

    def construct(self) -> None:

        self.add_header()
        self.add_recipient()
        self.add_metadata()

        table, table_bottom = (
            self.make_table()
        )

        self.add(table)

        summary_y = (
            self.add_summary(
                table_bottom
            )
        )

        self.add_footer(
            summary_y
        )
