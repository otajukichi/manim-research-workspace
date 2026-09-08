"""Style resolution tests: no Pango, TeX, camera, or rendering required."""

from dataclasses import replace
from unittest.mock import Mock

import pytest
from manim import ManimColor

import manim_research.theme as theme_module
from manim_research import (
    DARK_THEME,
    EDUCATION_THEME,
    LIGHT_THEME,
    RESEARCH_DARK_THEME,
    RESEARCH_THEME,
    DarkScene,
    EducationScene,
    LightScene,
    ResearchDarkScene,
    ResearchScene,
    TextStyle,
    Theme,
)


@pytest.fixture
def text_constructor(monkeypatch):
    constructor = Mock()
    monkeypatch.setattr(theme_module, "Text", constructor)
    return constructor


@pytest.mark.parametrize("scene_type", [ResearchScene, ResearchDarkScene, EducationScene])
@pytest.mark.parametrize(
    ("role", "color_role"),
    [
        ("title", "foreground"),
        ("subtitle", "muted"),
        ("body", "foreground"),
        ("caption", "muted"),
        ("keyword", "accent"),
    ],
)
def test_helpers_use_their_theme_style(scene_type, role, color_role, text_constructor):
    scene = object.__new__(scene_type)
    style = getattr(scene.theme.typography, role)
    result = getattr(scene, f"{role}_text")("日本語 / English")
    assert result is text_constructor.return_value
    text_constructor.assert_called_once_with(
        "日本語 / English",
        font=scene.theme.sans_font,
        font_size=style.font_size,
        weight=style.weight,
        line_spacing=style.line_spacing,
        color=getattr(scene.theme, color_role),
    )


def test_theme_font_family_and_role_font_are_independently_editable(text_constructor):
    scene = object.__new__(EducationScene)
    scene.theme = replace(
        EDUCATION_THEME,
        sans_font="Alternative Sans",
        serif_font="Alternative Serif",
        typography=replace(
            EDUCATION_THEME.typography,
            caption=TextStyle(serif=True, font_size=29),
            title=TextStyle(font="Title Font", font_size=62, color="#123456"),
        ),
    )
    scene.body_text("本文")
    assert text_constructor.call_args.kwargs["font"] == "Alternative Sans"
    scene.caption_text("出典")
    assert text_constructor.call_args.kwargs["font"] == "Alternative Serif"
    assert text_constructor.call_args.kwargs["font_size"] == 29
    scene.title_text("見出し")
    assert text_constructor.call_args.kwargs["font"] == "Title Font"
    assert text_constructor.call_args.kwargs["color"] == "#123456"
    assert EDUCATION_THEME.sans_font == "Noto Sans JP"
    assert EDUCATION_THEME.typography.title.font is None


def test_per_call_settings_override_the_role_and_forward_manim_options(text_constructor):
    scene = object.__new__(ResearchScene)
    scene.body_text(
        "注目",
        font="Custom Font",
        font_size=43,
        weight="BOLD",
        line_spacing=0.7,
        color="#223344",
        t2c={"注目": "#ABCDEF"},
        disable_ligatures=True,
    )
    text_constructor.assert_called_once_with(
        "注目",
        font="Custom Font",
        font_size=43,
        weight="BOLD",
        line_spacing=0.7,
        color="#223344",
        t2c={"注目": "#ABCDEF"},
        disable_ligatures=True,
    )


@pytest.mark.parametrize("scene_type", [ResearchScene, ResearchDarkScene, EducationScene])
def test_caption_can_select_serif_at_call_site(scene_type, text_constructor):
    scene = object.__new__(scene_type)
    scene.caption_text("明朝体", serif=True)
    assert text_constructor.call_args.kwargs["font"] == scene.theme.serif_font


def test_none_color_uses_the_role_color(text_constructor):
    scene = object.__new__(EducationScene)
    scene.keyword_text("強調", color=None)
    assert text_constructor.call_args.kwargs["color"] == EDUCATION_THEME.accent


