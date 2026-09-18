"""Animate a conditional CondOT figure from 2D contour view
to a 3D density view.

The horizontal plane is the SAME 2D state space as the previous figure.
We simply add the probability-density direction upward.

The terminal x_1 is shown as a narrow high peak in the final 3D view.

This revision includes:
- compressed but stronger height scaling
- safer initial framing
- a subtle 2D grid plane beneath the distributions
"""

from __future__ import annotations

import numpy as np
from manim import (
    DEGREES,
    DOWN,
    RIGHT,
    TAU,
    Circle,
    Dot,
    FadeIn,
    FadeOut,
    MathTex,
    ManimColor,
    NumberPlane,
    Surface,
    ThreeDScene,
    Transform,
    VGroup,
    config,
)

# ============================================================
# Canvas
# ============================================================

config.frame_width = 7.0
config.frame_height = 7.0


# ============================================================
# Presentation palette
# ============================================================

BACKGROUND = ManimColor("#FFFFFF")
INK = ManimColor("#1F2933")

SOURCE_FILL = ManimColor("#AEBFCC")
SOURCE_STROKE = ManimColor("#7C8894")

MID_FILL = ManimColor("#C9D4DE")
MID_STROKE = ManimColor("#8B99A6")

PEAK_FILL = ManimColor("#B8C9D9")
PEAK_STROKE = ManimColor("#2D5B84")

GRID_COLOR = ManimColor("#D3D9E0")


# ============================================================
# Geometry of the conditional path
# ============================================================

ROW_Y = -0.10

SOURCE_MEAN = np.array([-2.35, ROW_Y])
X1_POINT = np.array([2.35, ROW_Y])

# Same intent as before:
# large move first, then smaller move near x1.
DISPLAY_TIMES = [0.00, 0.45, 0.78]

SIGMA_MIN = 0.05

# Visualization scales in scene units.
VISUAL_SIGMA_SCALE = 0.52
VISUAL_SIGMA_OFFSET = 0.03

# Height scaling:
# raise the whole family a bit while keeping the terminal peak
# within the frame by also loosening the final camera slightly.
HEIGHT_MIN = 0.82
HEIGHT_MAX = 1.82
HEIGHT_GAMMA = 0.92

# Contour levels used both in 2D and 3D.
LEVEL_FRACTIONS = [0.14, 0.28, 0.45, 0.65, 0.85]

# Matching fill opacities for nested contours
SOURCE_FILL_OPACITIES = [0.04, 0.07, 0.11, 0.17, 0.25]
MID_FILL_OPACITIES = [0.03, 0.055, 0.09, 0.14, 0.20]


# ============================================================
# Schedules
# ============================================================

def sigma_t(t: float) -> float:
    """Conditional CondOT standard-deviation schedule."""
    return 1.0 - (1.0 - SIGMA_MIN) * t


def visual_sigma_t(t: float) -> float:
    """Convert the schedule into scene units."""
    return VISUAL_SIGMA_SCALE * sigma_t(t) + VISUAL_SIGMA_OFFSET


def mean_t(t: float) -> np.ndarray:
    """Linear conditional mean path for fixed x_1."""
    return (1.0 - t) * SOURCE_MEAN + t * X1_POINT


def normalized_sharpness(t: float) -> float:
    """Map sharpness to [0, 1] for bounded visual height scaling."""
    sigma0 = visual_sigma_t(0.0)
    sigma1 = visual_sigma_t(1.0)
    sharp0 = 1.0 / sigma0
    sharp1 = 1.0 / sigma1
    sharp_t = 1.0 / visual_sigma_t(t)

    alpha = (sharp_t - sharp0) / (sharp1 - sharp0)
    return float(np.clip(alpha, 0.0, 1.0))


def peak_height_t(t: float) -> float:
    """Compressed peak-height schedule for readable visualization."""
    alpha = normalized_sharpness(t)
    return HEIGHT_MIN + (HEIGHT_MAX - HEIGHT_MIN) * (alpha ** HEIGHT_GAMMA)


