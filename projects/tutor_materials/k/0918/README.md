# 0918の家庭教師教材

教材ごとにPython・問題JSON・素材・成果物をまとめています。
既存のEducation ThemeとA4縦（2480×3508 px）を使います。

```text
0918/
├── README.md
├── test_worksheets.py
├── animal_counting_addition/
│   ├── animal_counting_addition.py
│   ├── json/
│   │   ├── animal_counting_01.json
│   │   └── animal_counting_02.json
│   └── output/images/
└── picture_hiragana_write/
    ├── picture_hiragana_write.py
    ├── json/picture_words_01.json
    ├── svg/
    │   ├── bear.svg
    │   ├── rabbit.svg
    │   └── turtle.svg
    └── output/images/
```

## 実行

リポジトリのルートから実行します。`scripts/manim.sh` がPythonファイルと同じ教材
ディレクトリの `output/` を出力先に設定します。Python側で出力先は上書きしません。
用紙・画素数は教材側でA4縦に設定するため、`-qh` でも横長の1080pにはなりません。

```bash
pixi run manim -- -s -qh \
  projects/tutor_materials/k/0918/picture_hiragana_write/picture_hiragana_write.py \
  PictureHiraganaWriteWorksheet

pixi run manim -- -s -qh \
  projects/tutor_materials/k/0918/animal_counting_addition/animal_counting_addition.py \
  AnimalCountingAdditionWorksheet
```

## ひらがな教材を増やす

1. `picture_hiragana_write/json/picture_words_01.json` を複製し、
   たとえば `picture_words_02.json` として保存します。
2. `title`・`subtitle` と、3問ぶんの `icon`・`answer` を変更します。
3. Python冒頭の `CONTENT_FILE_NAME` を新しいJSON名にして、上のコマンドを実行します。

```json
{
  "title": "えをみて かいてみよう",
  "subtitle": "えの なまえを、ひらがなで かいてみよう！",
  "problems": [
    {"icon": "bear.svg", "answer": "くま"},
    {"icon": "rabbit.svg", "answer": "うさぎ"},
    {"icon": "turtle.svg", "answer": "かめ"}
  ]
}
```

`answer` の文字数だけ空欄を作り、答えそのものは印刷しません。マスには縦横の破線が
入ります。長い答えは、マス数を保ったまま枠の横幅に収まるよう縮小します。
任意項目 `bottom_note` で下部の補足文を指定できます。省略・空文字なら表示しません。

### SVGを追加する

`picture_hiragana_write/svg/` に新しいSVG（例：`apple.svg`）を置き、JSONの
`icon` にそのファイル名を書きます。Pythonへの動物名登録は不要です。
SVGの色と縦横比を保ち、`ICON_MAX_WIDTH`・`ICON_MAX_HEIGHT` の両方に収めます。
同梱の3点は既存教材を参考に、このプロジェクト用に作成したオリジナルSVGです。

文字サイズ・余白・絵の大きさ・マスのサイズや破線の濃さは、Python冒頭の
日本語コメント付き定数で調整できます。全問題の上下位置は `PROBLEMS_CENTER_Y`、
絵とマスの位置は `ICON_Y_OFFSET`・`WRITE_AREA_Y_OFFSET` です。

## 数かぞえ教材を切り替える

`animal_counting_addition/json/` のJSONを編集・複製し、Python冒頭の
`CONTENT_FILE_NAME` を変更します。既存設定を維持し、初期値は `animal_counting_02.json`
です。問題は4問、動物は従来どおり `rabbit`・`bear`・`chick` です。

1プレートは0〜6体。1〜3体は1段、4体は2＋2、5体は3＋2、6体は3＋3で中央揃えに
配置します。7体以上はエラーです。0体の場合は従来どおり「0」を表示します。

## 動作確認

```bash
pixi run bash scripts/with_tex.sh python -m pytest \
  projects/tutor_materials/k/0918/test_worksheets.py
```

JSONの入力エラー、存在しないSVGのファイル名表示、任意のSVG追加、答えとマス数、
A4内への配置、数かぞえの1〜6体の配置と7体以上の拒否を確認します。
見た目を変更したときは、上記レンダリングコマンドで出力PNGも確認してください。
