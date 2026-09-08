"""Editable first-pass themes; helpers return ordinary Manim Text objects."""

from dataclasses import dataclass, replace

from manim import ManimColor, Scene, Text

FONT_SANS_JP = "Noto Sans JP"
FONT_SERIF_JP = "Noto Serif JP"


@dataclass(frozen=True, slots=True)
class TextStyle:
    """Pango settings. None inherits the theme's font or the role's color.

    ``line_spacing`` is Manim's extra spacing, not a CSS line-height ratio:
    0.4 means a baseline distance of 1.4 times the font size.
    """

    font: str | None = None
    serif: bool = False
    font_size: float = 36
    weight: str = "NORMAL"
    line_spacing: float = 0.4
    color: ManimColor | str | None = None


@dataclass(frozen=True, slots=True)
class Typography:
    """The five text roles; override individual roles with dataclasses.replace."""

    title: TextStyle = TextStyle(font_size=52, weight="BOLD")
    subtitle: TextStyle = TextStyle(font_size=30)
    body: TextStyle = TextStyle(font_size=34)
    caption: TextStyle = TextStyle(font_size=24)
    keyword: TextStyle = TextStyle(font_size=38, weight="BOLD")


@dataclass(frozen=True, slots=True)
class Layout:
    """Opt-in spacing in Manim scene units (used by the template/showcases)."""

    edge_buff: float = 0.6
    row_buff: float = 0.24
    section_buff: float = 0.45


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
    typography: Typography = Typography()
    layout: Layout = Layout()
    surface: ManimColor = ManimColor("#152238")
    success: ManimColor = ManimColor("#6ED6AC")
    warning: ManimColor = ManimColor("#F5BF69")
    danger: ManimColor = ManimColor("#FF929B")
    # Brighter emphasis for shape fills and decorative rules, not text.
    accent_fill: ManimColor = ManimColor("#38BDF8")


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
    surface=ManimColor("#F1F5F9"),
    success=ManimColor("#247653"),
    warning=ManimColor("#A34B12"),
    danger=ManimColor("#B43D4C"),
    accent_fill=ManimColor("#BAE6FD"),
)


# Design review starts here: palette, fonts, typography, then spacing.
# Keep the legacy palettes above stable for existing scenes.
RESEARCH_THEME = Theme(
    background=ManimColor("#FCFCF9"),
    foreground=ManimColor("#243247"),
    muted=ManimColor("#566477"),
    accent=ManimColor("#2463A6"),
    secondary=ManimColor("#A34B12"),
    surface=ManimColor("#F1F3F4"),
    success=ManimColor("#247653"),
    warning=ManimColor("#A34B12"),
    danger=ManimColor("#B43D4C"),
    accent_fill=ManimColor("#DCEAF5"),
    sans_font=FONT_SANS_JP,
    serif_font=FONT_SERIF_JP,
    typography=Typography(
        title=TextStyle(font_size=52, weight="BOLD", line_spacing=0.25),
        subtitle=TextStyle(font_size=30, line_spacing=0.35),
        body=TextStyle(font_size=34, line_spacing=0.4),
        caption=TextStyle(font_size=24, line_spacing=0.35),
        keyword=TextStyle(font_size=38, weight="BOLD", line_spacing=0.3),
    ),
    layout=Layout(edge_buff=0.6, row_buff=0.24, section_buff=0.45),
)

# Preserve the original research palette as an explicit dark variant.
# Typography, fonts and spacing follow Research unless overridden here.
RESEARCH_DARK_THEME = replace(
    RESEARCH_THEME,
    background=ManimColor("#101827"),
    foreground=ManimColor("#F1F5FA"),
    muted=ManimColor("#B2BED0"),
    accent=ManimColor("#64CEED"),
    secondary=ManimColor("#B5A6F4"),
    surface=ManimColor("#1A2940"),
    success=ManimColor("#6ED6AC"),
    warning=ManimColor("#F5BF69"),
    danger=ManimColor("#FF929B"),
    accent_fill=ManimColor("#23465B"),
)

