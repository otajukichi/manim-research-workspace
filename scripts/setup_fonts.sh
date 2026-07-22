#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
font_dir="$repo_root/.local/share/fonts/manim"
mkdir -p "$font_dir"

download_font() {
    local filename="$1"
    local url="$2"
    local expected_sha256="$3"
    local target="$font_dir/$filename"

    if [[ -f "$target" ]] && echo "$expected_sha256  $target" | sha256sum --check --status; then
        echo "Font already verified: $filename"
        return
    fi

    echo "Downloading $filename ..."
    curl --proto '=https' --tlsv1.2 -fsSL --retry 5 --retry-all-errors \
        "$url" -o "$target.tmp"
    echo "$expected_sha256  $target.tmp" | sha256sum --check --status
    mv "$target.tmp" "$target"
}

download_font \
    "NotoSansJP-Regular.otf" \
    "https://raw.githubusercontent.com/notofonts/noto-cjk/Sans2.004/Sans/SubsetOTF/JP/NotoSansJP-Regular.otf" \
    "dff723ba59d57d136764a04b9b2d03205544f7cd785a711442d6d2d085ac5073"
download_font \
    "NotoSansJP-Bold.otf" \
    "https://raw.githubusercontent.com/notofonts/noto-cjk/Sans2.004/Sans/SubsetOTF/JP/NotoSansJP-Bold.otf" \
    "1b0edfb500b73a4fa8a4fcaae1bbbd403994e08e73e3e0da37e70d3853f42c5f"
download_font \
    "NotoSerifJP-Regular.otf" \
    "https://raw.githubusercontent.com/notofonts/noto-cjk/Serif2.003/Serif/SubsetOTF/JP/NotoSerifJP-Regular.otf" \
    "2c9a12dbd4f2408c4610c7ee84a108b62d7236c3775baed618c64d9cb44b2f04"
download_font \
    "NotoSerifJP-Bold.otf" \
    "https://raw.githubusercontent.com/notofonts/noto-cjk/Serif2.003/Serif/SubsetOTF/JP/NotoSerifJP-Bold.otf" \
    "1e03488a0d5e819f07fcd74f54703a7961ba466d3ae900f8a2a730541e6d4543"

XDG_DATA_HOME="$repo_root/.local/share" \
XDG_CACHE_HOME="$repo_root/.cache" \
fc-cache -f "$font_dir"

echo "Fonts are ready: $font_dir"
