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
        "title": "中2数学 テスト前まとめ②",
        "subtitle": "道のり・速さ・時間 / 連立方程式の作り方",
    },

    # --------------------------------------------------------
    # SECTION 1
    # 道のり・速さ・時間
    # --------------------------------------------------------
    "relation": {
        "title": "1. 道のり・速さ・時間の関係",

        # 日本語を MathTex に直接入れないため、
        # 表示要素を分けて持つ。
        "main_formula": {
            "left": "道のり",
            "right_1": "速さ",
            "right_2": "時間",
        },

        "derived": [
            {
                "label": "時間を求める",
                "left": "時間",
                "numerator": "道のり",
                "denominator": "速さ",
            },
            {
                "label": "速さを求める",
                "left": "速さ",
                "numerator": "道のり",
                "denominator": "時間",
            },
        ],

        "example": {
            "distance": "120 km",
            "speed": "40 km/h",
            "time": "3 時間",
        },

        "key_point": "文章題では、まず「何を道のり・速さ・時間として見るか」を整理する。",
    },

    # --------------------------------------------------------
    # SECTION 2
    # 連立方程式の作り方
    # --------------------------------------------------------
    "system": {
        "title": "2. 文章題から連立方程式を作る",

        "problem": (
            "A→B を時速40km、B→C を時速50kmで進み、"
            "A→C は全部で92km、かかった時間は2時間。"
        ),

        "variables": {
            "left": "A→B の道のりを x km",
            "right": "B→C の道のりを y km",
        },

        "variable_check": "x と y を「道のり」と「時間」のどちらとしておくか考える",

        # 表の内容
        "table": {
            "columns": ["", "A→B", "B→C", "合計"],
            "rows": [
                ["道のり", "x", "y", "92"],
                ["速さ", "40", "50", ""],
                ["時間", "x/40", "y/50", "2"],
            ],
        },

        # 2本の式
        "equations": [
            {
                "label": "道のりの式",
                "equation": r"x+y=92",
                "note": "道のりの合計が 92 km",
                "color": "blue",
            },
            {
                "label": "時間の式",
                "equation": r"\frac{x}{40}+\frac{y}{50}=2",
                "note": "時間の合計が 2 時間",
                "color": "orange",
            },
        ],

        "key_point": "「道のりの合計」と「時間の合計」の2本で連立方程式を作る。",
    },
}


# ============================================================
# 2. 見た目
#
# 印刷で薄くなりすぎない配色にしている。
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

    # 道のり
    "blue": "#2563EB",
    "blue_light": "#DCEAFE",

    # 時間
    "orange": "#D97706",
    "orange_light": "#FFEDD5",

    # 速さ
    # 既存の青・オレンジ・緑と被らないように紫系を使う。
    "purple": "#7C3AED",
    "purple_light": "#EDE9FE",

    # 強調
    "green": "#15803D",
    "green_light": "#DCFCE7",

    # 表
    "table_header": "#E2E8F0",
    "table_row": "#F8FAFC",
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
# 数字を変えることで、上下の占有割合を人の手で調整できる。
# ============================================================
LAYOUT = {
    "page_width": 7.55,

    "title_y": 5.38,
    "subtitle_y": 4.98,

    # Section 1 は情報量が少ないのでコンパクトにする。
    "section1_top": 4.62,
    "section1_height": 2.65,

    # Section 1 で空いた高さを、そのまま Section 2 に渡す。
    # 下端は従来とほぼ同じ位置に保つ。
    "section2_top": 1.72,
    "section2_height": 7.04,

    "panel_header_height": 0.55,
}


# ============================================================
# 4. SECTION 1 の調整パラメータ
#
# relation_formula_font_size:
#   「道のり = 速さ × 時間」の大きさ。
#
# derived_box_width / height:
#   「時間を求める」「速さを求める」カードの大きさ。
#
# example_bar_width:
#   120km の例を示す横棒の長さ。
#
# example_bar_y:
#   例の横棒の上下位置。
# ============================================================
RELATION_LAYOUT = {
    # Section 1 の共通横幅。
    # 上の主公式と中央の2カード列の左右端をそろえる。
    "content_width": 6.80,

    # 主公式の箱の高さ。
    "main_box_height": 0.66,

    # 「道のり」「速さ」「時間」の文字サイズ。
    # Section 1 全体を少しだけ小さくする。
    "relation_formula_font_size": 22,

    # 下段2つの式カードのすき間
    "derived_gap": 0.20,

    # 下段2つの式カード。
    # 2枚 + derived_gap の合計が content_width になる。
    "derived_box_width": 3.30,
    "derived_box_height": 0.90,

    # 下段2つの式の文字サイズ。
    # 上段の用語サイズとそろえる。
    "derived_formula_font_size": 22,

    # 主公式と下段カードの縦方向のすき間
    "content_gap": 0.14,
}


