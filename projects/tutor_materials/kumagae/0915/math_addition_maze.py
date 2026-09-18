"""A4縦・小1初級向け「たしざん迷路」プリント。

表示する文章・問題配置は外部JSONから読み込む。

JSONを差し替えることで、
同じデザインの別問題を簡単に作成できる。
"""

import json
from pathlib import Path

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circle,
    Line,
    Rectangle,
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

CONTENT_FILE_PATH = "math_data/addition_maze_10.json"

OUTPUT_FILE_PREFIX = "math"


# ============================================================
# タイトル周辺
# ============================================================

TITLE_FONT_SIZE = 58              # 一番上のタイトル「たしざん たからじま」の文字サイズ
TITLE_TOP_BUFF = 1.5             # タイトルと用紙上端との余白

SUBTITLE_FONT_SIZE = 36           # タイトル下の説明文「『5』になる マスだけを〜」の文字サイズ
SUBTITLE_LINE_SPACING = 0.28      # 説明文が2行以上になったときの行間
SUBTITLE_BUFF = 0.28              # タイトルと説明文の間隔

TARGET_FONT_SIZE = 44             # 「こたえ ＝ 5」の文字サイズ

TARGET_BOX_WIDTH = 5.2            # 「こたえ ＝ 5」を囲む枠の横幅
TARGET_BOX_HEIGHT = 1.15          # 「こたえ ＝ 5」を囲む枠の高さ
TARGET_BOX_CORNER_RADIUS = 0.30   # 「こたえ ＝ 5」の枠の角の丸み
TARGET_BOX_STROKE_WIDTH = 3.0     # 「こたえ ＝ 5」の枠線の太さ

TARGET_BUFF = 0.38                # 説明文と「こたえ ＝ 5」の枠との間隔


# ============================================================
# 迷路
# ============================================================

CELL_SIZE = 2.30

CELL_GAP = 0.10
CELL_CORNER_RADIUS = 0.22

CELL_STROKE_WIDTH = 2.3

CELL_FILL_OPACITY_A = 0.35
CELL_FILL_OPACITY_B = 0.16

PROBLEM_FONT_SIZE = 36

# 数式が長すぎた場合、
# マス幅の何割まで許可するか。
PROBLEM_MAX_WIDTH_RATIO = 0.82

# 迷路上端のY座標。
GRID_TOP_Y = 7.30

GRID_CENTER_X = 0.0


# ============================================================
# スタート・ゴール
# ============================================================

LABEL_FONT_SIZE = 23

START_GOAL_BUFF = 0.32

CONNECTOR_STROKE_WIDTH = 4.0


# ============================================================
# スタート顔
# ============================================================

FACE_RADIUS = 0.52

FACE_EYE_RADIUS = 0.055

FACE_SCALE = 1.0


# ============================================================
# 宝箱
# ============================================================

TREASURE_SCALE = 0.82

TREASURE_BODY_WIDTH = 1.75
TREASURE_BODY_HEIGHT = 0.92

TREASURE_LID_WIDTH = 1.75
TREASURE_LID_HEIGHT = 0.58


# ============================================================
# 下部ミッション
# ============================================================

MISSION_BOX_WIDTH = 15.7              # 下部の「ミッション」全体を囲む枠の横幅
MISSION_BOX_HEIGHT = 2.15             # 下部の「ミッション」全体を囲む枠の高さ

MISSION_BOX_CORNER_RADIUS = 0.30      # ミッション枠の角の丸み
MISSION_BOX_STROKE_WIDTH = 2.8        # ミッション枠の線の太さ

MISSION_BOTTOM_BUFF = 4            # ミッション枠と用紙下端との余白

MISSION_TITLE_FONT_SIZE = 35         # 「★ ミッション ★」の文字サイズ
MISSION_FONT_SIZE = 32                # ミッション本文「まずは ゆびで〜」の文字サイズ

MISSION_LINE_SPACING = 0.5           # ミッション本文が2行以上になったときの行間
MISSION_INTERNAL_BUFF = 0.16          # 「★ ミッション ★」と本文の間隔


# ============================================================
# 内部設定
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CONTENT_FILE = BASE_DIR / CONTENT_FILE_PATH

OUTPUT_FILE_NAME = (
    f"{OUTPUT_FILE_PREFIX}_{CONTENT_FILE.stem}"
)

config.frame_width = A4_WIDTH
config.frame_height = A4_HEIGHT

config.pixel_width = PIXEL_WIDTH
config.pixel_height = PIXEL_HEIGHT

config.output_file = OUTPUT_FILE_NAME


# ============================================================
# JSON読み込み
# ============================================================

