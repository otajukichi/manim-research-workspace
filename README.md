# BD_Adv ManimCE Workspace

研究提案、論文、授業発表で使う図とアニメーションを、
[Manim Community Edition](https://www.manim.community/) で継続的に制作するための
ワークスペースです。WSL2を含むx86_64 Linuxを対象に、sudoなしで再現できる環境を提供します。

## このリポジトリでできること

- ManimCE 0.20.1とPython 3.12をPixiのロックファイルで再現
- 日本語用のNoto Sans JP／Noto Serif JPを検証済み固定版で導入
- 数式と日本語LaTeXに必要なTeX Live 2025最小環境をリポジトリ内へ導入
- 発表・動画向け暗色テーマと、論文・印刷向け白背景テーマを共用
- 1080p・30 fpsのMP4、高解像度PNG、透過PNGをコマンド一つで生成
- Ruff、pytest、低画質レンダリングによるローカル検証

生成物、Pixi環境、TeX環境、フォントはそれぞれ `media/`、`.pixi/`、`.tools/`、`.local/` に作られ、
Gitには含まれません。

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
# 低画質で素早く確認
pixi run render-preview

# 16:9、1920x1080、30 fpsのMP4
pixi run render-final

# 3840x2160の白背景PNG
pixi run render-paper

# 3840x2160の透過PNG
pixi run render-transparent
```

出力先は `media/` です。サーバーでも安全に動くよう、標準タスクは動画プレイヤーや
ファイルブラウザーを自動起動しません。

任意のSceneを実行する場合は、ManimCEの引数をそのまま渡せます。

```bash
pixi run manim -- -ql projects/template/template_scene.py FirstScene
```

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
    └── assets/
```

表示する日本語、コメント、文書は日本語で構いません。ファイル名、ディレクトリ名、
Sceneクラス名は、LinuxサーバーとTeXでの問題を避けるため英数字にします。

共通テーマは `src/bd_adv_manim/theme.py`、日本語TeXテンプレートは
`src/bd_adv_manim/tex.py` にあります。

```python
from manim import Circle, Create

from bd_adv_manim import DarkScene


class MyScene(DarkScene):
    def construct(self) -> None:
        circle = Circle(color=self.theme.accent)
        title = self.jp_text("研究発表", font_size=48)
        self.add(title)
        self.play(Create(circle))
```

白背景の図では `LightScene` を継承します。通常の日本語はPangoを使う `jp_text()`、
数式は `MathTex`、一つのTeX式に日本語も含める場合だけ `JAPANESE_TEX_TEMPLATE` を使います。

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

## GitHubで公開するとき

今回はローカルリポジトリだけを作成します。内容を確認してGitHub側に空の公開リポジトリを
作った後、次の形で接続できます。

```bash
git remote add origin https://github.com/USER/REPOSITORY.git
git push -u origin main
```

未発表研究、共同研究、講義資料、第三者の画像やデータは、この公開リポジトリへ
誤ってコミットしないでください。非公開案件は別のprivateリポジトリで扱うのが安全です。

## ライセンス

コードと付属サンプルは [MIT License](LICENSE) です。ManimCE、フォント、TeX、
外部素材、研究データ、生成物にはそれぞれのライセンスや権利関係が適用されます。
