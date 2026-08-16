"""Short examples covering the workspace's supported Manim features."""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Axes,
    Circle,
    Create,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    Matrix,
    ReplacementTransform,
    Square,
    SurroundingRectangle,
    Tex,
    Transform,
    VGroup,
    Write,
)

from manim_research import JAPANESE_TEX_TEMPLATE, DarkScene, LightScene


class WorkspaceShowcase(DarkScene):
    """A compact tour of shapes, Japanese, TeX, matrices, and plots."""

    def construct(self) -> None:
        title = self.jp_text("ManimCE 制作ワークスペース", font_size=54)
        subtitle = self.jp_text(
            "研究・論文・授業発表のための再現可能な図",
            font_size=28,
            color=self.theme.muted,
        ).next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle, shift=UP * 0.15))
        self.wait(0.5)
        self.play(FadeOut(VGroup(title, subtitle)))

        circle = Circle(color=self.theme.accent, fill_opacity=0.2)
        square = Square(color=self.theme.secondary, fill_opacity=0.2)
        shape_label = self.jp_text("基本図形を正確に変形", font_size=34).to_edge(UP)
        self.play(Write(shape_label), Create(circle))
        self.play(Transform(circle, square))
        self.play(FadeOut(VGroup(shape_label, circle)))

        japanese_tex = Tex(
            r"日本語と \LaTeX を同じシーンで扱えます",
            tex_template=JAPANESE_TEX_TEMPLATE,
            font_size=42,
            color=self.theme.foreground,
        ).to_edge(UP)
        formula = MathTex(
            r"\boldsymbol{y}=\boldsymbol{A}\boldsymbol{x}",
            color=self.theme.accent,
        ).next_to(japanese_tex, DOWN, buff=0.6)
        self.play(Write(japanese_tex), Write(formula))
        self.wait(0.5)
        self.play(FadeOut(VGroup(japanese_tex, formula)))

        matrix_a = Matrix([[1, 2], [3, 4]]).scale(0.75)
        matrix_b = Matrix([[2, 0], [1, 2]]).scale(0.75)
        matrix_c = Matrix([[4, 4], [10, 8]]).scale(0.75)
        for matrix in (matrix_a, matrix_b, matrix_c):
            matrix.set_color(self.theme.foreground)
        times = MathTex(r"\times", color=self.theme.muted)
        equals = MathTex("=", color=self.theme.muted)
        equation = VGroup(matrix_a, times, matrix_b, equals, matrix_c).arrange(RIGHT, buff=0.3)
        matrix_label = self.jp_text("行と列の対応を強調", font_size=32).next_to(
            equation, UP, buff=0.5
        )
        row_box = SurroundingRectangle(matrix_a.get_rows()[0], color=self.theme.accent, buff=0.08)
        column_box = SurroundingRectangle(
            matrix_b.get_columns()[0], color=self.theme.secondary, buff=0.08
        )
        result_box = SurroundingRectangle(
            matrix_c.get_entries()[0], color=self.theme.accent, buff=0.08
        )
        self.play(FadeIn(equation), Write(matrix_label))
        self.play(Create(row_box), Create(column_box))
        self.play(ReplacementTransform(row_box, result_box), FadeOut(column_box))
        self.wait(0.5)
        self.play(FadeOut(VGroup(equation, matrix_label, result_box)))

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 2],
            x_length=7,
            y_length=4,
            tips=False,
            axis_config={"color": self.theme.muted},
        )
        curve = axes.plot(lambda x: x**2, x_range=[-2.8, 2.8], color=self.theme.accent)
        graph_label = MathTex(r"y=x^2", color=self.theme.accent).next_to(axes, UP)
        self.play(Create(axes), Create(curve), Write(graph_label))
        self.wait(0.75)


class PaperFigure(LightScene):
    """A high-resolution white-background figure for papers and handouts."""

    def construct(self) -> None:
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 2],
            x_length=8,
            y_length=4.8,
            tips=False,
            axis_config={
                "color": self.theme.foreground,
                "include_numbers": True,
                "font_size": 24,
            },
        )
        curve = axes.plot(lambda x: x**2, x_range=[-2.8, 2.8], color=self.theme.accent)
        formula = MathTex(r"f(x)=x^2", color=self.theme.accent).next_to(axes, UP, buff=0.3)
        caption = self.jp_text(
            "図1：二次関数の例",
            font_size=30,
            serif=True,
            color=self.theme.foreground,
        ).next_to(axes, DOWN, buff=0.35)
        self.add(axes, curve, formula, caption)


class TransparentFigure(DarkScene):
    """A background-free diagram intended for compositing in slides."""

    def construct(self) -> None:
        left = Circle(radius=1.25, color=self.theme.accent, fill_opacity=0.12).shift(LEFT * 2.2)
        right = Square(side_length=2.4, color=self.theme.secondary, fill_opacity=0.12).shift(
            RIGHT * 2.2
        )
        arrow = Line(
            left.get_right(),
            right.get_left(),
            color=self.theme.accent,
            stroke_width=8,
        ).add_tip()
        label = MathTex(r"\mathcal{T}", color=self.theme.secondary).next_to(arrow, UP)
        self.add(left, right, arrow, label)


class RenderSmoke(DarkScene):
    """One-frame scene used by the local environment check."""

    def construct(self) -> None:
        text = self.jp_text("日本語 OK", font_size=34)
        formula = MathTex(r"A\boldsymbol{x}=\boldsymbol{b}", color=self.theme.accent)
        matrix = Matrix([[1, 2], [3, 4]]).scale(0.65).set_color(self.theme.foreground)
        group = VGroup(text, formula, matrix).arrange(RIGHT, buff=0.75)
        self.add(group)
