"""Twelve independent A4-landscape English tutoring sheets.

The layout intentionally follows ``tutor_english_a4.py`` and
``tutor_english_four_pages.py`` from the existing tutoring-material project.
Each class is an independent static Manim scene and can be rendered with ``-s``.

Suggested order:
1-2  connection-word vocabulary (reference / practice)
3-6  basic-verb vocabulary (reference / practice, two sets)
7    third-person singular -s
8    There is / There are
9    gerunds
10   if
11   that
12   when / because
"""

from __future__ import annotations

import html
import re

from manim import Line, MarkupText, Rectangle, Scene, Text, VGroup, WHITE, config


config.frame_width = 14.14
config.frame_height = 10.0
config.pixel_width = 3508
config.pixel_height = 2480
config.frame_rate = 1

NAVY = "#062F67"
INK = "#111827"
GRID = "#8B98AA"
PALE_GRAY = "#F7F9FC"
FONT = "Noto Sans JP"
LATIN_FONT = "DejaVu Sans"
LINE_SPACING = 0.35


def label(
    value: str,
    size: float,
    *,
    color: str = INK,
    weight: str = "NORMAL",
) -> MarkupText:
    """Create readable mixed Japanese/Latin text with explicit line spacing."""
    pieces: list[str] = []
    cursor = 0
    for match in re.finditer(r"[\x20-\x7e]+", value):
        pieces.append(html.escape(value[cursor : match.start()]))
        for token in re.split(r"( +)", match.group()):
            if not token:
                continue
            spacing = "180" if token.isspace() else "-100"
            pieces.append(
                f'<span font_family="{LATIN_FONT}" letter_spacing="{spacing}">'
                f"{html.escape(token)}</span>"
            )
        cursor = match.end()
    pieces.append(html.escape(value[cursor:]))

    return MarkupText(
        "".join(pieces),
        font=FONT,
        font_size=size,
        color=color,
        weight=weight,
        line_spacing=LINE_SPACING,
        disable_ligatures=True,
    )


def table(
    headers: list[str],
    rows: list[list[str]],
    widths: list[float],
    row_height: float,
    header_height: float,
    font_size: float,
) -> VGroup:
    """Create a simple navy-header table."""
    group = VGroup()
    total_width = sum(widths)
    total_height = header_height + row_height * len(rows)
    left = -total_width / 2
    top = total_height / 2

    x = left
    for heading, width in zip(headers, widths, strict=True):
        cell = Rectangle(
            width=width,
            height=header_height,
            stroke_color=WHITE,
            stroke_width=1.4,
            fill_color=NAVY,
            fill_opacity=1,
        ).move_to([x + width / 2, top - header_height / 2, 0])
        text = label(heading, font_size + 1, color=WHITE, weight="BOLD")
        text.move_to(cell)
        group.add(cell, text)
        x += width

    for row_index, values in enumerate(rows):
        y = top - header_height - row_height * (row_index + 0.5)
        x = left
        for value, width in zip(values, widths, strict=True):
            cell = Rectangle(
                width=width,
                height=row_height,
                stroke_color=GRID,
                stroke_width=0.8,
                fill_color=PALE_GRAY if row_index % 2 else WHITE,
                fill_opacity=1,
            ).move_to([x + width / 2, y, 0])
            text = label(value, font_size)
            if text.width > width - 0.14:
                text.scale_to_fit_width(width - 0.14)
            if text.height > row_height - 0.1:
                text.scale_to_fit_height(row_height - 0.1)
            text.move_to(cell)
            group.add(cell, text)
            x += width

    return group


