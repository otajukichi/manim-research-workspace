"""A4縦・年少さん向け
どうぶつを数えて、ぜんぶの数を考えるプリント。

表示する内容は外部JSONから読み込む。

1プレートに入る動物は最大6体。
配置ルール:
    1体 -> 1
    2体 -> 2
    3体 -> 3
    4体 -> 2 + 2
    5体 -> 3 + 2
    6体 -> 3 + 3
"""

import json
from pathlib import Path

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circle,
    Ellipse,
    Line,
    Polygon,
    RoundedRectangle,
    Text,
    VGroup,
    config,
)

from manim_research import EducationScene


# ============================================================
# 用紙
# ============================================================

A4_WIDTH = 21.0
A4_HEIGHT = 29.7

PIXEL_WIDTH = 2480
PIXEL_HEIGHT = 3508


# ============================================================
# 外部データ
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
JSON_DIR = BASE_DIR / "json"

CONTENT_FILE_NAME = "animal_counting_02.json"  # 使用する問題JSONを切り替える
CONTENT_FILE = JSON_DIR / CONTENT_FILE_NAME
OUTPUT_FILE_PREFIX = "animal_counting"


# ============================================================
# タイトル周辺
# ============================================================

TITLE_FONT_SIZE = 70                  # 「どうぶつを かぞえよう」
TITLE_TOP_BUFF = 1.0                  # 用紙上端からタイトルまで

SUBTITLE_FONT_SIZE = 35               # タイトル下の説明文
SUBTITLE_LINE_SPACING = 0.30
SUBTITLE_BUFF = 0.30                  # タイトルと説明文の間隔


# ============================================================
# 問題全体の配置
# ============================================================

ROW_COUNT = 4

PROBLEMS_CENTER_Y = 0.75              # 4問全体の上下位置
ROW_BUFF = 0.42                       # 問題同士の縦間隔


# ============================================================
# 問題番号
# ============================================================

NUMBER_BADGE_RADIUS = 0.56
NUMBER_FONT_SIZE = 32


# ============================================================
# 動物プレート
# ============================================================

GROUP_BOX_WIDTH = 5.25
GROUP_BOX_HEIGHT = 3.50

GROUP_BOX_CORNER_RADIUS = 0.25
GROUP_BOX_STROKE_WIDTH = 2.8

GROUP_BOX_FILL_OPACITY = 0.92


# ============================================================
# ＋ と ＝
# ============================================================

SYMBOL_FONT_SIZE = 54


# ============================================================
# 答えを書く枠
# ============================================================

ANSWER_BOX_WIDTH = 2.75
ANSWER_BOX_HEIGHT = 2.35

ANSWER_BOX_CORNER_RADIUS = 0.20
ANSWER_BOX_STROKE_WIDTH = 3.0

ANSWER_HINT_FONT_SIZE = 19


# ============================================================
# 1問の横方向の間隔
# ============================================================

ROW_ITEM_BUFF = 0.28


# ============================================================
# 動物アイコン配置
# ============================================================

MAX_ANIMALS_PER_GROUP = 6             # 1つのプレートに置ける最大数

ICON_HORIZONTAL_GAP = 0.32            # 動物同士の横間隔
ICON_VERTICAL_GAP = 0.32              # 1段目と2段目の間隔

ICON_AREA_HORIZONTAL_MARGIN = 0.55    # プレート内の左右余白
ICON_AREA_VERTICAL_MARGIN = 0.42      # プレート内の上下余白

ICON_SCALE_FACTOR = 1.00              # 配置後のグループ全体倍率


# ============================================================
# 動物アイコンそのもの
# ============================================================

ANIMAL_FACE_SCALE = 1.18
ANIMAL_OUTLINE_STROKE = 2.8

RABBIT_FILL = "#F7F2FF"
BEAR_FILL = "#D8A36D"
CHICK_FILL = "#FFE066"

EAR_INNER_FILL = "#FFD7E6"
CHICK_BEAK_FILL = "#F4A259"