EDUCATION_THEME = Theme(
    background=ManimColor("#FFF9EE"),
    foreground=ManimColor("#3D342E"),
    muted=ManimColor("#756253"),
    accent=ManimColor("#B64C24"),
    secondary=ManimColor("#246B75"),
    surface=ManimColor("#FFF0D8"),
    success=ManimColor("#36704E"),
    warning=ManimColor("#925E17"),
    danger=ManimColor("#B13F4C"),
    accent_fill=ManimColor("#F6BF61"),
    sans_font=FONT_SANS_JP,
    serif_font=FONT_SERIF_JP,
    typography=Typography(
        title=TextStyle(font_size=60, weight="BOLD", line_spacing=0.35),
        subtitle=TextStyle(font_size=34, line_spacing=0.45),
        body=TextStyle(font_size=40, weight="BOLD", line_spacing=0.55),
        caption=TextStyle(font_size=28, line_spacing=0.45),
        keyword=TextStyle(font_size=46, weight="BOLD", line_spacing=0.4),
    ),
    layout=Layout(edge_buff=0.7, row_buff=0.34, section_buff=0.6),
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
        font: str | None = None,
        color: ManimColor | str | None = None,
        **kwargs: object,
    ) -> Text:
        """Create Japanese-capable text with a deterministic workspace font."""

        if font is None:
            font = self.theme.serif_font if serif else self.theme.sans_font
        return Text(
            text,
            font=font,
            font_size=font_size,
            color=self.theme.foreground if color is None else color,
            **kwargs,
        )

    def _styled_text(self, text: str, role: str, **kwargs: object) -> Text:
        style = getattr(self.theme.typography, role)
        role_color = {
            "title": self.theme.foreground,
            "subtitle": self.theme.muted,
            "body": self.theme.foreground,
            "caption": self.theme.muted,
            "keyword": self.theme.accent,
        }[role]
        options = {
            "font": style.font,
            "serif": style.serif,
            "font_size": style.font_size,
            "weight": style.weight,
            "line_spacing": style.line_spacing,
            "color": role_color if style.color is None else style.color,
        }
        options.update(kwargs)
        if options["color"] is None:
            options["color"] = role_color
        return self.jp_text(text, **options)

    def title_text(self, text: str, **kwargs: object) -> Text:
        """Primary heading. Per-call Text settings override the theme style."""
        return self._styled_text(text, "title", **kwargs)

    def subtitle_text(self, text: str, **kwargs: object) -> Text:
        """Secondary heading in the muted palette color."""
        return self._styled_text(text, "subtitle", **kwargs)

    def body_text(self, text: str, **kwargs: object) -> Text:
        """Body copy; insert explicit newlines to control wrapping."""
        return self._styled_text(text, "body", **kwargs)

    def caption_text(self, text: str, **kwargs: object) -> Text:
        """Source, annotation, or supporting label."""
        return self._styled_text(text, "caption", **kwargs)

    def keyword_text(self, text: str, **kwargs: object) -> Text:
        """Key concept in the accent color and a heavier weight."""
        return self._styled_text(text, "keyword", **kwargs)


class ResearchScene(ThemedScene):
    """Paper-white palette and compact typography for research explanations."""

    theme = RESEARCH_THEME


class ResearchDarkScene(ResearchScene):
    """Original navy, cyan and violet research palette with the same text API."""

    theme = RESEARCH_DARK_THEME


class EducationScene(ThemedScene):
    """Warm, bright palette and spacious typography for school lessons."""

    theme = EDUCATION_THEME


class DarkScene(ThemedScene):
    """Base scene for talks, slides, and video."""

    theme = DARK_THEME


class LightScene(ThemedScene):
    """Base scene for papers, print, and white slides."""

    theme = LIGHT_THEME
