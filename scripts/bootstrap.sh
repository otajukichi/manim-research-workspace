#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
pixi_bin="$(command -v pixi || true)"
pixi_home="${PIXI_HOME:-$HOME/.pixi}"

if [[ -z "$pixi_bin" && -x "$pixi_home/bin/pixi" ]]; then
    pixi_bin="$pixi_home/bin/pixi"
fi

if [[ -z "$pixi_bin" ]]; then
    temp_dir="$(mktemp -d)"
    trap 'rm -rf "$temp_dir"' EXIT
    installer="$temp_dir/install-pixi.sh"

    echo "Pixi was not found; installing it without sudo..."
    curl --proto '=https' --tlsv1.2 -fsSL --retry 5 --retry-all-errors \
        https://pixi.sh/install.sh -o "$installer"
    PIXI_VERSION="v0.72.2" sh "$installer"

    pixi_bin="$pixi_home/bin/pixi"
fi

if [[ ! -x "$pixi_bin" ]]; then
    echo "Pixi installation finished, but its executable was not found." >&2
    exit 1
fi

cd "$repo_root"
"$pixi_bin" install --frozen
"$pixi_bin" run setup

echo
echo "Setup complete. Try: $pixi_bin run render-preview"