EYE_RADIUS = 0.032


# ============================================================
# 下部説明枠
# ============================================================

INSTRUCTION_BOX_WIDTH = 18.0
INSTRUCTION_BOX_HEIGHT = 3.35

INSTRUCTION_BOX_CORNER_RADIUS = 0.30
INSTRUCTION_BOX_STROKE_WIDTH = 2.8

INSTRUCTION_CENTER_Y = -11.05

INSTRUCTION_TITLE_FONT_SIZE = 33
INSTRUCTION_FONT_SIZE = 28

INSTRUCTION_LINE_SPACING = 0.32
INSTRUCTION_INTERNAL_BUFF = 0.20


# ============================================================
# 内部設定
# ============================================================

OUTPUT_FILE_NAME = f"{OUTPUT_FILE_PREFIX}_{CONTENT_FILE.stem}"

config.frame_width = A4_WIDTH
config.frame_height = A4_HEIGHT

config.pixel_width = PIXEL_WIDTH
config.pixel_height = PIXEL_HEIGHT

config.output_file = OUTPUT_FILE_NAME


# ============================================================
# データ読み込み
# ============================================================

def load_content() -> dict:
    """外部JSONから教材内容を読み込む。"""

    if not CONTENT_FILE.exists():
        raise FileNotFoundError(
            f"教材データが見つかりません:\n{CONTENT_FILE}"
        )

    with CONTENT_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    required_keys = [
        "title",
        "subtitle",
        "instruction_title",
        "instruction_text",
        "problems",
    ]

    for key in required_keys:
        if key not in data:
            raise ValueError(
                f"JSONに必要なキーがありません: {key}"
            )

    problems = data["problems"]

    if not isinstance(problems, list):
        raise ValueError(
            "problems は配列にしてください。"
        )

    if len(problems) != ROW_COUNT:
        raise ValueError(
            f"problems は {ROW_COUNT} 問にしてください。"
            f" 現在: {len(problems)} 問"
        )

    for index, problem in enumerate(problems):
        for key in [
            "animal",
            "left_count",
            "right_count",
        ]:
            if key not in problem:
                raise ValueError(
                    f"{index + 1}問目に必要なキーがありません: {key}"
                )

        if problem["animal"] not in {
            "rabbit",
            "bear",
            "chick",
        }:
            raise ValueError(
                f"{index + 1}問目の animal は "
                "rabbit / bear / chick のいずれかにしてください。"
            )

        for count_name in [
            "left_count",
            "right_count",
        ]:
            count = problem[count_name]

            if not isinstance(count, int):
                raise ValueError(
                    f"{index + 1}問目の {count_name} は"
                    "整数にしてください。"
                )

            if count < 0:
                raise ValueError(
                    f"{index + 1}問目の {count_name} は"
                    "0以上にしてください。"
                )

            if count > MAX_ANIMALS_PER_GROUP:
                raise ValueError(
                    f"{index + 1}問目の {count_name} が"
                    f"{MAX_ANIMALS_PER_GROUP} を超えています。"
                    "\n1プレートに置ける動物は最大6体です。"
                )

    return data


# ============================================================
# 共通パーツ
# ============================================================

def make_eye(theme) -> Circle:
    """動物用の目。"""

    return Circle(
        radius=EYE_RADIUS,
        stroke_width=0,
        fill_color=theme.foreground,
        fill_opacity=1.0,
    )


# ============================================================
# うさぎ
# ============================================================

