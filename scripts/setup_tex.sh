#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tex_root="$repo_root/.tools/texlive/2025"
package_file="$repo_root/scripts/tex-packages.txt"
tex_repository="${TEXLIVE_REPOSITORY:-https://pi.kwarc.info/historic/systems/texlive/2025/tlnet-final}"
tex_bin="$tex_root/bin/x86_64-linux"

if [[ "$(uname -s)" != "Linux" || "$(uname -m)" != "x86_64" ]]; then
    echo "This setup currently supports x86_64 Linux and WSL2 only." >&2
    exit 1
fi

if [[ ! -x "$tex_bin/tlmgr" ]]; then
    temp_dir="$(mktemp -d)"
    trap 'rm -rf "$temp_dir"' EXIT
    archive="$temp_dir/install-tl-unx.tar.gz"
    checksum="$archive.sha512"

    echo "Downloading the frozen TeX Live 2025 installer..."
    curl --proto '=https' --tlsv1.2 -fsSL --retry 5 --retry-all-errors \
        --connect-timeout 20 --max-time 180 \
        "$tex_repository/install-tl-unx.tar.gz" \
        -o "$archive"
    curl --proto '=https' --tlsv1.2 -fsSL --retry 5 --retry-all-errors \
        --connect-timeout 20 --max-time 180 \
        "$tex_repository/install-tl-unx.tar.gz.sha512" \
        -o "$checksum"

    (
        cd "$temp_dir"
        sha512sum --check "$(basename "$checksum")"
    )
    tar -xzf "$archive" -C "$temp_dir"

    installer_dir=""
    for candidate in "$temp_dir"/install-tl-*; do
        if [[ -x "$candidate/install-tl" ]]; then
            installer_dir="$candidate"
            break
        fi
    done
    if [[ -z "$installer_dir" ]]; then
        echo "The TeX Live installer could not be extracted." >&2
        exit 1
    fi

    profile="$temp_dir/texlive.profile"
    {
        echo "selected_scheme scheme-infraonly"
        echo "TEXDIR $tex_root"
        echo "TEXMFCONFIG $tex_root/texmf-config"
        echo "TEXMFHOME $tex_root/texmf-home"
        echo "TEXMFLOCAL $tex_root/texmf-local"
        echo "TEXMFSYSCONFIG $tex_root/texmf-config"
        echo "TEXMFSYSVAR $tex_root/texmf-var"
        echo "TEXMFVAR $tex_root/texmf-var"
        echo "binary_x86_64-linux 1"
        echo "instopt_adjustpath 0"
        echo "instopt_portable 1"
        echo "tlpdbopt_install_docfiles 0"
        echo "tlpdbopt_install_srcfiles 0"
    } >"$profile"

    echo "Installing TeX Live into $tex_root ..."
    perl "$installer_dir/install-tl" \
        -profile "$profile" \
        -repository "$tex_repository"
fi

if [[ ! -x "$tex_bin/tlmgr" ]]; then
    echo "TeX Live was found, but tlmgr is unavailable under $tex_bin." >&2
    exit 1
fi

mapfile -t packages < <(sed -E '/^[[:space:]]*(#|$)/d' "$package_file")

echo "Installing the package set declared in scripts/tex-packages.txt ..."
"$tex_bin/tlmgr" option repository "$tex_repository"
"$tex_bin/tlmgr" install "${packages[@]}"

echo "TeX setup is ready: $tex_root"
