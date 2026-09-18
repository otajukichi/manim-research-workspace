from math import sqrt

from manim import *


# ============================================================
# 0. A4 portrait
# ============================================================
config.pixel_width = 1400
config.pixel_height = int(1400 * sqrt(2))
config.frame_width = 8.27
config.frame_height = 11.69
config.background_color = WHITE


# ============================================================
# 1. 教材内容
#
# 基本的にはここを書き換えれば、内容だけ差し替えられる。
# ============================================================
CONTENT = {
    "header": {
        "title": "中2数学 テスト前まとめ③",
        "subtitle": "一次関数 / 変化の割合",
    },

    # --------------------------------------------------------
    # SECTION 1
    # 一次関数の見極め方
    # --------------------------------------------------------
    "linear_function": {
        "title": "1. 一次関数の見極め方",

        # 一次関数の基本形
        "standard_form": r"y=ax+b",

        # 見極め用の3例
        "examples": [
            {
                "mark": "○",
                "equation": r"y=2x-4",
                "note": "一次関数",
                "kind": "ok",
            },
            {
                "mark": "×",
                "equation": r"y=\frac{2}{x}",
                "note": "x が分母にある",
                "kind": "ng",
            },
            {
                "mark": "×",
                "equation": r"y=x^2+1",
                "note": "x に 2 乗以上がある",
                "kind": "ng",
            },
        ],

        # 最小限の確認ポイント
        "check_points": [
            "x が分母にない",
            "x に 2 乗以上の指数がついていない",
        ],
    },

    # --------------------------------------------------------
    # SECTION 2
    # 変化の割合
    # --------------------------------------------------------
    "rate_of_change": {
        "title": "2. 変化の割合",

        # y = ax + b の a が変化の割合
        "coefficient_message": "変化の割合 = x の係数",

        # 増加量との接続に使う例
        # 値を変えれば、下の表と計算は自動で変わる。
        "example": {
            "a": 3,
            "b": 2,
            "x_start": 1,
            "x_end": 5,
        },

        # 増加量の一般式
        "fraction_numerator": "y の増加量",
        "fraction_denominator": "x の増加量",
    },
}


# ============================================================
# 2. 見た目
#
# これまでの2枚と同じ印刷向けの配色を使う。
# ============================================================
STYLE = {
    "font": "Noto Sans JP",

    # 基本文字
    "text": "#1F2937",

    # 補足文字
    "muted": "#334155",

    # 枠線
    "line": "#94A3B8",

    # セクション見出し背景
    "panel": "#E2E8F0",

    # 基本の青
    "blue": "#2563EB",
    "blue_light": "#DCEAFE",

    # 変化の割合・正解強調
    "green": "#15803D",
    "green_light": "#DCFCE7",

    # 注意・NG
    "red": "#B91C1C",
    "red_light": "#FEE2E2",

    # 補助色
    "orange": "#D97706",
    "orange_light": "#FFEDD5",

    # 表
    "table_header": "#E2E8F0",
}


# ============================================================
# 3. ページ全体のレイアウト
#
# section*_top:
#   セクション上端のY座標。
#
# section*_height:
#   セクション全体の高さ。
#
# 3枚目は内容が少ないため、余白を広めに取っている。
# ============================================================
LAYOUT = {
    "page_width": 7.55,

    "title_y": 5.38,
    "subtitle_y": 4.98,

    "section1_top": 4.62,
    "section1_height": 3.25,

    "section2_top": 1.12,
    "section2_height": 6.40,

    "panel_header_height": 0.55,
}


# ============================================================
# 4. SECTION 1 の調整パラメータ
#
# standard_box_*:
#   y = ax + b を表示する上段カード。
#
# example_box_*:
#   ○×の3例を並べるカード。
#
# check_box_*:
#   「分母」「指数」の2条件を表示するカード。
# ============================================================
LINEAR_LAYOUT = {
    "content_width": 6.85,

    "standard_box_height": 0.72,
    "standard_formula_font_size": 31,

    "example_gap": 0.16,
    "example_box_width": 2.17,
    "example_box_height": 1.05,
    "example_formula_font_size": 24,
    "example_note_font_size": 13,

    "check_gap": 0.18,
    "check_box_width": 3.33,
    "check_box_height": 0.62,
    "check_font_size": 14,

    "content_gap": 0.16,
}


