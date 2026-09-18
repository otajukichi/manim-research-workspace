"""A4縦向き・ひらがなワードサーチ／文字練習シート。

文字配置は data/ 以下の外部JSONから読み込む。
JSONは上から下、左から右の見た目どおりの2次元配列で指定する。

問題JSONは --content-file で実行時に切り替えられる。

例:
pixi run manim -- \
    --content-file wordsearch_01.json \
    -s \
    --resolution 2480,3508 \
    projects/tutor_materials/k/0918/hiragana_wordsearch/hiragana_wordsearch.py \
    HiraganaWordSearch
"""

import json
import os
from pathlib import Path

import manimpango
from manim import (
    DashedLine,
    Line,
    Rectangle,
    Scene,
    Text,
    VGroup,
    config,
)

from manim_research.theme import EDUCATION_THEME


# ============================================================
# 用紙
# ============================================================

A4_WIDTH = 21.0  # A4用紙の横幅。1 Manim unit = 1 cmとして扱う。
A4_HEIGHT = 29.7  # A4用紙の縦幅。1 Manim unit = 1 cmとして扱う。


# ============================================================
# 方眼
# ============================================================

CELL_SIZE = 2.85  # 方眼1マスの一辺の長さ [cm]。
COLS = 6  # 方眼の横方向のマス数。
ROWS = 10  # 方眼の縦方向のマス数。


# ============================================================
# デザイン（Education Theme / 印刷向け）
# ============================================================

THEME = EDUCATION_THEME  # リポジトリ共通の子ども向けEducation Themeを使用する。

PAGE_BACKGROUND_COLOR = THEME.background  # 用紙背景。温かみのあるアイボリー。
OUTER_BORDER_COLOR = THEME.accent  # 方眼全体の外枠。親しみやすいオレンジ系。
GRID_COLOR = THEME.muted  # 方眼内部の実線。落ち着いた茶系。
GUIDE_COLOR = THEME.secondary  # マス中央の破線。青緑系のアクセント。
TEXT_COLOR = THEME.foreground  # 見本文字。読みやすい濃い焦げ茶。

OUTER_STROKE_WIDTH = 3.0  # 方眼全体の外枠の太さ。
GRID_STROKE_WIDTH = 2.2  # 方眼内部の実線の太さ。
GUIDE_STROKE_WIDTH = 1.8  # マス中央にある破線ガイドの太さ。

GRID_OPACITY = 1  # 方眼内部の実線の濃さ。0.0で透明、1.0で完全不透明。
GUIDE_OPACITY = 1  # マス中央の破線ガイドの濃さ。0.0で透明、1.0で完全不透明。

GUIDE_INSET = 0.12  # 破線ガイドをマスの外枠からどれだけ内側に離すか [cm]。
DASH_LENGTH = 0.16  # 破線1本あたりのおおよその長さ。
DASH_RATIO = 0.55  # 破線の線部分が占める割合。0.5前後で線と空白がほぼ同程度。


# ============================================================
# 見本字の調整パラメータ
# ============================================================

SAMPLE_FONT_SIZE = 177  # すべての見本文字に共通して使用するフォントサイズ。
#SAMPLE_FILL_OPACITY = 0.6  # 見本文字内部の濃さ。0.0で透明、1.0で完全不透明。
#SAMPLE_STROKE_OPACITY = 0.6  # 見本文字の輪郭線の濃さ。0.0で透明、1.0で完全不透明。
SAMPLE_FILL_OPACITY = 1  # 見本文字内部の濃さ。0.0で透明、1.0で完全不透明。
SAMPLE_STROKE_OPACITY = 1  # 見本文字の輪郭線の濃さ。0.0で透明、1.0で完全不透明。
SAMPLE_STROKE_WIDTH = 0.8  # 見本文字の輪郭線の太さ。
SAMPLE_X_OFFSET = 0.0  # すべての見本文字を左右へ一括移動する量 [cm]。正で右、負で左。
SAMPLE_Y_OFFSET = 0.0  # すべての見本文字を上下へ一括移動する量 [cm]。正で上、負で下。


