"""A4縦・数字なぞり練習プリント。

- 左側の絵を見て数える
- 右上で薄い数字をなぞる
- 右下で自分で数字を書く

JSONの問題データを切り替えることで、数字や絵の組み合わせを増やせる。
出力先は scripts/manim.sh 側に任せる。
"""

import json
from pathlib import Path

import manimpango
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    UL,
    ArcBetweenPoints,
    Circle,
    DashedLine,
    Ellipse,
    Line,
    Polygon,
    RoundedRectangle,
    Scene,
    Square,
    Star,
    Text,
    VGroup,
    WHITE,
    config,
)


# ============================================================
# 用紙・出力
# ============================================================

A4_WIDTH = 21.0
A4_HEIGHT = 29.7
PIXEL_WIDTH = 2480
PIXEL_HEIGHT = 3508

BASE_DIR = Path(__file__).resolve().parent
JSON_DIR = BASE_DIR / "json"

CONTENT_FILE_NAME = "number_trace_01.json"
CONTENT_FILE = JSON_DIR / CONTENT_FILE_NAME

OUTPUT_FILE_PREFIX = "number_trace"

config.frame_width = A4_WIDTH
config.frame_height = A4_HEIGHT
config.pixel_width = PIXEL_WIDTH
config.pixel_height = PIXEL_HEIGHT
config.background_color = "#FFFDF7"
config.output_file = f"{OUTPUT_FILE_PREFIX}_{CONTENT_FILE.stem}"


# ============================================================
# 配色
# ============================================================

TITLE_COLOR = "#5B4636"
SUBTITLE_COLOR = "#6D5A4A"
BODY_TEXT_COLOR = "#5B4636"
PANEL_STROKE = "#D8B98C"
PANEL_FILL = "#FFF7EA"
PANEL_FILL_OPACITY = 0.85
BOX_STROKE = "#B88C5A"
GUIDE_COLOR = "#79A8A9"
TRACE_COLOR = "#B9B9B9"
ACCENT_COLOR = "#F3A64A"


# ============================================================
# レイアウト
# ============================================================

PAGE_TOP_Y = 13.2

TITLE_FONT_SIZE = 62
SUBTITLE_FONT_SIZE = 34
BOTTOM_NOTE_FONT_SIZE = 28

TITLE_TO_SUBTITLE_BUFF = 0.32

PROBLEM_BOX_WIDTH = 18.2
PROBLEM_BOX_HEIGHT = 6.2
PROBLEM_BOX_CORNER_RADIUS = 0.35
PROBLEM_BOX_STROKE_WIDTH = 2.5
PROBLEM_BOX_VERTICAL_GAP = 0.7

PROBLEMS_TOP_Y = 8.8

LEFT_AREA_WIDTH = 7.2
RIGHT_AREA_WIDTH = 9.2

MOTIF_MAX_WIDTH = 5.3
MOTIF_MAX_HEIGHT = 2.6

NUMBER_LABEL_FONT_SIZE = 30
PROMPT_FONT_SIZE = 28

TRACE_ROW_Y_OFFSET = 0.85
WRITE_ROW_Y_OFFSET = -1.25

CELL_SIZE = 2.05
CELL_GAP = 0.35
CELL_CORNER_RADIUS = 0.14
CELL_STROKE_WIDTH = 2.4
GUIDE_STROKE_WIDTH = 1.35
GUIDE_OPACITY = 0.5

TRACE_FONT_SIZE = 132
TRACE_FILL_OPACITY = 0.28
TRACE_STROKE_OPACITY = 0.28
TRACE_STROKE_WIDTH = 0.7

WRITE_HINT_FONT_SIZE = 24


# ============================================================
# フォント
# ============================================================

PREFERRED_FONTS = [
    "UD Digi Kyokasho N",
    "UD Digi Kyokasho NP",
    "UD Digi Kyokasho NK",
]


def require_education_font() -> str:
    available_fonts = set(manimpango.list_fonts())

    for font_name in PREFERRED_FONTS:
        if font_name in available_fonts:
            return font_name

    raise ValueError(
        "教育用フォントが見つかりません。"
        " 次のいずれかを使用できるようにしてください: "
        + ", ".join(PREFERRED_FONTS)
    )


