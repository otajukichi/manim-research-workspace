r"""Conditional CondOT path figure aligned with the fixed FM figure.

Shared with fm_state_paths_figure.py
------------------------------------
- canvas size
- initial distribution
- initial point X_0
- typography
- point sizes
- final fixed transform

Conditional-specific requirements
---------------------------------
- all conditional marginal centers lie on one horizontal mean line
- the fixed terminal point X_1 is chosen on that same horizontal mean line
- therefore the representative state path X_0 -> X_1 is NOT the same
  as the horizontal mean line
- the visible gaps between neighboring OUTERMOST contours are constant
- X_1 is treated as a degenerate outer contour with radius zero
"""

from __future__ import annotations

import numpy as np
from contourpy import contour_generator
from manim import (
    LEFT,
    RIGHT,
    UP,
    Dot,
    Line,
    MathTex,
    ManimColor,
    VGroup,
    VMobject,
    config,
)

from manim_research import LightScene


# ============================================================
# Canvas
# Shared with fm_state_paths_figure.py
# ============================================================

config.frame_width = 7.0
config.frame_height = 7.0


# ============================================================
# Presentation palette
# Shared with fm_state_paths_figure.py
# ============================================================

BACKGROUND = ManimColor("#FFFFFF")

INK = ManimColor("#1F2933")
ACCENT = ManimColor("#2D5B84")

SOURCE_FILL = ManimColor("#AEBFCC")
SOURCE_STROKE = ManimColor("#7C8894")

TARGET_FILL = ACCENT
TARGET_STROKE = ACCENT

PATH_COLOR = ACCENT
POINT_COLOR = INK
MOVING_COLOR = ACCENT


# ============================================================
# Fixed final transform
# EXACTLY the same as the fixed FM figure
# ============================================================

FIGURE_SCALE = 0.92

FM_REFERENCE_CENTER = np.array(
    [
        0.41958489,
        -0.93950548,
        0.0,
    ]
)

FM_FINAL_CENTER = np.array(
    [
        0.0,
        -0.10,
        0.0,
    ]
)


# ============================================================
# Shared geometry anchors
# ============================================================

PATH_Y = -1.00

# Shared initial distribution center
X_0_CENTER = -2.45

# Shared selected terminal point X_1
# This is the point that should visually align with the FM figure.
X_1_CENTER = 3.10

SOURCE_MEAN = np.array(
    [
        X_0_CENTER,
        PATH_Y,
    ]
)

FIXED_X1_POINT = np.array(
    [
        X_1_CENTER,
        PATH_Y,
    ]
)

# Shared initial sample point X_0
X0_SAMPLE_POINT = np.array(
    [
        X_0_CENTER + 0.10,
        PATH_Y + 0.34,
        0.0,
    ]
)

X1_FIXED_POSITION = np.array(
    [
        X_1_CENTER,
        PATH_Y,
        0.0,
    ]
)

# Shared representative-path convention
XT_PROPORTION = 0.74


# ============================================================
# Typography / point sizes
# Shared with fm_state_paths_figure.py
# ============================================================

PATH_STROKE_WIDTH = 2.2

ENDPOINT_DOT_RADIUS = 0.045
MOVING_DOT_RADIUS = 0.060

LABEL_FONT_SIZE = 30


# ============================================================
# Conditional sigma schedule
# ============================================================

SIGMA_START = 0.34
SIGMA_MIN = 0.05


def sigma_t(t: float) -> float:
    """Linear conditional standard-deviation schedule."""
    return SIGMA_START - (SIGMA_START - SIGMA_MIN) * t


def mean_t(t: float) -> np.ndarray:
    """Conditional mean path on one horizontal mean line."""
    return (
        (1.0 - t) * SOURCE_MEAN
        + t * FIXED_X1_POINT
    )


# ============================================================
# Equal outer-gap schedule
# ============================================================

OUTER_CONTOUR_LEVEL = 0.05
OUTER_RADIUS_FACTOR = np.sqrt(
    -2.0 * np.log(OUTER_CONTOUR_LEVEL)
)

NUM_DISPLAY_DISTRIBUTIONS = 3


def outer_radius_t(t: float) -> float:
    """Radius of the outermost displayed contour."""
    return OUTER_RADIUS_FACTOR * sigma_t(t)


