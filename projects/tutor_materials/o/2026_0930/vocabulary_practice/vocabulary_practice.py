from __future__ import annotations

import json
import os
from dataclasses import replace
from pathlib import Path

from manim import Line, ManimColor, Text, VGroup, config

from manim_research import EDUCATION_THEME, EducationScene


# ============================================================
# Fixed worksheet settings
# ============================================================

_ROWS_PER_COLUMN = 15
_COLUMN_COUNT = 2
_ENTRIES_PER_PAGE = _ROWS_PER_COLUMN * _COLUMN_COUNT

A4_WIDTH_MM = 210
A4_HEIGHT_MM = 297
A4_PIXEL_WIDTH = 2480
A4_PIXEL_HEIGHT = 3508

FRAME_HEIGHT = 14.0
FRAME_WIDTH = FRAME_HEIGHT * A4_WIDTH_MM / A4_HEIGHT_MM

# A4 portrait, 300 dpi.
config.pixel_width = A4_PIXEL_WIDTH
config.pixel_height = A4_PIXEL_HEIGHT
config.frame_width = FRAME_WIDTH
config.frame_height = FRAME_HEIGHT


PRINT_THEME = replace(
    EDUCATION_THEME,
    background=ManimColor("#FFFFFF"),
    foreground=ManimColor("#26221F"),
    muted=ManimColor("#8D857F"),
    accent=ManimColor("#A84624"),
    surface=ManimColor("#FFFFFF"),
)


def _content_file() -> Path:
    raw = os.environ.get("MANIM_CONTENT_FILE")

    if not raw:
        raise RuntimeError(
            "MANIM_CONTENT_FILE is not set. "
            "Run with: pixi run manim -- --content-file ..."
        )

    path = Path(raw).expanduser()

    if not path.is_absolute():
        path = Path.cwd() / path

    return path.resolve()