SELECTED_FONT = require_education_font()


# ============================================================
# JSON読み込み
# ============================================================

def load_content() -> dict:
    if not CONTENT_FILE.exists():
        raise FileNotFoundError(
            f"問題JSONが見つかりません: {CONTENT_FILE}"
        )

    with CONTENT_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if "problems" not in data:
        raise ValueError("problems がありません。")

    problems = data["problems"]

    if not isinstance(problems, list) or len(problems) != 3:
        raise ValueError("problems は3問の配列にしてください。")

    for index, problem in enumerate(problems, start=1):
        if not isinstance(problem, dict):
            raise ValueError(f"{index}問目が辞書ではありません。")

        if "number" not in problem:
            raise ValueError(f"{index}問目に number がありません。")

        if "motif" not in problem:
            raise ValueError(f"{index}問目に motif がありません。")

        if "label" not in problem:
            raise ValueError(f"{index}問目に label がありません。")

        number = problem["number"]
        motif = problem["motif"]
        label = problem["label"]

        if not isinstance(number, int) or not (0 <= number <= 9):
            raise ValueError(
                f"{index}問目の number は 0〜9 の整数にしてください。"
            )

        if motif not in {"apple", "star", "balloon"}:
            raise ValueError(
                f"{index}問目の motif は apple / star / balloon のいずれかにしてください。"
            )

        if not isinstance(label, str) or label == "":
            raise ValueError(
                f"{index}問目の label は空でない文字列にしてください。"
            )

    return data


# ============================================================
# 基本部品
# ============================================================

def make_center_guides(square: Square) -> VGroup:
    size = square.width
    cx = square.get_center()[0]
    cy = square.get_center()[1]
    half = size / 2 - 0.12

    horizontal = DashedLine(
        start=[cx - half, cy, 0],
        end=[cx + half, cy, 0],
        dash_length=0.14,
        dashed_ratio=0.55,
        color=GUIDE_COLOR,
        stroke_width=GUIDE_STROKE_WIDTH,
    )
    horizontal.set_stroke(opacity=GUIDE_OPACITY)

    vertical = DashedLine(
        start=[cx, cy - half, 0],
        end=[cx, cy + half, 0],
        dash_length=0.14,
        dashed_ratio=0.55,
        color=GUIDE_COLOR,
        stroke_width=GUIDE_STROKE_WIDTH,
    )
    vertical.set_stroke(opacity=GUIDE_OPACITY)

    return VGroup(horizontal, vertical)


def make_write_cell() -> VGroup:
    square = Square(
        side_length=CELL_SIZE,
        color=BOX_STROKE,
        stroke_width=CELL_STROKE_WIDTH,
    )
    square.round_corners(CELL_CORNER_RADIUS)

    guides = make_center_guides(square)

    return VGroup(square, guides)


def make_trace_text(number: int) -> Text:
    text = Text(
        str(number),
        font=SELECTED_FONT,
        font_size=TRACE_FONT_SIZE,
        color=TRACE_COLOR,
    )
    text.set_fill(TRACE_COLOR, opacity=TRACE_FILL_OPACITY)
    text.set_stroke(
        TRACE_COLOR,
        width=TRACE_STROKE_WIDTH,
        opacity=TRACE_STROKE_OPACITY,
    )
    return text


def make_trace_cell(number: int) -> VGroup:
    base = make_write_cell()
    square = base[0]

    trace = make_trace_text(number)
    max_size = CELL_SIZE * 0.76

    if trace.width > max_size:
        trace.scale(max_size / trace.width)

    if trace.height > max_size:
        trace.scale(max_size / trace.height)

    trace.move_to(square.get_center())

    return VGroup(base, trace)


# ============================================================
# モチーフ
# ============================================================