class TutorPage(Scene):
    """Shared A4 landscape page furniture."""

    page_number = ""

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = WHITE

    def add_heading(self, title: str) -> None:
        heading = label(title, 44, color=NAVY, weight="BOLD")
        heading.move_to([0, 4.4, 0])
        self.add(heading)

    def add_page_number(self) -> None:
        page = label(self.page_number, 16, color=NAVY)
        page.move_to([6.45, -4.72, 0])
        self.add(page)

    def add_cell_lines(
        self,
        *,
        center_y: float,
        header_height: float,
        row_height: float,
        row_count: int,
        column_widths: list[float],
        writable_columns: list[int],
        line_ratio: float = 0.76,
        y_offset: float = -0.1,
    ) -> None:
        total_height = header_height + row_count * row_height
        top = center_y + total_height / 2
        left = -sum(column_widths) / 2
        column_centers: list[float] = []
        current_x = left

        for width in column_widths:
            column_centers.append(current_x + width / 2)
            current_x += width

        for row_index in range(row_count):
            y = top - header_height - row_height * (row_index + 0.5) + y_offset
            for column_index in writable_columns:
                width = column_widths[column_index]
                center_x = column_centers[column_index]
                half_length = width * line_ratio / 2
                self.add(
                    Line(
                        [center_x - half_length, y, 0],
                        [center_x + half_length, y, 0],
                        color=GRID,
                        stroke_width=1.4,
                    )
                )


TOTAL_PAGES = 12


def fitted_label(
    value: str,
    size: float,
    *,
    max_width: float | None = None,
    max_height: float | None = None,
    color: str = INK,
    weight: str = "NORMAL",
):
    """Create a label and shrink it only when it exceeds the given bounds."""
    text = label(value, size, color=color, weight=weight)
    if max_width is not None and text.width > max_width:
        text.scale_to_fit_width(max_width)
    if max_height is not None and text.height > max_height:
        text.scale_to_fit_height(max_height)
    return text


def add_panel(
    scene: TutorPage,
    *,
    center: tuple[float, float],
    width: float,
    height: float,
    title: str,
    body: str,
    title_size: float = 25,
    body_size: float = 21,
    title_height: float = 0.64,
    fill_color: str = WHITE,
) -> Rectangle:
    """Add a bordered explanation panel with a navy title band."""
    x, y = center
    panel = Rectangle(
        width=width,
        height=height,
        stroke_color=GRID,
        stroke_width=1.1,
        fill_color=fill_color,
        fill_opacity=1,
    ).move_to([x, y, 0])

    title_band = Rectangle(
        width=width,
        height=title_height,
        stroke_color=NAVY,
        stroke_width=0,
        fill_color=NAVY,
        fill_opacity=1,
    ).move_to([x, y + height / 2 - title_height / 2, 0])

    heading = fitted_label(
        title,
        title_size,
        max_width=width - 0.28,
        max_height=title_height - 0.12,
        color=WHITE,
        weight="BOLD",
    )
    heading.move_to(title_band)

    body_text = fitted_label(
        body,
        body_size,
        max_width=width - 0.38,
        max_height=height - title_height - 0.3,
    )
    body_text.move_to([x, y - title_height / 2 - 0.02, 0])

    scene.add(panel, title_band, heading, body_text)
    return panel


def add_callout(
    scene: TutorPage,
    *,
    center: tuple[float, float],
    width: float,
    height: float,
    text: str,
    font_size: float = 21,
) -> None:
    """Add a pale one-line or two-line emphasis box."""
    x, y = center
    box = Rectangle(
        width=width,
        height=height,
        stroke_color=NAVY,
        stroke_width=1.2,
        fill_color=PALE_GRAY,
        fill_opacity=1,
    ).move_to([x, y, 0])
    content = fitted_label(
        text,
        font_size,
        max_width=width - 0.32,
        max_height=height - 0.18,
        color=NAVY,
        weight="BOLD",
    )
    content.move_to(box)
    scene.add(box, content)


class TodayTutorPage(TutorPage):
    """Shared page-number handling for today's twelve-sheet packet."""

    page_index = 0

    def add_today_page_number(self) -> None:
        self.page_number = f"{self.page_index} / {TOTAL_PAGES}"
        self.add_page_number()