def make_rabbit_icon(theme) -> VGroup:
    """うさぎアイコン。"""

    head = Circle(
        radius=0.42,
        color=theme.foreground,
        stroke_width=ANIMAL_OUTLINE_STROKE,
        fill_color=RABBIT_FILL,
        fill_opacity=1.0,
    )

    left_ear = Ellipse(
        width=0.22,
        height=0.54,
        color=theme.foreground,
        stroke_width=ANIMAL_OUTLINE_STROKE,
        fill_color=RABBIT_FILL,
        fill_opacity=1.0,
    )

    right_ear = left_ear.copy()

    left_ear.move_to(
        head.get_center()
        + LEFT * 0.16
        + UP * 0.54
    )

    right_ear.move_to(
        head.get_center()
        + RIGHT * 0.16
        + UP * 0.54
    )

    left_inner = Ellipse(
        width=0.10,
        height=0.34,
        stroke_width=0,
        fill_color=EAR_INNER_FILL,
        fill_opacity=1.0,
    )

    right_inner = left_inner.copy()

    left_inner.move_to(
        left_ear.get_center()
    )

    right_inner.move_to(
        right_ear.get_center()
    )

    left_eye = make_eye(theme)
    right_eye = make_eye(theme)

    left_eye.move_to(
        head.get_center()
        + LEFT * 0.12
        + UP * 0.04
    )

    right_eye.move_to(
        head.get_center()
        + RIGHT * 0.12
        + UP * 0.04
    )

    nose = Circle(
        radius=0.03,
        stroke_width=0,
        fill_color="#F08AA6",
        fill_opacity=1.0,
    )

    nose.move_to(
        head.get_center()
        + DOWN * 0.06
    )

    mouth_left = Line(
        nose.get_center()
        + DOWN * 0.03,

        nose.get_center()
        + LEFT * 0.06
        + DOWN * 0.09,

        color=theme.foreground,
        stroke_width=1.8,
    )

    mouth_right = Line(
        nose.get_center()
        + DOWN * 0.03,

        nose.get_center()
        + RIGHT * 0.06
        + DOWN * 0.09,

        color=theme.foreground,
        stroke_width=1.8,
    )

    icon = VGroup(
        left_ear,
        right_ear,
        left_inner,
        right_inner,
        head,
        left_eye,
        right_eye,
        nose,
        mouth_left,
        mouth_right,
    )

    icon.scale(
        ANIMAL_FACE_SCALE
    )

    return icon


# ============================================================
# くま
# ============================================================

def make_bear_icon(theme) -> VGroup:
    """くまアイコン。"""

    head = Circle(
        radius=0.42,
        color=theme.foreground,
        stroke_width=ANIMAL_OUTLINE_STROKE,
        fill_color=BEAR_FILL,
        fill_opacity=1.0,
    )

    left_ear = Circle(
        radius=0.15,
        color=theme.foreground,
        stroke_width=ANIMAL_OUTLINE_STROKE,
        fill_color=BEAR_FILL,
        fill_opacity=1.0,
    )

    right_ear = left_ear.copy()

    left_ear.move_to(
        head.get_center()
        + LEFT * 0.26
        + UP * 0.28
    )

    right_ear.move_to(
        head.get_center()
        + RIGHT * 0.26
        + UP * 0.28
    )

    snout = Ellipse(
        width=0.30,
        height=0.22,
        color=theme.foreground,
        stroke_width=1.8,
        fill_color="#F6DFC8",
        fill_opacity=1.0,
    )

    snout.move_to(
        head.get_center()
        + DOWN * 0.08
    )

    left_eye = make_eye(theme)
    right_eye = make_eye(theme)

    left_eye.move_to(
        head.get_center()
        + LEFT * 0.12
        + UP * 0.04
    )

    right_eye.move_to(
        head.get_center()
        + RIGHT * 0.12
        + UP * 0.04
    )

    nose = Circle(
        radius=0.03,
        stroke_width=0,
        fill_color=theme.foreground,
        fill_opacity=1.0,
    )

    nose.move_to(
        snout.get_center()
        + UP * 0.01
    )

    mouth = Line(
        snout.get_center()
        + DOWN * 0.02,

        snout.get_center()
        + DOWN * 0.08,

        color=theme.foreground,
        stroke_width=1.7,
    )

    icon = VGroup(
        left_ear,
        right_ear,
        head,
        snout,
        left_eye,
        right_eye,
        nose,
        mouth,
    )

    icon.scale(
        ANIMAL_FACE_SCALE
    )

    return icon