def load_content() -> dict:
    """外部JSONから教材データを読み込む。"""

    if not CONTENT_FILE.exists():
        raise FileNotFoundError(
            "教材データが見つかりません:\n"
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
        "target_answer",
        "target_text",
        "start_text",
        "goal_text",
        "mission_title",
        "mission_text",
        "start",
        "goal",
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
            "problems は2次元配列にしてください。"
        )

    if len(problems) == 0:
        raise ValueError(
            "problems が空です。"
        )

    cols = len(problems[0])

    if cols == 0:
        raise ValueError(
            "problems の列数が0です。"
        )

    for row_index, row in enumerate(problems):
        if not isinstance(row, list):
            raise ValueError(
                f"{row_index + 1}行目が配列ではありません。"
            )

        if len(row) != cols:
            raise ValueError(
                "problems の列数をすべて"
                "同じにしてください。"
            )

        for col_index, value in enumerate(row):
            if not isinstance(value, str):
                raise ValueError(
                    f"{row_index + 1}行"
                    f"{col_index + 1}列は"
                    "文字列にしてください。"
                )

    rows = len(problems)

    for name in ["start", "goal"]:
        point = data[name]

        if (
            not isinstance(point, list)
            or len(point) != 2
        ):
            raise ValueError(
                f"{name} は [行, 列] で指定してください。"
            )

        row, col = point

        if not (
            0 <= row < rows
            and 0 <= col < cols
        ):
            raise ValueError(
                f"{name} が迷路の範囲外です。"
            )

    return data


# ============================================================
# 顔
# ============================================================

def make_face(theme) -> VGroup:
    """スタート地点の顔。"""

    head = Circle(
        radius=FACE_RADIUS,
        color=theme.accent,
        stroke_width=3.0,
        fill_color=theme.accent_fill,
        fill_opacity=0.55,
    )

    left_eye = Circle(
        radius=FACE_EYE_RADIUS,
        stroke_width=0,
        fill_color=theme.foreground,
        fill_opacity=1.0,
    )

    right_eye = left_eye.copy()

    left_eye.move_to(
        head.get_center()
        + LEFT * 0.17
        + UP * 0.12
    )

    right_eye.move_to(
        head.get_center()
        + RIGHT * 0.17
        + UP * 0.12
    )

    mouth = Line(
        head.get_center()
        + LEFT * 0.18
        + DOWN * 0.12,
        head.get_center()
        + RIGHT * 0.18
        + DOWN * 0.12,
        color=theme.foreground,
        stroke_width=3.0,
    )

    face = VGroup(
        head,
        left_eye,
        right_eye,
        mouth,
    )

    face.scale(FACE_SCALE)

    return face


# ============================================================
# 宝箱
# ============================================================

def make_treasure(theme) -> VGroup:
    """ゴール地点の宝箱。"""

    body = RoundedRectangle(
        width=TREASURE_BODY_WIDTH,
        height=TREASURE_BODY_HEIGHT,
        corner_radius=0.14,
        color=theme.foreground,
        stroke_width=3.0,
        fill_color=theme.warning,
        fill_opacity=0.75,
    )

    lid = RoundedRectangle(
        width=TREASURE_LID_WIDTH,
        height=TREASURE_LID_HEIGHT,
        corner_radius=0.25,
        color=theme.foreground,
        stroke_width=3.0,
        fill_color=theme.warning,
        fill_opacity=0.75,
    )

    lid.next_to(
        body,
        UP,
        buff=-0.10,
    )

    whole_box = VGroup(
        body,
        lid,
    )

    band = Rectangle(
        width=0.28,
        height=1.25,
        stroke_width=0,
        fill_color=theme.accent_fill,
        fill_opacity=1.0,
    )

    band.move_to(
        whole_box.get_center()
    )

    lock = Rectangle(
        width=0.34,
        height=0.30,
        color=theme.foreground,
        stroke_width=2.2,
        fill_color=theme.accent_fill,
        fill_opacity=1.0,
    )

    lock.move_to(
        body.get_center()
        + UP * 0.18
    )

    treasure = VGroup(
        body,
        lid,
        band,
        lock,
    )

    treasure.scale(
        TREASURE_SCALE
    )

    return treasure


# ============================================================
# Scene
# ============================================================

