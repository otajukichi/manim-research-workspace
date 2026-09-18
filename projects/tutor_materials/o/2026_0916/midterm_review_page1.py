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
# 1. 教材内容：基本的にはここだけ編集
# ============================================================
CONTENT = {
    "header": {
        "title": "中2数学 テスト前まとめ①",
        "subtitle": "連立方程式 / 等式変形",
    },
    "section1": {
        "title": "1. 連立方程式の解き方",
        "steps": [
            ("①", "消す文字を決める", "x か y、消しやすい方を選ぶ"),
            ("②", "係数をそろえる", "必要なら式全体を何倍かする"),
            ("③", "足す・引く", "1文字だけの式にする"),
            ("④", "元の式に代入", "もう1つの文字を求める"),
        ],
        "bridge": [
            "小数・分数でも手順は同じ。",
            "式を何倍かするときは『両辺』を動かす。",
        ],
    },
    "section2": {
        "title": "2. 等式はてんびん",
        "before_caption": "① まずは、つり合っている",
        "addition_caption": "② 左右に同じ量を追加する",
        "after_caption": "③ 追加しても、つり合いは保たれる",
        "equation_before": {
            "left": r"0.3x+1.4y",
            "right": r"-1",
        },
        "equation_after": {
            "left": r"3x+14y",
            "right": r"-10",
        },
        "operation": "両辺を ×10",
        "key_phrase": "同じ操作を両辺にすれば、『＝』は保たれる",
    },
}


# ============================================================
# 2. 見た目
# ============================================================
STYLE = {
    "font": "Noto Sans JP",

    # 基本文字
    "text": "#1F2937",

    # 補足文字：
    # 印刷時に薄くならないよう濃くする
    "muted": "#334155",

    # 枠線：
    # 印刷時に消えにくい濃さへ
    "line": "#94A3B8",

    # セクション見出しの背景
    "panel": "#E2E8F0",

    # 青系
    "blue": "#2563EB",

    # 手順カード背景：
    # 印刷でも見える程度まで濃くする
    "blue_light": "#DCEAFE",

    # オレンジ系
    "orange": "#D97706",
    "orange_light": "#FEF3C7",

    # 緑系
    "green": "#16A34A",
    "green_light": "#DCFCE7",
}


# ============================================================
# 3. レイアウト
# ============================================================
LAYOUT = {
    "page_width": 7.55,
    "title_y": 5.38,
    "subtitle_y": 4.98,
    "section1_top": 4.62,
    "section1_height": 2.72,
    "section2_top": 1.64,
    "section2_height": 6.82,
    "panel_header_height": 0.55,
}