CONNECTION_WORDS = [
    ["原因", "because", "なぜなら／～なので", "I stayed home because it rained."],
    ["結果", "so", "だから／それで", "It rained, so I stayed home."],
    ["逆接", "but", "しかし／でも", "I was tired, but I studied."],
    ["逆接", "however", "しかしながら", "It was hard. However, I tried."],
    ["条件", "if", "もし～なら", "If it rains, I will stay home."],
    ["時間", "when", "～するとき", "Call me when you arrive."],
    ["時間", "before", "～する前に", "Wash your hands before you eat."],
    ["時間", "after", "～した後に", "I studied after I ate dinner."],
    ["時間", "while", "～している間", "I listened to music while I studied."],
    ["時間", "until", "～まで", "Wait here until I come back."],
    ["譲歩", "though", "～だけれども", "Though it was cold, we went out."],
    ["追加", "also", "～もまた", "She also likes music."],
    ["結果", "therefore", "それゆえ／したがって", "He practiced. Therefore, he improved."],
    ["内容", "that", "～ということ", "I think that he is kind."],
]


BASIC_VERBS_1 = [
    ["1", "食べる", "eat", "eat breakfast"],
    ["2", "飲む", "drink", "drink water"],
    ["3", "眠る", "sleep", "sleep well"],
    ["4", "勉強する", "study", "study English"],
    ["5", "読む", "read", "read a book"],
    ["6", "書く", "write", "write a letter"],
    ["7", "遊ぶ／競技する", "play", "play tennis"],
    ["8", "使う", "use", "use a computer"],
    ["9", "働く", "work", "work hard"],
    ["10", "住む", "live", "live in Tokyo"],
    ["11", "滞在する", "stay", "stay at home"],
    ["12", "持っている", "have", "have a bike"],
    ["13", "得る／～になる", "get", "get a present"],
    ["14", "作る", "make", "make dinner"],
    ["15", "取る／持っていく", "take", "take a picture"],
    ["16", "置く", "put", "put it here"],
    ["17", "開ける", "open", "open the door"],
    ["18", "閉める", "close", "close the window"],
    ["19", "始める", "start", "start the lesson"],
    ["20", "終える", "finish", "finish homework"],
]


BASIC_VERBS_2 = [
    ["1", "行く", "go", "go to school"],
    ["2", "来る", "come", "come here"],
    ["3", "去る／出発する", "leave", "leave home"],
    ["4", "到着する", "arrive", "arrive at school"],
    ["5", "訪れる", "visit", "visit Kyoto"],
    ["6", "知っている", "know", "know the answer"],
    ["7", "思う／考える", "think", "think about it"],
    ["8", "理解する", "understand", "understand English"],
    ["9", "好む", "like", "like music"],
    ["10", "欲しい／～したい", "want", "want a new bag"],
    ["11", "必要とする", "need", "need help"],
    ["12", "覚えている", "remember", "remember his name"],
    ["13", "忘れる", "forget", "forget the key"],
    ["14", "言う", "say", "say hello"],
    ["15", "人に伝える", "tell", "tell me the truth"],
    ["16", "たずねる／頼む", "ask", "ask a question"],
    ["17", "答える", "answer", "answer the question"],
    ["18", "与える", "give", "give me a book"],
    ["19", "見せる", "show", "show me the picture"],
    ["20", "助ける", "help", "help my mother"],
]


class ConnectionWordsReferenceA4(TodayTutorPage):
    """Connection-word vocabulary reference."""

    page_index = 1

    def construct(self) -> None:
        self.add_heading("接続詞・文をつなぐ語")

        widths = [1.35, 2.05, 3.15, 6.1]
        chart = table(
            ["関係", "英語", "意味", "短い例文"],
            CONNECTION_WORDS,
            widths,
            0.50,
            0.70,
            16,
        )
        chart.move_to([0, -0.32, 0])
        self.add(chart)
        self.add_today_page_number()


