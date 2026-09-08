"""Copy this directory and rename both the directory and this file."""

from manim import DOWN, LEFT, UP, Circle, Create

from manim_research import EducationScene, ResearchScene


class FirstScene(ResearchScene):
    def construct(self) -> None:
        layout = self.theme.layout
        title = self.title_text("研究発表のタイトル").to_corner(UP + LEFT, buff=layout.edge_buff)
        body = self.body_text("図と言葉で、関係を伝える。").next_to(
            title, DOWN, aligned_edge=LEFT, buff=layout.section_buff
        )
        circle = Circle(color=self.theme.accent).shift(DOWN)
        self.add(title, body)
        self.play(Create(circle))


class FractionLesson(EducationScene):
    def construct(self) -> None:
        layout = self.theme.layout
        title = self.title_text("分数ってなに？").to_corner(UP + LEFT, buff=layout.edge_buff)
        body = self.body_text("1つのものを、同じ大きさに分ける。").next_to(
            title, DOWN, aligned_edge=LEFT, buff=layout.section_buff
        )
        keyword = self.keyword_text("3分の1").next_to(
            body, DOWN, aligned_edge=LEFT, buff=layout.section_buff
        )
        self.add(title, body, keyword)
