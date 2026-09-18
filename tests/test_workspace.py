import subprocess
from pathlib import Path

from manim_research import DARK_THEME, FONT_SANS_JP, FONT_SERIF_JP, LIGHT_THEME
from projects.showcase.showcase import (
    PaperFigure,
    RenderSmoke,
    TransparentFigure,
    WorkspaceShowcase,
)


def test_git_tracks_projects_and_artifacts_but_ignores_caches(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(Path(".gitignore").read_text(encoding="utf-8"))
    subprocess.run(["git", "init", "--quiet", str(tmp_path)], check=True)
    included = [
        "projects/new_project/scene.py",
        "projects/new_project/assets/image.png",
        "projects/new_project/assets/Tex/formula.tex",
        "projects/new_project/assets/texts/label.svg",
        "projects/new_project/main.tex",
        "projects/new_project/figures/report.pdf",
        "projects/lessons/unit/data.json",
    ]
    ignored = [
        ".pixi/envs/default/bin/python",
        ".tools/texlive/bin/latex",
        ".local/share/fonts/font.otf",
        ".cache/tool/data",
        ".pytest_cache/v/cache/nodeids",
        ".ruff_cache/data",
        "projects/new_project/__pycache__/scene.cpython-312.pyc",
        "projects/new_project/missfont.log",
    ]
    for output in (
        "media",
        "output",
        "projects/showcase/output",
        "projects/new_project/output",
        "projects/lessons/unit/output",
    ):
        included.extend(
            f"{output}/{path}"
            for path in (
                "images/figure.png",
                "videos/scene/1080p30/Scene.mp4",
                "videos/scene/480p15/Scene.mp4",
            )
        )
        ignored.extend(
            f"{output}/{path}"
            for path in (
                "Tex/formula.svg",
                "texts/label.svg",
                "videos/scene/1080p30/partial_movie_files/Scene/clip.mp4",
                "videos/scene/1080p30/partial_movie_files/Scene/partial_movie_file_list.txt",
            )
        )
    result = subprocess.run(
        ["git", "-c", "core.excludesFile=/dev/null", "check-ignore", "--no-index", "--stdin"],
        cwd=tmp_path,
        input="\n".join(included + ignored) + "\n",
        text=True,
        capture_output=True,
        check=True,
    )
    assert set(result.stdout.splitlines()) == set(ignored)


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