class ConnectionWordsPracticeA4(TodayTutorPage):
    """Connection-word vocabulary writing practice."""

    page_index = 2

    def construct(self) -> None:
        self.add_heading("接続詞・文をつなぐ語　練習")

        rows = [
            [str(index), relation, meaning, ""]
            for index, (relation, _word, meaning, _example) in enumerate(
                CONNECTION_WORDS,
                start=1,
            )
        ]
        widths = [0.85, 1.55, 4.2, 5.95]
        row_height = 0.50
        header_height = 0.70
        center_y = -0.32

        chart = table(
            ["番号", "関係", "意味", "英語"],
            rows,
            widths,
            row_height,
            header_height,
            17,
        )
        chart.move_to([0, center_y, 0])
        self.add(chart)
        self.add_cell_lines(
            center_y=center_y,
            header_height=header_height,
            row_height=row_height,
            row_count=len(rows),
            column_widths=widths,
            writable_columns=[3],
            line_ratio=0.82,
            y_offset=-0.07,
        )
        self.add_today_page_number()


class BasicVerbsReference1A4(TodayTutorPage):
    """Basic verbs: daily life and core actions."""

    page_index = 3

    def construct(self) -> None:
        self.add_heading("基本動詞①　日常・基本動作")
        widths = [0.8, 3.45, 2.4, 5.95]
        chart = table(
            ["番号", "意味", "英語", "よく使う形"],
            BASIC_VERBS_1,
            widths,
            0.365,
            0.70,
            16,
        )
        chart.move_to([0, -0.35, 0])
        self.add(chart)
        self.add_today_page_number()


class BasicVerbsPractice1A4(TodayTutorPage):
    """Writing practice for daily-life and core-action verbs."""

    page_index = 4

    def construct(self) -> None:
        self.add_heading("基本動詞①　練習")
        rows = [[number, meaning, "", ""] for number, meaning, _word, _chunk in BASIC_VERBS_1]
        widths = [0.8, 3.65, 3.45, 4.7]
        row_height = 0.365
        header_height = 0.70
        center_y = -0.35

        chart = table(
            ["番号", "意味", "英語", "もう一度書く"],
            rows,
            widths,
            row_height,
            header_height,
            16,
        )
        chart.move_to([0, center_y, 0])
        self.add(chart)
        self.add_cell_lines(
            center_y=center_y,
            header_height=header_height,
            row_height=row_height,
            row_count=len(rows),
            column_widths=widths,
            writable_columns=[2, 3],
            line_ratio=0.80,
            y_offset=-0.055,
        )
        self.add_today_page_number()


class BasicVerbsReference2A4(TodayTutorPage):
    """Basic verbs: movement, thought, and communication."""

    page_index = 5

    def construct(self) -> None:
        self.add_heading("基本動詞②　移動・考え・やり取り")
        widths = [0.8, 3.45, 2.4, 5.95]
        chart = table(
            ["番号", "意味", "英語", "よく使う形"],
            BASIC_VERBS_2,
            widths,
            0.365,
            0.70,
            16,
        )
        chart.move_to([0, -0.35, 0])
        self.add(chart)
        self.add_today_page_number()


class BasicVerbsPractice2A4(TodayTutorPage):
    """Writing practice for movement, thought, and communication verbs."""

    page_index = 6

    def construct(self) -> None:
        self.add_heading("基本動詞②　練習")
        rows = [[number, meaning, "", ""] for number, meaning, _word, _chunk in BASIC_VERBS_2]
        widths = [0.8, 3.65, 3.45, 4.7]
        row_height = 0.365
        header_height = 0.70
        center_y = -0.35

        chart = table(
            ["番号", "意味", "英語", "もう一度書く"],
            rows,
            widths,
            row_height,
            header_height,
            16,
        )
        chart.move_to([0, center_y, 0])
        self.add(chart)
        self.add_cell_lines(
            center_y=center_y,
            header_height=header_height,
            row_height=row_height,
            row_count=len(rows),
            column_widths=widths,
            writable_columns=[2, 3],
            line_ratio=0.80,
            y_offset=-0.055,
        )
        self.add_today_page_number()