# ============================================================
# ひよこ
# ============================================================

def make_chick_icon(theme) -> VGroup:
    """ひよこアイコン。"""

    head = Circle(
        radius=0.42,
        color=theme.foreground,
        stroke_width=ANIMAL_OUTLINE_STROKE,
        fill_color=CHICK_FILL,
        fill_opacity=1.0,
    )

    left_eye = make_eye(theme)
    right_eye = make_eye(theme)

    left_eye.move_to(
        head.get_center()
        + LEFT * 0.12
        + UP * 0.05
    )

    right_eye.move_to(
        head.get_center()
        + RIGHT * 0.12
        + UP * 0.05
    )

    beak = Polygon(
        head.get_center()
        + DOWN * 0.02
        + LEFT * 0.06,

        head.get_center()
        + DOWN * 0.02
        + RIGHT * 0.06,

        head.get_center()
        + DOWN * 0.11,

        color=theme.foreground,
        stroke_width=1.8,
        fill_color=CHICK_BEAK_FILL,
        fill_opacity=1.0,
    )

    icon = VGroup(
        head,
        left_eye,
        right_eye,
        beak,
    )

    icon.scale(
        ANIMAL_FACE_SCALE
    )

    return icon


# ============================================================
# 動物選択
# ============================================================

def make_animal_icon(
    animal: str,
    theme,
) -> VGroup:
    """指定された種類の動物を作る。"""

    if animal == "rabbit":
        return make_rabbit_icon(theme)

    if animal == "bear":
        return make_bear_icon(theme)

    if animal == "chick":
        return make_chick_icon(theme)

    raise ValueError(
        f"未対応の動物です: {animal}"
    )


# ============================================================
# 1段分の動物を作る
# ============================================================

def make_icon_row(
    animal: str,
    count: int,
    theme,
) -> VGroup:
    """1〜3体を横一列に並べる。"""

    if not 1 <= count <= 3:
        raise ValueError(
            "make_icon_row の count は1〜3にしてください。"
        )

    row = VGroup(
        *[
            make_animal_icon(
                animal,
                theme,
            )
            for _ in range(count)
        ]
    )

    row.arrange(
        RIGHT,
        buff=ICON_HORIZONTAL_GAP,
    )

    return row


# ============================================================
# プレート内の動物配置
# ============================================================

def make_animal_group(
    animal: str,
    count: int,
    theme,
) -> VGroup:
    """0〜6体の動物を、最大3列×2段で配置する。

    配置:
        1 -> 1
        2 -> 2
        3 -> 3
        4 -> 2 + 2
        5 -> 3 + 2
        6 -> 3 + 3

    各段は中央揃えにする。
    """

    if count < 0:
        raise ValueError(
            "動物の数は0以上にしてください。"
        )

    if count > MAX_ANIMALS_PER_GROUP:
        raise ValueError(
            f"動物は1プレート最大"
            f"{MAX_ANIMALS_PER_GROUP}体です。"
        )

    # --------------------------------------------------------
    # 0体
    # --------------------------------------------------------

    if count == 0:
        empty_text = Text(
            "0",
            font=theme.sans_font,
            font_size=52,
            weight="BOLD",
            color=theme.muted,
        )

        return VGroup(
            empty_text
        )

    # --------------------------------------------------------
    # 何体ずつ各段に置くか
    # --------------------------------------------------------

    if count <= 3:
        row_counts = [count]

    elif count == 4:
        row_counts = [2, 2]

    elif count == 5:
        row_counts = [3, 2]

    else:
        # count == 6
        row_counts = [3, 3]

    # --------------------------------------------------------
    # 各段を作る
    # --------------------------------------------------------

    rows = VGroup()

    for row_count in row_counts:
        icon_row = make_icon_row(
            animal,
            row_count,
            theme,
        )

        rows.add(
            icon_row
        )

    # --------------------------------------------------------
    # 2段の場合は上下に配置
    # --------------------------------------------------------

    if len(rows) == 2:
        rows.arrange(
            DOWN,
            buff=ICON_VERTICAL_GAP,
        )

    # --------------------------------------------------------
    # プレートからはみ出さないための安全処理
    # --------------------------------------------------------

    max_width = (
        GROUP_BOX_WIDTH
        - ICON_AREA_HORIZONTAL_MARGIN
    )

    max_height = (
        GROUP_BOX_HEIGHT
        - ICON_AREA_VERTICAL_MARGIN
    )

    if rows.width > max_width:
        rows.scale_to_fit_width(
            max_width
        )

    if rows.height > max_height:
        rows.scale_to_fit_height(
            max_height
        )

    rows.scale(
        ICON_SCALE_FACTOR
    )

    return rows


