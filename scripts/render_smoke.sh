#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "$repo_root/scripts/manim.sh" \
    -ql \
    -s \
    projects/showcase/showcase.py \
    RenderSmoke