# ============================================================
# 文字配置ファイル
# ============================================================

DEFAULT_CONTENT_FILE_NAME = "wordsearch_01.json"
OUTPUT_FILE_PREFIX = "wordsearch"


# ============================================================
# フォント
# ============================================================

PREFERRED_FONTS = ["UD Digi Kyokasho N", "UD Digi Kyokasho NP", "UD Digi Kyokasho NK"]  # 使用する教育用フォントの優先順位。


# ============================================================
# 内部設定
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def resolve_content_file() -> Path:
    """実行時に指定されたJSONファイルを解決する。

    ファイル名だけの場合:
        wordsearch_02.json

    フルパス・相対パス指定も可能。
    """

    requested = os.environ.get(
        "MANIM_CONTENT_FILE",
        DEFAULT_CONTENT_FILE_NAME,
    )

    requested_path = Path(
        requested
    ).expanduser()

    # 絶対パス
    if requested_path.is_absolute():
        return requested_path

    # リポジトリルート等からの相対パス
    cwd_path = (
        Path.cwd()
        / requested_path
    )

    if cwd_path.is_file():
        return cwd_path.resolve()

    # この教材フォルダ基準
    local_path = (
        BASE_DIR
        / requested_path
    )

    if local_path.is_file():
        return local_path.resolve()

    # ファイル名だけなら data/ を使う
    return (
        DATA_DIR
        / requested_path
    )


CONTENT_FILE = resolve_content_file()

OUTPUT_FILE_NAME = (
    f"{OUTPUT_FILE_PREFIX}_{CONTENT_FILE.stem}"
)

GRID_WIDTH = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE

config.frame_width = A4_WIDTH
config.frame_height = A4_HEIGHT
config.background_color = PAGE_BACKGROUND_COLOR
config.output_file = OUTPUT_FILE_NAME


# ============================================================
# 文字データ読み込み
# ============================================================

def load_content_grid() -> list[list[str]]:
    """外部JSONから全マスの文字配置を読み込む.

    JSONの指定方法:
    - 外側の配列: 上から下
    - 内側の配列: 左から右
    - 空白マス: ""
    """

    if not CONTENT_FILE.exists():
        raise FileNotFoundError(
            f"文字配置ファイルが見つかりません:\n{CONTENT_FILE}"
        )

    with CONTENT_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "文字配置JSONの最上位は配列にしてください。"
        )

    if len(data) != ROWS:
        raise ValueError(
            f"文字配置JSONの行数が不正です。"
            f" 必要: {ROWS}行 / 実際: {len(data)}行"
        )

    for row_index, row in enumerate(data):
        if not isinstance(row, list):
            raise ValueError(
                f"{row_index + 1}行目が配列ではありません。"
            )

        if len(row) != COLS:
            raise ValueError(
                f"{row_index + 1}行目の列数が不正です。"
                f" 必要: {COLS}列 / 実際: {len(row)}列"
            )

        for col_index, value in enumerate(row):
            if not isinstance(value, str):
                raise ValueError(
                    f"{row_index + 1}行"
                    f"{col_index + 1}列の値は文字列にしてください。"
                )

    return data


# ============================================================
# フォント
# ============================================================

def require_education_font() -> str:
    """利用可能な教育用フォントを優先順に探す."""

    available_fonts = set(manimpango.list_fonts())

    for font_name in PREFERRED_FONTS:
        if font_name in available_fonts:
            return font_name

    raise ValueError(
        "教育用フォントが見つかりません。"
        " 少なくとも次のいずれかを使用できるようにしてください: "
        + ", ".join(PREFERRED_FONTS)
    )


SELECTED_FONT = require_education_font()


# ============================================================
# ガイド線
# ============================================================

