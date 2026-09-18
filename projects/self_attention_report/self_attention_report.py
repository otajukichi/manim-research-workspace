"""Figures for the self-attention course report."""

import math

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arc,
    Arrow,
    DashedLine,
    Dot,
    Line,
    ManimColor,
    MathTex,
    Matrix,
    Polygon,
    RoundedRectangle,
    VGroup,
    interpolate_color,
)

from bd_adv_manim import LightScene

TOKENS = ("少年", "が", "リンゴ", "を", "食べた", "それ", "は", "赤かった")

TOKEN_VECTORS = (
    ("0.8", "0.1", "-0.4", "0.2", "0.7", "-0.1", "0.3", "0.6"),
    ("-0.2", "0.5", "0.9", "-0.3", "0.1", "0.8", "-0.6", "0.4"),
    ("0.6", "-0.7", "0.2", "0.5", "-0.4", "0.3", "0.1", "0.9"),
    ("0.1", "0.4", "-0.5", "0.8", "0.6", "-0.2", "0.7", "-0.3"),
    ("-0.5", "0.2", "0.3", "-0.6", "0.9", "0.5", "-0.4", "0.1"),
)

ATTENTION_SCORES = (
    (1.6, 0.5, -0.3, -0.4, 1.3, -0.5, -0.2, -0.4),
    (1.4, 0.7, -0.2, -0.3, 1.1, -0.4, 0.1, -0.5),
    (-0.1, -0.2, 1.7, 0.8, 1.5, 0.9, -0.3, 1.1),
    (-0.3, -0.1, 1.5, 0.6, 1.1, 0.2, -0.2, 0.0),
    (1.5, 0.3, 1.8, 0.7, 1.4, -0.1, -0.3, 0.1),
    (-0.4, -0.3, 2.4, 0.1, 0.6, 0.9, 0.4, 1.4),
    (-0.2, 0.1, 0.4, -0.1, 0.2, 1.3, 0.6, 1.1),
    (-0.3, -0.4, 2.2, 0.2, 0.5, 1.8, 0.7, 1.3),
)

COLUMN_FILL = ManimColor("#EAF3FA")
CONNECTOR_COLOR = ManimColor("#8BAFC7")
PROJECTION_FILL = ManimColor("#CFE4F2")
QUERY_COLOR = ManimColor("#0369A1")
KEY_COLOR = ManimColor("#BE185D")
VALUE_COLOR = ManimColor("#0F766E")
QUERY_CARD_FILL = ManimColor("#F1F7FB")
KEY_CARD_FILL = ManimColor("#FDF2F8")
VALUE_CARD_FILL = ManimColor("#F0FDFA")
INPUT_CARD_FILL = ManimColor("#F6F8FB")
SCORE_LOW_FILL = ManimColor("#F8FAFC")
SCORE_HIGH_FILL = ManimColor("#A9CFE3")


class TokensToVectorsFigure(LightScene):
    """Eight sentence tokens represented as the columns of one matrix."""

    def construct(self) -> None:
        matrix = Matrix(
            TOKEN_VECTORS,
            h_buff=1.45,
            v_buff=0.72,
            bracket_h_buff=0.28,
            bracket_v_buff=0.28,
            element_to_mobject_config={
                "font_size": 34,
                "color": self.theme.foreground,
            },
            bracket_config={
                "color": self.theme.foreground,
                "stroke_width": 2.5,
            },
        )
        matrix.move_to(DOWN * 0.55)

        columns = matrix.get_columns()
        column_bands = VGroup()
        connectors = VGroup()
        labels = VGroup()

        for token, column in zip(TOKENS, columns, strict=True):
            band = RoundedRectangle(
                width=column.width + 0.52,
                height=column.height + 0.46,
                corner_radius=0.12,
                stroke_width=0,
                fill_color=COLUMN_FILL,
                fill_opacity=0.72,
            ).move_to(column)

            label = self.jp_text(
                token,
                font_size=31,
                color=self.theme.foreground,
                weight="MEDIUM",
            )
            label.move_to(
                [
                    column.get_center()[0],
                    matrix.get_top()[1] + 0.95,
                    0,
                ]
            )

            connector = Line(
                start=label.get_bottom() + DOWN * 0.08,
                end=band.get_top() + DOWN * 0.02,
                color=CONNECTOR_COLOR,
                stroke_width=2.2,
            )

            column_bands.add(band)
            connectors.add(connector)
            labels.add(label)

        self.add(column_bands, connectors, matrix, labels)


