"""Three review screens per theme; the first two use identical content."""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Axes,
    Circle,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    Rectangle,
    RoundedRectangle,
    VGroup,
)

from manim_research import RESEARCH_DARK_THEME, EducationScene, ResearchScene

# Review-only composition/timing. Theme colors, fonts and gaps live in theme.py.
PAGE_HOLD_SECONDS = 5
GRAPH_WIDTH = 4.8
GRAPH_HEIGHT = 3.0
DIAGRAM_NODE_RADIUS = 0.23
FRACTION_CELL_WIDTH = 1.35


class _ThemeShowcase:
    """Local composition helpers, not a slide framework or public component API."""

    theme_label: str

    def construct(self) -> None:
        pages = (self.typography_page(), self.visuals_page(), self.example_page())
        for index, page in enumerate(pages):
            self.play(FadeIn(page), run_time=0.4)
            self.wait(PAGE_HOLD_SECONDS)
            if index < len(pages) - 1:
                self.play(FadeOut(page), run_time=0.3)

    def header(self, title: str, subtitle: str) -> VGroup:
        layout = self.theme.layout
        heading = self.title_text(title).to_corner(UP + LEFT, buff=layout.edge_buff)
        subheading = self.subtitle_text(subtitle).next_to(
            heading, DOWN, aligned_edge=LEFT, buff=layout.row_buff
        )
        return VGroup(heading, subheading)

    def footer(self, label: str, page: int) -> VGroup:
        margin = self.theme.layout.edge_buff
        caption = self.caption_text(label).to_corner(DOWN + LEFT, buff=margin)
        identifier = self.caption_text(f"{self.theme_label}  /  0{page}").to_corner(
            DOWN + RIGHT, buff=margin
        )
        return VGroup(caption, identifier)

    def typography_page(self) -> VGroup:
        layout = self.theme.layout
        header = self.header("伝わる説明をつくる", "日本語と English / 見出し・本文・強調")
        body = self.body_text(
            "同じ内容を、見やすく伝える。\n図と言葉で、関係をたしかめよう。"
        ).next_to(header, DOWN, aligned_edge=LEFT, buff=layout.section_buff)

        bullets = VGroup()
        for number, text in (("01", "変化を見つける"), ("02", "理由を言葉にする")):
            marker = self.caption_text(number, color=self.theme.accent, weight="BOLD")
            line = VGroup(marker, self.body_text(text)).arrange(RIGHT, buff=layout.row_buff)
            bullets.add(line)
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=layout.row_buff).next_to(
            body, DOWN, aligned_edge=LEFT, buff=layout.section_buff
        )

        keyword = self.keyword_text("関係に注目")
        serif = self.caption_text("日本語の明朝体も比較", serif=True)
        emphasis = VGroup(keyword, serif).arrange(DOWN, aligned_edge=LEFT, buff=layout.row_buff)
        emphasis.align_to(bullets, UP).shift(RIGHT * (0.8 - emphasis.get_left()[0]))
        rule = Line(
            emphasis.get_left() + LEFT * 0.22 + UP * emphasis.height / 2,
            emphasis.get_left() + LEFT * 0.22 + DOWN * emphasis.height / 2,
            color=self.theme.accent_fill,
            stroke_width=4,
        )
        return VGroup(
            header, body, bullets, emphasis, rule, self.footer("文字見本 / Typography", 1)
        )

    def visuals_page(self) -> VGroup:
        header = self.header("式・図・グラフをつなぐ", "入力から出力へ / Input → Output")
        formula = MathTex(
            r"y=2x+1",
            font_size=self.theme.typography.keyword.font_size,
            color=self.theme.accent,
        ).move_to([-3.5, 1.15, 0])
        axes = Axes(
            x_range=[0, 3, 1],
            y_range=[0, 7, 1],
            x_length=GRAPH_WIDTH,
            y_length=GRAPH_HEIGHT,
            tips=False,
            axis_config={
                "color": self.theme.muted,
                "include_numbers": True,
                "font_size": self.theme.typography.caption.font_size,
            },
            y_axis_config={"numbers_to_include": [1, 3, 5, 7]},
        ).move_to([-3.65, -0.85, 0])
        # NumberLine's numeric labels do not inherit axis_config['color'].
        axes.x_axis.numbers.set_color(self.theme.muted)
        axes.y_axis.numbers.set_color(self.theme.muted)
        graph = axes.plot(lambda x: 2 * x + 1, x_range=[0, 3], color=self.theme.accent)
        point = Dot(axes.c2p(1, 3), color=self.theme.secondary, radius=0.09)
        annotation = self.caption_text("(1, 3)", color=self.theme.secondary).move_to(
            axes.c2p(1.9, 2)
        )
        pointer = Arrow(
            annotation.get_left(),
            point.get_center(),
            buff=0.12,
            color=self.theme.secondary,
            stroke_width=3,
        )
        axis_x = MathTex(
            "x", color=self.theme.muted, font_size=self.theme.typography.caption.font_size
        ).next_to(axes.x_axis, RIGHT)
        axis_y = MathTex(
            "y", color=self.theme.muted, font_size=self.theme.typography.caption.font_size
        ).next_to(axes.y_axis, UP)

        boxes = VGroup()
        for x, tex in ((0.8, "x"), (3.0, "2x+1"), (5.2, "y")):
            box = RoundedRectangle(
                width=1.55,
                height=0.95,
                corner_radius=0.12,
                color=self.theme.accent,
                fill_color=self.theme.accent_fill if tex == "2x+1" else self.theme.surface,
                fill_opacity=1,
            ).move_to([x, 0.6, 0])
            label = MathTex(
                tex, color=self.theme.foreground, font_size=self.theme.typography.body.font_size
            ).move_to(box)
            boxes.add(VGroup(box, label))
        arrows = VGroup(
            *(
                Arrow(left.get_right(), right.get_left(), buff=0.08, color=self.theme.muted)
                for left, right in zip(boxes, boxes[1:], strict=False)
            )
        )
        diagram_label = self.body_text("同じルールで変わる").move_to([3.0, -0.55, 0])
        explanation = self.caption_text("x が 1 増えると、y は 2 増える").next_to(
            diagram_label, DOWN, buff=self.theme.layout.row_buff
        )
        legend = (
            VGroup(
                self.caption_text("線：関係", color=self.theme.accent),
                self.caption_text("点：注目する値", color=self.theme.secondary),
            )
            .arrange(RIGHT, buff=0.5)
            .move_to([3.0, -2.15, 0])
        )
        return VGroup(
            header,
            formula,
            axes,
            graph,
            point,
            annotation,
            pointer,
            axis_x,
            axis_y,
            boxes,
            arrows,
            diagram_label,
            explanation,
            legend,
            self.footer("共通サンプル / y = 2x + 1", 2),
        )


