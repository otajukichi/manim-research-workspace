"""Static figure for emphasizing standard deviation and terminal-time optimization.

The conditional CondOT geometry is kept as context:
- the straight mean path from 0 to X_1,
- the common tangent envelope showing the standard-deviation schedule.

Only two isotropic Gaussian distributions are shown:

1. the reference distribution centered at \\hat{t}X_1,
2. the predicted distribution centered at \\hat{\\mu}.

The two distributions have exactly the same displayed standard deviation.
Only their means differ.

The 1-sigma circle of the reference distribution centered at \\hat{t}X_1
is strongly highlighted in purple and explicitly labeled \\hat{\\sigma}.

In addition, a red arrow from \\hat{t}X_1 to X_1 is shown to emphasize
the optimization pressure toward terminal time t = 1.
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

# Standard-deviation emphasis:
# match the previously fixed strong purple tangent styling.
SIGMA_EMPHASIS_COLOR = ManimColor("#7B2CBF")
SIGMA_EMPHASIS_WIDTH = 1.75
SIGMA_EMPHASIS_OPACITY = 0.84

# Terminal-time optimization:
# \hat{t}X_1 -> X_1
TERMINAL_ARROW_COLOR = ManimColor("#C94A4A")


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
# Sigma-label styling
# ============================================================

SIGMA_LABEL_FONT_SIZE = 25

# Position the label on the upper-left side of the
# strongly highlighted purple 1-sigma circle.
SIGMA_LABEL_ANGLE_DEG = 145.0
SIGMA_LABEL_RADIAL_FACTOR = 1.28


# ============================================================
# Point sizes
# ============================================================

REFERENCE_DOT_RADIUS = 0.042
PREDICTED_DOT_RADIUS = 0.042

SOURCE_DOT_RADIUS = 0.028
X1_DOT_RADIUS = 0.038


# ============================================================
# Distribution styling
# ============================================================

FAINT_RADIUS_MULTIPLIERS = [
    0.55,
    1.45,
    1.90,
]

EMPHASIZED_RADIUS_MULTIPLIER = 1.00

AUXILIARY_CIRCLE_WIDTH = 0.90
AUXILIARY_CIRCLE_OPACITY = 0.22

# Normal, non-highlighted 1-sigma circle.
SIGMA_CIRCLE_WIDTH = 1.20
SIGMA_CIRCLE_OPACITY = 0.42

INNER_DISK_STROKE_WIDTH = 0.80
INNER_DISK_STROKE_OPACITY = 0.20
INNER_DISK_FILL_OPACITY = 0.09


# ============================================================
# Tangent styling
# ============================================================

TANGENT_WIDTH = 0.90
TANGENT_OPACITY = 0.36


# ============================================================
# Mean-line styling
# ============================================================

MEAN_LINE_WIDTH = 1.60
MEAN_LINE_OPACITY = 0.70


# ============================================================
# Arrow styling
# ============================================================

# \hat{\mu} -> \hat{t}X_1
MU_TO_T_ARROW_END_GAP = 0.050

# \hat{t}X_1 -> X_1
T_TO_X1_ARROW_END_GAP = 0.065

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
    sigma_circle_color: ManimColor,
    sigma_circle_width: float,
    sigma_circle_opacity: float,
) -> VGroup:
    """Draw one isotropic Gaussian distribution.

    Geometry and auxiliary contours are identical between the two
    distributions. Only the visual styling of the 1-sigma circle can
    differ.
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
        color=sigma_circle_color,
        width=sigma_circle_width,
        opacity=sigma_circle_opacity,
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
# Utilities
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
    color: ManimColor,
    stroke_width: float,
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
        color=color,
        stroke_width=stroke_width,
        tip_length=ARROW_TIP_LENGTH,
        max_tip_length_to_length_ratio=10.0,
        max_stroke_width_to_length_ratio=10.0,
    )


# ============================================================
# Figure
# ============================================================

class CSTMSFMStandardDeviationEmphasisWithTerminalArrowSigmaLabelFigure(
    LightScene
):
    """Highlight sigma-hat, mean discrepancy, and terminal-time optimization."""

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

        mean_line.set_z_index(
            1
        )

        # --------------------------------------------------------
        # Common tangent envelope
        # --------------------------------------------------------

        tangents = make_common_tangent_lines()

        tangents.set_z_index(
            1
        )

        # --------------------------------------------------------
        # Reference geometry
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

        # --------------------------------------------------------
        # Reference distribution centered at \hat{t}X_1
        #
        # Purple 1-sigma circle:
        #   color   = #7B2CBF
        #   width   = 1.75
        #   opacity = 0.84
        # --------------------------------------------------------

        reference_distribution = make_comparison_distribution(
            mean=reference_mean_2d,
            sigma=sigma_hat,
            sigma_circle_color=SIGMA_EMPHASIS_COLOR,
            sigma_circle_width=SIGMA_EMPHASIS_WIDTH,
            sigma_circle_opacity=SIGMA_EMPHASIS_OPACITY,
        )

        reference_distribution.set_z_index(
            0
        )

        # --------------------------------------------------------
        # Explicit label for the purple sigma-hat circle
        # --------------------------------------------------------

        sigma_label_direction = unit_vector_from_angle_deg(
            SIGMA_LABEL_ANGLE_DEG
        )

        sigma_label_position = (
            reference_point
            + SIGMA_LABEL_RADIAL_FACTOR
            * sigma_hat
            * sigma_label_direction
        )

        sigma_hat_label = MathTex(
            r"\hat{\sigma}",
            font_size=SIGMA_LABEL_FONT_SIZE,
            color=INK,
        ).move_to(
            sigma_label_position
        )

        sigma_hat_label.set_z_index(
            10
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
        # Same sigma as reference, but its 1-sigma circle
        # remains subdued blue.
        # --------------------------------------------------------

        predicted_distribution = make_comparison_distribution(
            mean=muhat_mean_2d,
            sigma=sigma_hat,
            sigma_circle_color=ACCENT,
            sigma_circle_width=SIGMA_CIRCLE_WIDTH,
            sigma_circle_opacity=SIGMA_CIRCLE_OPACITY,
        )

        predicted_distribution.set_z_index(
            0
        )

        # --------------------------------------------------------
        # Endpoints
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

        x1_point = np.array(
            [
                X1_POINT[0],
                X1_POINT[1],
                0.0,
            ]
        )

        x1_dot = Dot(
            x1_point,
            radius=X1_DOT_RADIUS,
            color=INK,
        )

        x1_dot.set_z_index(
            9
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
            9
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
        # Distribution-mean discrepancy:
        # \hat{\mu} -> \hat{t}X_1
        # --------------------------------------------------------

        mu_to_t_arrow = make_gap_arrow(
            start_point=muhat_point,
            target_point=reference_point,
            end_gap=MU_TO_T_ARROW_END_GAP,
            color=LOSS_ARROW_COLOR,
            stroke_width=1.8,
        )

        mu_to_t_arrow.set_z_index(
            7
        )

        # --------------------------------------------------------
        # Terminal-time optimization:
        # \hat{t}X_1 -> X_1
        # --------------------------------------------------------

        t_to_x1_arrow = make_gap_arrow(
            start_point=reference_point,
            target_point=x1_point,
            end_gap=T_TO_X1_ARROW_END_GAP,
            color=TERMINAL_ARROW_COLOR,
            stroke_width=2.6,
        )

        t_to_x1_arrow.set_z_index(
            4
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
            mu_to_t_arrow,
            t_to_x1_arrow,
            reference_dot,
            reference_label,
            muhat_dot,
            muhat_label,
            sigma_hat_label,
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