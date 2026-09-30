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


_CIRCLED_NUMBERS = {
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
    11: "⑪",
    12: "⑫",
    13: "⑬",
    14: "⑭",
    15: "⑮",
    16: "⑯",
    17: "⑰",
    18: "⑱",
    19: "⑲",
    20: "⑳",
}


def circled_number(number: int) -> str:
    return _CIRCLED_NUMBERS.get(number, f"({number})")


def load_entries(
    path: Path,
) -> tuple[str, list[dict[str, object]]]:
    data = json.loads(path.read_text(encoding="utf-8"))

    title = str(
        data.get(
            "title",
            "中学英語 基本単語",
        )
    )

    entries = data.get("entries")

    if not isinstance(entries, list):
        raise ValueError("'entries' must be a list")

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

    for index, entry in enumerate(entries, start=1):
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

        if entry["no"] != index:
            raise ValueError(
                f"Expected no={index}, "
                f"found no={entry['no']}"
            )

    return title, entries


def chunked(
    entries: list[dict[str, object]],
    size: int,
) -> list[list[dict[str, object]]]:
    return [
        entries[index : index + size]
        for index in range(0, len(entries), size)
    ]


def write_page(
    output: Path,
    *,
    title: str,
    header_range: str,
    subtitle: str,
    mode: str,
    pattern_number: int | None,
    seed: int | None,
    page_index: int,
    page_count: int,
    entries: list[dict[str, object]],
) -> None:
    payload = {
        "title": title,
        "header_range": header_range,
        "subtitle": subtitle,
        "mode": mode,
        "pattern_number": pattern_number,
        # seedは再現用としてJSON内だけに保持。
        # プリント上には表示しない。
        "seed": seed,
        "page_index": page_index,
        "page_count": page_count,
        "entry_count": len(entries),
        "numbers": [
            int(entry["no"])
            for entry in entries
        ],
        "entries": entries,
    }

    output.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def build_ordered(
    *,
    title: str,
    entries: list[dict[str, object]],
    output_dir: Path,
) -> None:
    pages = chunked(
        entries,
        WORDS_PER_PAGE,
    )

    if len(pages) != 8:
        raise ValueError(
            f"Ordered pages must be 8, got {len(pages)}"
        )

    for page_index, page_entries in enumerate(
        pages,
        start=1,
    ):
        group_index = (page_index - 1) // 2

        start_no, end_no = GROUP_RANGES[group_index]

        half_label = (
            "前半"
            if (page_index - 1) % 2 == 0
            else "後半"
        )

        write_page(
            output_dir / f"page_{page_index:02d}.json",
            title=title,
            header_range=f"{start_no}-{end_no}",
            subtitle=half_label,
            mode="ordered",
            pattern_number=None,
            seed=None,
            page_index=page_index,
            page_count=8,
            entries=page_entries,
        )