# ============================================================
# 1問ぶん
# ============================================================

def make_problem_row(
    scene: EducationScene,
    index: int,
    animal: str,
    left_count: int,
    right_count: int,
) -> VGroup:
    """数かぞえ問題1問を作る。"""

    theme = scene.theme

    # --------------------------------------------------------
    # 問題番号
    # --------------------------------------------------------

    badge = Circle(
        radius=NUMBER_BADGE_RADIUS,
        color=theme.accent,
        stroke_width=2.8,
        fill_color=theme.accent_fill,
        fill_opacity=1.0,
    )

    badge_text = Text(
        str(index),
        font=theme.sans_font,
        font_size=NUMBER_FONT_SIZE,
        weight="BOLD",
        color=theme.foreground,
    )

    badge_text.move_to(
        badge
    )

    badge_group = VGroup(
        badge,
        badge_text,
    )

    # --------------------------------------------------------
    # 左グループ
    # --------------------------------------------------------

    left_box = RoundedRectangle(
        width=GROUP_BOX_WIDTH,
        height=GROUP_BOX_HEIGHT,
        corner_radius=GROUP_BOX_CORNER_RADIUS,
        color=theme.secondary,
        stroke_width=GROUP_BOX_STROKE_WIDTH,
        fill_color=theme.surface,
        fill_opacity=GROUP_BOX_FILL_OPACITY,
    )

    left_icons = make_animal_group(
        animal,
        left_count,
        theme,
    )

    left_icons.move_to(
        left_box
    )

    left_group = VGroup(
        left_box,
        left_icons,
    )

    # --------------------------------------------------------
    # ＋
    # --------------------------------------------------------

    plus_text = Text(
        "+",
        font=theme.sans_font,
        font_size=SYMBOL_FONT_SIZE,
        weight="BOLD",
        color=theme.accent,
    )

    # --------------------------------------------------------
    # 右グループ
    # --------------------------------------------------------

    right_box = RoundedRectangle(
        width=GROUP_BOX_WIDTH,
        height=GROUP_BOX_HEIGHT,
        corner_radius=GROUP_BOX_CORNER_RADIUS,
        color=theme.secondary,
        stroke_width=GROUP_BOX_STROKE_WIDTH,
        fill_color=theme.surface,
        fill_opacity=GROUP_BOX_FILL_OPACITY,
    )

    right_icons = make_animal_group(
        animal,
        right_count,
        theme,
    )

    right_icons.move_to(
        right_box
    )

    right_group = VGroup(
        right_box,
        right_icons,
    )

    # --------------------------------------------------------
    # ＝
    # --------------------------------------------------------

    equal_text = Text(
        "=",
        font=theme.sans_font,
        font_size=SYMBOL_FONT_SIZE,
        weight="BOLD",
        color=theme.secondary,
    )

    # --------------------------------------------------------
    # 答え欄
    # --------------------------------------------------------

    answer_box = RoundedRectangle(
        width=ANSWER_BOX_WIDTH,
        height=ANSWER_BOX_HEIGHT,
        corner_radius=ANSWER_BOX_CORNER_RADIUS,
        color=theme.warning,
        stroke_width=ANSWER_BOX_STROKE_WIDTH,
        fill_color=theme.background,
        fill_opacity=1.0,
    )

    answer_hint = scene.jp_text(
        "こたえ",
        font_size=ANSWER_HINT_FONT_SIZE,
        color=theme.muted,
        weight="BOLD",
    )

    answer_hint.next_to(
        answer_box,
        UP,
        buff=0.07,
    )

    answer_group = VGroup(
        answer_box,
        answer_hint,
    )

    # --------------------------------------------------------
    # 横に並べる
    # --------------------------------------------------------

    row = VGroup(
        badge_group,
        left_group,
        plus_text,
        right_group,
        equal_text,
        answer_group,
    )

    row.arrange(
        RIGHT,
        buff=ROW_ITEM_BUFF,
    )

    return row


