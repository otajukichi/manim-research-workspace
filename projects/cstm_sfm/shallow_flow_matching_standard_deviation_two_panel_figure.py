r"""SFM の標準偏差ベース図を上下2段に並べた静止画です。

上段:
- 標準偏差ベースの CondOT 背景
- \hat{X}_h と t_h X_1 の誤差
- \hat{t}_h と t_h X_1 の誤差

下段:
- 上段とまったく同じ CondOT 背景
- 通常の標準偏差包絡線に加えて 1/2 標準偏差包絡線を表示
- 選択時刻の 1/2 標準偏差円だけを紫色で強調
- \hat{X}_h は基準時刻の真上ではなく斜め方向に配置
- \hat{X}_h 周りの分布は描かない
- 基準時刻から X_1 への赤い矢印を表示

さらに、
- 各図の右上にタイトルを表示できます。
- タイトルは文字・位置・文字サイズ・色を調整できます。

調整したい値は、ファイル冒頭の
「ユーザー調整用パラメータ」だけを触ればよい構成にしています。
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Dot,
    Line,
    MathTex,
    ManimColor,
    Text,
    VGroup,
    config,
)

from manim_research import LightScene


# ============================================================
# キャンバス
# ============================================================

# 上下2段を並べるため、ほぼ正方形のキャンバスにしています。
config.frame_width = 8.8
config.frame_height = 8.8


# ============================================================
# 色
# ============================================================

BACKGROUND = ManimColor("#FFFFFF")
INK = ManimColor("#1F2933")

# CondOT の平均線・標準偏差曲線・標準偏差円に使う青色です。
ACCENT = ManimColor("#2D5B84")
MUTED = ManimColor("#7C8894")
VERY_FAINT = ManimColor("#C8D1DA")

SOURCE_FILL = ManimColor("#AEBFCC")
MID_FILL = ManimColor("#C9D4DE")

PREDICTED_COLOR = ManimColor("#244A6A")
LOSS_ARROW_COLOR = ManimColor("#355F86")

# 下段の終端時刻方向の矢印だけ赤色にします。
TERMINAL_ARROW_COLOR = ManimColor("#C94A4A")

# 紫色は「選択時刻の 1/2 標準偏差円」だけに使います。
# 1/2 標準偏差の包絡線そのものは ACCENT と同じ青色です。
HALF_SIGMA_CIRCLE_COLOR = ManimColor("#7B2CBF")


# ============================================================
# ユーザー調整用パラメータ
# ============================================================
#
# 基本的には、このブロックだけ触れば図の主要な配置を調整できます。
#
# 座標の微調整はすべて (dx, dy) で指定します。
#
#   dx > 0 : 右へ移動
#   dx < 0 : 左へ移動
#   dy > 0 : 上へ移動
#   dy < 0 : 下へ移動
#
# 例:
#   (0.20, 0.10)   -> 右へ 0.20、上へ 0.10
#   (-0.15, -0.05) -> 左へ 0.15、下へ 0.05
#
# ============================================================


# ------------------------------------------------------------
# 1. 標準偏差全体の広がり
# ------------------------------------------------------------
#
# この値を大きくすると、
# - 各分布の標準偏差円
# - 標準偏差の包絡線
# - 下段の 1/2 標準偏差円
# - 下段の 1/2 標準偏差包絡線
# が全体的に大きくなります。
#
# 下段は 1/2 スケールを見るため、見づらい場合はこの値を大きくします。
SIGMA_VISUAL_MAX = 1


# ------------------------------------------------------------
# 2. 上下2つの図の間隔
# ------------------------------------------------------------
#
# 大きくすると上下の図が離れます。
# 小さくすると上下の図が近づきます。
# 0 に近づけるほど密着します。
PANEL_VERTICAL_GAP = -0.2


# ------------------------------------------------------------
# 3. 上段の \hat{X}_h の位置
# ------------------------------------------------------------
#
# まず、t_h X_1 から標準偏差半径の何倍上に置くかを指定します。
XHAT_VERTICAL_SIGMA_MULTIPLIER = 0.85

# その基本位置からさらに (左右, 上下) を微調整します。
# 横方向も自由に動かしたい場合はこちらを使います。
TOP_XHAT_POINT_SHIFT = (0.00, 0.00)


# ------------------------------------------------------------
# 4. 下段の \hat{X}_h の位置
# ------------------------------------------------------------
#
# 基準点 \hat{t}_h X_1 から、標準偏差半径の何倍離すかを指定します。
XHAT_DIAGONAL_RADIUS_FACTOR = 0.85

# 斜め方向の角度です。単位は degree です。
# 0度   : 右
# 45度  : 右上
# 90度  : 真上
XHAT_DIAGONAL_ANGLE_DEG = 52.0

# 上の距離・角度で決めた位置から、さらに (左右, 上下) を微調整します。
BOTTOM_XHAT_POINT_SHIFT = (0.00, 0.00)


# ------------------------------------------------------------
# 5. 各ラベルの位置
# ------------------------------------------------------------
#
# すべて (dx, dy) の2値だけで調整します。
# 点そのものは動かさず、文字だけを動かします。

# 上段
TOP_SOURCE_LABEL_SHIFT = (0.05, 0.00)
TOP_X1_LABEL_SHIFT = (0.00, 0.00)
TOP_XHAT_LABEL_SHIFT = (-0.3, -0.25)
TOP_TX1_LABEL_SHIFT = (0.00, 0.00)
TOP_THAT_LABEL_SHIFT = (0.00, 0.02)

# 下段
BOTTOM_SOURCE_LABEL_SHIFT = (0.05, 0.00)
BOTTOM_X1_LABEL_SHIFT = (0.00, 0.00)
BOTTOM_XHAT_LABEL_SHIFT = (0.00, -0.1)
BOTTOM_REFERENCE_LABEL_SHIFT = (0.02, 0.07)
BOTTOM_HALF_SIGMA_LABEL_SHIFT = (-0.38, 0.18)


# ------------------------------------------------------------
# 6. 図の右上に表示するタイトル
# ------------------------------------------------------------
#
# 各図の右上に名称を表示します。
# 位置は「各パネルの右上」を基準にして、そのあと (dx, dy) だけ動かします。
#
# 文字そのもの、文字サイズ、色、位置を個別に調整できます。

# 上段タイトル
TOP_PANEL_TITLE_TEXT = "SFM"
TOP_PANEL_TITLE_FONT_SIZE = 20
TOP_PANEL_TITLE_COLOR = INK

# 右上基準からの微調整
TOP_PANEL_TITLE_SHIFT = (-0.55, -0.55)

# 下段タイトル
BOTTOM_PANEL_TITLE_TEXT = "CSTM-SFM"
BOTTOM_PANEL_TITLE_FONT_SIZE = 20
BOTTOM_PANEL_TITLE_COLOR = INK

# 右上基準からの微調整
BOTTOM_PANEL_TITLE_SHIFT = (-0.55, -0.55)


# ------------------------------------------------------------
# 7. その他の位置関係
# ------------------------------------------------------------

# 上段で使う時刻です。
T_SELECTED = 0.3

# 下段も同じ時刻を使います。
T_HAT_SELECTED = T_SELECTED

# 上段の \hat{t}_h の点を t_h X_1 から右へどれだけ離すかです。
THAT_SCALAR_SHIFT_RIGHT = 0.7

# 下段の標準偏差スケール倍率です。
# 二乗距離に対して CondOT 分散の 1/2 を許容するため、
# 距離として描く半径は sqrt(1/2) = 1/sqrt(2) 倍にします。
HALF_SIGMA_RADIUS_FACTOR = 1.0 / np.sqrt(2.0)


# ============================================================
# CondOT 共通幾何
# ============================================================

ROW_Y = 0.00

# 左端の source 平均位置です。
SOURCE_MEAN = np.array([-1.95, ROW_Y])

# X_1 は以前より source 側へ近づけています。
X1_POINT = np.array([1.35, ROW_Y])

# 背景に表示する分布の個数です。
NUM_DISPLAY_CIRCLES = 6

# 隣接する分布の重なり具合を決める係数です。
OVERLAP_RATIO = 0.22


# ============================================================
# 分布の補助円
# ============================================================

# 通常の分布では、
# - 0.55 : 標準偏差円より内側
# - 1.45 : 標準偏差円より外側
# - 1.90 : さらに外側
# の3本の補助円を描きます。
GENERAL_AUXILIARY_RADIUS_MULTIPLIERS = [0.55, 1.45, 1.90]

# 左端の最大分布だけは、画像の縦方向を無駄に広げないように、
# 標準偏差円より外側の補助円を「1本だけ」にしています。
#
# 残る補助円は
# - 0.55 : 内側の補助円
# - 1.45 : 外側の補助円 1本
#
# 1.90 の一番外側の補助円は描きません。
SOURCE_AUXILIARY_RADIUS_MULTIPLIERS = [0.55, 1.45]

# 青色で強調する標準偏差円そのものの倍率です。
EMPHASIZED_RADIUS_MULTIPLIER = 1.00


# ============================================================
# 線・円・点の見た目
# ============================================================

PANEL_SCALE = 1.00

AUXILIARY_CIRCLE_OPACITY = 0.18
AUXILIARY_CIRCLE_WIDTH = 0.85

SIGMA_CIRCLE_OPACITY = 0.42
SIGMA_CIRCLE_WIDTH = 1.20

ENVELOPE_OPACITY = 0.36
ENVELOPE_WIDTH = 0.90

MEAN_LINE_OPACITY = 0.55
MEAN_LINE_WIDTH = 1.35

FAINT_CENTER_DOT_OPACITY = 0.28

INNER_DISK_STROKE_WIDTH = 0.75
INNER_DISK_STROKE_OPACITY = 0.16
INNER_DISK_FILL_SOURCE_OPACITY = 0.11
INNER_DISK_FILL_MID_OPACITY = 0.08

MAIN_DOT_RADIUS = 0.040
ENDPOINT_DOT_RADIUS = 0.036
CENTER_DOT_RADIUS = 0.018
SECONDARY_DOT_RADIUS = 0.024

HALF_SIGMA_CIRCLE_WIDTH = 1.75
HALF_SIGMA_CIRCLE_OPACITY = 0.84


# ============================================================
# 矢印の見た目
# ============================================================

VERTICAL_ARROW_END_GAP = 0.060
HORIZONTAL_ARROW_END_GAP = 0.065
XHAT_TO_T_ARROW_END_GAP = 0.050
T_TO_X1_ARROW_END_GAP = 0.065

ARROW_TIP_LENGTH = 0.11


# ============================================================
# 1/2 標準偏差ラベルの基本配置
# ============================================================

HALF_SIGMA_LABEL_FONT_SIZE = 24

# 紫色の 1/2 標準偏差円の中心から見て、ラベルを置く方向です。
HALF_SIGMA_LABEL_ANGLE_DEG = 145.0

# 紫色の円の半径に対して、どれくらい外側へラベルを置くかです。
HALF_SIGMA_LABEL_RADIAL_FACTOR = 1.28


# ============================================================
# 共通ユーティリティ
# ============================================================


def shift_vector(shift_xy: tuple[float, float]) -> np.ndarray:
    """(dx, dy) を Manim の3次元移動ベクトルへ変換します。"""
    dx, dy = shift_xy
    return np.array([dx, dy, 0.0])


def mean_t(t: float) -> np.ndarray:
    """CondOT の平均を source から X_1 まで線形に移動させます。"""
    return (1.0 - t) * SOURCE_MEAN + t * X1_POINT


def visual_sigma_t(t: float, *, factor: float = 1.0) -> float:
    """標準偏差に比例した表示半径を返します。

    CondOT の標準偏差が (1-t) に比例するため、
    表示半径も (1-t) に比例して線形に減少させています。
    """
    return factor * SIGMA_VISUAL_MAX * (1.0 - t)


def visual_sigma_derivative_t(
    t: float,
    *,
    factor: float = 1.0,
) -> float:
    """表示用標準偏差半径を時刻 t で微分した値を返します。"""
    return -factor * SIGMA_VISUAL_MAX


def unit_vector_from_angle_deg(angle_deg: float) -> np.ndarray:
    """指定した角度 degree に対応する2次元単位ベクトルを返します。"""
    theta = np.deg2rad(angle_deg)
    return np.array([np.cos(theta), np.sin(theta), 0.0])


def make_panel_title(
    panel: VGroup,
    *,
    title_text: str,
    font_size: float,
    color: ManimColor,
    shift: tuple[float, float],
) -> Text:
    """パネル右上に置くタイトルを作ります。

    使い方:
    - まず panel の右上を基準点にします。
    - その後、shift=(dx, dy) で微調整します。
    - 文字列、文字サイズ、色も自由に変更できます。
    """
    title = Text(
        title_text,
        font_size=font_size,
        color=color,
    )

    anchor = panel.get_corner(UP + RIGHT)
    title.move_to(anchor + shift_vector(shift))
    title.set_z_index(20)

    return title


# ============================================================
# 背景分布を置く時刻
# ============================================================


def make_display_times() -> list[float]:
    """隣り合う分布の重なり具合が概ね一定になるように時刻を決めます。"""
    path_length = X1_POINT[0] - SOURCE_MEAN[0]
    rho = OVERLAP_RATIO

    times = [0.0]

    for _ in range(NUM_DISPLAY_CIRCLES - 1):
        current_t = times[-1]
        current_radius = visual_sigma_t(current_t)

        def overlap_equation(next_t: float) -> float:
            center_gap = path_length * (next_t - current_t)
            next_radius = visual_sigma_t(next_t)
            desired_gap = (
                current_radius
                + (1.0 - rho) * next_radius
            )
            return center_gap - desired_gap

        if overlap_equation(1.0) <= 0.0:
            raise ValueError(
                "分布を t=1 より前に配置できません。"
                "NUM_DISPLAY_CIRCLES または "
                "SIGMA_VISUAL_MAX を小さくしてください。"
            )

        low = current_t
        high = 1.0

        # 単調な1変数方程式なので二分法で次の時刻を求めます。
        for _ in range(64):
            mid = 0.5 * (low + high)

            if overlap_equation(mid) < 0.0:
                low = mid
            else:
                high = mid

        times.append(
            0.5 * (low + high)
        )

    return times


DISPLAY_TIMES = make_display_times()


# ============================================================
# 標準偏差包絡線
# ============================================================


def sigma_envelope_point(
    t: float,
    *,
    sign: float,
    factor: float = 1.0,
) -> np.ndarray:
    """標準偏差半径の円族に対する包絡線上の点を返します。

    factor=1.0 なら通常の標準偏差包絡線、
    factor=0.5 なら 1/2 標準偏差包絡線になります。
    """
    center = mean_t(t)
    radius = visual_sigma_t(
        t,
        factor=factor,
    )
    radius_rate = visual_sigma_derivative_t(
        t,
        factor=factor,
    )

    center_speed = (
        X1_POINT[0]
        - SOURCE_MEAN[0]
    )

    # 円族とその t 微分を同時に満たす接触点を計算します。
    x_offset = (
        -radius
        * radius_rate
        / center_speed
    )

    y_squared = max(
        radius**2
        - x_offset**2,
        0.0,
    )

    y_offset = (
        sign
        * np.sqrt(y_squared)
    )

    return np.array(
        [
            center[0] + x_offset,
            ROW_Y + y_offset,
            0.0,
        ]
    )


def make_sigma_envelope_lines(
    *,
    factor: float,
    color: ManimColor,
    width: float,
    opacity: float,
) -> VGroup:
    """指定した標準偏差倍率に対応する上下の直線包絡線を作ります。

    標準偏差半径は時間に対して線形なので、
    円族の包絡線も X_1 に向かう直線になります。
    """

    upper_envelope = Line(
        sigma_envelope_point(0.0, sign=+1.0, factor=factor),
        sigma_envelope_point(1.0, sign=+1.0, factor=factor),
        color=color,
        stroke_width=width,
        stroke_opacity=opacity,
    )

    lower_envelope = Line(
        sigma_envelope_point(0.0, sign=-1.0, factor=factor),
        sigma_envelope_point(1.0, sign=-1.0, factor=factor),
        color=color,
        stroke_width=width,
        stroke_opacity=opacity,
    )

    return VGroup(
        upper_envelope,
        lower_envelope,
    )


# ============================================================
# 分布の描画
# ============================================================


def make_isotropic_distribution(
    *,
    mean: np.ndarray,
    sigma_radius: float,
    is_source: bool,
) -> VGroup:
    """標準偏差半径に基づく等方的な分布の模式図を作ります。"""

    fill_color = (
        SOURCE_FILL
        if is_source
        else MID_FILL
    )

    # 左端の source 分布だけ補助円を減らします。
    auxiliary_multipliers = (
        SOURCE_AUXILIARY_RADIUS_MULTIPLIERS
        if is_source
        else GENERAL_AUXILIARY_RADIUS_MULTIPLIERS
    )

    group = VGroup()

    # --------------------------------------------------------
    # 中心付近の薄い塗りつぶし円
    # --------------------------------------------------------

    inner_disk = Circle(
        radius=(
            0.55
            * sigma_radius
        )
    )

    inner_disk.set_stroke(
        color=VERY_FAINT,
        width=INNER_DISK_STROKE_WIDTH,
        opacity=INNER_DISK_STROKE_OPACITY,
    )

    inner_disk.set_fill(
        color=fill_color,
        opacity=(
            INNER_DISK_FILL_SOURCE_OPACITY
            if is_source
            else INNER_DISK_FILL_MID_OPACITY
        ),
    )

    inner_disk.move_to(
        [
            mean[0],
            mean[1],
            0.0,
        ]
    )

    group.add(
        inner_disk
    )

    # --------------------------------------------------------
    # 薄い補助円
    # --------------------------------------------------------

    for multiplier in auxiliary_multipliers:
        circle = Circle(
            radius=(
                multiplier
                * sigma_radius
            )
        )

        circle.set_stroke(
            color=MUTED,
            width=AUXILIARY_CIRCLE_WIDTH,
            opacity=AUXILIARY_CIRCLE_OPACITY,
        )

        circle.set_fill(
            color=fill_color,
            opacity=0.0,
        )

        circle.move_to(
            [
                mean[0],
                mean[1],
                0.0,
            ]
        )

        group.add(
            circle
        )

    # --------------------------------------------------------
    # 標準偏差そのものを表す青い円
    # --------------------------------------------------------

    sigma_circle = Circle(
        radius=(
            EMPHASIZED_RADIUS_MULTIPLIER
            * sigma_radius
        )
    )

    sigma_circle.set_stroke(
        color=ACCENT,
        width=SIGMA_CIRCLE_WIDTH,
        opacity=SIGMA_CIRCLE_OPACITY,
    )

    sigma_circle.set_fill(
        color=fill_color,
        opacity=0.0,
    )

    sigma_circle.move_to(
        [
            mean[0],
            mean[1],
            0.0,
        ]
    )

    group.add(
        sigma_circle
    )

    # --------------------------------------------------------
    # 各分布の平均位置
    # --------------------------------------------------------

    center_dot = Dot(
        [
            mean[0],
            mean[1],
            0.0,
        ],
        radius=CENTER_DOT_RADIUS,
        color=(
            INK
            if is_source
            else MUTED
        ),
    )

    if is_source:
        center_dot.set_fill(
            INK,
            opacity=1.0,
        )
    else:
        center_dot.set_fill(
            MUTED,
            opacity=FAINT_CENTER_DOT_OPACITY,
        )

    group.add(
        center_dot
    )

    return group


# ============================================================
# 矢印
# ============================================================


def make_gap_arrow(
    start_point: np.ndarray,
    target_point: np.ndarray,
    *,
    end_gap: float,
    color: ManimColor,
    stroke_width: float,
    tip_length: float = ARROW_TIP_LENGTH,
) -> Arrow:
    """終点の点と矢印先端が重ならないよう少し隙間を空けます。"""

    direction = (
        target_point
        - start_point
    )

    direction = (
        direction
        / np.linalg.norm(direction)
    )

    arrow_end = (
        target_point
        - end_gap
        * direction
    )

    return Arrow(
        start=start_point,
        end=arrow_end,
        buff=0.0,
        color=color,
        stroke_width=stroke_width,
        tip_length=tip_length,
        max_tip_length_to_length_ratio=10.0,
        max_stroke_width_to_length_ratio=10.0,
    )


# ============================================================
# 上段・下段で共通する CondOT 背景
# ============================================================


def make_condot_background(
    *,
    source_label_shift: tuple[float, float],
    x1_label_shift: tuple[float, float],
) -> VGroup:
    """上段・下段で完全に共通の CondOT 背景を作ります。"""

    # --------------------------------------------------------
    # 平均直線
    # --------------------------------------------------------

    mean_line = Line(
        [
            SOURCE_MEAN[0],
            SOURCE_MEAN[1],
            0.0,
        ],
        [
            X1_POINT[0],
            X1_POINT[1],
            0.0,
        ],
        color=ACCENT,
        stroke_width=MEAN_LINE_WIDTH,
        stroke_opacity=MEAN_LINE_OPACITY,
    )

    mean_line.set_z_index(
        1
    )

    # --------------------------------------------------------
    # 通常の標準偏差包絡線
    # --------------------------------------------------------

    sigma_envelopes = make_sigma_envelope_lines(
        factor=1.0,
        color=ACCENT,
        width=ENVELOPE_WIDTH,
        opacity=ENVELOPE_OPACITY,
    )

    sigma_envelopes.set_z_index(
        0
    )

    # --------------------------------------------------------
    # 時間方向に並べる分布
    # --------------------------------------------------------

    distributions = VGroup()

    for index, t in enumerate(
        DISPLAY_TIMES
    ):
        distribution = make_isotropic_distribution(
            mean=mean_t(t),
            sigma_radius=visual_sigma_t(t),
            is_source=(index == 0),
        )

        distributions.add(
            distribution
        )

    distributions.set_z_index(
        0
    )

    # --------------------------------------------------------
    # source 側の点とラベル
    # --------------------------------------------------------

    source_dot = Dot(
        [
            SOURCE_MEAN[0],
            SOURCE_MEAN[1],
            0.0,
        ],
        radius=ENDPOINT_DOT_RADIUS,
        color=INK,
    )

    source_dot.set_z_index(
        5
    )

    source_label = MathTex(
        r"0",
        font_size=26,
        color=INK,
    ).next_to(
        source_dot,
        LEFT,
        buff=0.12,
    )

    source_label.shift(
        shift_vector(
            source_label_shift
        )
    )

    source_label.set_z_index(
        7
    )

    # --------------------------------------------------------
    # X_1 側の点とラベル
    # --------------------------------------------------------

    x1_dot = Dot(
        [
            X1_POINT[0],
            X1_POINT[1],
            0.0,
        ],
        radius=ENDPOINT_DOT_RADIUS,
        color=INK,
    )

    x1_dot.set_z_index(
        5
    )

    x1_label = MathTex(
        r"X_1",
        font_size=26,
        color=INK,
    ).next_to(
        x1_dot,
        DOWN + RIGHT,
        buff=0.12,
    )

    x1_label.shift(
        shift_vector(
            x1_label_shift
        )
    )

    x1_label.set_z_index(
        7
    )

    return VGroup(
        sigma_envelopes,
        mean_line,
        distributions,
        source_dot,
        source_label,
        x1_dot,
        x1_label,
    )


# ============================================================
# 上段
# ============================================================


def make_top_panel() -> VGroup:
    r"""上段の \hat{X}_h と \hat{t}_h の誤差を表す図を作ります。"""

    base = make_condot_background(
        source_label_shift=TOP_SOURCE_LABEL_SHIFT,
        x1_label_shift=TOP_X1_LABEL_SHIFT,
    )

    # --------------------------------------------------------
    # t_h X_1 の位置
    # --------------------------------------------------------

    tx1_point = np.array(
        [
            mean_t(T_SELECTED)[0],
            mean_t(T_SELECTED)[1],
            0.0,
        ]
    )

    selected_sigma_radius = visual_sigma_t(
        T_SELECTED
    )

    # --------------------------------------------------------
    # \hat{X}_h の位置
    # --------------------------------------------------------

    xhat_point = np.array(
        [
            tx1_point[0],
            (
                tx1_point[1]
                + XHAT_VERTICAL_SIGMA_MULTIPLIER
                * selected_sigma_radius
            ),
            0.0,
        ]
    )

    xhat_point = (
        xhat_point
        + shift_vector(
            TOP_XHAT_POINT_SHIFT
        )
    )

    # --------------------------------------------------------
    # \hat{t}_h の模式的な点
    # --------------------------------------------------------

    hat_t_scalar_point = (
        tx1_point
        + np.array(
            [
                THAT_SCALAR_SHIFT_RIGHT,
                0.0,
                0.0,
            ]
        )
    )

    # --------------------------------------------------------
    # \hat{X}_h
    # --------------------------------------------------------

    xhat_dot = Dot(
        xhat_point,
        radius=MAIN_DOT_RADIUS,
        color=PREDICTED_COLOR,
    )

    xhat_dot.set_z_index(
        8
    )

    xhat_label = MathTex(
        r"\hat{X}_h",
        font_size=27,
        color=INK,
    ).next_to(
        xhat_dot,
        UP,
        buff=0.05,
    )

    xhat_label.shift(
        shift_vector(
            TOP_XHAT_LABEL_SHIFT
        )
    )

    xhat_label.set_z_index(
        8
    )

    # --------------------------------------------------------
    # t_h X_1
    # --------------------------------------------------------

    tx1_dot = Dot(
        tx1_point,
        radius=MAIN_DOT_RADIUS,
        color=PREDICTED_COLOR,
    )

    tx1_dot.set_z_index(
        8
    )

    tx1_label = MathTex(
        r"t_h X_1",
        font_size=25,
        color=INK,
    ).next_to(
        tx1_dot,
        DOWN,
        buff=0.09,
    )

    tx1_label.shift(
        shift_vector(
            TOP_TX1_LABEL_SHIFT
        )
    )

    tx1_label.set_z_index(
        8
    )

    # --------------------------------------------------------
    # \hat{X}_h -> t_h X_1 の誤差矢印
    # --------------------------------------------------------

    vertical_arrow = make_gap_arrow(
        start_point=xhat_point,
        target_point=tx1_point,
        end_gap=VERTICAL_ARROW_END_GAP,
        color=LOSS_ARROW_COLOR,
        stroke_width=1.8,
    )

    vertical_arrow.set_z_index(
        7
    )

    # --------------------------------------------------------
    # \hat{t}_h
    # --------------------------------------------------------

    hat_t_scalar_dot = Dot(
        hat_t_scalar_point,
        radius=SECONDARY_DOT_RADIUS,
        color=INK,
    )

    hat_t_scalar_dot.set_z_index(
        8
    )

    hat_t_scalar_label = MathTex(
        r"\hat{t}_h",
        font_size=25,
        color=INK,
    ).next_to(
        hat_t_scalar_dot,
        DOWN,
        buff=0.09,
    )

    hat_t_scalar_label.shift(
        shift_vector(
            TOP_THAT_LABEL_SHIFT
        )
    )

    hat_t_scalar_label.set_z_index(
        8
    )

    # --------------------------------------------------------
    # \hat{t}_h -> t_h X_1 の誤差矢印
    # --------------------------------------------------------

    time_arrow = make_gap_arrow(
        start_point=hat_t_scalar_point,
        target_point=tx1_point,
        end_gap=HORIZONTAL_ARROW_END_GAP,
        color=LOSS_ARROW_COLOR,
        stroke_width=1.8,
    )

    time_arrow.set_z_index(
        7
    )

    # --------------------------------------------------------
    # 上段をまとめる
    # --------------------------------------------------------

    panel = VGroup(
        base,
        vertical_arrow,
        time_arrow,
        tx1_dot,
        tx1_label,
        hat_t_scalar_dot,
        hat_t_scalar_label,
        xhat_dot,
        xhat_label,
    )

    panel.scale(
        PANEL_SCALE
    )

    # --------------------------------------------------------
    # 上段タイトル
    # --------------------------------------------------------

    top_title = make_panel_title(
        panel,
        title_text=TOP_PANEL_TITLE_TEXT,
        font_size=TOP_PANEL_TITLE_FONT_SIZE,
        color=TOP_PANEL_TITLE_COLOR,
        shift=TOP_PANEL_TITLE_SHIFT,
    )

    panel.add(top_title)

    return panel


# ============================================================
# 下段
# ============================================================


def make_bottom_panel() -> VGroup:
    """下段の 1/2 標準偏差と終端時刻方向を表す図を作ります。"""

    base = make_condot_background(
        source_label_shift=BOTTOM_SOURCE_LABEL_SHIFT,
        x1_label_shift=BOTTOM_X1_LABEL_SHIFT,
    )

    # --------------------------------------------------------
    # 基準時刻 \hat{t}_h X_1
    # --------------------------------------------------------

    reference_point = np.array(
        [
            mean_t(T_HAT_SELECTED)[0],
            mean_t(T_HAT_SELECTED)[1],
            0.0,
        ]
    )

    x1_point = np.array(
        [
            X1_POINT[0],
            X1_POINT[1],
            0.0,
        ]
    )

    selected_sigma_radius = visual_sigma_t(
        T_HAT_SELECTED
    )

    selected_half_sigma_radius = visual_sigma_t(
        T_HAT_SELECTED,
        factor=HALF_SIGMA_RADIUS_FACTOR,
    )

    # --------------------------------------------------------
    # 1/2 標準偏差包絡線
    # --------------------------------------------------------

    half_sigma_envelopes = make_sigma_envelope_lines(
        factor=HALF_SIGMA_RADIUS_FACTOR,
        color=ACCENT,
        width=ENVELOPE_WIDTH,
        opacity=ENVELOPE_OPACITY,
    )

    half_sigma_envelopes.set_z_index(
        2
    )

    # --------------------------------------------------------
    # 選択時刻の 1/2 標準偏差円
    # --------------------------------------------------------

    half_sigma_circle = Circle(
        radius=selected_half_sigma_radius
    )

    half_sigma_circle.set_stroke(
        color=HALF_SIGMA_CIRCLE_COLOR,
        width=HALF_SIGMA_CIRCLE_WIDTH,
        opacity=HALF_SIGMA_CIRCLE_OPACITY,
    )

    half_sigma_circle.set_fill(
        color=MID_FILL,
        opacity=0.0,
    )

    half_sigma_circle.move_to(
        reference_point
    )

    half_sigma_circle.set_z_index(
        3
    )

    # --------------------------------------------------------
    # 1/2 標準偏差円のラベル
    # --------------------------------------------------------

    label_direction = unit_vector_from_angle_deg(
        HALF_SIGMA_LABEL_ANGLE_DEG
    )

    label_position = (
        reference_point
        + HALF_SIGMA_LABEL_RADIAL_FACTOR
        * selected_half_sigma_radius
        * label_direction
    )

    half_sigma_label = MathTex(
        r"\frac{1}{\sqrt{2}}\sigma_{\mathrm{CondOT}}",
        font_size=HALF_SIGMA_LABEL_FONT_SIZE,
        color=INK,
    ).move_to(
        label_position
    )

    half_sigma_label.shift(
        shift_vector(
            BOTTOM_HALF_SIGMA_LABEL_SHIFT
        )
    )

    half_sigma_label.set_z_index(
        10
    )

    # --------------------------------------------------------
    # 下段の \hat{X}_h の位置
    # --------------------------------------------------------

    direction = unit_vector_from_angle_deg(
        XHAT_DIAGONAL_ANGLE_DEG
    )

    xhat_point = (
        reference_point
        + XHAT_DIAGONAL_RADIUS_FACTOR
        * selected_sigma_radius
        * direction
    )

    xhat_point = (
        xhat_point
        + shift_vector(
            BOTTOM_XHAT_POINT_SHIFT
        )
    )

    # --------------------------------------------------------
    # 基準時刻の点
    # --------------------------------------------------------

    reference_dot = Dot(
        reference_point,
        radius=MAIN_DOT_RADIUS,
        color=PREDICTED_COLOR,
    )

    reference_dot.set_z_index(
        9
    )

    reference_label = MathTex(
        r"\hat{t}_h X_1",
        font_size=25,
        color=INK,
    ).next_to(
        reference_dot,
        DOWN,
        buff=0.08,
    )

    reference_label.shift(
        shift_vector(
            BOTTOM_REFERENCE_LABEL_SHIFT
        )
    )

    reference_label.set_z_index(
        9
    )

    # --------------------------------------------------------
    # \hat{X}_h
    # --------------------------------------------------------

    xhat_dot = Dot(
        xhat_point,
        radius=MAIN_DOT_RADIUS,
        color=PREDICTED_COLOR,
    )

    xhat_dot.set_z_index(
        9
    )

    xhat_label = MathTex(
        r"\hat{X}_h",
        font_size=27,
        color=INK,
    ).next_to(
        xhat_dot,
        UP + RIGHT,
        buff=0.03,
    )

    xhat_label.shift(
        shift_vector(
            BOTTOM_XHAT_LABEL_SHIFT
        )
    )

    xhat_label.set_z_index(
        9
    )

    # --------------------------------------------------------
    # \hat{X}_h -> \hat{t}_h X_1
    # --------------------------------------------------------

    xhat_to_t_arrow = make_gap_arrow(
        start_point=xhat_point,
        target_point=reference_point,
        end_gap=XHAT_TO_T_ARROW_END_GAP,
        color=LOSS_ARROW_COLOR,
        stroke_width=1.8,
    )

    xhat_to_t_arrow.set_z_index(
        7
    )

    # --------------------------------------------------------
    # \hat{t}_h X_1 -> X_1
    # --------------------------------------------------------

    terminal_arrow = make_gap_arrow(
        start_point=reference_point,
        target_point=x1_point,
        end_gap=T_TO_X1_ARROW_END_GAP,
        color=TERMINAL_ARROW_COLOR,
        stroke_width=2.6,
    )

    terminal_arrow.set_z_index(
        4
    )

    # --------------------------------------------------------
    # 下段をまとめる
    # --------------------------------------------------------

    panel = VGroup(
        base,
        half_sigma_envelopes,
        half_sigma_circle,
        terminal_arrow,
        xhat_to_t_arrow,
        reference_dot,
        reference_label,
        xhat_dot,
        xhat_label,
        half_sigma_label,
    )

    panel.scale(
        PANEL_SCALE
    )

    # --------------------------------------------------------
    # 下段タイトル
    # --------------------------------------------------------

    bottom_title = make_panel_title(
        panel,
        title_text=BOTTOM_PANEL_TITLE_TEXT,
        font_size=BOTTOM_PANEL_TITLE_FONT_SIZE,
        color=BOTTOM_PANEL_TITLE_COLOR,
        shift=BOTTOM_PANEL_TITLE_SHIFT,
    )

    panel.add(bottom_title)

    return panel


# ============================================================
# 上下2段を結合
# ============================================================


class ShallowFlowMatchingStandardDeviationTwoPanelFigure(
    LightScene
):
    """上下2段で構成した標準偏差ベースの SFM 図です。"""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        top_panel = make_top_panel()
        bottom_panel = make_bottom_panel()

        figure = VGroup(
            top_panel,
            bottom_panel,
        )

        # ----------------------------------------------------
        # 上下2つの図の距離
        # ----------------------------------------------------

        figure.arrange(
            DOWN,
            buff=PANEL_VERTICAL_GAP,
        )

        figure.move_to(
            [
                0.0,
                0.0,
                0.0,
            ]
        )

        self.add(
            figure
        )