# ============================================================
# 5. SECTION 2 の調整パラメータ
#
# coefficient_box_*:
#   「変化の割合 = x の係数」を表示するカード。
#
# example_equation_font_size:
#   y = 3x + 2 などの例の大きさ。
#
# table_*:
#   x, y の「はじめ・おわり・増加量」を示す表。
#
# rate_box_*:
#   増加量の式と最終結果を表示するカード。
# ============================================================
RATE_LAYOUT = {
    "content_width": 6.85,

    "coefficient_box_height": 0.72,
    "coefficient_font_size": 22,

    "example_equation_font_size": 31,
    "coefficient_label_font_size": 15,

    "table_width": 6.20,
    "table_row_height": 0.56,
    "table_font_size": 15,

    "rate_box_height": 1.18,
    "rate_label_font_size": 16,
    "fraction_font_size": 15,
    "calculation_font_size": 27,

    "content_gap": 0.18,
}


Text.set_default(
    font=STYLE["font"],
    color=STYLE["text"],
)

MathTex.set_default(
    color=STYLE["text"],
)

Tex.set_default(
    color=STYLE["text"],
)


class MidtermReviewPage3(Scene):

    # ========================================================
    # 共通
    # ========================================================

    def fit_to_box(
        self,
        mob,
        max_width,
        max_height,
    ):
        """縦横比を保ったまま指定領域内に収める。"""

        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)

        if mob.height > max_height:
            mob.scale_to_fit_height(max_height)

        return mob


    def make_panel(
        self,
        title,
        top_y,
        height,
    ):
        """これまでの資料と同じセクション枠。"""

        box = RoundedRectangle(
            width=LAYOUT["page_width"],
            height=height,
            corner_radius=0.11,
            stroke_color=STYLE["line"],
            stroke_width=1.3,
            fill_color=WHITE,
            fill_opacity=1,
        )

        box.move_to(
            [
                0,
                top_y - height / 2,
                0,
            ]
        )

        header_h = LAYOUT["panel_header_height"]

        header = RoundedRectangle(
            width=LAYOUT["page_width"],
            height=header_h,
            corner_radius=0.11,
            stroke_width=0,
            fill_color=STYLE["panel"],
            fill_opacity=1,
        )

        header.move_to(
            [
                0,
                top_y - header_h / 2,
                0,
            ]
        )

        title_mob = Text(
            title,
            font_size=23,
            weight=BOLD,
        )

        self.fit_to_box(
            title_mob,
            LAYOUT["page_width"] - 0.45,
            header_h - 0.12,
        )

        title_mob.move_to(
            header.get_center()
        )

        title_mob.align_to(
            box,
            LEFT,
        )

        title_mob.shift(
            RIGHT * 0.22
        )

        return VGroup(
            box,
            header,
            title_mob,
        )


    def panel_content_center(
        self,
        panel,
        pad=0.16,
    ):
        """見出しを除いた本文領域の中心と高さを返す。"""

        box = panel[0]
        header_h = LAYOUT["panel_header_height"]

        top = (
            box.get_top()[1]
            - header_h
            - pad
        )

        bottom = (
            box.get_bottom()[1]
            + pad
        )

        center = np.array(
            [
                0,
                (top + bottom) / 2,
                0,
            ]
        )

        return center, top - bottom


    def make_text_fraction(
        self,
        numerator,
        denominator,
        font_size,
        color=None,
    ):
        """
        日本語を含む分数を Text + Line で描く。
        MathTex に日本語を入れないための共通部品。
        """

        if color is None:
            color = STYLE["text"]

        numerator_mob = Text(
            numerator,
            font_size=font_size,
            weight=BOLD,
            color=color,
        )

        denominator_mob = Text(
            denominator,
            font_size=font_size,
            weight=BOLD,
            color=color,
        )

        width = max(
            numerator_mob.width,
            denominator_mob.width,
        ) + 0.20

        line = Line(
            LEFT * width / 2,
            RIGHT * width / 2,
            stroke_color=color,
            stroke_width=2.0,
        )

        numerator_mob.next_to(
            line,
            UP,
            buff=0.055,
        )

        denominator_mob.next_to(
            line,
            DOWN,
            buff=0.055,
        )

        return VGroup(
            numerator_mob,
            line,
            denominator_mob,
        )


    # ========================================================
    # SECTION 1
    # 一次関数の見極め方
    # ========================================================

    def make_standard_form_box(self):
        """y = ax + b の基本形。"""

        box = RoundedRectangle(
            width=LINEAR_LAYOUT["content_width"],
            height=LINEAR_LAYOUT["standard_box_height"],
            corner_radius=0.08,
            stroke_color=STYLE["blue"],
            stroke_width=1.4,
            fill_color=STYLE["blue_light"],
            fill_opacity=1,
        )

        formula = MathTex(
            CONTENT["linear_function"]["standard_form"],
            font_size=LINEAR_LAYOUT["standard_formula_font_size"],
        )

        formula.move_to(
            box
        )

        return VGroup(
            box,
            formula,
        )


    def make_example_box(
        self,
        item,
    ):
        """一次関数かどうかを見る例。"""

        is_ok = item["kind"] == "ok"

        color = (
            STYLE["green"]
            if is_ok
            else STYLE["red"]
        )

        light_color = (
            STYLE["green_light"]
            if is_ok
            else STYLE["red_light"]
        )

        box = RoundedRectangle(
            width=LINEAR_LAYOUT["example_box_width"],
            height=LINEAR_LAYOUT["example_box_height"],
            corner_radius=0.08,
            stroke_color=color,
            stroke_width=1.3,
            fill_color=light_color,
            fill_opacity=1,
        )

        mark = Text(
            item["mark"],
            font_size=20,
            weight=BOLD,
            color=color,
        )

        equation = MathTex(
            item["equation"],
            font_size=LINEAR_LAYOUT["example_formula_font_size"],
        )

        note = Text(
            item["note"],
            font_size=LINEAR_LAYOUT["example_note_font_size"],
            weight=BOLD,
            color=color,
        )

        content = VGroup(
            mark,
            equation,
            note,
        ).arrange(
            DOWN,
            buff=0.07,
        )

        self.fit_to_box(
            content,
            LINEAR_LAYOUT["example_box_width"] - 0.24,
            LINEAR_LAYOUT["example_box_height"] - 0.15,
        )

        content.move_to(
            box
        )

        return VGroup(
            box,
            content,
        )


    def make_check_box(
        self,
        text_value,
    ):
        """一次関数の見極め条件。"""

        box = RoundedRectangle(
            width=LINEAR_LAYOUT["check_box_width"],
            height=LINEAR_LAYOUT["check_box_height"],
            corner_radius=0.07,
            stroke_color=STYLE["blue"],
            stroke_width=1.1,
            fill_color=STYLE["blue_light"],
            fill_opacity=1,
        )

        check = Text(
            "✓",
            font_size=17,
            weight=BOLD,
            color=STYLE["blue"],
        )

        text = Text(
            text_value,
            font_size=LINEAR_LAYOUT["check_font_size"],
            weight=BOLD,
            color=STYLE["text"],
        )

        content = VGroup(
            check,
            text,
        ).arrange(
            RIGHT,
            buff=0.12,
        )

        self.fit_to_box(
            content,
            LINEAR_LAYOUT["check_box_width"] - 0.28,
            LINEAR_LAYOUT["check_box_height"] - 0.16,
        )

        content.move_to(
            box
        )

        return VGroup(
            box,
            content,
        )


    def make_linear_content(
        self,
        panel,
    ):
        """SECTION 1 全体。"""

        data = CONTENT["linear_function"]

        standard = self.make_standard_form_box()

        example_row = VGroup(
            *[
                self.make_example_box(item)
                for item in data["examples"]
            ]
        ).arrange(
            RIGHT,
            buff=LINEAR_LAYOUT["example_gap"],
        )

        check_row = VGroup(
            *[
                self.make_check_box(text_value)
                for text_value in data["check_points"]
            ]
        ).arrange(
            RIGHT,
            buff=LINEAR_LAYOUT["check_gap"],
        )

        content = VGroup(
            standard,
            example_row,
            check_row,
        ).arrange(
            DOWN,
            buff=LINEAR_LAYOUT["content_gap"],
        )

        center, inner_h = self.panel_content_center(
            panel
        )

        self.fit_to_box(
            content,
            7.00,
            inner_h,
        )

        content.move_to(
            center
        )

        return content


    # ========================================================
    # SECTION 2
    # 変化の割合
    # ========================================================

    def example_values(self):
        """CONTENT の a, b, x から例題の値を計算する。"""

        data = CONTENT["rate_of_change"]["example"]

        a = data["a"]
        b = data["b"]
        x_start = data["x_start"]
        x_end = data["x_end"]

        y_start = a * x_start + b
        y_end = a * x_end + b

        dx = x_end - x_start
        dy = y_end - y_start

        return {
            "a": a,
            "b": b,
            "x_start": x_start,
            "x_end": x_end,
            "y_start": y_start,
            "y_end": y_end,
            "dx": dx,
            "dy": dy,
        }


    def make_coefficient_box(self):
        """変化の割合 = x の係数。"""

        box = RoundedRectangle(
            width=RATE_LAYOUT["content_width"],
            height=RATE_LAYOUT["coefficient_box_height"],
            corner_radius=0.08,
            stroke_color=STYLE["green"],
            stroke_width=1.4,
            fill_color=STYLE["green_light"],
            fill_opacity=1,
        )

        text = Text(
            CONTENT["rate_of_change"]["coefficient_message"],
            font_size=RATE_LAYOUT["coefficient_font_size"],
            weight=BOLD,
            color=STYLE["green"],
        )

        self.fit_to_box(
            text,
            RATE_LAYOUT["content_width"] - 0.40,
            RATE_LAYOUT["coefficient_box_height"] - 0.18,
        )

        text.move_to(
            box
        )

        return VGroup(
            box,
            text,
        )


    def make_example_equation(self):
        """
        y = 3x + 2 の 3 だけ色を変え、
        x の係数が変化の割合だと視覚的に示す。
        """

        values = self.example_values()

        a = values["a"]
        b = values["b"]

        # b の符号を崩さず表示する。
        if b >= 0:
            b_tex = f"+{b}"
        else:
            b_tex = str(b)

        equation = MathTex(
            "y",
            "=",
            str(a),
            "x",
            b_tex,
            font_size=RATE_LAYOUT["example_equation_font_size"],
        )

        equation[2].set_color(
            STYLE["green"]
        )

        label = Text(
            "x の係数",
            font_size=RATE_LAYOUT["coefficient_label_font_size"],
            weight=BOLD,
            color=STYLE["green"],
        )

        arrow = Arrow(
            label.get_top(),
            equation[2].get_bottom(),
            buff=0.05,
            stroke_color=STYLE["green"],
            stroke_width=3,
            max_tip_length_to_length_ratio=0.22,
        )

        group = VGroup(
            equation,
            label,
            arrow,
        )

        label.next_to(
            equation,
            DOWN,
            buff=0.28,
        )

        arrow.put_start_and_end_on(
            label.get_top(),
            equation[2].get_bottom() + DOWN * 0.02,
        )

        return group


    def make_increment_table(self):
        """x, y の増加量を表で確認する。"""

        values = self.example_values()

        data = [
            ["", "はじめ", "おわり", "増加量"],
            [
                "x",
                str(values["x_start"]),
                str(values["x_end"]),
                f"+{values['dx']}",
            ],
            [
                "y",
                str(values["y_start"]),
                str(values["y_end"]),
                f"+{values['dy']}",
            ],
        ]

        table_width = RATE_LAYOUT["table_width"]
        row_h = RATE_LAYOUT["table_row_height"]

        col_widths = [
            table_width * 0.18,
            table_width * 0.25,
            table_width * 0.25,
            table_width * 0.32,
        ]

        table = VGroup()

        for r, row_values in enumerate(data):

            row = VGroup()

            for c, value in enumerate(row_values):

                is_header = (r == 0)
                is_row_header = (c == 0 and r > 0)

                fill = (
                    STYLE["table_header"]
                    if is_header or is_row_header
                    else WHITE
                )

                cell = Rectangle(
                    width=col_widths[c],
                    height=row_h,
                    stroke_color=STYLE["line"],
                    stroke_width=1,
                    fill_color=fill,
                    fill_opacity=1,
                )

                color = STYLE["text"]

                if c == 3 and r > 0:
                    color = STYLE["green"]

                label = Text(
                    value,
                    font_size=RATE_LAYOUT["table_font_size"],
                    weight=(
                        BOLD
                        if is_header or is_row_header or c == 3
                        else NORMAL
                    ),
                    color=color,
                )

                self.fit_to_box(
                    label,
                    col_widths[c] - 0.15,
                    row_h - 0.12,
                )

                label.move_to(
                    cell
                )

                row.add(
                    VGroup(
                        cell,
                        label,
                    )
                )

            row.arrange(
                RIGHT,
                buff=0,
            )

            table.add(
                row
            )

        table.arrange(
            DOWN,
            buff=0,
        )

        return table


    def make_rate_box(self):
        """
        変化の割合
        = y の増加量 / x の増加量
        = 12 / 4
        = 3
        を1つのカードで示す。
        """

        values = self.example_values()

        box = RoundedRectangle(
            width=RATE_LAYOUT["content_width"],
            height=RATE_LAYOUT["rate_box_height"],
            corner_radius=0.08,
            stroke_color=STYLE["blue"],
            stroke_width=1.3,
            fill_color=STYLE["blue_light"],
            fill_opacity=1,
        )

        label = Text(
            "変化の割合",
            font_size=RATE_LAYOUT["rate_label_font_size"],
            weight=BOLD,
            color=STYLE["blue"],
        )

        equal1 = MathTex(
            "=",
            font_size=24,
        )

        general_fraction = self.make_text_fraction(
            CONTENT["rate_of_change"]["fraction_numerator"],
            CONTENT["rate_of_change"]["fraction_denominator"],
            font_size=RATE_LAYOUT["fraction_font_size"],
        )

        equal2 = MathTex(
            "=",
            font_size=24,
        )

        calculation = MathTex(
            rf"\frac{{{values['dy']}}}{{{values['dx']}}}"
            rf"={values['a']}",
            font_size=RATE_LAYOUT["calculation_font_size"],
            color=STYLE["green"],
        )

        row = VGroup(
            label,
            equal1,
            general_fraction,
            equal2,
            calculation,
        ).arrange(
            RIGHT,
            buff=0.14,
        )

        self.fit_to_box(
            row,
            RATE_LAYOUT["content_width"] - 0.40,
            RATE_LAYOUT["rate_box_height"] - 0.18,
        )

        row.move_to(
            box
        )

        return VGroup(
            box,
            row,
        )


    def make_rate_content(
        self,
        panel,
    ):
        """SECTION 2 全体。"""

        coefficient_box = self.make_coefficient_box()

        equation = self.make_example_equation()

        table = self.make_increment_table()

        rate_box = self.make_rate_box()

        content = VGroup(
            coefficient_box,
            equation,
            table,
            rate_box,
        ).arrange(
            DOWN,
            buff=RATE_LAYOUT["content_gap"],
        )

        center, inner_h = self.panel_content_center(
            panel
        )

        self.fit_to_box(
            content,
            7.00,
            inner_h,
        )

        content.move_to(
            center
        )

        return content


    # ========================================================
    # Main
    # ========================================================

    def construct(self):

        # ----------------------------------------------------
        # ヘッダー
        # ----------------------------------------------------

        title = Text(
            CONTENT["header"]["title"],
            font_size=29,
            weight=BOLD,
        )

        self.fit_to_box(
            title,
            7.10,
            0.45,
        )

        title.move_to(
            [
                0,
                LAYOUT["title_y"],
                0,
            ]
        )

        subtitle = Text(
            CONTENT["header"]["subtitle"],
            font_size=16,
            color=STYLE["muted"],
        )

        subtitle.move_to(
            [
                0,
                LAYOUT["subtitle_y"],
                0,
            ]
        )


        # ----------------------------------------------------
        # SECTION 1
        # ----------------------------------------------------

        panel1 = self.make_panel(
            CONTENT["linear_function"]["title"],
            LAYOUT["section1_top"],
            LAYOUT["section1_height"],
        )

        content1 = self.make_linear_content(
            panel1
        )


        # ----------------------------------------------------
        # SECTION 2
        # ----------------------------------------------------

        panel2 = self.make_panel(
            CONTENT["rate_of_change"]["title"],
            LAYOUT["section2_top"],
            LAYOUT["section2_height"],
        )

        content2 = self.make_rate_content(
            panel2
        )


        self.add(
            title,
            subtitle,

            panel1,
            content1,

            panel2,
            content2,
        )