class InnerProductProjectionFigure(LightScene):
    """The inner product visualized as a response along a question direction."""

    def construct(self) -> None:
        origin = [-4.7, -1.65, 0]
        question_end = [4.55, -1.65, 0]
        projection_end = [1.65, -1.65, 0]
        element_end = [1.65, 2.35, 0]

        projection_area = Polygon(
            origin,
            projection_end,
            element_end,
            stroke_width=0,
            fill_color=COLUMN_FILL,
            fill_opacity=0.52,
        )
        projection_highlight = Line(
            origin,
            projection_end,
            color=PROJECTION_FILL,
            stroke_width=18,
        )

        question_vector = Arrow(
            origin,
            question_end,
            buff=0,
            color=self.theme.accent,
            stroke_width=5.5,
            max_tip_length_to_length_ratio=0.055,
        )
        element_vector = Arrow(
            origin,
            element_end,
            buff=0,
            color=self.theme.foreground,
            stroke_width=5.5,
            max_tip_length_to_length_ratio=0.07,
        )
        perpendicular = DashedLine(
            element_end,
            projection_end,
            color=CONNECTOR_COLOR,
            stroke_width=2.7,
            dash_length=0.15,
            dashed_ratio=0.56,
        )

        right_angle_size = 0.27
        right_angle = VGroup(
            Line(
                [projection_end[0] - right_angle_size, projection_end[1], 0],
                [
                    projection_end[0] - right_angle_size,
                    projection_end[1] + right_angle_size,
                    0,
                ],
                color=CONNECTOR_COLOR,
                stroke_width=2.4,
            ),
            Line(
                [
                    projection_end[0] - right_angle_size,
                    projection_end[1] + right_angle_size,
                    0,
                ],
                [
                    projection_end[0],
                    projection_end[1] + right_angle_size,
                    0,
                ],
                color=CONNECTOR_COLOR,
                stroke_width=2.4,
            ),
        )

        vector_angle = math.atan2(
            element_end[1] - origin[1],
            element_end[0] - origin[0],
        )
        angle_arc = Arc(
            radius=0.9,
            start_angle=0,
            angle=vector_angle,
            arc_center=origin,
            color=self.theme.muted,
            stroke_width=2.4,
        )
        origin_dot = Dot(origin, radius=0.065, color=self.theme.foreground)

        question_word = self.jp_text(
            "質問",
            font_size=30,
            color=self.theme.foreground,
            weight="MEDIUM",
        )
        question_symbol = MathTex(
            r"\hat{\boldsymbol q}",
            font_size=38,
            color=self.theme.accent,
        )
        question_label = VGroup(question_word, question_symbol).arrange(
            RIGHT,
            buff=0.16,
        )
        question_label.next_to(question_vector.get_end(), UP + LEFT, buff=0.22)

        element_word = self.jp_text(
            "要素",
            font_size=30,
            color=self.theme.foreground,
            weight="MEDIUM",
        )
        element_symbol = MathTex(
            r"\boldsymbol x",
            font_size=38,
            color=self.theme.foreground,
        )
        element_label = VGroup(element_word, element_symbol).arrange(
            RIGHT,
            buff=0.16,
        )
        element_label.next_to(element_vector.get_end(), UP + RIGHT, buff=0.2)

        measure_y = -2.55
        measure_line = Line(
            [origin[0], measure_y, 0],
            [projection_end[0], measure_y, 0],
            color=self.theme.accent,
            stroke_width=3,
        )
        measure_ticks = VGroup(
            Line(
                [origin[0], measure_y - 0.14, 0],
                [origin[0], measure_y + 0.14, 0],
                color=self.theme.accent,
                stroke_width=3,
            ),
            Line(
                [projection_end[0], measure_y - 0.14, 0],
                [projection_end[0], measure_y + 0.14, 0],
                color=self.theme.accent,
                stroke_width=3,
            ),
        )

        match_word = self.jp_text(
            "一致度",
            font_size=31,
            color=self.theme.foreground,
            weight="MEDIUM",
        )
        match_expression = MathTex(
            r"= \boldsymbol x \cdot \hat{\boldsymbol q}",
            font_size=39,
            color=self.theme.foreground,
        )
        match_label = VGroup(match_word, match_expression).arrange(
            RIGHT,
            buff=0.2,
        )
        match_label.next_to(measure_line, DOWN, buff=0.2)

        self.add(
            projection_area,
            projection_highlight,
            perpendicular,
            right_angle,
            question_vector,
            element_vector,
            angle_arc,
            origin_dot,
            measure_line,
            measure_ticks,
            question_label,
            element_label,
            match_label,
        )


