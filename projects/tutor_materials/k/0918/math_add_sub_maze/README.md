# たしひきざん迷路

0915 の math_addition_maze.py をベースにした、
たし算・ひき算混在版の迷路教材です。

構成:

math_add_sub_maze/
├── README.md
├── math_add_sub_maze.py
├── json/
│   └── add_sub_maze_05.json
└── output/
    └── images/

内容:

答えが 5 になるマスだけを通って、
スタートからゴールまで進みます。

足し算と引き算の両方を使用します。

レンダリング:

pixi run manim -- -s -qh projects/tutor_materials/k/0918/math_add_sub_maze/math_add_sub_maze.py AddSubMazeWorksheet