def contour_radius(sigma: float, level_fraction: float) -> float:
    """Radius of a Gaussian contour at a given relative level."""
    return sigma * np.sqrt(-2.0 * np.log(level_fraction))


def density_height_at_radius(
    radius: float,
    sigma: float,
    peak_height: float,
) -> float:
    """Height of the schematic bell surface at radius r."""
    return peak_height * np.exp(-0.5 * (radius / sigma) ** 2)


# ============================================================
# Drawing helpers
# ============================================================

def make_plane_grid() -> NumberPlane:
    """Create the subtle 2D grid plane in the state space."""
    plane = NumberPlane(
        x_range=[-4.5, 4.5, 1.0],
        y_range=[-2.8, 2.8, 1.0],
        background_line_style={
            "stroke_color": GRID_COLOR,
            "stroke_width": 1.0,
            "stroke_opacity": 0.34,
        },
        faded_line_style={
            "stroke_color": GRID_COLOR,
            "stroke_width": 0.8,
            "stroke_opacity": 0.14,
        },
        faded_line_ratio=2,
        axis_config={
            "stroke_color": GRID_COLOR,
            "stroke_width": 1.1,
            "stroke_opacity": 0.40,
            "include_ticks": False,
            "include_numbers": False,
        },
    )
    plane.move_to([0.0, 0.0, 0.0])
    plane.set_z_index(-20)
    return plane


def make_flat_distribution(
    t: float,
    *,
    is_source: bool,
) -> VGroup:
    """Create the 2D contour-style distribution at z=0."""
    mean = mean_t(t)
    sigma = visual_sigma_t(t)

    if is_source:
        stroke_color = SOURCE_STROKE
        fill_color = SOURCE_FILL
        fill_opacities = SOURCE_FILL_OPACITIES
    else:
        stroke_color = MID_STROKE
        fill_color = MID_FILL
        fill_opacities = MID_FILL_OPACITIES

    group = VGroup()

    for level, opacity in zip(
        LEVEL_FRACTIONS,
        fill_opacities,
        strict=True,
    ):
        radius = contour_radius(sigma, level)

        circle = Circle(radius=radius)
        circle.set_stroke(
            stroke_color,
            width=1.0,
            opacity=0.78,
        )
        circle.set_fill(
            fill_color,
            opacity=opacity,
        )
        circle.move_to([mean[0], mean[1], 0.0])

        group.add(circle)

    return group


def make_lifted_contours(
    t: float,
    *,
    is_source: bool,
) -> VGroup:
    """Create 3D contour rings lifted to their density heights."""
    mean = mean_t(t)
    sigma = visual_sigma_t(t)
    peak_height = peak_height_t(t)

    if is_source:
        stroke_color = SOURCE_STROKE
        fill_color = SOURCE_FILL
    else:
        stroke_color = MID_STROKE
        fill_color = MID_FILL

    group = VGroup()

    for level in LEVEL_FRACTIONS:
        radius = contour_radius(sigma, level)
        z = density_height_at_radius(
            radius,
            sigma,
            peak_height,
        )

        circle = Circle(radius=radius)
        circle.set_stroke(
            stroke_color,
            width=1.0,
            opacity=0.72,
        )
        circle.set_fill(
            fill_color,
            opacity=0.04,
        )
        circle.move_to([mean[0], mean[1], z])

        group.add(circle)

    return group


def make_density_surface(
    t: float,
    *,
    fill_color: ManimColor,
    stroke_color: ManimColor,
) -> Surface:
    """Create a 3D bell-shaped schematic density surface."""
    mean = mean_t(t)
    sigma = visual_sigma_t(t)
    peak_height = peak_height_t(t)

    r_max = 3.0 * sigma

    surface = Surface(
        lambda r, theta: np.array(
            [
                mean[0] + r * np.cos(theta),
                mean[1] + r * np.sin(theta),
                density_height_at_radius(r, sigma, peak_height),
            ]
        ),
        u_range=[0.0, r_max],
        v_range=[0.0, TAU],
        resolution=(18, 36),
        checkerboard_colors=[fill_color, fill_color],
        fill_opacity=0.26,
        stroke_color=stroke_color,
        stroke_opacity=0.16,
        stroke_width=0.5,
    )

    return surface