class AllPairwiseInnerProductsFigure(LightScene):
    """A matrix product collecting every element-question inner product."""

    def construct(self) -> None:
        element_rows = (
            (r"\boldsymbol{x}_1^{\mathsf T}",),
            (r"\boldsymbol{x}_2^{\mathsf T}",),
            (r"\boldsymbol{x}_3^{\mathsf T}",),
        )
        question_columns = (
            (
                r"\boldsymbol{q}_1",
                r"\boldsymbol{q}_2",
                r"\boldsymbol{q}_3",
            ),
        )
        inner_products = tuple(
            tuple(
                rf"\boldsymbol{{x}}_{row} \mathbin{{\cdot}} "
                rf"\boldsymbol{{q}}_{column}"
                for column in range(1, 4)
            )
            for row in range(1, 4)
        )

        element_matrix = Matrix(
            element_rows,
            h_buff=1.3,
            v_buff=0.92,
            bracket_h_buff=0.25,
            bracket_v_buff=0.25,
            element_to_mobject_config={
                "font_size": 34,
                "color": self.theme.foreground,
            },
            bracket_config={
                "color": self.theme.foreground,
                "stroke_width": 2.5,
            },
        )
        question_matrix = Matrix(
            question_columns,
            h_buff=1.35,
            v_buff=0.92,
            bracket_h_buff=0.25,
            bracket_v_buff=0.25,
            element_to_mobject_config={
                "font_size": 34,
                "color": self.theme.accent,
            },
            bracket_config={
                "color": self.theme.foreground,
                "stroke_width": 2.5,
            },
        )
        product_matrix = Matrix(
            inner_products,
            h_buff=1.8,
            v_buff=0.92,
            bracket_h_buff=0.25,
            bracket_v_buff=0.25,
            element_to_mobject_config={
                "font_size": 30,
                "color": self.theme.foreground,
            },
            bracket_config={
                "color": self.theme.foreground,
                "stroke_width": 2.5,
            },
        )

        multiplication = MathTex(
            r"\times",
            font_size=45,
            color=self.theme.foreground,
        )
        equality = MathTex(
            r"=",
            font_size=45,
            color=self.theme.foreground,
        )
        equation = VGroup(
            element_matrix,
            multiplication,
            question_matrix,
            equality,
            product_matrix,
        ).arrange(RIGHT, buff=0.34)
        equation.scale_to_fit_width(12.65)
        equation.move_to(DOWN * 0.18)

        selected_element = element_matrix.get_rows()[1]
        selected_question = question_matrix.get_columns()[2]
        selected_product = product_matrix.get_rows()[1][2]

        element_highlight = RoundedRectangle(
            width=selected_element.width + 0.48,
            height=selected_element.height + 0.3,
            corner_radius=0.1,
            stroke_width=0,
            fill_color=COLUMN_FILL,
            fill_opacity=0.82,
        ).move_to(selected_element)
        question_highlight = RoundedRectangle(
            width=selected_question.width + 0.4,
            height=selected_question.height + 0.3,
            corner_radius=0.1,
            stroke_width=0,
            fill_color=COLUMN_FILL,
            fill_opacity=0.82,
        ).move_to(selected_question)
        product_highlight = RoundedRectangle(
            width=selected_product.width + 0.38,
            height=selected_product.height + 0.3,
            corner_radius=0.1,
            stroke_color=CONNECTOR_COLOR,
            stroke_width=2,
            fill_color=PROJECTION_FILL,
            fill_opacity=0.9,
        ).move_to(selected_product)

        label_y = equation.get_top()[1] + 0.72
        element_label = self.jp_text(
            "要素ベクトル",
            font_size=29,
            color=self.theme.foreground,
            weight="MEDIUM",
        )
        element_label.move_to([element_matrix.get_center()[0], label_y, 0])

        question_label = self.jp_text(
            "質問ベクトル",
            font_size=29,
            color=self.theme.foreground,
            weight="MEDIUM",
        )
        question_label.move_to([question_matrix.get_center()[0], label_y, 0])

        self.add(
            element_highlight,
            question_highlight,
            product_highlight,
            equation,
            element_label,
            question_label,
        )


class SelfAttentionParametersFigure(LightScene):
    """The three learned transformations held by self-attention."""

    def construct(self) -> None:
        card_specs = (
            (
                r"\boldsymbol W_Q",
                (
                    ("0.8", "-0.2", "0.4"),
                    ("0.1", "0.7", "-0.5"),
                    ("-0.3", "0.2", "0.6"),
                ),
                "問いかける観点",
                QUERY_COLOR,
                QUERY_CARD_FILL,
            ),
            (
                r"\boldsymbol W_K",
                (
                    ("0.3", "0.7", "-0.1"),
                    ("-0.6", "0.2", "0.8"),
                    ("0.5", "-0.4", "0.1"),
                ),
                "問いに応える観点",
                KEY_COLOR,
                KEY_CARD_FILL,
            ),
            (
                r"\boldsymbol W_V",
                (
                    ("-0.2", "0.6", "0.5"),
                    ("0.9", "-0.3", "0.2"),
                    ("0.4", "0.1", "-0.7"),
                ),
                "伝える情報",
                VALUE_COLOR,
                VALUE_CARD_FILL,
            ),
        )

        cards = VGroup()
        for symbol_tex, values, role_text, accent, fill in card_specs:
            card = RoundedRectangle(
                width=3.65,
                height=4.45,
                corner_radius=0.22,
                stroke_color=accent,
                stroke_width=2,
                stroke_opacity=0.4,
                fill_color=fill,
                fill_opacity=0.88,
            )

            symbol = MathTex(
                symbol_tex,
                font_size=53,
                color=accent,
            )
            symbol.move_to(card.get_top() + DOWN * 0.64)

            matrix = Matrix(
                values,
                h_buff=0.78,
                v_buff=0.6,
                bracket_h_buff=0.2,
                bracket_v_buff=0.2,
                element_to_mobject_config={
                    "font_size": 24,
                    "color": self.theme.foreground,
                },
                bracket_config={
                    "color": accent,
                    "stroke_width": 2.3,
                },
            )
            matrix.move_to(card.get_center() + UP * 0.05)

            divider = Line(
                card.get_left() + RIGHT * 0.42,
                card.get_right() + LEFT * 0.42,
                color=accent,
                stroke_width=1.6,
                stroke_opacity=0.32,
            )
            divider.move_to([card.get_center()[0], card.get_bottom()[1] + 0.92, 0])

            role = self.jp_text(
                role_text,
                font_size=27,
                color=self.theme.foreground,
                weight="MEDIUM",
            )
            role.move_to(card.get_bottom() + UP * 0.52)

            cards.add(VGroup(card, symbol, matrix, divider, role))

        cards.arrange(RIGHT, buff=0.62)
        cards.move_to(DOWN * 0.08)
        self.add(cards)


