"""Static figure for explaining why distribution comparison becomes simple.

The conditional CondOT geometry is kept as context:
- the straight mean path from 0 to X_1,
- the common tangent envelope showing the standard-deviation schedule.

Instead of displaying the full family of Gaussian marginals, this figure
shows only two isotropic Gaussian distributions:

1. the reference distribution centered at \\hat{t}X_1,
2. a predicted distribution centered at \\hat{\\mu}.

The two distributions have exactly the same displayed standard deviation.
Only their means differ.

This visually represents the idea that once equal isotropic covariance is
guaranteed, distribution comparison reduces to comparison of the means.
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

MID_FILL = ManimColor("#C9D4DE")

PREDICTED_COLOR = ManimColor("#244A6A")
LOSS_ARROW_COLOR = ManimColor("#355F86")


# ============================================================
# Geometry
# ============================================================

ROW_Y = 0.00

SOURCE_MEAN = np.array(
    [
        -1.95,
        ROW_Y,
    ]
)

X1_POINT = np.array(
    [
        1.95,
        ROW_Y,
    ]
)

SIGMA_VISUAL_MAX = 0.62

FIGURE_SCALE = 1.18


# ============================================================
# Selected comparison point
# ============================================================

T_HAT = 0.28

# The predicted mean is displaced from \hat{t}X_1.
# This is intentionally not a perpendicular construction.
MUHAT_RADIUS_FACTOR = 1.32
MUHAT_ANGLE_DEG = 52.0


# ============================================================
# Point sizes
# ============================================================

REFERENCE_DOT_RADIUS = 0.042
PREDICTED_DOT_RADIUS = 0.042

SOURCE_DOT_RADIUS = 0.028
X1_DOT_RADIUS = 0.038


# ============================================================
# Distribution styling
#
# Match the subdued styling used in the previous figure.
# ============================================================

FAINT_RADIUS_MULTIPLIERS = [
    0.55,
    1.45,
    1.90,
]

EMPHASIZED_RADIUS_MULTIPLIER = 1.00

AUXILIARY_CIRCLE_WIDTH = 0.90
AUXILIARY_CIRCLE_OPACITY = 0.22

SIGMA_CIRCLE_WIDTH = 1.20
SIGMA_CIRCLE_OPACITY = 0.42

INNER_DISK_STROKE_WIDTH = 0.80
INNER_DISK_STROKE_OPACITY = 0.20
INNER_DISK_FILL_OPACITY = 0.09


# ============================================================
# Tangent styling
#
# Keep the subdued tangent styling from the previous figure.
# ============================================================

TANGENT_WIDTH = 0.90
TANGENT_OPACITY = 0.36


# ============================================================
# Mean-line styling
#
# Keep the original mean line.
# ============================================================

MEAN_LINE_WIDTH = 1.60
MEAN_LINE_OPACITY = 0.70


# ============================================================
# Comparison-arrow styling
# ============================================================

ARROW_END_GAP = 0.050
ARROW_TIP_LENGTH = 0.11


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
    """Displayed standard deviation shrinks linearly with time."""
    return (
        SIGMA_VISUAL_MAX
        * (1.0 - t)
    )


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
            1.0
            - radius_ratio**2
        )
    )


def make_common_tangent_lines() -> VGroup:
    """Create the common tangent envelope."""
    slope = tangent_slope()

    x_left = (
        SOURCE_MEAN[0]
        - 0.55
    )

    x_right = X1_POINT[0]

    y_upper_left = (
        ROW_Y
        + slope
        * (
            x_left
            - X1_POINT[0]
        )
    )

    y_lower_left = (
        ROW_Y
        - slope
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


# ============================================================
# Distribution drawing
# ============================================================

def make_comparison_distribution(
    *,
    mean: np.ndarray,
    sigma: float,
) -> VGroup:
    """Draw one subdued isotropic Gaussian distribution.

    The center dot is intentionally not created here.
    The two important mean locations are drawn separately as
    \hat{t}X_1 and \hat{\mu}.
    """

    group = VGroup()

    # --------------------------------------------------------
    # Faint filled center region
    # --------------------------------------------------------

    inner_disk = Circle(
        radius=(
            0.55
            * sigma
        )
    )

    inner_disk.set_stroke(
        color=VERY_FAINT,
        width=INNER_DISK_STROKE_WIDTH,
        opacity=INNER_DISK_STROKE_OPACITY,
    )

    inner_disk.set_fill(
        color=MID_FILL,
        opacity=INNER_DISK_FILL_OPACITY,
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
    # Auxiliary contours
    # --------------------------------------------------------

    for multiplier in FAINT_RADIUS_MULTIPLIERS:
        circle = Circle(
            radius=(
                multiplier
                * sigma
            )
        )

        circle.set_stroke(
            color=MUTED,
            width=AUXILIARY_CIRCLE_WIDTH,
            opacity=AUXILIARY_CIRCLE_OPACITY,
        )

        circle.set_fill(
            color=MID_FILL,
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
        color=MID_FILL,
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

    return group


# ============================================================
# Utility
# ============================================================

def unit_vector_from_angle_deg(
    angle_deg: float,
) -> np.ndarray:
    """2D unit vector with a prescribed angle."""
    theta = np.deg2rad(
        angle_deg
    )

    return np.array(
        [
            np.cos(theta),
            np.sin(theta),
            0.0,
        ]
    )


def make_gap_arrow(
    *,
    start_point: np.ndarray,
    target_point: np.ndarray,
    end_gap: float,
) -> Arrow:
    """Arrow from start_point toward target_point with a terminal gap."""
    direction = (
        target_point
        - start_point
    )

    direction = (
        direction
        / np.linalg.norm(
            direction
        )
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
        color=LOSS_ARROW_COLOR,
        stroke_width=1.8,
        tip_length=ARROW_TIP_LENGTH,
        max_tip_length_to_length_ratio=0.20,
        max_stroke_width_to_length_ratio=10.0,
    )


# ============================================================
# Figure
# ============================================================

class CSTMSFMDistributionComparisonEqualVarianceFigure(
    LightScene
):
    """Compare two equal-variance Gaussian distributions through their means."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --------------------------------------------------------
        # Mean path
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

        # --------------------------------------------------------
        # Common tangent envelope
        # --------------------------------------------------------

        tangents = make_common_tangent_lines()

        tangents.set_z_index(1)

        # --------------------------------------------------------
        # Reference distribution centered at \hat{t}X_1
        # --------------------------------------------------------

        reference_mean_2d = mean_t(
            T_HAT
        )

        reference_point = np.array(
            [
                reference_mean_2d[0],
                reference_mean_2d[1],
                0.0,
            ]
        )

        sigma_hat = visual_sigma_t(
            T_HAT
        )

        reference_distribution = make_comparison_distribution(
            mean=reference_mean_2d,
            sigma=sigma_hat,
        )

        reference_distribution.set_z_index(
            0
        )

        # --------------------------------------------------------
        # Predicted mean \hat{\mu}
        # --------------------------------------------------------

        direction = unit_vector_from_angle_deg(
            MUHAT_ANGLE_DEG
        )

        muhat_point = (
            reference_point
            + MUHAT_RADIUS_FACTOR
            * sigma_hat
            * direction
        )

        muhat_mean_2d = np.array(
            [
                muhat_point[0],
                muhat_point[1],
            ]
        )

        # --------------------------------------------------------
        # Predicted distribution
        #
        # IMPORTANT:
        # exactly the same sigma as the reference distribution.
        # Only its center is shifted to \hat{\mu}.
        # --------------------------------------------------------

        predicted_distribution = make_comparison_distribution(
            mean=muhat_mean_2d,
            sigma=sigma_hat,
        )

        predicted_distribution.set_z_index(
            0
        )

        # --------------------------------------------------------
        # Endpoints of the original CondOT mean path
        # --------------------------------------------------------

        source_dot = Dot(
            [
                SOURCE_MEAN[0],
                SOURCE_MEAN[1],
                0.0,
            ],
            radius=SOURCE_DOT_RADIUS,
            color=INK,
        )

        source_dot.set_z_index(
            8
        )

        source_label = MathTex(
            r"0",
            font_size=26,
            color=INK,
        ).next_to(
            source_dot,
            LEFT,
            buff=0.14,
        )

        source_label.set_z_index(
            8
        )

        x1_dot = Dot(
            [
                X1_POINT[0],
                X1_POINT[1],
                0.0,
            ],
            radius=X1_DOT_RADIUS,
            color=INK,
        )

        x1_dot.set_z_index(
            8
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

        x1_label.set_z_index(
            8
        )

        # --------------------------------------------------------
        # Reference mean marker
        # --------------------------------------------------------

        reference_dot = Dot(
            reference_point,
            radius=REFERENCE_DOT_RADIUS,
            color=PREDICTED_COLOR,
        )

        reference_dot.set_z_index(
            9
        )

        reference_label = MathTex(
            r"\hat{t}X_1",
            font_size=27,
            color=INK,
        ).next_to(
            reference_dot,
            DOWN,
            buff=0.05,
        )

        reference_label.set_z_index(
            9
        )

        # --------------------------------------------------------
        # Predicted mean marker
        # --------------------------------------------------------

        muhat_dot = Dot(
            muhat_point,
            radius=PREDICTED_DOT_RADIUS,
            color=PREDICTED_COLOR,
        )

        muhat_dot.set_z_index(
            9
        )

        muhat_label = MathTex(
            r"\hat{\mu}",
            font_size=27,
            color=INK,
        ).next_to(
            muhat_dot,
            UP + RIGHT,
            buff=0.03,
        )

        muhat_label.set_z_index(
            9
        )

        # --------------------------------------------------------
        # Mean discrepancy
        # --------------------------------------------------------

        discrepancy_arrow = make_gap_arrow(
            start_point=muhat_point,
            target_point=reference_point,
            end_gap=ARROW_END_GAP,
        )

        discrepancy_arrow.set_z_index(
            7
        )

        # --------------------------------------------------------
        # Assemble
        # --------------------------------------------------------

        figure = VGroup(
            reference_distribution,
            predicted_distribution,
            tangents,
            mean_line,
            source_dot,
            source_label,
            x1_dot,
            x1_label,
            discrepancy_arrow,
            reference_dot,
            reference_label,
            muhat_dot,
            muhat_label,
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