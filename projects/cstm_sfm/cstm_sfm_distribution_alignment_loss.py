"""Static figure for explaining the distribution-alignment loss in CSTM-SFM.

This figure is based on the same conditional CondOT geometry:
- isotropic Gaussian marginals along the straight mean path from 0 to X_1,
- common tangents showing the linear radius schedule.

On top of that, we add
- a reference mean location \\hat{t} X_1 on the mean line,
- a predicted mean \\hat{\\mu} near the corresponding intermediate Gaussian,
- an arrow from \\hat{\\mu} to \\hat{t}X_1.

Important:
Unlike the previous Shallow Flow Matching figure, this is NOT a perpendicular
construction. The segment from \\hat{\\mu} to \\hat{t}X_1 is simply
a comparison/discrepancy vector.
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

SOURCE_FILL = ManimColor("#AEBFCC")
MID_FILL = ManimColor("#C9D4DE")

PREDICTED_COLOR = ManimColor("#244A6A")
LOSS_ARROW_COLOR = ManimColor("#355F86")


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
# Use an explicit intermediate time, rather than one of the
# displayed circle centers, so that \hat{t}X_1 is shown as an
# independent reference point just like in the SFM figure.
# ------------------------------------------------------------

T_HAT = 0.28

# Place \hat{\mu} clearly outside the emphasized 1-sigma circle
# so that it visually matches the SFM teacher-signal figure.
# This is intentionally NOT a perpendicular construction.
MUHAT_RADIUS_FACTOR = 1.32
MUHAT_ANGLE_DEG = 52.0

# Small emphasis
REFERENCE_DOT_RADIUS = 0.042
PREDICTED_DOT_RADIUS = 0.042

# Arrow should start at \hat{\mu} and stop slightly before \hat{t}X_1.
ARROW_END_GAP = 0.050


# ============================================================
# Background styling
#
# Match shallow_flow_matching_three_distribution_losses.py
# only for:
# - emphasized sigma circles
# - ordinary distribution center dots
# - common tangent lines
# ============================================================

SIGMA_CIRCLE_OPACITY = 0.42
SIGMA_CIRCLE_WIDTH = 1.20

FAINT_CENTER_DOT_OPACITY = 0.28

TANGENT_OPACITY = 0.36
TANGENT_WIDTH = 0.90


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

    The 1-sigma circle and ordinary center marker are intentionally
    subdued to match the three-distribution-loss reference figure.
    """
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
        width=0.8,
        opacity=0.20,
    )

    inner_disk.set_fill(
        color=fill_color,
        opacity=(
            0.12
            if is_source
            else 0.09
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
    # Faint auxiliary contours
    #
    # Unchanged in this revision.
    # --------------------------------------------------------

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
    #
    # Matched to the faint SFM three-loss figure.
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

    group.add(
        sigma_circle
    )

    # --------------------------------------------------------
    # Distribution center marker
    #
    # Source center remains dark, as in the reference figure.
    # Intermediate centers are intentionally faint.
    # --------------------------------------------------------

    center_dot = Dot(
        [
            mean[0],
            mean[1],
            0.0,
        ],
        radius=0.020,
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


def make_common_tangent_lines() -> VGroup:
    """Create subdued common tangents of the emphasized 1-sigma circles."""
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


# ============================================================
# Figure
# ============================================================

class CSTMSFMDistributionAlignmentLossFigure(
    LightScene
):
    """Figure for explaining the distribution-alignment loss in CSTM-SFM."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --------------------------------------------------------
        # Straight mean path
        #
        # IMPORTANT:
        # unchanged in this revision.
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
            stroke_width=1.6,
            stroke_opacity=0.70,
        )

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

            distributions.add(
                distribution
            )

        # --------------------------------------------------------
        # Endpoints
        #
        # Unchanged.
        # --------------------------------------------------------

        source_dot = Dot(
            [
                SOURCE_MEAN[0],
                SOURCE_MEAN[1],
                0.0,
            ],
            radius=0.028,
            color=INK,
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

        x1_dot = Dot(
            [
                X1_POINT[0],
                X1_POINT[1],
                0.0,
            ],
            radius=0.038,
            color=INK,
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

        # --------------------------------------------------------
        # Common tangents
        # --------------------------------------------------------

        tangents = make_common_tangent_lines()

        # --------------------------------------------------------
        # Reference mean \hat{t}X_1 on the mean line
        # --------------------------------------------------------

        reference_mean = mean_t(
            T_HAT
        )

        sigma_hat = visual_sigma_t(
            T_HAT
        )

        reference_dot = Dot(
            [
                reference_mean[0],
                reference_mean[1],
                0.0,
            ],
            radius=REFERENCE_DOT_RADIUS,
            color=PREDICTED_COLOR,
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

        # --------------------------------------------------------
        # Predicted mean \hat{\mu}
        #
        # Important:
        # not a perpendicular construction.
        # --------------------------------------------------------

        direction = unit_vector_from_angle_deg(
            MUHAT_ANGLE_DEG
        )

        muhat_point = (
            np.array(
                [
                    reference_mean[0],
                    reference_mean[1],
                    0.0,
                ]
            )
            + MUHAT_RADIUS_FACTOR
            * sigma_hat
            * direction
        )

        muhat_dot = Dot(
            muhat_point,
            radius=PREDICTED_DOT_RADIUS,
            color=PREDICTED_COLOR,
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

        # --------------------------------------------------------
        # Discrepancy arrow: \hat{\mu} -> \hat{t}X_1
        # Start exactly from \hat{\mu}, but stop slightly before
        # the reference point.
        # --------------------------------------------------------

        reference_point = np.array(
            [
                reference_mean[0],
                reference_mean[1],
                0.0,
            ]
        )

        arrow_direction = (
            reference_point
            - muhat_point
        )

        arrow_direction = (
            arrow_direction
            / np.linalg.norm(
                arrow_direction
            )
        )

        arrow_end = (
            reference_point
            - ARROW_END_GAP
            * arrow_direction
        )

        discrepancy_arrow = Arrow(
            start=muhat_point,
            end=arrow_end,
            buff=0.0,
            color=LOSS_ARROW_COLOR,
            stroke_width=1.8,
            tip_length=0.11,
            max_tip_length_to_length_ratio=0.20,
            max_stroke_width_to_length_ratio=10.0,
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
            reference_dot,
            reference_label,
            discrepancy_arrow,
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