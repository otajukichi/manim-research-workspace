"""Static SFM figure with variance-based distribution geometry.

This file is derived from the original standard-deviation-based figure.

Changes in this version:
- the displayed distribution radius is proportional to variance,
- the variance schedule is quadratic in time,
- the straight common std tangents are replaced by curved variance envelopes,
- all explicit variance-loss annotations are removed,
  including the predicted/target variance label, double arrow, and guide line,
- the X_h and t_h discrepancy annotations are kept.

The SFM paper defines the CondOT marginal covariance as sigma_t^2 I and uses a
standard deviation sigma_t that is linear in t.  Under the zero-floor visual
simplification used by the source figure, variance therefore scales as
(1 - t)^2.
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
    ParametricFunction,
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

# Visual radius assigned to variance at t = 0.
# This is a drawing scale, not the numerical variance of the paper.
VARIANCE_VISUAL_MAX = 0.62

FAINT_RADIUS_MULTIPLIERS = [
    0.55,
    1.45,
    1.90,
]

EMPHASIZED_RADIUS_MULTIPLIER = 1.00

FIGURE_SCALE = 1.18


# ============================================================
# Selected geometry for the two remaining losses
# ============================================================

T_SELECTED = 0.30

# \hat{X}_h is above t_h X_1 by a multiple of the displayed variance radius.
XHAT_VERTICAL_VARIANCE_MULTIPLIER = 1.30

# Separate schematic point for \hat{t}_h.
THAT_SCALAR_SHIFT_RIGHT = 0.95


# ============================================================
# Styling for background distributions
# ============================================================

AUXILIARY_CIRCLE_OPACITY = 0.18
AUXILIARY_CIRCLE_WIDTH = 0.85

VARIANCE_CIRCLE_OPACITY = 0.42
VARIANCE_CIRCLE_WIDTH = 1.20

ENVELOPE_OPACITY = 0.36
ENVELOPE_WIDTH = 0.90

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
# Variance schedule
# ============================================================


def mean_t(t: float) -> np.ndarray:
    """Mean moves linearly from the source mean to X_1."""
    return (1.0 - t) * SOURCE_MEAN + t * X1_POINT


def visual_variance_t(t: float) -> float:
    """Displayed radius is proportional to variance, hence quadratic in time."""
    return VARIANCE_VISUAL_MAX * (1.0 - t) ** 2


def visual_variance_derivative_t(t: float) -> float:
    """Time derivative of the displayed variance radius."""
    return -2.0 * VARIANCE_VISUAL_MAX * (1.0 - t)


def make_display_times() -> list[float]:
    """Choose display times with approximately constant fractional overlap.

    For consecutive circles at t_a and t_b, enforce

        center_gap = r_a + (1 - rho) r_b,

    where r(t) is now quadratic.  The previous closed-form geometric schedule
    only applies when the displayed radius is linear in time, so we solve this
    monotone scalar equation by bisection for each next circle.
    """
    path_length = X1_POINT[0] - SOURCE_MEAN[0]
    rho = OVERLAP_RATIO

    times = [0.0]

    for _ in range(NUM_DISPLAY_CIRCLES - 1):
        current_t = times[-1]
        current_radius = visual_variance_t(current_t)

        def overlap_equation(next_t: float) -> float:
            center_gap = path_length * (next_t - current_t)
            next_radius = visual_variance_t(next_t)
            desired_gap = current_radius + (1.0 - rho) * next_radius
            return center_gap - desired_gap

        if overlap_equation(1.0) <= 0.0:
            raise ValueError(
                "Could not place all variance circles before t=1. "
                "Reduce NUM_DISPLAY_CIRCLES or VARIANCE_VISUAL_MAX."
            )

        low = current_t
        high = 1.0

        for _ in range(64):
            mid = 0.5 * (low + high)
            if overlap_equation(mid) < 0.0:
                low = mid
            else:
                high = mid

        times.append(0.5 * (low + high))

    return times


DISPLAY_TIMES = make_display_times()


# ============================================================
# Curved envelope geometry
# ============================================================


def variance_envelope_point(t: float, sign: float) -> np.ndarray:
    """Return a point on the envelope of the variance-radius circle family.

    The circle family is

        (x - c(t))^2 + y^2 = r(t)^2,

    with a linear center c(t) and quadratic radius r(t).  Solving the circle
    equation together with its time derivative gives the envelope contact
    offset

        x - c(t) = -r(t) r'(t) / c'(t).

    Because r(t) is quadratic, the resulting upper/lower envelopes are curved.
    """
    center = mean_t(t)
    radius = visual_variance_t(t)
    radius_rate = visual_variance_derivative_t(t)
    center_speed = X1_POINT[0] - SOURCE_MEAN[0]

    x_offset = -radius * radius_rate / center_speed
    y_squared = max(radius**2 - x_offset**2, 0.0)
    y_offset = sign * np.sqrt(y_squared)

    return np.array(
        [
            center[0] + x_offset,
            ROW_Y + y_offset,
            0.0,
        ]
    )


def make_variance_envelope_curves() -> VGroup:
    """Create upper and lower curved envelopes for the variance geometry."""
    upper_envelope = ParametricFunction(
        lambda t: variance_envelope_point(t, +1.0),
        t_range=[0.0, 1.0, 0.01],
        color=ACCENT,
        stroke_width=ENVELOPE_WIDTH,
        stroke_opacity=ENVELOPE_OPACITY,
    )

    lower_envelope = ParametricFunction(
        lambda t: variance_envelope_point(t, -1.0),
        t_range=[0.0, 1.0, 0.01],
        color=ACCENT,
        stroke_width=ENVELOPE_WIDTH,
        stroke_opacity=ENVELOPE_OPACITY,
    )

    return VGroup(
        upper_envelope,
        lower_envelope,
    )


# ============================================================
# Drawing helpers
# ============================================================


def make_isotropic_distribution(
    *,
    mean: np.ndarray,
    variance_radius: float,
    is_source: bool,
) -> VGroup:
    """Draw one isotropic distribution with radii based on variance."""
    fill_color = SOURCE_FILL if is_source else MID_FILL

    group = VGroup()

    # --------------------------------------------------------
    # Faint filled center
    # --------------------------------------------------------

    inner_disk = Circle(radius=0.55 * variance_radius)

    inner_disk.set_stroke(
        color=VERY_FAINT,
        width=0.75,
        opacity=0.16,
    )

    inner_disk.set_fill(
        color=fill_color,
        opacity=(0.11 if is_source else 0.08),
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
        circle = Circle(radius=multiplier * variance_radius)

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
    # Emphasized variance-radius circle
    # --------------------------------------------------------

    variance_circle = Circle(
        radius=EMPHASIZED_RADIUS_MULTIPLIER * variance_radius
    )

    variance_circle.set_stroke(
        color=ACCENT,
        width=VARIANCE_CIRCLE_WIDTH,
        opacity=VARIANCE_CIRCLE_OPACITY,
    )

    variance_circle.set_fill(
        color=fill_color,
        opacity=0.0,
    )

    variance_circle.move_to(
        [
            mean[0],
            mean[1],
            0.0,
        ]
    )

    group.add(variance_circle)

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
        color=(INK if is_source else MUTED),
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
    direction = target_point - start_point
    direction = direction / np.linalg.norm(direction)

    arrow_end = target_point - end_gap * direction

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


class ShallowFlowMatchingVarianceDistributionLossesFigure(LightScene):
    """SFM distribution figure using variance-based path geometry."""

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

        variance_envelopes = make_variance_envelope_curves()
        variance_envelopes.set_z_index(0)

        distributions = VGroup()

        for index, t in enumerate(DISPLAY_TIMES):
            distribution = make_isotropic_distribution(
                mean=mean_t(t),
                variance_radius=visual_variance_t(t),
                is_source=(index == 0),
            )

            distributions.add(distribution)

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

        selected_variance_radius = visual_variance_t(T_SELECTED)

        xhat_point = np.array(
            [
                tx1_point[0],
                tx1_point[1]
                + XHAT_VERTICAL_VARIANCE_MULTIPLIER * selected_variance_radius,
                0.0,
            ]
        )

        hat_t_scalar_point = tx1_point + np.array(
            [
                THAT_SCALAR_SHIFT_RIGHT,
                0.0,
                0.0,
            ]
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
        # Assemble
        # --------------------------------------------------------

        figure = VGroup(
            variance_envelopes,
            mean_line,
            distributions,
            source_dot,
            source_label,
            x1_dot,
            x1_label,
            vertical_arrow,
            time_arrow,
            tx1_dot,
            tx1_label,
            hat_t_scalar_dot,
            hat_t_scalar_label,
            xhat_dot,
            xhat_label,
        )

        figure.scale(FIGURE_SCALE)

        figure.move_to(
            [
                0.0,
                -0.06,
                0.0,
            ]
        )

        self.add(figure)
