r"""Static figure for viewing discrepancy in units of standard deviation.

Design policy:
- explain only with geometry
- no equations, no numeric annotations
- keep only minimal point labels
- keep the sigma ruler and its ticks
- show one ruler interval as one sigma by a split arc
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    ArcBetweenPoints,
    Arrow,
    BackgroundRectangle,
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

PREDICTED_COLOR = ManimColor("#2D5B84")
LOSS_ARROW_COLOR = ManimColor("#355F86")

SIGMA_EMPHASIS_COLOR = ManimColor("#8A3FD1")
SIGMA_EMPHASIS_WIDTH = 1.85
SIGMA_EMPHASIS_OPACITY = 0.86


# ============================================================
# Geometry
# ============================================================

ROW_Y = 0.00

SOURCE_MEAN = np.array(
    [
        -2.05,
        ROW_Y,
    ]
)

X1_POINT = np.array(
    [
        2.35,
        ROW_Y,
    ]
)

SIGMA_VISUAL_MAX = 0.76

FIGURE_SCALE = 1.14


# ============================================================
# Selected comparison point
# ============================================================

T_HAT = 0.30

MUHAT_RADIUS_FACTOR = 1.35
MUHAT_ANGLE_DEG = 54.0


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

INNER_DISK_STROKE_WIDTH = 0.80
INNER_DISK_STROKE_OPACITY = 0.20
INNER_DISK_FILL_OPACITY = 0.09


# ============================================================
# Tangent styling
# ============================================================

TANGENT_WIDTH = 0.90
TANGENT_OPACITY = 0.34


# ============================================================
# Mean-line styling
# ============================================================

MEAN_LINE_WIDTH = 1.55
MEAN_LINE_OPACITY = 0.70


# ============================================================
# Arrow styling
# ============================================================

MU_TO_T_ARROW_END_GAP = 0.050
ARROW_TIP_LENGTH = 0.11


# ============================================================
# Sigma ruler styling
# ============================================================

RULER_WIDTH = 1.55
RULER_OPACITY = 0.82

RULER_TICK_WIDTH = 1.45
RULER_TICK_OPACITY = 0.82
RULER_TICK_SIZE = 0.038

RULER_NEGATIVE_EXTENT = 2.65
RULER_POSITIVE_EXTENT = 2.70

RULER_PERPENDICULAR_OFFSET = 0.13


# ============================================================
# One-sigma arc
#
# Adjacent ruler ticks are the endpoints of the chord.
# The arc is physically split around its midpoint.
# \hat{\sigma} is placed exactly inside that gap.
# ============================================================

SIGMA_ARC_ANGLE = -0.78
SIGMA_ARC_WIDTH = 1.55
SIGMA_ARC_OPACITY = 0.86

SIGMA_ARC_GAP_START = 0.30
SIGMA_ARC_GAP_END = 0.70

SIGMA_LABEL_BACKGROUND_BUFF = 0.030
SIGMA_LABEL_BACKGROUND_OPACITY = 1.0


# ============================================================
# Label styling
# ============================================================

MAIN_LABEL_FONT_SIZE = 27


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
            1.0 - radius_ratio**2
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
# Distribution
# ============================================================

def make_reference_distribution(
    *,
    mean: np.ndarray,
    sigma: float,
) -> VGroup:
    r"""Draw the reference isotropic Gaussian centered at \hat{t}X_1."""
    group = VGroup()

    inner_disk = Circle(
        radius=0.55 * sigma
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

    sigma_circle = Circle(
        radius=(
            EMPHASIZED_RADIUS_MULTIPLIER
            * sigma
        )
    )

    sigma_circle.set_stroke(
        color=SIGMA_EMPHASIS_COLOR,
        width=SIGMA_EMPHASIS_WIDTH,
        opacity=SIGMA_EMPHASIS_OPACITY,
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


def perpendicular_unit(
    vector_3d: np.ndarray,
) -> np.ndarray:
    """Return a 2D perpendicular unit vector."""
    vec = np.array(
        [
            vector_3d[0],
            vector_3d[1],
            0.0,
        ]
    )

    unit = (
        vec
        / np.linalg.norm(
            vec[:2]
        )
    )

    return np.array(
        [
            -unit[1],
            unit[0],
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


def make_sigma_ruler(
    *,
    center_point: np.ndarray,
    direction_unit: np.ndarray,
    sigma_length: float,
) -> tuple[
    VGroup,
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """Create the ruler and return the 0/1 sigma tick centers."""
    perp_unit = perpendicular_unit(
        direction_unit
    )

    ruler_center = (
        center_point
        + RULER_PERPENDICULAR_OFFSET
        * perp_unit
    )

    start_point = (
        ruler_center
        - RULER_NEGATIVE_EXTENT
        * sigma_length
        * direction_unit
    )

    end_point = (
        ruler_center
        + RULER_POSITIVE_EXTENT
        * sigma_length
        * direction_unit
    )

    ruler_line = Line(
        start=start_point,
        end=end_point,
        color=SIGMA_EMPHASIS_COLOR,
        stroke_width=RULER_WIDTH,
        stroke_opacity=RULER_OPACITY,
    )

    ticks = VGroup()

    zero_tick_center = None
    one_tick_center = None

    for k in [-2, -1, 0, 1, 2]:
        tick_center = (
            ruler_center
            + k
            * sigma_length
            * direction_unit
        )

        tick = Line(
            tick_center
            - RULER_TICK_SIZE
            * perp_unit,
            tick_center
            + RULER_TICK_SIZE
            * perp_unit,
            color=SIGMA_EMPHASIS_COLOR,
            stroke_width=RULER_TICK_WIDTH,
            stroke_opacity=RULER_TICK_OPACITY,
        )

        ticks.add(
            tick
        )

        if k == 0:
            zero_tick_center = tick_center

        if k == 1:
            one_tick_center = tick_center

    return (
        VGroup(
            ruler_line,
            ticks,
        ),
        ruler_center,
        zero_tick_center,
        one_tick_center,
    )


def make_sigma_arc_indicator(
    *,
    zero_tick_center: np.ndarray,
    one_tick_center: np.ndarray,
) -> tuple[VGroup, np.ndarray]:
    """Split one sigma arc and return the center of its gap."""
    full_arc = ArcBetweenPoints(
        zero_tick_center,
        one_tick_center,
        angle=SIGMA_ARC_ANGLE,
        color=SIGMA_EMPHASIS_COLOR,
        stroke_width=SIGMA_ARC_WIDTH,
        stroke_opacity=SIGMA_ARC_OPACITY,
    )

    # This is exactly where the sigma text belongs:
    # at the center of the arc, and therefore at the
    # center of the gap between the two arc pieces.
    arc_midpoint = full_arc.point_from_proportion(
        0.5
    )

    first_arc = full_arc.copy()

    first_arc.pointwise_become_partial(
        full_arc,
        0.0,
        SIGMA_ARC_GAP_START,
    )

    second_arc = full_arc.copy()

    second_arc.pointwise_become_partial(
        full_arc,
        SIGMA_ARC_GAP_END,
        1.0,
    )

    return (
        VGroup(
            first_arc,
            second_arc,
        ),
        arc_midpoint,
    )


# ============================================================
# Figure
# ============================================================

class CSTMSFMStandardDeviationCountViewFigure(
    LightScene
):
    """Geometric view of discrepancy measured in sigma units."""

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

        # Keep every existing geometric line above the
        # sigma-label background.
        mean_line.set_z_index(
            6
        )

        # --------------------------------------------------------
        # Tangent envelope
        # --------------------------------------------------------

        tangents = make_common_tangent_lines()

        tangents.set_z_index(
            6
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
        # Predicted mean
        # --------------------------------------------------------

        muhat_direction = unit_vector_from_angle_deg(
            MUHAT_ANGLE_DEG
        )

        muhat_point = (
            reference_point
            + MUHAT_RADIUS_FACTOR
            * sigma_hat
            * muhat_direction
        )

        # --------------------------------------------------------
        # Reference distribution
        # --------------------------------------------------------

        reference_distribution = make_reference_distribution(
            mean=reference_mean_2d,
            sigma=sigma_hat,
        )

        reference_distribution.set_z_index(
            6
        )

        # The highlighted sigma circle must never be broken
        # by the sigma-label background.
        reference_distribution[-1].set_z_index(
            8
        )

        # --------------------------------------------------------
        # Sigma ruler
        # --------------------------------------------------------

        (
            sigma_ruler,
            _,
            zero_tick_center,
            one_tick_center,
        ) = make_sigma_ruler(
            center_point=reference_point,
            direction_unit=muhat_direction,
            sigma_length=sigma_hat,
        )

        # Ruler and ticks also remain completely continuous.
        sigma_ruler.set_z_index(
            8
        )

        # --------------------------------------------------------
        # One-sigma arc
        #
        # ONE ruler interval is the chord.
        # The arc is split in the center.
        # --------------------------------------------------------

        (
            sigma_arc,
            sigma_arc_midpoint,
        ) = make_sigma_arc_indicator(
            zero_tick_center=zero_tick_center,
            one_tick_center=one_tick_center,
        )

        # Arc alone sits below the sigma background.
        sigma_arc.set_z_index(
            4
        )

        # --------------------------------------------------------
        # Sigma label
        #
        # THIS is the important part:
        #
        #     arc ----   sigma   ---- arc
        #
        # sigma is not shifted away from the arc.
        # It sits exactly in the central gap.
        # --------------------------------------------------------

        sigma_label = MathTex(
            r"\hat{\sigma}",
            font_size=MAIN_LABEL_FONT_SIZE,
            color=INK,
        )

        sigma_label.move_to(
            sigma_arc_midpoint
        )
        sigma_label.shift(UP * 0.06) 

        sigma_label_background = BackgroundRectangle(
            sigma_label,
            color=BACKGROUND,
            fill_opacity=SIGMA_LABEL_BACKGROUND_OPACITY,
            buff=SIGMA_LABEL_BACKGROUND_BUFF,
            stroke_opacity=0.0,
        )

        # Only objects below z=5 can be hidden by this.
        # The arc is z=4.
        # Every other geometric element is z>=6.
        sigma_label_background.set_z_index(
            5
        )

        sigma_label.set_z_index(
            9
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
            font_size=MAIN_LABEL_FONT_SIZE,
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
            8
        )

        x1_label = MathTex(
            r"X_1",
            font_size=MAIN_LABEL_FONT_SIZE,
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
        # Reference marker
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
            font_size=MAIN_LABEL_FONT_SIZE,
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
        # Predicted marker
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
            font_size=MAIN_LABEL_FONT_SIZE,
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
        # Discrepancy arrow
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
        # Assemble
        # --------------------------------------------------------

        figure = VGroup(
            reference_distribution,
            tangents,
            mean_line,
            sigma_arc,
            sigma_label_background,
            sigma_ruler,
            mu_to_t_arrow,
            source_dot,
            source_label,
            x1_dot,
            x1_label,
            reference_dot,
            reference_label,
            muhat_dot,
            muhat_label,
            sigma_label,
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