def make_apple() -> VGroup:
    body = Circle(
        radius=0.42,
        stroke_color="#B53E3E",
        stroke_width=2.0,
        fill_color="#E95A5A",
        fill_opacity=1.0,
    )

    leaf = Ellipse(
        width=0.26,
        height=0.16,
        stroke_color="#5E9D57",
        stroke_width=1.6,
        fill_color="#8BCF7B",
        fill_opacity=1.0,
    )
    leaf.rotate(0.55)
    leaf.next_to(body, UP, buff=-0.06)
    leaf.shift(RIGHT * 0.16)

    stem = Line(
        start=[0, 0, 0],
        end=[0, 0.24, 0],
        color="#8A5A3C",
        stroke_width=3.0,
    )
    stem.next_to(body, UP, buff=-0.02)
    stem.shift(LEFT * 0.02)

    shine = Circle(
        radius=0.08,
        stroke_width=0,
        fill_color="#FFD7D7",
        fill_opacity=0.75,
    )
    shine.move_to(body.get_center() + LEFT * 0.12 + UP * 0.1)

    return VGroup(body, stem, leaf, shine)


def make_star() -> VGroup:
    star = Star(
        n=5,
        outer_radius=0.45,
        color="#E4B23C",
        stroke_width=2.0,
    )
    star.set_fill("#FFD665", opacity=1.0)

    smile = ArcBetweenPoints(
        start=[-0.12, -0.02, 0],
        end=[0.12, -0.02, 0],
        angle=-1.1,
        color="#8A6430",
        stroke_width=2.0,
    )

    eye_left = Circle(
        radius=0.022,
        stroke_width=0,
        fill_color="#8A6430",
        fill_opacity=1.0,
    )
    eye_right = eye_left.copy()
    eye_left.move_to(LEFT * 0.09 + UP * 0.07)
    eye_right.move_to(RIGHT * 0.09 + UP * 0.07)

    return VGroup(star, eye_left, eye_right, smile)


def make_balloon() -> VGroup:
    body = Circle(
        radius=0.38,
        stroke_color="#4F94C4",
        stroke_width=2.0,
        fill_color="#89CCF5",
        fill_opacity=1.0,
    )
    knot = Polygon(
        [-0.06, -0.36, 0],
        [0.06, -0.36, 0],
        [0.00, -0.47, 0],
        color="#4F94C4",
        stroke_width=2.0,
    )
    knot.set_fill("#89CCF5", opacity=1.0)

    string = ArcBetweenPoints(
        start=[0.0, -0.47, 0],
        end=[0.08, -0.95, 0],
        angle=-0.4,
        color="#8A6B52",
        stroke_width=2.0,
    )

    shine = Circle(
        radius=0.07,
        stroke_width=0,
        fill_color="#DDF4FF",
        fill_opacity=0.9,
    )
    shine.move_to(LEFT * 0.11 + UP * 0.09)

    return VGroup(body, knot, string, shine)


def make_single_motif(name: str) -> VGroup:
    if name == "apple":
        return make_apple()

    if name == "star":
        return make_star()

    if name == "balloon":
        return make_balloon()

    raise ValueError(f"未対応の motif です: {name}")


def make_motif_row(motif_name: str, count: int) -> VGroup:
    if count == 0:
        zero_text = Text(
            "0 こ",
            font=SELECTED_FONT,
            font_size=38,
            color=BODY_TEXT_COLOR,
        )
        return VGroup(zero_text)

    motifs = VGroup()

    for _ in range(count):
        motifs.add(make_single_motif(motif_name))

    motifs.arrange(RIGHT, buff=0.35)

    if motifs.width > MOTIF_MAX_WIDTH:
        motifs.scale(MOTIF_MAX_WIDTH / motifs.width)

    if motifs.height > MOTIF_MAX_HEIGHT:
        motifs.scale(MOTIF_MAX_HEIGHT / motifs.height)

    return motifs


# ============================================================
# 問題1段
# ============================================================

def make_two_cell_row(number: int, trace: bool) -> VGroup:
    cells = VGroup()

    for _ in range(2):
        if trace:
            cell = make_trace_cell(number)
        else:
            cell = make_write_cell()

        cells.add(cell)

    cells.arrange(RIGHT, buff=CELL_GAP)
    return cells


