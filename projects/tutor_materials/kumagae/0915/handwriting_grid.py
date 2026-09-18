"""A4縦向き・ひらがな／漢字練習用方眼紙."""

from manim import (
    DashedLine,
    Line,
    ManimColor,
    Rectangle,
    Scene,
    VGroup,
    WHITE,
    config,
)


# ============================================================
# 用紙
# ============================================================

# 1 Manim unit = 1 cm として扱う
A4_WIDTH = 21.0
A4_HEIGHT = 29.7

config.frame_width = A4_WIDTH
config.frame_height = A4_HEIGHT
config.background_color = WHITE


# ============================================================
# 方眼
# ============================================================

CELL_SIZE = 2.85  # 10行入るサイズ

COLS = 6
ROWS = 10

GRID_WIDTH = COLS * CELL_SIZE   # 17.1 cm
GRID_HEIGHT = ROWS * CELL_SIZE  # 28.5 cm


# ============================================================
# デザイン（印刷向けに濃く・太く）
# ============================================================

GRID_COLOR = ManimColor("#444444")
GUIDE_COLOR = ManimColor("#666666")

OUTER_STROKE_WIDTH = 3.0
GRID_STROKE_WIDTH = 2.2
GUIDE_STROKE_WIDTH = 1.8

# 破線がマス枠に触れないよう少し内側に入れる
GUIDE_INSET = 0.12

# 破線の設定
DASH_LENGTH = 0.16
DASH_RATIO = 0.55  # 線の割合。大きいほど「線」が長く見える


def make_horizontal_guide(center_x: float, center_y: float) -> DashedLine:
    """マス中央を通る横方向の破線."""

    half_length = CELL_SIZE / 2 - GUIDE_INSET

    guide = DashedLine(
        start=[center_x - half_length, center_y, 0],
        end=[center_x + half_length, center_y, 0],
        dash_length=DASH_LENGTH,
        dashed_ratio=DASH_RATIO,
        color=GUIDE_COLOR,
        stroke_width=GUIDE_STROKE_WIDTH,
    )

    guide.set_stroke(opacity=0.95)

    return guide


def make_vertical_guide(center_x: float, center_y: float) -> DashedLine:
    """マス中央を通る縦方向の破線."""

    half_length = CELL_SIZE / 2 - GUIDE_INSET

    guide = DashedLine(
        start=[center_x, center_y - half_length, 0],
        end=[center_x, center_y + half_length, 0],
        dash_length=DASH_LENGTH,
        dashed_ratio=DASH_RATIO,
        color=GUIDE_COLOR,
        stroke_width=GUIDE_STROKE_WIDTH,
    )

    guide.set_stroke(opacity=0.95)

    return guide


class JapaneseWritingGrid(Scene):
    """ひらがな・漢字練習用のA4方眼紙."""

    def construct(self) -> None:
        left = -GRID_WIDTH / 2
        right = GRID_WIDTH / 2
        bottom = -GRID_HEIGHT / 2
        top = GRID_HEIGHT / 2

        # ----------------------------------------------------
        # 外枠
        # ----------------------------------------------------

        border = Rectangle(
            width=GRID_WIDTH,
            height=GRID_HEIGHT,
            color=GRID_COLOR,
            stroke_width=OUTER_STROKE_WIDTH,
        )

        # ----------------------------------------------------
        # 方眼
        # ----------------------------------------------------

        grid = VGroup()

        # 縦線
        for col in range(1, COLS):
            x = left + col * CELL_SIZE
            grid.add(
                Line(
                    [x, bottom, 0],
                    [x, top, 0],
                    color=GRID_COLOR,
                    stroke_width=GRID_STROKE_WIDTH,
                )
            )

        # 横線
        for row in range(1, ROWS):
            y = bottom + row * CELL_SIZE
            grid.add(
                Line(
                    [left, y, 0],
                    [right, y, 0],
                    color=GRID_COLOR,
                    stroke_width=GRID_STROKE_WIDTH,
                )
            )

        # ----------------------------------------------------
        # 各マス中央の縦横破線
        # ----------------------------------------------------

        guides = VGroup()

        for row in range(ROWS):
            for col in range(COLS):
                center_x = left + (col + 0.5) * CELL_SIZE
                center_y = bottom + (row + 0.5) * CELL_SIZE

                guides.add(
                    make_horizontal_guide(center_x, center_y),
                    make_vertical_guide(center_x, center_y),
                )

        self.add(border, grid, guides)