@pytest.mark.parametrize(
    ("scene_type", "theme"), [(DarkScene, DARK_THEME), (LightScene, LIGHT_THEME)]
)
def test_legacy_jp_text_defaults_and_explicit_font(scene_type, theme, text_constructor):
    scene = object.__new__(scene_type)
    scene.jp_text("既存コード")
    text_constructor.assert_called_once_with(
        "既存コード",
        font=theme.sans_font,
        font_size=48,
        color=theme.foreground,
    )
    scene.jp_text("明朝体", serif=True)
    assert text_constructor.call_args.kwargs["font"] == theme.serif_font
    # Regression: font= formerly collided with the helper's own keyword.
    scene.jp_text("個別指定", serif=True, font="Custom Font", font_size=31, weight="BOLD")
    assert text_constructor.call_args.kwargs["font"] == "Custom Font"
    assert text_constructor.call_args.kwargs["font_size"] == 31
    assert text_constructor.call_args.kwargs["weight"] == "BOLD"


def test_legacy_theme_constructor_remains_compatible():
    custom = Theme(
        DARK_THEME.background,
        DARK_THEME.foreground,
        DARK_THEME.muted,
        DARK_THEME.accent,
        DARK_THEME.secondary,
        "My Sans",
        "My Serif",
    )
    assert custom.sans_font == "My Sans"
    assert custom.serif_font == "My Serif"


def test_education_has_larger_type_and_more_space():
    assert ResearchScene.theme is RESEARCH_THEME
    assert EducationScene.theme is EDUCATION_THEME
    assert RESEARCH_THEME.background != EDUCATION_THEME.background
    assert RESEARCH_THEME.accent != EDUCATION_THEME.accent
    for role in ("title", "subtitle", "body", "caption", "keyword"):
        research = getattr(RESEARCH_THEME.typography, role)
        education = getattr(EDUCATION_THEME.typography, role)
        assert education.font_size > research.font_size
        assert education.line_spacing > research.line_spacing
    assert EDUCATION_THEME.typography.body.weight == "BOLD"
    assert RESEARCH_THEME.typography.body.weight == "NORMAL"
    assert EDUCATION_THEME.layout.edge_buff > RESEARCH_THEME.layout.edge_buff
    assert EDUCATION_THEME.layout.row_buff > RESEARCH_THEME.layout.row_buff
    assert EDUCATION_THEME.layout.section_buff > RESEARCH_THEME.layout.section_buff


def test_research_dark_preserves_the_original_palette_and_research_typography():
    assert ResearchDarkScene.theme is RESEARCH_DARK_THEME
    assert RESEARCH_DARK_THEME.background == ManimColor("#101827")
    assert RESEARCH_DARK_THEME.foreground == ManimColor("#F1F5FA")
    assert RESEARCH_DARK_THEME.accent == ManimColor("#64CEED")
    assert RESEARCH_DARK_THEME.secondary == ManimColor("#B5A6F4")
    assert RESEARCH_DARK_THEME.typography == RESEARCH_THEME.typography
    assert RESEARCH_DARK_THEME.layout == RESEARCH_THEME.layout
    assert RESEARCH_DARK_THEME.background != RESEARCH_THEME.background
    assert RESEARCH_DARK_THEME != DARK_THEME


def _luminance(color: ManimColor) -> float:
    linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in color.to_rgb()]
    return sum(v * weight for v, weight in zip(linear, (0.2126, 0.7152, 0.0722), strict=True))


@pytest.mark.parametrize("theme", [RESEARCH_THEME, RESEARCH_DARK_THEME, EDUCATION_THEME])
@pytest.mark.parametrize("background", ["background", "surface"])
def test_text_palette_contrast(theme, background):
    for role in ("foreground", "muted", "accent", "secondary", "success", "warning", "danger"):
        dark, light = sorted(
            (_luminance(getattr(theme, role)), _luminance(getattr(theme, background)))
        )
        ratio = (light + 0.05) / (dark + 0.05)
        assert ratio >= 4.5, (role, background, ratio)
