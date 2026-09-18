"""Figure showing that an intermediate prediction must correspond
to a distribution on the CondOT path.
"""

from __future__ import annotations

import numpy as np
from contourpy import contour_generator
from manim import (
    DOWN,
    RIGHT,
    UP,
    Arrow,
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
PALE = ManimColor("#D8DEE5")

SOURCE_FILL = ManimColor("#AEBFCC")
SOURCE_STROKE = ManimColor("#7C8894")

TARGET_FILL = ACCENT
TARGET_STROKE = ACCENT


# ============================================================
# Overall figure scale
# ============================================================

FIGURE_SCALE = 0.78


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
    components: list[tuple[float, np.ndarray, np.ndarray]],
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


def target_mean_offset() -> np.ndarray:
    """Weighted mean offset of the target mixture."""
    offset = np.zeros(2)

    for weight, mean, _ in TARGET_COMPONENTS:
        offset += weight * mean

    return offset


# ============================================================
# Automatic plotting bounds
# ============================================================


def distribution_bounds(
    components: list[tuple[float, np.ndarray, np.ndarray]],
    *,
    sigma_extent: float = 3.2,
    padding: float = 0.08,
) -> tuple[
    tuple[float, float],
    tuple[float, float],
]:
    """Compute a sufficiently large plotting region for a Gaussian mixture."""
    x_min = np.inf
    x_max = -np.inf
    y_min = np.inf
    y_max = -np.inf

    for _, mean, covariance in components:
        sigma_x = np.sqrt(covariance[0, 0])
        sigma_y = np.sqrt(covariance[1, 1])

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


def make_density_contours(
    *,
    components: list[tuple[float, np.ndarray, np.ndarray]],
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

    x_bounds, y_bounds = distribution_bounds(
        components,
        sigma_extent=3.2,
        padding=0.10,
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

    max_density = float(density.max())

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
        contour_level = level * max_density

        for path in generator.lines(contour_level):
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
# CondOT path marginals
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
    """Construct display marginals along the CondOT path."""
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
    *,
    highlight: bool = False,
) -> VGroup:
    """Draw one marginal along the CondOT path."""
    if highlight or t >= 0.95:
        stroke_color = TARGET_STROKE
        fill_color = TARGET_FILL

        fill_opacities = [
            0.03,
            0.06,
            0.10,
            0.16,
            0.24,
        ]

        stroke_opacity = 0.85

    elif t <= 0.05:
        stroke_color = SOURCE_STROKE
        fill_color = SOURCE_FILL

        fill_opacities = [
            0.04,
            0.07,
            0.11,
            0.17,
            0.25,
        ]

        stroke_opacity = 0.70

    else:
        stroke_color = SOURCE_STROKE
        fill_color = SOURCE_FILL

        fill_opacities = [
            0.035,
            0.06,
            0.095,
            0.145,
            0.22,
        ]

        stroke_opacity = 0.75

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
        resolution=300,
    )


# ============================================================
# Time-axis helper
# ============================================================


def make_tick(
    x: float,
    y: float,
) -> Line:
    """Create one vertical tick on the time axis."""
    return Line(
        [x, y - 0.08, 0.0],
        [x, y + 0.08, 0.0],
        stroke_color=MUTED,
        stroke_width=1.6,
    )


# ============================================================
# Figure
# ============================================================


class CondOTIntermediateCorrespondenceFigure(LightScene):
    """Show that the predicted intermediate must lie on the CondOT path."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --------------------------------------------------------
        # Layout
        # --------------------------------------------------------

        path_y = -0.75
        SHIFT_RIGHT = 0.18

        x_positions = [
            -2.55,
            -0.95 + SHIFT_RIGHT,
            0.85,
            2.72,
        ]

        p0_center = np.array(
            [
                x_positions[0],
                path_y,
                0.0,
            ]
        )

        p03_center = np.array(
            [
                x_positions[1],
                path_y,
                0.0,
            ]
        )

        p06_center = np.array(
            [
                x_positions[2],
                path_y,
                0.0,
            ]
        )

        p1_center = np.array(
            [
                x_positions[3],
                path_y,
                0.0,
            ]
        )

        predicted_center = np.array(
            [
                0.85,
                1.55,
                0.0,
            ]
        )

        # --------------------------------------------------------
        # CondOT marginals
        # --------------------------------------------------------

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
            highlight=True,
        )

        p1 = make_condot_distribution(
            p1_center[:2],
            t=1.0,
        )

        predicted = make_condot_distribution(
            predicted_center[:2],
            t=0.6,
            highlight=True,
        )

        # --------------------------------------------------------
        # Predicted intermediate
        # --------------------------------------------------------

        predicted_label = self.jp_text(
            "前段出力",
            font_size=30,
            color=INK,
        ).next_to(
            predicted,
            UP,
            buff=0.18,
        )

        correspondence_arrow = Arrow(
            start=predicted.get_bottom()
            + DOWN * 0.04,
            end=p06.get_top()
            + UP * 0.05,
            buff=0.08,
            color=ACCENT,
            stroke_width=2.5,
            tip_length=0.16,
        )

        # --------------------------------------------------------
        # Time axis
        # --------------------------------------------------------

        mean_offset = target_mean_offset()

        tick_x_0 = p0_center[0]
        tick_x_03 = p03_center[0] + 0.3 * mean_offset[0]
        tick_x_06 = p06_center[0] + 0.6 * mean_offset[0]
        tick_x_1 = p1_center[0] + mean_offset[0]

        time_axis_y = -2.45

        time_axis = Arrow(
            start=[
                tick_x_0 - 0.30,
                time_axis_y,
                0.0,
            ],
            end=[
                tick_x_1 + 0.30,
                time_axis_y,
                0.0,
            ],
            buff=0.0,
            color=MUTED,
            stroke_width=1.7,
            tip_length=0.13,
        )

        tick_0 = make_tick(
            tick_x_0,
            time_axis_y,
        )

        tick_03 = make_tick(
            tick_x_03,
            time_axis_y,
        )

        tick_06 = make_tick(
            tick_x_06,
            time_axis_y,
        )

        tick_1 = make_tick(
            tick_x_1,
            time_axis_y,
        )

        label_0 = MathTex(
            r"0",
            font_size=24,
            color=MUTED,
        ).next_to(
            tick_0,
            DOWN,
            buff=0.10,
        )

        label_1 = MathTex(
            r"1",
            font_size=24,
            color=MUTED,
        ).next_to(
            tick_1,
            DOWN,
            buff=0.10,
        )

        time_label = MathTex(
            r"t",
            font_size=26,
            color=MUTED,
        ).next_to(
            time_axis,
            RIGHT,
            buff=0.10,
        )

        # --------------------------------------------------------
        # Assemble
        # --------------------------------------------------------

        figure = VGroup(
            p0,
            p03,
            p06,
            p1,
            predicted,
            predicted_label,
            correspondence_arrow,
            time_axis,
            tick_0,
            tick_03,
            tick_06,
            tick_1,
            label_0,
            label_1,
            time_label,
        )

        figure.scale(FIGURE_SCALE)
        figure.move_to([0.0, -0.02, 0.0])

        self.add(figure)