def make_x1_peak() -> Surface:
    """Create the final narrow high peak at x_1."""
    t = 1.0
    mean = mean_t(t)
    sigma = visual_sigma_t(t)
    peak_height = peak_height_t(t)

    r_max = 3.0 * sigma

    surface = Surface(
        lambda r, theta: np.array(
            [
                mean[0] + r * np.cos(theta),
                mean[1] + r * np.sin(theta),
                density_height_at_radius(r, sigma, peak_height),
            ]
        ),
        u_range=[0.0, r_max],
        v_range=[0.0, TAU],
        resolution=(22, 40),
        checkerboard_colors=[PEAK_FILL, PEAK_FILL],
        fill_opacity=0.30,
        stroke_color=PEAK_STROKE,
        stroke_opacity=0.18,
        stroke_width=0.5,
    )

    return surface


# ============================================================
# Scene
# ============================================================

class ConditionalCondOTDensityLift(ThreeDScene):
    """Lift the conditional 2D figure into a 3D density view."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --------------------------------------------------------
        # Base plane grid
        # --------------------------------------------------------

        plane = make_plane_grid()

        # --------------------------------------------------------
        # Initial near-2D camera
        # --------------------------------------------------------

        self.set_camera_orientation(
            phi=5 * DEGREES,
            theta=-90 * DEGREES,
            zoom=1.02,
            frame_center=[-0.18, 0.02, 0.0],
        )

        # --------------------------------------------------------
        # 2D objects (same state-space figure as before)
        # --------------------------------------------------------

        flat_groups = VGroup()
        lifted_groups = VGroup()
        surfaces = VGroup()

        for index, t in enumerate(DISPLAY_TIMES):
            is_source = index == 0

            flat = make_flat_distribution(
                t,
                is_source=is_source,
            )
            lifted = make_lifted_contours(
                t,
                is_source=is_source,
            )

            if is_source:
                surface = make_density_surface(
                    t,
                    fill_color=SOURCE_FILL,
                    stroke_color=SOURCE_STROKE,
                )
            else:
                surface = make_density_surface(
                    t,
                    fill_color=MID_FILL,
                    stroke_color=MID_STROKE,
                )

            flat_groups.add(flat)
            lifted_groups.add(lifted)
            surfaces.add(surface)

        x1_dot = Dot(
            [X1_POINT[0], X1_POINT[1], 0.0],
            radius=0.045,
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

        x1_peak = make_x1_peak()

        x1_label_target = MathTex(
            r"X_1",
            font_size=30,
            color=INK,
        ).move_to([X1_POINT[0] + 0.22, X1_POINT[1] - 0.24, 0.0])

        self.add(plane, flat_groups, x1_dot, x1_label)
        self.wait(0.6)

        # --------------------------------------------------------
        # 2D contours -> 3D densities
        # --------------------------------------------------------

        morph_anims = []

        for flat, lifted, surface in zip(
            flat_groups,
            lifted_groups,
            surfaces,
            strict=True,
        ):
            morph_anims.append(Transform(flat, lifted))
            morph_anims.append(FadeIn(surface))

        morph_anims.extend(
            [
                FadeOut(x1_dot),
                FadeIn(x1_peak),
                Transform(x1_label, x1_label_target),
            ]
        )

        self.move_camera(
            phi=68 * DEGREES,
            theta=-55 * DEGREES,
            zoom=0.93,
            frame_center=[-0.06, 0.00, 0.90],
            added_anims=morph_anims,
            run_time=3.8,
        )

        self.wait(1.2)