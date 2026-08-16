from pathlib import Path

from bd_adv_manim import DARK_THEME, FONT_SANS_JP, FONT_SERIF_JP, LIGHT_THEME
from projects.showcase.showcase import (
    PaperFigure,
    RenderSmoke,
    TransparentFigure,
    WorkspaceShowcase,
)


def test_project_outputs_are_ignored() -> None:
    gitignore = Path(".gitignore").read_text(encoding="utf-8")
    assert "projects/**/output/" in gitignore


def test_manim_wrapper_routes_output_next_to_input() -> None:
    wrapper = Path("scripts/manim.sh").read_text(encoding="utf-8")
    assert "project_dir/output" in wrapper
    assert "--media_dir" in wrapper
    assert "media_dir_set" in wrapper


def test_themes_have_distinct_backgrounds() -> None:
    assert DARK_THEME.background != LIGHT_THEME.background
    assert DARK_THEME.foreground != DARK_THEME.background
    assert LIGHT_THEME.foreground != LIGHT_THEME.background


def test_japanese_fonts_are_explicit() -> None:
    assert FONT_SANS_JP == "Noto Sans JP"
    assert FONT_SERIF_JP == "Noto Serif JP"


def test_showcase_scenes_are_importable() -> None:
    assert all(
        scene.__name__ for scene in (WorkspaceShowcase, PaperFigure, TransparentFigure, RenderSmoke)
    )
