from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_SELECTION_COUNT = 20


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--selection", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)

    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise ValueError(
            f"JSON root must be an object: {path}"
        )

    return data


def resolve_item(
    source_entries: list[dict[str, Any]],
    *,
    grade: int,
    kanji: str,
    reading_type: str,
    reading: str,
) -> dict[str, Any]:

    entry_matches = [
        entry
        for entry in source_entries
        if entry.get("grade") == grade
        and entry.get("kanji") == kanji
    ]

    if len(entry_matches) != 1:
        raise ValueError(
            f"Expected exactly one grade={grade} "
            f"entry for {kanji!r}; "
            f"found {len(entry_matches)}"
        )

    entry = entry_matches[0]

    readings = (
        entry
        .get("readings", {})
        .get(reading_type)
    )

    if not isinstance(readings, list):
        raise ValueError(
            f"Invalid reading_type={reading_type!r} "
            f"for {kanji!r}"
        )

    reading_matches = [
        item
        for item in readings
        if item.get("reading") == reading
    ]

    if len(reading_matches) != 1:
        raise ValueError(
            f"Expected exactly one "
            f"{reading_type} reading={reading!r} "
            f"for {kanji!r}; "
            f"found {len(reading_matches)}"
        )

    item = reading_matches[0]
    example = item.get("example")

    if not isinstance(example, dict):
        raise ValueError(
            f"Missing example for "
            f"{kanji!r} {reading!r}"
        )

    word = example.get("word")
    word_reading = example.get("word_reading")
    sentence = example.get("sentence")

    if not all(
        isinstance(value, str) and value
        for value in (
            word,
            word_reading,
            sentence,
        )
    ):
        raise ValueError(
            f"Invalid example fields for "
            f"{kanji!r} {reading!r}"
        )

    if kanji not in word:
        raise ValueError(
            f"Target kanji {kanji!r} "
            f"is not in word {word!r}"
        )

    if word not in sentence:
        raise ValueError(
            f"Word {word!r} "
            f"is not in sentence {sentence!r}"
        )

    return {
        "kanji": kanji,
        "stroke_count": entry.get("stroke_count"),
        "reading_type": reading_type,
        "reading": reading,
        "kanji_reading": item.get(
            "kanji_reading",
            "",
        ),
        "okurigana": item.get(
            "okurigana",
            "",
        ),
        "word": word,
        "word_reading": word_reading,
        "sentence": sentence,
    }


def main() -> None:
    args = parse_args()

    source = load_json(args.source)
    selection = load_json(args.selection)

    source_entries = source.get("entries")
    selected_items = selection.get("items")
    grade = selection.get("grade")

    if not isinstance(source_entries, list):
        raise ValueError(
            "Source JSON field 'entries' "
            "must be a list"
        )

    if not isinstance(grade, int):
        raise ValueError(
            "Selection field 'grade' "
            "must be an integer"
        )

    if not isinstance(selected_items, list):
        raise ValueError(
            "Selection field 'items' "
            "must be a list"
        )

    if len(selected_items) != REQUIRED_SELECTION_COUNT:
        raise ValueError(
            "Selection must contain exactly "
            f"{REQUIRED_SELECTION_COUNT} items; "
            f"found {len(selected_items)}"
        )

    seen: set[tuple[str, str, str]] = set()
    problems: list[dict[str, Any]] = []

    for index, spec in enumerate(
        selected_items,
        start=1,
    ):
        if not isinstance(spec, dict):
            raise ValueError(
                f"items[{index - 1}] "
                "must be an object"
            )

        try:
            kanji = str(spec["kanji"])
            reading_type = str(
                spec["reading_type"]
            )
            reading = str(spec["reading"])

        except KeyError as exc:
            raise ValueError(
                f"items[{index - 1}] "
                f"is missing {exc.args[0]!r}"
            ) from exc

        if reading_type not in {
            "on",
            "kun",
        }:
            raise ValueError(
                f"items[{index - 1}]"
                ".reading_type must be "
                "'on' or 'kun'"
            )

        identity = (
            kanji,
            reading_type,
            reading,
        )

        if identity in seen:
            raise ValueError(
                f"Duplicate selection: {identity}"
            )

        seen.add(identity)

        problem = resolve_item(
            source_entries,
            grade=grade,
            kanji=kanji,
            reading_type=reading_type,
            reading=reading,
        )

        problem["no"] = index
        problems.append(problem)

    output = {
        "schema_version": "1.0.0",
        "source": str(args.source),
        "source_schema_version": (
            source.get("schema_version")
        ),
        "grade": grade,
        "title": selection.get(
            "title",
            f"小学{grade}年 漢字練習",
        ),
        "subtitle": selection.get(
            "subtitle",
            "読みを手がかりに、"
            "□に漢字を書きましょう。",
        ),
        "problems": problems,
    }

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        json.dumps(
            output,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"wrote: {args.output}")
    print(f"grade: {grade}")
    print(f"problems: {len(problems)}")
    print(
        "selected:",
        " ".join(
            problem["kanji"]
            for problem in problems
        ),
    )


if __name__ == "__main__":
    main()
