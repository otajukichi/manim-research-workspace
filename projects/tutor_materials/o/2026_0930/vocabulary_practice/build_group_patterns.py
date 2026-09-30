from __future__ import annotations

import json
import random
import shutil
import sys
from pathlib import Path


WORDS_PER_PAGE = 30
GROUP_SIZE = 60
TOTAL_WORDS = 240

GROUP_RANGES = [
    (1, 60),
    (61, 120),
    (121, 180),
    (181, 240),
]

CIRCLED = {
    1: "①",
    2: "②",
    3: "③",
    4: "④",
    5: "⑤",
    6: "⑥",
    7: "⑦",
    8: "⑧",
    9: "⑨",
    10: "⑩",
}


def circled(number: int) -> str:
    return CIRCLED.get(number, f"({number})")


def load_source(
    path: Path,
) -> tuple[str, list[dict[str, object]]]:
    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    title = str(
        data.get(
            "title",
            "中学英語 基本単語",
        )
    )

    entries = data.get("entries")

    if not isinstance(entries, list):
        raise ValueError(
            "'entries' must be a list"
        )

    if len(entries) != TOTAL_WORDS:
        raise ValueError(
            f"Expected {TOTAL_WORDS} entries, "
            f"found {len(entries)}"
        )

    required = {
        "no",
        "english",
        "pronunciation",
        "meaning",
    }

    for index, entry in enumerate(
        entries,
        start=1,
    ):
        if not isinstance(entry, dict):
            raise ValueError(
                f"Entry {index} is not an object"
            )

        missing = required - set(entry)

        if missing:
            raise ValueError(
                f"Entry {index} missing fields: "
                f"{sorted(missing)}"
            )

        if int(entry["no"]) != index:
            raise ValueError(
                f"Expected no={index}, "
                f"found {entry['no']}"
            )

    return title, entries


def write_page(
    path: Path,
    *,
    title: str,
    pattern_number: int,
    page_index: int,
    start_no: int,
    end_no: int,
    half_label: str,
    entries: list[dict[str, object]],
) -> None:
    seed = pattern_number

    payload = {
        "title": title,
        "header_range": f"{start_no}-{end_no}",
        "subtitle": (
            f"パターン{circled(pattern_number)}"
            f"　{half_label}"
        ),
        "mode": "group_pattern",
        "pattern_number": pattern_number,
        "seed": seed,
        "page_index": page_index,
        "page_count": 8,
        "entry_count": len(entries),
        "numbers": [
            int(entry["no"])
            for entry in entries
        ],
        "entries": entries,
    }

    path.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def build_pattern(
    *,
    title: str,
    source_entries: list[dict[str, object]],
    json_root: Path,
    pattern_number: int,
) -> None:
    seed = pattern_number

    output_dir = (
        json_root
        / f"pattern_{pattern_number:02d}_groups"
    )

    # このパターンだけ作り直す。
    # pattern_01_groups には触れない。
    if output_dir.exists():
        shutil.rmtree(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    rng = random.Random(seed)

    page_index = 1

    for start_no, end_no in GROUP_RANGES:
        group_entries = [
            entry
            for entry in source_entries
            if start_no
            <= int(entry["no"])
            <= end_no
        ]

        if len(group_entries) != GROUP_SIZE:
            raise ValueError(
                f"{start_no}-{end_no}: "
                f"expected {GROUP_SIZE} entries, "
                f"found {len(group_entries)}"
            )

        shuffled = list(group_entries)
        rng.shuffle(shuffled)

        front = shuffled[:WORDS_PER_PAGE]
        back = shuffled[WORDS_PER_PAGE:]

        if len(front) != 30:
            raise ValueError(
                "Front page must contain 30 entries"
            )

        if len(back) != 30:
            raise ValueError(
                "Back page must contain 30 entries"
            )

        # 同一60語内で同じNo.が重複していないことを確認。
        combined_numbers = [
            int(entry["no"])
            for entry in front + back
        ]

        expected_numbers = list(
            range(
                start_no,
                end_no + 1,
            )
        )

        if sorted(combined_numbers) != expected_numbers:
            raise ValueError(
                f"{start_no}-{end_no}: "
                "shuffle lost or duplicated entries"
            )

        write_page(
            output_dir / f"page_{page_index:02d}.json",
            title=title,
            pattern_number=pattern_number,
            page_index=page_index,
            start_no=start_no,
            end_no=end_no,
            half_label="前半",
            entries=front,
        )

        page_index += 1

        write_page(
            output_dir / f"page_{page_index:02d}.json",
            title=title,
            pattern_number=pattern_number,
            page_index=page_index,
            start_no=start_no,
            end_no=end_no,
            half_label="後半",
            entries=back,
        )

        page_index += 1

    files = sorted(
        output_dir.glob("page_*.json")
    )

    if len(files) != 8:
        raise ValueError(
            f"Pattern {pattern_number}: "
            f"expected 8 pages, "
            f"found {len(files)}"
        )

    print()
    print(
        f"=== パターン{circled(pattern_number)} "
        f"(seed={seed}) ==="
    )

    for path in files:
        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        nums = data["numbers"]

        print(
            f"{path.name}: "
            f"{data['header_range']} / "
            f"{data['subtitle']} / "
            f"{len(nums)} words"
        )


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit(
            "Usage:\n"
            "pixi run python build_group_patterns.py "
            "<source_json> <json_root> "
            "<pattern> [<pattern> ...]"
        )

    source_json = Path(
        sys.argv[1]
    ).resolve()

    json_root = Path(
        sys.argv[2]
    ).resolve()

    pattern_numbers = [
        int(value)
        for value in sys.argv[3:]
    ]

    if len(set(pattern_numbers)) != len(
        pattern_numbers
    ):
        raise ValueError(
            "Pattern numbers must not duplicate"
        )

    title, source_entries = load_source(
        source_json
    )

    for pattern_number in pattern_numbers:
        if pattern_number < 1:
            raise ValueError(
                "Pattern number must be >= 1"
            )

        build_pattern(
            title=title,
            source_entries=source_entries,
            json_root=json_root,
            pattern_number=pattern_number,
        )


if __name__ == "__main__":
    main()
