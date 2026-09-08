#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tex_root="$repo_root/.tools/texlive/2025"
tex_bin=""

if [[ -d "$tex_root/bin" ]]; then
    for candidate in "$tex_root"/bin/*; do
        if [[ -x "$candidate/latex" ]]; then
            tex_bin="$candidate"
            break
        fi
    done
fi

if [[ -z "$tex_bin" ]]; then
    echo "TeX is not installed for this workspace." >&2
    echo "Run: pixi run setup-tex" >&2
    exit 1
fi

export PATH="$tex_bin:$PATH"
export XDG_DATA_HOME="$repo_root/.local/share"
export XDG_CACHE_HOME="$repo_root/.cache"

# Pixi/Conda の Fontconfig がデフォルト設定を自動発見できない環境向け。
# Pixi 環境内の fonts.conf を明示的に使用する。
if [[ -n "${CONDA_PREFIX:-}" && -f "$CONDA_PREFIX/etc/fonts/fonts.conf" ]]; then
    export FONTCONFIG_FILE="$CONDA_PREFIX/etc/fonts/fonts.conf"
    export FONTCONFIG_PATH="$CONDA_PREFIX/etc/fonts"
elif [[ -f /etc/fonts/fonts.conf ]]; then
    export FONTCONFIG_FILE="/etc/fonts/fonts.conf"
    export FONTCONFIG_PATH="/etc/fonts"
fi

exec "$@"