# ============================================================
# 5. SECTION 2 の調整パラメータ
#
# problem_font_size:
#   問題文の文字サイズ。
#
# variable_box_width:
#   x, y の定義カードの横幅。
#
# table_width:
#   表全体の横幅。
#
# table_row_height:
#   表1行の高さ。
#
# equation_box_width:
#   「道のりの式」「時間の式」のカード幅。
#
# equation_font_size:
#   連立方程式の数式サイズ。
# ============================================================
SYSTEM_LAYOUT = {
    # 問題文。1行に収まる範囲で少し大きくする。
    "problem_font_size": 16,

    # 問題文の直後に入れる緑枠
    "variable_check_box_width": 6.85,
    "variable_check_box_height": 0.60,
    "variable_check_font_size": 15,

    # x, y の定義カード
    "variable_box_width": 3.25,
    "variable_box_height": 0.62,
    "variable_font_size": 16,

    # 表
    "table_width": 6.75,
    "table_row_height": 0.56,
    "table_font_size": 15,
    "table_fraction_font_size": 24,

    # 道のりの式 / 時間の式
    "equation_box_width": 3.25,
    "equation_box_height": 1.24,
    "equation_label_font_size": 17,
    "equation_font_size": 28,
    "equation_note_font_size": 13,

    # 最下部のまとめ
    "key_box_width": 6.85,
    "key_box_height": 0.62,
    "key_font_size": 15,

    # Section 2 内の各要素の縦方向のすき間
    "content_gap": 0.14,
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


class MidtermReviewPage2(Scene):

    # ========================================================
    # 共通
    # ========================================================

    def fit_to_box(
        self,
        mob,
        max_width,
        max_height,
    ):
        """縦横比を保ったまま指定サイズ内に収める。"""

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
        """セクション共通の外枠と見出し。"""

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
        pad=0.14,
    ):
        """
        パネル見出しを除いた本文領域の
        中心座標と高さを返す。
        """

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


    # ========================================================
    # SECTION 1
    # 道のり・速さ・時間
    # ========================================================

    def make_mixed_main_formula(self, data):
        """
        「道のり = 速さ × 時間」を、
        日本語は Text、数学記号は MathTex で描画する。

        通常の MathTex に日本語を直接渡すと
        LaTeX の Unicode エラーになるため、このように分離する。
        """

        word_style = {
            "font_size": RELATION_LAYOUT["relation_formula_font_size"],
            "weight": BOLD,
            "color": STYLE["text"],
        }

        # 「=」「×」も同じ見え方になるよう、
        # 用語と同じサイズを使う。
        symbol_size = RELATION_LAYOUT["relation_formula_font_size"]

        left = Text(
            data["left"],
            **word_style,
        )

        equal = MathTex(
            "=",
            font_size=symbol_size,
            color=STYLE["text"],
        )

        right_1 = Text(
            data["right_1"],
            **word_style,
        )

        multiply = MathTex(
            r"\times",
            font_size=symbol_size,
            color=STYLE["text"],
        )

        right_2 = Text(
            data["right_2"],
            **word_style,
        )

        return VGroup(
            left,
            equal,
            right_1,
            multiply,
            right_2,
        ).arrange(
            RIGHT,
            buff=0.11,
        )


    def make_text_fraction(
        self,
        numerator,
        denominator,
        font_size=20,
        color=None,
    ):
        """
        日本語の分数を LaTeX に渡さず描くための部品。

            道のり
            ───
             速さ

        のように Text + Line で作る。
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

        fraction_width = max(
            numerator_mob.width,
            denominator_mob.width,
        ) + 0.18

        fraction_line = Line(
            LEFT * fraction_width / 2,
            RIGHT * fraction_width / 2,
            stroke_color=color,
            stroke_width=2.0,
        )

        numerator_mob.next_to(
            fraction_line,
            UP,
            buff=0.055,
        )

        denominator_mob.next_to(
            fraction_line,
            DOWN,
            buff=0.055,
        )

        return VGroup(
            numerator_mob,
            fraction_line,
            denominator_mob,
        )


    def make_derived_formula(self, item):
        """
        「時間 = 道のり / 速さ」のような式を
        Text + MathTex("=") + 手描き分数で作る。
        """

        left = Text(
            item["left"],
            font_size=RELATION_LAYOUT["derived_formula_font_size"],
            weight=BOLD,
            color=STYLE["text"],
        )

        equal = MathTex(
            "=",
            font_size=RELATION_LAYOUT["derived_formula_font_size"] + 1,
            color=STYLE["text"],
        )

        fraction = self.make_text_fraction(
            numerator=item["numerator"],
            denominator=item["denominator"],
            font_size=RELATION_LAYOUT["derived_formula_font_size"],
            color=STYLE["text"],
        )

        formula = VGroup(
            left,
            equal,
            fraction,
        ).arrange(
            RIGHT,
            buff=0.12,
        )

        return formula


    def make_main_formula(self):
        """道のり = 速さ × 時間 の主公式。"""

        data = CONTENT["relation"]

        box = RoundedRectangle(
            width=RELATION_LAYOUT["content_width"],
            height=RELATION_LAYOUT["main_box_height"],
            corner_radius=0.08,
            stroke_color=STYLE["blue"],
            stroke_width=1.4,
            fill_color=STYLE["blue_light"],
            fill_opacity=1,
        )

        formula = self.make_mixed_main_formula(
            data["main_formula"]
        )

        self.fit_to_box(
            formula,
            RELATION_LAYOUT["content_width"] - 0.50,
            RELATION_LAYOUT["main_box_height"] - 0.18,
        )

        formula.move_to(
            box
        )

        return VGroup(
            box,
            formula,
        )


    def make_derived_formula_box(
        self,
        item,
        color,
        light_color,
    ):
        """時間・速さを求める変形式カード。"""

        box = RoundedRectangle(
            width=RELATION_LAYOUT["derived_box_width"],
            height=RELATION_LAYOUT["derived_box_height"],
            corner_radius=0.08,
            stroke_color=color,
            stroke_width=1.2,
            fill_color=light_color,
            fill_opacity=1,
        )

        formula = self.make_derived_formula(
            item
        )

        self.fit_to_box(
            formula,
            RELATION_LAYOUT["derived_box_width"] - 0.28,
            RELATION_LAYOUT["derived_box_height"] - 0.14,
        )

        formula.move_to(
            box
        )

        return VGroup(
            box,
            formula,
        )


    def make_distance_example(self):
        """
        120km を時速40kmで進むと3時間、
        という関係を簡単な線分図で示す。
        """

        data = CONTENT["relation"]["example"]

        bar_width = RELATION_LAYOUT["example_bar_width"]

        line = Line(
            LEFT * bar_width / 2,
            RIGHT * bar_width / 2,
            stroke_color=STYLE["text"],
            stroke_width=3,
        )

        left_tick = Line(
            line.get_left() + DOWN * 0.10,
            line.get_left() + UP * 0.10,
            stroke_color=STYLE["text"],
            stroke_width=2,
        )

        right_tick = Line(
            line.get_right() + DOWN * 0.10,
            line.get_right() + UP * 0.10,
            stroke_color=STYLE["text"],
            stroke_width=2,
        )

        distance = Text(
            data["distance"],
            font_size=16,
            weight=BOLD,
            color=STYLE["blue"],
        )
        distance.next_to(
            line,
            UP,
            buff=0.08,
        )

        speed = Text(
            f"速さ：{data['speed']}",
            font_size=14,
            color=STYLE["muted"],
        )

        time = Text(
            f"時間：{data['time']}",
            font_size=14,
            color=STYLE["muted"],
        )

        labels = VGroup(
            speed,
            time,
        ).arrange(
            RIGHT,
            buff=0.55,
        )

        labels.next_to(
            line,
            DOWN,
            buff=0.12,
        )

        group = VGroup(
            line,
            left_tick,
            right_tick,
            distance,
            labels,
        )

        group.shift(
            UP * RELATION_LAYOUT["example_bar_y"]
        )

        return group


    def make_relation_key_box(self):
        """SECTION 1 最後の確認文。"""

        box = RoundedRectangle(
            width=RELATION_LAYOUT["content_width"],
            height=RELATION_LAYOUT["key_box_height"],
            corner_radius=0.07,
            stroke_color=STYLE["green"],
            stroke_width=1.1,
            fill_color=STYLE["green_light"],
            fill_opacity=1,
        )

        text = Text(
            CONTENT["relation"]["key_point"],
            font_size=14,
            weight=BOLD,
            color=STYLE["green"],
        )

        self.fit_to_box(
            text,
            RELATION_LAYOUT["content_width"] - 0.35,
            RELATION_LAYOUT["key_box_height"] - 0.20,
        )

        text.move_to(
            box
        )

        return VGroup(
            box,
            text,
        )


    def make_relation_content(
        self,
        panel,
    ):
        """SECTION 1 全体。"""

        data = CONTENT["relation"]

        main_formula = self.make_main_formula()

        derived_left = self.make_derived_formula_box(
            data["derived"][0],
            STYLE["orange"],
            STYLE["orange_light"],
        )

        derived_right = self.make_derived_formula_box(
            data["derived"][1],
            STYLE["purple"],
            STYLE["purple_light"],
        )

        derived_row = VGroup(
            derived_left,
            derived_right,
        ).arrange(
            RIGHT,
            buff=RELATION_LAYOUT["derived_gap"],
        )

        content = VGroup(
            main_formula,
            derived_row,
        ).arrange(
            DOWN,
            buff=RELATION_LAYOUT["content_gap"],
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
    # 文章題 → 連立方程式
    # ========================================================

    def make_problem_text(self):
        """問題文の要約。"""

        text = Text(
            CONTENT["system"]["problem"],
            font_size=SYSTEM_LAYOUT["problem_font_size"],
            color=STYLE["text"],
        )

        self.fit_to_box(
            text,
            6.90,
            0.45,
        )

        return text


    def make_variable_box(
        self,
        text_value,
        color,
        light_color,
    ):
        """x, y の定義カード。"""

        box = RoundedRectangle(
            width=SYSTEM_LAYOUT["variable_box_width"],
            height=SYSTEM_LAYOUT["variable_box_height"],
            corner_radius=0.07,
            stroke_color=color,
            stroke_width=1.2,
            fill_color=light_color,
            fill_opacity=1,
        )

        text = Text(
            text_value,
            font_size=SYSTEM_LAYOUT["variable_font_size"],
            weight=BOLD,
            color=color,
        )

        self.fit_to_box(
            text,
            SYSTEM_LAYOUT["variable_box_width"] - 0.30,
            SYSTEM_LAYOUT["variable_box_height"] - 0.18,
        )

        text.move_to(
            box
        )

        return VGroup(
            box,
            text,
        )


    def make_data_table(self):
        """
        道のり・速さ・時間の表。
        Manim の Table を使わず、印刷調整しやすいよう
        手動でセルを作る。
        """

        data = CONTENT["system"]["table"]

        columns = data["columns"]
        rows = data["rows"]

        table_width = SYSTEM_LAYOUT["table_width"]
        row_h = SYSTEM_LAYOUT["table_row_height"]

        # 4列
        col_widths = [
            table_width * 0.19,
            table_width * 0.25,
            table_width * 0.25,
            table_width * 0.31,
        ]

        all_rows = [
            columns,
            *rows,
        ]

        table_group = VGroup()

        for r, row_values in enumerate(all_rows):
            row_group = VGroup()

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

                # 分数だけ MathTex、それ以外は Text
                if "/" in value and value:
                    numerator, denominator = value.split("/")

                    label = MathTex(
                        rf"\frac{{{numerator}}}{{{denominator}}}",
                        font_size=SYSTEM_LAYOUT["table_fraction_font_size"],
                    )

                else:
                    label = Text(
                        value,
                        font_size=SYSTEM_LAYOUT["table_font_size"],
                        weight=BOLD if is_header or is_row_header else NORMAL,
                    )

                self.fit_to_box(
                    label,
                    col_widths[c] - 0.15,
                    row_h - 0.12,
                )

                label.move_to(
                    cell
                )

                row_group.add(
                    VGroup(
                        cell,
                        label,
                    )
                )

            row_group.arrange(
                RIGHT,
                buff=0,
            )

            table_group.add(
                row_group
            )

        table_group.arrange(
            DOWN,
            buff=0,
        )

        return table_group


    def make_equation_box(
        self,
        item,
    ):
        """道のりの式 / 時間の式カード。"""

        color = STYLE[item["color"]]

        light_color = (
            STYLE["blue_light"]
            if item["color"] == "blue"
            else STYLE["orange_light"]
        )

        box = RoundedRectangle(
            width=SYSTEM_LAYOUT["equation_box_width"],
            height=SYSTEM_LAYOUT["equation_box_height"],
            corner_radius=0.08,
            stroke_color=color,
            stroke_width=1.4,
            fill_color=light_color,
            fill_opacity=1,
        )

        label = Text(
            item["label"],
            font_size=SYSTEM_LAYOUT["equation_label_font_size"],
            weight=BOLD,
            color=color,
        )

        equation = MathTex(
            item["equation"],
            font_size=SYSTEM_LAYOUT["equation_font_size"],
            color=STYLE["text"],
        )

        note = Text(
            item["note"],
            font_size=SYSTEM_LAYOUT["equation_note_font_size"],
            color=STYLE["muted"],
        )

        content = VGroup(
            label,
            equation,
            note,
        ).arrange(
            DOWN,
            buff=0.07,
        )

        self.fit_to_box(
            content,
            SYSTEM_LAYOUT["equation_box_width"] - 0.25,
            SYSTEM_LAYOUT["equation_box_height"] - 0.20,
        )

        content.move_to(
            box
        )

        return VGroup(
            box,
            content,
        )


    def make_system_key_box(self):
        """SECTION 2 最後の確認文。"""

        box = RoundedRectangle(
            width=SYSTEM_LAYOUT["key_box_width"],
            height=SYSTEM_LAYOUT["key_box_height"],
            corner_radius=0.07,
            stroke_color=STYLE["green"],
            stroke_width=1.1,
            fill_color=STYLE["green_light"],
            fill_opacity=1,
        )

        text = Text(
            CONTENT["system"]["key_point"],
            font_size=SYSTEM_LAYOUT["key_font_size"],
            weight=BOLD,
            color=STYLE["green"],
        )

        self.fit_to_box(
            text,
            SYSTEM_LAYOUT["key_box_width"] - 0.35,
            SYSTEM_LAYOUT["key_box_height"] - 0.20,
        )

        text.move_to(
            box
        )

        return VGroup(
            box,
            text,
        )




    def make_variable_check_box(self):
        """問題文の直後に置く確認用の緑枠。"""

        box = RoundedRectangle(
            width=SYSTEM_LAYOUT["variable_check_box_width"],
            height=SYSTEM_LAYOUT["variable_check_box_height"],
            corner_radius=0.07,
            stroke_color=STYLE["green"],
            stroke_width=1.1,
            fill_color=STYLE["green_light"],
            fill_opacity=1,
        )

        text = Text(
            CONTENT["system"]["variable_check"],
            font_size=SYSTEM_LAYOUT["variable_check_font_size"],
            weight=BOLD,
            color=STYLE["green"],
        )

        self.fit_to_box(
            text,
            SYSTEM_LAYOUT["variable_check_box_width"] - 0.35,
            SYSTEM_LAYOUT["variable_check_box_height"] - 0.20,
        )

        text.move_to(
            box
        )

        return VGroup(
            box,
            text,
        )

    def make_system_content(
        self,
        panel,
    ):
        """SECTION 2 全体。"""

        data = CONTENT["system"]

        problem = self.make_problem_text()

        variable_check = self.make_variable_check_box()

        variable_left = self.make_variable_box(
            data["variables"]["left"],
            STYLE["blue"],
            STYLE["blue_light"],
        )

        variable_right = self.make_variable_box(
            data["variables"]["right"],
            STYLE["blue"],
            STYLE["blue_light"],
        )

        variable_row = VGroup(
            variable_left,
            variable_right,
        ).arrange(
            RIGHT,
            buff=0.25,
        )

        table = self.make_data_table()

        equation_left = self.make_equation_box(
            data["equations"][0]
        )

        equation_right = self.make_equation_box(
            data["equations"][1]
        )

        equation_row = VGroup(
            equation_left,
            equation_right,
        ).arrange(
            RIGHT,
            buff=0.25,
        )

        key = self.make_system_key_box()

        content = VGroup(
            problem,
            variable_check,
            variable_row,
            table,
            equation_row,
            key,
        ).arrange(
            DOWN,
            buff=SYSTEM_LAYOUT["content_gap"],
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
            CONTENT["relation"]["title"],
            LAYOUT["section1_top"],
            LAYOUT["section1_height"],
        )

        content1 = self.make_relation_content(
            panel1
        )


        # ----------------------------------------------------
        # SECTION 2
        # ----------------------------------------------------

        panel2 = self.make_panel(
            CONTENT["system"]["title"],
            LAYOUT["section2_top"],
            LAYOUT["section2_height"],
        )

        content2 = self.make_system_content(
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
