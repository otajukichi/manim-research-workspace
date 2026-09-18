"""0918教材の入力検証、SVG追加、マス数、動物の配置規則を確認する。"""

import importlib.util
import json
from pathlib import Path

import pytest
from manim import DashedLine, Text, tempconfig

from manim_research import EDUCATION_THEME

BASE_DIR = Path(__file__).resolve().parent


def import_worksheet(name):
    spec = importlib.util.spec_from_file_location(name, BASE_DIR / name / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def picture(tmp_path):
    with tempconfig({"media_dir": str(tmp_path / "output")}):
        yield import_worksheet("picture_hiragana_write")


@pytest.fixture
def counting(tmp_path):
    with tempconfig({"media_dir": str(tmp_path / "output")}):
        yield import_worksheet("animal_counting_addition")


def set_content(module, data, tmp_path, monkeypatch):
    path = tmp_path / "worksheet.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(module, "CONTENT_FILE", path)


@pytest.mark.parametrize("name", ["animal_counting_addition", "picture_hiragana_write"])
def test_content_paths_do_not_depend_on_working_directory(name, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with tempconfig({}):
        module = import_worksheet(name)
        assert module.load_content()["problems"]
        assert module.CONTENT_FILE.parent == BASE_DIR / name / "json"


def test_picture_reports_missing_json(picture, tmp_path, monkeypatch):
    monkeypatch.setattr(picture, "CONTENT_FILE", tmp_path / "missing.json")
    with pytest.raises(FileNotFoundError, match="missing.json"):
        picture.load_content()


@pytest.mark.parametrize("problems", [None, {}, "invalid", [], [{}, {}]])
def test_picture_rejects_invalid_problem_lists(picture, problems, tmp_path, monkeypatch):
    data = picture.load_content()
    data["problems"] = problems
    set_content(picture, data, tmp_path, monkeypatch)
    with pytest.raises(ValueError, match="problems"):
        picture.load_content()


@pytest.mark.parametrize(
    ("problem", "message"),
    [
        (None, "1問目"),
        ({"answer": "くま"}, "icon"),
        ({"icon": "bear.svg"}, "answer"),
        ({"icon": "bear.svg", "answer": ""}, "answer"),
        ({"icon": "bear.svg", "answer": "  "}, "answer"),
        ({"icon": "bear.svg", "answer": 2}, "answer"),
        ({"icon": "", "answer": "くま"}, "icon"),
        ({"icon": None, "answer": "くま"}, "icon"),
    ],
)
def test_picture_rejects_invalid_problems(picture, problem, message, tmp_path, monkeypatch):
    data = picture.load_content()
    data["problems"][0] = problem
    set_content(picture, data, tmp_path, monkeypatch)
    with pytest.raises(ValueError, match=message):
        picture.load_content()


def test_picture_reports_missing_svg_name(picture, tmp_path, monkeypatch):
    data = picture.load_content()
    data["problems"][0]["icon"] = "missing.svg"
    set_content(picture, data, tmp_path, monkeypatch)
    with pytest.raises(FileNotFoundError, match="missing.svg"):
        picture.load_content()


def test_new_svg_needs_no_python_animal_registration(picture, tmp_path, monkeypatch):
    (tmp_path / "apple.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100">'
        '<rect width="1000" height="100" fill="#B64C24"/></svg>',
        encoding="utf-8",
    )
    data = picture.load_content()
    for problem in data["problems"]:
        problem["icon"] = "apple.svg"
    set_content(picture, data, tmp_path, monkeypatch)
    monkeypatch.setattr(picture, "SVG_DIR", tmp_path)
    assert picture.load_content() == data
    icon = picture.make_icon("apple.svg")
    assert icon.width / icon.height == pytest.approx(10)
    assert icon.width <= picture.ICON_MAX_WIDTH + 1e-6
    assert icon.height <= picture.ICON_MAX_HEIGHT + 1e-6


def test_picture_cells_are_blank_and_match_answers(picture):
    content = picture.load_content()
    for problem in content["problems"]:
        box, icon, cells = picture.make_problem(
            problem["icon"], problem["answer"], EDUCATION_THEME
        )
        assert len(cells) == len(problem["answer"])
        assert not any(isinstance(item, Text) for item in cells.get_family())
        assert icon.get_bottom()[1] > cells.get_top()[1]
        for item in (icon, cells):
            assert item.get_left()[0] >= box.get_left()[0]
            assert item.get_right()[0] <= box.get_right()[0]
            assert item.get_top()[1] <= box.get_top()[1]
            assert item.get_bottom()[1] >= box.get_bottom()[1]
        for cell in cells:
            assert isinstance(cell[1], DashedLine)
            assert isinstance(cell[2], DashedLine)
            assert cell[1].height == pytest.approx(0)
            assert cell[2].width == pytest.approx(0)


@pytest.mark.parametrize("icon_name", ["bear.svg", "rabbit.svg", "turtle.svg"])
def test_original_svg_outlines_keep_the_education_palette(picture, icon_name):
    icon = picture.make_icon(icon_name)
    for shape in icon.family_members_with_points():
        if shape.get_stroke_width() > 0 and shape.get_stroke_opacity() > 0:
            assert shape.get_stroke_color() == EDUCATION_THEME.foreground


def test_long_answer_keeps_all_cells_inside_problem_box(picture):
    answer = "あいうえおかきくけこ"
    box, _, cells = picture.make_problem("bear.svg", answer, EDUCATION_THEME)
    assert len(cells) == len(answer)
    assert cells.width < box.width


def test_picture_page_fits_a4(picture):
    scene = picture.PictureHiraganaWriteWorksheet()
    scene.setup()
    scene.construct()
    for item in scene.mobjects:
        assert item.get_left()[0] > -picture.A4_WIDTH / 2
        assert item.get_right()[0] < picture.A4_WIDTH / 2
        assert item.get_bottom()[1] > -picture.A4_HEIGHT / 2
        assert item.get_top()[1] < picture.A4_HEIGHT / 2
    title, subtitle, problems = scene.mobjects[:3]
    assert title.get_bottom()[1] > subtitle.get_top()[1]
    assert subtitle.get_bottom()[1] > problems.get_top()[1]


@pytest.mark.parametrize("animal", ["bear", "rabbit", "chick"])
@pytest.mark.parametrize("rows", [(1,), (2,), (3,), (2, 2), (3, 2), (3, 3)])
def test_counting_uses_at_most_three_columns_and_two_centered_rows(counting, animal, rows):
    group = counting.make_animal_group(animal, sum(rows), EDUCATION_THEME)
    assert tuple(len(row) for row in group) == rows
    assert group.width < counting.GROUP_BOX_WIDTH
    assert group.height < counting.GROUP_BOX_HEIGHT
    for row in group:
        assert row.get_center()[0] == pytest.approx(group.get_center()[0])
        assert len({round(icon.get_center()[1], 6) for icon in row}) == 1
    if len(group) == 2:
        assert group[0].get_bottom()[1] > group[1].get_top()[1]


@pytest.mark.parametrize("count", [7, 8, 100])
def test_counting_rejects_more_than_six_animals(counting, count, tmp_path, monkeypatch):
    with pytest.raises(ValueError, match="最大6"):
        counting.make_animal_group("bear", count, EDUCATION_THEME)
    data = counting.load_content()
    data["problems"][0]["left_count"] = count
    set_content(counting, data, tmp_path, monkeypatch)
    with pytest.raises(ValueError, match="最大6"):
        counting.load_content()
