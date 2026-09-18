"""Vector reconstruction of the hand-drawn sketch from IMG_0278.jpeg.

The photograph is interpreted in landscape orientation (rotated 90 degrees
counter-clockwise from the uploaded portrait). The scene intentionally keeps
the loose, layered geometry of the sketch while replacing pen strokes with
editable Manim primitives.
"""

from __future__ import annotations

import numpy as np
from manim import (
    BLACK,
    Arrow,
    Create,
    Dot,
    Ellipse,
    FadeIn,
    LaggedStart,
    Line,
    Polygon,
    Square,
    VGroup,
    VMobject,
)

from manim_research import LightScene


INK = BLACK


def smooth_path(
    points: list[tuple[float, float]],
    *,
    stroke_width: float = 2.0,
    opacity: float = 0.82,
) -> VMobject:
    """Create one smooth pen-like curve through 2-D control points."""
    path = VMobject()
    path.set_points_smoothly([np.array([x, y, 0.0]) for x, y in points])
    path.set_stroke(INK, width=stroke_width, opacity=opacity)
    return path


def cross_mark(
    x: float,
    y: float,
    *,
    size: float = 0.18,
    stroke_width: float = 2.0,
) -> VGroup:
    """Small X marker used throughout the original sketch."""
    return VGroup(
        Line(
            [x - size, y - size, 0],
            [x + size, y + size, 0],
            color=INK,
            stroke_width=stroke_width,
        ),
        Line(
            [x - size, y + size, 0],
            [x + size, y - size, 0],
            color=INK,
            stroke_width=stroke_width,
        ),
    )


def parallel_strokes(
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    count: int = 4,
    gap: float = 0.055,
    stroke_width: float = 1.6,
) -> VGroup:
    """Bundle of nearly parallel lines that mimics scribbled emphasis."""
    x0, y0 = start
    x1, y1 = end
    dx = x1 - x0
    dy = y1 - y0
    length = max((dx**2 + dy**2) ** 0.5, 1e-6)
    nx = -dy / length
    ny = dx / length

    strokes = VGroup()
    center = (count - 1) / 2
    for i in range(count):
        offset = (i - center) * gap
        strokes.add(
            Line(
                [x0 + nx * offset, y0 + ny * offset, 0],
                [x1 + nx * offset, y1 + ny * offset, 0],
                color=INK,
                stroke_width=stroke_width,
            )
        )
    return strokes


