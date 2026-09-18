#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ------------------------------------------------------------
# Workspace独自引数
#
# --content-file FILE
# --content-file=FILE
#
# を受け取り、Manimには渡さずPython側へ環境変数で渡す。
# ------------------------------------------------------------

original_args=("$@")
args=()
content_file=""

i=0

while (( i < ${#original_args[@]} )); do
    arg="${original_args[$i]}"

    if [[ "$arg" == "--content-file" ]]; then
        i=$((i + 1))

        if (( i >= ${#original_args[@]} )); then
            echo "ERROR: --content-file の後にJSONファイルを指定してください。" >&2
            exit 2
        fi

        content_file="${original_args[$i]}"

    elif [[ "$arg" == --content-file=* ]]; then
        content_file="${arg#--content-file=}"

    else
        args+=("$arg")
    fi

    i=$((i + 1))
done

if [[ -n "$content_file" ]]; then
    export MANIM_CONTENT_FILE="$content_file"
fi


# ------------------------------------------------------------
# 入力Pythonと同じ教材ディレクトリの output/ を
# Manimの media_dir に設定する。
# ------------------------------------------------------------

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
    exec "$repo_root/scripts/with_tex.sh"         python -m manim "${args[@]}"
fi

exec "$repo_root/scripts/with_tex.sh"     python -m manim "${render_args[@]}"
