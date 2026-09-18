# Manim Research Workspace

大学・研究発表と、小中学生向けの家庭教師教材で使う図とアニメーションを、
[Manim Community Edition](https://www.manim.community/) で継続的に制作するための
ワークスペースです。制作環境に加え、各プロジェクトのソース・素材・成果物も
このリポジトリでまとめてGit管理します。WSL2を含むx86_64 Linuxを対象に、
sudoなしで再現できる環境を提供します。

## このリポジトリでできること

- ManimCE 0.20.1とPython 3.12をPixiのロックファイルで再現
- 日本語用のNoto Sans JP／Noto Serif JPを検証済み固定版で導入
- 数式と日本語LaTeXに必要なTeX Live 2025最小環境をリポジトリ内へ導入
- 調整可能なResearch Theme（明・暗）／Education Themeと、共通の文字ヘルパー
- 同じ内容を3種類の配色で比べる1080pの動画・静止画（デザイン検討中）
- 1080p・30 fpsのMP4、高解像度PNG、透過PNGをコマンド一つで生成
- 制作したプロジェクト、素材、動画・画像・文書をソースと一緒にGitで保存
- Ruff、pytest、低画質レンダリングによるローカル検証

生成物は、実行したPythonファイルと同じディレクトリの `output/` に作られます。
完成した動画や画像はGitの管理対象です。Manimの中間キャッシュは除外します。
Pixi環境、TeX環境、フォントはそれぞれ `.pixi/`、`.tools/`、`.local/` に作られ、
これらのローカルファイルはGitには含まれません。

## 最初のセットアップ

前提は、x86_64のLinuxまたはWSL2、Git、curlです。Dockerとsudoは不要です。

```bash
bash scripts/bootstrap.sh
```

スクリプトはPixiがなければユーザー領域へ導入し、続いてManimCE、フォント、
リポジトリ専用TeX Liveをセットアップして診断を行います。初回は多くのファイルを
ダウンロードし、展開後に合計約2GBを使用するため、回線によって数分以上かかります。

個別に進める場合は次のとおりです。

```bash
# Pixiの導入後
pixi install --frozen
pixi run setup-fonts
pixi run setup-tex
pixi run doctor
```

## まずレンダリングする

```bash
# 新テーマを比較：各3画面の1080p30動画
pixi run render-research-showcase
pixi run render-research-dark-showcase
pixi run render-education-showcase

# Researchの明・暗とEducationの全画面を1080p PNGにする（計9枚）
pixi run render-theme-stills

# 低画質で素早く確認
pixi run render-preview

# 16:9、1920x1080、30 fpsのMP4
pixi run render-final

# 3840x2160の白背景PNG
pixi run render-paper

# 3840x2160の透過PNG
pixi run render-transparent
```

たとえば上記のデモは `projects/showcase/output/` に出力されます。ソースと成果物が
プロジェクト単位でまとまるため、リポジトリ直下の共通 `media/` からコピーする必要は
ありません。標準タスクは動画プレイヤーやファイルブラウザーを自動起動しません。

テーマ比較の進め方・調整箇所は [デザインレビューガイド](projects/showcase/README.md) を
参照してください。フォントも配色も仮案です。既存の機能デモと旧テーマも引き続き使えます。

任意のSceneを実行する場合は、ManimCEの引数をそのまま渡せます。

```bash
pixi run manim -- -ql projects/template/template_scene.py FirstScene
```

この場合の出力先は `projects/template/output/` です。`scripts/manim.sh` が入力Python
ファイルの親ディレクトリを判定し、ManimCEの `--media_dir` を自動設定します。

## プロジェクトを追加する

`projects/template/` をASCIIの `snake_case` 名で複製し、Pythonファイルも同じ名前へ
変更します。ファイル名を案件ごとに一意にすると、Manimの生成物が衝突しません。

```text
projects/
├── showcase/           # 機能例と動作確認
│   └── showcase.py
├── template/           # 新規プロジェクトのひな型
│   └── template_scene.py
└── my_research_topic/  # 追加例
    ├── my_research_topic.py
    ├── assets/
    └── output/            # 動画・画像などの成果物もGit管理
```

`showcase/` と `template/` に限らず、`projects/` 配下の全プロジェクトを管理対象に
します。新規プロジェクトや入れ子の教材フォルダーも、除外規則を変更せずに追加できます。

表示する日本語、コメント、文書は日本語で構いません。ファイル名、ディレクトリ名、
Sceneクラス名は、LinuxサーバーとTeXでの問題を避けるため英数字にします。

共通テーマは `src/manim_research/theme.py`、日本語TeXテンプレートは
`src/manim_research/tex.py` にあります。

```python
from manim import DOWN, LEFT, UP

from manim_research import ResearchScene


class MyScene(ResearchScene):
    def construct(self) -> None:
        layout = self.theme.layout
        title = self.title_text("研究発表").to_corner(UP + LEFT, buff=layout.edge_buff)
        body = self.body_text("図と言葉で、関係を伝える。").next_to(
            title, DOWN, aligned_edge=LEFT, buff=layout.section_buff
        )
        self.add(title, body)
```

暗い研究発表では `ResearchDarkScene`、教材では `EducationScene` を継承し、
同じ `title_text()`、`subtitle_text()`、`body_text()`、
`caption_text()`、`keyword_text()` を使います。全ヘルパーは通常のManim `Text` を返し、
`next_to()` や `arrange()` で配置できます。自動折り返し・自動縮小は行いません。

`DarkScene`、`LightScene`、既存の `jp_text()` の既定値は維持しています。
通常の日本語はPangoを使う文字ヘルパー、数式は `MathTex`、一つのTeX式に日本語も含める
場合だけ `JAPANESE_TEX_TEMPLATE` を使います。新テーマはTeXのフォント設定を変更しません。

## 品質確認

```bash
# フォーマット、Lint、単体テストだけ
pixi run check-fast

# 上記に環境診断と代表フレームのレンダリングを追加
pixi run check

# 自動整形
pixi run format
```

研究室サーバーへクローンした後は `bash scripts/bootstrap.sh` と `pixi run check` を
実行してください。古いLinuxではglibc互換性のためPixiが起動できない場合があります。
その場合はサーバーのOS情報を確認してから対応プラットフォームを追加します。

## ソースと成果物をGitに保存する

各プロジェクトのPython・TeXソース、素材・データ、完成した動画・画像・PDFなどを
一緒にコミットします。プレビュー画質の出力も管理対象です。従来の `media/` と、
Manimを直接実行したときのリポジトリ直下の `output/` にある成果物も追加できます。

Git管理から除外するのは、ローカルの実行環境、Python・開発ツールのキャッシュ、
Manim出力先の `Tex/`・`texts/`・`videos/**/partial_movie_files/`、
TeXの診断ログ `missfont.log` などです。プロジェクト内に手で置いたTeXソースやSVG素材は
管理対象のままです。

```bash
# ソース・素材・成果物をまとめて追加
git add projects/ media/

# 直接実行でルートのoutput/に出力した場合は、そのフォルダーも追加
# git add output/

# 追加内容を確認して保存
git diff --cached --stat
git diff --cached
git commit -m "Add project sources and rendered artifacts"
git push
```

成果物を更新するときも、ソースの変更と再レンダリングしたファイルを一緒に追加します。
画像・動画は通常のGitで保存し、現時点ではGit LFSのセットアップは不要です。

このリポジトリは `manim-research-workspace` としてGitHubで公開されています。
公開してよい変更だけが含まれていることを、コミット前に必ず確認してください。

## ライセンス

コードと付属サンプルは [MIT License](LICENSE) です。ManimCE、フォント、TeX、
外部素材、研究データ、生成物にはそれぞれのライセンスや権利関係が適用されます。