class CreateQueryKeyValueFigure(LightScene):
    """One input matrix transformed into Query, Key, and Value."""

    def construct(self) -> None:
        input_name = MathTex(
            r"\boldsymbol X =",
            font_size=46,
            color=self.theme.foreground,
        )
        input_matrix = Matrix(
            (
                (
                    r"\boldsymbol{x}_1",
                    r"\boldsymbol{x}_2",
                    r"\boldsymbol{x}_3",
                ),
            ),
            h_buff=0.92,
            v_buff=0.7,
            bracket_h_buff=0.22,
            bracket_v_buff=0.22,
            element_to_mobject_config={
                "font_size": 34,
                "color": self.theme.foreground,
            },
            bracket_config={
                "color": self.theme.foreground,
                "stroke_width": 2.4,
            },
        )
        input_content = VGroup(input_name, input_matrix).arrange(RIGHT, buff=0.2)
        input_card = RoundedRectangle(
            width=input_content.width + 0.7,
            height=input_content.height + 0.65,
            corner_radius=0.2,
            stroke_color=self.theme.muted,
            stroke_width=2,
            stroke_opacity=0.28,
            fill_color=INPUT_CARD_FILL,
            fill_opacity=0.9,
        ).move_to(input_content)
        input_group = VGroup(input_card, input_content)
        input_group.move_to(LEFT * 4.45)

        formula_specs = (
            (
                r"\boldsymbol Q",
                r"\boldsymbol W_Q",
                QUERY_COLOR,
                QUERY_CARD_FILL,
            ),
            (
                r"\boldsymbol K",
                r"\boldsymbol W_K",
                KEY_COLOR,
                KEY_CARD_FILL,
            ),
            (
                r"\boldsymbol V",
                r"\boldsymbol W_V",
                VALUE_COLOR,
                VALUE_CARD_FILL,
            ),
        )

        formula_cards = VGroup()
        for output_tex, weight_tex, accent, fill in formula_specs:
            output_symbol = MathTex(
                output_tex,
                font_size=49,
                color=accent,
            )
            equality = MathTex(
                r"=",
                font_size=43,
                color=self.theme.foreground,
            )
            weight_symbol = MathTex(
                weight_tex,
                font_size=49,
                color=accent,
            )
            multiplication = MathTex(
                r"\times",
                font_size=41,
                color=self.theme.muted,
            )
            shared_input = MathTex(
                r"\boldsymbol X",
                font_size=49,
                color=self.theme.foreground,
            )
            formula = VGroup(
                output_symbol,
                equality,
                weight_symbol,
                multiplication,
                shared_input,
            ).arrange(RIGHT, buff=0.24)

            card = RoundedRectangle(
                width=5.25,
                height=1.45,
                corner_radius=0.18,
                stroke_color=accent,
                stroke_width=2,
                stroke_opacity=0.4,
                fill_color=fill,
                fill_opacity=0.9,
            )
            formula.move_to(card)
            formula_cards.add(VGroup(card, formula))

        formula_cards.arrange(DOWN, buff=0.55)
        formula_cards.move_to(RIGHT * 2.25)

        branch_offsets = (0.42, 0.0, -0.42)
        branch_arrows = VGroup()
        for formula_card, start_offset, accent in zip(
            formula_cards,
            branch_offsets,
            (QUERY_COLOR, KEY_COLOR, VALUE_COLOR),
            strict=True,
        ):
            branch_arrows.add(
                Arrow(
                    input_card.get_right() + UP * start_offset,
                    formula_card[0].get_left(),
                    buff=0.14,
                    color=accent,
                    stroke_width=3.2,
                    stroke_opacity=0.76,
                    max_tip_length_to_length_ratio=0.12,
                )
            )

        self.add(input_group, branch_arrows, formula_cards)


