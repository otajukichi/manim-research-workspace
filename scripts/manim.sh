#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Keep each project's source and rendered files together.  Manim itself does
# not provide a placeholder for the input file's directory, so derive the
# media directory here and inject it immediately before the input file.
args=("$@")
render_args=()
input_found=false
media_dir_set=false

for arg in "${args[@]}"; do
    if [[ "$arg" == "--media_dir" || "$arg" == --media_dir=* ]]; then
        media_dir_set=true
        break
    fi
done

for arg in "${args[@]}"; do
    if [[ "$input_found" == false && "$arg" == *.py ]]; then
        input_file="$arg"
        if [[ "$input_file" != /* ]]; then
            input_file="$PWD/$input_file"
        fi
        project_dir="$(cd "$(dirname "$input_file")" && pwd)"
        if [[ "$media_dir_set" == false ]]; then
            render_args+=(--media_dir "$project_dir/output")
        fi
        input_found=true
    fi
    render_args+=("$arg")
done

if [[ "$input_found" == false ]]; then
    exec "$repo_root/scripts/with_tex.sh" python -m manim "${args[@]}"
fi

exec "$repo_root/scripts/with_tex.sh" python -m manim "${render_args[@]}"