def make_horizontal_guide(
    center_x: float,
    center_y: float,
) -> DashedLine:
    """マス中央を通る横方向の破線."""

    half_length = CELL_SIZE / 2 - GUIDE_INSET

    guide = DashedLine(
        start=[
            center_x - half_length,
            center_y,
            0,
        ],
        end=[
            center_x + half_length,
            center_y,
            0,
        ],
        dash_length=DASH_LENGTH,
        dashed_ratio=DASH_RATIO,
        color=GUIDE_COLOR,
        stroke_width=GUIDE_STROKE_WIDTH,
    )

    guide.set_stroke(opacity=GUIDE_OPACITY)

    return guide


def make_vertical_guide(
    center_x: float,
    center_y: float,
) -> DashedLine:
    """マス中央を通る縦方向の破線."""

    half_length = CELL_SIZE / 2 - GUIDE_INSET

    guide = DashedLine(
        start=[
            center_x,
            center_y - half_length,
            0,
        ],
        end=[
            center_x,
            center_y + half_length,
            0,
        ],
        dash_length=DASH_LENGTH,
        dashed_ratio=DASH_RATIO,
        color=GUIDE_COLOR,
        stroke_width=GUIDE_STROKE_WIDTH,
    )

    guide.set_stroke(opacity=GUIDE_OPACITY)

    return guide


# ============================================================
# 見本字
# ============================================================

def make_sample_character(
    char: str,
    center_x: float,
    center_y: float,
) -> Text:
    """なぞり書き用の見本字."""

    sample = Text(
        char,
        font=SELECTED_FONT,
        color=TEXT_COLOR,
        font_size=SAMPLE_FONT_SIZE,
    )

    sample.move_to(
        [
            center_x + SAMPLE_X_OFFSET,
            center_y + SAMPLE_Y_OFFSET,
            0,
        ]
    )

    sample.set_fill(
        TEXT_COLOR,
        opacity=SAMPLE_FILL_OPACITY,
    )

    sample.set_stroke(
        TEXT_COLOR,
        opacity=SAMPLE_STROKE_OPACITY,
        width=SAMPLE_STROKE_WIDTH,
    )

    return sample


# ============================================================
# Scene
# ============================================================

class HiraganaWordSearch(Scene):
    """JSONで自由に文字配置できるひらがなワードサーチ."""

    def construct(self) -> None:
        content_grid = load_content_grid()

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
            color=OUTER_BORDER_COLOR,
            stroke_width=OUTER_STROKE_WIDTH,
        )

        # ----------------------------------------------------
        # 方眼
        # ----------------------------------------------------

        grid = VGroup()

        for col in range(1, COLS):
            x = left + col * CELL_SIZE

            grid.add(
                Line(
                    [x, bottom, 0],
                    [x, top, 0],
                    color=GRID_COLOR,
                    stroke_width=GRID_STROKE_WIDTH,
                ).set_stroke(opacity=GRID_OPACITY)
            )

        for row in range(1, ROWS):
            y = bottom + row * CELL_SIZE

            grid.add(
                Line(
                    [left, y, 0],
                    [right, y, 0],
                    color=GRID_COLOR,
                    stroke_width=GRID_STROKE_WIDTH,
                ).set_stroke(opacity=GRID_OPACITY)
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
                    make_horizontal_guide(
                        center_x,
                        center_y,
                    ),
                    make_vertical_guide(
                        center_x,
                        center_y,
                    ),
                )

        # ----------------------------------------------------
        # JSONで指定された文字
        # ----------------------------------------------------

        samples = VGroup()

        for row_from_top, row_data in enumerate(content_grid):
            manim_row = ROWS - 1 - row_from_top

            for col, char in enumerate(row_data):
                if char == "":
                    continue

                center_x = left + (col + 0.5) * CELL_SIZE
                center_y = bottom + (manim_row + 0.5) * CELL_SIZE

                samples.add(
                    make_sample_character(
                        char,
                        center_x,
                        center_y,
                    )
                )

        self.add(
            border,
            grid,
            guides,
            samples,
        )