class QueryKeyScoreTableFigure(LightScene):
    """Raw Query-Key dot products aligned with their sentence tokens."""

    def construct(self) -> None:
        cell_width = 1.24
        cell_height = 0.62
        table_width = cell_width * len(TOKENS)
        table_height = cell_height * len(TOKENS)
        table_center = [0.55, -0.72, 0]
        table_left = table_center[0] - table_width / 2
        table_right = table_center[0] + table_width / 2
        table_top = table_center[1] + table_height / 2
        table_bottom = table_center[1] - table_height / 2

        minimum_score = min(min(row) for row in ATTENTION_SCORES)
        maximum_score = max(max(row) for row in ATTENTION_SCORES)

        cells = VGroup()
        values = VGroup()
        for row_index, row in enumerate(ATTENTION_SCORES):
            for column_index, score in enumerate(row):
                normalized_score = (score - minimum_score) / (maximum_score - minimum_score)
                fill_color = interpolate_color(
                    SCORE_LOW_FILL,
                    SCORE_HIGH_FILL,
                    normalized_score,
                )
                cell_center = [
                    table_left + (column_index + 0.5) * cell_width,
                    table_top - (row_index + 0.5) * cell_height,
                    0,
                ]
                cell = RoundedRectangle(
                    width=cell_width - 0.055,
                    height=cell_height - 0.055,
                    corner_radius=0.055,
                    stroke_width=0,
                    fill_color=fill_color,
                    fill_opacity=1,
                ).move_to(cell_center)
                value = self.jp_text(
                    f"{score:.1f}",
                    font_size=21,
                    color=self.theme.foreground,
                )
                value.move_to(cell_center)
                cells.add(cell)
                values.add(value)

        bracket_depth = 0.2
        bracket_offset = 0.14
        left_bracket_x = table_left - bracket_offset
        right_bracket_x = table_right + bracket_offset
        brackets = VGroup(
            Line(
                [left_bracket_x, table_bottom - 0.08, 0],
                [left_bracket_x, table_top + 0.08, 0],
                color=self.theme.foreground,
                stroke_width=2.6,
            ),
            Line(
                [left_bracket_x, table_top + 0.08, 0],
                [left_bracket_x + bracket_depth, table_top + 0.08, 0],
                color=self.theme.foreground,
                stroke_width=2.6,
            ),
            Line(
                [left_bracket_x, table_bottom - 0.08, 0],
                [left_bracket_x + bracket_depth, table_bottom - 0.08, 0],
                color=self.theme.foreground,
                stroke_width=2.6,
            ),
            Line(
                [right_bracket_x, table_bottom - 0.08, 0],
                [right_bracket_x, table_top + 0.08, 0],
                color=self.theme.foreground,
                stroke_width=2.6,
            ),
            Line(
                [right_bracket_x - bracket_depth, table_top + 0.08, 0],
                [right_bracket_x, table_top + 0.08, 0],
                color=self.theme.foreground,
                stroke_width=2.6,
            ),
            Line(
                [right_bracket_x - bracket_depth, table_bottom - 0.08, 0],
                [right_bracket_x, table_bottom - 0.08, 0],
                color=self.theme.foreground,
                stroke_width=2.6,
            ),
        )

        column_labels = VGroup()
        column_connectors = VGroup()
        column_label_y = table_top + 0.57
        for column_index, token in enumerate(TOKENS):
            column_center_x = table_left + (column_index + 0.5) * cell_width
            label = self.jp_text(
                token,
                font_size=25,
                color=self.theme.foreground,
                weight="MEDIUM",
            )
            label.move_to([column_center_x, column_label_y, 0])
            connector = Line(
                label.get_bottom() + DOWN * 0.06,
                [column_center_x, table_top + 0.04, 0],
                color=KEY_COLOR,
                stroke_width=2,
                stroke_opacity=0.48,
            )
            column_labels.add(label)
            column_connectors.add(connector)

        row_labels = VGroup()
        row_connectors = VGroup()
        row_label_x = table_left - 1.12
        for row_index, token in enumerate(TOKENS):
            row_center_y = table_top - (row_index + 0.5) * cell_height
            label = self.jp_text(
                token,
                font_size=25,
                color=self.theme.foreground,
                weight="MEDIUM",
            )
            label.move_to([row_label_x, row_center_y, 0])
            connector = Line(
                label.get_right() + RIGHT * 0.06,
                [left_bracket_x - 0.03, row_center_y, 0],
                color=QUERY_COLOR,
                stroke_width=2,
                stroke_opacity=0.48,
            )
            row_labels.add(label)
            row_connectors.add(connector)

        role_label_y = table_top + 1.28
        query_label = self.jp_text(
            "Query",
            font_size=28,
            color=QUERY_COLOR,
            weight="MEDIUM",
        )
        query_label.rotate(math.pi / 2)
        query_label.move_to([table_left - 2.2, table_center[1], 0])
        key_label = self.jp_text(
            "Key",
            font_size=28,
            color=KEY_COLOR,
            weight="MEDIUM",
        )
        key_label.move_to([table_center[0], role_label_y, 0])

        query_term = MathTex(
            r"\boldsymbol Q^{\mathsf T}",
            font_size=31,
            color=QUERY_COLOR,
        )
        key_term = MathTex(
            r"\boldsymbol K",
            font_size=31,
            color=KEY_COLOR,
        )
        operation_label = VGroup(query_term, key_term).arrange(RIGHT, buff=0.08)
        operation_label.move_to([row_label_x, column_label_y, 0])

        self.add(
            cells,
            column_connectors,
            row_connectors,
            brackets,
            values,
            column_labels,
            row_labels,
            query_label,
            key_label,
            operation_label,
        )