def solve_equal_outer_gap_times() -> tuple[list[float], float]:
    r"""Solve display times so that outer-contour gaps are constant.

    We display:
        D0 = distribution at t=0
        D1 = distribution at t=t1
        D2 = distribution at t=t2
        X1 = terminal point, treated as radius zero

    and enforce

        gap(D0, D1) = gap(D1, D2) = gap(D2, X1),

    where each gap is measured between neighboring OUTERMOST contours.
    """
    path_length = float(
        FIXED_X1_POINT[0]
        - SOURCE_MEAN[0]
    )

    # outer_radius_t(t) = radius_intercept + radius_slope * t
    radius_intercept = (
        OUTER_RADIUS_FACTOR
        * SIGMA_START
    )

    radius_slope = (
        OUTER_RADIUS_FACTOR
        * (SIGMA_MIN - SIGMA_START)
    )

    # Unknowns: t1, t2, g
    matrix = np.zeros((3, 3))
    rhs = np.zeros(3)

    # --------------------------------------------------------
    # gap(D0, D1) = g
    #
    # (m1 - r1) - (m0 + r0) = g
    # --------------------------------------------------------
    matrix[0, 0] = path_length - radius_slope
    matrix[0, 2] = -1.0
    rhs[0] = 2.0 * radius_intercept

    # --------------------------------------------------------
    # gap(D1, D2) = g
    #
    # (m2 - r2) - (m1 + r1) = g
    # --------------------------------------------------------
    matrix[1, 0] = -path_length - radius_slope
    matrix[1, 1] = path_length - radius_slope
    matrix[1, 2] = -1.0
    rhs[1] = 2.0 * radius_intercept

    # --------------------------------------------------------
    # gap(D2, X1) = g
    #
    # X1 - (m2 + r2) = g
    # --------------------------------------------------------
    matrix[2, 1] = -path_length - radius_slope
    matrix[2, 2] = -1.0
    rhs[2] = -path_length + radius_intercept

    solution = np.linalg.solve(
        matrix,
        rhs,
    )

    t1 = float(solution[0])
    t2 = float(solution[1])
    common_gap = float(solution[2])

    display_times = [
        0.0,
        t1,
        t2,
    ]

    if not (
        0.0
        <= display_times[0]
        < display_times[1]
        < display_times[2]
        < 1.0
    ):
        raise ValueError(
            "Equal-gap solver produced invalid display times."
        )

    if common_gap <= 0.0:
        raise ValueError(
            "Equal-gap solver produced a non-positive gap."
        )

    return display_times, common_gap


DISPLAY_TIMES, COMMON_OUTER_GAP = solve_equal_outer_gap_times()


# ============================================================
# Density helpers
# ============================================================


def gaussian_density(
    x_grid: np.ndarray,
    y_grid: np.ndarray,
    mean: np.ndarray,
    covariance: np.ndarray,
) -> np.ndarray:
    """Evaluate a 2D Gaussian density."""
    dx = x_grid - mean[0]
    dy = y_grid - mean[1]

    inv_cov = np.linalg.inv(covariance)
    det_cov = np.linalg.det(covariance)

    exponent = (
        inv_cov[0, 0] * dx**2
        + 2.0 * inv_cov[0, 1] * dx * dy
        + inv_cov[1, 1] * dy**2
    )

    return np.exp(-0.5 * exponent) / (
        2.0 * np.pi * np.sqrt(det_cov)
    )


def distribution_bounds(
    mean: np.ndarray,
    covariance: np.ndarray,
    *,
    sigma_extent: float = 3.2,
    padding: float = 0.10,
) -> tuple[
    tuple[float, float],
    tuple[float, float],
]:
    """Compute safe plotting bounds for one isotropic Gaussian."""
    sigma_x = np.sqrt(covariance[0, 0])
    sigma_y = np.sqrt(covariance[1, 1])

    x_bounds = (
        float(mean[0] - sigma_extent * sigma_x - padding),
        float(mean[0] + sigma_extent * sigma_x + padding),
    )

    y_bounds = (
        float(mean[1] - sigma_extent * sigma_y - padding),
        float(mean[1] + sigma_extent * sigma_y + padding),
    )

    return x_bounds, y_bounds


# ============================================================
# Contour helpers
# ============================================================


def contour_to_mobject(
    points_2d: np.ndarray,
    *,
    stroke_color: ManimColor,
    fill_color: ManimColor,
    fill_opacity: float,
    stroke_width: float,
    stroke_opacity: float,
) -> VMobject:
    """Convert one contour path into a Manim object."""
    points_3d = np.column_stack(
        [
            points_2d[:, 0],
            points_2d[:, 1],
            np.zeros(len(points_2d)),
        ]
    )

    contour = VMobject()
    contour.set_points_as_corners(points_3d)
    contour.close_path()

    contour.set_stroke(
        stroke_color,
        width=stroke_width,
        opacity=stroke_opacity,
    )

    contour.set_fill(
        fill_color,
        opacity=fill_opacity,
    )

    return contour


