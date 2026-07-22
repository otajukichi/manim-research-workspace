"""Copy this directory and rename both the directory and this file."""

from manim import Circle, Create

from bd_adv_manim import DarkScene


class FirstScene(DarkScene):
    def construct(self) -> None:
        circle = Circle(color=self.theme.accent)
        self.play(Create(circle))