# ============================================================
# Scene
# ============================================================

class AnimalCountingAdditionWorksheet(EducationScene):
    """年少向け・動物を使った数かぞえプリント。"""

    def construct(self) -> None:
        content = load_content()

        theme = self.theme

        # ----------------------------------------------------
        # タイトル
        # ----------------------------------------------------

        title = self.title_text(
            content["title"],
            font_size=TITLE_FONT_SIZE,
            color=theme.accent,
        )

        title.to_edge(
            UP,
            buff=TITLE_TOP_BUFF,
        )

        # ----------------------------------------------------
        # 説明文
        # ----------------------------------------------------

        subtitle = self.jp_text(
            content["subtitle"],
            font_size=SUBTITLE_FONT_SIZE,
            color=theme.foreground,
            weight="BOLD",
            line_spacing=SUBTITLE_LINE_SPACING,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=SUBTITLE_BUFF,
        )

        # ----------------------------------------------------
        # 問題
        # ----------------------------------------------------

        problem_rows = VGroup()

        for index, problem in enumerate(
            content["problems"],
            start=1,
        ):
            row = make_problem_row(
                self,
                index=index,
                animal=problem["animal"],
                left_count=problem["left_count"],
                right_count=problem["right_count"],
            )

            problem_rows.add(
                row
            )

        problem_rows.arrange(
            DOWN,
            buff=ROW_BUFF,
        )

        problem_rows.move_to(
            [
                0,
                PROBLEMS_CENTER_Y,
                0,
            ]
        )

        # ----------------------------------------------------
        # 下部説明枠
        # ----------------------------------------------------

        instruction_box = RoundedRectangle(
            width=INSTRUCTION_BOX_WIDTH,
            height=INSTRUCTION_BOX_HEIGHT,
            corner_radius=INSTRUCTION_BOX_CORNER_RADIUS,
            color=theme.accent,
            stroke_width=INSTRUCTION_BOX_STROKE_WIDTH,
            fill_color=theme.background,
            fill_opacity=1.0,
        )

        instruction_box.move_to(
            [
                0,
                INSTRUCTION_CENTER_Y,
                0,
            ]
        )

        instruction_title = self.jp_text(
            content["instruction_title"],
            font_size=INSTRUCTION_TITLE_FONT_SIZE,
            color=theme.accent,
            weight="BOLD",
        )

        instruction_text = self.jp_text(
            content["instruction_text"],
            font_size=INSTRUCTION_FONT_SIZE,
            color=theme.foreground,
            weight="BOLD",
            line_spacing=INSTRUCTION_LINE_SPACING,
        )

        instruction_group = VGroup(
            instruction_title,
            instruction_text,
        )

        instruction_group.arrange(
            DOWN,
            buff=INSTRUCTION_INTERNAL_BUFF,
        )

        max_instruction_width = (
            INSTRUCTION_BOX_WIDTH
            - 1.0
        )

        if instruction_group.width > max_instruction_width:
            instruction_group.scale_to_fit_width(
                max_instruction_width
            )

        instruction_group.move_to(
            instruction_box
        )

        # ----------------------------------------------------
        # 描画
        # ----------------------------------------------------

        self.add(
            title,
            subtitle,
            problem_rows,
            instruction_box,
            instruction_group,
        )