def make_conditional_distribution(
    *,
    mean: np.ndarray,
    sigma: float,
    display_index: int,
) -> VGroup:
    """Draw one isotropic conditional Gaussian marginal."""
    covariance = (sigma**2) * np.eye(2)

    x_bounds, y_bounds = distribution_bounds(
        mean,
        covariance,
    )

    resolution = 300

    x_values = np.linspace(
        x_bounds[0],
        x_bounds[1],
        resolution,
    )

    y_values = np.linspace(
        y_bounds[0],
        y_bounds[1],
        resolution,
    )

    x_grid, y_grid = np.meshgrid(
        x_values,
        y_values,
    )

    density = gaussian_density(
        x_grid,
        y_grid,
        mean,
        covariance,
    )

    density_max = float(density.max())

    generator = contour_generator(
        x=x_values,
        y=y_values,
        z=density,
        name="serial",
    )

    if display_index == NUM_DISPLAY_DISTRIBUTIONS - 1:
        stroke_color = TARGET_STROKE
        fill_color = TARGET_FILL
        fill_opacities = [
            0.025,
            0.05,
            0.085,
            0.14,
            0.21,
        ]
        stroke_opacity = 0.80

    elif display_index == 0:
        stroke_color = SOURCE_STROKE
        fill_color = SOURCE_FILL
        fill_opacities = [
            0.035,
            0.06,
            0.10,
            0.16,
            0.24,
        ]
        stroke_opacity = 0.68

    else:
        stroke_color = SOURCE_STROKE
        fill_color = SOURCE_FILL
        fill_opacities = [
            0.03,
            0.05,
            0.085,
            0.13,
            0.20,
        ]
        stroke_opacity = 0.72

    level_fractions = [
        0.05,
        0.10,
        0.18,
        0.31,
        0.50,
    ]

    group = VGroup()

    for level, opacity in zip(
        level_fractions,
        fill_opacities,
        strict=True,
    ):
        paths = generator.lines(level * density_max)

        for path in paths:
            if len(path) < 3:
                continue

            group.add(
                contour_to_mobject(
                    path,
                    stroke_color=stroke_color,
                    fill_color=fill_color,
                    fill_opacity=opacity,
                    stroke_width=1.0,
                    stroke_opacity=stroke_opacity,
                )
            )

    return group


# ============================================================
# Figure
# ============================================================


class ConditionalCondOTPathFigure(LightScene):
    """Conditional CondOT path toward one fixed terminal state X_1."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --------------------------------------------------------
        # Conditional marginals
        # --------------------------------------------------------

        distributions = VGroup()

        for index, t in enumerate(DISPLAY_TIMES):
            distribution = make_conditional_distribution(
                mean=mean_t(t),
                sigma=sigma_t(t),
                display_index=index,
            )
            distributions.add(distribution)

        distributions.set_z_index(0)

        # --------------------------------------------------------
        # Representative state path
        # --------------------------------------------------------

        state_path = Line(
            X0_SAMPLE_POINT,
            X1_FIXED_POSITION,
            stroke_color=PATH_COLOR,
            stroke_width=PATH_STROKE_WIDTH,
        )
        state_path.set_z_index(3)

        # --------------------------------------------------------
        # X_0
        # --------------------------------------------------------

        x0_dot = Dot(
            X0_SAMPLE_POINT,
            radius=ENDPOINT_DOT_RADIUS,
            color=POINT_COLOR,
        )
        x0_dot.set_z_index(5)

        x0_label = MathTex(
            r"X_0",
            font_size=LABEL_FONT_SIZE,
            color=INK,
        ).next_to(
            x0_dot,
            UP + LEFT,
            buff=0.10,
        )
        x0_label.set_z_index(6)

        # --------------------------------------------------------
        # X_1
        # --------------------------------------------------------

        x1_dot = Dot(
            X1_FIXED_POSITION,
            radius=ENDPOINT_DOT_RADIUS,
            color=POINT_COLOR,
        )
        x1_dot.set_z_index(5)

        x1_label = MathTex(
            r"X_1",
            font_size=LABEL_FONT_SIZE,
            color=INK,
        ).next_to(
            x1_dot,
            UP + RIGHT,
            buff=0.10,
        )
        x1_label.set_z_index(6)

        # --------------------------------------------------------
        # X_t
        # --------------------------------------------------------

        xt_position = state_path.point_from_proportion(
            XT_PROPORTION
        )

        xt_dot = Dot(
            xt_position,
            radius=MOVING_DOT_RADIUS,
            color=MOVING_COLOR,
        )
        xt_dot.set_z_index(6)

        xt_label = MathTex(
            r"X_t",
            font_size=LABEL_FONT_SIZE,
            color=INK,
        ).next_to(
            xt_dot,
            UP,
            buff=0.12,
        )
        xt_label.set_z_index(7)

        # --------------------------------------------------------
        # Assemble
        # --------------------------------------------------------

        figure = VGroup(
            distributions,
            state_path,
            x0_dot,
            x1_dot,
            x0_label,
            x1_label,
            xt_dot,
            xt_label,
        )

        # --------------------------------------------------------
        # Fixed final transform
        # EXACTLY the same as the fixed FM figure
        # --------------------------------------------------------

        figure.scale(
            FIGURE_SCALE,
            about_point=FM_REFERENCE_CENTER,
        )

        figure.shift(
            FM_FINAL_CENTER
            - FM_REFERENCE_CENTER
        )

        self.add(figure)