class ResearchThemeShowcase(_ThemeShowcase, ResearchScene):
    """Shared typography/visuals followed by a neural-network example."""

    theme_label = "Research Theme"

    def example_page(self) -> VGroup:
        header = self.header(
            "ニューラルネットワーク", "線形変換と非線形変換 / A small feed-forward network"
        )
        layers = VGroup()
        for x, count, color in (
            (-5.25, 3, self.theme.accent),
            (-3.35, 4, self.theme.secondary),
            (-1.45, 2, self.theme.accent),
        ):
            layer = (
                VGroup(
                    *(
                        Circle(
                            radius=DIAGRAM_NODE_RADIUS,
                            color=color,
                            fill_color=self.theme.surface,
                            fill_opacity=1,
                            stroke_width=3,
                        )
                        for _ in range(count)
                    )
                )
                .arrange(DOWN, buff=self.theme.layout.row_buff)
                .move_to([x, -0.25, 0])
            )
            layers.add(layer)
        edges = VGroup(
            *(
                Line(a.get_right(), b.get_left(), color=self.theme.muted, stroke_width=1.6)
                for left, right in zip(layers, layers[1:], strict=False)
                for a in left
                for b in right
            )
        )
        labels = VGroup(
            *(
                self.caption_text(text).move_to([x, -2.15, 0])
                for x, text in ((-5.25, "入力 x"), (-3.35, "隠れ層 h"), (-1.45, "出力 y"))
            )
        )

        heading = self.keyword_text("線形変換 + 活性化")
        equation = MathTex(
            r"\mathbf{h}=\sigma(W\mathbf{x}+\mathbf{b})",
            font_size=self.theme.typography.keyword.font_size + 4,
            color=self.theme.foreground,
        )
        details = self.body_text("重み W で特徴を混ぜる\n活性化関数で表現を広げる")
        note = self.caption_text("模式図：3 → 4 → 2 次元", color=self.theme.muted)
        text = (
            VGroup(heading, equation, details, note)
            .arrange(DOWN, aligned_edge=LEFT, buff=self.theme.layout.section_buff)
            .move_to([3.05, -0.5, 0])
        )
        return VGroup(
            header,
            edges,
            layers,
            labels,
            text,
            self.footer("技術解説 / 構造・数式・注記を同時に読む", 3),
        )


class ResearchDarkThemeShowcase(ResearchThemeShowcase):
    """The same research screens in the original dark palette."""

    theme = RESEARCH_DARK_THEME
    theme_label = "Research Dark"


class EducationThemeShowcase(_ThemeShowcase, EducationScene):
    """Shared typography/visuals followed by an elementary fraction lesson."""

    theme_label = "Education Theme"

    def example_page(self) -> VGroup:
        layout = self.theme.layout
        header = self.header("分数ってなに？", "同じ大きさに分けて考えよう")
        prompt = self.body_text("1つのものを、3つに等しく分ける。").next_to(
            header, DOWN, aligned_edge=LEFT, buff=layout.section_buff
        )
        cells = (
            VGroup(
                *(
                    Rectangle(
                        width=FRACTION_CELL_WIDTH,
                        height=1.35,
                        color=self.theme.foreground,
                        stroke_width=3,
                        fill_color=self.theme.accent_fill if index == 0 else self.theme.surface,
                        fill_opacity=1,
                    )
                    for index in range(3)
                )
            )
            .arrange(RIGHT, buff=0)
            .move_to([-3.3, -0.4, 0])
        )
        selected = self.caption_text("この1つ分", color=self.theme.accent, weight="BOLD").next_to(
            cells[0], DOWN, buff=0.65
        )
        pointer = Arrow(
            selected.get_top(),
            cells[0].get_bottom(),
            buff=0.1,
            color=self.theme.accent,
            stroke_width=4,
        )
        fraction = MathTex(
            r"\frac{1}{3}",
            font_size=self.theme.typography.keyword.font_size * 1.7,
            color=self.theme.accent,
        )
        keyword = self.keyword_text("3分の1")
        answer = (
            VGroup(fraction, keyword)
            .arrange(RIGHT, buff=layout.section_buff)
            .move_to([3.0, -0.4, 0])
        )
        reminder = self.body_text("ポイント：同じ大きさ", color=self.theme.warning).next_to(
            answer, DOWN, buff=layout.section_buff
        )
        # The meaning is also conveyed by area, an arrow, words and the fraction.
        return VGroup(
            header,
            prompt,
            cells,
            selected,
            pointer,
            answer,
            reminder,
            self.footer("算数 / 分けた数と、選んだ数", 3),
        )
