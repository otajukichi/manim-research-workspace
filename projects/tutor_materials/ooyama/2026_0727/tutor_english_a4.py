"""Shared A4 layout helpers for the tutoring-material scenes."""

from __future__ import annotations

from manim import WHITE, Rectangle, Text, VGroup, config

config.frame_width = 14.14
config.frame_height = 10.0
config.pixel_width = 3508
config.pixel_height = 2480
config.frame_rate = 1

NAVY = "#062F67"
NAVY_DARK = "#032654"
INK = "#111827"
GRID = "#8B98AA"
PALE_GRAY = "#F7F9FC"
FONT = "Noto Sans JP"


def label(
    value: str,
    size: float,
    *,
    color: str = INK,
    weight: str = "NORMAL",
) -> Text:
    """Create consistently styled Japanese-capable text."""
    return Text(value, font=FONT, font_size=size, color=color, weight=weight)


def table(
    headers: list[str],
    rows: list[list[str]],
    widths: list[float],
    row_height: float,
    header_height: float,
    font_size: float,
) -> VGroup:
    """Create a simple navy-header table."""
    group = VGroup()
    total_width = sum(widths)
    total_height = header_height + row_height * len(rows)
    left = -total_width / 2
    top = total_height / 2

    x = left
    for heading, width in zip(headers, widths, strict=True):
        cell = Rectangle(
            width=width,
            height=header_height,
            stroke_color=WHITE,
            stroke_width=1.4,
            fill_color=NAVY,
            fill_opacity=1,
        ).move_to([x + width / 2, top - header_height / 2, 0])
        text = label(heading, font_size + 1, color=WHITE, weight="BOLD")
        text.move_to(cell)
        group.add(cell, text)
        x += width

    for row_index, values in enumerate(rows):
        y = top - header_height - row_height * (row_index + 0.5)
        x = left
        for value, width in zip(values, widths, strict=True):
            cell = Rectangle(
                width=width,
                height=row_height,
                stroke_color=GRID,
                stroke_width=0.8,
                fill_color=PALE_GRAY if row_index % 2 else WHITE,
                fill_opacity=1,
            ).move_to([x + width / 2, y, 0])
            text = label(value, font_size)
            if text.width > width - 0.14:
                text.scale_to_fit_width(width - 0.14)
            if text.height > row_height - 0.1:
                text.scale_to_fit_height(row_height - 0.1)
            text.move_to(cell)
            group.add(cell, text)
            x += width

    return group