class SketchReconstruction(LightScene):
    """Clean Manim version of the uploaded hand-drawn composition."""

    def construct(self) -> None:
        central_loop = smooth_path(
            [
                (-3.25, -0.25), (-2.65, -1.00), (-1.75, -1.95),
                (-0.10, -2.30), (1.35, -2.20), (2.65, -1.55),
                (2.30, -0.35), (1.25, 0.55), (-0.45, 0.90),
                (-1.80, 0.55), (-2.75, 0.10), (-3.25, -0.25),
            ],
            stroke_width=2.3,
            opacity=0.84,
        )

        upper_left_loop = smooth_path(
            [
                (-3.45, 1.05), (-3.55, 2.15), (-3.10, 2.75),
                (-2.45, 2.55), (-1.85, 1.65), (-1.70, 0.72),
            ],
            stroke_width=2.0,
            opacity=0.72,
        )

        right_channel = smooth_path(
            [
                (1.55, 2.95), (1.92, 2.18), (2.08, 1.28),
                (2.55, 0.70), (3.35, 0.25), (4.15, -0.05),
                (4.95, -0.55),
            ],
            stroke_width=2.1,
            opacity=0.78,
        )

        right_inner = smooth_path(
            [
                (1.08, 2.65), (1.35, 1.82), (1.72, 1.05),
                (2.08, 0.55), (2.95, 0.18), (3.85, -0.20),
            ],
            stroke_width=1.7,
            opacity=0.70,
        )

        lower_right_loop = smooth_path(
            [
                (2.05, 0.18), (2.45, -0.95), (3.15, -1.62),
                (4.05, -1.78), (4.55, -1.32), (4.15, -0.72),
                (3.20, -0.30), (2.05, 0.18),
            ],
            stroke_width=2.0,
            opacity=0.76,
        )

        target_island = (
            Ellipse(width=2.45, height=0.85, color=INK, stroke_width=2.0)
            .rotate(-0.10)
            .move_to([4.15, 2.60, 0])
        )
        target_pin = Dot([4.00, 2.55, 0], radius=0.035, color=INK)
        target_pole = Line(
            target_pin.get_center(),
            [4.00, 3.30, 0],
            color=INK,
            stroke_width=2.0,
        )
        target_flag = Polygon(
            [4.00, 3.30, 0],
            [4.65, 3.13, 0],
            [4.08, 2.97, 0],
            color=INK,
            stroke_width=1.7,
        )

        regions = VGroup(
            central_loop,
            upper_left_loop,
            right_channel,
            right_inner,
            lower_right_loop,
            target_island,
            target_pin,
            target_pole,
            target_flag,
        )

        source_box = Square(side_length=0.62, color=INK, stroke_width=2.0).move_to(
            [-5.72, -2.55, 0]
        )
        source_dot = Dot([-5.88, -2.53, 0], radius=0.11, color=INK)
        source_bundle = parallel_strokes(
            (-5.62, -2.45),
            (-4.52, -2.00),
            count=5,
            gap=0.045,
        )

        rays = VGroup(
            Line([-5.65, -2.48, 0], [-2.62, -0.30, 0], color=INK, stroke_width=1.4),
            Line([-5.68, -2.50, 0], [-0.55, 0.80, 0], color=INK, stroke_width=1.4),
            Line([-4.90, -1.90, 0], [0.65, -0.55, 0], color=INK, stroke_width=1.4),
            Arrow(
                [-4.55, -1.78, 0],
                [-2.30, -1.70, 0],
                buff=0,
                color=INK,
                stroke_width=1.6,
                max_tip_length_to_length_ratio=0.05,
            ),
        )
        source = VGroup(source_box, source_dot, source_bundle, rays)

        hub = Dot([-1.15, -0.48, 0], radius=0.045, color=INK)
        hub_paths = VGroup(
            smooth_path(
                [(-3.05, -0.10), (-2.10, 0.28), (-1.20, -0.42), (0.45, -0.05), (1.65, -0.25)],
                stroke_width=1.7,
            ),
            smooth_path(
                [(-2.20, 0.50), (-1.65, 0.25), (-1.10, -0.48), (-0.60, -1.10), (0.10, -1.55)],
                stroke_width=1.7,
            ),
            smooth_path(
                [(-2.00, 0.78), (-1.55, 0.35), (-1.15, -0.48), (-0.55, 0.25), (-0.20, 1.20)],
                stroke_width=1.6,
            ),
            smooth_path(
                [(-1.20, -0.48), (-0.30, -0.15), (0.35, 0.75), (1.10, 1.52)],
                stroke_width=1.6,
            ),
            Line([-1.10, -0.45, 0], [2.25, -1.62, 0], color=INK, stroke_width=1.5),
            Line([-1.10, -0.45, 0], [2.35, 0.45, 0], color=INK, stroke_width=1.5),
        )

        central_scribble = VGroup(
            parallel_strokes((-2.52, 0.08), (-1.65, 0.47), count=4, gap=0.035),
            parallel_strokes((-2.08, -0.28), (-1.45, -0.82), count=4, gap=0.035),
            Line([-1.00, -0.70, 0], [-0.55, -0.75, 0], color=INK, stroke_width=1.4),
            Line([-0.95, -0.60, 0], [-0.80, -0.15, 0], color=INK, stroke_width=1.4),
            Line([-0.80, -0.58, 0], [-0.35, -0.45, 0], color=INK, stroke_width=1.4),
        )

        trajectories = VGroup(
            Line([-2.95, 0.25, 0], [2.95, -1.42, 0], color=INK, stroke_width=1.25),
            Line([-2.70, 0.55, 0], [3.15, 0.10, 0], color=INK, stroke_width=1.25),
            Line([-2.35, 0.00, 0], [1.30, 2.70, 0], color=INK, stroke_width=1.25),
            Line([-1.35, -1.90, 0], [1.38, 1.78, 0], color=INK, stroke_width=1.25),
            Line([-0.50, -2.00, 0], [2.30, 0.20, 0], color=INK, stroke_width=1.25),
            smooth_path(
                [
                    (-0.25, -1.95), (0.30, -1.15), (1.00, -0.35),
                    (1.75, 0.65), (2.15, 1.65),
                ],
                stroke_width=1.35,
                opacity=0.70,
            ),
        )

        top_detector = VGroup(
            parallel_strokes((-0.45, 2.00), (-0.45, 2.78), count=4, gap=0.035),
            smooth_path([(-0.85, 3.05), (-0.45, 3.20), (-0.05, 3.02)], stroke_width=1.5),
            Line([-0.75, 3.05, 0], [-0.20, 2.88, 0], color=INK, stroke_width=1.2),
            Line([-0.70, 2.92, 0], [-0.18, 3.08, 0], color=INK, stroke_width=1.2),
        )
        top_links = VGroup(
            Line([-0.18, 3.02, 0], [1.32, 2.22, 0], color=INK, stroke_width=1.35),
            Line([-0.10, 2.95, 0], [1.72, 0.95, 0], color=INK, stroke_width=1.15),
        )

        crosses = VGroup(
            cross_mark(-4.55, -1.95),
            cross_mark(-3.18, -0.02),
            cross_mark(-2.72, 0.28),
            cross_mark(-1.70, 0.72),
            cross_mark(-1.20, -1.62),
            cross_mark(-0.02, -1.94),
            cross_mark(0.05, 0.95),
            cross_mark(0.82, -0.16),
            cross_mark(1.45, 2.10),
            cross_mark(1.62, 0.62),
            cross_mark(2.12, -1.45),
            cross_mark(2.55, 0.24),
            cross_mark(3.72, -1.22),
            cross_mark(4.35, -0.52),
        )

        loose_arrows = VGroup(
            Arrow(
                [-3.65, -2.05, 0],
                [-4.52, -2.05, 0],
                buff=0,
                color=INK,
                stroke_width=1.4,
                max_tip_length_to_length_ratio=0.08,
            ),
            Arrow(
                [2.65, 0.10, 0],
                [3.62, 0.48, 0],
                buff=0,
                color=INK,
                stroke_width=1.3,
                max_tip_length_to_length_ratio=0.08,
            ),
            Arrow(
                [1.52, 1.05, 0],
                [0.68, 1.38, 0],
                buff=0,
                color=INK,
                stroke_width=1.3,
                max_tip_length_to_length_ratio=0.08,
            ),
            Arrow(
                [-0.10, -0.20, 0],
                [0.62, -0.16, 0],
                buff=0,
                color=INK,
                stroke_width=1.3,
                max_tip_length_to_length_ratio=0.08,
            ),
        )

        self.play(
            LaggedStart(
                *[Create(mob) for mob in regions if not isinstance(mob, Dot)],
                lag_ratio=0.06,
                run_time=2.4,
            ),
            FadeIn(VGroup(target_pin)),
        )
        self.play(
            LaggedStart(
                *[Create(mob) for mob in source if not isinstance(mob, Dot)],
                lag_ratio=0.05,
                run_time=1.8,
            ),
            FadeIn(source_dot),
        )
        self.play(
            LaggedStart(
                *[Create(mob) for mob in hub_paths],
                *[Create(mob) for mob in central_scribble],
                lag_ratio=0.035,
                run_time=2.2,
            ),
            FadeIn(hub),
        )
        self.play(
            LaggedStart(
                *[Create(mob) for mob in trajectories],
                *[Create(mob) for mob in top_detector],
                *[Create(mob) for mob in top_links],
                lag_ratio=0.025,
                run_time=2.4,
            )
        )
        self.play(
            LaggedStart(
                *[Create(mob) for mob in crosses],
                *[Create(mob) for mob in loose_arrows],
                lag_ratio=0.025,
                run_time=1.6,
            )
        )
        self.wait(1.0)
