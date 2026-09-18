"""Static figure for explaining the three distribution-related losses in SFM.

The background geometry is the conditional CondOT family:
- isotropic Gaussian marginals,
- linear mean path from 0 to X_1,
- linear standard-deviation envelope.

Three quantities are highlighted:
1. X_h-related discrepancy:
       \hat{X}_h -> t_h X_1
2. t_h-related discrepancy:
       \hat{t}_h -> t_h X_1
3. sigma_h-related discrepancy:
       \hat{\sigma}_h -> \sigma_h

For the sigma visualization:
- drop the vertical line from \hat{X}_h to the mean line,
- place a vertical DoubleArrow parallel to that perpendicular,
- make the DoubleArrow span from the mean line to the height of \hat{X}_h,
- draw a dashed horizontal guide through \hat{X}_h and the DoubleArrow top.
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
    DashedLine,
    Dot,
    DoubleArrow,
    Line,
    MathTex,
    ManimColor,
    VGroup,
    config,
)

from manim_research import LightScene


# ============================================================
# Wide canvas
# ============================================================

config.frame_width = 8.8
config.frame_height = 4.4


# ============================================================
# Presentation palette
# ============================================================

BACKGROUND = ManimColor("#FFFFFF")
INK = ManimColor("#1F2933")

ACCENT = ManimColor("#2D5B84")
MUTED = ManimColor("#7C8894")
VERY_FAINT = ManimColor("#C8D1DA")

SOURCE_FILL = ManimColor("#AEBFCC")
MID_FILL = ManimColor("#C9D4DE")

PREDICTED_COLOR = ManimColor("#244A6A")
LOSS_ARROW_COLOR = ManimColor("#355F86")


# ============================================================
# Geometry
# ============================================================

ROW_Y = 0.00

SOURCE_MEAN = np.array([-1.95, ROW_Y])
X1_POINT = np.array([1.95, ROW_Y])

NUM_DISPLAY_CIRCLES = 6
OVERLAP_RATIO = 0.22
SIGMA_VISUAL_MAX = 0.62

FAINT_RADIUS_MULTIPLIERS = [
    0.55,
    1.45,
    1.90,
]

EMPHASIZED_RADIUS_MULTIPLIER = 1.00

FIGURE_SCALE = 1.18


# ============================================================
# Selected geometry for the three losses
# ============================================================

T_SELECTED = 0.30

# \hat{X}_h is above t_h X_1.
XHAT_VERTICAL_SIGMA = 1.30

# Separate schematic point for \hat{t}_h.
THAT_SCALAR_SHIFT_RIGHT = 0.95


# ============================================================
# Styling for background distributions
# ============================================================

AUXILIARY_CIRCLE_OPACITY = 0.18
AUXILIARY_CIRCLE_WIDTH = 0.85

SIGMA_CIRCLE_OPACITY = 0.42
SIGMA_CIRCLE_WIDTH = 1.20

TANGENT_OPACITY = 0.36
TANGENT_WIDTH = 0.90

MEAN_LINE_OPACITY = 0.55
MEAN_LINE_WIDTH = 1.35

FAINT_CENTER_DOT_OPACITY = 0.28


# ============================================================
# Point sizes
# ============================================================

MAIN_DOT_RADIUS = 0.040
ENDPOINT_DOT_RADIUS = 0.036
CENTER_DOT_RADIUS = 0.018


# ============================================================
# Loss-arrow styling
# ============================================================

VERTICAL_ARROW_END_GAP = 0.060
HORIZONTAL_ARROW_END_GAP = 0.065

ARROW_TIP_LENGTH = 0.11


# ============================================================
# Sigma-loss visualization
# ============================================================

# Keep the sigma DoubleArrow close to the original
# perpendicular through \hat{X}_h.
SIGMA_ARROW_X_SHIFT = 0.32

# Dashed horizontal guide extends slightly beyond both the DoubleArrow
# and \hat{X}_h so that the equality of the two heights is clear.
SIGMA_GUIDE_LEFT_EXTENSION = 0.13
SIGMA_GUIDE_RIGHT_EXTENSION = 0.13

SIGMA_GUIDE_DASH_LENGTH = 0.030
SIGMA_GUIDE_DASHED_RATIO = 0.58
SIGMA_GUIDE_WIDTH = 1.15
SIGMA_GUIDE_OPACITY = 0.82

SIGMA_DOUBLE_ARROW_WIDTH = 1.65
SIGMA_DOUBLE_ARROW_OPACITY = 0.82
SIGMA_DOUBLE_ARROW_TIP_LENGTH = 0.085

SIGMA_LABEL_FONT_SIZE = 24
SIGMA_LABEL_BUFF = 0.09


# ============================================================
# Schedules
# ============================================================

def mean_t(t: float) -> np.ndarray:
    """Mean moves linearly from 0 to X_1."""
    return (
        (1.0 - t) * SOURCE_MEAN
        + t * X1_POINT
    )


def visual_sigma_t(t: float) -> float:
    """Displayed standard deviation changes linearly with time."""
    return SIGMA_VISUAL_MAX * (1.0 - t)


def make_display_times() -> list[float]:
    """Choose times with constant fractional overlap."""
    length = (
        X1_POINT[0]
        - SOURCE_MEAN[0]
    )

    radius_scale = SIGMA_VISUAL_MAX
    rho = OVERLAP_RATIO

    denominator = (
        length
        + radius_scale
        - rho * radius_scale
    )

    q = (
        length
        - radius_scale
    ) / denominator

    if not 0.0 < q < 1.0:
        raise ValueError(
            "OVERLAP_RATIO gives an invalid time schedule."
        )

    s_values = [
        q**index
        for index in range(NUM_DISPLAY_CIRCLES)
    ]

    return [
        1.0 - s
        for s in s_values
    ]


DISPLAY_TIMES = make_display_times()


# ============================================================
# Tangent geometry
# ============================================================

def tangent_slope() -> float:
    """Magnitude of the common tangent slope."""
    line_length = (
        X1_POINT[0]
        - SOURCE_MEAN[0]
    )

    radius_ratio = (
        SIGMA_VISUAL_MAX
        / line_length
    )

    return (
        radius_ratio
        / np.sqrt(
            1.0 - radius_ratio**2
        )
    )


def upper_tangent_y(x: float) -> float:
    """Y coordinate of the upper sigma tangent at x."""
    slope = tangent_slope()

    return (
        ROW_Y
        - slope
        * (x - X1_POINT[0])
    )


# ============================================================
# Drawing helpers
# ============================================================

def make_isotropic_distribution(
    *,
    mean: np.ndarray,
    sigma: float,
    is_source: bool,
) -> VGroup:
    """Draw one isotropic Gaussian with subdued visual weight."""
    fill_color = (
        SOURCE_FILL
        if is_source
        else MID_FILL
    )

    group = VGroup()

    # --------------------------------------------------------
    # Faint filled center
    # --------------------------------------------------------

    inner_disk = Circle(
        radius=0.55 * sigma
    )

    inner_disk.set_stroke(
        color=VERY_FAINT,
        width=0.75,
        opacity=0.16,
    )

    inner_disk.set_fill(
        color=fill_color,
        opacity=(
            0.11
            if is_source
            else 0.08
        ),
    )

    inner_disk.move_to(
        [
            mean[0],
            mean[1],
            0.0,
        ]
    )

    group.add(inner_disk)

    # --------------------------------------------------------
    # Faint auxiliary contours
    # --------------------------------------------------------

    for multiplier in FAINT_RADIUS_MULTIPLIERS:
        circle = Circle(
            radius=multiplier * sigma
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

        group.add(circle)

    # --------------------------------------------------------
    # 1-sigma circle
    # --------------------------------------------------------

    sigma_circle = Circle(
        radius=(
            EMPHASIZED_RADIUS_MULTIPLIER
            * sigma
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

    group.add(sigma_circle)

    # --------------------------------------------------------
    # Mean marker
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

    group.add(center_dot)

    return group


def make_common_tangent_lines() -> VGroup:
    """Create faint common tangents."""
    slope = tangent_slope()

    x_left = (
        SOURCE_MEAN[0]
        - 0.55
    )

    x_right = X1_POINT[0]

    y_upper_left = (
        ROW_Y
        - slope
        * (
            x_left
            - X1_POINT[0]
        )
    )

    y_lower_left = (
        ROW_Y
        + slope
        * (
            x_left
            - X1_POINT[0]
        )
    )

    upper_tangent = Line(
        [
            x_left,
            y_upper_left,
            0.0,
        ],
        [
            x_right,
            ROW_Y,
            0.0,
        ],
        color=ACCENT,
        stroke_width=TANGENT_WIDTH,
        stroke_opacity=TANGENT_OPACITY,
    )

    lower_tangent = Line(
        [
            x_left,
            y_lower_left,
            0.0,
        ],
        [
            x_right,
            ROW_Y,
            0.0,
        ],
        color=ACCENT,
        stroke_width=TANGENT_WIDTH,
        stroke_opacity=TANGENT_OPACITY,
    )

    return VGroup(
        upper_tangent,
        lower_tangent,
    )


def make_gap_arrow(
    start_point: np.ndarray,
    target_point: np.ndarray,
    *,
    end_gap: float,
    color: ManimColor,
    stroke_width: float,
    tip_length: float = ARROW_TIP_LENGTH,
) -> Arrow:
    """Arrow toward target_point with a terminal gap."""
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
        - end_gap * direction
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
# Figure
# ============================================================

class ShallowFlowMatchingThreeDistributionLossesFigure(
    LightScene
):
    """Figure for explaining three distribution-related losses in SFM."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --------------------------------------------------------
        # Base CondOT geometry
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

        mean_line.set_z_index(1)

        tangents = make_common_tangent_lines()
        tangents.set_z_index(0)

        distributions = VGroup()

        for index, t in enumerate(
            DISPLAY_TIMES
        ):
            distribution = make_isotropic_distribution(
                mean=mean_t(t),
                sigma=visual_sigma_t(t),
                is_source=(index == 0),
            )

            distributions.add(
                distribution
            )

        distributions.set_z_index(0)

        # --------------------------------------------------------
        # Endpoints
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
        source_dot.set_z_index(5)

        source_label = MathTex(
            r"0",
            font_size=26,
            color=INK,
        ).next_to(
            source_dot,
            LEFT,
            buff=0.12,
        )
        source_label.set_z_index(7)

        x1_dot = Dot(
            [
                X1_POINT[0],
                X1_POINT[1],
                0.0,
            ],
            radius=ENDPOINT_DOT_RADIUS,
            color=INK,
        )
        x1_dot.set_z_index(5)

        x1_label = MathTex(
            r"X_1",
            font_size=26,
            color=INK,
        ).next_to(
            x1_dot,
            DOWN + RIGHT,
            buff=0.12,
        )
        x1_label.set_z_index(7)

        # --------------------------------------------------------
        # Selected geometry
        # --------------------------------------------------------

        tx1_point = np.array(
            [
                mean_t(T_SELECTED)[0],
                mean_t(T_SELECTED)[1],
                0.0,
            ]
        )

        sigma_selected = visual_sigma_t(
            T_SELECTED
        )

        xhat_point = np.array(
            [
                tx1_point[0],
                tx1_point[1]
                + XHAT_VERTICAL_SIGMA
                * sigma_selected,
                0.0,
            ]
        )

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
        # X_h loss
        # --------------------------------------------------------

        xhat_dot = Dot(
            xhat_point,
            radius=MAIN_DOT_RADIUS,
            color=PREDICTED_COLOR,
        )
        xhat_dot.set_z_index(8)

        xhat_label = MathTex(
            r"\hat{X}_h",
            font_size=27,
            color=INK,
        ).next_to(
            xhat_dot,
            UP,
            buff=0.05,
        )
        xhat_label.set_z_index(8)

        tx1_dot = Dot(
            tx1_point,
            radius=MAIN_DOT_RADIUS,
            color=PREDICTED_COLOR,
        )
        tx1_dot.set_z_index(8)

        tx1_label = MathTex(
            r"t_h X_1",
            font_size=25,
            color=INK,
        ).next_to(
            tx1_dot,
            DOWN,
            buff=0.09,
        )
        tx1_label.set_z_index(8)

        vertical_arrow = make_gap_arrow(
            start_point=xhat_point,
            target_point=tx1_point,
            end_gap=VERTICAL_ARROW_END_GAP,
            color=LOSS_ARROW_COLOR,
            stroke_width=1.8,
        )
        vertical_arrow.set_z_index(7)

        # --------------------------------------------------------
        # t_h loss
        # --------------------------------------------------------

        hat_t_scalar_dot = Dot(
            hat_t_scalar_point,
            radius=0.024,
            color=INK,
        )
        hat_t_scalar_dot.set_z_index(8)

        hat_t_scalar_label = MathTex(
            r"\hat{t}_h",
            font_size=25,
            color=INK,
        ).next_to(
            hat_t_scalar_dot,
            DOWN,
            buff=0.09,
        )
        hat_t_scalar_label.set_z_index(8)

        time_arrow = make_gap_arrow(
            start_point=hat_t_scalar_point,
            target_point=tx1_point,
            end_gap=HORIZONTAL_ARROW_END_GAP,
            color=LOSS_ARROW_COLOR,
            stroke_width=1.8,
        )
        time_arrow.set_z_index(7)

        # --------------------------------------------------------
        # sigma_h loss
        #
        # The DoubleArrow is parallel to the perpendicular dropped
        # from \hat{X}_h and has exactly the same vertical span:
        # from the mean line up to the height of \hat{X}_h.
        #
        # A dashed horizontal guide passes through both the top of
        # the DoubleArrow and \hat{X}_h, making that equality visible.
        # --------------------------------------------------------

        sigma_arrow_x = (
            tx1_point[0]
            - SIGMA_ARROW_X_SHIFT
        )

        sigma_arrow_bottom = np.array(
            [
                sigma_arrow_x,
                ROW_Y,
                0.0,
            ]
        )

        sigma_arrow_top = np.array(
            [
                sigma_arrow_x,
                xhat_point[1],
                0.0,
            ]
        )

        sigma_guide = DashedLine(
            start=[
                sigma_arrow_x
                - SIGMA_GUIDE_LEFT_EXTENSION,
                xhat_point[1],
                0.0,
            ],
            end=[
                xhat_point[0]
                + SIGMA_GUIDE_RIGHT_EXTENSION,
                xhat_point[1],
                0.0,
            ],
            dash_length=SIGMA_GUIDE_DASH_LENGTH,
            dashed_ratio=SIGMA_GUIDE_DASHED_RATIO,
            color=LOSS_ARROW_COLOR,
            stroke_width=SIGMA_GUIDE_WIDTH,
            stroke_opacity=SIGMA_GUIDE_OPACITY,
        )
        sigma_guide.set_z_index(7)

        sigma_double_arrow = DoubleArrow(
            start=sigma_arrow_bottom,
            end=sigma_arrow_top,
            buff=0.0,
            color=LOSS_ARROW_COLOR,
            stroke_width=SIGMA_DOUBLE_ARROW_WIDTH,
            tip_length=SIGMA_DOUBLE_ARROW_TIP_LENGTH,
            max_tip_length_to_length_ratio=10.0,
            max_stroke_width_to_length_ratio=10.0,
        )

        sigma_double_arrow.set_stroke(
            color=LOSS_ARROW_COLOR,
            width=SIGMA_DOUBLE_ARROW_WIDTH,
            opacity=SIGMA_DOUBLE_ARROW_OPACITY,
        )
        sigma_double_arrow.set_z_index(8)

        sigma_label = MathTex(
            r"\hat{\sigma}_h \rightarrow \sigma_h",
            font_size=SIGMA_LABEL_FONT_SIZE,
            color=INK,
        ).next_to(
            sigma_double_arrow,
            LEFT,
            buff=SIGMA_LABEL_BUFF,
        )
        sigma_label.shift(
            UP * 0.04
        )
        sigma_label.set_z_index(8)

        # --------------------------------------------------------
        # Assemble
        # --------------------------------------------------------

        figure = VGroup(
            tangents,
            mean_line,
            distributions,
            source_dot,
            source_label,
            x1_dot,
            x1_label,
            sigma_guide,
            sigma_double_arrow,
            sigma_label,
            vertical_arrow,
            time_arrow,
            tx1_dot,
            tx1_label,
            hat_t_scalar_dot,
            hat_t_scalar_label,
            xhat_dot,
            xhat_label,
        )

        figure.scale(
            FIGURE_SCALE
        )

        figure.move_to(
            [
                0.0,
                -0.06,
                0.0,
            ]
        )

        self.add(
            figure
        )