"""TeX templates used across scenes."""

from manim import TexTemplate


def _build_japanese_template() -> TexTemplate:
    template = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
    template.preamble = r"""
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{zxjatype}
\setCJKmainfont{Noto Serif JP}
\setCJKsansfont{Noto Sans JP}
""".strip()
    return template


JAPANESE_TEX_TEMPLATE = _build_japanese_template()