class ThirdPersonSingularSA4(TodayTutorPage):
    """One-page explanation of third-person singular present forms."""

    page_index = 7

    def construct(self) -> None:
        self.add_heading("三人称単数の s")

        add_callout(
            self,
            center=(0, 3.35),
            width=12.8,
            height=0.78,
            text="現在形で、主語が he / she / it または『1人・1つ』なら、一般動詞の形を変える。",
            font_size=21,
        )

        rules = [
            ["ふつう", "動詞 + s", "play → plays\nread → reads"],
            ["語尾が s / sh / ch / x / o", "動詞 + es", "wash → washes\nwatch → watches\ngo → goes"],
            ["子音字 + y", "y を i にして es", "study → studies\ntry → tries"],
            ["特別", "have → has", "She has a dog."],
        ]
        rule_chart = table(
            ["動詞の形", "作り方", "例"],
            rules,
            [3.3, 3.6, 5.4],
            0.80,
            0.66,
            19,
        )
        rule_chart.move_to([0, 1.00, 0])
        self.add(rule_chart)

        add_panel(
            self,
            center=(-3.25, -2.36),
            width=6.15,
            height=2.45,
            title="文の中で比べる",
            body=(
                "I play tennis.　→　He plays tennis.\n"
                "They study English.　→　Ken studies English.\n"
                "I have a bike.　→　She has a bike."
            ),
            body_size=20,
        )
        add_panel(
            self,
            center=(3.25, -2.36),
            width=6.15,
            height=2.45,
            title="否定文・疑問文",
            body=(
                "He does not play tennis.\n"
                "Does he play tennis?\n\n"
                "does が s の役目を持つので、後ろは原形 play。"
            ),
            body_size=20,
        )

        self.add_today_page_number()


class ThereIsAreA4(TodayTutorPage):
    """One-page explanation of There is / There are."""

    page_index = 8

    def construct(self) -> None:
        self.add_heading("There is / There are")

        add_callout(
            self,
            center=(0, 3.35),
            width=12.8,
            height=0.78,
            text="『場所に、人・物がある／いる』と初めて伝える形。後ろの名詞が1つか複数かを見る。",
            font_size=21,
        )

        forms = [
            ["1人・1つ", "There is + 単数名詞", "There is a book on the desk."],
            ["2人・2つ以上", "There are + 複数名詞", "There are two books on the desk."],
            ["数えられない名詞", "There is + 名詞", "There is some water in the bottle."],
        ]
        form_chart = table(
            ["後ろの名詞", "形", "例文"],
            forms,
            [2.85, 4.0, 5.45],
            0.74,
            0.68,
            19,
        )
        form_chart.move_to([0, 1.49, 0])
        self.add(form_chart)

        add_panel(
            self,
            center=(-3.25, -1.28),
            width=6.15,
            height=2.25,
            title="否定文・疑問文",
            body=(
                "There isn't a park near here.\n"
                "There aren't any students in the room.\n"
                "Is there a station nearby?\n"
                "Are there any questions?"
            ),
            body_size=19,
        )
        add_panel(
            self,
            center=(3.25, -1.28),
            width=6.15,
            height=2.25,
            title="have との違い",
            body=(
                "There is：ある場所の存在を伝える\n"
                "There is a library in my town.\n\n"
                "have：人・物が所有している\n"
                "My town has a library."
            ),
            body_size=19,
        )

        add_callout(
            self,
            center=(0, -3.18),
            width=12.3,
            height=0.82,
            text="場所を表す語：in ～（～の中に） / on ～（～の上に） / under ～（～の下に） / near ～（～の近くに）",
            font_size=19,
        )
        self.add_today_page_number()