class AdditionMazeWorksheet(EducationScene):
    """A4縦・たし算迷路。"""

    def construct(self) -> None:
        content = load_content()

        theme = self.theme

        problems = content["problems"]

        rows = len(problems)
        cols = len(problems[0])

        start_row, start_col = content["start"]
        goal_row, goal_col = content["goal"]

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
        # 説明
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
        # 今回の数字
        # ----------------------------------------------------

        target_box = RoundedRectangle(
            width=TARGET_BOX_WIDTH,
            height=TARGET_BOX_HEIGHT,
            corner_radius=TARGET_BOX_CORNER_RADIUS,
            color=theme.secondary,
            stroke_width=TARGET_BOX_STROKE_WIDTH,
            fill_color=theme.surface,
            fill_opacity=1.0,
        )

        target_text = self.jp_text(
            content["target_text"],
            font_size=TARGET_FONT_SIZE,
            color=theme.secondary,
            weight="BOLD",
        )

        target_text.move_to(
            target_box
        )

        target = VGroup(
            target_box,
            target_text,
        )

        target.next_to(
            subtitle,
            DOWN,
            buff=TARGET_BUFF,
        )

        # ----------------------------------------------------
        # 迷路位置
        # ----------------------------------------------------

        grid_width = cols * CELL_SIZE

        left = (
            GRID_CENTER_X
            - grid_width / 2
        )

        top = GRID_TOP_Y

        cells = VGroup()
        expressions = VGroup()

        cell_objects = []

        # ----------------------------------------------------
        # マス
        # ----------------------------------------------------

        for row in range(rows):
            cell_row = []

            for col in range(cols):
                x = (
                    left
                    + (col + 0.5)
                    * CELL_SIZE
                )

                y = (
                    top
                    - (row + 0.5)
                    * CELL_SIZE
                )

                fill_opacity = (
                    CELL_FILL_OPACITY_A
                    if (row + col) % 2 == 0
                    else CELL_FILL_OPACITY_B
                )

                cell = RoundedRectangle(
                    width=CELL_SIZE - CELL_GAP,
                    height=CELL_SIZE - CELL_GAP,
                    corner_radius=CELL_CORNER_RADIUS,
                    color=theme.muted,
                    stroke_width=CELL_STROKE_WIDTH,
                    fill_color=theme.surface,
                    fill_opacity=fill_opacity,
                )

                cell.move_to(
                    [x, y, 0]
                )

                expression = Text(
                    problems[row][col],
                    font=theme.sans_font,
                    font_size=PROBLEM_FONT_SIZE,
                    weight="BOLD",
                    color=theme.foreground,
                )

                max_width = (
                    CELL_SIZE
                    * PROBLEM_MAX_WIDTH_RATIO
                )

                if expression.width > max_width:
                    expression.scale_to_fit_width(
                        max_width
                    )

                expression.move_to(
                    cell
                )

                cells.add(
                    cell
                )

                expressions.add(
                    expression
                )

                cell_row.append(
                    cell
                )

            cell_objects.append(
                cell_row
            )

        grid = VGroup(
            cells,
            expressions,
        )

        # ----------------------------------------------------
        # スタート
        # ----------------------------------------------------

        start_cell = (
            cell_objects
            [start_row]
            [start_col]
        )

        face = make_face(
            theme
        )

        face.next_to(
            start_cell,
            LEFT,
            buff=START_GOAL_BUFF,
        )

        start_text = self.jp_text(
            content["start_text"],
            font_size=LABEL_FONT_SIZE,
            color=theme.accent,
            weight="BOLD",
        )

        start_text.next_to(
            face,
            DOWN,
            buff=0.08,
        )

        start_line = Line(
            face.get_right()
            + RIGHT * 0.04,
            start_cell.get_left()
            + LEFT * 0.04,
            color=theme.accent,
            stroke_width=CONNECTOR_STROKE_WIDTH,
        )

        # ----------------------------------------------------
        # ゴール
        # ----------------------------------------------------

        goal_cell = (
            cell_objects
            [goal_row]
            [goal_col]
        )

        treasure = make_treasure(
            theme
        )

        treasure.next_to(
            goal_cell,
            RIGHT,
            buff=START_GOAL_BUFF,
        )

        goal_text = self.jp_text(
            content["goal_text"],
            font_size=LABEL_FONT_SIZE,
            color=theme.secondary,
            weight="BOLD",
        )

        goal_text.next_to(
            treasure,
            DOWN,
            buff=0.08,
        )

        goal_line = Line(
            goal_cell.get_right()
            + RIGHT * 0.04,
            treasure.get_left()
            + LEFT * 0.04,
            color=theme.secondary,
            stroke_width=CONNECTOR_STROKE_WIDTH,
        )

        # ----------------------------------------------------
        # 下部ミッション
        # ----------------------------------------------------

        mission_box = RoundedRectangle(
            width=MISSION_BOX_WIDTH,
            height=MISSION_BOX_HEIGHT,
            corner_radius=MISSION_BOX_CORNER_RADIUS,
            color=theme.accent,
            stroke_width=MISSION_BOX_STROKE_WIDTH,
            fill_color=theme.background,
            fill_opacity=1.0,
        )

        mission_box.to_edge(
            DOWN,
            buff=MISSION_BOTTOM_BUFF,
        )

        mission_title = self.jp_text(
            content["mission_title"],
            font_size=MISSION_TITLE_FONT_SIZE,
            color=theme.accent,
            weight="BOLD",
        )

        mission_text = self.jp_text(
            content["mission_text"],
            font_size=MISSION_FONT_SIZE,
            color=theme.foreground,
            weight="BOLD",
            line_spacing=MISSION_LINE_SPACING,
        )

        mission = VGroup(
            mission_title,
            mission_text,
        )

        mission.arrange(
            DOWN,
            buff=MISSION_INTERNAL_BUFF,
        )

        mission.move_to(
            mission_box
        )

        # ----------------------------------------------------
        # 描画
        # ----------------------------------------------------

        self.add(
            title,
            subtitle,
            target,
            grid,
            face,
            start_text,
            start_line,
            treasure,
            goal_text,
            goal_line,
            mission_box,
            mission,
        )