class SoftmaxReferenceRatiosFigure(LightScene):
    """One Query row converted from raw scores to reference ratios."""

    def construct(self) -> None:
        query_token = "それ"
        query_index = TOKENS.index(query_token)
        raw_scores = ATTENTION_SCORES[query_index]
        stabilized_exponentials = tuple(math.exp(score - max(raw_scores)) for score in raw_scores)
        exponential_sum = sum(stabilized_exponentials)
        reference_ratios = tuple(value / exponential_sum for value in stabilized_exponentials)

        cell_width = 1.13
        table_width = cell_width * len(TOKENS)
        table_center_x = 0.35
        table_left = table_center_x - table_width / 2
        table_right = table_center_x + table_width / 2
        raw_row_y = 0.95
        ratio_row_y = -1.25
        raw_cell_height = 0.72
        ratio_cell_height = 0.86

        global_minimum_score = min(min(row) for row in ATTENTION_SCORES)
        global_maximum_score = max(max(row) for row in ATTENTION_SCORES)
        maximum_ratio = max(reference_ratios)

        raw_cells = VGroup()
        raw_values = VGroup()
        ratio_cells = VGroup()
        ratio_values = VGroup()
        for column_index, (score, ratio) in enumerate(
            zip(raw_scores, reference_ratios, strict=True)
        ):
            column_center_x = table_left + (column_index + 0.5) * cell_width

            normalized_score = (score - global_minimum_score) / (
                global_maximum_score - global_minimum_score
            )
            raw_fill = interpolate_color(
                SCORE_LOW_FILL,
                SCORE_HIGH_FILL,
                normalized_score,
            )
            raw_cell = RoundedRectangle(
                width=cell_width - 0.055,
                height=raw_cell_height,
                corner_radius=0.065,
                stroke_width=0,
                fill_color=raw_fill,
                fill_opacity=1,
            ).move_to([column_center_x, raw_row_y, 0])
            raw_value = self.jp_text(
                f"{score:.1f}",
                font_size=22,
                color=self.theme.foreground,
            )
            raw_value.move_to(raw_cell)

            ratio_fill = interpolate_color(
                QUERY_CARD_FILL,
                SCORE_HIGH_FILL,
                ratio / maximum_ratio,
            )
            ratio_cell = RoundedRectangle(
                width=cell_width - 0.055,
                height=ratio_cell_height,
                corner_radius=0.065,
                stroke_width=0,
                fill_color=ratio_fill,
                fill_opacity=1,
            ).move_to([column_center_x, ratio_row_y, 0])
            ratio_value = self.jp_text(
                f"{ratio:.2f}",
                font_size=22,
                color=self.theme.foreground,
                weight="MEDIUM",
            )
            ratio_value.move_to(ratio_cell)

            raw_cells.add(raw_cell)
            raw_values.add(raw_value)
            ratio_cells.add(ratio_cell)
            ratio_values.add(ratio_value)

        token_labels = VGroup()
        token_connectors = VGroup()
        token_label_y = 2.55
        for column_index, token in enumerate(TOKENS):
            column_center_x = table_left + (column_index + 0.5) * cell_width
            label = self.jp_text(
                token,
                font_size=23,
                color=self.theme.foreground,
                weight="MEDIUM",
            )
            label.move_to([column_center_x, token_label_y, 0])
            connector = Line(
                label.get_bottom() + DOWN * 0.055,
                [
                    column_center_x,
                    raw_row_y + raw_cell_height / 2 + 0.04,
                    0,
                ],
                color=KEY_COLOR,
                stroke_width=2,
                stroke_opacity=0.48,
            )
            token_labels.add(label)
            token_connectors.add(connector)

        key_label = self.jp_text(
            "Key",
            font_size=28,
            color=KEY_COLOR,
            weight="MEDIUM",
        )
        key_label.move_to([table_center_x, 3.3, 0])

        query_word = self.jp_text(
            "Query",
            font_size=27,
            color=QUERY_COLOR,
            weight="MEDIUM",
        )
        query_value = self.jp_text(
            f"「{query_token}」",
            font_size=27,
            color=self.theme.foreground,
            weight="MEDIUM",
        )
        query_label = VGroup(query_word, query_value).arrange(RIGHT, buff=0.12)
        row_label_x = table_left - 1.15
        query_label.move_to([row_label_x, token_label_y, 0])

        raw_row_label = self.jp_text(
            "一致度",
            font_size=25,
            color=self.theme.foreground,
            weight="MEDIUM",
        )
        raw_row_label.move_to([row_label_x, raw_row_y, 0])
        ratio_row_label = self.jp_text(
            "参照割合",
            font_size=25,
            color=self.theme.foreground,
            weight="MEDIUM",
        )
        ratio_row_label.move_to([row_label_x, ratio_row_y, 0])

        row_connectors = VGroup(
            Line(
                raw_row_label.get_right() + RIGHT * 0.06,
                [table_left - 0.04, raw_row_y, 0],
                color=QUERY_COLOR,
                stroke_width=2,
                stroke_opacity=0.48,
            ),
            Line(
                ratio_row_label.get_right() + RIGHT * 0.06,
                [table_left - 0.04, ratio_row_y, 0],
                color=QUERY_COLOR,
                stroke_width=2,
                stroke_opacity=0.48,
            ),
        )

        softmax_card = RoundedRectangle(
            width=2.15,
            height=0.56,
            corner_radius=0.16,
            stroke_color=QUERY_COLOR,
            stroke_width=1.8,
            stroke_opacity=0.38,
            fill_color=QUERY_CARD_FILL,
            fill_opacity=0.94,
        )
        softmax_card.move_to([table_center_x, -0.05, 0])
        softmax_label = self.jp_text(
            "Softmax",
            font_size=25,
            color=QUERY_COLOR,
            weight="MEDIUM",
        )
        softmax_label.move_to(softmax_card)

        transformation_arrows = VGroup(
            Arrow(
                [table_center_x, raw_row_y - raw_cell_height / 2 - 0.04, 0],
                [table_center_x, softmax_card.get_top()[1] + 0.05, 0],
                buff=0,
                color=QUERY_COLOR,
                stroke_width=2.7,
                stroke_opacity=0.7,
                max_tip_length_to_length_ratio=0.2,
            ),
            Arrow(
                [table_center_x, softmax_card.get_bottom()[1] - 0.05, 0],
                [
                    table_center_x,
                    ratio_row_y + ratio_cell_height / 2 + 0.05,
                    0,
                ],
                buff=0,
                color=QUERY_COLOR,
                stroke_width=2.7,
                stroke_opacity=0.7,
                max_tip_length_to_length_ratio=0.16,
            ),
        )

        total_line_y = -2.05
        total_line = Line(
            [table_left, total_line_y, 0],
            [table_right, total_line_y, 0],
            color=QUERY_COLOR,
            stroke_width=2.5,
        )
        total_ticks = VGroup(
            Line(
                [table_left, total_line_y - 0.13, 0],
                [table_left, total_line_y + 0.13, 0],
                color=QUERY_COLOR,
                stroke_width=2.5,
            ),
            Line(
                [table_right, total_line_y - 0.13, 0],
                [table_right, total_line_y + 0.13, 0],
                color=QUERY_COLOR,
                stroke_width=2.5,
            ),
        )
        total_label = self.jp_text(
            f"合計 = {sum(reference_ratios):.2f}",
            font_size=25,
            color=self.theme.foreground,
            weight="MEDIUM",
        )
        total_label.next_to(total_line, DOWN, buff=0.18)

        self.add(
            raw_cells,
            ratio_cells,
            token_connectors,
            row_connectors,
            transformation_arrows,
            softmax_card,
            total_line,
            total_ticks,
            raw_values,
            ratio_values,
            token_labels,
            key_label,
            query_label,
            raw_row_label,
            ratio_row_label,
            softmax_label,
            total_label,
        )


