"""Slide-ready integrated system illustration for the Group B disaster-response deck.

This scene is designed for a single still image to be embedded into slides.
It visualizes:
1. contour-line mountains,
2. a swarm-controlled drone network,
3. an AI / integration hub,
4. an AR head-display interface for responders.

Suggested render:
    pixi run manim -- --resolution 1920,1080 -s projects/groupb_system/groupb_system.py IntegratedRescueSystemSlide
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arc,
    Arrow,
    Circle,
    DashedLine,
    Dot,
    Line,
    Polygon,
    RoundedRectangle,
    Square,
    Triangle,
    VGroup,
    VMobject,
)

from manim_research import LightScene


def smooth_curve(
    points: list[tuple[float, float]],
    *,
    color,
    stroke_width: float = 2.0,
    opacity: float = 1.0,
) -> VMobject:
    """Create a smooth contour-like curve."""
    curve = VMobject()
    curve.set_points_smoothly([np.array([x, y, 0.0]) for x, y in points])
    curve.set_stroke(color, width=stroke_width, opacity=opacity)
    return curve


def drone_icon(color, *, scale_factor: float = 1.0) -> VGroup:
    """Small drone pictogram for the swarm network."""
    body = RoundedRectangle(
        width=0.42,
        height=0.18,
        corner_radius=0.06,
        stroke_color=color,
        fill_color=color,
        fill_opacity=1.0,
        stroke_width=1.6,
    )
    arm_l = Line([-0.36, 0.0, 0], [-0.10, 0.0, 0], color=color, stroke_width=2)
    arm_r = Line([0.10, 0.0, 0], [0.36, 0.0, 0], color=color, stroke_width=2)
    arm_u = Line([0.0, 0.10, 0], [0.0, 0.30, 0], color=color, stroke_width=2)
    arm_d = Line([0.0, -0.10, 0], [0.0, -0.30, 0], color=color, stroke_width=2)

    rotors = VGroup(
        Circle(radius=0.09, color=color, stroke_width=1.8).move_to([-0.42, 0.0, 0]),
        Circle(radius=0.09, color=color, stroke_width=1.8).move_to([0.42, 0.0, 0]),
        Circle(radius=0.09, color=color, stroke_width=1.8).move_to([0.0, 0.36, 0]),
        Circle(radius=0.09, color=color, stroke_width=1.8).move_to([0.0, -0.36, 0]),
    )
    return VGroup(body, arm_l, arm_r, arm_u, arm_d, rotors).scale(scale_factor)


class IntegratedRescueSystemSlide(LightScene):
    """Single-frame illustration for the proposal slide."""

    def construct(self) -> None:
        accent = self.theme.accent
        secondary = self.theme.secondary
        fg = self.theme.foreground
        muted = self.theme.muted

        contour_color = "#4F87B8"
        contour_soft = "#A9C8E5"
        contour_fill = "#DCEBF7"
        panel_fill = "#F8FBFE"
        panel_stroke = "#CBD5E1"

        def chip(text: str, *, width: float = 1.9, fill_color: str = "#E8F1FB") -> VGroup:
            box = RoundedRectangle(
                width=width,
                height=0.48,
                corner_radius=0.12,
                stroke_color=fill_color,
                fill_color=fill_color,
                fill_opacity=1.0,
                stroke_width=1.0,
            )
            label = self.jp_text(text, font_size=20, color=fg)
            return VGroup(box, label)

        # ------------------------------------------------------------------
        # Title area
        # ------------------------------------------------------------------
        title = self.jp_text(
            "群制御ドローン × ARヘッドディスプレイ統合システム",
            font_size=34,
            color=fg,
            weight="BOLD",
        ).to_edge(UP, buff=0.28)
        subtitle = self.jp_text(
            "等高線で地形を捉え、空から集めた情報を現場の視界へ重ねる",
            font_size=20,
            color=muted,
        ).next_to(title, DOWN, buff=0.12)

        # ------------------------------------------------------------------
        # Left panel: contour mountains + drone swarm
        # ------------------------------------------------------------------
        left_panel = RoundedRectangle(
            width=6.2,
            height=5.6,
            corner_radius=0.18,
            stroke_color=panel_stroke,
            fill_color=panel_fill,
            fill_opacity=1.0,
            stroke_width=1.2,
        ).move_to([-3.6, -0.2, 0])

        left_title = self.jp_text("地形把握と群制御ドローン", font_size=24, color=fg, weight="BOLD")
        left_title.next_to(left_panel.get_top(), DOWN, buff=0.22).align_to(left_panel, LEFT).shift(RIGHT * 0.30)

        mountain_back = Polygon(
            [-6.15, -2.45, 0],
            [-5.10, -0.95, 0],
            [-4.25, -1.55, 0],
            [-3.20, -0.55, 0],
            [-2.20, -1.15, 0],
            [-1.10, -0.50, 0],
            [-1.10, -2.45, 0],
            color=contour_soft,
            fill_color="#EAF3FB",
            fill_opacity=1.0,
            stroke_opacity=0,
        )
        mountain_mid = Polygon(
            [-6.15, -2.45, 0],
            [-5.50, -1.70, 0],
            [-4.55, -0.90, 0],
            [-3.85, -1.35, 0],
            [-2.95, -0.70, 0],
            [-2.15, -1.15, 0],
            [-1.35, -0.85, 0],
            [-1.10, -1.02, 0],
            [-1.10, -2.45, 0],
            color=contour_soft,
            fill_color="#DDEDF9",
            fill_opacity=1.0,
            stroke_opacity=0,
        )
        mountain_front = Polygon(
            [-6.15, -2.45, 0],
            [-5.85, -1.95, 0],
            [-5.15, -1.28, 0],
            [-4.55, -1.65, 0],
            [-3.75, -1.05, 0],
            [-3.15, -1.58, 0],
            [-2.30, -1.05, 0],
            [-1.60, -1.45, 0],
            [-1.10, -1.22, 0],
            [-1.10, -2.45, 0],
            color=contour_soft,
            fill_color=contour_fill,
            fill_opacity=1.0,
            stroke_opacity=0,
        )

        contour_lines = VGroup(
            smooth_curve(
                [(-5.85, -1.70), (-5.15, -1.25), (-4.55, -1.36), (-3.82, -0.96), (-3.15, -1.16), (-2.38, -0.82), (-1.55, -0.96)],
                color=contour_color,
                stroke_width=2.2,
            ),
            smooth_curve(
                [(-5.95, -1.42), (-5.32, -1.02), (-4.62, -1.12), (-3.90, -0.70), (-3.10, -0.92), (-2.35, -0.48), (-1.65, -0.58)],
                color=contour_color,
                stroke_width=1.8,
                opacity=0.95,
            ),
            smooth_curve(
                [(-5.98, -1.10), (-5.42, -0.72), (-4.75, -0.78), (-4.02, -0.38), (-3.22, -0.55), (-2.55, -0.18), (-1.95, -0.22)],
                color=contour_color,
                stroke_width=1.6,
                opacity=0.9,
            ),
            smooth_curve(
                [(-5.68, -2.00), (-5.00, -1.68), (-4.25, -1.84), (-3.45, -1.52), (-2.78, -1.72), (-2.00, -1.36), (-1.35, -1.48)],
                color=contour_color,
                stroke_width=1.5,
                opacity=0.9,
            ),
            smooth_curve(
                [(-5.52, -0.56), (-5.02, -0.26), (-4.35, -0.28), (-3.55, 0.08), (-2.82, 0.02), (-2.15, 0.28), (-1.68, 0.24)],
                color=contour_color,
                stroke_width=1.4,
                opacity=0.75,
            ),
            smooth_curve(
                [(-4.85, -0.08), (-4.45, 0.16), (-3.82, 0.22), (-3.22, 0.52), (-2.55, 0.50), (-1.95, 0.72)],
                color=contour_color,
                stroke_width=1.2,
                opacity=0.68,
            ),
        )

        contour_peak_1 = VGroup(
            Circle(radius=0.22, color=contour_color, stroke_width=1.2, fill_opacity=0).move_to([-4.65, -0.82, 0]),
            Circle(radius=0.42, color=contour_color, stroke_width=1.0, fill_opacity=0).move_to([-4.65, -0.82, 0]),
        )
        contour_peak_2 = VGroup(
            Circle(radius=0.20, color=contour_color, stroke_width=1.2, fill_opacity=0).move_to([-2.78, -0.45, 0]),
            Circle(radius=0.38, color=contour_color, stroke_width=1.0, fill_opacity=0).move_to([-2.78, -0.45, 0]),
        )

        drones = VGroup(
            drone_icon(accent, scale_factor=0.48).move_to([-5.0, 1.18, 0]),
            drone_icon(accent, scale_factor=0.48).move_to([-4.05, 0.65, 0]),
            drone_icon(accent, scale_factor=0.48).move_to([-3.15, 1.18, 0]),
            drone_icon(accent, scale_factor=0.48).move_to([-2.15, 0.55, 0]),
            drone_icon(accent, scale_factor=0.48).move_to([-1.55, 1.06, 0]),
        )

        base = VGroup(
            RoundedRectangle(
                width=1.35,
                height=0.62,
                corner_radius=0.12,
                stroke_color=accent,
                fill_color="#E7F3FD",
                fill_opacity=1.0,
                stroke_width=1.4,
            ),
            self.jp_text("活動拠点", font_size=19, color=fg, weight="BOLD"),
        ).move_to([-5.1, 2.05, 0])

        lost_person = VGroup(
            Circle(radius=0.12, color=secondary, fill_color=secondary, fill_opacity=1.0),
            Line([0, -0.12, 0], [0, -0.40, 0], color=secondary, stroke_width=2.5),
            Line([0, -0.22, 0], [-0.15, -0.35, 0], color=secondary, stroke_width=2.2),
            Line([0, -0.22, 0], [0.15, -0.35, 0], color=secondary, stroke_width=2.2),
            Line([0, -0.40, 0], [-0.15, -0.58, 0], color=secondary, stroke_width=2.2),
            Line([0, -0.40, 0], [0.15, -0.58, 0], color=secondary, stroke_width=2.2),
        ).scale(0.8).move_to([-1.95, -1.55, 0])

        danger_zone = Polygon(
            [-2.20, -0.15, 0],
            [-1.55, 0.55, 0],
            [-1.05, 0.10, 0],
            [-1.32, -0.55, 0],
            color="#EF4444",
            fill_color="#FCA5A5",
            fill_opacity=0.45,
            stroke_width=2.0,
        )
        danger_outline = VGroup(
            DashedLine([-2.20, -0.15, 0], [-1.55, 0.55, 0], dash_length=0.08, color="#DC2626"),
            DashedLine([-1.55, 0.55, 0], [-1.05, 0.10, 0], dash_length=0.08, color="#DC2626"),
            DashedLine([-1.05, 0.10, 0], [-1.32, -0.55, 0], dash_length=0.08, color="#DC2626"),
            DashedLine([-1.32, -0.55, 0], [-2.20, -0.15, 0], dash_length=0.08, color="#DC2626"),
        )
        warning = VGroup(
            Triangle(color="#DC2626", fill_color="#DC2626", fill_opacity=1.0).scale(0.22),
            self.jp_text("崩落リスク", font_size=18, color="#991B1B", weight="BOLD"),
        ).arrange(RIGHT, buff=0.10).move_to([-1.55, 0.88, 0])

        links = VGroup(
            Line(base.get_bottom() + [0.0, -0.10, 0], drones[0].get_top(), color=accent, stroke_width=1.8),
            Line(drones[0].get_right(), drones[1].get_left(), color=accent, stroke_width=1.8),
            Line(drones[1].get_right(), drones[2].get_left(), color=accent, stroke_width=1.8),
            Line(drones[2].get_right(), drones[4].get_left(), color=accent, stroke_width=1.8),
            Line(drones[1].get_bottom(), drones[3].get_top(), color=accent, stroke_width=1.8),
            Line(drones[2].get_bottom(), drones[3].get_top(), color=accent, stroke_width=1.8),
        )

        scan_beams = VGroup(
            DashedLine(drones[1].get_bottom(), [-4.20, -0.75, 0], color=accent, dash_length=0.08),
            DashedLine(drones[2].get_bottom(), [-3.05, -0.62, 0], color=accent, dash_length=0.08),
            DashedLine(drones[4].get_bottom(), [-1.80, -0.02, 0], color=accent, dash_length=0.08),
        )

        contour_chip = chip("等高線地図", width=1.6).move_to([-5.25, 2.55, 0])
        swarm_chip = chip("群制御", width=1.35, fill_color="#E0F2FE").move_to([-3.65, 2.55, 0])
        search_chip = chip("捜索・監視", width=1.75, fill_color="#FCE7F3").move_to([-2.00, 2.55, 0])

        # ------------------------------------------------------------------
        # Center hub: data fusion / AI
        # ------------------------------------------------------------------
        hub_panel = RoundedRectangle(
            width=2.15,
            height=4.65,
            corner_radius=0.18,
            stroke_color=panel_stroke,
            fill_color=panel_fill,
            fill_opacity=1.0,
            stroke_width=1.2,
        ).move_to([0.05, -0.05, 0])

        hub_circle = Circle(
            radius=0.68,
            color=accent,
            stroke_width=2.5,
            fill_color="#E0F2FE",
            fill_opacity=1.0,
        ).move_to([0.05, 0.88, 0])
        ai_ring = Arc(radius=0.88, start_angle=0.45, angle=5.0, color=accent, stroke_width=2.0).move_to(hub_circle)
        hub_nodes = VGroup(
            Dot(hub_circle.get_center() + UP * 0.20, radius=0.045, color=accent),
            Dot(hub_circle.get_center() + LEFT * 0.18 + DOWN * 0.10, radius=0.045, color=accent),
            Dot(hub_circle.get_center() + RIGHT * 0.18 + DOWN * 0.10, radius=0.045, color=accent),
        )
        hub_edges = VGroup(
            Line(hub_nodes[0].get_center(), hub_nodes[1].get_center(), color=accent, stroke_width=2.0),
            Line(hub_nodes[1].get_center(), hub_nodes[2].get_center(), color=accent, stroke_width=2.0),
            Line(hub_nodes[2].get_center(), hub_nodes[0].get_center(), color=accent, stroke_width=2.0),
        )

        hub_title = self.jp_text("統合判断エンジン", font_size=22, color=fg, weight="BOLD").next_to(hub_circle, DOWN, buff=0.22)
        hub_desc_1 = self.jp_text("• 群制御経路生成", font_size=18, color=fg).next_to(hub_title, DOWN, buff=0.18)
        hub_desc_2 = self.jp_text("• 危険度推定", font_size=18, color=fg).next_to(hub_desc_1, DOWN, buff=0.10)
        hub_desc_3 = self.jp_text("• 要救助者候補統合", font_size=18, color=fg).next_to(hub_desc_2, DOWN, buff=0.10)
        hub_desc_4 = self.jp_text("• 音声 / AR指示生成", font_size=18, color=fg).next_to(hub_desc_3, DOWN, buff=0.10)

        arrow_left_to_hub = Arrow(
            left_panel.get_right() + RIGHT * 0.05 + UP * 0.62,
            hub_panel.get_left() + LEFT * 0.05 + UP * 0.62,
            buff=0.05,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.08,
            color=accent,
        )
        left_to_hub_label = self.jp_text("センシング", font_size=18, color=accent, weight="BOLD").next_to(arrow_left_to_hub, UP, buff=0.06)

        # ------------------------------------------------------------------
        # Right panel: AR head display
        # ------------------------------------------------------------------
        right_panel = RoundedRectangle(
            width=5.25,
            height=5.6,
            corner_radius=0.18,
            stroke_color=panel_stroke,
            fill_color=panel_fill,
            fill_opacity=1.0,
            stroke_width=1.2,
        ).move_to([4.0, -0.2, 0])

        right_title = self.jp_text("現場隊員のARヘッドディスプレイ", font_size=24, color=fg, weight="BOLD")
        right_title.next_to(right_panel.get_top(), DOWN, buff=0.22).align_to(right_panel, LEFT).shift(RIGHT * 0.30)

        head = Circle(radius=0.88, color=fg, stroke_width=2.0, fill_color="#F3F4F6", fill_opacity=1.0).move_to([3.30, -0.20, 0])
        helmet = Arc(radius=1.02, start_angle=np.pi, angle=np.pi, color=fg, stroke_width=2.5).move_to([3.30, 0.05, 0])
        helmet_band = RoundedRectangle(
            width=2.15,
            height=0.34,
            corner_radius=0.10,
            stroke_color=fg,
            fill_color="#D1D5DB",
            fill_opacity=1.0,
            stroke_width=1.8,
        ).move_to([3.30, 0.68, 0])
        lamp = RoundedRectangle(
            width=0.42,
            height=0.28,
            corner_radius=0.08,
            stroke_color=fg,
            fill_color="#94A3B8",
            fill_opacity=1.0,
            stroke_width=1.8,
        ).move_to([3.30, 0.98, 0])

        visor = RoundedRectangle(
            width=2.05,
            height=0.78,
            corner_radius=0.12,
            stroke_color=accent,
            fill_color="#BFDBFE",
            fill_opacity=0.45,
            stroke_width=2.2,
        ).move_to([3.35, 0.02, 0])

        mask = Polygon(
            [2.72, -0.10, 0],
            [3.86, -0.10, 0],
            [4.12, -0.42, 0],
            [3.98, -1.08, 0],
            [3.25, -1.35, 0],
            [2.52, -1.05, 0],
            [2.48, -0.45, 0],
            color=fg,
            fill_color="#374151",
            fill_opacity=1.0,
            stroke_width=2.0,
        )
        filter_box = RoundedRectangle(
            width=0.52,
            height=0.32,
            corner_radius=0.06,
            stroke_color="#9CA3AF",
            fill_color="#6B7280",
            fill_opacity=1.0,
            stroke_width=1.6,
        ).move_to([3.72, -0.78, 0])

        eye_l = Dot([3.02, 0.00, 0], radius=0.045, color=fg)
        eye_r = Dot([3.52, 0.00, 0], radius=0.045, color=fg)
        brow_l = Line([2.82, 0.18, 0], [3.15, 0.10, 0], color=fg, stroke_width=2.2)
        brow_r = Line([3.40, 0.10, 0], [3.70, 0.18, 0], color=fg, stroke_width=2.2)

        hud_center = Circle(radius=0.10, color=accent, stroke_width=1.6, fill_opacity=0).move_to([4.06, -0.02, 0])
        hud_cross = VGroup(
            Line([3.92, -0.02, 0], [4.20, -0.02, 0], color=accent, stroke_width=1.2),
            Line([4.06, -0.16, 0], [4.06, 0.12, 0], color=accent, stroke_width=1.2),
        )
        hud_path = smooth_curve(
            [(2.62, -0.40), (3.00, -0.35), (3.38, -0.28), (3.72, -0.08), (4.02, 0.06)],
            color=accent,
            stroke_width=2.2,
            opacity=0.9,
        )
        hud_waypoints = VGroup(
            Dot([2.90, -0.34, 0], radius=0.028, color=accent),
            Dot([3.28, -0.28, 0], radius=0.028, color=accent),
            Dot([3.62, -0.16, 0], radius=0.028, color=accent),
        )

        info_box_1 = RoundedRectangle(
            width=1.85,
            height=0.82,
            corner_radius=0.12,
            stroke_color=accent,
            fill_color="#FFFFFF",
            fill_opacity=0.96,
            stroke_width=1.4,
        ).move_to([5.55, 1.25, 0])
        info_title_1 = self.jp_text("活動拠点", font_size=18, color=fg, weight="BOLD").move_to(info_box_1.get_center() + UP * 0.14)
        info_line_1 = self.jp_text("距離: 350m", font_size=17, color=fg).move_to(info_box_1.get_center() + DOWN * 0.18)

        info_box_2 = RoundedRectangle(
            width=2.10,
            height=0.96,
            corner_radius=0.12,
            stroke_color="#DC2626",
            fill_color="#FFFFFF",
            fill_opacity=0.96,
            stroke_width=1.4,
        ).move_to([5.65, 0.10, 0])
        info_title_2 = self.jp_text("危険領域", font_size=18, color="#991B1B", weight="BOLD").move_to(info_box_2.get_center() + UP * 0.18)
        info_line_2 = self.jp_text("前方斜面に崩落リスク", font_size=16, color=fg).move_to(info_box_2.get_center() + DOWN * 0.16)

        info_box_3 = RoundedRectangle(
            width=2.40,
            height=1.24,
            corner_radius=0.12,
            stroke_color=accent,
            fill_color="#FFFFFF",
            fill_opacity=0.97,
            stroke_width=1.4,
        ).move_to([5.70, -1.15, 0])
        info_title_3 = self.jp_text("AI解析からの助言", font_size=18, color=fg, weight="BOLD").move_to(info_box_3.get_center() + UP * 0.34)
        info_line_3a = self.jp_text("• 隊から離れています", font_size=15, color=fg).move_to(info_box_3.get_center() + UP * 0.06)
        info_line_3b = self.jp_text("• 右へ迂回して進行", font_size=15, color=fg).move_to(info_box_3.get_center() + DOWN * 0.16)
        info_line_3c = self.jp_text("• 要救助者候補まで 120m", font_size=15, color=fg).move_to(info_box_3.get_center() + DOWN * 0.38)

        arrow_hub_to_right = Arrow(
            hub_panel.get_right() + RIGHT * 0.05,
            right_panel.get_left() + LEFT * 0.05,
            buff=0.06,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.08,
            color=accent,
        )
        hub_to_right_label = self.jp_text("AR指示 / 音声通知", font_size=18, color=accent, weight="BOLD").next_to(arrow_hub_to_right, UP, buff=0.06)

        # ------------------------------------------------------------------
        # Bottom benefit strip
        # ------------------------------------------------------------------
        benefit_1 = VGroup(
            Circle(radius=0.23, color=accent, fill_color="#E0F2FE", fill_opacity=1.0, stroke_width=1.6),
            self.jp_text("迅速な\n状況把握", font_size=17, color=fg, weight="BOLD"),
        )
        benefit_1[1].move_to(benefit_1[0].get_center() + DOWN * 0.70)

        benefit_2 = VGroup(
            Circle(radius=0.23, color=secondary, fill_color="#FCE7F3", fill_opacity=1.0, stroke_width=1.6),
            self.jp_text("二次災害\nリスク低減", font_size=17, color=fg, weight="BOLD"),
        )
        benefit_2[1].move_to(benefit_2[0].get_center() + DOWN * 0.70)

        benefit_3 = VGroup(
            Circle(radius=0.23, color=accent, fill_color="#E0F2FE", fill_opacity=1.0, stroke_width=1.6),
            self.jp_text("現場判断を\n一貫支援", font_size=17, color=fg, weight="BOLD"),
        )
        benefit_3[1].move_to(benefit_3[0].get_center() + DOWN * 0.70)

        benefits = VGroup(benefit_1, benefit_2, benefit_3).arrange(RIGHT, buff=1.4).move_to([1.1, -3.15, 0])

        footer = self.jp_text(
            "空からの群制御センシング → 統合解析 → 現場AR提示 の一体化",
            font_size=18,
            color=muted,
        ).move_to([0.2, -3.50, 0])

        # ------------------------------------------------------------------
        # Compose scene
        # ------------------------------------------------------------------
        self.add(
            title,
            subtitle,
            left_panel,
            left_title,
            mountain_back,
            mountain_mid,
            mountain_front,
            contour_lines,
            contour_peak_1,
            contour_peak_2,
            drones,
            base,
            lost_person,
            danger_zone,
            danger_outline,
            warning,
            links,
            scan_beams,
            contour_chip,
            swarm_chip,
            search_chip,
            hub_panel,
            hub_circle,
            ai_ring,
            hub_nodes,
            hub_edges,
            hub_title,
            hub_desc_1,
            hub_desc_2,
            hub_desc_3,
            hub_desc_4,
            arrow_left_to_hub,
            left_to_hub_label,
            right_panel,
            right_title,
            head,
            helmet,
            helmet_band,
            lamp,
            visor,
            mask,
            filter_box,
            eye_l,
            eye_r,
            brow_l,
            brow_r,
            hud_center,
            hud_cross,
            hud_path,
            hud_waypoints,
            info_box_1,
            info_title_1,
            info_line_1,
            info_box_2,
            info_title_2,
            info_line_2,
            info_box_3,
            info_title_3,
            info_line_3a,
            info_line_3b,
            info_line_3c,
            arrow_hub_to_right,
            hub_to_right_label,
            benefits,
            footer,
        )