class GerundA4(TodayTutorPage):
    """One-page explanation of gerunds."""

    page_index = 9

    def construct(self) -> None:
        self.add_heading("動名詞：動詞 + ing")

        add_callout(
            self,
            center=(0, 3.35),
            width=12.8,
            height=0.78,
            text="動詞に -ing をつけて、名詞のように『～すること』を表す。",
            font_size=22,
        )

        uses = [
            ["主語になる", "Reading books is fun.", "本を読むことは楽しい。"],
            ["動詞の目的語になる", "I like playing soccer.", "私はサッカーをすることが好きだ。"],
            ["前置詞の後ろに置く", "Thank you for helping me.", "私を助けてくれてありがとう。"],
        ]
        use_chart = table(
            ["使う場所", "例文", "意味"],
            uses,
            [3.2, 5.1, 4.0],
            0.83,
            0.68,
            18,
        )
        use_chart.move_to([0, 1.34, 0])
        self.add(use_chart)

        add_panel(
            self,
            center=(-3.25, -1.45),
            width=6.15,
            height=2.35,
            title="-ing の作り方",
            body=(
                "ふつう：play → playing\n"
                "e を取る：make → making / use → using\n"
                "最後を重ねる：run → running / swim → swimming"
            ),
            body_size=19,
        )
        add_panel(
            self,
            center=(3.25, -1.45),
            width=6.15,
            height=2.35,
            title="よく後ろに -ing を置く動詞",
            body=(
                "enjoy：楽しむ　　finish：終える\n"
                "stop：やめる　　practice：練習する\n\n"
                "I enjoyed talking with you.\n"
                "She finished doing her homework."
            ),
            body_size=18,
        )

        add_callout(
            self,
            center=(0, -3.32),
            width=12.3,
            height=0.84,
            text="見分け方：I am reading. は進行形（読んでいる）／ Reading is fun. は動名詞（読むこと）",
            font_size=20,
        )
        self.add_today_page_number()


class IfConjunctionA4(TodayTutorPage):
    """Detailed one-page explanation of if."""

    page_index = 10

    def construct(self) -> None:
        self.add_heading("接続詞 if")

        add_panel(
            self,
            center=(0, 2.58),
            width=12.7,
            height=2.05,
            title="① 条件：もし～なら",
            body=(
                "If it rains, I will stay home.　もし雨が降れば、私は家にいます。\n"
                "I will stay home if it rains.　私は、もし雨が降れば家にいます。\n\n"
                "未来の条件でも if 節は現在形：if it rains（× if it will rain）"
            ),
            body_size=20,
        )

        add_panel(
            self,
            center=(0, 0.10),
            width=12.7,
            height=2.15,
            title="② ～かどうか：whether に近い if",
            body=(
                "I don't know if he is busy.　彼が忙しいかどうか分かりません。\n"
                "Please check if the door is closed.　ドアが閉まっているか確認してください。\n\n"
                "この if は条件ではないので、未来なら will を使える：\n"
                "I don't know if it will rain tomorrow."
            ),
            body_size=19,
        )

        add_panel(
            self,
            center=(-3.25, -2.55),
            width=6.15,
            height=1.72,
            title="語順",
            body=(
                "if の後ろはふつうの文：\n"
                "if + 主語 + 動詞\n"
                "if he is busy / if it rains"
            ),
            body_size=20,
        )
        add_panel(
            self,
            center=(3.25, -2.55),
            width=6.15,
            height=1.72,
            title="コンマ",
            body=(
                "If ～ が先ならコンマを置く。\n"
                "If it rains, I will stay home.\n"
                "後ろなら通常は不要。"
            ),
            body_size=19,
        )
        self.add_today_page_number()