# ============================================================
# 4. 天秤の調整パラメータ
#
# center_axis_length : 天秤中央の縦軸の長さ
#                      大きくすると横棒が上がり、天秤そのものが縦に伸びる。
#
# rope_length        : 横棒から皿までのひもの長さ
#                      大きくすると皿が下がり、ひもが長くなる。
# ============================================================
BALANCE_LAYOUT = {
    "center_axis_length": 1,
    "rope_length": 0.70,

    # 左辺・右辺ラベルの上下位置。
    # 値を大きくすると上へ、小さくすると下へ移動する。
    "left_label_vertical_offset": -0.2,
    "right_label_vertical_offset": -0.2,
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


class MidtermReviewPage1(Scene):

    # ========================================================
    # 共通
    # ========================================================

    def fit_to_box(
        self,
        mob,
        max_width,
        max_height,
    ):
        """
        オブジェクトを縦横比を保ったまま
        必ず指定領域の中へ収める。
        """

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
    ):
        """
        パネルのヘッダーを除いた本文領域を返す。
        """

        box = panel[0]

        header_h = LAYOUT["panel_header_height"]

        top = (
            box.get_top()[1]
            - header_h
            - 0.12
        )

        bottom = (
            box.get_bottom()[1]
            + 0.12
        )

        center = np.array(
            [
                0,
                (top + bottom) / 2,
                0,
            ]
        )

        height = top - bottom

        return center, height


    # ========================================================
    # Section 1
    # ========================================================

    def make_step_row(
        self,
        number,
        title,
        note,
    ):

        row = RoundedRectangle(
            width=6.95,
            height=0.46,
            corner_radius=0.07,
            stroke_color=STYLE["line"],
            stroke_width=1,
            fill_color=STYLE["blue_light"],
            fill_opacity=0.62,
        )


        badge = Circle(
            radius=0.135,
            stroke_width=0,
            fill_color=STYLE["blue"],
            fill_opacity=1,
        )


        badge_text = Text(
            number,
            font_size=14,
            weight=BOLD,
            color=WHITE,
        )

        badge_text.move_to(
            badge
        )


        badge_group = VGroup(
            badge,
            badge_text,
        )

        badge_group.move_to(
            row.get_left()
            + RIGHT * 0.27
        )


        title_mob = Text(
            title,
            font_size=17,
            weight=BOLD,
        )

        title_mob.next_to(
            badge_group,
            RIGHT,
            buff=0.14,
        )


        note_mob = Text(
            note,
            font_size=13,
            color=STYLE["muted"],
        )

        self.fit_to_box(
            note_mob,
            3.30,
            0.30,
        )

        note_mob.align_to(
            row,
            RIGHT,
        )

        note_mob.shift(
            LEFT * 0.20
        )


        return VGroup(
            row,
            badge_group,
            title_mob,
            note_mob,
        )


    def make_section1_content(
        self,
        panel,
    ):

        data = CONTENT["section1"]


        rows = VGroup(
            *[
                self.make_step_row(*step)
                for step
                in data["steps"]
            ]
        )

        rows.arrange(
            DOWN,
            buff=0.075,
        )


        center, inner_h = self.panel_content_center(
            panel
        )

        self.fit_to_box(
            rows,
            7.00,
            inner_h,
        )

        rows.move_to(
            center
        )


        return rows



    # ========================================================
    # 錘
    # ========================================================

    def make_big_weight(
        self,
        added=False,
    ):

        outline = (
            STYLE["green"]
            if added
            else STYLE["blue"]
        )

        stroke_w = (
            3.0
            if added
            else 1.6
        )

        # 錘は完全不透明にする。
        # 背後のひもが錘を透けて見えないようにする。
        opacity = 1.0


        body = RoundedRectangle(
            width=0.62,
            height=0.52,
            corner_radius=0.07,
            stroke_color=outline,
            stroke_width=stroke_w,
            fill_color=STYLE["blue"],
            fill_opacity=opacity,
        )


        mark = Circle(
            radius=0.065,
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=0.95,
        )

        mark.move_to(
            body
        )


        return VGroup(
            body,
            mark,
        )


    def make_small_weight(
        self,
        added=False,
    ):

        outline = (
            STYLE["green"]
            if added
            else STYLE["orange"]
        )

        stroke_w = (
            2.6
            if added
            else 1.2
        )

        # 錘は完全不透明にする。
        # 背後のひもが錘を透けて見えないようにする。
        opacity = 1.0


        return RoundedRectangle(
            width=0.25,
            height=0.23,
            corner_radius=0.035,
            stroke_color=outline,
            stroke_width=stroke_w,
            fill_color=STYLE["orange"],
            fill_opacity=opacity,
        )


    def make_big_weight_group(
        self,
        count,
        added_count=0,
    ):

        normal_count = (
            count - added_count
        )


        items = VGroup()


        for _ in range(normal_count):

            items.add(
                self.make_big_weight(
                    False
                )
            )


        for _ in range(added_count):

            items.add(
                self.make_big_weight(
                    True
                )
            )


        items.arrange(
            RIGHT,
            buff=0.10,
        )


        return items


    def make_small_weight_group(
        self,
        count,
        added_count=0,
    ):

        # ----------------------------------------------------
        # 3個
        # ----------------------------------------------------

        if count <= 3:

            items = VGroup(
                *[
                    self.make_small_weight(
                        i >= count - added_count
                    )
                    for i
                    in range(count)
                ]
            )

            items.arrange(
                RIGHT,
                buff=0.055,
            )

            return items


        # ----------------------------------------------------
        # 6個
        #
        # 上段 = 追加分
        # 下段 = もともとの分
        # ----------------------------------------------------

        base_row = VGroup(
            *[
                self.make_small_weight(
                    False
                )
                for _
                in range(3)
            ]
        )

        base_row.arrange(
            RIGHT,
            buff=0.055,
        )


        add_row = VGroup(
            *[
                self.make_small_weight(
                    True
                )
                for _
                in range(3)
            ]
        )

        add_row.arrange(
            RIGHT,
            buff=0.055,
        )


        return VGroup(
            add_row,
            base_row,
        ).arrange(
            DOWN,
            buff=0.035,
        )


    # ========================================================
    # 天秤
    # ========================================================

    def make_balance(
        self,
        left_big_count,
        right_small_count,
        left_added=0,
        right_added=0,
    ):

        # ----------------------------------------------------
        # 人が調整する天秤パラメータ
        # ----------------------------------------------------
        center_axis_length = BALANCE_LAYOUT["center_axis_length"]
        rope_length = BALANCE_LAYOUT["rope_length"]
        left_label_vertical_offset = BALANCE_LAYOUT["left_label_vertical_offset"]
        right_label_vertical_offset = BALANCE_LAYOUT["right_label_vertical_offset"]

        # ----------------------------------------------------
        # 基準座標
        #
        # 真ん中の縦軸の下端は固定し、
        # center_axis_length を大きくすると横棒だけが上へ伸びる。
        # ----------------------------------------------------
        post_bottom_y = -0.34
        beam_y = post_bottom_y + center_axis_length

        beam_half_width = 2.05
        side_x = 1.40
        pan_half_width = 0.76

        # ひもの長さから皿の高さを決める。
        pan_y = beam_y - rope_length


        beam = Line(
            [-beam_half_width, beam_y, 0],
            [beam_half_width, beam_y, 0],
            stroke_color=STYLE["text"],
            stroke_width=3.2,
        )


        # 真ん中の縦軸
        post = Line(
            [0, beam_y, 0],
            [0, post_bottom_y, 0],
            stroke_color=STYLE["text"],
            stroke_width=3,
        )


        base = Polygon(
            [-0.32, -0.50, 0],
            [0.32, -0.50, 0],
            [0, -0.10, 0],
            stroke_color=STYLE["text"],
            stroke_width=2.3,
            fill_color=WHITE,
            fill_opacity=1,
        )


        left_rope = Line(
            [-side_x, beam_y, 0],
            [-side_x, pan_y, 0],
            stroke_color=STYLE["text"],
            stroke_width=2,
        )


        right_rope = Line(
            [side_x, beam_y, 0],
            [side_x, pan_y, 0],
            stroke_color=STYLE["text"],
            stroke_width=2,
        )


        left_pan = Line(
            [-side_x - pan_half_width, pan_y, 0],
            [-side_x + pan_half_width, pan_y, 0],
            stroke_color=STYLE["text"],
            stroke_width=3,
        )


        right_pan = Line(
            [side_x - pan_half_width, pan_y, 0],
            [side_x + pan_half_width, pan_y, 0],
            stroke_color=STYLE["text"],
            stroke_width=3,
        )


        left_weights = self.make_big_weight_group(
            left_big_count,
            left_added,
        )

        left_weights.next_to(
            left_pan,
            UP,
            buff=0.025,
        )

        left_weights.move_to(
            [
                -side_x,
                left_weights.get_center()[1],
                0,
            ]
        )


        right_weights = self.make_small_weight_group(
            right_small_count,
            right_added,
        )

        right_weights.next_to(
            right_pan,
            UP,
            buff=0.025,
        )

        right_weights.move_to(
            [
                side_x,
                right_weights.get_center()[1],
                0,
            ]
        )


        # 左辺・右辺ラベルは皿の位置を基準にしつつ、
        # BALANCE_LAYOUT から個別に上下調整できる。
        left_label_y = pan_y + left_label_vertical_offset
        right_label_y = pan_y + right_label_vertical_offset

        left_label = Text(
            "左辺",
            font_size=15,
            weight=BOLD,
            color=STYLE["blue"],
        )

        left_label.move_to(
            [
                -side_x,
                left_label_y,
                0,
            ]
        )


        right_label = Text(
            "右辺",
            font_size=15,
            weight=BOLD,
            color=STYLE["orange"],
        )

        right_label.move_to(
            [
                side_x,
                right_label_y,
                0,
            ]
        )


        return VGroup(
            beam,
            post,
            base,
            left_rope,
            right_rope,
            left_pan,
            right_pan,
            left_weights,
            right_weights,
            left_label,
            right_label,
        )


    # ========================================================
    # 追加する錘
    # ========================================================

    def make_added_weights_strip(
        self,
    ):

        left_add = VGroup(

            Text(
                "＋",
                font_size=28,
                weight=BOLD,
                color=STYLE["green"],
            ),

            self.make_big_weight(
                True
            ),

        )

        left_add.arrange(
            RIGHT,
            buff=0.10,
        )


        right_add = VGroup(

            Text(
                "＋",
                font_size=28,
                weight=BOLD,
                color=STYLE["green"],
            ),

            self.make_small_weight_group(
                3,
                added_count=3,
            ),

        )

        right_add.arrange(
            RIGHT,
            buff=0.10,
        )


        center_text = Text(
            CONTENT["section2"]["addition_caption"],
            font_size=16,
            weight=BOLD,
            color=STYLE["text"],
        )


        strip = VGroup(
            left_add,
            center_text,
            right_add,
        )

        strip.arrange(
            RIGHT,
            buff=0.40,
        )


        self.fit_to_box(
            strip,
            6.75,
            0.72,
        )


        return strip


    # ========================================================
    # 数式
    # ========================================================

    def make_equation(
        self,
        left_tex,
        right_tex,
        font_size=22,
    ):

        left = MathTex(
            left_tex,
            font_size=font_size,
            color=STYLE["blue"],
        )


        equal = MathTex(
            "=",
            font_size=font_size,
            color=STYLE["text"],
        )


        right = MathTex(
            right_tex,
            font_size=font_size,
            color=STYLE["orange"],
        )


        return VGroup(
            left,
            equal,
            right,
        ).arrange(
            RIGHT,
            buff=0.10,
        )


    def make_equation_strip(
        self,
    ):

        data = CONTENT["section2"]


        before = self.make_equation(
            data["equation_before"]["left"],
            data["equation_before"]["right"],
        )


        arrow = Arrow(
            LEFT,
            RIGHT,
            buff=0,
            stroke_color=STYLE["green"],
            stroke_width=4,
        )

        arrow.scale(
            0.48
        )


        op_text = Text(
            data["operation"],
            font_size=14,
            weight=BOLD,
            color=STYLE["green"],
        )


        operation = VGroup(
            op_text,
            arrow,
        )

        operation.arrange(
            DOWN,
            buff=0.025,
        )


        after = self.make_equation(
            data["equation_after"]["left"],
            data["equation_after"]["right"],
        )


        flow = VGroup(
            before,
            operation,
            after,
        )

        flow.arrange(
            RIGHT,
            buff=0.25,
        )


        self.fit_to_box(
            flow,
            6.45,
            0.65,
        )


        box = RoundedRectangle(
            width=6.85,
            height=0.78,
            corner_radius=0.07,
            stroke_color=STYLE["line"],
            stroke_width=1.1,
            fill_color=STYLE["panel"],
            fill_opacity=1,
        )


        flow.move_to(
            box
        )


        return VGroup(
            box,
            flow,
        )


    # ========================================================
    # Section 2
    # ========================================================

    def make_section2_content(
        self,
        panel,
    ):

        data = CONTENT["section2"]


        # ----------------------------------------------------
        # 最初の天秤
        # ----------------------------------------------------

        before_caption = Text(
            data["before_caption"],
            font_size=16,
            weight=BOLD,
        )


        before_balance = self.make_balance(
            1,
            3,
        )
        before_balance.scale(1.10)


        before_block = VGroup(
            before_caption,
            before_balance,
        )

        before_block.arrange(
            DOWN,
            buff=0.10,
        )


        # ----------------------------------------------------
        # 追加する錘
        # ----------------------------------------------------

        addition_strip = self.make_added_weights_strip()
        addition_strip.scale(1.05)


        # ----------------------------------------------------
        # 追加後の天秤
        # ----------------------------------------------------

        after_caption = Text(
            data["after_caption"],
            font_size=16,
            weight=BOLD,
            color=STYLE["text"],
        )


        after_balance = self.make_balance(
            2,
            6,
            left_added=1,
            right_added=3,
        )
        after_balance.scale(1.10)


        after_block = VGroup(
            after_caption,
            after_balance,
        )

        after_block.arrange(
            DOWN,
            buff=0.10,
        )


        # ----------------------------------------------------
        # 数式との接続
        # ----------------------------------------------------

        equation_strip = self.make_equation_strip()


        # ----------------------------------------------------
        # 最後の一言
        # ----------------------------------------------------

        key = Text(
            data["key_phrase"],
            font_size=17,
            weight=BOLD,
            color=STYLE["green"],
        )


        self.fit_to_box(
            key,
            6.60,
            0.36,
        )


        # ----------------------------------------------------
        # 下半分全体
        # ----------------------------------------------------

        content = VGroup(
            before_block,
            addition_strip,
            after_block,
            equation_strip,
            key,
        )


        content.arrange(
            DOWN,
            buff=0.18,
        )


        center, inner_h = self.panel_content_center(
            panel
        )


        # ----------------------------------------------------
        # 重要：
        # ここでは高さ方向の自動縮小をしない。
        #
        # rope_length を長くすると content.height は大きくなるが、
        # それをパネル内へ収めるために全体を縮小すると、
        # 錘まで一緒に小さくなってしまう。
        #
        # 横幅だけは必要なら調整する。
        # rope_length は横幅に影響しないため、
        # 糸を長くしても錘の大きさは変わらない。
        # ----------------------------------------------------
        if content.width > 7.00:
            content.scale_to_fit_width(7.00)


        content.move_to(
            center
        )


        return content



    # ========================================================
    # Main
    # ========================================================

    def construct(self):

        # ----------------------------------------------------
        # Header
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
        # Section 1
        # ----------------------------------------------------

        panel1 = self.make_panel(
            CONTENT["section1"]["title"],
            LAYOUT["section1_top"],
            LAYOUT["section1_height"],
        )


        content1 = self.make_section1_content(
            panel1
        )


        # ----------------------------------------------------
        # Section 2
        # ----------------------------------------------------

        panel2 = self.make_panel(
            CONTENT["section2"]["title"],
            LAYOUT["section2_top"],
            LAYOUT["section2_height"],
        )


        content2 = self.make_section2_content(
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