r"""Vertical structural diagram of the prediction heads in CSTM-SFM.

The figure emphasizes the model architecture.

Main structure:
- a shared Front model,
- a Mean Head predicting \hat{\mu},
- a Scale Head predicting a raw scalar a,
- a transformed scale \hat{\sigma},
- a structural CondOT correspondence from \hat{\sigma} to \hat{t},
- a Gaussian q_\phi constructed from \hat{\mu} and \hat{\sigma}.

The note at the bottom distinguishes:
- structural guarantee: \hat{\sigma} <-> \hat{t},
- learned alignment: \hat{\mu} <-> \hat{t}X_1.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    MathTex,
    ManimColor,
    RoundedRectangle,
    VGroup,
    config,
)

from manim_research import LightScene


# ============================================================
# Portrait canvas
# ============================================================

config.frame_width = 5.4
config.frame_height = 8.0


# ============================================================
# Presentation palette
# ============================================================

BACKGROUND = ManimColor("#FFFFFF")

INK = ManimColor("#1F2933")
ACCENT = ManimColor("#2D5B84")
MUTED = ManimColor("#6B7785")

PALE = ManimColor("#D8DEE5")
VERY_FAINT = ManimColor("#EEF2F6")

FRONT_FILL = ManimColor("#EEF3F7")
HEAD_FILL = ManimColor("#F5F7F9")
OUTPUT_FILL = ManimColor("#FFFFFF")
NOTE_FILL = ManimColor("#F8FAFC")


# ============================================================
# Geometry
# ============================================================

FRONT_CENTER = np.array(
    [
        0.0,
        3.10,
        0.0,
    ]
)

MEAN_HEAD_CENTER = np.array(
    [
        -1.30,
        2.00,
        0.0,
    ]
)

SCALE_HEAD_CENTER = np.array(
    [
        1.30,
        2.00,
        0.0,
    ]
)

MU_CENTER = np.array(
    [
        -1.30,
        0.95,
        0.0,
    ]
)

RAW_SCALE_CENTER = np.array(
    [
        1.30,
        1.10,
        0.0,
    ]
)

SIGMA_CENTER = np.array(
    [
        1.30,
        0.35,
        0.0,
    ]
)

CONDOT_CENTER = np.array(
    [
        1.30,
        -0.45,
        0.0,
    ]
)

THAT_CENTER = np.array(
    [
        1.30,
        -1.25,
        0.0,
    ]
)

Q_CENTER = np.array(
    [
        -0.15,
        -2.20,
        0.0,
    ]
)

NOTE_CENTER = np.array(
    [
        0.0,
        -3.30,
        0.0,
    ]
)


# ============================================================
# Styling
# ============================================================

BOX_STROKE_WIDTH = 1.35

ARROW_STROKE_WIDTH = 1.65
ARROW_TIP_LENGTH = 0.12

HEAD_WIDTH = 1.72
HEAD_HEIGHT = 0.62

OUTPUT_HEIGHT = 0.48

NOTE_WIDTH = 4.10
NOTE_HEIGHT = 1.08


# ============================================================
# Drawing helpers
# ============================================================

def make_box(
    scene: LightScene,
    *,
    center: np.ndarray,
    width: float,
    height: float,
    title: str,
    subtitle: str | None = None,
    fill_color: ManimColor = HEAD_FILL,
    stroke_color: ManimColor = ACCENT,
    title_font_size: int = 22,
    subtitle_font_size: int = 15,
) -> VGroup:
    """Create one rounded architecture box."""
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.12,
        stroke_color=stroke_color,
        stroke_width=BOX_STROKE_WIDTH,
        fill_color=fill_color,
        fill_opacity=1.0,
    )

    box.move_to(center)
    box.set_z_index(2)

    if subtitle is None:
        title_text = scene.jp_text(
            title,
            font_size=title_font_size,
            color=INK,
        ).move_to(
            box.get_center()
        )

        title_text.set_z_index(3)

        return VGroup(
            box,
            title_text,
        )

    title_text = scene.jp_text(
        title,
        font_size=title_font_size,
        color=INK,
    )

    subtitle_text = scene.jp_text(
        subtitle,
        font_size=subtitle_font_size,
        color=MUTED,
    )

    text_group = VGroup(
        title_text,
        subtitle_text,
    ).arrange(
        DOWN,
        buff=0.035,
    )

    text_group.move_to(
        box.get_center()
    )

    text_group.set_z_index(3)

    return VGroup(
        box,
        text_group,
    )


def make_math_node(
    *,
    center: np.ndarray,
    latex: str,
    width: float,
    font_size: int = 24,
) -> VGroup:
    """Create a compact mathematical output node."""
    box = RoundedRectangle(
        width=width,
        height=OUTPUT_HEIGHT,
        corner_radius=0.11,
        stroke_color=ACCENT,
        stroke_width=1.25,
        fill_color=OUTPUT_FILL,
        fill_opacity=1.0,
    )

    box.move_to(center)
    box.set_z_index(2)

    label = MathTex(
        latex,
        font_size=font_size,
        color=INK,
    ).move_to(
        box.get_center()
    )

    label.set_z_index(3)

    return VGroup(
        box,
        label,
    )


def make_arrow(
    start: np.ndarray,
    end: np.ndarray,
    *,
    color: ManimColor = ACCENT,
) -> Arrow:
    """Create one architecture arrow."""
    arrow = Arrow(
        start=start,
        end=end,
        buff=0.055,
        color=color,
        stroke_width=ARROW_STROKE_WIDTH,
        tip_length=ARROW_TIP_LENGTH,
        max_tip_length_to_length_ratio=8.0,
        max_stroke_width_to_length_ratio=8.0,
    )

    arrow.set_z_index(0)

    return arrow


# ============================================================
# Figure
# ============================================================

class CSTMSFMHeadStructureFigure(
    LightScene
):
    """Vertical architecture diagram of the CSTM-SFM prediction heads."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # ========================================================
        # Shared front model
        # ========================================================

        front = make_box(
            self,
            center=FRONT_CENTER,
            width=2.05,
            height=0.72,
            title="Front model",
            subtitle="共有特徴",
            fill_color=FRONT_FILL,
            title_font_size=21,
            subtitle_font_size=14,
        )

        # ========================================================
        # Mean / Scale heads
        # ========================================================

        mean_head = make_box(
            self,
            center=MEAN_HEAD_CENTER,
            width=HEAD_WIDTH,
            height=HEAD_HEIGHT,
            title="Mean Head",
            fill_color=HEAD_FILL,
            title_font_size=20,
        )

        scale_head = make_box(
            self,
            center=SCALE_HEAD_CENTER,
            width=HEAD_WIDTH,
            height=HEAD_HEIGHT,
            title="Scale Head",
            fill_color=HEAD_FILL,
            title_font_size=20,
        )

        # ========================================================
        # Head outputs
        # ========================================================

        mu_node = make_math_node(
            center=MU_CENTER,
            latex=r"\hat{\mu}",
            width=0.78,
            font_size=25,
        )

        raw_scale_node = make_math_node(
            center=RAW_SCALE_CENTER,
            latex=r"a",
            width=0.58,
            font_size=24,
        )

        sigma_node = make_math_node(
            center=SIGMA_CENTER,
            latex=r"\hat{\sigma}",
            width=0.82,
            font_size=25,
        )

        condot_box = make_box(
            self,
            center=CONDOT_CENTER,
            width=1.25,
            height=0.52,
            title="CondOT",
            subtitle="対応",
            fill_color=VERY_FAINT,
            title_font_size=18,
            subtitle_font_size=13,
        )

        that_node = make_math_node(
            center=THAT_CENTER,
            latex=r"\hat{t}",
            width=0.72,
            font_size=25,
        )

        # ========================================================
        # Final Gaussian
        # ========================================================

        q_box = RoundedRectangle(
            width=3.45,
            height=0.76,
            corner_radius=0.14,
            stroke_color=ACCENT,
            stroke_width=1.45,
            fill_color=FRONT_FILL,
            fill_opacity=1.0,
        )

        q_box.move_to(
            Q_CENTER
        )

        q_box.set_z_index(2)

        q_label = MathTex(
            r"q_{\phi}"
            r"="
            r"\mathcal{N}"
            r"\!\left("
            r"\hat{\mu},"
            r"\hat{\sigma}^{2}I"
            r"\right)",
            font_size=25,
            color=INK,
        ).move_to(
            q_box.get_center()
        )

        q_label.set_z_index(3)

        q_group = VGroup(
            q_box,
            q_label,
        )

        # ========================================================
        # Note
        # ========================================================

        note_box = RoundedRectangle(
            width=NOTE_WIDTH,
            height=NOTE_HEIGHT,
            corner_radius=0.13,
            stroke_color=PALE,
            stroke_width=1.15,
            fill_color=NOTE_FILL,
            fill_opacity=1.0,
        )

        note_box.move_to(
            NOTE_CENTER
        )

        note_box.set_z_index(1)

        note_title = self.jp_text(
            "対応の意味",
            font_size=17,
            color=INK,
        ).move_to(
            NOTE_CENTER
            + UP * 0.32
        )

        structural_text = self.jp_text(
            "構造で保証",
            font_size=14,
            color=MUTED,
        ).move_to(
            NOTE_CENTER
            + LEFT * 1.10
            + DOWN * 0.02
        )

        structural_math = MathTex(
            r"\hat{\sigma}"
            r"\leftrightarrow"
            r"\hat{t}",
            font_size=19,
            color=INK,
        ).move_to(
            NOTE_CENTER
            + LEFT * 0.05
            + DOWN * 0.02
        )

        learned_text = self.jp_text(
            "学習で整合",
            font_size=14,
            color=MUTED,
        ).move_to(
            NOTE_CENTER
            + RIGHT * 0.80
            + DOWN * 0.02
        )

        learned_math = MathTex(
            r"\hat{\mu}"
            r"\leftrightarrow"
            r"\hat{t}X_1",
            font_size=19,
            color=INK,
        ).move_to(
            NOTE_CENTER
            + RIGHT * 1.65
            + DOWN * 0.02
        )

        note_contents = VGroup(
            note_title,
            structural_text,
            structural_math,
            learned_text,
            learned_math,
        )

        note_contents.set_z_index(3)

        note_group = VGroup(
            note_box,
            note_contents,
        )

        # ========================================================
        # Connections
        # ========================================================

        # Front model -> Mean Head
        front_to_mean = make_arrow(
            front[0].get_bottom()
            + LEFT * 0.48,
            mean_head[0].get_top(),
        )

        # Front model -> Scale Head
        front_to_scale = make_arrow(
            front[0].get_bottom()
            + RIGHT * 0.48,
            scale_head[0].get_top(),
        )

        # Mean Head -> mu
        mean_to_mu = make_arrow(
            mean_head[0].get_bottom(),
            mu_node[0].get_top(),
        )

        # Scale Head -> raw scalar a
        scale_to_a = make_arrow(
            scale_head[0].get_bottom(),
            raw_scale_node[0].get_top(),
        )

        # a -> sigma
        a_to_sigma = make_arrow(
            raw_scale_node[0].get_bottom(),
            sigma_node[0].get_top(),
        )

        # sigma -> CondOT correspondence
        sigma_to_condot = make_arrow(
            sigma_node[0].get_bottom(),
            condot_box[0].get_top(),
        )

        # CondOT -> t-hat
        condot_to_that = make_arrow(
            condot_box[0].get_bottom(),
            that_node[0].get_top(),
        )

        # mu -> q_phi
        mu_to_q = make_arrow(
            mu_node[0].get_bottom(),
            q_box.get_top()
            + LEFT * 0.95,
        )

        # sigma -> q_phi
        sigma_to_q = make_arrow(
            sigma_node[0].get_left()
            + DOWN * 0.05,
            q_box.get_top()
            + RIGHT * 0.75,
        )

        # ========================================================
        # Assemble
        # ========================================================

        connectors = VGroup(
            front_to_mean,
            front_to_scale,
            mean_to_mu,
            scale_to_a,
            a_to_sigma,
            sigma_to_condot,
            condot_to_that,
            mu_to_q,
            sigma_to_q,
        )

        architecture = VGroup(
            connectors,
            front,
            mean_head,
            scale_head,
            mu_node,
            raw_scale_node,
            sigma_node,
            condot_box,
            that_node,
            q_group,
            note_group,
        )

        self.add(
            architecture
        )