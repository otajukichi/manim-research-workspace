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

    with path.open(
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    sessions = data.get(
        "sessions",
        [],
    )

    tuition_subtotal = 0
    transport_subtotal = 0

    for session in sessions:

        hours = session.get(
            "hours"
        )

        hourly_rate = session.get(
            "hourly_rate"
        )

        if (
            hours is not None
            and hourly_rate is not None
        ):
            session["amount"] = round(
                float(hours)
                * float(hourly_rate)
            )
        else:
            session["amount"] = None

        if session["amount"] is not None:
            tuition_subtotal += session[
                "amount"
            ]

        transport_fee = session.get(
            "transport_fee",
            0,
        )

        if transport_fee in (
            None,
            "",
        ):
            transport_fee = 0

        transport_fee = round(
            float(transport_fee)
        )

        session["transport_fee"] = (
            transport_fee
        )

        transport_subtotal += (
            transport_fee
        )

    data["tuition_subtotal"] = (
        tuition_subtotal
    )

    data["transport_subtotal"] = (
        transport_subtotal
    )

    data["grand_total"] = (
        tuition_subtotal
        + transport_subtotal
    )

    return data


CONTENT = load_content(
    CONTENT_FILE
)


# ============================================================
# 表示
# ============================================================

def format_yen(value) -> str:
    if value is None:
        return ""

    return (
        f"{round(float(value)):,}円"
    )


def recipient_text(
    value: str,
) -> str:

    value = value.strip()

    if not value:
        return "＿＿＿＿＿＿＿＿＿＿ 様"

    if value.endswith("様"):
        return value

    return f"{value} 様"


# ============================================================
# デザイン
#
# 印刷で薄くならないよう、
# グレー系もかなり濃く設定する。
# ============================================================

PAGE_LEFT = -9.1
PAGE_RIGHT = 9.1
PAGE_WIDTH = (
    PAGE_RIGHT
    - PAGE_LEFT
)

TEXT_COLOR = "#1F2937"

MUTED_COLOR = "#273444"

LINE_COLOR = "#2F3B4A"

ACCENT_COLOR = "#234F7D"

ACCENT_LIGHT = "#B7CCE3"

SURFACE_COLOR = "#CBD5E1"


# ============================================================
# Scene
# ============================================================

class TutoringReceipt(
    LightScene
):

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
            mob.scale_to_fit_width(
                max_width
            )

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

    def add_header(
        self,
    ) -> None:

        title = self.make_text(
            CONTENT["title"],
            font_size=54,
            weight="BOLD",
        )

        title.move_to(
            [
                0,
                13.25,
                0,
            ]
        )

        rule = Line(
            [
                PAGE_LEFT,
                12.55,
                0,
            ],
            [
                PAGE_RIGHT,
                12.55,
                0,
            ],
            color=ACCENT_COLOR,
            stroke_width=2.3,
        )

        self.add(
            title,
            rule,
        )


    # ========================================================
    # 宛名
    # ========================================================

    def add_recipient(
        self,
    ) -> None:

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
            [
                PAGE_LEFT,
                10.48,
                0,
            ],
            [
                6.0,
                10.48,
                0,
            ],
            color=LINE_COLOR,
            stroke_width=1.8,
        )

        self.add(
            label,
            recipient,
            line,
        )


    # ========================================================
    # 対象月・領収日・但し書き
    # ========================================================

    def add_metadata(
        self,
    ) -> None:

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

        description_label = (
            self.make_text(
                "但し",
                font_size=22,
                color=MUTED_COLOR,
            )
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
    # 指導明細
    #
    # 縦線は一切使用しない。
    # 左右の外枠もなし。
    # 横線のみ。
    # ========================================================

    def make_table(
        self,
    ):

        sessions = CONTENT.get(
            "sessions",
            [],
        )

        row_count = max(
            5,
            len(sessions),
        )

        table_top = 7.95

        header_height = 0.92
        row_height = 0.88

        columns = [
            (
                "指導日",
                3.0,
            ),
            (
                "指導時間",
                5.2,
            ),
            (
                "時給",
                3.0,
            ),
            (
                "指導料",
                3.5,
            ),
            (
                "交通費",
                3.5,
            ),
        ]

        header_bottom = (
            table_top
            - header_height
        )

        table_bottom = (
            header_bottom
            - row_count
            * row_height
        )

        table = VGroup()

        # ----------------------------------------
        # ヘッダー背景
        # ストロークなしなので縦枠は出ない
        # ----------------------------------------

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

        table.add(
            header_bg
        )

        # ----------------------------------------
        # 上端
        # ----------------------------------------

        table.add(
            Line(
                [
                    PAGE_LEFT,
                    table_top,
                    0,
                ],
                [
                    PAGE_RIGHT,
                    table_top,
                    0,
                ],
                color=LINE_COLOR,
                stroke_width=2.0,
            )
        )

        # ----------------------------------------
        # ヘッダー下
        # ----------------------------------------

        table.add(
            Line(
                [
                    PAGE_LEFT,
                    header_bottom,
                    0,
                ],
                [
                    PAGE_RIGHT,
                    header_bottom,
                    0,
                ],
                color=LINE_COLOR,
                stroke_width=1.8,
            )
        )

        # ----------------------------------------
        # 各行の横線
        # 最後の線が表の下端になる
        # ----------------------------------------

        for row in range(
            1,
            row_count + 1,
        ):

            y = (
                header_bottom
                - row
                * row_height
            )

            table.add(
                Line(
                    [
                        PAGE_LEFT,
                        y,
                        0,
                    ],
                    [
                        PAGE_RIGHT,
                        y,
                        0,
                    ],
                    color=LINE_COLOR,
                    stroke_width=1.35,
                )
            )

        # ----------------------------------------
        # ヘッダー文字
        # ----------------------------------------

        x = PAGE_LEFT

        for label, width in columns:

            text = self.make_text(
                label,
                font_size=24,
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

            table.add(
                text
            )

            x += width

        # ----------------------------------------
        # データ
        # ----------------------------------------

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
                    format_yen(
                        session.get(
                            "transport_fee",
                            0,
                        )
                    ),
                ]

            else:

                values = [
                    "",
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

            for value, (
                _,
                width,
            ) in zip(
                values,
                columns,
                strict=True,
            ):

                text = self.make_text(
                    value,
                    font_size=24,
                    max_width=width - 0.35,
                )

                text.move_to(
                    [
                        x + width / 2,
                        row_y,
                        0,
                    ]
                )

                table.add(
                    text
                )

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
            ),
            (
                "交通費小計",
                CONTENT.get(
                    "transport_subtotal"
                ),
            ),
        ]

        start_y = (
            table_bottom
            - 0.60
        )

        label_x = 2.7
        amount_x = PAGE_RIGHT

        row_gap = 0.72

        for index, (
            label,
            amount,
        ) in enumerate(
            rows
        ):

            y = (
                start_y
                - index
                * row_gap
            )

            label_mob = (
                self.make_text(
                    label,
                    font_size=23,
                    color=MUTED_COLOR,
                )
            )

            amount_mob = (
                self.make_text(
                    format_yen(
                        amount
                    ),
                    font_size=28,
                    max_width=4.1,
                )
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
            - len(rows)
            * row_gap
            - 0.35
        )

        total_box = RoundedRectangle(
            width=7.35,
            height=1.18,
            corner_radius=0.13,
            stroke_color=ACCENT_COLOR,
            stroke_width=2.4,
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

        total_amount = (
            self.make_text(
                format_yen(
                    CONTENT.get(
                        "grand_total"
                    )
                ),
                font_size=36,
                color=ACCENT_COLOR,
                weight="BOLD",
            )
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

        # 発行者は控えめにする
        issuer_y = (
            statement_y
            - 1.25
        )

        issuer_label = (
            self.make_text(
                "発行者",
                font_size=17,
                color=MUTED_COLOR,
            )
        )

        issuer_name = (
            self.make_text(
                CONTENT.get(
                    "issuer",
                    {},
                ).get(
                    "name",
                    "",
                ),
                font_size=25,
                weight="BOLD",
            )
        )

        self.put_left(
            issuer_label,
            PAGE_LEFT,
            issuer_y,
        )

        self.put_left(
            issuer_name,
            PAGE_LEFT + 1.45,
            issuer_y,
        )

        self.add(
            statement,
            issuer_label,
            issuer_name,
        )


    # ========================================================
    # Scene
    # ========================================================

    def construct(
        self,
    ) -> None:

        self.add_header()
        self.add_recipient()
        self.add_metadata()

        table, table_bottom = (
            self.make_table()
        )

        self.add(
            table
        )

        summary_y = (
            self.add_summary(
                table_bottom
            )
        )

        self.add_footer(
            summary_y
        )