def make_problem_panel(number: int, motif: str, label: str) -> VGroup:
    panel = RoundedRectangle(
        corner_radius=PROBLEM_BOX_CORNER_RADIUS,
        width=PROBLEM_BOX_WIDTH,
        height=PROBLEM_BOX_HEIGHT,
        stroke_color=PANEL_STROKE,
        stroke_width=PROBLEM_BOX_STROKE_WIDTH,
        fill_color=PANEL_FILL,
        fill_opacity=PANEL_FILL_OPACITY,
    )

    left_anchor_x = panel.get_left()[0] + 1.0
    right_anchor_x = panel.get_right()[0] - 3.1

    # 左側：絵
    motif_row = make_motif_row(motif, number)
    motif_row.move_to([left_anchor_x + 1.8, panel.get_center()[1] + 0.7, 0])

    prompt = Text(
        f"{label}は なんこ？",
        font=SELECTED_FONT,
        font_size=PROMPT_FONT_SIZE,
        color=BODY_TEXT_COLOR,
    )
    prompt.move_to([left_anchor_x + 1.8, panel.get_center()[1] - 1.35, 0])

    # 右側：なぞり + 自力
    trace_hint = Text(
        "なぞろう",
        font=SELECTED_FONT,
        font_size=WRITE_HINT_FONT_SIZE,
        color=BODY_TEXT_COLOR,
    )
    trace_hint.move_to([right_anchor_x, panel.get_center()[1] + 1.65, 0])

    trace_row = make_two_cell_row(number, trace=True)
    trace_row.move_to([right_anchor_x, panel.get_center()[1] + TRACE_ROW_Y_OFFSET, 0])

    write_hint = Text(
        "じぶんで かこう",
        font=SELECTED_FONT,
        font_size=WRITE_HINT_FONT_SIZE,
        color=BODY_TEXT_COLOR,
    )
    write_hint.move_to([right_anchor_x, panel.get_center()[1] - 0.1, 0])

    write_row = make_two_cell_row(number, trace=False)
    write_row.move_to([right_anchor_x, panel.get_center()[1] + WRITE_ROW_Y_OFFSET, 0])

    big_number_badge = Circle(
        radius=0.45,
        stroke_color=ACCENT_COLOR,
        stroke_width=2.5,
        fill_color="#FFE3BA",
        fill_opacity=1.0,
    )
    big_number_badge.move_to(panel.get_corner(UL) + RIGHT * 0.8 + DOWN * 0.8)

    badge_text = Text(
        str(number),
        font=SELECTED_FONT,
        font_size=34,
        color=BODY_TEXT_COLOR,
    )
    badge_text.move_to(big_number_badge.get_center())

    return VGroup(
        panel,
        motif_row,
        prompt,
        trace_hint,
        trace_row,
        write_hint,
        write_row,
        big_number_badge,
        badge_text,
    )


# ============================================================
# シーン
# ============================================================

class NumberTracePracticeWorksheet(Scene):
    def construct(self) -> None:
        data = load_content()

        title = Text(
            data["title"],
            font=SELECTED_FONT,
            font_size=TITLE_FONT_SIZE,
            color=TITLE_COLOR,
        )
        title.move_to([0, PAGE_TOP_Y, 0])

        subtitle = Text(
            data["subtitle"],
            font=SELECTED_FONT,
            font_size=SUBTITLE_FONT_SIZE,
            color=SUBTITLE_COLOR,
        )
        subtitle.next_to(title, DOWN, buff=TITLE_TO_SUBTITLE_BUFF)

        problems_group = VGroup()

        for problem in data["problems"]:
            number = problem["number"]
            motif = problem["motif"]
            label = problem["label"]

            panel = make_problem_panel(number, motif, label)
            problems_group.add(panel)

        problems_group.arrange(DOWN, buff=PROBLEM_BOX_VERTICAL_GAP)
        problems_group.move_to([0, 0.1, 0])

        bottom_note = Text(
            data.get("bottom_note", ""),
            font=SELECTED_FONT,
            font_size=BOTTOM_NOTE_FONT_SIZE,
            color=SUBTITLE_COLOR,
        )
        bottom_note.move_to([0, -13.65, 0])

        self.add(title, subtitle, problems_group, bottom_note)
