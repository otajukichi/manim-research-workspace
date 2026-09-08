# Theme design review — 第2案（配色調整）

今回はフォントや配色を確定せず、研究発表と小中学生向け教材を比較するための実装です。
既存の固定版Noto Sans JP／Noto Serif JPのRegular・Boldを使います。
Researchは白に近い背景と落ち着いた青、Educationはクリーム背景とオレンジ・ハニー色を
使います。文字サイズと基本レイアウトは第1案を引き継いでいます。
第1案の紺・cyan・紫のResearchも、`ResearchDarkScene`／`RESEARCH_DARK_THEME` として
保持しています。明るいResearchと同じ内容・文字サイズ・余白で比較できます。

## レンダリング

リポジトリ直下で実行します。

```bash
pixi run render-research-showcase
pixi run render-research-dark-showcase
pixi run render-education-showcase
pixi run render-theme-stills

# 編集中は低画質でプレビューできる
pixi run manim -- -ql projects/showcase/theme_showcase.py ResearchThemeShowcase
pixi run manim -- -ql projects/showcase/theme_showcase.py ResearchDarkThemeShowcase
pixi run manim -- -ql projects/showcase/theme_showcase.py EducationThemeShowcase
```

動画は各約17秒、1920×1080・30 fpsです。各画面を5秒間表示します。
静止画タスクは動画と同じ組み立て関数を使い、全9画面を出力します。
`-s` を動画Sceneに直接渡した場合に得られるのは最後の画面だけです。

| 確認内容 | Research PNG | Education PNG |
| --- | --- | --- |
| 同一の日本語・英語、本文2行、箇条書き、強調、明朝体 | `ResearchTypography_ManimCE_v0.20.1.png` | `EducationTypography_ManimCE_v0.20.1.png` |
| 同一の数式、グラフ、図形、矢印、注記 | `ResearchVisuals_ManimCE_v0.20.1.png` | `EducationVisuals_ManimCE_v0.20.1.png` |
| 用途別：ニューラルネットワーク／分数 | `ResearchExample_ManimCE_v0.20.1.png` | `EducationExample_ManimCE_v0.20.1.png` |

Research Darkの3枚は、Researchのファイル名の先頭を `ResearchDark` に変えた
`ResearchDarkTypography_ManimCE_v0.20.1.png`、`ResearchDarkVisuals_ManimCE_v0.20.1.png`、
`ResearchDarkExample_ManimCE_v0.20.1.png` です。

- PNG：`projects/showcase/output/images/`
- MP4：`projects/showcase/output/videos/theme_showcase/1080p30/ResearchThemeShowcase.mp4`、`EducationThemeShowcase.mp4`
- Research Dark MP4：同じディレクトリの `ResearchDarkThemeShowcase.mp4`
- 生成物は従来どおりGit管理外です。

## 次に編集する場所

原則として [theme.py](../../src/manim_research/theme.py) の
`RESEARCH_THEME`／`RESEARCH_DARK_THEME`／`EDUCATION_THEME` を編集して比較できます。
Research Darkは `replace(RESEARCH_THEME, ...)` で配色を指定しています。
Research共通のフォント・文字サイズ・余白は `RESEARCH_THEME`、暗色版だけの配色は
`RESEARCH_DARK_THEME` を編集してください。暗色版だけの文字設定も `replace` で上書きできます。

| 用途・配色 | Scene | 設定 |
| --- | --- | --- |
| 研究発表・白背景 | `ResearchScene` | `RESEARCH_THEME` |
| 研究発表・紺背景（第1案） | `ResearchDarkScene` | `RESEARCH_DARK_THEME` |
| 教材・クリーム背景 | `EducationScene` | `EDUCATION_THEME` |

