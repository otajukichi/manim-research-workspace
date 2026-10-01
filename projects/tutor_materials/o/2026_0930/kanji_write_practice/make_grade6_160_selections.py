from __future__ import annotations

import json
import random
from pathlib import Path


REPO_ROOT = Path.cwd()

SOURCE = (
    REPO_ROOT
    / "projects/tutor_materials/o/2026_0930"
    / "kanji_grade4_6_print_data.json"
)

SELECTION_DIR = (
    REPO_ROOT
    / "projects/tutor_materials/o/2026_0930"
    / "kanji_write_practice/selections"
)

GRADE = 6
TOTAL_KANJI = 160
QUESTIONS_PER_SHEET = 20
SHEET_COUNT = 8

SEED = 20260930


def main() -> None:
    data = json.loads(
        SOURCE.read_text(
            encoding="utf-8"
        )
    )

    grade6 = [
        entry
        for entry in data["entries"]
        if entry["grade"] == GRADE
    ]

    if len(grade6) < TOTAL_KANJI:
        raise RuntimeError(
            f"6年生漢字が不足しています: "
            f"{len(grade6)} < {TOTAL_KANJI}"
        )

    # 元JSON自体で漢字が一意であることも確認。
    kanji_list = [
        entry["kanji"]
        for entry in grade6
    ]

    if len(set(kanji_list)) != len(kanji_list):
        raise RuntimeError(
            "6年生エントリに重複漢字があります。"
        )

    rng = random.Random(SEED)

    # --------------------------------------------
    # 160字をランダム抽出
    # --------------------------------------------

    selected_entries = grade6[:]
    rng.shuffle(selected_entries)

    selected_entries = selected_entries[
        :TOTAL_KANJI
    ]

    selections = []

    for entry in selected_entries:
        reading_candidates = []

        for reading_type in (
            "on",
            "kun",
        ):
            for reading in entry[
                "readings"
            ][reading_type]:
                reading_candidates.append(
                    (
                        reading_type,
                        reading,
                    )
                )

        if not reading_candidates:
            raise RuntimeError(
                f"読みがありません: "
                f"{entry['kanji']}"
            )

        # 今日の版では読みも固定seedでランダム。
        reading_type, reading_data = (
            rng.choice(
                reading_candidates
            )
        )

        selections.append(
            {
                "kanji": entry["kanji"],
                "reading_type": reading_type,
                "reading": (
                    reading_data["reading"]
                ),
                "word": (
                    reading_data["example"]["word"]
                ),
                "word_reading": (
                    reading_data["example"][
                        "word_reading"
                    ]
                ),
                "sentence": (
                    reading_data["example"][
                        "sentence"
                    ]
                ),
                "okurigana": (
                    reading_data.get(
                        "okurigana",
                        "",
                    )
                ),
            }
        )

    if len(selections) != TOTAL_KANJI:
        raise RuntimeError(
            "160問生成できませんでした。"
        )

    if len(
        {
            item["kanji"]
            for item in selections
        }
    ) != TOTAL_KANJI:
        raise RuntimeError(
            "選択漢字が160字で一意ではありません。"
        )

    SELECTION_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------
    # 20問 × 8 JSON
    # --------------------------------------------

    for sheet_index in range(
        SHEET_COUNT
    ):
        start = (
            sheet_index
            * QUESTIONS_PER_SHEET
        )

        end = (
            start
            + QUESTIONS_PER_SHEET
        )

        chunk = selections[
            start:end
        ]

        items = [
            {
                "kanji": item["kanji"],
                "reading_type": (
                    item["reading_type"]
                ),
                "reading": item["reading"],
            }
            for item in chunk
        ]

        sheet_number = (
            sheet_index + 1
        )

        output = {
            "title": (
                "小学6年 漢字の書き取り "
                f"{sheet_number}"
            ),
            "subtitle": (
                "読みを手がかりに、"
                "漢字を書きましょう。"
            ),
            "grade": GRADE,
            "items": items,
        }

        output_path = (
            SELECTION_DIR
            / f"grade6_{sheet_number:02d}.json"
        )

        output_path.write_text(
            json.dumps(
                output,
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        print(
            f"{sheet_number}:",
            "".join(
                item["kanji"]
                for item in chunk
            ),
        )

    # --------------------------------------------
    # 選定記録
    # 後日、厳密なルール版と比較できるよう残す。
    # --------------------------------------------

    manifest = {
        "grade": GRADE,
        "seed": SEED,
        "selection_policy": (
            "grade6 entries を固定seedでshuffleし"
            "先頭160字を採用。各漢字の読み候補から"
            "固定seedで1つ選択。"
        ),
        "total_kanji": TOTAL_KANJI,
        "questions_per_sheet": (
            QUESTIONS_PER_SHEET
        ),
        "sheet_count": SHEET_COUNT,
        "items": [
            {
                "no": index,
                **item,
            }
            for index, item in enumerate(
                selections,
                start=1,
            )
        ],
    }

    manifest_path = (
        SELECTION_DIR
        / "grade6_160_manifest.json"
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print()
    print(
        "manifest:",
        manifest_path,
    )


if __name__ == "__main__":
    main()
