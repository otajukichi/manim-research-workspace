"""Static square figure of one representative state path.

The figure shows:
- four CondOT-style intermediate distributions
- one representative straight path X_0 -> X_1
- one fixed X_t between p_{0.6} and p_1

This is a static image version for slides.
"""

from __future__ import annotations

import numpy as np
from contourpy import contour_generator
from manim import (
    DOWN,
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
# Square canvas
# ============================================================

config.frame_width = 7.0
config.frame_height = 7.0


# ============================================================
# Presentation palette
# ============================================================

BACKGROUND = ManimColor("#FFFFFF")

INK = ManimColor("#1F2933")
ACCENT = ManimColor("#2D5B84")
MUTED = ManimColor("#6B7785")

SOURCE_FILL = ManimColor("#AEBFCC")
SOURCE_STROKE = ManimColor("#7C8894")

TARGET_FILL = ACCENT
TARGET_STROKE = ACCENT

PATH_COLOR = ACCENT
POINT_COLOR = INK
MOVING_COLOR = ACCENT


# ============================================================
# Fixed final figure transform
# ============================================================

FIGURE_SCALE = 0.92

# Measured center of this FM figure before the original
# scale() + move_to() operations.
#
# This is now fixed so that the exact same transform can later
# be reused by the corresponding conditional CondOT figure.
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
# Layout
# ============================================================

PATH_Y = -1.00

X_03_SHIFT_RIGHT = 0.18

X_0_CENTER = -2.45
X_03_CENTER = -0.95 + X_03_SHIFT_RIGHT
X_06_CENTER = 0.75
X_1_CENTER = 2.55

XT_PROPORTION = 0.74


# ============================================================
# CondOT-style distribution parameters
# ============================================================

SIGMA_START = 0.34
SIGMA_MIN = 0.05

TARGET_COMPONENTS = [
    (
        0.46,
        np.array([0.22, 0.52]),
        np.array(
            [
                [0.12, -0.05],
                [-0.05, 0.10],
            ]
        ),
    ),
    (
        0.54,
        np.array([0.52, -0.38]),
        np.array(
            [
                [0.19, 0.06],
                [0.06, 0.11],
            ]
        ),
    ),
]


# ============================================================
# Density helpers
# ============================================================


def sigma_t(t: float) -> float:
    """Display noise schedule."""
    return SIGMA_START - (SIGMA_START - SIGMA_MIN) * t


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


def mixture_density(
    x_grid: np.ndarray,
    y_grid: np.ndarray,
    components: list[
        tuple[
            float,
            np.ndarray,
            np.ndarray,
        ]
    ],
) -> np.ndarray:
    """Evaluate a Gaussian mixture density."""
    density = np.zeros_like(x_grid)

    for weight, mean, covariance in components:
        density += weight * gaussian_density(
            x_grid,
            y_grid,
            mean,
            covariance,
        )

    return density


# ============================================================
# Automatic contour bounds
# ============================================================


def distribution_bounds(
    components: list[
        tuple[
            float,
            np.ndarray,
            np.ndarray,
        ]
    ],
    *,
    sigma_extent: float = 3.2,
    padding: float = 0.10,
) -> tuple[
    tuple[float, float],
    tuple[float, float],
]:
    """Compute plotting bounds large enough to avoid contour clipping."""
    x_min = np.inf
    x_max = -np.inf
    y_min = np.inf
    y_max = -np.inf

    for _, mean, covariance in components:
        sigma_x = np.sqrt(
            covariance[0, 0]
        )
        sigma_y = np.sqrt(
            covariance[1, 1]
        )

        x_min = min(
            x_min,
            mean[0] - sigma_extent * sigma_x,
        )

        x_max = max(
            x_max,
            mean[0] + sigma_extent * sigma_x,
        )

        y_min = min(
            y_min,
            mean[1] - sigma_extent * sigma_y,
        )

        y_max = max(
            y_max,
            mean[1] + sigma_extent * sigma_y,
        )

    return (
        (
            float(x_min - padding),
            float(x_max + padding),
        ),
        (
            float(y_min - padding),
            float(y_max + padding),
        ),
    )


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
            np.zeros(
                len(points_2d)
            ),
        ]
    )

    contour = VMobject()

    contour.set_points_as_corners(
        points_3d
    )
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


def make_density_contours(
    *,
    components: list[
        tuple[
            float,
            np.ndarray,
            np.ndarray,
        ]
    ],
    level_fractions: list[float],
    stroke_color: ManimColor,
    fill_color: ManimColor,
    fill_opacities: list[float],
    stroke_width: float = 1.0,
    stroke_opacity: float = 0.82,
    resolution: int = 300,
) -> VGroup:
    """Create contour-style density drawings."""
    if len(level_fractions) != len(fill_opacities):
        raise ValueError(
            "level_fractions and fill_opacities must match."
        )

    x_bounds, y_bounds = (
        distribution_bounds(
            components
        )
    )

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

    density = mixture_density(
        x_grid,
        y_grid,
        components,
    )

    density_max = float(
        density.max()
    )

    generator = contour_generator(
        x=x_values,
        y=y_values,
        z=density,
        name="serial",
    )

    group = VGroup()

    for level, opacity in zip(
        level_fractions,
        fill_opacities,
        strict=True,
    ):
        for path in generator.lines(
            level * density_max
        ):
            if len(path) < 3:
                continue

            group.add(
                contour_to_mobject(
                    path,
                    stroke_color=stroke_color,
                    fill_color=fill_color,
                    fill_opacity=opacity,
                    stroke_width=stroke_width,
                    stroke_opacity=stroke_opacity,
                )
            )

    return group