def build_group_pattern(
    *,
    title: str,
    entries: list[dict[str, object]],
    json_root: Path,
    pattern_number: int,
) -> None:
    # パターン番号 = seed
    seed = pattern_number

    output_dir = (
        json_root
        / f"pattern_{pattern_number:02d}_groups"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    rng = random.Random(seed)

    overall_page_index = 1

    for start_no, end_no in GROUP_RANGES:
        group_entries = [
            entry
            for entry in entries
            if start_no
            <= int(entry["no"])
            <= end_no
        ]

        if len(group_entries) != GROUP_SIZE:
            raise ValueError(
                f"{start_no}-{end_no}: "
                f"expected {GROUP_SIZE}, "
                f"found {len(group_entries)}"
            )

        shuffled = list(group_entries)
        rng.shuffle(shuffled)

        pages = chunked(
            shuffled,
            WORDS_PER_PAGE,
        )

        if len(pages) != 2:
            raise ValueError(
                f"{start_no}-{end_no} "
                "must produce exactly 2 pages"
            )

        for half_index, page_entries in enumerate(
            pages,
            start=1,
        ):
            half_label = (
                "前半"
                if half_index == 1
                else "後半"
            )

            subtitle = (
                f"パターン"
                f"{circled_number(pattern_number)}"
                f"　{half_label}"
            )

            write_page(
                output_dir
                / f"page_{overall_page_index:02d}.json",
                title=title,
                header_range=f"{start_no}-{end_no}",
                subtitle=subtitle,
                mode="group_pattern",
                pattern_number=pattern_number,
                seed=seed,
                page_index=overall_page_index,
                page_count=8,
                entries=page_entries,
            )

            overall_page_index += 1


def build_all_pattern(
    *,
    title: str,
    entries: list[dict[str, object]],
    json_root: Path,
    pattern_number: int,
) -> None:
    seed = pattern_number

    output_dir = (
        json_root
        / f"pattern_{pattern_number:02d}_all"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    rng = random.Random(seed)

    shuffled = list(entries)
    rng.shuffle(shuffled)

    pages = chunked(
        shuffled,
        WORDS_PER_PAGE,
    )

    if len(pages) != 8:
        raise ValueError(
            f"All-word pattern must produce 8 pages, "
            f"got {len(pages)}"
        )

    for page_index, page_entries in enumerate(
        pages,
        start=1,
    ):
        subtitle = (
            f"パターン"
            f"{circled_number(pattern_number)}"
            f"　{page_index}/8"
        )

        write_page(
            output_dir / f"page_{page_index:02d}.json",
            title=title,
            header_range="1-240",
            subtitle=subtitle,
            mode="all_pattern",
            pattern_number=pattern_number,
            seed=seed,
            page_index=page_index,
            page_count=8,
            entries=page_entries,
        )


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit(
            "Usage:\n"
            "pixi run python build_practice_jsons.py "
            "<source_json> <json_root> <pattern_count>"
        )

    source_json = Path(sys.argv[1]).resolve()
    json_root = Path(sys.argv[2]).resolve()
    pattern_count = int(sys.argv[3])

    if pattern_count < 1:
        raise ValueError(
            "pattern_count must be >= 1"
        )

    title, entries = load_entries(
        source_json
    )

    # --------------------------------------------------------
    # 旧生成ディレクトリを整理
    # --------------------------------------------------------

    old_generated_dirs = [
        json_root / "ordered",
        json_root / "shuffle_groups_seed49",
        json_root / "shuffle_all_seed49",
    ]

    for directory in old_generated_dirs:
        if directory.exists():
            shutil.rmtree(directory)

    for directory in json_root.glob("pattern_*"):
        if directory.is_dir():
            shutil.rmtree(directory)

    # --------------------------------------------------------
    # 通常順
    # --------------------------------------------------------

    ordered_dir = json_root / "ordered"

    ordered_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    build_ordered(
        title=title,
        entries=entries,
        output_dir=ordered_dir,
    )

    # --------------------------------------------------------
    # パターン①、②、③...
    #
    # pattern_number と seed は常に同じ値。
    # --------------------------------------------------------

    for pattern_number in range(
        1,
        pattern_count + 1,
    ):
        build_group_pattern(
            title=title,
            entries=entries,
            json_root=json_root,
            pattern_number=pattern_number,
        )

        build_all_pattern(
            title=title,
            entries=entries,
            json_root=json_root,
            pattern_number=pattern_number,
        )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("=== generated patterns ===")
    print(f"pattern count: {pattern_count}")

    for pattern_number in range(
        1,
        pattern_count + 1,
    ):
        print(
            f"pattern "
            f"{circled_number(pattern_number)} "
            f"= seed {pattern_number}"
        )

        for suffix in ("groups", "all"):
            directory = (
                json_root
                / f"pattern_{pattern_number:02d}_{suffix}"
            )

            files = sorted(
                directory.glob("page_*.json")
            )

            print(
                f"  {directory.name}: "
                f"{len(files)} pages"
            )

            for path in files:
                data = json.loads(
                    path.read_text(
                        encoding="utf-8"
                    )
                )

                nums = data["numbers"]

                print(
                    f"    {path.name}: "
                    f"{data['header_range']} / "
                    f"{data['subtitle']} / "
                    f"{len(nums)} words"
                )


if __name__ == "__main__":
    main()
