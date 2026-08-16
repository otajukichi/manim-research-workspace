"""Reproducible dark and light themes for Manim scenes."""

from dataclasses import dataclass

from manim import ManimColor, Scene, Text

FONT_SANS_JP = "Noto Sans JP"
FONT_SERIF_JP = "Noto Serif JP"


@dataclass(frozen=True, slots=True)
class Theme:
    """Colors and fonts shared by a family of scenes."""

    background: ManimColor
    foreground: ManimColor
    muted: ManimColor
    accent: ManimColor
    secondary: ManimColor
    sans_font: str = FONT_SANS_JP
    serif_font: str = FONT_SERIF_JP


DARK_THEME = Theme(
    background=ManimColor("#0B1020"),
    foreground=ManimColor("#F8FAFC"),
    muted=ManimColor("#A7B0C0"),
    accent=ManimColor("#38BDF8"),
    secondary=ManimColor("#F472B6"),
)

LIGHT_THEME = Theme(
    background=ManimColor("#FFFFFF"),
    foreground=ManimColor("#172033"),
    muted=ManimColor("#5B6472"),
    accent=ManimColor("#0369A1"),
    secondary=ManimColor("#BE185D"),
)


class ThemedScene(Scene):
    """Base scene that applies a palette and provides Japanese text helpers."""

    theme = DARK_THEME

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = self.theme.background

    def jp_text(
        self,
        text: str,
        *,
        font_size: float = 48,
        serif: bool = False,
        color: ManimColor | None = None,
        **kwargs: object,
    ) -> Text:
        """Create Japanese-capable text with a deterministic workspace font."""

        font = self.theme.serif_font if serif else self.theme.sans_font
        return Text(
            text,
            font=font,
            font_size=font_size,
            color=color or self.theme.foreground,
            **kwargs,
        )


class DarkScene(ThemedScene):
    """Base scene for talks, slides, and video."""

    theme = DARK_THEME


class LightScene(ThemedScene):
    """Base scene for papers, print, and white slides."""

    theme = LIGHT_THEME