class WeightedValueCollectionFigure(LightScene):
    """Value vectors gathered using one Query's reference ratios."""

    def construct(self) -> None:
        query_token = "それ"
        query_index = TOKENS.index(query_token)
        raw_scores = ATTENTION_SCORES[query_index]
        stabilized_exponentials = tuple(math.exp(score - max(raw_scores)) for score in raw_scores)
        exponential_sum = sum(stabilized_exponentials)
        reference_ratios = tuple(value / exponential_sum for value in stabilized_exponentials)
        maximum_ratio = max(reference_ratios)

        header_y = 2.97
        value_header = self.jp_text(
            "Value",
            font_size=24,
            color=VALUE_COLOR,
            weight="MEDIUM",
        ).move_to([-4.25, header_y, 0])
        ratio_header = self.jp_text(
            "参照割合",
            font_size=23,
            color=QUERY_COLOR,
            weight="MEDIUM",
        ).move_to([-2.15, header_y, 0])
        weighted_value_header = self.jp_text(
            "重み付きValue",
            font_size=24,
            color=VALUE_COLOR,
            weight="MEDIUM",
        ).move_to([1.75, header_y, 0])

        row_top = 2.55
        row_spacing = 0.66
        token_right_x = -5.72
        original_vector_start_x = -5.28
        original_vector_end_x = -4.42
        original_vector_label_x = -3.85
        multiply_x = -3.15
        ratio_x = -2.15
        transformation_start_x = -1.62
        transformation_end_x = -1.17
        weighted_vector_start_x = -0.72
        weighted_vector_max_length = 2.72
        weighted_vector_label_x = 3.35

        row_separators = VGroup()
        token_labels = VGroup()
        original_vectors = VGroup()
        original_vector_labels = VGroup()
        multiplication_symbols = VGroup()
        ratio_cards = VGroup()
        ratio_labels = VGroup()
        transformation_arrows = VGroup()
        weighted_vectors = VGroup()
        weighted_vector_labels = VGroup()

        for row_index, (token, ratio) in enumerate(zip(TOKENS, reference_ratios, strict=True)):
            row_y = row_top - row_index * row_spacing
            token_label = self.jp_text(
                token,
                font_size=22,
                color=self.theme.foreground,
                weight="MEDIUM",
            )
            token_label.move_to([token_right_x, row_y, 0])
            token_label.align_to([token_right_x, row_y, 0], RIGHT)

            original_vector = Arrow(
                [original_vector_start_x, row_y, 0],
                [original_vector_end_x, row_y, 0],
                buff=0,
                color=VALUE_COLOR,
                stroke_width=4,
                stroke_opacity=0.78,
                max_tip_length_to_length_ratio=0.19,
            )
            original_vector_label = MathTex(
                rf"\boldsymbol{{v}}_{{{row_index + 1}}}",
                font_size=28,
                color=VALUE_COLOR,
            )
            original_vector_label.move_to([original_vector_label_x, row_y, 0])

            multiplication_symbol = MathTex(
                r"\times",
                font_size=29,
                color=self.theme.muted,
            ).move_to([multiply_x, row_y, 0])

            ratio_strength = ratio / maximum_ratio
            ratio_fill = interpolate_color(
                QUERY_CARD_FILL,
                SCORE_HIGH_FILL,
                ratio_strength,
            )
            ratio_card = RoundedRectangle(
                width=0.82,
                height=0.43,
                corner_radius=0.1,
                stroke_width=0,
                fill_color=ratio_fill,
                fill_opacity=1,
            ).move_to([ratio_x, row_y, 0])
            ratio_label = self.jp_text(
                f"{ratio:.2f}",
                font_size=20,
                color=self.theme.foreground,
                weight="MEDIUM",
            )
            ratio_label.move_to(ratio_card)

            transformation_arrow = Arrow(
                [transformation_start_x, row_y, 0],
                [transformation_end_x, row_y, 0],
                buff=0,
                color=CONNECTOR_COLOR,
                stroke_width=2.3,
                stroke_opacity=0.62,
                max_tip_length_to_length_ratio=0.24,
            )

            weighted_vector_length = max(
                0.16,
                weighted_vector_max_length * ratio_strength,
            )
            weighted_vector = Arrow(
                [weighted_vector_start_x, row_y, 0],
                [weighted_vector_start_x + weighted_vector_length, row_y, 0],
                buff=0,
                color=VALUE_COLOR,
                stroke_width=2.4 + 3.8 * ratio_strength,
                stroke_opacity=0.32 + 0.64 * ratio_strength,
                max_tip_length_to_length_ratio=0.28,
            )
            weighted_vector_label = MathTex(
                rf"{ratio:.2f}\,\boldsymbol{{v}}_{{{row_index + 1}}}",
                font_size=25,
                color=interpolate_color(
                    self.theme.muted,
                    VALUE_COLOR,
                    0.35 + 0.65 * ratio_strength,
                ),
            )
            weighted_vector_label.move_to([weighted_vector_label_x, row_y, 0])

            if row_index < len(TOKENS) - 1:
                separator_y = row_y - row_spacing / 2
                row_separators.add(
                    Line(
                        [-6.38, separator_y, 0],
                        [4.6, separator_y, 0],
                        color=self.theme.muted,
                        stroke_width=1,
                        stroke_opacity=0.1,
                    )
                )

            token_labels.add(token_label)
            original_vectors.add(original_vector)
            original_vector_labels.add(original_vector_label)
            multiplication_symbols.add(multiplication_symbol)
            ratio_cards.add(ratio_card)
            ratio_labels.add(ratio_label)
            transformation_arrows.add(transformation_arrow)
            weighted_vectors.add(weighted_vector)
            weighted_vector_labels.add(weighted_vector_label)

        bracket_x = 4.78
        bracket_top_y = row_top + 0.27
        bracket_bottom_y = row_top - (len(TOKENS) - 1) * row_spacing - 0.27
        collection_bracket = VGroup(
            Line(
                [bracket_x - 0.24, bracket_top_y, 0],
                [bracket_x, bracket_top_y, 0],
                color=VALUE_COLOR,
                stroke_width=2.4,
                stroke_opacity=0.45,
            ),
            Line(
                [bracket_x, bracket_top_y, 0],
                [bracket_x, bracket_bottom_y, 0],
                color=VALUE_COLOR,
                stroke_width=2.4,
                stroke_opacity=0.45,
            ),
            Line(
                [bracket_x - 0.24, bracket_bottom_y, 0],
                [bracket_x, bracket_bottom_y, 0],
                color=VALUE_COLOR,
                stroke_width=2.4,
                stroke_opacity=0.45,
            ),
        )
        collection_label = VGroup(
            self.jp_text(
                "集めた",
                font_size=21,
                color=self.theme.foreground,
                weight="MEDIUM",
            ),
            self.jp_text(
                "情報",
                font_size=21,
                color=VALUE_COLOR,
                weight="MEDIUM",
            ),
        ).arrange(DOWN, buff=0.05)
        collection_label.move_to([5.65, 0.23, 0])

        self.add(
            row_separators,
            collection_bracket,
            original_vectors,
            transformation_arrows,
            weighted_vectors,
            ratio_cards,
            token_labels,
            original_vector_labels,
            multiplication_symbols,
            ratio_labels,
            weighted_vector_labels,
            value_header,
            ratio_header,
            weighted_value_header,
            collection_label,
        )