| 調整対象 | 設定 | 現在の方針 |
| --- | --- | --- |
| 背景・通常文字・注記 | `background` / `foreground` / `muted` | Researchは白・濃紺、Educationはクリーム・濃い茶系グレー |
| 強調・補助色 | `accent` / `secondary` | Researchは青・橙、Educationはオレンジ・青緑 |
| 図形の面・明るい強調 | `surface` / `accent_fill` | Researchは薄いグレー・淡い青、Educationは淡いアプリコット・ハニー色 |
| 意味を持つ色 | `success` / `warning` / `danger` | 確認・正解／ポイント・注意／誤りの候補 |
| フォント全体 | `sans_font` / `serif_font` | Notoのまま。将来ここから交換可能 |
| 役割ごとの文字 | `typography.title` / `subtitle` / `body` / `caption` / `keyword` | `TextStyle`で設定 |
| 文字の詳細 | `font` / `serif` / `font_size` / `weight` / `line_spacing` / `color` | Educationは大きく、本文もBold |
| 外周余白・項目間・節間 | `layout.edge_buff` / `row_buff` / `section_buff` | Manimの座標単位。Educationを広めに設定 |
| 画面の情報量・配置・図の大きさ | [theme_showcase.py](theme_showcase.py) の各`*_page()`、冒頭の定数 | 自動レイアウトを介さず通常のManimで記述 |
| 画面の表示時間 | `theme_showcase.py` の `PAGE_HOLD_SECONDS` | 初期値5秒 |

`layout` はヘルパーの自動配置設定ではありません。Scene側で明示的に使う値です。
特に図・グラフは比較しやすい共通座標を使っています。フォントの幅やサイズを大きく
変えた場合は、文章の改行と各ページの配置も確認してください。

`TextStyle.font=None` はテーマのsansフォントを継承し、`serif=True` ならserifフォントを
継承します。`font="別の日本語フォント"` はスタイルまたは呼び出し単位の指定です。
明示された `font` は `serif` に優先します。フォント自体のインストールは別途必要です。

`TextStyle.color=None` の場合、title/bodyは `foreground`、subtitle/captionは `muted`、
keywordは `accent` を使います。したがって通常はパレットの変更だけで全体に反映されます。
スタイルの `color` や呼び出し時の `color=` で個別に変更できます。

`accent_fill` は図形の塗りや装飾線用です。明るい色を使えるよう文字色の `accent` と
分けています。文字には `accent`、明るい塗りの上の文字には `foreground` を使います。

初期値はResearchがtitle/body/caption = 52/34/24、Educationが60/40/28です。
`line_spacing=0.55` はManimの指定で、基準線間隔が文字サイズの1.55倍になります。
Manimの自動値に戻す場合は `-1` を指定します。文字列中の `\n` で明示的に改行します。

## プロジェクト内だけで試す

共有テーマを直接変えず、`dataclasses.replace` で一部を変更できます。

```python
from dataclasses import replace

from manim import DOWN, LEFT, UP

from manim_research import EDUCATION_THEME, EducationScene


class MyLesson(EducationScene):
    theme = replace(
        EDUCATION_THEME,
        sans_font="Noto Sans JP",  # 将来ここを別フォントに交換
        typography=replace(
            EDUCATION_THEME.typography,
            body=replace(EDUCATION_THEME.typography.body, font_size=42, weight="NORMAL"),
            caption=replace(EDUCATION_THEME.typography.caption, serif=True),
        ),
        layout=replace(EDUCATION_THEME.layout, section_buff=0.65),
    )

    def construct(self):
        layout = self.theme.layout
        title = self.title_text("分数ってなに？").to_corner(UP + LEFT, buff=layout.edge_buff)
        # 通常のText引数もそのまま利用可能
        word = self.keyword_text("3分の1", color=self.theme.warning).next_to(
            title, DOWN, aligned_edge=LEFT, buff=layout.section_buff
        )
        note = self.caption_text("補足", font="Noto Serif JP").next_to(
            word, DOWN, aligned_edge=LEFT, buff=layout.section_buff
        )
        self.add(title, word, note)
```

優先順位は、呼び出し時の指定 → 役割のTextStyle → テーマのフォント・役割色です。
全体への `Text.set_default()` は使わないため、同じプロセスで3種類を生成できます。
数式は通常の `MathTex(..., color=self.theme.foreground, font_size=...)` で指定します。
Pangoのsans/serifとTeXの数式フォントは別設定です。

## レビューしてほしい点

1. Researchの本文・注記が、プロジェクターや縮小した動画でも読めるか。
2. Educationの本文Bold・文字サイズが適切か。中学生にも使いやすい印象か。
3. Researchの白系背景と青の落ち着き、Educationのクリーム背景と暖色の明るさが適切か。
4. 余白と1画面の情報量。本文や注記をさらに減らす／大きくする必要があるか。
5. 明朝体の用途。本文にも試すか、注記や引用だけにするか。

パレットは背景・surface上の文字色を4.5:1以上のコントラスト比でテストしています。
色だけで意味を伝えず、ラベル・点・矢印・面積も併用しています。投影時の見え方や
色の区別は、実際の視聴環境で確認してください。
