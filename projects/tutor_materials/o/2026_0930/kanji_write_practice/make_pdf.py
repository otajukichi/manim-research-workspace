from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


A4_PIXEL_SIZE = (
    2480,
    3508,
)

A4_RATIO = (
    A4_PIXEL_SIZE[0]
    / A4_PIXEL_SIZE[1]
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "images",
        nargs="+",
        type=Path,
    )

    return parser.parse_args()


def open_page(
    path: Path,
) -> Image.Image:

    if not path.is_file():
        raise FileNotFoundError(path)

    with Image.open(path) as image:
        width, height = image.size
        ratio = width / height

        if abs(
            ratio - A4_RATIO
        ) > 0.01:
            raise ValueError(
                "Not an A4 portrait "
                "aspect ratio: "
                f"{path} "
                f"({width}x{height})"
            )

        if (
            image.mode in {
                "RGBA",
                "LA",
            }
            or "transparency"
            in image.info
        ):
            rgba = image.convert(
                "RGBA"
            )

            white = Image.new(
                "RGBA",
                rgba.size,
                "white",
            )

            white.alpha_composite(
                rgba
            )

            page = white.convert(
                "RGB"
            )

        else:
            page = image.convert(
                "RGB"
            )

        if (
            page.size
            != A4_PIXEL_SIZE
        ):
            page = page.resize(
                A4_PIXEL_SIZE,
                Image.Resampling.LANCZOS,
            )

        return page.copy()


def main() -> None:
    args = parse_args()

    pages = [
        open_page(path)
        for path in args.images
    ]

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    first, *rest = pages

    first.save(
        args.output,
        "PDF",
        resolution=300.0,
        save_all=True,
        append_images=rest,
        quality=95,
        subsampling=0,
    )

    for page in pages:
        page.close()

    print(
        f"wrote: {args.output}"
    )

    print(
        f"pages: {len(args.images)}"
    )


if __name__ == "__main__":
    main()
