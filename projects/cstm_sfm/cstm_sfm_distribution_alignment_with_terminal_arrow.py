"""Static figure for explaining the distribution-alignment loss in CSTM-SFM.

This figure is based on the same conditional CondOT geometry:
- isotropic Gaussian marginals along the straight mean path from 0 to X_1,
- common tangents showing the linear radius schedule.

On top of that, we add
- a reference mean location \\hat{t} X_1 on the mean line,
- a predicted mean \\hat{\\mu} near the corresponding intermediate Gaussian,
- an arrow from \\hat{\\mu} to \\hat{t}X_1,
- an additional arrow from \\hat{t}X_1 to X_1.

The terminal arrow \\hat{t}X_1 -> X_1 is highlighted in red.

Background CondOT geometry is intentionally subdued:
- sigma circles use the same faint styling as the SFM three-loss figure,
- ordinary mean markers are faint,
- the mean line is faint,
while the purple tangent constraint remains strongly emphasized.
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

# Terminal-flow arrow:
# \hat{t}X_1 -> X_1
TERMINAL_ARROW_COLOR = ManimColor("#C94A4A")

# Constraint envelope:
# keep the strong purple styling already decided.
TANGENT_COLOR = ManimColor("#7B2CBF")
TANGENT_WIDTH = 1.75
TANGENT_OPACITY = 0.84


# ============================================================
# Background CondOT styling
# Match shallow_flow_matching_three_distribution_losses.py
# ============================================================

SIGMA_CIRCLE_WIDTH = 1.20
SIGMA_CIRCLE_OPACITY = 0.42

MEAN_LINE_WIDTH = 1.35
MEAN_LINE_OPACITY = 0.55

FAINT_CENTER_DOT_OPACITY = 0.28


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

# Independent reference point.
T_HAT = 0.28

# \hat{\mu} geometry.
MUHAT_RADIUS_FACTOR = 1.32
MUHAT_ANGLE_DEG = 52.0

# Dot sizes
REFERENCE_DOT_RADIUS = 0.042
PREDICTED_DOT_RADIUS = 0.042

# Arrow end gaps
ARROW_END_GAP_MU_TO_T = 0.050
ARROW_END_GAP_T_TO_X1 = 0.065

# Fixed arrowhead size
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
    """Standard deviation changes linearly with time."""
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
# Drawing helpers
# ============================================================

def make_isotropic_distribution(
    *,
    mean: np.ndarray,
    sigma: float,
    is_source: bool,
    show_center_dot: bool,
) -> VGroup:
    """Draw one isotropic Gaussian schematically."""
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
    # 1-sigma circle
    #
    # Match the faint styling from the SFM three-loss figure.
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
    # Ordinary distribution center
    #
    # Source remains clear.
    # Intermediate centers are subdued like the reference figure.
    # --------------------------------------------------------

    if show_center_dot:
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
    """Create strongly emphasized purple constraint tangents."""
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
        color=TANGENT_COLOR,
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
        color=TANGENT_COLOR,
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


def make_gap_arrow(
    start_point: np.ndarray,
    target_point: np.ndarray,
    *,
    end_gap: float,
    color: ManimColor,
    stroke_width: float = 1.8,
    tip_length: float = ARROW_TIP_LENGTH,
) -> Arrow:
    """Arrow starting at start_point and stopping before target_point."""
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

class CSTMSFMDistributionAlignmentWithTerminalArrowFigure(
    LightScene
):
    """Figure for explaining the distribution-alignment loss in CSTM-SFM."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --------------------------------------------------------
        # Key reference geometry
        # --------------------------------------------------------

        reference_mean = mean_t(
            T_HAT
        )

        sigma_hat = visual_sigma_t(
            T_HAT
        )

        reference_point = np.array(
            [
                reference_mean[0],
                reference_mean[1],
                0.0,
            ]
        )

        # --------------------------------------------------------
        # Mean path
        #
        # Match the subdued styling from the SFM three-loss figure.
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
        # Gaussian marginals
        # --------------------------------------------------------

        distributions = VGroup()

        for index, t in enumerate(
            DISPLAY_TIMES
        ):
            current_mean = mean_t(
                t
            )

            show_center_dot = bool(
                current_mean[0]
                < reference_mean[0]
                - 1e-9
            )

            distribution = make_isotropic_distribution(
                mean=current_mean,
                sigma=visual_sigma_t(t),
                is_source=(index == 0),
                show_center_dot=show_center_dot,
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
            radius=0.028,
            color=INK,
        )

        source_dot.set_z_index(8)

        source_label = MathTex(
            r"0",
            font_size=26,
            color=INK,
        ).next_to(
            source_dot,
            LEFT,
            buff=0.14,
        )

        source_label.set_z_index(8)

        x1_dot = Dot(
            [
                X1_POINT[0],
                X1_POINT[1],
                0.0,
            ],
            radius=0.038,
            color=INK,
        )

        x1_dot.set_z_index(8)

        x1_label = MathTex(
            r"X_1",
            font_size=26,
            color=INK,
        ).next_to(
            x1_dot,
            DOWN + RIGHT,
            buff=0.12,
        )

        x1_label.set_z_index(8)

        # --------------------------------------------------------
        # Purple constraint tangents
        #
        # IMPORTANT:
        # these keep the previously fixed strong purple styling.
        # --------------------------------------------------------

        tangents = make_common_tangent_lines()

        tangents.set_z_index(1)

        # --------------------------------------------------------
        # Reference mean \hat{t}X_1
        # --------------------------------------------------------

        reference_dot = Dot(
            reference_point,
            radius=REFERENCE_DOT_RADIUS,
            color=PREDICTED_COLOR,
        )

        reference_dot.set_z_index(9)

        reference_label = MathTex(
            r"\hat{t}X_1",
            font_size=27,
            color=INK,
        ).next_to(
            reference_dot,
            DOWN,
            buff=0.05,
        )

        reference_label.set_z_index(9)

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

        muhat_dot = Dot(
            muhat_point,
            radius=PREDICTED_DOT_RADIUS,
            color=PREDICTED_COLOR,
        )

        muhat_dot.set_z_index(9)

        muhat_label = MathTex(
            r"\hat{\mu}",
            font_size=27,
            color=INK,
        ).next_to(
            muhat_dot,
            UP + RIGHT,
            buff=0.03,
        )

        muhat_label.set_z_index(9)

        # --------------------------------------------------------
        # Arrows
        # --------------------------------------------------------

        mu_to_t_arrow = make_gap_arrow(
            start_point=muhat_point,
            target_point=reference_point,
            end_gap=ARROW_END_GAP_MU_TO_T,
            color=LOSS_ARROW_COLOR,
            stroke_width=1.8,
        )

        mu_to_t_arrow.set_z_index(5)

        t_to_x1_arrow = make_gap_arrow(
            start_point=reference_point,
            target_point=np.array(
                [
                    X1_POINT[0],
                    X1_POINT[1],
                    0.0,
                ]
            ),
            end_gap=ARROW_END_GAP_T_TO_X1,
            color=TERMINAL_ARROW_COLOR,
            stroke_width=2.6,
        )

        t_to_x1_arrow.set_z_index(4)

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
            mu_to_t_arrow,
            t_to_x1_arrow,
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