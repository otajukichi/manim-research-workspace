"""Static figure for explaining the teacher signal in Shallow Flow Matching.

This figure is based on the conditional CondOT geometry:
- isotropic Gaussian marginals along the straight mean path from 0 to X_1,
- common tangents showing the linear radius schedule.

On top of that, we add
- a predicted intermediate point \\hat{X}_h,
- a perpendicular dropped from \\hat{X}_h to the mean line,
- the corresponding parameter location t_h on the line.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circle,
    DashedLine,
    Dot,
    Line,
    MathTex,
    ManimColor,
    Polygon,
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


# ============================================================
# Geometry
# ============================================================

ROW_Y = 0.00

# Internal geometry:
# keep 0 and X_1 somewhat close to enlarge the tangent opening,
# then enlarge the whole figure uniformly.
SOURCE_MEAN = np.array([-1.95, ROW_Y])
X1_POINT = np.array([1.95, ROW_Y])

# Number of displayed Gaussian marginals.
NUM_DISPLAY_CIRCLES = 6

# Constant fractional overlap between neighboring emphasized circles.
OVERLAP_RATIO = 0.22

# Maximum displayed standard deviation.
SIGMA_VISUAL_MAX = 0.62

FAINT_RADIUS_MULTIPLIERS = [
    0.55,
    1.45,
    1.90,
]
EMPHASIZED_RADIUS_MULTIPLIER = 1.00

FIGURE_SCALE = 1.18

# ------------------------------------------------------------
# Predicted intermediate point:
# move it a bit to the left by choosing a smaller T_H.
# This keeps the perpendicular relation intact while avoiding
# the crowded central region.
# ------------------------------------------------------------
T_H = 0.28
XHAT_VERTICAL_SIGMA = 1.28

# Projection-line appearance
PROJECTION_DASH_LENGTH = 0.022
PROJECTION_DASHED_RATIO = 0.68
PROJECTION_STROKE_WIDTH = 1.35
PROJECTION_STROKE_OPACITY = 0.95

# Right-angle-marker appearance
RIGHT_ANGLE_SIZE = 0.085
RIGHT_ANGLE_STROKE_WIDTH = 1.10
RIGHT_ANGLE_STROKE_OPACITY = 0.95


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
    """Standard deviation changes linearly with time."""
    return SIGMA_VISUAL_MAX * (1.0 - t)


def make_display_times() -> list[float]:
    """Choose times with constant fractional overlap.

    For neighboring emphasized circles, the overlap width divided by the
    smaller circle radius is kept constant.
    """
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
# Drawing helpers
# ============================================================

def make_isotropic_distribution(
    *,
    mean: np.ndarray,
    sigma: float,
    is_source: bool,
) -> VGroup:
    """Draw one isotropic Gaussian schematically.

    The 1-sigma circle is emphasized.
    Other concentric circles are intentionally faint.
    """
    fill_color = (
        SOURCE_FILL
        if is_source
        else MID_FILL
    )

    group = VGroup()

    # faint filled center
    inner_disk = Circle(
        radius=0.55 * sigma
    )
    inner_disk.set_stroke(
        color=VERY_FAINT,
        width=0.8,
        opacity=0.20,
    )
    inner_disk.set_fill(
        color=fill_color,
        opacity=(
            0.12 if is_source else 0.09
        ),
    )
    inner_disk.move_to(
        [mean[0], mean[1], 0.0]
    )
    group.add(inner_disk)

    # faint auxiliary contours
    for multiplier in FAINT_RADIUS_MULTIPLIERS:
        circle = Circle(
            radius=multiplier * sigma
        )
        circle.set_stroke(
            color=MUTED,
            width=0.9,
            opacity=0.22,
        )
        circle.set_fill(
            color=fill_color,
            opacity=0.0,
        )
        circle.move_to(
            [mean[0], mean[1], 0.0]
        )
        group.add(circle)

    # emphasized 1-sigma circle
    sigma_circle = Circle(
        radius=(
            EMPHASIZED_RADIUS_MULTIPLIER
            * sigma
        )
    )
    sigma_circle.set_stroke(
        color=ACCENT,
        width=1.6,
        opacity=0.80,
    )
    sigma_circle.set_fill(
        color=fill_color,
        opacity=0.0,
    )
    sigma_circle.move_to(
        [mean[0], mean[1], 0.0]
    )
    group.add(sigma_circle)

    # mean marker
    center_dot = Dot(
        [mean[0], mean[1], 0.0],
        radius=0.020,
        color=INK,
    )
    group.add(center_dot)

    return group


def make_common_tangent_lines() -> VGroup:
    """Create common tangents of the emphasized 1-sigma circles."""
    line_length = (
        X1_POINT[0]
        - SOURCE_MEAN[0]
    )

    radius_ratio = (
        SIGMA_VISUAL_MAX
        / line_length
    )

    slope = (
        radius_ratio
        / np.sqrt(
            1.0 - radius_ratio**2
        )
    )

    x_left = SOURCE_MEAN[0] - 0.55
    x_right = X1_POINT[0]

    y_upper_left = (
        ROW_Y
        + slope
        * (x_left - X1_POINT[0])
    )
    y_lower_left = (
        ROW_Y
        - slope
        * (x_left - X1_POINT[0])
    )

    upper_tangent = Line(
        [x_left, y_upper_left, 0.0],
        [x_right, ROW_Y, 0.0],
        color=ACCENT,
        stroke_width=1.2,
        stroke_opacity=0.62,
    )

    lower_tangent = Line(
        [x_left, y_lower_left, 0.0],
        [x_right, ROW_Y, 0.0],
        color=ACCENT,
        stroke_width=1.2,
        stroke_opacity=0.62,
    )

    return VGroup(
        upper_tangent,
        lower_tangent,
    )


def make_right_angle_marker(
    foot: np.ndarray,
) -> Polygon:
    """Draw a proper right-angle marker anchored at the foot.

    The marker occupies the upper-right quadrant from the foot:
        foot -> right -> up-right -> up

    It is filled with the background color so the dashed projection line
    does not visually cut through it.
    """
    p0 = np.array([foot[0], foot[1], 0.0])
    p1 = np.array([foot[0] + RIGHT_ANGLE_SIZE, foot[1], 0.0])
    p2 = np.array([foot[0] + RIGHT_ANGLE_SIZE, foot[1] + RIGHT_ANGLE_SIZE, 0.0])
    p3 = np.array([foot[0], foot[1] + RIGHT_ANGLE_SIZE, 0.0])

    marker = Polygon(
        p0,
        p1,
        p2,
        p3,
        color=MUTED,
        stroke_width=RIGHT_ANGLE_STROKE_WIDTH,
    )
    marker.set_fill(
        BACKGROUND,
        opacity=1.0,
    )
    marker.set_stroke(
        color=MUTED,
        width=RIGHT_ANGLE_STROKE_WIDTH,
        opacity=RIGHT_ANGLE_STROKE_OPACITY,
    )
    marker.set_z_index(6)

    return marker


# ============================================================
# Figure
# ============================================================

class ShallowFlowMatchingTeacherSignalFigure(LightScene):
    """Figure for explaining the teacher signal in Shallow Flow Matching."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --------------------------------------------------------
        # Straight mean path
        # --------------------------------------------------------

        mean_line = Line(
            [SOURCE_MEAN[0], SOURCE_MEAN[1], 0.0],
            [X1_POINT[0], X1_POINT[1], 0.0],
            color=ACCENT,
            stroke_width=1.6,
            stroke_opacity=0.70,
        )
        mean_line.set_z_index(1)

        # --------------------------------------------------------
        # Gaussian marginals
        # --------------------------------------------------------

        distributions = VGroup()

        for index, t in enumerate(
            DISPLAY_TIMES
        ):
            distribution = make_isotropic_distribution(
                mean=mean_t(t),
                sigma=visual_sigma_t(t),
                is_source=(index == 0),
            )
            distributions.add(distribution)

        distributions.set_z_index(0)

        # --------------------------------------------------------
        # Endpoints
        # --------------------------------------------------------

        source_dot = Dot(
            [SOURCE_MEAN[0], SOURCE_MEAN[1], 0.0],
            radius=0.028,
            color=INK,
        )
        source_dot.set_z_index(4)

        source_label = MathTex(
            r"0",
            font_size=26,
            color=INK,
        ).next_to(
            source_dot,
            LEFT,
            buff=0.14,
        )
        source_label.set_z_index(6)

        x1_dot = Dot(
            [X1_POINT[0], X1_POINT[1], 0.0],
            radius=0.038,
            color=INK,
        )
        x1_dot.set_z_index(4)

        x1_label = MathTex(
            r"X_1",
            font_size=26,
            color=INK,
        ).next_to(
            x1_dot,
            DOWN + RIGHT,
            buff=0.12,
        )
        x1_label.set_z_index(6)

        # --------------------------------------------------------
        # Common tangents
        # --------------------------------------------------------

        tangents = make_common_tangent_lines()
        tangents.set_z_index(1)

        # --------------------------------------------------------
        # Predicted intermediate point \hat{X}_h and projection
        # --------------------------------------------------------

        foot = mean_t(T_H)
        sigma_h = visual_sigma_t(T_H)

        xhat_point = np.array(
            [
                foot[0],
                foot[1] + XHAT_VERTICAL_SIGMA * sigma_h,
                0.0,
            ]
        )

        xhat_dot = Dot(
            xhat_point,
            radius=0.042,
            color=PREDICTED_COLOR,
        )
        xhat_dot.set_z_index(6)

        xhat_label = MathTex(
            r"\hat{X}_h",
            font_size=27,
            color=INK,
        ).next_to(
            xhat_dot,
            UP + RIGHT,
            buff=0.05,
        )
        xhat_label.set_z_index(6)

        projection_line = DashedLine(
            xhat_point,
            [foot[0], foot[1], 0.0],
            dash_length=PROJECTION_DASH_LENGTH,
            dashed_ratio=PROJECTION_DASHED_RATIO,
            color=MUTED,
            stroke_width=PROJECTION_STROKE_WIDTH,
            stroke_opacity=PROJECTION_STROKE_OPACITY,
        )
        projection_line.set_z_index(3)

        foot_dot = Dot(
            [foot[0], foot[1], 0.0],
            radius=0.042,
            color=PREDICTED_COLOR,
        )
        foot_dot.set_z_index(7)

        th_label = MathTex(
            r"t_h",
            font_size=25,
            color=INK,
        ).next_to(
            foot_dot,
            DOWN,
            buff=0.10,
        )
        th_label.set_z_index(6)

        right_angle = make_right_angle_marker(
            foot
        )

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
            projection_line,
            right_angle,
            foot_dot,
            th_label,
            xhat_dot,
            xhat_label,
        )

        figure.scale(FIGURE_SCALE)
        figure.move_to([0.0, -0.10, 0.0])

        self.add(figure)