class ThatConjunctionA4(TodayTutorPage):
    """Detailed one-page explanation of that."""

    page_index = 11

    def construct(self) -> None:
        self.add_heading("接続詞 that")

        add_callout(
            self,
            center=(0, 3.35),
            width=12.8,
            height=0.78,
            text="that + 完全な文 で、『～ということ』という内容のまとまりを作る。",
            font_size=22,
        )

        examples = [
            ["think", "I think that he is kind.", "私は、彼が親切だと思う。"],
            ["know", "I know that she likes music.", "私は、彼女が音楽を好きだと知っている。"],
            ["say", "He said that he was tired.", "彼は、疲れていると言った。"],
            ["hope", "I hope that you will be well.", "あなたが元気になることを願う。"],
        ]
        example_chart = table(
            ["前の動詞", "例文", "意味"],
            examples,
            [2.0, 5.65, 4.65],
            0.62,
            0.64,
            17,
        )
        example_chart.move_to([0, 1.34, 0])
        self.add(example_chart)

        add_panel(
            self,
            center=(-3.25, -1.45),
            width=6.15,
            height=2.35,
            title="that は省略できることが多い",
            body=(
                "会話では、動詞の目的語になる that を\n"
                "省略することが多い。\n\n"
                "I think (that) he is kind.\n"
                "I know (that) you are busy."
            ),
            body_size=19,
        )
        add_panel(
            self,
            center=(3.25, -1.45),
            width=6.15,
            height=2.35,
            title="that の後ろはふつうの語順",
            body=(
                "that + 主語 + 動詞\n"
                "I know that he is busy.\n\n"
                "疑問文の語順にはしない：\n"
                "× I know that is he busy."
            ),
            body_size=19,
        )

        add_callout(
            self,
            center=(0, -3.32),
            width=12.3,
            height=0.84,
            text="見分け方：that の直後に『主語＋動詞』が続けば、接続詞の that の可能性が高い。",
            font_size=20,
        )
        self.add_today_page_number()


class WhenBecauseConjunctionA4(TodayTutorPage):
    """Detailed one-page explanation of when and because."""

    page_index = 12

    def construct(self) -> None:
        self.add_heading("接続詞 when / because")

        add_panel(
            self,
            center=(0, 2.08),
            width=12.7,
            height=3.0,
            title="when：～するとき／いつ～か",
            body=(
                "【時を表す】When I get home, I do my homework.\n"
                "　　　　　　家に帰るとき、私は宿題をします。\n"
                "未来の時でも when 節は現在形：\n"
                "When he comes, I will call you.（× when he will come）\n\n"
                "【いつ～か】I don't know when he will come.\n"
                "　　　　　　彼がいつ来るのか分かりません。"
            ),
            body_size=19,
        )

        add_panel(
            self,
            center=(0, -1.43),
            width=12.7,
            height=3.35,
            title="because：なぜなら／～なので",
            body=(
                "I stayed home because it rained.\n"
                "雨が降ったので、私は家にいました。\n"
                "Because it rained, I stayed home.\n"
                "because 節を先に置くと、後ろにコンマを置く。\n\n"
                "because + 主語 + 動詞：because it rained\n"
                "because of + 名詞：because of the rain\n"
                "基本練習では because と so を同じ文で重ねない。"
            ),
            body_size=19,
        )

        self.add_today_page_number()


SCENE_NAMES = [
    "ConnectionWordsReferenceA4",
    "ConnectionWordsPracticeA4",
    "BasicVerbsReference1A4",
    "BasicVerbsPractice1A4",
    "BasicVerbsReference2A4",
    "BasicVerbsPractice2A4",
    "ThirdPersonSingularSA4",
    "ThereIsAreA4",
    "GerundA4",
    "IfConjunctionA4",
    "ThatConjunctionA4",
    "WhenBecauseConjunctionA4",
]


if __name__ == "__main__":
    print("Render these scenes in order:")
    print(" ".join(SCENE_NAMES))
