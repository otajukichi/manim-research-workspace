"""Static figure explaining three properties of the conditional CondOT path.

This figure emphasizes:
1. each intermediate marginal is isotropic Gaussian,
2. the means lie on the straight line connecting 0 and x_1,
3. the standard deviation changes linearly with time.

The 1-sigma circle is emphasized for each time, while the other
concentric circles are drawn very faintly.

Displayed times are chosen so that the overlap width between
neighboring emphasized circles, relative to the smaller circle's
radius, is constant.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
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
config.frame_height = 3.6


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


# ============================================================
# Geometry
# ============================================================

ROW_Y = 0.00

# Internal geometry.
# The whole figure is enlarged afterwards to preserve the
# desired apparent width while keeping a relatively wide tangent angle.
SOURCE_MEAN = np.array([-1.95, ROW_Y])
X1_POINT = np.array([1.95, ROW_Y])

# Number of displayed Gaussian marginals.
NUM_DISPLAY_CIRCLES = 6

# Constant fractional overlap:
#
#   overlap width
#   ------------------------- = OVERLAP_RATIO
#   radius of the smaller circle
#
# 0.22 means that neighboring 1-sigma circles overlap
# by about 22% of the later/smaller circle's radius.
OVERLAP_RATIO = 0.22

# Maximum displayed standard deviation.
SIGMA_VISUAL_MAX = 0.62

FAINT_RADIUS_MULTIPLIERS = [
    0.55,
    1.45,
    1.90,
]

EMPHASIZED_RADIUS_MULTIPLIER = 1.00

FIGURE_SCALE = 1.24


# ============================================================
# Schedules
# ============================================================

def mean_t(t: float) -> np.ndarray:
    """Mean moves linearly from 0 to x_1."""
    return (
        (1.0 - t) * SOURCE_MEAN
        + t * X1_POINT
    )


def visual_sigma_t(t: float) -> float:
    """Standard deviation changes linearly with time."""
    return SIGMA_VISUAL_MAX * (1.0 - t)


def make_display_times() -> list[float]:
    """Choose times with constant fractional overlap.

    Let

        s_i = 1 - t_i

    so that both

        distance(mean_i, x_1) ∝ s_i
        radius_i              ∝ s_i.

    For neighboring emphasized circles,

        r_i     = R s_i
        r_{i+1} = R s_{i+1}

        d_i = L (s_i - s_{i+1})

    where

        R = SIGMA_VISUAL_MAX
        L = distance(0, x_1).

    The overlap width along the mean line is

        w_i = r_i + r_{i+1} - d_i.

    We impose

        w_i / r_{i+1} = rho

    with rho = OVERLAP_RATIO.

    This yields

        s_{i+1} = q s_i

    with a constant q, so the displayed times naturally
    become denser toward t = 1.
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
    # Emphasized 1-sigma circle
    # --------------------------------------------------------

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
    # Mean
    # --------------------------------------------------------

    center_dot = Dot(
        [
            mean[0],
            mean[1],
            0.0,
        ],
        radius=0.020,
        color=INK,
    )

    group.add(
        center_dot
    )

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
            1.0
            - radius_ratio**2
        )
    )

    x_left = (
        SOURCE_MEAN[0]
        - 0.55
    )

    # Tangents stop exactly at x_1.
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
        stroke_width=1.2,
        stroke_opacity=0.62,
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
        stroke_width=1.2,
        stroke_opacity=0.62,
    )

    return VGroup(
        upper_tangent,
        lower_tangent,
    )


# ============================================================
# Figure
# ============================================================

class ConditionalCondOTThreePropertiesFigure(
    LightScene
):
    """Figure for explaining the three properties of conditional CondOT."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --------------------------------------------------------
        # Straight mean path
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
            distribution = (
                make_isotropic_distribution(
                    mean=mean_t(t),
                    sigma=visual_sigma_t(t),
                    is_source=(
                        index == 0
                    ),
                )
            )

            distributions.add(
                distribution
            )

        # --------------------------------------------------------
        # Endpoint 0
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
            font_size=30,
            color=INK,
        ).next_to(
            source_dot,
            DOWN + LEFT,
            buff=0.10,
        )

        # --------------------------------------------------------
        # Fixed x_1
        # --------------------------------------------------------

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
            font_size=30,
            color=INK,
        ).next_to(
            x1_dot,
            DOWN + RIGHT,
            buff=0.12,
        )

        # --------------------------------------------------------
        # Common tangents
        # --------------------------------------------------------

        tangents = (
            make_common_tangent_lines()
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
        )

        figure.scale(
            FIGURE_SCALE
        )

        figure.move_to(
            [
                0.0,
                -0.02,
                0.0,
            ]
        )

        self.add(
            figure
        )