def load_content() -> tuple[dict[str, object], list[dict[str, object]]]:
    path = _content_file()

    if not path.exists():
        raise FileNotFoundError(f"Content JSON not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data.get("entries")

    if not isinstance(entries, list):
        raise ValueError("JSON field 'entries' must be a list")

    if len(entries) != _ENTRIES_PER_PAGE:
        raise ValueError(
            f"Expected {_ENTRIES_PER_PAGE} entries, found {len(entries)}"
        )

    required = {"no", "english", "pronunciation", "meaning"}

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValueError(f"entries[{index}] must be an object")

        missing = required - set(entry)

        if missing:
            raise ValueError(
                f"entries[{index}] is missing fields: {sorted(missing)}"
            )

    return data, entries


def _layout_spec() -> dict[str, float | str]:
    return {
        "margin_x": 0.28,
        "margin_y": 0.24,
        "column_gap": 0.20,
        "number_gutter": 0.42,
        "number_font_size": 12,
        "prompt_font_size": 14,
        "prompt_weight": "NORMAL",
        "answer_ratio": 0.54,
        "answer_gap": 0.10,
        "header_title_font_size": 20,
        "header_subtitle_font_size": 15,
        "header_height": 1.08,
        "header_line_gap": 0.08,
    }


def _preferred_break_positions(text: str) -> list[int]:
    positions: list[int] = []
    boundary_chars = " )）]］】、。・／/~～-"

    for index in range(1, len(text)):
        if text[index - 1].isspace() or text[index].isspace():
            positions.append(index)
        elif text[index - 1] in boundary_chars or text[index] in boundary_chars:
            positions.append(index)

    return positions


def _make_prompt(
    text: str,
    *,
    max_width: float,
    max_height: float,
    font_size: float,
    weight: str,
    color: ManimColor,
    font: str,
) -> Text:
    def make(content: str) -> Text:
        return Text(
            content,
            font=font,
            font_size=font_size,
            weight=weight,
            line_spacing=0.60,
            color=color,
        )

    single = make(text)

    if single.width <= max_width and single.height <= max_height:
        return single

    midpoint = len(text) / 2
    preferred = _preferred_break_positions(text)
    candidates = preferred or list(range(1, len(text)))
    candidates = sorted(candidates, key=lambda index: abs(index - midpoint))

    best: Text | None = None
    best_score: float | None = None

    for index in candidates:
        left = text[:index].strip()
        right = text[index:].strip()

        if not left or not right:
            continue

        wrapped = make(f"{left}\n{right}")

        if wrapped.width <= max_width and wrapped.height <= max_height:
            return wrapped

        width_scale = max_width / wrapped.width if wrapped.width > 0 else 1.0
        height_scale = max_height / wrapped.height if wrapped.height > 0 else 1.0
        required_scale = min(1.0, width_scale, height_scale)

        if best_score is None or required_scale > best_score:
            best = wrapped
            best_score = required_scale

    if best is None:
        best = single

    if best.width > max_width:
        best.scale_to_fit_width(max_width)

    if best.height > max_height:
        best.scale_to_fit_height(max_height)

    return best


class VocabularyPractice(EducationScene):
    theme = PRINT_THEME

    def construct(self) -> None:
        data, entries = load_content()
        spec = _layout_spec()

        margin_x = float(spec["margin_x"])
        margin_y = float(spec["margin_y"])
        column_gap = float(spec["column_gap"])
        header_height = float(spec["header_height"])
        header_title_font_size = float(
            spec["header_title_font_size"]
        )
        header_subtitle_font_size = float(
            spec["header_subtitle_font_size"]
        )
        header_line_gap = float(spec["header_line_gap"])

        title = str(
            data.get(
                "title",
                "中学英語 基本単語",
            )
        )

        header_range = str(
            data.get(
                "header_range",
                "",
            )
        ).strip()

        subtitle = str(
            data.get(
                "subtitle",
                "",
            )
        ).strip()

        header_text = (
            f"{title} {header_range}"
        ).strip()

        top_outer = config.frame_height / 2 - margin_y
        row_area_top = top_outer - header_height
        bottom_outer = -config.frame_height / 2 + margin_y

        content_width = config.frame_width - 2 * margin_x
        content_height = row_area_top - bottom_outer

        column_width = (
            content_width - column_gap * (_COLUMN_COUNT - 1)
        ) / _COLUMN_COUNT

        row_height = content_height / _ROWS_PER_COLUMN
        left_edge = -config.frame_width / 2 + margin_x

        page = VGroup()

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        header_title = Text(
            header_text,
            font=self.theme.sans_font,
            font_size=header_title_font_size,
            weight="BOLD",
            color=self.theme.foreground,
        )

        header_subtitle = Text(
            subtitle,
            font=self.theme.sans_font,
            font_size=header_subtitle_font_size,
            weight="BOLD",
            color=self.theme.accent,
        )

        header_group = VGroup(
            header_title,
            header_subtitle,
        ).arrange(
            direction=[0, -1, 0],
            buff=0.08,
        )

        header_group.move_to(
            [
                0,
                top_outer
                - header_height / 2
                + 0.05,
                0,
            ]
        )

        header_line_y = (
            row_area_top
            + header_line_gap
        )

        header_line = Line(
            [
                -config.frame_width / 2
                + margin_x,
                header_line_y,
                0,
            ],
            [
                config.frame_width / 2
                - margin_x,
                header_line_y,
                0,
            ],
            color=ManimColor("#BBB3AC"),
            stroke_width=1.1,
        )

        page.add(
            header_group,
            header_line,
        )

        # ----------------------------------------------------
        # Center separator
        # ----------------------------------------------------

        separator_x = left_edge + column_width + column_gap / 2

        page.add(
            Line(
                [separator_x, row_area_top, 0],
                [separator_x, bottom_outer, 0],
                color=ManimColor("#C9C2BC"),
                stroke_width=1.0,
            )
        )

        answer_ratio = float(spec["answer_ratio"])

        # ----------------------------------------------------
        # Rows
        # ----------------------------------------------------

        for column_index in range(_COLUMN_COUNT):
            start = column_index * _ROWS_PER_COLUMN
            end = start + _ROWS_PER_COLUMN
            column_entries = entries[start:end]

            cell_left = left_edge + column_index * (column_width + column_gap)
            cell_right = cell_left + column_width

            prompt_left = cell_left + float(spec["number_gutter"])
            answer_right = cell_right - 0.05
            answer_width = column_width * answer_ratio
            answer_left = answer_right - answer_width
            prompt_right = answer_left - float(spec["answer_gap"])

            prompt_max_width = max(0.20, prompt_right - prompt_left)
            prompt_max_height = row_height * 0.66

            for row_index, entry in enumerate(column_entries):
                row_top = row_area_top - row_index * row_height
                row_center_y = row_top - row_height / 2

                number = Text(
                    f"{int(entry['no'])}.",
                    font=self.theme.sans_font,
                    font_size=float(spec["number_font_size"]),
                    weight="BOLD",
                    color=self.theme.accent,
                )
                number.move_to(
                    [
                        cell_left + 0.03 + number.width / 2,
                        row_center_y,
                        0,
                    ]
                )

                prompt = _make_prompt(
                    str(entry["meaning"]),
                    max_width=prompt_max_width,
                    max_height=prompt_max_height,
                    font_size=float(spec["prompt_font_size"]),
                    weight=str(spec["prompt_weight"]),
                    color=self.theme.foreground,
                    font=self.theme.sans_font,
                )
                prompt.move_to(
                    [
                        prompt_left + prompt.width / 2,
                        row_center_y,
                        0,
                    ]
                )

                answer_y = row_center_y - row_height * 0.16

                answer_line = Line(
                    [answer_left, answer_y, 0],
                    [answer_right, answer_y, 0],
                    color=ManimColor("#6F6964"),
                    stroke_width=1.35,
                )

                page.add(number, prompt, answer_line)

        self.add(page)
