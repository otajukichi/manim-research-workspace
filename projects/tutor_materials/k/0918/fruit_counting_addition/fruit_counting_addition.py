"""A4縦・くだものを数えて足し算するプリント。

表示内容は外部JSONから読み込む。
画像素材は ../figures/food/ 以下のPNGを使用する。

1プレートに入るくだものは最大6個。

配置:
    1 -> 1
    2 -> 2
    3 -> 3
    4 -> 2 + 2
    5 -> 3 + 2
    6 -> 3 + 3

問題JSONは --content-file で実行時に切り替えられる。
"""

import json
import os
from pathlib import Path

from manim import (
    DOWN,
    RIGHT,
    UP,
    Circle,
    Group,
    ImageMobject,
    RoundedRectangle,
    Text,
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

# 0918/figures/food/
FOOD_FIGURES_DIR = BASE_DIR.parent / "figures" / "food"

DEFAULT_CONTENT_FILE_NAME = "fruit_counting_01.json"

OUTPUT_FILE_PREFIX = "fruit_counting"


def resolve_content_file() -> Path:
    """--content-file で指定されたJSONを解決する。"""

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


# ============================================================
# タイトル周辺
# ============================================================

TITLE_FONT_SIZE = 70
TITLE_TOP_BUFF = 1.0

SUBTITLE_FONT_SIZE = 44
SUBTITLE_LINE_SPACING = 0.30
SUBTITLE_BUFF = 0.30


# ============================================================
# 問題全体
# ============================================================

ROW_COUNT = 4

PROBLEMS_CENTER_Y = 0.75
ROW_BUFF = 0.42


# ============================================================
# 問題番号
# ============================================================

NUMBER_BADGE_RADIUS = 0.56
NUMBER_FONT_SIZE = 32


# ============================================================
# くだものプレート
# ============================================================

GROUP_BOX_WIDTH = 5.25
GROUP_BOX_HEIGHT = 3.50

GROUP_BOX_CORNER_RADIUS = 0.25
GROUP_BOX_STROKE_WIDTH = 2.8
GROUP_BOX_FILL_OPACITY = 0.92


# ============================================================
# ＋ / ＝
# ============================================================

SYMBOL_FONT_SIZE = 54


# ============================================================
# 答え欄
# ============================================================

ANSWER_BOX_WIDTH = 2.75
ANSWER_BOX_HEIGHT = 2.35

ANSWER_BOX_CORNER_RADIUS = 0.20
ANSWER_BOX_STROKE_WIDTH = 3.0

ANSWER_HINT_FONT_SIZE = 19


# ============================================================
# 横方向の間隔
# ============================================================

ROW_ITEM_BUFF = 0.28


# ============================================================
# くだもの画像の配置
# ============================================================

MAX_FRUITS_PER_GROUP = 6

ICON_HORIZONTAL_GAP = 0.25
ICON_VERTICAL_GAP = 0.22

ICON_AREA_HORIZONTAL_MARGIN = 0.55
ICON_AREA_VERTICAL_MARGIN = 0.42

# 画像1個の最大サイズ
FRUIT_ICON_MAX_WIDTH = 1.32
FRUIT_ICON_MAX_HEIGHT = 1.32

ICON_SCALE_FACTOR = 1.0


# ============================================================
# 下部説明枠
# ============================================================

INSTRUCTION_BOX_WIDTH = 18.0
INSTRUCTION_BOX_HEIGHT = 3.35

INSTRUCTION_BOX_CORNER_RADIUS = 0.30
INSTRUCTION_BOX_STROKE_WIDTH = 2.8

INSTRUCTION_CENTER_Y = -11.05

INSTRUCTION_TITLE_FONT_SIZE = 50
INSTRUCTION_FONT_SIZE = 38

INSTRUCTION_LINE_SPACING = 0.32
INSTRUCTION_INTERNAL_BUFF = 0.20


# ============================================================
# Manim設定
# ============================================================

OUTPUT_FILE_NAME = (
    f"{OUTPUT_FILE_PREFIX}_{CONTENT_FILE.stem}"
)

config.frame_width = A4_WIDTH
config.frame_height = A4_HEIGHT

config.pixel_width = PIXEL_WIDTH
config.pixel_height = PIXEL_HEIGHT

config.output_file = OUTPUT_FILE_NAME


# ============================================================
# 画像
# ============================================================

def get_fruit_path(fruit: str) -> Path:
    """JSONで指定されたフルーツPNGを探す。"""

    path = FOOD_FIGURES_DIR / fruit

    if not path.is_file():
        raise FileNotFoundError(
            f"くだもの画像が見つかりません: {fruit}\n"
            f"{path}"
        )

    return path


def make_fruit_icon(
    fruit: str,
) -> ImageMobject:
    """くだものPNGを1個作る。"""

    path = get_fruit_path(fruit)

    icon = ImageMobject(
        str(path)
    )

    if icon.width <= 0 or icon.height <= 0:
        raise ValueError(
            f"PNG画像を表示できません: {path}"
        )

    icon.scale(
        min(
            FRUIT_ICON_MAX_WIDTH / icon.width,
            FRUIT_ICON_MAX_HEIGHT / icon.height,
        )
    )

    return icon


# ============================================================
# JSON読み込み
# ============================================================

def load_content() -> dict:
    """外部JSONから教材内容を読み込む。"""

    if not CONTENT_FILE.is_file():
        raise FileNotFoundError(
            f"教材データが見つかりません:\n"
            f"{CONTENT_FILE}"
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

    if not isinstance(
        problems,
        list,
    ):
        raise ValueError(
            "problems は配列にしてください。"
        )

    if len(problems) != ROW_COUNT:
        raise ValueError(
            f"problems は {ROW_COUNT} 問にしてください。"
            f" 現在: {len(problems)} 問"
        )

    for index, problem in enumerate(
        problems,
        start=1,
    ):
        for key in (
            "fruit",
            "left_count",
            "right_count",
        ):
            if key not in problem:
                raise ValueError(
                    f"{index}問目に必要なキーがありません: "
                    f"{key}"
                )

        fruit = problem["fruit"]

        if (
            not isinstance(fruit, str)
            or not fruit.strip()
        ):
            raise ValueError(
                f"{index}問目の fruit は"
                "空ではない文字列にしてください。"
            )

        get_fruit_path(fruit)

        for count_name in (
            "left_count",
            "right_count",
        ):
            count = problem[count_name]

            if not isinstance(
                count,
                int,
            ):
                raise ValueError(
                    f"{index}問目の {count_name} は"
                    "整数にしてください。"
                )

            if count < 0:
                raise ValueError(
                    f"{index}問目の {count_name} は"
                    "0以上にしてください。"
                )

            if count > MAX_FRUITS_PER_GROUP:
                raise ValueError(
                    f"{index}問目の {count_name} が"
                    f"{MAX_FRUITS_PER_GROUP} を超えています。\n"
                    "1プレートに置けるくだものは最大6個です。"
                )

    return data


# ============================================================
# 1段分
# ============================================================

def make_icon_row(
    fruit: str,
    count: int,
) -> Group:
    """1〜3個を横一列に並べる。"""

    if not 1 <= count <= 3:
        raise ValueError(
            "make_icon_row の count は"
            "1〜3にしてください。"
        )

    row = Group(
        *(
            make_fruit_icon(
                fruit
            )
            for _ in range(count)
        )
    )

    row.arrange(
        RIGHT,
        buff=ICON_HORIZONTAL_GAP,
    )

    return row


# ============================================================
# プレート内配置
# ============================================================

def make_fruit_group(
    fruit: str,
    count: int,
    theme,
) -> Group:
    """0〜6個のくだものを最大3列×2段で配置する。"""

    if count < 0:
        raise ValueError(
            "くだものの数は0以上にしてください。"
        )

    if count > MAX_FRUITS_PER_GROUP:
        raise ValueError(
            f"くだものは1プレート最大"
            f"{MAX_FRUITS_PER_GROUP}個です。"
        )

    # 0個
    if count == 0:
        empty_text = Text(
            "0",
            font=theme.sans_font,
            font_size=52,
            weight="BOLD",
            color=theme.muted,
        )

        return Group(
            empty_text
        )

    # 各段の個数
    if count <= 3:
        row_counts = [count]

    elif count == 4:
        row_counts = [2, 2]

    elif count == 5:
        row_counts = [3, 2]

    else:
        row_counts = [3, 3]

    rows = Group()

    for row_count in row_counts:
        rows.add(
            make_icon_row(
                fruit,
                row_count,
            )
        )

    if len(rows) == 2:
        rows.arrange(
            DOWN,
            buff=ICON_VERTICAL_GAP,
        )

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
# 1問
# ============================================================

def make_problem_row(
    scene: EducationScene,
    index: int,
    fruit: str,
    left_count: int,
    right_count: int,
) -> Group:
    """くだもの足し算問題を1問作る。"""

    theme = scene.theme

    # 問題番号
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

    badge_group = Group(
        badge,
        badge_text,
    )

    # 左プレート
    left_box = RoundedRectangle(
        width=GROUP_BOX_WIDTH,
        height=GROUP_BOX_HEIGHT,
        corner_radius=GROUP_BOX_CORNER_RADIUS,
        color=theme.secondary,
        stroke_width=GROUP_BOX_STROKE_WIDTH,
        fill_color=theme.surface,
        fill_opacity=GROUP_BOX_FILL_OPACITY,
    )

    left_icons = make_fruit_group(
        fruit,
        left_count,
        theme,
    )

    left_icons.move_to(
        left_box
    )

    left_group = Group(
        left_box,
        left_icons,
    )

    # +
    plus_text = Text(
        "+",
        font=theme.sans_font,
        font_size=SYMBOL_FONT_SIZE,
        weight="BOLD",
        color=theme.accent,
    )

    # 右プレート
    right_box = RoundedRectangle(
        width=GROUP_BOX_WIDTH,
        height=GROUP_BOX_HEIGHT,
        corner_radius=GROUP_BOX_CORNER_RADIUS,
        color=theme.secondary,
        stroke_width=GROUP_BOX_STROKE_WIDTH,
        fill_color=theme.surface,
        fill_opacity=GROUP_BOX_FILL_OPACITY,
    )

    right_icons = make_fruit_group(
        fruit,
        right_count,
        theme,
    )

    right_icons.move_to(
        right_box
    )

    right_group = Group(
        right_box,
        right_icons,
    )

    # =
    equal_text = Text(
        "=",
        font=theme.sans_font,
        font_size=SYMBOL_FONT_SIZE,
        weight="BOLD",
        color=theme.secondary,
    )

    # 答え欄
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

    answer_group = Group(
        answer_box,
        answer_hint,
    )

    row = Group(
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

class FruitCountingAdditionWorksheet(
    EducationScene
):
    """くだものを使った数かぞえ・足し算プリント。"""

    def construct(self) -> None:
        content = load_content()
        theme = self.theme

        # タイトル
        title = self.title_text(
            content["title"],
            font_size=TITLE_FONT_SIZE,
            color=theme.accent,
        )

        title.to_edge(
            UP,
            buff=TITLE_TOP_BUFF,
        )

        # 説明
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

        # 4問
        problem_rows = Group()

        for index, problem in enumerate(
            content["problems"],
            start=1,
        ):
            problem_rows.add(
                make_problem_row(
                    self,
                    index=index,
                    fruit=problem["fruit"],
                    left_count=problem["left_count"],
                    right_count=problem["right_count"],
                )
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

        # 下部説明枠
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

        instruction_group = Group(
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

        if (
            instruction_group.width
            > max_instruction_width
        ):
            instruction_group.scale_to_fit_width(
                max_instruction_width
            )

        instruction_group.move_to(
            instruction_box
        )

        self.add(
            title,
            subtitle,
            problem_rows,
            instruction_box,
            instruction_group,
        )
