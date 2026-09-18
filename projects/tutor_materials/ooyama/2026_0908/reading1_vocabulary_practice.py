from __future__ import annotations

import csv
import random
import secrets
from dataclasses import replace
from pathlib import Path

from manim import Line, ManimColor, Text, VGroup, config

from manim_research import EDUCATION_THEME, EducationScene


# ============================================================
# Control Parameters
# ============================================================

DISPLAY_LANGUAGE = "japanese"  # "english" / "japanese"

SELECTED_SECTIONS = ("left",)  # tuple of sections to include
# 例:
# ("left",)
# ("middle", "right")
# ("left", "right")
# ("left", "middle", "right")  # all

SHUFFLE = True

RANDOM_SEED: int | None = 49
# int  : 同じ並びを再現
# None : 実行ごとに新しいseedを生成し、その値を出力ファイル名に入れる


# ============================================================
# Fixed worksheet settings
# ============================================================

DATA_FILE = Path(__file__).with_name("reading1_vocabulary.tsv")

_ALLOWED_LANGUAGES = {"english", "japanese"}
_SECTION_ORDER = ("left", "middle", "right")
_ROWS_PER_COLUMN = 16

A4_WIDTH_MM = 210
A4_HEIGHT_MM = 297
A4_PIXEL_WIDTH = 2480
A4_PIXEL_HEIGHT = 3508
FRAME_HEIGHT = 14.0
FRAME_WIDTH = FRAME_HEIGHT * A4_WIDTH_MM / A4_HEIGHT_MM


def _validate_controls() -> tuple[str, ...]:
    if DISPLAY_LANGUAGE not in _ALLOWED_LANGUAGES:
        raise ValueError(
            f"DISPLAY_LANGUAGE must be one of {sorted(_ALLOWED_LANGUAGES)}, "
            f"got {DISPLAY_LANGUAGE!r}"
        )

    if not SELECTED_SECTIONS:
        raise ValueError("SELECTED_SECTIONS must contain at least one section.")

    if len(set(SELECTED_SECTIONS)) != len(SELECTED_SECTIONS):
        raise ValueError("SELECTED_SECTIONS must not contain duplicates.")

    unknown = set(SELECTED_SECTIONS) - set(_SECTION_ORDER)
    if unknown:
        raise ValueError(
            f"Unknown section(s): {sorted(unknown)}. "
            f"Choose from {_SECTION_ORDER}."
        )

    return tuple(section for section in _SECTION_ORDER if section in SELECTED_SECTIONS)


SELECTED_SECTIONS_NORMALIZED = _validate_controls()

if SHUFFLE:
    ACTIVE_SEED = RANDOM_SEED if RANDOM_SEED is not None else secrets.randbelow(1_000_000_000)
else:
    ACTIVE_SEED = None

if SELECTED_SECTIONS_NORMALIZED == _SECTION_ORDER:
    RANGE_LABEL = "all"
else:
    RANGE_LABEL = "-".join(SELECTED_SECTIONS_NORMALIZED)

ORDER_LABEL = f"seed{ACTIVE_SEED}" if SHUFFLE else "ordered"
OUTPUT_STEM = f"vocab_practice_{DISPLAY_LANGUAGE}_{RANGE_LABEL}_{ORDER_LABEL}"

# A4 portrait, 300 dpi.
config.pixel_width = A4_PIXEL_WIDTH
config.pixel_height = A4_PIXEL_HEIGHT
config.frame_width = FRAME_WIDTH
config.frame_height = FRAME_HEIGHT
config.output_file = OUTPUT_STEM


PRINT_THEME = replace(
    EDUCATION_THEME,
    background=ManimColor("#FFFFFF"),
    foreground=ManimColor("#26221F"),
    muted=ManimColor("#8D857F"),
    accent=ManimColor("#A84624"),
    surface=ManimColor("#FFFFFF"),
)


