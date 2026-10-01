#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd
)"

REPO_ROOT="$(
    git -C "$BASE_DIR" rev-parse --show-toplevel
)"

cd "$REPO_ROOT"

SOURCE_JSON="$BASE_DIR/../kanji_grade4_6_print_data.json"

SELECTION_DIR="$BASE_DIR/selections"
JSON_DIR="$BASE_DIR/json"

OUTPUT_DIR="$BASE_DIR/output"
RENDER_DIR="$OUTPUT_DIR/rendered"
PDF_DIR="$OUTPUT_DIR/pdf"

PY_FILE="$BASE_DIR/kanji_write_practice.py"
MAKE_CONTENT="$BASE_DIR/make_content.py"
MAKE_PDF="$BASE_DIR/make_pdf.py"

BUNDLE_NAME="${BUNDLE_NAME:-grade6_kanji_0930}"

if (( $# == 0 )); then
    SHEETS=(
        grade6_01
    )
else
    SHEETS=(
        "$@"
    )
fi

mkdir -p \
    "$JSON_DIR" \
    "$RENDER_DIR" \
    "$PDF_DIR"

# ------------------------------------------------------------
# Syntax check
# ------------------------------------------------------------

pixi run python -m py_compile \
    "$PY_FILE" \
    "$MAKE_CONTENT" \
    "$MAKE_PDF"

# 問題と答えは常にセットで扱う。
# PDFはこの配列の順に
# 問題1 -> 解答1 -> 問題2 -> 解答2 -> ...
# で1本にまとめる。
SET_PNGS=()

for name in "${SHEETS[@]}"; do
    selection="$SELECTION_DIR/${name}.json"
    content="$JSON_DIR/${name}.json"

    if [[ ! -f "$selection" ]]; then
        echo "ERROR: selection JSON not found: $selection" >&2
        exit 1
    fi

    pixi run python "$MAKE_CONTENT" \
        --source "$SOURCE_JSON" \
        --selection "$selection" \
        --output "$content"

    pixi run python -m json.tool "$content" >/dev/null

    find "$RENDER_DIR" \
        -type f \
        \( \
            -name "${name}_problem.png" \
            -o \
            -name "${name}_answer.png" \
        \) \
        -delete

    MANIM_PAGE_MODE=problem \
    pixi run manim -- \
        --content-file "$content" \
        --media_dir "$RENDER_DIR" \
        -s -qh \
        -o "${name}_problem" \
        "$PY_FILE" \
        KanjiWriteWorksheet

    MANIM_PAGE_MODE=answer \
    pixi run manim -- \
        --content-file "$content" \
        --media_dir "$RENDER_DIR" \
        -s -qh \
        -o "${name}_answer" \
        "$PY_FILE" \
        KanjiWriteWorksheet

    problem_png="$(
        find "$RENDER_DIR" \
            -type f \
            -name "${name}_problem.png" \
            -print \
            -quit
    )"

    answer_png="$(
        find "$RENDER_DIR" \
            -type f \
            -name "${name}_answer.png" \
            -print \
            -quit
    )"

    if [[ -z "$problem_png" || -z "$answer_png" ]]; then
        echo "ERROR: rendered PNG not found for $name" >&2

        find "$RENDER_DIR" \
            -type f \
            -name '*.png' \
            -print \
            >&2

        exit 1
    fi

    SET_PNGS+=(
        "$problem_png"
        "$answer_png"
    )
done

OUTPUT_PDF="$PDF_DIR/${BUNDLE_NAME}.pdf"

rm -f "$OUTPUT_PDF"

pixi run python "$MAKE_PDF" \
    --output "$OUTPUT_PDF" \
    "${SET_PNGS[@]}"

echo
echo "===== PDF output ====="
ls -lh "$OUTPUT_PDF"

if command -v pdfinfo >/dev/null 2>&1; then
    echo
    echo "===== PDF info ====="
    pdfinfo "$OUTPUT_PDF" \
        | grep -E '^(Pages|Page size):' \
        || true
fi

if command -v pdftoppm >/dev/null 2>&1; then
    PREVIEW_DIR="$PDF_DIR/preview"
    mkdir -p "$PREVIEW_DIR"

    rm -f "$PREVIEW_DIR/${BUNDLE_NAME}_page1.png"

    pdftoppm \
        -png \
        -f 1 \
        -singlefile \
        -r 150 \
        "$OUTPUT_PDF" \
        "$PREVIEW_DIR/${BUNDLE_NAME}_page1"

    echo
    echo "preview: $PREVIEW_DIR/${BUNDLE_NAME}_page1.png"
fi
