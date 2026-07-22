"""Fail-fast diagnostics for a cloned workspace."""

from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from importlib.metadata import version

import manimpango

EXPECTED_MANIM = "0.20.1"
EXPECTED_FONTS = ("Noto Sans JP", "Noto Serif JP")
EXPECTED_COMMANDS = ("latex", "xelatex", "dvisvgm")


def main() -> int:
    failures: list[str] = []

    if platform.system() != "Linux" or platform.machine() != "x86_64":
        detected_platform = f"{platform.system()} {platform.machine()}"
        failures.append(f"unsupported platform: {detected_platform} (expected Linux x86_64)")

    manim_version = version("manim")
    if manim_version != EXPECTED_MANIM:
        failures.append(f"ManimCE {manim_version} is installed; expected {EXPECTED_MANIM}")

    installed_fonts = set(manimpango.list_fonts())
    for font in EXPECTED_FONTS:
        if font not in installed_fonts:
            failures.append(f"font is missing from Pango: {font}")

    command_versions: dict[str, str] = {}
    for command in EXPECTED_COMMANDS:
        executable = shutil.which(command)
        if executable is None:
            failures.append(f"command is missing: {command}")
            continue
        completed = subprocess.run(
            [executable, "--version"],
            check=False,
            capture_output=True,
            text=True,
        )
        first_line = (completed.stdout or completed.stderr).splitlines()
        command_versions[command] = first_line[0] if first_line else executable

    if failures:
        print("Environment check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print(f"Platform: {platform.system()} {platform.machine()}")
    print(f"Manim Community: {manim_version}")
    print("Japanese fonts: " + ", ".join(EXPECTED_FONTS))
    for command, output in command_versions.items():
        print(f"{command}: {output}")
    print("Environment check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