def load_selected_entries() -> list[dict[str, str]]:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Vocabulary file not found: {DATA_FILE}")

    with DATA_FILE.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file, delimiter="\t")
        required = {"section", "english", "japanese"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError("TSV header must contain: section, english, japanese")

        entries = [
            row
            for row in reader
            if row["section"] in SELECTED_SECTIONS_NORMALIZED
        ]

    expected = _ROWS_PER_COLUMN * len(SELECTED_SECTIONS_NORMALIZED)
    if len(entries) != expected:
        raise ValueError(
            f"Expected {expected} entries for {SELECTED_SECTIONS_NORMALIZED}, "
            f"but found {len(entries)}."
        )

    # Mix all selected sections first, then split into 16-row display columns.
    if SHUFFLE:
        random.Random(ACTIVE_SEED).shuffle(entries)

    return entries


def _layout_spec(column_count: int) -> dict[str, float | str]:
    """Visual settings only; worksheet rows always stay fixed at 16."""
    if column_count == 1:
        return {
            "margin_x": 0.38,
            "margin_y": 0.34,
            "column_gap": 0.00,
            "number_gutter": 0.52,
            "number_font_size": 21,
            "prompt_font_size": 32,
            "prompt_weight": "BOLD",
            "answer_ratio_english": 0.46,
            "answer_ratio_japanese": 0.58,
            "answer_gap": 0.18,
            "separator": 0.0,
        }

    if column_count == 2:
        return {
            "margin_x": 0.28,
            "margin_y": 0.30,
            "column_gap": 0.20,
            "number_gutter": 0.42,
            "number_font_size": 17,
            "prompt_font_size": 22,
            "prompt_weight": "BOLD",
            "answer_ratio_english": 0.44,
            "answer_ratio_japanese": 0.54,
            "answer_gap": 0.12,
            "separator": 1.0,
        }

    return {
        "margin_x": 0.20,
        "margin_y": 0.24,
        "column_gap": 0.14,
        "number_gutter": 0.33,
        "number_font_size": 12,
        "prompt_font_size": 16,
        "prompt_weight": "NORMAL",
        "answer_ratio_english": 0.43,
        "answer_ratio_japanese": 0.53,
        "answer_gap": 0.08,
        "separator": 1.0,
    }


def _preferred_break_positions(text: str) -> list[int]:
    """Prefer natural boundaries, but allow Japanese text to break anywhere."""
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
    """Fit a prompt into its left-hand area, using at most two lines."""

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

    # Natural boundaries first. If there is no useful boundary, Japanese text
    # may be broken between characters.
    candidates = preferred or list(range(1, len(text)))

    # Try the most balanced break first.
    candidates = sorted(candidates, key=lambda index: abs(index - midpoint))

    best: Text | None = None
    best_score: float | None = None

    for index in candidates:
        left = text[:index].strip()
        right = text[index:].strip()
        if not left or not right:
            continue

        wrapped = make(f"{left}\n{right}")

        # Prefer a candidate that already fits without shrinking.
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
    """A4 portrait vocabulary worksheet generated from reading1_vocabulary.tsv."""

    theme = PRINT_THEME

    def construct(self) -> None:
        entries = load_selected_entries()
        column_count = len(SELECTED_SECTIONS_NORMALIZED)
        spec = _layout_spec(column_count)

        margin_x = float(spec["margin_x"])
        margin_y = float(spec["margin_y"])
        column_gap = float(spec["column_gap"])

        content_width = config.frame_width - 2 * margin_x
        content_height = config.frame_height - 2 * margin_y
        column_width = (
            content_width - column_gap * (column_count - 1)
        ) / column_count
        row_height = content_height / _ROWS_PER_COLUMN

        left_edge = -config.frame_width / 2 + margin_x
        top_edge = config.frame_height / 2 - margin_y

        page = VGroup()

        if float(spec["separator"]) > 0:
            for column_index in range(1, column_count):
                x = (
                    left_edge
                    + column_index * column_width
                    + (column_index - 0.5) * column_gap
                )
                page.add(
                    Line(
                        [x, top_edge, 0],
                        [x, top_edge - content_height, 0],
                        color=ManimColor("#E1DDD9"),
                        stroke_width=0.9,
                    )
                )

        answer_ratio_key = (
            "answer_ratio_japanese"
            if DISPLAY_LANGUAGE == "japanese"
            else "answer_ratio_english"
        )
        answer_ratio = float(spec[answer_ratio_key])

        for column_index in range(column_count):
            column_entries = entries[
                column_index * _ROWS_PER_COLUMN :
                (column_index + 1) * _ROWS_PER_COLUMN
            ]

            cell_left = left_edge + column_index * (column_width + column_gap)
            cell_right = cell_left + column_width

            prompt_left = cell_left + float(spec["number_gutter"])
            answer_right = cell_right - 0.05
            answer_width = column_width * answer_ratio
            answer_left = answer_right - answer_width
            prompt_right = answer_left - float(spec["answer_gap"])

            prompt_max_width = max(0.20, prompt_right - prompt_left)
            prompt_max_height = row_height * 0.78

            for row_index, entry in enumerate(column_entries):
                question_number = column_index * _ROWS_PER_COLUMN + row_index + 1
                row_top = top_edge - row_index * row_height
                row_center_y = row_top - row_height / 2

                number = Text(
                    f"{question_number}.",
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
                    entry[DISPLAY_LANGUAGE],
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

                # The blank is deliberately on the RIGHT of the prompt.
                # Japanese prompts reserve a little more width because the
                # student will usually write the longer English answer.
                answer_y = row_center_y - row_height * 0.16
                answer_line = Line(
                    [answer_left, answer_y, 0],
                    [answer_right, answer_y, 0],
                    color=ManimColor("#756E68"),
                    stroke_width=1.25,
                )

                page.add(number, prompt, answer_line)

        self.add(page)