# ============================================================
# Intermediate distributions
# ============================================================


def condot_components_at_t(
    t: float,
    center: np.ndarray,
) -> list[
    tuple[
        float,
        np.ndarray,
        np.ndarray,
    ]
]:
    """Construct display marginals along the path."""
    sigma = sigma_t(t)
    identity = np.eye(2)

    components = []

    for (
        weight,
        target_mean,
        target_covariance,
    ) in TARGET_COMPONENTS:
        mean_t = (
            center
            + t * target_mean
        )

        covariance_t = (
            (t**2) * target_covariance
            + (sigma**2) * identity
        )

        components.append(
            (
                weight,
                mean_t,
                covariance_t,
            )
        )

    return components


def make_condot_distribution(
    center: np.ndarray,
    t: float,
) -> VGroup:
    """Draw one distribution along the path."""
    if t >= 0.55:
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

    elif t <= 0.05:
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

    components = condot_components_at_t(
        t=t,
        center=center,
    )

    return make_density_contours(
        components=components,
        level_fractions=[
            0.05,
            0.10,
            0.18,
            0.31,
            0.50,
        ],
        stroke_color=stroke_color,
        fill_color=fill_color,
        fill_opacities=fill_opacities,
        stroke_width=1.0,
        stroke_opacity=stroke_opacity,
    )


# ============================================================
# Scene
# ============================================================


class FMStatePathsFigure(LightScene):
    """Static square figure with one representative path and fixed X_t."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --------------------------------------------------------
        # Distributions
        # --------------------------------------------------------

        p0_center = np.array(
            [
                X_0_CENTER,
                PATH_Y,
                0.0,
            ]
        )

        p03_center = np.array(
            [
                X_03_CENTER,
                PATH_Y,
                0.0,
            ]
        )

        p06_center = np.array(
            [
                X_06_CENTER,
                PATH_Y,
                0.0,
            ]
        )

        p1_center = np.array(
            [
                X_1_CENTER,
                PATH_Y,
                0.0,
            ]
        )

        p0 = make_condot_distribution(
            p0_center[:2],
            t=0.0,
        )

        p03 = make_condot_distribution(
            p03_center[:2],
            t=0.3,
        )

        p06 = make_condot_distribution(
            p06_center[:2],
            t=0.6,
        )

        p1 = make_condot_distribution(
            p1_center[:2],
            t=1.0,
        )

        # --------------------------------------------------------
        # Representative state path
        # --------------------------------------------------------

        x0_position = np.array(
            [
                X_0_CENTER + 0.10,
                PATH_Y + 0.34,
                0.0,
            ]
        )

        x1_position = np.array(
            [
                3.10,
                PATH_Y,
                0.0,
            ]
        )

        state_path = Line(
            x0_position,
            x1_position,
            stroke_color=PATH_COLOR,
            stroke_width=2.2,
        )

        x0_dot = Dot(
            x0_position,
            radius=0.045,
            color=POINT_COLOR,
        )

        x1_dot = Dot(
            x1_position,
            radius=0.045,
            color=POINT_COLOR,
        )

        x0_label = MathTex(
            r"X_0",
            font_size=30,
            color=INK,
        ).next_to(
            x0_dot,
            UP + LEFT,
            buff=0.10,
        )

        x1_label = MathTex(
            r"X_1",
            font_size=30,
            color=INK,
        ).next_to(
            x1_dot,
            UP + RIGHT,
            buff=0.10,
        )

        xt_position = (
            state_path.point_from_proportion(
                XT_PROPORTION
            )
        )

        xt_dot = Dot(
            xt_position,
            radius=0.060,
            color=MOVING_COLOR,
        )

        xt_label = MathTex(
            r"X_t",
            font_size=30,
            color=INK,
        ).next_to(
            xt_dot,
            UP,
            buff=0.12,
        )

        # --------------------------------------------------------
        # Assemble
        # --------------------------------------------------------

        figure = VGroup(
            p0,
            p03,
            p06,
            p1,
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
        #
        # This reproduces the previous:
        #
        #     figure.scale(0.92)
        #     figure.move_to([0.0, -0.10, 0.0])
        #
        # using the measured FM center explicitly.
        # --------------------------------------------------------

        figure.scale(
            FIGURE_SCALE,
            about_point=FM_REFERENCE_CENTER,
        )

        figure.shift(
            FM_FINAL_CENTER
            - FM_REFERENCE_CENTER
        )

        self.add(
            figure
        )