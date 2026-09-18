"""Minimal figure showing the difference in FM integration start time."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    UP,
    Arrow,
    Dot,
    DoubleArrow,
    Line,
    MathTex,
    ManimColor,
    VGroup,
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


# ============================================================
# Layout
# ============================================================

X_LEFT = -2.85
X_RIGHT = 2.85

# Increase the gap between the upper and lower rows
# by giving a little of the outer margins to the center spacing.
Y_TOP = 1.72
Y_BOTTOM = -0.98

START_FRACTION = 0.46


def interpolate_x(
    x_left: float,
    x_right: float,
    fraction: float,
) -> float:
    """Linear position on the horizontal time axis."""
    return (1.0 - fraction) * x_left + fraction * x_right


class FMStartFromIntermediateFigure(LightScene):
    """Compare full FM integration with FM started from an intermediate time."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # ========================================================
        # Top: FM from t = 0
        # ========================================================

        top_start = [X_LEFT, Y_TOP, 0.0]
        top_end = [X_RIGHT, Y_TOP, 0.0]

        top_path = Line(
            top_start,
            top_end,
            color=ACCENT,
            stroke_width=8,
        )

        top_start_dot = Dot(
            top_start,
            radius=0.085,
            color=INK,
        )

        top_end_dot = Dot(
            top_end,
            radius=0.085,
            color=INK,
        )

        top_fm = MathTex(
            r"\mathrm{FM}",
            font_size=36,
            color=ACCENT,
        ).next_to(
            top_path,
            UP,
            buff=0.24,
        )

        top_t0 = MathTex(
            r"t=0",
            font_size=34,
            color=INK,
        ).next_to(
            top_start_dot,
            DOWN,
            buff=0.18,
        )

        top_t1 = MathTex(
            r"t=1",
            font_size=34,
            color=INK,
        ).next_to(
            top_end_dot,
            DOWN,
            buff=0.18,
        )

        top_interval = DoubleArrow(
            [X_LEFT, Y_TOP - 0.85, 0.0],
            [X_RIGHT, Y_TOP - 0.85, 0.0],
            buff=0.0,
            color=MUTED,
            stroke_width=2.2,
            tip_length=0.14,
        )

        top_interval_label = self.jp_text(
            "積分",
            font_size=30,
            color=MUTED,
        ).next_to(
            top_interval,
            DOWN,
            buff=0.12,
        )

        # ========================================================
        # Bottom: FM from intermediate time
        # ========================================================

        start_x = interpolate_x(
            X_LEFT,
            X_RIGHT,
            START_FRACTION,
        )

        bottom_start = [X_LEFT, Y_BOTTOM, 0.0]
        intermediate = [start_x, Y_BOTTOM, 0.0]
        bottom_end = [X_RIGHT, Y_BOTTOM, 0.0]

        skipped_path = Line(
            bottom_start,
            intermediate,
            color=PALE,
            stroke_width=8,
        )

        active_path = Line(
            intermediate,
            bottom_end,
            color=ACCENT,
            stroke_width=8,
        )

        bottom_start_dot = Dot(
            bottom_start,
            radius=0.065,
            color=MUTED,
        )

        intermediate_dot = Dot(
            intermediate,
            radius=0.12,
            color=ACCENT,
        )

        bottom_end_dot = Dot(
            bottom_end,
            radius=0.085,
            color=INK,
        )

        start_label = MathTex(
            r"\mathrm{start}",
            font_size=30,
            color=ACCENT,
        ).next_to(
            intermediate_dot,
            UP,
            buff=0.22,
        )

        bottom_fm = MathTex(
            r"\mathrm{FM}",
            font_size=36,
            color=ACCENT,
        ).next_to(
            active_path,
            UP,
            buff=0.24,
        )

        bottom_t0 = MathTex(
            r"t=0",
            font_size=32,
            color=MUTED,
        ).next_to(
            bottom_start_dot,
            DOWN,
            buff=0.18,
        )

        t_hat = MathTex(
            r"\hat{t}",
            font_size=38,
            color=ACCENT,
        ).next_to(
            intermediate_dot,
            DOWN,
            buff=0.18,
        )

        bottom_t1 = MathTex(
            r"t=1",
            font_size=34,
            color=INK,
        ).next_to(
            bottom_end_dot,
            DOWN,
            buff=0.18,
        )

        bottom_interval = DoubleArrow(
            [start_x, Y_BOTTOM - 0.85, 0.0],
            [X_RIGHT, Y_BOTTOM - 0.85, 0.0],
            buff=0.0,
            color=MUTED,
            stroke_width=2.2,
            tip_length=0.14,
        )

        bottom_interval_label = self.jp_text(
            "積分",
            font_size=30,
            color=MUTED,
        ).next_to(
            bottom_interval,
            DOWN,
            buff=0.12,
        )

        # ========================================================
        # Prediction annotation
        # ========================================================

        predict_label = self.jp_text(
            "中間分布を予測",
            font_size=28,
            color=INK,
        ).move_to([-1.55, -2.72, 0.0])

        predict_arrow = Arrow(
            start=predict_label.get_top() + UP * 0.08 + LEFT * 0.18,
            end=intermediate_dot.get_center() + DOWN * 0.16 + LEFT * 0.04,
            buff=0.04,
            color=INK,
            stroke_width=2.0,
            tip_length=0.14,
        )

        # ========================================================
        # Assemble
        # ========================================================

        top_group = VGroup(
            top_path,
            top_start_dot,
            top_end_dot,
            top_fm,
            top_t0,
            top_t1,
            top_interval,
            top_interval_label,
        )

        bottom_group = VGroup(
            skipped_path,
            active_path,
            bottom_start_dot,
            intermediate_dot,
            bottom_end_dot,
            start_label,
            bottom_fm,
            bottom_t0,
            t_hat,
            bottom_t1,
            bottom_interval,
            bottom_interval_label,
            predict_label,
            predict_arrow,
        )

        figure = VGroup(
            top_group,
            bottom_group,
        )

        figure.move_to([0.0, 0.0, 0.0])

        self.add(figure)